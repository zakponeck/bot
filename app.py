import os
import time
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# ---------- 1. Servidor web mínimo (para que Render lo vea como web) ----------
class SimpleServer(BaseHTTPRequestHandler):
    def _ok(self, body=True):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        if body:
            self.wfile.write(b"OK")

    def do_GET(self):
        self._ok()

    def do_HEAD(self):
        self._ok(body=False)

    def log_message(self, format, *args):
        pass  # silencia los logs de red


def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), SimpleServer).serve_forever()


threading.Thread(target=run_server, daemon=True).start()

# ---------- 2. Bot en bucle: si termina, se vuelve a lanzar ----------
env = os.environ.copy()
env["PYTHONUNBUFFERED"] = "1"

token = os.environ.get("BOT_TOKEN", "")
# AUTOUPDATE=0 en Render desactiva la actualización automática
autoupdate = os.environ.get("AUTOUPDATE", "1") == "1"

cmd = "yes '' | python main.py"
if autoupdate:
    cmd += " --autoupdate"

fallos = 0
while True:
    # Reescribimos .env por si una actualización lo pisó
    with open(".env", "w") as f:
        f.write(f"BOT_TOKEN={token}\n")

    print("Iniciando el proceso principal del bot...", flush=True)
    inicio = time.time()
    try:
        codigo = subprocess.call(cmd, shell=True, env=env)
    except Exception as e:
        print(f"Error lanzando el bot: {e}", flush=True)
        codigo = -1
    duracion = time.time() - inicio

    print(f"Bot terminó (código {codigo}) tras {duracion:.0f}s.", flush=True)
    if codigo in (137, -9):
        print("Posible falta de memoria (el sistema mató el proceso).", flush=True)

    # Si dura menos de 2 min cuenta como fallo y esperamos más cada vez
    if duracion < 120:
        fallos = min(fallos + 1, 10)
    else:
        fallos = 0

    espera = min(5 * (2 ** fallos), 120)
    print(f"Reiniciando en {espera}s...", flush=True)
    time.sleep(espera)
