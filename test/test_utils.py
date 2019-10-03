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
