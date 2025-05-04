from langchain_groq import ChatGroq

from dotenv import load_dotenv
import os
load_dotenv(".env")

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key = api_key
)

messages = [
    ("system", "You are a web search chatbot assistant."),
    ("human", "what is the weather today?"),
]

result = llm.invoke(messages)

print(result.content)