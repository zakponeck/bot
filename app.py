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

# ---------- 2. Configuración ----------
env = os.environ.copy()
env["PYTHONUNBUFFERED"] = "1"

# Limpia espacios y comillas por si se pegaron junto con el token
token = os.environ.get("BOT_TOKEN", "").strip().strip('"').strip("'")

# AUTOUPDATE=0 en Render desactiva la actua
