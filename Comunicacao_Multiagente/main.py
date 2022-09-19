from spade import agent, quit_spade

class DummyAgent(agent.Agent):
    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))

PASSWORD = ''
try:
   from secret import *
except ImportError:
   pass

dummy = DummyAgent("hydrobr@jix.im", PASSWORD)
future = dummy.start()
future.result()

dummy.stop()
quit_spade()