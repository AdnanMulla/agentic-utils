import os
import logging
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated, Literal, List, Union
from pydantic import BaseModel, Field
from system_prompt import system_prompt_multi
from mcp_utils import (
    call_mcp_tool_jsonrpc,
    BASIC_MATH_SERVER_URL,
    NUMERICS_MATH_SERVER_URL,
)

print("=========================================START================================")

load_dotenv()

# Logging setup
log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
log_level = getattr(logging, log_level_str, logging.INFO)
logging.basicConfig(
    level=log_level, format="%(asctime)s [%(levelname)s] %(message)s"
)

# ----- LLM  -----
llm = init_chat_model(
    "gemini-2.5-flash",
    model_provider="google-genai"
)

# ----- Structured type -----


class Arguments(BaseModel):
    a: str
    b: str


class Step(BaseModel):
    server: Literal["basic_math",
                    "numerics_math"] = Field(..., description="Which MCP server to use.")
    tool: Literal["add", "subtract", "gcd",
                  "lcm"] = Field(..., description="The specific tool to call")
    arguments: Arguments


class MultiStepPlan(BaseModel):
    steps: List[Step]

# ----- State definition ------


class State(TypedDict):
    messages: Annotated[list, add_messages]
    plan: MultiStepPlan | None
    tool_result: float | None


graph_builder = StateGraph(State)


# ----- Nodes -----


PLAN_NODE = "plan"
EXECURE_NODE = "execute_steps"
RESPOND_NODE = "respond"


# ----- Node: plan_node
def plan_node(state: State):
    """Use LLM to convert a user query into a structured MultiStepPlan."""
    last_message = state["messages"][-1]

    logging.info("💬 User Query: %s", last_message.content)

    planner = llm.with_structured_output(MultiStepPlan)

    try:
        result: MultiStepPlan = planner.invoke([
            {"role": "system", "content": system_prompt_multi},
            {"role": "user", "content": last_message.content}
        ])
    except Exception as e:
        logging.error(f"Planning failed: {e}")
        raise

    state["plan"] = result.model_dump()

    logging.info("📝 Generated Plan: %s", state.get("plan"))

    return state

# ----- Node: execute_node


def execute_node(state: State):
    """Execute each step from the plan sequentially, chaining results."""

    plan = state.get("plan")
    if not plan or "steps" not in plan:
        raise ValueError("No plan found in state")

    previous_result = None

    for idx, step_dict in enumerate(plan["steps"]):
        logging.info("▶️ Executing Step %d/%d: %s", idx +
                     1, len(plan["steps"]), step_dict['tool'])

        step = Step(**step_dict)

        def resolve(arg: str) -> float:
            if arg == "<previous_result>":
                if previous_result is None:
                    raise ValueError(
                        "No previous result to use for <previous_result>")
                return previous_result
            return float(arg)

        resolved_args = {
            "a": resolve(step.arguments.a),
            "b": resolve(step.arguments.b)
        }
        logging.debug("   🧮 Arguments: a=%s, b=%s",
                      resolved_args["a"], resolved_args["b"])

        if step.server == "basic_math":
            server_url = BASIC_MATH_SERVER_URL
        else:
            server_url = NUMERICS_MATH_SERVER_URL

        result = call_mcp_tool_jsonrpc(server_url, step.tool, resolved_args)

        previous_result = float(result)
        logging.info("✅ Step %d Result: %s", idx+1, previous_result)

    state["tool_result"] = previous_result
    return state

# ----- Node: respond


def respond(state: State):
    result = state.get("tool_result")
    logging.info("🏁 Final Result: %s", result)
    return {"messages": [{"role": "assistant", "content": f"Result: {result}"}]}


# ----- Add nodes -----

graph_builder.add_node(PLAN_NODE, plan_node)
graph_builder.add_node(EXECURE_NODE, execute_node)
graph_builder.add_node(RESPOND_NODE, respond)

# ----- Add edges -----

graph_builder.add_edge(START, PLAN_NODE)
graph_builder.add_edge(PLAN_NODE, EXECURE_NODE)
graph_builder.add_edge(EXECURE_NODE, RESPOND_NODE)
graph_builder.add_edge(RESPOND_NODE, END)

# ----- Compilte graph -----

graph = graph_builder.compile(name="smart_math_agent")

# ----- Invoke graph -----

if __name__ == "__main__":
    user_input = input("Enter a message: ")
    state = graph.invoke(
        {"messages": [{"role": "user", "content": user_input}]})


print("=========================================END==================================")
