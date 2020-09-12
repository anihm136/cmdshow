from pathlib import Path

import ffmpeg

from .sounds import createSoundEffect
from .transitions import applyTransitions
from .utils import getImagesFromPath, orderImages


def createSlideshow(
    images_path,
    music_path,
    frame_duration,
    frame_rate,
    image_resolution,
    transition_duration,
    transition_name
):
    images_path = Path(images_path)
    assert images_path.is_dir(), "Given path is not a directory"
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
        createSoundEffect(music_path, vid_length)
        output_streams.append(ffmpeg.input("new_audio.wav"))
    out = ffmpeg.output(
        *output_streams, "sorted_images.mp4", t=vid_length, r=frame_rate
    ).overwrite_output()
    ffmpeg.run(out)
