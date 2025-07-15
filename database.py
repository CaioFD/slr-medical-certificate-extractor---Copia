import os
import psycopg2
from dotenv import load_dotenv
from atestado import Atestado
from datetime import datetime

load_dotenv()

class DB:
    def __init__(self):
        self.conn = None
        self.cur = None

    def conect(self):
        try:
            # print("os.getenv('PSQL_DB')", os.getenv("PSQL_DB"))
            # print("os.getenv('PSQL_USER')", os.getenv("PSQL_USER"))
            # print("os.getenv('PSQL_PASS')", os.getenv("PSQL_PASS"))
            # print("os.getenv('PSQL_HOST')", os.getenv("PSQL_HOST"))
            self.conn = psycopg2.connect(
                dbname="atestados_db",
                user=os.getenv("PSQL_USER"),
                password=os.getenv("PSQL_PASS"),
                host=os.getenv("PSQL_HOST", "localhost"),
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f"[ERRO] Falha ao conectar: {e}")
    # def_connect(self):

    def deconect(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
    # def deconect(self):

    def insertAtestado(self, atestado: Atestado):
        try:
            self.cur.execute("""
                INSERT INTO atestados (
                    nome_funcionario, data_envio, crm_medico,
                    nome_medico, dias_afastado
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                atestado.nomePaciente,
                atestado.dataAtendimento,  
                atestado.crmMedico,
                atestado.nomeMedico,
                int(atestado.diasAtestado) if atestado.diasAtestado is not None else None
            ))
            self.conn.commit()
            print("[INFO] Atestado inserido com sucesso.")
        except Exception as e:
            print(f"[ERRO] Falha ao inserir: {e}")
    # def insertAtestado(self, atestado: Atestado):

    def updateAtestado(self, id: int, novo_dias: int):
        try:
            self.cur.execute("""
                UPDATE atestados
                SET dias_afastado = %s
                WHERE id = %s
            """, (novo_dias, id))
            self.conn.commit()
            print("[INFO] Atestado atualizado com sucesso.")
        except Exception as e:
            print(f"[ERRO] Falha ao atualizar: {e}")
    # def updateAtestado(self, id: int, novo_dias: int):

    def deleteAtestado(self, id: int):
        try:
            self.cur.execute("DELETE FROM atestados WHERE id = %s", (id,))
            self.conn.commit()
            print("[INFO] Atestado deletado com sucesso.")
        except Exception as e:
            print(f"[ERRO] Falha ao deletar: {e}")
    # def deleteAtestado(self, id: int):

    def deleteALL_Atestado(self):
        try:
            self.cur.execute("DELETE FROM atestados")
            self.conn.commit()
            print("[INFO] Todos os atestados foram deletados com sucesso.")
        except Exception as e:
            print(f"[ERRO] Falha ao deletar: {e}")
    # def deleteALL_Atestado(self):

    def getAtestados(self, atestado_id=None, nome_paciente=None, nome_medico=None, data_atestado=None):
        try:
            query = "SELECT * FROM atestados WHERE TRUE"
            params = []

            if atestado_id:
                query += " AND id = %s"
                params.append(atestado_id)
            if nome_paciente:
                query += " AND nome_funcionario ILIKE %s"
                params.append(f"%{nome_paciente}%")
            if nome_medico:
                query += " AND nome_medico ILIKE %s"
                params.append(f"%{nome_medico}%")
            if data_atestado:
                query += " AND data_envio = %s"
                params.append(data_atestado)

            self.cur.execute(query, tuple(params))
            resultados = self.cur.fetchall()

            if resultados:
                for row in resultados:
                    print(row)
            else:
                print("Nenhum atestado encontrado com os critérios fornecidos.")
        except Exception as e:
            print(f"[ERRO] Falha ao buscar atestados filtrados: {e}")
    # def getAtestados(self, atestado_id=None, nome_paciente=None, nome_medico=None, data_atestado=None):


    def insert_login(self, nome_usuario: str):
        print(f"[DEBUG] Tentando inserir login para: {nome_usuario}")
        try:
            agora = datetime.now()
            self.cur.execute("""
                INSERT INTO logins (nome_usuario, data_hora_login)
                VALUES (%s, %s)
            """, (nome_usuario, agora))
            self.conn.commit()
            print(f"[INFO] Login registrado para {nome_usuario} em {agora}.")
        except Exception as e:
            print(f"[ERRO] Falha ao registrar login: {e}")

    def get_logins(self, nome_usuario: str = None):
        try:
            query = "SELECT * FROM logins WHERE TRUE"
            params = []
            if nome_usuario:
                query += " AND nome_usuario ILIKE %s"
                params.append(f"%{nome_usuario}%")

            self.cur.execute(query, tuple(params))
            resultados = self.cur.fetchall()
            return resultados
        except Exception as e:
            print(f"[ERRO] Falha ao buscar logins: {e}")
            return []