# cmdshow
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)  
`cmdshow` is a Python tool/library to create slideshows out of images - super fast! It provides a wide range of options to customize the slideshow, while setting sensible defaults for when you need that slideshow yesterday. A user-friendly CLI as well as a GUI are available, whichever camp you belong to. 
## Usage
At the most basic level, all you need to do is enter the path to your directory of images - simple as that! `cmdshow` will create a video slideshow out of the images in the given directory, add some background music and some transition effects and generally make it look good. For a list of all configuration options, see the [CLI help](#cli) below
## Installation
See [INSTALL.md](./INSTALL.md)
## CLI
```
$ python cmdshow.py --help
usage: cmdshow.py [-h] [-m PATH_TO_MUSIC] [-fd FRAME_DURATION]
                  [-td TRANSITION_DURATION] [-t TRANSITION_TYPE]
                  [-r RESOLUTION] [-fps FRAMES_PER_SECOND] [-o OUTPUT_PATH]
                  path_to_images

positional arguments:
  path_to_images        Path to dirctory containing the images.

optional arguments:
  -h, --help            show this help message and exit
  -m PATH_TO_MUSIC, --music PATH_TO_MUSIC
                        Path to the music file.
  -fd FRAME_DURATION, --fduration FRAME_DURATION
                        Duration of each frame.
  -td TRANSITION_DURATION, --tduration TRANSITION_DURATION
                        Duration of transition.
  -t TRANSITION_TYPE, --transition TRANSITION_TYPE
                        Type of transition. For more clarity visit: https://trac.ffmpeg.org/wiki/Xfade
  -r RESOLUTION, --resolution RESOLUTION
                        Desired resolution
  -fps FRAMES_PER_SECOND, --frames FRAMES_PER_SECOND
                        Number of Frames per second.
  -o OUTPUT_PATH, --output OUTPUT_PATH
                        Output path for the resultant sildeshow.
```
## GUI
![Screenshot of GUI](./GUI.png)
## License
[MIT License](./LICENSE)
