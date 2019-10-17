# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:52:34 2019

@author: Reuben

Adapters in this module transform data structures between different formats.

"""

def flat_dict(obj, out=None, root=None, sep='\\'):
    out = {} if out is None else out
    if isinstance(obj, dict):
        _flat_dict_dict(obj, out=out, root=root, sep=sep)
    elif isinstance(obj, list):
        _flat_dict_list(obj, out=out, root=root, sep=sep)
    else:
        out[root] = obj
    return out

def _flat_dict_dict(dct, out=None, root=None, sep='\\'):
    base = '' if root is None else str(root) + sep
    out = {} if out is None else out
    for k, v in dct.items():
        new_root = base + '__key__' + str(k)
        flat_dict(v, out=out, root=new_root, sep=sep)

def _flat_dict_list(lst, out=None, root=None, sep='\\'):
    base = '' if root is None else str(root) + sep
    out = {} if out is None else out
    for i, v in enumerate(lst):
        new_root = base + '__ind__' + str(i)
        flat_dict(v, out=out, root=new_root, sep=sep)
    

def _assign(dct, reverse_keys, val):
    key = reverse_keys.pop()
    if len(reverse_keys) == 0:
        if key.startswith('__key__'):
            dct[key.lstrip('__key__')] = val
        else:
            dct[key] = val
    else:
        if key not in dct:
            dct[key]= {}
        _assign(dct[key], reverse_keys, val)

def compose_dct(flat_dict, sep='\\'):
    dct = {}
    for k, v in flat_dict.items():
        reverse_keys = k.split(sep)
        reverse_keys.reverse()
        _assign(dct, reverse_keys, v)
    return dct
    