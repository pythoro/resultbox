# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 21:45:56 2019

@author: Reuben
"""

import unittest

from resultbox import Box, Tabulator, Table, Variable, Aliases

def get_lst():
    lst = [{'index': 0, 'a': 1, 'b': 1, 'c': 1, 'd': 11},
           {'index': 1, 'a': 1, 'b': 2, 'c': 2, 'd': 12},
           {'index': 2, 'a': 1, 'b': 2, 'c': 1, 'd': 13},
           {'index': 3, 'a': 1, 'b': 1, 'c': 2, 'd': 14},
           {'index': 4, 'a': 2, 'b': 1, 'c': 1, 'd': 15},
           {'index': 5, 'a': 2, 'b': 1, 'c': 2, 'd': 16},
           {'index': 6, 'a': 2, 'b': 2, 'c': 1, 'd': 17},
           {'index': 7, 'a': 2, 'b': 2, 'c': 2, 'd': 18}]
    return lst


def get_lst2():
    lst = [{'index': 0, 'a': 1, 'b': 1, 'c': [1, 2], 'd': [12, 30]},
           {'index': 1, 'a': 1, 'b': 2, 'c': [1, 2], 'd': [13, 31]},
           {'index': 4, 'a': 2, 'b': 1, 'c': [1, 2], 'd': [16, 34]},
           {'index': 7, 'a': 2, 'b': 2, 'c': [1, 2], 'd': [19, 37]}]
    return lst

    
class Test_Tabulator(unittest.TestCase):
    def test_tabulate(self):
        t = Tabulator()
        box = Box(get_lst())
        index = ['a', 'b']
        columns = ['c']
        values = 'd'
        pt = t.tabulate(box=box, values=values, columns=columns, index=index)
        expected = 'c     1   2\na b        \n1 1  11  14\n  2  13  12\n2 1  15  16\n  2  17  18'
        self.assertEqual(str(pt), expected)
        
    def test_tabulate2(self):
        t = Tabulator()
        box = Box(get_lst2())
        index = ['a', 'b']
        columns = ['c']
        values = 'd'
        pt = t.tabulate(box=box, values=values, columns=columns, index=index)
        expected = 'c     1   2\na b        \n1 1  12  30\n  2  13  31\n2 1  16  34\n  2  19  37'
        self.assertEqual(str(pt), expected)

    def test_tabulate_translated(self):
        dct = {'a': Variable('one', 'blah', 'mm'),
               'b': Variable('two', 'blah2', 's'),
               'c': Variable('three', 'blah2', 'N')}
        a = Aliases(dct)

        t = Tabulator()
        box = Box(get_lst())
        index = ['a', 'b']
        columns = ['c']
        values = 'd'
        pt = t.tabulate(box=box, values=values, columns=columns, index=index,
                        aliases=a)
        expected = 'three [N]          1   2\none [mm] two [s]        \n1        1        11  14\n         2        13  12\n2        1        15  16\n         2        17  18'
        self.assertEqual(str(pt), expected)
        
    def test_tabulate_guessed_indices(self):
        t = Tabulator()
        box = Box(get_lst())
        columns = ['c']
        values = 'd'
        pt = t.tabulate(box=box, values=values, columns=columns)
        expected = 'c     1   2\na b        \n1 1  11  14\n  2  13  12\n2 1  15  16\n  2  17  18'
        self.assertEqual(str(pt), expected)
        