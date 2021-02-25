import numpy as np
import cv2
from pynput.keyboard import Key, Controller

keyboard = Controller()
flag= -1
x1,y1=260,200
x2,y2=x1+130,y1+130

#default called trackbar function
def setValues(x):
   print("")


# Creating the trackbars needed for adjusting the marker colour
cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180,setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255,setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255,setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180,setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255,setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 49, 255,setValues)


#The kernel to be used for dilation purpose
kernel = np.ones((5,5),np.uint8)

cap = cv2.VideoCapture(0)

# Keep looping
while True:
    # Reading the frame from the camera
    ret, frame = cap.read()
    #Flipping the frame to see same side of yours
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
    u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
    u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
    l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
    l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
    l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
    Upper_hsv = np.array([u_hue,u_saturation,u_value])
    Lower_hsv = np.array([l_hue,l_saturation,l_value])

    #Creating control region
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)

    # Identifying the pointer by making its mask
    Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

    # Find contours for the pointer after idetifying it
    cnts,_ = cv2.findContours(Mask, cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    center = None

    # If the contours are formed
    if len(cnts) > 0:
    	# sorting the contours to find biggest
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        # Get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        # Draw the circle around the contour
        cv2.circle(frame, (int(x), int(y)), 0, (0, 255, 255), 5)
        # Calculating the center of the detected contour
        M = cv2.moments(cnt)
        center = [int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])]

        if center[0]>x1 and center[0]<x2 and center[1]>y1 and center[1]<y2:
            flag = 0

        if flag == 0:
            if center[0] > x2:
                keyboard.press(Key.right)
                keyboard.release(Key.right)
                print("Right")
                flag = 1

            if center[0] < x1:
                keyboard.press(Key.left)
                keyboard.release(Key.left)
                print("Left")
                flag = 1

            if center[1] < y1:
                keyboard.press(Key.up)
                keyboard.release(Key.up)
                print("Up")
                flag = 1

            if center[1] > y2:
                keyboard.press(Key.down)
                keyboard.release(Key.down)
                print("Down")
                flag = 1



    else:
        pass


    # Show all the windows
    cv2.imshow("Tracking", frame)
    cv2.imshow("mask",Mask)

	# If the 'q' key is pressed then stop the application
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and all resources
cap.release()
cv2.destroyAllWindows()