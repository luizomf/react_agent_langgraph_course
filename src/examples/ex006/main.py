from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph.state import RunnableConfig
from rich import print
from rich.markdown import Markdown
from rich.prompt import Prompt

from examples.ex006.graph import build_graph
from examples.ex006.prompts import SYSTEM_PROMPT


def main() -> None:
    graph = build_graph()
    config = RunnableConfig(configurable={"thread_id": 1})
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

        print("[bold cyan]RESPOSTA: \n")
        print(Markdown(result["messages"][-1].content))
        print(Markdown("\n\n  ---  \n\n"))

        all_messages = result["messages"]

    print(all_messages)


if __name__ == "__main__":
    main()
