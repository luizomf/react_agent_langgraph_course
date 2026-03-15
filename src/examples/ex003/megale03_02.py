from typing import Annotated, TypedDict, Literal
from langgraph.graph import StateGraph, END, START
from rich import print
import operator
from dataclasses import dataclass


@dataclass
class State:
    nodes_path: Annotated[list[str],operator.add]  
    current_number: int = 0

#2 Definir os nodes 


def node_a(state: State) -> State:
    output_state: State = State(nodes_path=["A"], current_number=state.current_number) 
    print("> node_a em execução", f"{state=}", f"{output_state=}")  
    return output_state


def node_b(state: State) -> State:
    output_state: State = State(nodes_path=["B"], current_number=state.current_number) 
    print("> node_b em execução", f"{state=}", f"{output_state=}")  
    return output_state

def node_c(state: State) -> State:
    output_state: State = State(nodes_path=["C"], current_number=state.current_number) 
    print("> node_c em execução", f"{state=}", f"{output_state=}")  
    return output_state

#Funcao condicional 

def the_conditional(state: State) -> Literal["B", "C"]:
    if state.current_number >= 50:
        return "C"
    else:
        return "B"









## definir o builder do grafo //stategraph 
builder = StateGraph(State)
builder.add_node("A", node_a)
builder.add_node("B", node_b)
builder.add_node("C", node_c)

##Conectar a Edges 
builder.add_edge(START, "A")
builder.add_conditional_edges("A", the_conditional,{"B":"B", "C":"C"}) ##ex 'goes_to_c' : 'c' /// 
builder.add_edge("B", END)
builder.add_edge("C", END)

## Compilar o grafo
graph = builder.compile()

## Pegar resultado

print()
response = graph.invoke(State(nodes_path=[]))
print(f"{response}")
print()

print()
response = graph.invoke(State(nodes_path=[], current_number=51))
print(f"{response}")
print()