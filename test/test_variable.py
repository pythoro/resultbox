# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 20:04:58 2019

@author: Reuben
"""

import unittest

from resultbox import Variable, Aliases

class Test_Variable(unittest.TestCase):
    def test_init(self):
        name = 'a'
        desc = 'b'
        unit = 'c'
        v = Variable(name, desc, unit)
        self.assertEqual(v.name, name)
        self.assertEqual(v.desc, desc)
        self.assertEqual(v.unit, unit)
        
        
class Test_Aliases(unittest.TestCase):
    def test_init(self):
        dct = {'a': 'something'}
        a = Aliases(dct)
        self.assertDictEqual(a, dct)
        
    def test_from_dict(self):
        dct = {'a': 'something'}
        a = Aliases(dct)
        d = {'a': 3}
        ret = a.from_dict(d)
        expected = dct
        self.assertDictEqual(ret, expected)

    def test_from_list(self):
        dct = {'a': 'something'}
        a = Aliases(dct)
        lst = ['a']
        ret = a.from_list(lst)
        expected = dct
        self.assertDictEqual(ret, expected)