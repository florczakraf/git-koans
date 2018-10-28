import os

import git
import pytest

import git_koan


@pytest.fixture(autouse=True)
def visual_separator():
    yield
    print('\n\n------------')


@pytest.fixture
def koan(tmpdir_factory):
    return git_koan.Koan(tmpdir_factory)


@pytest.fixture
def basic_upstream(koan, tmpdir_factory):
    bare_repo = git.Repo.init(koan.upstream, bare=True)
    clone_dir = tmpdir_factory.mktemp('clone')
    clone = bare_repo.clone(str(clone_dir))

    foo = clone_dir.join('foo')
    foo.ensure(file=True)

    clone.index.add(['foo'])
    clone.index.commit('Add foo')
    clone.git.push()


@pytest.fixture
def empty_repo(koan):
    git.Repo.init(koan.workspace)


@pytest.fixture
def assert_repo_exists(koan):
    yield
    koan.assert_commands()
    koan.assert_repo()


@pytest.fixture
def assert_repo_exists_in_other_directory(koan):
    yield
    koan.assert_commands()
    koan.assert_repo('my_new_repo')


@pytest.fixture
def assert_cloned_repo_exists(koan, basic_upstream):
    yield
    clone_path = os.path.basename(koan.upstream)
    koan.assert_commands()
    koan.assert_repo(clone_path)
    koan.assert_remotes(relative_path=clone_path, expected_remotes={('origin', koan.upstream)})


@pytest.fixture
def assert_cloned_repo_exists_in_other_directory(koan, basic_upstream):
    yield
    koan.assert_commands()
    koan.assert_repo('cloned_repo')
    koan.assert_remotes(relative_path='cloned_repo', expected_remotes={('origin', koan.upstream)})


@pytest.fixture
def assert_index_includes_added_file(koan):
    yield
    koan.assert_commands()
    koan.assert_repo()

    index = set(file for file, _ in koan.repo.index.entries.keys())
    expected_files = {'foo'}
    extra_files = index.difference(expected_files)

    assert expected_files.issubset(index), ('Expected to find file `foo` in the index. '
                                            'Current index is {}'.format(index or 'empty'))
    assert not extra_files, f'Unexpected files in the index: {extra_files}'
    assert koan.repo.is_dirty(), 'There are supposed to be uncommitted changes in the repo.'
    assert not koan.repo.untracked_files, 'There are some files in the working directory that are not under version control'


def _assert_identity(config):
    expected_name = 'Foo Bar'
    expected_email = 'foo.bar@example.com'

    assert 'user' in config, 'Git config must inlcude "user" config key'
    name = config.get('user', 'name', fallback=None)
    assert name == expected_name, f'Expected user.name to be "{expected_name}", got "{name}" instead'
    email = config.get('user', 'email', fallback=None)
    assert email == expected_email, f'Expected user.email to be "{expected_email}", got "{email}" instead'


@pytest.fixture
def assert_local_identity_set(koan, empty_repo):
    yield
    config = koan.repo.config_reader('repository')
    _assert_identity(config)


@pytest.fixture
def assert_global_identity_set(koan, empty_repo):
    yield
    config = koan.repo.config_reader('global')
    _assert_identity(config)
