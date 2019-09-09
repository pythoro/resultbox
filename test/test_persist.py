# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 21:44:10 2019

@author: Reuben
"""

import unittest
import tempfile
import os

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

class Test_JSON(unittest.TestCase):
    def test_uncompresed_save_load(self):
        box = Box(get_lst())
        with tempfile.TemporaryDirectory() as tmpdirname:
            fname = os.path.join(tmpdirname, 'test.box')
            save(box, fname)
            box_check = load(fname)
        self.assertListEqual(box, box_check)

    def test_compressed_save_load(self):
        box = Box(get_lst())
        with tempfile.TemporaryDirectory() as tmpdirname:
            fname = os.path.join(tmpdirname, 'test.cbox')
            save(box, fname, compression=True)
            box_check = load(fname)
        self.assertListEqual(box, box_check)

        