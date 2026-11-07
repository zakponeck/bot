import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# 1. Mandamos la página web al fondo (para que solo sea un despertador silencioso)
class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("OK", "utf-8"))
        
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
        
    def log_message(self, format, *args):
        pass # Silencia los textos de red para no ensuciar la consola

def run_server():
    PORT = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", PORT), SimpleServer)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

import time

# 2. Bot en bucle: si termina (por autoupdate o por error), se relanza
os.environ["PYTHONUNBUFFERED"] = "1"
token = os.environ.get("BOT_TOKEN", "")

fallos_seguidos = 0
while True:
    # Reescribimos .env por si la actualización lo pisó
    with open(".env", "w") as f:
        f.write(f"BOT_TOKEN={token}\n")

    print("Iniciando el proceso principal del bot...", flush=True)
    inicio = time.time()
    os.system("yes '' | python main.py --autoupdate")
    duracion = time.time() - inicio

    # Si duró menos de 30s, cuenta como fallo y esperamos más
    if duracion < 30:
        fallos_seguidos += 1
    else:
        fallos_seguidos = 0

    espera = min(5 * (2 ** fallos_seguidos), 120)
    print(f"Bot terminó tras {duracion:.0f}s. Reiniciando en {espera}s...", flush=True)
    time.sleep(espera)
