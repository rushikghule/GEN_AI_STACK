# langchain_mcp_client.py  (fixed for langchain-mcp-adapters 0.1.0+)

import asyncio
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyBx7AweqVuomkT1QwXbHfbj4tXW_SjiQBk")

async def main():
    # 1. Set up Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
    )

    # 2. Create client WITHOUT async with (new API in 0.1.0+)
    client = MultiServerMCPClient(
        {
            "demo": {
                "command": "python",
                "args": ["mcp_server.py"],
                "transport": "stdio",
            }
        }
    )

    # 3. Get tools — note: await is required now
    tools = await client.get_tools()
    print(f"✅ Tools available: {[t.name for t in tools]}\n")

    # 4. Create agent using langgraph
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt="You are a helpful assistant. Always use tools to compute exact answers.",
    )

    # 5. Run queries
    questions = [
        "What is (25 * 4) + (100 / 5)?"
    ]

    for q in questions:
        print(f"\n{'='*55}")
        print(f"❓ {q}")
        print('='*55)
        result = await agent.ainvoke({"messages": [HumanMessage(content=q)]})
        print(f"💡 Answer: {result['messages'][-1].content}")

if __name__ == "__main__":
    asyncio.run(main())