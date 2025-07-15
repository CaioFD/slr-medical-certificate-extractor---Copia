from database import DB
from models import User

def autenticar_usuario(user: User) -> bool:
    # Autenticação simples: email e senha fixos (como no seu exemplo)
    EMAIL_FIXO = "admin@teste.com"
    SENHA_FIXA = "123456"

    if user.email == EMAIL_FIXO and user.senha == SENHA_FIXA:
        registrar_login(user.email)  # registra login com o email (ou nome, se preferir)
        return True
    else:
        return False

def registrar_login(nome_usuario: str):
    db = DB()
    db.conect()
    try:
        db.insert_login(nome_usuario)
    except Exception as e:
        print(f"[ERRO] Registro de login: {e}")
    finally:
        db.deconect()
