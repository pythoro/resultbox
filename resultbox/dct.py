# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 14:27:38 2019

@author: Reuben
"""

class Dict(dict):
    def subdict(self, key, val):
        dct = Dict(self)
        dct[key] = val
        return dct
    
    def copy(self):
        return Dict(self)