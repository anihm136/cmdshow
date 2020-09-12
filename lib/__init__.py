from glob import glob  # Testing only
from pathlib import Path

import cv2 as cv

from utils import getImagesFromPath


def createSlideshow(images_path, frame_duration, transition_duration):
    images_path = Path(images_path)
    assert images_path.is_dir(), "Given path is not a directory"
    # assert isinstance(frame_duration, int), "Frame duration must be an integer"
    # assert isinstance(transition_duration, int), "Transition duration must be an integer"
    # sorted_images = sortedImages(images_path)
    # images, transition_frames = applyTransition(sorted_images)
    FRAMERATE = 5
    fourcc = cv.VideoWriter_fourcc(*"DIVX")
    frame_array = []
    size = 0
    frame_images = getImagesFromPath(images_path)
    for file in frame_images:
        frame = cv.imread(file.as_posix())
        height, width, _ = frame.shape
        if not size or (width, height) == size:
            frame_array.append(frame)
            size = (width, height)

    out = cv.VideoWriter("output.avi", fourcc, FRAMERATE, size)
    num_writes = frame_duration * FRAMERATE
    for i in frame_array:
        for _ in range(num_writes):
            out.write(i)
    # Release everything if job is finished
    out.release()

createSlideshow("../img", 5, 1)
