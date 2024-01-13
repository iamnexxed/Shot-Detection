
"""
Copyrights Reserved. Levenetic Inc.
Author: Sudhanshu Bhamburkar

Description: 
    This is the script for generating the keypoints for a video.
    Run this script along with a bash script which executes for all the generated video files.
    Make sure you have python ffmpeg installed

Run with:
    # If you haven't initialized virtual environment for the project run this command
    python3 -m venv env 

    source env/bin/activate
    pip install -r requirements.txt
    python keypoints.py -i videos/serve.mp4 -o videos/output_video.mp4 -b False -m 1

Reference:
    https://github.com/google/mediapipe/blob/master/docs/solutions/pose.md
    https://medium.com/nerd-for-tech/deep-learning-based-human-pose-estimation-using-opencv-and-mediapipe-d0be7a834076
"""

import cv2
import mediapipe as mp
import time
import numpy as np

# Total keypoints
KEYPOINT_COUNT = 33
# Max frames in a video
MAX_FRAME_COUNT = 58

class PoseDetector:

    def __init__(self, mode = False, upBody = False, smooth=True, detectionCon = 0.5, trackCon = 0.5):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode, 
                                    smooth_landmarks=self.upBody, 
                                    smooth_segmentation=self.smooth, 
                                    min_detection_confidence=self.detectionCon, 
                                    min_tracking_confidence=self.trackCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS

    def getPosition(self, img, draw=True):
        lmList= []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList



import time

import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to our input video")
ap.add_argument("-o", "--output",
	help="path to our output video")
ap.add_argument("-s", "--fps", type=int, default=30,
	help="set fps of output video")
ap.add_argument("-b", "--black", type=str, default=False,
	help="set black background")
ap.add_argument("-k", "--keypoints", type=str, default="key.points",
	help="output keypoints")
# Handling missing values
ap.add_argument("-m", "--handle_missing", type=int, default=0,
	help="Set 0 if you dont want to handle missing values")    
args = vars(ap.parse_args())


pTime = 0
black_flag = eval(args["black"])
cap = cv2.VideoCapture(args["input"])

out = None
if args["output"] is not None:
    out = cv2.VideoWriter(args["output"], cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 
                        args["fps"], (int(cap.get(3)), int(cap.get(4))))


detector = PoseDetector()
export_file = args["keypoints"]
handle_missing = args["handle_missing"]

rows = []
image_count = 0
missing_indices = []

f = open(export_file, "w")

while(cap.isOpened()):
    success, img = cap.read()
    
    if success == False:
        break
    
    img, p_landmarks, p_connections = detector.findPose(img, False)
    #print(p_landmarks)
    # use black background
    if black_flag:
        img = img * 0
    
    # draw points
    # mp.solutions.drawing_utils.draw_landmarks(img, p_landmarks, p_connections)
    lmList = detector.getPosition(img)
    if len(lmList) < KEYPOINT_COUNT:
        print(f"Warning: Incorrect frame keypoint size detected ({len(lmList)}). Filling in zero values.")
        idcount = 0
        lmList = []
        missing_indices.append(image_count)
        while idcount < KEYPOINT_COUNT:
            lmList.append(np.array([idcount, 0, 0]))
            idcount += 1
    rows.append(lmList)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    if out is not None:
        out.write(img)
    image_count += 1
    #cv2.imshow("Image", img)
    cv2.waitKey(1)

def findNextFilledIndex(startIndex, rows, emptyIndices):
    currentIndex = startIndex
    while currentIndex < len(rows) and currentIndex in emptyIndices:
        currentIndex += 1
    return currentIndex


# Trim the list if it has more than MAX_FRAME_COUNT elements
if len(rows) > MAX_FRAME_COUNT:
    print(f"Warning: Too many frames than desired ({len(rows)}). Resizing to default {MAX_FRAME_COUNT}")
    rows = rows[:MAX_FRAME_COUNT]

if len(rows) < MAX_FRAME_COUNT:
    print(f"Warning: Less frames than desired ({len(rows)}). Resizing to default {MAX_FRAME_COUNT}")
    rows = rows[:MAX_FRAME_COUNT]

# Append an empty array to the list if it has less than MAX_FRAME_COUNT elements
while len(rows) < MAX_FRAME_COUNT:
    idcount = 0
    lmList = []
    while idcount < KEYPOINT_COUNT:
        lmList.append(np.array([idcount, 0, 0]))
        idcount += 1
    rows.append(lmList)
#rows = np.array(rows)

print(f"Frame Count: {len(rows)}")

last_index = 0
for i in range(len(rows)):
    # lmList = np.array(rows[i])
    # Check for missing  values
    # Find the next frame which contains all the values
    next_index = findNextFilledIndex(i, rows, missing_indices)
    if next_index == i or next_index >= len(rows):
        next_index = last_index
    # print(f"Last index: {last_index}, Next Index: {next_index}")
    for j in range(KEYPOINT_COUNT):
        # if the line is empty
        if handle_missing != 0 and i in missing_indices:
            # Set second index as average of X Coordinate of (last_index row, next_index row)
            rows[i][j][1] = (rows[last_index][j][1] + rows[next_index][j][1]) / 2
            # Set third index as average of Y Coordinate of (last_index row, next_index row)
            rows[i][j][2] = (rows[last_index][j][2] + rows[next_index][j][2]) / 2
        # Store the string of the row in the line variable
        if len(rows[i][j]) > 0:
            line = ' '.join(map(str, np.array(rows[i][j])))
            f.write(line + ' ')
    f.write('\n')
    last_index = i

f.close()
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()

print("\n\n")