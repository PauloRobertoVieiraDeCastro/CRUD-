from tkinter import *
import sqlite3
from tkinter import ttk
from tkinter import tix
from tkinter import messagebox
from tkinter import scrolledtext
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate
import webbrowser
from PIL import ImageTk, Image
import base64
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

class Funcionalidades(): #função CRUD

    def limpa_amostra(self):
        self.codigo_entry1.delete(0,END)
        self.codigo_entry2.delete(0,END)
        self.poco_entry.delete(0,END)
        self.fantasia_entry.delete(0,END)
        self.data_entry.delete(0,END)
        self.tipo_entry.delete(0,END)
        self.e2.delete(0,END)
        self.v2.delete(0,END)
        self.a2.delete(0,END)

        if self.qtd_cads >30:
            while(self.qtd_cads >30):
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
                
        
        try:
            self.df = self.consulta() 
            self.contagem = len(self.df['Nome_Fantasia'].unique())+1
            self.codigo_entry1.insert(END,self.contagem)
            self.codigo_entry2.insert(END,self.contagem)
            Label(self.aba2,text="  ",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.23,rely=0.34,relwidth=0.06)
            Label(self.aba2,text="  ",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.23,rely=0.42,relwidth=0.06)
            Label(self.aba2,text="   ",bg=self.a,font = ('Helvetica', 11, 'bold'),fg='white').place(relx=0.24,rely=0.26)
            Label(self.aba2,text=self.volume_total(),bg=self.a,font = ('Helvetica', 11, 'bold'),fg='white').place(relx=0.24,rely=0.26)
        except ValueError:
            self.contagem = 1
            self.codigo_entry1.insert(END,self.contagem)
            self.codigo_entry2.insert(END,self.contagem)
        #self.codigo_entry = Entry(self.root,font = ('verdana', 8),fg='white')
        #self.codigo_entry.place(relx=0.25,rely=0.04)
        #(self.root,text=self.contagem,bg=self.a,font = ('Helvetica', 14, 'bold'),fg='white').place(relx=0.31,rely=0.03)
        #self.textoa.delete(0,END)#APAGANDO OS ENTRIES
        

        
    def variaveis(self):
        self.poco1 = self.poco_entry.get()
        self.fantasia1 = self.fantasia_entry.get()
        self.data1 = self.data_entry.get()
        self.tipo1 = self.tipo_entry.get()
        self.volume1 = np.array([float(self.vol[i].get()) for i in range(len(self.vol))])
        self.peso1 = np.array([float(self.peso[i].get()) for i in range(len(self.peso))])
        self.local1 = np.array([self.local[i].get() for i in range(len(self.local))])
        
    def conecta_bd(self):
        self.conn = sqlite3.connect('amostras.db') #CONECTANDO O BANCO DE DADOS
        self.cursor = self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()

    def montaTabelas(self):
        self.conecta_bd();print('Conectando')
        ##criando a tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS amostras (
                Codigo TEXT PRIMARY KEY,
                Nome_Fantasia CHAR(50),
                Tipo CHAR(20),
                Data CHAR(20),
                Nome_Poco CHAR(50),
                Peso FLOAT,
                Volume FLOAT,
                Local CHAR(50)
            );
        """) #CRIA A TABELA, SE NÃO EXISTIR COM AS COLUNAS
        
        self.conn.commit(); print('Banco de dados criado') #valida o BD
        self.desconecta_bd()

    #------------------------------cadastro de amostra no banco de dados--------------------------------------------------------------------------------------------------------
    def add_amostra(self):
        print(self.variaveis())
        try:
            self.poco1 = self.poco_entry.get()
            self.fantasia1 = self.fantasia_entry.get()
            self.data1 = self.data_entry.get()
            self.tipo1 = self.tipo_entry.get()
            self.volume1 = np.array([float(self.vol[i].get()) for i in range(len(self.vol))])
            self.peso1 = np.array([float(self.peso[i].get()) for i in range(len(self.peso))])
            self.local1 = np.array([self.local[i].get() for i in range(len(self.local))])
            lista = []
            print(self.poco1)
            print(self.local1)
            cont = 64
            try:
                self.df = self.consulta() 
                self.contagem = len(self.df['Nome_Fantasia'].unique())+1
            except ValueError:
                self.contagem = 1
                
            for i in range(len(self.peso1)):
                cont+=1
                k = str(self.contagem)+chr(cont)
                lista.append([k,self.fantasia1,self.data1,self.poco1,self.tipo1,self.volume1[i],self.peso1[i],self.local1[i]])
                
            #self.add_amostra(lista)
            #chama o sqlite e conecta o bd
            self.y_add = messagebox.askyesno("Confirmação","Você realmente deseja adicionar a amostra")
            if self.y_add == True:
                self.conecta_bd()
                self.cursor.executemany(""" INSERT INTO amostras (Codigo, Nome_Fantasia, Tipo, Data, Nome_Poco, Peso, Volume, Local)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", lista)
                self.conn.commit()
                self.desconecta_bd()
                messagebox.showinfo('Cadastro de amostras','Cadastro feito com sucesso')
                self.select_lista()
                self.codigo_entry1.delete(0,END)
                self.codigo_entry2.delete(0,END)
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
                self.limpa_amostra()
                #self.codigo_entry.insert(END,self.contagem)
                self.contagem += 1
                
            else:
                pass
            
        except ValueError:
            messagebox.showinfo('Cadastro de amostras','Erro - Nem todos os campos foram preenchidos')    


    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT Codigo, Nome_Fantasia, Tipo, Data, Nome_Poco, Peso, Volume, Local FROM amostras; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()

    def altera_amostra(self):
        self.poco1 = self.poco_entry.get()
        self.fantasia1 = self.fantasia_entry.get()
        self.data1 = self.data_entry.get()
        self.tipo1 = self.tipo_entry.get()
        self.codigo = self.codigo_entry1.get()
        self.volume1 = np.array([float(self.vol[i].get()) for i in range(len(self.vol))])
        self.peso1 = np.array([float(self.peso[i].get()) for i in range(len(self.peso))])
        self.local1 = np.array([self.local[i].get() for i in range(len(self.local))])
        self.y_altera = messagebox.askyesno("Confirmação","Você realmente deseja alterar a amostra")
        if self.y_altera == True:
            self.conecta_bd()
            self.cursor.execute(""" UPDATE amostras SET Nome_Fantasia = ?, Tipo = ?, Data = ?, Nome_Poco = ?, Peso = ?, Volume = ?, Local = ?
            WHERE Codigo = ?""", (self.fantasia1, self.tipo1, self.data1, self.poco1, self.peso1[0], self.volume1[0], self.local1[0], self.codigo))
            self.conn.commit() #executa o comando
            self.desconecta_bd()
            self.select_lista()
            messagebox.showinfo('Cadastro de amostras','Alteração realizada com sucesso')
            self.codigo_entry1.delete(0,END)
            self.codigo_entry2.delete(0,END)

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
            self.limpa_amostra()
            
            #self.codigo_entry.insert(END,self.contagem)
        else:
            pass

    def busca_amostra(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())
        self.fantasia_entry.insert(END, '%') ##pega todos os caracteres
        nome = self.fantasia_entry.get()
        self.cursor.execute(
            """ SELECT Codigo, Nome_Fantasia, Tipo, Data, Nome_Poco, Peso, Volume, Local FROM amostras
            WHERE Nome_Fantasia LIKE '%s' """ % nome)
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", END, values=i)
        self.codigo_entry1.delete(0,END)
        self.codigo_entry2.delete(0,END)
        
        self.limpa_amostra()
        #self.codigo_entry.insert(END,self.contagem)
        self.desconecta_bd()

    def deleta_amostra(self):
        self.poco1 = self.poco_entry.get()
        self.fantasia1 = self.fantasia_entry.get()
        self.data1 = self.data_entry.get()
        self.tipo1 = self.tipo_entry.get()
        self.codigo = self.codigo_entry1.get()
        self.volume1 = np.array([float(self.vol[i].get()) for i in range(len(self.vol))])[0]
        self.peso1 = np.array([float(self.peso[i].get()) for i in range(len(self.peso))])[0]
        self.local1 = np.array([self.local[i].get() for i in range(len(self.local))])[0]
        self.y_deleta = messagebox.askyesno("Confirmação","Você realmente deseja excluir a amostra")
        if self.y_deleta == True:
            self.conecta_bd()
            self.cursor.execute(""" DELETE FROM amostras WHERE Codigo = ? AND Nome_Fantasia = ?""", (self.codigo,self.fantasia1))
            self.conn.commit()
            self.desconecta_bd()
            self.select_lista()
            messagebox.showinfo('Cadastro de amostras','Remoção de amostra realizada com sucesso')
            self.codigo_entry1.delete(0,END)
            self.codigo_entry2.delete(0,END)
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
            self.limpa_amostra()
            
            #self.codigo_entry.insert(END,self.contagem)
        else:
            pass
        

    def consulta(self):
        conn = sqlite3.connect("amostras.db")
        try:
            df = pd.read_sql_query("select * from amostras",conn)
            return df
        except ValueError:
            return None

    def OnDoubleClick(self, event): #o event indica ao Python um evento
        self.limpa_amostra() #limpa o que tiver
        self.listaCli.selection() ##seleciona os itens que eu der o duplo click
        for n in self.listaCli.selection():
            col1,col2,col3,col4,col5,col6,col7,col8 = self.listaCli.item(n, 'values')
            self.codigo_entry1.delete(0,END)
            #self.codigo_entry2.delete(0,END)
            self.codigo_entry1.insert(END, col1)
            #self.codigo_entry2.insert(END, col1)
            self.fantasia_entry.insert(END, col2)
            self.tipo_entry.insert(END,col3)
            self.data_entry.insert(END, col4)
            self.poco_entry.insert(END, col5)
            self.e2.delete(0,END)
            self.v2.delete(0,END)
            self.a2.delete(0,END)
            self.e2.insert(END, col6)
            self.v2.insert(END, col7)
            self.a2.insert(END, col8)

    def volume_total(self):
        conn = sqlite3.connect("amostras.db")
        try:
            df = pd.read_sql_query("select * from amostras",conn)
            return df['Volume'].sum()
        except:
            return 0

    def volume_parcial(self):
        conn = sqlite3.connect("amostras.db")
        try:
            df = pd.read_sql_query("select * from amostras",conn)
            e = self.f_entry.get()
            self.rrr = self.rr.get()
            
            if self.rrr == 'Nome Fantasia':
                self.rrr = 'Nome_Fantasia'
            if self.rrr == 'Poço':
                self.rrr = 'Data'
            if self.rrr == 'Tipo':
                self.rrr = 'Nome_Poco'
            if self.rrr == 'Local':
                self.rrr = 'Local'
            
            Label(self.aba2,text="  ",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.23,rely=0.34,relwidth=0.06)
            Label(self.aba2,text="  ",bg=self.a,font = ('Helvetica', 10, 'bold'),fg='white').place(relx=0.23,rely=0.42,relwidth=0.06)
            Label(self.aba2,text=df[df[self.rrr]==e]['Volume'].sum(),bg=self.a,font = ('Helvetica', 11, 'bold'),fg='white').place(relx=0.23,rely=0.34,relwidth=0.06)
            Label(self.aba2,text=df[df[self.rrr]==e]['Peso'].sum(),bg=self.a,font = ('Helvetica', 11, 'bold'),fg='white').place(relx=0.23,rely=0.42,relwidth=0.06)
            
        except ValueError:
            return None

    def consultando(self,nome):
        try:
            conn = sqlite3.connect("amostras.db")
            df = pd.read_sql_query("select * from amostras",conn)
            return list(df[nome].unique())
        except:
            return " "

    def download_excel(self):
        try:
            conn = sqlite3.connect("amostras.db")
            df = pd.read_sql_query("select * from amostras",conn)
            df.columns = ["Código","Nome Fantasia","Data","Poço","Tipo de amostra","Peso (Kgs)","Volume (L)","Local"]
            df.to_excel("Amostras_Cadastradas.xlsx")
            messagebox.showinfo('Cadastro de amostras','Download feito com sucesso.')
        except:
            messagebox.showinfo("Cadastro de amostras","Não há amostra cadastrada para exportar em formato .xlsx")

    def evento_grafico(self):
        self.tipo_g = self.tipo_graf.get()
        print(self.tipo_g)

    def evento_grafico2(self):
        self.tipo_g2 = self.tipo_graf2.get()
        print(self.tipo_g2)
        return self.tipo_g2
    
    def graficando(self):
        self.tipo_g1 = self.tipo_graf.get()
        self.tipo_g2 = self.tipo_graf2.get()
        try:
            
            conn = sqlite3.connect("amostras.db")
            df = pd.read_sql_query("select * from amostras",conn)
            
            tipo_amostra = df.groupby('Nome_Poco')['Volume'].sum()
            x = list(tipo_amostra.index)
            y = list(tipo_amostra.values)
            
            local_amostra = df.groupby('Local')['Volume'].sum()
            x1 = list(local_amostra.index)
            y1 = list(local_amostra.values)
            
            df['date'] = pd.to_datetime(df["Tipo"]).dt.to_period('D').dt.to_timestamp()
            dff = df.groupby('date')['Volume'].sum()
            cinco_vol_nome = df.groupby('Nome_Fantasia')['Volume'].sum().nlargest(5)
            cinco_poco_nome = df.groupby('Data')['Volume'].sum().nlargest(5)
            dff1 = df.copy()
            dff1['year'] = df['date'].dt.year
            dff1.sort_values(by='year',inplace=True)
            
            x2 = list(df.groupby('Nome_Fantasia')['Volume'].sum().nlargest(5).index)
            y2 = list(df.groupby('Nome_Fantasia')['Volume'].sum().nlargest(5))
            x3 = list(df.groupby('Data')['Volume'].sum().nlargest(5).index)
            y3 = list(df.groupby('Data')['Volume'].sum().nlargest(5))
            x4 = list(df.groupby('Nome_Fantasia')['Volume'].sum().nsmallest(5).index)
            y4 = list(df.groupby('Nome_Fantasia')['Volume'].sum().nsmallest(5))
            x5 = np.array(dff1.groupby('year')['Volume'].sum().nlargest(5).index)
            y5 = list(dff1.groupby('year')['Volume'].sum().nlargest(5))
            x55 = x5.astype(str)

            local_amostra_QT = df['Local'].value_counts()
            x6 = list(local_amostra_QT.index)
            y6 = list(local_amostra_QT.values)
            
            dfff = df[['date','Volume']].sort_values(by='date')
            
            dfff.set_index("date",inplace=True)
            dfff2 = pd.Series(dfff["Volume"]).cumsum()
        
            t = list(dfff2.index)#
            self.xq = [str(i).split(" ")[0] for i in t]
            yt = list(dfff2.values)
            
            
            
            ###-------------------------volume por tipo de amostra-------------------------------------------------
            if(self.tipo_g2 == "Volume acumulado por Tipo"):
                self.fig = Figure(figsize=(6.5,5.5),dpi=53)
                self.graf = self.fig.add_subplot(111)
                self.graf.set_title('Volume por tipo de amostra',fontsize=18,color='white')
                self.fig.patch.set_color('#6a5acd')
                self.graf.tick_params(axis='both', which='major', labelsize=11, colors='white')
                self.graf.xaxis.label.set_color('white')
                self.graf.yaxis.label.set_color('white')
                self.graf.bar(x,y,color='y')
                self.canvas = FigureCanvasTkAgg(self.fig,master=self.aba2)
                self.canvas.get_tk_widget().place(relx=0.66,rely=0.0)
                self.canvas.draw()
            if(self.tipo_g2 == "Volume acumulado por Local"):
                self.fig = Figure(figsize=(6.5,5.5),dpi=53)
                self.graf = self.fig.add_subplot(111)
                self.graf.set_title('Volume por local de amostra',fontsize=18,color='white')
                self.fig.patch.set_color('#6a5acd')
                self.graf.tick_params(axis='both', which='major', labelsize=11, colors='white')
                self.graf.xaxis.label.set_color('white')
                self.graf.yaxis.label.set_color('white')
                self.graf.bar(x1,y1,color='r')
                self.canvas = FigureCanvasTkAgg(self.fig,master=self.aba2)
                self.canvas.get_tk_widget().place(relx=0.66,rely=0.0)
                self.canvas.draw()
            if(self.tipo_g2 == "Quantidade de amostra por Local"):
                self.fig = Figure(figsize=(6.5,5.5),dpi=53)
                self.graf = self.fig.add_subplot(111)
                self.graf.set_title('Quantidade de amostra por Local',fontsize=18,color='white')
                self.fig.patch.set_color('#6a5acd')
                self.graf.tick_params(axis='both', which='major', labelsize=11, colors='white')
                self.graf.xaxis.label.set_color('white')
                self.graf.yaxis.label.set_color('white')
                self.graf.bar(x6,y6,color='r')
                self.canvas = FigureCanvasTkAgg(self.fig,master=self.aba2)
                self.canvas.get_tk_widget().place(relx=0.66,rely=0.0)
                self.canvas.draw()
            if(self.tipo_g2 == "Proporção de Volume por Local"):
                self.fig = Figure(figsize=(6.5,5.5),dpi=53)
                self.graf = self.fig.add_subplot(111)
                self.graf.set_title('Proporção de Volume por Local',fontsize=18,color='white')
                self.fig.patch.set_color('#6a5acd')
                self.colors = ["r","b","y","g","c","k"]
                self.graf.pie(y1,labels = x1, autopct='%1.1f%%',startangle=90,textprops={'fontsize': 11,'color':'w'},colors=self.colors)
                self.canvas = FigureCanvasTkAgg(self.fig,master=self.aba2)
                self.canvas.get_tk_widget().place(relx=0.66,rely=0.0)
                self.canvas.draw()
            if(self.tipo_g2 == "Proporção de Volume por Tipo"):
                self.fig = Figure(figsize=(6.5,5.5),dpi=53)
                self.graf = self.fig.add_subplot(111)
                self.graf.set_title('Proporção de Volume por Tipo',fontsize=18,color='white')
                self.fig.patch.set_color('#6a5acd')
                self.colors = ["r","b","y","g","c","k"]
                self.graf.pie(y,labels = x, autopct='%1.1f%%',startangle=90,textprops={'fontsize': 11,'color':'w'},colors=self.colors)
                self.canvas = FigureCanvasTkAgg(self.fig,master=self.aba2)
                self.canvas.get_tk_widget().place(relx=0.66,rely=0.0)
                self.canvas.draw()
            #---------------------------------------volume por nome fantasia----------------------------------------------------

            if(self.tipo_g1 == "5 Maiores Volumes por Nome"):
                self.fig2 = Figure(figsize=(6.5,5.5),dpi=53)
                self.graf2 = self.fig2.add_subplot(111)
                self.graf2.set_title('5 maiores volumes por Nome Fantasia',fontsize=18,color='white')
                self.fig2.patch.set_color('#6a5acd')
                self.graf2.bar(x2,y2)
                self.graf2.tick_params(axis='both', which='major', labelsize=11, colors='white')
                self.graf2.xaxis.label.set_color('white')
                self.graf2.yaxis.label.set_color('white')
                self.graf2.set_xticklabels(x2, rotation = 15)
                self.canvas2 = FigureCanvasTkAgg(self.fig2,master=self.aba2)
                self.canvas2.get_tk_widget().place(relx=0.33,rely=0.0)
                self.canvas2.draw()
            if(self.tipo_g1 == "5 Maiores Volumes por Poço"):
                self.fig2 = Figure(figsize=(6.5,5.5),dpi=53)
                self.graf2 = self.fig2.add_subplot(111)
                self.graf2.set_title('5 maiores volumes por Poço',fontsize=18,color='white')
                self.fig2.patch.set_color('#6a5acd')
                self.graf2.bar(x3,y3,color='g')
                self.graf2.tick_params(axis='both', which='major', labelsize=11, colors='white')
                self.graf2.xaxis.label.set_color('white')
                self.graf2.yaxis.label.set_color('white')
                self.graf2.set_xticklabels(x3, rotation = 15)
                self.canvas2 = FigureCanvasTkAgg(self.fig2,master=self.aba2)
                self.canvas2.get_tk_widget().place(relx=0.33,rely=0.0)
                self.canvas2.draw()
            if(self.tipo_g1 == "5 Menores Volumes por Nome"):
                self.fig2 = Figure(figsize=(6.5,5.5),dpi=53)
                self.graf2 = self.fig2.add_subplot(111)
                self.graf2.set_title('5 menores volumes por Nome',fontsize=18,color='white')
                self.fig2.patch.set_color('#6a5acd')
                self.graf2.bar(x4,y4,color='r')
                self.graf2.tick_params(axis='both', which='major', labelsize=11, colors='white')
                self.graf2.xaxis.label.set_color('white')
                self.graf2.yaxis.label.set_color('white')
                self.graf2.set_xticklabels(x4, rotation = 15)
                self.canvas2 = FigureCanvasTkAgg(self.fig2,master=self.aba2)
                self.canvas2.get_tk_widget().place(relx=0.33,rely=0.0)
                self.canvas2.draw()
            if(self.tipo_g1 == "Volumes acumulado por data"):
                self.fig2 = Figure(figsize=(6.5,5.5),dpi=53)
                self.graf2 = self.fig2.add_subplot(111)
                self.graf2.set_title("Volume acumulado por data",fontsize=18,color='white')
                self.fig2.patch.set_color('#6a5acd')
                self.graf2.plot(t,yt)
                self.graf2.tick_params(axis='both', which='major', labelsize=11, colors='white')
                self.graf2.xaxis.label.set_color('white')
                self.graf2.yaxis.label.set_color('white')
                self.graf2.set_xticklabels(self.xq, rotation = 15)
                self.canvas2 = FigureCanvasTkAgg(self.fig2,master=self.aba2)
                self.canvas2.get_tk_widget().place(relx=0.33,rely=0.0)
                self.canvas2.draw()
            if(self.tipo_g1 == "Volumes de amostra por ano de entrada"):
                self.fig2 = Figure(figsize=(6.5,5.5),dpi=53)
                self.graf2 = self.fig2.add_subplot(111)
                self.graf2.set_title("Volume de amostra por ano de entrada",fontsize=18,color='white')
                self.fig2.patch.set_color('#6a5acd')
                self.graf2.bar(x55,y5,color = 'c')
                self.graf2.tick_params(axis='both', which='major', labelsize=11, colors='white')
                self.graf2.xaxis.label.set_color('white')
                self.graf2.yaxis.label.set_color('white')
                self.graf2.set_xticklabels(x55, rotation = 15)
                self.canvas2 = FigureCanvasTkAgg(self.fig2,master=self.aba2)
                self.canvas2.get_tk_widget().place(relx=0.33,rely=0.0)
                self.canvas2.draw()

            #dff = df['Tipo'].dt.strftime("%d-%m-%y")
            self.conn.commit()
            self.desconecta_bd()
            return list(df[nome].unique())
        except:
            return " "
