import cv2
from PIL import Image
from pathlib import Path
import shutil


def getImagesFromPath(imgPath):
    imgFormats = [".gif", ".tif", ".tiff",
                  ".jpg", ".jpeg", ".bmp", ".png", ".eps"]
    directoryPath = Path(imgPath)
    return [f.resolve() for f in directoryPath.iterdir() if f.suffix in imgFormats]


def orderImages(images, parameter='name'):
    if parameter == 'name':
        images.sort(key=lambda x: x.name)
    else:
        pass


def createDirectory(parent, child):
    directoryPath = Path(parent)
    tempPath = directoryPath / f"{child}"
    try:
        tempPath.mkdir(parents=True)
    except FileExistsError:
        for f in tempPath.iterdir():
            f.unlink()
    return tempPath


def copyImagesToDirectory(images, ToPath):
    for img in images:
        shutil.copy(img, ToPath)


def resizeImages(imgPath, mode='mean'):
    images = getImagesFromPath(imgPath)
    tmpPath = createDirectory(imgPath, "tmp")
    copyImagesToDirectory(images, tmpPath)

    tmpImages = getImagesFromPath(tmpPath)
    num_images = len(tmpImages)
    mean_width, mean_height = 0, 0

    for f in tmpImages:
        img = Image.open(f)
        width, height = img.size
        mean_width+= width
        mean_height+= height
    
    mean_width/= num_images
    mean_height/= num_images

    for f in tmpImages:
        img = Image.open(f)
        imResize = img.resize((mean_width, mean_height), Image.ANTIALIAS)  
        imResize.save(f, 'JPEG', quality = 100) # setting quality 
        # printing each resized image name 
        print(img.filename.split('\\')[-1], " is resized")

p = r"../img"
resizeImages(p)
