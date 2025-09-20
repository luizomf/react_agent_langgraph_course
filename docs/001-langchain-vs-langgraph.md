# ReAct Agent com LangGraph e LangChain

A maior parte do curso vai focar em **LangGraph**, mas em vários momentos vamos
usar recursos do **LangChain** para atingir nossos objetivos. Principalmente as
ferramentas que ele já traz prontas e que tornam o trabalho com o **LangGraph**
muito mais fácil.

Por isso, antes de avançar, vamos entender a diferença entre os dois para não
ficar nenhuma dúvida sobre o papel de cada um.

---

## LangChain vs LangGraph

### LangChain

O **LangChain** é uma caixa de ferramentas gigante para trabalhar com LLMs. Ele
tenta resolver quase tudo: integração com diferentes modelos e providers, banco
de dados, RAG, ferramentas externas (tools), encadeamento de chamadas com o
**LCEL (LangChain Expression Language)**, e muito mais.

O próprio nome já entrega a ideia: a parte _"chain"_ vem de **chains**
(correntes, cadeias, encadeamento). Ou seja, você monta uma **sequência de
passos** onde a saída de um vira a entrada do próximo. Um fluxo típico fica
assim:

```
Prompt -> LLM -> Solução -> FIM
```

Isso funciona bem para pipelines lineares e previsíveis. Mas quando o problema
exige **condições, loops ou estado persistente**, até dá pra forçar no
LangChain, só que o código fica pesado e difícil de depurar.

É aí que entra o **LangGraph**, feito para lidar diretamente com grafos de
execução mais complexos, de forma clara e controlada.

### LangGraph

O **LangGraph** nasceu para resolver justamente as limitações do LangChain
quando o fluxo deixa de ser linear. Aqui a ideia principal não é só "chain", mas
sim **graph** (grafo), onde você pode controlar **o caminho que a execução vai
seguir**.

Com o LangGraph você consegue criar fluxos que:

- têm **condições** (se a LLM pedir uma tool, segue por um caminho; se não,
  segue por outro),
- suportam **loops controlados** (repetir até a resposta estar ok, por exemplo),
- e mantêm **estado persistente** ao longo da conversa.

Na prática, você monta um grafo de execução em que cada nó é um passo (um LLM,
uma função, uma tool) e cada aresta define a lógica de transição entre eles.
Isso dá muito mais clareza e previsibilidade do que tentar forçar tudo dentro de
uma chain.

Resumindo: enquanto o **LangChain** brilha em pipelines lineares e simples, o
**LangGraph** é feito sob medida para **agentes** e fluxos complexos, onde você
precisa de controle fino sobre cada decisão.

Isso é só uma parte teórica para você saber que existem diferenças entre ambos,
mas vamos falar muito sobre os detalhes ao longo das aulas.

---
