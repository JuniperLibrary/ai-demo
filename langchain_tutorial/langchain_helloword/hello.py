import dotenv
from langchain_openai import ChatOpenAI
import os

dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

llm = ChatOpenAI(model="gpt-4o-mini")

response = llm.invoke("什么是大模型？")
print(response)