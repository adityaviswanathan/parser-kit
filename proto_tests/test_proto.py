#!/usr/bin/env python
'''
Tests basic proto functionality with py3.
'''

__author__ = 'Aditya Viswanathan'
__email__ = 'aditya@adityaviswanathan.com'

import test_pb2
import unittest

TESTSTRING = 'test'
TESTINT = 1
TESTFLOAT = 1.1
TESTBOOL = True
TESTENUM = test_pb2.TestEnum.FIRST

FLOAT_PRECISION = 2

class ProtobufSanity(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        composition_proto_as_py = test_pb2.TestComposition()
        message_proto_as_py = composition_proto_as_py.testmessages.add()
        message_proto_as_py.teststring = TESTSTRING
        message_proto_as_py.testint = TESTINT
        message_proto_as_py.testfloat = TESTFLOAT
        message_proto_as_py.testbool = TESTBOOL
        composition_proto_as_py.testenum = TESTENUM
        self.serialized = composition_proto_as_py.SerializeToString()

    def test_deserialize(self):
        composition_proto_as_py = test_pb2.TestComposition()
        composition_proto_as_py.ParseFromString(self.serialized)
        self.assertEqual(composition_proto_as_py.testenum, TESTENUM)
        self.assertEqual(len(composition_proto_as_py.testmessages), 1)
        self.assertEqual(composition_proto_as_py.testmessages[0].teststring, TESTSTRING)
        self.assertEqual(composition_proto_as_py.testmessages[0].testint, TESTINT)
        # Python floats suck, let's limit to n digits of precision.
        format_str = "{0:%sf}" % FLOAT_PRECISION
        self.assertEqual(format_str.format(composition_proto_as_py.testmessages[0].testfloat),
                         format_str.format(TESTFLOAT))
        self.assertEqual(composition_proto_as_py.testmessages[0].testbool, TESTBOOL)
        pass

if __name__ == '__main__':
    unittest.main()
