import sqlite3
from mes_extenso import *
import locale
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Defina a localização para o formato desejado
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def formatar_valor(valor):
    return locale.currency(valor, grouping=True, symbol=None)

def por_mes():
    try:
        # Conectar-se ao banco de dados SQLite
        conn = sqlite3.connect('financeiro.db')
        cursor = conn.cursor()
        # Consulta SQL para recuperar os dados agrupados por mês
        consulta = """
        SELECT 
            strftime('%Y-%m', data) AS mes,
            SUM(CASE WHEN tipo = 'ENTRADA' THEN valor ELSE 0 END) AS total_entradas,
            SUM(CASE WHEN tipo = 'SAIDA' THEN valor ELSE 0 END) AS total_saidas
        FROM tbl_lancamentos
        GROUP BY mes
        ORDER BY mes;
        """
        # Executar a consulta SQL
        cursor.execute(consulta)
        # Recuperar os resultados
        resultados = cursor.fetchall()
        # Fechar a conexão com o banco de dados
        conn.close()
        return resultados
    except Exception as e:
        return None

# Exibir os resultados
rel = por_mes()

# Criar um PDF com os resultados
doc = SimpleDocTemplate("relatorio_financeiro.pdf", pagesize=letter)
elements = []

# Adicionar o título
styles = getSampleStyleSheet()
title_style = styles['Title']
title = Paragraph("Relatório por Mês", title_style)
elements.append(title)

# Cabeçalho da tabela
data = [['Mês', 'Total de Entradas', 'Total de Saídas', 'Saldo']]
for row in rel:
    mes, total_entradas, total_saidas = row
    mes_e = mes.split("-")
    extenso_mes = mes_e[1]
    nome = nome_mes(extenso_mes)
    nome = f"{nome}/{mes_e[0]}"
    
    # Calcular o saldo
    saldo = total_entradas - total_saidas
    
    # Formatar os valores
    total_entradas_fmt = formatar_valor(total_entradas)
    total_saidas_fmt = formatar_valor(total_saidas)
    saldo_fmt = formatar_valor(saldo)
    
    data.append([nome, total_entradas_fmt, total_saidas_fmt, saldo_fmt])

# Criar a tabela
table = Table(data)
style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)])

table.setStyle(style)

elements.append(table)

# Construir o PDF
doc.build(elements)
