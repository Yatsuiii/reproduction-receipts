#!/bin/sh
# Does the host process exit on its own after client.close()?
# usage: AI_SDK_MCP=<path to node_modules/@ai-sdk/mcp> sh run.sh [trials]
# Prints the exit code per trial: 0 = host exited, 124 = still running after 12 s.
n=${1:-10}; here=$(dirname "$0"); codes=""
for i in $(seq "$n"); do
  timeout 12 node "$here/client.mjs" >/dev/null 2>&1; codes="$codes $?"
  pkill -9 -f "$here/server.mjs"
done
echo "exit codes:$codes"
