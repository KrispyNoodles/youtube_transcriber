from dotenv import dotenv_values
from supadata import Supadata

config = dotenv_values(".env")

SUPADATA_API_KEY=config.get("SUPADATA_API_KEY")

# Initialize the client
supadata = Supadata(api_key=SUPADATA_API_KEY)

from langchain_openai import AzureChatOpenAI

API_KEY=config.get("API_KEY")
API_ENDPOINT=config.get("ENDPOINT")
API_MODEL=config.get("MODEL")

# Initialize the LLM
llm = AzureChatOpenAI(
                model=API_MODEL, 
                openai_api_version="2024-05-01-preview",
                temperature=0,
                api_key= API_KEY,
                azure_endpoint=API_ENDPOINT
                )
