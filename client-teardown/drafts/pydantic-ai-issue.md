<!-- DRAFT for review. Not posted. Target: pydantic/pydantic-ai -->

# Leaving an `MCPToolset` does not stop its stdio server, so servers pile up when toolsets are built per request

## Summary

`docs/mcp/client.md` says `async with agent` / `async with toolset` will "open and close connections ... (and in the case of stdio servers, start and stop the subprocesses)", and that without a context manager "the toolset will be opened and closed automatically as needed".

With a stdio server the subprocess is not stopped. After the context exits (or `agent.run()` returns), the server keeps running for as long as the transport object lives, and in my runs it was still running after the toolset was deleted and `gc.collect()` was called. A handler that builds a toolset per request starts one more server per request and never stops any of them.

The cause looks like FastMCP's `StdioTransport` default `keep_alive=True`: `MCPToolset.__aexit__` closes the FastMCP client session, but with `keep_alive=True` the transport keeps the subprocess. `load_mcp_toolsets()` builds its `StdioTransport` with the default too.

## Reproduction

pydantic-ai-slim 2.71.0, fastmcp-slim 4.2.4, Python 3.12.3, Linux. No model provider needed.

```python
import asyncio, subprocess
from fastmcp.client.transports import StdioTransport
from pydantic_ai.mcp import MCPToolset

async def main():
    for _ in range(3):  # three "requests"
        toolset = MCPToolset(StdioTransport(command="python", args=["my_server.py"]))
        async with toolset:
            await toolset.client.list_tools()
        del toolset
    await asyncio.sleep(5)
    print(subprocess.run(["pgrep", "-fc", "my_server.py"], capture_output=True, text=True).stdout)

asyncio.run(main())
```

Expected: 0 servers running. Actual: 3. The server I used exits as soon as its stdin closes, so this means stdin was never closed.

## Measured

Each row is 10 trials. "Residue" means the server was still running 10 s after the toolset context exited (or the run returned).

| path | result |
|---|---|
| `async with MCPToolset(StdioTransport(...))` | residue 10/10 |
| `load_mcp_toolsets(config)` then `async with toolset` | residue 10/10 |
| `Agent(FunctionModel(...), toolsets=[toolset]).run(...)`, no context manager | residue 10/10 |
| same as row 1 with `StdioTransport(..., keep_alive=False)` | clean 10/10 |
| 3 fresh toolsets per trial, each entered and dropped | 3 servers left in 10/10 trials |

The same harness gives clean 10/10 for the MCP Python SDK, FastMCP's own `Client`, Agno, LangChain, LlamaIndex, OpenAI Agents SDK and others, so the measurement is not inventing residue.

## Possible fix

Close the stdio transport when the last context exits:

```diff
             if self._running_count == 0 and self._exit_stack is not None:
                 await self._exit_stack.aclose()
                 self._exit_stack = None
+                # FastMCP's StdioTransport defaults to keep_alive=True, which keeps the
+                # subprocess running after the client session closes. Leaving the toolset is
+                # documented to stop the subprocess, so close the transport too.
+                transport = getattr(self.client, 'transport', None)
+                if isinstance(transport, StdioTransport) and transport.keep_alive:
+                    await transport.close()
```

With this, every row above comes out clean 10/10, the per-request test leaves 0 servers in 10/10 trials, and `tests/test_mcp.py` passes (178 passed, 19 skipped). Passing `keep_alive=False` in `load_mcp_toolsets()` would be a smaller change but would not cover a user-built `StdioTransport`. If keeping the server warm between `async with` blocks is intended, then the docs line about stopping subprocesses is what needs changing, and the per-request pile-up is still worth a warning.

Full harness, controls and raw trials: <link to receipt>
