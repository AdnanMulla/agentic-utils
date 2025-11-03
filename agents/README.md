# Agents
**Agent‑orchestration code for multi‑step tool workflows**  

This directory contains the agent logic used with the MCP tool servers (in `mcp‑servers/`). The agent is designed to parse user queries, plan multiple tool calls, execute those calls, and return results to the user.

## Example of running smart-math-agent

```bash
$ uv run python main.py
💬 User Query: Add 5 and 3, then find gcd of that result with 4
📝 Generated Plan: { "steps": [ ... ] }
▶️ Executing Step 1/2: add
   🧮 Arguments: a=5, b=3
✅ Step 1 Result: 8
▶️ Executing Step 2/2: gcd
   🧮 Arguments: a=<previous_result>, b=4
✅ Step 2 Result: 4
🏁 Final Result: 4
```

### More info in each of the agent README.md
