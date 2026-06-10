# OBSERVAÇÃO IMPORTANTE: o `.env` tem que estar carregado aqui, seja por
# `python-dotenv` ou `uv`. Estou usando `uv` com o seguinte comando que já
# carrega automaticamente as variáveis de ambiente do `.env`.
#
# uv run --env-file='.env' src/examples/ex001/main.py
#

# Sobre `init_chat_model`
# `init_chat_model` nos permite criar uma instância de um chat model sem
# especificar a classe do provider.
# Por exemplo, se eu fosse usar OpenAI, seria necessário importar a classe
# `ChatOpenAI` do pacote `langchain_openai` isso deixaria o meu código um pouco
# mais acoplado, já que eu precisaria fazer isso sempre que mudasse de modelo.
# Pense nele como um atalho para criar um novo Chat Model.

from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

################################################################################

# Abaixo estão exemplos de uso do `init_chat_model` para Anthropic, OpenAI,
# Google GenAI e Ollama. Perceba que basta passar `provider:modelo` para o
# primeiro parâmetro.
# Você também pode passar argumentos específicos para o modelo, mas veremos isso
# ao longo das aulas.

# Exemplos:
# Para Anthropic
# llm = init_chat_model("anthropic:claude-3-7-sonnet-latest")

# Para OpenAI
# llm = init_chat_model("openai:gpt-5-nano")

# Para Google Gemini
# llm = init_chat_model("google_genai:gemini-2.5-flash")

# Para Ollama
# llm = init_chat_model("ollama:gpt-oss:20b")

################################################################################

# Vou usar Ollama neste exemplo

llm = init_chat_model("google_genai:gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))  # passa explicitamente

# A beleza do LangChain é que daqui para baixo, tudo é praticamente igual
# para qualquer modelo.
# O `invoke` é um método síncrono para enviar algo para a LLM e receber uma
# resposta se tudo estiver certo.
response = llm.invoke("Olá, como vai?")
print(response)

# A saída do print acima (formatada) fica mais ou menos assim:
# AIMessage(
#     content='Olá! Tudo bem? Como posso ajudar você hoje?',
#     additional_kwargs={},
#     response_metadata={
#         'model': 'gpt-oss:20b',
#         'created_at': '2025-09-20T18:08:56.340905Z',
#         'done': True,
#         'done_reason': 'stop',
#         'total_duration': 1680955000,
#         'load_duration': 124544834,
#         'prompt_eval_count': 72,
#         'prompt_eval_duration': 262665750,
#         'eval_count': 78,
#         'eval_duration': 1293221250,
#         'model_name': 'gpt-oss:20b'
#     },
#     id='run--f83c27bf-02da-4b7d-bdc5-16ec4be1139a-0',
#     usage_metadata={'input_tokens': 72, 'output_tokens': 78, 'total_tokens': 150}
# )
#
