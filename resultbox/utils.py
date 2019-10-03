# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 08:24:09 2019

@author: Reuben
"""

import numpy as np
from scipy.interpolate import interp1d


def cosort(xs, ys, min_diff=0):
    ''' Sort into monotonic x 
    
    See: https://stackoverflow.com/questions/11851770/spline-interpolation-with-python
    '''
    # Combine lists into list of tuples
    tups = zip(xs, ys)
    
    # Sort list of tuples by x-value
    tups = sorted(tups, key=lambda tup: tup[0])
    if min_diff is not None:
        tups = deduplicate_xs(tups, min_diff=min_diff)
    # Split list of tuples into two list of x values any y values
    xs_sorted, ys_sorted = zip(*tups)
    if isinstance(xs, np.ndarray):
        return np.array(xs_sorted), np.array(ys_sorted)
    elif isinstance(xs, list):
        return list(xs_sorted), list(ys_sorted)
    else:
        return xs_sorted, ys_sorted


def deduplicate_xs(tups, min_diff=0):
    ''' Remove duplicate xs
    
    Args:
        tups: Sorted list of tuples of values
        min_diff: Minimum difference between x values
    
    See https://www.geeksforgeeks.org/python-remove-tuples-having-duplicate-first-value-from-given-list-of-tuples/
    '''
    m = tups[0][0] - min_diff - 1
    out = []
    for t in tups:
        if t[0] > (m + min_diff):
            out.append(t)
        m = t[0]
    return out

def interp(xs, ys, new_xs, min_diff=1e-4, bounds_error=False, 
           fill_value=None, **kwargs):
    xs, ys = cosort(xs, ys, min_diff=min_diff)
    if fill_value is None:
        fill_value = (ys[0], ys[-1])
    f = interp1d(xs, ys, bounds_error=bounds_error, fill_value=fill_value,
                 **kwargs)
    return f(new_xs)