"""Rank replication packages by the chance of a clean, boring, complete rerun on a free-software Linux machine.

The rule was written before any candidate was scored (see the commit that adds this file). Input: candidates.json, one
record per package, every field a fact read from the package with the file it came from. Output: a ranked table.

Gates (a package failing any gate is listed, with the gate, and not ranked):
  G1 target_journal     the authors name one of the target journals as published or forthcoming
  G2 authors_package    the authors' own package, not a third-party replication or port
  G3 free_software      the tier to be rerun needs no proprietary software (Stata, MATLAB, SAS, GAMS, Mathematica)
  G4 inputs_available   every input of that tier is in the repository or on a host this machine can reach

Points, for the tier to be rerun:
  +3 inputs all in the repository (no download at run time)
  +3 committed numeric outputs (tables or text with numbers) to compare against
  +2 stated run time <= 1 hour, +1 if <= 24 hours, 0 if longer or unstated
  +1 package versions pinned (a lockfile, renv.lock, Manifest.toml, or == pins)
  +1 seeds or determinism stated
  +1 published or forthcoming in 2025 or 2026
  +1 the tier recomputes the paper's main estimates, not only figures or descriptive tables

Stdlib only. usage: python candidates/score.py [--md]
"""
import json
import sys
from pathlib import Path

TARGET = {"REStud", "Econometrica", "JPE", "Journal of Finance", "Economic Journal", "JEEA", "CJE", "Economic Inquiry",
          "Econometrics Journal"}
GATES = ["target_journal", "authors_package", "free_software", "inputs_available"]


def score(c: dict) -> tuple:
    failed = [g for g in GATES if not (c["journal"] in TARGET if g == "target_journal" else c[g])]
    if failed:
        return None, failed
    pts = 3 * c["inputs_in_repo"] + 3 * c["committed_numeric_outputs"]
    rt = c.get("runtime_hours")
    pts += 2 if rt is not None and rt <= 1 else (1 if rt is not None and rt <= 24 else 0)
    pts += c["pinned"] + c["seeded"] + (c["year"] >= 2025) + c["main_estimates"]
    return pts, []


def main(argv):
    cands = json.loads((Path(__file__).parent / "candidates.json").read_text())["candidates"]
    ranked, gated = [], []
    for c in cands:
        pts, failed = score(c)
        (ranked if pts is not None else gated).append((pts, failed, c))
    ranked.sort(key=lambda r: -r[0])
    for pts, _, c in ranked:
        print(f"| {pts} | {c['journal']} | [{c['repo']}](https://github.com/{c['repo']}/tree/{c['commit']}) | {c['tier']} | {c['status']} |")
    print()
    for _, failed, c in gated:
        print(f"| {c['journal']} | {c['repo']} | {', '.join(failed)} | {c['why_gated']} |")


if __name__ == "__main__":
    main(sys.argv[1:])
