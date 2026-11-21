"""Replication package triage: decide in minutes whether a package can run at all, before anyone spends a day on it.

Given a package (a directory, a .zip or .tar.gz, or a git URL with an optional commit), it reads the files and reports a verdict:

  runnable                  nothing found that stops an as-is run on this desk
  runnable-with-deviations  it can probably run, but only after changes a receipt must log (pinning versions, editing paths, ...)
  blocked                   something the desk cannot supply is missing (restricted data, proprietary software, a dead data link, ...)

Each verdict carries the findings behind it, with file:line evidence. Triage never executes package code: it reads text, and with
--check-links it sends HEAD/GET requests to the URLs the package names. It says nothing about whether a paper's results are correct;
it says whether the committed materials can be run here, and what a rerun would have to change.

Stdlib only (Python 3.10+), so a desk can run it on its own machine with no installs and nothing leaving its network.

usage: python triage.py PACKAGE [--commit SHA] [--have stata,matlab] [--check-links] [--max-hours 24] [--json OUT] [--md OUT]"""
from __future__ import annotations

import argparse
import ast
import concurrent.futures
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

FORMAT = "triage-verdict/1"
BLOCKER, DEVIATION, NOTE = "blocker", "deviation", "note"
TEXT_LIMIT = 2_000_000          # bytes read per file for scanning; larger files are inventoried, not read
SKIP_DIRS = {".git", "__MACOSX", "__pycache__", ".ipynb_checkpoints", "renv/library", "node_modules", ".venv", "venv"}

LANGUAGES = {  # extension -> language
    ".py": "python", ".ipynb": "python", ".r": "r", ".rmd": "r", ".qmd": "r", ".do": "stata", ".ado": "stata",
    ".m": "matlab", ".mlx": "matlab", ".jl": "julia", ".sas": "sas", ".nb": "mathematica", ".wl": "mathematica",
    ".gss": "gauss", ".prg": "eviews", ".sps": "spss", ".f90": "fortran", ".f": "fortran", ".cpp": "c++", ".c": "c",
    ".sh": "shell", ".mod": "dynare", ".gms": "gams",
}
PROPRIETARY = {"stata", "matlab", "sas", "mathematica", "gauss", "eviews", "spss", "gams"}
SYSTEM_PATH = re.compile(r"^(/etc|/proc|/dev|/sys|/usr|/bin|/tmp)/")
DYNARE_OUTPUTS = ("_results.mat", ".log", "_dynamic.m", "_static.m", "_set_auxiliary_variables.m", "_steadystate2.m")
EARTH_ENGINE = re.compile(r"\bee\.(?:ImageCollection|Image|FeatureCollection|Initialize|Geometry)\b|\bExport\.(?:table|image)\.")
TOOLBOX = re.compile(r"\b((?:[A-Z][A-Za-z]+ ){0,3}Toolbox)\b")
VERSION_LISTING = re.compile(r"Version\s+[\d.]+\s+\(R20\d\d[ab]\)")
DATA_EXT = {".csv", ".tsv", ".txt", ".dta", ".rds", ".rdata", ".rda", ".xlsx", ".xls", ".parquet", ".feather", ".json", ".sav",
            ".sas7bdat", ".mat", ".npy", ".npz", ".pkl", ".pickle", ".h5", ".hdf5", ".nc", ".shp", ".dbf", ".zip", ".gz", ".fst"}
DOC_NAMES = re.compile(r"(readme|read_me|data.?availability|instructions|replication|codebook)", re.I)

# Phrases that mark data the desk cannot obtain by downloading (tier "restricted") or can obtain after registering ("registration").
RESTRICTED = [r"confidential", r"restricted[- ]use", r"restricted access", r"proprietary", r"not (?:be )?publicly available",
              r"cannot be (?:shared|made available|redistributed|posted|provided|included)", r"(?:available )?upon request",
              r"data use agreement", r"\bDUA\b", r"non-?disclosure", r"\bFSRDC\b", r"\bRDC\b", r"research data cent(?:er|re)",
              r"\bWRDS\b", r"compustat", r"\bCRSP\b", r"bloomberg", r"refinitiv", r"datastream", r"\borbis\b", r"nielsen",
              r"purchased? (?:from|the)", r"licensed from", r"secure (?:data )?(?:enclave|environment|server)", r"must apply",
              r"apply for access", r"statistics (?:denmark|sweden|norway|netherlands)", r"administrative data"]
REGISTRATION = [r"\bIPUMS\b", r"\bICPSR\b", r"openicpsr", r"\bPSID\b", r"UK Data Service", r"\bDHS\b", r"kaggle",
                r"free (?:registration|account)", r"register (?:for|at|on)", r"requires? (?:a |an )?(?:free )?(?:login|account)"]
LICENCES = [("CC BY-NC", r"\bCC[- ]BY[- ]NC|non-?commercial"), ("CC BY", r"\bCC[- ]?BY\b|creative commons attribution"),
            ("CC0", r"\bCC0\b|public domain"), ("MIT", r"\bMIT licen[cs]e\b|^MIT License"), ("BSD", r"\bBSD\b"),
            ("GPL", r"\bGPL|GNU General Public"), ("Apache", r"Apache Licen[cs]e"), ("ODC", r"\bODbL\b|\bODC-BY\b")]
MASTER = re.compile(r"^(master|main|run_?all|runall|run|replicate\w*|reproduce\w*|make\w*|build|0+_?\w*)$", re.I)
URL = re.compile(r"https?://[^\s)\]>\"'<`]+")
PY_DIST = {"sklearn": "scikit-learn", "cv2": "opencv-python", "PIL": "pillow", "yaml": "pyyaml", "bs4": "beautifulsoup4",
           "skimage": "scikit-image", "dateutil": "python-dateutil", "Bio": "biopython", "attr": "attrs", "jwt": "pyjwt",
           "dotenv": "python-dotenv", "nilearn": "nilearn", "nibabel": "nibabel", "mpl_toolkits": "matplotlib",
           "google": "google-api-core", "pylab": "matplotlib", "linearmodels": "linearmodels", "pyfixest": "pyfixest"}


@dataclass
class Finding:
    code: str
    severity: str
    message: str
    evidence: list = field(default_factory=list)


@dataclass
class Ref:
    path: str      # the path as written, normalised to forward slashes
    file: str      # where it was found
    line: int
    lang: str


# ----------------------------------------------------------------------------------------------------------------- loading

def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_package(src: str, commit: str | None, work: Path) -> tuple[Path, dict]:
    """Return the package root and a description of where it came from. Archives are unpacked, URLs cloned, into `work`."""
    p = Path(src)
    if re.match(r"^(https?://|git@)", src):
        dest = work / "checkout"
        if commit:
            subprocess.run(["git", "init", "-q", str(dest)], check=True)
            subprocess.run(["git", "-C", str(dest), "fetch", "-q", "--depth", "1", src, commit], check=True)
            subprocess.run(["git", "-C", str(dest), "checkout", "-q", "FETCH_HEAD"], check=True)
        else:
            subprocess.run(["git", "clone", "-q", "--depth", "1", src, str(dest)], check=True)
        head = subprocess.run(["git", "-C", str(dest), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
        return dest, {"kind": "git", "url": src, "commit": head}
    if p.is_file() and zipfile.is_zipfile(p):
        dest = work / "unpacked"
        with zipfile.ZipFile(p) as z:
            for m in z.infolist():                       # refuse paths that would land outside dest
                target = (dest / m.filename).resolve()
                if not str(target).startswith(str(dest.resolve())):
                    raise ValueError(f"archive member escapes the package: {m.filename}")
            z.extractall(dest)
        return single_child(dest), {"kind": "zip", "path": str(p), "sha256": sha256_file(p)}
    if p.is_file() and tarfile.is_tarfile(p):
        dest = work / "unpacked"
        with tarfile.open(p) as t:
            kw = {"filter": "data"} if hasattr(tarfile, "data_filter") else {}
            for m in t.getmembers():
                if not str((dest / m.name).resolve()).startswith(str(dest.resolve())) or m.issym() or m.islnk():
                    raise ValueError(f"archive member escapes the package or is a link: {m.name}")
            t.extractall(dest, **kw)
        return single_child(dest), {"kind": "tar", "path": str(p), "sha256": sha256_file(p)}
    if p.is_dir():
        info = {"kind": "directory", "path": str(p)}
        r = subprocess.run(["git", "-C", str(p), "rev-parse", "HEAD"], capture_output=True, text=True)
        if r.returncode == 0:
            info["commit"] = r.stdout.strip()
        return p, info
    raise FileNotFoundError(f"not a directory, archive or git URL: {src}")


def single_child(d: Path) -> Path:
    """Archives often wrap everything in one top-level folder; triage that folder."""
    kids = [k for k in d.iterdir() if k.name != "__MACOSX"]
    return kids[0] if len(kids) == 1 and kids[0].is_dir() else d


def walk(root: Path) -> list[Path]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).relative_to(root).as_posix()
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and f"{rel}/{d}".lstrip("./") not in SKIP_DIRS]
        out += [Path(dirpath) / f for f in filenames]
    return sorted(out)


def read_text(p: Path) -> str | None:
    try:
        if p.stat().st_size > TEXT_LIMIT:
            return None
        b = p.read_bytes()
    except OSError:
        return None
    if b"\x00" in b[:4096]:
        return None
    for enc in ("utf-8", "latin-1"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    return None


def notebook_source(text: str) -> tuple[str, str]:
    """Code cells of a notebook joined as one source, and the kernel language."""
    try:
        nb = json.loads(text)
    except json.JSONDecodeError:
        return "", "python"
    lang = (nb.get("metadata", {}).get("kernelspec", {}).get("language") or "python").lower()
    cells = [c for c in nb.get("cells", []) if c.get("cell_type") == "code"]
    src = "\n".join("".join(c.get("source", [])) if isinstance(c.get("source"), list) else c.get("source", "") for c in cells)
    return src, ("r" if lang == "r" else "python")


# ---------------------------------------------------------------------------------------------------------- path extraction

STR = re.compile(r"\"([^\"\n]*)\"|'([^'\n]*)'")
STATA_READ = re.compile(r"^\s*(?:quietly\s+|qui\s+|capture\s+|cap\s+)*(use|merge|append|joinby|cross|import\s+delimited|import\s+excel|"
                        r"insheet|infile|infix|do|run|include)\b(.*)$")
STATA_WRITE = re.compile(r"^\s*(?:quietly\s+|qui\s+|capture\s+|cap\s+)*(save|saveold|export\s+delimited|export\s+excel|outsheet|"
                         r"esttab|estout|outreg2|graph\s+export|log\s+using|estimates\s+save|putexcel\s+set|texsave|file\s+open)\b(.*)$")
R_READ = re.compile(r"\b(read\.csv2?|read\.table|read\.delim|fread|read_csv2?|read_tsv|read_delim|read_dta|read_sav|read_sas|"
                    r"read_excel|read_xlsx?|readRDS|read_rds|load|read_parquet|read_feather|read_fst|st_read|source|readLines)\s*\(([^)]*)")
R_WRITE = re.compile(r"\b(write\.csv2?|write\.table|fwrite|write_csv|write_tsv|saveRDS|write_rds|save|ggsave|write_dta|"
                     r"write_parquet|write_fst|pdf|png|jpeg|sink|writeLines|stargazer|etable|modelsummary|texreg)\s*\(([^)]*)")
PY_READ = re.compile(r"\b(read_csv|read_table|read_stata|read_excel|read_parquet|read_feather|read_pickle|read_json|read_sas|"
                     r"read_spss|read_hdf|np\.load|numpy\.load|loadtxt|genfromtxt|loadmat|load_workbook|imread|nib\.load|"
                     r"xr\.open_dataset|open_dataset)\s*\(([^)]*)")
PY_WRITE = re.compile(r"\b(to_csv|to_parquet|to_stata|to_excel|to_pickle|to_json|to_latex|to_feather|np\.save|numpy\.save|savetxt|"
                      r"np\.savez(?:_compressed)?|savefig|savemat|imsave|to_filename)\s*\(([^)]*)")
PY_OPEN = re.compile(r"\bopen\s*\(([^)]*)\)")
M_READ = re.compile(r"\b(load|readtable|readmatrix|csvread|xlsread|dlmread|importdata|readcell|textscan|fopen)\s*\(([^)]*)")
M_WRITE = re.compile(r"\b(save|writetable|writematrix|csvwrite|xlswrite|saveas|exportgraphics|print)\s*\(([^)]*)")
JL_READ = re.compile(r"\b(CSV\.read|CSV\.File|load|readdlm|DataFrame\(CSV\.File|read_dta|readstat|jldopen|include)\s*\(([^)]*)")
JL_WRITE = re.compile(r"\b(CSV\.write|save|writedlm|savefig|jldsave)\s*\(([^)]*)")
COMMENT = {"python": "#", "r": "#", "stata": ("*", "//"), "matlab": "%", "julia": "#", "shell": "#", "sas": "*"}


def literals(s: str) -> list[str]:
    return [a or b for a, b in STR.findall(s)]


def pathlike(s: str) -> bool:
    return bool(s) and ("/" in s or "\\" in s or "." in Path(s.replace("\\", "/")).name) and not s.startswith(("%", "{"))


def last_path_literal(arg: str) -> str | None:
    lits = [x for x in literals(arg) if pathlike(x)]
    return lits[-1] if lits else None


JOIN = re.compile(r"\b(?:os\.path\.join|path\.join|file\.path|fullfile|joinpath|here::here|here)\s*\(")
ASSIGN = re.compile(r"^\s*([A-Za-z_][\w.]*)\s*(?:=|<-)\s*(.+)$")


def path_of(arg: str, env: dict) -> str | None:
    """The path an argument names: joined literals of a join call, else the last path literal, else a variable set earlier."""
    outside = STR.sub("", arg)
    if literals(arg) and re.search(r"\bpaste0?\s*\(|sprintf\s*\(|strcat\s*\(|\+|\[|\bf[\"']", arg) and re.search(r"[A-Za-z_]\w*", re.sub(r"\b(paste0?|sprintf|strcat|sep|f)\b", "", outside)):
        return "{concat}" + (last_path_literal(arg) or "")
    if JOIN.search(arg):
        lits = [x for x in literals(arg.split(")")[0] if ")" in arg else arg)]
        if lits and pathlike(lits[-1]):
            return "/".join(lits)
    lit = last_path_literal(arg)
    if lit:
        return lit
    m = re.match(r"\s*(?:file\s*=\s*|fname\s*=\s*)?([A-Za-z_][\w.]*)\s*(?:,|$)", arg)
    return env.get(m.group(1)) if m else None


def stata_target(cmd: str, rest: str) -> str | None:
    rest = rest.split("//")[0]
    m = re.search(r"\busing\s+(\"[^\"]+\"|`\"[^\"]+\"'|[^\s,]+)", rest)
    if m:
        tok = m.group(1)
    elif cmd.lower().split()[0] in ("use", "do", "run", "include", "save", "saveold", "insheet", "outsheet") or cmd.lower().startswith("import"):
        m = re.match(r"\s*(\"[^\"]+\"|`\"[^\"]+\"'|[^\s,]+)", rest)
        tok = m.group(1) if m else None
    else:
        tok = None
    if not tok:
        return None
    if "`" in tok:                                   # a local macro: the file name is only known at run time
        return "{macro}" + tok.strip("\"")
    tok = tok.strip("`'\"")
    base = tok.replace("\\", "/").rsplit("/", 1)[-1]
    if "." not in base:
        c = cmd.lower().split()[0]
        tok += {"use": ".dta", "merge": ".dta", "append": ".dta", "joinby": ".dta", "cross": ".dta", "save": ".dta",
                "saveold": ".dta", "do": ".do", "run": ".do", "include": ".do", "estimates": ".ster"}.get(c, "")
    return tok


def extract_refs(path: Path, rel: str, text: str, lang: str) -> tuple[list[Ref], list[Ref], list[tuple[str, int, str]]]:
    """Reads, writes and every non-comment code line (for later line checks) of one code file."""
    reads, writes, lines = [], [], []
    env: dict[str, str] = {}
    cm = COMMENT.get(lang, "#")
    blank = lambda m: "\n" * m.group(0).count("\n")  # noqa: E731  keep line numbers
    if lang == "stata":
        text = re.sub(r"/\*.*?\*/", blank, text, flags=re.S)
    elif lang == "matlab":
        text = re.sub(r"^\s*%\{.*?^\s*%\}", blank, text, flags=re.S | re.M)
    for i, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith(cm if isinstance(cm, tuple) else (cm,)):
            continue
        lines.append((rel, i, raw))
        if lang == "stata":
            for rx, out in ((STATA_READ, reads), (STATA_WRITE, writes)):
                m = rx.match(raw)
                if m:
                    t = stata_target(m.group(1), m.group(2))
                    if t:
                        out.append(Ref(t, rel, i, lang))
            continue
        table = {"python": ((PY_READ, reads), (PY_WRITE, writes)), "r": ((R_READ, reads), (R_WRITE, writes)),
                 "matlab": ((M_READ, reads), (M_WRITE, writes)), "julia": ((JL_READ, reads), (JL_WRITE, writes))}.get(lang, ())
        if lang == "matlab":
            m = re.match(r"^\s*(save|load)\s+([^\s(=;,'][^\s;,]*)", raw)    # command syntax: save targets.mat x y
            if m:
                f = m.group(2) if "." in m.group(2) else m.group(2) + ".mat"
                (writes if m.group(1) == "save" else reads).append(Ref(f, rel, i, lang))
        a = ASSIGN.match(raw)
        if a and not re.match(r"\s*(if|while|for|elif|return)\b", raw):
            v = path_of(a.group(2), env) if (JOIN.search(a.group(2)) or re.match(r"\s*[\"']", a.group(2))) else None
            if v:
                env[a.group(1)] = v
        for rx, out in table:
            for m in rx.finditer(raw):
                t = path_of(m.group(2), env)
                if t:
                    out.append(Ref(t, rel, i, lang))
        if lang == "python":
            for m in PY_OPEN.finditer(raw):
                lits = literals(m.group(1))
                if lits and pathlike(lits[0]):
                    mode = lits[1] if len(lits) > 1 else "r"
                    (writes if any(c in mode for c in "wax") else reads).append(Ref(lits[0], rel, i, lang))
    return reads, writes, lines


def basename(p: str) -> str:
    return p.replace("\\", "/").rstrip("/").rsplit("/", 1)[-1].lower()


def unresolved(p: str) -> bool:
    return any(c in basename(p) for c in "*?{}$`%") or basename(p) in ("", ".", "..")


# ------------------------------------------------------------------------------------------------------------- dependencies

# APIs that current releases no longer have. A run either installs versions old enough (which an unpinned package does not name)
# or edits the code, and either is a deviation. Each entry: (language, pattern, what it is, where it went).
REMOVED_APIS = [
    ("python", r"\bsklearn\.cross_validation\b", "sklearn.cross_validation", "removed in scikit-learn 0.20"),
    ("python", r"\bsklearn\.grid_search\b", "sklearn.grid_search", "removed in scikit-learn 0.20"),
    ("python", r"\bsklearn\.learning_curve\b", "sklearn.learning_curve", "removed in scikit-learn 0.20"),
    ("python", r"\bsklearn\.externals\.(joblib|six)\b", "sklearn.externals.joblib / six", "removed in scikit-learn 0.23"),
    ("python", r"\bsklearn\.datasets\.base\b", "sklearn.datasets.base", "removed in scikit-learn 0.24"),
    ("python", r"\b(?:np|numpy)\.(?:int|float|bool|object|str|complex|long|unicode)\b(?![\w(]*\d)", "NumPy scalar aliases (np.int, np.float, ...)",
     "removed in NumPy 1.24"),
    ("python", r"\.ix\[", "pandas .ix indexer", "removed in pandas 1.0"),
    ("python", r"\bpd\.(?:rolling_\w+|ewma|ols|datetools|stats)\b|\bpandas\.io\.data\b", "old pandas top-level functions",
     "removed in pandas 0.20 to 0.23"),
    ("python", r"\bscipy\.misc\.(?:imread|imsave|imresize|comb|factorial|logsumexp)\b|\bfrom scipy\.misc import (?:imread|imsave|imresize|comb|factorial|logsumexp)",
     "scipy.misc image and special functions", "removed in SciPy 1.0 to 1.3"),
    ("python", r"^\s*(?:import|from)\s+distutils\b", "distutils", "removed from the standard library in Python 3.12"),
    ("python", r"^\s*(?:import|from)\s+imp\b", "imp", "removed from the standard library in Python 3.12"),
    ("python", r"\bcollections\.(?:Mapping|MutableMapping|Sequence|Iterable|Callable)\b|from collections import (?:Mapping|MutableMapping|Sequence|Iterable|Callable)\b",
     "collections ABC aliases", "removed in Python 3.10 (moved to collections.abc)"),
    ("python", r"\.get_data\(\)", "nibabel get_data()", "removed in nibabel 5.0"),
    ("python", r"\.get_affine\(\)|\.get_header\(\)", "nibabel get_affine() / get_header()", "deprecated, removed in later nibabel"),
]
PY2 = re.compile(r"^\s*print\s+[^\s(=]|^\s*except\s+[\w.]+\s*,\s*\w+\s*:|^\s*exec\s+\"|\bur\"|^\s*raise\s+\w+\s*,", re.M)
FETCH = {
    "python": re.compile(r"\b(fetch_\w+|urlretrieve|urlopen|requests\.get|wget\.download|gdown\.download|load_dataset|hf_hub_download|"
                         r"snapshot_download|pdr\.DataReader|DataReader|yf\.download)\s*\("),
    "r": re.compile(r"\b(download\.file|curl_download|httr::GET|GET|get_acs|get_decennial|WDI|fredr|getSymbols|Quandl|pins::pin_get)\s*\("),
    "stata": re.compile(r"^\s*(?:qui(?:etly)?\s+|cap(?:ture)?\s+)*(copy\s+\"?https?|use\s+\"?https?|webuse|wbopendata|freduse|import\s+fred)\b"),
    "matlab": re.compile(r"\b(websave|urlread|webread|urlwrite)\s*\("),
    "julia": re.compile(r"\b(download|Downloads\.download)\s*\("),
}

def py_imports(text: str) -> set[str]:
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return {m for m in re.findall(r"^\s*(?:import|from)\s+([A-Za-z_]\w*)", text, re.M)}
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            out |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            out.add(node.module.split(".")[0])
    return out


def norm_dist(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def parse_requirements(text: str) -> list[tuple[str, bool, str]]:
    """(distribution, pinned, line) for each requirement line. Pinned means == / === or a direct reference with a hash or commit."""
    out = []
    for raw in text.splitlines():
        line = raw.split("#")[0].strip()
        if not line or line.startswith(("-", "--")):
            continue
        m = re.match(r"([A-Za-z0-9][A-Za-z0-9._-]*)", line)
        if m:
            out.append((norm_dist(m.group(1)), bool(re.search(r"===?\s*[\w.]+|@\s*\S+", line)) and ">" not in line and "<" not in line, raw.strip()))
    return out


def parse_conda(text: str) -> list[tuple[str, bool, str]]:
    out, in_deps = [], False
    for raw in text.splitlines():
        if re.match(r"^dependencies\s*:", raw):
            in_deps = True
            continue
        if in_deps and re.match(r"^\S", raw):
            in_deps = False
        m = re.match(r"^\s*-\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*(.*)$", raw) if in_deps else None
        if m and m.group(1) != "pip":
            out.append((norm_dist(m.group(1)), bool(re.match(r"=+\s*[\w.]", m.group(2).strip())), raw.strip()))
        m = re.match(r"^\s+-\s+([A-Za-z0-9][A-Za-z0-9._-]*)(.*)$", raw) if in_deps and raw.startswith("    ") else None
        if m and m.group(1) != "pip":
            out += parse_requirements(m.group(1) + m.group(2))
    return out


# ------------------------------------------------------------------------------------------------------------------- links

def check_link(url: str, timeout: float) -> dict:
    headers = {"User-Agent": "replication-triage/1 (link check)"}
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return {"url": url, "status": r.status, "ok": r.status < 400, "final_url": r.geturl()}
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (400, 403, 405, 501):
                continue
            return {"url": url, "status": e.code, "ok": False, "error": f"HTTP {e.code}"}
        except Exception as e:  # noqa: BLE001  DNS failure, refused connection, timeout, TLS: the link could not be fetched
            return {"url": url, "status": None, "ok": False, "error": f"{type(e).__name__}: {e}"[:200]}
    return {"url": url, "status": None, "ok": False, "error": "no response"}


def clean_url(u: str) -> str:
    return u.rstrip(".,;:!?*_")


# ------------------------------------------------------------------------------------------------------------------ triage

def paragraphs(text: str) -> list[str]:
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def has_any(patterns: list[str], text: str) -> list[str]:
    return [m.group(0) for p in patterns for m in [re.search(p, text, re.I | re.M)] if m]


def triage(root: Path, have: set[str], check_links: bool = False, max_hours: float = 24.0, link_timeout: float = 15.0) -> dict:
    t0 = time.monotonic()
    findings: list[Finding] = []
    add = lambda *a, **k: findings.append(Finding(*a, **k))  # noqa: E731

    files = walk(root)
    rels = {f: f.relative_to(root).as_posix() for f in files}
    by_base: dict[str, list[str]] = {}
    for f, r in rels.items():
        by_base.setdefault(f.name.lower(), []).append(r)
    total_bytes = sum(f.stat().st_size for f in files)

    # ---- inventory and languages
    code: dict[str, str] = {}               # rel -> language
    texts: dict[str, str] = {}
    for f, r in rels.items():
        ext = f.suffix.lower()
        lang = LANGUAGES.get(ext)
        if lang:
            t = read_text(f)
            if t is None:
                if ext == ".mlx":
                    code[r] = lang
                continue
            if ext == ".ipynb":
                t, lang = notebook_source(t)
            code[r], texts[r] = lang, t
    for f, r in rels.items():
        if f.suffix.lower() == ".js" and (t := read_text(f)) and EARTH_ENGINE.search(t):
            code[r], texts[r] = "earthengine", t
    languages = sorted(set(code.values()))

    # ---- documentation
    docs = {r: t for f, r in rels.items() if DOC_NAMES.search(f.name) and f.suffix.lower() in (".md", ".txt", ".rst", "")
            and (t := read_text(f)) is not None}
    docs.update({r: t for f, r in rels.items() if f.suffix.lower() == ".md" and r not in docs and (t := read_text(f)) is not None})
    readme_any = [r for f, r in rels.items() if re.match(r"read_?me", f.name, re.I)]
    doc_text = "\n\n".join(docs.values())
    if not readme_any:
        add("NO_README", DEVIATION, "No README. The run order, software and data sources must be inferred, and each inference is a "
            "deviation a receipt has to log.")
    elif not any(r in docs for r in readme_any):
        add("README_NOT_TEXT", NOTE, f"The README is not plain text ({', '.join(readme_any)}). Triage cannot read it, so the data "
            "availability statement, licence and run time below were not checked against it. Read it by hand.", readme_any)

    # ---- no code
    if not code:
        add("NO_CODE", BLOCKER, "No code files were found, so there is nothing to run. The package may hold data or results only.")

    # ---- software
    for lang in languages:
        version = None
        if lang == "stata":
            vs = [(r, i, m.group(1)) for r, l in code.items() if l == "stata" for i, line in enumerate(texts.get(r, "").splitlines(), 1)
                  for m in [re.match(r"^\s*version\s+(\d+(?:\.\d+)?)", line)] if m]
            if vs:
                version = sorted({v for _, _, v in vs})
            else:
                add("STATA_VERSION_MISSING", DEVIATION, "No `version` statement in any do-file. Stata's behaviour depends on the "
                    "version, so a rerun must choose one and log it.")
        if lang in PROPRIETARY:
            used = sorted(r for r, l in code.items() if l == lang)
            if lang in have:
                add("SOFTWARE_REQUIRED", NOTE, f"Requires {lang.upper() if lang in ('sas', 'spss') else lang.title()}"
                    + (f" (version {', '.join(version)} named in code)" if version else "") + "; the desk says it has it.", used[:5])
            else:
                add("PROPRIETARY_SOFTWARE", BLOCKER, f"Requires {lang.title()}, which is proprietary and not declared available on this "
                    f"desk. Rerun triage with --have {lang} if a licensed copy is available.", used[:5])

    # ---- dependencies: Python
    py_files = [r for r, l in code.items() if l == "python"]
    py_pinned = True
    py2 = []
    for r in py_files:
        t = texts.get(r, "")
        try:
            ast.parse(t)
        except (SyntaxError, ValueError):
            m = PY2.search(t)
            py2.append(f"{r}:{t[:m.start()].count(chr(10)) + 1}" if m else r)
    if py2:
        add("PYTHON2_SYNTAX", DEVIATION, f"{len(py2)} Python files do not parse as Python 3, most likely Python 2. A rerun needs a Python 2.7 "
            "interpreter (end of life since 2020) or a port, and either is a logged deviation.", py2[:10])
    if py_files:
        spec_files = [r for f, r in rels.items() if re.match(r"requirements.*\.txt$|environment\.ya?ml$|pyproject\.toml$|setup\.(py|cfg)$|"
                                                             r"Pipfile(\.lock)?$|poetry\.lock$|uv\.lock$|pdm\.lock$|conda-lock\.ya?ml$", f.name)]
        locked = [r for r in spec_files if re.search(r"(\.lock|conda-lock\.ya?ml)$", r)]
        reqs: list[tuple[str, bool, str]] = []
        for r in spec_files:
            t = read_text(root / r) or ""
            if r.endswith(".txt"):
                reqs += parse_requirements(t)
            elif re.search(r"environment\.ya?ml$", r):
                reqs += parse_conda(t)
            elif r.endswith("pyproject.toml"):
                reqs += parse_requirements("\n".join(re.findall(r"^\s*\"([^\"]+)\",?\s*$", t, re.M)))
            elif r.endswith("Pipfile"):
                reqs += [(norm_dist(n), v.strip().strip('"') not in ("*", ""), f"{n} = {v}") for n, v in re.findall(r"^([A-Za-z0-9._-]+)\s*=\s*(.+)$", t, re.M)]
        local = {Path(r).stem for r in py_files} | {p for r in rels.values() for p in r.split("/")[:-1]}
        third = set()
        for r in py_files:
            third |= {m for m in py_imports(texts.get(r, "")) if m not in sys.stdlib_module_names and m not in local and m != "__future__"}
        declared = {d for d, _, _ in reqs}
        undeclared = sorted(m for m in third if norm_dist(PY_DIST.get(m, m)) not in declared and norm_dist(m) not in declared)
        if not spec_files:
            py_pinned = False
        if not spec_files and third:
            add("NO_DEPENDENCY_SPEC", DEVIATION, f"Python code imports {', '.join(sorted(third))} but the package has no requirements "
                "file, environment file or lockfile. A rerun must choose versions and log them.", py_files[:5])
        elif spec_files:
            unpinned = [line for _, pinned, line in reqs if not pinned]
            py_pinned = bool(locked) or not unpinned
            if unpinned and not locked:
                add("UNPINNED_DEPENDENCIES", DEVIATION, f"Python requirements without an exact version: {'; '.join(unpinned[:10])}. "
                    "A rerun installs whatever is current and must log the versions it got.", spec_files)
            if undeclared and not locked:
                add("UNDECLARED_DEPENDENCIES", DEVIATION, f"Python code imports {', '.join(undeclared)}, which no dependency file names.",
                    py_files[:5])

    # ---- dependencies: R
    r_files = [r for r, l in code.items() if l == "r"]
    if r_files:
        pkgs, ev = set(), []
        for r in r_files:
            for i, line in enumerate(texts.get(r, "").splitlines(), 1):
                for m in re.finditer(r"\b(?:library|require|requireNamespace)\s*\(\s*[\"']?([A-Za-z][A-Za-z0-9.]*)", line):
                    pkgs.add(m.group(1)); ev.append(f"{r}:{i}")
                for m in re.finditer(r"\b([A-Za-z][A-Za-z0-9.]*)::", line):
                    pkgs.add(m.group(1))
                for m in re.finditer(r"p_load\s*\(([^)]*)\)", line):
                    pkgs |= set(re.findall(r"[A-Za-z][A-Za-z0-9.]*", m.group(1))) - {"char", "install", "update", "TRUE", "FALSE"}
        pkgs -= {"base", "stats", "utils", "methods", "graphics", "grDevices", "datasets", "parallel", "grid", "tools", "splines", "compiler", "stats4", "tcltk"}
        lock = [r for f, r in rels.items() if f.name == "renv.lock"]
        if lock:
            try:
                locked_pkgs = set(json.loads(read_text(root / lock[0]) or "{}").get("Packages", {}))
            except json.JSONDecodeError:
                locked_pkgs = set()
                add("BAD_LOCKFILE", DEVIATION, f"{lock[0]} is not valid JSON, so the R versions it pins cannot be restored.", lock)
            missing = sorted(pkgs - locked_pkgs)
            if missing and locked_pkgs:
                add("UNDECLARED_DEPENDENCIES", DEVIATION, f"R code loads {', '.join(missing)}, which {lock[0]} does not pin.", lock)
        elif pkgs:
            add("UNPINNED_DEPENDENCIES", DEVIATION, f"R code loads {', '.join(sorted(pkgs))} with no renv.lock. A rerun installs current "
                "CRAN versions and must log them.", ev[:5])

    # ---- dependencies: Stata
    st_files = [r for r, l in code.items() if l == "stata"]
    if st_files:
        installs = []
        for r in st_files:
            for i, line in enumerate(texts.get(r, "").splitlines(), 1):
                m = re.match(r"^\s*(?:cap(?:ture)?\s+)?(ssc\s+install|net\s+install|github\s+install)\s+([^\s,]+)", line, re.I)
                if m and not line.strip().startswith(("*", "//")):
                    installs.append((m.group(2).rsplit("/", 1)[-1], f"{r}:{i}"))
        net = [(p, e) for p, e in installs if f"{p.lower()}.ado" not in by_base]
        if net:
            add("STATA_NETWORK_INSTALL", DEVIATION, f"Do-files install {', '.join(sorted({p for p, _ in net}))} from the network at run time, "
                "with no version pinned and no copy bundled. SSC serves the current version, which may differ from the authors'.",
                [e for _, e in net][:10])

    # ---- dependencies: Julia
    jl_files = [r for r, l in code.items() if l == "julia"]
    if jl_files and not any(f.name == "Manifest.toml" for f in files):
        add("UNPINNED_DEPENDENCIES" if any(f.name == "Project.toml" for f in files) else "NO_DEPENDENCY_SPEC", DEVIATION,
            "Julia code without a Manifest.toml: package versions are not pinned.", jl_files[:5])

    if any(f.name in ("Dockerfile", "Containerfile") or ".devcontainer" in r for f, r in rels.items()):
        add("ENVIRONMENT_IMAGE", NOTE, "The package ships a container definition. A rerun can build it, but image tags and base "
            "images must be pinned by digest to be reproducible.", [r for f, r in rels.items() if f.name in ("Dockerfile", "Containerfile")])

    # ---- removed APIs
    hits: dict[str, list] = {}
    for r, lang in code.items():
        for i, line in enumerate(texts.get(r, "").splitlines(), 1):
            if line.lstrip().startswith("#"):
                continue
            for l2, rx, what, when in REMOVED_APIS:
                if l2 == lang and re.search(rx, line):
                    hits.setdefault(f"{what} ({when})", []).append(f"{r}:{i}")
    if hits:
        pinned_py = bool(py_files) and py_pinned
        add("REMOVED_API", NOTE if pinned_py else DEVIATION, "Code uses APIs that current releases no longer have: "
            + "; ".join(hits) + (". The package pins its versions, so an install of those versions should still have them, if they "
            "still install on a current interpreter." if pinned_py else ". Nothing pins versions old enough, so a rerun must either "
            "reconstruct an old environment or edit the code, and log which."), [e for v in hits.values() for e in v][:10])

    # ---- data fetched at run time
    fetches: dict[str, list] = {}
    for r, lang in code.items():
        rx = FETCH.get(lang)
        if not rx:
            continue
        for i, line in enumerate(texts.get(r, "").splitlines(), 1):
            st = line.strip()
            if st.startswith(("#", "def ", "*", "//", "%", "function ")) or not st:
                continue
            for m in rx.finditer(line):
                fetches.setdefault(m.group(1).split("(")[0].strip(' "'), []).append(f"{r}:{i}")

    # ---- inputs and outputs
    reads, writes, code_lines = [], [], []
    for r, lang in code.items():
        rd, wr, ln = extract_refs(root / r, r, texts.get(r, ""), lang)
        reads += rd; writes += wr; code_lines += ln
    for r, lang in code.items():
        if lang == "earthengine":                  # Export.table.toDrive({description: 'ndvi', fileFormat: 'CSV'}) writes ndvi.csv
            for m in re.finditer(r"description\s*:\s*['\"]([^'\"]+)['\"](?:[^}]*?fileFormat\s*:\s*['\"](\w+)['\"])?", texts[r]):
                writes.append(Ref(f"{m.group(1)}.{(m.group(2) or 'csv').lower()}", r, texts[r][:m.start()].count("\n") + 1, lang))
        if lang == "dynare":                       # dynare <model> writes <model>_results.mat and friends
            writes += [Ref(Path(r).stem + suffix, r, 0, lang) for suffix in DYNARE_OUTPUTS]
    written = {basename(w.path) for w in writes}
    system_reads = [x for x in reads if SYSTEM_PATH.match(x.path)]
    reads = [x for x in reads if x not in system_reads]
    unres = [x for x in reads if unresolved(x.path)]
    remote = [x for x in reads if URL.match(x.path)]
    missing: dict[str, list[Ref]] = {}
    for x in reads:
        if x in unres or x in remote:
            continue
        b = basename(x.path)
        if b in by_base or b in written:
            continue
        missing.setdefault(b, []).append(x)
    precomputed = sorted({w.path for w in writes if not unresolved(w.path) and basename(w.path) in by_base
                          and any(basename(w.path) == basename(x.path) for x in reads)})
    if precomputed:
        add("PRECOMPUTED_OUTPUTS", NOTE, f"Files the code both writes and reads are already in the package: {', '.join(precomputed[:10])}. "
            "A run may read these instead of recomputing them. A receipt must say whether it replayed them or recomputed them, and "
            "a matching output hash alone does not show recomputation.", precomputed[:10])
    lfs = [r for f, r in rels.items() if f.stat().st_size < 400 and (read_text(f) or "").startswith("version https://git-lfs")]
    if lfs:
        add("LFS_POINTERS", DEVIATION, f"{len(lfs)} files are Git LFS pointers, not data. The data must be fetched with git lfs, "
            "which may need the host's quota or credentials.", lfs[:10])
    if system_reads:
        add("SYSTEM_FILE_READS", NOTE, f"Code reads system files ({', '.join(sorted({x.path for x in system_reads}))}), usually to "
            "detect the operating system. Not package inputs; a rerun on another OS may take a different branch.",
            [f"{x.file}:{x.line}" for x in system_reads[:5]])
    if unres:
        add("UNRESOLVED_PATHS", NOTE, f"{len(unres)} file reads use paths built at run time (macros, globs, variables), so triage could "
            "not check that those inputs exist.", [f"{x.file}:{x.line}" for x in unres[:10]])

    # Every URL the package names, and which missing input (if any) each one documents.
    doc_paras = [(r, p) for r, t in docs.items() for p in paragraphs(t)]
    urls: dict[str, set] = {}
    for r, p in doc_paras:
        for u in URL.findall(p):
            urls.setdefault(clean_url(u), set()).add(r)
    for x in remote:
        urls.setdefault(clean_url(x.path), set()).add(f"{x.file}:{x.line}")
    for r, i, line in code_lines:                  # URLs in code strings: often where a fetcher gets its data
        for lit in literals(line):
            for u in URL.findall(lit):
                urls.setdefault(clean_url(u), set()).add(f"{r}:{i}")
    link_results = {}
    if check_links and urls:
        targets = sorted(urls)[:100]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
            for res in ex.map(lambda u: check_link(u, link_timeout), targets):
                link_results[res["url"]] = res

    def dead(u: str) -> dict | None:
        """Only an HTTP 404 or 410 shows that a link is gone. Anything else says nothing about the link."""
        r = link_results.get(clean_url(u))
        return r if r is not None and r.get("status") in (404, 410) else None

    def failed(u: str) -> dict | None:
        r = link_results.get(clean_url(u))
        return r if r is not None and not r["ok"] and not dead(u) else None

    def link_problems(links: list, ev: list):
        """A deviation for each required link that could not be verified, kept apart from dead links."""
        bad = [u for u in links if failed(u)]
        net = [u for u in bad if not link_results[clean_url(u)].get("status")]
        http = [u for u in bad if link_results[clean_url(u)].get("status")]
        if net:
            add("DATA_LINK_UNREACHABLE", DEVIATION, f"Could not reach {', '.join(net[:3])} from this machine ("
                f"{link_results[clean_url(net[0])].get('error')}). That is evidence about this machine's network, not about the link; "
                "check it from another network before treating the data as unavailable.", ev + net[:3])
        if http:
            add("DATA_LINK_UNVERIFIED", DEVIATION, "The server answered "
                + ", ".join(f"{u} with HTTP {link_results[clean_url(u)]['status']}" for u in http[:3])
                + ". That does not show the data are gone (only 404 or 410 would); it may need a login, a browser or a retry.", ev + http[:3])

    restricted_global = has_any(RESTRICTED, doc_text)
    # Documents that list where raw data come from, by dataset rather than by file name.
    source_docs = sorted({r for r, t in docs.items() if URL.search(t) and (re.search(r"source|data", Path(r).stem, re.I) and not
                          re.match(r"read_?me", Path(r).name, re.I) or re.search(r"^#+\s*(?:data|raw data|data sources?)\b", t, re.I | re.M))})
    source_urls = {clean_url(u) for r in source_docs for u in URL.findall(docs[r])}
    for b, refs in sorted(missing.items()):
        stem = b.rsplit(".", 1)[0]
        ev = [f"{x.file}:{x.line}" for x in refs[:5]]
        mentions = [(r, p) for r, p in doc_paras if b in p.lower() or (len(stem) > 3 and re.search(rf"\b{re.escape(stem)}\b", p, re.I))]
        text = "\n\n".join(p for _, p in mentions)
        restricted, registration = has_any(RESTRICTED, text), has_any(REGISTRATION, text)
        links = [clean_url(u) for u in URL.findall(text)]
        where = f" ({', '.join(sorted({r for r, _ in mentions}))})" if mentions else ""
        if restricted:
            add("MISSING_INPUT_RESTRICTED", BLOCKER, f"`{refs[0].path}` is read by the code but is not in the package, and the "
                f"documentation{where} describes it as restricted (\"{restricted[0]}\"). The desk cannot run this without access.", ev)
        elif links and all(dead(u) for u in links):
            add("DEAD_DATA_LINK", BLOCKER, f"`{refs[0].path}` is not in the package. The documentation points to {links[0]}, which "
                f"answered HTTP {dead(links[0])['status']}: the file is gone from that address.", ev + links[:3])
        elif registration:
            add("MISSING_INPUT_REGISTRATION", DEVIATION, f"`{refs[0].path}` is not in the package; the documentation{where} says it comes "
                f"from a source that needs registration (\"{registration[0]}\"). The desk must register, download and log the extract.", ev)
        elif links:
            add("MISSING_INPUT_DOWNLOAD", DEVIATION, f"`{refs[0].path}` is not in the package; the documentation{where} says to download it "
                f"from {', '.join(links[:3])}. The download date and the file's SHA-256 become part of the receipt"
                + ("" if check_links else "; links were not checked (use --check-links)") + ".", ev + links[:3])
            link_problems(links, ev)
        elif mentions:
            add("MISSING_INPUT_UNDOCUMENTED", BLOCKER, f"`{refs[0].path}` is read by the code and named in the documentation{where}, "
                "but it is not in the package and no source for it is given.", ev)
        elif restricted_global:
            add("MISSING_INPUT_RESTRICTED", BLOCKER, f"`{refs[0].path}` is read by the code but is not in the package. The documentation "
                f"does not name it, but does describe restricted data (\"{restricted_global[0]}\"), so it is most likely one of those.", ev)
        elif source_docs:
            add("MISSING_INPUT_SOURCE_LISTED", DEVIATION, f"`{refs[0].path}` is read by the code but is not in the package. The "
                f"documentation does not name the file but lists external data sources ({', '.join(source_docs)}: {len(source_urls)} "
                "links). Matching this file to a source is a manual step, and each match is a logged deviation; a file no source "
                "accounts for would make this blocked.", ev)
        else:
            add("MISSING_INPUT_UNDOCUMENTED", BLOCKER, f"`{refs[0].path}` is read by the code but is not in the package, and the "
                "documentation does not say where it comes from.", ev)
    if fetches:
        add("RUNTIME_DOWNLOAD", DEVIATION, f"Code fetches data over the network when it runs ({', '.join(sorted(fetches))}). What the "
            "server returns today may differ from what the authors got; a receipt must record each file fetched and its SHA-256.",
            [e for v in fetches.values() for e in v][:10])
    for x in remote:
        d = dead(x.path)
        if d:
            add("DEAD_DATA_LINK", BLOCKER, f"Code downloads {x.path} at run time, which answered HTTP {d['status']}: the file is gone "
                "from that address.", [f"{x.file}:{x.line}"])
            continue
        add("RUNTIME_DOWNLOAD", DEVIATION, f"Code downloads {x.path} at run time. The content may have changed since publication; "
            "a receipt must record its SHA-256" + ("" if check_links else " (link not checked)") + ".", [f"{x.file}:{x.line}"])
        link_problems([x.path], [f"{x.file}:{x.line}"])
    if restricted_global and not any(f.code == "MISSING_INPUT_RESTRICTED" for f in findings):
        add("RESTRICTED_DATA_MENTIONED", NOTE, f"The documentation mentions restricted data (\"{restricted_global[0]}\") but every input "
            "triage could trace is present. Check by hand that no restricted file is read through a path triage could not resolve.")
    cited = {e for f in findings for e in f.evidence}
    http_dead = [u for u in urls if dead(u) and u not in cited]
    unverified = [u for u in urls if failed(u) and u not in cited and link_results[u].get("status")]
    unreachable = [u for u in urls if failed(u) and u not in cited and not link_results[u].get("status")]
    if http_dead:
        add("DEAD_LINK", NOTE, f"{len(http_dead)} other links answered 404 or 410: "
            + ", ".join(f"{u} ({link_results[u]['status']})" for u in http_dead[:10]) + ".", http_dead[:10])
    if unverified:
        add("LINK_UNVERIFIED", NOTE, f"{len(unverified)} other links answered with an HTTP error other than 404 or 410, which does not "
            "show they are gone: " + ", ".join(f"{u} ({link_results[u]['status']})" for u in unverified[:10]) + ".", unverified[:10])
    if unreachable:
        add("LINK_UNREACHABLE", NOTE, f"{len(unreachable)} other links could not be reached from this machine (DNS, refused, timeout or "
            "proxy). That may be this machine's network rather than the link.", unreachable[:10])

    # ---- absolute paths
    abs_hits = [f"{r}:{i}" for r, i, line in code_lines
                if re.search(r"[\"'\s(=]([A-Za-z]:[\\/]|/Users/|/home/|~/(?:Dropbox|Documents|Desktop|Box)|\\\\\w+\\)", line)]
    if abs_hits:
        add("ABSOLUTE_PATH", DEVIATION, f"{len(abs_hits)} code lines use absolute paths from the authors' machines. A rerun must edit "
            "them, and each edit is a logged deviation.", abs_hits[:10])

    # ---- run order
    called: set[str] = set()
    for r, lang in code.items():
        if lang == "python":
            called |= py_imports(texts.get(r, ""))
    called_paths = {basename(x.path) for x in reads if x.lang in ("r", "stata", "julia")}
    scripts = [r for r in code if not r.endswith(".ado") and Path(r).stem not in called and Path(r).name.lower() not in called_paths
               and not set(r.split("/")[:-1]) & called and Path(r).name != "__init__.py"]
    masters = [r for f, r in rels.items() if (f.suffix.lower() in LANGUAGES and MASTER.match(f.stem))
               or f.name in ("Makefile", "Snakefile", "dvc.yaml", "justfile", "run.sh", "run_all.sh")]
    named_in_docs = [r for r in scripts if Path(r).name in doc_text]
    if len(scripts) > 1 and not masters and len(named_in_docs) < 2:
        add("NO_RUN_ORDER", DEVIATION, f"{len(scripts)} scripts, no master script, and the README does not name an order. A rerun must "
            "choose one and log it.", scripts[:10])

    # ---- compute
    hours = []
    unit_h = {"hour": 1, "hr": 1, "day": 24, "week": 168, "month": 720, "minute": 1 / 60, "min": 1 / 60}
    for m in re.finditer(r"(\d+(?:\.\d+)?)\s*(?:-|to)?\s*(?:\d+(?:\.\d+)?)?\s*(hours?|hrs?|days?|weeks?|months?|minutes?|mins?)\b", doc_text, re.I):
        ctx = doc_text[max(0, m.start() - 160): m.end() + 80].lower()
        if re.search(r"\b(take|takes|took|run|runs|runtime|run time|running|approximately|about|around|compute|computation|estimat)", ctx):
            u = m.group(2).lower().rstrip("s")
            hours.append(float(m.group(1)) * unit_h.get(u, unit_h.get(u[:3], 1)))
    if hours and max(hours) > max_hours:
        add("LONG_COMPUTE", DEVIATION, f"The documentation claims a run time of about {max(hours):.0f} hours, over this desk's budget of "
            f"{max_hours:.0f} hours (--max-hours). A full rerun needs a compute plan; a partial rerun must say which parts it skipped.")
    prose = "\n".join(l for l in doc_text.splitlines() if not VERSION_LISTING.search(l))
    if re.search(r"\b(GPU|CUDA|cuDNN)\b", prose) or any(re.search(r"\b(cuda|cupy|\.to\(['\"]cuda)", t) for t in texts.values()):
        add("GPU_REQUIRED", DEVIATION, "The package refers to GPUs or CUDA. A CPU rerun may be slower or numerically different and "
            "must say so.")
    if re.search(r"\b(SLURM|sbatch|PBS|HPC|supercomputer|cluster)\b", doc_text, re.I) or any(f.suffix in (".slurm", ".pbs", ".sbatch") for f in files):
        add("CLUSTER_MENTIONED", NOTE, "The package mentions a cluster or batch scheduler; scripts may assume one.")

    # ---- other software and services the run needs
    if "matlab" in languages:
        boxes = sorted({m.group(1).strip() for l in doc_text.splitlines() for m in TOOLBOX.finditer(l)} - {"Toolbox"})
        if boxes:
            add("MATLAB_TOOLBOX", NOTE, f"Documentation names MATLAB toolboxes: {', '.join(boxes)}. Each is licensed separately; check the "
                "desk's MATLAB has them.")
    if "dynare" in languages:
        dv = sorted(set(re.findall(r"Dynare\s+v?(\d+(?:\.\d+)+)", doc_text, re.I)))
        add("SOFTWARE_REQUIRED", NOTE if dv else DEVIATION, "Requires Dynare (free) inside MATLAB or Octave"
            + (f", version {', '.join(dv)} named in the documentation." if dv else ", with no version named; a rerun must choose one and log it."),
            [r for r, l in code.items() if l == "dynare"][:5])
    if "earthengine" in languages:
        add("EXTERNAL_SERVICE", DEVIATION, "A step runs in Google Earth Engine, which needs an account and exports through Google Drive. "
            "Its outputs are inputs to later steps; a receipt must record the export date and hash, because the hosted image "
            "collections change.", [r for r, l in code.items() if l == "earthengine"][:5])

    # ---- licence
    lic_files = [r for f, r in rels.items() if re.match(r"(licen[cs]e|copying)", f.name, re.I)]
    lic_text = "\n".join(read_text(root / r) or "" for r in lic_files) + "\n" + doc_text
    lic = [name for name, rx in LICENCES if re.search(rx, lic_text, re.I | re.M)]
    if "CC BY-NC" in lic:
        lic.remove("CC BY") if "CC BY" in lic else None
        add("NONCOMMERCIAL_LICENCE", NOTE, "Non-commercial licence. Rerunning for an editorial check is normally fine; a receipt should "
            "not redistribute the package's files.", lic_files)
    if not lic_files and not lic:
        add("NO_LICENCE", NOTE, "No licence file and no licence named in the documentation. Running it for a check is unaffected, but "
            "a receipt should quote and hash files rather than redistribute them.")

    if total_bytes > 5 * 1024 ** 3:
        add("LARGE_PACKAGE", NOTE, f"The package is {total_bytes / 1024 ** 3:.1f} GB on disk.")

    sev = {f.severity for f in findings}
    verdict = "blocked" if BLOCKER in sev else "runnable-with-deviations" if DEVIATION in sev else "runnable"
    order = {BLOCKER: 0, DEVIATION: 1, NOTE: 2}
    findings.sort(key=lambda f: order[f.severity])
    return {
        "verdict": verdict,
        "counts": {s: sum(f.severity == s for f in findings) for s in (BLOCKER, DEVIATION, NOTE)},
        "findings": [asdict(f) for f in findings],
        "inventory": {"files": len(files), "bytes": total_bytes, "languages": languages,
                      "code_files": {lang: sum(v == lang for v in code.values()) for lang in languages},
                      "docs_read": sorted(docs), "licences_named": lic, "master_scripts": masters},
        "inputs": {"reads": len(reads), "writes": len(writes), "missing": sorted(missing), "unresolved": len(unres),
                   "remote": sorted({x.path for x in remote})},
        "links": {"found": len(urls), "checked": check_links, "results": [link_results[u] for u in sorted(link_results)]},
        "seconds": round(time.monotonic() - t0, 3),
    }


# ----------------------------------------------------------------------------------------------------------------- reports

def render_md(doc: dict) -> str:
    s, inv, inp = doc["source"], doc["result"]["inventory"], doc["result"]["inputs"]
    res = doc["result"]
    label = {"runnable": "RUNNABLE", "runnable-with-deviations": "RUNNABLE WITH DEVIATIONS", "blocked": "BLOCKED"}[res["verdict"]]
    out = [f"# Triage verdict: {label}", ""]
    src = s.get("url") or s.get("path")
    out += [f"- Package: `{src}`" + (f" at commit `{s['commit']}`" if s.get("commit") else "") + (f", SHA-256 `{s['sha256']}`" if s.get("sha256") else ""),
            f"- Triaged: {doc['when']} on {doc['environment']['platform']}, Python {doc['environment']['python']}, "
            f"{res['seconds']} s of analysis",
            f"- Triage script: `triage.py` SHA-256 `{doc['triage_sha256']}`; options: {doc['options']}",
            f"- {res['counts']['blocker']} blockers, {res['counts']['deviation']} deviations, {res['counts']['note']} notes", "",
            "Triage reads the package and never executes it. This verdict says whether the committed materials can be run on this desk "
            "and what a rerun would have to change. It says nothing about whether the paper's results are correct.", ""]
    for sev, title in ((BLOCKER, "Blockers"), (DEVIATION, "Deviations a rerun would have to log"), (NOTE, "Notes")):
        fs = [f for f in res["findings"] if f["severity"] == sev]
        if fs:
            out += [f"## {title}", ""]
            for f in fs:
                out.append(f"- **{f['code']}**: {f['message']}")
                if f["evidence"]:
                    out.append("  Evidence: " + ", ".join(f"`{e}`" for e in f["evidence"]))
            out.append("")
    out += ["## What triage looked at", "",
            f"- {inv['files']} files, {inv['bytes']:,} bytes. Languages: {', '.join(f'{k} ({v})' for k, v in inv['code_files'].items()) or 'none'}.",
            f"- Documentation read: {', '.join(inv['docs_read']) or 'none'}. Licences named: {', '.join(inv['licences_named']) or 'none'}.",
            f"- Master scripts: {', '.join(inv['master_scripts']) or 'none'}.",
            f"- File reads traced: {inp['reads']}; writes: {inp['writes']}; unresolved paths: {inp['unresolved']}; "
            f"missing: {', '.join(inp['missing']) or 'none'}.",
            f"- Links found: {res['links']['found']}; checked: {'yes' if res['links']['checked'] else 'no'}."]
    for r in res["links"]["results"]:
        out.append(f"  - {r['url']}: {'ok' if r['ok'] else 'FAILED'} ({r.get('status') or r.get('error')})")
    return "\n".join(out) + "\n"


def run(argv: list[str] | None = None) -> dict:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("package", help="directory, .zip/.tar.gz, or git URL")
    ap.add_argument("--commit", help="commit to check out when PACKAGE is a git URL")
    ap.add_argument("--have", default="", help="comma-separated proprietary software this desk has, e.g. stata,matlab")
    ap.add_argument("--check-links", action="store_true", help="fetch every URL the package names (network)")
    ap.add_argument("--link-timeout", type=float, default=15.0)
    ap.add_argument("--max-hours", type=float, default=24.0, help="run-time budget; longer documented run times are a deviation")
    ap.add_argument("--json", help="write the verdict as JSON here")
    ap.add_argument("--md", help="write the verdict as Markdown here")
    ap.add_argument("--label", help="name the package in the report instead of its local path")
    a = ap.parse_args(argv)
    have = {h.strip().lower() for h in a.have.split(",") if h.strip()}
    work = Path(tempfile.mkdtemp(prefix="triage-"))
    try:
        root, source = load_package(a.package, a.commit, work)
        if a.label:
            source["path" if "path" in source else "url"] = a.label
        result = triage(root, have, a.check_links, a.max_hours, a.link_timeout)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    opts = []
    if have:
        opts.append(f"--have {','.join(sorted(have))}")
    if a.check_links:
        opts.append("--check-links")
    if a.max_hours != 24.0:
        opts.append(f"--max-hours {a.max_hours:g}")
    doc = {"format": FORMAT, "source": source, "when": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "triage_sha256": sha256_file(Path(__file__)), "options": " ".join(opts) or "defaults",
           "environment": {"python": platform.python_version(), "platform": platform.platform()}, "result": result}
    md = render_md(doc)
    if a.json:
        Path(a.json).write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8", newline="\n")
    if a.md:
        Path(a.md).write_text(md, encoding="utf-8", newline="\n")
    if not a.json and not a.md:
        sys.stdout.write(md)
    return doc


if __name__ == "__main__":
    run()
