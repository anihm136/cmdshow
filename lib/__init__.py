from pathlib import Path
import gevent.monkey
from sys import platform
from .sounds import createSoundEffect
from .transitions import applyTransitions
from .utils import Spinner, getImagesFromPath, orderImages

gevent.monkey.patch_all()
import contextlib
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import ffmpeg
import gevent


@contextlib.contextmanager
def _tmpdir_scope():
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


def _watch_progress(filename, sock, handler):
    connection, client_address = sock.accept()
    data = ""
    with contextlib.closing(connection):
        while True:
            more_data = connection.recv(16)
            if not more_data:
                break
            data += more_data.decode("utf8")
            lines = data.split("\n")
            for line in lines[:-1]:
                parts = line.split("=")
                key = parts[0] if len(parts) > 0 else None
                value = parts[1] if len(parts) > 1 else None
                handler(key, value)
            data = lines[-1]


@contextlib.contextmanager
def watch_progress(handler):
    with _tmpdir_scope() as tmpdir:
        filename = os.path.join(tmpdir, "sock")
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


duration = 0
prev_text = None


def handler(key, value):
    global prev_text
    if key == "out_time_ms":
        text = "{:4.02f}%".format(float(value) / 10000.0 / duration)
        if text != prev_text:
            print("\b \b" * 100, end="")
            print(text, end="", flush=True)
            prev_text = text


def progress_handler(progress_info):
    print("{:.2f}".format(progress_info["percentage"]))


def createSlideshow(
    sorted_images,
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
    :param sorted_images: Final list of images to be used for the video
    :param music_path Path: Path to music file to use
    :param frame_duration int: Duration for each image to be displayed
    :param frame_rate int: Frame rate of final video (does not affect duration)
    :param image_resolution tuple(int,int): Width and height of final video
    :param transition_duration int: Duration for transition effect to last
    :param transition_name str: Name of the transition effect to use
    :param out_file Path: Path of file to output video
    """
    music_path = Path(music_path)
    assert music_path.is_file(), "Given path is not a file"
    assert isinstance(frame_duration, int), "Frame duration must be an integer"
    assert isinstance(
        transition_duration, int
    ), "Transition duration must be an integer"

    vid_length = len(sorted_images) * frame_duration
    global duration
    duration = vid_length
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

    if platform == "linux" or platform == "linux2":
        with watch_progress(handler) as filename:
            out = (
                ffmpeg.output(*output_streams, out_file, t=vid_length, r=frame_rate)
                .global_args("-progress", "unix://{}".format(filename))
                .overwrite_output()
                .compile()
            )
            p = subprocess.Popen(
                out,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            output = p.communicate()

        with open("log.txt", "w") as log:
            log.write(output[0].decode("utf8"))

        if music_path:
            Path("new_audio.{ext}".format(ext=extension)).unlink()

        if p.returncode != 0:
            with open("errorlog.txt", "w") as errorlog:
                errorlog.write(output[1].decode("utf8"))
            sys.stderr.write("An error occurred. Please check errorlog.txt for details")
            sys.exit(1)

        # spinner = Spinner()
        # spinner.start("Creating slideshow... ")
        # try:
        #     ffmpeg.run(out, quiet=True)
        #     spinner.stop("Done! Created slideshow at {}".format(out_file))
        # except Exception as e:
        #     spinner.stop("Error: {}. Slideshow could not be created".format(e))

    elif platform == "win32":
        out = ffmpeg.output(
            *output_streams, out_file, t=vid_length, r=frame_rate
        ).overwrite_output()
        ffmpeg.run(out)
        if music_path:
            Path("new_audio.{ext}".format(ext=extension)).unlink()
