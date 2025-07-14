import pandas as pd

# Nomes dos arquivos
arquivo_licencas = 'data/sample_60k_motivos_licenca_medica_cid.csv'
arquivo_cid_mestre = 'data/CID-10.csv' 

try:
    # Calcular as médias a partir do arquivo de licenças 
    print(f"Lendo o arquivo de licenças: '{arquivo_licencas}'...")
    df_licencas = pd.read_csv(arquivo_licencas, sep=',') # Separador é vírgula 

    # Converte datas, remove erros e calcula dias de afastamento
    df_licencas['data_inicio'] = pd.to_datetime(df_licencas['data_inicio'], errors='coerce')
    df_licencas['data_fim'] = pd.to_datetime(df_licencas['data_fim'], errors='coerce')
    df_licencas.dropna(subset=['data_inicio', 'data_fim'], inplace=True)
    df_licencas = df_licencas[df_licencas['data_fim'] >= df_licencas['data_inicio']]
    df_licencas['dias_afastamento'] = (df_licencas['data_fim'] - df_licencas['data_inicio']).dt.days + 1

    # Agrupa e calcula a média
    media_por_cid = df_licencas.groupby('cid')['dias_afastamento'].mean().round(2).reset_index()
    media_por_cid.rename(columns={'dias_afastamento': 'MEDIA_DIAS_AFASTAMENTO'}, inplace=True)
    
    # Padronização crucial da chave de junção
    # Converte a coluna 'cid' para texto e remove espaços extras
    media_por_cid['cid'] = media_por_cid['cid'].astype(str).str.strip()
    
    print("Médias calculadas. Amostra:")
    print(media_por_cid.head())
    print("-" * 40)

    # Carregar o arquivo mestre CID-10.csv 
    print(f"Lendo o arquivo mestre: '{arquivo_cid_mestre}'...")
    df_cid_mestre = pd.read_csv(
        arquivo_cid_mestre,
        sep=';',              # Especifica o separador ponto e vírgula 
        encoding='latin-1'    # Especifica a codificação para ler acentos corretamente 
    )

    # Padronização crucial da chave de junção (mestre) 
    # Converte a coluna 'CODIGO' para texto e remove espaços extras
    df_cid_mestre['CODIGO'] = df_cid_mestre['CODIGO'].astype(str).str.strip()

    print(f"Arquivo mestre carregado com sucesso. {len(df_cid_mestre)} linhas encontradas.")
    print("Colunas do arquivo mestre:", df_cid_mestre.columns.tolist())
    print("-" * 40)
    
    # Renomeia a coluna no DataFrame de médias para corresponder à do mestre
    media_por_cid.rename(columns={'cid': 'CODIGO'}, inplace=True)

    # ETAPA 3: Unir os dados e salvar 

    # Remove a coluna de média antiga, se existir, para evitar duplicatas
    if 'MEDIA_DIAS_AFASTAMENTO' in df_cid_mestre.columns:
        df_cid_mestre = df_cid_mestre.drop('MEDIA_DIAS_AFASTAMENTO', axis=1)
        print("Coluna de média antiga removida para atualização.")

    df_cid_mestre = df_cid_mestre.drop('DIAS DE AFASTAMENTO', axis=1)
    # Une os dois DataFrames. 'how=left' mantém todas as linhas do seu CID-10.csv original.
    df_final = pd.merge(df_cid_mestre, media_por_cid, on='CODIGO', how='left')

    print(f"Junção completa. O arquivo final terá {len(df_final)} linhas.")
    
    # Salva o arquivo final, sobrescrevendo o antigo com os dados atualizados
    # Mantém o formato original (separador ';' e codificação 'latin-1')
    df_final.to_csv(arquivo_cid_mestre, sep=';', index=False, encoding='latin-1')

    print(f"\nSUCESSO! O arquivo '{arquivo_cid_mestre}' foi atualizado.")
    print("Amostra do resultado final:")
    print(df_final.head())

except FileNotFoundError as e:
    print(f"ERRO: Arquivo não encontrado -> {e.filename}")
    print("Por favor, certifique-se de que ambos os arquivos CSV estão na mesma pasta que o script.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")

