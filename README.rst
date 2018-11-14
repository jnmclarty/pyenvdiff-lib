===============================
PyEnvDiff
===============================


.. image:: https://img.shields.io/pypi/v/pyenvdiff.svg
        :target: https://pypi.python.org/pypi/pyenvdiff

.. image:: https://travis-ci.org/jnmclarty/pyenvdiff-lib.svg?branch=master
    :target: https://travis-ci.org/jnmclarty/pyenvdiff-lib

.. image:: https://readthedocs.org/projects/pyenvdiff/badge/?version=latest
    :target: http://pyenvdiff.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Python environment comparison tool.  Maximized for compatibility between versions 2.6 to 3.7, pypy,
operating systems, distributions, and forks!  Virtualenv, pyenv, pyvenv, conda, system!

Command Usage
-------------

From the command line, to get information on the current environment:

::

    python -m pyenvdiff.info


Serialize the information to a file...

::

    python -m pyenvdiff.info my_environment.json


Switch to another environment (you'll need pyenvdiff installed in both)

::

    python -m pyenvdiff.compare my_environment.json


Or compare two from any environment

::

    python -m pyenvdiff.compare my_environment.json my_other_environment.json


Programmatic Usage
------------------
.. code-block:: python

    >>> from pyenvdiff import Environment

    >>> e = Environment()
    >>> e.to_file('my_env.json')

    >>> o = Environment.from_file('other_env.json')

    >>> e == o
    True

    >>> print(e)
    ... # prints a dump of the environment details

    >>> from pyenvdiff import EnvironmentDiff
    >>> ed = EnvironmentDiff(e, o)
    >>> print(ed)
    ... # prints a diff of the two environments


Sooo much room for activities!
------------------------------

* Compare dev, test & prod!
* Works on my machine, strange it doesn't work on yours
* Confirming deployments
* Auditing user desktops, servers, research environments & ecosystems
* Filing (or requesting) bug reports

Installation
------------

There are no manditory, nor automatically installing, dependencies.

::

    pip install pyenvdiff

OR just copy & paste pyenvdiff anywhere on PYTHONPATH

There is one optional dependency.  The core functionality doesn't use it.  It's only needed for more advanced HTML-based comparison.

::

    pip install ghdiff


Under the hood
--------------

* Zero dependency, pure-python, harmless `pip install pyenvdiff` or copy anywhere on PYTHONPATH.
* As-needed import statements, to maximize compatibility across python flavours.
* Favours compatible python-code over succinct or newer-style python-code
* Free software: BSD license
* Documentation: https://pyenvdiff.readthedocs.io.

Credits
---------

This package was started with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
