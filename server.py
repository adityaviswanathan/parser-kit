#!/usr/bin/env python
'''
HTTP server starting point.
'''

__author__ = 'Aditya Viswanathan'
__email__ = 'aditya@adityaviswanathan.com'

import semantics_pb2 as semantics
from flask import Flask, request, Response
from parser import Parser
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world'


@app.route('/', methods=['POST'])
def parse():
    # TODO(aditya): Check for sane content length before deserializing protobuf.
    input_text = semantics.InputText()
    input_text.ParseFromString(request.get_data())
    parser = Parser()
    # Get ParseTree as protobuf.
    parse_tree = parser.parse(input_text.text)
    resp = Response(parse_tree.SerializeToString(), status=200,
                    mimetype='application/octet-stream')
    return resp

if __name__ == '__main__':
    # TODO(aditya): Structured port assignment/discovery.
    app.run(debug=True, port=8080)
