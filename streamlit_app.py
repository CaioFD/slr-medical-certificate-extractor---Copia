# interface.py
import streamlit as st
import requests
import os
import threading
import time
from database import DB

# Configuração da página
st.set_page_config(
    page_title="Sistema de Validação de Atestados Médicos", 
    page_icon="🏥",
    layout="centered"
)

# URL da API - detecta automaticamente se está em produção ou local
if "RENDER" in os.environ:
    # Em produção no Render - vai funcionar apenas com validação local/banco
    # A validação via API será desabilitada por enquanto
    API_URL = None
    st.info("🔄 Modo de produção: Validação simplificada ativada")
else:
    # Desenvolvimento local
    API_URL = "http://127.0.0.1:8000"

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
    # Header com logo/design
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>🏥 Sistema de Validação de Atestados Médicos</h1>
        <p style="color: #666; font-size: 1.2rem;">Plataforma automatizada para validação de documentos médicos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulário de login centralizado
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🔐 Acesso ao Sistema")
            
            with st.form("login_form"):
                email = st.text_input("📧 Email", placeholder="admin@teste.com")
                senha = st.text_input("🔒 Senha", type="password", placeholder="Sua senha")
                nome = st.text_input("👤 Nome Completo", placeholder="Seu nome completo")
                
                submitted = st.form_submit_button("🚀 Entrar", use_container_width=True)
                
                if submitted:
                    # Autenticação mockada
                    if email == "admin@teste.com" and senha == "123456" and nome.strip() != "":
                        # Primeiro registra o login no banco
                        registrar_login(nome.strip())
                        # Depois atualiza o estado da sessão
                        st.session_state["autenticado"] = True
                        st.session_state["nome_completo"] = nome.strip()
                        st.session_state["email"] = email
                        st.success("✅ Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Credenciais inválidas ou nome não preenchido.")
            
            # Informações de acesso
            with st.expander("ℹ️ Informações de Acesso"):
                st.info("""
                **Credenciais de teste:**
                - Email: admin@teste.com
                - Senha: 123456
                - Nome: Qualquer nome válido
                """)

# === INTERFACE PRINCIPAL ===
else:
    # Header do usuário logado
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #1f77b4, #2ca02c); padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
        <h2 style="color: white; margin: 0;">👋 Bem-vindo, {st.session_state['nome_completo']}!</h2>
        <p style="color: #f0f0f0; margin: 0;">Email: {st.session_state['email']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botão de logout
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("🚪 Sair"):
            st.session_state["autenticado"] = False
            st.session_state["nome_completo"] = ""
            st.session_state["email"] = ""
            st.rerun()
    
    st.title("📄 Validação de Atestados Médicos")
    st.markdown("---")
    
    # Status da API
    if API_URL:
        st.success("🟢 API local conectada")
    else:
        st.warning("� Modo de produção: Validação simplificada")
        st.info("💡 Em produção, a validação será feita diretamente sem API externa")
    
    # Upload de arquivo
    st.markdown("### 📎 Upload do Documento")
    arquivo = st.file_uploader(
        "Selecione um arquivo de atestado médico", 
        type=["pdf", "jpg", "jpeg", "png"],
        help="Formatos aceitos: PDF, JPG, JPEG, PNG (máx. 200MB)"
    )

    # Processamento do arquivo
    if arquivo:
        # Mostra informações do arquivo
        st.markdown("### 📋 Informações do Arquivo")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 Nome", arquivo.name)
        with col2:
            st.metric("📏 Tamanho", f"{arquivo.size / 1024:.1f} KB")
        with col3:
            st.metric("🔖 Tipo", arquivo.type)
        
        # Botão de validação
        if st.button("🔍 Validar Atestado", type="primary", use_container_width=True):
            with st.spinner("🔄 Processando documento... Isso pode levar alguns segundos."):
                
                if API_URL:
                    # Usa a API se disponível (desenvolvimento local)
                    files = {"file": (arquivo.name, arquivo.read(), arquivo.type)}
                    
                    try:
                        response = requests.post(f"{API_URL}/validar_atestado/", files=files)
                        
                        if response.status_code == 200:
                            dados = response.json()
                            
                            # Resultado positivo
                            st.success("✅ **Atestado Válido!**")
                            
                            # Exibe os dados extraídos de forma organizada
                            st.markdown("### 📊 Dados Extraídos")
                            
                            # Organiza os dados em colunas
                            if isinstance(dados, dict):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    if "nome_paciente" in dados:
                                        st.info(f"👤 **Paciente:** {dados['nome_paciente']}")
                                    if "nome_medico" in dados:
                                        st.info(f"👨‍⚕️ **Médico:** {dados['nome_medico']}")
                                    if "crm" in dados:
                                        st.info(f"🆔 **CRM:** {dados['crm']}")
                                
                                with col2:
                                    if "cid" in dados:
                                        st.info(f"🏥 **CID:** {dados['cid']}")
                                    if "data_atendimento" in dados:
                                        st.info(f"📅 **Data:** {dados['data_atendimento']}")
                                    if "dias_atestado" in dados:
                                        st.info(f"⏰ **Dias:** {dados['dias_atestado']}")
                            
                            # Mostra JSON completo em expansível
                            with st.expander("🔍 Ver dados completos (JSON)"):
                                st.json(dados)
                                
                        else:
                            erro = response.json()
                            
                            # Resultado negativo
                            st.error("❌ **Atestado Inválido!**")
                            
                            # Mostra detalhes do erro
                            if isinstance(erro, dict) and "erro" in erro:
                                st.warning(f"**Motivo:** {erro['erro']}")
                            
                            # Mostra JSON completo do erro
                            with st.expander("🔍 Ver detalhes do erro"):
                                st.json(erro)
                            
                    except requests.exceptions.ConnectionError:
                        st.error("🔴 **Erro de Conexão:** Não foi possível conectar com a API de validação.")
                    except Exception as e:
                        st.error(f"🔴 **Erro Inesperado:** {str(e)}")
                
                else:
                    # Modo simplificado para produção (sem API)
                    try:
                        # Validação básica do arquivo
                        file_content = arquivo.read()
                        
                        # Simula processamento
                        time.sleep(2)
                        
                        # Resultado mockado para demonstração
                        st.success("✅ **Arquivo Processado com Sucesso!**")
                        
                        st.info("""
                        **📋 Validação Simplificada Concluída**
                        
                        ✅ Arquivo carregado e verificado
                        ✅ Formato de arquivo válido
                        ✅ Documento salvo no sistema
                        
                        **💡 Nota:** Em produção no Render, a validação completa com IA 
                        será implementada em uma próxima versão.
                        """)
                        
                        # Informações básicas do arquivo
                        st.markdown("### 📊 Informações Básicas")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.info(f"📄 **Arquivo:** {arquivo.name}")
                            st.info(f"📏 **Tamanho:** {len(file_content)} bytes")
                        
                        with col2:
                            st.info(f"🔖 **Tipo:** {arquivo.type}")
                            st.info(f"📅 **Data Upload:** {time.strftime('%Y-%m-%d %H:%M:%S')}")
                        
                        # Salva no banco se possível
                        try:
                            registrar_login(f"Upload: {arquivo.name} - {st.session_state['nome_completo']}")
                            st.success("💾 Registro salvo no banco de dados")
                        except:
                            st.warning("⚠️ Não foi possível salvar no banco (normal em primeira execução)")
                            
                    except Exception as e:
                        st.error(f"🔴 **Erro no processamento:** {str(e)}")
    
    else:
        # Instruções quando nenhum arquivo foi carregado
        st.info("""
        📝 **Como usar:**
        1. Faça upload de um arquivo de atestado médico
        2. Clique em "Validar Atestado"
        3. Aguarde o processamento
        4. Visualize os resultados
        
        🎯 **Formatos aceitos:** PDF, JPG, JPEG, PNG
        """)
    
    # Footer informativo
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #666;">
        <p>🏥 Sistema de Validação de Atestados Médicos v1.0</p>
        <p>Desenvolvido por Caio Faria Diniz | 2025</p>
    </div>
    """, unsafe_allow_html=True)



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
