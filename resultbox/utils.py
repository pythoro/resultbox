# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 08:24:09 2019

@author: Reuben
"""

import numpy as np
from scipy.interpolate import interp1d


def listify(obj):
    if not isinstance(obj, list):
        return [obj]
    else:
        return obj

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

def orient(arr, n, axis='rows'):
    ''' Orient a 2D array so that it has n rows or columns
    
    Args:
        arr (array-like): The array
        n (int, list): The number of rows for the desired output. Must equal the
        length of one array axis. Or a list of elements.
    
    Returns:
        ndarray: The oriented array. It behaves as a list.
    '''
    a = np.atleast_2d(arr)
    ax = None
    n = len(n) if isinstance(n, list) else n
    for i in range(2):
        if a.shape[i] == n:
            ax = i
    if ax is None:
        raise ValueError('Neither dimension in arr has ' + str(n) + ' elements.')
    if (axis == 'rows' and ax == 0) or (axis != 'rows' and ax == 1):
        return a
    else:
        return a.T

def _interp_1D(xs, ys, new_xs, min_diff=1e-4, bounds_error=False, 
           fill_value=None, **kwargs):
    ''' Return interpolated values for 1D array '''
    xs, ys = cosort(xs, ys, min_diff=min_diff)
    if fill_value is None:
        fill_value = (ys[0], ys[-1])
    f = interp1d(xs, ys, bounds_error=bounds_error, fill_value=fill_value,
                 **kwargs)
    return f(new_xs)    

def interp(xs, ys, new_xs, min_diff=1e-4, bounds_error=False, 
           fill_value=None, **kwargs):
    n = np.ndim(ys)
    xs = xs.flatten() if isinstance(xs, np.ndarray) else xs
    if n == 1:
        return _interp_1D(xs, ys, new_xs, min_diff, bounds_error, fill_value,
                          **kwargs)
    elif n == 2:
        a = orient(ys, n, 'cols')
        out = [_interp_1D(xs, row, new_xs, min_diff, bounds_error, fill_value,
                          **kwargs) for row in a]
        out = np.array(out) if isinstance(ys, np.ndarray) else out
        return out
    raise ValueError('ys must have 1 or 2 dimensions')
            

def list_to_str(lst, length=18, brackets=True):
    l = [val_to_str(num) for num in lst]
    s = ' '.join(l)[:length]
    if brackets:
        return '[' + s + ']'
    else:
        return s

def val_to_str(num, precision=2):
    format_str = '{:0.' + str(precision) + 'g}'
    if isinstance(num, str):
        return num
    elif isinstance(num, int):
        return str(num)
    elif isinstance(num, float):
        return format_str.format(num)
    elif isinstance(num, list):
        return list_to_str(num)
    elif isinstance(num, np.ndarray):
        if num.size == 1:
            return format_str.format(num.item())
        else:
            return list_to_str(num.flatten().tolist())
        
def dict_to_str(dct, val_sep=' ', key_sep=' '):
    lst = []
    for key, val in dct.items():
        s = str(key) + val_sep + val_to_str(val)
        lst.append(s)
    return key_sep.join(lst)