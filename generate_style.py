#!/usr/bin/env python

import argparse
import importlib

# these are the preconfigured styles that can be called when creating the final mapfile,
# e.g. with `make STYLE=google`. This will create an osm-google.map mapfile
style_aliases = {

    # map with no road casing and few colors, suited for using as a basemap when overlaying
    # other layers without risk of confusion between layers.
    "default": "default",

    # a style resembling the google-maps theme
    "google": "default,outlined,google",

    # same style as above, but using data coming from an osm2pgsql schema rather than imposm
    "googleosm2pgsql": "default,outlined,google,osm2pgsql",
    "bing": "default,outlined,bing",
    "michelin": "default,outlined,centerlined,michelin",
    "michelin2": "default,outlined,centerlined,michelin2"
}

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--level", dest="level", type=int, action="store", default=-1, help="generate file for level n")
parser.add_argument("-g", "--global", dest="full", action="store_true", default=False, help="generate global include file")
parser.add_argument("-s", "--style", action="store", dest="style", default="default", help="comma separated list of styles to apply (order is important)")

args = parser.parse_args()

style = {}

# each style module contains a dictionary with the same name as the file
# and any other code required
for namedstyle in style_aliases[args.style].split(','):
    ndstyle = importlib.import_module("styles.{0}".format(namedstyle))
    style.update(getattr(ndstyle, namedstyle))

if args.full:
    print("###### level 0 ######")
    for k, v in style.items():
        if isinstance(v, dict):
            print("#define _{0}0 {1}".format(k, v[0]))
        else:
            print("#define _{0}0 {1}".format(k, v))

    for i in range(1, 19):
        print('')
        print("###### level {0} ######".format(i))
        for k, v in style.items():
            if isinstance(v, dict):
                if not i in v:
                    print("#define _{0}{1} _{0}{2}".format(k, i, i-1))
                else:
                    print("#define _{0}{1} {2}".format(k, i, v[i]))
            else:
                print("#define _{0}{1} {2}".format(k, i, v))

if args.level != -1:
    level = args.level
    for k, v in style.items():
        print("#undef _{0}".format(k))

    for k, v in style.items():
        print("#define _{0} _{0}{1}".format(k, level))
