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

    index = set(file for file, _ in koan.get_repo().index.entries.keys())
    expected_files = {'foo'}
    extra_files = index.difference(expected_files)

    assert expected_files.issubset(index), ('Expected to find file `foo` in the index. '
                                            'Current index is {}'.format(index or 'empty'))

    assert not extra_files, f'Unexpected files in the index: {extra_files}'
