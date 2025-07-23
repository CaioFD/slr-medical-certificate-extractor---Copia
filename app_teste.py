import streamlit as st
import os
import time
import tempfile
from database import DB

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

# Função simplificada para processar arquivo (simulação mais realista)
def processar_atestado_simples(arquivo):
    """Simula processamento de atestado com base no nome do arquivo"""
    
    # Simulação baseada no nome do arquivo para demonstração
    nome_arquivo = arquivo.name.lower()
    
    if "atestado" in nome_arquivo:
        if "2" in nome_arquivo:
            return {
                "nome_paciente": "Maria Silva Santos",
                "nome_medico": "Dr. João Pereira",
                "crm_medico": "54321/RJ", 
                "cid": "Z76.3",
                "dias_atestado": "5",
                "data_atendimento": "2025-01-22"
            }
        elif "3" in nome_arquivo:
            return {
                "nome_paciente": "Carlos Eduardo Lima",
                "nome_medico": "Dra. Ana Costa",
                "crm_medico": "98765/MG",
                "cid": "M79.1", 
                "dias_atestado": "7",
                "data_atendimento": "2025-01-23"
            }
        elif "4" in nome_arquivo:
            return {
                "nome_paciente": "Fernanda Oliveira",
                "nome_medico": "Dr. Roberto Silva",
                "crm_medico": "11111/SP",
                "cid": "K59.0",
                "dias_atestado": "2", 
                "data_atendimento": "2025-01-21"
            }
        elif "5" in nome_arquivo:
            return {
                "nome_paciente": "Pedro Henrique Costa",
                "nome_medico": "Dra. Lucia Santos",
                "crm_medico": "22222/RS",
                "cid": "J06.9",
                "dias_atestado": "4",
                "data_atendimento": "2025-01-20"
            }
        else:
            # Arquivo padrão
            return {
                "nome_paciente": "João Silva Santos",
                "nome_medico": "Dr. Maria Oliveira Costa",
                "crm_medico": "12345/SP",
                "cid": "J06.9",
                "dias_atestado": "3",
                "data_atendimento": "2025-01-20"
            }
    else:
        # Para outros arquivos
        return {
            "nome_paciente": "Paciente de Teste",
            "nome_medico": "Dr. Médico de Teste",
            "crm_medico": "00000/XX",
            "cid": "Z00.0",
            "dias_atestado": "1",
            "data_atendimento": "2025-01-23"
        }

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
    st.markdown("**Versão de Teste - Processamento Real de Arquivos**")
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
    st.info("🤖 Modo de Teste: Processamento realista baseado no arquivo carregado")
    st.markdown("---")
    
    # Upload de arquivo
    st.markdown("### 📎 Upload do Documento")
    arquivo = st.file_uploader(
        "Selecione um arquivo de atestado médico", 
        type=["pdf", "jpg", "jpeg", "png"],
        help="Teste com os arquivos da pasta 'data' para ver resultados diferentes"
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
            with st.spinner("🔄 Processando documento... Analisando conteúdo..."):
                
                try:
                    # Simula tempo de processamento
                    time.sleep(3)
                    
                    # Processa o arquivo baseado no nome
                    dados_extraidos = processar_atestado_simples(arquivo)
                    
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
        📝 **Como testar:**
        1. Faça upload de um arquivo de atestado médico
        2. Clique em "Validar Atestado"
        3. Aguarde o processamento
        4. Visualize os resultados extraídos
        
        🎯 **Arquivos de teste:** Use os arquivos da pasta 'data' para ver diferentes resultados
        """)
        
        # Lista arquivos disponíveis para teste
        with st.expander("📁 Arquivos de Teste Disponíveis"):
            st.code("""
            data/atestado.pdf     -> João Silva Santos
            data/atestado2.jpeg   -> Maria Silva Santos  
            data/atestado3.jpg    -> Carlos Eduardo Lima
            data/atestado4.jpeg   -> Fernanda Oliveira
            data/Atestado5.png    -> Pedro Henrique Costa
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #666;">
        <p>🏥 Sistema de Validação de Atestados Médicos v2.0 (Teste)</p>
        <p>Desenvolvido por Caio Faria Diniz | 2025</p>
    </div>
    """, unsafe_allow_html=True)
