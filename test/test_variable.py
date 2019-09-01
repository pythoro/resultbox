# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 20:04:58 2019

@author: Reuben
"""

import unittest

from resultbox import Variable

class Test_Variable(unittest.TestCase):
    def test_init(self):
        name = 'a'
        desc = 'b'
        unit = 'c'
        v = Variable(name, desc, unit)
        self.assertEqual(v.name, name)
        self.assertEqual(v.desc, desc)
        self.assertEqual(v.unit, unit)
        