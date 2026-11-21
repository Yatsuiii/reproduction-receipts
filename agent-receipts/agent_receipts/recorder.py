"""Recording side: wrap each tool call, write one signed, chained record per call."""
from __future__ import annotations

import inspect
import os
import secrets
import threading
import time
from pathlib import Path
from typing import Any, Callable, Iterable

from . import ed25519
from .canon import body, canonical, record_hash, sha256_json

FORMAT = "agent-receipts/0"


class Signer:
    """An Ed25519 key. The private seed never goes into a receipt; only `public_hex` does."""

    def __init__(self, seed: bytes):
        if len(seed) != 32:
            raise ValueError("seed must be 32 bytes")
        self._seed = bytes(seed)
        self.public = ed25519.public_key(self._seed)
        self.public_hex = self.public.hex()

    @classmethod
    def generate(cls) -> "Signer":
        return cls(secrets.token_bytes(32))

    @classmethod
    def from_seed(cls, seed: bytes) -> "Signer":
        return cls(seed)

    @classmethod
    def from_file(cls, path) -> "Signer":
        """Read a 64-hex-char seed from a file (create one with `python -m agent_receipts keygen`)."""
        return cls(bytes.fromhex(Path(path).read_text(encoding="ascii").strip()))

    def sign(self, msg: bytes) -> bytes:
        return ed25519.sign(self._seed, msg)

    def __repr__(self):
        return f"Signer(public={self.public_hex[:16]}...)"


def seal(record: dict, signer: Signer) -> dict:
    """Set `key` and `sig` on a record in place, and return it."""
    record.pop("sig", None)
    record["key"] = signer.public_hex
    record["sig"] = signer.sign(body(record)).hex()
    return record


def to_json(value: Any) -> Any:
    """Default encoder for tool results: JSON values pass through; pydantic models (MCP results) are dumped; else TypeError."""
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json", by_alias=True, exclude_none=True)
    canonical(value)  # raises TypeError / ValueError for anything that is not plain JSON
    return value


class Recorder:
    """Writes a receipt. One Recorder is one session; call `close()` at the end.

    rec = Recorder("run.receipt.jsonl", signer=Signer.from_file("agent.key"), actor="billing-agent@acme")
    result = rec.call("search", search, {"query": "x"}, sources=["web:kb"], replayable=True)
    anchor = rec.close()        # publish this somewhere the key holder cannot rewrite
    """

    def __init__(self, path, *, signer: Signer, actor: str, clock: Callable[[], float] = time.time,
                 meta: dict | None = None, encode: Callable[[Any], Any] = to_json, fsync: bool = False):
        self.path = Path(path)
        self.signer, self.actor, self.clock, self.encode, self.fsync = signer, actor, clock, encode, fsync
        self.session = secrets.token_hex(16)
        self._seq = 0
        self._calls = 0
        self._prev = None
        self._closed = False
        self._lock = threading.Lock()
        if self.path.exists() and self.path.stat().st_size:
            raise FileExistsError(f"{self.path} already holds a receipt; one file is one session")
        self._fh = open(self.path, "w", encoding="utf-8", newline="\n")
        self._write({"type": "open", "actor": actor, "meta": meta or {}, "t": clock()})

    # -- writing --
    def _write(self, rec: dict) -> dict:
        rec.update({"format": FORMAT, "session": self.session, "seq": self._seq, "prev": self._prev})
        seal(rec, self.signer)
        self._fh.write(canonical(rec).decode("utf-8") + "\n")
        self._fh.flush()
        if self.fsync:
            os.fsync(self._fh.fileno())
        self._prev = record_hash(rec)
        self._seq += 1
        return rec

    def _call_record(self, tool, args, t_start, status, result, error, sources, derived_from, replayable,
                     redact_args, redact_result) -> dict:
        return {
            "type": "call", "tool": tool,
            "args": None if redact_args else args, "args_sha256": sha256_json(args),
            "status": status,
            "result": None if (redact_result or status != "ok") else result,
            "result_sha256": sha256_json(result) if status == "ok" else None,
            "error": error, "t_start": t_start, "t": self.clock(),
            "sources": list(sources), "derived_from": [int(s) for s in derived_from],
            "replayable": bool(replayable),
        }

    def _check(self, derived_from):
        if self._closed:
            raise RuntimeError("receipt is closed")
        for s in derived_from:
            if not (1 <= int(s) < self._seq):
                raise ValueError(f"derived_from={s} is not an earlier call in this session")

    @property
    def last_seq(self) -> int:
        """seq of the most recent record; pass it in `derived_from` of a later call that used that output."""
        return self._seq - 1

    def call(self, tool: str, fn: Callable, args: dict | None = None, *, sources: Iterable[str] = (),
             derived_from: Iterable[int] = (), replayable: bool = False, fence: Callable[[], dict] | None = None,
             redact_args: bool = False, redact_result: bool = False):
        """Run fn(**args), record what happened, return fn's result (or re-raise its exception).

        fence: optional callable run first; a non-empty return (e.g. stalefence `Premises.changed(...)`) means something
        the call relied on moved, so the tool is NOT run, a `fenced` record is written and `Fenced` is raised."""
        args = dict(args or {})
        derived_from = list(derived_from)
        with self._lock:
            self._check(derived_from)
            canonical(args)
            t_start = self.clock()
            if fence is not None:
                changed = fence()
                if changed:
                    err = "fenced: " + "; ".join(f"{k!r}: {a!r} -> {b!r}" for k, (a, b) in changed.items())
                    self._calls += 1
                    self._write(self._call_record(tool, args, t_start, "fenced", None, err, sources, derived_from,
                                                  replayable, redact_args, redact_result))
                    raise Fenced(changed)
            try:
                raw = fn(**args)
                if inspect.isawaitable(raw):
                    raise TypeError("fn returned an awaitable; use acall() for async tools")
            except Exception as e:
                self._calls += 1
                self._write(self._call_record(tool, args, t_start, "error", None, f"{type(e).__name__}: {e}", sources,
                                              derived_from, replayable, redact_args, redact_result))
                raise
            try:
                result = self.encode(raw)
            except Exception as e:   # the tool ran; say so even though its result cannot be stored
                self._calls += 1
                self._write(self._call_record(tool, args, t_start, "error", None,
                                              f"unrecordable result: {type(e).__name__}: {e}", sources, derived_from,
                                              False, redact_args, redact_result))
                raise
            self._calls += 1
            self._write(self._call_record(tool, args, t_start, "ok", result, None, sources, derived_from, replayable,
                                          redact_args, redact_result))
            return raw

    async def acall(self, tool: str, fn: Callable, args: dict | None = None, *, sources: Iterable[str] = (),
                    derived_from: Iterable[int] = (), replayable: bool = False,
                    fence: Callable[[], dict] | None = None, redact_args: bool = False, redact_result: bool = False):
        """Async form of call(): awaits fn(**args). Calls are recorded in completion order."""
        args = dict(args or {})
        derived_from = list(derived_from)
        self._check(derived_from)
        canonical(args)
        t_start = self.clock()
        if fence is not None:
            changed = fence()
            if changed:
                err = "fenced: " + "; ".join(f"{k!r}: {a!r} -> {b!r}" for k, (a, b) in changed.items())
                with self._lock:
                    self._calls += 1
                    self._write(self._call_record(tool, args, t_start, "fenced", None, err, sources, derived_from,
                                                  replayable, redact_args, redact_result))
                raise Fenced(changed)
        try:
            raw = await fn(**args)
        except Exception as e:
            with self._lock:
                self._calls += 1
                self._write(self._call_record(tool, args, t_start, "error", None, f"{type(e).__name__}: {e}", sources,
                                              derived_from, replayable, redact_args, redact_result))
            raise
        try:
            result = self.encode(raw)
        except Exception as e:
            with self._lock:
                self._calls += 1
                self._write(self._call_record(tool, args, t_start, "error", None,
                                              f"unrecordable result: {type(e).__name__}: {e}", sources, derived_from,
                                              False, redact_args, redact_result))
            raise
        with self._lock:
            self._calls += 1
            self._write(self._call_record(tool, args, t_start, "ok", result, None, sources, derived_from, replayable,
                                          redact_args, redact_result))
        return raw

    def close(self) -> str:
        """Write the close record and return its hash. Publish that hash outside the key holder's control (a ticket, an
        email to the reviewer, a git commit) to make a later rewrite by the key holder detectable."""
        with self._lock:
            if self._closed:
                raise RuntimeError("already closed")
            rec = self._write({"type": "close", "count": self._calls, "t": self.clock()})
            self._closed = True
            self._fh.close()
            return record_hash(rec)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        if not self._closed:
            self.close()


class Fenced(Exception):
    """A premise the call depended on changed; the tool was not run and a `fenced` record was written."""

    def __init__(self, changed: dict):
        self.changed = changed
        super().__init__("fenced: premise changed since it was read: " + ", ".join(map(repr, changed)))
