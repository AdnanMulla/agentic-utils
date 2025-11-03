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

### More info in each of the MCP Server README.md

