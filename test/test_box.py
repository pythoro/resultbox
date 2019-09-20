# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 20:13:44 2019

@author: Reuben
"""

import unittest

from resultbox import Box


def get_dct():
    dct = {'a': 1, 'b': 2}
    return dct
   
def get_lst3():
    lst = [{'index': 0, 'independent': {'a': 1, 'b': 1}, 'dependent': {'d': [12, 30]}},
           {'index': 1, 'independent': {'a': 1, 'b': 2}, 'dependent': {'d': [13, 31]}},
           {'index': 4, 'independent': {'a': 1, 'b': 1}, 'dependent': {'e': [1, 2]}},
           {'index': 7, 'independent': {'a': 1, 'b': 2}, 'dependent': {'e': [1, 2]}}]
    return lst

class Test_Box(unittest.TestCase):
    def test_init(self):
        b = Box()

    def test_add(self):
        b = Box()    
        dct = get_dct()
        b.add(dct, 'test', 7)
        self.assertEqual(len(b), 1)
        expected = {'index': 0, 'independent': {'a': 1, 'b': 2},
                    'dependent': {'test': 7}}
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
        expected = [{'index': 1, 'independent': {'a': 1, 'b': 2},
                     'dependent': {'test2': 8}},
                    {'index': 2, 'independent': {'a': 1, 'b': 3},
                     'dependent': {'test2': 9}}]
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
        expected = [{'index': 2, 'independent': {'a': 1, 'b': 3},\
                     'dependent': {'test':  9}},
                    {'index': 3, 'independent': {'a': 1, 'b': 3},
                     'dependent': {'test2':  11}}]
        ret = b.where({'b': 3})
        self.assertEqual(ret, expected)
        ret = b.where(b=3)
        self.assertEqual(ret, expected)
        
    def test_minimal(self):
        b = Box()    
        dct = get_dct()
        b.add(dct, 'test', 7)
        b.add(dct, 'test2', 8)
        minimal = b.minimal()
        expected = [{'a': 1, 'b': 2, 'test': 7, 'test2': 8}]
        self.assertEqual(minimal, expected)
        
    def test_combined(self):
        b = Box()    
        dct = get_dct()
        b.add(dct, 'test', 7)
        b.add(dct, 'test2', 8)
        combined = b.combined()
        expected = [{'independent': {'a': 1, 'b': 2},
                     'dependent': {'test': 7, 'test2': 8}}]
        self.assertEqual(combined, expected)
        
    def test_merge_in_place(self):
        b1 = Box()
        b2 = Box()
        dct = get_dct()
        b1.add(dct, 'test', 7)
        b2.add(dct, 'test2', 8)
        b1.merge(b2)
        expected = [{'index': 0,
                     'independent': {'a': 1, 'b': 2}, 
                     'dependent': {'test': 7}},
                    {'index': 1,
                     'independent': {'a': 1, 'b': 2}, 
                     'dependent': {'test2': 8}}]
        self.assertListEqual(b1, expected)

    def test_merge_not_in_place(self):
        b1 = Box()
        b2 = Box()
        dct = get_dct()
        b1.add(dct, 'test', 7)
        b2.add(dct, 'test2', 8)
        b3 = b1.merge(b2, in_place=False)
        expected = [{'index': 0,
                     'independent': {'a': 1, 'b': 2}, 
                     'dependent': {'test': 7}},
                    {'index': 1,
                     'independent': {'a': 1, 'b': 2}, 
                     'dependent': {'test2': 8}}]
        self.assertListEqual(b3, expected)

        
    def test_getitem(self):
        b = Box(get_lst3())
        keys = ['d', 'e']
        res = b[keys]
        expected = [[[12, 30], [13, 31]], [[1, 2], [1, 2]], ['a=1, b=1', 'a=1, b=2']]
        self.assertListEqual(expected, res)