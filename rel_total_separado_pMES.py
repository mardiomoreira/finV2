import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def gerar_relatorio_pdf(db_path, pdf_filename):
    # Conectar-se ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Consulta SQL para obter registros agrupados por mês
    query = """
    SELECT strftime('%Y-%m', data) AS mes, 
           SUM(CASE WHEN tipo = 'ENTRADA' THEN valor ELSE 0 END) AS receita_total,
           SUM(CASE WHEN tipo = 'SAIDA' THEN valor ELSE 0 END) AS despesa_total
    FROM tbl_lancamentos
    GROUP BY mes
    ORDER BY mes
    """

    cursor.execute(query)
    resultados = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    conn.close()

    # Criar um arquivo PDF
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Centralizar o título no PDF
    titulo = "RELATÓRIO FINANCEIRO POR MÊS"
    largura_pagina, altura_pagina = letter
    largura_texto = c.stringWidth(titulo, "Helvetica", 12)
    posicao_x = (largura_pagina - largura_texto) / 2
    c.drawString(posicao_x, altura_pagina - 50, titulo)

    # Escrever os dados do relatório no PDF
    y = 700
    for row in resultados:
        mes, receita_total, despesa_total = row
        saldo = receita_total - despesa_total
        
        # Adicionar um fundo cinza à linha do mês
        c.setFillColor(colors.lightgrey)
        c.rect(90, y - 8, 420, 20, fill=True)
        c.setFillColor(colors.black)
        
        c.drawString(100, y, f"Mês: {mes}")
        c.drawString(100, y - 20, f"Receita Total: R${receita_total:.2f}")
        c.drawString(100, y - 40, f"Despesa Total: R${despesa_total:.2f}")
        c.drawString(100, y - 60, f"Saldo: R${saldo:.2f}")
        y -= 80

    # Salvar o PDF
    c.save()

# Exemplo de uso da função
if __name__ == "__main__":
    db_path = "financeiro.db"
    pdf_filename = "relatorio_financeiro_p_MES.pdf"
    gerar_relatorio_pdf(db_path, pdf_filename)
