#!/usr/bin/env python3
"""
Launcher simples e estável para Streamlit
"""
import os
import sys

def main():
    port = os.environ.get('PORT', '8501')
    
    # Configurações via argumentos simples
    sys.argv = [
        'streamlit',
        'run',
        'app_main.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true'
    ]
    
    # Executa streamlit
    import streamlit.web.cli as stcli
    stcli.main()

if __name__ == '__main__':
    main()
