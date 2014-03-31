Interpolation project
=====================

[![Build Status](https://travis-ci.org/Linkid/interpol_project.svg)](https://travis-ci.org/Linkid/interpol_project)
[![Coverage Status](https://coveralls.io/repos/Linkid/interpol_project/badge.png)](https://coveralls.io/r/Linkid/interpol_project)

Date: 28/03/2014

Surface interpolation project (2A n7, imm)


Topic
-----

I choose to implement the Catmull-Clark subdivision surface algorithm to create smooth surfaces. This algorithm is used in some famous applications like Blender.


Dependencies
------------

You have to install dependencies to run those scripts:

    pip install -r requirements.txt

Futhermore, to view an OBJ file with the Pygame interface, you have to install
``pygame`` and ``PyOpenGL``.


How To
------

The main script use OBJ files.

To view an OBJ file, there is a Pygame script in ``pygame/``:

    python2 pygame/sample.py file.obj

To run the main script:

    python2 proj_interpol2A.py [-h] [--nbiter NBITER] file.obj

To run tests:

    python2 test.py
    # ou nosetests2


Links
-----

* Github repo: https://github.com/Linkid/interpol_project
* Bitbucket (hg) repo: https://bitbucket.org/Linkid/interpol_project/overview
* Wikipedia: http://en.wikipedia.org/wiki/Catmull%E2%80%93Clark_subdivision_surface
* Another website: http://www.rorydriscoll.com/2008/08/01/catmull-clark-subdivision-the-basics/
* OBJ octahedre_regulier: http://guides.recitmst.qc.ca/geometrie/IMG/obj/octaedre_regulier.obj
* More OBJ objects: http://people.sc.fsu.edu/~jburkardt/data/obj/obj.html
