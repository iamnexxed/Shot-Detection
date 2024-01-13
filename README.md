# Building a Neural Network Model for Shot Detection for macOS

## <b>PART A: Extracting Keypoints from videos</b>

### Skip this PART if you already have the keypoints needed to build a model

### <b>Note</b>: Currently the Shot Detection Model takes in training 30 videos of Forehand shots, 30 videos of Backhand shots, 30 videos of Serves and 60 videos of No Stroke (each video consists of 58 frames). In case a keypoint is missing or not found for a frame an average of previous frame and next frame's coordinates is taken for the current frame's keypoint pixel coordinates.
------------------------------------------------------------------------
### Execution steps
1. Create a virtual enviroment in your current project directory
```
python3 -m venv env
```

2. Activate the environment
```
source env/bin/activate
```

3. Install the package requirements
```
pip install -r requirements.txt
```

4. <b>Ensure that this project directory contains the "videos" folder with all the stroke videos</b>

5. Make the shell script executable
```
chmod +x process_mp4_files.sh
```

6. Run the shell script
```
./process_mp4_files.sh
```

This will create an output folder in each stroke directory. The output folder will contain keypoint files named as "<b>video_number.mp4.points</b>". The last step might take some time as it calculates the keypoints using mediapipe on a single thread on the CPU.

------------------------------------------------------------------------

## <b>PART B: Creating Neural Network Model from Keypoints</b>
1. Open the Python Notebook <i>lstm.ipynb</i>
2. If you have Anaconda preinstalled, select the python notebook kernel as <i>anaconda3/bin/python3</i>. The anaconda framework should already contain the necessary packages.
3. Follow this step if you don't have anaconda installed.
- Install- "matplotlib.pyplot, tensorflow, keras" python packages in your python notebook.
4. Now run all the cells in the python notebook
5. It should create an images folder which contains all the distances for each tennis stroke
6. Further it should also create a model folder which stores the tensorflow model


## References:
1. Keypoints: 
https://github.com/google/mediapipe/blob/master/docs/solutions/pose.md
![Alt text](image.png)

2. Tennis Strokes Recognition from Generated Stick Figure Video Overlays by Boris Bačić and Ishara Bandara
https://www.scitepress.org/Papers/2022/108273/108273.pdf