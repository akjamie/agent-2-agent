from pydantic_settings import BaseSettings

class Configuration(BaseSettings):
    DASHSCOPE_API_KEY: str = ""
    HUGGINGFACEHUB_API_TOKEN: str = ""
    TAVILY_API_KEY: str = ""
    QDRANT_URL: str = ""
    QDRANT_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_ENDPOINT: str = ""

    LANGSMITH_API_KEY: str = ""
    LANGSMITH_TRACING: str = ""
    LANGSMITH_ENDPOINT: str = ""
    LANGSMITH_PROJECT: str = ""

    class Config:
        env_file = "../../.env"

def get_config() -> Configuration:
    return Configuration()