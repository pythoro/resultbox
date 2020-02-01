# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 14:27:27 2019

@author: Reuben

Variables help resultbox know how to interpret and display data. Sometimes,
variables have different components, like x, y, and z coordinates. They
often have units, such as meters. 

The idea is that we define a variable just once. Whenever we add in some
data for that variable to a Box, we also pass in that variable. Then, we
can let resultbox take care of the rest. 

"""

from difflib import SequenceMatcher
from . import utils

def _expand_single(key, val, store, specified=None):
    ''' Expand a value into its components 
    
    Args:
        key (Variable): The variable key
        val: The data for that variable
        store (Store): The variable store
        
    Returns:
        dict: A dictionary of keys and values. If the variables has components,
        the dictionary contains the component keys and component values.
    '''
    if isinstance(val, dict):
        r = expand(val, store)
        return {key: r}
    else:
        if key in store:
            if specified is not None and key not in specified:
                return {key, val}
            if store[key].subkeys is not None:
                subkeys = store[key].subkeys
                if len(val) == len(subkeys):
                    out = {}
                    for subkey, v in zip(subkeys, val):
                        out[subkey] = v
                    return out
        return {key: val}

def expand(source, store, specified=None):
    ''' Expand variable components within a list or dictionary recursively 
    
    Args:
        source (list or dict): The source list (of dictionaries) or dictionary.
        The keys must exist in the store.
        store (Store): The corresponding Store instance.
        
    Returns:
        list or dict: The expanded list or dictionary.
    '''
    if isinstance(source, list):
        out = []
        for val in source:
            r = expand(val, store)
            out.append(r)
    elif isinstance(source, dict):
        out = {}
        for key, val in source.items():
            out.update( _expand_single(key, val, store, specified))
    return out


class Store(dict):
    ''' A store is a container for Variables  '''
    def new(self, name, doc=None, unit=None, components=None, sep=' - ',
            category=None, tags=None):
        ''' Create a new variable 
        
        Args:
            name (str): The variable name
            doc (str): A documentation string. Defaults to None.
            unit (str): The units of the variable (usually abbreviated).
            Defaults to None.
            components (list[str]): A list of names for each
            component. Defaults to None.
            sep (str): The separator between the name and any component names.
            category (str): An optional category
            tags (list[str]): Optional tags
            
        Returns:
            Variable: The new variable
            
        Note:
            The 'add' method is a copy of this method.
        '''
        new = Variable(name, doc, unit, components=components, sep=sep,
                       category=category, tags=tags)
        if new.key in self:
            raise KeyError('Key "' + str(name) + '" already exists. Names '
                          + 'must be unique.')
        self[new.key] = new
        return new
    
    def nearest(self, key):
        ''' Return the variable that best best-matches the input string
        
        Args:
            key (str): The input string
            
        Returns:
            Variable: The variable with the key that best matches the input
        '''
        keys = list(self.keys())
        ratios = [SequenceMatcher(None, key, k).ratio() for k in keys]
        return self[keys[ratios.index(max(ratios))]]
    
    add = new

class Variable(str):
    ''' Metadata for specific data 
    
    Args:
        name (str): The name of the variable
        doc (str): A documentation string. Defaults to None.
        unit (str): The units of the variable (usually abbreviated).
        Defaults to None.
        components (list[str]): A list of names for each
        component. Defaults to None.
        sep (str): The separator between the name and any component names.
        category (str): An optional category
        tags (list[str]): Optional tags
        
    Note:
        Variables subclass `str`, so they can be used like strings. Care is
        needed when serialising and deserialising them, as otherwise their
        special attributes will be lost.
    '''
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
        self.tags = None if tags is None else utils.listify(tags)
        self.key = self._append_unit(self.name, self.unit)
        
    def to_dict(self):
        ''' Create a dictionary containing the Variable attributes '''
        d = {'name': self.name,
                'doc': self.doc,
                'unit': self.unit,
                'components': self.components,
                'sep': self.sep,
                'category': self.category,
                'tags': self.tags}
        return d
    
    @classmethod
    def from_dict(cls, dct):
        ''' Create a new Variable instance from a dictionary of attributes '''
        return cls(**dct)
    
    def to_str(self):
        ''' Create a string containing the Variable attributes '''
        dct = self.to_dict()
        return utils.dict_to_str(dct, val_sep='=', key_sep=';')
    
    @classmethod
    def from_str(cls, s):
        ''' Create a new Variable instance from a string of attributes '''
        d = utils.str_to_dict(s, val_sep='=', key_sep=';')
        return cls.from_dict(d)
    
    def __str__(self):
        return self.key

    @classmethod
    def _append_unit(cls, string, unit):
        ''' Add the unit to the string '''
        if unit is not None:
            return string + ' [' + unit + ']'
        else:
            return string
    
    def _component_name(self, component):
        ''' Get the full key for a component '''
        component_name = self.name + self.sep + component
        return self._append_unit(component_name, self.unit)
    
    @property
    def subkeys(self):
        ''' Return a list of keys for the variable components '''
        if self.components is None:
            return None
        keys = []
        for component in self.components:
            keys.append(self._component_name(component))
        return keys

    @property
    def label(self):
        ''' The variable name formatted with a trailing colon '''
        return self.name + ':'
    
    def __getitem__(self, component):
        if not isinstance(component, str):
            return super().__getitem__(component)
        if component in self.components:
            return self._component_name(component)
        else:
            return super().__getitem__(component)
    
        
class Aliases(dict):
    ''' Variables allow other keys to be used as aliases for variables 
    
    This class is a subclass of `dict`. It is designed so that each key
    is an alias, and its value is the corresponding variable. The Aliases
    instance provides methods to 'translate' (swap) aliases within standard
    data structures to be their corresponding variables.
    '''
    def __init__(self, data):
        self.update(data)
        
    def __missing__(self, key):
        return key

    def translate(self, obj):
        ''' Recusively translate an object, swapping any dictionary keys '''
        if obj is None:
            return None
        if isinstance(obj, str):
            return self.translate_str(obj)
        elif isinstance(obj, list):
            return self.translate_list(obj)
        elif isinstance(obj, dict):
            return self.translate_dict(obj)
        else:
            return obj

    def translate_str(self, s):
        ''' Translate a string '''
        return self[s]

    def translate_dict_vals(self, dct):
        ''' Translate the values in a dictionary '''
        return {k: self.translate(v) for k, v in dct.items()}
        
    def translate_dict(self, dct):
        ''' Translate the keys in a dictionary '''
        return {self[k]: self.translate(v) for k, v in dct.items()}

    def translate_list(self, lst):
        ''' Translate the objects in a list '''
        return [self.translate(k) for k in lst]

