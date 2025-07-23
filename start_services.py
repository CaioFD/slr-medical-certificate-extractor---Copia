#!/usr/bin/env python3
"""
Script para rodar FastAPI e Streamlit simultaneamente no Render
"""
import os
import subprocess
import sys
import threading
import time
import signal

def run_fastapi():
    """Roda o servidor FastAPI"""
    port = int(os.environ.get("PORT", 8000))
    cmd = [
        "uvicorn", 
        "main:app", 
        "--host", "0.0.0.0", 
        "--port", str(port)
    ]
    
    print(f"🚀 Iniciando FastAPI na porta {port}")
    subprocess.run(cmd)

def run_streamlit():
    """Roda o servidor Streamlit"""
    # Streamlit roda em uma porta diferente
    streamlit_port = int(os.environ.get("STREAMLIT_PORT", 8501))
    
    cmd = [
        "streamlit", 
        "run", 
        "Interface.py",
        "--server.port", str(streamlit_port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    
    print(f"🎨 Iniciando Streamlit na porta {streamlit_port}")
    subprocess.run(cmd)

def signal_handler(signum, frame):
    """Handler para encerramento gracioso"""
    print("🛑 Encerrando serviços...")
    sys.exit(0)

if __name__ == "__main__":
    # Registra handler para sinais
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Detecta qual serviço rodar baseado na variável de ambiente
    service_type = os.environ.get("SERVICE_TYPE", "both")
    
    if service_type == "api":
        # Roda apenas FastAPI
        run_fastapi()
    elif service_type == "streamlit":
        # Roda apenas Streamlit
        run_streamlit()
    else:
        # Roda ambos em threads separadas
        print("🔄 Iniciando FastAPI e Streamlit...")
        
        # Thread para FastAPI
        api_thread = threading.Thread(target=run_fastapi, daemon=True)
        api_thread.start()
        
        # Aguarda um pouco antes de iniciar o Streamlit
        time.sleep(3)
        
        # Roda Streamlit no thread principal
        run_streamlit()
