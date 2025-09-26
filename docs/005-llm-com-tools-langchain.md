# LLM com tools no LangChain

Agora que você já sabe
[montar um grafo com LangGraph e LangChain](./004-langgraph-com-llm.md) podemos
dar um passo a mais e adicionar tools (ferramentas) para os nossos LLMs. Com
isso a IA poderá executar tarefas além do que está em seu treinamento.

---

## O que são ferramentas?

Ferramentas (tools) são funções Python, scripts ou serviços externos que expomos
para que a IA execute em nosso nome. Cada tool descreve quais argumentos aceita
e o que devolve, permitindo que o modelo peça ações determinísticas, como
calcular algo, consultar uma API, ler um arquivo e várias outras coisas. Por
isso, a documentação da sua ferramenta é extremamente importante.

Outro ponto que muitas pessoas confundem é que a IA não executa diretamente a
ferramenta, ela apenas sabe da sua existência. Quando alguma conversa do usuário
é direcionada para algo que uma das ferramentas disponíveis resolve, a IA
enviará um pedido para executar a ferramenta com os argumentos que o usuário
solicitou.

### Exemplo

Suponha que você tem uma ferramenta chamada `multiply` que recebe `a` e `b`. Sua
ferramenta está bem documentada, de forma que a IA não terá dificuldades em
saber quando chamá-la:

```python
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
```

Quando uma conversa direciona a IA para usar a ferramenta, acontece algo
semelhante a isso:

```text
Usuário: Oi, sou Otávio Miranda.
IA: Olá Otávio, como posso te ajudar hoje?
Usuário: Poderia me dizer quanto é 5.2 vezes 10?
```

Nesse momento o fluxo muda um pouco. Acontece algo semelhante a isso:

```text
IA: (SOLICITA A CHAMADA DA FERRAMENTA: multiply com 5.2 e 10)

Dev: Chama a Ferramenta
Dev: Injeta o resultado de volta na IA (52.0)
```

Depois disso, a IA retoma a conversa:

```text
IA: Otávio, o resultado entre 5.2 * 10 é 52.0.
```

---

## Por que usar ferramentas com LLMs?

LLMs trabalham apenas com o que está na janela de contexto e no treinamento.

Ferramentas nos permitem ultrapassar essas barreiras:

- Executar cálculos ou transformações determinísticas sem depender da
  "imaginação" do modelo.
- Buscar informações atualizadas em APIs, bancos de dados ou arquivos locais.
- Aplicar regras de negócio específicas do produto sem expô-las ao modelo.
- Integrar a conversa com outros sistemas (e-mails, automações, tickets, etc)
  mantendo rastreabilidade do que foi feito.

---

## Como o LangChain organiza esse fluxo

O LangChain padroniza todo esse processo. Com o decorator `@tool` ou classes que
herdam de `BaseTool`, definimos o schema de entrada e a execução da função. O
próprio LangChain usa Pydantic para validar os argumentos antes da chamada,
então sabemos que a tool receberá dados coerentes (ou que uma exceção será
lançada caso algo esteja errado).

Quando chamamos `llm.bind_tools(tools)`, o modelo passa a responder com objetos
`AIMessage` contendo `tool_calls`. Cada chamada informa o nome da tool, os
argumentos serializados e um `id` único. O nosso código então decide se a
chamada faz sentido, executa a ferramenta com `tool.invoke`, trata eventuais
erros (`ValidationError`, `ToolException` etc.) e finalmente devolve o resultado
para a LLM usando um `ToolMessage`. Esse `ToolMessage` carrega o `tool_call_id`
para que o modelo saiba qual requisição foi atendida e possa produzir a resposta
final para o usuário.

Esse mecanismo manual que você verá na aula (multiplicar dois números, por
exemplo) é o mesmo que utilizaremos para qualquer automação com tools.

---

## Fluxo da aula (sem LangGraph ainda)

- **Mensagem do usuário**: iniciamos uma lista de `messages` e adicionamos um
  `HumanMessage` com a pergunta.
- **Decisão da LLM**: com as tools vinculadas, a resposta vem como `AIMessage`
  indicando qual ferramenta deve ser executada e com quais argumentos.
- **Execução segura**: procuramos a tool pelo nome, chamamos `invoke` e tratamos
  erros comuns. Nada impede que a LLM peça algo inválido, então essa etapa é
  nossa responsabilidade.
- **Retorno para o modelo**: construímos um `ToolMessage` com o resultado (ou
  com o erro) e repassamos tudo para `llm_with_tools.invoke`. A LLM usa essa
  nova mensagem para formular a resposta final.
- **Histórico**: armazenamos as mensagens para continuar a conversa ou repetir o
  ciclo com novas requisições.

Esse passo a passo sem grafo deixa claro o que está acontecendo por trás das
cortinas antes de delegarmos parte da orquestração para o LangGraph.

---

## Preparando o terreno para o LangGraph

Nas próximas aulas vamos conectar esse mesmo raciocínio ao LangGraph. Cada nó do
grafo poderá chamar uma LLM com tools ou até uma tool específica. O LangGraph
vai cuidar do estado, do histórico e dos checkpointers enquanto continuamos
usando o LangChain para definir como cada tool funciona. Dessa forma conseguimos
descrever rotas condicionais, paralelizar passos e reutilizar tools em
diferentes partes do fluxo sem duplicar código.

Quando juntarmos tudo, o LangGraph fornecerá a orquestração (quem chama quem e
quando), enquanto o LangChain continua sendo a base para falar com modelos e
ferramentas. É por isso que entender bem o fluxo manual agora vai facilitar
muito a transição para o grafo nas próximas aulas.

---

## O código

Fiz toda a explicação do código em vídeo. O código comentado está no arquivo a
seguir:

- Link do arquivo - [ex005 - code02.py](../src/examples/ex005/code01.py)

---

## Unindo tudo com o LangGraph

Agora que já sabemos como fazer todo o que vimos nas aulas anteriores, podemos
unir tudo isso no grafo com o LangGraph. Explico tudo em vídeo e deixo o código
completo na pasta `src/examples/ex006` (link abaixo):

- Link da pasta ex006 - [ex006 (pasta)](../src/examples/ex006/)

---
