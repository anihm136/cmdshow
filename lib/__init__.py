from pathlib import Path

# import ffmpeg

from .sounds import createSoundEffect
from .transitions import applyTransitions
from .utils import Spinner, getImagesFromPath, orderImages

import gevent.monkey; gevent.monkey.patch_all()

import contextlib
import ffmpeg
import gevent
import os
import shutil
import socket
import subprocess
import sys
import tempfile


@contextlib.contextmanager
def _tmpdir_scope():
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


def _watch_progress(filename, sock, handler):
    connection, client_address = sock.accept()
    data = ''
    with contextlib.closing(connection):
        while True:
            more_data = connection.recv(16)
            if not more_data:
                break
            data += more_data
            lines = data.split('\n')
            for line in lines[:-1]:
                parts = line.split('=')
                key = parts[0] if len(parts) > 0 else None
                value = parts[1] if len(parts) > 1 else None
                handler(key, value)
            data = lines[-1]


@contextlib.contextmanager
def watch_progress(handler):
    with _tmpdir_scope() as tmpdir:
        filename = os.path.join(tmpdir, 'sock')
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        with contextlib.closing(sock):
            sock.bind(filename)
            sock.listen(1)
            child = gevent.spawn(_watch_progress, filename, sock, handler)
            try:
                yield filename
            except:
                gevent.kill(child)
                raise


duration = float(ffmpeg.probe('new_audio.wav')['format']['duration'])

prev_text = None

def handler(key, value):
    global prev_text
    if key == 'out_time_ms':
        text = '{:.02f}%'.format(float(value) / 10000. / duration)
        if text != prev_text:
            print(text)
            prev_text = text


with watch_progress(handler) as filename:
    p = subprocess.Popen(
        (ffmpeg
            .input('in.mp4')
            .output('out.mp4')
            .global_args('-progress', 'unix://{}'.format(filename))
            .overwrite_output()
            .compile()
        ),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out = p.communicate()

if p.returncode != 0:
    sys.stderr.write(out[1])
    sys.exit(1)

def progress_handler(progress_info):
    print('{:.2f}'.format(progress_info['percentage']))


def createSlideshow(
    images_path,
    music_path,
    frame_duration,
    frame_rate,
    image_resolution,
    transition_duration,
    transition_name,
    out_file,
):
    """
    Main function to create slideshow
    :param images_path Path: Path to directory of images to use
    :param music_path Path: Path to music file to use
    :param frame_duration int: Duration for each image to be displayed
    :param frame_rate int: Frame rate of final video (does not affect duration)
    :param image_resolution tuple(int,int): Width and height of final video
    :param transition_duration int: Duration for transition effect to last
    :param transition_name str: Name of the transition effect to use
    :param out_file Path: Path of file to output video
    """
    images_path = Path(images_path)
    music_path = Path(music_path)
    assert images_path.is_dir(), "Given path is not a directory"
    assert music_path.is_file(), "Given path is not a file"
    assert isinstance(frame_duration, int), "Frame duration must be an integer"
    assert isinstance(
        transition_duration, int
    ), "Transition duration must be an integer"

    frame_images = [str(i) for i in getImagesFromPath(images_path)]
    sorted_images = [str(i) for i in orderImages(frame_images)]
    vid_length = len(sorted_images) * frame_duration
    output_streams = []
    output_streams.append(
        applyTransitions(
            sorted_images,
            image_resolution,
            transition_name,
            frame_duration,
            transition_duration,
        )
    )
    if music_path:
        extension = music_path.suffix[1:]
        createSoundEffect(music_path, vid_length)
        output_streams.append(ffmpeg.input("new_audio.{ext}".format(ext=extension)))
    out = ffmpeg.output(
        *output_streams, out_file, t=vid_length, r=frame_rate
    ).overwrite_output().progress(progress_handler)

    # (ffmpeg
    # .input('in.mp4')
    # .output('out.mp4')
    # .progress(progress_handler)
    # .overwrite_output()
    # .run()
    # )


    spinner = Spinner()
    spinner.start("Creating slideshow... ")
    try:
        ffmpeg.run(out, quiet=True)
        spinner.stop("Done! Created slideshow at {}".format(out_file))
    except Exception as e:
        spinner.stop("Error: {}. Slideshow could not be created".format(e))

    if music_path:
        Path("new_audio.{ext}".format(ext=extension)).unlink()
