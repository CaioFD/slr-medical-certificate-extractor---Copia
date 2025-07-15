from database import DB
from crm_validator import validate_crm
from cid_validator import validate_cid
from extract_info import extrair_informacoes_arquivo

def validate_atestado(arquivo: str) -> dict:
    resposta = {
        "valido": False,
        "motivo": "Erro não identificado.",
        "dados_extraidos": None
    }
    
    db = DB()
    db.conect()

    try:
        atestado = extrair_informacoes_arquivo(arquivo)
        if not atestado:
            resposta["motivo"] = "Não foi possível extrair informações do arquivo. O formato pode ser inválido."
            # A função para aqui e retorna a resposta de erro
            return resposta

        # Validação do CRM
        crm_validado = validate_crm(atestado.crmMedico)
        if not crm_validado:
            resposta["motivo"] = "CRM do médico é inválido."
            return resposta
        
        # Validação do CID (opcional)
        if atestado.cid:
            validate_cid(atestado.cid, atestado.diasAtestado) 
        
        resposta["valido"] = True
        resposta["motivo"] = "Atestado validado com sucesso."
        resposta["dados_extraidos"] = atestado.to_dict() 
        # db.insertAtestado(atestado) 

    except Exception as e:
        # Se qualquer erro acontecer, nós o capturamos para a resposta
        resposta["motivo"] = f"Erro crítico durante a validação: {str(e)}"
    
    finally:
        db.deconect()

    return resposta


# from database import DB
# from crm_validator import validate_crm
# from cid_validator import validate_cid
# from extract_info import extrair_informacoes_arquivo

# def validate_atestado(arquivo):
#     valido = False
#     db = DB()
#     db.conect()
#     try:
#         atestado = extrair_informacoes_arquivo(arquivo)
#         if atestado:
#             crm_validado = validate_crm(atestado.crmMedico)

#             if not crm_validado:
#                 print("❌ Atestado inválido! CRM do médico não é válido.")
#             else:
#                 # Verificação de CID
#                 if not atestado.cid:
#                     print("⚠️ CID não encontrado no atestado.")
#                 else:
#                     # A função de validação do CID ainda é chamada, mas seu resultado
#                     # não precisa ser verificado se não vamos mais exibir a mensagem.
#                     validate_cid(atestado.cid, atestado.diasAtestado)

#                 # CRM válido = atestado aceito mesmo sem CID
#                 print("✅ Atestado válido!")
#                 # db.insertAtestado(atestado)
#                 print("-" * 50)
#                 print("Informações Extraídas do Atestado:")
#                 print(atestado)
#                 valido = True
#     except Exception as e:
#         print(f"⛔ Erro crítico: {str(e)}")
#     finally:
#         print("-" * 50)
#         print("Dentro do banco de dados: ")
#         db.getAtestados()
#         db.deconect()
        
#     return valido



