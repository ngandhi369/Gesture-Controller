# Gesture-Controller

## Problems:-
* Many of the Disabled People find it difficult to write using keyboard ,Also in Covid Situation many people don’t want to touch stuff that’s related to Covid.
* Sometimes when Mouse or Keyboard doesnt Work Properly Incase of a laptop is a Difficulty.

## Solution (Overview of project):-
* We make a Gesture Based Keyboard Interface using Webcam so that one can type things in a new Interactive way.
The Way it Works is using your Hand gesture and Eye tracking to use the Gui keyboard and mouse to Interact With it.

<p align="center">
<img src="https://github.com/ngandhi369/Gesture-Controller/blob/master/GUI.png?raw=true" width="490" alt="TKINTER GUI">
</p>

<!-- ![GUI Image](https://github.com/ngandhi369/Gesture-Controller/blob/master/GUI.png?raw=true) -->

## Key Features:-
* Developed python exe file setup using tkinter to fully control mouse & keyboard movements by human hand & eye gestures.
* It works with the help of different libraries and packages like OpenCV, Mediapipe, Cvzone, Dlib, Haar Cascade, etc.
* Also included Voice & basic storage features. Helpful in such a circumstances like COVID-19.

## Working:-

Model Detects Face and Hand points using following modules:

### dlib's 68 points facial detection:

* The mouth can be accessed through points [48, 68].
* The right eyebrow through points [17, 22].
* The left eyebrow through points [22, 27].
* The right eye using [36, 42].
* The left eye with [42, 48].
* The nose using [27, 35].
* And the jaw via [0, 17].

<img src="https://user-images.githubusercontent.com/49865067/171594764-e6eb099f-035b-476c-b77d-2e97d1e3d9ad.jpg" width="500" alt="FACE DETECTION">
<!-- ![overlayindices](https://user-images.githubusercontent.com/49865067/171594764-e6eb099f-035b-476c-b77d-2e97d1e3d9ad.jpg) -->

### HandtrackingModule's 21 points in hand:

* 4,8,12,16,20 - top of all five fingers, thumb top to pinky fingure top respectively.

<img src="https://user-images.githubusercontent.com/49865067/171595341-8b72e7ed-07b2-4571-9805-769f5a77e68c.png" width="600" alt="HAND TRACKING">
<!-- ![Hand_tracking](https://user-images.githubusercontent.com/49865067/171595341-8b72e7ed-07b2-4571-9805-769f5a77e68c.png) -->


Different packages:

cvzone's HandTrackingModule to detect hands.
Dlib's shape predictor(shape_predictor_68_face_landmarks.dat) and haarcascade classifier(frontal_face_detcetor.xml) to detects face 
imutils to fetch eyes landmarks from dlib's 68 points facial detection.
Eye-aspect-ratio(EAR) for detect blinking.
pynput for controlling keyboard events.
pyautogui for mouse events


## Dependencies:-

* CvZone
* Pynput
* HaarCascade
* PyAutoGui
* Tkinter
* Mediapipe
* auto-py-to-exe
* Dlib

<p align="center">
<img src="https://github.com/ngandhi369/Gesture-Controller/blob/master/gc.jpg?raw=true" width="850" alt="MAIN IMAGE">
</p>

<!-- ![GC Image](https://github.com/ngandhi369/Gesture-Controller/blob/master/gc.jpg?raw=true) -->

## References:-
* > ###  [Demo Link](https://drive.google.com/file/d/1swmmA05yG83uVJiyZJT6lMpWhf7o_nkY/view?usp=sharing)
* > ###  [Reference link for .dat file](https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat)

https://user-images.githubusercontent.com/49865067/159437765-fd7fbaf9-934e-4f2a-9d2b-ac7c19b0cdfa.mp4

