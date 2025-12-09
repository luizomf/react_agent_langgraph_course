from langgraph.prebuilt.tool_node import ToolNode
from langgraph.runtime import Runtime

from examples.ex012.context import Context
from examples.ex012.state import State
from examples.ex012.tools import TOOLS
from examples.ex012.utils import load_llm

tool_node = ToolNode(tools=TOOLS)


def call_llm(state: State, runtime: Runtime[Context]) -> State:
    print("> call llm")
    ctx = runtime.context
    user_type = ctx.user_type

    model_provider = "ollama" if user_type == "plus" else "ollama"  # noqa: RUF034
    model = "gpt-oss:20b" if user_type == "plus" else "qwen3-coder:30b"

    llm_with_tools = load_llm().bind_tools(TOOLS)
    llm_with_config = llm_with_tools.with_config(
        config={
            "configurable": {
                "model": model,
                "model_provider": model_provider,
            }
        }
    )

    result = llm_with_config.invoke(
        state["messages"],
    )

    return {"messages": [result]}
