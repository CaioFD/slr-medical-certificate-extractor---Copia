import pandas as pd
import os

def _carregar_dataset(path="data/CID-10.CSV"):
    """
    Carrega e limpa o dataset com os dados CID-10.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    # Detecta o separador automaticamente
    try:
        df = pd.read_csv(path, sep=";", encoding="latin1")
    except Exception:
        df = pd.read_csv(path, encoding="utf-8")

    # Normaliza o CID
    df["CODIGO"] = df["CODIGO"].astype(str).str.replace(r"\W", "", regex=True).str.upper()

    return df
# _carregar_dataset

def _limpar_cid(codigo_cid: str) -> str:
    """
    Limpa e padroniza o código CID.
    """
    return codigo_cid.replace(".", "").strip().upper()
# _limpar_cid

def _obter_media_afastamento(df: pd.DataFrame, cid_limpo: str) -> float:
    """
    Retorna a média dos dias de afastamento para um CID específico.
    """
    if "MEDIA_DIAS_AFASTAMENTO" not in df.columns:
        raise KeyError("Coluna 'MEDIA_DIAS_AFASTAMENTO' não encontrada no dataset.")

    filtro = df["CODIGO"] == cid_limpo
    return df.loc[filtro, "MEDIA_DIAS_AFASTAMENTO"].mean()
# _obter_media_afastamento

def validate_cid(cid: str, dias_atestados: int, tolerancia: float = 0.4, path_csv="data/CID-10.csv") -> bool:
    """
    Valida se o CID está presente no dataset e retorna a média dos dias de afastamento.
    """
    valido = False
    try:
        df = _carregar_dataset(path_csv)
        cid_limpo = _limpar_cid(cid)

        if cid_limpo in df["CODIGO"].values:
            media = _obter_media_afastamento(df, cid_limpo)
            margem = media * tolerancia
            limite_inferior = media - margem
            limite_superior = media + margem

            print(f"CID {cid} encontrado — média de afastamento: {media:.0f} dias.")
            print(f"Tolerância considerada: ±{tolerancia*100:.0f}% -> intervalo: {limite_inferior:.1f} a {limite_superior:.1f} dias")

            if limite_inferior <= dias_atestados <= limite_superior:
                print(f"Dias atestados ({dias_atestados}) estão dentro da média com tolerância.")
                valido = True
            elif dias_atestados > limite_superior:
                print(f"Dias atestados ({dias_atestados}) excedem a média esperada.")
            else:
                print(f"Dias atestados ({dias_atestados}) estão abaixo do esperado.")
        else:
            print(f"CID {cid} não encontrado no dataset.")
    except FileNotFoundError as e:
        print(f"Erro: {e}")
    except KeyError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
    return valido
# validate_cid

def teste_validacao_cid():
    """
    Função de teste para validar o funcionamento do módulo.
    """
    cid = "A00"
    dias_atestados = 10
    assert validate_cid(cid, dias_atestados) == True, "Teste falhou para CID A00"

    cid_errado = "Z1000"
    dias_atestados_errados = 5
    assert validate_cid(cid_errado, dias_atestados_errados) == False, "Teste falhou para CID Z1000"
    print("Todos os testes passaram com sucesso!")


