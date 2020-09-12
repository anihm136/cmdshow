from glob import glob  # Testing only
from pprint import pp  # Testing only
from pathlib import Path

import ffmpeg
from sounds import createSoundEffect
from utils import getImagesFromPath, orderImages
from transitions import applyTransitions


def createSlideshow(images_path, frame_duration, transition_duration):
    images_path = Path(images_path)
    assert images_path.is_dir(), "Given path is not a directory"
    assert isinstance(frame_duration, int), "Frame duration must be an integer"
    assert isinstance(
        transition_duration, int
    ), "Transition duration must be an integer"
    FRAMERATE = 5
    frame_images = getImagesFromPath(images_path)
    sorted_images = orderImages(frame_images)
    vid_length = len(sorted_images) * frame_duration
    im_stream = applyTransitions(sorted_images, crossFade, frame_duration, transition_duration)
    createSoundEffect("audio.wav", vid_length)
    audio_strem = ffmpeg.input("new_audio.wav")
    out = ffmpeg.output(im_stream, audio_strem, "sorted_images.mp4", t=vid_length, r=FRAMERATE).overwrite_output()
    # out = ffmpeg.output(concat_images, audio_strem, "with_audio.avi").overwrite_output()
    pp(ffmpeg.compile(out))
    # print(" ".join(ffmpeg.compile(out)))
    ffmpeg.run(out)

createSlideshow("../img", 5, 1)
