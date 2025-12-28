# To install: pip install tavily-python
from tavily import TavilyClient
import os
import dotenv
dotenv.load_dotenv()

client = TavilyClient(os.getenv("TAVILY_API_KEY"))
response = client.search(
    query="今天的北京天气情况怎么样"
)
print(response)