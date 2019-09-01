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