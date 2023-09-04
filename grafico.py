import sqlite3, os
from mes_extenso import *
import locale
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import matplotlib
import random  # Importe a biblioteca random
from io import BytesIO
matplotlib.use('Agg')  # Modo não interativo
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
def Gerar_grafico():
    pass
    try:
        rel = por_mes()
        if rel == None:
            # print("Não fazer nada")
            return None
        else:
            # print("Gerar Gráfico")
            # Preparar dados para o gráfico
            meses = []
            saldos = []
            for row in rel:
                mes, total_entradas, total_saidas = row
                mes_e = mes.split("-")
                extenso_mes = mes_e[1]
                nome = nome_mes(extenso_mes)
                nome = f"{nome}/{mes_e[0]}"
                
                # Calcular o saldo
                saldo = total_entradas - total_saidas
                
                meses.append(nome)
                saldos.append(saldo)

            # Defina uma lista de cores sortidas
            cores = [random.choice(['#FF5733', '#33FF57', '#5733FF', '#FF33E8', '#33E8FF']) for _ in meses]

            # diretorio absoluto
            diretorio_atual = os.path.dirname(os.path.abspath(__file__))
            nome_do_arquivo = "relatorio_financeiro.pdf"
            caminho_do_arquivo = os.path.join(diretorio_atual, nome_do_arquivo)
            # Criar um PDF com os resultados
            doc = SimpleDocTemplate("C:\\Fin_Foco\\relatorio_financeiro.pdf", pagesize=letter)
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

            # Adicionar um espaço em branco
            elements.append(Spacer(1, 24))

            # Criar o gráfico
            plt.figure(figsize=(8, 4))
            plt.bar(meses, saldos, color=cores)  # Atribuir cores sortidas
            plt.xlabel('Mês')
            plt.ylabel('Saldo')
            plt.title('Saldo por Mês')
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Salvar o gráfico em um BytesIO
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()

            # Criar uma imagem do gráfico a partir dos bytes
            graph = Image(buffer, width=400, height=200)
            elements.append(graph)

            # Construir o PDF
            doc.build(elements)
            return 0
    except Exception as e:
        return 1
