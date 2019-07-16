# Making a stand-alone executable

## Summary

The simplest way to make your script into a stand-alone executable is with [PyInstaller](http://www.pyinstaller.org/). Once you've installed PyInstaller, you can run `pyinstaller name_of_your_script.py`, and it will make a folder called `dist/name_of_your_script` which contains an executable version of your script along with other files that are necessary for it to run. A few ways to customize the behavior of PyInstaller are described [here](pyinstaller_usage.html).

The compiled executable should be compatible with all computers with an operating system of a similar age or newer than the computer it was built on. If you want to have very broad compatibility, do the compilation in a relatively old environment. See [here](build_env.html) for some guidelines on setting up a build environment, and building for different OSes.

There are a variety of problems you could potentially run into. Some are described [here](problems.html).

## Motivations

It can be inconvenient to run Python scripts. Unless you've set things up otherwise, you generally have to open a terminal, or your editor in order to run a script. Not to mention, Python might not even be installed on the computer you want to use.

These might seem like petty issues, but they should cause some hesitation when considering using Python.

However, it is possible to pack your script together with a portable distribution of Python, allowing you to run your script by double-clicking it. If done correctly, it will also run on a variety of computers, without needing any installation or administrative privileges.

## General considerations

Making an executable version of a script is not always straightforward. There are many variables that can influence your results, including your code, what Python libraries you use, what versions of those libraries you have installed, etc. As such, this document is not (and cannot be) comprehensive. It is merely meant to be a loose guide, and also to address some issues specific to this library.

You must decide what platforms you want to support. Windows, Mac, or Linux? 32-bit or 64-bit? Is it okay if it only runs on Windows 10, or should it support Windows 7 and Windows XP too? Keep in mind that newer versions of Python might not work on older operating systems. For example, Python 3.5 and newer do not officially support Windows XP, so you might be forced to rewrite code to run on Python 3.4, or decide not to support Windows XP in that case.

As a rule of thumb, it is easiest to target machines that are as similar as possible to yours. If you work in an office where your IT department has provided the same type of computer to you and all your colleagues, then you can fairly easily compile an executable that runs in that environment. If you run Mac, but want to build your script to use on old Windows XP machines in your lab, you should be prepared to do more work. **If it's feasible for your application, you should compile it on the same computer that you intend to use the executable on.**

Another rule of thumb is that when you compile your script, it will typically have good forward compatibility, and poor backward compatibility. That is, if you compile your script on a 32-bit Windows XP machine, it will probably also run on 64-bit Windows 10 machines, but the reverse is less likely to be true.

Although many tools exist for creating standalone executables from Python scripts, this guide will focus on [PyInstaller](http://www.pyinstaller.org/), since it supports many platforms, and is being actively developed at the time of writing (2016). Well-known alternatives include [cx_Freeze](http://cx-freeze.sourceforge.net/), [py2exe](http://www.py2exe.org/), and [py2app](https://pythonhosted.org/py2app/).
