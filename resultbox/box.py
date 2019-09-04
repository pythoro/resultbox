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
    def update(d):
        for k, v in d.items():
            h.update(to_bytes(k))
            if isinstance(v, dict):
                update(v)
            else:
                h.update(to_bytes(v))
    update(dct)
    return h.digest()

class Box(list):
        
    def add(self, dct, key=None, value=None, dep=None, **kwargs):
        d = {key: value} if key is not None and value is not None else {}
        if dep is not None:
            d.update(dep)
        d.update(kwargs)
        self.append({'index': len(self),
                    'independent': dct.copy(),
                    'dependent': d})
        
    def filter(self, keys, lst=None):
        if lst is None:
            lst = self
            filt_self = True
        else:
            filt_self = False
            
        def filt_func(d):
            if filt_self:
                return all([k in d['independent'] or k in d['dependent']
                            for k in listify(keys)])
            else:
                return all([k in d for k in listify(keys)])
            
        return filter(filt_func, lst)
    
    def filtered(self, keys, lst=None):
        return [row for row in self.filter(keys, lst)]
    
    def iwhere(self, dct=None, lst=None, **kwargs):
        dct = {} if dct is None else dct
        m = {**dct, **kwargs}
        if lst is None:
            lst = self
            filt_self = True
        else:
            filt_self = False
            
        def filt_func(d):
            if filt_self:
                return all([v == d['independent'].get(k, d['dependent'].get(k, None))
                            for k, v in m.items()])
            else:
                return all([v == d.get(k, None) for k, v in m.items()])
            
        return filter(filt_func, lst)
    
    def where(self, dct=None, lst=None, **kwargs):
        return [row for row in self.iwhere(dct, lst, **kwargs)]
    
    def combined(self, lst=None):
        lst = self if lst is None else lst
        d = {}
        for dct in lst:
            independent = dct['independent']
            h = hash_dict(independent)
            if h not in d:
                d[h] = independent.copy()
            d[h].update(dct['dependent'])
        return [c for key, c in d.items()]
    
    