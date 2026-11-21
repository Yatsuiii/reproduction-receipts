"""Command line. Installed as `receipt`; `python -m agent_receipts` is the same.

  receipt verify run.jsonl                         # one command for a third party; see below for what it reads
  receipt keygen agent.key                         # new private seed (0600), prints the public key
  receipt pubkey agent.key
  receipt anchor run.jsonl --key agent.key         # publish the close record's hash to Rekor (public, permanent)
  receipt log-key [--log-url URL] > rekor.pub      # fetch a log's public key once, to pin it

verify reads, when not given on the command line:
  public_key.txt        next to the receipt, lines of ACTOR=PUBHEX (only meaningful if it reached you separately from
                        the receipt, e.g. from the operator's website; the output says where the trust came from)
  anchor.txt            next to the receipt, a close hash handed over out of band
  <receipt>.anchor.json a transparency-log anchor; needs --log-key, the log's public key pinned by you

Exit 0 when the receipt is valid (warnings such as stale allowed), 1 when it is not, 2 on usage errors."""
from __future__ import annotations

import argparse
import json
import os
import secrets
import sys
import urllib.request
from pathlib import Path

from .recorder import Signer
from .verify import verify


def _trust_lines(text: str) -> dict:
    out = {}
    for ln in text.splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            if "=" not in ln:
                raise ValueError(f"trust line wants ACTOR=PUBHEX, got {ln!r}")
            actor, key = ln.rsplit("=", 1)
            out[actor.strip()] = key.strip()
    return out


def cmd_verify(a) -> int:
    rp = Path(a.receipt)
    if not rp.is_file():
        print(f"no such receipt: {rp}", file=sys.stderr)
        return 2
    side = rp.parent
    notes = []
    try:
        trusted = _trust_lines("\n".join(a.trust))
        if a.trust_file:
            trusted.update(_trust_lines(Path(a.trust_file).read_text()))
            notes.append(f"trust list: {a.trust_file}")
        elif not trusted and (side / "public_key.txt").exists():
            trusted = _trust_lines((side / "public_key.txt").read_text())
            notes.append("trust list: public_key.txt next to the receipt (check you got that key from somewhere else)")
        elif trusted:
            notes.append("trust list: --trust")
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2
    anchor = a.anchor
    if anchor is None and (side / "anchor.txt").exists():
        anchor = (side / "anchor.txt").read_text().strip()
        notes.append("anchor: anchor.txt next to the receipt")
    bundle = None
    bp = Path(a.anchor_bundle) if a.anchor_bundle else Path(str(rp) + ".anchor.json")
    if bp.exists():
        bundle = json.loads(bp.read_text())
        if not a.log_key:
            print(f"{bp.name} is a transparency-log anchor: pass --log-key with the log's public key "
                  f"(get it once with `receipt log-key > rekor.pub` and keep it)", file=sys.stderr)
            return 2
        notes.append(f"log anchor: {bp.name}, log key {a.log_key}")
    log_keys = [Path(k).read_bytes() for k in a.log_key]
    rep = verify(rp, trusted=trusted, anchor=anchor, revoked=a.revoke, anchor_bundle=bundle, log_keys=log_keys,
                 require_anchor=a.require_anchor, max_delay=a.max_delay)
    if a.json:
        print(json.dumps(dict(rep.to_dict(), sources=notes), indent=1))
    else:
        print(rep)
        for n in notes:
            print(f"  ({n})")
    return 0 if rep.ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="receipt", description="agent-receipts: record, verify and anchor tool-call receipts")
    sub = ap.add_subparsers(dest="cmd", required=True)
    k = sub.add_parser("keygen", help="write a new private key")
    k.add_argument("path")
    p = sub.add_parser("pubkey", help="print a key's public half")
    p.add_argument("path")
    v = sub.add_parser("verify", help="verify a receipt offline")
    v.add_argument("receipt")
    v.add_argument("--trust", action="append", default=[], metavar="ACTOR=PUBHEX")
    v.add_argument("--trust-file")
    v.add_argument("--anchor", help="close hash handed over out of band")
    v.add_argument("--anchor-bundle", help="transparency-log anchor (default: <receipt>.anchor.json if present)")
    v.add_argument("--log-key", action="append", default=[], help="pinned log public key, PEM file")
    v.add_argument("--require-anchor", action="store_true")
    v.add_argument("--max-delay", type=float, default=3600)
    v.add_argument("--revoke", action="append", default=[], metavar="SOURCE")
    v.add_argument("--json", action="store_true")
    an = sub.add_parser("anchor", help="publish a closed receipt's hash to a transparency log (public and permanent)")
    an.add_argument("receipt")
    an.add_argument("--key", required=True)
    an.add_argument("--log-url", default=None)
    lk = sub.add_parser("log-key", help="fetch a transparency log's public key (network)")
    lk.add_argument("--log-url", default=None)
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
    if a.cmd == "verify":
        return cmd_verify(a)
    from . import rekor
    url = a.log_url or rekor.DEFAULT_LOG
    if a.cmd == "anchor":
        b = rekor.upload(a.receipt, Signer.from_file(a.key), log_url=url)
        print(f"anchored at {url}, logIndex {b['entry']['logIndex']}; bundle {rekor.bundle_path(a.receipt)}")
        return 0
    with urllib.request.urlopen(url.rstrip("/") + "/api/v1/log/publicKey", timeout=30) as r:
        sys.stdout.write(r.read().decode())
    return 0


if __name__ == "__main__":
    sys.exit(main())
