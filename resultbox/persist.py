# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 21:22:35 2019

@author: Reuben
"""

import json_tricks


class Manager():
    default_handler = 'cbox'
    
    def __init__(self):
        self.handlers = {'box': JSON(),
                         'cbox': CJSON()}
        self.specified = None
        
    def add_handler(self, key, handler):
        self.handlers[key] = handler
        
    def specify(self, key):
        self.specified = key
        
    def load(self, source, handler=None, **kwargs):
        if handler is not None:
            return self.handlers[handler].load(source, **kwargs)
        if self.specified is not None:
            return self.handlers[self.specified].load(source, **kwargs)
        for k, handler in self.handlers.items():
            if handler.suitable(source, **kwargs):
                return handler.load(source, **kwargs)
            else:
                f = source + '.cbox'
                return self.handlers[self.default_handler].load(f, **kwargs)
        raise ValueError('No suitable load handler found for source: "'
                          + source + '"')

    def save(self, box, target, handler=None, **kwargs):
        if handler is not None:
            return self.handlers[handler].save(box, target, **kwargs)
        if self.specified is not None:
            return self.handlers[self.specified].save(box, target, **kwargs)
        for k, handler in self.handlers.items():
            if handler.suitable(target, **kwargs):
                return handler.save(box, target, **kwargs)
            else:
                f = target + '.cbox'
                return self.handlers[self.default_handler].save(box, f, **kwargs)
        raise ValueError('No suitable save handler found for target: "' 
                         + target + '"')


class JSON():
    def suitable(self, fname, **kwargs):
        if fname.endswith('.box'):
            return True
        
    def save(self, box, fname, **kwargs):
        with open(fname, mode='w') as f:
            json_tricks.dump(list(box), f, compression=False)
    
    def load(self, fname, **kwargs):
        with open(fname, mode='r') as f:
            lst = json_tricks.load(f)
        # Tidy up from the default OrderedDict of json-tricks,
        # Now dicts are ordered in Python 3.7+.
        for row in lst:
            row['dependent'] = dict(row['dependent'])
            row['independent'] = dict(row['independent'])
        lst = [dict(row) for row in lst]
        return lst


class CJSON():
    def suitable(self, fname, **kwargs):
        if fname.endswith('.cbox'):
            return True
        
    def save(self, box, fname, **kwargs):
        with open(fname, mode='wb') as f:
            json_tricks.dump(list(box), f, compression=True)
    
    def load(self, fname, **kwargs):
        with open(fname, mode='rb') as f:
            lst = json_tricks.load(f)
        # Tidy up from the default OrderedDict of json-tricks,
        # Now dicts are ordered in Python 3.7+.
        for row in lst:
            row['dependent'] = dict(row['dependent'])
            row['independent'] = dict(row['independent'])
        lst = [dict(row) for row in lst]
        return lst
            
            
manager = Manager()
load = manager.load
save = manager.save
