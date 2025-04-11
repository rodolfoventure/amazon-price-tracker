import os
import requests
from bs4 import BeautifulSoup
import time

# Produto e alvo
url = "https://www.amazon.com.br/Ouro-Fino-Sem-numero-ATIVI/dp/B0849Z34ZM"
preco_alvo = 50.0

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36"
}

def enviar_notificacao(mensagem):
    token = os.environ.get("PUSHBULLET_TOKEN")
    if not token:
        print("❌ Token do Pushbullet não encontrado.")
        return
    data = {
        "type": "note",
        "title": "🔔 Alerta de preço Amazon!",
        "body": mensagem
    }
    resp = requests.post(
        "https://api.pushbullet.com/v2/pushes",
        json=data,
        headers={"Access-Token": token}
    )
    if resp.status_code == 200:
        print("✅ Notificação enviada!")
    else:
        print("❌ Erro ao enviar: ", resp.text)

def verificar_preco():
    try:
        resposta = requests.get(url, headers=headers)
        sopa = BeautifulSoup(resposta.content, "html.parser")
        preco_texto = sopa.find("span", class_="a-offscreen").get_text().strip()
        preco = float(preco_texto.replace("R$", "").replace(".", "").replace(",", "."))
        print(f"Preço atual: R$ {preco:.2f}")
        if preco < preco_alvo:
            mensagem = f"🔥 Preço baixou para R$ {preco:.2f}!\n{url}"
            enviar_notificacao(mensagem)
        else:
            print("Ainda acima do desejado. Sem notificação.")
    except Exception as e:
        print("Erro ao verificar preço:", e)

# Checa a cada 12 horas (opcional se rodar em loop)
if __name__ == "__main__":
    verificar_preco()
