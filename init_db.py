#!/usr/bin/env python3
"""
Script para inicializar o banco de dados no Render
"""
import os
import sys
from database import DB

def init_database():
    """Inicializa o banco de dados criando as tabelas necessárias"""
    try:
        print("🔧 Inicializando banco de dados...")
        
        db = DB()
        db.conect()
        
        # SQL para criar tabela de atestados (ajuste conforme sua necessidade)
        create_atestados_table = """
        CREATE TABLE IF NOT EXISTS atestados (
            id SERIAL PRIMARY KEY,
            nome_paciente VARCHAR(255),
            nome_medico VARCHAR(255),
            crm VARCHAR(20),
            cid VARCHAR(10),
            data_atendimento DATE,
            dias_atestado INTEGER,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            valido BOOLEAN DEFAULT FALSE
        );
        """
        
        # SQL para criar tabela de logs de login
        create_logs_table = """
        CREATE TABLE IF NOT EXISTS login_logs (
            id SERIAL PRIMARY KEY,
            usuario VARCHAR(255),
            data_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        db.cur.execute(create_atestados_table)
        db.cur.execute(create_logs_table)
        db.conn.commit()
        
        print("✅ Banco de dados inicializado com sucesso!")
        print("✅ Tabelas criadas: atestados, login_logs")
        
        db.disconnect()
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()
