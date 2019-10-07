# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 14:27:27 2019

@author: Reuben
"""

def _expand_single(key, val, store, expanded=None):
    if isinstance(val, dict):
        r = expand(val, store)
        return {key: r}
    else:
        if key in store:
            if store[key].subkeys is not None:
                subkeys = store[key].subkeys
                if len(val) == len(subkeys):
                    out = {}
                    for subkey, v in zip(subkeys, val):
                        out[subkey] = v
                    return out
        return {key: val}

def expand(source, store):
    if isinstance(source, list):
        out = []
        for val in source:
            r = expand(val, store)
            out.append(r)
    elif isinstance(source, dict):
        out = {}
        for key, val in source.items():
            out.update( _expand_single(key, val, store))
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
        return new
    

class Variable(str):
    def __new__(cls,
               name,
               doc=None,
               unit=None,
               components=None,
               sep=' - ',
               category=None,
               tags=None):
        return super().__new__(cls, cls._append_unit(name, unit))
    
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
        self.key = self._append_unit(self.name, self.unit)
        
    def __str__(self):
        return self.key

    @classmethod
    def _append_unit(cls, string, unit):
        if unit is not None:
            return string + ' [' + unit + ']'
        else:
            return string
    
    def _component_name(self, component):
        component_name = self.name + self.sep + component
        return self._append_unit(component_name, self.unit)
    
    @property
    def subkeys(self):
        ''' Return a list of keys for the variable, including components '''
        if self.components is None:
            return None
        component_names = []
        for component in self.components:
            component_names.append(self._component_name(component))
        return component_names
    
    @property
    def label(self):
        return '(' + self.name + ')'
    
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

