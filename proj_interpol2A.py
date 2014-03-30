#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as pdfagg
import Tkinter as Tk


# for each face, add a face point
## face point : the average point of all the control points for the face
# for each edge, add an edge point
## edge point : the average of the two control points on either side of the
## edge, and the face points of the touching faces
# move the control point to the vertex point
## vertex point : P = (Q + 2*R + (n-3)*S) / n
### n : the valence (number of edges the connect to that point)
### Q : the average of all surroundings face points
### R : the average of all surrounding edge midpoints
### S : the original control point
# connect the new points to define new faces
## for each face point, connect the face point to the edge points of the face
## for each vertex point, connect the vertex point to the edge points of the
## face


plt.ion()

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111)


plt.ioff()
plt.show()
