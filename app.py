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

# 2. Ponemos al bot en el escenario principal para ver sus errores reales
os.environ["PYTHONUNBUFFERED"] = "1"
token = os.environ.get("BOT_TOKEN", "")

with open(".env", "w") as f:
    f.write(f"BOT_TOKEN={token}\n")

print("Iniciando el proceso principal del bot...")
# Mantenemos el truco de los 'Enter' automáticos
os.system("yes '' | python main.py --autoupdate")
