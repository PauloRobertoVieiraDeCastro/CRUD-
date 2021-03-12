from tkinter import *
import sqlite3
from tkinter import ttk
from tkinter import tix
from tkinter import messagebox
from tkinter import scrolledtext
import tkinter as tk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate
import webbrowser
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import funcionalidades
import relatorio

root = tix.Tk() #instanciando a classe tk

class Principal(funcionalidades.Funcionalidades, relatorio.GeraRelatorio):
    def __init__(self):
        self.root = root
        self.nome_fantasia3 = StringVar()
        self.poco3 = StringVar()
        self.data_rec3 = StringVar()
        self.inf3 = StringVar()
        self.contador3 = StringVar()
        self.texto3 = StringVar()
        self.tipo3 = StringVar()
        self.tela_principal()
        self.frame_da_tela()
        self.w_frame_1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        self.root.mainloop()

    def tela_principal(self):
        """
        Configurando a tela
        """
        self.root.title("Cadastro de amostras")
        self.a = 'slate blue'
        self.root.configure(background=self.a)#'#1e3743')
        self.root.geometry("1000x700") #geometria inicial
        self.root.resizable(True,True) #redimensiona nos eixos
        self.root.maxsize(width=1100,height=750) #dimensões máximas
        self.root.minsize(width=900,height=700)#dimensões mínimas

        #mudo o favicon
        self.favicon = PhotoImage(file = "petro.png")
        self.root.iconphoto(False,self.favicon)

    def frame_da_tela(self):
        
        self.frame1 = Frame(self.root, bd=4,bg=self.a) #crio uma borda, uma cor de background, uma cor de borda e uma espessura de borda
        self.frame1.place(relx = 0.01, rely = 0.0, relwidth = 0.98, relheight=0.53)

        self.frame2 = Frame(self.root, bd=4,bg='#dfe3ee',
                            highlightbackground = 'white',
                            highlightthickness=3) #crio uma borda, uma cor de background, uma cor de borda e uma espessura de borda
        self.frame2.place(relx = 0.01, rely = 0.54, relwidth = 0.98, relheight=0.44)

    def w_frame_1(self):
        self.abas = ttk.Notebook(self.frame1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)
        self.aba1.configure(background='slate blue')
        self.aba2.configure(background="slate blue")
        self.abas.add(self.aba1, text = "Entrada de amostra")
        self.abas.add(self.aba2, text = "Estatísticas")

        self.abas.place(relx=0,rely=0,relwidth=1.0,relheight=1.0)
        try:
            self.df = self.consulta() 
            self.contagem = len(self.df['Nome_Fantasia'].unique())+1
        except:
            self.contagem = 1

        self.vol = []
        self.peso = []
        self.local = []
        self.qtd_cads = 30
        #Entradas e labels-------------------------------------------------------------------------------------------------------------------------------------------
        Label(self.aba1,text="Contagem",bg=self.a,font = ('Helvetica', 9, 'bold'),fg='white').place(relx=0.02,rely=0.02)

        #-------------------------------------------eVENTO CODIGO--------------------------------------------
        self.codigo_entry1 = Entry(self.aba1,font = ('verdana', 8),justify='center')
        self.codigo_entry1.place(relx=0.18,rely=0.02)
        self.codigo_entry1.insert(END,self.contagem)

        #--------------------------------------AUTOCOMPLETE----------------------------------------------------------------------------------
        def match_string():
            hits = []
            got = self.auto.get()
            for item in self.chiefs:
                if item.startswith(got):
                    hits.append(item)
            return hits    

        def get_typed(event):
            if len(event.keysym) == 1:
                hits = match_string()
                show_hit(hits)

        def show_hit(lst):
            if len(lst) == 1:
                self.auto.set(lst[0])
                detect_pressed.filled = True

        def detect_pressed(event):    
            key = event.keysym
            if len(key) == 1 and detect_pressed.filled is True:
                pos = self.f_entry.index(tk.INSERT)
                self.f_entry.delete(self.pos, tk.END)

        self.rr = StringVar()
        self.rrr = self.rr.get()
           
        if self.rrr == 'Nome Fantasia':
            self.rrr = 'Nome_Fantasia'
        if self.rrr == 'Poço':
            self.rrr = 'Data'
        if self.rrr == 'Tipo':
            self.rrr = 'Nome_Poco'
        if self.rrr == 'Local':
            self.rrr = 'Local'
        
        
        detect_pressed.filled = False
        self.auto = StringVar()
        try:
            self.chiefs = self.consultando('Nome_Fantasia') #ENTRADA INICIAL
        except:
            pass
       
        Label(self.aba1,text="Nome fantasia",bg=self.a,font = ('Helvetica', 9, 'bold'),fg='white').place(relx=0.02,rely=0.1)
        self.fantasia_entry = Entry(self.aba1,font = ('verdana', 8),justify="center",textvariable=self.auto)
        self.fantasia_entry.place(relx=0.18,rely=0.1)
        #self.fantasia_entry.focus_set()
        #self.fantasia_entry.bind('<KeyRelease>', get_typed)
        #self.fantasia_entry.bind('<Key>', detect_pressed)
        #-------------------------------------------------------FINAL DO AUTOCOMPLETE POR NOME----------------------------------------------
        
        Label(self.aba1,text="Data de recebimento",bg=self.a,font = ('Helvetica', 9, 'bold'),fg='white').place(relx=0.02,rely=0.18)
        self.data_entry = Entry(self.aba1,font = ('verdana', 8),justify="center")
        self.data_entry.place(relx=0.18,rely=0.18)
        
        Label(self.aba1,text="Poço",bg=self.a,font = ('Helvetica', 9, 'bold'),fg='white').place(relx=0.02,rely=0.26)
        self.poco_entry = Entry(self.aba1,font = ('verdana', 8),justify="center")
        self.poco_entry.place(relx=0.18,rely=0.26)
        

        Label(self.aba1,text="Tipo de amostra",bg=self.a,font = ('Helvetica', 9, 'bold'),fg='white').place(relx=0.02,rely=0.34)
        self.tipo_entry = Entry(self.aba1,font = ('verdana', 8),justify="center")
        self.tipo_entry.place(relx=0.18,rely=0.34)
        

        #Label(self.root,text="I",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.05,rely=0.24)
        
        Label(self.aba1,text="Informações extras",bg=self.a,font = ('Helvetica', 9, 'bold'),fg='white').place(relx=0.02,rely=0.42)
        self.textoa = scrolledtext.ScrolledText(self.aba1,bg='white',relief=GROOVE,height=60,width=40,font='TkFixedFont')
        self.textoa.place(relx=0.18,rely=0.42,relwidth= 0.2,relheight= 0.4)

        Label(self.aba1,text="Quantidade de recipientes",bg=self.a,font = ('Helvetica', 9, 'bold'),fg='white').place(relx=0.45,rely=0.04)
        Label(self.aba1,text="Peso (kgs)",bg=self.a,font = ('Helvetica', 9, 'bold'),fg='white').place(relx=0.4,rely=0.2)
        Label(self.aba1,text="Volume (L)",bg=self.a,font = ('Helvetica', 9, 'bold'),fg='white').place(relx=0.5,rely=0.2)
        Label(self.aba1,text="Local",bg=self.a,font = ('Helvetica', 9, 'bold'),fg='white').place(relx=0.6,rely=0.2)
        Label(self.aba1,text="Peso (kgs)",bg=self.a,font = ('Helvetica', 9, 'bold'),fg='white').place(relx=0.71,rely=0.2)
        Label(self.aba1,text="Volume (L)",bg=self.a,font = ('Helvetica', 9, 'bold'),fg='white').place(relx=0.81,rely=0.2)
        Label(self.aba1,text="Local",bg=self.a,font = ('Helvetica', 9, 'bold'),fg='white').place(relx=0.91,rely=0.2)

        #Botões -----------------------------------------------------------------------------------------------------------------------------------------------------
        Button(self.aba1,command=self.adicionars,text="Adicionar",width=8,font=('verdana',9,'bold')).place(relx=0.44,rely=0.11)
        Button(self.aba1,command=self.removers,text="Remover",width=8,font=('verdana',9,'bold')).place(relx=0.54,rely=0.11)
        Button(self.aba1,command=self.add_amostra,text="Cadastrar amostra",width=16,font=('verdana',9,'bold'),bg='blue',fg='white').place(relx=0.02,rely=0.6)
        Button(self.aba1,command=self.deleta_amostra,text="Remover amostra",width=16,font=('verdana',9,'bold'),bg='blue',fg='white').place(relx=0.02,rely=0.7)
        Button(self.aba1,command=self.altera_amostra,text="Alterar amostra",width=16,font=('verdana',9,'bold'),bg='blue',fg='white').place(relx=0.02,rely=0.8)
        Button(self.aba1,command=self.busca_amostra,text="Buscar amostra",width=16,font=('verdana',9,'bold'),bg='blue',fg='white').place(relx=0.02,rely=0.9)
        texto_balao_limpar = "Clique aqui para buscar amostra pelo seu nome fantasia"

        #entrada especial--------------------------------------------------------------------------------------------------------------------------------------------
        self.peso_am = StringVar()
        self.vol_am = StringVar()
        self.local_am = StringVar()
        
        self.e2 = Entry(self.aba1,font = ("verdana",8), width = 7,relief = "sunken",justify = 'center'
                                       ,textvariable = self.peso_am)
        self.e2.place(relx=0.405,rely=0.26 + 0.001)
        self.peso.append(self.peso_am)
        
        self.v2 = Entry(self.aba1,font = ("verdana",8), width = 7,relief = "sunken",justify = 'center'
                                       ,textvariable = self.vol_am)
        self.v2.place(relx=0.505,rely=0.26 + 0.001)
        self.vol.append(self.vol_am)

        self.a2 = Entry(self.aba1,font = ("verdana",8), width = 7,relief = "sunken",justify = 'center'
                                       ,textvariable = self.local_am)
        self.a2.place(relx=0.595,rely=0.26 + 0.001)
        self.local.append(self.local_am)


        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------Inserindo na aba2 - estatísticas----------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        Label(self.aba2,text="Contagem",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.02,rely=0.02)
        self.codigo_entry2 = Entry(self.aba2,font = ('verdana', 8),justify='center')
        self.codigo_entry2.place(relx=0.18,rely=0.02)
        self.codigo_entry2.insert(END,self.contagem)

        Label(self.aba2,text="Filtrar por",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.02,rely=0.1)
        self.rr = StringVar()
        self.met1 = ['Nome Fantasia','Tipo','Local']
        Spinbox(self.aba2,values=self.met1,justify = "center",textvariable=self.rr,command = self.evento).place(relx = 0.18,rely = 0.1,relwidth= 0.15) 
        Label(self.aba2,text="Nome fantasia",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.02,rely=0.18)
        self.f_entry = Entry(self.aba2,font = ('verdana', 8),justify="center",textvariable=self.auto)
        self.f_entry.place(relx=0.18,rely=0.18)
        self.f_entry.focus_set()
        #self.f_entry.bind('<Enter>',self.volume_parcial)
        self.f_entry.bind('<KeyRelease>', get_typed)
        self.f_entry.bind('<Key>', detect_pressed)
        Label(self.aba2,text="Volume total disponível (L)",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.02,rely=0.26)
        Label(self.aba2,text=self.volume_total(),bg=self.a,font = ('Helvetica', 11, 'bold'),fg='white').place(relx=0.24,rely=0.26)
        Label(self.aba2,text="Volume total da amostra (L)",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.02,rely=0.34)
        Label(self.aba2,text="Massa total da amostra (Kgs)",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.02,rely=0.42)
        Button(self.aba2,command=self.volume_parcial,text="Calcular",width=16,font=('verdana',9,'bold'),bg='blue',fg='white').place(relx=0.13,rely=0.6)

        self.tipo_graf = StringVar()
        self.tipo_graf2 = StringVar()
        self.met1 = ['5 Maiores Volumes por Nome','5 Maiores Volumes por Poço',
                     "5 Menores Volumes por Nome","Volumes acumulado por data","Volumes de amostra por ano de entrada"]
        Spinbox(self.aba2,values=self.met1,justify = "center",textvariable=self.tipo_graf,command = self.graficando).place(relx = 0.41,rely = 0.9,relwidth= 0.23)
        self.tipo_graf2 = StringVar()
        self.met2 = ['Volume acumulado por Tipo','Volume acumulado por Local',"Quantidade de amostra por Local",
                     "Proporção de Volume por Tipo","Proporção de Volume por Local"]
        Spinbox(self.aba2,values=self.met2,justify = "center",textvariable=self.tipo_graf2,command = self.graficando).place(relx = 0.74,rely = 0.9,relwidth= 0.23) 


        self.fig = Figure(figsize=(6.5,5.5),dpi=53)
        self.graf = self.fig.add_subplot(111)
        self.fig2 = Figure(figsize=(6.5,5.5),dpi=53)
        self.graf2 = self.fig2.add_subplot(111)
        self.graficando()
        self.canvas = FigureCanvasTkAgg(self.fig,master=self.aba2)
        self.canvas.get_tk_widget().place(relx=0.66,rely=0.0)
        self.canvas.draw()
        self.canvas2 = FigureCanvasTkAgg(self.fig2,master=self.aba2)
        self.canvas2.get_tk_widget().place(relx=0.33,rely=0.0)
        self.canvas2.draw()

        
        
        
        #Button(self.aba2,command=self.busca_amostra,text="Buscar amostra",width=16,font=('verdana',9,'bold'),bg='blue',fg='white').place(relx=0.02,rely=0.9)
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def evento(self): #mudar lista de consulta para autocomplete a partir do spinbox  
        conn = sqlite3.connect("amostras.db")
        df = pd.read_sql_query("select * from amostras",conn)
        def match_string():
            hits = []
            got = self.auto.get()
            for item in self.chiefs:
                if item.startswith(got):
                    hits.append(item)
            return hits    

        def get_typed(event):
            if len(event.keysym) == 1:
                hits = match_string()
                show_hit(hits)

        def show_hit(lst):
            if len(lst) == 1:
                self.auto.set(lst[0])
                detect_pressed.filled = True

        def detect_pressed(event):    
            key = event.keysym
            if len(key) == 1 and detect_pressed.filled is True:
                pos = self.f_entry.index(tk.INSERT)
                self.f_entry.delete(self.pos, tk.END)
        detect_pressed.filled = False
        self.rrr = self.rr.get()
 
        if self.rrr == 'Nome Fantasia':
            self.rrr = 'Nome_Fantasia'
            self.chiefs = self.consultando(self.rrr)
            #print('self.chiefs',self.chiefs)
            Label(self.aba2, text=" ",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.02,rely=0.18,relwidth=0.12)
            Label(self.aba2,text="Nome fantasia",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.02,rely=0.18)
            self.auto = StringVar()
            self.f_entry = Entry(self.aba2,font = ('verdana', 8),justify="center",textvariable=self.auto)
            self.f_entry.place(relx=0.18,rely=0.18)
            self.f_entry.place(relx=0.18,rely=0.18)
            self.f_entry.bind('<KeyRelease>', get_typed)
            self.f_entry.bind('<Key>', detect_pressed)
        if self.rrr == 'Tipo':
            self.rrr = 'Nome_Poco'
            self.chiefs = self.consultando(self.rrr)
            self.auto = StringVar()
            Label(self.aba2, text=" ",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.02,rely=0.18,relwidth=0.12)
            Label(self.aba2,text="Tipo de amostra",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.02,rely=0.18)
            self.f_entry = Entry(self.aba2,font = ('verdana', 8),justify="center",textvariable=self.auto)
            self.f_entry.place(relx=0.18,rely=0.18)
            self.f_entry.bind('<KeyRelease>', get_typed)
            self.f_entry.bind('<Key>', detect_pressed)
        if self.rrr == 'Local':
            self.rrr = 'Local'
            self.chiefs = self.consultando(self.rrr)
            self.auto = StringVar()
            Label(self.aba2, text=" ",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.02,rely=0.18,relwidth=0.12)
            Label(self.aba2,text="Local de amostra",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.02,rely=0.18)
            self.f_entry = Entry(self.aba2,font = ('verdana', 8),justify="center",textvariable=self.auto)
            self.f_entry.place(relx=0.18,rely=0.18)
            self.f_entry.bind('<KeyRelease>', get_typed)
            self.f_entry.bind('<Key>', detect_pressed)
        
    #------------------------------adicionando amostra -----------------------------------------------------------------------------------------------------------------   
    def adicionars(self):
        if self.qtd_cads <=300:
            self.peso_am = StringVar()
            self.vol_am = StringVar()
            self.local_am = StringVar()
            self.e1 = Entry(self.aba1,font = ("verdana",8), width = 7,relief = "sunken",justify = 'center'
                                   ,textvariable = self.peso_am)
            self.e1.place(relx=0.405,rely=0.26 + 0.0022*self.qtd_cads)
            self.peso.append(self.peso_am)
            self.v1 = Entry(self.aba1,font = ("verdana",8), width = 7,relief = "sunken",justify = 'center'
                                   ,textvariable = self.vol_am)
            self.v1.place(relx=0.505,rely=0.26 + 0.0022*self.qtd_cads)
            self.vol.append(self.vol_am)

            self.a1 = Entry(self.aba1,font = ("verdana",8), width = 7,relief = "sunken",justify = 'center'
                                       ,textvariable = self.local_am)
            self.a1.place(relx=0.595,rely=0.26 + 0.0022*self.qtd_cads)
            self.local.append(self.local_am)
            self.qtd_cads += 30

        if self.qtd_cads >300 and self.qtd_cads <= 630:
            self.peso_am = StringVar()
            self.vol_am = StringVar()
            self.local_am = StringVar()
            self.e1 = Entry(self.aba1,font = ("verdana",8), width = 7,relief = "sunken",justify = 'center'
                                   ,textvariable = self.peso_am)
            self.e1.place(relx=0.715,rely=0.26 + 0.0022*(self.qtd_cads-330))
            self.peso.append(self.peso_am)
            self.v1 = Entry(self.aba1,font = ("verdana",8), width = 7,relief = "sunken",justify = 'center'
                                   ,textvariable = self.vol_am)
            self.v1.place(relx=0.815,rely=0.26 + 0.0022*(self.qtd_cads-330))
            self.vol.append(self.vol_am)

            self.a1 = Entry(self.aba1,font = ("verdana",8), width = 7,relief = "sunken",justify = 'center'
                                       ,textvariable = self.local_am)
            self.a1.place(relx=0.905,rely=0.26 + 0.0022*(self.qtd_cads-330))
            self.local.append(self.local_am)
            
            self.qtd_cads += 30

    #------------------------------removendo amostra --------------------------------------------------------------------------------------------------------
    def removers(self):
        if self.qtd_cads >30:
            self.qtd_cads -= 30

            if len(self.peso)>0:
                if self.qtd_cads<=300:
                    del(self.peso[-1])
                    del(self.vol[-1])
                    del(self.local[-1])
                    Label(self.aba1,text = " ",bg = self.a,font = ("Arial",10), width = 10).place(relx=0.4,rely = 0.26 + 0.0022*self.qtd_cads)
                    Label(self.aba1,text = " ",bg = self.a,font = ("Arial",10), width = 10).place(relx=0.5,rely = 0.26 + 0.0022*self.qtd_cads)
                    Label(self.aba1,text = " ",bg = self.a,font = ("Arial",10), width = 10).place(relx=0.59,rely = 0.26 + 0.0022*self.qtd_cads)       
                if self.qtd_cads>300 and self.qtd_cads<=630:
                    del(self.peso[-1])
                    del(self.vol[-1])
                    del(self.local[-1])
                    Label(self.aba1,text = " ",bg = self.a,font = ("Arial",10), width = 10).place(relx=0.71,rely = 0.26 + 0.0022*(self.qtd_cads-330))
                    Label(self.aba1,text = " ",bg = self.a,font = ("Arial",10), width = 10).place(relx=0.81,rely = 0.26 + 0.0022*(self.qtd_cads-330))
                    Label(self.aba1,text = " ",bg = self.a,font = ("Arial",10), width = 8).place(relx=0.9,rely = 0.26 + 0.0022*(self.qtd_cads-330))
                    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------TABELA COM BANCO DE DADOS----------------------------------------------------------------
    def lista_frame2(self):
        #CRIANDO A TABELA
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica",10,"bold"),bg="blue",justify='center')
        self.listaCli = ttk.Treeview(self.frame2, height=2,
                                     column=("Codigo","Nome Fantasia","Data","Poço","Tipo","Peso","Volume","Local"),selectmode='browse')

        self.listaCli["columns"] = ("1", "2","3","4","5","6","7","8")
        self.listaCli['show'] = 'headings'
        self.listaCli.heading("#1", text="Codigo")
        self.listaCli.heading("#2", text="Nome Fantasia")
        self.listaCli.heading("#3", text="Data")
        self.listaCli.heading("#4", text="Poço")
        self.listaCli.heading("#5", text="Tipo")
        self.listaCli.heading("#6", text="Peso (kgs)")
        self.listaCli.heading("#7", text="Volume (L)")
        self.listaCli.heading("#8", text="Local")
       
        self.listaCli.column("#1", width=70, anchor='c')
        self.listaCli.column("#2", width=160, anchor='c')
        self.listaCli.column("#3", width=120, anchor='c')
        self.listaCli.column("#4", width=120, anchor='c')
        self.listaCli.column("#5", width=100, anchor='c')
        self.listaCli.column("#6", width=100, anchor='c')
        self.listaCli.column("#7", width=100, anchor='c')
        self.listaCli.column("#8", width=100, anchor='c')
        self.listaCli.place(relx=0.01, rely=0.05, relwidth=0.95, relheight=0.88)
        self.scroolLista = Scrollbar(self.frame2, orient='vertical',command=self.listaCli.yview)
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.05, relwidth=0.03, relheight=0.88)

        #VINCULANDO A TABELA AO CLICK DUPLO E FAZENDO A FUNÇÃO
        self.listaCli.bind('<Double-1>',self.OnDoubleClick) #determina que chama a função qdo interajo com a lista. No caso é um duplo clique

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)
        

        def Quit():
            self.root.destroy()

        menubar.add_cascade(label = "Opções", menu = filemenu) #menu dentro do filemenu
        menubar.add_cascade(label = "Relatórios", menu = filemenu2)
        

        filemenu.add_command(label="Sair",command = Quit) #opções dentro do file
        filemenu.add_command(label="Limpa Tela",command = self.limpa_amostra)
        
        filemenu2.add_command(label="Imprimir relatório",command = self.geraRelatAmostra)
        filemenu2.add_command(label="Download de cadastro de amostras",command = self.download_excel)
                
Principal()
