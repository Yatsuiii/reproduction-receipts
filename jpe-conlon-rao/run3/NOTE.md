# Run 3: stopped by the machine, not by the package

Run 3 started 2026-11-25 16:55 UTC on the cloud container. The container restarted at about 17:29 UTC while the main
estimation was still solving, which killed every process. The last log line is the estimator's own progress message
("Updating starting values for the weighting matrix and delta ..."); no step had finished or failed.

Nothing in this directory is a result. Run 4 uses the same spec ([`../spec3.json`](../spec3.json)) unchanged, from a fresh
clone, and is the run the receipt reports.

`spec3.json`'s environment command reads the virtual environment at the fixed path `/tmp/claude-0/jpe-work3/checkout/venv`.
For run 4 that path is a symbolic link to run 4's own work directory, so the recorded package versions are run 4's.
