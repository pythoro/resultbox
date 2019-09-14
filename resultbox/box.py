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


def make_str(dct):
    out = [str(k) + '=' + str(v) for k, v in dct.items()]
    return ', '.join(out)


class Box(list):
    def __init__(self, lst=None):
        self._combined = {}
        if lst is not None:
            super().__init__(lst)
            for row in lst:
                self._combine(row)
        
    def add(self, dct, key=None, value=None, dep=None, **kwargs):
        d = {key: value} if key is not None and value is not None else {}
        if dep is not None:
            d.update(dep)
        d.update(kwargs)
        dfull = {'index': len(self),
                 'independent': dct.copy(),
                 'dependent': d}
        self.append(dfull)
        self._combine(dfull)
        
    def filter(self, keys, lst=None):
        if lst is None:
            lst = self
        if 'dependent' in lst[0] and 'independent' in lst[0]:
            filt_dep = True
        else:
            filt_dep = False
            
        def filt_func(d):
            if filt_dep:
                return all([k in d['independent'] or k in d['dependent']
                            for k in listify(keys)])
            else:
                return all([k in d for k in listify(keys)])
            
        return filter(filt_func, lst)
    
    def filtered(self, keys, lst=None):
        return [row for row in self.filter(keys, lst)]
    
    def iwhere(self, dct=None, lst=None, **kwargs):
        dct = {} if dct is None else dct
        m = dct.copy()
        m.update(kwargs)
        if lst is None:
            lst = self
        if 'dependent' in lst[0] and 'independent' in lst[0]:
            filt_dep = True
        else:
            filt_dep = False
            
        def filt_func(d):
            if filt_dep:
                return all([v == d['independent'].get(k, d['dependent'].get(k, None))
                            for k, v in m.items()])
            else:
                return all([v == d.get(k, None) for k, v in m.items()])
            
        return filter(filt_func, lst)
    
    def where(self, dct=None, lst=None, **kwargs):
        return [row for row in self.iwhere(dct, lst, **kwargs)]
    
    def minimal(self):
        combined = self._combined
        out = []
        for k, d in combined.items():
            dct = d['independent'].copy()
            dct.update(d['dependent'])
            out.append(dct)
        return out
    
    def _combine(self, dct):
        d = self._combined
        independent = dct['independent']
        h = hash_dict(independent)
        if h not in d:
            d[h] = {'independent': independent.copy(), 'dependent': {}}
        d[h]['dependent'].update(dct['dependent'])
    
    def combined(self):
        d = self._combined
        return [c for key, c in d.items()]
    
    def merge(self, box, in_place=True):
        def _merge(base_box, box):
            for row in box:
                row['index'] = len(base_box)
                base_box.append(row)
                base_box._combine(row)
        if in_place:
            _merge(self, box)
        else:
            base = self.copy()
            _merge(base, box)
            return base
    
    def vectors(self, keys, dct=None):
        keys = listify(keys)
        combined = self.combined()
        filtered = self.filtered(keys, lst=combined)
        if dct is not None:
            filtered = self.where(dct, filtered)
        out = {k: [] for k in keys}
        out['labels'] = []
        for dct in filtered:
            out['labels'].append(make_str(dct['independent']))
            dep = dct['dependent']
            for k in keys:
                out[k].append(dep[k])
        return [v for k, v in out.items()]
    
    def __getitem__(self, keys):
        if isinstance(keys, int):
            return super().__getitem__(keys)
        else:
            return self.vectors(keys)
    
    def copy(self):
        return Box(self)
        