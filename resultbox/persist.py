# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 21:22:35 2019

@author: Reuben
"""

from .box import Box
import json_tricks
import os

def ensure_ext(fname, ext='.box'):
    if fname.endswith(ext):
        return fname
    else:
        return fname + ext


class JSON():
    def save(self, box, fname, compression=True):
        mode = 'wb' if compression else 'w'
        ext = '.cbox' if compression else '.box'
        with open(ensure_ext(fname, ext), mode=mode) as f:
            json_tricks.dump(list(box), f, compression=compression)
        
    
    def load(self, fname):
        compressed =  os.path.isfile(ensure_ext(fname, '.cbox'))
        ext = '.cbox' if compressed else '.box'
        mode = 'rb' if compressed else 'r'
        with open(ensure_ext(fname, ext), mode=mode) as f:
            lst = json_tricks.load(f)
        # Tidy up from the default OrderedDict of json-tricks,
        # Now dicts are ordered in Python 3.7+.
        for row in lst:
            row['independent'] = dict(row['independent'])
        lst = [dict(row) for row in lst]
        return Box(lst)
    
    
handler = JSON()
save = handler.save
load = handler.load

def set_handler(cls):
    global handler, save, load
    handler = cls()
    save = handler.save
    load = handler.load