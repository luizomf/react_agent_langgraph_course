from collections.abc import Sequence
from typing import Annotated, TypedDict

from langgraph.graph.message import BaseMessage, add_messages


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
