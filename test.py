#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unittest
import numpy as np
import numpy.testing as np_test
from proj_interpol2A import CatmullClark


class TestEvalution(unittest.TestCase):
    def setUp(self):
        ## init the mesh
        self.vertices = [[1, 0, 0],
                         [0, 1, 0],
                         [-1, 0, 0],
                         [0, -1, 0],
                         [0, 0, 1],
                         [0, 0, -1]]
        self.faces = [[0, 4, 3],
                      [3, 4, 2],
                      [2, 4, 1],
                      [1, 4, 0],
                      [0, 3, 5],
                      [3, 2, 5],
                      [2, 1, 5],
                      [1, 0, 5]]
        self.mesh = {'vertices': self.vertices, 'faces': self.faces}

        ## create the CatmullClark object
        self.cat = CatmullClark(self.mesh)

    def test_face_point(self):
        vertices = [self.vertices[v] for v in self.faces[0]]
        #print(vertices)
        face_point = self.cat.face_point(vertices)
        np_test.assert_array_equal(face_point, np.array([1/3., -1/3., 1/3.]))

    def test_edges_vertex(self):
        # Faces of vertices to edges of vertices
        self.cat.edges_vertex()
        self.assertEqual(self.cat.edges_v, {0: (1, 2),
                                            1: (0, 1),
                                            2: (2, 5),
                                            3: (1, 4),
                                            4: (1, 5),
                                            5: (2, 3),
                                            6: (0, 4),
                                            7: (0, 5),
                                            8: (0, 3),
                                            9: (3, 4),
                                            10: (2, 4),
                                            11: (3, 5)})

    def test_faces_edge(self):
        # Faces of vertices to faces of edges
        self.cat.faces_edge()
        self.assertEqual(self.cat.faces_e, {0: [6, 8, 9],
                                            1: [5, 9, 10],
                                            2: [0, 3, 10],
                                            3: [1, 3, 6],
                                            4: [7, 8, 11],
                                            5: [2, 5, 11],
                                            6: [0, 2, 4],
                                            7: [1, 4, 7]})

    def test_edge_point(self):
        id_edge = 9  # vertices (3, 4)
        face_points = []

        # add the face point of the face 0
        vertices = [self.vertices[v] for v in self.faces[0]]
        face_points.append(self.cat.face_point(vertices))
        np_test.assert_array_equal(face_points[-1],
                                   np.array([1/3., -1/3., 1/3.]))
        # add the face point of the face 1
        vertices = [self.vertices[v] for v in self.faces[1]]
        face_points.append(self.cat.face_point(vertices))
        np_test.assert_array_equal(face_points[-1],
                                   np.array([-1/3., -1/3., 1/3.]))

        edge_point = self.cat.edge_point(id_edge, face_points)

        # grrrr ! Works, but…
        np_test.assert_array_almost_equal_nulp(edge_point,
                                   np.array([0, -5/12., 5/12.]))


if __name__ == '__main__':
    unittest.main()
