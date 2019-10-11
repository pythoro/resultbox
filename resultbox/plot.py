# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 20:02:36 2019

@author: Reuben
"""

import numpy as np
import matplotlib.pyplot as plt
from . import utils
import warnings

def plot():
    pass

def vector_plot(box, x_var, y_var, fig_num=None, legend=False, xlim=None, 
                ylim=None, y_ind=None, **kwargs):
    keys = [x_var, y_var]
    vectors, labels = box.vectors(keys)
    if len(labels) == 0:
        warnings.warn('No data for plot of: ' + str(keys))
    x_list, y_list = vectors
    fig = plt.figure(fig_num)
    for x, y, label in zip(x_list, y_list, labels):
        if np.ndim(y) == 3:
            if y_ind is None:
                raise ValueError('y_ind must be supplied for 2D arrays' )
            # It's a list of 2D vectors, so try to select the right ones
            y = [vector[y_ind] for vector in utils.orient(y, len(x))]
        plt.plot(x, y, label=label, **kwargs)
    plt.xlabel(x_var)
    plt.ylabel(y_var)
    if legend:
        plt.legend()
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    return fig

