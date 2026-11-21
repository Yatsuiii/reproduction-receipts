"""A small MCP server for the worked example (mcp 2.x, stdio). KB_VERSION=2 simulates the knowledge base changing upstream."""
import os

from mcp.server.mcpserver import MCPServer

server = MCPServer("support-kb")
KB = {
    "1": {"refund": ["kb/refunds.md#30-days", "kb/billing.md"], "shipping": ["kb/shipping.md"]},
    "2": {"refund": ["kb/refunds-2027.md#14-days"], "shipping": ["kb/shipping.md"]},
}[os.environ.get("KB_VERSION", "1")]
NOTES = {"policy.txt": "Refunds within 30 days of delivery. Escalate anything older to billing."}
ORDERS = {"A-100": {"delivered_days_ago": 12, "total": 49.0}}


@server.tool()
def read_note(name: str) -> dict:
    """Read an internal note."""
    return {"name": name, "text": NOTES[name]}


@server.tool()
def search_kb(query: str) -> dict:
    """Search the support knowledge base."""
    return {"query": query, "hits": [h for k, v in KB.items() if k in query for h in v]}


@server.tool()
def lookup_order(order_id: str) -> dict:
    """Look up an order."""
    if order_id not in ORDERS:
        raise ValueError(f"no order {order_id}")
    return {"order_id": order_id, **ORDERS[order_id]}


@server.tool()
def send_reply(to: str, body: str) -> dict:
    """Send a reply to a customer (side effect; the example only pretends)."""
    return {"queued": True, "to": to, "chars": len(body)}


if __name__ == "__main__":
    import anyio
    anyio.run(server.run_stdio_async)
