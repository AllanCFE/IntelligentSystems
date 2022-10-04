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


class SenderAgent(Agent):
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
        print("SenderAgent started")
        b = self.InformBehav()
        self.add_behaviour(b)

class ReceiverAgent(Agent):
    class TypeRequest(CyclicBehaviour):
        async def run(self):
            print("TypeRequest running")

            msg = await self.receive(timeout=5) # wait for a message for 10 seconds
            if msg:
                #print("Message received with content: {}".format(msg.body))
                if msg.body == "Function type":
                    print('a')
                else:
                    print('b')
            else:
                print("Did not received any message after 10 seconds")

            # stop agent from behaviour
            #await self.agent.stop()

    class ResponseType(OneShotBehaviour):
        async def run (senderUser, self):
            msg = Message(to=senderUser)     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "Type: " & self.typeFunction                    # Set the message content

            await self.send(msg)
            print("Type message sent!")

            # stop agent from behaviour
            await self.agent.stop()
    
    def generateFunction (self):
        self.indexes = []
        
        for x in range(self.typeFunction):
            self.indexes.append(random.randint(-1000,1001))

    async def setup(self):
        print("ReceiverAgent started")
        b = self.TypeRequest()
        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(b, template)
        
        self.typeFunction = random.randint(1,3)
        #print(self.typeFunction)
        
        self.generateFunction()
        #print(self.indexes)



if __name__ == "__main__":
    receiveragent = ReceiverAgent("laykere@jix.im", PASSWORD)
    future = receiveragent.start()
    future.result() # wait for receiver agent to be prepared.
    senderagent = SenderAgent("hydrobr@jix.im", PASSWORD)
    senderagent.start()

    while receiveragent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            senderagent.stop()
            receiveragent.stop()
            break
    print("Agents finished")