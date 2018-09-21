#!/usr/bin/env python
'''
Class comments here.
'''

__author__ = 'Aditya Viswanathan'
__email__ = 'aditya@adityaviswanathan.com'

import en_core_web_sm
nlp = en_core_web_sm.load()
doc = nlp(u'Hello how are you doing today?')

for token in doc:
    print(token.text,
          token.lemma_,
          token.pos_,
          token.tag_,
          token.dep_,
          token.shape_,
          token.is_alpha,
          token.is_stop)
