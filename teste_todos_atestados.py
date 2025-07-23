#!/usr/bin/env python3
# Teste todos os atestados para verificar melhorias

from ocr_real_simple import processar_atestado_real
import os

def testar_atestado(arquivo):
    """Testa um atestado específico"""
    print(f"\n=== TESTANDO {arquivo.upper()} ===")
    
    image_path = f'data/{arquivo}'
    
    if not os.path.exists(image_path):
        print(f"❌ {arquivo} não encontrado!")
        return
    
    try:
        with open(image_path, 'rb') as f:
            arquivo_bytes = f.read()
        
        resultado = processar_atestado_real(arquivo_bytes, arquivo)
        
        if resultado:
            print(f"👤 Paciente: {resultado.get('nome_paciente', 'N/A')}")
            print(f"👨‍⚕️ Médico: {resultado.get('nome_medico', 'N/A')}")
            print(f"🏥 CRM: {resultado.get('crm_medico', 'N/A')}")
            print(f"📅 Data: {resultado.get('data_atendimento', 'N/A')}")
            print(f"⏰ Dias: {resultado.get('dias_atestado', 'N/A')}")
            print(f"🏷️ CID: {resultado.get('cid', 'N/A')}")
        else:
            print("❌ Erro no processamento!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

def main():
    print("=== TESTE GERAL - TODOS OS ATESTADOS ===")
    
    atestados = [
        'atestado4.jpeg',
        'Atestado5.png',
        'atestado3.jpg',
        'atestado2.jpeg'
    ]
    
    for atestado in atestados:
        testar_atestado(atestado)
    
    print("\n=== TESTE COMPLETO ===")

if __name__ == "__main__":
    main()
