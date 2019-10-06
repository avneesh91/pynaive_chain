from argparse import ArgumentParser
from blockchain_server import *

parser = ArgumentParser()
parser.add_argument(
    '-pid', '--peer_id', help='Id of the peer to synce from after startup')
parser.add_argument(
    '-pport', '--peer_port', help='Port of the peer to connect to')
parser.add_argument('-p', '--port', help='Port for the instance')

args = parser.parse_args()

if not args.peer_id:
  # need to start this as a standalone server
  current_instance = BlockChain(args.port)
else:
  # peer is given ,need to start this with peer Id etc added
  peer_info_dict = {
      "existing_peer": True,
      "peer_id": args.peer_id,
      "peer_host": "0.0.0.0",
      "peer_port": args.peer_port
  }
  # start new instance
  current_instance = BlockChain(args.port, **peer_info_dict)
