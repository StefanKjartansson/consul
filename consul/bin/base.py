# -*- coding: utf-8
import shlex
import subprocess


class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    EC = '\033[0m'

    @staticmethod
    def green(msg):
        print(color.OKGREEN + msg + color.EC)

    @staticmethod
    def blue(msg):
        print(color.OKBLUE + msg + color.EC)

    @staticmethod
    def yellow(msg):
        print(color.WARNING + msg + color.EC)

    @staticmethod
    def red(msg):
        print(color.FAIL + msg + color.EC)


def command(cmd):
    p = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    o, e = p.communicate()
    if p.returncode:
        raise Exception(e)
    return o


class AttributeDictMixin(object):
    """Adds attribute access to mappings.

    >>> d.key -> d[key]
    """

    def __getattr__(self, key):
        """`d.key -> d[key]`"""
        try:
            return self[key]
        except KeyError:
            raise AttributeError("'%s' object has no attribute '%s'" % (
                    self.__class__.__name__, key))

    def __setattr__(self, key, value):
        """`d[key] = value -> d.key = value`"""
        self[key] = value


class AttributeDict(dict, AttributeDictMixin):
    pass
