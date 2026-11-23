#!/bin/bash
cd /home/claude/receipt2
for s in value_estimation/inventory_control value_estimation/ttt3x3_value_estimation value_estimation/ttt4x4_value_estimation policy_performance/ttt4x4_random policy_performance/ttt4x4_softmax value_estimation/intruder_monitor; do
  n=$(basename $s)
  rm -rf work/$n; git clone -q https://github.com/INFORMSJoC/2024.0863 work/$n
  (cd work/$n && git ls-files | while read f; do sha256sum "$f"; done | diff -q - /home/claude/receipt2/package-files.sha256 && echo "hash ok") > logs/$n.hashcheck.txt 2>&1
  ./step.sh $n work/$n /home/claude/receipt2/venv/bin/python scripts/$s.py
done
echo ALLDONE >> logs/SUMMARY.txt
