# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 21:12:24 2019

@author: Reuben
"""

import os
import hashlib
import pandas as pd
from collections import defaultdict
from . import utils
from . import variable
import numpy as np
from . import constants
import warnings

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
    if obj is None:
        return []
    if not isinstance(obj, list):
        return [obj]
    return obj

def _custom_headed_table(df, fname, sep=',', **kwargs):
    ''' CSV table with label for columns index '''
    def pad(s, n):
        out = [str(a) for a in s] if isinstance(s, list) else [str(s)]
        for i in range(n-1):
            out.append('')
        return out
    
    cols = [str(c) for c in df.columns]    
    if isinstance(df.index, pd.MultiIndex):
        n = len(df.index.levels)
        header_2 = pad(df.index.names, n + len(cols))
    else:
        n = 1
        header_2 = pad(df.index.name, n + len(cols))
    header_1 = pad(df.columns.name, n) + cols
    s = sep.join(header_1) + '\n' + sep.join(header_2) + '\n'
    with open(fname, mode='a') as f:
        f.write(s)
    df.to_csv(path_or_buf=fname, sep=sep, header=None, mode='a', **kwargs)

def to_csv(df, fname, variable=None, mode='w', sep=',', **kwargs):
    fname = utils.safe_fname(fname)
    fname = utils.ensure_ext(fname, '.csv')
    s = '\n\n' if mode=='a' else ''
    if variable is not None:
        s += variable + '\n' + variable.doc + '\n\n'
    with open(fname, mode=mode) as f:
        f.write(s)
    if isinstance(df.columns, pd.MultiIndex):
        # Default behaviour is OK
        df.to_csv(fname, sep=sep, mode='a', **kwargs)
    else:
        # Need some extra to print columns label
        _custom_headed_table(df, fname, sep=sep, **kwargs)
    return True

class Table():
    pass



class Tabulator():
    def guess_index(self, box, values, columns=None):
        all_keys = self.all_keys(values, columns)
        filtered = box.filtered(all_keys, box.combined())
        index = {}
        for row in filtered:
            keys = row[constants.INDEP].keys()
            for k in keys:
                if k not in index.values():
                    index[len(index)] = k
        for k, v in index.copy().items():
            if v in all_keys:
                del index[k]
        return list(index.values())
    
    def all_keys(self, *args):
        out = []
        for arg in args:
            l = listify(arg)
            out.extend([a for a in l if not a.endswith(':')])
        return out
    
    def merge_keys(self, *args):
        return [k for ks in args for k in listify(ks)]
    
    def _prepare_data(self, box, base_keys, store=None):
        keys = self.all_keys(base_keys)
        minimal = box.minimal()
        if store is not None:
            keys_to_expand = self.get_keys_to_expand(base_keys, store)
            minimal = variable.expand(minimal, store, specified=keys_to_expand)
            for k in keys_to_expand:
                keys.remove(k)
                keys.extend(store[k].subkeys)
        filtered = box.filtered(keys, minimal)
        if len(filtered) == 0:
            raise ValueError('No records left in filtered results.')
        return filtered
    
    def get_keys_to_expand(self, keys, store):
        labels = []
        for k in keys:
            if k.endswith(':'):
                name = k.rstrip(':')
                for var in store.values():
                    if var.name == name:
                        labels.append(var)
        return labels
    
    def _vec_to_str(self, filtered, protected):
        for row in filtered:
            for k, v in row.copy().items():
                if k in protected:
                    continue
                if isinstance(v, (np.ndarray, list)):
                    row[k] = utils.vec_to_str(v)
    
    def _regenerate_key_in_columns(self, var, df):
        cols = list(df.columns)
        for i, c in enumerate(cols):
            if c == var.name:
                cols[i] = var.key
        df.columns = cols
   
    def tabulate(self, box, values, columns=None, index=None, aggfunc='mean',
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
        base_keys = self.merge_keys(values, columns, index)
        index = self.guess_index(box, values, columns) if index is None else index
        columns = [] if columns is None else columns
        filtered = self._prepare_data(box, base_keys, store)
        if aliases is not None:
            filtered = aliases.translate(filtered)
            values = aliases.translate(values)
            index = aliases.translate(index)
            columns = aliases.translate(columns)
        # Use dataframes for 'rows' to handle vectors
        if store is not None:
            keys_to_expand = self.get_keys_to_expand(base_keys, store)
            self._vec_to_str(filtered, protected=keys_to_expand)
            df = pd.DataFrame(filtered)
            df["id"] = df.index
            pd.set_option('display.max_columns', 30)
            for e in keys_to_expand:
                df = pd.wide_to_long(df, stubnames=e.name, i='id', j=e.label,
                                      sep=e.sep, suffix='.*')
                self._regenerate_key_in_columns(e, df)
        else:
            rows = [pd.DataFrame(row, index=indices(row)) for row in filtered]
            df = rows[0].copy()
            for row in rows[1:]:
                df = df.append(row)
            df = df.reset_index(drop=True)
        # pd.set_option('display.max_columns', 5)
        # print(df)
        if len(df) == 1:
            return df
        try:
            df = pd.pivot_table(df, values=values, index=index, columns=columns,
                                aggfunc=aggfunc)
        except Exception as e:
            raise e
        return df

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

    def vector_table(self, box, values, index, index_vals=None, orient='rows',
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
        values_list, index_list, labels = box.vectors([values, index], labels='dict')
        interp_list = []
        index_vals_candidate = None
        labels = [{k: str(v) for k, v in label.items()} for label in labels]
        for vec, ind_vec in zip(values_list, index_list):
            if index_vals is None:
                if index_vals_candidate is None:
                    index_vals_candidate = ind_vec
                else:
                    if not np.array_equal(ind_vec, index_vals_candidate):
                        raise ValueError('Vector indices must be consistent if'
                                         + ' not specified.')
                interp_list.append(vec)
            else:
                interp_list.append(utils.interp(ind_vec,
                                            np.squeeze(vec),
                                            np.squeeze(index_vals)))
        if index_vals_candidate is not None:
            index_vals = index_vals_candidate
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

