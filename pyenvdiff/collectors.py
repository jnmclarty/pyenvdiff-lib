
from .import_macros import import_sys
from .compat import supported_info_types

def _compatible_pad(a_string="", a_char=">", width=80):
    l = len(a_string)
    return a_string + (a_char * (width - l))

_cp = _compatible_pad


def make_error_safe(func):
    def wrapper(self, *args):
        if self.error:
            return self.info
        else:
            return func(self, *args)
    return wrapper

class CollectorDiff(object):

    def __init__(self, coll_left, coll_right):
        self.coll_l = coll_left
        self.coll_r = coll_right
        self.matching = coll_left == coll_right

    def as_bool(self):  # avoid the __bool__ / __nonzero__ headache.
        return self.matching

    def __str__(self):
        if self.matching:
            return _cp("MATCHING  ", "!", 77 - len(self.coll_l.__class__.__name__))
        else:
            out = []
            out.append(_cp("DOES NOT MATCH  ", "!"))
            out.append(_cp("LEFT:           "))
            out.append(str(self.coll_l))
            out.append(_cp("RIGHT:          ", "<"))
            out.append(str(self.coll_r))
            out.append(_cp(a_char="=<*>=", width=16))
        return "\n".join(out)

    def for_json(self):
        out = {"matching": self.matching,
               "left": self.coll_l.for_json(),
               "right": self.coll_r.for_json(),
               "english" : self.coll_l.english,
               "comparison": None}

        if not self.matching:
            comparison = self.coll_l.diff(self.coll_r)
            if comparison['tool'] == 'difflib':
                comparison['diff'] = str(comparison['diff'])
            out["comparison"] = comparison

        return out

    def for_web(self):
        out = {"matching": self.matching,
               "left": self.coll_l.for_web(),
               "right": self.coll_r.for_web(),
               "english" : self.coll_l.english,
               "comparison": None}

        if not self.matching:
            comparison = self.coll_l.diff(self.coll_r)
            comparison = comparison['diff']
            out["comparison"] = comparison

        return out

class Collector(object):

    # Invasive Collectors are ones that could contain personal information
    # The base Environment object does not use invasive Collectors
    # A user-defined subclass of Environment could.
    invasive = False

    def __init__(self, info=None):
        try:
            self.info = info or self.__class__.from_env()
            self.error = False
        except:
            sys = import_sys()
            e_info = sys.exc_info()[1]
            msg = "Error attempting to collect (%s): %s"
            self.info = msg % (self.__class__.__name__, e_info)
            self.error = True

    def __str__(self):
        return str(self.info)

    def for_json(self):
        return self.info

    def for_web(self):
        return str(self.info)

    def diff(self, oth):
        left = str(self)
        right = str(oth)

        out = None

        #pyenvdiff is designed to be dependency free, so we put import statements for a few dependencies in nice-to-have features.
        try:
            import ghdiff
            out = ghdiff.diff(left, right)
            tool = 'ghdiff'
        except:
            print("ghdiff is an optional dependency, which is missing.")

        if out is None:

            from difflib import HtmlDiff
            from difflib import unified_diff

            # out = "<br>".join(list(unified_diff(left.split("\n"), right.split("\n"), "", "")))

            out = HtmlDiff().make_table(left.split("\n"), right.split("\n"), "A", "B")
            tool = 'difflib'


        return  {"type": "html", "diff": out, "tool" : tool}

    def _check_for_error(self):
        if isinstance(self.info, str):
            self.error = True

    @classmethod
    def from_dict(cls, info_dict):
        info = info_dict[cls.__name__]
        collector = cls(info)
        collector._check_for_error()
        return collector

    def _type_equality_check(self, oth):
        if not isinstance(oth, type(self)):
            return False
        # TODO: We can gain some performance wins with this hook
        # if not isinstance(oth.info, type(self.info)):
        #     return False
        return True

    def _basic_content_check(self, oth):
        if isinstance(oth.info, supported_info_types):
            return self.info == oth.info
        else:
            msg = "Comparison between {self} from {self!r}"
            msg += " and {oth} from {oth!r} is unhandled"
            raise NotImplementedError(msg.format(self=self, oth=oth))

    def __eq__(self, oth):
        if self._type_equality_check(oth):
            return self._basic_content_check(oth)
        return False

    def compare(self, collector):
        return CollectorDiff(self, collector)


class Platform(Collector):

    @staticmethod
    def from_env():

        # pyenvdiff is designed to be dependency free.
        # Each collector will return an error if its required dependency isn't available.
        # ...but allows other collectors to continue on.
        import platform as p
        return [p.platform(), p.processor()] + list(p.architecture())

    @make_error_safe
    def __str__(self):
        return " | ".join(self.info)

    @property
    def english(self):
        return "Platform"


class PkgutilModules(Collector):

    @staticmethod
    def from_env():

        # pyenvdiff is designed to be dependency free.
        # Each collector will return an error if its required dependency isn't available.
        # ...but allows other collectors to continue on.
        import pkgutil
        info = [m for i, m, p in pkgutil.iter_modules() if p]
        info.sort()
        return info

    @make_error_safe
    def __str__(self):
        return "\n".join(self.info)

    def for_web(self):
        return "<br>".join(self.info)

    @property
    def english(self):
        return "Pkgutil Modules"


class PipDistributions(Collector):
    attrs = ['key', 'parsed_version', 'project_name', 'version',
             'platform', 'py_version', 'location']

    @staticmethod
    def from_env():

        # pyenvdiff is designed to be dependency free.
        # Each collector will return an error if its required dependency isn't available.
        # ...but allows other collectors to continue on.
        import pip

        # pip ~9
        try:
            from pip import get_installed_distributions
        except:
            pass

        # pip ~ 10
        try:
            from pip._internal.utils.misc import get_installed_distributions
        except:
            pass

        try:
            ins_dis = get_installed_distributions()
        except:
            raise Exception("Couldn't get pip's get_installed_distributions")

        info = []
        for dis in ins_dis:
            relevant = {}
            for attr in PipDistributions.attrs:
                relevant[attr] = str(getattr(dis, attr))
            info.append(relevant)
        return sorted(info, key=lambda x: x['project_name'])

    @make_error_safe
    def __str__(self):
        try:
            out = []
            for i in self.info:
                out.append("{key: <16} v{parsed_version: <10} -> {location}".format(**i))

                if i['key'] == i['project_name']:
                    sub_proj_name = ""
                else:
                    sub_proj_name = " `*.-> {: <16}".format(i['project_name'])

                if i['parsed_version'] == i['version']:
                    sub_version = ""
                else:
                    sub_version = " \_,-> {: <10}".format(i['version'])

                sub = "  " + sub_proj_name + sub_version

                if str(i['platform']) != 'None':
                    sub = sub + "{: <10}".format(i['platform'])

                # DNE for non-eggs is a str that == "None".
                # pip grabs this from egg file's directory names.
                if str(i['py_version']) != 'None':
                    sub = sub + "py v{: <10}".format(i['py_version'])

                out.append(sub)
            return "\n".join(out)
        except:
            return str(self.info)

    @property
    def english(self):
        return "Pip Installed Distributions"

    @make_error_safe
    def for_web(self):
        def make_pretty(row):

            tmpl = ["{project_name}"]

            if row['version'] != row['parsed_version']:
                tmpl += ["{version}|{parsed_version}"]
            else:
                tmpl += ["{version}"]

            tmpl += ["({location}) {py_version}"]

            if row['platform'] != "None":
                tmpl += ["{platform}"]

            if row['key'] != row['project_name'].lower():
                tmpl += ["{key}"]

            return " ".join(tmpl).format(**row)

        out = "<br>".join([make_pretty(x) for x in self.info])
        return out


class SysPath(Collector):

    @staticmethod
    def from_env():
        import sys
        return [x for x in sys.path]

    @make_error_safe
    def __str__(self):
        return "\n".join(self.info)

    english = "sys.path Contents"

    def for_web(self):
        out = "<br>".join(self.info)
        return out


class SysFloatInfo(Collector):

    @staticmethod
    def from_env():
        # pyenvdiff is designed to be dependency free.  Yes, even sys.
        # Each collector will return an error if its required dependency isn't available.
        # ...but allows other collectors to continue on.
        import sys
        return list(map(str, sys.float_info))

    @make_error_safe
    def __str__(self):
        return " ".join(self.info)

    @property
    def english(self):
        return "sys.float_info Contents"


class SysExecutable(Collector):

    @staticmethod
    def from_env():

         # pyenvdiff is designed to be dependency free.  Yes, even sys.
        # Each collector will return an error if its required dependency isn't available.
        # ...but allows other collectors to continue on.
        import sys
        return sys.executable or "None Found"

    @property
    def english(self):
        return "sys.executable Information"



class SysPrefix(Collector):

    @staticmethod
    def from_env():
        # pyenvdiff is designed to be dependency free.  Yes, even sys.
        # Each collector will return an error if its required dependency isn't available.
        # ...but allows other collectors to continue on.
        import sys

        out = []
        for attr in ['prefix', 'exec_prefix', 'base_exec_prefix']:
            try:
                out.append(attr + " : " + getattr(sys, attr))
            except:
                pass
        return out

    @make_error_safe
    def __str__(self):
        return "\n".join(self.info)

    english = "sys.prefix, exec_prefix, base_exec_prefix"

    def for_web(self):
        out = "<br>".join(self.info)
        return out

class SysByteOrder(Collector):

    @staticmethod
    def from_env():

        # pyenvdiff is designed to be dependency free.  Yes, even sys.
        # Each collector will return an error if its required dependency isn't available.
        # ...but allows other collectors to continue on.
        import sys
        return sys.byteorder

    @property
    def english(self):
        return "sys.byteorder Information"


class OSUname(Collector):

    @staticmethod
    def from_env():

        # pyenvdiff is designed to be dependency free.  Yes, even os, because some builds might omit.
        # Each collector will return an error if its required dependency isn't available.
        # ...but allows other collectors to continue on.
        import os
        return " ".join(os.uname())  # Unix only

    @property
    def english(self):
        return "os.uname() Information"


class SysPlatform(Collector):

    @staticmethod
    def from_env():
        import sys
        return sys.platform

    @property
    def english(self):
        return "sys.platform Information"


class SysVersion(Collector):

    @staticmethod
    def from_env():
        # pyenvdiff is designed to be dependency free.  Yes, even os, because some builds might omit.
        # Each collector will return an error if its required dependency isn't available.
        # ...but allows other collectors to continue on.
        import sys
        return sys.version

    @property
    def english(self):
        return "sys.version Information"


class SysApiVersion(Collector):

    @staticmethod
    def from_env():
        # pyenvdiff is designed to be dependency free.  Yes, even sys, because some builds might omit.
        # Each collector will return an error if its required dependency isn't available.
        # ...but allows other collectors to continue on.
        import sys
        return sys.api_version

    @property
    def english(self):
        return "sys.api_version Information"


class SysVersionInfo(Collector):
    attrs = ['major', 'minor', 'micro', 'serial', 'releaselevel']

    @staticmethod
    def from_env():
        # pyenvdiff is designed to be dependency free.  Yes, even sys, because some builds might omit.
        # Each collector will return an error if its required dependency isn't available.
        # ...but allows other collectors to continue on.
        import sys
        info = {}
        for i, attr in enumerate(SysVersionInfo.attrs):
            info[attr] = sys.version_info[i]
        return info

    @make_error_safe
    def __str__(self):
        return ".".join([str(self.info[a]) for a in self.attrs])

    @property
    def english(self):
        return "Interpreter Version Information"


class TimeZone(Collector):

    @staticmethod
    def from_env():
        # pyenvdiff is designed to be dependency free.  Yes, even time, because some builds might omit.
        # Each collector will return an error if its required dependency isn't available.
        # ...but allows other collectors to continue on.
        import time
        return [str(time.timezone)] + list(time.tzname)

    @make_error_safe
    def __str__(self):
        return " | ".join(self.info)

    @property
    def english(self):
        return "Time Zone Information"

class OSEnviron(Collector):

    invasive = True

    @staticmethod
    def from_env():

        # pyenvdiff is designed to be dependency free.  Yes, even os, because some builds might omit.
        # Each collector will return an error if its required dependency isn't available.
        # ...but allows other collectors to continue on.
        import os
        environ = dict(os.environ)
        keys = list(environ.keys())
        keys.sort()
        out = [(k, environ[k]) for k in keys]
        return out

    @make_error_safe
    def __str__(self):
        return "\n".join([key + ":" + value for key, value in self.info])

    english = "os.environ Contents"

    def for_web(self):
        out = "<br>".join(self.info)
        return out

class UserName(Collector):

    invasive = True

    @staticmethod
    def from_env():

        # pyenvdiff is designed to be dependency free.  Yes, even os, because some builds might omit.
        # Each collector will return an error if its required dependency isn't available.
        # ...but allows other collectors to continue on.

        # Note this only works on linux-based systems
        import pwd, os
        return pwd.getpwuid(os.getuid())[0]

    english = "User Name"

class HomeDirectory(Collector):

    invasive = True

    @staticmethod
    def from_env():

        # pyenvdiff is designed to be dependency free.  Yes, even os, because some builds might omit.
        # Each collector will return an error if its required dependency isn't available.
        # ...but allows other collectors to continue on.
        import os
        return os.path.expanduser('~')

    english = "Home directory (~)"



collector_classes = [Platform, PkgutilModules, PipDistributions,
                     SysByteOrder, SysExecutable, SysPath, SysPlatform, SysVersion,
                     SysVersionInfo, SysFloatInfo, SysApiVersion,
                     OSUname, TimeZone, SysPrefix,

                     OSEnviron, UserName, HomeDirectory]

invasive_collector_classes = [c for c in collector_classes if c.invasive]
harmless_collector_classes = [c for c in collector_classes if not c.invasive]


collector_class_lookup = {}
for CollectorClass in collector_classes:
    collector_class_lookup[CollectorClass.__name__] = CollectorClass
del CollectorClass
