from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class NaiveChainHTTPServer(object):
    def __init__(self, chain_instance, host, port, *args, **kwargs):
        self.host = host
        self.port = port
        self.chain_instance = chain_instance

    def start_server(self):
        import ipdb;ipdb.set_trace()
        app.config['chain_instance'] = self.chain_instance
        app.run(host=self.host, port=self.port)


class Peers(Resource):
    def post(self):
        print(self)
        return {'status': 'OK'}, 200

    def get(self):
        current_bc = app.config.get('chain_instance')
        return {'status': 'OK', 'data': current_bc.peer_connect_dict}, 200


api.add_resource(Peers, '/peers')
