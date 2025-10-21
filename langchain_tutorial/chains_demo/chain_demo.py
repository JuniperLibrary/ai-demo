from dotenv import load_dotenv
from langchain_core.output_parsers import  StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()
chat_model = ChatOpenAI(model="gpt-4o-mini")

prompt_template = PromptTemplate.from_template(template="给我讲一个{topic}话题的简短笑话")

parser = StrOutputParser()

chain = prompt_template | chat_model | parser

response_message = chain.invoke({"topic":"ice_cream"})

print(response_message)
print(type(response_message))