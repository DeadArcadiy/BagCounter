import numpy as np
import cv2 as cv

class MaskCreator:
    def __init__(self) -> None:
        self.kernel = np.ones((3,3),np.uint8)


    def __call__(self, frame):
        #replace bags with green boxes
        mask = self.preprocess(frame)
        cnts = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        #find all objects and using shape find bags
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        mask = np.zeros(frame.shape)#create black mask
        for c in cnts:
            x,y,w,h = cv.boundingRect(c)
            if w > 200 and h < 300 and h > 100 and w > h:
                cv.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 10) #add green outline to original frame
                cv.rectangle(mask, (x, y), (x + w, y + h), (0,255,0), -1) # create green squares on the black mask
        return mask,frame


    def preprocess(self,frame):
        #make image very blurry and use adaptive thresholding to make bags finding easier 
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray,(5,5),0)
        r,thresh = cv.threshold(blur,0,255,cv.THRESH_TOZERO+cv.THRESH_OTSU)
        opening = cv.morphologyEx(thresh,cv.MORPH_OPEN,self.kernel, iterations = 30)
        mask = cv.inRange(opening, 140, 255)
        return mask

