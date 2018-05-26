from flask import Flask, request
from flask_restful import Resource, Api

from utils import get_logger

app = Flask(__name__)
api = Api(app)


#import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)

http_logger = get_logger('HTTP_SERVER')

class NaiveChainHTTPServer(object):
    def __init__(self, chain_instance, host, port, *args, **kwargs):
        self.host = host
        self.port = port
        self.chain_instance = chain_instance

    def start_server(self):
        app.config['chain_instance'] = self.chain_instance
        app.run(host=self.host, port=self.port)


class Peers(Resource):
    def post(self):
        bc_instance = app.config.get('chain_instance')

        http_logger('Adding Perr to node')
        request_json = request.get_json(force=True)
        bc_instance.protocol_processor
        return {'status': 'OK'}, 200

    def get(self):
        current_bc = app.config.get('chain_instance')
        return {'status': 'OK', 'data': current_bc.peer_connect_dict}, 200

class Data(Resource):

    def post(self):
        current_bc = app.config.get('chain_instance')
        request_json = request.get_json(force=True)

        # the data to be saved in the block chain
        curr_data = request_json.get('data')

        added_data = current_bc.add_data(str(curr_data))

        return {'status': 'OK', 'data': added_data}, 200

    def get(self):
        current_bc = app.config.get('chain_instance')
        all_data = [ i.serialize() for i in current_bc.block_data]
        return {'status': 'OK', 'data': all_data}, 200




api.add_resource(Peers, '/peers')
api.add_resource(Data, '/data')
