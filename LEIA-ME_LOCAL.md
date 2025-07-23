# === ARQUIVO: LEIA-ME_LOCAL.md ===

# 🏥 Sistema de Validação de Atestados Médicos - Execução Local

## 📋 Arquivos Necessários para Rodar Localmente

### ✅ Arquivos OBRIGATÓRIOS:
```
app_main_local.py        # Interface principal do Streamlit
ocr_real_simple.py       # Processamento OCR simplificado
database_simple.py       # Banco de dados simplificado
requirements_local.txt   # Dependências Python
.env                     # Configurações (copie de .env_template)
```

### 🔄 Arquivos OPCIONAIS:
```
.env_template           # Template de configuração
LEIA-ME_LOCAL.md       # Este arquivo de instruções
```

## 🚀 Como Executar

### 1. Instalar Dependências:
```bash
pip install -r requirements_local.txt
```

### 2. Configurar API (OBRIGATÓRIO):
```bash
# Copie o template
cp .env_template .env

# Edite o .env e adicione sua chave do Gemini
GEMINI_API_KEY=sua_chave_aqui
```

### 3. Executar o Sistema:
```bash
streamlit run app_main_local.py
```

### 4. Acessar no Navegador:
```
http://localhost:8501
```

## 🔑 Obter Chave do Google Gemini

1. Acesse: https://makersuite.google.com/app/apikey
2. Clique em "Create API Key"
3. Copie a chave gerada
4. Cole no arquivo .env

## 🏆 Funcionalidades

✅ **Interface completa igual ao original**
✅ **OCR real com Google Gemini**
✅ **Sistema de login**
✅ **Processamento de PDF e imagens**
✅ **Banco de dados opcional**
✅ **Funciona sem PostgreSQL**

## 🔧 Configurações Opcionais

### PostgreSQL (Opcional):
Se quiser usar banco de dados real, configure no .env:
```
PSQL_HOST=localhost
PSQL_DB=atestados_db
PSQL_USER=postgres
PSQL_PASS=sua_senha
```

### Sem PostgreSQL:
O sistema funciona perfeitamente sem banco, armazenando dados em memória.

## 📞 Suporte

Em caso de problemas:
1. Verifique se todas as dependências estão instaladas
2. Confirme se a chave do Gemini está correta no .env
3. Execute: `streamlit run app_main_local.py --server.headless true`

## 🎯 Resumo Rápido

**Para funcionar localmente você precisa apenas:**
1. `app_main_local.py`
2. `ocr_real_simple.py` 
3. `database_simple.py`
4. `requirements_local.txt`
5. `.env` (com chave do Gemini)

**Comando para rodar:**
```bash
streamlit run app_main_local.py
```

**Login de teste:**
- Email: admin@teste.com
- Senha: 123456
- Nome: Qualquer nome
