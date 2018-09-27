#!/usr/bin/env python
'''
Labeler CLI tool to label a set of examples.

usage: labeler.py [-h] --infile INFILE --outfile OUTFILE

required arguments:
  --infile INFILE    path to examples that need to be labeled
  --outfile OUTFILE  path where labeled data will be written

optional arguments:
  -h, --help         show this help message and exit
'''
__author__ = 'Aditya Viswanathan'
__email__ = 'aditya@adityaviswanathan.com'

import argparse
import pickle
import semantics_pb2 as semantics


def get_parse_types():
    semantic_type_names = []
    for semantic_type, _ in semantics.ParsedToken().DESCRIPTOR.enum_values_by_name.items():
        semantic_type_names.append(semantic_type)
    print(semantic_type_names)
    return semantic_type_names


def validate_selection(input_str, num_selections, selection_name):
    if not input_str:
        print('Please enter a valid value')
        return False
    try:
        if int(input_str) not in range(len(get_parse_types())):
            print('Please enter a valid %s between 0 and %d' %
                  (selection_name, num_selections - 1))
            return False
    except:
        print('Input %s cannot be cast to integer, please make sure you are entering numeric input' % input_str)
        return False
    return True


def label_example(example, example_idx):
    # TODO(aditya): This is way too naive, should have better token matching logic to decide on the words.
    # E.g. "San Francisco" should be one token while "isn't" should be two.
    words = example.split()
    print('Labeling example %d: %s' % (example_idx + 1, example))
    input_prompt = '%d) %s'
    cursor_prompt = '\n---> '
    semantic_type_input_prompt = '\n'.join(input_prompt % (
        idx, val) for idx, val in enumerate(get_parse_types())) + cursor_prompt
    modifier_input_prompt = '\n'.join(input_prompt % (idx, val)
                                      for idx, val in enumerate(words)) + cursor_prompt
    words_data = [] # cleaner (debug) representation
    spacy_word_deps = [] # maps to 'deps' property in spacy training data schema
    spacy_word_heads = [] # maps to 'heads' property in spacy training data schema
    for word in words:
        word_data = {}
        label_type = 'semantic type'
        user_input_valid = False
        print('What is the %s of the word \'%s\' in example \'%s\'?' %
              (label_type, word, example.strip('\n')))
        while not user_input_valid:
            user_input = input(semantic_type_input_prompt)
            user_input_valid = validate_selection(
                user_input, len(get_parse_types()), label_type)
        word_data['semantic_type'] = get_parse_types()[int(user_input)]
        spacy_word_deps.append(word_data['semantic_type'])
        label_type = 'modifier'
        user_input_valid = False
        print('What is the word that \'%s\' is a %s of in example \'%s\'?' %
              (word, label_type, example.strip('\n')))
        while not user_input_valid:
            user_input = input(modifier_input_prompt)
            user_input_valid = validate_selection(
                user_input, len(words), label_type)
        word_data['modifier'] = words[int(user_input)]
        spacy_word_heads.append(int(user_input))
        words_data.append(word_data)
    return (example.strip('\n'),
            {'heads': spacy_word_heads, 'deps': spacy_word_deps})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile',
                        required=True,
                        help='path to examples that need to be labeled')
    parser.add_argument('--outfile',
                        required=True,
                        help='path where labeled data will be written')
    args = parser.parse_args()
    example_idx = 0
    spacy_training_data = []
    with open(args.infile, 'r') as f:
        for example in f:
            spacy_training_data.append(label_example(example, example_idx))
            print(spacy_training_data)
            example_idx += 1
    with open(args.outfile, 'wb') as f:
        pickle.dump(spacy_training_data, f)
        print('Serialized labeled data to %s' % args.outfile)
