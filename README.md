# PyNaive Chain [![Build Status](https://travis-ci.org/avneesh91/pynaive_chain.svg?branch=master)](https://travis-ci.org/avneesh91/pynaive_chain)
This is the source code for a toy block chain introduced <a href="https://technokeeda.com/programming/python-blockchain-implementation-toy/" target="_blank">here</a>

PyNaiveChain is a toy blockchain implemented completly in python. It has the following features as of now
   - Peer discovery of a loosely implemented gossip protocol
   - Simple consensus based data addition
   - Dedicated WebSocket Communication layer implemetation
   - Protocol Processing for inter-node comuunication
   - Flask based HTTP Layer for handling client requests

What it doesn't have at the moment:
   - Proof of work/Proof of stake based consensus
   - Proper implementation of node discovery
   - Block Data persistence
   - Chain reparing

Note: This only supports python 3, it is not compatible with Python 2.

## Usage and quickstart

### Starting a Single Node
Setup the virtual environment and install all the requirements
```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Check out the startup script for information about different options:
```
python start_node --help
usage: start_node.py [-h] [-pid PEER_ID] [-pport PEER_PORT] [-p PORT]

optional arguments:
  -h, --help                                   show this help message and exit
  -pid PEER_ID, --peer_id PEER_ID              Id of the peer to synce from after startup
  -pport PEER_PORT, --peer_port PEER_PORT      Port of the peer to connect to
  -p PORT, --port PORT                         Port for the instance
```

Once you are done installing the requirements, you can start by firing up a single node.
```sh
python start_node.py -p 15001
```

You should see outlogs like this
```
[INFO]: BLOCKCHAIN-Setting up naive chain server
[INFO]: BLOCKCHAIN-Intializing websocket RPC
[INFO]: RPC_SERVER-Intializing RPC server
[INFO]: BLOCKCHAIN-Intializing websocket RPC
[INFO]: BLOCKCHAIN-Intializing protocol processing
[INFO]: PROTOCOL_PROCESSOR-Intializing protocol processor
[INFO]: RPC_SERVER-Starting RPC server on port 0.0.0.0:15001
[INFO]: RPC_SERVER-RPC server waiting for connections
[INFO]: BLOCKCHAIN-Node 7a02e5b3-de28-49e5-947f-93a2c15d1d47 live on 0.0.0.0:15001
[INFO]: BLOCKCHAIN-No Peer Specified. Intializing genesis block for standalone operation
 * Serving Flask app "http_server" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:15002/ (Press CTRL+C to quit)
```
The http server starts on websocket port + 1. You can access HTTP based RPCs on :
```
Running on http://0.0.0.0:15002/ (Press CTRL+C to quit)
```

 The Node id is displayed in the output log:
 ```
 [INFO]: BLOCKCHAIN-Node 7a02e5b3-de28-49e5-947f-93a2c15d1d47 live on 0.0.0.0:15001
 ```

NOTE: Currently, a single node will not let you add any data. You need atleast 2 nodes to add any kind of data.

 ### Starting Multiple Nodes

Start a single node as shown in the previous section , and copy it's port and node id.(this example is going to use the node from above as the pre-exsiting peer.
```
python start_node.py -pid 7a02e5b3-de28-49e5-947f-93a2c15d1d47 -pport 15001 -p 9803
```

This should display the same output as above:
```
[INFO]: BLOCKCHAIN-Setting up naive chain server
[INFO]: BLOCKCHAIN-Intializing websocket RPC
[INFO]: RPC_SERVER-Intializing RPC server
[INFO]: BLOCKCHAIN-Intializing websocket RPC
[INFO]: BLOCKCHAIN-Intializing protocol processing
[INFO]: PROTOCOL_PROCESSOR-Intializing protocol processor
[INFO]: RPC_SERVER-Starting RPC server on port 0.0.0.0:9803
[INFO]: RPC_SERVER-RPC server waiting for connections
[INFO]: BLOCKCHAIN-Node be809443-c21f-4130-9ba8-b18a8f6e7e56 live on 0.0.0.0:9803
[INFO]: BLOCKCHAIN-Peer Discovered
[INFO]: BLOCKCHAIN-Joining remote peer
[INFO]: BLOCKCHAIN-Intializing data sync peer
[INFO]: PROTOCOL_PROCESSOR-NEW_PEER_JOIN_DATA_UPLOAD recieved
[INFO]: PROTOCOL_PROCESSOR-Saving data from remote peer
 * Serving Flask app "http_server" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:9804/ (Press CTRL+C to quit)
```

This is the same as above, but our new node gets all the info from the existing node as well:
```
[INFO]: BLOCKCHAIN-Peer Discovered
[INFO]: BLOCKCHAIN-Joining remote peer
[INFO]: BLOCKCHAIN-Intializing data sync peer
[INFO]: PROTOCOL_PROCESSOR-NEW_PEER_JOIN_DATA_UPLOAD recieved
[INFO]: PROTOCOL_PROCESSOR-Saving data from remote peer
```

You can add as many nodes as like this desired.
### HTTP Endpoints
All the nodes expose all their functionality throught HTTP endpoints

Name | End Point| Methof | Description |
| ------ | ------ | ------ |------ |
Add Data | /data | POST | Add new data to the blockchain |
Get Data | /data | GET | Get all the data currently residing in the blockchain |
Node Info| /node | GET | Get all information against a node |
Get Peers| /peers | GET | Get all the peers of a node |

#### Example Requests

##### Add Data

Request:
```
curl -X POST \
  http://127.0.0.1:15002/data \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{"data": "Testing String Again"}'
```
Response:
```
{"status": "OK", "data": true}
```

##### Get Data

Request:
```
curl -X GET http://127.0.0.1:15002/data
```
Response:
```
{
   "status":"OK",
   "data":[
      {
         "index":0,
         "previous_hash":"ioiiiuasyi891qbduquiuqwiqwiupwe",
         "data":"\"random\"",
         "curr_hash":"71fbc6a1c90d94050b32ab9f9d6a11fc41724f8f954905c120c4c16b71f1f80f"
      },
      {
         "index":1,
         "previous_hash":"71fbc6a1c90d94050b32ab9f9d6a11fc41724f8f954905c120c4c16b71f1f80f",
         "data":"\"Testing String Again\"",
         "curr_hash":"c8a8924ed4d8c58638b9f4fcbb7609bb0edb4a509d1514246a04ebba680d5a1f"
      }
   ]
}
```

##### Node Info
Request:
```
curl -X GET http://127.0.0.1:15002/node
```

Response:
```
{
   "status":"OK",
   "data":{
      "peer_id":"7a02e5b3-de28-49e5-947f-93a2c15d1d47",
      "data_count":2,
      "health":true,
      "rpc_port":"15001",
      "age":"2018-06-02 12:42:13.860551"
   }
}
```

##### Get Peers
Request:
```
curl -X GET http://127.0.0.1:15002/peers
```

Response:
```
{
   "status":"OK",
   "data":{
      "01cfb470-65a3-4267-a33c-28be309b5887":{
         "host":"0.0.0.0",
         "port":"9803"
      }
   }
}
```
