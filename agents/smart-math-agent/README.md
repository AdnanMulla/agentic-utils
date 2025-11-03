# 🧠 Smart Math Agent (Multi-Step)

This project implements a Python-based agent that can classify and execute mathematical tasks using an LLM and MCP servers. It supports operations like GCD, LCM, addition, subtraction, and more by routing user queries to the appropriate computation server.


## 🤖 Agent Workflow

- User Input: Read the query from the user.
- Planner Node: Use LLM to prepare a plan to execute the user query.
- Executor Node: Execute the steps listed in the plan. Call the tool from the appropriate MCP server as per the plan.
- Return Result: Display the tool’s result to the user.

## 🚀 Usage

Make sure the MCP servers are running before starting the agent.

Requires following env vars:
- GOOGLE_API_KEY
- BASIC_MATH_SERVER_URL
- NUMERICS_MATH_SERVER_URL
- BASIC_MATH_SERVER_SESSION_ID (run `client.py` in mcp-server to get this value)
- NUMERICS_MATH_SERVER_SESSION_ID (run `client.py` in mcp-server to get this value)

Set the env var in `.env` file (follow `.env.template` file)

```
uv sync
uv run python main.py
```


### 🏗️ Architecture

![Smart Math Agent](assets/smart-math-agent-architecture.png)

### ✨ Smart Math Agent

![Smart Math Agent](assets/smart-math-agent.png)

### ✨Chat Interface (we can use agent-chat-ui by langsmith to use deployed UI and run our langgraph as server)

```
uv sync
uv run langgraph dev
```

![Local server](assets/local-server.png)

https://agentchat.vercel.app/?apiUrl=http://127.0.0.1:2024&assistantId=smart_math_agent

![Chat Interface](assets/chat-interface.png)

### ✨Running the agent as server (only for local development, not to be used with chat-ui)
```
uv run uvicorn server:app --reload --port 7000
```

![Agent as server](assets/server.png)

## Example Queries for Multi-Step Math Agent

These queries can be used to test the multi-step agent that calls MCP tools (`add`, `subtract`, `gcd`, `lcm`) and supports dependent results (`<previous_result>`).

---

## Single-Step Queries

| #  | Query                              | Description                     |
|----|------------------------------------|---------------------------------|
| 1  | Add 5 and 3                         | Simple addition                 |
| 2  | Subtract 2 from 10                  | Simple subtraction              |
| 3  | Find gcd of 12 and 18               | GCD calculation                 |
| 4  | Find lcm of 4 and 6                  | LCM calculation                 |


---

## Two-Step Queries (Dependent Steps)

| #  | Query                                                     | Description                                       |
|----|-----------------------------------------------------------|-------------------------------------------------|
| 1  | Add 5 and 3, then find gcd of that result with 4         | Uses result of addition in GCD calculation     |
| 2 | Subtract 2 from 10, then find lcm with 6                 | Uses result of subtraction in LCM calculation  |
| 3 | Find gcd of 12 and 18, then add 7 to it                  | Uses GCD result in addition                     |
| 4 | Find lcm of 4 and 6, then subtract 5                      | Uses LCM result in subtraction                  |
| 5 | Add 10 and 5, then add 2 to that result                  | Sequential additions                             |
| 6 | Subtract 8 from 20, then find gcd of that result with 12 | Subtraction then GCD                             |

---

## Three-Step Queries (Complex Multi-Step Chains)

| #  | Query                                                                 | Description                                       |
|----|-----------------------------------------------------------------------|-------------------------------------------------|
| 1 | Add 5 and 2, subtract 3 from that result, then find gcd with 4       | Chain: addition → subtraction → GCD             |
| 2 | Find gcd of 20 and 30, add 5 to the result, then find lcm with 12    | Chain: GCD → addition → LCM                     |
| 3 | Subtract 10 from 50, add 7, then find gcd with 14                     | Subtraction → addition → GCD                    |
| 4 | Add 6 and 4, find lcm of that result with 8, then subtract 3         | Addition → LCM → subtraction                     |
| 5 | Find lcm of 3 and 5, add 10, then find gcd with 15                     | LCM → addition → GCD                             |
| 6 | Add 2 and 3, add 4 to that result, then subtract 5                    | Sequential addition → subtraction               |

---

### Notes

* Multi-step queries test the agent's ability to use `<previous_result>` from prior steps.
* You can modify numbers or reorder steps to create more test cases.
* Use logging (`▶️`, `🧮`, `✅`) to track execution step-by-step.
