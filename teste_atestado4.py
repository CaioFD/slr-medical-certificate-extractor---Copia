#!/usr/bin/env python3
# Teste específico para atestado4

from ocr_real_simple import processar_atestado_real
import os

def main():
    print("=== TESTE ESPECÍFICO ATESTADO4 ===")
    
    # Carregar atestado4
    image_path = 'data/atestado4.jpeg'
    
    if not os.path.exists(image_path):
        print("❌ Arquivo não encontrado!")
        return
    
    print("✅ Arquivo encontrado, carregando...")
    
    try:
        with open(image_path, 'rb') as f:
            arquivo_bytes = f.read()
        
        print("📊 Processando com OCR...")
        resultado = processar_atestado_real(arquivo_bytes, 'atestado4.jpeg')
        
        if resultado:
            print("\n=== RESULTADO ===")
            print(f"Nome Paciente: {resultado.get('nome_paciente', 'N/A')}")
            print(f"Nome Médico: {resultado.get('nome_medico', 'N/A')}")
            print(f"CRM: {resultado.get('crm_medico', 'N/A')}")
            print(f"Data: {resultado.get('data_atendimento', 'N/A')}")
            print(f"Dias: {resultado.get('dias_atestado', 'N/A')}")
            print(f"CID: {resultado.get('cid', 'N/A')}")
            
            print(f"\n=== ANÁLISE ===")
            paciente = resultado.get('nome_paciente', '')
            medico = resultado.get('nome_medico', '')
            
            if 'Everton' in paciente or 'Alves' in paciente:
                print("✅ Nome do paciente correto!")
            else:
                print(f"❌ Nome do paciente incorreto. Deveria ser 'Everton Alves', mas foi identificado: '{paciente}'")
            
            if 'Everton' in medico or 'Alves' in medico:
                print("❌ Nome do paciente foi colocado como médico!")
            else:
                print("✅ Distinção entre paciente e médico OK")
                
        else:
            print("❌ Erro no processamento!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
