# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 14:27:38 2019

@author: Reuben
"""
    
class Dict_Container(dict):
    def __missing__(self, key):
        self[key] = {}
        return self[key]

dict_container = Dict_Container()

def get_dict(name):
    return dict_container[name]
