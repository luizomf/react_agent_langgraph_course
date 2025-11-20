# Curso LangChain e LangGraph

Este repositório acompanha a playlist no YouTube sobre **LangChain** e
**LangGraph**.

👉 Playlist completa:
[YouTube — Curso LangChain & LangGraph](https://www.youtube.com/playlist?list=PLbIBj8vQhvm09IqqLYIwLF5dGrcbJzFZc)

O **foco principal é o vídeo**. Aqui você encontra apenas o **material de
apoio**: exemplos de código e explicações em texto que complementam o conteúdo
mostrado nas aulas.

---

## Estrutura do repositório

```

.
├── docs/               # Textos de apoio (um por aula)
│   ├── 001-*.md
│   ├── 002-*.md
│   └── ...
├── src/examples/       # Exemplos de código (um por aula)
│   ├── ex001/
│   ├── ex002/
│   └── ...
├── pyproject.toml      # Dependências (uv)
└── uv.lock

```

- Os arquivos em `docs/` seguem a numeração das aulas.
- Os diretórios em `src/examples/` seguem a mesma numeração, cada um com os
  códigos usados em aula.
- Assim, fica fácil relacionar vídeo <-> doc <-> exemplo de código.

---

## Aulas disponíveis

- [001 — LangChain vs LangGraph](./docs/001-langchain-vs-langgraph.md)
- [002 — Chat simples com LangChain](./docs/002-chat-simples-langchain.md)
- [003 — Introdução ao LangGraph](./docs/003-introducao-ao-langgraph.md)
- [004 — LangGraph com LLM](./docs/004-langgraph-com-llm.md)
- [005 — LangChain com LLM e Tools](./docs/005-llm-com-tools-langchain.md)
- [006 — LangStudio](./docs/006-langgraph-studio.md)
- [007 — config e RunnableConfig](./docs/007-runnable-config.md)

_(a lista será atualizada conforme novas aulas forem publicadas)_

---

## Como rodar os exemplos

Este projeto usa [uv](https://docs.astral.sh/uv/) para gerenciar dependências.

### Instalar dependências

```bash
uv sync
```

### Rodar exemplos

```bash
uv run --env-file=".env" src/examples/ex001/main.py
```

Na aula em vídeo estou mencionando o que estou usando em `src/examples/`
(`ex001`, `ex002`, ...). Verifique o doc correspondente em `docs/NNN-*.md` para
entender o que está acontecendo.

---

## Links importantes

- 🌐 Site: [otaviomiranda.com.br](https://www.otaviomiranda.com.br/)
- 📰 Newsletter: [luizomf.substack.com](https://luizomf.substack.com/)

Se quiser acompanhar novidades, tutoriais e conteúdos complementares, não
esqueça de se inscrever na newsletter.

---
