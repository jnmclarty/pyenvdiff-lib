from pyenvdiff.collectors import collector_classes

import inspect

for CollectorClass in collector_classes:
    from_env = CollectorClass.from_env

    code = inspect.getsourcelines(from_env)

    for c in code:
        if not isinstance(c, int):
            name = CollectorClass.__name__
            english = CollectorClass().english

            print(english)
            print("=" * len(str(english)))
            print("See *pyenvdiff.collectors.{}*".format(name))
            if CollectorClass.invasive:
                print("Included by default.  A user-app must add it to an Environment.")
            else:
                print("NOT Included by default.  A user-app would need to delete it from an Environment.")
            print("```python")
            print("".join(map(lambda x : x[8:], c[2:])))
            print("```")

