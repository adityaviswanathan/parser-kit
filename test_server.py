#!/usr/bin/env python
'''
Tests.
'''

__author__ = 'Aditya Viswanathan'
__email__ = 'aditya@adityaviswanathan.com'

import requests
import semantics_pb2 as semantics
import subprocess
import threading
import time
import unittest
from flask import request
from server import app


class ServerSanity(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # TODO(aditya): Make tests work by background launching the server here.
        # Temporarily we need to run the server in a separate process and then
        # run tests.
        # self.server_process = subprocess.Popen(['python', 'server.py'])
        pass

    @classmethod
    def tearDownClass(self):
        # self.server_process.terminate()
        pass

    def testServerUp(self):
        headers = {'Content-Type': 'application/octet-stream'}
        input_text = semantics.InputText()
        input_text.text = 'Hello how are you doing?'
        resp = requests.post('http://localhost:8080/',
                             headers=headers, data=input_text.SerializeToString())
        parse_tree = semantics.ParseTree()
        parse_tree.ParseFromString(resp.content)
        # TODO(aditya): Decide on testing strategy for parse trees here.
        # Goldens-based validation can work but every improvement/modification
        # to parser code will require an overwrite of the goldens. Or we can
        # just do a baseline check here that ensures a valid semantics proto is
        # returned by the HTTP server, but that doesn't really guarantee much
        # about this service.
        print(parse_tree)

if __name__ == '__main__':
    unittest.main()
