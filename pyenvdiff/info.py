# -*- coding: utf-8 -*-

# We shouldn't have any import errors here, they should be inside
# any given class, to maximize compatibility.
from pyenvdiff.import_macros import import_sys
from pyenvdiff import __version__

from pyenvdiff.collectors import collector_classes, collector_class_lookup


DEBUG = False

class Environment():
    def __init__(self, collectors=None):

        if collectors:
            self.collectors = collectors
        else:
            self.collectors = {}

            for CollectorClass in collector_classes:
                self.collectors[CollectorClass.__name__] = CollectorClass()
    def __getitem__(self, name):
        return self.collectors.get(name, None)

    def info(self):
        out = {}
        for k,d in self.collectors.items():
            out[k] = d.info
        return out
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
    def _to_yaml_fs(self, outfilestream):
        import yaml
        outfilestream.write("# PyEnvColla Environment File v%s\n" % str(__version__))
        yaml.dump(self.info(), outfilestream)
    @staticmethod
    def _from_yaml_fs(outfilestream):
        import yaml

        env_collected_info = yaml.load(outfilestream)

        return Environment.from_dict(env_collected_info)

    @staticmethod
    def from_dict(an_env_dict):
        collected_info = {}
        for collector_name in an_env_dict.keys():
            CollectorClass = collector_class_lookup[collector_name]
            collected_info[collector_name] = CollectorClass.from_dict(an_env_dict)

        return Environment(collected_info)


    def to_yaml(self, fname):
        with open(fname, 'w') as outfile:
            self._to_yaml_fs(outfile)

    @staticmethod
    def from_yaml(fname):
        with open(fname, 'r') as infile:
            return Environment._from_yaml_fs(infile)
if __name__ == '__main__':
    env = Environment()
    env.to_yaml("try_it.yaml")
    env2 = Environment.from_yaml("try_it.yaml")