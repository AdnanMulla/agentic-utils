# 🧠 Dynamic Math Agent (Multi-Step)

This project implements a Python-based agent that can classify and execute mathematical tasks using an LLM and MCP servers. It supports operations like GCD, LCM, addition, subtraction, and more by routing user queries to the appropriate computation server.

Just plug the MCP servers and let the agent do the magic. No seesion-ids / nodes / edges definition required !!

## 🚀 Usage

Make sure the MCP servers are running before starting the agent.

Requires following env vars:
- GOOGLE_API_KEY

Set the env var in `.env` file (follow `.env.template` file)

```bash
uv sync
uv run python main.py
```

## Example
```
(agentic-utils) C:\Users\Adnan\Desktop\Experiments\agentic-utils\agents\dynamic-math-agent>uv run python main.py
✅ Loaded 12 tools from MCP servers.
Enter a message:Find gcd of 20 and 30, add 5 to the result, then find lcm with 12

🧠 Agent output:
The GCD of 20 and 30 is 10. Adding 5 to this gives 15. The LCM of 15 and 12 is 60.
```

### Logs from MCP server to help understand what tools were called 

Numerics Server
```
2025-11-04 12:27:48,482 [INFO] Processing request of type CallToolRequest
2025-11-04 12:27:48,483 [INFO] [CALL] Tool: gcd
2025-11-04 12:27:48,483 [INFO] [INPUT] args=(), kwargs={'a': 20, 'b': 30}
2025-11-04 12:27:48,483 [INFO] [OUTPUT] 10

2025-11-04 12:27:53,025 [INFO] Processing request of type CallToolRequest
2025-11-04 12:27:53,025 [INFO] [CALL] Tool: lcm
2025-11-04 12:27:53,026 [INFO] [INPUT] args=(), kwargs={'a': 15, 'b': 12}
2025-11-04 12:27:53,026 [INFO] [OUTPUT] 60
```

Math Server
```
2025-11-04 12:27:51,345 [INFO] Processing request of type CallToolRequest
2025-11-04 12:27:51,346 [INFO] [CALL] Tool: add
2025-11-04 12:27:51,347 [INFO] [INPUT] args=(), kwargs={'a': 10.0, 'b': 5.0}
2025-11-04 12:27:51,347 [INFO] [OUTPUT] 15.0
```

