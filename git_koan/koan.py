import os

import delegator
import git
import pytest


class Koan:
    TIMEOUT = 3

    def __init__(self, tmpdir):
        self.verbose = False

        self._tmpdir = tmpdir
        self._commands = []

    def assert_repo(self, relative_path='.'):
        assert self.get_repo(relative_path), 'Repository has not been created.' + self._debug_prints()

    def assert_commands(self):
        for c in self._commands:
            assert c.return_code == 0, \
                f'Command "{c.cmd}" finished with a non-zero status ({c.return_code}).' + self._debug_prints()

    def get_repo(self, relative_path='.'):
        try:
            repo = git.Repo(os.path.join(self.tmpdir, relative_path))
        except (git.InvalidGitRepositoryError, git.NoSuchPathError):
            repo = None

        return repo

    @property
    def tmpdir(self):
        return str(self._tmpdir)

    def shell(self, command):
        if not command:
            pytest.fail('Cannot run an empty command!')

        self._commands.append(delegator.run(command, timeout=Koan.TIMEOUT, cwd=self.tmpdir))

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

        return buffer.replace(str(self.tmpdir), '.')
