from langgraph.checkpoint.memory import InMemorySaver

from examples.ex010.utils import Connection


def build_checkpointer(conn: Connection) -> InMemorySaver:
    conn.use()
    return InMemorySaver()
