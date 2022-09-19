#Algoritmo de Resolução de Labirinto
#
#allan
#EMB5617: Sistemas Inteligentes
#from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

a = np.zeros((10,10), dtype=np.int64)


class Labirinto(object):
    def setUp_Map_1():
        print ("Labirinto criado")
        a[0:5, 1:5] = 1
        a[1:7, 6:9] = 1
        a[6:7, 0:5] = 1
        a[8:9, 1:9] = 1
        a[7:8, 1:2] = 1
        a[3:5, 9:10] = 1
        a[0:1, 0:1] = 2
        a[7:8, 0:1] = 3
        print (a)
        print ("\n\n")

class Operador(object):
    
    def solver(tipo, self):
        #assumindo q o labirinto comece no 0,0
        s = [[0,0]]
        hold = 0
        
        while hold != 3:
            #Salva na variavel a posicao a ser analisada nesse ciclo
            posicao_atual = s.pop(0)
            
            #Encerra a busca caso estejamos no final do labirinto
            if a[posicao_atual[0]][posicao_atual[1]] == 3 :
                hold = 3
                continue
            
            resultados_busca = self.search(posicao_atual[0], posicao_atual[1], self)
            
            #Se nenhuma casa ao redor da atual for válida, parte para a próxima
            if len(resultados_busca) <= 0 :
                continue
            
            #Caso seja necessário adicionar casas para análise, verifica qual método utilizar
            for res_busca in resultados_busca:
                if tipo == "bfs":
                    s.append([res_busca[0], res_busca[1]])
                else:
                    s.insert(0, [res_busca[0], res_busca[1]])
            
            
            print (s)
        
    def search(linha, coluna, self):
        
        posicoes = []
        
        print ("\n", "Posição encontrada na Linha ", linha+1, " e Coluna ", coluna+1)
        print (a[linha][coluna])
        
        if self.look_up(linha, coluna) != 1:
            posicoes.append([linha-1,coluna])
        if self.look_left(linha, coluna) != 1:
            posicoes.append([linha,coluna-1])
        if self.look_down(linha, coluna) != 1:
            posicoes.append([linha+1,coluna])
        if self.look_right(linha, coluna) != 1:
            posicoes.append([linha,coluna+1])
        
        #Marca a casa atual como "Verificada", a não ser que seja a última
        if a[linha][coluna] != 3 :
            a[linha][coluna] = 4
        
        return posicoes
                    
    def look_up(linha, coluna):
        #procura em cima
        if linha-1 < 0 or a[linha-1][coluna] == 4:
            print ("Atingiu a beirada de cima")
            return 1
        
        if a[linha-1][coluna] == 0:
            print ("Existe caminho em cima")
        
        return a[linha-1][coluna]
                   
    def look_left(linha, coluna):
        #procura na esquerda
        if coluna-1 < 0 or a[linha][coluna-1] == 4:
            print ("Atingiu a beirada da esquerda")
            return 1
            
        if a[linha][coluna-1] == 0:
            print ("Existe caminho na esquerda")
        
        return a[linha][coluna-1]
        
    def look_right(linha, coluna):
        #procura na direita
        if coluna+1 > 9 or a[linha][coluna+1] == 4:
            print ("Atingiu a beirada da direita")
            return 1
            
        if a[linha][coluna+1] == 0:
            print ("Existe caminho na direita")
            
        return a[linha][coluna+1]
        
    def look_down(linha, coluna):
        #procura embaixo
        if linha+1 > 9 or a[linha+1][coluna] == 4:
            print ("Atingiu a beirada de baixo")
            return 1
            
        if a[linha+1][coluna] == 0:
            print ("Existe caminho embaixo")
            
        return a[linha+1][coluna]
    

maze = Labirinto
maze.setUp_Map_1()

op = Operador
op.solver("dfs", op)

print(a)

#testes
data = []
#data = maze.a[]