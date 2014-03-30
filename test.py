#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unittest
import numpy as np
import numpy.testing as np_test
from proj_interpol2A import CatmullClark


class TestEvalution(unittest.TestCase):
    def setUp(self):
        ## init the mesh
        self.vertices = [[1, 0, 0], [0, 0, 1], [0, -1, 0]]
        self.faces = [[1, 5, 4]]
        self.mesh = {'vertices': self.vertices, 'faces': self.faces}

        ## create the CatmullClark object
        self.cat = CatmullClark(self.mesh)

    def test_face_point(self):
        face_point = self.cat.face_point(self.vertices)
        np_test.assert_array_equal(face_point, np.array([1/3., -1/3., 1/3.]))

    def test_edges_vertex(self):
        self.cat.edges_vertex()
        self.assertEqual(self.cat.edges_v, {2: (1, 4), 1: (1, 5), 0: (4, 5)})

    def test_faces_edge(self):
        self.cat.faces_edge()
        self.assertEqual(self.cat.faces_e, {0: [0, 1, 2]})


if __name__ == '__main__':
    unittest.main()
