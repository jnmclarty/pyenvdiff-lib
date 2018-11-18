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


Python environment comparison tool.  Maximized for compatibility between versions 2.6 to 3.8, pypy,
operating systems, distributions, and forks!  Virtualenv, pyenv, pyvenv, conda and system!

via Command-Line
----------------

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


via Hub-Based Compare
---------------------

An HTTP-based service comes with pyenvdiff, all without dependencies (thanks to a copy of bottle).  It stores environment
information in RAM, for as long as it runs.  This service should be considered alpha-stage.

To launch the built-in hub (server):

::

    python -m pyenvdiff.hub


Then navigate in your browser to the URL it gives you to see the menu of available options.  Before you send information
about other environments on the same machine, your options will be limited to just viewing the server's environment.

Samples of the `Hub Landing Page`_ and the `Environment Information Page`_ illustrate the features.

From one or more other environments run:

::

   python -m pyenvdiff.post_to_hub


A URL will be displayed to view environment information from any machine on the same network.

Navigate back to the base URL, you'll see more options to compare the two environments.

A Sample of the `Environment Diff Page`_ illustrate what the diff can do (if ```ghdiff``` is installed for the hub).

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

There are no mandatory, nor automatically installing, dependencies.  There are optional dependencies which increase.

::

    pip install pyenvdiff

OR just copy & paste pyenvdiff anywhere on PYTHONPATH

There is one optional dependency.  The core functionality doesn't use it.  It's only needed for pretty HTML-based comparisons via the web.

::

    pip install ghdiff


Under the hood
--------------

* Robust and organized object model collects and serializes environment information.
* Zero dependency, pure-python, harmless install!  Simply `pip install pyenvdiff` or copy anywhere on PYTHONPATH.
* As-needed import statements, to maximize compatibility across python flavours.
* Favours compatible python-code over succinct or newer-style python-code
* Free software: BSD license
* Documentation: https://pyenvdiff.readthedocs.io.

Credits
---------

This package was started with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Hub Landing Page`: https://htmlpreview.github.io/?https://github.com/jnmclarty/pyenvdiff-lib/docs/examples/home.html
.. _`Environment Information Page`: https://htmlpreview.github.io/?https://github.com/jnmclarty/pyenvdiff-lib/docs/examples/environment_info.html
.. _`Environment Diff Page`: https://htmlpreview.github.io/?https://github.com/jnmclarty/pyenvdiff-lib/docs/examples/environment_diff_view.html
