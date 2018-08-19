# Git Koans

## Usage
Fill in the tasks in `git-koans/git-koans.py` and run:
```bash
$ ./enlighten.sh
```

You interact with the working directory using `koan.shell` method which executes your commands. You can alter the 
working directory by providing a relative path as the `cwd` argument. Please note that there are no input constraints 
on the commands you type so type wisely, as they will be executed on the real filesystem. Examples:
```python
koan.shell('echo foo > bar')
koan.shell('mkdir qux')
koan.shell('touch', cwd='qux')
```

Each koan starts with an empty working directory unless stated otherwise in the assignment's description.

To increase the verbosity of the output, use:
```python
koan.verbose = True
```
inside the assignment. For example, it will print the actual paths used during execution instead of `.` so you can 
verify everything yourself when something goes west.

## Requirements:
`git` in `PATH` and all the python packages from `requirements.txt`. You can get the latter with `pip`:
```bash
[sudo] pip install -r requirements.txt
```
