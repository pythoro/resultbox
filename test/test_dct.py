# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 20:04:58 2019

@author: Reuben
"""

import unittest

from resultbox import Dict


def get_dct():
    dct = {'a': 1, 'b': 2}
    d = Dict(dct)
    return d
   

class Test_Dict(unittest.TestCase):
    def test_init(self):
        dct = {'a': 1, 'b': 2}
        d = Dict(dct)
        self.assertEqual(d, dct)

    def test_subdict(self):
        d = get_dct()
        d2 = d.subdict('c', 5)
        expected = {'a': 1, 'b': 2, 'c': 5}
        self.assertDictEqual(d2, expected)
        self.assertTrue(isinstance(d2, Dict))
        
    def test_copy(self):
        d = get_dct()
        d2 = d.copy()
        self.assertDictEqual(d2, d)
        self.assertTrue(isinstance(d2, Dict))
