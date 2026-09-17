import os
import requests
from bs4 import BeautifulSoup

URL_PAGINA = "https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/"

# No Google Colab, use a URL pública do n8n Cloud ou de um túnel.
# Não use localhost:5678, pois ele aponta para o próprio Colab.
N8N_WEBHOOK = os.getenv(
    "N8N_WEBHOOK",
    "COLE_AQUI_A_URL_DO_WEBHOOK"
)

def extrair_clientes():
    resposta = requests.get(URL_PAGINA, timeout=30)
    resposta.raise_for_status()

    soup = BeautifulSoup(resposta.text, "html.parser")
    clientes = []

    for linha in soup.select("#clientes tbody tr"):
        colunas = linha.find_all("td")
        if len(colunas) < 4:
            continue

        clientes.append({
            "nome": colunas[0].get_text(" ", strip=True),
            "email": colunas[1].get_text(" ", strip=True),
            "saldo": colunas[2].get_text(" ", strip=True),
            "perfil": colunas[3].get_text(" ", strip=True),
        })

    return clientes

clientes = extrair_clientes()
print(f"Clientes encontrados: {len(clientes)}")
for cliente in clientes:
    print(cliente)

if N8N_WEBHOOK == "COLE_AQUI_A_URL_DO_WEBHOOK":
    raise ValueError(
        "Configure N8N_WEBHOOK com a URL de teste ou produção do seu Webhook n8n."
    )

payload = {"clientes": clientes}

resposta = requests.post(
    N8N_WEBHOOK,
    json=payload,
    headers={"Content-Type": "application/json"},
    timeout=60,
)

print("Status:", resposta.status_code)
print("Resposta:", resposta.text[:2000])
resposta.raise_for_status()
