"""This package contains extensions to distutils. Its my hope we can
move some of this into a proper set of Plone shared code
"""
from test import TestCommand
from doc import DocCommand
import utils

def extensions():
    return {
        'test' : TestCommand,
        'doc' : DocCommand,
        }


__all__ = ['TestCommand', 'DocCommand', 'utils']

