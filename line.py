import cv2
import numpy as np 
import math

class LineTracer:
    thresh = 50
    maxValue =255
    horizontalRes = 32
    verticalRes = 24

    def __init__(self,filename, turn_precision):
        self.filename = filename
        self.turn_res = turn_precision

    def getTurnDir():
        line_xval = self.__findLine()
        if(line_xval >= 0.0): #Line detected, proceed calculate turn signal
            divisor = float(self.horizontalRes)/ self.turn_res;
            return int(math.floor(
                (line_xval / divisor) + 0.5))
        else: #No line detected so return landing signal
            return self.turn_res+1;

    
    def __findLine():
        org_img = cv2.imread(self.filename,cv2.IMREAD_COLOR)
        
        #Convert to Grayscale
        img = cv2.cvtColor(org_img, cv2.COLOR_BGR2GRAY)

        #Do Thresholding
        h,img = cv2.threshold(img, self.thresh, self.maxValue, cv2.THRESH_BINARY_INV)

        #Blur to reduce noise
        img = cv2.medianBlur(img,17)

        #Make image smaller
        img = cv2.resize(img, (self.horizontalRes, self.verticalRes))
        #org_img = cv2.resize(org_img, (self.horizontalRes, self.verticalRes))

        #Create skeleton
        size = np.size(img)
        skel = np.zeros(img.shape,np.uint8)
        element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
        done = False
        while( not done):
            eroded = cv2.erode(img,element)
            temp = cv2.dilate(eroded,element)
            temp = cv2.subtract(img,temp)
            skel = cv2.bitwise_or(skel,temp)
            img = eroded.copy()
            zeros = size - cv2.countNonZero(img)
            if zeros==size:
                done = True

        #Do Line Detection
        minLineLength = 100
        maxLineGap = 0
        lines = cv2.HoughLinesP(skel,1,np.pi/180,10,minLineLength,maxLineGap)


        #get minimum and maximum x-coordinate from lines
        x_min = self.horizontalRes+1.0
        x_max = -1.0;
        for x1,y1,x2,y2 in lines[0]:
            x_min = min(x_min, x1, x2)
            x_max = max(x_max, x1, x2)
            #cv2.line(org_img,(x1,y1),(x2,y2),(0,255,0),2)

        #write output visualization
        #cv2.imwrite("output-img.png",org_img);

        #find the middle point x of the line and return
        #return -1.0 if no lines found
        if(x_max == -1.0 | x_min == (self.horizontalRes+1.0) ):
            return -1.0 #no line found
        else:
            return (x_min + x_max) / 2.0
        
