PASSWORD = ''
try:
   from secret import *
except ImportError:
   pass

import time
from xml.dom.minidom import TypeInfo
from kiwisolver import Solver
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
import random


class SolverAgent(Agent):
    grauFuncao = 0
    xEnviado = 0
    xTestados = [0]
    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            msg = Message(to="laykere@jix.im")     # Instantiate the message
            msg.set_metadata("performative", "request")  # Set the "inform" FIPA performative
            msg.body = "Function type"                    # Set the message content

            await self.send(msg)
            print("Message sent!")

    class FirstGuess(OneShotBehaviour):
        async def run(self):
            msg = Message(to="laykere@jix.im")
            msg.set_metadata("performative", "subscribe")
            msg.body = "0"

            await self.send(msg)
            print("GUESS sent!")

    class AwaitCalculation (CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            
            if msg:
                if 'u' == msg.body[len(msg.body)-1]:
                    SolverAgent.grauFuncao = msg.body[0]
                    print("Grau recebido: {}".format(SolverAgent.grauFuncao))
                else:
                    if int(format(msg.body)) == 0:
                        print("Uma das raízes é {}!".format(SolverAgent.xEnviado))
                        await SolverAgent.stop()
                    
                    print("Y = {}".format(msg.body))
                    
                    novoX = SolverAgent.resolvedor()
                    SolverAgent.xEnviado = novoX
                    
                    msg = Message(to="laykere@jix.im")
                    msg.set_metadata("performative", "subscribe")
                    msg.body = str(novoX)

                    await self.send(msg)
                    print("GUESS sent: {}!".format(msg.body))
                    
            else:
                print("Not received response after 5s")

    def resolvedor():
        SolverAgent.xTestados.append(SolverAgent.xEnviado)
        
        novoX = 0
        
        while novoX in SolverAgent.xTestados:
            novoX = random.randint(-10,11)
            
        return novoX
        

    async def setup(self):
        print("SolverAgent started")
        guessBehaviour = self.AwaitCalculation()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(guessBehaviour, template)
        
        requestTypeBehaviour = self.InformBehav()
        self.add_behaviour(requestTypeBehaviour)
        
        shootFirstGuess = self.FirstGuess()
        self.add_behaviour(shootFirstGuess)

class GeneratorAgent(Agent):
    
    typeFunction = random.randint(1,3)
    indexes = []
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
    
    def generateFunction (self):        
        for x in range(self.typeFunction):
            self.indexes.append(random.randint(-10,11))
        print(GeneratorAgent.indexes)

    class ReturnY(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10) # wait for a message for 10 seconds
            
            response = 1
            entry = 0
            if msg:
                entry = int(format(msg.body))
                for raiz in GeneratorAgent.indexes:
                    response = response * (entry - raiz)
                
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