import os
import requests
import time

# Obtenemos credenciales desde variables de entorno
API_KEY_FOOTBALL = os.environ["API_KEY_FOOTBALL"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Headers de la API-Football
HEADERS = {
    "X-RapidAPI-Key": API_KEY_FOOTBALL,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# IDs de ligas que activan el mercado 'Under X' en Bet365
ligas_validas = [
    292,  # Corea K-League 1
    197,  # China Super League
    278,  # Uruguay Liga AUF
    233,  # Sudáfrica Premier Shift
    284,  # Perú Liga 1
    297,  # Finlandia Veikkausliiga
    259,  # EE.UU. USL Championship
    296,  # Ecuador Liga Pro Serie A
    276,  # Brasil Brasileirão Femenino
    558,  # CONCACAF Gold Cup
    398   # UEFA Sub-21
]

def enviar_telegram(mensaje):
    """Envía un mensaje a Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("✅ Mensaje enviado a Telegram correctamente.")
    else:
        print("❌ Error al enviar mensaje a Telegram:", response.text)

def obtener_partidos_en_vivo():
    """Consulta la API para detectar partidos ideales."""
    print("🔎 Buscando partidos en vivo ideales...\n")
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    params = {"live": "all"}

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()
        partidos = data.get('response', [])

        for match in partidos:
            fixture = match['fixture']
            league = match['league']
            goals = match['goals']
            minuto = fixture['status']['elapsed']

            total_goles = (goals['home'] or 0) + (goals['away'] or 0)
            liga_id = league['id']

            if (
                liga_id in ligas_validas and
                minuto is not None and
                51 <= minuto <= 61 and
                1 <= total_goles <= 3
            ):
                mensaje = f"""⚽ PARTIDO IDEAL DETECTADO
🏆 {league['name']}
🆚 {match['teams']['home']['name']} vs {match['teams']['away']['name']}
⏱ Minuto: {minuto}
🔢 Goles totales: {total_goles}
✅ Revisa mercado 'Under X' (+4 goles)"""
                print(mensaje)
                enviar_telegram(mensaje)

    except Exception as e:
        print("⚠️ Error al consultar API:", e)
        enviar_telegram("⚠️ Error al consultar API-Football. Posible límite alcanzado.")

# Bucle principal: se repite cada 2 minutos
while True:
    obtener_partidos_en_vivo()
    print("⏳ Esperando 120 segundos...\n")
    time.sleep(120)
