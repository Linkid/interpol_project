#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unittest
import numpy as np
import numpy.testing as np_test
import tempfile
from proj_interpol2A import CatmullClark
from wavefront_parser import ObjFile


class TestEvalution(unittest.TestCase):
    def setUp(self):
        ## init the mesh
        self.vertices = [[-0.5, -0.5, 0.5],  # 0
                         [-0.5, -0.5, -0.5],  # 1
                         [-0.5, 0.5, -0.5],  # 2
                         [-0.5, 0.5, 0.5],  # 3
                         [0.5, -0.5, 0.5],  # 4
                         [0.5, -0.5, -0.5],  # 5
                         [0.5, 0.5, -0.5],  # 6
                         [0.5, 0.5, 0.5]]  # 7
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
        self.assertEqual(self.cat.edges_v, {0: (1, 2),
                                            1: (0, 1),
                                            2: (5, 6),
                                            3: (2, 6),
                                            4: (6, 7),
                                            5: (4, 5),
                                            6: (4, 7),
                                            7: (1, 5),
                                            8: (2, 3),
                                            9: (0, 4),
                                            10: (3, 7),
                                            11: (0, 3)})

    def test_faces_edge(self):
        # Faces of vertices to faces of edges
        self.cat.faces_edge()
        self.assertEqual(self.cat.faces_e, {0: [0, 1, 8, 11],
                                            1: [1, 5, 7, 9],
                                            2: [0, 2, 3, 7],
                                            3: [3, 4, 8, 10],
                                            4: [6, 9, 10, 11],
                                            5: [2, 4, 5, 6]})

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
                                np.array([-3/8., 3/8., 0.]))

    def test_vertex_point(self):
        # n = 3  # valence for a cube
        vertex = self.vertices[0]
        fps = []
        for face in self.faces:
            vs = [self.vertices[v] for v in face]
            fps.append(self.cat.face_point(vs))
        self.cat.face_points = fps
        vertex_point = self.cat.vertex_point(vertex)

        np_test.assert_allclose(vertex_point, np.array([-0.09259259,
                                -0.09259259,  0.09259259]))


class TestObj(unittest.TestCase):
    def setUp(self):
        self.obj = ObjFile()
        self.comment = b"""
                        # this is a comment with spaces  
                        # v 0 0 0
                        """
        self.vertices = b"""
                          v  0 0 1
                         v 0  1 0
                         v 0 1  1
                         """
        self.normals = b"""
                         vn 0 0.3  3.2
                        vn  1  2.3 5.1
                        """
        self.textures = b"""
                         vt 2 0.3  3.2
                        vt  3  0.3 3.2
                        """
        self.faces = [b"""
                      f 1 2
                      f  2  3
                      """,
                      b"""
                      f 1/2 2/3
                      f 3/4 4/5
                      """,
                      b"""
                      f 1//2 2//3
                      f 3//4 4//5
                      """,
                      b"""
                      f 1/2/3 4/5/6
                      f 7/8/9 10/11/12
                      """]

    def objs_asserts(self, v, vn, vt, f, ft, fn):
        """
        Do the asserts for vertices (v), normals (vn), textures (vt) and
        faces (f)
        """
        self.assertEqual(self.obj.verts, v)
        self.assertEqual(self.obj.norms, vn)
        self.assertEqual(self.obj.textco, vt)
        self.assertEqual(self.obj.faces, f)
        self.assertEqual(self.obj.faces_textco, ft)
        self.assertEqual(self.obj.faces_norms, fn)

    def test_init(self):
        self.objs_asserts([], [], [], [], [], [])

    def test_read_empty_file(self):
        # create a temporary obj file
        empty_file = tempfile.NamedTemporaryFile()
        # read the file
        self.obj.read(empty_file.name)

        self.objs_asserts([], [], [], [], [], [])

    def test_read_commented_file(self):
        # create a temporary obj file
        commented_file = tempfile.NamedTemporaryFile()
        # add a comment to the temp file
        commented_file.write(self.comment)
        # go to the beginning of the temp file
        commented_file.seek(0)
        # read the file
        self.obj.read(commented_file.name)

        self.objs_asserts([], [], [], [], [], [])

    def test_read_file_with_vertices(self):
        # create a temporary obj file
        vertices_file = tempfile.NamedTemporaryFile()
        # add vertices to the temp file
        vertices_file.write(self.vertices)
        # go to the beginning of the temp file
        vertices_file.seek(0)
        # read the file
        self.obj.read(vertices_file.name)

        v = [[0., 0., 1.], [0., 1., 0.], [0., 1., 1.]]
        self.objs_asserts(v, [], [], [], [], [])

    def test_read_file_with_normals(self):
        # create a temporary obj file
        normals_file = tempfile.NamedTemporaryFile()
        # add vertices to the temp file
        normals_file.write(self.normals)
        # go to the beginning of the temp file
        normals_file.seek(0)
        # read the file
        self.obj.read(normals_file.name)

        vn = [[0., 0.3, 3.2], [1., 2.3, 5.1]]
        self.objs_asserts([], vn, [], [], [], [])

    def test_read_file_with_textures(self):
        # create a temporary obj file
        textures_file = tempfile.NamedTemporaryFile()
        # add vertices to the temp file
        textures_file.write(self.textures)
        # go to the beginning of the temp file
        textures_file.seek(0)
        # read the file
        self.obj.read(textures_file.name)

        vt = [[2., 0.3, 3.2], [3., 0.3, 3.2]]
        self.objs_asserts([], [], vt, [], [], [])

    def test_read_file_with_faces(self):
        # create a temporary obj file
        faces_file = tempfile.NamedTemporaryFile()
        # add vertices to the temp file
        faces_file.write(self.faces[0])
        # go to the beginning of the temp file
        faces_file.seek(0)
        # read the file
        self.obj.read(faces_file.name)

        f = [[0, 1], [1, 2]]
        self.objs_asserts([], [], [], f, [], [])

    def test_read_file_with_faces_textco(self):
        # create a temporary obj file
        faces_file = tempfile.NamedTemporaryFile()
        # add vertices to the temp file
        faces_file.write(self.faces[1])
        # go to the beginning of the temp file
        faces_file.seek(0)
        # read the file
        self.obj.read(faces_file.name)

        f = [[0, 1], [2, 3]]
        ft = [[1, 2], [3, 4]]
        self.objs_asserts([], [], [], f, ft, [])

    def test_read_file_with_faces_normals(self):
        # create a temporary obj file
        faces_file = tempfile.NamedTemporaryFile()
        # add vertices to the temp file
        faces_file.write(self.faces[2])
        # go to the beginning of the temp file
        faces_file.seek(0)
        # read the file
        self.obj.read(faces_file.name)

        f = [[0, 1], [2, 3]]
        fn = [[1, 2], [3, 4]]
        self.objs_asserts([], [], [], f, [], fn)

    def test_read_file_with_faces_textco_normals(self):
        # create a temporary obj file
        faces_file = tempfile.NamedTemporaryFile()
        # add vertices to the temp file
        faces_file.write(self.faces[3])
        # go to the beginning of the temp file
        faces_file.seek(0)
        # read the file
        self.obj.read(faces_file.name)

        f = [[0, 3], [6, 9]]
        ft = [[1, 4], [7, 10]]
        fn = [[2, 5], [8, 11]]
        self.objs_asserts([], [], [], f, ft, fn)


if __name__ == '__main__':
    unittest.main()
