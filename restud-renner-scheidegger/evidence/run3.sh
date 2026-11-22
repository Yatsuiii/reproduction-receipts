#!/bin/bash
# Fresh checkout, Steps 2 and 4 unchanged except N_PROCS=4, with OMP_NUM_THREADS=1 in the environment.
set -u
cd /home/claude && rm -rf run3 && git clone -q https://github.com/GaussianProcessesForDynamicEcon/DynamicIncentiveProblems run3 && cd run3 && git checkout -q 374fe17a6a21bb137c469260a7e1f72f2c6246ed
(git ls-files -s | awk '$1 != "120000" {print $4}' | xargs sha256sum) | diff - /home/claude/receipt/package-files.sha256 > /home/claude/receipt/logs/run3-hashcheck.txt && echo "run3 package hashes match run1" >> /home/claude/receipt/logs/SUMMARY.txt
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 OMP_NUM_THREADS=1
/home/claude/receipt/scripts/step.sh run3_2_replicate_original /home/claude/run3 bash ./2_replicate_original.sh
sed -i 's/^N_PROCS=16 /N_PROCS=4 /' 4_validate_BE.sh
git diff 4_validate_BE.sh > /home/claude/receipt/run3-deviation-nprocs.diff
/home/claude/receipt/scripts/step.sh run3_4_validate_BE /home/claude/run3 bash ./4_validate_BE.sh
rm -rf /home/claude/receipt/outputs/run3_step4; cp -r figure_replication/figure_and_table_outputs/4 /home/claude/receipt/outputs/run3_step4
git status --short > /home/claude/receipt/run3-status-after-step4.txt
echo RUN3_DONE >> /home/claude/receipt/logs/SUMMARY.txt
