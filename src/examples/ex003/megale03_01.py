from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, add_messages
from rich import print
##import operator


# def reducer(a: list[str], b: list[str]) -> list[str]:
#     reducer_result = a + b
#     print("> reducer em execução", f"{reducer_result=}")
#     return reducer_result

## O estado do grafo
class State(TypedDict):
    nodes_path: Annotated[list[str],add_messages]  # operator.add   Usando o operador de adição como reducer

#2 Definir os nodes 

def node_a(state: State) -> State:
    output_state: State = {"nodes_path": ["A"]}
    print("> node_a em execução", f"{state=}", f"{output_state=}")  
    return output_state


def node_b(state: State) -> State:
    output_state: State = {"nodes_path": ["B"]}
    print("> node_b em execução", f"{state=}", f"{output_state=}")  
    return output_state

## definir o builder do grafo //stategraph 
builder = StateGraph(State)

builder.add_node("A", node_a)
builder.add_node("B", node_b)

##Conectar a Edges 

builder.add_edge('__start__', "A")
builder.add_edge("A", "B")
builder.add_edge("B", "__end__")

## Compilar o grafo

graph = builder.compile()

## Executar o grafo

#print(graph.get_graph().draw_mermaid()) ## quiser ver img, sio colcar no mermeid chart 

##Pegar o resultado

response = graph.invoke({"nodes_path": []})

print()
print(f"{response}")
print()