import cv2
import numpy as np
import pickle
import cvzone

width,height=107,48

cap=cv2.VideoCapture('carPark.mp4')

with open('carParkPos.P', 'rb') as f:
    posList = pickle.load(f)

def checkPosSpace(imgProc):
    spaceCounter=0
    for pos in posList:
        x,y=pos
        imgCrop=imgProc[y:y+height,x:x+width]
        #cv2.imshow(str(x*y),imgCrop)
        count = cv2.countNonZero(imgCrop)

        if count<1000:
            color=(0,255,0)
            thickness=5
            spaceCounter += 1
        else:
            color=(0,0,255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)
    cvzone.putTextRect(img, "Free "+str(spaceCounter)+"/"+str(len(posList)), (100,50), scale=3,
                       thickness=2, offset=20, colorR=(0, 200, 0))


while True:

    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)



    checkPosSpace(imgDilate)




    cv2.imshow('image',img)
    #cv2.imshow('imageThree',imgDilate)

    cv2.waitKey(10)
