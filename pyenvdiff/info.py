

if __name__ == '__main__':

    from .environment import Environment
    from .import_macros import import_sys

    env = Environment()
    print(env)

    sys = import_sys()

    # We're not going to expand on this, in order to maintain compatibility.
    args = sys.argv
    if len(args) > 1:
        fname = args[1]
        env.to_file(fname)
        print("\nStored environment information to " + fname)
