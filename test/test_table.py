# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 21:45:56 2019

@author: Reuben
"""

import unittest

from resultbox import Box, Tabulator, Table, Store, Variable, Aliases

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

def get_lst2_b():
    lst = [{'index': 0, 'independent': {'a': 1, 'b': 1}, 'dependent': {'d': [12, 30]}},
           {'index': 1, 'independent': {'a': 1, 'b': 2}, 'dependent': {'d': [13, 31]}},
           {'index': 4, 'independent': {'a': 2, 'b': 1}, 'dependent': {'d': [16, 34]}},
           {'index': 7, 'independent': {'a': 2, 'b': 2}, 'dependent': {'d': [19, 37]}}]
    return lst


def get_lst3():
    lst = [{'index': 0, 'independent': {'a': 1, 'b': 1}, 'dependent': {'d': [12, 30]}},
           {'index': 1, 'independent': {'a': 1, 'b': 2}, 'dependent': {'d': [13, 31]}},
           {'index': 4, 'independent': {'a': 1, 'b': 1}, 'dependent': {'e': [1, 2]}},
           {'index': 7, 'independent': {'a': 1, 'b': 2}, 'dependent': {'e': [1, 2]}}]
    return lst

def get_lst4():
    lst = [{'index': 0, 'independent': {'a': 1, 'b': 1}, 'dependent': {'c': [1, 2], 'd': [12, 30]}},
           {'index': 1, 'independent': {'a': 1, 'b': 2}, 'dependent': {'c': [1, 2], 'd': [13, 31]}},
           {'index': 4, 'independent': {'a': 2, 'b': 1}, 'dependent': {'c': [1, 2], 'd': [16, 34]}},
           {'index': 7, 'independent': {'a': 2, 'b': 2}, 'dependent': {'c': [1, 2], 'd': [19, 37]}}]
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

    def test_tabulate2b(self):
        t = Tabulator()
        box = Box(get_lst2())
        index = ['c']
        columns = ['a', 'b']
        values = 'd'
        pt = t.tabulate(box=box, values=values, columns=columns, index=index)
        expected = 'a   1       2    \nb   1   2   1   2\nc                \n1  12  13  16  19\n2  30  31  34  37'
        self.assertEqual(str(pt), expected)

    def test_tabulate_store(self):
        t = Tabulator()
        box = Box(get_lst2_b())
        store = Store()
        key_d = store.new('d', components=['x', 'y'])
        index = ['a', 'b']
        columns = []
        values = store[key_d].subkeys
        pt = t.tabulate(box=box, values=values, columns=columns, index=index, store=store)
        expected = '''     d - x  d - y
a b              
1 1     12     30
  2     13     31
2 1     16     34
  2     19     37'''
        self.assertEqual(str(pt), expected)

    def test_tabulate_store2(self):
        # TODO: FIX
        t = Tabulator()
        box = Box(get_lst2_b())
        store = Store()
        key_d = store.new('d', components=['x', 'y'])
        index = []
        columns = ['a', 'b']
        values = store[key_d].subkeys
        pt = t.tabulate(box=box, values=values, columns=columns, index=index, store=store)
        print(pt)
        expected = '''     d - x  d - y
a b              
1 1     12     30
  2     13     31
2 1     16     34
  2     19     37'''
        # self.assertEqual(str(pt), expected)

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
        
    def test_vector_table(self):
        t = Tabulator()
        box = Box(get_lst4())
        values = 'd'
        index = 'c'
        index_vals = [1, 2]
        df = t.vector_table(box, values, index, index_vals)
        expected = '''a     1           2      
b     1     2     1     2
1  12.0  13.0  16.0  19.0
2  30.0  31.0  34.0  37.0'''
        self.assertEqual(expected, str(df))
        
    def test_vector_table_cols(self):
        t = Tabulator()
        box = Box(get_lst4())
        values = 'd'
        index = 'c'
        index_vals = [1, 2]
        df = t.vector_table(box, values, index, index_vals, orient='cols')
        expected = '''        1     2
a b            
1 1  12.0  30.0
  2  13.0  31.0
2 1  16.0  34.0
  2  19.0  37.0'''
        self.assertEqual(expected, str(df))
        
        
