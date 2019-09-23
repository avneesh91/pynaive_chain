import asyncio
import websockets

from utils import get_logger
from threading import Thread

rpc_logger = get_logger('RPC_SERVER')


class WebSocketServer(object):
  """
    class for running the websocket server for py_naive_chain
    """

  def __init__(self, port, chain_instance, *args, **kwargs):
    rpc_logger('Intializing RPC server')
    self.host = '0.0.0.0'
    self.port = port
    self.chain_instance = chain_instance
    self.websocket_loop = asyncio.new_event_loop()

  def start_websocket(self):
    rpc_logger('Starting RPC server on port {}:{}'.format(self.host, self.port))
    self.executor_thread = Thread(target=self.__start_websocket__, args=())
    self.executor_thread.start()
    rpc_logger('RPC server waiting for connections')

  def __start_websocket__(self):
    execution_loop = asyncio.new_event_loop()
    start_server = websockets.serve(
        self.process_commands, self.host, self.port, loop=execution_loop)
    asyncio.set_event_loop(execution_loop)
    execution_loop.run_until_complete(start_server)
    execution_loop.run_forever()

    #asyncio.get_event_loop().run_until_complete(start_server)
    #asyncio.get_event_loop().run_forever()

  async def process_commands(self, websocket, path):
    command = await websocket.recv()
    response = self.chain_instance.process_command(command)
    await websocket.send(response)
    self.process_commands(websocket, path)
