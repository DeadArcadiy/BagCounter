import numpy as np

class Counter:
    def __init__(self,line_down,line_middle,line_up) -> None:
        #save position of lines and create useful vars for future
        self.line_down = line_down
        self.line_middle = line_middle
        self.line_up = line_up
        self.output_counted = 0
        self.already_counted = 0
        self.counted = False
        self.backward = False


    def __call__(self, mask) -> (int,int):
        #if bag cross red/blue and white line we wait until the white line is empty
        if self.counted:
            if not np.any(mask[self.line_middle],where=[0,255,0]):
               self.counted = False
            #if bag is going backwards and do not leave the area between red and blue lines we can track it and count
            elif self.backward:
               if np.any(mask[self.line_down],where=[0,255,0]) and np.any(mask[self.line_up],where=[0,255,0]):
                  self.already_counted -= 1
                  self.backward = False

        #if bag is crossing blue and white line we add one to output or subtract one from already counted
        elif np.any(mask[self.line_down],where=[0,255,0]) and np.any(mask[self.line_middle],where=[0,255,0]):
            if self.already_counted > 0:
               self.already_counted -= 1
            else:
               self.output_counted += 1
            self.counted = True
                    
        #if bag is crossing red and white line it is going backwards so we turn on backwards mode
        # and counting already counted bags just to substact it in future
        elif np.any(mask[self.line_up],where=[0,255,0]) and np.any(mask[self.line_middle],where=[0,255,0]):
            self.already_counted += 1
            self.backward = True
            self.counted = True

        return self.output_counted,self.already_counted