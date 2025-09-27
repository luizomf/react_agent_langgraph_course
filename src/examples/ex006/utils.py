from langchain.chat_models import BaseChatModel, init_chat_model


def load_llm() -> BaseChatModel:
    return init_chat_model("ollama:gpt-oss:20b", base_url="http://127.0.0.1:11434")
