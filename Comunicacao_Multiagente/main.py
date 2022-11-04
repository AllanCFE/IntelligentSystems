# Comunicação Multiagente
# Allan Echeverria e Felipe Akerley

PASSWORD = ''
try:
   from secret import *
except ImportError:
   pass

from math import factorial
from multiprocessing.forkserver import set_forkserver_preload
import time
from xml.dom.minidom import TypeInfo
from kiwisolver import Solver
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
import random
import math


class SolverAgent(Agent):
    grauFuncao = 0 # salvar o grau da função que o Gerador retornar
    xEnviado = 0 # salvar o último X enviado 
    xTestados = [0] # salvar todos os X tentandos
    variavelA = 0 # responsável por armazenar o valor do primeiro termo da equação
    variavelB = 0 # resṕonsável por armazenar o valor do segundo termo da equação
    n_testes = 0 # responsável por armazenar o valor da quantidade de vezes que um valor de x foi testado.
    yRecebido = 0 # responsável por armazenar o valor de Y recebido pelo calculo no gerador.
    
    #Comportamento que pede o tipo da função ao Gerador e para
    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            msg = Message(to="laykere@jix.im")     # Instantiate the message
            msg.set_metadata("performative", "request")  # Set the "inform" FIPA performative
            msg.body = "Function type"                    # Set the message content

            await self.send(msg)
            print("Message sent!")

    # Comportamento que dá o primeiro palpite e para (a cíclica não dá o primeiro palpite)
    class FirstGuess(OneShotBehaviour):
        async def run(self):
            msg = Message(to="laykere@jix.im")
            msg.set_metadata("performative", "subscribe")
            msg.body = "0"

            await self.send(msg)
            print("GUESS sent!")

    # Comportamento que tenta um novo X até conseguir uma raiz
    class AwaitCalculation (CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            
            if msg:
                # Se recebe uma letra, reconhece que é o tipo da função e salva
                if 'u' == msg.body[len(msg.body)-1]:
                    SolverAgent.grauFuncao = int(msg.body[0])
                    print("Grau recebido: {}".format(SolverAgent.grauFuncao))
                
                # Se não é o tipo de função, valida o último palpite
                else:
                    #Para o Solver se achar 1 raiz
                    if int(format(msg.body)) == 0:
                        print("Uma das raízes é {}!".format(SolverAgent.xEnviado))
                        await SolverAgent.stop()
                    
                    print("Y = {}".format(msg.body))
                    SolverAgent.yRecebido = int(format(msg.body))
                    
                    # Pede um novo X pra função de achar o X
                    novoX = SolverAgent.resolvedor()
                    # Salva o X recebido na variável global
                    SolverAgent.xEnviado = novoX
                    
                    #Envia o novo palpite
                    msg = Message(to="laykere@jix.im")
                    msg.set_metadata("performative", "subscribe")
                    msg.body = str(novoX)

                    await self.send(msg)
                    print("GUESS sent: {}!".format(msg.body))
                    
                    SolverAgent.n_testes = SolverAgent.n_testes + 1
                    time.sleep(1)
                    
                    
            else:
                print("Not received response after 5s")

    # Função para achar o próximo X
    def resolvedor():
        SolverAgent.xTestados.append(SolverAgent.xEnviado)
        
        novoX = 0
        print(SolverAgent.grauFuncao)
        
        if(SolverAgent.grauFuncao == 1):
            
            if (SolverAgent.n_testes == 0):
                return 0
                
            if (SolverAgent.n_testes == 1):
                SolverAgent.variavelB = SolverAgent.yRecebido
                return 1
                
            if (SolverAgent.n_testes == 2):
                SolverAgent.variavelA = SolverAgent.yRecebido - SolverAgent.variavelB
                return int(-SolverAgent.variavelB/SolverAgent.variavelA)
           
        if(solverAgent.grauFuncao == 2):
            
            if (SolverAgent.n_testes == 0):
                return 0
                
            if (SolverAgent.n_testes == 1):
                SolverAgent.variavelB = - SolverAgent.yRecebido
                return 1
                
            if (SolverAgent.n_testes == 2):
                SolverAgent.variavelA = SolverAgent.yRecebido + SolverAgent.variavelB
                return int(math.sqrt(SolverAgent.variavelB/SolverAgent.variavelA))
        
        if(solverAgent.grauFuncao == 3):
            
            if (SolverAgent.n_testes == 0):
                return 0
                
            if (SolverAgent.n_testes == 1):
                SolverAgent.variavelB =  -SolverAgent.yRecebido
                return 1  
            
            if (SolverAgent.n_testes == 2):
                SolverAgent.variavelA = SolverAgent.yRecebido + SolverAgent.variavelB
                return int((SolverAgent.variavelB/SolverAgent.variavelA)**(1/3) + 1)    
            
        
        while novoX in SolverAgent.xTestados:
            novoX = random.randint(-1000,1001)
            
        return novoX
        

    async def setup(self):
        print("SolverAgent started")
        # Configura o comportamento ciclico de palpite
        guessBehaviour = self.AwaitCalculation()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(guessBehaviour, template)
        
        
        # Pede o tipo da função
        requestTypeBehaviour = self.InformBehav()
        self.add_behaviour(requestTypeBehaviour)
        
        # Da o primeiro palpite
        shootFirstGuess = self.FirstGuess()
        self.add_behaviour(shootFirstGuess)

class GeneratorAgent(Agent):
    typeFunction = random.randint(1,3) # Define o tipo de função
    # indexes = [] # Salva as raizes
    constantA = 0
    constantB = 0
    variableX = 0
    
    # Responde o tipo da função
    class TypeRequest(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            if msg:
                r_msg = Message(to= format(msg.sender))     # Instantiate the message
                r_msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                r_msg.body = format(GeneratorAgent.typeFunction)+"grau" # Set the message content
                await self.send(r_msg)
            else:
                print("Did not received any message after 10 seconds")
    
    # Gera as raízes da função de forma aleatória
    def generateFunction (self):        
        if(GeneratorAgent.typeFunction == 1):
            GeneratorAgent.variableX = random.randint(-1000, 1000)
            GeneratorAgent.constantA = random.randint(-100,100)
            GeneratorAgent.constantB = -1*(GeneratorAgent.constantA*GeneratorAgent.variableX)
            print("Equação gerada = ", GeneratorAgent.constantA, "x", GeneratorAgent.constantB)
            
        if(GeneratorAgent.typeFunction == 2):
            GeneratorAgent.variableX = random.randint(-1000,1000)
            GeneratorAgent.constantA = random.randint(-10, 10)
            GeneratorAgent.constantB = -1*(GeneratorAgent.constantA*GeneratorAgent.variableX*GeneratorAgent.variableX)
            print("Equação gerada = ", GeneratorAgent.constantA, "x²", GeneratorAgent.constantB)
            
        if(GeneratorAgent.typeFunction == 3):
            GeneratorAgent.variableX = random.randint(0, 100)
            GeneratorAgent.constantA = random.randint(-10,10)
            GeneratorAgent.constantB = -1*(GeneratorAgent.constantA*GeneratorAgent.variableX*GeneratorAgent.variableX*GeneratorAgent.variableX)
            
            print("Equação gerada = ", GeneratorAgent.constantA,"x³", GeneratorAgent.constantB)
            
    # Retorna ao Solver o resultado de Y com X recebido aplicado
    class ReturnY(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            
            # Variaveis que vao guardar o retorno e o X recebido
            response = 1
            entry = 0
            
            if msg:
                entry = int(format(msg.body))
                
                # Calcula Y
                # for raiz in GeneratorAgent.indexes:
                #     response = response * (entry - raiz)
                
                # Calcula Y com base no grau da função
                if(GeneratorAgent.typeFunction==1):
                    response = GeneratorAgent.constantA*entry + GeneratorAgent.constantB
                
                if(GeneratorAgent.typeFunction==2):
                    response = GeneratorAgent.constantA*entry*entry + GeneratorAgent.constantB
                
                if(GeneratorAgent.typeFunction==3):
                    response = GeneratorAgent.constantA*entry*entry*entry + GeneratorAgent.constantB
                
                # Retorna ao Solver
                r_msg = Message(to=format(msg.sender))
                r_msg.set_metadata("performative","inform")
                r_msg.body = format(response)
                
                await self.send(r_msg)
            else:
                print("To parado")

    async def setup(self):
        print("GeneratorAgent started")
        #Configura o comportamento que retorna o tipo de função
        b = self.TypeRequest()
        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(b, template)
        
        #Configura o comportamento que retorna o valor de Y
        rY = self.ReturnY()
        tY = Template()
        tY.set_metadata("performative","subscribe")
        self.add_behaviour(rY, tY)
        
        self.generateFunction()



if __name__ == "__main__":
    generatoragent = GeneratorAgent("laykere@jix.im", PASSWORD)
    future = generatoragent.start()
    future.result() # wait for receiver agent to be prepared.
    solverAgent = SolverAgent("hydrobr@jix.im", PASSWORD)
    solverAgent.start()

    while generatoragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            solverAgent.stop()
            generatoragent.stop()
            break
    print("Agents finished")