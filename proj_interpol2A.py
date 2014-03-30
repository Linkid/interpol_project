#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#import matplotlib
#matplotlib.use('TkAgg')

import numpy as np
#import scipy as sp
#import matplotlib.pyplot as plt
#import matplotlib.backends.backend_tkagg as pdfagg
#import Tkinter as Tk

from itertools import combinations


class CatmullClark:
    def __init__(self, mesh):
        """
        mesh: dictionary of vertices and faces (obj file decoded)
        """
        self.mesh = mesh
        self.vertices = mesh['vertices']
        self.edges_v = {}
        self.faces_v = mesh['faces']
        self.faces_e = {}

        self.face_points = []
        self.edge_points = []
        self.vertex_points = []

        # convert faces of vertices to edges of vertices
        self.edges_vertex()
        # convert faces of vertices to faces of edges
        self.faces_edge()

    def algo(self):
        """Calcuate the new points"""
        # for each face, add a face point
        self.face_points = []
        for face in self.faces_v:
            self.face_points.append(self.face_point(self.vertices(face)))

        # for each edge, add an edge point
        self.edge_points = []
        for id_edge, id_vertices in self.edges_v.items():
            self.edge_points.append(self.edge_point(id_edge_v, self.face_points))

        # move the control point to the vertex point
        self.vertex_points = []
        for vertex in self.vertices:
            self.vertex_point(vertex)

    def edges_vertex(self):
        """
        Return edges depending on vertices number
        """
        edges = set()  # unique elements
        for face in self.faces_v:
            combis = combinations(face, 2)  # [('a','b'), ('a', 'c'), …]
            for edge in combis:
                edges.add(tuple(sorted(edge)))
        self.edges_v = dict(zip(range(len(edges)), edges))

    def faces_edge(self):
        """
        Return faces depending on edges number
        """
        for n, face in enumerate(self.faces_v):
            faces = []
            # get the key of the edge from its vertices
            combis = combinations(face, 2)  # [('a','b'), ('a', 'c'), …]
            for edge in combis:
                edge_ = tuple(sorted(edge))
                faces.extend([k for k, v in self.edges_v.items()
                             if v == edge_])
            # update the faces dict
            self.faces_e[n] = sorted(faces)

    def face_point(self, ctrl_points):
        """
        The average point of all the control points for the face

        Parameters
        ----------
        ctrl_points: list of int list
            Control points for the face

        Returns
        -------
        np.array
            The face point
        """
        return np.average(ctrl_points, axis=0)

    def edge_point(self, id_edge_v, face_points):
        """
        The average of the two control points on either side of the edge, and
        the face points of the touching faces

        id_edge: the dict key of the edge from self.edges_v
        face_points: list of face points ([np.array, …])
        """
        # the center of the edge
        edges = self.edges_v[id_edge_v]  # tuple of id of vertices
        ctrl_points = [self.vertices[i] for i in edges]
        edge_center = np.average(ctrl_points, axis=0)

        # the center of the face points of the touching faces
        touching_faces = [f for f, edges in self.faces_e.items()
                          if id_edge_v in edges]
        touching_face_points = [face_points[i] for i in touching_faces]
        face_points_center = np.average(touching_face_points, axis=0)

        return np.average([edge_center, face_points_center], axis=0)

    def vertex_point(self, S):
        """
        VP = (Q + 2*R + (n-3)*S) / n
        with:
        n: the valence (number of edges the connect to that point)
        Q: the average of all surroundings face points
        R: the average of all surrounding edge midpoints
        S: the original control point
        """
        # valence
        n = 0
        ind_vertex = self.vertices.index(S)
        touching_edges = []
        for id_edge, id_vertices in self.edges_v.items():
            if ind_vertex in id_vertices:
                touching_edges.append(id_edge)  # add the edge id
                n += 1

        # surroundings face points
        # surroundings edge midpoints
        touching_face_points = set()
        edge_midpoints = set()
        for id_edge_v in touching_edges:
            # face points of the touching faces
            touching_faces = [f for f, edges in self.faces_e.items()
                              if id_edge_v in edges]
            touching_face_points.add([self.face_points[i]
                                     for i in touching_faces])

            # edge midpoint
            vertices_ = [self.vertices[v] for v in self.edges_v[id_edge_v]]
            edge_midpoints.add(np.average(vertices_, axis=0))

        Q = np.average(list(touching_face_points), axis=0)
        R = np.average(list(edge_midpoints.add), axis=0)

        vertex_point = (1 / (n * 1.)) * np.average([Q, R, S], axis=0,
                                                   weights=[1., 2., (n-3.)])
        return vertex_point


# connect the new points to define new faces
## for each face point, connect the face point to the edge points of the face
## for each vertex point, connect the vertex point to the edge points of the
## face


#plt.ion()
#
#if __name__ == '__main__':
#    fig = plt.figure()
#    ax = fig.add_subplot(111)
#
#
#plt.ioff()
#plt.show()
