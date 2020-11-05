# -*- coding: utf-8 -*-
"""

@author: Nikhil Gona
"""


import cv2
import time
import numpy as np

MODE = "MPI"
device = "gpu"
     
if MODE == "MPI" :
    protoFile = "pose\mpi\pose_deploy_linevec_faster_4_stages.prototxt"
    weightsFile = "pose\mpi\pose_iter_160000.caffemodel"
    nPoints = 15
    POSE_PAIRS = [[0,1], [1,2]]
inWidth = 368
inHeight = 368
threshold = 0.1


#input_source = args.video_file
cap = cv2.VideoCapture("input_video.mp4")

#setting the frame size
cap.set(3, 320) #setting the horizontal frame size 
cap.set(4, 240) #setting the vertical frame size

hasFrame, frame = cap.read()


vid_writer = cv2.VideoWriter('output_video.mp4',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame.shape[1],frame.shape[0]))

net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
if device == "cpu":
    net.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)
    print("Using CPU device")
elif device == "gpu":
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    print("Using GPU device")

while cv2.waitKey(1) < 0:
    t = time.time()
    hasFrame, frame = cap.read()
    frameCopy = np.copy(frame)
    if not hasFrame:
        cv2.waitKey()
        break

    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]

    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight),
                              (0, 0, 0), swapRB=False, crop=False)
    net.setInput(inpBlob)
    output = net.forward()

    H = output.shape[2]
    W = output.shape[3]
    # Empty list to store the detected keypoints
    points = []

    for i in range(nPoints):
        if i == 7:
            probMap = output[0, i, :, :]
            # Find global maxima of the probMap.
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
        
            # Scale the point to fit on the original image
            x = (frameWidth * point[0]) / W
            y = (frameHeight * point[1]) / H

            if prob > threshold :
                if x >= 140 and x <= 180:
                    if y < 120:
                        linear_velocity = (120 - y)*5/120 
                        angular_velocity = 0
                    elif y > 120:
                        linear_velocity = -(y - 120)*5/120
                        angular_velocity = 0
                elif x < 140:
                    if y < 120:
                        linear_velocity = (120 - y)*5/120 
                        angular_velocity = (140 - x)*np.pi/140 
                    elif y > 120:
                        linear_velocity = -(y - 120)*5/120
                        angular_velocity = (140 - x)*np.pi/140
                elif x > 180:
                    if y < 120:
                        linear_velocity = (120 - y)*5/120 
                        angular_velocity = -(x - 180)*np.pi/140 
                    elif y > 120:
                        linear_velocity = -(y - 120)*5/120
                        angular_velocity = -(x - 180)*np.pi/140
                cv2.putText(frame, "linear_velocity="+str(linear_velocity), (int(60), int(40)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, lineType=cv2.LINE_AA)
                cv2.putText(frame, "angular_velocity="+str(angular_velocity), (int(60), int(28)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, lineType=cv2.LINE_AA)
                # Add the point to the list if the probability is greater than the threshold
                points.append((int(x), int(y)))
            else :
                points.append(None)

    cv2.imshow('Output', frame)

    vid_writer.write(frame)
            
vid_writer.release()


