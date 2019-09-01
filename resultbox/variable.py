# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 14:27:27 2019

@author: Reuben
"""

class Variable(dict):
    def __init__(self, name, desc, unit):
        self.name = name
        self.desc = desc
        self.unit = unit
        
        
class Aliases(dict):
    def __init__(self, data):
        self.update(data)
        
    def from_dict(self, dct):
        return {k: self[k] for k in dct.keys()}

    def from_list(self, lst):
        return {k: self[k] for k in lst}
