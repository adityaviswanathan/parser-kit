#!/usr/bin/env python
'''
HTTP server starting point.
'''

__author__ = 'Aditya Viswanathan'
__email__ = 'aditya@adityaviswanathan.com'

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=True)
