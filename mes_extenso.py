def nome_mes(numero_mes):
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril",
        "Maio", "Junho", "Julho", "Agosto",
        "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    numero_mes=int(numero_mes)
    if 1 <= numero_mes <= 12:
        return meses[numero_mes - 1]
    else:
        return "Mês inválido"

# Exemplo de uso:
# numero = "12"
# # numero=int(numero)
# nome = nome_mes(numero)
# print(f"O nome do mês {numero} é {nome}.")
