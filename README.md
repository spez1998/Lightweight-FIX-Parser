# Lightweight-FIX-Parser
A lightweight, fast parser for FIX messages.

Intended to be used for quick translation of a FIX message whilst debugging.

Licensed under the GNU General Public License 3.0

## Installation
### Linux
1. Clone or download the repository.
2. Run `linux_installer` as root. **NOTE that this is optional** as explained in the Usage section.

### Windows
1. Simply clone or download the repository.

## Usage
### Linux
If you used the `linux_installer` script, an executable script file called `fixparse` is placed into your `/usr/bin` directory. Therefore, run:
```
$ fixparse
```
to run the script.

If you did not use the `linux_installer` script, the script can be run as follows:
```
$ python3 /path/to/repository/parser.py
```
### Windows
Double-click the `parser.py` file to run the script. 

## Known Issues
- Piping data into the script causes Python's standard input to reach EOF before you can be prompted to run the script again. This will cause the script to exit, just re-run the script without piping data into it to continue using it and keep it open indefinitely. The exit message for the condition described details this.
<<<<<<< HEAD
- On Windows, CTRL-C will not break the script and close the program. To exit the program, close the terminal window.
=======
- CTRL-V in Windows caused the program to close because CTRL-V is a KeyboardInterrupt, so the exit condition for this is temporarily disabled. Standby for a proper exit function.

