#!/usr/bin/env python
# Magnus Axelson-Fisk
# Hopefully this will work later without pageWidth or pageHeigth
# but instead with imagemagick canny function
# Bokskanner 2015

import PythonMagick as PM


def imageCrop(pageWidth, pageHeight, bookLength):
    pixPerCm = 98.4 #update when measured 3888/picturelength
    pageID = 0
    
    pageWidthPix = pixPerCm*pageWidth*2
    pageHeightPix = pixPerCm*pageHeight
    
    cropXPixel = 1944-(pageWidth*pixPerCm)
    cropYPixel = 2592-pageHeightPix
    cropArea = "%sx%s+%s+%s" % (pageWidthPix, pageHeightPix, cropXPixel, cropYPixel)

    
    for pageID in range(0,bookLength):
        img = PM.Image(str(pageID) + ".jpg")
        img.rotate(180.0)
        img.crop(cropArea)
        img.write(str(pageID) + "crop.jpg")
    if pageID == (bookLength - 1):
        return True
    else:
        return False
    



