"""
Launcher para Streamlit - Versão simplificada
"""
import os
import sys

# Adiciona argumentos para streamlit
sys.argv = [
    "streamlit",
    "run", 
    "Interface.py",
    "--server.port", os.environ.get('PORT', '8501'),
    "--server.address", "0.0.0.0",
    "--server.headless", "true",
    "--server.enableCORS", "false"
]

# Importa e executa streamlit
if __name__ == '__main__':
    import streamlit.web.cli as stcli
    stcli.main()
