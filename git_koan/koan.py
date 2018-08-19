from collections import namedtuple
import os
import subprocess


import git
import pexpect
import pytest

Command = namedtuple('Command', ('cmd', 'return_code', 'out', 'err'))


class Koan:
    TIMEOUT = 3

    def __init__(self, tmpdir_factory):
        self.verbose = False

        self._workspace = tmpdir_factory.mktemp('workspace')
        self._upstream = tmpdir_factory.mktemp('upstream')
        self._commands = []

    def assert_repo(self, relative_path='.'):
        assert self.get_repo(relative_path), 'Repository has not been created.' + self._debug_prints()

    def assert_commands(self):
        for c in self._commands:
            assert c.return_code == 0, \
                f'Command "{c.cmd}" finished with a non-zero status ({c.return_code}).' + self._debug_prints()

    def assert_remotes(self, expected_remotes=None, relative_path='.'):
        assert expected_remotes is not None, 'assert_remotes cannot be called with `None` as `expected_remotes`'

        repo = self.get_repo(relative_path)
        remotes = {(remote.name, url) for remote in repo.remotes for url in remote.urls}
        for r in expected_remotes:
            assert r in remotes, f'Expected remote: {r} is not present in remote urls: {remotes}'

        unexpected_remotes = remotes.difference(expected_remotes)
        assert not unexpected_remotes, f'There are some unexpected remotes: {unexpected_remotes}'

    def get_repo(self, relative_path='.'):
        try:
            repo = git.Repo(os.path.join(self.workspace, relative_path))
        except (git.InvalidGitRepositoryError, git.NoSuchPathError):
            repo = None

        return repo

    @property
    def workspace(self):
        return str(self._workspace)

    @property
    def upstream(self):
        return str(self._upstream)

    def shell(self, command, cwd='.'):
        if not command:
            pytest.fail('Cannot run an empty command!')

        p = subprocess.Popen(command, shell=True, cwd=os.path.join(self.workspace, cwd),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            stdout, stderr = p.communicate(timeout=Koan.TIMEOUT)
            return_code = p.returncode
        except subprocess.TimeoutExpired:
            p.kill()
            stdout, stderr = p.communicate()
            return_code = 'TIMED OUT'

        self._commands.append(Command(command, return_code, stdout, stderr))

    def edit(self, file, cwd='.', editor='editor'):
        editor = pexpect.spawn(f'{editor} {file}', cwd=os.path.join(self.workspace, cwd))
        editor.interact()

    def _debug_prints(self):
        buffer = ''
        for i, c in enumerate(self._commands):
            buffer += (f'''
# Command ({i+1}/{len(self._commands)}): "{c.cmd}":
# exit code: {c.return_code}
# stdout:
{c.out}
# stderr:
{c.err}
''')

        if self.verbose:
            return buffer

        return buffer.replace(str(self.workspace), '.')
