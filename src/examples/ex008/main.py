import builtins
from typing import Literal

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.tracers.stdout import FunctionCallbackHandler
from langgraph.graph.state import RunnableConfig
from rich import print
from rich.markdown import Markdown
from rich.prompt import Prompt

from examples.ex008.graph import build_graph
from examples.ex008.prompts import SYSTEM_PROMPT


def main() -> None:
    graph = build_graph()

    fn_handler_cb = FunctionCallbackHandler(function=builtins.print)
    user_type: Literal["plus", "enterprise"] = "plus"
    config = RunnableConfig(
        run_name="meu_grafo",
        tags=["enterprise"],
        configurable={"thread_id": 1, "user_type": user_type},
        max_concurrency=4,
        recursion_limit=25,
        # callbacks=[fn_handler_cb],
    )
    all_messages: list[BaseMessage] = []

    prompt = Prompt()
    Prompt.prompt_suffix = ""

    while True:
        user_input = prompt.ask("[bold cyan]Você: \n")
        print(Markdown("\n\n  ---  \n\n"))

        if user_input.lower() in ["q", "quit"]:
            break

        human_message = HumanMessage(user_input)
        current_loop_messages = [human_message]

        if len(all_messages) == 0:
            current_loop_messages = [SystemMessage(SYSTEM_PROMPT), human_message]

        result = graph.invoke({"messages": current_loop_messages}, config=config)

        model_name = ""
        last_message = result["messages"][-1]

        if isinstance(last_message, AIMessage):
            model_name = last_message.response_metadata.get("model", "")

        print(f"[bold cyan]RESPOSTA ({model_name}): \n")
        print(Markdown(last_message.text))
        print(last_message)
        print(Markdown("\n\n  ---  \n\n"))

        all_messages = result["messages"]

    print(graph.get_state(config=config))


if __name__ == "__main__":
    main()
