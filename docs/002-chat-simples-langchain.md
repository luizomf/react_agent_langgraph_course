# Um Chat Simples Com LangChain

Na maioria das aulas vamos usar pelo menos um LLM para executar qualquer tarefa
que precisarmos.

Com o **LangChain**, você pode escolher qualquer LLM e provider de sua
preferência, seja pago, gratuito, local ou online.

---

## Ollama (local)

Quando estou testando alguma coisa com LLMs nos meus códigos, prefiro usar
modelos locais com **Ollama** (ou similares). Isso me permite fazer testes mais
complexos sem estourar o limite de tokens gratuitos ou gastar demais com APIs
pagas.

Se você também quiser usar Ollama, já fiz um vídeo sobre isso no canal:

- [Como Usar Ollama para LLMs no Seu Computador?](https://youtu.be/9Yz42WSISr4?si=aBVdWmfR8aQmtKD4)

---

## Google AI Studio (API gratuita)

Nem todo mundo tem hardware suficiente para rodar um modelo local. Geralmente
isso exige uma boa CPU/GPU e bastante espaço em disco e memória. Mesmo quando o
hardware dá conta, pode ser que o modelo não esteja otimizado para a sua máquina
e acabe rodando de forma tão lenta que inviabiliza os testes.

Nesses casos, a alternativa são **APIs externas** (gratuitas ou pagas).

No momento em que escrevo este texto, a **Google** oferece uma API Key gratuita
para desenvolvedores e entusiastas. Isso permite usar os modelos **Gemini**,
suficientes para nossos testes. Você pode gerar a chave no link:

- [Google AI Studio](https://aistudio.google.com/apikey)

---

## API paga

Se você não conseguir usar nenhuma das opções anteriores, sempre existe a
possibilidade de usar uma API paga. Geralmente, o custo inicial não é alto (no
momento em torno de 5 dólares de créditos mínimos).

Basta criar uma conta em um provider como Google, Anthropic, OpenAI ou outro,
adicionar créditos e obter sua **API Key**.

Links diretos para geração de chave:

- [Google AI Studio](https://aistudio.google.com/apikey)
- [OpenAI API Key](https://platform.openai.com/api-keys)
- [Anthropic API Key](https://console.anthropic.com/settings/keys)

---

## Variáveis de ambiente e o arquivo `.env`

Se optar por uma API externa (paga ou gratuita), é importante carregar suas
variáveis de ambiente de forma **segura**.

Crie um arquivo chamado `.env` na raiz do seu projeto com o seguinte conteúdo:

```sh
ANTHROPIC_API_KEY="VALOR"
OPENAI_API_KEY="VALOR"
GOOGLE_API_KEY="VALOR"
```

Para carregar esse arquivo, você pode usar o pacote `python-dotenv` ou deixar o
`uv` cuidar disso automaticamente:

```bash
uv run --env-file=".env" caminho/do/arquivo.py
```

Depois de carregar o `.env`, teste se as variáveis estão acessíveis com:

```python
import os

print(f"{os.getenv('GOOGLE_API_KEY', 'Não configurado')=}")
print(f"{os.getenv('ANTHROPIC_API_KEY', 'Não configurado')=}")
print(f"{os.getenv('OPENAI_API_KEY', 'Não configurado')=}")
```

Se os valores aparecerem corretamente, está tudo certo.

**IMPORTANTE:** nunca versionar o arquivo `.env` nem expor suas API Keys no
GitHub. Adicione o `.env` ao `.gitignore` do projeto para evitar problemas de
segurança.

---

## Chat simples com LangChain: Primeiro teste

A primeira coisa é instalar o **LangChain** (`langchain`) e os providers que
você pretende usar. Esse pacote já depende de outros internos como
`langchain-core`, `langgraph`, `pydantic` e vários outros.

### Instalação do(s) pacote(s)

```sh
uv add "langchain[ollama]" -U --pre       # para usar Ollama local
uv add "langchain[google-genai]" -U --pre # para modelos Gemini (Google)
uv add "langchain[openai]" -U --pre       # para modelos da OpenAI
uv add "langchain[anthropic]" -U --pre    # para modelos da Anthropic
```

Sobre as flags:

- `-U` - força upgrade se o pacote já estiver instalado.
- `--pre` - necessário enquanto o LangChain está em transição para a versão 1
  (pré-release no momento em que escrevo). Se a versão estável já tiver saído
  quando você ler isso, `--pre` pode ser omitido.

Você não precisa instalar todos os providers, apenas os que pretende usar. Se
quiser instalar todos de uma vez:

```sh
uv add "langchain[ollama,google-genai,openai,anthropic]" -U --pre
```

Exemplo de como fica no `pyproject.toml`:

```toml
dependencies = [
    "langchain[anthropic,google-genai,ollama,openai]>=1.0.0a6",
]
```

### Testando tudo e criando dois chats manualmente

Vou manter as partes de código em pastas separadas para as aulas. Essas pastas
podem ter um ou vários arquivos.

A nomenclatura de pastas será `src/examples/exNNN`, onde `NNN` representa a
sequência em que a aula foi criada (001, 002, 003, ..., 999). Espero que eu não
passe de 999 exemplos haha.

Para essa aula, nada mais justo do que começarmos com `ex001`, então acesse:

- [`src/examples/ex001/main.py`](../src/examples/ex001/main.py)

Deixei os comentários no código.

E só para você não ficar na mão, também criei um segundo exemplo mostrando um
chat com `SystemMessage`, `HumanMessage` e `AIMessage`. Isso nos permite montar
um histórico bem rústico em um loop para conversarmos com o modelo sem que ele
tenha amnésia (fique esquecendo do que estamos falando). Acesse:

- [`src/examples/ex002/main.py`](../src/examples/ex002/main.py)

---
