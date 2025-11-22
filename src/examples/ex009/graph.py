from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import END, START
from langgraph.graph.state import CompiledStateGraph, StateGraph
from langgraph.prebuilt.tool_node import tools_condition

from examples.ex009.context import Context
from examples.ex009.nodes import call_llm, tool_node
from examples.ex009.state import State


def build_graph() -> CompiledStateGraph[State, Context, State, State]:
    builder = StateGraph(
        state_schema=State,
        context_schema=Context,
        input_schema=State,
        output_schema=State,
    )

    builder.add_node("call_llm", call_llm)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "call_llm")
    builder.add_conditional_edges("call_llm", tools_condition, ["tools", END])
    builder.add_edge("tools", "call_llm")

    return builder.compile(checkpointer=InMemorySaver())
