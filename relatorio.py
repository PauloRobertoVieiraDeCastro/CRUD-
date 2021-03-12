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
from reportlab.lib.utils import ImageReader
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import webbrowser
import PIL
import os
#from cStringIO import StringIO

import base64
import numpy as np

class GeraRelatorio():
    def printCliente(self):
        webbrowser.open("amostra.pdf") #abre o navegador com o pdf

    def geraRelatAmostra(self):
        self.c = canvas.Canvas("amostra.pdf")
        
        self.im = ImageReader('petro.png')
        #self.im = Image(self.logo)

        try:
            self.codigoRel = self.codigo_entry1.get()
            self.fantasiaRel = self.fantasia_entry.get()
            self.pocoRel = self.poco_entry.get()
            self.tipoRel = self.tipo_entry.get()
            self.dataRel = self.data_entry.get()
            self.volume1 = np.array([float(self.vol[i].get()) for i in range(len(self.vol))])
            self.peso1 = np.array([float(self.peso[i].get()) for i in range(len(self.peso))])
            self.local1 = np.array([self.local[i].get() for i in range(len(self.local))])
            self.c.setFont("Helvetica-Bold",24) #fonte do pdf
            self.c.drawString(200,790,"Amostra")
            #print(self.volume1[0])
            #o 200 cria um espaçamento da esquerda para a direita
            #o 790 de cima para baixo
            self.c.drawImage(self.im, 450,690,width=120,height=120)
            self.c.setFont("Helvetica-Bold",18) #fonte do pdf
            self.c.drawString(100,700,"Código:")
            self.c.drawString(100,665,"Nome Fantasia:")
            self.c.drawString(100,630,"Tipo de amostra:")
            self.c.drawString(100,595,"Data:")
            self.c.drawString(100,560,"Poço:")
            self.c.drawString(100,525,"Peso (Kgs):")
            self.c.drawString(100,490,"Volume (L):")
            self.c.drawString(100,455,"Local:")
            
            self.c.setFont("Helvetica-Bold",18) #fonte do pdf
            self.c.drawString(300,700,self.codigoRel)
            self.c.drawString(300,665,self.fantasiaRel)
            self.c.drawString(300,630,self.pocoRel)
            self.c.drawString(300,595,self.tipoRel)
            self.c.drawString(300,560,self.dataRel)
            self.c.drawString(300,525,str(self.peso1[0]))
            self.c.drawString(300,490,str(self.volume1[0]))
            self.c.drawString(300,455,str(self.local1[0]))
            #self.c.rect(20,720,550,200,fill=False, stroke=True) #cria uma borda
            
            
            self.c.showPage()
            self.c.save() #salva
            self.printCliente() #mostra no navegador
        except ValueError:
            messagebox.showinfo('Cadastro de amostras','Erro - Na aba Entrada de amostras, selecione sua amostra e solicite impressão.')
