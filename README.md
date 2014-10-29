AntiPackage
===========

Automagically import single file Python modules from GitHub.

## Installation

Th `antigravity` package can be installed from GitHub using `pip`:

```
pip install git+https://git.myproject.org/antipackage#egg=antipackage
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
