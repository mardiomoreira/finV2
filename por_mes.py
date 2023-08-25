import sqlite3, locale

def pesquisa_e_soma_por_mes(numero_mes):
    # Conecta ao banco de dados
    conn = sqlite3.connect('financeiro.db')
    cursor = conn.cursor()

    # Define a consulta SQL para selecionar os registros do mês especificado
    consulta_registros = f"SELECT * FROM tbl_lancamentos WHERE strftime('%m', data) = ?"

    # Define a consulta SQL para calcular a soma das entradas do mês especificado
    consulta_entradas = f"SELECT SUM(valor) FROM tbl_lancamentos WHERE strftime('%m', data) = ? AND tipo = 'ENTRADA'"
    
    # Define a consulta SQL para calcular a soma das saídas do mês especificado
    consulta_saidas = f"SELECT SUM(valor) FROM tbl_lancamentos WHERE strftime('%m', data) = ? AND tipo = 'SAIDA'"

    # Executa a consulta para os registros
    cursor.execute(consulta_registros, (numero_mes,))
    registros = cursor.fetchall()
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
    # Executa as consultas para as entradas e saídas
    cursor.execute(consulta_entradas, (numero_mes,))
    soma_entradas = cursor.fetchone()[0] or 0  # Se não houver resultados, retorna 0
    soma_entradas_formatado = locale.format_string("%.2f", soma_entradas, grouping=True)
    cursor.execute(consulta_saidas, (numero_mes,))
    soma_saidas = cursor.fetchone()[0] or 0  # Se não houver resultados, retorna 0
    soma_saidas_formatado = locale.format_string("%.2f", soma_saidas, grouping=True)

    # Fecha a conexão com o banco de dados
    conn.close()

    # Retorna os registros, soma das entradas e soma das saídas
    return registros, soma_entradas_formatado, soma_saidas_formatado

# # Exemplo de uso:
# numero_mes = '09'  # Altere para o mês desejado
# registros, soma_entradas, soma_saidas = pesquisa_e_soma_por_mes(numero_mes)

# # Imprime os registros, soma das entradas e soma das saídas
# print("Registros:")
# for registro in registros:
#     print(registro)

# print(f"Soma das ENTRADAS: {soma_entradas}")
# print(f"Soma das SAIDAS: {soma_saidas}")
