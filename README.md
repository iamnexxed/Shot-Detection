# Building a Neural Network Model for Shot Detection for macOS

## <b>PART A: Extracting Keypoints from videos</b>

### Skip this PART if you already have the keypoints needed to build a model

<b>Note</b>: Currently the Shot Detection Model takes in training 30 videos of Forehand shots, 30 videos of Backhand shots, 30 videos of Serves and 60 videos of No Stroke (each video consists of 58 frames). In case a keypoint is missing or not found for a frame an average of previous frame and next frame's coordinates is taken for the current frame's keypoint pixel coordinates.

------------------------------------------------------------------------
### Execution steps
1. Clone the repo
```
git clone https://github.com/iamnexxed/Shot-Detection
```
2. cd to the folder directory
```
cd Shot-Detection
```
3. Create a virtual enviroment in the project directory
```
python3 -m venv env
```

4. Activate the environment
```
source env/bin/activate
```

5. Install the package requirements
```
pip install -r requirements.txt
```

6. <b>Ensure that this project directory contains the "videos" folder with all the stroke videos</b>

7. Make the shell script executable
```
chmod +x process_mp4_files.sh
```

8. Run the shell script
```
./process_mp4_files.sh
```

This will create an output folder in each stroke directory. The output folder will contain keypoint files named as "<b>video_number.mp4.points</b>". The last step might take some time as it calculates the keypoints using mediapipe on a single thread on the CPU.

------------------------------------------------------------------------

## <b>PART B: Creating Neural Network Model from Keypoints</b>
1. Open the Python Notebook <i>lstm.ipynb</i>
2. If you have Anaconda preinstalled, select the python notebook kernel as <i>anaconda3/bin/python3</i>. The anaconda framework should already contain the necessary packages.
3. Follow this step if you don't have anaconda installed.
- Install- "matplotlib.pyplot, tensorflow, keras, scikit-learn" python packages in your python notebook.
4. Now run all the cells in the python notebook
5. It should create an images folder which contains all the distances for each tennis stroke
6. Further it should also create a models folder which stores the LSTM tensorflow model


## References:
1. Keypoints: 
https://github.com/google/mediapipe/blob/master/docs/solutions/pose.md
![Keypoints](https://camo.githubusercontent.com/54e5f06106306c59e67acc44c61b2d3087cc0a6ee7004e702deb1b3eb396e571/68747470733a2f2f6d65646961706970652e6465762f696d616765732f6d6f62696c652f706f73655f747261636b696e675f66756c6c5f626f64795f6c616e646d61726b732e706e67)

2. Tennis Strokes Recognition from Generated Stick Figure Video Overlays by Boris Bačić and Ishara Bandara
https://www.scitepress.org/Papers/2022/108273/108273.pdf