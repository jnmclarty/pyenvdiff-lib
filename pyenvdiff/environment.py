# -*- coding: utf-8 -*-

# We shouldn't have any import errors here, they should be inside
# any given class, to maximize compatibility.
from .collectors import harmless_collector_classes, collector_class_lookup, \
    CollectorDiff, Collector
from .version import __version__
from .import_macros import import_json

DEBUG = False


class EnvironmentDiff(object):

    def __init__(self, env_left, env_right):
        self.env_l = env_left
        self.env_r = env_right

        self.results = {}

        all_keys = list(env_left.collectors.keys()) + \
            list(env_right.collectors.keys())
        self.keys = list(set(all_keys))
        self.keys.sort()

        for key in self.keys:
            coll_left = env_left[key]
            coll_right = env_right[key]
            self.results[key] = CollectorDiff(coll_left, coll_right)
        if DEBUG:
            print("Done Comparing")

    def __str__(self):
        out = []
        for key in self.keys:

            result = str(self.results[key])

            if len(result.split("\n")) > 1:
                out.append("\n" + key)
                out.append("*" * len(key))
                out.append(result)
            else:
                one_line = "\n" + key + " : " + result
                out.append(one_line)
                out.append("*" * (len(one_line) - 1))

        return "\n".join(out)

    def as_bool(self):
        ans = [self.results[k].as_bool() for k in self.keys]
        return all(ans)

    def for_app(self, output='for_json', collectors=None, include_matching=True):
        out = {}

        if collectors is None:
            collectors = list(self.results.keys())
        elif isinstance(collectors, (str)):
            collectors = [collectors]

        for col in collectors:
            col_diff = self.results[col]
            col_diff = getattr(col_diff, output)()
            if include_matching or (not col_diff['matching']):
                out[col] = col_diff
        return out

    def for_json(self, collectors=None, include_matching=True):

        return self.for_app('for_json', collectors, include_matching)

    def for_web(self, collectors=None, include_matching=True):

        return self.for_app('for_web', collectors, include_matching)

class Environment():

    def __init__(self, collectors=None):

        if collectors:
            self.collectors = collectors
        else:
            self.collectors = {}

            for CollectorClass in harmless_collector_classes:
                self.collectors[CollectorClass.__name__] = CollectorClass()

    def __getitem__(self, name):
        return self.collectors.get(name, None)

    def info(self):
        out = {}
        for k, d in self.collectors.items():
            out[k] = d.info
        return out

    def for_app(self, output='for_json'):
        out = {}
        for k, d in self.collectors.items():
            out[k] = {}
            out[k]['info'] = getattr(d, output)()
            out[k]['english'] = d.english
        return out

    def for_web(self):
        return self.for_app('for_web')

    def for_json(self):
        return self.for_app('for_json')

    def __str__(self):
        out = []
        info_sets = [self.collectors]
        if DEBUG:
            info_sets.append(self.errors)
        for info_set in info_sets:
            keys = list(info_set.keys())
            keys.sort()
            for key in keys:
                out.append("\n" + key)
                out.append("*" * len(key))
                out.append(str(info_set[key]))
        return "\n".join(out)

    def _to_json_fs(self, outfilestream):
        json = import_json()

        env_file_data = {
            '__pyenvdiff__file_version__' : str(__version__),
            'info' : self.info()
        }
        data = json.dumps(env_file_data, sort_keys=True, separators=(',', ':'), indent=2)
        outfilestream.write(data)

    @staticmethod
    def _from_json_fs(outfilestream):
        json = import_json()
        data = json.load(outfilestream)
        return Environment.from_dict(data['info'])

    @staticmethod
    def from_dict(an_env_dict):
        collected_info = {}
        for collector_name in an_env_dict.keys():
            CollectorClass = collector_class_lookup[collector_name]
            collected_info[collector_name] = CollectorClass.from_dict(
                an_env_dict)

        return Environment(collected_info)

    def to_file(self, fname):
        with open(fname, 'w') as outfile:
            self._to_json_fs(outfile)

    @staticmethod
    def from_file(fname):
        with open(fname, 'r') as infile:
            return Environment._from_json_fs(infile)

    def __add__(self, other):
        if isinstance(other, Environment):
            raise NotImplementedError("Can't add two environments together")
        elif issubclass(type(other), Collector):
            self.collectors[other.__class__.__name__] = other
            return self
