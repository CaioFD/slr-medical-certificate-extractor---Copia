#!/bin/bash
echo "🚀 Iniciando aplicação Streamlit..."
echo "Porta: $PORT"
echo "Comando: streamlit run Interface.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true"

# Executa o Streamlit
streamlit run Interface.py \
  --server.port=$PORT \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false
