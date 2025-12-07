# Sobre o conceito de Lifespan com Context Managers no Python

Se você já trabalha com programação há algum tempo, provavelmente já ouviu a
regra de ouro: "sempre que você abre um recurso, você deve fechá-lo". Seja um
arquivo, uma conexão de rede ou uma transação de banco de dados, garantir a
liberação desses recursos é crucial para evitar vazamentos de memória e manter
sua aplicação saudável.

No Python, essa prática foi elegantemente resolvida com os Context Managers (o
famoso bloco with).

Quando fazemos `with open(...)`, não precisamos nos preocupar em chamar
`.close()` explicitamente; a linguagem cuida disso para nós, inclusive em casos
de erro.

Mas como aplicamos isso no contexto de agentes de IA com LangGraph? Como
aplicamos isso em contexto assíncrono? Não, pelo amor de Deus não jogue tudo
dentro do bloco with (isso seria muito porco).

Hoje vou mostrar como usar o padrão Lifespan (muito comum no FastAPI e me
inspirei nele) para gerenciar o ciclo de vida da sua aplicação de IA, garantindo
que conexões de banco de dados e checkpointers sejam abertos e fechados
corretamente.

---

## O Problema: Ciclo de Vida em Agentes de IA

Ao construir agentes mais complexos, frequentemente precisamos de persistência.
O LangGraph utiliza checkpointers para salvar o estado do grafo, permitindo
"memória" entre interações.

Esses checkpointers, por sua vez, dependem de bases de dados como PostgreSQL,
SQLite, Redis ou qualquer outra que você escolher.

Porém, nosso desafio é o seguinte: precisamos abrir a conexão com o banco antes
de iniciar nosso grafo (workflow) e fechá-la assim que a execução terminar.
Fazer isso manualmente em cada execução pode ser propenso a erros.

Você pode (e vai) simplesmente esquecer de chamar "close". Além disso, se
ocorrer um erro no meio do seu workflow, a conexão vai ficar pendurada (não será
fechada).

Solução: Padrão Lifespan com Context Managers (Ou Async Context Managers)
Podemos criar uma função que atue como um gerenciador de contexto para toda a
nossa aplicação. Ela será responsável por configurar o ambiente (setup) e limpar
tudo depois (teardown).

Vamos começar com um exemplo simples e síncrono.

---

## Criando um Context Manager Síncrono

No Python, podemos usar o decorator `@contextmanager` da biblioteca padrão
`contextlib` para transformar uma função geradora em um gerenciador de contexto.

```python
from contextlib import contextmanager
from typing import Generator

# Simulando uma classe de conexão
class Connection:
    def open_connection(self):
        print("CONNECTION OPENED")

    def close_connection(self):
        print("CONNECTION CLOSED")

    def use(self):
        print("Estou usando a connection...")

@contextmanager
def sync_lifespan() -> Generator[Connection, None, None]:
    # Setup: Código executado ao ENTRAR no bloco with
    connection = Connection()
    connection.open_connection()

    try:
        # O yield entrega o controle (e o objeto) para o bloco with
        yield connection
    finally:
        # Teardown: Código executado ao SAIR do bloco with
        connection.close_connection()
```

**Não se esqueça do try/finally.**

No vídeo, nem coloquei try/finally (realmente, nem lembrei), mas é interessante.

Isso porque com o `yield` puro, se houver algum erro no meio do caminho, a
aplicação não roda o Teardown. Com try/finally não teríamos problemas.

### No main.py

Para usar isso no seu script principal (main):

```python
def main():
    with sync_lifespan() as conn:
        print("Executando o grafo...")
        conn.use()
        # Aqui rodaria seu grafo LangGraph

if __name__ == "__main__":
    main()
```

A saída seria algo como:

```
CONNECTION OPENED
Executando o grafo...
Estou usando a connection...
CONNECTION CLOSED
```

Agora, com try/finally, mesmo que ocorra um erro dentro do bloco with, o bloco
finally (implícito no `@contextmanager`) garante que a conexão seja fechada.

---

## Evoluindo para Assíncrono (Async Lifespan com Async Context Manager)

O LangGraph e o LangChain são fortemente baseados em concorrência e execução
assíncrona. Portanto, o ideal é que nosso gerenciamento de ciclo de vida também
seja assíncrono.

A partir do Python 3.7+, temos o suporte a async with, e na versão 3.8+ o
contextlib introduziu o `@asynccontextmanager`.

Vamos refatorar nosso código para o mundo async. De novo, não esqueça do
try/finally como fiz no vídeo (expliquei antes o motivo).

```python
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

class AsyncConnection:
    async def open_connection(self):
        print("ASYNC CONNECTION OPENED")

    async def close_connection(self):
        print("ASYNC CONNECTION CLOSED")

@asynccontextmanager
async def async_lifespan() -> AsyncGenerator[AsyncConnection, None]:
    connection = AsyncConnection()
    await connection.open_connection()

    try:
        yield connection
    finally:
        await connection.close_connection()

async def run_graph(conn: AsyncConnection):
    # Simula a execução do grafo
    print("Olá, LLM! Executando workflow...")
```

E o nosso ponto de entrada (main) ficaria assim:

```python
async def main():
    async with async_lifespan() as conn:
        await run_graph(conn)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Por que isso é importante para Checkpointers?

Quando configuramos um checkpointer no LangGraph, como o AsyncSqliteSaver ou
PostgresSaver, eles herdam de BaseCheckpointSaver. É uma boa prática injetar a
conexão de banco de dados nesses checkpointers.

Ao usar o padrão Lifespan, você garante que:

- A conexão é criada antes do grafo ser montado.
- O grafo utiliza essa conexão durante a execução.
- A conexão é encerrada graciosamente ao final, liberando recursos do banco de
  dados.

Isso é especialmente útil se você usa pools de conexão ou se sua aplicação roda
como um serviço contínuo (como uma API FastAPI), onde o Lifespan gerencia o
tempo de vida da aplicação inteira, não apenas de uma única execução.

---

## Conclusão

Gerenciar recursos corretamente é o que separa scripts de hobby de aplicações
robustas. O padrão Lifespan, emprestado do ecossistema ASGI/FastAPI, casa
perfeitamente com a arquitetura do LangGraph.

Nas próximas etapas do nosso projeto, vamos utilizar essa estrutura para
inicializar nossos checkpointers de banco de dados reais, permitindo que nossos
agentes tenham memória de longo prazo de forma segura e eficiente.

Até o próximo algo que eu criar... tamo junto!
