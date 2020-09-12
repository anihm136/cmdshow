from pathlib import Path
def getImagesFromPath(imgPath):
    imgFormats = [".gif", ".tif", ".tiff", ".jpg", ".jpeg", ".bmp", ".png", ".eps"]
    directoryPath = Path(imgPath)
    return [f.resolve() for f in directoryPath.iterdir() if f.name[f.name.rfind("."):] in imgFormats]

def orderImages(imgPath, parameter):
    if parameter == 'sort':
        imgPath.sort(key = lambda x: x.name)
    else:
        pass
 


p = r"../img"
print(getImagesFromPath(p))
