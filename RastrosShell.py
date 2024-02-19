# -*- coding:utf-8 -*-

from cmd import *
from RastrosWindow import RastrosWindow
from RastrosEngine import RastrosEngine

'''
Grupo 7:
    - Ana Rita Pires A95378
    - Hugo Miguel Lopes A96149
    - Rúben Filipe Ganança A95268
'''

class RastrosShell(Cmd):
    intro = 'Interpretador de comandos para o Rastros. Escrever help ou ? para listar os comandos disponíveis.\n'
    prompt = 'Rastros> '
                               
    def do_jogar(self, arg):
        " -  comando jogar que leva como parâmetro o nome de um ficheiro e carrega o tabuleiro permitindo jogá-lo..: jogar <nome_ficheiro> \n" 
        try:
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 1:
                eng.ler_tabuleiro_ficheiro(lista_arg[0])
                eng.print_tab_estado()
            else:
                print("Número de argumentos inválido!")
        except:
            print("Erro: ao mostrar o puzzle")
            
    def do_gravar(self, arg):
        " - comando gravar que leva como parâmetro o nome de um ficheiro e permite gravar o estado do jogo atual..: gravar <nome_ficheiro>  \n"
        try:
            #verificação do número de argumentos.
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 1:
                #Chama a função que se encontra no RastrosEngine responsável por gravar o estado do jogo num ficheiro.
                #Quando esta função é chamada grava também todos os movimentos já feitos.
                #Foi implementado como tendo dois argumentos em baixo para o caso do jogador se enganar e ao chamar a função tenha posto um argumento.
                posições = self.do_movs("0 0")
                eng.gravartabuleiro(posições)
            else:
                print("Número de argumentos inválido!!")
        except Exception as f:print(f)
            #print("Erro ao gravar!")
    
    def do_coord(self, arg):    
        " - comando coordenada que leva como parâmetros a coluna e a linha de uma casa onde se pretende jogar..: <c><l>  \n"
        try:
            #variáveis globais e veificação do número e argumentos.
            lista_arg = arg.split()
            num_args = len(lista_arg) 
            if num_args == 2:
                coluna_let=str(arg[0])
                linha=int(arg[2])
                letras={"a":1, "b":2, "c":3, "d":4, "e":5, "f":6, "g":7, "h":8}
                #numero={1:"a", 2:"b", 3:"c", 4:"d", 5:"e", 6:"f", 7:"g", 8:"h"}
                coluna_descodificada=(letras[coluna_let])
             
                try:
                    M=eng.gettab_estado()
                    coluna=int(coluna_descodificada)
                    indexcoluna = coluna -1 #O índice das colunas é igual ao número da coluna que as representa -1 (o índice de "a" que é a primeira coluna é 0 e assim por diante...)
                    indexlinha = 8-linha #O índice das linhas está ao contrário da ordem pela qual estão apresentadas, isto é, o "8" tem índice 0 e o "1" tem índice 7 
                    isblock = False #Variável criada para validar se a casa para onde pediu para jogar está bloqueada ou não.
                    player = eng.getjogador() #Variável que guarda numa string o jogador que pediu esta jogada
                    t = 0
                    countL = len(BloquedPlaces)
                    #Ciclo for que apartir da lista de casas bloqueadas avalia se a jogada é possível ou não.
                    for t in range(countL):
                        if(BloquedPlaces[t][0] == str(indexcoluna)) and (BloquedPlaces[t][1]==str(indexlinha)):
                            isblock = True
                        t +=1
                    
                    #Manda uma mensagem de impossibilidade de jogar porque a casa está bloqueada 
                    if(isblock == True):
                        print("Esta casa já foi bloqueada!") 
                        
                        
                    #Manda uma mensagem a informar que a peça está  nessa mesma casa  
                    elif(lastmove[0] == (str(indexcoluna)+str(indexlinha))):
                        print("Está a jogar para a casa onde a peça se encontra!") 
                        
                    #Se a peça for mandada para a casa assinalada por "1", dependendo do jogador que fez a jogada, esse jogador perdeu ou ganhou e o jogo acabou.
                    elif(indexcoluna == 0 and indexlinha == 7):   
                        if(player == 2):
                            print("O jogador 2 perdeu o jogo! Parabéns jogador 1!")
                            self.do_sair("sair")
                        else:
                            print("Parabéns o jogador 1 ganhou!") 
                            eng.movimentos_tab_estado((str(coluna_let)+ " " +str(linha)))
                            self.do_sair("sair")
                            
                    #Se a peça for mandada para a casa assinalada por "2", dependendo do jogador que fez a jogada, esse jogador perdeu ou ganhou e o jogo acabou.                     
                    elif(indexcoluna == 7 and indexlinha == 0):
                        if(player == 1):
                            print("O jogador 1 perdeu o jogo! Parabéns jogador 2!") 
                            self.do_sair("sair")
                        else:
                            print("Parabéns o jogador 2 ganhou!") 
                            eng.movimentos_tab_estado((str(coluna_let)+ " " +str(linha)))
                            self.do_sair("sair")
                            
                    #Avalia se todas as casas à volta da peça estão bloqueadas ou não e em caso afirmativo, o jogo termina e perde o jogador que ficou sem jogadas possíveis.
                        ##feita função auxiliar para descobrir se todos à volta estão bloqueados do_validate_neighbors
                    elif(self.do_validate_neighbors() == True):
                        if(player == 1):
                            print("O Jogador 1 perdeu o jogo. Não há casas livres!") 
                            self.do_sair("sair")
                        else:
                            print("O Jogador 2 perdeu o jogo. Não há casas livres!") 
                            self.do_sair("sair")
                            
                    #se não entrar em nenhuma validação inicial que impeça o jogo
                    else:
                        
                        #validar que as coordenadas estão dentro do tabuleiro
                        if(indexlinha < 8 and indexlinha >= 0 and indexcoluna < 8 and indexcoluna >= 0):
                            #ir buscar o tabuleiro ao RastrosEngine com o qual se pretende jogar
                            M=eng.gettab_estado()
                            # ciclo que percorrerá todas as linhas do tabuleiro para, em cada uma delas, fazer a gestão de elementos("." "*" "#")
                            i = 0
                            for i in range(8):
                                line = M[i][0]
                                #valida se a linha que estamos a ler é a linha para onde o jogador quer mudar a peça
                                if(i == indexlinha): 
                                    #descobrir se a peça já se encontrava nesta linha. Se sim, retorna a coluna.
                                    index = line.find('*')
                                    
                                    result = ""  #representa a linha no final da gestão
                                    
                                    #ciclo que percorrerá as colunas da linha em que estamos para atribuir os valores à linha
                                    #grosso modo este ciclo percorre as colunas da linha "line"
                                    y = 0 
                                    for y in range(8):
                                        
                                        #se a coluna a ser lida da linha for a mesma onde previamente encontramos a peça - Bloquear a casa
                                        if(y == index):
                                            result = result + "#"
                                            
                                            #converter a casa anterior da peça de forma a armazenar na lista das casas bloqueadas
                                            bloqueado=str(y)+str(i)
                                            BloquedPlaces.append(bloqueado)
                                        #se a coluna a ser lida da linha for a coluna para onde o jogador pediu que a peça fosse movimentada - Colocar a peça
                                        elif(y == indexcoluna):
                                            #Quando o valor do i e do y forem correspondentes aos das coordenadas da linha e coluna respectivamente, mudar a peça de posição: o "." passa a "*"
                                            result = result +  "*"
                                            #uma vez havendo alteração de posição. Guardar a nova posição da peça
                                            eng.movimentos_tab_estado((str(coluna_let)+ " " +str(linha)))
                                           
                                            #A lista fica sempre com um elemento que é o movimento feito na jogada mais recente e sempre que é feita uma nova jogada esse elemento sai para dar lugar à jogada mais recente.
                                            lastmove.pop()
                                            lastmove.append((str(indexcoluna)+str(indexlinha)))
                                            
                                        #Marcar no tabuleiro a casa "2" e "1"         
                                        elif(y == 7 and i == 0):
                                            result = result + "2"
                                        elif(y==0 and i == 7):
                                            result = result + "1"
                                       #se a coluna nao for a pretendida pelo jogador nem a respresentante do "2" e do "1"
                                       #Validar se é uma casa bloqueada (colocar "#") ou nao (colocar ".")
                                        else:
                                            #variavel para guardar valor do bloqueio da casa (True - bloqueada ; False - livre)
                                            isblocked = False
                                            #ciclo que percorre todas as casas bloqueadas
                                            p=0
                                            for p in range(countL):
                                                if(BloquedPlaces[p][0] == str(y)) and (BloquedPlaces[p][1]==str(i)):
                                                      isblocked=True      
                                                p +=1
                                            #acrescentar à linha, nesta coluna o valor certo com base no isblocked
                                            if(isblocked == True):
                                                result=result+ "#"
                                            else:
                                                result = result + "."
                                        y+=1        
                                    #Faz com que o tabuleiro se atualize de acordo com as mudanças que houve nas posições das peças e das casas bloqueadas.
                                    M[i][0]=result
                                
                                #se a linha que estamos a ler, não é a linha para onde o utilizador quer mandar a peça
                                else: 
                                    
                                   #descobrir se a peça já se encontrava nesta linha. Se sim, retorna a coluna.
                                    index = line.find('*')
                                    
                                    result = ""  #representa a linha no final da gestão
                                    
                                    #ciclo que percorrerá as colunas da linha em que estamos para atribuir os valores à linha
                                    #grosso modo este ciclo percorre as colunas da linha "line"
                                    y = 0 
                                    for y in range(8):
                                        #se a coluna a ser lida da linha for a mesma onde previamente encontramos a peça - Bloquear a casa
                                        if(y == index):
                                            result = result + "#"
                                            
                                            #converter a casa anterior da peça de forma a armazenar na lista das casas bloqueadas
                                            bloqueado=str(y)+str(i)
                                           
                                            BloquedPlaces.append(bloqueado)
                                       
                                        #Marcar no tabuleiro a casa "2" e "1"         
                                        elif(y == 7 and i == 0):
                                            result = result + "2"
                                        elif(y==0 and i == 7):
                                            result = result + "1"
                                        #se a coluna nao tinha a peça previamente nem é a respresentante do "2" e do "1"
                                        #Validar se é uma casa bloqueada (colocar "#") ou nao (colocar ".")
                                        else:
                                            #variavel para guardar valor do bloqueio da casa (True - bloqueada ; False - livre)
                                            isblocked = False
                                            #ciclo que percorre todas as casas bloqueadas
                                            p = 0
                                            for p in range(countL):
                                                if(BloquedPlaces[p][0] == str(y)) and (BloquedPlaces[p][1]==str(i)):
                                                      isblocked=True      
                                                p +=1
                                            #acrescentar à linha, nesta coluna o valor certo com base no isblocked
                                            if(isblocked == True):
                                                result=result+ "#"
                                            else:
                                                result = result + "."
                                    y+=1 #coluna seguinte
                                M[i][0]=result #Faz com que o tabuleiro se atualize de acordo com as mudanças que houve nas posições das peças e das casas bloqueadas
                                i+=1 #linha segunte
                                
                            #Gestão de jogadores Vai alternando entre os jogadores de forma a se saber quem joga de seguida.
                            player = eng.getjogador()
                            self.do_setjogador(player)
                            
                            #mostra o tabuleiro após a jogada
                            eng.print_tab_estado()
                            
                            #É feita novamente a validação após o jogador ter feito a jogada para verificar ora se as casas que rodeiam a peça estão livres (prossegue o jogo) ora se elas não estão (o jogo termina perdendo o jogador que não tem jogadas para fazer).  
                            if(self.do_validate_neighbors() == True):
                                if(player == 1):
                                    print("O Jogador 1 perdeu o jogo. Não há casas livres!") 
                                    self.do_sair("sair")
                                else:
                                    print("O Jogador 2 perdeu o jogo. Não há casas livres!") 
                                    self.do_sair("sair")
                                    
                           
                        #quando a coluna ou linha para a qual o jogador enviou a peça não está contida no tabuleiro    
                        else:
                            print("O tabuleiro não contém essa posição!")
                        
                except Exception as f: print(f) 
            #quando o numero de argumentos não é valido para o jogo
            else:
                print("Número de argumentos inválido! Por favor escreva coord [coluna] [linha]")        
        except Exception: print("Ups! Aqui há gato!")

                
    
    def do_jogada(self, arg):
        " - comando jogada que escolhe a melhor jogada para o jogador atual..: jogada  \n"

        
        #variáveis globais 
        #dicionarios necessários
        letras={"a":1, "b":2, "c":3, "d":4, "e":5, "f":6, "g":7, "h":8}
        numero={1:"a", 2:"b", 3:"c", 4:"d", 5:"e", 6:"f", 7:"g", 8:"h"}
        #descobrir posição da peça - ultima posição da lista de movimentos efetuados
        allmoves = eng.get_movimentos_tab()
        position = allmoves[-1]
        coluna = int(letras[position[0]]) -1 #O índice das colunas é igual ao número da coluna que as representa -1 (o índice de "a" que é a primeira coluna é 0 e assim por diante...)
        linha = 8 - int(position[2]) #O índice das linhas está ao contrário da ordem pela qual estão apresentadas, isto é, o "8" tem índice 0 e o "1" tem índice 7 
        #veificação do número de argumentos.
        lista_arg = arg.split()
        num_args = len(lista_arg) 
        
        if num_args == 0:
            #valores possiveis para colunas e linhas tendo por referencia a coluna e a linha em que a peça se encontra
            coluna_backward = coluna -1
            coluna_foward = coluna + 1
            linha_up = linha - 1
            linha_down = linha + 1
            #variaveis que serão avaliadas
            first = ""
            second = ""
            third = ""
            fourth = ""
            fifth = ""
            sixth = ""
            seventh = ""
            eighth = ""

            bestmove = "" #variavel onde será escrita a melhor jogada, se for descoberta
            #descobrir jogar que jogadorpediu a jogada
            player = eng.getjogador()
            
            #com base no jogador a ordem de preferencia das combinações possiveis altera. Pelo que aqui estão a ser preenchidas da melhor à pior opção. Para no fim dar a primeira válida
            if(player == "1"):
                #primeira escolha - linha desce e coluna recua
                if(coluna_backward >= 0 and coluna_backward < 8 and linha_down >= 0 and linha_down < 8 and coluna_backward != 7 and linha_down != 0):
                    first = str(coluna_backward)+str(linha_down)
                #segunda escolha - coluna inicial e linha desce
                if(coluna >= 0 and coluna < 8 and linha_down >= 0 and linha_down < 8 and coluna != 7 and linha_down != 0):
                    second = str(coluna)+str(linha_down)
                #terceira escolha - coluna recua e linha inicial
                if(coluna_backward >= 0 and coluna_backward < 8 and linha >= 0 and linha < 8 and coluna_backward != 7 and linha != 0):
                    third = str(coluna_backward)+str(linha)
                #quarta escolha - coluna avança e linha desce 
                if(coluna_foward >= 0 and coluna_foward < 8 and linha_down >= 0 and linha_down < 8 and coluna_foward != 7 and linha_down != 0):
                    fourth = str(coluna_foward)+str(linha_down)  
                #quinta escolha - coluna avança e linha inicial
                if(coluna_foward >= 0 and coluna_foward < 8 and coluna_foward != 7 and linha != 0):
                    fifth = str(coluna_foward)+str(linha)
                #sexta escolha - coluna recua e linha sobe
                if(coluna_backward >= 0 and coluna_backward < 8 and linha_up >= 0 and linha_up < 8 and coluna_backward != 7 and linha_up != 0):
                    sixth = str(coluna_backward)+str(linha_up)
                #setima escolha - coluna inicial e linha sobe
                if(linha_up >= 0 and linha_up < 8 and coluna != 7 and linha_up != 0):
                    seventh = str(coluna)+str(linha_up)
                #oitava escolha - coluna avança e sobe linha
                if(coluna_foward >= 0 and coluna_foward < 8 and linha_up >= 0 and linha_up < 8 and coluna_foward != 0 and linha_up != 7):
                    eighth = str(coluna_foward)+str(linha_up)
                
            elif(player == "2"):
                 #primeira escolha - coluna avança e sobe linha
                if(coluna_foward >= 0 and coluna_foward < 8 and linha_up >= 0 and linha_up < 8 and coluna_foward != 0 and linha_up != 7):
                    first = str(coluna_foward)+str(linha_up)
                #segunda escolha - coluna inicial e linha sobe
                if(linha_up >= 0 and linha_up < 8 and coluna != 0 and linha_up != 7):
                    second = str(coluna)+str(linha_up)
                #terceira escolha - coluna recua e linha sobe
                if(coluna_backward >= 0 and coluna_backward < 8 and linha_up >= 0 and linha_up < 8 and coluna_backward != 0 and linha_up != 7):
                    third = str(coluna_backward)+str(linha_up)
                #quarta escolha - coluna avança e linha inicial
                if(coluna_foward > 0 and coluna_foward < 8 and coluna_foward != 0 and linha != 7):
                    fourth = str(coluna_foward)+str(linha)
                #quinta escolha - coluna avança e linha desce 
                if(coluna_foward >= 0 and coluna_foward < 8 and linha_down >= 0 and linha_down <= 8 and coluna_foward != 0 and linha_down != 7):
                    fifth = str(coluna_foward)+str(linha_down)  
                #sexta escolha - coluna recua e linha inicial
                if(coluna_backward >= 0 and coluna_backward < 8 and linha >= 0 and linha < 8 and coluna_backward != 0 and linha != 7):
                    sixth = str(coluna_backward)+str(linha)
                #sétima escolha - coluna inicial e linha desce
                if(coluna >= 0 and coluna < 8 and linha_down >= 0 and linha_down < 8 and coluna != 0 and linha_down != 7):
                    seventh = str(coluna)+str(linha_down)
                #oitava escolha - linha desce e coluna recua
                if(coluna_backward >= 0 and coluna_backward < 8 and linha_down >= 0 and linha_down < 8 and coluna_backward != 0 and linha_down != 7):
                    eighth = str(coluna_backward)+str(linha_down)
            
          
            #verificar se alguma das opçoes está bloqueada
            #se estiver bloqueada limpa a hipotese
            i =0
            for i in range(len(BloquedPlaces)):
                if(first == BloquedPlaces[i]):
                    first = ""
                if(second == BloquedPlaces[i]):
                    second = ""
                if(third == BloquedPlaces[i]):
                    third = ""
                if(fourth == BloquedPlaces[i]):
                    fourth = ""
                if(fifth == BloquedPlaces[i]):
                    fifth = ""
                if(sixth == BloquedPlaces[i]):
                    sixth = ""
                if(seventh == BloquedPlaces[i]):
                    seventh = ""
                if(eighth == BloquedPlaces[i]):
                    eighth = ""
                i+=1
                
                
            #valores finais de coluna e linha a serem preenchidos
            coluna_final = ""
            linha_final = None 
            
            #descobrir qual a primeira variável preechida e válida porque será essa a melhor jogada encontrada
            if(first != ""):
              coluna_final = numero[int(first[0])+1]
              linha_final = int(8) - int(first[1])
            elif(second != ""):
              coluna_final = numero[int(second[0])+1]
              linha_final = int(8) - int(second[1])
            elif(third != ""):
              coluna_final = numero[int(third[0])+1]
              linha_final = int(8) - int(third[1])
            elif(fourth != ""):
              coluna_final = numero[int(fourth[0])+1]
              linha_final = int(8) - int(fourth[1])
            elif(fifth != ""):
              coluna_final = numero[int(fifth[0])+1]
              linha_final = int(8) - int(fifth[1])
            elif(sixth != ""):
              coluna_final = numero[int(sixth[0])+1]
              linha_final = int(8) - int(sixth[1])
            elif(seventh != ""):
              coluna_final = numero[int(seventh[0])+1]
              linha_final = int(8) - int(seventh[1])
            elif(eighth != ""):
              coluna_final = numero[int(eighth[0])+1]
              linha_final = int(8) - int(eighth[1])
              
            #mensagem a retornar com base nos valores finais de coluna e linha
            if(coluna_final != "" and linha_final != None):
               bestmove = str(coluna_final) + " " + str(linha_final)
               print("A melhor jogada encontrada foi: " + bestmove)
            else:
                print("Não é possível avançar para nenhuma casa. O Jogo Terminou!")
                self.do_sair("sair")
        #Se numero de argumentos for superior a 0
        else:
            print("Número de argumentos inválido!!")
        
    
    def do_pos(self, arg): 
        " - comando posição que leva como parâmetro o nº da jogada a visualizar..: pos <no.>  \n"
                
        #veificação do número e argumentos.
        lista_arg = arg.split()
        num_args = len(lista_arg) 
        if num_args == 1:
            #variaveis globais
            allmoves = eng.get_movimentos_tab() #Vai guardar todos os movimentos do tabuleiro já efetuados
            move = "" #variavel onde vai ser escrito o movimento pedido
            
            #descobrir index da jogada pedida uma vez que as jogadas começam a ser contadas a partir do 1 mas no ciclo for as contagens começam do 0.
            pos = int(arg) - 1  
            count = len(allmoves)  
            if(int(arg) > count):
                move = "Ainda não foi feita essa jogada"
            else:
                move = allmoves[pos] #Ao serem guardados os movimentos numa lista, a jogada que queremos consultar terá indice na lista igual à jogada -1, por exemplo, a jogada 1 estará nesta lista guardada no índice 0.
            
            print(move) #Print da jogada pretendida.
        #se numero de argumentos nao for válido
        else:
            print("Ups! Chegaram aqui coisas a menos ou a mais! É só uma!")
 
    def do_movs(self, arg):    
        " - comando movimentos que imprime a lista dos movimentos efetuados no jogo atual..: movs  \n"
        #variáveis globais e veificação do número e argumentos.
        lista_arg = arg.split()
        num_args = len(lista_arg) 
        
        #variaveis globais
        printm=""
        #guarda numa variável todos os movimentos já feitos e imprime-a
        allmoves = eng.get_movimentos_tab()
        #Variável local que tem a todo o momento a última jogada escrita.
        move = 0
        i = 0
        
        #Ciclo de for com a finalidade de organizar as jogadas que estão em lista, por jogada: jogador 1 | jogador 2
        for i in range(len(allmoves)):
            if(i == 0):
                move = 1
                printm = printm + "Jogada_1: " + allmoves[i]
            else:
                if(i%2==0): #se o index da lista for par significa que é do jogador 1. Necessário criar nova jogada
                    move +=1
                    printm = printm + "Jogada_"+str(move) +": " + allmoves[i]
                else: #se o index da lista for impar significa que é do jogador 2. Necessário adicionar a jogada do jogador 2 e fazer quebra de linha.
                    printm = printm + " | " + allmoves[i] + str("\n")
            i+=1
                    
        #Isto será chamado diretamente pelo jogador que irá mostrar-lhe todas as jogadas do jogo.
        if num_args == 0:
            print(printm)
        #Isto será o resultado da chamada feita pela função do_gravar para reutilizar e gravar no ficheiro todas as jogadas.
        elif num_args == 2:
            return printm
        else:
            print("Número de argumentos inválido!!")
    
    def do_bot(self, arg):    
        " - comando bot que leva com parâmetros o nome do ficheiro inicial e o nome do ficheiro final com a melhor jogada já eftuada..: bot <nome_ficheiro> <nome_ficheiro>  \n"
        pass

    def do_ver(self, arg):    
        " - Comando para visualizar o estado atual do tabuleiro em ambiente grafico caso seja válido: VER  \n"
        global janela  # pois pretendo atribuir um valor a um identificador global
        if janela is not None:
            del janela  # invoca o metodo destruidor de instancia __del__()
        janela = RastrosWindow(40) 
        janela.mostraJanela(eng.gettab_estado())        
        
    def do_sair(self, arg):
        "Sair do programa Rastros: sair"
        print('Obrigado por ter utilizado o Rastros. Espero que tenha sido divertido!')
        global janela  # pois pretendo atribuir um valor a um identificador global
        if janela is not None:
                    del janela  # invoca o metodo destruidor de instancia __del__()
        return True
    
    #Função criada para avaliar na vizinhança da peça branca as casas livres
    def do_validate_neighbors(self):
        #dicionarios necessários
        letras={"a":1, "b":2, "c":3, "d":4, "e":5, "f":6, "g":7, "h":8}
        
        #descbrir posiçao atual da peça
        allmoves = eng.get_movimentos_tab()
        #variaveis globais a preencher no final
        coluna_atual = ""
        linha_atual = None
        
        if(len(allmoves) > 0): #Se já tiverem sido feitas jogadas
            position = allmoves[-1] #última jogada efetuada
            coluna_atual = int(letras[position[0]]) -1
            linha_atual = 8 - int(position[2])
        #Se não houver ainda nenhuma jogada já feita, a casa considerada é a inicial.
        else: 
            coluna_atual = int(letras["e"]) -1
            linha_atual = 8 - int(5)
       
        #posições circundantes
        position1 = str(coluna_atual -1) + str(linha_atual + 1)
        position2 = str(coluna_atual) + str(linha_atual + 1)
        position3 = str(coluna_atual + 1) + str(linha_atual + 1)
        position4 = str(coluna_atual - 1) + str(linha_atual)
        position5 = str(coluna_atual + 1) + str(linha_atual)
        position6 = str(coluna_atual - 1) + str(linha_atual -1)
        position7 = str(coluna_atual) + str(linha_atual - 1)
        position8 = str(coluna_atual + 1) + str(linha_atual -1)
        
       
        #ciclo que percorre todas as casas bloqueadas e caso alguma delas seja uma das posições possíveis, limpa-as
        i=0
        for i in range(len(BloquedPlaces)):
            if(position1 == BloquedPlaces[i] or ("8" in position1)):
                position1 = ""
            if(position2 == BloquedPlaces[i] or ("8" in position2)):
                position2 = ""
            if(position3 == BloquedPlaces[i] or ("8" in position3)):
                position3 = ""
            if(position4 == BloquedPlaces[i] or ("8" in position4)):
                position4 = ""
            if(position5 == BloquedPlaces[i] or ("8" in position5)):
                position5 = ""
            if(position6 == BloquedPlaces[i] or ("8" in position6)):
                position6 = ""
            if(position7 == BloquedPlaces[i] or ("8" in position7)):
                position7 = ""
            if(position8 == BloquedPlaces[i] or ("8" in position8)):
                position8 = ""
            i+=1
            #se todas as posições circndantes possiveis estiverem bloqueadas, é devolvido True
        if(position1 == "" and position2 == "" and position3 == "" and position4 == "" and position5 == "" and position6 == "" and position7 == "" and position8 == ""):
            return True
        #caso haja pelo menos uma posição circundante lire devolve false
        else:
            return False
            
        
    def do_setjogador(self, player):
        
        #validação que alterna o jogador seguinte. Se jogador atual (player) for o um - altera-se para o 2 e vice-versa
        if(player == "1"):
            eng.setjogador("2")
        elif(player == "2"):
            eng.setjogador("1")
    
    
if __name__ == '__main__':
    eng = RastrosEngine()
    janela = None
    BloquedPlaces=[] #Lista vazia que é global e irá guardar as casas bloquadas.
    lastmove=['00'] #Lista que irá guardar a última jogada feita.
    sh = RastrosShell()
    sh.cmdloop()
    
