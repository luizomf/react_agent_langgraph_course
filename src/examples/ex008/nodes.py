from langgraph.graph.state import RunnableConfig
from langgraph.prebuilt.tool_node import ToolNode

from examples.ex008.state import State
from examples.ex008.tools import TOOLS
from examples.ex008.utils import load_llm

tool_node = ToolNode(tools=TOOLS)


def call_llm(state: State, config: RunnableConfig) -> State:
    print("> call llm")
    user_type = config.get("configurable", {}).get("user_type")
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
