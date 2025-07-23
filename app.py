"""
Launcher simples para Streamlit
"""
import streamlit.web.cli as stcli
import sys
import os

if __name__ == '__main__':
    port = os.environ.get('PORT', '8501')
    
    sys.argv = [
        "streamlit",
        "run",
        "Interface.py",
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.headless", "true"
    ]
    
    sys.exit(stcli.main())
