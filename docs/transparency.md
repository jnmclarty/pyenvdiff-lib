Platform
========
See *pyenvdiff.collectors.Platform*
NOT Included by default.  A user-app would need to delete it from an Environment.
```python
import platform as p
return [p.platform(), p.processor()] + list(p.architecture())

```
Pkgutil Modules
===============
See *pyenvdiff.collectors.PkgutilModules*
NOT Included by default.  A user-app would need to delete it from an Environment.
```python
import pkgutil
info = [m for i, m, p in pkgutil.iter_modules() if p]
info.sort()
return info

```
Pip Installed Distributions
===========================
See *pyenvdiff.collectors.PipDistributions*
NOT Included by default.  A user-app would need to delete it from an Environment.
```python
import pip
ins_dis = pip.get_installed_distributions()
info = []
for dis in ins_dis:
    relevant = {}
    for attr in PipDistributions.attrs:
        relevant[attr] = str(getattr(dis, attr))
    info.append(relevant)
return sorted(info, key=lambda x: x['project_name'])

```
sys.byteorder Information
=========================
See *pyenvdiff.collectors.SysByteOrder*
NOT Included by default.  A user-app would need to delete it from an Environment.
```python
import sys
return sys.byteorder

```
sys.executable Information
==========================
See *pyenvdiff.collectors.SysExecutable*
NOT Included by default.  A user-app would need to delete it from an Environment.
```python
import sys
return sys.executable or "None Found"

```
sys.path Contents
=================
See *pyenvdiff.collectors.SysPath*
NOT Included by default.  A user-app would need to delete it from an Environment.
```python
import sys
return [x for x in sys.path]

```
sys.platform Information
========================
See *pyenvdiff.collectors.SysPlatform*
NOT Included by default.  A user-app would need to delete it from an Environment.
```python
import sys
return sys.platform

```
sys.version Information
=======================
See *pyenvdiff.collectors.SysVersion*
NOT Included by default.  A user-app would need to delete it from an Environment.
```python
import sys
return sys.version

```
Interpreter Version Information
===============================
See *pyenvdiff.collectors.SysVersionInfo*
NOT Included by default.  A user-app would need to delete it from an Environment.
```python
import sys
info = {}
for i, attr in enumerate(SysVersionInfo.attrs):
    info[attr] = sys.version_info[i]
return info

```
sys.float_info Contents
=======================
See *pyenvdiff.collectors.SysFloatInfo*
NOT Included by default.  A user-app would need to delete it from an Environment.
```python
import sys
return list(map(str, sys.float_info))

```
sys.api_version Information
===========================
See *pyenvdiff.collectors.SysApiVersion*
NOT Included by default.  A user-app would need to delete it from an Environment.
```python
import sys
return sys.api_version

```
os.uname() Information
======================
See *pyenvdiff.collectors.OSUname*
NOT Included by default.  A user-app would need to delete it from an Environment.
```python
import os
return " ".join(os.uname())  # Unix only

```
Time Zone Information
=====================
See *pyenvdiff.collectors.TimeZone*
NOT Included by default.  A user-app would need to delete it from an Environment.
```python
import time
return [str(time.timezone)] + list(time.tzname)

```
sys.prefix, exec_prefix, base_exec_prefix
=========================================
See *pyenvdiff.collectors.SysPrefix*
NOT Included by default.  A user-app would need to delete it from an Environment.
```python
import sys
return [sys.prefix, sys.exec_prefix, sys.base_exec_prefix]

```
os.environ Contents
===================
See *pyenvdiff.collectors.OSEnviron*
Included by default.  A user-app must add it to an Environment.
```python
import os
environ = dict(os.environ)
keys = list(environ.keys())
keys.sort()
out = [(k, environ[k]) for k in keys]
return out

```
User Name
=========
See *pyenvdiff.collectors.UserName*
Included by default.  A user-app must add it to an Environment.
```python
# Note this only works on linux-based systems
import pwd, os
return pwd.getpwuid(os.getuid())[0]

```
Home directory (~)
==================
See *pyenvdiff.collectors.HomeDirectory*
Included by default.  A user-app must add it to an Environment.
```python
import os
return os.path.expanduser('~')

```