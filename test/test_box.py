# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 20:13:44 2019

@author: Reuben
"""

import unittest

from resultbox import Box, Dict


def get_dct():
    dct = {'a': 1, 'b': 2}
    d = Dict(dct)
    return d
   

class Test_Box(unittest.TestCase):
    def test_init(self):
        b = Box()

    def test_add(self):
        b = Box()    
        dct = get_dct()
        b.add(dct, 'test', 7)
        self.assertEqual(len(b), 1)
        expected = {'index': 0, 'a': 1, 'b': 2, 'test': 7}
        self.assertEqual(b[0], expected)
        
    def test_filtered(self):
        b = Box()    
        dct = get_dct()
        b.add(dct, 'test', 7)
        b.add(dct, 'test2', 8)
        dct['b'] = 3
        b.add(dct, 'test2', 9)
        dct['b'] = 6
        b.add(dct, 'test', 11)
        expected = [{'index': 1, 'a': 1, 'b': 2, 'test2': 8},
                    {'index': 2, 'a': 1, 'b': 3, 'test2': 9}]
        ret = b.filtered('test2')
        self.assertEqual(ret, expected)
        ret = b.filtered(['test2'])
        self.assertEqual(ret, expected)
        
    def test_where(self):
        b = Box()    
        dct = get_dct()
        b.add(dct, 'test', 7)
        b.add(dct, 'test2', 8)
        dct['b'] = 3
        b.add(dct, 'test', 9)
        b.add(dct, 'test2', 11)
        expected = [{'index': 2, 'a': 1, 'b': 3, 'test': 9},
                    {'index': 3, 'a': 1, 'b': 3, 'test2': 11}]
        ret = b.where({'b': 3})
        self.assertEqual(ret, expected)
        ret = b.where(b=3)
        self.assertEqual(ret, expected)
        