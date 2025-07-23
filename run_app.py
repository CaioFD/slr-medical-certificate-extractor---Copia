#!/usr/bin/env python3
"""
Script de inicialização para Streamlit no Render
"""
import os
import sys
import subprocess

def main():
    """Inicia o Streamlit com configurações para produção"""
    
    # Obtém a porta do ambiente
    port = os.environ.get('PORT', '8501')
    
    print(f"🚀 Iniciando Streamlit na porta {port}")
    print(f"📁 Diretório: {os.getcwd()}")
    
    # Verifica se o arquivo existe
    if not os.path.exists('Interface.py'):
        print("❌ Erro: Interface.py não encontrado!")
        sys.exit(1)
    
    print("✅ Interface.py encontrado")
    
    # Comando para executar o Streamlit
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'Interface.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.enableCORS', 'false',
        '--server.enableXsrfProtection', 'false'
    ]
    
    print(f"🔄 Executando: {' '.join(cmd)}")
    
    # Executa o comando
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar Streamlit: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("🛑 Aplicação interrompida")
        sys.exit(0)

if __name__ == '__main__':
    main()
