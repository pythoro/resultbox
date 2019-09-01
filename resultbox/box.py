# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 08:47:07 2019

@author: Reuben
"""


def listify(obj):
    if not isinstance(obj, list):
        return [obj]
    else:
        return obj

class Box(list):
        
    def add(self, dct, key, value):
        d = {}
        d['index'] = len(self)
        d.update(dct)
        d[key] = value
        self.append(d)
        
    def filter(self, keys):
        def filt_func(d):
            return all([k in d for k in listify(keys)])
        return filter(filt_func, self)
    
    def filtered(self, keys):
        return [row for row in self.filter(keys)]
    
    def iwhere(self, dct=None, **kwargs):
        dct = {} if dct is None else dct
        m = {**dct, **kwargs}
        def filt_func(d):
            return all([v == d.get(k, False) for k, v in m.items()])
        return filter(filt_func, self)
    
    def where(self, dct=None, **kwargs):
        return [row for row in self.iwhere(dct, **kwargs)]