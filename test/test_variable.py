# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 20:04:58 2019

@author: Reuben
"""

import unittest

from resultbox import Store, Variable, Aliases
from resultbox import variable

class Test_Expand(unittest.TestCase):
    def test_expand_basic(self):
        s = Store()
        key_a = s.new('a', components=['x', 'y'])
        dct = {key_a: [0, 1]}
        out = variable.expand(dct, s)
        expected = {'a - x': 0, 'a - y': 1}
        self.assertDictEqual(out, expected)

    def test_expand_nested(self):
        s = Store()
        key_a = s.new('a', components=['x', 'y'])
        dct = {'dependent': {'another_level': {key_a: [0, 1]}}}
        out = variable.expand(dct, s)
        expected = {'dependent': {'another_level': {'a - x': 0, 'a - y': 1}}}
        self.assertDictEqual(out, expected)


class Test_Store(unittest.TestCase):
    def test_new(self):
        s = Store()
        name = 'a'
        doc = 'b'
        unit = 'c'
        v = s.new(name, doc, unit)
        v_check = Variable(name, doc, unit)
        self.assertEqual(str(v_check), str(v))
        self.assertTrue(v in s)
        self.assertEqual(str(s[v]), str(v))

class Test_Variable(unittest.TestCase):
    def test_init(self):
        name = 'a'
        doc = 'b'
        unit = 'c'
        v = Variable(name, doc, unit)
        self.assertEqual(v.name, name)
        self.assertEqual(v.doc, doc)
        self.assertEqual(v.unit, unit)
        
    def test_str(self):
        name = 'a'
        doc = 'b'
        unit = 'mm'
        v = Variable(name, doc, unit)
        self.assertEqual(str(v), 'a [mm]')
        
    def test_components_getitem(self):
        name = 'a'
        doc = 'b'
        unit = 'mm'
        xyz = ['x', 'y', 'z']
        sep = ' - '
        v = Variable(name, doc, unit, components=xyz, sep=sep)
        self.assertEqual(v['x'], 'a - x [mm]')
        
    def test_components_key(self):
        name = 'a'
        doc = 'b'
        unit = 'mm'
        xyz = ['x', 'y', 'z']
        sep = ' - '
        v = Variable(name, doc, unit, components=xyz, sep=sep)
        self.assertEqual(v.key, 'a [mm]')
        
    def test_components_keys(self):
        name = 'a'
        doc = 'b'
        unit = 'mm'
        xyz = ['x', 'y', 'z']
        sep = ' - '
        v = Variable(name, doc, unit, components=xyz, sep=sep)
        keys = ['a - x [mm]', 'a - y [mm]', 'a - z [mm]']
        self.assertListEqual(v.subkeys, keys)
        
        
class Test_Aliases(unittest.TestCase):
    def test_init(self):
        dct = {'a': 'something'}
        a = Aliases(dct)
        self.assertDictEqual(a, dct)

    def test_translate_str(self):
        dct = {'a': 'something'}
        a = Aliases(dct)
        s = 'a'
        ret = a.translate(s)
        expected = 'something'
        self.assertEqual(ret, expected)
        
    def test_translate_dict(self):
        dct = {'a': 'something'}
        a = Aliases(dct)
        d = {'a': 3}
        ret = a.translate(d)
        expected = {'something': 3}
        self.assertDictEqual(ret, expected)

    def test_translate_dict_vals(self):
        dct = {'a': 'something'}
        a = Aliases(dct)
        d = {'one': 'a'}
        ret = a.translate_dict_vals(d)
        expected = {'one': 'something'}
        self.assertDictEqual(ret, expected)

    def test_translate_list(self):
        dct = {'a': 'something'}
        a = Aliases(dct)
        lst = ['a']
        ret = a.translate(lst)
        expected = ['something']
        self.assertListEqual(ret, expected)
        
    def test_translate_dlist(self):
        dct = {'a': 'something', 'b': 'other'}
        a = Aliases(dct)
        lst = [{'a': 3, 'b': 5}, {'a': 7, 'b': 8}]
        ret = a.translate(lst)
        expected = [{'something': 3, 'other': 5}, {'something': 7, 'other': 8}]
        self.assertListEqual(ret, expected)
        
    def test_translate_dlist_variables(self):
        dct = {'a': Variable('one', 'blah', 'mm'),
               'b': Variable('two', 'blah2', 's')}
        a = Aliases(dct)
        lst = [{'a': 3, 'b': 5}, {'a': 7, 'b': 8}]
        ret = a.translate(lst)
        expected = [{'one [mm]': 3, 'two [s]': 5},
                     {'one [mm]': 7, 'two [s]': 8}]
        self.assertListEqual(ret, expected)