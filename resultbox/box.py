# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 08:47:07 2019

@author: Reuben
"""

import hashlib

def listify(obj):
    if not isinstance(obj, list):
        return [obj]
    else:
        return obj

def to_bytes(obj):
    if isinstance(obj, str):
        return bytes(obj, 'utf-8')
    return bytes(obj)

def hash_dict(dct):
    h = hashlib.md5()
    for k, v in dct.items():
        h.update(to_bytes(k))
        h.update(to_bytes(v))
    return h.digest()

class Box(list):
        
    def add(self, dct, key, value):
        self.append({'index': len(self),
                    'independent': dct.copy(),
                    'key': key,
                    'value': value})
        
    def filter(self, keys):
        def filt_func(d):
            return all([k in d['independent'] or k == d['key'] for k in listify(keys)])
        return filter(filt_func, self)
    
    def filtered(self, keys):
        return [row for row in self.filter(keys)]
    
    def iwhere(self, dct=None, **kwargs):
        dct = {} if dct is None else dct
        m = {**dct, **kwargs}
        def filt_func(d):
            return all([v == d['independent'].get(k, d.get('value', False))
                            for k, v in m.items()])
        return filter(filt_func, self)
    
    def where(self, dct=None, **kwargs):
        return [row for row in self.iwhere(dct, **kwargs)]
    
    def combined(self, lst=None):
        lst = self if lst is None else lst
        d = {}
        for dct in lst:
            independent = dct['independent']
            h = hash_dict(independent)
            if h not in d:
                d[h] = independent.copy()
            d[h][dct['key']] = dct['value']
        return [c for key, c in d.items()]
    
    