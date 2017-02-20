# -*- coding: utf-8 -*-

from .import_macros import import_sys, import_os
from .environment import Environment, EnvironmentDiff

if __name__ == '__main__':
    sys = import_sys()
    os = import_os()

    args = sys.argv

    if len(args) == 2:
        fname = args[1]
        cur_env = Environment()
        print(cur_env)

        if os.path.exists(fname):
            oth_env = Environment.from_file(fname)
        else:
            print("\nFile not found:" + fname)
            sys.exit()

    elif len(args) == 3:
        left_env = args[1]
        right_env = args[2]

        for fname in [left_env, right_env]:
            if not os.path.exists(fname):
                print("\nFile not found:" + fname)
                sys.exit()

        left_env = Environment.from_file(left_env)
        right_env = Environment.from_file(right_env)

        ed = EnvironmentDiff(left_env, right_env)
        print(ed)

    else:
        print("\nPyEnvDiff comparison usage options:")
        print("\n   python -m pyenvdiff.compare env_one.yaml env_two.yaml")
        print("\n   python compare.py env_one.yaml env_two.yaml")
