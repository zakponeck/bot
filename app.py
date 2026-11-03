import os
import threading
import gradio as gr

def start_bot():
    # Enciende el bot directamente (Render ya instaló todo)
    os.system("python main.py")

# Inicia el proceso del bot en segundo plano
threading.Thread(target=start_bot, daemon=True).start()

# Crea la página web para el despertador virtual
with gr.Blocks() as demo:
    gr.Markdown("# 🚀 Servidor TKA Activo")
    gr.Markdown("El bot de Whiteout Survival se está ejecutando en segundo plano.")

# Render necesita un puerto específico para mantener la web visible
demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 10000)))
