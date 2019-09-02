# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 21:12:24 2019

@author: Reuben
"""

import hashlib
from collections import defaultdict


def encoded(obj):
    if isinstance(obj, str):
        return bytes(obj, 'utf-8')
    return bytes(obj)

def safe_hash(lst):
    h = hashlib.md5()
    for obj in lst:
        h.update(encoded(obj))
    return h.digest()
    

class Table():
    pass



class Tabulator():
    
    def tabulate(self, box, row_vars, col_vars, cell_var):
        keys = row_vars + col_vars
        filtered = box.filtered(keys)
        rows, row_inds = self.make_index(filtered, row_vars)
        cols, col_inds = self.make_index(filtered, col_vars)
        
    def make_nested_index(self, filtered, var_list):
        ''' Create nested dictionary of all key-value combinations '''
        val_dict = {}
        d = {}
        n = len(var_list)
        for row in filtered:
            current = d
            for i, k in enumerate(var_list):
                val = row[k]
                s = safe_hash([val]) # Hash better, but not always available, see python-xxhash, https://stackoverflow.com/questions/16589791/most-efficient-property-to-hash-for-numpy-array
                val_dict[safe_hash([k, s])] = val # Track actual values
                if s not in current:
                    current[s] = {}
                current = current[s] # Get next nesting layer
                if i == n - 1:
                    # No more variables to nest
                    if '__index__' not in current:
                        current['__index__'] = []
                    current['__index__'].append(row['index'])
        return d, val_dict
        
    def make_index(self, filtered, var_list):
        ''' Make a full list of dictionaries for key-value combinations '''
        nested, val_dict = self.make_nested_index(filtered, var_list)
        out = []
        indices = []
        def unfold(dct, row=None, i=0):
            if '__index__' in dct:
                # Not more nested variables
                out.append(row.copy()) # Add in the index row
                indices.append(dct['__index__']) # Record the indices
                return
            row = {} if row is None else row
            for s, v in dct.items():
                k = var_list[i] # Get key
                row[k] = val_dict[safe_hash([k, s])] # put together values
                if isinstance(v, dict):
                    unfold(v, row, i+1) # Add next layers of nested structure
        unfold(nested)
        out_ind = {i: j for j, lst in enumerate(indices) for i in lst}
        return out, out_ind
        
    def allocate(self, filtered, row_inds, col_inds, cell_var):
        n = max(col_inds.values()) + 1
        m = max(row_inds.values()) + 1
        table = [[0 for i in range(n)] for j in range(m)]
        for i, row in enumerate(filtered):
            table[row_inds[i]][col_inds[i]] = row[cell_var]
        return table