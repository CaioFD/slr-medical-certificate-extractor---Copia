"""
Aplicação híbrida: Streamlit como frontend + FastAPI como backend interno
"""
import streamlit as st
import multiprocessing
import uvicorn
import threading
import time
import os
from main import app

def run_fastapi_background():
    """Roda FastAPI em background na porta 8000"""
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

def start_background_api():
    """Inicia a API em uma thread separada"""
    if not hasattr(st.session_state, 'api_started'):
        # Inicia FastAPI em thread separada
        api_thread = threading.Thread(target=run_fastapi_background, daemon=True)
        api_thread.start()
        
        # Aguarda a API inicializar
        time.sleep(2)
        
        st.session_state.api_started = True
        print("✅ FastAPI iniciada em background")

if __name__ == "__main__":
    # Inicia a API em background quando necessário
    start_background_api()
