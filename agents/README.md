# Agents
**Agent‑orchestration code for multi‑step tool workflows**  

This directory contains the agent logic used with the MCP tool servers (in `mcp‑servers/`). The agent is designed to parse user queries, plan multiple tool calls, execute those calls, and return results to the user.

## 🚀 Why this folder exists  
- To separate **reasoning and orchestration** (agent) from **execution** (MCP servers).  
- To support multi‑step workflows where the output of one tool is used in the next.  
- To provide a reusable framework for agent‑tool integration, logging, and planning.  
- To demonstrate a clean pipeline: user query → planning → execution → result.

## 🧠 What’s included  
- A LangGraph‑based agent (`graph_builder`, nodes for planning, executing, responding)  
- Prompting logic to convert user natural‑language into structured plans  
- Logging instrumentation (step‑by‑step, arguments, results) to trace agent behaviour  
- Example queries for testing (screenshots below)

## 📦 Getting started  
1. Make sure the MCP servers (in `mcp‑servers/`) are running and reachable. (Applicable only if you are using math agents)
2. Install dependencies (e.g., `langgraph`, `langchain`, `pydantic`, etc.).  
3. Configure `.env` with any needed API keys or session IDs.  
4. Run the agent script (for example `uv run python main.py`).  
5. Enter a user query in the prompt, e.g., `Add 5 and 3, then find gcd of that result with 4`.  
6. Observe step‑by‑step logging and final result output.

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

## How to run ?

- Install dependencies `uv add python-dotenv langgraph "langchain[google-genai]" ipykernel`
- Verify the `pyproject.toml` file
- Specify env vars in `.env` file - copy the `.env.template` and create `.env` file
- Run the code `uv run python main.py`

## Usage

1. Smart Math Agent

- User inputs in the terminal
- START -> classify_input -> call_tool -> respond -> END

![Smart Math Agent](smart-math-agent/smart-math-agent.png)


2. Simple Math Agent

- User inputs in the terminal
- START -> classify_input -> call_tool -> respond -> END

![Simple Math Agent](simple-math-agent/numerics_server.png)

3. Simple Chatbot 
- User inputs in the terminal
- START -> chatbot -> END

![Simple chatbot](simple-chatbot.png)

4. Smart Chatbot (2 agents)
- User inputs in the terminal
- START -> Classify_message -> router -> (logical | therapist) -> END

![Smart chatbot](smart-chatbot.png)