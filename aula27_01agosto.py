# PROGRAMA PARA CONSULTA, ALTERAÇÃO, INSERÇÃO E REMOÇÃO DE DADOS

import mysql.connector
from mysql.connector import Error
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, ttk

# CRIAÇÃO DA TELA
master = Tk()
master.maxsize(width=600, height=400)
master.minsize(width=600, height=400)
master.geometry('-350+100')
master['bg'] = "#252729"
master.focus_force()

# FUNÇÃO PARA CONECTAR AO BANCO DE DADOS
def conectar():
    try:
        global con
        con = mysql.connector.connect(
        host='localhost',
        database='cadastros',
        user='root',
        password=''
        )
    except Error as erro:
        print('Erro de conexão '+ erro)

# FUNÇÃO PARA LIMPAR ENTRADAS E TABELA
def clear():
    EntNome.delete(0, 'end')
    EntIdade.delete(0,'end')
    cbSexo.delete(0, 'end')
    cbCidade.delete(0, 'end')
    EntAltura.delete(0, 'end')

    for item in tv.get_children():
                tv.delete(item)

# FUNÇÃO PARA CARREGAR OS ENTRYS COM A LINHA SELECIONADA
def obter():
    itemSelecionado = tv.selection()
    valores = tv.item(itemSelecionado, 'values')
    vago = ', '.join(valores)

    if(vago != ('')):
        EntNome.delete(0, 'end')
        EntIdade.delete(0, 'end')
        cbSexo.delete(0, 'end')
        cbCidade.delete(0, 'end')
        EntAltura.delete(0, 'end')

        itemSelecionado = tv.selection()[0]
        valores = tv.item(itemSelecionado, 'values')
        EntNome.insert(0,valores[1])
        EntIdade.insert(0,valores[2])
        cbSexo.insert(0,valores[3])
        cbCidade.insert(0,valores[4])
        EntAltura.insert(0,valores[5])         
    else:
        messagebox.showerror(title='Erro', message=('Selecione um item!'))

# FUNÇÃO PARA LISTAR NA TABELA
def listar():
    try:
        conectar()
        consulta_listar = """ SELECT
                                A.idCliente,
                                A.nomeCliente,
                                A.dataNascimentoCliente,
                                B.nomeSexo,
                                C.nomeCidade,
                                A.altura
                            FROM
                                cliente A,
                                sexo B,
                                cidade C
                            WHERE
                                A.idSexo = B.idSexo AND
                                A.idCidade = C.idCidade """
    
        cursor = con.cursor()
        cursor.execute(consulta_listar)
        resultado = cursor.fetchall()
        tamanho = len(resultado)

        clear()
        messagebox.showinfo(title='Carregando tabela', message='Aguarde, carregando tabela.')
        print('Número de registros retornados: ', cursor.rowcount)

        for info in range(tamanho):
             tv.insert('','end', values=(resultado[info]))
        messagebox.showinfo(title='Carregado', message='Lista carregada.')

    except Error as erro:
        print('Falha ao acessar tabela MySQL: {}'. format(erro))
    finally:
        if(con.is_connected()):
            cursor.close()
            con.close()
            print('Conexão ao MySQL finalizada')
        
    EntIdade.insert(0, "AAAA-MM-DD")

# FUNÇÃO PARA ADICIONAR CADASTROS NA TABELA
def adicionar(nome, idade, sexo, cidade, altura):
    try:
        conectar()
        inserir_cadastro = f""" INSERT INTO cliente
                                    (nomeCliente,
                                    dataNascimentoCliente,
                                    idSexo,
                                    idCidade,
                                    altura)
                                VALUES
                                    ("{nome}", "{idade}", {sexo}, {cidade}, {altura}) """
        cursor = con.cursor()
        cursor.execute(inserir_cadastro)
        con.commit()
        print(f'Foram inseridos {cursor.rowcount} registros na tabela!')
        cursor.close()

        messagebox.showinfo(title='Inserido', message='Registro inserido com sucesso!')

    except Error as erro:
        print('Falha ao inserir dadods MySQL: {}'.format(erro))

    finally:
        if(con.is_connected()):
            cursor.close()
            con.close()
            print('Conexão ao MySQL finalizada')

    # chamando a função de listar para atualizar a tabela
    listar()

# FUNÇÃO PARA CHAMAR O ADICIONAR E TESTAR SE OS CAMPOS ESTÃO PREENCHIDOS
def salvar():
    nome = EntNome.get()
    idade = EntIdade.get()
    sexo = cbSexo.current()
    cidade = cbCidade.current()
    altura = EntAltura.get()

    if(nome != ''):
        if(idade != ''):
            if(sexo == 1 or sexo == 2):
                if(cidade == 1 or cidade == 2):
                    if(altura != ''):
                        adicionar(nome, idade, sexo, cidade, altura)
                    else:
                        messagebox.showerror(title='ERRO', message='Você precisa informar todos os dados para inserir')
                else:
                    messagebox.showerror(title='ERRO', message='Você precisa informar todos os dados para inserir')

            else:
                messagebox.showerror(title='ERRO', message='Você precisa informar todos os dados para inserir')
        else: 
            messagebox.showerror(title='ERRO', message='Você precisa informar todos os dados para inserir')
    else:
        messagebox.showerror(title='ERRO', message='Você precisa informar todos os dados para inserir')

# FUNÇÃO PARA ALTERAR ITEM NA TABELA
def alterar():
    nome = EntNome.get()
    idade = EntIdade.get()
    sexo = cbSexo.current()
    cidade = cbCidade.current()
    altura = EntAltura.get()

    itemSelecionado = tv.selection()
    valores = tv.item(itemSelecionado, 'values')
    vago = ', '.join(valores)

    if(vago != ''):
        cod = valores[0]
        if(nome != ''):
            if(idade != ''):
                if(sexo == 1 or sexo == 2):
                    if(cidade == 1 or cidade == 2):
                        if(altura != ''):
                            try:
                                conectar()
                                alterar_cadastro = f""" UPDATE cliente SET
                                                            nomeCliente = '{nome}',
                                                            dataNascimentoCliente = '{idade}',
                                                            idSexo = {sexo},
                                                            idCidade = {cidade},
                                                            altura = {altura}
                                                        WHERE idCliente = {cod}"""
                                cursor = con.cursor()
                                cursor.execute(alterar_cadastro)
                                con.commit()

                            except Error as erro:
                                print('Falha ao acessar tabela MySQL: {}'.format(erro))
                            
                            finally:
                                if(con.is_connected()):
                                    cursor.close()
                                    con.close()
                                    print('Conexão ao MySQL finalizada')
                            
                            print('Cadastro alterado com sucesso!')
                            messagebox.showinfo(title='Atualizado', message='Cadastro atualizado com sucesso!')
                            listar()
                        else:
                            messagebox.showerror(title='ERRO', message='Você precisa informar todos os dados para inserir')
                    else:
                        messagebox.showerror(title='ERRO', message='Você precisa informar todos os dados para inserir')

                else:
                    messagebox.showerror(title='ERRO', message='Você precisa informar todos os dados para inserir')
            else: 
                messagebox.showerror(title='ERRO', message='Você precisa informar todos os dados para inserir')
        else:
            messagebox.showerror(title='ERRO', message='Você precisa informar todos os dados para inserir')
    else:
        messagebox.showerror(title='ERRO', message='Você precisa selecionar um registro')
        messagebox.showinfo(title='AVISO', message='Para alterar, você precisa primeiro selecionar OBTER!')

# FUNÇÃO PARA DELETAR UM REGISTRO
def deletar():
    itemSelecionado = tv.selection()
    valores = tv.item(itemSelecionado, 'values')
    vago = ', '.join(valores)

    if(vago != ('')):
        cod = valores[0]
        res = messagebox.askyesno('Deletar', 'Deseja deletar o item selecionado?')
        if (res==True ):
            try:
                conectar()
                deletar_registro = f'DELETE FROM cliente WHERE idCliente = {cod}'
                cursor = con.cursor()
                cursor.execute(deletar_registro)
                con.commit()

            except Error as erro:
                print('Falha ao acessar tabela MySQL: {}'.format(erro))
            
            finally:
                if(con.is_connected()):
                    cursor.close()
                    con.close()
                    print('Conexão ao MySQL finalizada')

            messagebox.showinfo(title='Deletado', message='Registro deletado!')
            listar()
        else:
            messagebox.showinfo(title='Cancelada', message=('Operação cancelada.'))
    else:
        messagebox.showerror(title='Erro', message=('Selecione um item!'))

#CRIAÇÃO DOS LABEL DAS ENTRYS
lbNome = Label(master, text='Nome: ', font='Arial 10 bold', background='#252729', foreground='white')
lbNome.place(relx=0.01, rely=0.06)
EntNome = Entry(master)
EntNome.place(relx=0.09, rely=0.06)

lbIdade = Label(master, text='Nascimento: ', font='Arial 10 bold', background='#252729', foreground='white')
lbIdade.place(relx=0.31, rely=0.06)
EntIdade = Entry(master)
EntIdade.place(relx=0.45, rely=0.06)

lbSexo = Label(master, text='Sexo: ', font='Arial 10 bold', background='#252729', foreground='white')
lbSexo.place(relx=0.67, rely=0.06)
cbSexo = Combobox(master)
cbSexo['values'] = ['>> SELECIONE <<', 'Masculino', 'Feminino']
cbSexo.place(relx=0.75, rely= 0.06)

lbCidade = Label(master, text='Cidade: ', font='Arial 10 bold', background='#252729', foreground='white')
lbCidade.place(relx=0.15, rely=0.15)
cbCidade = Combobox(master)
cbCidade['values'] = ['>> SELECIONE <<', 'Venâncio Aires', 'Santa Cruz do Sul']
cbCidade.place(relx=0.25, rely= 0.15)

lbAltura = Label(master, text='Altura: ', font='Arial 10 bold', background='#252729', foreground='white')
lbAltura.place(relx=0.51, rely=0.15)
EntAltura = Entry(master)
EntAltura.place(relx=0.6, rely=0.15)

# CRIAÇÃO DO FRAME PRA TABELA
TreeArea = Frame(master)
TreeArea.place(relx=0.08, rely=0.3, relwidth=0.85, relheight=0.45)

# CRIAÇÃO DA TABELA TREE VIEW
tv = ttk.Treeview(TreeArea, columns=('cod','nome','nasc','sexo', 'cidade', 'altura'), show='headings')
tv.column('cod', minwidth=0,width=30)
tv.column('nome', minwidth=0, width=155)
tv.column('nasc', minwidth=0, width=75)
tv.column('sexo', minwidth=0, width=70)
tv.column('cidade', minwidth=0, width=120)
tv.column('altura', minwidth=0, width=45)
tv.heading('cod', text='Cod')
tv.heading('nome', text='Nome')
tv.heading('nasc', text='Nasc')
tv.heading('sexo', text='Sexo')
tv.heading('cidade', text='Cidade')
tv.heading('altura', text='Altura')
tv.grid(column=0, row=0, columnspan=3, pady=0)
tv.pack(side ='left')

# CRIAÇÃO DA SCROLL BAR
verscrlbar = ttk.Scrollbar(TreeArea, orient ="vertical", command = tv.yview)
verscrlbar.pack(side ='right', fill ='y')

# CRIAÇÃO DOS BOTÕES
# photoObter = PhotoImage(file= "C:/Users/kauan/Documentos/Curso Python/Kauany/python/agosto/icon_obter.png")
# photoObter = PhotoImage(file="C:/Users/Aluno/Documents/Kauany/python/agosto/icon_obter.png")
# btObter = Button(master, text='Obter', image= photoObter, compound=LEFT, command=obter)
# btObter.place(relx=0.81, rely= 0.23, height = 25, width = 70)

btObter = Button(master, text='Obter', compound=LEFT, command=obter)
btObter.place(relx=0.81, rely= 0.23, height = 25, width = 70)

# photoAdicionar = PhotoImage(file= "C:/Users/kauan/Documentos/Curso Python/Kauany/python/agosto/icon_salvar.png")
# photoAdicionar = PhotoImage(file= "C:/Users/Aluno/Documents/Kauany/python/agosto/icon_salvar.png")
# btAdicionar = Button(master, text='Salvar', image= photoAdicionar, compound=LEFT, command=salvar)
# btAdicionar.place(relx=0.08, rely= 0.82)

btAdicionar = Button(master, text='Salvar', compound=LEFT, command=salvar)
btAdicionar.place(relx=0.08, rely= 0.82)

# photoAlterar = PhotoImage(file= "C:/Users/kauan/Documentos/Curso Python/Kauany/python/agosto/icon_alterar.png")
# photoAlterar = PhotoImage(file= "C:/Users/Aluno/Documents/Kauany/python/agosto/icon_alterar.png")
# btAlterar = Button(master, text='Alterar', image= photoAlterar, compound=LEFT, command=alterar)
# btAlterar.place(relx=0.29, rely= 0.82)

btAlterar = Button(master, text='Alterar', compound=LEFT, command=alterar)
btAlterar.place(relx=0.29, rely= 0.82)

# photoAtualizar = PhotoImage(file= "C:/Users/kauan/Documentos/Curso Python/Kauany/python/agosto/icon_atualizar.png")
# photoAtualizar = PhotoImage(file="C:/Users/Aluno/Documents/Kauany/python/agosto/icon_atualizar.png")
# btAtualizar = Button(master, text='Atualizar', image= photoAtualizar, compound=LEFT, command=listar)
# btAtualizar.place(relx=0.50, rely= 0.82)

btAtualizar = Button(master, text='Atualizar', compound=LEFT, command=listar)
btAtualizar.place(relx=0.50, rely= 0.82)

# photoDeletar = PhotoImage(file= "C:/Users/kauan/Documentos/Curso Python/Kauany/python/agosto/icon_deletar.png")
# photoDeletar = PhotoImage(file="C:/Users/Aluno/Documents/Kauany/python/agosto/icon_deletar.png")
# btDeletar = Button(master, text='Deletar', image= photoDeletar, compound=LEFT, command=deletar)
# btDeletar.place(relx=0.71, rely= 0.82)

btDeletar = Button(master, text='Deletar', compound=LEFT, command=deletar)
btDeletar.place(relx=0.71, rely= 0.82)

listar()

mainloop()