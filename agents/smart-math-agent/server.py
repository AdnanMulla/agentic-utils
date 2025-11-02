"""
Run this file only if you want to use the agent as server
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from main import graph

app = FastAPI()


@app.post("/agent")
async def agent_endpoint(request: Request):
    data = await request.json()
    user_input = data.get("query")

    result_state = graph.invoke(
        {"messages": [{"role": "user", "content": user_input}]})
    final_message = result_state["messages"][-1].content

    return JSONResponse({"response": final_message})
