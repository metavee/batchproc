# Setting up a build environment

## Targeting Windows from Mac or Linux

### Compiling on the target machine
If you have access to the target machine, try compiling there. If the machine doesn't have Python installed, [WinPython](https://winpython.github.io/) provides a portable distribution of Python that can be used without administrative privileges. Just unpack it on the target machine, do your build there, and you should be good to go.

### Virtual Machine
If you have a spare license key for Windows, you can quickly set up a virtual machine using something like [VirtualBox](https://www.virtualbox.org/). You can then install Python and get your script working and run PyInstaller from within the VM to build the executable. Although it's a rather heavyweight solution, it is fairly reliable.

### Wine
You can use [Wine](https://www.winehq.org/) to install the Windows version of Python on your Linux or Mac machine. Then, through Wine, you can run the Windows version of PyInstaller on your script. It's a little awkward, but doesn't require a real copy of Windows itself. Building your script in Wine should provide Windows XP-level compatibility, but you should make sure to install the 32-bit version of Wine if you need your script to work on 32-bit machines.

## Targeting Linux from Mac or Windows

### Virtual Machine
There are many Linux distributions which can be downloaded and used free of charge, so you can set up a virtual machine as described in the section on targeting Windows from Mac or Linux. To ensure compatibility on a variety of Linux systems, you may need to install an older distribution, as the version of libc present on the system will determine the level of backwards compatibility. The PyInstaller FAQ suggests [CentOS 5](https://wiki.centos.org/Download) as an extreme case, though it comes with Python 2.4, meaning that you will have to go through some trouble installing a modern version. If the requirements for backwards compatibility are less severe, choosing the oldest [Ubuntu LTS](https://wiki.ubuntu.com/Releases) still supported will likely be more convenient.

Note that on Linux, 64-bit systems may have compatibility issues with 32-bit applications. So if you plan to support both architectures, you may need to build a 64-bit and 32-bit version and distribute them separately.

## Targeting Mac from Windows or Linux
I am not personally familiar with any good way to do this. Virtual machines are generally not an option, due to legal and technical issues.

However, there are some businesses which rent remote access to Macs, so that may be a method to quickly get access to a Mac build environment. I have never tried any of these services, so I can't vouch for their authenticity, but some are listed in [this StackOverflow thread](https://stackoverflow.com/questions/7308039/do-on-demand-mac-os-x-cloud-services-exist-comparable-to-amazons-ec2-on-demand).
