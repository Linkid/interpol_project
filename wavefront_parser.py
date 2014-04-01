#!/usr/bin/env python2
# -*- coding: utf-8 -*-


class ObjFile:
    def __init__(self):
        self.verts = []
        self.norms = []
        self.textco = []
        self.faces = []
        self.faces_textco = []
        self.faces_norms = []

    def read(self, filename):
        with open(filename, "r") as f:
            for line in f:
                words = line.strip().split()
                if not words:
                    continue

                cmd = words[0]
                if cmd == '#':
                    continue
                elif cmd == 'v':
                    self.verts.append(map(float, words[1:]))
                elif cmd == 'vn':
                    self.norms.append(map(float, words[1:]))
                elif cmd == 'vt':
                    self.textco.append(map(float, words[1:]))
                elif cmd == 'f':
                    face = []
                    ftextco = []
                    fnorms = []
                    for f in words[1:]:
                        w = f.split("/")
                        # OBJ Files are 1-indexed so we must subtract 1 below
                        face.append(int(w[0]) - 1)
                        if len(w) >= 2 and w[1] != "":
                            ftextco.append(int(w[1]) - 1)
                        if len(w) == 3 and w[2] != "":
                            fnorms.append(int(w[2]) - 1)
                    self.faces.append(face)
                    if len(ftextco):
                        self.faces_textco.append(ftextco)
                    if len(fnorms):
                        self.faces_norms.append(fnorms)
