"""Command line: keygen, pubkey, verify.

  python -m agent_receipts keygen agent.key            # writes a new 32-byte seed as hex (keep it private)
  python -m agent_receipts pubkey agent.key            # prints the public key to hand to verifiers
  python -m agent_receipts verify run.jsonl --trust ACTOR=PUBHEX [--anchor HASH] [--revoke SOURCE ...] [--json]

verify exits 0 when the receipt is valid (warnings such as stale allowed), 1 when it is not, 2 on usage errors."""
from __future__ import annotations

import argparse
import json
import os
import secrets
import sys
from pathlib import Path

from .recorder import Signer
from .verify import verify


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="agent_receipts")
    sub = ap.add_subparsers(dest="cmd", required=True)
    k = sub.add_parser("keygen")
    k.add_argument("path")
    p = sub.add_parser("pubkey")
    p.add_argument("path")
    v = sub.add_parser("verify")
    v.add_argument("receipt")
    v.add_argument("--trust", action="append", default=[], metavar="ACTOR=PUBHEX")
    v.add_argument("--anchor")
    v.add_argument("--revoke", action="append", default=[], metavar="SOURCE")
    v.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "keygen":
        path = Path(a.path)
        if path.exists():
            print(f"{path} exists; not overwriting", file=sys.stderr)
            return 2
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w") as fh:
            fh.write(secrets.token_bytes(32).hex() + "\n")
        print(Signer.from_file(path).public_hex)
        return 0
    if a.cmd == "pubkey":
        print(Signer.from_file(a.path).public_hex)
        return 0
    trusted = {}
    for t in a.trust:
        if "=" not in t:
            print(f"--trust wants ACTOR=PUBHEX, got {t!r}", file=sys.stderr)
            return 2
        actor, key = t.rsplit("=", 1)
        trusted[actor] = key
    rep = verify(a.receipt, trusted=trusted, anchor=a.anchor, revoked=a.revoke)
    print(json.dumps(rep.to_dict(), indent=1) if a.json else rep)
    return 0 if rep.ok else 1


if __name__ == "__main__":
    sys.exit(main())
