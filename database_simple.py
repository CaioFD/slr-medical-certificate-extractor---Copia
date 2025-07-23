# === ARQUIVO: database_simple.py ===
# Versão simplificada do database para funcionar sem PostgreSQL

import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class DB:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.logs = []  # Lista em memória para simular banco

    def conect(self):
        """Simulação de conexão que sempre funciona"""
        try:
            # Tenta conectar com PostgreSQL se disponível
            try:
                import psycopg2
                
                # Tenta variáveis de ambiente
                host = os.getenv("PSQL_HOST", "localhost")
                port = os.getenv("PSQL_PORT", "5432")
                db = os.getenv("PSQL_DB", "atestados_db")
                user = os.getenv("PSQL_USER", "postgres")
                password = os.getenv("PSQL_PASS", "admin")
                
                self.conn = psycopg2.connect(
                    dbname=db,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                )
                self.cur = self.conn.cursor()
                print("✅ Conexão com PostgreSQL estabelecida!")
                return
                
            except Exception as e:
                print(f"[INFO] PostgreSQL não disponível ({e}), usando armazenamento em memória")
                self.conn = "memory"  # Indica modo memória
                print("✅ Sistema funcionando em modo local (sem banco)")
                
        except Exception as e:
            print(f"[AVISO] Erro na conexão: {e}")
            self.conn = "memory"

    def deconect(self):
        """Desconecta do banco"""
        try:
            if self.cur and self.conn != "memory":
                self.cur.close()
            if self.conn and self.conn != "memory":
                self.conn.close()
            print("[INFO] Conexão encerrada.")
        except Exception as e:
            print(f"[ERRO] Erro ao fechar conexão: {e}")

    def insert_login(self, nome_usuario: str):
        """Registra login"""
        try:
            agora = datetime.now()
            
            if self.conn == "memory":
                # Armazena em memória
                self.logs.append({
                    "usuario": nome_usuario,
                    "timestamp": agora,
                    "tipo": "login"
                })
                print(f"[INFO] Login registrado em memória: {nome_usuario}")
            else:
                # Tenta inserir no banco real
                self.cur.execute("""
                    INSERT INTO logins (nome_usuario, data_hora_login)
                    VALUES (%s, %s)
                """, (nome_usuario, agora))
                self.conn.commit()
                print(f"[INFO] Login registrado no banco: {nome_usuario}")
                
        except Exception as e:
            print(f"[ERRO] Falha ao registrar login: {e}")

    def get_logins(self, nome_usuario: str = None):
        """Busca logins"""
        try:
            if self.conn == "memory":
                # Retorna logs em memória
                if nome_usuario:
                    return [log for log in self.logs if nome_usuario.lower() in log["usuario"].lower()]
                return self.logs
            else:
                # Busca no banco real
                query = "SELECT * FROM logins WHERE TRUE"
                params = []
                if nome_usuario:
                    query += " AND nome_usuario ILIKE %s"
                    params.append(f"%{nome_usuario}%")
                
                self.cur.execute(query, tuple(params))
                return self.cur.fetchall()
                
        except Exception as e:
            print(f"[ERRO] Falha ao buscar logins: {e}")
            return []
