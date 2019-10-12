# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 21:22:35 2019

@author: Reuben

The persist module helps the user save and load Box instances. It is
able to be extended for use with any handler.

"""

import json
import zlib
import numpy as np

from .box import Box

class Manager():
    ''' The manager looks after different classes that can process Box data.
    
    It provides two key methods - load and save.
    '''
    
    default_handler = 'cbox'
    
    def __init__(self):
        self.handlers = {'box': JSON(),
                         'cbox': CJSON()}
        self.specified = None
        
    def add_handler(self, key, handler):
        ''' Add a handler 
        
        Args:
            key (str): The unique name of the handler.
            handler (Handler): A Handler subclass.
        '''
        self.handlers[key] = handler
        
    def del_handler(self, key):
        ''' Delete a handler 
        
        Args:
            key (str): The unique name of the handler
        '''
        
    def specify(self, key):
        ''' Specify the handler to use '''
        self.specified = key
        
    def _load(self, source, handler=None, **kwargs):
        h = handler if handler is not None else None
        if h is None and self.specified is not None:
            h = self.specified
        if h is None:
            for k, handler in self.handlers.items():
                if handler.suitable(source, **kwargs):
                    h = handler
        if h is None:
            h = self.default_handler
            source += '.cbox'
        return h.load(source, **kwargs)

    def load(self, source, handler=None, as_box=True, **kwargs):
        ''' Return a new Box by reading the source 
        
        Args:
            source (str): The source to load from
            handler (str): Optional key specifying which handler to use
            as_box (bool): If true (the default), return a Box, otherwise
            return just the raw data.
            kwargs: Other keyword arguments passed to the handler.
        '''
        ret = self._load(source, handler, **kwargs)
        if as_box:
            return Box(ret)
        else:
            return ret

    def save(self, box, target, handler=None, **kwargs):
        ''' Save the Box data to the target 
        
        Args:
            box (Box): The Box instance.
            target (str): A string specifying the target
            handler (str): Optional key specifying which handler to use
            kwargs: Other keyword arguments passed to the handler.
        '''
        h = handler if handler is not None else None
        if h is None and self.specified is not None:
            h = self.specified
        if h is None:
            for k, handler in self.handlers.items():
                if handler.suitable(target, **kwargs):
                    h = handler
        if h is None:
            h = self.default_handler
            target += '.cbox'
        return h.save(box, target, **kwargs)


class Handler():
    ''' A handler that can load or save Box data '''
    
    def suitable(self, s, **kwargs):
        ''' Return true the handler suits the target/source string, s '''
        raise NotImplementedError

    def save(self, box, fname, **kwargs):
        ''' Save the box '''
        raise NotImplementedError
    
    def load(self, fname, **kwargs):
        ''' Load a box 
        
        Returns:
            list: The raw data for the Box
        '''
        raise NotImplementedError
        

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
    

class JSON(Handler):
    def suitable(self, fname, **kwargs):
        if fname.endswith('.box'):
            return True
        
    def save(self, box, fname, **kwargs):
        jsn = json.dumps(list(box), cls=JSONEncoder)
        with open(fname, mode='w') as f:
            f.write(jsn)
    
    def load(self, fname, **kwargs):
        with open(fname, mode='r') as f:
            jsn = f.read()
        lst = json.loads(jsn, object_hook=np_decode)
        return lst


class CJSON(Handler):
    def suitable(self, fname, **kwargs):
        if fname.endswith('.cbox'):
            return True
        
    def save(self, box, fname, **kwargs):
        jsn = json.dumps(list(box), cls=JSONEncoder)
        compressed = zlib.compress(jsn.encode(), level=9)
        with open(fname, mode='wb') as f:
            f.write(compressed)
    
    def load(self, fname, **kwargs):
        with open(fname, mode='rb') as f:
            compressed = f.read()
        jsn = zlib.decompress(compressed).decode()
        lst = json.loads(jsn, object_hook=np_decode)
        return lst
            
            
manager = Manager()
load = manager.load
save = manager.save
