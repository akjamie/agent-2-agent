# Example LangChain Studio integration
from app.config.config import Configuration

def get_langchain_client(config: Configuration):
    # Use config.LANGCHAIN_API_KEY and config.LANGCHAIN_ENDPOINT
    return {
        "api_key": config.LANGCHAIN_API_KEY,
        "endpoint": config.LANGCHAIN_ENDPOINT
    }

