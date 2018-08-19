import importlib
import sys

REQUIRED_MODULES = ('pytest', 'delegator', 'git')
NO_GIT = 'Looks like `git` is not in PATH. Make sure it is present there before running this script.'
MISSING_MODULE = ('Looks like "{name}" module is missing in your environment. '
                  'Please make sure that you have installed all the requirements from the requirements.txt file.\n')

has_modules = True
for m in REQUIRED_MODULES:
    try:
        locals()[m] = importlib.import_module(m)
    except ImportError:
        sys.stderr.write(MISSING_MODULE.format(name=m))
        has_modules = False

if not has_modules:
    exit(1)

assert delegator.run('which git', timeout=2).return_code == 0, NO_GIT
