# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 21:12:24 2019

@author: Reuben
"""

from collections import defaultdict

class Table():
    pass



class Tabulator():
    
    def tabulate(self, box, row_vars, col_vars):
        keys = row_vars + col_vars
        filtered = box.filtered(keys)
        row_index = self.make_index(filtered, row_vars)
        col_index = self.make_index(filtered, col_vars)
        
    def make_nested_index(self, filtered, var_list):
        ''' Create nested dictionary of all key-value combinations '''
        val_dict = {}
        d = {}
        for row in filtered:
            current = d
            for k in var_list:
                val = row[k]
                s = str(val)
                val_dict[k + '.' + s] = val
                if s not in current:
                    current[s] = {}
                current = current[s]
        return d, val_dict
        
    def make_index(self, filtered, var_list):
        ''' Make a full list of dictionaries for key-value combinations '''
        nested, val_dict = self.make_nested_index(filtered, var_list)
        out = []
        def unfold(dct, row=None, i=0):
            if len(dct) == 0:
                out.append(row.copy())
                return
            row = {} if row is None else row
            for s, v in dct.items():
                k = var_list[i]
                row[k] = val_dict[k + '.' + s]
                if isinstance(v, dict):
                    unfold(v, row, i+1)
        unfold(nested)
        return out
        
            
        
        