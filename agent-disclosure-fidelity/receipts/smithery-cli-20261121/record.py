"""Records the per-trial numbers behind the smithery-cli receipt (10 broken, 10 fixed)."""
import dataclasses, json, sys, time
from shutdown_integrity import runner
from shutdown_integrity.adapters.smithery_cli.harness import UPLINK_STDIO_LEAKS_TREE_HARNESS as H
from shutdown_integrity.scenarios.smithery_cli import SCENARIO_UPLINK_STDIO_LEAKS_TREE as S

out = {}
for name, fx in (("unpatched", S.broken_control), ("patched", S.fixed_control)):
    t0 = time.time()
    r = runner.run(S, fx, H, trials=10, settle_deadline_s=3.0)
    d = dataclasses.asdict(r)
    d["wall_clock_s"] = round(time.time() - t0, 1)
    out[name] = d
json.dump(out, sys.stdout, indent=2, default=str)
