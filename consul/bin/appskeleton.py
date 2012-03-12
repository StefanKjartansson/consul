# -*- coding: utf-8

import ConfigParser
import argparse
import getpass
import os
import tarfile
import requests

from cStringIO import StringIO
from jinja2 import Template


if __name__ == "__main__" and __package__ is None:
    __package__ = "consul.bin.appskeleton"


from .base import color, AttributeDict


def create_package(context):

    color.green('Creating module')
    name = context.name

    #Download tarball from github
    t = tarfile.open(fileobj=StringIO(requests.get(context.skeleton).content),
        mode='r:gz')

    #List all non root folders from the tarball and create
    #a subfolder for them. tar lists each folder separate so
    #theres no need to use a set to filter out duplicates.
    for p in (x for x in ('/'.join(i.name.split('/')[1:])
            for i in t.getmembers() if i.isdir()) if x):
        os.makedirs('%s/%s' % (name, p))

    #Create the package itself
    os.makedirs('%s/%s' % (name, name))
    with open('%s/%s/__init__.py' % (name, name), 'w') as f:
        f.write('')

    #Extract files in the tarball, create jinja templates from their
    #contents and render with the context
    for key, value in (('/'.join(i.name.split('/')[1:]),
            t.extractfile(i.name).read())
                for i in t.getmembers() if i.isfile()):

        if context.ignore_hidden and key.startswith('.'):
            continue

        with open('%s/%s' % (context.name, key), 'w') as f:
            f.write(Template(value).render(**context))

    color.green('finished')


def main():

    parser = argparse.ArgumentParser(
        description='''Creates a python package from a
            pre-configured skeleton''')

    parser.add_argument('name', metavar='name', type=str,
        help='Name')
    parser.add_argument('--description', metavar='description', type=str,
        help='Description', default='', required=False)
    parser.add_argument('--author', metavar='author', type=str,
        help='Author', default=None, required=False)
    parser.add_argument('--email', metavar='email', type=str,
        help='Email', default=None, required=False)
    parser.add_argument('--skeleton', metavar='skeleton', type=str,
        help='Package skeleton', required=False,
        default='https://github.com/StefanKjartansson/pps/')
    parser.add_argument('--branch', type=str,
        help='Branch', required=False, default='master')
    parser.add_argument('--hidden', help='Include hidden files from skeleton',
        default=False, required=False, action='store_true')

    args = parser.parse_args()
    author_name, email = args.author, args.email

    if None in [author_name, email]:

        config_path = os.path.expanduser('~/.pjutils')

        if not os.path.isfile(config_path):
            import socket
            author_name = author_name or getpass.getuser()
            email = email or '%s@%s' % (author_name, socket.gethostname())
        else:
            config = ConfigParser.RawConfigParser(allow_no_value=True)
            config.readfp(open(os.path.expanduser('~/.pjutils')))
            author_name = config.get('defaults', 'author')
            email = config.get('defaults', 'email')

    context = AttributeDict(
        author=AttributeDict(name=author_name, email=email),
        skeleton='%starball/%s/' % (args.skeleton, args.branch),
        name=args.name,
        description=args.description,
        ignore_hidden=(not args.hidden))

    create_package(context)


if __name__ == '__main__':
    main()
