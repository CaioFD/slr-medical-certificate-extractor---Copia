import os
import requests
import re
from dotenv import load_dotenv
# import logging

load_dotenv()

# logging.basicConfig(level=logging.INFO)

def validate_crm(crm_input):
    """
    Valida CRM no formato 'UF-CRM', por exemplo 'SP-123456'.
    Consulta API externa e retorna True se válido, False caso contrário.
    """

    # Validar formato básico e separar
    pattern = r"^([A-Z]{2})-(\d+)$"
    match = re.match(pattern, crm_input.strip().upper())
    if not match:
        print("❌ Formato de CRM inválido. Use 'UF-CRM' (ex: SP-123456).")
        # logging.warning("Formato inválido: %s", crm_input)
        return False

    uf, crm_number = match.groups()

    # Verificar se UF está na lista oficial (exemplo simplificado)
    valid_ufs = {
        "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS",
        "MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"
    }
    if uf not in valid_ufs:
        print(f"❌ Unidade Federativa (UF) inválida: {uf}")
        # logging.warning("UF inválida: %s", uf)
        return False

    api_key = os.getenv("CFM_API_KEY")
    if not api_key:
        print("❌ Chave da API não encontrada. Configure a variável CFM_API_KEY.")
        # logging.error("Chave da API não encontrada no ambiente")
        return False

    url = "https://www.consultacrm.com.br/api/index.php"
    params = {
        "tipo": "crm",
        "uf": uf,
        "q": crm_number,
        "chave": api_key,
        "destino": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "true":
            nome = data.get("item", [{}])[0].get("nome", "Nome não disponível")
            print(f"✅ CRM {crm_input} válido: {nome}")
            # logging.info("CRM válido: %s - %s", crm_input, nome)
            return True
        else:
            print(f"❌ CRM {crm_input} inválido ou não encontrado.")
            # logging.info("CRM inválido ou não encontrado: %s", crm_input)
            return False

    except requests.exceptions.Timeout:
        print(f"⚠️ Timeout na consulta do CRM {crm_input}. Tente novamente mais tarde.")
        # logging.warning("Timeout na consulta do CRM %s", crm_input)
        return False
    except requests.exceptions.ConnectionError:
        print(f"⚠️ Erro de conexão na consulta do CRM {crm_input}. Verifique sua internet.")
        # logging.warning("Erro de conexão na consulta do CRM %s", crm_input)
        return False
    except requests.exceptions.HTTPError as http_err:
        print(f"⚠️ Erro HTTP ao consultar CRM {crm_input}: {http_err}")
        # logging.error("Erro HTTP %s na consulta do CRM %s", http_err, crm_input)
        return False
    except ValueError:
        print(f"⚠️ Resposta da API do CRM {crm_input} não está no formato JSON esperado.")
        # logging.error("JSON inválido na resposta da API para %s", crm_input)
        return False
    except Exception as e:
        print(f"⚠️ Erro inesperado ao consultar CRM {crm_input}: {e}")
        # logging.error("Erro inesperado %s ao consultar CRM %s", e, crm_input)
        return False
