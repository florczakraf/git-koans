def test_create_repository(koan, assert_repo_exists):
    """ Create new empty repository in the current directory """
    koan.shell('')


def test_create_repository_in_other_directory(koan, assert_repo_exists_in_other_directory):
    """ Create new empty repository in `my_new_repo` directory """
    koan.shell('')


def test_clone_repository(koan, assert_cloned_repo_exists):
    """ Clone repo which address is available in koan.upstream into current directory """
    koan.shell('')


def test_clone_repository_into_other_directory(koan, assert_cloned_repo_exists_in_other_directory):
    """ Clone repo which address is available in koan.upstream into `cloned_repo` directory"""
    koan.shell('')
