"""Fetch model weights while the network is still on, and check every byte against the pin.

This is the only step that touches the network. The harness runs afterwards inside a network namespace with no interface but lo.

  --discover: read the repository at a revision, download the listed files, hash them, compare with the SHA-256 Hugging Face
              stores for LFS files, print a MODEL.json candidate. Used once, before the pin was frozen.
  --fetch:    download exactly the files in MODEL.json at its pinned commit, refuse on any hash mismatch, copy them into an
              empty directory that holds nothing else.

usage: python offline-model/fetch_weights.py --discover --repo ORG/NAME --revision REV --files a b c
       python offline-model/fetch_weights.py --fetch --model offline-model/MODEL.json --dest DIR"""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def discover(repo: str, revision: str, files: list) -> int:
    from huggingface_hub import HfApi, hf_hub_download
    info = HfApi().model_info(repo, revision=revision, files_metadata=True)
    siblings = {s.rfilename: s for s in info.siblings}
    out = {"format": "offline-model/1", "repo": repo, "revision": info.sha,
           "licence_declared": (info.card_data or {}).get("license") if info.card_data else None, "files": {}}
    problems = []
    for name in files:
        s = siblings.get(name)
        if s is None:
            problems.append(f"not in repo at {info.sha}: {name}")
            continue
        local = Path(hf_hub_download(repo, name, revision=info.sha))
        digest = sha256(local)
        lfs = getattr(s, "lfs", None)
        lfs_sha = (lfs.sha256 if hasattr(lfs, "sha256") else (lfs or {}).get("sha256")) if lfs else None
        if lfs_sha and lfs_sha != digest:
            problems.append(f"{name}: downloaded {digest}, hub says {lfs_sha}")
        out["files"][name] = {"sha256": digest, "bytes": local.stat().st_size, "hub_lfs_sha256": lfs_sha}
    print(json.dumps(out, indent=1))
    for p in problems:
        print("DISCOVER PROBLEM:", p, file=sys.stderr)
    return 1 if problems else 0


def fetch(model_path: Path, dest: Path) -> int:
    from huggingface_hub import hf_hub_download
    model = json.loads(model_path.read_text(encoding="utf-8"))
    dest.mkdir(parents=True, exist_ok=True)
    if any(dest.iterdir()):
        print(f"refuse: {dest} is not empty", file=sys.stderr)
        return 2
    for name, meta in model["files"].items():
        local = Path(hf_hub_download(model["repo"], name, revision=model["revision"]))
        digest = sha256(local)
        if digest != meta["sha256"]:
            print(f"refuse: {name} is {digest}, MODEL.json pins {meta['sha256']}", file=sys.stderr)
            return 2
        shutil.copyfile(local, dest / name)
        print(f"ok {name} {digest} {meta['bytes']} bytes")
    return 0


def main(argv: list) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--discover", action="store_true")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--repo")
    ap.add_argument("--revision", default="main")
    ap.add_argument("--files", nargs="*", default=[])
    ap.add_argument("--model", type=Path)
    ap.add_argument("--dest", type=Path)
    a = ap.parse_args(argv)
    if a.discover:
        return discover(a.repo, a.revision, a.files)
    if a.fetch:
        return fetch(a.model, a.dest)
    ap.error("pass --discover or --fetch")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
