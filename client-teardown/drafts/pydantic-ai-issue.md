<!-- DRAFT for review. Not posted. Target: pydantic/pydantic-ai -->

# A dropped `MCPToolset` never stops its stdio server, so servers pile up when toolsets are built per request

## Summary

With FastMCP's default `keep_alive=True`, leaving `async with toolset` keeps the stdio subprocess running so the
next entry can reuse it. I understand that is intended (#12177 keeps the transport alive across activities on
purpose). FastMCP's `StdioTransport` still stops the subprocess when the transport is garbage collected, so a
plain FastMCP `Client` that goes out of scope cleans up after itself.

An `MCPToolset` never gets collected. `_build_message_handler()` returns a closure that holds the toolset
strongly, and FastMCP's keep-alive connection task holds that handler (through the session kwargs) for as long
as the subprocess runs. That makes a cycle the collector can't break: task → handler → toolset → client →
transport. The transport's finalizer never runs and the server never stops.

So a handler that builds a toolset per request (or a test suite that builds one per test) starts one more server
each time and none of them are ever stopped, even after `del toolset` and `gc.collect()`.

## Reproduction

pydantic-ai-slim 2.71.0, fastmcp-slim 4.2.4, Python 3.12.3, Linux. No model provider needed. `my_server.py` is
any stdio server that exits when its stdin closes.

```python
import asyncio, gc, subprocess
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from pydantic_ai.mcp import MCPToolset

def count():
    return subprocess.run(["pgrep", "-fc", "my_server.py"], capture_output=True, text=True).stdout.strip()

async def main():
    for _ in range(3):  # plain FastMCP client, dropped after use
        client = Client(StdioTransport(command="python", args=["my_server.py"]))
        async with client:
            await client.list_tools()
        del client
    gc.collect(); await asyncio.sleep(2)
    print("FastMCP Client:", count())  # 0

    for _ in range(3):  # same thing through MCPToolset
        toolset = MCPToolset(StdioTransport(command="python", args=["my_server.py"]))
        async with toolset:
            await toolset.client.list_tools()
        del toolset
    gc.collect(); await asyncio.sleep(2)
    print("MCPToolset:", count())  # 3

asyncio.run(main())
```

## Measured

10 trials, 3 toolsets per trial, each entered once and dropped, count taken 5 s later.

| | servers left per trial |
|---|---|
| pydantic-ai-slim 2.71.0 | 3 in 10/10 trials |
| with the patch below | 0 in 10/10 trials (also 0 in 5/5 without calling `gc.collect()`) |
| patched, one toolset entered twice | 1 server, reused, as before |

Toolsets from `load_mcp_toolsets()` behave the same way (3 left unpatched, 0 patched, same script).

## Possible fix

Have the handler hold the toolset weakly:

```diff
+    # FastMCP's keep-alive stdio connection task holds this handler for as long as the subprocess runs,
+    # so a strong reference would keep the toolset, its client and the transport reachable, and the
+    # transport's finalizer, which stops the subprocess, would never run.
+    toolset_ref = weakref.ref(toolset)
+
     async def handler(message: Any) -> None:
         notification = getattr(message, 'root', message)
-        if isinstance(notification, mcp_types.ToolListChangedNotification):
+        toolset = toolset_ref()
+        if toolset is None:
+            pass
+        elif isinstance(notification, mcp_types.ToolListChangedNotification):
```

This keeps keep-alive reuse unchanged and only affects toolsets nobody references any more. `tests/test_mcp.py`
passes with it (178 passed, 19 skipped).

A smaller related point: `docs/mcp/client.md` says entering and leaving the toolset will "start and stop the
subprocesses". With the default keep-alive that is not what happens on exit, so the line could say the server
stays up for reuse until the toolset is dropped, and mention `keep_alive=False` for code that wants it stopped
on exit.

Full harness, controls and raw trials: https://github.com/yatsuiii/reproduction-receipts/tree/claude/project-thread-757w48/client-teardown
