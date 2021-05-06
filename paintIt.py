# A virtual painting program
# just hold markers of Red Blue Green and become an artist
import cv2 
import numpy as np

frameWidth = 640
frameheight = 480 

cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameheight)
cap.set(10,120)


def color_picker():


    def empty(a):
        pass

    cv2.namedWindow("HSV")
    cv2.resizeWindow("HSV",640,240)
    cv2.createTrackbar("HUE Min","HSV",0,179,empty)
    cv2.createTrackbar("SAT Min","HSV",0,255,empty)
    cv2.createTrackbar("VALUE Min","HSV",0,255,empty)
    cv2.createTrackbar("HUE Max","HSV",179,179,empty)
    cv2.createTrackbar("SAT Max","HSV",255,255,empty)
    cv2.createTrackbar("VALUE Max","HSV",255,255,empty)

    while True:

        _, img = cap.read()
        imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

        h_min = cv2.getTrackbarPos("HUE Min","HSV")
        h_max = cv2.getTrackbarPos("HUE Max", "HSV")
        s_min = cv2.getTrackbarPos("SAT Min", "HSV")
        s_max = cv2.getTrackbarPos("SAT Max", "HSV")
        v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
        v_max = cv2.getTrackbarPos("VALUE Max", "HSV")
        print(h_min)

        lower = np.array([h_min,s_min,v_min])
        upper = np.array([h_max,s_max,v_max])
        mask = cv2.inRange(imgHsv,lower,upper)
        result = cv2.bitwise_and(img,img, mask = mask)

        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        hStack = np.hstack([img,mask,result])
        #cv2.imshow('Original', img)
        #cv2.imshow('HSV Color Space', imgHsv)
        #cv2.imshow('Mask', mask)
       #cv2.imshow('Result', result)
        cv2.imshow('Horizontal Stacking', hStack)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



# R G B
myColors = [[123,116,0,179,255,255],
            [40,97,188,82,255,255],
            [102,92,0,130,255,255]]

# BGR

myColorValues = [[0,0,255],
                 [0,255,0],
                 [255,0,0]]

# [x,y,colorID]
myPoints = []

def findColor(img,myColors,myColorValues) : 
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors :
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
        # cv2.imshow(str(color[0]),mask)
    return newPoints

# color_picker()


def getContours(img):

    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours : 
        area = cv2.contourArea(cnt)
        if area > 500 : 
            # cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
            peri = cv2.arcLength(cnt,True)

            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h = cv2.boundingRect(approx)

            # tip of the marker not centre
    return x + w//2,y


def drawIt(myPoints,myColorValues):
    for point in myPoints : 
        cv2.circle(imgResult,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)




while True : 
    ret,img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img,myColors,myColorValues)

    if len(newPoints)!=0:
        for newP in newPoints : 
            myPoints.append(newP)

    if len(myPoints)!=0:
        drawIt(myPoints,myColorValues)

    cv2.imshow("Frame",imgResult)
    
    if cv2.waitKey(1)&0xFF == ord('q'):
        break
