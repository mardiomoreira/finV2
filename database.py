import sqlite3
from datetime import datetime

class MinhaBaseDeDados:
    def __init__(self):
        self.conn = sqlite3.connect("financeiro.db")
        self.cursor = self.conn.cursor()
        self.DB_criar_tabela()

    def DB_criar_tabela(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tbl_lancamentos (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                data DATE,
                                tipo TEXT,
                                descricao VARCHAR,
                                valor REAL
                            )''')
        self.conn.commit()

    def DB_inserir_registro(self, data, tipo, descricao, valor):
        self.cursor.execute("INSERT INTO tbl_lancamentos (data, tipo, descricao, valor) VALUES (?, ?, ?, ?)",
                            (data, tipo, descricao, valor))
        self.conn.commit()

    def DB_atualizar_registro(self, id, data, tipo, descricao, valor):
        self.cursor.execute("UPDATE tbl_lancamentos SET data=?, tipo=?, descricao=?, valor=? WHERE id=?",
                            (data, tipo, descricao, valor, id))
        self.conn.commit()

    def DB_pesquisar_registro(self, id):
        self.cursor.execute("SELECT * FROM tbl_lancamentos WHERE id=?", (id,))
        registro = self.cursor.fetchone()
        return registro

    def DB_excluir_registro(self, id):
        self.cursor.execute("DELETE FROM tbl_lancamentos WHERE id=?", (id,))
        self.conn.commit()

    def DB_retornar_todos_os_registros(self):
        self.cursor.execute("SELECT * FROM tbl_lancamentos ORDER BY id DESC")
        registros = self.cursor.fetchall()
        return registros
    
    def DB_retornar_registros_entre_datas(self, data_inicio, data_fim):
        self.cursor.execute("SELECT * FROM tbl_lancamentos WHERE data BETWEEN ? AND ?", (data_inicio, data_fim))
        registros = self.cursor.fetchall()
        return registros

    def DB_calcular_soma_entradas_saidas(self):
        try:
            self.cursor.execute("SELECT SUM(CAST(REPLACE(valor, ',', '.') AS REAL)) FROM tbl_lancamentos WHERE tipo = 'ENTRADA'")
            soma_entradas = self.cursor.fetchone()[0] or 0  # Se for None, definimos como 0
            
            self.cursor.execute("SELECT SUM(CAST(REPLACE(valor, ',', '.') AS REAL)) FROM tbl_lancamentos WHERE tipo = 'SAIDA'")
            soma_saidas = self.cursor.fetchone()[0] or 0  # Se for None, definimos como 0
            return soma_entradas, soma_saidas
        except Exception as e:
            return None


    def DB_fechar_conexao(self):
        self.conn.close()

# if __name__ == "__main__":
#     base_de_dados = MinhaBaseDeDados()
    # resultado_entradas, resultado_saidas = base_de_dados.DB_calcular_soma_entradas_saidas()
    # print(resultado_entradas - resultado_saidas)
    # Exemplo de uso das funções
    # base_de_dados.DB_inserir_registro("2023-08-23", "SAIDA", "Aluguel", 8000.00)
    # base_de_dados.DB_inserir_registro("2023-08-24", "ENTRADA", "Salario", 9800.00)
    # base_de_dados.atualizar_registro(1, "2023-08-24", "ENTRADA", "Salario", 1800.00)
    
    # registros = base_de_dados.DB_retornar_todos_os_registros()
    # if registros:
    #     # print("Registro encontrado:", registros)
    #     for registro in registros:
    #         id, data, tipo, descricao, valor = registro
    #         valor_formatado = valor
    #         data_formatada = data
    #         print(f"ID: {id}, Data: {data_formatada}, Tipo: {tipo}, Descrição: {descricao}, Valor: {valor_formatado}")
    # else:
    #     print("Registro não encontrado.")
    
    # base_de_dados.excluir_registro(1)
    
    # base_de_dados.DB_fechar_conexao()
