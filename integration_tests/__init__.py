import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import threading
from blockchain_server import BlockChain

class PyNaiveChainTestingThread(threading.Thread):

   def __init__(self, port):
       self.port = port
       threading.Thread.__init__(self, daemon=True)

   def start_naive_chain(self, port):
      self.bc = BlockChain(port)

   def run(self):
      self.start_naive_chain(self.port)

   def shutdown(self):
       #sys.exit(0)
       self._is_running = False
