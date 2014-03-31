#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unittest
import numpy as np
import numpy.testing as np_test
from proj_interpol2A import CatmullClark


class TestEvalution(unittest.TestCase):
    def setUp(self):
        ## init the mesh
        self.vertices = [[-0.5, -0.5, 0.5],
                         [-0.5, -0.5, -0.5],
                         [-0.5, 0.5, -0.5],
                         [-0.5, 0.5, 0.5],
                         [0.5, -0.5, 0.5],
                         [0.5, -0.5, -0.5],
                         [0.5, 0.5, -0.5],
                         [0.5, 0.5, 0.5]]
        self.faces = [[4, 3, 2, 1],
                      [2, 6, 5, 1],
                      [3, 7, 6, 2],
                      [8, 7, 3, 4],
                      [5, 8, 4, 1],
                      [6, 7, 8, 5]]
        self.mesh = {'vertices': self.vertices, 'faces': self.faces}

        ## create the CatmullClark object
        self.cat = CatmullClark(self.mesh)

    def test_face_point(self):
        vertices = [self.vertices[v] for v in self.faces[0]]
        face_point = self.cat.face_point(vertices)
        np_test.assert_array_equal(face_point, np.array([-1/4., 0., 0.]))

    def test_edges_vertex(self):
        # Faces of vertices to edges of vertices
        self.cat.edges_vertex()
        self.assertEqual(self.cat.edges_v, {0: (4, 7),
                                            1: (1, 3),
                                            2: (4, 8),
                                            3: (5, 6),
                                            4: (1, 6),
                                            5: (3, 7),
                                            6: (2, 5),
                                            7: (5, 8),
                                            8: (1, 2),
                                            9: (6, 7),
                                            10: (1, 5),
                                            11: (3, 6),
                                            12: (2, 6),
                                            13: (4, 5),
                                            14: (1, 4),
                                            15: (2, 3),
                                            16: (2, 7),
                                            17: (6, 8),
                                            18: (3, 4),
                                            19: (5, 7),
                                            20: (3, 8),
                                            21: (1, 8),
                                            22: (7, 8),
                                            23: (2, 4)})

    def test_faces_edge(self):
        # Faces of vertices to faces of edges
        self.cat.faces_edge()
        self.assertEqual(self.cat.faces_e, {0: [1, 8, 14, 15, 18, 23],
                                            1: [3, 4, 6, 8, 10, 12],
                                            2: [5, 9, 11, 12, 15, 16],
                                            3: [0, 2, 5, 18, 20, 22],
                                            4: [2, 7, 10, 13, 14, 21],
                                            5: [3, 7, 9, 17, 19, 22]})

    def test_edge_point(self):
        id_edge = 8  # vertices (0, 1)
        face_points = []

        # add the face point of the face 0
        vertices = [self.vertices[v] for v in self.faces[0]]
        face_points.append(self.cat.face_point(vertices))
        np_test.assert_array_equal(face_points[-1],
                                   np.array([-1/4., 0., 0.]))
        # add the face point of the face 1
        vertices = [self.vertices[v] for v in self.faces[1]]
        face_points.append(self.cat.face_point(vertices))
        np_test.assert_array_equal(face_points[-1],
                                   np.array([0., 0., -1/2.]))

        edge_point = self.cat.edge_point(id_edge, face_points)

        np_test.assert_allclose(edge_point,
                                np.array([-5/16., 0., -3/8.]))


if __name__ == '__main__':
    unittest.main()
