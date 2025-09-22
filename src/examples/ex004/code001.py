import operator
from dataclasses import dataclass
from typing import Annotated, Literal

from langgraph.graph import END, START, StateGraph
from rich import print

# Este é o último código da aula anterior

# Definições do estado e dos nodes


@dataclass
class State:
    nodes_path: Annotated[list[str], operator.add]  # operator.add = a + b
    # Vamos usar esse current_number para nossa conditional edge
    current_number: float = 0


def node_a(state: State) -> State:
    final_state: State = State(nodes_path=["A"], current_number=state.current_number)
    print("> node_a em execução", f"{state=}", f"{final_state=}")
    return final_state  # só estou gerando um novo estado


def node_b(state: State) -> State:
    final_state: State = State(nodes_path=["B"], current_number=state.current_number)
    print("> node_b em execução", f"{state=}", f"{final_state=}")
    return final_state  # só estou gerando um novo estado


# TEMOS UM NOVO NODE!
def node_c(state: State) -> State:
    final_state: State = State(nodes_path=["C"], current_number=state.current_number)
    print("> node_c em execução", f"{state=}", f"{final_state=}")
    return final_state  # só estou gerando um novo estado


# A definição de uma função condicional
# Essa função será usada como condição para uma `conditional edge`.
# Ela também recebe o estado e terá o trabalho de retornar o nome da edge que
# o grafo deve seguir.
def the_conditions(state: State) -> Literal["goes_to_b", "goes_to_c"]:
    # Vamos definir um valor arbitrário para ficar fácil de visualizar.
    # Iremos para o `node_b` enquanto `current_number` for menor ou igual a 50
    b_max_number = 50
    should_go_to_b = state.current_number <= b_max_number

    # Não é muito comum dar nomes para edges assim, onde temos:
    # `goes_to_b` seria apenas `B`
    # `goes_to_c` seria apenas `C`
    # Só que eu queria te mostrar isso. Se o nome da edge for diferente do nome
    # do nome, a sua edge acabou de ganhar um nome (no grafo desenhado isso se
    # torna uma tag sobre o nome da edge).

    if should_go_to_b:
        # Então retornamos o nome da edge para o grafo seguir
        return "goes_to_b"

    # Único outro caminho possível é este
    return "goes_to_c"


# Definição e compilação do grafo

builder = StateGraph(
    State, input_schema=State, context_schema=None, output_schema=State
)

builder.add_node("A", node_a)
builder.add_node("B", node_b)
builder.add_node("C", node_c)  # NOVO NODE!!!

# Aqui agora temos que mudar umas coisas
# Ainda vamos de `__start__` para `A`
builder.add_edge(START, "A")
# Mas de `A` temos duas possibilidades, ou `B` ou `C`. Então precisamos definir
# uma conditional edge.
# Primeiro parâmetro: de onde estamos iniciando? `A`.
# Segundo parâmetro: quais as condições? A função `the_conditions` faz isso.
# Terceiro parâmetro: um mapeamento de qual edge vai para qual node
builder.add_conditional_edges(
    "A",
    the_conditions,
    {
        "goes_to_b": "B",
        "goes_to_c": "C",
    },
)

# E agora qual nome vai para END? `B` e `C`.
builder.add_edge("B", END)
builder.add_edge("C", END)


graph = builder.compile()

if __name__ == "__main__":
    # Execução do código

    print()
    # 10 deve ir de `A` para `B`
    response = graph.invoke(State(nodes_path=[], current_number=10))
    print(f"{response=}")
    print()
    # 51 deve ir de `A` para `C`
    response = graph.invoke(State(nodes_path=[], current_number=51))
    print(f"{response=}")
    print()
