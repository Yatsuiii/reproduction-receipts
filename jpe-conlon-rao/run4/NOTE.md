# Run 4: stopped by the machine, not by the package

Run 4 (same [`spec3.json`](../spec3.json) as run 3) started 2026-11-25 17:32 UTC on the cloud container and was killed
when the container restarted, before 18:03 UTC, again during the main estimation with no step finished or failed. This
container restarts when the session is idle, so it cannot hold a run of about 20 hours, and GitHub-hosted runners stop
jobs at 6 hours. The full estimation needs a machine that stays up for a day; nothing in this directory is a result.
