import numpy as np
import cv2 as cv

class FrameWrapper:
    def __init__(self,line_down,line_middle,line_up,frameWidth) -> None:
        #using hight of lines position and width of frame to create point to plot lines on a screen 
        self.line_down = np.array([[0, line_down],[frameWidth, line_down]], np.int32)
        self.line_down = self.line_down.reshape((-1,1,2))
        self.line_up = np.array([[0, line_up],[frameWidth, line_up]], np.int32)
        self.line_up = self.line_up.reshape((-1,1,2))
        self.line_middle= np.array([[0, line_middle],[frameWidth, line_middle]], np.int32)
        self.line_middle = self.line_middle.reshape((-1,1,2))


    def __call__(self, frame, output_counted,already_counted):
        #plot lines to make solution easier to understand
        cv.polylines(frame,[self.line_down],False,[255,0,0],thickness=2)
        cv.polylines(frame,[self.line_up],False,[0,0,255],thickness=2)
        cv.polylines(frame,[self.line_middle],False,[255,255,255],thickness=2)
        #add info on a frame
        str_on_frame = "Total Counting = %d, Already Counted = %d" % (output_counted,already_counted)
        cv.putText(frame, str_on_frame, (5,60), cv.FONT_HERSHEY_SIMPLEX ,2, (0,0,255), 2, cv.LINE_AA)

        return frame