# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 21:45:56 2019

@author: Reuben
"""

import unittest

from resultbox import Box, Tabulator, Vector_Tabulator, Table, Variable, Aliases

def get_lst():
    lst = [{'index': 0, 'independent': {'a': 1, 'b': 1, 'c': 1}, 'dependent': {'d': 11}},
           {'index': 1, 'independent': {'a': 1, 'b': 2, 'c': 2}, 'dependent': {'d': 12}},
           {'index': 2, 'independent': {'a': 1, 'b': 2, 'c': 1}, 'dependent': {'d': 13}},
           {'index': 3, 'independent': {'a': 1, 'b': 1, 'c': 2}, 'dependent': {'d': 14}},
           {'index': 4, 'independent': {'a': 2, 'b': 1, 'c': 1}, 'dependent': {'d': 15}},
           {'index': 5, 'independent': {'a': 2, 'b': 1, 'c': 2}, 'dependent': {'d': 16}},
           {'index': 6, 'independent': {'a': 2, 'b': 2, 'c': 1}, 'dependent': {'d': 17}},
           {'index': 7, 'independent': {'a': 2, 'b': 2, 'c': 2}, 'dependent': {'d': 18}}]
    return lst


def get_lst2():
    lst = [{'index': 0, 'independent': {'a': 1, 'b': 1, 'c': [1, 2]}, 'dependent': {'d': [12, 30]}},
           {'index': 1, 'independent': {'a': 1, 'b': 2, 'c': [1, 2]}, 'dependent': {'d': [13, 31]}},
           {'index': 4, 'independent': {'a': 2, 'b': 1, 'c': [1, 2]}, 'dependent': {'d': [16, 34]}},
           {'index': 7, 'independent': {'a': 2, 'b': 2, 'c': [1, 2]}, 'dependent': {'d': [19, 37]}}]
    return lst


def get_lst3():
    lst = [{'index': 0, 'independent': {'a': 1, 'b': 1}, 'dependent': {'d': [12, 30]}},
           {'index': 1, 'independent': {'a': 1, 'b': 2}, 'dependent': {'d': [13, 31]}},
           {'index': 4, 'independent': {'a': 1, 'b': 1}, 'dependent': {'e': [1, 2]}},
           {'index': 7, 'independent': {'a': 1, 'b': 2}, 'dependent': {'e': [1, 2]}}]
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

    def test_tabulate3(self):
        t = Tabulator()
        box = Box(get_lst3())
        index = ['a', 'b']
        columns = ['e']
        values = 'd'
        pt = t.tabulate(box=box, values=values, columns=columns, index=index)
        expected = 'e     1   2\na b        \n1 1  12  30\n  2  13  31'
        self.assertEqual(str(pt), expected)        
        
        
class Test_Vector_Tabulator(unittest.TestCase):
    def test_tabulate(self):
        t = Vector_Tabulator()
        box = Box(get_lst3())
        columns = 'd'
        values = 'e'
        data = t.tabulate(box=box, values=values, columns=columns)
        expected = [{'independent': {'a': 1, 'b': 1},
                     'dependent': {'d': [12, 30], 'e': [1, 2]}},
                    {'independent': {'a': 1, 'b': 2},
                     'dependent': {'d': [13, 31], 'e': [1, 2]}}]
        self.assertListEqual(data, expected)

    def test_vecs(self):
        t = Vector_Tabulator()
        box = Box(get_lst3())
        columns = 'd'
        values = 'e'
        data = t.vecs(box=box, values=values, columns=columns)
        expected = [{'label': "{'a': 1, 'b': 1}",
                     'values': [1, 2], 'columns': [12, 30]},
                    {'label': "{'a': 1, 'b': 2}",
                     'values': [1, 2], 'columns': [13, 31]}]
        self.assertListEqual(data, expected)
