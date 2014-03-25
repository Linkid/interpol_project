#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as pdfagg
import Tkinter as Tk



class PointBuilder:
    def __init__(self, point):
        self.point = point
        self.xs = []
        self.ys = []
        self.cid = point.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if event.inaxes != self.point.axes:
            return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.point.scatter(self.xs, self.ys)
        self.point.figure.canvas.draw()

    def disconnect(self):
        self.point.figure.canvas.mpl_disconnect(self.cid)


plt.ion()

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111)

#pointbuilder = PointBuilder(ax)
    points = plt.ginput(n=0, timeout=0, show_clicks=True, mouse_stop=2)
    for pt in points:
        ax.scatter(pt[0], pt[1], s=80, marker='+')
        plt.draw()
        print pt

plt.ioff()
plt.show()

