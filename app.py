import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def start_bot():
    # 1. Fuerza a la consola a mostrar en vivo todo lo que hace el bot
    os.environ["PYTHONUNBUFFERED"] = "1"
    
    token = os.environ.get("BOT_TOKEN", "")
    with open(".env", "w") as f:
        f.write(f"BOT_TOKEN={token}\n")
        
    # 2. Inyecta los "Enter" automáticos para saltar pantallas de actualización
    os.system("yes '' | python main.py --autoupdate")

threading.Thread(target=start_bot, daemon=True).start()

class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("<html><body><h1>🚀 Servidor Activo</h1></body></html>", "utf-8"))
    
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

PORT = int(os.environ.get("PORT", 10000))
server = HTTPServer(("0.0.0.0", PORT), SimpleServer)
server.serve_forever()
