#!/usr/bin/env python
'''
Language model generator CLI tool to read a set of labeled traning data and
build a language model, which is serialized to disk.

usage: model_generator.py [-h] --infile INFILE --outfile OUTFILE

required arguments:
--infile INFILE    path to labeled training data
--outfile OUTFILE  path where language model will be written

optional arguments:
-h, --help         show this help message and exit
'''

__author__ = 'Aditya Viswanathan'
__email__ = 'aditya@adityaviswanathan.com'

import argparse
import pickle
import random
import spacy
from pathlib import Path

def gen_model(training_data, outfile, model=None, iterations=5):
    # Load the model, set up the pipeline and train the parser.
    if model is not None:
        nlp = spacy.load(model)
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # Create blank Language model
        print("Created blank 'en' model")

    # We'll use the built-in dependency parser class, but we want to create a
    # fresh instance – just in case.
    if 'parser' in nlp.pipe_names:
        nlp.remove_pipe('parser')
    parser = nlp.create_pipe('parser')
    nlp.add_pipe(parser, first=True)

    for text, annotations in training_data:
        for dep in annotations.get('deps', []):
            parser.add_label(dep)

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'parser']
    with nlp.disable_pipes(*other_pipes):  # only train parser
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            random.shuffle(training_data)
            losses = {}
            for text, annotations in training_data:
                nlp.update([text], [annotations], sgd=optimizer, losses=losses)
            # print(losses)

    # Save model to output directory
    if outfile is not None:
        outfile = Path(outfile)
        if not outfile.exists():
            outfile.mkdir()
        nlp.to_disk(outfile)
        print("Saved model to", outfile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile',
                        required=True,
                        help='path to labeled training data')
    parser.add_argument('--outfile',
                        required=True,
                        help='path where language model will be written')
    args = parser.parse_args()
    labeled_training_data = []
    with open(args.infile, 'rb') as f:
        labeled_training_data = pickle.load(f)
    gen_model(labeled_training_data, args.outfile)
