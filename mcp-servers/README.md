# MCP Servers

This directory contains a collection of light‑weight MCP servers that expose simple math operations—useful for agent workflows, chaining tools, and demonstration of multi‑step reasoning. These servers adhere to the MCP standard and can be invoked by agents or other tools.

## 🚀 Why this exists  
- Enable agents to offload computation (e.g., basic math, number theory) to tools rather than doing everything internally.  
- Provide a clean separation between reasoning (via the agent / LLM) and execution (via the MCP server).  
- Offer a reproducible setup for experimentations in agent‑tool collaboration using MCP.

## 🧮 What’s included  
- **basic‑math**: Provides simple arithmetic tools such as `add`, `subtract`.  
- **number‑theory**: Provides mathematical tools such as `gcd`, `lcm`.  
- Each server implements standardized MCP tool endpoints to allow discovery, invocation and chaining.

## How to use?

1. Run python server
1. Use python client to get sessionId.
2. Use the sessionId to make subsequent calls.

## How to run server ?
- Install dependencies `uv add fastmcp`
- Run `uv run python server.py`

## How to run python client ?
- Run `uv run python client.py`

![Capture Session Id from client](client.png)

## How to list and invoke mcp tools ? 

Refer to `list_tools.ps1` and `call_tool.ps1` scripts.

1. Sample output for `list_tools` 

`data: {"jsonrpc":"2.0","id":2,"result":{"tools":[{"name":"add","description":"Add two numbers.","inputSchema":{"properties":{"a":{"type":"integer"},"b":{"type":"integer"}},"required":["a","b"],"type":"object"},"outputSchema":{"properties":{"result":{"type":"integer"}},"required":["result"],"type":"object","x-fastmcp-wrap-result":true},"_meta":{"_fastmcp":{"tags":[]}}}]}}`

2. Sample output for `call_tool` 

`data: {"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"8"}],"structuredContent":{"result":8},"isError":false}}`

