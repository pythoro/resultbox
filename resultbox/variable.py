# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 14:27:27 2019

@author: Reuben
"""


class Store(dict):
    def new(self, name, desc, unit):
        new = Variable(name, desc, unit)
        self[name] = new
        return str(new)
    
    

class Variable(dict):
    def __init__(self, name, desc, unit):
        self.name = name
        self.desc = desc
        self.unit = unit
        
    def __str__(self):
        return self.name + ' [' + self.unit + ']'
    
        
class Aliases(dict):
    def __init__(self, data):
        self.update(data)
        
    def __missing__(self, key):
        return key

    def translate(self, obj):
        if obj is None:
            return None
        if isinstance(obj, str):
            return self.translate_str(obj)
        elif isinstance(obj, list):
            return self.translate_list(obj)
        elif isinstance(obj, dict):
            return self.translate_dict(obj)

    def translate_str(self, s):
        return str(self[s])

    def translate_dict_vals(self, dct):
        return {k: str(self[v]) for k, v in dct.items()}
        
    def translate_dict(self, dct):
        return {str(self[k]): v for k, v in dct.items()}

    def translate_list(self, lst):
        return [self.translate(k) for k in lst]

