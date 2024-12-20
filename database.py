import sqlite3
import uuid
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('mrkeep.db')
        self.cursor = self.conn.cursor()
        self.criar_tabela()
    
    def criar_tabela(self):
        self.cursor.execute('''
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
        self.conn.commit()
    
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
        
        self.cursor.execute('''
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
        
        self.conn.commit()
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
        
        query = f"UPDATE notas SET {', '.join(campos)} WHERE id = ?"
        self.cursor.execute(query, valores)
        self.conn.commit()
    
    def excluir_nota(self, id):
        self.cursor.execute("DELETE FROM notas WHERE id = ?", (id,))
        self.conn.commit()
    
    def obter_nota(self, id):
        self.cursor.execute("SELECT * FROM notas WHERE id = ?", (id,))
        return self.cursor.fetchone()
    
    def listar_notas(self, arquivadas=False, lixeira=False):
        query = """
            SELECT * FROM notas 
            WHERE arquivada = ? AND lixeira = ?
            ORDER BY fixada DESC, dataUltimaModificacao DESC, horaUltimaModificacao DESC
        """
        self.cursor.execute(query, (1 if arquivadas else 0, 1 if lixeira else 0))
        return self.cursor.fetchall()
    
    def __del__(self):
        self.conn.close() 