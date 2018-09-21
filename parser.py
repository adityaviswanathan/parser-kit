#!/usr/bin/env python
'''
Intent parser that builds a parse tree over the input text using a pregenerated
language model.

usage: parser.py [-h] --text TEXT --infile INFILE

required arguments:
--text TEXT      path to labeled training data
--infile INFILE  path to labeled training data

optional arguments:
-h, --help       show this help message and exit
'''

__author__ = 'Aditya Viswanathan'
__email__ = 'aditya@adityaviswanathan.com'

import argparse
import spacy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--text',
                        required=True,
                        help='input text to parse')
    parser.add_argument('--infile',
                        required=True,
                        help='path to language model')
    args = parser.parse_args()
    nlp = spacy.load(args.infile)
    docs = nlp.pipe([args.text])
    for doc in docs:
        print(doc.text)
        print([(t.text, t.dep_, t.head.text) for t in doc])
