# -*- coding:utf-8 -*-
'''
Grupo 7:
    - Ana Rita Pires A95378
    - Hugo Miguel Lopes A96149
    - Rúben Filipe Ganança A95268
'''
class RastrosEngine:
    
    def __init__(self):
        self.tab_jogo = [] #matriz que representa o tabuleiro de jogo original
        self.tab_estado = [] #matriz que representa o tabuleiro com o estado do jogo
        self.jogador= "1" 
        self.jogadas=[] #Foi criada uma lista que vai conter as jogadas realizadas no jogo

    def ler_tabuleiro_ficheiro(self, filename):
        '''
        Cria nova instancia do jogo numa matriz
        :param filename: nome do ficheiro a ler
        como o formato é fixo sabe-se o que contem cada linha
        '''
        try:
            ficheiro = open(filename, "r")
            lines = ficheiro.readlines() #ler as linhas do ficheiro para a lista lines
            self.tab_jogo=[]
            for i in range(0,8): #as linhas 0 a 7 contêm o tabuleiro de jogo
                self.tab_jogo.append(lines[i].split())
            self.tab_estado=[]
            for i in range(0,8): #as linhas 0 a 7 contêm o tabuleiro de jogo
                self.tab_estado.append(lines[i].split())
            estado=True
        except:
            print("Erro: na leitura do tabuleiro")
            estado=False
        else:
            ficheiro.close()
        return estado
      
    def print_tab_estado(self):
        
        numeros=['8','7','6','5','4','3','2','1'] 
        i=0
        for linha in self.tab_estado:
            print(numeros[i],end=" ")
            i+=1
            for simbolo in linha:
                print(simbolo,end=" ")
            print()
        print("  a b c d e f g h")
        print("[Próximo a jogar: jogador %s]"%(self.jogador))

    def setjogador(self,jog):
        self.jogador=jog
    
    def getjogador(self):
        return self.jogador
    
    def gettab_estado(self):
        return self.tab_estado

    def settab_estado(self, t):
        self.tab_estado = t
      
    
        
    def gravartabuleiro(self,arg):
        try:
            #É criado um ficheiro para escrita com o nome de "estadotabuleiro.txt" 
            #Num ciclo de for, com o cumprimento de 8 (linhas do tabuleiro), vamos guardar no ficheiro linha a linha o estado do jogo
            #A variável h guarda o estado do jogo atual.
            #O x começa em 8 e vai descendo um valor a cada ciclo de for pois as listas no tabuleiro estão ordenadas de 8 a 1 (de forma decrescente).
           
            h=self.gettab_estado() 
            x=8        
                
            with open("estadotabuleiro.txt","w+") as f:  
                for i in range(len(h)):   
                    positi= str(h[i])
                    y=str(x)+str(positi)+str("\n")                                   
                    f.write(y)
                    x-=1
                #linha que representa as letras do tabuleiro (colunas)    
                k=str("  a b c d e f g h")
                f.write(k)
                #Por questão estética acrescentam-se duas linhas em branco e posteriormente são anexadas todas as jogadas.
                f.write(str("\n"))
                f.write(str("\n"))
                f.write(str(arg))
                f.close()               
                

        except Exception as e: print(e)
            
    def movimentos_tab_estado(self, j):
        #Função que à lista vazia inicial vai acrescentar as jogadas já feitas.
        self.jogadas.append(j)
        
    def get_movimentos_tab(self):
        #Função que retorna a lista das jogadas já feitas.
        return self.jogadas
        
    
          
 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        