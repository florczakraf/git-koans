# Git Koans

## Usage
Fill in the tasks in `git-koans/git-koans.py` and run:
```bash
$ ./enlighten.sh
```

## Manual
Each task is represented by a pytest's test case. In the docstring there's an explanation of the result you want to
achieve at it's end. Each koan starts with an empty working directory unless stated otherwise in the assignment's
description.

You interact with the working directory using `koan.shell(command, interactive=False, cwd='.')` method which executes
your commands. You can switch the working directory by providing a relative path as the `cwd` argument. Please note
that there are no input constraints on the commands you type so type wisely, as they will be executed on the real
filesystem. `shell` by default works in a non-interactive mode -- it means that your commands will execute silently,
without outputting anything to the stdout/err. If their execution is taking long time, the interactive mode will be
enabled for you so you will have an opportunity to see all of it's output as well as interact using keyboard/mouse.
For instance, it could be an interactive git command that requires some input from user. When you expect your command
to be interactive, you can use the `interactive=True` as an argument, to skip the waiting time and go straight to the
interactive mode.

There's also an experimental `koan.edit(file, cwd='.', editor='editor')` method that should run your favorite editor
with a specified file from the working directory in case you want to inspect or modify it. It's just a shorthand for
`shell` with interactive mode enabled and default command set to the 'editor' with given file. Please note that on some
operating systems there's no `editor` command so you will have to pick your editor explicitly. In this case there's no
gain compared to the usual `shell` command ran in interactive mode.

Examples:
```python
koan.shell('echo foo > bar')
koan.shell('mkdir qux')
koan.shell('touch', cwd='qux')
koan.shell('git log', interactive=True)
koan.edit('bar')
koan.edit('bar', editor='emacs -nw')
```

In some cases it might be useful to understand what is happening by checking non-interactive commands' output. You can
get the summary as a neat string with `koan.commands_debug()` method. Simple usage: `print(koan.commands_debug())`. It
also includes exit code of each command.

To increase the verbosity of the output (both koan's default and debug's), use:
```python
koan.verbose = True
```
inside the assignment. For example, it will print the actual paths used as workspace during execution instead of `.`
so you can verify everything yourself when something goes west.

## Requirements:
`git` in `PATH` and all the python packages from `requirements.txt`. You can get the latter with `pip`:
```bash
[sudo] pip install -r requirements.txt
```
