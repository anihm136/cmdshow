from glob import glob  # Testing only
from pprint import pp  # Testing only
from pathlib import Path

import ffmpeg
from sounds import createSoundEffect
from utils import getImagesFromPath


def createSlideshow(images_path, frame_duration, transition_duration):
    images_path = Path(images_path)
    assert images_path.is_dir(), "Given path is not a directory"
    # assert isinstance(frame_duration, int), "Frame duration must be an integer"
    # assert isinstance(
    #     transition_duration, int
    # ), "Transition duration must be an integer"
    # sorted_images = sortedImages(images_path)
    # images, transition_frames = applyTransition(sorted_images)
    FRAMERATE = 5
    frame_images = getImagesFromPath(images_path)
    vid_length = len(frame_images) * frame_duration
    im_streams = []
    for file in frame_images[1:]:
        im_streams.append(ffmpeg.input(file.as_posix(), t=frame_duration, loop=1))
    createSoundEffect("audio.wav", vid_length)
    for i in range(len(im_streams)):
        im_streams[i] = (
            im_streams[i]
            .filter(
                "scale", width=1280, height=720, force_original_aspect_ratio="decrease"
            )
            .filter("pad", width=1280, height=720, x="(ow-iw)/2", y="(oh-ih)/2")
            .filter("setsar", 1)
        )
    concat_images = ffmpeg.concat(*im_streams, v=1, a=0)
    audio_strem = ffmpeg.input("new_audio.wav")
    out = ffmpeg.output(concat_images, audio_strem, "with_audio_2.mp4", t=vid_length, r=FRAMERATE).overwrite_output()
    # out = ffmpeg.output(concat_images, audio_strem, "with_audio.avi").overwrite_output()
    pp(ffmpeg.compile(out))
    # print(" ".join(ffmpeg.compile(out)))
    ffmpeg.run(out)

createSlideshow("../img", 5, 1)
