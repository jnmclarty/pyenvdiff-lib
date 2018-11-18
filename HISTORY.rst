=======
History
=======

0.3.0 (2018-11-18)
------------------

* Add bottle-based Hub for P2P Comparisons
* Added Python 3.8 Support
* Fixed bug impacting Ubuntu 18 [GH Issue #15]
* Removed documented support for Third-party API-enabled comparisons
* Enhanced the SysPrefix collector. [PR#16]
* Add error attribute to Collectors. [PR#16]
* Fixed Docs on PyPI, added comments inline.
* Improved language in console output.

0.2.0 (2018-06-8)
-----------------

* Refactor info.py into environment.py to account for regression in cpython micro release (#5) [PR #6]
* Change file format from yaml to json with sorted keys (#4) [PR #7]
* Remove pyenvdiff.com as default server. [PR #8]
* Simplify user-created custom Collector. [PR #8]
* Enable user-created custom POST command. [PR #8]
* Add more Collectors (OSEnviron, UserName, HomeDirectory, SysPrefix). [PR #9]
* Add transparency to systematically disclose what information is collected. [PR #9]
* Add invasive property [PR #9]
* Make compatible with pip 10. [PR #10]
* Enhance PipDistribution output. [PR #10]

0.1.0 (2016-12-24)
------------------

* First release on PyPI.
