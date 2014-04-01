#!/usr/bin/env python2
# -*- coding: utf-8 -*-


class ObjFile:
    def __init__(self):
        self.verts = []
        self.norms = []
        self.textco = []
        self.faces = []

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
                    face = words[1:]
                    # OBJ Files are 1-indexed so we must subtract 1 below
                    iface = [int(k) - 1 for k in face]
                    self.faces.append(iface)
