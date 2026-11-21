"""Build the target list from the official MCP registry.

    python mcp-teardown/targets.py --limit 1000 --out mcp-teardown/targets.jsonl

Reads https://registry.modelcontextprotocol.io/v0/servers (public, no auth),
keeps the latest active version of each server that ships a stdio package on
npm or PyPI and names a GitHub repository, drops servers whose launch needs a
value we cannot supply honestly (a required argument with no default), and
keeps one server per repository.

Ordering is deterministic so the list can be rebuilt and diffed: servers that
need no required environment variables first (fewer placeholder deviations in
the receipt), then most recently updated. The raw registry snapshot is written
next to the list with its SHA-256, so the receipt can name exactly which
registry state the target came from.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

REGISTRY = "https://registry.modelcontextprotocol.io/v0/servers"
META = "io.modelcontextprotocol.registry/official"


def fetch_all(page_size: int = 100) -> list[dict]:
    servers: list[dict] = []
    cursor = None
    while True:
        url = f"{REGISTRY}?limit={page_size}"
        if cursor:
            url += "&cursor=" + urllib.parse.quote(cursor)
        for attempt in range(4):
            try:
                with urllib.request.urlopen(url, timeout=60) as resp:
                    page = json.load(resp)
                break
            except OSError:
                if attempt == 3:
                    raise
                time.sleep(2 ** attempt)
        servers.extend(page["servers"])
        cursor = page.get("metadata", {}).get("nextCursor")
        if not cursor:
            return servers


def _github_repo(server: dict) -> str | None:
    url = ((server.get("repository") or {}).get("url") or "").strip().rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    if not url.startswith("https://github.com/"):
        return None
    parts = url[len("https://github.com/"):].split("/")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        return None
    return f"{parts[0]}/{parts[1]}"


def _args_ok(args: list[dict]) -> tuple[bool, list[str]]:
    """Flatten registry arguments into argv. A required argument with no
    default or fixed value cannot be filled without inventing it, so the
    server is skipped rather than launched with a made-up value."""
    argv: list[str] = []
    for arg in args or []:
        value = arg.get("value", arg.get("default"))
        if value is None:
            if arg.get("isRequired"):
                return False, []
            continue
        if arg.get("type") == "named":
            argv.append(arg.get("name", ""))
        argv.append(str(value))
    return True, [a for a in argv if a != ""]


def select(servers: list[dict]) -> list[dict]:
    picked: dict[str, dict] = {}
    for entry in servers:
        meta = entry.get("_meta", {}).get(META, {})
        if not meta.get("isLatest") or meta.get("status") != "active":
            continue
        server = entry["server"]
        repo = _github_repo(server)
        if not repo:
            continue
        for pkg in server.get("packages") or []:
            if pkg.get("registryType") not in ("npm", "pypi"):
                continue
            if (pkg.get("transport") or {}).get("type") != "stdio":
                continue
            ok, pkg_argv = _args_ok(pkg.get("packageArguments"))
            if not ok:
                continue
            env = pkg.get("environmentVariables") or []
            required_env = sorted(
                v["name"] for v in env if v.get("isRequired") and v.get("name") and not v.get("default")
            )
            defaults_env = {
                v["name"]: str(v["default"]) for v in env if v.get("name") and v.get("default") is not None
            }
            target = {
                "name": server["name"],
                "version": server.get("version"),
                "repo": repo,
                "subfolder": (server.get("repository") or {}).get("subfolder"),
                "registry_type": pkg["registryType"],
                "identifier": pkg["identifier"],
                "package_version": pkg.get("version"),
                "package_args": pkg_argv,
                "required_env": required_env,
                "default_env": defaults_env,
                "updated_at": meta.get("updatedAt") or meta.get("publishedAt"),
            }
            key = repo.lower()
            prev = picked.get(key)
            # One server per repository: a maintainer gets at most one receipt
            # from this batch. Prefer the entry with fewer required env vars.
            if prev is None or (len(required_env), prev["updated_at"] or "") < (
                len(prev["required_env"]),
                target["updated_at"] or "",
            ):
                picked[key] = target
            break
    out = list(picked.values())
    out.sort(key=lambda t: t["updated_at"] or "", reverse=True)
    out.sort(key=lambda t: len(t["required_env"]))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=1000)
    ap.add_argument("--out", type=Path, default=Path(__file__).parent / "targets.jsonl")
    ap.add_argument("--snapshot", type=Path, help="reuse a saved registry snapshot instead of fetching")
    args = ap.parse_args(argv)

    if args.snapshot:
        raw = args.snapshot.read_bytes()
    else:
        raw = json.dumps(fetch_all(), sort_keys=True).encode()
        snap = args.out.with_suffix(".registry.json")
        snap.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    servers = json.loads(raw)
    targets = select(servers)
    with args.out.open("w") as fh:
        for t in targets[: args.limit]:
            t["registry_snapshot_sha256"] = digest
            fh.write(json.dumps(t, sort_keys=True) + "\n")
    print(
        f"registry entries {len(servers)}, eligible {len(targets)}, written {min(len(targets), args.limit)}, "
        f"snapshot sha256 {digest}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
