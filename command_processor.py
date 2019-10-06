import json
import asyncio
import websockets
import websocket as websocket_client

from utils import get_logger, get_block
from block_data import Block

protocol_logger = get_logger('PROTOCOL_PROCESSOR')


class CommandProcessor(object):
  """
    Command process for the py_naive_chain
    This clas is responsbile for interpreting the incoming rpcs
    from other peers, and process them accordingly
    """

  def __init__(self, chain_instance, *args, **kwargs):
    """
        Init function for command processor
        """
    protocol_logger('Intializing protocol processor')
    self.chain_instance = chain_instance

  def command_processor(self, command_dict):
    """
        Function for processing the incoming commands
        from other nodes
        """
    current_command = command_dict.get('CMD')

    if current_command == 'PING':
      return {'CMD': 'PONG'}

    elif current_command == 'NEW_PEER_JOIN':
      peer_id = command_dict.get('peer_id')
      peer_host = command_dict.get('peer_host')
      port = command_dict.get('peer_port')
      protocol_logger('NEW_PEER_JOIN recieved from {} at {}:{}'.format(
          peer_id, peer_host, port))

      protocol_logger('Adding new peer with id {} at {}:{}'.format(
          peer_id, peer_host, port))
      self.add_new_peer(peer_id, peer_host, port)

      protocol_logger(
          'Peer added successfully. Initiating upload node data to remote peer')
      self.data_upload(peer_id)

    elif current_command == 'NEW_JOIN_DATA_UPLOAD':
      protocol_logger('NEW_PEER_JOIN_DATA_UPLOAD recieved')

      self.handle_data_upload(
          command_dict.get('peer_list'), command_dict.get('data_list'))

    elif current_command == 'ADD_PEER':

      peer_id = command_dict.get('peer_id')
      peer_host = command_dict.get('peer_host')
      port = command_dict.get('peer_port')
      protocol_logger('ADD_PEER recieved')

      self.add_new_peer(peer_id, peer_host, port)
      protocol_logger(
          'New peer {} at {}:{} added to peer list successfully'.format(
              peer_id, peer_host, port))

    elif current_command == 'VALIDATE_BLOCK':
      protocol_logger('VALIDATE_BLOCK recieved')
      block_data = command_dict.get('block_data')

      protocol_logger('Initiaiting block validation')
      if not self.chain_instance.validate_block(block_data):
        protocol_logger('Block validation failed')
        return 'KCA'

    elif current_command == 'ADD_BLOCK':
      protocol_logger('ADD_BLOCK recieved')
      block_data = command_dict.get('data')
      protocol_logger('Adding data block')
      self.chain_instance.add_block(block_data)
      protocol_logger('Block added successfully')

    return 'ACK'

  def add_new_peer(self, peer_id, peer_host, port):
    """
        Add a new pair to the network
        """
    protocol_logger('Invoking the block chain function for adding new peer')
    self.chain_instance.add_new_peer(peer_id, {'host': peer_host, 'port': port})

  def handle_data_upload(self, peer_list, data_list):
    protocol_logger('Saving data from remote peer')
    intro_dict = {
        'CMD': 'ADD_PEER',
        'peer_id': self.chain_instance.peer_id,
        'peer_host': '0.0.0.0',
        'peer_port': self.chain_instance.websocket_port
    }

    for peer in peer_list:
      self.add_new_peer(peer.get('peer'), peer.get('host'), peer.get('port'))

    self.write_to_peers([i.get('peer') for i in peer_list],
                        json.dumps(intro_dict))

    for block in data_list:
      block['data'] = block.get('data')
      protocol_logger("upload data recieved {}".format(block))
      self.chain_instance.insert_uploaded_block(get_block(**block))

  def data_upload(self, new_peer):
    peer_list = []
    data_list = []

    # send all the peers for the new peer to connect to
    for peer in self.chain_instance.get_peer_id_list():

      if peer == new_peer:
        continue

      curr_peer = self.chain_instance.get_peer(peer)
      peer_list.append({
          'peer': peer,
          'host': curr_peer.get('host'),
          'port': curr_peer.get('port')
      })

    data_list = [i.serialize() for i in self.chain_instance.get_block_data()]

    data_dict = {
        "CMD": "NEW_JOIN_DATA_UPLOAD",
        "peer_list": peer_list,
        "data_list": data_list
    }

    self.write_to_peers([new_peer], json.dumps(data_dict))

  def write_to_peers(self, peer_ids, data):
    """
        Function for writing data to peers
        """
    result_list = []
    for peer in peer_ids:
      curr_peer = self.chain_instance.get_peer(peer)
      peer_host = curr_peer.get('host')
      port = curr_peer.get('port')
      try:
        conn = websocket_client.create_connection(
            "ws://{}:{}".format(peer_host, port), timeout=10)
        conn.send(data)
        response = conn.recv()
        result_list.append(response)
      except websocket_client.WebSocketTimeoutException:
        self.chain_instance.remove_peer(peer)

    return result_list

  def get_peer_agreement(self, data):
    """
        Rudamentory consesous
        """
    peers = self.chain_instance.get_peer_id_list()
    total_count = len(peers)

    if total_count < 1:
      return True

    result_list = self.write_to_peers(peers, json.dumps(data))
    if not result_list.count('ACK') > total_count / 2:
      # motion not carried
      return False
    return True
