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
        expected = {'1': {'1': {'__index__': [0, 3]},
                          '2': {'__index__': [1, 2]}},
                    '2': {'1': {'__index__': [4, 5]},
                          '2': {'__index__': [6, 7]}}}
        self.assertDictEqual(nested, expected)
        self.assertDictEqual(val_dict, {'a.1': 1, 'a.2': 2, 'b.1': 1, 'b.2': 2})
        
    def test_make_index(self):
        t = Tabulator()
        lst = get_lst()
        var_list = ['a', 'b']
        index, indices = t.make_index(lst, var_list)
        print(index)
        print(indices)
        return
        expected = {'1': {'1': {}, '2': {}}, '2': {'1': {}, '2': {}}}
        self.assertDictEqual(nested, expected)
        self.assertDictEqual(val_dict, {'a.1': 1, 'a.2': 2, 'b.1': 1, 'b.2': 2})
        


