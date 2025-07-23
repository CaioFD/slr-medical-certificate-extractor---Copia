# interface.py
import streamlit as st
import requests
import os
import threading
import time
from database import DB
from extract_info import extrair_informacoes_arquivo
import tempfile

# Configuração da página
st.set_page_config(
    page_title="Sistema de Validação de Atestados Médicos", 
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS para estabilizar a interface e evitar erros JS
st.markdown("""
<style>
    /* Remove elementos que podem causar conflitos JS */
    .reportview-container .main .block-container {
        max-width: 800px;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Estabiliza formulários */
    .stTextInput > div > div > input {
        background-color: white !important;
        border: 1px solid #ddd !important;
        border-radius: 4px !important;
        padding: 0.5rem !important;
    }
    
    /* Remove colunas vazias */
    .stTextInput > div {
        background-color: transparent !important;
    }
    
    /* Remove animações desnecessárias */
    .element-container {
        animation: none !important;
    }
    
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Disable default error handling */
    .stException {display: none;}
    
    /* Fix white columns issue */
    .row-widget.stTextInput {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# URL da API - detecta automaticamente se está em produção ou local
if "RENDER" in os.environ:
    # Em produção no Render - usa processamento real com IA
    API_URL = None
    # Configura ambiente de produção
    os.environ["ENVIRONMENT"] = "production"
    st.info("🔄 Modo de produção: Processamento real com IA ativado")
else:
    # Desenvolvimento local - permite escolher entre API e processamento local
    API_URL = "http://127.0.0.1:8000"
    st.info("💻 Modo de desenvolvimento: Processamento real disponível")

# Inicializa session_state
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
    st.session_state["nome_completo"] = ""
    st.session_state["email"] = ""

def registrar_login(nome_usuario: str):
    """Insere um registro de login na tabela logins via database.py"""
    try:
        db = DB()
        db.conect()
        
        # Verifica se a conexão foi bem-sucedida
        if db.conn is None:
            st.warning("⚠️ Banco de dados não disponível. Login registrado apenas na sessão.")
            return
            
        db.insert_login(nome_usuario)
        st.success("💾 Login registrado no banco de dados")
        
    except Exception as e:
        st.warning(f"⚠️ Não foi possível registrar no banco: {str(e)}")
        print(f"[ERRO] Falha ao registrar login no banco: {e}")
    finally:
        try:
            if 'db' in locals():
                db.deconect()
        except:
            pass

# === LOGIN ===
if not st.session_state["autenticado"]:
    # Header simples
    st.title("🏥 Sistema de Validação de Atestados Médicos")
    st.markdown("**Plataforma automatizada para validação de documentos médicos**")
    st.markdown("---")
    
    # Formulário de login mais simples
    st.subheader("🔐 Acesso ao Sistema")
    
    # Usando campos simples em vez de formulário complexo
    email = st.text_input("📧 Email", value="", placeholder="admin@teste.com")
    senha = st.text_input("🔒 Senha", type="password", value="", placeholder="Sua senha")
    nome = st.text_input("👤 Nome Completo", value="", placeholder="Seu nome completo")
    
    # Botão de login
    if st.button("🚀 Entrar", type="primary"):
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
        st.warning("⚡ Modo de produção: Validação simplificada")
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
        
        # Opção de processamento em desenvolvimento
        if API_URL and not "RENDER" in os.environ:
            st.markdown("### ⚙️ Modo de Processamento")
            modo_processamento = st.radio(
                "Escolha o método de processamento:",
                ["🤖 IA Local (Recomendado)", "🌐 API FastAPI"],
                help="IA Local: Processa diretamente com Gemini | API FastAPI: Usa endpoint local"
            )
            usar_ia_local = modo_processamento.startswith("🤖")
        else:
            usar_ia_local = True
        
        # Botão de validação
        if st.button("🔍 Validar Atestado", type="primary", use_container_width=True):
            with st.spinner("🔄 Processando documento... Isso pode levar alguns segundos."):
                
                if API_URL and not usar_ia_local:
                    # Usa a API se selecionado (desenvolvimento local)
                    files = {"file": (arquivo.name, arquivo.read(), arquivo.type)}
                    
                    try:
                        response = requests.post(f"{API_URL}/validar_atestado/", files=files)
                        
                        if response.status_code == 200:
                            dados = response.json()
                            
                            # Resultado positivo
                            st.success("✅ **Atestado Válido!**")
                            
                            # Exibe os dados extraídos de forma organizada
                            st.markdown("### 📋 Informações Extraídas do Atestado")
                            
                            # Organiza os dados em duas colunas
                            if isinstance(dados, dict):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown("#### 👤 Dados do Paciente")
                                    if "nome_paciente" in dados:
                                        st.info(f"**Nome:** {dados['nome_paciente']}")
                                    if "data_atendimento" in dados:
                                        st.info(f"**Data Atendimento:** {dados['data_atendimento']}")
                                    if "dias_atestado" in dados:
                                        st.info(f"**Dias de Atestado:** {dados['dias_atestado']} dias")
                                
                                with col2:
                                    st.markdown("#### 👨‍⚕️ Dados do Médico")
                                    if "nome_medico" in dados:
                                        st.info(f"**Nome:** {dados['nome_medico']}")
                                    if "crm" in dados:
                                        st.info(f"**CRM:** {dados['crm']}")
                                    if "cid" in dados:
                                        st.info(f"**CID:** {dados['cid']}")
                                
                                # Resumo em formato de tabela
                                st.markdown("#### 📊 Resumo Completo")
                                
                                # Cria DataFrame para exibição em tabela
                                import pandas as pd
                                
                                resumo_data = {
                                    "Campo": [],
                                    "Valor": []
                                }
                                
                                # Adiciona campos disponíveis
                                if "nome_paciente" in dados:
                                    resumo_data["Campo"].append("Nome do Paciente")
                                    resumo_data["Valor"].append(dados["nome_paciente"])
                                if "nome_medico" in dados:
                                    resumo_data["Campo"].append("Nome do Médico")
                                    resumo_data["Valor"].append(dados["nome_medico"])
                                if "crm" in dados:
                                    resumo_data["Campo"].append("CRM do Médico")
                                    resumo_data["Valor"].append(dados["crm"])
                                if "cid" in dados:
                                    resumo_data["Campo"].append("CID")
                                    resumo_data["Valor"].append(dados["cid"])
                                if "dias_atestado" in dados:
                                    resumo_data["Campo"].append("Dias de Atestado")
                                    resumo_data["Valor"].append(f"{dados['dias_atestado']} dias")
                                if "data_atendimento" in dados:
                                    resumo_data["Campo"].append("Data de Atendimento")
                                    resumo_data["Valor"].append(dados["data_atendimento"])
                                
                                resumo_data["Campo"].append("Status da Validação")
                                resumo_data["Valor"].append("✅ Válido")
                                
                                if resumo_data["Campo"]:  # Se há dados para mostrar
                                    df_resumo = pd.DataFrame(resumo_data)
                                    st.dataframe(df_resumo, use_container_width=True, hide_index=True)
                            
                            # Mostra JSON completo em expansível
                            with st.expander("🔍 Ver dados técnicos completos (JSON)"):
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
                    # Processamento REAL do atestado usando IA
                    try:
                        # Salva o arquivo temporariamente para processamento
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{arquivo.name.split('.')[-1]}") as temp_file:
                            temp_file.write(arquivo.read())
                            temp_file_path = temp_file.name
                        
                        st.info("🔍 Processando documento com IA... Extraindo informações reais...")
                        
                        # Usa o sistema real de extração
                        atestado_extraido = extrair_informacoes_arquivo(temp_file_path)
                        
                        # Remove arquivo temporário
                        os.unlink(temp_file_path)
                        
                        if atestado_extraido:
                            # Resultado positivo
                            st.success("✅ **Atestado Processado com Sucesso!**")
                            
                            # Converte o objeto Atestado para dicionário para exibição
                            dados_extraidos = {
                                "valido": True,
                                "nome_paciente": atestado_extraido.nomePaciente or "Não identificado",
                                "nome_medico": atestado_extraido.nomeMedico or "Não identificado",
                                "crm_medico": atestado_extraido.crmMedico or "Não identificado",
                                "cid": atestado_extraido.cid or "Não identificado",
                                "dias_atestado": str(atestado_extraido.diasAtestado) if atestado_extraido.diasAtestado else "Não identificado",
                                "data_atendimento": str(atestado_extraido.dataAtendimento) if atestado_extraido.dataAtendimento else "Não identificado",
                                "observacoes": f"Informações extraídas via IA do arquivo {arquivo.name}",
                                "arquivo_processado": arquivo.name,
                                "data_processamento": time.strftime('%Y-%m-%d %H:%M:%S')
                            }
                            
                            # Exibe os dados extraídos de forma organizada
                            st.markdown("### 📋 Informações Extraídas do Atestado")
                        
                        # Organiza os dados em duas colunas
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("#### 👤 Dados do Paciente")
                            st.info(f"**Nome:** {dados_extraidos['nome_paciente']}")
                            st.info(f"**Data Atendimento:** {dados_extraidos['data_atendimento']}")
                            st.info(f"**Dias de Atestado:** {dados_extraidos['dias_atestado']} dias")
                            
                        with col2:
                            st.markdown("#### 👨‍⚕️ Dados do Médico")
                            st.info(f"**Nome:** {dados_extraidos['nome_medico']}")
                            st.info(f"**CRM:** {dados_extraidos['crm_medico']}")
                            st.info(f"**CID:** {dados_extraidos['cid']}")
                        
                        # Seção adicional com mais detalhes
                        st.markdown("#### 🏥 Informações Médicas")
                        col3, col4 = st.columns(2)
                        
                        with col3:
                            st.success(f"**Diagnóstico (CID):** {dados_extraidos['cid']}")
                            st.info(f"**Descrição:** {dados_extraidos['observacoes']}")
                            
                        with col4:
                            st.success(f"**Período Afastamento:** {dados_extraidos['dias_atestado']} dias")
                            st.info(f"**Data Início:** {dados_extraidos['data_atendimento']}")
                        
                        # Informações técnicas do processamento
                        st.markdown("#### ⚙️ Detalhes do Processamento")
                        col5, col6 = st.columns(2)
                        
                        with col5:
                            st.metric("📄 Arquivo", dados_extraidos['arquivo_processado'])
                            st.metric("📅 Processado em", dados_extraidos['data_processamento'])
                            
                        with col6:
                            st.metric("📏 Tamanho", f"{arquivo.size} bytes")
                            st.metric("✅ Status", "Processado com IA")
                        
                        # Resumo em formato de tabela
                        st.markdown("#### 📊 Resumo Completo")
                        
                        # Cria DataFrame para exibição em tabela
                        import pandas as pd
                        
                        resumo_data = {
                            "Campo": [
                                "Nome do Paciente",
                                "Nome do Médico", 
                                "CRM do Médico",
                                "CID",
                                "Dias de Atestado",
                                "Data de Atendimento",
                                "Status da Validação"
                            ],
                            "Valor": [
                                dados_extraidos['nome_paciente'],
                                dados_extraidos['nome_medico'],
                                dados_extraidos['crm_medico'],
                                dados_extraidos['cid'],
                                f"{dados_extraidos['dias_atestado']} dias",
                                dados_extraidos['data_atendimento'],
                                "✅ Válido"
                            ]
                        }
                        
                        df_resumo = pd.DataFrame(resumo_data)
                        st.dataframe(df_resumo, use_container_width=True, hide_index=True)
                        
                        # Mostra JSON completo em expansível
                        with st.expander("🔍 Ver dados técnicos completos (JSON)"):
                            st.json(dados_extraidos)
                        
                        # Salva no banco se possível
                        try:
                            registrar_login(f"Validação: {arquivo.name} - {st.session_state['nome_completo']}")
                            st.success("💾 Validação registrada no banco de dados")
                        except Exception as e:
                            st.warning("⚠️ Não foi possível salvar no banco (normal em primeira execução)")
                        
                        else:
                            # Caso não consiga extrair informações
                            st.error("❌ **Não foi possível extrair informações do atestado**")
                            st.warning("**Possíveis causas:**")
                            st.info("• Qualidade da imagem muito baixa")
                            st.info("• Texto ilegível ou manuscrito")
                            st.info("• Formato de atestado não reconhecido")
                            st.info("• Problema temporário na API de IA")
                            
                            with st.expander("🔧 Dicas para melhorar o processamento"):
                                st.markdown("""
                                - **Use imagens nítidas e bem iluminadas**
                                - **Certifique-se de que todo o texto está visível**
                                - **Evite fotos com sombras ou reflexos**
                                - **Prefira PDFs ou arquivos escaneados de alta qualidade**
                                - **Verifique se todas as informações médicas estão legíveis**
                                """)
                            
                    except Exception as e:
                        st.error(f"🔴 **Erro no processamento:** {str(e)}")
                        st.warning("**Detalhes do erro:**")
                        st.code(str(e))
                        
                        with st.expander("📋 Informações para suporte"):
                            st.info(f"**Arquivo:** {arquivo.name}")
                            st.info(f"**Tamanho:** {arquivo.size} bytes")
                            st.info(f"**Tipo:** {arquivo.type}")
                            st.info(f"**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
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
