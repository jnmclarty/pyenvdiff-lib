# We're not catching ImportError because that class might not exist in all
# versions of python.

compatibility = "This flavour of python isn't compatible with pyenvdiff, yet.  "
instructions = "Please file an issue at github.com/jnmclarty/pyenvdiff.  "


def import_warn():
    try:
        from warnings import warn
    except:
        print("You have no modern warnings library, using print instead.")

        def warn(text):
            print(text)
    return warn


warn = import_warn()


def import_sys():
    try:
        import sys
    except:
        warn("Coundn't import sys.  " + compatibility + instructions)
    return sys


def import_json():
    try:
        import json
    except:
        warn("Couldn't import json.  " + compatibility + instructions)
    return json


def import_os():
    try:
        import os
    except:
        warn("Couldn't import os.  " + compatibility + instructions)
    return os


def import_urllib_x():
    sys = import_sys()
    try:
        if sys.version_info[0] < 3:
            from urllib2 import Request, urlopen, HTTPError
        else:
            from urllib.request import Request, urlopen
            from urllib.error import HTTPError
    except:
        warn("Couldn't import Request & urlopen.  " +
             compatibility + instructions)
    return Request, urlopen, HTTPError
