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
import argparse
from wavefront_parser import ObjFile


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
            vertices_ = [self.vertices[v] for v in face]
            self.face_points.append(self.face_point(vertices_))

        # for each edge, add an edge point → 12 edge points for a box
        # 1 edge point for 2 faces
        # data struct: {id_face: [edge points]}
        self.edge_points = dict()  # all edge points of the mesh
        for id_edge in self.edges_v.keys():
            e_pt, e_faces = self.edge_point(id_edge, self.face_points)
            # add the edge point to the dict associated to faces e_faces
            for e_f in e_faces:
                if e_f in self.edge_points:
                    # have already edge points for the face e_f
                    self.edge_points[e_f].append(e_pt)
                else:
                    # init the data struct for the face
                    self.edge_points[e_f] = [e_pt]
            #self.edge_points.append(self.edge_point(id_edge, self.face_points))
        #print "Edge points:", len(self.edge_points)

        # move the control point to the vertex point → 8x3 vertex pts for a box
        # 1 vertex point for 3 faces
        # data struct: {id_face: [vertex points]}
        self.vertex_points = dict()  # all vertex points of the mesh
        for vertex in self.vertices:
            v_pt, v_faces = self.vertex_point(vertex)
            for v_f in v_faces:
                if v_f in self.vertex_points:
                    self.vertex_points[v_f].append(v_pt)
                else:
                    self.vertex_points[v_f] = [v_pt]
        #print "Vertex points:", len(self.vertex_points)

        # update control points
        # → set of tuples
        self.n_vertices = set()
        # vertex points
        for vp_val in self.vertex_points.values():
            self.n_vertices.update(map(tuple, vp_val))
        # edge points
        for ep_val in self.edge_points.values():
            self.n_vertices.update(map(tuple, ep_val))
        self.n_vertices.update(map(tuple, self.face_points))  # face points
        self.n_vertices = list(self.n_vertices)  # unique tuples → get a list
        # update edges (init)
        self.n_edges_v = set()
        # update faces (init)
        self.n_faces_e = set()
        self.n_faces_v = []

        # connect the new points to define new faces
        for id_face, fp in enumerate(self.face_points):
            ind_fp = map(list, self.n_vertices).index(list(fp))  # ouch ! XXX

            # new edges of a face
            edge_points_ = self.edge_points[id_face]
            # new vertices of a face
            vertex_points_ = self.vertex_points[id_face]

            # connect points to get new faces
            for pt_v in vertex_points_:
                # find the id of the vertex
                ind_pt_v = map(list, self.n_vertices).index(list(pt_v))
                # get the two new edge points linked to the new vp
                dists = self.dist_points(pt_v, edge_points_)
                sorted_dists = sorted(dists)[:2]  # only the two lowest
                pts_e = [edge_points_[dists.index(k)] for k in sorted_dists]
                # init the new face
                n_face_v = [ind_pt_v]

                # connect points to get new edges
                for pt_e in pts_e:
                    # find the id of the vertex
                    ind_pt_e = map(list, self.n_vertices).index(list(pt_e))
                    # connect the vertex point to those edge points
                    self.n_edges_v.add(tuple(sorted([ind_pt_v, ind_pt_e])))
                    # connect the face point to the edge points
                    self.n_edges_v.add(tuple(sorted([ind_pt_e, ind_fp])))
                    # add the id of the edge point to the new face
                    n_face_v.append(ind_pt_e)
                    # add the id of the face point to the new face
                    n_face_v.append(ind_fp)

                # update new faces (delete the last face point to the new face=
                self.n_faces_v.append(n_face_v[:-1])


    def edges_vertex(self):
        """
        Return edges depending on vertices number
        """
        edges = set()  # unique elements
        for face in self.faces_v:
            nb_vertices = len(face)
            ed = [tuple(sorted((face[v], face[(v+1) % nb_vertices])))
                  for v in range(nb_vertices)]
            edges.update(ed)
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

        id_edge_v: the dict key of the edge from self.edges_v
        face_points: list of face points ([np.array, …])
        """
        # the center of the edge
        edges = self.edges_v[id_edge_v]  # tuple of id of vertices
        ctrl_points = [self.vertices[i] for i in edges]
        edge_center = np.average(ctrl_points, axis=0)

        # the center of the face points of the touching faces
        touching_faces = [f for f, i_edges in self.faces_e.items()
                          if id_edge_v in i_edges]
        touching_face_points = [face_points[i] for i in touching_faces]
        face_points_center = np.average(touching_face_points, axis=0)

        return np.average([edge_center, face_points_center], axis=0), touching_faces

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
        touching_faces_all = set()
        touching_face_points = set()
        edge_midpoints = set()
        for id_edge_v in touching_edges:
            # face points of the touching faces
            touching_faces = [f for f, edges in self.faces_e.items()
                              if id_edge_v in edges]
            touching_faces_all.update(touching_faces)
            for i in touching_faces:
                touching_face_points.add(tuple(self.face_points[i]))

            # edge midpoint
            vertices_ = [self.vertices[v] for v in self.edges_v[id_edge_v]]
            edge_midpoints.add(tuple(np.average(vertices_, axis=0)))

        Q = np.average(list(touching_face_points), axis=0)
        R = np.average(list(edge_midpoints), axis=0)

        vertex_point = (1 / (n * 1.)) * np.average([Q, R, S], axis=0,
                                                   weights=[1., 2., (n-3.)])

        return vertex_point, touching_faces_all

    def dist_points(self, pt_orig, lst_pts):
        """
        Return the list of distances between the point pt_orig to points in
        lst_pts.
        Distance between two points: euclidean distance.

        pt_orig: a point
        lst_pts: a list of points
        """
        dists = []
        pt_a = np.array(pt_orig)

        for pt_b in lst_pts:
            dists.append(np.linalg.norm(pt_a - pt_b))

        return dists

#plt.ion()
#
if __name__ == '__main__':
    # parse the options
    parser = argparse.ArgumentParser()
    parser.add_argument("obj_file", help="OBJ filename to smooth", type=str)
    parser.add_argument("--nbiter", help="Number of iterations", type=int,
                        default=1)
    args = parser.parse_args()

    if args.obj_file:
        obj = ObjFile()
        obj.read(args.obj_file)
        mesh = {'vertices': obj.verts, 'faces': obj.faces}

        surface = CatmullClark(mesh)
        for nbiter in xrange(args.nbiter):
            surface.algo()

#    fig = plt.figure()
#    ax = fig.add_subplot(111)
#
#
#plt.ioff()
#plt.show()
