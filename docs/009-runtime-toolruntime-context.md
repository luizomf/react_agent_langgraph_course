# Runtime e ToolRuntime no LangGraph / LangChain

## Runtime

O **Runtime** é o objeto que o LangGraph injeta automaticamente dentro de cada
nó do grafo enquanto ele está sendo executado. Ele representa o "ambiente de
execução atual" reunindo tudo o que o nó precisa para trabalhar sem depender de
variáveis globais, singletons ou hacks.

Quando você define um `Context` (normalmente via `context_schema`), esse
contexto tipado aparece dentro do Runtime como `runtime.context`. Ele é imutável
durante a execução e funciona como um pacote de dependências que você configura:
usuário atual, conexões, configs fixas, clientes de API, serviços, etc.

Além do contexto, o Runtime também expõe outros recursos internos do LangGraph,
como acesso a memória persistente (store), mecanismos de streaming, informações
sobre o passo atual e referências ao estado anterior (não falamos desses outros
recursos ainda). Mas a função principal, na prática, é permitir que os nós
acessem o **contexto estático** da execução de forma segura e organizada.

Em resumo: **Runtime existe para dar aos nós do grafo acesso ao contexto da
execução, memória, streaming e metadados, tudo num lugar só.**

## ToolRuntime

O **ToolRuntime** é a versão especializada desse mesmo conceito, mas voltada
para **tools** do LangChain (as tools que já criamos anteriormente). Ele foi
criado para substituir APIs antigas como `InjectedState`, `InjectedStore`,
`get_runtime` e outras anotações que já viraram legado.

Enquanto o Runtime é usado em nós do grafo, o ToolRuntime é usado dentro das
tools.

Ele fornece os mesmos recursos essenciais, como estado atual, contexto, memória
persistente, streaming. Porém, também adiciona informações.

A diferença entre o Runtime e o ToolRuntime, é que o ToolRuntime é um "tudo em
um", vem muito mais informações do que no Runtime (vou mostrar isso no código).

Outro ponto importante: o ToolRuntime é totalmente invisível para o modelo. O
LLM não enxerga esse parâmetro na definição da tool. Isso significa que você
pode passar contexto, estado e dependências de forma segura sem que isso
influencie o schema ou gere confusão para o modelo.

Em resumo: **ToolRuntime oferece para tools o mesmo ambiente rico de execução
que o Runtime oferece para nós, só que o ToolRuntime tem acesso ao contexto,
estado, config, memória e streaming, tudo de forma unificada e invisível ao
modelo.**

## Código para esta aula:

O código para esta aula estará na pasta:

- [../src/examples/ex009](../src/examples/ex009)

---
