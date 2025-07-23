"""
Alternativa usando subprocess
"""
import os
import subprocess
import sys

def main():
    port = os.environ.get('PORT', '8501')
    
    print(f"🚀 Iniciando Streamlit na porta {port}")
    
    cmd = [
        'streamlit', 'run', 'Interface.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true'
    ]
    
    print(f"Executando: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
