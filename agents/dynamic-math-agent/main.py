import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()


async def main():
    # 1️⃣  Initialize your Gemini model
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    # 2️⃣  Connect to one or more MCP servers
    client = MultiServerMCPClient({
        "basic_math_server": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http",
        },
        "numerics_math_server": {
            "url": "http://127.0.0.1:8001/mcp",
            "transport": "streamable_http",
        },
    })

    # 3️⃣  Discover tools dynamically (no manual function defs!)
    tools = await client.get_tools()
    print(f"✅ Loaded {len(tools)} tools from MCP servers.")

    # 4️⃣  Define your persistent system prompt
    system_message = SystemMessage(
        content=(
            "You are a helpful assistant specialized in reasoning and using external tools.Do not perform any computation.\n"
            "Always explain your reasoning briefly before calling a tool.\n"
            "Always use tools and provide clear, concise answers."
        )
    )

    # 5️⃣  Build a prompt template that always includes system message
    prompt = ChatPromptTemplate.from_messages([
        system_message,
        MessagesPlaceholder(variable_name="messages"),
    ])

    # 6️⃣  Create a ReAct agent using the Gemini model + MCP tools + prompt
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=prompt
    )

    user_input = input("Enter a message:")

    # 7️⃣  Run the agent (async)
    result = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    })

    # 8️⃣  Print result
    print("\n🧠 Agent output:")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
