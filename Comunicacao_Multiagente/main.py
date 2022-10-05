PASSWORD = ''
try:
   from secret import *
except ImportError:
   pass

import time
from xml.dom.minidom import TypeInfo
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.message import Message
from spade.template import Template
import random


class SolverAgent(Agent):
    class InformBehav(OneShotBehaviour):
        async def run(self):
            print("InformBehav running")
            msg = Message(to="laykere@jix.im")     # Instantiate the message
            msg.set_metadata("performative", "request")  # Set the "inform" FIPA performative
            msg.body = "Function type"                    # Set the message content

            await self.send(msg)
            print("Message sent!")

            # stop agent from behaviour
            await self.agent.stop()

    async def setup(self):
        print("SolverAgent started")
        b = self.InformBehav()
        self.add_behaviour(b)

class GeneratorAgent(Agent):
    
    typeFunction = random.randint(1,3)
    indexes = []
    class TypeRequest(CyclicBehaviour):
        async def run(self):
            print("TypeRequest running")

            msg = await self.receive(timeout=5) # wait for a message for 10 seconds
            if msg:
                #print("Message received with content: {}".format(msg.body))
                if msg.body == "Function type":
                    r_msg = Message(to= format(msg.sender))     # Instantiate the message
                    r_msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
                    r_msg.body = format(GeneratorAgent.typeFunction)+"grau" # Set the message content

                    await self.send(r_msg)
                else:
                    print('b')
            else:
                print("Did not received any message after 10 seconds")

            # stop agent from behaviour
            #await self.agent.stop()
    
    def generateFunction (self):        
        for x in range(self.typeFunction):
            self.indexes.append(random.randint(-1000,1001))

    async def setup(self):
        print("GeneratorAgent started")
        b = self.TypeRequest()
        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(b, template)
        
        #print(self.typeFunction)
        
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