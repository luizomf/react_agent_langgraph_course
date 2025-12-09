from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver


def build_checkpointer() -> InMemorySaver:
    return InMemorySaver()


@asynccontextmanager
async def build_checkpointer_psql(db_dsn: str) -> AsyncGenerator[AsyncPostgresSaver]:
    async with AsyncPostgresSaver.from_conn_string(db_dsn) as checkpointer:
        await checkpointer.setup()
        yield checkpointer


@asynccontextmanager
async def build_checkpointer_sqlite(db_dsn: str) -> AsyncGenerator[AsyncSqliteSaver]:
    async with AsyncSqliteSaver.from_conn_string(db_dsn) as checkpointer:
        yield checkpointer
