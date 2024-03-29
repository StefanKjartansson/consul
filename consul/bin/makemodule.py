#!/usr/bin/env python
# -*- coding: utf-8
import argparse
import os
import sys

if __name__ == "__main__" and __package__ is None:
    __package__ = "consul.bin.makemodule"

from .base import color


def create_module(p):
    p = p.strip('/')
    try:
        os.makedirs(p)
        for root, _, _ in os.walk(p.split('/')[0]):
            with open('%s/__init__.py' % root, 'w') as f:
                f.write('#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n')
    except:
        color.red('Error')
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Creates a module.')
    parser.add_argument('path', metavar='P', type=str,
        help='Intended module path')
    args = parser.parse_args()
    color.blue('Creating module')
    create_module(args.path)


if __name__ == '__main__':
    main()
