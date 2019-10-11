# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 21:12:24 2019

@author: Reuben
"""

import hashlib
import pandas as pd
from collections import defaultdict
from . import utils
from . import variable
import numpy as np

def encoded(obj):
    if isinstance(obj, str):
        return bytes(obj, 'utf-8')
    return bytes(obj)

def safe_hash(lst):
    h = hashlib.md5()
    for obj in lst:
        h.update(encoded(obj))
    return h.digest()
    
def listify(obj):
    if not isinstance(obj, list):
        return [obj]
    return obj


class Table():
    pass



class Tabulator():
    def guess_index(self, box, values, columns=None):
        def remove_others(keys):
            for v in values:
                keys.remove(v)
            for v in columns:
                keys.remove(v)
        
        values = listify(values)
        columns = [] if columns is None else listify(columns)
        minimal = box.minimal()
        filtered = box.filtered(values + columns, minimal)
        index = set()
        for row in filtered:
            keys = set(row.keys())
            remove_others(keys)
            index = index.union(keys)
        for row in filtered:
            keys = set(row.keys())
            remove_others(keys)
            if len(keys) == len(index):
                return [k for k in row.keys() if k in index]
        return list(index)
    
    def all_keys(self, *args):
        out = []
        for arg in args:
            l = listify(arg)
            out.extend([a for a in l if not a.endswith(':')])
        return out
    
    def _prepare_data(self, box, values, columns, index=None,
                 store=None):
        keys = self.all_keys(values, columns, index)
        minimal = box.minimal()
        if store is not None:
            minimal = variable.expand(minimal, store)
            new_keys = []
            for k in keys:
                if k in store:
                    if store[k].subkeys is not None:
                        new_keys.extend(store[k].subkeys)
                        continue
                new_keys.append(k)
        else:
            new_keys = keys
        filtered = box.filtered(new_keys, minimal)
        if len(filtered) == 0:
            raise ValueError('No records left in filtered results.')
        return filtered
    
    
    def tabulate(self, box, values, columns, index=None, aggfunc='mean',
                 aliases=None, store=None):
        ''' General purpose tabulation
        
        Can handle mixtures of scalars and vectors
        '''
        def indices(d):
            m = 1
            for key, val in d.items():
                if isinstance(val, list):
                    m = max(m, len(val))
            return range(m)
        index = self.guess_index(box, values, columns) if index is None else index
        filtered = self._prepare_data(box, values, columns, index, store)
        if aliases is not None:
            filtered = aliases.translate(filtered)
            values = aliases.translate(values)
            index = aliases.translate(index)
            columns = aliases.translate(columns)
        # Use dataframes for 'rows' to handle vectors
        if store is not None:
            keys = self.all_keys(values, columns, index)
            df = pd.DataFrame(filtered)
            df["id"] = df.index
            for e in keys:
                if not isinstance(e, variable.Variable):
                    continue
                if e.subkeys is not None:
                    df = pd.wide_to_long(df, stubnames=e, i='id', j=e.label,
                                          sep=e.sep, suffix='\\w+')
                    keys.remove(e)
                    keys.append(e.label)
        else:
            rows = [pd.DataFrame(row, index=indices(row)) for row in filtered]
            df = rows[0].copy()
            for row in rows[1:]:
                df = df.append(row)
            df = df.reset_index(drop=True)
        pt = pd.pivot_table(df, values=values, index=index, columns=columns,
                            aggfunc=aggfunc)
        return pt

    def _unfold_3D(self, arr, labels, variable, components):
        ''' Unfold a 3D array into a 2D array 
        
        Used for vector tables in which each value is a 2D array
        '''
        def add(d, k, v):
            d2 = d.copy()
            d2.update({k: v})
            return d2
        arr2 = [np.squeeze(v) for row in arr for v in row]
        labels2 = [add(d, variable, c) for d in labels for c in components]
        return arr2, labels2

    def vector_table(self, box, values, index, index_vals, orient='rows',
                     components=None):
        ''' A table of vectors with an interpolated index
        
        Args:
            box (Box): The box of data
            values (str): The key for the values. If the values are 2D,
            components must also be specified.
            index (str): The key for the index (vector-wise)
            index_vals (list-like): The index values for the vector
            orient (str): The direction of the vectors. Defaults to 'rows'
            and can be set to 'cols'.
            components (list[str]): A list of component names. Only required
            if the values are 2D. If the 'values' is a Variable, this cam
            be gained through variable.components.
            
        Note:
            Headings are automatically created.
        '''
        vectors, labels = box.vectors([values, index], labels='dict')
        values_list, index_list = vectors
        interp_list = []
        labels = [{k: str(v) for k, v in label.items()} for label in labels]
        for vec, ind_vec in zip(values_list, index_list):
            interp_list.append(utils.interp(ind_vec,
                                            np.squeeze(vec),
                                            np.squeeze(index_vals)))
        if np.ndim(interp_list) == 3:
            interp_list, labels = self._unfold_3D(interp_list, labels,
                          values + ':', components)
        ind = pd.MultiIndex.from_frame(pd.DataFrame(labels))
        if orient=='rows':
            df = pd.DataFrame(np.array(interp_list).T, index=index_vals, columns=ind)
            df = df.rename_axis(index, axis=0)
        else:
            df = pd.DataFrame(interp_list, index=ind, columns=index_vals)
            df = df.rename_axis(index, axis=1)
        return df
    
    
    
tabulator = Tabulator()
vector_table = tabulator.vector_table
tabulate = tabulator.tabulate

def to_csv(df, fname, *args, **kwargs):
    fname = utils.safe_fname(fname)
    fname = utils.ensure_ext(fname, '.csv')
    return df.to_csv(fname, *args, **kwargs)