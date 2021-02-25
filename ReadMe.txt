Game Play using Gestures:
Computer vision project implemented with OpenCV

Ever wanted to play games using Gestures just by waiving your hands in the air and controlling the game at your end.
The project is all about the same.
I have used the computer vision techniques of OpenCV to build this project.
I have used a blue color object in order to give instructions to the system and have adjusted the hsv values as per the color.
You can also adjust the hue-saturation values as per your object color.
It includes the further steps of morphological operations on the mask produced which are Erosion and Dilation.
Erosion reduces the impurities present in the mask and dilation further restores the eroded main mask.


Algorithm
1.Start reading the frames and convert the captured frames to HSV colour space.
2.Adjust the trackbar values for finding the mask of coloured marker.
3.Preprocess the mask with morphological operations.(Erotion and dilation)
4.Detect the contours, find the center coordinates of largest contour
5.Give the conditions for navigation around the control region.
6.All set to play any navigation based games using gestures.
