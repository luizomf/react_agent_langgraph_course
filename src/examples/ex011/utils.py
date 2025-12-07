# ruff: noqa: S101
from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager, contextmanager
from functools import lru_cache
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


class Connection:
    def use(self) -> None:
        print("Ok, estou usando a connection...")

    def open_connection(self) -> None:
        print("Connection Opened")

    def close_connection(self) -> None:
        print("Connection Closed")


@lru_cache
def get_connection() -> Connection:
    return Connection()


@contextmanager
def sync_lifespan() -> Generator[Connection]:
    print("Sync Abri")
    yield get_connection()
    print("Sync Fechei")


@asynccontextmanager
async def async_lifespan() -> AsyncGenerator[Connection]:
    print("Async Abri")
    yield get_connection()
    print("Async Fechei")
