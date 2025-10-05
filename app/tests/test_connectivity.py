from app.config.config import Configuration
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_deepseek import ChatDeepSeek
from app.services.log_util import LogUtil

PROMPT = "Hello, are you online?"


def test_tongyi():
    config = Configuration()
    if not config.DASHSCOPE_API_KEY:
        LogUtil.error("DASHSCOPE_API_KEY not set in .env")
        return
    llm = ChatTongyi(api_key=config.DASHSCOPE_API_KEY, model="qwen-plus-2025-07-28")
    try:
        result = llm.invoke(PROMPT)
        LogUtil.info(f"Tongyi (Qwen) response: {result}")
    except Exception as e:
        LogUtil.error(f"Tongyi (Qwen) error: {e}", exc=e)


def test_deepseek():
    config = Configuration()
    if not config.DEEPSEEK_API_KEY:
        LogUtil.error("DEEPSEEK_API_KEY not set in .env")
        return
    llm = ChatDeepSeek(api_key=config.DEEPSEEK_API_KEY, model="deepseek-chat")
    try:
        result = llm.invoke(PROMPT)
        LogUtil.info(f"Deepseek response: {result}")
    except Exception as e:
        LogUtil.error(f"Deepseek error: {e}", exc=e)


if __name__ == "__main__":
    LogUtil.info("Testing Tongyi (Qwen) connectivity...")
    test_tongyi()
    LogUtil.info("\nTesting Deepseek connectivity...")
    test_deepseek()
