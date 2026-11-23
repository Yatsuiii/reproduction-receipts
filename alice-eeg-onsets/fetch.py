"""Fetch annexed files of a NEMAR dataset clone from its public S3 remote, checking each SHA-256 against its key.

usage: python fetch.py <clone_dir> <out_dir> <glob> [<glob> ...]

Files land at <out_dir>/<same relative path>. A file whose hash does not match its key is deleted and reported.
"""
import glob
import hashlib
import os
import re
import sys
import time
import urllib.request

BASE = "https://nemar.s3.us-east-2.amazonaws.com/nm000180/objects/"
KEY_RE = re.compile(r"(SHA256E-s(\d+)--([0-9a-f]{64})[^/\s]*)")


def annex_key(path):
    if os.path.islink(path):
        m = KEY_RE.search(os.path.basename(os.readlink(path)))
    else:
        with open(path, "rb") as f:
            head = f.read(300).decode("ascii", "ignore")
        m = KEY_RE.search(head) if head.startswith("/annex/objects/") else None
    return m.groups() if m else None


def fetch(clone, out, rel):
    k = annex_key(os.path.join(clone, rel))
    dst = os.path.join(out, rel)
    if k is None:  # plain git file: copy it so the BrainVision triplet sits together
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(os.path.join(clone, rel), "rb") as a, open(dst, "wb") as b:
            b.write(a.read())
        return "copied-from-git"
    key, size, sha = k
    if os.path.exists(dst) and os.path.getsize(dst) == int(size):
        return "cached"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    for attempt in range(4):
        try:
            h = hashlib.sha256()
            with urllib.request.urlopen(BASE + key, timeout=120) as r, open(dst, "wb") as f:
                while chunk := r.read(1 << 20):
                    h.update(chunk)
                    f.write(chunk)
            break
        except Exception as e:  # network retry
            print(f"  retry {attempt + 1} {rel}: {e}", flush=True)
            time.sleep(2 ** attempt)
    else:
        return "download-failed"
    if h.hexdigest() != sha or os.path.getsize(dst) != int(size):
        os.remove(dst)
        return "HASH-MISMATCH"
    return "ok"


def main():
    clone, out, pats = sys.argv[1], sys.argv[2], sys.argv[3:]
    rels = sorted({os.path.relpath(p, clone) for pat in pats for p in glob.glob(os.path.join(clone, pat))})
    bad = 0
    for rel in rels:
        s = fetch(clone, out, rel)
        print(f"{s}\t{rel}", flush=True)
        bad += s in ("HASH-MISMATCH", "download-failed")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
