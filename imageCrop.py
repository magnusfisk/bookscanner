#!/usr/bin/env python
# Magnus Axelson-Fisk
# Bokskanner 2015

import PythonMagick as PM

def imageCrop(pageWidth, pageHeight, bookLength):
    pixPerCm = 14
    pageID = 0
    
    pageWidthPix = pixPerCm*pageWidth*2
    pageHeigthPix = pixPerCm*pageHeigth
    
    cropXPixel = 1944-(pageWidth*pixPerCm)
    cropArea = "%sx%s+%s+%s" % (pageWidthPix, pageHeigthPix, cropXPixel, pageHeigthPix)

    
    for pageID in range(0,bookLength):
        img = PM.Image(str(pageID + ".jpg")
        img.rotate(180)
        img.crop(cropArea)
        img.write(pageID + "crop.jpg")


    
