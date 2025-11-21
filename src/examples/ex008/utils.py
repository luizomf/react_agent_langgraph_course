# ruff: noqa: S101
from typing import cast

from langchain.chat_models import BaseChatModel, init_chat_model


def load_llm() -> BaseChatModel:
    model = cast(
        "BaseChatModel",
        init_chat_model(
            model="gpt-oss:20b",
            model_provider="ollama",
            base_url="http://127.0.0.1:11434",
            temperature=0.2,
            configurable_fields="any",
        ),
    )

    assert hasattr(model, "bind_tools")
    assert hasattr(model, "invoke")
    assert hasattr(model, "with_config")

    return model
