import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
from atestado_validator import validate_atestado
from auth import autenticar_usuario
from models import User

app = FastAPI()

# Diretório temporário para arquivos
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# Serve os arquivos estáticos da pasta frontend
# app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/")
def home():
    """
    Endpoint de boas-vindas da API.
    """
    return {"mensagem": "API de Validação de Atestados"}


@app.get("/login/", response_class=HTMLResponse)
def login_page():
    with open("frontend/login.html", "r") as f:
        return f.read()


@app.get("/index.html", response_class=HTMLResponse)
def index_page():
    with open("frontend/index.html", "r") as f:
        return f.read()


@app.post("/login/")
async def login(email: str = Form(...), senha: str = Form(...)):
    """
    Endpoint para autenticação de usuários via formulário.
    """
    user = User(email=email, senha=senha)
    if autenticar_usuario(user):
        return {"login": True}
    return {"login": False}


@app.post("/validar_atestado/")
async def validar(file: UploadFile = File(...)):
    """
    Endpoint para validar um arquivo de atestado.
    Recebe um arquivo UploadFile e o processa usando a lógica de validação.
    """
    caminho_temp = os.path.join(TEMP_DIR, file.filename)

    try:
        with open(caminho_temp, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        resultado_validacao = validate_atestado(caminho_temp)

        if not resultado_validacao["valido"]:
            return JSONResponse(
                content=resultado_validacao,
                status_code=422
            )

        return JSONResponse(
            content=resultado_validacao,
            status_code=200
        )

    except Exception as e:
        print(f"Erro inesperado na API: {e}")
        return JSONResponse(
            content={"erro": f"Erro interno do servidor: {str(e)}"},
            status_code=500
        )

    finally:
        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)




# import os
# import shutil
# from fastapi.responses import JSONResponse
# from fastapi import FastAPI, UploadFile, File
# from atestado_validator import validate_atestado

# app = FastAPI()

# # Cria diretório temporário, se não existir
# TEMP_DIR = "temp"
# os.makedirs(TEMP_DIR, exist_ok=True)

# @app.get("/")
# def home():
#     return {"mensagem": "API de Validação de Atestados"}

# @app.post("/validar_atestado/")
# async def validar(file: UploadFile = File(...)):
#     caminho_temp = os.path.join(TEMP_DIR, file.filename)
#     try:
#         with open(caminho_temp, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)

#         resultado = validate_atestado(caminho_temp)

#         return JSONResponse(content={"valido": resultado}, status_code=200)
#     except Exception as e:
#         return JSONResponse(content={"erro": str(e)}, status_code=500)
#     finally:
#         if os.path.exists(caminho_temp):
#             os.remove(caminho_temp)

# if __name__ == "__main__":
#     arquivo_teste = "data/atestado5.png"  # Pode ser .jpeg, .jpg, .png, .pdf
#     validate_atestado(arquivo_teste)