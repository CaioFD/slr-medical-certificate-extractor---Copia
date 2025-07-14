import os
import re
import cv2
from PIL import Image
from atestado import Atestado
import google.generativeai as genai
from pdf2image import convert_from_path
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

def extrair_informacoes_arquivo(arquivo):
    try:
        if _verificar_extensao(arquivo):
            imgs = _transformar_em_imagem(arquivo)
            if imgs:
                for img in imgs:
                    texto_extraido = _extrair_info_relevante(img)
                    if texto_extraido:
                        dict_informacoes = texto_para_dict(texto_extraido)
                        if dict_informacoes:
                            # print("-" * 50)
                            # print(texto_extraido)
                            # print("-" * 50)
                            # print(dict_informacoes)
                            # print("-" * 50)                            
                            return Atestado.from_dict(dict_informacoes)
                    else:
                        print(f"Nenhuma informação relevante encontrada no arquivo {arquivo}.")
            else:
                print(f"Não foi possível transformar o arquivo {arquivo} em imagem.")
        else:
            print(f"Extensão do arquivo {arquivo} não suportada. Use .pdf, .png, .jpeg ou .jpg.")
    except Exception as e:
        print(f"Erro ao processar o arquivo {arquivo}: {str(e)}")
# extrair_informacoes_arquivo

def _verificar_extensao(nome_arquivo):
    extensoes_validas = [".pdf", ".png", ".jpeg", ".jpg"]
    return any(nome_arquivo.lower().endswith(ext) for ext in extensoes_validas)
# _verificar_extensao

def _transformar_em_imagem(caminho_arquivo):
    if caminho_arquivo.lower().endswith(".pdf"):
        imagens = convert_from_path(caminho_arquivo)
        paths = []
        for i, img in enumerate(imagens):
            caminho = f"temp_pagina_{i}.jpg"
            img.save(caminho, "JPEG")
            paths.append(caminho)
        return paths
    return [caminho_arquivo]
# _transformar_em_imagem

def _extrair_info_relevante(img_path):
    imagem = cv2.imread(img_path)
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(imagem)

    prompt = """
Extraia as seguintes informações do atestado médico:
- Data do atendimento
- Primeiro e Segundo Nome do Paciente
- Nome Completo do Médico
- UF do Médico
- CRM do Médico
- CID da doença
- Quantos dias de atestado

Formato de resposta:
Data do Atendimento: <data>
Nome do Paciente: <nome>
Nome do Médico: <nome>
CRM do Médico: <uf>-<crm>
CID: <cid>
Dias de Atestado: <quantidade>
"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt, pil_image])
    return response.text or ""
# _extrair_info_relevante

# TODO: Corrigir problemas (todos)
def texto_para_dict(texto):
    info = {
        "data_atendimento": None,
        "nome_paciente": None,
        "nome_medico": None,
        "crm_medico": None,
        "cid": None,
        "dias_atestado": None
    }

    # Permitir acentos e caracteres unicode
    flags = re.UNICODE

    # Data do atendimento
    data_match = re.search(r"Data\s*do\s*Atendimento\s*:\s*(\d{2}/\d{2}/\d{4})", texto, flags)
    if data_match:
        info["data_atendimento"] = data_match.group(1).strip()

    # Nome do paciente: captura até próxima linha chave
    nome_paciente_match = re.search(r"Nome\s*do\s*Paciente\s*:\s*(.*?)\s*Nome\s*do\s*M[eé]dico", texto, flags | re.DOTALL)
    if nome_paciente_match:
        info["nome_paciente"] = nome_paciente_match.group(1).strip()

    # Nome do médico: captura até a linha do CRM
    nome_medico_match = re.search(r"Nome\s*do\s*M[eé]dico\s*:\s*(.*?)\s*CRM\s*do\s*M[eé]dico", texto, flags | re.DOTALL)
    if nome_medico_match:
        info["nome_medico"] = nome_medico_match.group(1).strip()

    # CRM
    crm_match = _extrair_crm(texto)
    if crm_match:
        info["crm_medico"] = f"{crm_match}"

    # CID
    cid_match = _extrair_cid(texto)
    if cid_match:
        info["cid"] = _corrigir_cid(cid_match)

    # Dias de Atestado
    dias_atestado = _extrair_dias_atestado(texto)
    if dias_atestado is not None:
        info["dias_atestado"] = dias_atestado

    return info
# texto_para_dict

def _extrair_crm(texto):
    padroes = [
        r"CRM\s*do\s*M[eé]dico\s*:\s*([A-Z]{2})\s*[-:]?\s*(\d{4,6})",  # DF-10158
        r"([A-Z]{2})\s*-\s*(\d{4,6})",
        r"CRM\s*:\s*([A-Z]{2})\s*-\s*(\d{4,6})"
    ]
    for padrao in padroes:
        match = re.search(padrao, texto)
        if match:
            uf = match.group(1).strip()
            crm = match.group(2).strip()
            return f"{uf}-{crm}"
    return None
# _extrair_crm

def _corrigir_cid(cid):
    if not cid:
        return cid
    cid = cid.upper().replace(".", "").strip()
    if cid and cid[0] == "0":
        cid = "J" + cid[1:]
    return cid
# _corrigir_cid

def _extrair_dias_atestado(texto):
    match = re.search(r"Dias\s+de\s+Atestado\s*\:\s*(\d+)", texto)
    return int(match.group(1)) if match else None
# _extrair_dias_atestado

def _extrair_cid(texto):
    match = re.search(r"CID\s*[\:\-]?\s*([A-Z0-9\.]+)", texto)
    return match.group(1).strip() if match else None
# _extrair_cid

