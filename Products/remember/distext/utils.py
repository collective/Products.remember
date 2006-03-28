#!/usr/bin/python2.4
import os, sys
from distutils.util import get_platform


def getBuildPath():
    plat_specifier = ".%s-%s" % (get_platform(), sys.version[0:3])
    build_platlib = os.path.join("build", 'lib' + plat_specifier)
    test_lib = os.path.abspath(build_platlib)
    if not os.path.exists(test_lib):
        build_platlib = os.path.join("build", 'lib')
        test_lib = os.path.abspath(build_platlib)
    return test_lib

def useBuildPath():
    sys.path.insert(0, getBuildPath())

