# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 21:44:10 2019

@author: Reuben
"""

import unittest
import tempfile
import os
import numpy as np

from resultbox import Box, load, save

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

def get_lst_2():
    lst = [{'index': 0, 'independent': {'a': 1, 'b': 1, 'c': 1}, 'dependent': {'d': np.array([0, 10])}},
           {'index': 1, 'independent': {'a': 1, 'b': 2, 'c': 2}, 'dependent': {'d': np.array([1, 11])}},
           {'index': 2, 'independent': {'a': 1, 'b': 2, 'c': 1}, 'dependent': {'d': np.array([2, 12])}},
           {'index': 3, 'independent': {'a': 1, 'b': 1, 'c': 2}, 'dependent': {'d': np.array([3, 13])}},
           {'index': 4, 'independent': {'a': 2, 'b': 1, 'c': 1}, 'dependent': {'d': np.array([4, 14])}},
           {'index': 5, 'independent': {'a': 2, 'b': 1, 'c': 2}, 'dependent': {'d': np.array([5, 15])}},
           {'index': 6, 'independent': {'a': 2, 'b': 2, 'c': 1}, 'dependent': {'d': np.array([6, 16])}},
           {'index': 7, 'independent': {'a': 2, 'b': 2, 'c': 2}, 'dependent': {'d': np.array([7, 17])}}]
    return lst

def get_box_check(box, fname):
    with tempfile.TemporaryDirectory() as tmpdirname:
        fname = os.path.join(tmpdirname, fname)
        save(box, fname)
        box_check = load(fname)
    return box_check
            

class Test_JSON(unittest.TestCase):
    def test_uncompresed_save_load(self):
        box = Box(get_lst())
        box_check = get_box_check(box, 'test.box')
        self.assertListEqual(box, box_check)

    def test_uncompresed_save_load_np_array(self):
        box = Box(get_lst_2())
        box_check = get_box_check(box, 'test.box')
        self.assertEqual(str(list(box)), str(list(box_check)))


class Test_CJSON(unittest.TestCase):
    def test_compressed_save_load(self):
        box = Box(get_lst())
        box_check = get_box_check(box, 'test.cbox')
        self.assertListEqual(box, box_check)

    def test_compressed_save_load_np_array(self):
        box = Box(get_lst_2())
        box_check = get_box_check(box, 'test.cbox')
        self.assertEqual(str(list(box)), str(list(box_check)))
        

class Test_NPZ(unittest.TestCase):
    def test_compressed_save_load(self):
        box = Box(get_lst())
        box_check = get_box_check(box, 'test.npz')
        self.assertListEqual(box, box_check)

    def test_compressed_save_load_np_array(self):
        box = Box(get_lst_2())
        box_check = get_box_check(box, 'test.npz')
        self.assertEqual(str(list(box)), str(list(box_check)))        