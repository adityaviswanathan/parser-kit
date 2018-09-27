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
import semantics_pb2 as semantics
import spacy

def add_parsed_token_to_tree(parent_token, children):
    for child in children:
        child_token = parent_token.children.add()
        child_token.token = child.text
        child_token.type = semantics.ParsedToken().DESCRIPTOR.enum_values_by_name[child.dep_].number
        add_parsed_token_to_tree(child_token, child.children)

class Parser(object):
    def __init__(self, model_file='models/model1'):
        self.nlp = spacy.load(model_file)

    def parse(self, text):
        docs = self.nlp.pipe([text])
        doc = next(docs) # There should be only one doc.
        parse_tree = semantics.ParseTree()
        # TODO(aditya): Remove hardcoded 'ROOT' label below.
        roots = [token for token in doc if token.dep_ == 'ROOT']
        if len(roots) > 0:
            root = roots[0]
            root_token = semantics.ParsedToken()
            root_token.token = root.text
            root_token.type = semantics.ParsedToken.ROOT
            add_parsed_token_to_tree(root_token, root.children)
            parse_tree.root.CopyFrom(root_token)
        # print(doc.text)
        # print([(t.text, t.dep_, t.head.text) for t in doc])
        # TODO(aditya): Validate this output with tests
        # print(parse_tree)
        return parse_tree


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--text',
                        required=True,
                        help='input text to parse')
    parser.add_argument('--infile',
                        required=True,
                        help='path to language model')
    args = parser.parse_args()
    parser = Parser(model_file=args.infile)
    parser.parse(args.text)
