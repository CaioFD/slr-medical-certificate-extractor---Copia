#!/bin/bash
set -e

echo "🚀 Iniciando aplicação Streamlit..."
echo "Porta: $PORT"
echo "Diretório atual: $(pwd)"
echo "Arquivos disponíveis:"
ls -la *.py

# Verifica se o arquivo existe
if [ ! -f "Interface.py" ]; then
    echo "❌ Erro: Interface.py não encontrado!"
    exit 1
fi

echo "✅ Interface.py encontrado"
echo "🔄 Executando Streamlit..."

# Executa o Streamlit com configurações básicas
exec streamlit run Interface.py \
  --server.port=$PORT \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false
