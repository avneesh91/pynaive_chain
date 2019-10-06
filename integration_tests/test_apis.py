import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import time
import unittest
import requests
import random
from . import PyNaiveChainTestingThread

class TestAPIUsingRequests(unittest.TestCase):

    def setUp(self):
        self.port = random.randint(10000, 20000)
        self.current_executor = PyNaiveChainTestingThread(str(self.port))
        self.daemon = True
        self.current_executor.start()

        # wait for the server to intialize
        time.sleep(1)

    def test_hello_world(self):
        #response = requests.get('http://localhost:15002/data', timeout=60)
        print("1")
    def test_hello_world_test(self):
        #response = requests.get('http://localhost:15002/data', timeout=60)
        print("12")

    def tearDown(self):
        self.current_executor.shutdown()
        print(self.current_executor.is_alive())

