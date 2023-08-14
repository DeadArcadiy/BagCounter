# BagCounter
This program can count bags on conveyor using opencv and numpy.

# The idea behind the solution
Read every tenth frame in video.
Use adaptive thresholding and blurring to create a mask.
Using mask we can easily find bags and replace them with a green box.
Using special adjustable lines we can track position and movement of green boxes and count them.
