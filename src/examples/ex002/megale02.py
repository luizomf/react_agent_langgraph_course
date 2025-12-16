# main.py
from dotenv import load_dotenv
import os
from rich import print

# Carrega as variáveis do .env 
load_dotenv()

# Verifica se a variável foi carregada
print("GOOGLE_API_KEY =", os.getenv("GOOGLE_API_KEY"))

# Importações corretas do LangChain

from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, SystemMessage

# Inicializa seu LLM
llm = init_chat_model(
    model="google_genai:gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# Mensagem do sistema (instrui o comportamento do assistente)
system_message = SystemMessage(
    content=(
        "Você é um guia de estudos que ajuda estudantes a aprenderem novos tópicos.\n\n"
        "Seu trabalho é guiar as ideias do estudante para que ele consiga entender o "
        "tópico escolhido sem receber respostas prontas da sua parte.\n\n"
        "Evite conversar sobre assuntos paralelos ao tópico escolhido. Se o estudante "
        "não fornecer um tópico inicialmente, seu primeiro trabalho será solicitar um "
        "tópico até que o estudante o informe.\n\n"
        "Você pode ser amigável, descolado e tratar o estudante como adolescente. Queremos "
        "evitar a fadiga de um estudo rígido e mantê-lo engajado no que estiver "
        "estudando.\n\n"
        "As próximas mensagens serão de um estudante."
    )
)

# Mensagem do humano (usuário)
human_message = HumanMessage(content="Olá, tudo bem?")

# Monta a lista de mensagens
messages = [system_message, human_message]

# Obtém a resposta do modelo
response = llm.invoke(messages)
print(f"{'AI':-^80}")
print(response.content)

messages.append(response)
while True:
    print(f"{'Human':-^80}")
    user_input = input("Digite sua mensagem: ")
    human_message = HumanMessage(content=user_input)

    if user_input.lower() in ["exit", "quit", "bye", "q"]:
        break

    messages.append(human_message)
    response = llm.invoke(messages)
    print(f"{'AI':-^80}")
    print(response.content)
    print()
    messages.append(response)
    
print()
print(f"{'Histórico':-^80}")
print(*[f"{m.type.upper()}\n{m.content}\n\n" for m in messages], sep="", end="" )
print()
