import cv2
import numpy as np 

org_img = cv2.imread('input-img.png',cv2.IMREAD_COLOR)
#org = cv2.imread('thresh.png',cv2.CV_LOAD_IMAGE_COLOR)

#Convert to Grayscale
img = cv2.cvtColor(org_img, cv2.COLOR_BGR2GRAY)

#Do Thresholding
thresh = 50
maxValue = 255
th,img = cv2.threshold(img, thresh, maxValue, cv2.THRESH_BINARY_INV)

#Blur to reduce noise
img = cv2.medianBlur(img,17)

#Make image smaller
img = cv2.resize(img,(0,0), fx=0.1, fy=0.1)
org_img = cv2.resize(org_img,(0,0), fx=0.1, fy=0.1)

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

#debug print lines
print lines[0]
for x1,y1,x2,y2 in lines[0]:
        cv2.line(org_img,(x1,y1),(x2,y2),(0,255,0),2)


#write output visualization
cv2.imwrite("output-img.png",org_img);

#Show results
cv2.imshow("skel",skel)
cv2.imshow("img",org_img);

cv2.waitKey(0)
cv2.destroyAllWindows()
