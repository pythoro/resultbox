# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 08:51:40 2019

@author: Reuben
"""

import unittest
import numpy as np

from resultbox import utils


class Test_Interp(unittest.TestCase):
    def test_cosort_tuple(self):
        xs = (0, 1, 2, 1, 2, 3)
        ys = (5, 8, 10, 6, 7, 9)
        xs_sorted, ys_sorted = utils.cosort(xs, ys)
        self.assertSequenceEqual(xs_sorted, (0, 1, 2 ,3))
        self.assertSequenceEqual(ys_sorted, (5, 8, 10, 9))

    def test_cosort_list(self):
        xs = [0, 1, 2, 1, 2, 3]
        ys = [5, 8, 10, 6, 7, 9]
        xs_sorted, ys_sorted = utils.cosort(xs, ys)
        self.assertListEqual(xs_sorted, [0, 1, 2 ,3])
        self.assertListEqual(ys_sorted, [5, 8, 10, 9])
    
    def test_cosort_ndarray(self):
        xs = np.array([0, 1, 2, 1, 2, 3])
        ys = np.array([5, 8, 10, 6, 7, 9])
        xs_sorted, ys_sorted = utils.cosort(xs, ys)
        self.assertTrue(np.array_equal(xs_sorted, np.array([0, 1, 2 ,3])))
        self.assertTrue(np.array_equal(ys_sorted, np.array([5, 8, 10, 9])))

    def test_interp(self):
        xs = np.array([0, 1, 2, 3])
        ys = np.array([5, 6, 7, 8])
        xs_new = np.array([-0.5, 0.5, 1.5, 2.5, 3.5])
        ys_new = utils.interp(xs, ys, xs_new)
        expected = np.array([5.0, 5.5, 6.5, 7.5, 8.0])
        self.assertTrue(all(np.isclose(expected, ys_new)))


class Test_Val_To_Str(unittest.TestCase):
    def test_str(self):
        self.assertEqual('test', utils.val_to_str('test'))
        
    def test_int(self):
        self.assertEqual('56', utils.val_to_str(56))
        
    def test_signed_int(self):
        self.assertEqual('-56', utils.val_to_str(-56))
        
    def test_float(self):
        self.assertEqual('4.6', utils.val_to_str(4.6))

    def test_float_2(self):
        self.assertEqual('4', utils.val_to_str(4.0))
        
    def test_ndarray_int(self):
        self.assertEqual('[1 2]', utils.val_to_str(np.array([1, 2])))
        
    def test_ndarray_float(self):
        self.assertEqual('[1.5 2]', utils.val_to_str(np.array([1.5, 2.0])))


class Test_List_To_Str(unittest.TestCase):
    def test_list(self):
        self.assertEqual('[4 5.6]', utils.val_to_str([4, 5.6]))
        
        
class Test_Dict_To_Str(unittest.TestCase):
    def test_str(self):
        d = {'apple': 5.7, 'banana': 7.8}
        expected = 'apple 5.7 banana 7.8'
        self.assertEqual(expected, utils.dict_to_str(d))
