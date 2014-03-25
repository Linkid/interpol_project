#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as pdfagg
import Tkinter as Tk


plt.ion()

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111)


plt.ioff()
plt.show()
