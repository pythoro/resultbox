# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 21:45:56 2019

@author: Reuben
"""

import unittest

from resultbox import Tabulator, Table

def get_lst():
    lst = [{'index': 0, 'a': 1, 'b': 1, 'c': 1},
           {'index': 1, 'a': 1, 'b': 2, 'c': 1},
           {'index': 2, 'a': 1, 'b': 2, 'c': 1},
           {'index': 3, 'a': 1, 'b': 1, 'c': 2},
           {'index': 4, 'a': 2, 'b': 1, 'c': 1},
           {'index': 5, 'a': 2, 'b': 1, 'c': 2},
           {'index': 6, 'a': 2, 'b': 2, 'c': 1},
           {'index': 7, 'a': 2, 'b': 2, 'c': 2}]
    return lst
    
class Test_Tabulator(unittest.TestCase):
    def test_make_nested_index(self):
        t = Tabulator()
        lst = get_lst()
        var_list = ['a', 'b']
        nested, val_dict = t.make_nested_index(lst, var_list)
        expected = {b'\x93\xb8\x85\xad\xfe\r\xa0\x89\xcd\xf64\x90O\xd5\x9fq': {b'\x93\xb8\x85\xad\xfe\r\xa0\x89\xcd\xf64\x90O\xd5\x9fq': {'__index__': [0, 3]}, b"\xc4\x10?\x12-'g|\x9d\xb1D\xca\xe19Jf": {'__index__': [1, 2]}}, b"\xc4\x10?\x12-'g|\x9d\xb1D\xca\xe19Jf": {b'\x93\xb8\x85\xad\xfe\r\xa0\x89\xcd\xf64\x90O\xd5\x9fq': {'__index__': [4, 5]}, b"\xc4\x10?\x12-'g|\x9d\xb1D\xca\xe19Jf": {'__index__': [6, 7]}}}
        self.assertDictEqual(nested, expected)
        expected2 = {b'\xcb\xa3\xf4\x85\x8b\x07\x83\xce\x80\xb8{\xed\xeb\xa1\x85\xb5': 1, b'~\x91C\x00\xd2\xcf\xe3\x1ag\x8af9\x10\xc5\x13\xa0': 1, b'?\x82n\x18\x9c\x92\xa3\x02\x05\x16\x1a\xd7\x89\x1d\x89\xbf': 2, b'\\\x04\xa9\x89\xc8S[>.c\x10\xd1\xa5~\xe8\x8d': 2}
        self.assertDictEqual(val_dict, expected2)
        
    def test_make_index(self):
        t = Tabulator()
        lst = get_lst()
        var_list = ['a', 'b']
        index, indices = t.make_index(lst, var_list)
        return
        expected = {'1': {'1': {}, '2': {}}, '2': {'1': {}, '2': {}}}
        self.assertDictEqual(nested, expected)
        self.assertDictEqual(val_dict, {'a.1': 1, 'a.2': 2, 'b.1': 1, 'b.2': 2})
        


