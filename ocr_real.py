import os
import re
import tempfile
import base64
from typing import Dict, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configuração da API Gemini
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def processar_atestado_real(arquivo_bytes: bytes, nome_arquivo: str) -> Optional[Dict]:
    """
    Processa um atestado médico usando Google Gemini Vision API
    
    Args:
        arquivo_bytes: Bytes do arquivo
        nome_arquivo: Nome do arquivo original
        
    Returns:
        Dicionário com informações extraídas ou None se falhar
    """
    
    try:
        # Verifica se a API está configurada
        if not api_key:
            print("[ERRO] API Key do Gemini não configurada")
            return None
            
        # Cria arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{nome_arquivo.split('.')[-1]}") as temp_file:
            temp_file.write(arquivo_bytes)
            temp_file_path = temp_file.name
        
        try:
            # Carrega a imagem para o Gemini
            from PIL import Image
            
            # Para PDFs, precisamos converter para imagem primeiro
            if nome_arquivo.lower().endswith('.pdf'):
                # Tenta usar pdf2image se disponível, senão retorna erro
                try:
                    from pdf2image import convert_from_path
                    images = convert_from_path(temp_file_path)
                    if images:
                        # Usa a primeira página
                        image = images[0]
                    else:
                        print("[ERRO] Não foi possível converter PDF")
                        return None
                except ImportError:
                    print("[ERRO] pdf2image não está disponível. Use imagens JPG/PNG.")
                    return None
            else:
                # Carrega imagem diretamente
                image = Image.open(temp_file_path)
            
            # Prompt específico para atestados médicos brasileiros
            prompt = """
Você é um especialista em análise de documentos médicos brasileiros. Analise este atestado médico e extraia EXATAMENTE as seguintes informações:

1. Nome do paciente (nome completo da pessoa que recebeu o atestado)
2. Nome do médico (nome completo do médico que emitiu o atestado)
3. CRM do médico (número do CRM seguido da UF, ex: 12345/SP)
4. CID (código da doença, ex: J06.9, M79.1, etc.)
5. Data do atendimento (data em que foi realizada a consulta)
6. Dias de atestado (quantos dias de afastamento foram concedidos)

IMPORTANTE:
- Se alguma informação não estiver claramente visível, retorne "Não identificado"
- Para o CRM, procure pelo formato número/UF (exemplo: 123456/SP)
- Para CID, procure códigos com letra seguida de números (exemplo: J06.9)
- Para dias, procure por números seguidos de "dias" ou similar

Formato de resposta (responda EXATAMENTE neste formato):
Nome do Paciente: [nome encontrado]
Nome do Médico: [nome encontrado]
CRM: [número/UF encontrado]
CID: [código encontrado]
Data do Atendimento: [data encontrada]
Dias de Atestado: [número encontrado]
"""
            
            # Chama a API Gemini
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([prompt, image])
            
            if response.text:
                # Processa a resposta
                dados = extrair_dados_da_resposta(response.text)
                
                print(f"[INFO] Processamento concluído para {nome_arquivo}")
                print(f"[DEBUG] Resposta da IA: {response.text}")
                print(f"[DEBUG] Dados extraídos: {dados}")
                
                return dados
            else:
                print("[ERRO] Resposta vazia da API")
                return None
                
        finally:
            # Remove arquivo temporário
            try:
                os.unlink(temp_file_path)
            except:
                pass
                
    except Exception as e:
        print(f"[ERRO] Falha no processamento: {str(e)}")
        return None

def extrair_dados_da_resposta(texto_resposta: str) -> Dict:
    """
    Extrai os dados estruturados da resposta do Gemini
    """
    dados = {
        "nome_paciente": "Não identificado",
        "nome_medico": "Não identificado", 
        "crm_medico": "Não identificado",
        "cid": "Não identificado",
        "data_atendimento": "Não identificado",
        "dias_atestado": "Não identificado"
    }
    
    try:
        # Padrões de regex para extrair informações
        padroes = {
            "nome_paciente": r"Nome do Paciente:\s*(.+?)(?:\n|$)",
            "nome_medico": r"Nome do Médico:\s*(.+?)(?:\n|$)",
            "crm_medico": r"CRM:\s*(.+?)(?:\n|$)",
            "cid": r"CID:\s*(.+?)(?:\n|$)",
            "data_atendimento": r"Data do Atendimento:\s*(.+?)(?:\n|$)",
            "dias_atestado": r"Dias de Atestado:\s*(.+?)(?:\n|$)"
        }
        
        for campo, padrao in padroes.items():
            match = re.search(padrao, texto_resposta, re.IGNORECASE)
            if match:
                valor = match.group(1).strip()
                # Remove caracteres especiais e limpa o valor
                valor = re.sub(r'[\[\]"]', '', valor)
                if valor and valor.lower() not in ["não identificado", "não encontrado", "n/a", ""]:
                    dados[campo] = valor
        
        # Validações específicas
        
        # Para CRM, verifica se tem o formato correto
        if dados["crm_medico"] != "Não identificado":
            crm_match = re.search(r'(\d+[/\-]\w{2})', dados["crm_medico"])
            if crm_match:
                dados["crm_medico"] = crm_match.group(1)
        
        # Para CID, verifica se tem o formato correto
        if dados["cid"] != "Não identificado":
            cid_match = re.search(r'([A-Z]\d{2}\.?\d?)', dados["cid"])
            if cid_match:
                dados["cid"] = cid_match.group(1)
        
        # Para dias, extrai apenas o número
        if dados["dias_atestado"] != "Não identificado":
            dias_match = re.search(r'(\d+)', dados["dias_atestado"])
            if dias_match:
                dados["dias_atestado"] = dias_match.group(1)
                
        return dados
        
    except Exception as e:
        print(f"[ERRO] Falha ao extrair dados da resposta: {str(e)}")
        return dados

def verificar_configuracao() -> bool:
    """Verifica se a configuração está correta"""
    if not api_key:
        return False
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"[ERRO] Configuração inválida: {str(e)}")
        return False
