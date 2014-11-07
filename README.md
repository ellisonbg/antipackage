AntiPackage
===========

Automagically import single file Python modules from GitHub.

## Installation

The `antigravity` package can be installed from GitHub using `pip`:

```
pip install git+https://github.com/ellisonbg/antipackage.git#egg=antipackage
```

## Usage

Enable `antipackage` by simply importing it:

```python
import antipackage
```

Once `antigravity` has been imported you can simply import modules from GitHub using the syntax:

```python
from github.username.repo import module
```

When you do this, the import hook will automatically download and install single file
Python modules into the location `~/.antipackage/github/username/repo/module.py`. If the
module every changes on GitHub it will be updated next time you import it.

## Absolute imports

The `antigravity` package is written looking forward to the days when Python 2 is no longer
supported. Because of this, the import hooks used in `antipackage` assume that relative imports
are not used in the single file modules that are being imported. To enable this behavior for Python 2,
add the following line at the top of your modules:

```python
from __future__ import absolute_import
```

Like this: https://github.com/ellisonbg/misc/blob/master/vizarray.py#L26
