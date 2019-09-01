# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 08:47:07 2019

@author: Reuben
"""



class Box(list):
        
    def add(self, dct, key, value):
        d = {}
        d['index'] = len(self)
        d.update(dct)
        d[key] = value
        self.append(d)
        
    