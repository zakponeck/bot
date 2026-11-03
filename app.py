import os
import threading
import gradio as gr

def start_bot():
    # 1. Crea el archivo de configuración con el token para que el bot no se detenga a preguntarlo
    token = os.environ.get("BOT_TOKEN", "")
    with open(".env", "w") as f:
        f.write(f"BOT_TOKEN={token}\n")
    
    # 2. Enciende el bot de forma automática sin hacer preguntas de actualización
    os.system("python main.py --autoupdate")

# Inicia el proceso del bot en segundo plano
threading.Thread(target=start_bot, daemon=True).start()

# Crea la página web para que Render detecte el puerto y el despertador funcione
with gr.Blocks() as demo:
    gr.Markdown("# 🚀 Servidor TKA Activo")
    gr.Markdown("El bot de Whiteout Survival se está ejecutando en segundo plano.")

# Conecta el puerto que Render exige
demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 10000)))
