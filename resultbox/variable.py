# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 14:27:27 2019

@author: Reuben
"""

def expand(dct, store):
    out = {}
    for key, val in dct.items():
        if isinstance(val, dict):
            out[key] = expand(val, store)
        else:
            if key in store:
                if store[key].components is not None:
                    subkeys = store[key].subkeys
                    if len(val) == len(subkeys):
                        for subkey, v in zip(subkeys, val):
                            out[subkey] = v
                        continue
            out[key] = val
    return out


class Store(dict):
    def new(self, name, doc=None, unit=None, components=None, sep=' - ',
            category=None, tags=None):
        if name in self:
            raise KeyError('Key "' + str(name) + '" already exists. Names '
                          + 'must be unique.')
        new = Variable(name, doc, unit, components=components, sep=sep,
                       category=category, tags=tags)
        self[new.key] = new
        return new.key
    

class Variable():
    def __init__(self,
                 name,
                 doc=None,
                 unit=None,
                 components=None,
                 sep=' - ',
                 category=None,
                 tags=None):
        self.name = name
        self.doc = name if doc is None else doc
        self.unit = unit
        self.components = components
        self.sep = sep
        self.category = category
        self.tags = [] if tags is None else tags
        self.key = self._append_unit(self.name)
        
    def __str__(self):
        return self.key
    
    def _append_unit(self, string):
        if self.unit is not None:
            return string + ' [' + self.unit + ']'
        else:
            return string
    
    def _component_name(self, component):
        component_name = self.name + self.sep + component
        return self._append_unit(component_name)
    
    @property
    def subkeys(self):
        ''' Return a list of keys for the variable, including components '''
        if self.components is None:
            return None
        component_names = []
        for component in self.components:
            component_names.append(self._component_name(component))
        return component_names
    
    def __getitem__(self, component):
        if component in self.components:
            return self._component_name(component)
    
        
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

