from collections import namedtuple
import io
import os

import git
import pexpect
import pytest

Command = namedtuple('Command', ('cmd', 'return_code', 'out'))


class Koan:
    TIMEOUT = 3

    def __init__(self, tmpdir_factory):
        self.verbose = False

        self._workspace = tmpdir_factory.mktemp('workspace')
        self._upstream = tmpdir_factory.mktemp('upstream')
        self._commands = []
        self._say('\n')

    def assert_repo(self, relative_path='.'):
        assert self.get_repo(relative_path), 'Repository has not been created.' + self.commands_debug()

    def assert_commands(self):
        for c in self._commands:
            assert c.return_code == 0, \
                f'Command "{c.cmd}" finished with a non-zero status ({c.return_code}).' + self.commands_debug()

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

    def _say(self, s):
        if self.verbose:
            print(s)

    @property
    def workspace(self):
        return str(self._workspace)

    @property
    def upstream(self):
        return str(self._upstream)

    def shell(self, command, interactive=False, cwd='.'):
        if not command:
            pytest.fail('Cannot run an empty command!')

        pretty_cwd = f'({cwd})' if cwd != '.' else ''
        self._say(f'{pretty_cwd}$ {command}')

        out = io.StringIO()
        p = pexpect.spawn(command, cwd=os.path.join(self.workspace, cwd), logfile=out, encoding='utf8')

        if interactive:
            p.logfile = None
            p.interact()
        else:
            try:
                p.expect(pexpect.EOF, timeout=self.TIMEOUT)
            except pexpect.TIMEOUT:
                print(f"Command `{command}` timed-out -- moving into interactive mode. "
                      f"Consider using ctrl-c to stop the command if it's not responding.")
                p.logfile = None
                p.interact()

        p.wait()
        out.seek(0)
        self._commands.append(Command(command, p.exitstatus, str(out.read())))

    def edit(self, file, cwd='.', editor='editor'):
        self.shell(f'{editor} {file}', interactive=True, cwd=cwd)

    def commands_debug(self):
        buffer = ''
        for i, c in enumerate(self._commands):
            buffer += (f'''
# Command ({i+1}/{len(self._commands)}): "{c.cmd}":
# exit code: {c.return_code}
# output:
{c.out}
''')

        if self.verbose:
            return buffer

        return buffer.replace(str(self.workspace), '.')
