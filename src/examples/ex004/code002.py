import threading
from collections.abc import Sequence
from typing import Annotated, TypedDict

from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph, add_messages
from langgraph.graph.state import RunnableConfig
from rich import print
from rich.markdown import Markdown

# llm = init_chat_model("google_genai:gemini-2.5-flash")
llm = init_chat_model("ollama:gpt-oss:20b")


# 1 - Defino o meu state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# 2 - Defino os meus nodes
def call_llm(state: AgentState) -> AgentState:
    llm_result = llm.invoke(state["messages"])
    return {"messages": [llm_result]}


# 3 - Crio o StateGraph
builder = StateGraph(
    AgentState, context_schema=None, input_schema=AgentState, output_schema=AgentState
)

# 4 - Adicionar nodes ao grafo
builder.add_node("call_llm", call_llm)
builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)

# 5 - Compilar o grafo
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
config = RunnableConfig(configurable={"thread_id": threading.get_ident()})

if __name__ == "__main__":
    while True:
        user_input = input("Digite sua mensage: ")
        print(Markdown("---"))

        if user_input.lower() in ["q", "quit"]:
            print("Bye 👋")
            print(Markdown("---"))
            break

        human_message = HumanMessage(user_input)
        result = graph.invoke({"messages": [human_message]}, config=config)

        print(Markdown(str(result["messages"][-1].content)))
        print(Markdown("---"))
