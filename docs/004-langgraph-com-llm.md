# LangGraph com LLMs

[Na aula anterior](./003-introducao-ao-langgraph.md) vimos que cada **nó do
grafo** pode ser uma função Python para fazer algo: somar números, concatenar
listas, tomar decisões condicionais etc.

Mas qual foi a única coisa que não chegamos a usar no grafo? **O LLM!**.

---

## O que faltou?

Nosso grafo só processou dados simples e fixos. Quando colocamos uma LLM em um
nó, ela passa a participar do fluxo como **parte da lógica de execução**. Ou
seja, o LangGraph não será só "um chat wrapper"
([como a nossa primeira aula](./002-chat-simples-langchain.md)), agora ele passa
a ser um **orquestrador de chamadas para LLMs**.

Vamos começar do básico para não inundar seu cérebro com um monte de detalhes.
Por isso, criaremos um grafo com um nó apenas. Esse nó receberá a mensagem do
usuário e fará o contato com o LLM. Quando recebermos um resultado, só
precisaremos retornar esse resultado para atualizar o estado.

---

## Estado com mensagens

Para conversar com modelos, precisamos manter um histórico de mensagens.

O LangGraph já traz um reducer chamado `add_messages` que sabe como juntar
**SystemMessage, HumanMessage e AIMessage** em uma lista (os tipos de mensagens
que já vimos antes).

Um exemplo:

```python
from typing import Annotated, TypedDict
from collections.abc import Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
```

Perceba que `add_messages` é um reducer. Isso significa que cada vez que o campo
`messages` for alterado, `add_messages` fará o trabalhar de unir `a` e `b`,
sendo `a` as mensagens anteriores e `b` as novas mensagens.

Vou detalhar isso bem mais na aula em vídeo e no código abaixo.

---

## O código

Não se esqueça do que eu disse na primeira aula. A maior parte das explicações
estará no código e na aula em vídeo:

- Aqui está o código - [ex004 - code001.py](../src/examples/ex004/code001.py)

---

## Checkpointers do LangGraph

Você pode ter percebido que estou gerenciando o histórico de conversas
manualmente, certo?

Se não, veja esse trecho de código do arquivo
[code001.py](../src/examples/ex004/code001.py) comentado:

```python
# ... código omitido
# Estou adicionando mensagens anteriores nesse ponto
current_messages = [*current_messages, human_message]
# ... código omitido
# Invocando o grafo com as mensagens
result = graph.invoke({"messages": current_messages})
# ... código omitido
# Pegando a resposta do grafo e jogando de volta em `current_messages`.
current_messages = result["messages"]
# ... código omitido
```

Bom, não é necessário fazer isso. O LangGraph conta com os "Checkpointers". Eles
são pontos onde o estado é salvo em algum local automaticamente (memória, base
de dados, ou onde você quiser).

Não vou entrar em detalhes sobre checkpointers nessa aula em específico para
dedicar aulas exclusivas a eles mais adiante. Este assunto envolve o contexto do
LLM e os tipos de memória que podemos decidir usar dependendo do que estivermos
fazendo (um pouco mais complexo do que apenas manter o histórico de conversas).

Mesmo assim, criar um checkpointer em memória é tão simples, que já vamos
adicionar ele a seguir.

---

## O código (com o checkpointer `InMemorySaver`)

Este é o mesmo código anterior, mas com algumas alterações. Deixei tudo
comentado para você e também detalhei isso na aula em vídeo.

- Aqui está o código - [ex004 - code002.py](../src/examples/ex004/code002.py)

---
