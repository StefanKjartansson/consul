# -*- coding: utf-8
import StringIO
import argparse
import collections
import glob
import itertools
import random
import string
import struct
import sys
import textwrap


if __name__ == "__main__" and __package__ is None:
    __package__ = "consul.bin.grayappend"

from base import color, command


IMAGE_FORMATS = (
    'png',
    'gif',
    'jpg',
)


Picture = collections.namedtuple('Picture',
    ['name', 'mimetype', 'x', 'y'])


def random_name():
    return ''.join((random.choice(string.lowercase)
        for i in xrange(5)))


#http://code.google.com/p/bfg-pages/source/browse/trunk/pages/getimageinfo.py
def get_image_info(data):
    data = str(data)
    size = len(data)
    height = -1
    width = -1
    content_type = ''

    # handle GIFs
    if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
        # Check to see if content_type is correct
        content_type = 'gif'
        w, h = struct.unpack("<HH", data[6:10])
        width = int(w)
        height = int(h)

    # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
    # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
    # and finally the 4-byte width, height
    elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n')
          and (data[12:16] == 'IHDR')):
        content_type = 'png'
        w, h = struct.unpack(">LL", data[16:24])
        width = int(w)
        height = int(h)

    # Maybe this is for an older PNG version.
    elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
        # Check to see if we have the right content type
        content_type = 'png'
        w, h = struct.unpack(">LL", data[8:16])
        width = int(w)
        height = int(h)

    # handle JPEGs
    elif (size >= 2) and data.startswith('\377\330'):
        content_type = 'jpg'
        jpeg = StringIO.StringIO(data)
        jpeg.read(2)
        b = jpeg.read(1)
        try:
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF): b = jpeg.read(1)
                while (ord(b) == 0xFF): b = jpeg.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    jpeg.read(3)
                    h, w = struct.unpack(">HH", jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0])-2)
                b = jpeg.read(1)
            width = int(w)
            height = int(h)
        except struct.error:
            pass
        except ValueError:
            pass

    return content_type, width, height


def main():

    parser = argparse.ArgumentParser(
        description='''Appends a grayscale version of an icon image
            to the bottom of it and outputs css rules for a grayscale
            disabled icon version of it based on background position''')

    parser.add_argument('--bottom', metavar='bottom', type=int,
        help='Pixel padding', default=0, required=False)
    parser.add_argument('--staticpath', type=str,
        help='Static path prefix for css', default='/static/icons',
        required=False)
    parser.add_argument('--opacity', type=int,
        help='Disabled css opacity', default=4,
        required=False)
    parser.add_argument('--verbose', help='Verbose output',
        default=False, required=False, action='store_true')

    try:
        command('convert --version')
    except:
        color.red("Requires ImageMagick to be installed")
        sys.exit(1)

    args = parser.parse_args()
    lst = []

    for pic in list(itertools.chain.from_iterable(
           (glob.glob('*.%s' % i) for i in IMAGE_FORMATS))):

        if args.verbose:
            color.green('Processing %s' % pic)

        t, x, y = get_image_info(open(pic).read())

        lst.append(Picture(pic, t, x, y))

        command('convert %s -crop %dx%d+0+%d +repage temp.%s' % (
            pic, x, y, args.bottom, t))
        command('convert temp.%s -colorspace gray gs.%s' % (t, t))
        command('convert temp.%s gs.%s -append rs_%s' % (t, t, pic))
        command('rm temp.%s gs.%s' % (t, t))

    kf = lambda i: (i.x, i.y)
    lst = sorted(lst, key=kf)

    css = "/* Autogenerated */"

    for k, grp in itertools.groupby(lst, key=kf):
        n = random_name()
        x, y = k
        css += textwrap.dedent("""
        .%(name)s { float: left; width: %(x)dpx; height: %(y)dpx;
            text-indent: -9999px; background-position: 0 0;
            background-repeat: no-repeat;}
        .%(name)s.disabled { background-position: 0 -%(y)dpx; opacity: 0.%(opacity)d;}
        """) % {'name': n,
                'x': x,
                'y': y,
                'opacity': args.opacity}

        t = ".%(name)s.%(sname)s { background-image: url('%(spath)s/rs_%(pname)s');}\n"
        for p in grp:
            css += t % {
                'name': n,
                'pname': p.name,
                'sname': p.name[:-4],
                'spath': args.staticpath}

    css += "/* eof Autogenerated */"
    if args.verbose:
        color.yellow('Generated CSS:')
    print(css)


if __name__ == '__main__':
    main()