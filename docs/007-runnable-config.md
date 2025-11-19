# RunnableConfig - Além do `thread_id`

> **Observação importante**: copiei todos os arquivos da nossa última aula e
> alterei todos os imports de `ex006` para `ex007`. Não se esqueça do
> `langgraph.json`.

Uma parte importante do LangGraph / LangChain são os runnables.

Referência: https://reference.langchain.com/python/langchain_core/runnables/

Foram eles que deram a possibilidade de criar chains uniformes no LangChain lá
no início. No entanto, ainda hoje eles estão no coração de quase tudo o que
vamos usar.

## Mas o que seria um Runnable?

A resposta curta é: quase tudo!

Uma função, a LLM, o grafo, um node do grafo, a configuração do grafo, até mesmo
os prompt templates que existem no LangChain são Runnables.

Veja se alguns desses métodos te lembra alguma coisa: `invoke`, `ainvoke`,
`batch`, `abatch`, `stream`, `astream`... entre outros.

Nós ainda estamos no `invoke`, mas nós chamamos este método tanto no nosso grafo
quanto no próprio model (LLM). Isso porque ambos são runnables.

Portanto, uma definição mais formal para um runnable seria a seguinte:

> Um runnable é **qualquer unidade executável com uma interface padronizada**,
> capaz de receber entrada, produzir saída e se encadear com outras unidades
> para formar pipelines ou grafos de execução.

Ou da própria referência no link acima:

> A unit of work that can be invoked, batched, streamed, transformed and
> composed.

## Ok, mas e `RunnableConfig`?

Existem vários `Runnables` que tem a classe
`langchain_core.runnables.base.Runnable` como base, então a maioria deles tem os
métodos que te mostrei anteriormente (veja a referência). No entanto, o
`RunnableConfig` herda de `TypedDict`, ou seja, é um dicionário.

Se você conferir na referência, verá que `RunnableConfig` é isso:

> Configuration for a Runnable.

Bem que poderiam detalhar melhor, mas tudo bem. É a configuração usada por um
`Runnable`. Como nosso grafo é um `Runnable`, foi por isso que a configuração do
nosso grafo ficou assim:

```python
config = RunnableConfig(configurable={"thread_id": 1})
```

Precisávamos de um `thread_id` para ativar o `checkpointer`. No início, te
mostrei que poderíamos ter usado um dicionário. Mas, eu prefiro usar a classe
`RunableConfig` para ser mais explícito (falamos sobre tudo isso nas aulas
anteriores).

## Tá, mais por que estamos voltando em `RunableConfig`?

Na verdade, não fizemos nada de interessante até agora. Mas podemos usar
`RunnableConfig` em qualquer node. Inclusive, podemos usar `config` temporárias
para algum objetivo qualquer. Por exemplo: se eu quiser trocar de LLM no meio da
execução do grafo, em qualquer node, basta chamar `invoke` (ou outros métodos do
Runnable) com outra `config`.

## Vamos entender isso na aula em vídeo

Vou falar mais sobre tudo isso durante a aula em vídeo, por que tem algumas
coisas para entendermos que deixariam este texto extremamente longo.

Então corre lá para a pasta:

- src/examples/ex007

Agora os arquivos estão todos separados e foram copiados da aula anterior
(ex006). Vamos trabalhar em cima do que fizemos antes.

Assuntos (só para eu não esquecer de nada):

- `RunnableConfig`

---
