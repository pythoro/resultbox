# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 20:02:36 2019

@author: Reuben
"""

import matplotlib.pyplot as plt

def plot():
    pass

def vector_plot(box, x_var, y_var, fig_num=None, legend=False, xlim=None, 
                ylim=None, **kwargs):
    keys = [x_var, y_var]
    vectors, labels = box.vectors(keys)
    x_list, y_list = vectors
    fig = plt.figure(fig_num)
    for x, y, label in zip(x_list, y_list, labels):
        plt.plot(x, y, label=label, **kwargs)
    if legend:
        plt.legend()
    if xlim is not None:
        plt.xlim(xlim)
    if ylim is not None:
        plt.ylim(ylim)
    return fig

