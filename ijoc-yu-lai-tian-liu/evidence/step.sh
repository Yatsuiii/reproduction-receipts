#!/bin/bash
name=$1; dir=$2; shift 2
log=/home/claude/receipt2/logs/$name.log
cd "$dir"
start=$(date -u +%s); echo "# step=$name start=$(date -u +%FT%TZ) cwd=$dir cmd=$*" > $log
"$@" >> $log 2>&1; rc=$?
end=$(date -u +%s)
echo "# step=$name end=$(date -u +%FT%TZ) exit=$rc wall_s=$((end-start))" >> $log
echo "$name exit=$rc wall_s=$((end-start))" >> /home/claude/receipt2/logs/SUMMARY.txt
