# interface.py
import streamlit as st
import requests
from database import DB

st.set_page_config(page_title="Validação de Atestados", layout="centered")

API_URL = "http://127.0.0.1:8000"  # Continua usado para validar o atestado

# Inicializa session_state
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
    st.session_state["nome_completo"] = ""
    st.session_state["email"] = ""

def registrar_login(nome_usuario: str):
    """Insere um registro de login na tabela logins via database.py"""
    db = DB()
    db.conect()
    try:
        db.insert_login(nome_usuario)
    except Exception as e:
        st.error(f"Falha ao registrar login no banco: {e}")
    finally:
        db.deconect()

# === LOGIN ===
if not st.session_state["autenticado"]:
    st.title("🔐 Login")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    nome = st.text_input("Nome Completo")

    if st.button("Entrar"):
        # Autenticação mockada
        if email == "admin@teste.com" and senha == "123456" and nome.strip() != "":
            # Primeiro registra o login no banco
            registrar_login(nome.strip())
            # Depois atualiza o estado da sessão
            st.session_state["autenticado"] = True
            st.session_state["nome_completo"] = nome.strip()
            st.session_state["email"] = email
        else:
            st.error("Credenciais inválidas ou nome não preenchido.")

# === INTERFACE PRINCIPAL ===
else:
    st.success(f"Usuário autenticado: {st.session_state['nome_completo']} ({st.session_state['email']})")
    st.title("📄 Validar Atestado")

    arquivo = st.file_uploader("Envie um arquivo de atestado (.pdf, .jpg, .png)", type=["pdf", "jpg", "jpeg", "png"])

    if arquivo and st.button("Validar"):
        with st.spinner("Enviando e validando..."):
            files = {"file": (arquivo.name, arquivo.read(), arquivo.type)}
            try:
                response = requests.post(f"{API_URL}/validar_atestado/", files=files)
                if response.status_code == 200:
                    dados = response.json()
                    st.success("✅ Atestado válido!")
                    st.json(dados)
                else:
                    erro = response.json()
                    st.error("❌ Atestado inválido!")
                    st.json(erro)
            except Exception as e:
                st.error(f"Erro ao conectar com a API: {e}")



# import streamlit as st
# import requests
# import os

# st.set_page_config(page_title="Validação de Atestados", layout="centered")

# API_URL = "http://127.0.0.1:8000"  # Altere para o endereço da API se estiver online

# # Inicializa as variáveis no session_state para evitar erros
# if "autenticado" not in st.session_state:
#     st.session_state["autenticado"] = False
# if "nome_completo" not in st.session_state:
#     st.session_state["nome_completo"] = ""

# # === LOGIN ===
# if not st.session_state["autenticado"]:
#     st.title("🔐 Login")

#     email = st.text_input("Email")
#     senha = st.text_input("Senha", type="password")
#     nome = st.text_input("Nome Completo")

#     if st.button("Entrar"):
#         if email == "admin@teste.com" and senha == "123456" and nome.strip() != "":
#             st.session_state["autenticado"] = True
#             st.session_state["nome_completo"] = nome.strip()
#             st.session_state["email"] = email
#             # st.experimental_rerun() 
#         else:
#             st.error("Credenciais inválidas ou nome não preenchido.")

# # === INTERFACE PRINCIPAL ===
# if st.session_state["autenticado"]:
#     st.success(f"Usuário autenticado: {st.session_state['nome_completo']} ({st.session_state['email']})")
#     st.title("📄 Validar Atestado")

#     arquivo = st.file_uploader("Envie um arquivo de atestado (.pdf, .jpg, .png)", type=["pdf", "jpg", "jpeg", "png"])

#     if arquivo and st.button("Validar"):
#         with st.spinner("Enviando e validando..."):
#             files = {"file": (arquivo.name, arquivo.read(), arquivo.type)}
#             try:
#                 response = requests.post(f"{API_URL}/validar_atestado/", files=files)
#                 if response.status_code == 200:
#                     dados = response.json()
#                     st.success("✅ Atestado válido!")
#                     st.json(dados)
#                 else:
#                     erro = response.json()
#                     st.error("❌ Atestado inválido!")
#                     st.json(erro)
#             except Exception as e:
#                 st.error(f"Erro ao conectar com a API: {e}")
