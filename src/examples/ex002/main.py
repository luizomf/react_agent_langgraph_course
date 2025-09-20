from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

llm = init_chat_model("ollama:gpt-oss:20b")

# Em vários momentos, queremos fazer o modelo se comportar de determinada forma.
# Para isso, podemos usar um tipo especial de mensagem que não deve ser exibida
# ao usuário final. Conseguimos isso criando uma `SystemMessage` com um
# prompt programador para fazê-lo se comportar de determinada maneira.
# No exemplo abaixo, estou criando uma `SystemMessage` com regras iniciais a
# serem seguidas pelo modelo.
system_message = SystemMessage(
    "Você é um guia de estudos que ajuda estudantes a aprenderem novos tópicos. \n\n"
    "Seu trabalho é guiar as ideias do estudante para que ele consiga entender o "
    "tópico escolhido sem receber respostas prontas da sua parte. \n\n"
    "Evite conversar sobre assuntos paralelos ao tópico escolhido. Se o estudante "
    "não fornecer um tópico inicialmente, seu primeiro trabalho será solicitar um "
    "tópico até que o estudante o informe. \n\n"
    "Você pode ser amigável, descolado e tratar o estudante como adolescente. Queremos "
    "evitar a fadiga de um estudo rígido e mantê-lo engajado no que estiver "
    "estudando. \n\n"
    "As próximas mensagens serão de um estudante. "
)
# Quando uma pessoa envia mensagens para o modelo, essa mensagem será convertida
# em uma `HumanMessage` que terá o formato específico para que o modelo saiba
# distinguir o que é mensagem do sistema, o que é mensagem de um usuário e o que
# é uma mensagem do próprio modelo respondendo o usuário.
# Isso forma um histórico de conversas bem estruturado para que o modelo tenha
# contexto do assunto que está sendo tratado no momento.
human_message = HumanMessage("Olá, meu nome é Luiz Otávio")

# Você pode enviar uma lista de mensagens para o modelo com o histórico de
# conversas. Se não fizer isso, cada mensagem será tratada como a primeira
# mensagem recebida pelo modelo e ele não saberá nada sobre as conversas
# anteriores.
messages = [system_message, human_message]
response = llm.invoke(messages)
print(f"{'AI':-^80}")
print(response.content)  # Em response.content, teremos uma AIMessage nesse contexto

# Também podemos fazer um loop infinito e montar um histórico de conversa
# artificialmente. Mas isso não é necessário quando usamos LangGraph.

# Adiciona a resposta do modelo em messages
messages.append(response)
while True:
    # Pega a mensagem do usuário
    print(f"{'Human':-^80}")
    user_input = input("Digite sua mensagem: ")
    human_message = HumanMessage(user_input)

    # Qualquer uma dessas palavras termina o loop
    if user_input.lower() in ["exit", "quit", "bye", "q"]:
        break

    # Adiciona a mensagem do usuário em messages
    messages.append(human_message)

    # Manda as mensagens com o histórico de volta para o modelo
    response = llm.invoke(messages)

    # Exibe a mensagem do modelo
    print(f"{'AI':-^80}")
    print(response.content)
    print()

    # Adiciona a resposta do modelo em messages
    messages.append(response)

# Isso é só para vermos como ficou nosso histórico de conversas
print()
print(f"{'Histórico':-^80}")
print(*[f"{m.type.upper()}\n{m.content}\n\n" for m in messages], sep="", end="")
print()
