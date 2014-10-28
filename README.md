AntiPackage
===========

The anti package manager for auto-importing Python modules from GitHub.

## Installation

```
pip install git+https://git.myproject.org/antipackage#egg=antipackage
```

## Usage

Enable `antipackage` by simply importing it:

```python
import antipackage
```

Then you can import single file Python modules at the top level of GitHub repos
using the syntax:

```python
from github.username.repo import module
```

So for example, this repo has a top-level `foo.py`. It can be imported using:

```python
from github.ellisonbg.antipackage import foo
```

When a module is imported it is downloaded into the location
`~/.antipackage/github/username/repo` and cached for future usage.