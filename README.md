A "graphical" text editor inspired by [PICO-8](https://www.lexaloffle.com/pico-8.php)'s code editor.

<p align="center">
  <img src="https://raw.githubusercontent.com/echo8/editor/master/resources/demo.gif"/>
</p>

### Installation

SDL2 + Python bindings:

    $ apt-get install python-sdl2

Clone this repository:

    $ git clone https://github.com/echo8/editor.git

Run it:

    $ cd editor
    $ python2.7 main.py

### Usage

    $ python2.7 main.py --help
    usage: main.py [-h] [-r RESOLUTION] [file]

    positional arguments:
      file                  file to edit

    optional arguments:
      -h, --help            show this help message and exit
      -r RESOLUTION, --resolution RESOLUTION
                            size of window in x,y format

#### Key Bindings

* **New File**: <kbd>Ctrl-N</kbd>
* **Open**: <kbd>Ctrl-O</kbd>
* **Save**: <kbd>Ctrl-S</kbd>
* **Save As**: <kbd>Ctrl-Shift-S</kbd>
* **Quit**: <kbd>Ctrl-Q</kbd>
