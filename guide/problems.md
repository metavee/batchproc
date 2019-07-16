# General issues

## The executable is created, but doesn't do anything
Check the log file to see if any Python errors show up. Try running the executable from the terminal to see if any other errors get printed out.

## Errors relating to `unexpected keyword argument 'delimiters'`
This issue should only affect Python 2.7. The Python package `future`, which is required by many packages (including PyInstaller) provides a duplicate version of `configparser`, which is incompatible with the version of `configparser` used by `doit`.

The bug is described [here](https://github.com/PythonCharmers/python-future/issues/118), and should be resolved with the release of `future` 0.16.

One very hackish workaround is to surgically remove the version of `configparser` installed by `future`. I found it in Python's `site-packages` folder, under `configparser`. You can just rename that folder to something else for the moment, run PyInstaller, and then name it back to prevent any nasty issues from cropping up in the future.

# Windows-specific issues

## Errors relating to `MSVCR71.dll` / `MSVCR90.dll` / `MSVCR100.dll`  / `MSVCR140.dll`

Running Python on Windows requires that a certain version of the Microsoft Visual C++ runtime be installed. The version required depends on the version of Python. Most computers should have these installed already, but if you get an error message that `MSVCR__.dll is missing`, then it indicates that you need to install the appropriate version. Microsoft freely provides downloads of these files on their website, with titles like `Visual C++ 2008 Redistributable Package` or `Visual C++ Redistributable for Visual Studio 2015`. 32-bit versions are labelled `x86`, and 64-bit versions are labelled `x64`.

The table below shows the required version of the Visual C++ runtime for each version of Python.

| Python version | MSVCR__.dll | Visual C++ ____ Redistributable |
|----------------|-------------|---------------------------------|
| 2.4 - 2.5      | 71          | 2005                            |
| 2.6 - 3.2      | 90          | 2008                            |
| 3.3 - 3.4      | 100         | 2010                            |
| 3.5 - 3.6      | 140         | 2015                            |

Note that PyInstaller 3.2 on Python 2.7 has a [bug](https://github.com/pyinstaller/pyinstaller/issues/1974) where it will also add a dependency on `MSVCR100.dll`, but this can be avoided by installing a newer or later version of PyInstaller.

## Can't import configparser/ConfigParser

This issue should only affect Python 2.7 on Windows. PyInstaller, up to version 3.2, has a [bug](https://github.com/pyinstaller/pyinstaller/issues/1935) where it fails to properly detect when multiple packages with the same name are used (not considering upper/lower case). As a result, it only includes one of configparser or ConfigParser.

One workaround for this issue is to force it to include ConfigParser, and write a hook that provides the functionality of configparser even if it's not properly included.

You can do this by running PyInstaller with the following options:

`--hiddenimport ConfigParser --runtime-hook replace_configparser.py`


where `replace_configparser.py` is a Python file containing the following program:
```
import ConfigParser
import sys

if 'configparser' in sys.modules:
    del sys.modules['configparser']

sys.modules['configparser'] = __import__('ConfigParser')
```
