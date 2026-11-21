#!/bin/bash
# usage: step.sh <name> <workdir> <command...>   logs stdout/stderr, exit code, wall clock
name=$1; dir=$2; shift 2
log=/home/claude/receipt/logs/$name.log
export PATH=/opt/miniforge/bin:$PATH
cd "$dir"
start=$(date -u +%s); echo "# step=$name start=$(date -u +%FT%TZ) cwd=$dir cmd=$*" > $log
"$@" >> $log 2>&1; rc=$?
end=$(date -u +%s)
echo "# step=$name end=$(date -u +%FT%TZ) exit=$rc wall_s=$((end-start))" >> $log
echo "$name exit=$rc wall_s=$((end-start))" >> /home/claude/receipt/logs/SUMMARY.txt
