# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 21:22:35 2019

@author: Reuben
"""

import json
import zlib
import numpy as np

from .box import Box

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
        
    def _load(self, source, handler=None, **kwargs):
        if handler is not None:
            return self.handlers[handler].load(source, **kwargs)
        if self.specified is not None:
            return self.handlers[self.specified].load(source, **kwargs)
        for k, handler in self.handlers.items():
            if handler.suitable(source, **kwargs):
                return handler.load(source, **kwargs)
        f = source + '.cbox'
        return self.handlers[self.default_handler].load(f, **kwargs)

    def load(self, source, handler=None, as_box=True, **kwargs):
        ret = self._load(source, handler, **kwargs)
        if as_box:
            return Box(ret)
        else:
            return ret

    def save(self, box, target, handler=None, **kwargs):
        if handler is not None:
            return self.handlers[handler].save(box, target, **kwargs)
        if self.specified is not None:
            return self.handlers[self.specified].save(box, target, **kwargs)
        for k, handler in self.handlers.items():
            if handler.suitable(target, **kwargs):
                return handler.save(box, target, **kwargs)
        f = target + '.cbox'
        return self.handlers[self.default_handler].save(box, f, **kwargs)


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return {'__ndarray__': obj.tolist(), 'dtype': str(obj.dtype)}
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

def np_decode(dct):
    if '__ndarray__' in dct:
        return np.array(dct['__ndarray__'], dtype=dct['dtype'])
    return dct
    

class JSON():
    def suitable(self, fname, **kwargs):
        if fname.endswith('.box'):
            return True
        
    def save(self, box, fname, **kwargs):
        with open(fname, mode='w') as f:
            jsn = json.dumps(list(box), cls=JSONEncoder)
            f.write(jsn)
    
    def load(self, fname, **kwargs):
        with open(fname, mode='r') as f:
            jsn = f.read()
        lst = json.loads(jsn, object_hook=np_decode)
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
            jsn = json.dumps(list(box), cls=JSONEncoder)
            compressed = zlib.compress(jsn.encode(), level=9)
            f.write(compressed)
    
    def load(self, fname, **kwargs):
        with open(fname, mode='rb') as f:
            compressed = f.read()
            jsn = zlib.decompress(compressed).decode()
        lst = json.loads(jsn, object_hook=np_decode)
        for row in lst:
            row['dependent'] = dict(row['dependent'])
            row['independent'] = dict(row['independent'])
        lst = [dict(row) for row in lst]
        return lst
            
            
manager = Manager()
load = manager.load
save = manager.save
