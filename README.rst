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


Python environment comparison tool.  Maximized for compatibility between
python forks, 2.6 to 3.7, pypy, and more!

Command Usage
-------------

From the command line, to get information on the current environment:
::

    python -m pyenvdiff.info


Serialize the information to a file...
::

    python -m pyenvdiff.info my_environment.yaml


Switch to another environment (you'll need pyenvdiff installed in both)
:: 

    python -m pyenvdiff.compare my_environment.yaml


Or compare two from any environment
::

    python -m pyenvdiff.compare my_environment.yaml my_other_environment.yaml
    

Programmatic Usage
------------------
.. code-block:: python
   
    >>> from pyenvdiff import Environment
    
    >>> e = Environment()
    >>> e.to_yaml('my_env.yaml')
    
    >>> o = Environment.from_yaml('other_env.yaml')
    
    >>> e == o
    True
    
    >>> print(e)
    ... # prints a dump of the environment details
    
    >>> from pyenvdiff import EnvironmentDiff
    >>> ed = EnvironmentDiff(e, o)
    >>> print(ed)
    ... # prints a diff of the two environments

Web Usage
---------

An alpha-level web-based comparison tool is available to browse and compare.  PyEnvDiff ships with a default API Key, which is severly throttled.  Some jerk is likely to abuse it, but until then, try it out.  API keys are manually issued by the maintainer.  You can get one by e-mailing, eg. "Hey, I'd like an API key.". :)  My e-mail is sprinkled in this repo, but also 

Install your own API key by setting a global environment variable "PYENVDIFF_API_KEY", set to the api key.

From any two python interpreters, you can run:
::

    python -m pyenvdiff.post --email your.email@someserver.com

    or...

    python -m pyenvdiff.post --domain your.website.com

    ...for more optional meta data fields:

    python -m pyenvdiff.post -h


Which should output... something like the below, (once for each environment you run it).
::

    Posting environment information to https://osa.pyenvdiff.com
    Using API KEY: ...
    Successful POST, use SHA XXXX for reference or comparison.

Then, hit http://pyenvdiff.com/compare.html?left=XXXX&right=YYYY where XXXX and YYYY are the two relevant SHAs.


Sooo much room for activities!
------------------------------

* Compare dev, test & prod!
* Works on my machine, strange it doesn't work on yours
* Confirming deployments
* Auditing user desktops, servers, research environments & ecosystems
* Filing (or requesting) bug reports

Installation
------------

``
pip install pyenvdiff 
``

OR just copy & paste pyenvdiff anywhere on PYTHONPATH

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

