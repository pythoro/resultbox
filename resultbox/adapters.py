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
    

def compose(flat, root=None, reverse_keys=None, val=None, sep='\\'):
    if root is None:
        k, v = flat.copy().popitem()
        keys = k.split(sep)
        _, is_dict = _interpret(keys[0])
        root = {} if is_dict else []
    for k, v in flat.items():
        reverse_keys = k.split(sep)
        reverse_keys.reverse()
        _assign(root, reverse_keys, v)
    return root

def _assign(current, reverse_keys, val):
    key = reverse_keys.pop()
    k, is_dict = _interpret(key)
    if len(reverse_keys) == 0:
        _safe_assign(current, k, val)
        return
    next_k, should_be_in_dict = _interpret(reverse_keys[0])
    new_current = _safe_sub(current, should_be_in_dict, k)
    _assign(new_current, reverse_keys, val)

def _interpret(key):
    if key.startswith('__key__'):
        is_dict = True
        new = key.lstrip('__key__')
    elif key.startswith('__ind__'):
        is_dict = False
        new = int(key.lstrip('__ind__'))
    return new, is_dict
            
def _safe_assign(obj, ind, val):
    if isinstance(obj, list):
        if ind >= len(obj):
            obj += [None]*(ind - len(obj) + 1)
    obj[ind] = val
    
def _safe_sub(obj, is_dict, key):
    new_obj = {} if is_dict else []
    if isinstance(obj, dict):
        if key not in obj:
            obj[key] = new_obj
    else:
        if key >= len(obj):
            obj += [None]*(key - len(obj) + 1)
        if obj[key] is None:
            obj[key] = new_obj
    return obj[key]
