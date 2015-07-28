#!/usr/bin/env python
# Magnus Axelson-Fisk
# Bokskanner 2015

import os
import time
import serial

from imageCrop import imageCrop

userDir = os.path.expanduser("~")


arduinoCom = serial.Serial()


#if the connection is not established or fails, might add a reconnect
def failedConnection(pageID):
    print "Failed to connect to arduino on page ", pageID, ", try to restart by pulling out USB-cable"
    arduinoCom.close()
    



#establish connection to arduino
#returns true if arduino reset function is executed
def estabConnection():
    while True:
        try:    
            arduinoCom.baudrate = 9600
            arduinoCom.timeout = 10
            arduinoCom.port = '/dev/ttyACM0'
            break
        except portNotOpenError:
            arduinoCom.open()
    if arduinoCom.isOpen()!=True:
        arduinoCom.open()
    time.sleep(5)
    arduinoCom.write('9')
    inputStr = arduinoCom.readline()
    connected = bool(inputStr[:1])
    return connected

#function for croping and merges pages, deletes the cropped photos
def pageScanComplete(pagewidth, pageHeight, bookLength, bookTitle):
    
    cropDone = imageCrop(pageWidth, pageHeight, bookLength)
    if cropDone:
        os.system("convert *crop.jpg " + bookTitle + ".pdf")
        
    else:
        print "Failed to crop images"
    
    bookDir = os.path.expanduser("~") + "/" + bookTitle
    fileEnding = "crop.jpg"
    fileList = os.listdir(bookDir)
    for i in range(0, len(fileList)):
        if fileList[i].endswith(fileEnding):
            os.remove(bookDir + "/" + fileList[i])


while True:
    try:
        bookTitle = raw_input('Boktitel ')
        bookDir = userDir + "/" + bookTitle
        os.mkdir(bookDir)
        break
    except OSError:
        print "Mappen finns redan, byt namn"
bookLength = int(raw_input('Antal sidor som ska skannas '))
pageWidth = int(raw_input('Bredden pa sidorna '))
pageHeight = int(raw_input('Hojden pa sidorna '))
os.chdir(bookDir)



pageTurned = True
connected = False
connectTries = 1


#connects to arduino, if not successful on 5 tries breaks and calls end function
while connected != True:
    connected = estabConnection()
    if connectTries == 5:
        failedConnection(0)
        break
    connectTries = connectTries + 1


#takes picture of page and calls for arduino to turn page
for pageID in range (0, bookLength):
    if pageTurned == True:
        os.system("gphoto2 --capture-image-and-download")
        os.rename("capt0000.jpg", str(pageID) + ".jpg")
        arduinoCom.write('1')
        time.sleep(1)
        inputStr = arduinoCom.readline()
        pageTurned = bool(inputStr[:1])
        print pageID
        print pageTurned
    else:
        failedConnection(pageID)
        break




#when all pages has been turned call for function to crop and merge pages
if pageID==(bookLength-1):
    pageScanComplete(pageWidth,pageHeight,bookLength,bookTitle)

print "reset"
arduinoCom.write('9')
print arduinoCom.readline()
arduinoCom.close()
print arduinoCom.isOpen()





