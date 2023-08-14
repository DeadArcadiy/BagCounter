import numpy as np
import cv2 as cv
from counter import Counter
from maskcreator import MaskCreator
from framewrapper import FrameWrapper


if __name__ == '__main__':
   #open video
   cap = cv.VideoCapture('example.mp4')
   #get video resolution
   frameWidth = cap.get(3)
   frameHight = cap.get(4)
   #you can enable recording
   recording = False
   #recording is tested on macos,may not work on other platforms
   if recording:
      out = cv.VideoWriter('output.mp4',cv.VideoWriter_fourcc('m', 'p', '4', 'v') , 20,(int(frameWidth), int(frameHight)))
   #location of lines that are tracking bags movement
   line_up = int(50*(frameHight/100))
   line_down = int(70*(frameHight/100))
   line_middle =int((line_up+line_down)/2)

   mCreator = MaskCreator()
   bagCounter = Counter(line_down,line_middle,line_up)
   wrapper = FrameWrapper(line_down,line_middle,line_up,frameWidth)

   framecounter = 0
   nBags = 0 

   while cap.isOpened():
      ret, frame = cap.read()
      framecounter+=1
      if framecounter == 10:
         if not ret:#check end of the video
            print("video ended")
            break
         #get mask and frame with outline
         mask, frame = mCreator(frame)
         #check collision of lines and boxes on a mask
         output_counted, already_counted = bagCounter(mask)
         #draw lines and information
         result = wrapper(frame,output_counted,already_counted)

         if recording:
            out.write(result)
         else:
            cv.imshow('frame', result)
            #Press ESC to exit
            k = cv.waitKey(1) & 0xff
            if k == 27:
               break

         nBags = output_counted

         #reset frame counter
         framecounter = 0

   cap.release()
   if recording:
      out.release()
   else:
      cv.destroyAllWindows()

   print(nBags)