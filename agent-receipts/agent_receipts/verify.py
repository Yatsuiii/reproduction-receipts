"""Checking side: verify a receipt, compute stale calls, replay deterministic calls. Needs only the receipt and the public key."""
from __future__ import annotations

import inspect
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable

from . import ed25519
from .canon import body, record_hash, sha256_json

FORMAT = "agent-receipts/0"
FAILURES = ("malformed", "bad_signature", "untrusted_key", "chain_broken", "sequence", "session_mismatch", "unclosed",
            "count_mismatch", "clock_backwards", "digest_mismatch", "anchor_mismatch")
WARNINGS = ("stale",)

_COMMON = {"type": str, "format": str, "session": str, "seq": int, "t": (int, float), "key": str, "sig": str}
_BY_TYPE = {
    "open": {"actor": str, "meta": dict},
    "call": {"tool": str, "args_sha256": str, "status": str, "t_start": (int, float), "sources": list,
             "derived_from": list, "replayable": bool},
    "close": {"count": int},
}


@dataclass
class Finding:
    code: str
    line: int          # 1-based line in the file
    seq: int | None
    detail: str

    def __str__(self):
        where = f"line {self.line}" + (f" (seq {self.seq})" if self.seq is not None else "")
        return f"{self.code:16} {where}: {self.detail}"


@dataclass
class Report:
    path: str
    findings: list = field(default_factory=list)
    stale: list = field(default_factory=list)
    actor: str | None = None
    session: str | None = None
    calls: int = 0
    close_hash: str | None = None

    @property
    def ok(self) -> bool:
        return not any(f.code in FAILURES for f in self.findings)

    def codes(self) -> set:
        return {f.code for f in self.findings} or {"ok"}

    def add(self, code, line, seq, detail):
        self.findings.append(Finding(code, line, seq, detail))

    def to_dict(self) -> dict:
        return {"path": self.path, "ok": self.ok, "codes": sorted(self.codes()), "actor": self.actor,
                "session": self.session, "calls": self.calls, "close_hash": self.close_hash, "stale": self.stale,
                "findings": [f.__dict__ for f in self.findings]}

    def __str__(self):
        head = "VALID" if self.ok else "INVALID"
        lines = [f"{head}: {self.path}  actor={self.actor} session={self.session} calls={self.calls}"]
        lines += [f"  {f}" for f in self.findings]
        if self.close_hash:
            lines.append(f"  close hash (anchor): {self.close_hash}")
        return "\n".join(lines)


def _read(path: Path, report: Report) -> list:
    """Return [(line_no, record_or_None)]."""
    out = []
    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            rec = json.loads(raw)
        except json.JSONDecodeError as e:
            report.add("malformed", i, None, f"not JSON: {e.msg}")
            out.append((i, None))
            continue
        if not isinstance(rec, dict):
            report.add("malformed", i, None, "record is not an object")
            out.append((i, None))
            continue
        need = dict(_COMMON, **_BY_TYPE.get(rec.get("type"), {}))
        bad = [k for k, t in need.items() if not isinstance(rec.get(k), t) or isinstance(rec.get(k), bool) and t is int]
        if rec.get("type") not in _BY_TYPE:
            bad.append("type")
        if "prev" not in rec or not (rec["prev"] is None or isinstance(rec["prev"], str)):
            bad.append("prev")
        if bad:
            report.add("malformed", i, rec.get("seq") if isinstance(rec.get("seq"), int) else None,
                       "missing or wrong type: " + ", ".join(sorted(set(bad))))
            out.append((i, None))
            continue
        out.append((i, rec))
    return out


def _sig_ok(rec: dict) -> bool:
    try:
        return ed25519.verify(bytes.fromhex(rec["key"]), body(rec), bytes.fromhex(rec["sig"]))
    except ValueError:
        return False


def verify(path, *, trusted: dict | None = None, anchor: str | None = None, revoked: Iterable[str] = (),
           check_signatures: bool = True) -> Report:
    """Verify a receipt file. `trusted` maps actor -> public key hex; without it, signatures are checked against each
    record's own key but nothing binds that key to anyone (reported as untrusted_key).

    check_signatures=False turns this into the unsigned-hash-chain baseline (used in baselines/, not for real checks)."""
    path = Path(path)
    report = Report(str(path))
    rows = _read(path, report)
    recs = [(ln, r) for ln, r in rows if r is not None]
    if not recs:
        report.add("malformed", 1, None, "no records")
        return report

    first_ln, first = recs[0]
    if first["type"] != "open":
        report.add("sequence", first_ln, first["seq"], "first record is not open")
    report.session = first["session"]
    report.actor = first.get("actor")
    open_key = first["key"]

    if check_signatures:
        want = (trusted or {}).get(report.actor)
        if want is None:
            report.add("untrusted_key", first_ln, first["seq"], f"actor {report.actor!r} is not in the trust list")
        elif want.lower() != open_key.lower():
            report.add("untrusted_key", first_ln, first["seq"], f"receipt is signed by {open_key[:16]}..., "
                                                                 f"trust list gives {want[:16]}... for {report.actor!r}")

    prev_rec, prev_ln, prev_t = None, None, None
    for idx, (ln, r) in enumerate(rows):
        if r is None:                       # a malformed line breaks the chain for the next record
            prev_rec = None
            continue
        seq = r["seq"]
        if r.get("format") != FORMAT:
            report.add("malformed", ln, seq, f"format {r.get('format')!r}, expected {FORMAT}")
        if check_signatures:
            if not _sig_ok(r):
                report.add("bad_signature", ln, seq, "signature does not verify")
            if r["key"].lower() != open_key.lower():
                report.add("untrusted_key", ln, seq, "signed by a different key from the open record")
        if r["session"] != report.session:
            report.add("session_mismatch", ln, seq, f"session {r['session'][:12]}... is not this receipt's")
        if seq != idx:
            report.add("sequence", ln, seq, f"seq {seq} at position {idx}")
        if r["type"] == "open" and idx > 0:
            report.add("sequence", ln, seq, "open record after the start")
        if idx == 0:
            if r["prev"] is not None:
                report.add("chain_broken", ln, seq, "first record has a prev")
        elif prev_rec is None:
            report.add("chain_broken", ln, seq, "record before it is unreadable")
        elif r["prev"] != record_hash(prev_rec):
            report.add("chain_broken", ln, seq, f"prev does not match the hash of line {prev_ln}")
        if prev_t is not None and r["t"] < prev_t:
            report.add("clock_backwards", ln, seq, f"t {r['t']} is earlier than the record before ({prev_t})")
        if r["type"] == "call":
            report.calls += 1
            if r["t_start"] > r["t"]:
                report.add("clock_backwards", ln, seq, "t_start is after t")
            if r.get("args") is not None and sha256_json(r["args"]) != r["args_sha256"]:
                report.add("digest_mismatch", ln, seq, "inline args do not hash to args_sha256")
            if r.get("result") is not None and sha256_json(r["result"]) != r.get("result_sha256"):
                report.add("digest_mismatch", ln, seq, "inline result does not hash to result_sha256")
        prev_rec, prev_ln, prev_t = r, ln, r["t"]

    last_ln, last = recs[-1]
    if rows[-1][1] is None or last["type"] != "close":
        report.add("unclosed", rows[-1][0], None, "last record is not a close: the receipt may be truncated")
    else:
        report.close_hash = record_hash(last)
        if last["count"] != report.calls:
            report.add("count_mismatch", last_ln, last["seq"], f"close says {last['count']} calls, file has {report.calls}")
    if anchor is not None and report.close_hash != anchor.lower():
        report.add("anchor_mismatch", last_ln, last["seq"],
                   f"close hash {str(report.close_hash)[:16]}... is not the published anchor {anchor[:16]}...")

    report.stale = stale_calls([r for _, r in recs], revoked)
    for ln, r in recs:
        if r["seq"] in report.stale and r["type"] == "call":
            report.add("stale", ln, r["seq"], "uses a revoked source, directly or through derived_from")
    return report


def stale_calls(records: list, revoked: Iterable[str]) -> list:
    """Custody's rule: a call is stale if any source is revoked, or it was derived from a stale call."""
    revoked = set(revoked)
    if not revoked:
        return []
    stale = set()
    for r in sorted((r for r in records if r.get("type") == "call"), key=lambda r: r["seq"]):
        if revoked.intersection(r.get("sources", [])) or stale.intersection(r.get("derived_from", [])):
            stale.add(r["seq"])
    return sorted(stale)


@dataclass
class ReplayReport:
    results: dict = field(default_factory=dict)    # seq -> (code, detail)

    def codes(self) -> set:
        return {c for c, _ in self.results.values()}

    def by_seq(self) -> dict:
        return {str(k): v[0] for k, v in sorted(self.results.items())}

    def __str__(self):
        return "\n".join(f"  seq {k:>3} {c:16} {d}" for k, (c, d) in sorted(self.results.items()))


def _replay_plan(path, tools):
    """Yield (seq, record, fn) for calls to re-run; record skipped calls in the report."""
    rr = ReplayReport()
    todo = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r.get("type") != "call":
            continue
        seq = r["seq"]
        if not r.get("replayable") or r["status"] == "fenced":
            rr.results[seq] = ("not_replayable", "not declared replayable" if not r.get("replayable") else "fenced")
        elif r.get("args") is None:
            rr.results[seq] = ("not_replayable", "args were redacted")
        elif tools.get(r["tool"]) is None:
            rr.results[seq] = ("not_replayable", f"no implementation given for {r['tool']}")
        else:
            todo.append((seq, r, tools[r["tool"]]))
    return rr, todo


def _judge(rr, seq, r, got):
    want = ("ok", r["result_sha256"]) if r["status"] == "ok" else ("error", r["error"])
    if got == want:
        rr.results[seq] = ("replay_match", "same result" if got[0] == "ok" else "same error")
    else:
        rr.results[seq] = ("replay_mismatch", f"recorded {want[0]} {str(want[1])[:24]}, re-run gave {got[0]} "
                                               f"{str(got[1])[:24]}")


def replay(path, tools: dict, *, encode: Callable | None = None) -> ReplayReport:
    """Re-run every call marked replayable with its recorded args and compare. Run `verify` first: replay trusts the file.
    Never re-runs a call that was not declared replayable, or that was fenced, or whose args were redacted.
    Use areplay() for async tools."""
    from .recorder import to_json
    encode = encode or to_json
    rr, todo = _replay_plan(path, tools)
    for seq, r, fn in todo:
        try:
            out = fn(**r["args"])
            if inspect.isawaitable(out):
                raise TypeError("async tool: use areplay()")
            got = ("ok", sha256_json(encode(out)))
        except Exception as e:
            got = ("error", f"{type(e).__name__}: {e}")
        _judge(rr, seq, r, got)
    return rr


async def areplay(path, tools: dict, *, encode: Callable | None = None) -> ReplayReport:
    """replay() for async tools (for example an MCP session's call_tool)."""
    from .recorder import to_json
    encode = encode or to_json
    rr, todo = _replay_plan(path, tools)
    for seq, r, fn in todo:
        try:
            out = fn(**r["args"])
            if inspect.isawaitable(out):
                out = await out
            got = ("ok", sha256_json(encode(out)))
        except Exception as e:
            got = ("error", f"{type(e).__name__}: {e}")
        _judge(rr, seq, r, got)
    return rr
