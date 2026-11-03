import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def start_bot():
    # Crea el archivo de configuración con el token automáticamente
    token = os.environ.get("BOT_TOKEN", "")
    with open(".env", "w") as f:
        f.write(f"BOT_TOKEN={token}\n")
    
    # Enciende el bot sin hacer preguntas en la consola
    os.system("python main.py --autoupdate")

# Inicia el proceso del bot en segundo plano
threading.Thread(target=start_bot, daemon=True).start()

# Crea una mini página web de fábrica (ultra ligera, no requiere instalar Gradio)
class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = "<html><body><h1>🚀 Servidor TKA Activo</h1><p>El bot de Whiteout Survival está corriendo en segundo plano.</p></body></html>"
        self.wfile.write(bytes(html, "utf-8"))

# Conecta el puerto para que Render mantenga el servicio encendido
PORT = int(os.environ.get("PORT", 10000))
server = HTTPServer(("0.0.0.0", PORT), SimpleServer)
server.serve_forever()
