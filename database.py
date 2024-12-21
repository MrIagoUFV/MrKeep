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
                    lixeira INTEGER,
                    ordem REAL
                )
            ''')
            conn.commit()
    
    def criar_nota(self, titulo="", conteudo="", cor_fundo="#202124"):
        agora = datetime.now()
        data_atual = agora.strftime('%Y-%m-%d')
        hora_atual = agora.strftime('%H:%M')
        
        # Obtém a última ordem e adiciona 1000
        ultima_ordem = self.obter_ultima_ordem()
        nova_ordem = ultima_ordem + 1000
        
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
            'lixeira': 0,
            'ordem': nova_ordem
        }
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO notas (
                    id, titulo, conteudo, dataCriacao, horaCriacao,
                    dataUltimaModificacao, horaUltimaModificacao,
                    fixada, corFundo, arquivada, lixeira, ordem
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                nota['id'], nota['titulo'], nota['conteudo'],
                nota['dataCriacao'], nota['horaCriacao'],
                nota['dataUltimaModificacao'], nota['horaUltimaModificacao'],
                nota['fixada'], nota['corFundo'],
                nota['arquivada'], nota['lixeira'], nota['ordem']
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
            if lixeira:
                # Se estiver listando notas da lixeira, não importa se está arquivada ou não
                query = """
                    SELECT * FROM notas 
                    WHERE lixeira = 1
                    ORDER BY ordem ASC
                """
                cursor.execute(query)
            else:
                # Se não estiver listando notas da lixeira, filtra por arquivada e lixeira = 0
                query = """
                    SELECT * FROM notas 
                    WHERE arquivada = ? AND lixeira = 0
                    ORDER BY fixada DESC, ordem ASC
                """
                cursor.execute(query, (1 if arquivadas else 0,))
            return cursor.fetchall()
    
    def obter_ultima_ordem(self, arquivada=False, lixeira=False):
        """Obtém a última ordem das notas na seção especificada"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if lixeira:
                query = "SELECT MAX(ordem) FROM notas WHERE lixeira = 1"
                cursor.execute(query)
            else:
                query = "SELECT MAX(ordem) FROM notas WHERE arquivada = ? AND lixeira = 0"
                cursor.execute(query, (1 if arquivada else 0,))
            resultado = cursor.fetchone()[0]
            return resultado if resultado is not None else 0
    
    def atualizar_ordem(self, note_id, nova_ordem):
        """Atualiza a ordem de uma nota específica"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE notas SET ordem = ? WHERE id = ?", (nova_ordem, note_id))
            conn.commit()