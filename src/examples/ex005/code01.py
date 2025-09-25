from langchain.chat_models import init_chat_model
from langchain.tools import BaseTool, tool
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from pydantic import ValidationError
from rich import print

# 1 - Criar as ferramentas


@tool
def multiply(a: float, b: float) -> float:
    """Multiply a * b and returns the result

    Args:
        a: float multiplicand
        b: float multiplier

    Returns:
        the resulting float of the equation a * b
    """
    return a * b


# 2 - Instanciamos nosso modelo.

# llm = init_chat_model("google_genai:gemini-2.5-flash")
llm = init_chat_model("ollama:gpt-oss:20b")

# 3 - Criamos as mensagens

system_message = SystemMessage(
    "You are a helpful assistant. You have access to tools. When the user asks "
    "for something, first look if you have a tool that solves that problem."
)
human_message = HumanMessage("Oi, sou Otávio. Pode me falar quanto é 1.13 vezes 2.31?")
# human_message = HumanMessage("Oi, sou Otávio.")

# Não se esqueça de adicionar as mensagens no histórico
messages: list[BaseMessage] = [system_message, human_message]


# 4 - Criamos a lista de ferramentas
tools: list[BaseTool] = [multiply]
# Isso ajuda a encontrar a ferramenta por nome
tools_by_name = {tool.name: tool for tool in tools}

# 5 - Criamos um LLM com base no anterior, mas com acesso a tools.
llm_with_tools = llm.bind_tools(tools)

# 6 - Agora podemos enviar as mensagens para o modelo
llm_response = llm_with_tools.invoke(messages)

# 7 - Adicionamos a resposta do modelo no histórico
messages.append(llm_response)

# 8 - Conferimos se o modelo tentou chamar alguma ferramenta
if isinstance(llm_response, AIMessage) and getattr(llm_response, "tool_calls", None):
    # 8.1 - Pegamos a última chamada para ferramenta
    call = llm_response.tool_calls[-1]
    # 8.2 - Pegamos os dados que o modelo tentou usar para chamar nossa
    # ferramenta.
    name, args, id_ = call["name"], call["args"], call["id"]

    # 8.3 - Tentamos garantir que não teremos erros aqui, por isso try/except
    try:
        # 8.4 - executamos a ferramenta com os dados que o modelo nos passou
        content = tools_by_name[name].invoke(args)
        status = "success"
    except (KeyError, IndexError, TypeError, ValidationError, ValueError) as error:
        # 8.4 - Se der erro, vou informar para o modelo
        content = f"Please, fix your mistakes: {error}"
        status = "error"

    # 8.5 - Crio uma tool message
    tool_message = ToolMessage(content=content, tool_call_id=id_, status=status)
    # 8.6 - Adiciono a tool message no histórico
    messages.append(tool_message)

    # 8.7 - Passo o histórico para o modelo (agora tem o resultado da tool)
    llm_response = llm_with_tools.invoke(messages)
    # 8.8 - Adiciono a resposta do modelo no histórico
    messages.append(llm_response)

# 9 - Exibo o resultado (com ou sem tool_calls)
print(messages)
