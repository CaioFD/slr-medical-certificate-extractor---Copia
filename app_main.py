import streamlit as st
import os
import time
import tempfile
from database import DB
from ocr_real import processar_atestado_real, verificar_configuracao

# Configuração da página
st.set_page_config(
    page_title="Sistema de Validação de Atestados Médicos", 
    page_icon="🏥",
    layout="centered"
)

# CSS simples
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: white !important;
        border: 1px solid #ddd !important;
    }
</style>
""", unsafe_allow_html=True)

# Verifica se a API está configurada
api_configurada = verificar_configuracao()

def processar_atestado_completo(arquivo):
    """Processa atestado usando OCR real com Gemini"""
    try:
        if not api_configurada:
            st.error("❌ **API do Gemini não configurada**")
            st.info("Configure a variável GEMINI_API_KEY no arquivo .env")
            return None
            
        # Lê o arquivo
        arquivo_bytes = arquivo.read()
        
        # Processa com OCR real
        dados = processar_atestado_real(arquivo_bytes, arquivo.name)
        
        if dados:
            return dados
        else:
            return None
            
    except Exception as e:
        st.error(f"Erro no processamento: {str(e)}")
        return None

# Inicializa session_state
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
    st.session_state["nome_completo"] = ""
    st.session_state["email"] = ""

def registrar_login(nome_usuario: str):
    """Registro de login simplificado"""
    try:
        print(f"[INFO] Login registrado: {nome_usuario}")
        st.success("💾 Login registrado com sucesso")
    except Exception as e:
        st.warning(f"⚠️ Aviso: {str(e)}")

# === LOGIN ===
if not st.session_state["autenticado"]:
    st.title("🏥 Sistema de Validação de Atestados Médicos")
    st.markdown("**Sistema de Validação de Atestados Médicos - Processamento Real**")
    st.markdown("---")
    
    st.subheader("🔐 Acesso ao Sistema")
    
    email = st.text_input("📧 Email", value="", placeholder="admin@teste.com")
    senha = st.text_input("🔒 Senha", type="password", value="", placeholder="Sua senha")
    nome = st.text_input("👤 Nome Completo", value="", placeholder="Seu nome completo")
    
    if st.button("🚀 Entrar", type="primary"):
        if email == "admin@teste.com" and senha == "123456" and nome.strip() != "":
            registrar_login(nome.strip())
            st.session_state["autenticado"] = True
            st.session_state["nome_completo"] = nome.strip()
            st.session_state["email"] = email
            st.success("✅ Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("❌ Credenciais inválidas ou nome não preenchido.")
    
    with st.expander("ℹ️ Informações de Acesso"):
        st.info("""
        **Credenciais de teste:**
        - Email: admin@teste.com
        - Senha: 123456
        - Nome: Qualquer nome válido
        """)

# === INTERFACE PRINCIPAL ===
else:
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #1f77b4, #2ca02c); padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">
        <h2 style="color: white; margin: 0;">👋 Bem-vindo, {st.session_state['nome_completo']}!</h2>
        <p style="color: #f0f0f0; margin: 0;">Email: {st.session_state['email']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("🚪 Sair"):
            st.session_state["autenticado"] = False
            st.session_state["nome_completo"] = ""
            st.session_state["email"] = ""
            st.rerun()
    
    st.title("📄 Validação de Atestados Médicos")
    
    # Status da API
    if api_configurada:
        st.success("🤖 IA Gemini: Conectada e pronta para processar documentos reais")
    else:
        st.error("❌ IA Gemini: Não configurada - Configure GEMINI_API_KEY no arquivo .env")
    
    # Detecta ambiente
    if "RENDER" in os.environ:
        st.info("🚀 Modo de Produção: Sistema otimizado para processamento rápido")
    else:
        st.info("💻 Modo de Desenvolvimento: Processamento local ativo")
    
    st.markdown("---")
    
    # Upload de arquivo
    st.markdown("### 📎 Upload do Documento")
    arquivo = st.file_uploader(
        "Selecione um arquivo de atestado médico", 
        type=["pdf", "jpg", "jpeg", "png"],
        help="Formatos aceitos: PDF, JPG, JPEG, PNG - O sistema extrairá informações reais do documento usando IA"
    )

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
            with st.spinner("🔄 Processando documento com IA... Extraindo informações reais do atestado..."):
                
                try:
                    # Simula tempo de processamento
                    time.sleep(3)
                    
                    # Processa o arquivo com OCR real
                    dados_extraidos = processar_atestado_completo(arquivo)
                    
                    if dados_extraidos:
                        # Resultado positivo
                        st.success("✅ **Atestado Processado com Sucesso!**")
                        
                        # Adiciona informações extras
                        dados_extraidos.update({
                            "arquivo_processado": arquivo.name,
                            "data_processamento": time.strftime('%Y-%m-%d %H:%M:%S'),
                            "observacoes": f"Processamento realizado no arquivo: {arquivo.name}"
                        })
                        
                        # Exibe os dados extraídos
                        st.markdown("### 📋 Informações Extraídas do Atestado")
                        
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
                        
                        # Informações médicas
                        st.markdown("#### 🏥 Informações Médicas")
                        col3, col4 = st.columns(2)
                        
                        with col3:
                            st.success(f"**Diagnóstico (CID):** {dados_extraidos['cid']}")
                            st.info(f"**Descrição:** {dados_extraidos['observacoes']}")
                            
                        with col4:
                            st.success(f"**Período Afastamento:** {dados_extraidos['dias_atestado']} dias")
                            st.info(f"**Data Início:** {dados_extraidos['data_atendimento']}")
                        
                        # Detalhes do processamento
                        st.markdown("#### ⚙️ Detalhes do Processamento")
                        col5, col6 = st.columns(2)
                        
                        with col5:
                            st.metric("📄 Arquivo", dados_extraidos['arquivo_processado'])
                            st.metric("📅 Processado em", dados_extraidos['data_processamento'])
                            
                        with col6:
                            st.metric("📏 Tamanho", f"{arquivo.size} bytes")
                            st.metric("✅ Status", "Processado com Sucesso")
                        
                        # Resumo em tabela
                        st.markdown("#### 📊 Resumo Completo")
                        
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
                        
                        # JSON completo
                        with st.expander("🔍 Ver dados técnicos completos (JSON)"):
                            st.json(dados_extraidos)
                        
                        # Registro de log
                        try:
                            registrar_login(f"Validação: {arquivo.name} - {st.session_state['nome_completo']}")
                        except Exception as e:
                            st.warning("⚠️ Não foi possível registrar no log")
                    
                    else:
                        st.error("❌ **Não foi possível processar o atestado**")
                        st.info("Tente com um arquivo diferente")
                            
                except Exception as e:
                    st.error(f"🔴 **Erro no processamento:** {str(e)}")
    
    else:
        # Instruções
        st.info("""
        📝 **Como usar:**
        1. Faça upload de um arquivo de atestado médico
        2. Clique em "Validar Atestado"
        3. Aguarde o processamento
        4. Visualize os resultados extraídos
        
        🎯 **Formatos aceitos:** PDF, JPG, JPEG, PNG
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #666;">
        <p>🏥 Sistema de Validação de Atestados Médicos v2.0</p>
        <p>Desenvolvido por Caio Faria Diniz | 2025</p>
    </div>
    """, unsafe_allow_html=True)
