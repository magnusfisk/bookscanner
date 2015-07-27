#!/usr/bin/env python
# Magnus Axelson-Fisk
# Sends pageturntime over serial port
# This feature has not worked on aurduino before
# Bokskanner 2015

import os
import time
import serial
#import picamera

arduinoCom = serial.Serial()
#camera = picamera.PiCamera()
#camera.resolution = (2592,1944)

#if the connection is not established or fails, might add a reconnect
def failedConnection(pageID):
    print "Failed to connect to arduino on page ", pageID, ", try to restart by pulling out USB-cable"
    arduinoCom.close()
    

#Gives the arduino pageturntime and holdtime variables
#returns true if arduino has received and set variables
def pushVariables (pageTurnTime,pageHoldTime):
    arduinoCom.write('9')
    arduinoCom.flushInput()
    arduinoCom.write(pageTurnTime)
    time.sleep(0.5)
    arduinoCom.write(pageHoldTime)

    inputStr = arduinoCom.readline()
    print inputStr
    variableSet = bool(inputStr[:1])
    return variableSet

#establish connection to arduino and makes sure pageturntime and holdtime ar set as 0
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

#def checkForUSBDevice(name):
#        usbAdress = ""
#        context = pyudev.Context()
#        for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
#                if device.get('ID_FS_LABEL') == name:
#                        res = device.device_node
#        return res
while True:
    try:
        bookTitle = raw_input('Boktitel ')
        bookDir = "/home/magnus/Dokument/Skanner/" + bookTitle
        os.mkdir(bookDir)
        break
    except OSError:
        print "Mappen finns redan, byt namn"
bookLength = int(raw_input('Antal sidor som ska skannas '))
pageLength = int(raw_input('Bredden pa sidorna '))
pageHeight = int(raw_input('Hojden pa sidorna '))
os.chdir(bookDir)

#ekvation for pageTurnTime och pageHoldTime
#pageTurnLength = bookLength - defaultLength
#turnRev = pageTurnLength/(diameter*math.pi)
#pageTurnTime = int(turnRev*turnPeriod)
pageTurnTime = "'1500'"
pageHoldTime = "'600'"
variableSet = False
pageTurned = True
connected = False
i = 0





while connected != True:
    connected = estabConnection()

variableSet = pushVariables(pageTurnTime, pageHoldTime)

if variableSet != True:
	while variableSet != True:
            variableSet = pushVariables(pageTurnTime, pageHoldTime)
            if i == 10:
                failedConnection(0)
                break
            i = i + 1
        

else:
	for pageID in range (0, bookLength):
		if pageTurned == True:
            os.system("gphoto2 --capture-image-and-download")
            os.rename("capt0000.jpg", pageID + ".jpg")
            
			arduinoCom.write('1')
			time.sleep(1)
			inputStr = arduinoCom.readline()
			pageTurned = bool(inputStr[:1])
			print pageID 
			print pageTurned
		else:
			failedConnection(pageID)
			break
		




#if pageID==bookLength:
	#merge to pdf
print "reset"
arduinoCom.write('9')
print arduinoCom.readline()
arduinoCom.close()
print arduinoCom.isOpen()





