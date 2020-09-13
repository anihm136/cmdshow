import itertools
import shutil
import sys
import threading
import time
from pathlib import Path

import imagehash
import numpy as np
from PIL import Image


def getImagesFromPath(imgPath):
    """
    Get all image files from given path

    :param imgPath Path: Path to directory of images
    """
    imgFormats = [".gif", ".tif", ".tiff", ".jpg", ".jpeg", ".bmp", ".png", ".eps"]
    directoryPath = Path(imgPath)
    return [f.resolve() for f in directoryPath.iterdir() if f.suffix in imgFormats]


def orderImages(images, parameter="sim"):
    """
    Order images based on given parameter

    :param images list(Path): List of paths to images
    :param parameter str: Name of the ordering method to use. 'name' sorts alphabetically by name, 'sim' uses an image similarity measure to keep dissimilar images together (to avoid monotony)
    """
    if parameter == "name":
        sorted_images = np.asarray(sorted(images, key=lambda x: x.stem))
    elif parameter == "sim":
        hashes = [imagehash.average_hash(Image.open(path)) for path in images]
        num_images = len(images)
        similarity = np.zeros((num_images, num_images))
        for i in range(num_images):
            for j in range(num_images):
                similarity[i, j] = hashes[i] - hashes[j]

        covered = list()
        last = np.random.randint(num_images)
        covered.append(last)
        count = 1
        while count < num_images:
            mostDifferent = covered[-1]
            while mostDifferent in covered and np.max(similarity[last]) != -1:
                mostDifferent = np.argmax(similarity[last])
                similarity[last, mostDifferent] = -1
            covered.append(mostDifferent)
            last = mostDifferent
            count += 1
        covered = np.asarray(covered)
        sorted_images = np.asarray(images)[covered]
    else:
        sorted_images = np.asarray(images)
    return sorted_images


class Spinner:
    spinner_cycle = itertools.cycle(["⢄", "⢂", "⢁", "⡁", "⡈", "⡐", "⡠"])

    def __init__(self):
        self.stop_running = threading.Event()
        self.spin_thread = threading.Thread(target=self.init_spin)

    def start(self, message=""):
        print(message, end=" ")
        self.spin_thread.start()

    def stop(self, message=""):
        self.stop_running.set()
        self.spin_thread.join()
        print(message)

    def init_spin(self):
        while not self.stop_running.is_set():
            sys.stdout.write(next(self.spinner_cycle))
            sys.stdout.flush()
            time.sleep(0.05)
            sys.stdout.write("\b")
