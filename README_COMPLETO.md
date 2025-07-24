# 🏥 Sistema de Extração e Validação de Atestados Médicos

> **Plataforma automatizada para análise, validação e processamento de atestados médicos utilizando OCR com IA e validação de dados médicos.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45.1-red.svg)](https://streamlit.io)
[![Google Gemini](https://img.shields.io/badge/OCR-Google%20Gemini-orange.svg)](https://ai.google.dev)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue.svg)](https://postgresql.org)

---

## 📋 Visão Geral

Este sistema automatiza completamente o processo de validação de atestados médicos, desde a extração de texto via OCR até a validação de dados médicos em bases oficiais. Utiliza inteligência artificial para identificar e extrair informações críticas dos documentos, reduzindo fraudes e agilizando processos de RH.

### 🎯 **Principais Funcionalidades:**
- ✅ **OCR Inteligente** com Google Gemini Vision API
- ✅ **Validação de CRM** médico via API do CFM
- ✅ **Verificação de CID** contra base oficial CID-10
- ✅ **Interface Web** responsiva com Streamlit
- ✅ **Sistema de Login** e auditoria
- ✅ **Suporte a múltiplos formatos** (PDF, JPG, PNG, JPEG)
- ✅ **Deploy em nuvem** (Render) e execução local

---

## 🏗️ Arquitetura do Projeto

### **📁 Estrutura de Diretórios:**

```
slr-medical-certificate-extractor/
├── INTERFACES PRINCIPAIS
│   ├── Interface.py              # Interface principal (Render/Produção)
│   ├── app_main.py              # Interface principal alternativa  
│   ├── app_main_local.py        # Interface otimizada para local
│   ├── app_standalone.py        # Interface independente (sem APIs)
│   └── app_hybrid.py            # Interface híbrida (local+API)
│
├── PROCESSAMENTO OCR
│   ├── ocr_real.py              # OCR principal (Google Gemini)
│   ├── ocr_real_simple.py       # OCR simplificado para local
│   └── extract_info.py          # Extração básica de informações
│
├── BANCO DE DADOS
│   ├── database.py              # Conexão PostgreSQL completa
│   ├── database_simple.py       # Banco simplificado (memória/local)
│   ├── models.py                # Modelos de dados (Pydantic)
│   └── init_db.py               # Inicialização do banco
│
├── VALIDAÇÃO E AUTENTICAÇÃO
│   ├── auth.py                  # Sistema de autenticação
│   ├── crm_validator.py         # Validação de CRM via CFM API
│   ├── cid_validator.py         # Validação de CID-10
│   └── atestado_validator.py    # Validação completa de atestados
│
├── DADOS E CONFIGURAÇÃO
│   ├── data/                    # Dados de teste e bases de referência
│   │   ├── atestado*.jpg        # Atestados médicos de exemplo
│   │   ├── CID-10.csv          # Base oficial de códigos CID-10
│   │   └── sample_*.csv        # Dados de exemplo
│   ├── .env                     # Configurações de ambiente
│   ├── .env_template           # Template de configuração
│   └── .streamlit/config.toml  # Configuração do Streamlit
│
├── DEPLOY E EXECUÇÃO
│   ├── requirements.txt         # Dependências principais
│   ├── requirements_local.txt   # Dependências para local
│   ├── requirements_prod.txt    # Dependências para produção
│   ├── Dockerfile              # Container Docker
│   ├── Procfile                # Deploy Heroku
│   ├── render.yaml             # Deploy Render
│   └── start.sh                # Script de inicialização
│
├── TESTES E UTILITÁRIOS
│   ├── teste_atestado4.py       # Teste específico
│   ├── teste_todos_atestados.py # Teste geral
│   ├── script_cid.py           # Utilitário CID
│   └── launcher.py             # Lançador alternativo
│
└──  DOCUMENTAÇÃO
    ├── README.md               # Este arquivo
    ├── LEIA-ME_LOCAL.md       # Guia execução local
    └── CORRECOES_APLICADAS.md # Log de correções
```

---

## 🔧 Componentes Principais

### **🎯 1. INTERFACES (Frontend)**

#### **`Interface.py`** - Interface Principal de Produção
- **Função:** Interface web principal usada no deploy do Render
- **Características:**
  - Sistema de login com banco PostgreSQL
  - Upload de arquivos (PDF, JPG, PNG, JPEG)
  - OCR via Google Gemini
  - Validação de CRM via API CFM
  - Responsiva e otimizada para produção
- **Uso:** `streamlit run Interface.py`

#### **`app_main_local.py`** - Interface Local Otimizada
- **Função:** Versão simplificada para execução local
- **Características:**
  - Usa `ocr_real_simple.py` e `database_simple.py`
  - Menor quantidade de dependências
  - Funciona sem PostgreSQL (memória)
  - OCR melhorado com correções específicas
- **Uso:** `streamlit run app_main_local.py`

#### **`app_standalone.py`** - Interface Independente
- **Função:** Versão que funciona sem APIs externas
- **Características:**
  - Não depende de APIs do CFM
  - OCR local apenas
  - Ideal para ambientes isolados
- **Uso:** Para cenários sem internet

### **🧠 2. PROCESSAMENTO OCR**

#### **`ocr_real.py`** - OCR Principal
- **Função:** Processamento principal de OCR com Google Gemini
- **Características:**
  - Integração com Google Gemini Vision API
  - Prompt específico para atestados médicos brasileiros
  - Extração de: paciente, médico, CRM, CID, data, dias
  - Suporte a PDF e imagens
- **APIs:** Google Generative AI

#### **`ocr_real_simple.py`** - OCR Simplificado
- **Função:** Versão otimizada do OCR para execução local
- **Características:**
  - Mesmo motor (Google Gemini) mas simplificado
  - Correção automática de CRMs conhecidos
  - Prompt melhorado para distinguir paciente/médico
  - Fallback para processamento offline
- **Melhorias:** Resolve problema do atestado4 (Everton Alves)

### **🗄️ 3. BANCO DE DADOS**

#### **`database.py`** - Banco PostgreSQL Completo
- **Função:** Conexão e operações com PostgreSQL
- **Tabelas:**
  - `usuarios` - Dados de login
  - `atestados` - Registros processados
  - `logins` - Auditoria de acessos
- **Recursos:** Pool de conexões, transações, logs

#### **`database_simple.py`** - Banco Simplificado
- **Função:** Alternativa leve ao PostgreSQL
- **Características:**
  - Armazenamento em memória
  - Fallback para execução local
  - Mesma interface que database.py
  - Não requer configuração

#### **`models.py`** - Modelos de Dados
- **Função:** Definições de estruturas de dados
- **Modelos:** User, Atestado (usando Pydantic)

### **✅ 4. VALIDAÇÃO E AUTENTICAÇÃO**

#### **`auth.py`** - Sistema de Autenticação
- **Função:** Gerenciamento de login e sessões
- **Recursos:**
  - Hash de senhas
  - Validação de credenciais
  - Gerenciamento de sessões

#### **`crm_validator.py`** - Validação de CRM
- **Função:** Valida CRM médico via API do CFM
- **Características:**
  - Consulta à base oficial do CFM
  - Verificação de status ativo/inativo
  - Cache de resultados
- **API:** Conselho Federal de Medicina

#### **`cid_validator.py`** - Validação de CID
- **Função:** Valida códigos CID-10
- **Base:** Arquivo `CID-10.csv` oficial
- **Verificações:** Existência e validade do código

#### **`atestado_validator.py`** - Validação Completa
- **Função:** Orquestra todas as validações
- **Processo:**
  1. OCR do documento
  2. Validação de CRM
  3. Validação de CID
  4. Verificação de consistência
  5. Relatório final

### **📊 5. DADOS E CONFIGURAÇÃO**

#### **Pasta `data/`**
- **`atestado*.jpg/png/pdf`** - Documentos de teste
- **`CID-10.csv`** - Base oficial de códigos CID-10
- **`sample_*.csv`** - Dados de exemplo para treinamento

#### **Arquivos de Configuração**
- **`.env`** - Variáveis de ambiente (APIs, banco)
- **`.env_template`** - Template para configuração
- **`.streamlit/config.toml`** - Configurações do Streamlit

### **🚀 6. DEPLOY E EXECUÇÃO**

#### **Requirements (Dependências)**
- **`requirements.txt`** - Dependências principais completas
- **`requirements_local.txt`** - Dependências mínimas para local
- **`requirements_prod.txt`** - Dependências otimizadas para produção

#### **Deploy**
- **`Dockerfile`** - Containerização Docker
- **`Procfile`** - Deploy Heroku
- **`render.yaml`** - Deploy Render (recomendado)
- **`start.sh`** - Script de inicialização

---

## 🚀 Como Executar

### **🏠 Execução Local (Recomendado para desenvolvimento)**

```bash
# 1. Instalar dependências
pip install -r requirements_local.txt

# 2. Configurar API
cp .env_template .env
# Editar .env e adicionar GEMINI_API_KEY

# 3. Executar
streamlit run app_main_local.py

# 4. Acessar
http://localhost:8501
```

### **☁️ Deploy em Produção (Render)**

```bash
# 1. Fork/Clone do repositório
git clone <repo-url>

# 2. Deploy no Render
# - Conectar repositório
# - Build: pip install -r requirements_prod.txt
# - Start: streamlit run Interface.py --server.port $PORT --server.address 0.0.0.0

# 3. Configurar variáveis de ambiente no Render
GEMINI_API_KEY=sua_chave
CFM_API_KEY=sua_chave (opcional)
PSQL_HOST=seu_host (opcional)
```

---

## 🔑 Configuração de APIs

### **Google Gemini (OBRIGATÓRIO)**
1. Acesse: https://makersuite.google.com/app/apikey
2. Crie uma API Key
3. Adicione no `.env`: `GEMINI_API_KEY=sua_chave`

### **CFM API (OPCIONAL)**
1. Registre-se na API do CFM
2. Obtenha sua chave
3. Adicione no `.env`: `CFM_API_KEY=sua_chave`

### **PostgreSQL (OPCIONAL)**
```env
PSQL_HOST=localhost
PSQL_DB=atestados_db
PSQL_USER=postgres
PSQL_PASS=sua_senha
```

---

## 🧪 Testes

### **Teste Específico (Atestado4)**
```bash
python teste_atestado4.py
```

### **Teste Geral (Todos os Atestados)**
```bash
python teste_todos_atestados.py
```

### **Arquivos de Teste Disponíveis:**
- `atestado.pdf` - PDF exemplo
- `atestado2.jpeg` - Imagem simples
- `atestado3.jpg` - Imagem complexa
- `atestado4.jpeg` - Teste específico (Everton Alves)
- `Atestado5.png` - PNG de alta qualidade

---

## 🔍 Fluxo de Funcionamento

### **1. Upload do Documento**
```
Usuário → Interface Web → Validação de formato → Armazenamento temporário
```

### **2. Processamento OCR**
```
Documento → Google Gemini Vision → Extração de texto → Parsing estruturado
```

### **3. Validação de Dados**
```
Dados extraídos → Validação CRM (CFM API) → Validação CID (base local) → Verificação de consistência
```

### **4. Resultado Final**
```
Validações → Relatório consolidado → Armazenamento no banco → Exibição para usuário
```

---

## 🐛 Resolução de Problemas

### **Problema: JavaScript Errors no Streamlit**
```bash
# Limpar cache do navegador
Ctrl + Shift + Delete

# Ou usar modo anônimo
Ctrl + Shift + N
```

### **Problema: OCR identificando dados incorretos**
- O sistema tem correções automáticas para casos conhecidos
- Arquivo `ocr_real_simple.py` contém melhorias específicas
- Para novos casos, adicionar correções na função `corrigir_crm_conhecido()`

### **Problema: API não configurada**
- Verificar se `GEMINI_API_KEY` está no `.env`
- Testar com: `python -c "from ocr_real_simple import verificar_configuracao; print(verificar_configuracao())"`

---

## 📚 Dependências Principais

### **Core**
- **Streamlit 1.45.1** - Interface web
- **google-generativeai** - OCR via Gemini
- **Pillow** - Processamento de imagens
- **pandas** - Manipulação de dados
- **psycopg2-binary** - PostgreSQL

### **Desenvolvimento**
- **python-dotenv** - Variáveis de ambiente
- **pydantic** - Validação de dados
- **pdf2image** - Conversão PDF para imagem

---

*Sistema desenvolvido para automatizar e modernizar o processo de validação de atestados médicos, reduzindo fraudes e agilizando workflows de RH.* 🏥✨
