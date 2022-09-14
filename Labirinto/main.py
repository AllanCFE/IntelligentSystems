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
        #a = np.zeros((10,10), dtype=np.float64)
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
    def bfs(Labirinto, self):
        print ("Sistema de Execução BFS")
        s = []
        hold = 0
        while hold != 3:
            s.append = self.search(0, 0, self)
            print (s)
     
    def dfs(Labirinto, self):
        print ("Sistema de Execução DFS")
        s = []
        hold = 0
        #assumindo q o labirinto comece no 0,0
        while hold != 3:
            
            s.insert = self.search(0, 0, self)
            print (s)
            
    def walk(linha, coluna, self):
           print("Anda")
        
    def search(linha, coluna, self):
        print ("Posição encontrada na Linha ", linha+1, " e Coluna ", coluna+1, "\n")
        print (a[linha][coluna])
        
        cima = self.look_up(linha, coluna)
        esquerda = self.look_left(linha, coluna)
        baixo = self.look_down(linha, coluna)
        direita = self.look_right(linha, coluna)
                    
    def look_up(linha, coluna):
        #procura em cima
        if linha-1 < 0:
            print ("Atingiu a beirada de cima")
            return 1
        
        if a[linha-1][coluna] == 0:
            print ("Existe caminho em cima")
        
        return a[linha-1][coluna]
                   
    def look_left(linha, coluna):
        #procura na esquerda
        if coluna-1 < 0:
            print ("Atingiu a beirada da esquerda")
            return 1
            
        if a[linha][coluna-1] == 0:
            print ("Existe caminho na esquerda")
        
        return a[linha][coluna-1]
        
    def look_right(linha, coluna):
        #procura na direita
        if coluna+1 > 9:
            print ("Atingiu a beirada da direita")
            return 1
            
        if a[linha][coluna+1] == 0:
            print ("Existe caminho na direita")
            
        return a[linha][coluna+1]
        
    def look_down(linha, coluna):
        #procura embaixo
        if linha+1 > 9:
            print ("Atingiu a beirada de baixo")
            return
            
        if a[linha+1][coluna] == 0:
            print ("Existe caminho embaixo")
            
        return a[linha+1][coluna]
    

maze = Labirinto
maze.setUp_Map_1()

op = Operador
op.search(0, 0, op)

#testes
data = []
#data = maze.a[]