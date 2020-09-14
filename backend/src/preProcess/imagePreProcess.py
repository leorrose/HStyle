import os
import numpy as np
import cv2 as cv
from PIL import Image
import matplotlib.pyplot as plt



def convertTifToJpg(filePath):
    # get all tiff files with blob
    tiffFiles = []

    for file in os.listdir(filePath):
        if file.endswith(".tif"):
            tiffFiles.append(filePath + '\\' + file)

    # convert to png
    for tiffPath in tiffFiles:
        name, _ = os.path.splitext(tiffPath)
        im = Image.open(tiffPath)
        im.thumbnail(im.size)
        im.save(name + '.jpg', "JPEG", quality=100)

def rotateImage(imgPath, angel):
    Image.open(imgPath).rotate(angel).save(imgPath)

def rotateJpgImages(filePath):
    for file in os.listdir(filePath):
        if file.endswith(".jpg"):
            rotateImage(filePath + '\\' + file, 180)

def cropImage(imgPath):
    im = Image.open(imgPath)
    left = 300
    top = 1900
    right = 4400
    bottom = 5000
    im.crop((left, top, right, bottom)).save(imgPath)

def cropJpgImages(filePath):
    for file in os.listdir(filePath):
        if file.endswith(".jpg"):
            cropImage(filePath + '\\' + file)

def removeYellowLine(filePath):
    for file in os.listdir(filePath):
        if file.endswith(".jpg"):
            # Load the aerial image and convert to HSV colourspace
            image = cv.imread(filePath + '\\' + file)
            hsv=cv.cvtColor(image, cv.COLOR_BGR2HSV)
            lowerLimit = np.array([21, 39, 64])
            upperLimit = np.array([40, 255, 255])
            mask = cv.inRange(hsv, lowerLimit, upperLimit)
            image[mask>0]=(255,255,255)
            cv.imwrite(filePath + '\\' + file, image)

if __name__ == '__main__':
    convertTifToJpg("E:\\My stuff\\FinalProject\\src\\preProcess")
    rotateJpgImages("E:\\My stuff\\FinalProject\\src\\preProcess")
    cropJpgImages("E:/My stuff/FinalProject/src/preProcess")
    removeYellowLine("E:/My stuff/FinalProject/src/preProcess")