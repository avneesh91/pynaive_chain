import asyncio
import websockets

from threading import Thread

class WebSocketServer(object):
    """
    class for running the websocket server for py_naive_chain
    """
    def __init__(self, port, chain_instance, *args, **kwargs):
        self.host = '0.0.0.0'
        self.port = port
        self.chain_instance = chain_instance
        self.websocket_loop = asyncio.new_event_loop()

    def start_websocket(self):
        self.executor_thread = Thread(target=self.__start_websocket__, args=())
        self.executor_thread.start()

    def __start_websocket__(self):
        execution_loop =asyncio.new_event_loop()
        start_server = websockets.serve(self.process_commands, self.host, self.port, loop=execution_loop)
        asyncio.set_event_loop(execution_loop)
        execution_loop.run_until_complete(start_server)
        execution_loop.run_forever()

        #asyncio.get_event_loop().run_until_complete(start_server)
        #asyncio.get_event_loop().run_forever()

    async def process_commands(self, websocket, path):
        command = await websocket.recv()
        response = self.chain_instance.process_command(command)
        await websocket.send(response)
        self.process_commands(websocket,path)
