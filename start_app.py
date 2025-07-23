#!/usr/bin/env python3
"""
Script de inicialização robusto para Streamlit
"""
import os
import sys
import subprocess

def main():
    # Obtém a porta
    port = os.environ.get('PORT', '8501')
    
    print(f"Iniciando aplicacao na porta {port}")
    
    # Lista arquivos disponíveis
    import glob
    python_files = glob.glob('*.py')
    print(f"Arquivos Python encontrados: {python_files}")
    
    # Determina qual arquivo usar
    main_file = None
    for candidate in ['app_main.py', 'Interface.py', 'streamlit_app.py']:
        if candidate in python_files:
            main_file = candidate
            break
    
    if not main_file:
        print("Nenhum arquivo principal encontrado!")
        sys.exit(1)
    
    print(f"Usando arquivo: {main_file}")
    
    # Executa streamlit
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', main_file,
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.enableCORS', 'false'
    ]
    
    print(f"Executando comando: {' '.join(cmd)}")
    
    try:
        os.execvp(sys.executable, cmd)
    except Exception as e:
        print(f"Erro ao executar: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
