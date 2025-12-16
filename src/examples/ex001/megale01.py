# main.py
from dotenv import load_dotenv
import os
from rich import print
# Carrega as variáveis do .env 

load_dotenv()

# Verifica se a variável foi carregada
print("GOOGLE_API_KEY =", os.getenv("GOOGLE_API_KEY"))



# Agora inicialize seu LLM normalmente
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    "google_genai:gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")  # passa explicitamente
)

response = llm.invoke("Olá, como vai?")
print(response)
