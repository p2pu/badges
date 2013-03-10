#!/usr/bin/env python

import sys
import os

import optparse

from django.conf import settings
from django.template import Template, Context
from django.template.loader import *

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        print "Requires Python 2.6 or Python 2.5 with the simplejson module"
        sys.exit(1)

## Parse options and set defaults
usage = "usage: %prog [options] TEMPLATE"
description = ("Populate a Django template with environment variables and STDIN"
    "\nenvironment variables containing valid JSON will be decoded.")
version = "%prog 1.0"

parser = optparse.OptionParser(
        usage=usage,
        description=description,
        version=version)

parser.add_option("--debug",
        dest='debug',
        action='store_true',
        default=False,
        help="activate template debugging")

parser.add_option("--undefined",
        dest='undefined',
        metavar='STRING',
        default="%UNDEFINED-TEMPLATE-VAR%",
        help="sets undefined variables to STRING during template expansion "
        "[default: %default]")

options, args = parser.parse_args()

if len(args) != 1:
    parser.error("No template specified")


## Configure Django
settings.configure(
        DEBUG_TEMPLATE = options.debug,
        TEMPLATE_DIRS = '.',
        TEMPLATE_STRING_IF_INVALID = options.undefined
)


## Build inputs
template = Template(open(args[0], 'r').read())

def decode(s):
    "if json, return object--otherwise return string as is"
    try:
        return json.loads(s)
    except ValueError:
        return s

env = dict((key, decode(v)) for key, v in os.environ.items())
# 0 = full line, n = nth field, for all n>1
# env['STDIN'] = [[line] + line.split() for line in sys.stdin.xreadlines()]


## Render template and output
sys.stdout.write(template.render(Context(env)))
sys.stdout.flush()
