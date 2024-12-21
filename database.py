import sqlite3
import uuid
from datetime import datetime

class Database:
    def __init__(self):
        self.db_path = 'mrkeep.db'
        # Cria a tabela na inicialização
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notas (
                    id TEXT PRIMARY KEY,
                    titulo TEXT,
                    conteudo TEXT,
                    dataCriacao TEXT,
                    horaCriacao TEXT,
                    dataUltimaModificacao TEXT,
                    horaUltimaModificacao TEXT,
                    fixada INTEGER,
                    corFundo TEXT,
                    arquivada INTEGER,
                    lixeira INTEGER
                )
            ''')
            conn.commit()
    
    def criar_nota(self, titulo="", conteudo="", cor_fundo="#202124"):
        agora = datetime.now()
        data_atual = agora.strftime('%Y-%m-%d')
        hora_atual = agora.strftime('%H:%M')
        
        nota = {
            'id': str(uuid.uuid4()),
            'titulo': titulo,
            'conteudo': conteudo,
            'dataCriacao': data_atual,
            'horaCriacao': hora_atual,
            'dataUltimaModificacao': data_atual,
            'horaUltimaModificacao': hora_atual,
            'fixada': 0,
            'corFundo': cor_fundo,
            'arquivada': 0,
            'lixeira': 0
        }
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO notas (
                    id, titulo, conteudo, dataCriacao, horaCriacao,
                    dataUltimaModificacao, horaUltimaModificacao,
                    fixada, corFundo, arquivada, lixeira
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                nota['id'], nota['titulo'], nota['conteudo'],
                nota['dataCriacao'], nota['horaCriacao'],
                nota['dataUltimaModificacao'], nota['horaUltimaModificacao'],
                nota['fixada'], nota['corFundo'],
                nota['arquivada'], nota['lixeira']
            ))
            conn.commit()
        
        return nota
    
    def atualizar_nota(self, id, **kwargs):
        agora = datetime.now()
        kwargs['dataUltimaModificacao'] = agora.strftime('%Y-%m-%d')
        kwargs['horaUltimaModificacao'] = agora.strftime('%H:%M')
        
        # Constrói a query de atualização dinamicamente
        campos = []
        valores = []
        for key, value in kwargs.items():
            campos.append(f"{key} = ?")
            valores.append(value)
        
        valores.append(id)  # Adiciona o ID para a cláusula WHERE
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = f"UPDATE notas SET {', '.join(campos)} WHERE id = ?"
            cursor.execute(query, valores)
            conn.commit()
    
    def excluir_nota(self, id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notas WHERE id = ?", (id,))
            conn.commit()
    
    def obter_nota(self, id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notas WHERE id = ?", (id,))
            return cursor.fetchone()
    
    def listar_notas(self, arquivadas=False, lixeira=False):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = """
                SELECT * FROM notas 
                WHERE arquivada = ? AND lixeira = ?
                ORDER BY fixada DESC, dataUltimaModificacao DESC, horaUltimaModificacao DESC
            """
            cursor.execute(query, (1 if arquivadas else 0, 1 if lixeira else 0))
            return cursor.fetchall() 