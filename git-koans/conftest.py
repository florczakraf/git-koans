import pytest

import git_koan

@pytest.fixture
def koan(tmpdir):
    return git_koan.Koan(tmpdir)


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
