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


def test_add_to_index(koan, assert_index_includes_added_file):
    """ Create a repository and add a file `foo` to the staging area (a.k.a index). Please note that you might need to
        use multiple commands to keep your solution clean and natural. Starting from the next koan, there
        will be only one placeholder by default. Feel free to use as many commands as you think you need.
    """
    koan.shell('')
    koan.shell('')
    koan.shell('')
