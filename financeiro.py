import tkinter as tk
from tkinter import ttk,messagebox
from tkinter import *
from tkinter.font import Font
from tkcalendar import DateEntry
import re, datetime, locale, os, subprocess
from database import MinhaBaseDeDados
from datetime import datetime
from tktooltip import ToolTip
from tkinter import PhotoImage
from PIL import Image, ImageTk
import threading, time
from por_mes import pesquisa_e_soma_por_mes
from grafico import Gerar_grafico
class JanelaCentrada:
    def __init__(self):
        self.id_update=None
        self.tela()
        self.componentes()
        self.exibir_registros_na_treeview()
        self.calcular_saldo()
        self.jprincipal.mainloop()

    def tela(self):
        self.jprincipal = Tk()
        self.jprincipal.iconbitmap("icone.ico")
        self.jprincipal.resizable(width=False,height=False)
        self.jprincipal.title("..:: Finanças em Foco ::..")
        self.jprincipal.configure(background='white')
        # Crie um objeto Menu
        self.barra_menu = tk.Menu(self.jprincipal)
        # Crie um submenu sob "Pesquisa"
        self.menu_pesquisa = tk.Menu(self.barra_menu, tearoff=0)
        self.menu_pesquisa.add_command(label="Por Mês", command=self.btn_por_mes)
        self.menu_pesquisa.add_command(label="Registros Por Mês",command=self.registros_por_mes)
        # Adicione o submenu "Pesquisa" à barra de menu
        self.barra_menu.add_cascade(label="Pesquisa", menu=self.menu_pesquisa)

        # Configure a barra de menu na janela principal
        self.jprincipal.config(menu=self.barra_menu)
        # Obtém a largura e a altura da tela
        largura_tela = self.jprincipal.winfo_screenwidth()
        altura_tela = self.jprincipal.winfo_screenheight()
        largura=500
        altura=420

        # Calcula as coordenadas X e Y para centralizar a janela
        x = (largura_tela - largura) // 2  # Largura da janela
        y = (altura_tela - altura) // 2   # Altura da janela

        # Define as dimensões e a posição da janela
        self.jprincipal.geometry("{}x{}+{}+{}".format(largura,altura,x, y))
    def registros_por_mes(self):
        from rel_total_separado_pMES import gerar_relatorio_pdf
        db_path = "financeiro.db"
        pdf_filename = "relatorio_financeiro_p_MES.pdf"
        if os.path.isfile(pdf_filename):
            os.remove(pdf_filename)
        gerar_relatorio_pdf(db_path, pdf_filename)
        os.system(f"start {pdf_filename}")
    def get_selected_date(self):
        selected_date = self.date_entry.get()
        print("Data selecionada:", selected_date)
        
    def limpar_campo(self):
        self.ent_valor.configure(validate='none')
        self.ent_valor.delete(0,END)
        self.ent_valor.configure(validate='key')
        self.date_entry.set_date(None)  # Limpa o campo DateEntry
        self.cbx_tipo.set("")           # Limpa o Combobox
        self.ent_descricao.delete(0, "end")  # Limpa o Entry de descrição
        
    def componentes(self):
        #WidGet
        self.lbf_data=LabelFrame(self.jprincipal,text=" Data ",labelanchor='n',border=2,padx=5,pady=5,background='white',font=('Arial',10,'bold italic'))
        self.date_entry = DateEntry(self.lbf_data, width=12, background='darkblue',foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.lbf_tipo=LabelFrame(self.jprincipal,text=" Tipo ",labelanchor='n',border=2,padx=5,pady=5,background='white',font=('Arial',10,'bold italic'))
        self.combo_var = tk.StringVar()
        self.cbx_tipo = ttk.Combobox(self.lbf_tipo, textvariable=self.combo_var, values=["ENTRADA", "SAIDA"],width=8)
        def validar_entrada(P):
            # Substituir vírgula por ponto para facilitar a conversão
            P = P.replace(',', '.')
            # Verificar se a entrada é um número válido
            if re.match(r"^\d+(\.\d{0,2})?$", P) is not None:
                return True
            else:
                return False
        self.lbf_valor=LabelFrame(self.jprincipal,text=" Valor ",labelanchor='n',border=2,padx=5,pady=5,background='white',font=('Arial',10,'bold italic'))
        self.ent_valor=Entry(self.lbf_valor,justify='center',width=15, validate="key")
        self.ent_valor["validatecommand"] = (self.ent_valor.register(validar_entrada), "%P")
        self.lbf_descricao=LabelFrame(self.jprincipal,text=" Descrição ",labelanchor='n',border=2,padx=5,pady=5,background='white',font=('Arial',10,'bold italic'))
        self.ent_descricao=Entry(self.lbf_descricao,justify='center',width=480)
        self.lbf_tree=LabelFrame(self.jprincipal,text=" Lançamentos ",labelanchor='n',border=2,padx=5,pady=5,background='white',font=('Arial',10,'bold italic'))
        self.tree_lancamentos = ttk.Treeview(self.lbf_tree, columns=("ID","Data", "Tipo", "Descrição", "Valor"), show="headings",style="mystyle.Treeview")
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Calibri', 11,'bold italic'))
        # Adiciona colunas formatadas
        self.tree_lancamentos.heading("ID", text="ID", anchor="center")
        self.tree_lancamentos.heading("Data", text="Data", anchor="center")
        self.tree_lancamentos.heading("Tipo", text="Tipo", anchor="center")
        self.tree_lancamentos.heading("Descrição", text="Descrição", anchor="center")
        self.tree_lancamentos.heading("Valor", text="Valor", anchor="center")
        # Define a largura das colunas
        self.tree_lancamentos.column("ID", width=50,anchor='center')
        self.tree_lancamentos.column("Data", width=70,anchor='center')
        self.tree_lancamentos.column("Tipo", width=60,anchor='center')
        self.tree_lancamentos.column("Descrição", width=150,anchor='center')
        self.tree_lancamentos.column("Valor", width=60,anchor='center')
        # Barra de Rolagem
        scrollbar = ttk.Scrollbar(self.lbf_tree, orient="vertical", command=self.tree_lancamentos.yview)
        self.tree_lancamentos.configure(yscrollcommand=scrollbar.set)
        # Insere alguns dados de exemplo
        self.lbf_botao=LabelFrame(self.jprincipal,text="",labelanchor='n',border=0,padx=5,pady=5,background='white',font=('Arial',10,'bold italic'))
        self.btn_cadastrar=Button(self.lbf_botao,text="Cadastrar",command=self.cadastrar_lancamento)
        ToolTip(widget=self.btn_cadastrar,msg="Cadastra lançamento digitado",delay=1)
        self.btn_limpar=Button(self.lbf_botao,text="Limpar",command=self.limpar_campo)
        ToolTip(widget=self.btn_limpar,msg="Limpa os Campos:\n- Tipo\n- Valor\n- Descrição",delay=1)
        self.btn_update=Button(self.lbf_botao,text="Editar",command=self.atualizar_registro)
        ToolTip(widget=self.btn_update,msg="Edita o registro Selecionado na Tabela",delay=1)
        self.img=PhotoImage(file="report48.png")
        self.btn_rel=Button(self.jprincipal,image=self.img,command=self.executar_open_relatorio,background="white")
        ToolTip(widget=self.btn_rel,msg="Relatorio Todos registos por mes",delay=1)
        # Posicionamento
        self.lbf_data.place(x=90,y=5)
        self.date_entry.pack()
        self.lbf_tipo.place(x=210,y=5)
        self.cbx_tipo.pack()
        self.lbf_valor.place(x=305,y=5)
        self.ent_valor.pack()        
        self.lbf_descricao.place(x=5,y=55,width=490)        
        self.ent_descricao.pack()
        self.lbf_tree.place(x=5,y=160,width=490, height=200)
        self.tree_lancamentos.pack(padx=10)
        scrollbar.place(x=435,y=3, height=165)
        self.lbf_botao.place(x=150,y=110,width=200)
        self.btn_cadastrar.pack(side="left", padx=5)   
        self.btn_limpar.pack(side="left", padx=5)
        self.btn_update.pack(side="left",padx=5)
        self.btn_rel.place(x=456,y=12)

    def btn_por_mes(self):
        self.lbf_porMes=LabelFrame(self.jprincipal,text=" Pesquisa Mês ",labelanchor='n',border=2,padx=5,pady=5,background='white',font=('Arial',10,'bold italic'),width=50)
        self.lbf_porMes.place(x=350,y=110,width=100)
        meses = {
            'Janeiro': '01',
            'Fevereiro': '02',
            'Março': '03',
            'Abril': '04',
            'Maio': '05',
            'Junho': '06',
            'Julho': '07',
            'Agosto': '08',
            'Setembro': '09',
            'Outubro': '10',
            'Novembro': '11',
            'Dezembro': '12',
        }
        self.cbx_pmes = ttk.Combobox(self.lbf_porMes, values=list(meses.keys()),width=50)
        self.cbx_pmes.pack()
        def obter_numero_mes(event):
            mes_selecionado = self.cbx_pmes.get()
            numero_mes = meses.get(mes_selecionado)
            if numero_mes:
                # print(f'Número do mês: {numero_mes}')
                registros, soma_entradas, soma_saidas = pesquisa_e_soma_por_mes(numero_mes)
                # print(soma_entradas.replace(".","").replace(",","."), soma_saidas)
                soma_entradas_formatada=soma_entradas.replace(".","").replace(",",".")
                soma_entradas_formatada=float(soma_entradas_formatada)
                soma_saidas_formatada=soma_saidas.replace(".","").replace(",",".")
                soma_saidas_formatada=float(soma_saidas_formatada)
                soma_total=soma_entradas_formatada - soma_saidas_formatada
                locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
                soma_total_formatada= locale.format_string("%.2f", soma_total, grouping=True)
                self.lbl_entrada.configure(text=soma_entradas)
                self.lbl_saida.configure(text=soma_saidas)
                self.lbl_total.configure(text=soma_total_formatada)
                if len(registros)>0:
                    # print("Popular Treeview")
                    self.limpar_treeview()
                    for registro in registros:
                        # print(registro)
                        self.tree_lancamentos.insert("","end",values=registro)
        self.cbx_pmes.bind("<<ComboboxSelected>>", obter_numero_mes)
        
    def open_relatorio(self):
        try:
            g=Gerar_grafico()
            if g == 0:
                nome_do_arquivo = "relatorio_financeiro.pdf"
                # diretorio_atual = os.path.dirname(os.path.abspath(__file__))
                diretorio_atual = "C:\\Fin_Foco"
                # Constrói o caminho completo para o arquivo
                caminho_do_arquivo = os.path.join(diretorio_atual, nome_do_arquivo)
                caminho_do_arquivo = os.path.join(diretorio_atual, nome_do_arquivo)
                if os.path.exists(caminho_do_arquivo):
                    # Deleta o arquivo
                    subprocess.run(f"del {caminho_do_arquivo}",shell=True)
                    # Gerando o Relatório com Gráfico Atualizador
                    Gerar_grafico()
                    # Abrindo o Relatório em PDF
                    os.system(command=f"start C:\\Fin_Foco\\relatorio_financeiro.pdf")
                else:
                    # Gerando o Relatório com Gráfico
                    Gerar_grafico()
                    time.sleep(2)  # import time
                    # Abrindo o Relatório em PDF
                    os.system(command=f"start C:\\Fin_Foco\\relatorio_financeiro.pdf")
            else:
                pass
            # end if
            # print("Resposta:",g)
        except Exception as e:
            messagebox.showerror(title="Erro:",message="Erro ao abir relataório")

    def executar_open_relatorio(self):
        threading.Thread(target=self.open_relatorio).start()
        
    def calcular_saldo(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        banco_dados= MinhaBaseDeDados()
        resultado_entradas, resultado_saidas = banco_dados.DB_calcular_soma_entradas_saidas()
        lbf_entrada=LabelFrame(self.jprincipal, text="Saldo Entradas",font=('Arial',9,'bold italic'),background="white")
        lbf_entrada.place(x=5,y=365)
        self.lbl_entrada=Label(lbf_entrada, text="",background="white")
        self.lbl_entrada.pack()
        lbf_saida=LabelFrame(self.jprincipal, text="Saldo Saídas",font=('Arial',9,'bold italic'),background="white")
        lbf_saida.place(x=210,y=365)
        self.lbl_saida=Label(lbf_saida, text="saida",background="white")
        self.lbl_saida.pack()
        num_entrada=float(resultado_entradas)
        numero_arredondado = round(num_entrada, 2)
        numero_formatado = locale.format_string("%.2f", numero_arredondado, grouping=True)
        self.lbl_entrada.configure(text=f"R$ {numero_formatado}")
        num_saida=float(resultado_saidas)
        saida_arredondado= round(num_saida,2)
        saida_formatado = locale.format_string("%.2f", saida_arredondado, grouping=True)
        self.lbl_saida.configure(text=f"R$ {saida_formatado}")
        lbf_total=LabelFrame(self.jprincipal, text="Saldo Total",font=('Arial',9,'bold italic'),background="white")
        lbf_total.place(x=420,y=365)
        self.lbl_total=Label(lbf_total,text="",background="white")
        self.lbl_total.pack()
        total = resultado_entradas - resultado_saidas
        total=float(total)
        total_aredondado= round(total,2)
        total_formatada=locale.format_string("%.2f",total_aredondado, grouping=True)
        self.lbl_total.configure(text=f"R$ {total_formatada}")
        
    def cadastrar_lancamento(self):
        campos_vazios = []
        if not self.date_entry.get():
            campos_vazios.append("Data")
        if not self.cbx_tipo.get():
            campos_vazios.append("Tipo")
        if not self.ent_valor.get():
            campos_vazios.append("Valor")
        if not self.ent_descricao.get():
            campos_vazios.append("Descrição")
        if campos_vazios:
            campos_faltando = ", ".join(campos_vazios)
            messagebox.showerror("Campos Obrigatórios", f"Os seguintes campos são obrigatórios: {campos_faltando}")
        else:
            # Faça o que quiser com os dados, porque todos os campos estão preenchidos
            # Por exemplo, envie os dados para o banco de dados ou realize outra ação.
            
            data=self.date_entry.get()
            dataf=datetime.strptime(data,'%d/%m/%Y')
            data_formatada=dataf.strftime('%Y-%m-%d')
            tipo=self.cbx_tipo.get()
            valor=self.ent_valor.get()
            descricao=self.ent_descricao.get()
            # print(f"data; {data}\ntipo: {tipo}\nvalor: {valor}\nDescrição: {descricao}")
            base_de_dados = MinhaBaseDeDados()
            base_de_dados.DB_inserir_registro(data=data_formatada,tipo=tipo,descricao=descricao,valor=valor)
            self.limpar_campo()
            self.exibir_registros_na_treeview()
            self.calcular_saldo()
            messagebox.showinfo("Sucesso", "Registo insrido com Sucesso!!")

    def limpar_treeview(self):
        try:
            # Obtém todos os itens da treeview
            itens = self.tree_lancamentos.get_children()
            
            # Remove todos os itens da treeview
            for item in itens:
                self.tree_lancamentos.delete(item)
        except Exception as e:
            pass

    def exibir_registros_na_treeview(self):
        self.limpar_treeview()
        base_de_dados = MinhaBaseDeDados()
        registros = base_de_dados.DB_retornar_todos_os_registros()
        if registros:
            # print("Registro encontrado:", registros)
            for registro in registros:
                # id, data, tipo, descricao, valor = registro
                # valor_formatado = f"{valor:.2f}"
                # data_datetime = datetime.strptime(data, '%Y-%m-%d')
                # data_formatada = data_datetime.strftime('%d/%m/%Y')
                # valor_formatado=float(valor_formatado)
                # print(f"ID: {id}, Data: {data_formatada}, Tipo: {tipo}, Descrição: {descricao}, Valor: {valor_formatado}")
                self.tree_lancamentos.insert("","end",values=registro)
        else:
            print("Registro não encontrado.")
                # self.tree_lancamentos.insert("", "end", values=registro)

    def atualizar_registro(self):
        selecionados = self.tree_lancamentos.selection()
        
        if selecionados:
            self.limpar_campo()
            # Pega o primeiro item selecionado (pode haver vários se a seleção múltipla estiver ativada)
            primeiro_selecionado = selecionados[0]
            
            # Obtém os valores da linha selecionada
            valores = self.tree_lancamentos.item(primeiro_selecionado, "values")
            id=valores[0]
            self.id_update=id
            data=valores[1]
            tipo=valores[2]
            descricao=valores[3]
            valor=valores[4]
            # print(f"id: {self.id_update} | data {data} | tipo {tipo} | valor: {valor}")
            self.ent_descricao.insert(0,descricao)
            self.ent_valor.configure(validate='none')
            self.ent_valor.insert(0,valor)
            self.ent_valor.configure(validate='key')
            self.cbx_tipo.insert(0,tipo)
            self.btn_update.destroy()
            self.btn_update=Button(self.lbf_botao,text="Update",command=self.update_registro_BD)
            self.btn_update.pack(side="left",padx=5)
            # Faça o que desejar com os valores da linha selecionada
            # print("Valores da linha selecionada:", valores)
        else:
            messagebox.showinfo(title="Selecionar",message="Favor selecionar o registro a ser editado")

    def update_registro_BD(self):
        if self.id_update == None:
            messagebox.showinfo(title='Selecionar',message="Favor selecionar algum registro para atualizar")
        else:
            # messagebox.showinfo(title='Selecionar',message=f"ok id: {self.id_update}")
            base_dados= MinhaBaseDeDados()
            data=self.date_entry.get_date()
            # dataf=datetime.strptime(data,'%d/%m/%Y')
            # data_formatada=dataf.strftime('%Y-%m-%d')
            tipo=self.cbx_tipo.get()
            valor=self.ent_valor.get()
            descricao=self.ent_descricao.get()
            # print(f"ID: {self.id_update}, Data: {data_formatada}, Tipo: {tipo}, Descrição: {descricao}, Valor: {valor}")
            base_dados.DB_atualizar_registro(id=self.id_update,data=data,tipo=tipo,descricao=descricao,valor=valor)
            self.exibir_registros_na_treeview()
    
if __name__ == "__main__":
    app = JanelaCentrada()
