# PyInstaller usage
PyInstaller is fairly simple to use. Although it doesn't come with Python, you can install it with `pip install pyinstaller`. Once it's installed, just run `pyinstaller name_of_your_script.py` for it to automatically build an executable. You should see a `build` folder and a `dist` folder appear; the executable will be in `dist`. It will likely appear in a folder together with files that are necessary for it to run. That's all that the basic usage entails, though there are many options that you can use to customize the output. A selection of these are described below. The [PyInstaller documentation](https://pythonhosted.org/PyInstaller/index.html) should be consulted for more complete details.

## Packing your script into a single file
Running PyInstaller with the `-F` option will result in all the resources of your script being packged into a single file, rather than a folder of needed files. This tends to result in a smaller overall filesize, though there is a tradeoff in that it may take some extra time to start running your program.

## Changing the icon of the executable
On Windows and Mac, icons can be embedded directly into the executable. Use the option `-i icon_file`, where `icon_file` will be a `.ico` file on Windows, and a `.icns` file on Mac.

On Linux, this can be set inside the `.Desktop` file for your application, which you have to make by hand, as described [here](https://linuxcritic.wordpress.com/2010/04/07/anatomy-of-a-desktop-file/).