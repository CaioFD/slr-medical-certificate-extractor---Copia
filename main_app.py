import os

# Configuração do Streamlit via variáveis de ambiente
os.environ['STREAMLIT_SERVER_PORT'] = os.environ.get('PORT', '8501')
os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'

# Importa a aplicação Streamlit
exec(open('Interface.py').read())
