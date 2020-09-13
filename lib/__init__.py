from pathlib import Path

import ffmpeg

from .sounds import createSoundEffect
from .transitions import applyTransitions
from .utils import Spinner, getImagesFromPath, orderImages


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

    frame_images = getImagesFromPath(images_path)
    sorted_images = orderImages(frame_images)
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
    ).overwrite_output()

    spinner = Spinner()
    spinner.start("Creating slideshow... ")
    ffmpeg.run_async(out, quiet=True).communicate()
    spinner.stop("Done! Created slideshow at {}".format(out_file))

    if music_path:
        Path("new_audio.{ext}".format(ext=extension)).unlink()
