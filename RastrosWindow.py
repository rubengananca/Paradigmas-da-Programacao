# -*- coding:utf-8 -*-

from graphics import *
from tkinter.constants import CENTER

class RastrosWindow:
    
    '''
    Classe que cria uma janela para vizualização grafica do estado do Rastros
    '''

    def __init__(self, cell_size, linhas=8, colunas=8):
        '''
        Cria nova instancia de RastrosWindow
        :param cell_size: tamanho da casa no ecra, em pixeis
        '''
        self.cell_size = cell_size
        self.nlinhas = linhas
        self.ncolunas = colunas
        self.puzzle = GraphWin("Rastros", self.nlinhas * self.cell_size + self.cell_size, self.ncolunas * self.cell_size + self.cell_size + self.cell_size)
        pass   
    
    def __del__(self):
        self.puzzle.close()  # fechar a janela    
    
    def desenhaCasa(self, coluna, linha):
        '''
        Desenha uma casa vazia 
        :param coluna: indice da coluna 
        :param linha: indice da linha
        '''
        p1 = Point(coluna * self.cell_size, linha * self.cell_size)
        p2 = Point(p1.getX() + self.cell_size, p1.getY() + self.cell_size)
        r = Rectangle(p1, p2)
        r.setFill("white")
        r.draw(self.puzzle)
        return r
                    
    def desenhaCasaPreta(self, coluna, linha):
        '''
        Desenha uma casa que ja foi jogada - peca preta 
        :param coluna: indice da coluna 
        :param linha: indice da linha
        '''
        p1 = Point(coluna * self.cell_size, linha * self.cell_size)
        p2 = Point(p1.getX() + self.cell_size, p1.getY() + self.cell_size)
        r = Rectangle(p1, p2)
        r.setFill("black")
        r.draw(self.puzzle)
        return r
        
    def desenhaCasaSimbolo(self, coluna, linha, char):
        '''
        Desenha uma casa que esteja bloqueada e contenha um numero
        :param coluna: indice da coluna 
        :param linha: indice da linha
        :param char: caracter numerico a inserir na casa bloqueada
        '''
        r = self.desenhaCasa(coluna, linha)  # aqui aproveitamos o retangulo que definimos para lhe colocar texto centrado
        label = Text(r.getCenter(), char)
        label.setTextColor("black")
        label.setStyle("bold")
        label.setSize(24)
        label.draw(self.puzzle)   
    
    def desenhaLinha(self, x1, y1, x2, y2, espessura, cor):
        '''
        Desenha uma linha
        :param x1: (x1,y1)
        :param y1: (x1,y1)
        :param x2: (x2,y2)
        :param x2: (x2,y2)
        '''    
        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        l = Line(p1, p2)
        l.setFill(cor)
        l.setWidth(espessura)
        l.draw(self.janela)
    
    def desenhaNumLinha(self, linha):
        '''
        Desenha os numeros das linhas e as linhas horizontais da grelha
        ''' 
        label = Text(Point(0 + self.cell_size / 2, linha * self.cell_size + self.cell_size / 2), str(linha))
        label.setTextColor("black")
        label.draw(self.puzzle)
        
    def desenhaNumerosDasLinhas(self, linha):
        '''
        Desenha os numeros das linhas e as linhas horizontais da grelha
        '''         
        numeros=['8','7','6','5','4','3','2','1']
        
        label = Text(Point(1 + self.cell_size / 2, (linha+0.5) * self.cell_size + self.cell_size / 2), numeros[linha])
        label.setTextColor("black")
        label.draw(self.puzzle)
    
    def desenhaLetrasDasColunas(self, coluna):
        '''
        Desenha as letras das colunas e as linhas verticais da grelha
        ''' 
        letras=['a','b','c','d','e','f','g','h']
                
        for i in range(1, coluna+1):
            label = Text(Point(i * self.cell_size + self.cell_size / 2 , coluna * self.cell_size + self.cell_size), letras[i-1])
            label.setTextColor("black")
            label.draw(self.puzzle)
    
    def mostraJanela(self, matriz):
        '''
        Percorre todo o puzzle, linha a linha e dentro de cada linha coluna a coluna, desenhando cada casa correspondente no puzzle
        '''
        try:
            self.puzzle.delete("all")
            linha = 0
            coluna = 0
            
            for line in matriz:
                for simbolo in line[0]:
                    self.desenhaNumerosDasLinhas(linha)
                    if simbolo == '.':
                        self.desenhaCasa(coluna + 1, linha + 0.5)
                    elif simbolo == '#':
                        self.desenhaCasaPreta(coluna + 1, linha + 0.5)
                    elif simbolo == '*':
                        self.desenhaCasaSimbolo(coluna + 1, linha + 0.5, 'O')
                    else:
                        self.desenhaCasaSimbolo(coluna + 1, linha + 0.5, simbolo)
                    coluna = coluna + 1
                coluna = 0
                linha = linha + 1
            self.desenhaLetrasDasColunas(self.ncolunas)
        except BaseException as e:
            print("erro ao desenhar:", e)
            return "NÃO"
        return "SIM"