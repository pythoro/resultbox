# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 21:12:24 2019

@author: Reuben
"""

import hashlib
import pandas as pd
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
        filtered = box.filtered(values + columns)
        combined = box.combined(filtered)
        index = set()
        for row in combined:
            keys = set(row.keys())
            remove_others(keys)
            index = index.union(keys)
        for row in combined:
            keys = set(row.keys())
            remove_others(keys)
            if len(keys) == len(index):
                return [k for k in row.keys() if k in index]
        return list(index)
    
    def tabulate(self, box, values, columns, index=None, aggfunc='mean',
                 aliases=None):
        def indices(d):
            m = 1
            for key, val in d.items():
                if isinstance(val, list):
                    m = max(m, len(val))
            return range(m)
        index = self.guess_index(box, values, columns) if index is None else index
        keys = listify(index) + listify(columns) + listify(values)
        filtered = box.filtered(keys)
        combined = box.combined(filtered)
        if aliases is not None:
            combined = aliases.translate(combined)
            values = aliases.translate(values)
            index = aliases.translate(index)
            columns = aliases.translate(columns)
        rows = [pd.DataFrame(row, index=indices(row)) for row in combined]
        df = rows[0].copy()
        for row in rows[1:]:
            df = df.append(row)
        df = df.reset_index(drop=True)
        pt = pd.pivot_table(df, values=values, index=index, columns=columns,
                            aggfunc=aggfunc)
        return pt
