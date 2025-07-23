FROM python:3.11-slim

# Instalar dependências do sistema para OCR e processamento de imagens
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgcc-s1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar e instalar dependências Python
COPY requirements.prod.txt .
RUN pip install --no-cache-dir -r requirements.prod.txt

# Copiar código da aplicação
COPY . .

# Criar diretório temporário
RUN mkdir -p temp

# Expor porta
EXPOSE 8000

# Comando para iniciar aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
