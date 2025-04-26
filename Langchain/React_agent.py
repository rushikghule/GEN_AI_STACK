from langchain_google_genai import GoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain.agents import initialize_agent,tool
from langchain_community.tools import TavilySearchResults
import datetime

load_dotenv(".env")

api_key = os.getenv("GROQ_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
# llm=GoogleGenerativeAI()
# print(api_key)
# response = llm.invoke("What is the capital of France?")
# print(response)

chat = ChatGroq(model="llama-3.1-8b-instant",api_key=api_key)

# Response = chat.invoke("What is the capital of France?")
# print("Result: ",Response.content)

# ------------------------------------------------------------------------------------------------------------------------

search_tool = TavilySearchResults(search_depth="basic",api_key=tavily_api_key)

@tool
def get_system_date(format:str = "%Y-%m-%d %H:%M:%S"):
    """Get the current date in a specified format."""
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

tools = [search_tool,get_system_date]

Agent = initialize_agent(tools=tools,llm=chat,agent="zero-shot-react-description",verbose=True)

Response = Agent.invoke("when was the space-x last launched? and how many days ago was that from this instant?")
print("Result: ",Response.content)