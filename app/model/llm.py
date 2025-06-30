from langchain_together import Together
import os
from dotenv import load_dotenv

load_dotenv()

llm = Together(
    model="meta-llama/Llama-3-8b-chat-hf",
    temperature=1,
    api_key=os.getenv("TOGETHER_API_KEY")
)


