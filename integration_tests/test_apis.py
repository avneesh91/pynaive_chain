import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import json
import time
import unittest
import requests
import random
from . import PyNaiveChainTestingThread


class TestAPIUsingRequests(unittest.TestCase):

  def setUp(self):
    self.port = random.randint(10000, 20000)
    self.current_executor = PyNaiveChainTestingThread(str(self.port))
    self.current_executor.start()

    # wait for the server to intialize
    time.sleep(1)

  def test__given_active_blockchain_node__when_node_info_api_invoked__then_return_node_info(
      self):
    response = requests.get(
        'http://localhost:{}/node'.format(self.port + 1), timeout=60)

    # network verification
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers['Content-Type'], 'application/json')

    payload = json.loads(response.content)
    node_info = payload.get('data', {})

    self.assertEqual(payload.get('status'), 'OK')
    self.assertEqual(
        set(node_info.keys()),
        {'peer_id', 'data_count', 'health', 'rpc_port', 'age'})

  def test__given_active_blockchain_node__when_data_api_invoked__then_return_data_info(
      self):
    response = requests.get(
        'http://localhost:{}/data'.format(self.port + 1), timeout=60)

    # network verification
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers['Content-Type'], 'application/json')

    payload = json.loads(response.content)

    self.assertEqual(payload.get('status'), 'OK')
    self.assertIsInstance(payload.get('data'), list)
    self.assertEqual(len(payload.get('data', [])), 1)

    self.assertEqual(
        set(payload.get('data')[0].keys()),
        {'index', 'previous_hash', 'data', 'curr_hash'})

  def test__given_active_blockchain_node__when_peer_api_invoked__then_return_peer_data(
      self):
    response = requests.get(
        'http://localhost:{}/peers'.format(self.port + 1), timeout=60)

    # network verification
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers['Content-Type'], 'application/json')

    payload = json.loads(response.content)

    self.assertEqual(payload.get('status'), 'OK')
    self.assertIsInstance(payload.get('data'), dict)

  def test__given_active_blockchain_node__when_add_data_api_invoked__then_add_data(
      self):

    test_data = {"data": "String for testing"}

    response = requests.post(
        'http://localhost:{}/data'.format(self.port + 1),
        timeout=60,
        data=json.dumps(test_data),
        headers={'Content-Type': 'application/json'})

    # network verification
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.headers['Content-Type'], 'application/json')

    payload = json.loads(response.content)

    self.assertEqual(payload.get('status'), 'OK')
    self.assertTrue(payload.get('data'))

  def tearDown(self):
    self.current_executor.shutdown()
    print(self.current_executor.is_alive())
