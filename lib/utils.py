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

'''
def resizeToMean(images):
    num_images = len(images)
    mean_width, mean_height = 0, 0

    for f in images:
        img = Image.open(f)
        width, height = img.size
        mean_width+= width
        mean_height+= height
    
    mean_width= int(mean_width/num_images)
    mean_height= int(mean_height/num_images)

    for f in images:
        img = Image.open(f)
        imResize = img.resize((mean_width, mean_height), Image.ANTIALIAS)  
        imResize.save(f, 'JPEG', quality = 100) 

def resizeToMax(images):
    max_width = float("-inf")
    max_height = float("-inf")
    for f in images:
        img = Image.open(f)
        width, height = img.size
        if width > max_width and height > max_height:
            max_width = width
            max_height = height

    for f in images:
        img = Image.open(f)
        imResize = img.resize((max_width, max_height), Image.ANTIALIAS)  
        imResize.save(f, 'JPEG', quality = 100) 

def resizeToMin(images):
    min_width = float("inf")
    min_height = float("inf")
    for f in images:
        img = Image.open(f)
        width, height = img.size
        if width < min_width and height < min_height:
            min_width = width
            min_height = height

    for f in images:
        img = Image.open(f)
        imResize = img.resize((min_width, min_height), Image.ANTIALIAS)  
        imResize.save(f, 'JPEG', quality = 100) 


def resizeImages(imgPath, mode='mean'):
    images = getImagesFromPath(imgPath)

    tmpPath = createDirectory(imgPath, "tmp-mean")
    copyImagesToDirectory(images, tmpPath)

    tmpImages = getImagesFromPath(tmpPath)
    resizeToMean(tmpImages)

    tmpPath = createDirectory(imgPath, "tmp-max")
    copyImagesToDirectory(images, tmpPath)

    tmpImages = getImagesFromPath(tmpPath)
    resizeToMax(tmpImages)

    tmpPath = createDirectory(imgPath, "tmp-min")
    copyImagesToDirectory(images, tmpPath)

    tmpImages = getImagesFromPath(tmpPath)
    resizeToMin(tmpImages)


p = r"../img"
resizeImages(p)
'''