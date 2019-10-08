# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 08:47:07 2019

@author: Reuben
"""

import hashlib
import numpy as np
from .utils import listify, dict_to_str

def hashable(obj):
    return bytes(str(obj), 'utf-8')

def hash_dict(dct):
    h = hashlib.md5()
    def update(d):
        for k, v in d.items():
            h.update(hashable(k))
            if isinstance(v, dict):
                update(v)
            else:
                h.update(hashable(v))
    update(dct)
    return h.digest()


class Box(list):
    def __init__(self, lst=None):
        self._combined = {}
        if lst is not None:
            super().__init__(lst)
            for row in lst:
                self._combine(row)
        
    def add(self, indep, key=None, value=None, dep=None,
            keys=None, values=None, **kwargs):
        ''' Add a new entry '''
        if key is not None and value is not None:
            if isinstance(key, str):
                self.add_value(indep, key, value)
            elif isinstance(key, list):
                self.add_array(indep, key, value)
        elif keys is not None and values is not None:
            self.add_array(indep, keys, values)
        elif dep is not None:
            self.add_dict(indep, dep)
        elif isinstance(key, dict):
            self.add_dict(indep, key)
        elif len(kwargs) > 0:
            self.add_dict(indep, kwargs)
        
    def add_value(self, indep, key, value):
        self.add_dict(indep, {key: value})
        
    def add_dict(self, indep, dep):
        dfull = {'index': len(self),
                 'independent': indep.copy(),
                 'dependent': dep}
        self.append(dfull)
        self._combine(dfull)
        
    def add_array(self, indep, keys, values):
        ''' Add an array of values 
        
        Args:
            indep (dict): A dictionary of independent key-value pairs
            keys (list): A list of keys
            values (arraylike): The values. Rows must correspond with the keys.
        '''
        if len(keys) != len(values):
            raise KeyError('Keys do not match with rows of values.')
        dep = {k: v for k, v in zip(keys, values)}
        self.add_dict(indep, dep)
        
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
    
    def _merge(self, box_list):
        if isinstance(box_list, self.__class__):
            box_list = [box_list]
        for box in box_list:
            for row in box:
                row['index'] = len(self)
                self.append(row)
                self._combine(row)
    
    def merge(self, box, in_place=True):
        ''' Merge with one or more other boxes 
        
        Args:
            box (Box): A Box instance of list of Box instances.
            in_place(bool): Either merge in place or return a new Box.
        '''
        if in_place:
            self._merge(box)
        else:
            base = self.copy()
            base._merge(box)
            return base
    
    def vectors(self, keys, dct=None, labels='str'):
        keys = listify(keys)
        combined = self.combined()
        filtered = self.filtered(keys, lst=combined)
        if dct is not None:
            filtered = self.where(dct, filtered)
        out = {k: [] for k in keys}
        label_list = []
        for dct in filtered:
            if labels=='str':
                label = dict_to_str(dct['independent'],
                                             val_sep='=',
                                             key_sep=', ')
            else:
                label = dct['independent']
            label_list.append(label)
            dep = dct['dependent']
            for k in keys:
                out[k].append(dep[k])
        return [out[k] for k in keys], label_list
    
    def find(self, key, lst=None):
        lst = self if lst is None else lst
        out = {}
        for row in lst:
            if key in row['dependent']:
                out[row['index']] = row['dependent'][key]
            elif key in row['independent']:
                out[row['index']] = row['independent'][key]
        return out
    
    def item(self, index, key):
        row = self[index]
        if key in row['dependent']:
            return row['dependent'][key]
        elif key in row['independent']:
            return row['independent'][key]
        else:
            raise KeyError
    
    def __getitem__(self, keys):
        if isinstance(keys, int):
            return super().__getitem__(keys)
        elif isinstance(keys, list):
            return self.vectors(keys)
        elif isinstance(keys, str):
            return self.find(keys)
        elif isinstance(keys, tuple):
            return self.item(keys[0], keys[1])
    
    def copy(self):
        return Box(self)
        
    def __str__(self):
        def f(v):
            if np.size(v) == 1:
                return str(v)
            elif np.size(v) > 1:
                return str(np.shape(v))
            else:
                return str(v)
        
        def buffer(l, m, n=25):
            end = len(l) - 1
            buffered = []
            for i in range(m):
                if i > end:
                    buffered.append(''.ljust(n))
                else:
                    buffered.append(l[i].ljust(n))
            return buffered
        
        out = ['index'.ljust(7) +
               'independent'.ljust(50) +
                'dependent'.ljust(50)]
        for row in self:
            ind = [str(row['index'])]
            dep = [k + ': ' + f(v) for k, v in row['dependent'].items()]
            indep = [k + ': ' + f(v) for k, v in row['independent'].items()]
            m = max(len(dep), len(indep), 1)
            ind = buffer(ind, m, 7)
            dep = buffer(dep, m, 50)
            indep = buffer(indep, m, 50)
            for a, b, c in zip(ind, indep, dep):
                out.append(a + b + c)
            out.append('')
        return '\n'.join(out)
    
    def __repr__(self):
        return self.__str__()
    
    def keys(self, dependent=True, independent=False):
        out = set()
        for row in self:
            if independent:
                out.update(row['independent'].keys())
            if dependent:
                out.update(row['dependent'].keys())
        return out
        
    