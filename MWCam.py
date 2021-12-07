# import the necessary packages
from scipy.spatial import distance as dist      
from imutils import face_utils
import numpy as np
import pyautogui
import imutils
import time
import dlib
import cv2

position1 = 960 
position2 = 540

video_capture = cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #detect face
font = cv2.FONT_HERSHEY_SIMPLEX

def eye_aspect_ratio(eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear


def main() :
    
    EYE_AR_THRESH = 0.2
    EYE_AR_CONSEC_FRAMES = 1.0
   

    # initialize the frame counters and the total number of blinks

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
 
    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    
    
    # start the video stream thread
    print("[INFO] starting video stream thread...")
    print("[INFO] print q to quit...")
    
    ret, frame = video_capture.read()
    time.sleep(1.0)
    COUNTER = 0
    TOTAL = 0

    COUNTER1 = 0
    TOTAL1 = 0
    
    s = 0
    p = 0
   
    #mlr.linear_regression_model()
    # loop over frames from the video stream
    while True:
        

        ret, frame = video_capture.read()
        rows, cols, _ = frame.shape
        frame = imutils.resize(frame, width=1200)
        frame = cv2.flip(frame, 1) 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        # detect faces in the grayscale frame
        ##############################################
        rects = detector(gray, 0)
        
        faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=7,
        minSize=(20, 20),  #  size of face  (move far the size of face decreases)
        flags=cv2.CASCADE_SCALE_IMAGE
        )
        ##############################################
        
        # loop over the face detections
        for rect in rects:
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
    
                # extract the left and right eye coordinates, then use the
                # coordinates to compute the eye aspect ratio for both eyes
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                
    
                # average the eye aspect ratio together for both eyes
                ear = (leftEAR + rightEAR) / 2.0
               
    
                # compute the convex hull for the left and right eye, then
                # visualize each of the eyes
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 2)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 2)
                
                for (x, y, w, h) in faces:
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 6)
                            roi_gray = gray[y:y+h, x:x+w]
                            roi_color = frame[y:y+h, x:x+w]
                            
                            #pyautogui.moveTo(x_medium-100,y_medium-100, duration = 0)
                            pyautogui.moveTo(x+20,y-80, duration = 0)
                            

                
    
                # check to see if the eye aspect ratio is below the blink
                # threshold, and if so, increment the blink frame counter
                start=0
                stop=0
    

       
                if ear < EYE_AR_THRESH:
                        COUNTER += 1
                        p=p+1
                                          
                        start = time.time()
                        if p == 1:
                             start1=start
                        
                else:                       
                        if COUNTER >= EYE_AR_CONSEC_FRAMES:
                                TOTAL += 1
                                stop = time.time()
                                total_time = round(abs(stop - start1),2)
                                print("time delay of blink = ", total_time)
                                
                                if total_time >=0.6:
                                    pyautogui.click(x+20, y-80) 
                                                               
                                p=0
                                total_time = 0
                                
                        
                        COUNTER = 0
                
                # draw the total number of blinks on the frame along with
                # the computed eye aspect ratio for the frame
                
                cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
           
        # show the frame
        cv2.imshow("Frame", frame)
        Kkey = cv2.waitKey(1) & 0xFF
     
        # if the `q` key was pressed, break from the loop
        if Kkey == ord("q"):
                break
    
    # do a bit of cleanup
    video_capture.release()
    cv2.destroyAllWindows()
if __name__ == '__main__' :
    main()
