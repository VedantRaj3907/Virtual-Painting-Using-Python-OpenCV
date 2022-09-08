import cv2 as cv
from matplotlib.pyplot import draw
import numpy as np
import os
import HandTrackingModule as htm


######################################################################################
#Importing images

folderpath_brushes = "E:\Extra Codes\Python\Python Projects\Virtual Painting\Images_Project\Brushes"
folderpath_shapes = "E:\Extra Codes\Python\Python Projects\Virtual Painting\Images_Project\Shapes"
myList_brushes = os.listdir(folderpath_brushes)
myList_shapes = os.listdir(folderpath_shapes)
overlayList = []
List_s = []
for path in myList_brushes:         #Insertin All the Images of Brushers
    image = cv.imread(f'{folderpath_brushes}/{path}')
    overlayList.append(image)

for path in myList_shapes:          #Inserting All the Images of Shapes
    image = cv.imread(f'{folderpath_shapes}/{path}')
    List_s.append(image)
print(len(overlayList))
print(len(List_s))
pic = overlayList[0]
shape = List_s[0]
shape_name = ''
######################################################################################
#Setting Up Video
vid = cv.VideoCapture(0)
vid.set(3, 1920)
vid.set(4,1080)

######################################################################################
#detecting hands using HandDetector Module

detector = htm.HandDetector(detectionCon=0.85)

######################################################################################
#Giving brush and eraser sizes and colors also creating Canvas image to draw on it

drawColor = (0,0,0)
xp, yp = 0, 0
brushThickness = 15
eraserThickness = 100
imgCanvas = np.zeros((1080,1920,3),np.uint8)

######################################################################################
#starting of the Video Loop

while True:

    # 1. Importing an Image
    success, frame = vid.read()
    img = cv.resize(frame,(1920,1080),interpolation = cv.INTER_LINEAR)
    img = cv.flip(img, 1)

    # 2. Drawing Hand Landmarks

    img = detector.FindHands(img)
    lmlist = detector.FindPosition(img, draw=False)
    if(len(lmlist)!=0):

        #tip of index finger and middle finger and thumb finger and pinky finger

        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]
        xt, yt = lmlist[4][1:]
        xq, yq = lmlist[20][1:]
        size = int((((yt-y1) ** 2 ) + ((xt - x1) ** 2)) **  0.5)            #for ensuring the distance between thum and index finger for size
        print(x1,y1," ",x2,y2)
        fingers = detector.fingersup()  #getting all the fingers if they are open

    #3. Checking for index and middle fingers (SELECTION MODE)

        if fingers[1] and fingers[2]:   #checking for index and middle finger
            xp, yp = 0, 0
            if x1<191:                  #checking for selecting brush and changing image accordingly
                if 160<x1<190 and 0<y1<100:
                    pic = overlayList[3]
                    drawColor = (255,200,0) #SkyBlue
                elif 0<x1<100 and 0<y1<100:
                    pic = overlayList[2]    #White
                    drawColor = (255,255,255)
                elif 160<x1<190 and 200<y1<250:
                    pic = overlayList[5]
                    drawColor = (0,247,255) #Yellow
                elif 0<x1<100 and 200<y1<250:
                    pic = overlayList[4]
                    drawColor = (55,255,0)  #Green
                elif 160<x1<190 and 320<y1<380:
                    pic = overlayList[7]
                    drawColor = (255,0,255) #Pink
                elif 0<x1<100 and 320<y1<380:
                    pic = overlayList[6]
                    drawColor = (0,0,255)   #Red
                elif 160<x1<190 and 450<y1<510:
                    pic = overlayList[9]
                    drawColor = (255,68,180) #Purple   
                elif 0<x1<100 and 450<y1<510:
                    pic = overlayList[8]
                    drawColor = (0,100,255) #Orange
                elif 100<x1<190 and 610<y1<670:
                    pic = overlayList[1]
                    drawColor = (0,0,0)     #Eraser
            if 1349<x1<1540:              #checking for selecting Shape
                if 1400<x1<1500 and 50<y1<200:
                    shape = List_s[1]
                    shape_name = 'Circle'
                elif 1400<x1<1500 and 290<y1<370:
                    shape = List_s[2]
                    shape_name = 'Square'
                elif 1400<x1<1500 and 430<y1<530:
                    shape = List_s[3]
                    shape_name = 'Freestyle'
                elif 1400<x1<1500 and 560<y1<670:
                    shape = List_s[4]
                    shape_name = 'Triangle'
            cv.rectangle(img, (x1,y1-25), (x2,y2+25), drawColor, cv.FILLED)
                

    #4. Checking if not index and middle finger (DRAWING MODE)

        if fingers[1] and fingers[2] == False:
            flag = 0
            cv.circle(img, (x1,y1), 15, drawColor, cv.FILLED)  
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            
            if drawColor == (0,0,0):
                if fingers[1] and fingers[0]:                                      
                    eraserThickness = size                              #for Eraser (converting eraserthickness to particular size from index and thumb)
                cv.line(img, (xp,yp), (x1,y1), drawColor, eraserThickness)
                cv.line(imgCanvas, (xp,yp), (x1,y1), drawColor, eraserThickness)
            else:
                if shape_name == 'Freestyle':
                    cv.line(img, (xp,yp), (x1,y1), drawColor, brushThickness)       #for drawing lines using ur finger tips
                    cv.line(imgCanvas, (xp,yp), (x1,y1), drawColor, brushThickness)
                elif shape_name == 'Circle':                                        #for drawing circle 
                    cv.circle(img, (x1,y1), size, drawColor, 20)
                    if fingers[4] == 1:
                        cv.circle(imgCanvas, (x1,y1), size, drawColor, 15)
                elif shape_name == 'Square':                                        #for drawing Square
                    cv.rectangle(img, (xt,yt), (x1,y1), drawColor, 15)
                    if fingers[4] == 1:
                        cv.rectangle(imgCanvas, (xt,yt), (x1,y1), drawColor, 15)
                elif shape_name == 'Triangle':                                      #for drawing rectangle
                    cv.line(img, (xt,yt), (x1,y1), drawColor,brushThickness)
                    cv.line(img, (x1,y1) ,(xq,yq), drawColor, brushThickness)
                    cv.line(img, (xq,yq), (xt,yt), drawColor, brushThickness)
                    if fingers[4] == 1 and fingers[0]==1 and fingers[3]==1:
                        cv.line(imgCanvas, (xt,yt), (x1,y1), drawColor,brushThickness)
                        cv.line(imgCanvas, (x1,y1) ,(xq,yq), drawColor, brushThickness)
                        cv.line(imgCanvas, (xq,yq), (xt,yt), drawColor, brushThickness)
            xp, yp = x1, y1

    #5. Drawing on gray and thresold images to insert onto main video

    imgGray = cv.cvtColor(imgCanvas,cv.COLOR_BGR2GRAY)                      #converting to grayscale and finding inverse thresolds and giving bitwise and "and" or operations to draw
    _, imginv = cv.threshold(imgGray, 50, 255, cv.THRESH_BINARY_INV)
    imginv = cv.cvtColor(imginv, cv.COLOR_GRAY2BGR)
    img = cv.bitwise_and(img,imginv)
    img = cv.bitwise_or(img,imgCanvas)

    #6. Displaying images and Videos

    img[0:720,0:191] = pic
    img[0:720,1349:1540] = shape
    cv.imshow("Video", img)
    if(cv.waitKey(1)==ord('q')):
        break 

######################################################################################
