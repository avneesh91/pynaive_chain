import uuid
import json
import datetime

from block_data import Block
from utils import get_logger

from concurrent.futures import ThreadPoolExecutor
from websocket_server import WebSocketServer
from command_processor import CommandProcessor
from http_server import NaiveChainHTTPServer


bc_logger = get_logger('BLOCKCHAIN')

class BlockChain(object):
    """
    Blockchain server object using which will be responsible for starting the HTTP
    server as well adding more information to the blockchain
    """
    def __init__(self, websocket_port, *args, **kwargs):
        """
        Function for intializing the block chain server.
        Initializes the BlockChain as well as the HTTP
        server for interacting with the blockchain
        """
        bc_logger( 'Setting up naive chain server')
        self.peer_id = str(uuid.uuid4())
        self.age = datetime.datetime.now()
        self.websocket_port = websocket_port


        bc_logger( 'Intializing websocket RPC')
        self.initialize_blockhain_rpc()

        bc_logger( 'Intializing websocket RPC')

        bc_logger( 'Intializing protocol processing')
        self.protocol_processor = CommandProcessor(self)

        self.peer_list = []
        self.peer_connect_dict = {}

        self.block_data = []# replace with a thread safe implementation

        # will run this in the background as a future that never returns!!
        self.rpc_server.start_websocket()
        bc_logger('Node {} live on {}:{}'.format(self.peer_id, '0.0.0.0', self.websocket_port))

        if kwargs.get('existing_peer'):
            bc_logger( 'Peer Discovered')
            epeer_id = kwargs.get('peer_id')
            epeer_host = kwargs.get('peer_host')
            epeer_port = kwargs.get('peer_port')
            self.join_existing_peer_on_startup(epeer_id, epeer_host, epeer_port)
        else:
            bc_logger( 'No Peer Specified. Intializing genesis block for standalone operation')
            self.configure_genesis()

        # will block on this
        self.intialize_http_server()
        self.http_server.start_server()

    def validate_blockchain(self):
        import hashlib
        for i in range(len(self.block_data)):
            hasher = hashlib.sha256()

            if i == 0:
                # genesis block, continue as
                # is
                continue
            prev_hash = self.block_data[i-1].curr_hash
            current_block = self.block_data[i].data
            hasher.update(prev_hash.encode() + current_block.encode())
            current_hash = hasher.hexdigest()

            if current_hash != self.block_data[i].curr_hash:
                return False

        return True


    def join_existing_peer_on_startup(self,peer_id, host, port):
        """
        Send intialization request for data upload and
        connecting to other peers
        """
        bc_logger( 'Joining remote peer')
        self.protocol_processor.add_new_peer(peer_id, host, port)

        command_dict = {}
        command_dict['CMD'] = 'NEW_PEER_JOIN'
        command_dict['peer_id'] = self.peer_id
        command_dict['peer_host'] = '0.0.0.0'
        command_dict['peer_port'] = self.websocket_port

        bc_logger( 'Intializing data sync peer')
        self.protocol_processor.write_to_peers([peer_id], json.dumps(command_dict))

    def configure_genesis(self):
        """
        Class function for configuring gensis
        """
        genesis_block = Block(0, 'ioiiiuasyi891qbduquiuqwiqwiupwe', 'random')
        self.block_data.append(genesis_block)

    def create_sample_block_data(self, data):
        latest_block = self.block_data[-1]
        last_block = Block(latest_block.index+1, latest_block.curr_hash, data)
        return last_block


    def add_block(self, data):
        latest_block = self.block_data[-1]
        last_block = Block(latest_block.index+1, latest_block.curr_hash, data)
        self.block_data.append(last_block)
        return last_block

    def validate_block(self, block_data):
        recieved_block = Block(**block_data)
        latest_block = self.block_data[-1]
        compiled_block_data = Block(latest_block.index+ 1, latest_block.curr_hash, block_data.get('data'))
        return recieved_block == compiled_block_data

    def add_data(self, data):
        block = self.create_sample_block_data(data)
        self.protocol_processor.write_to_peers(self.peer_connect_dict.keys(), json.dumps({'CMD': 'ADD_BLOCK', 'data': data}))
        return self.protocol_processor.get_peer_agreement(block.serialize())

    def intialize_http_server(self):
        """
        Initialize the HTTP server for handling incoming
        requests from the user
        """
        self.http_server = NaiveChainHTTPServer(self, '0.0.0.0', self.websocket_port +1)


    def initialize_blockhain_rpc(self):
        """
        Intialize block chain using web sockets
        """
        # remote server for handling incoming requests
        self.rpc_server = WebSocketServer(self.websocket_port, self)

    def process_command(self, command):
        """
        Class function for processing any incoming commands from other peers
        or nodes
        """
        # get the command dict
        current_command = json.loads(command)
        return self.protocol_processor.command_processor(current_command)

    def process_data_upload(self, data):
        """
        Class function for replicating and pre-processing data
        before adding it to the nodes master records
        """
        #derp!!!
        return data
