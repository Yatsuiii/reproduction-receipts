"""Canonical JSON bytes and digests, as defined in FORMAT.md."""
from __future__ import annotations

import hashlib
import json


def canonical(x) -> bytes:
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_json(x) -> str:
    return hashlib.sha256(canonical(x)).hexdigest()


def body(record: dict) -> bytes:
    """A record's canonical bytes: everything except `sig`."""
    return canonical({k: v for k, v in record.items() if k != "sig"})


def record_hash(record: dict) -> str:
    return hashlib.sha256(body(record)).hexdigest()
