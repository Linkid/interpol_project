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
        self.faces = [[3, 2, 1, 0],
                      [1, 5, 4, 0],
                      [2, 6, 5, 1],
                      [7, 6, 2, 3],
                      [4, 7, 3, 0],
                      [5, 6, 7, 4]]
        self.mesh = {'vertices': self.vertices, 'faces': self.faces}

        ## create the CatmullClark object
        self.cat = CatmullClark(self.mesh)

    def test_face_point(self):
        vertices = [self.vertices[v] for v in self.faces[0]]
        face_point = self.cat.face_point(vertices)
        np_test.assert_array_equal(face_point, np.array([-1/2., 0., 0.]))

    def test_edges_vertex(self):
        # Faces of vertices to edges of vertices
        self.cat.edges_vertex()
        self.assertEqual(self.cat.edges_v, {0: (4, 7),
                                            1: (1, 3),
                                            2: (5, 6),
                                            3: (0, 7),
                                            4: (1, 6),
                                            5: (3, 7),
                                            6: (2, 5),
                                            7: (0, 3),
                                            8: (1, 2),
                                            9: (6, 7),
                                            10: (1, 5),
                                            11: (3, 6),
                                            12: (0, 4),
                                            13: (2, 7),
                                            14: (2, 6),
                                            15: (4, 5),
                                            16: (1, 4),
                                            17: (2, 3),
                                            18: (0, 1),
                                            19: (4, 6),
                                            20: (5, 7),
                                            21: (0, 5),
                                            22: (3, 4),
                                            23: (0, 2)})

    def test_faces_edge(self):
        # Faces of vertices to faces of edges
        self.cat.faces_edge()
        self.assertEqual(self.cat.faces_e, {0: [1, 7, 8, 17, 18, 23],
                                            1: [10, 12, 15, 16, 18, 21],
                                            2: [2, 4, 6, 8, 10, 14],
                                            3: [5, 9, 11, 13, 14, 17],
                                            4: [0, 3, 5, 7, 12, 22],
                                            5: [0, 2, 9, 15, 19, 20]})

    def test_edge_point(self):
        id_edge = 8  # vertices (0, 1)
        face_points = []

        # add the face point of the face 0
        vertices = [self.vertices[v] for v in self.faces[0]]
        face_points.append(self.cat.face_point(vertices))
        np_test.assert_array_equal(face_points[-1],
                                   np.array([-1/2., 0., 0.]))
        # add the face point of the face 1
        vertices = [self.vertices[v] for v in self.faces[1]]
        face_points.append(self.cat.face_point(vertices))
        np_test.assert_array_equal(face_points[-1],
                                   np.array([0., -1/2., 0.]))
        # add the face point of the face 2
        vertices = [self.vertices[v] for v in self.faces[2]]
        face_points.append(self.cat.face_point(vertices))
        np_test.assert_array_equal(face_points[-1],
                                   np.array([0., 0., -1/2.]))
        # add the face point of the face 3
        vertices = [self.vertices[v] for v in self.faces[3]]
        face_points.append(self.cat.face_point(vertices))
        np_test.assert_array_equal(face_points[-1],
                                   np.array([0., 1/2., 0.]))
        # add the face point of the face 4
        vertices = [self.vertices[v] for v in self.faces[4]]
        face_points.append(self.cat.face_point(vertices))
        np_test.assert_array_equal(face_points[-1],
                                   np.array([0., 0., 1/2.]))
        # add the face point of the face 5
        vertices = [self.vertices[v] for v in self.faces[5]]
        face_points.append(self.cat.face_point(vertices))
        np_test.assert_array_equal(face_points[-1],
                                   np.array([1/2., 0., 0.]))

        edge_point = self.cat.edge_point(id_edge, face_points)

        np_test.assert_allclose(edge_point,
                                np.array([-3/8., 0., -3/8.]))


if __name__ == '__main__':
    unittest.main()
