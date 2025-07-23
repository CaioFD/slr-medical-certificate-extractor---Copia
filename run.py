import os
import sys

# Configurar porta
port = os.environ.get('PORT', '8501')

# Executar streamlit diretamente
from streamlit.web import cli as stcli

if __name__ == '__main__':
    sys.argv = [
        'streamlit',
        'run',
        'app_main.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true'
    ]
    sys.exit(stcli.main())
