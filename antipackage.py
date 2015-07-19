# encoding: utf-8
"""Automagically import single file Python modules from GitHub.

To use, just import `antigravity`:

    import antigravity

Then you can import single file Python modules from GitHub using:

    from github.username.repo import module

Modules are downloaded and cached locally. They are automatically updated to the latest version
anytime they change on GitHub.
"""

from __future__ import print_function
import os
import sys
import hashlib
import shutil
# Imports for urllib are different in py2 vs. py3
try: 
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve


class InstallError(Exception):
    pass

class GitHubImporter(object):
    
    def __init__(self):
        self.base_dir = os.path.expanduser('~/.antipackage')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        sys.path.append(self.base_dir)

    def _parse_fullname(self, fullname):
        comps = fullname.split('.')
        top, username, repo, modname = None, None, None, None
        if len(comps)>=1:
            top = 'github'
        if len(comps)>=2:
            username = comps[1]
        if len(comps)>=3:
            repo = comps[2]
        if len(comps)>=4:
            modname = comps[3]
        return top, username, repo, modname
        
    def _install_init(self, path):
            ipath = os.path.join(path, '__init__.py')
            # print('Installing: ', ipath)
            self._touch(ipath)

    def _setup_package(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        self._install_init(path)

    def _update_if_changed(self, old, new):
        new_hash = ''
        with open(new, 'r') as f:
            new_hash = hashlib.md5(f.read()).hexdigest()
        old_hash = ''
        if os.path.isfile(old):
            with open(old, 'r') as f:
                old_hash = hashlib.md5(f.read()).hexdigest()
        if new_hash!=old_hash:
            shutil.copy(new, old)
            if old_hash:
                return 'updated'
            else:
                return 'installed'
        return 'noaction'

    def _touch(self, path):
        with open(path, 'a'):
            os.utime(path, None)

    def _install_module(self, fullname):
        top, username, repo, modname = self._parse_fullname(fullname)
        url = 'https://raw.githubusercontent.com/%s/%s/master/%s' % (username, repo, modname+'.py')
        print('Downloading: ', url)
        try:
            tmp_file, resp = urlretrieve(url)
            with open(tmp_file, 'r') as f:
                new_content = f.read()
            if new_content=='Not Found':
                raise InstallError('remote file does not exist')
        except IOError:
            raise InstallError('error downloading file')
        
        new = tmp_file
        old = self._install_path(fullname)
        updated = self._update_if_changed(old, new)
        if updated=='updated':
            print('Updating module: ', fullname)
        elif updated=='installed':
            print('Installing module: ', fullname)
        elif updated=='noaction':
            print('Using existing version: ', fullname)

    def _install_path(self, fullname):
        top, username, repo, modname = self._parse_fullname(fullname)
        return os.path.join(self.base_dir, top, username, repo, modname+'.py')

    def _make_package(self, fullname):
        top, username, repo, modname = self._parse_fullname(fullname)
        if repo is not None:
            repo_path = os.path.join(self.base_dir, top, username, repo)
            self._setup_package(repo_path)
        if username is not None:
            user_path = os.path.join(self.base_dir, top, username)
            self._setup_package(user_path)
        if top is not None:
            top_path = os.path.join(self.base_dir, top)
            self._setup_package(top_path)
        if modname is not None:
            try:
                self._install_module(fullname)
            except InstallError:
                if os.path.isfile(self._install_path(fullname)):
                    print('Using existing version: ', fullname)
                else:
                    print('Error installing/updating module: ', fullname)

    def find_module(self, fullname, path=None):
        # print('find_module', fullname, path)
        if fullname.startswith('github'):
            self._make_package(fullname)
        return None

sys.meta_path = [GitHubImporter()]