
# Docker Image: Heart Rate, Mediapipe Pose and OpenFace 

## Heart Rate Detection

- Used [rPPG-Toolbox](https://github.com/ubicomplab/rPPG-Toolbox) for extraction of heart rate from videos. We used an interval of 5 seconds to compute the heart rate for each 5 second interval. This can be modified by changing the `interval` variable in `evaluation/metrics.py`. 

- The output is available in CSV format in the folder `output_files`. The code uses 2 algorithms to estimate the heart rate: based on PPG using peak detection, and based on PPG using Fast Fourier transform (FFT).

Supported models: 
- Deepphys
- TSCAN
- Physnet
- EfficientPhys

The directory containing the input files along with other hyperparameters can be set in the config files, as shown in the sample command below.

#### Commands Used:
- `cd /home/rPPG-Toolbox`
- `python main.py --config_file ./configs/infer_configs/PURE_UBFC_DEEPPHYS_BASIC.yaml`


## Mediapipe Pose

Mediapipe is used for extraction of 3-dimensional pose information for 33 human body pose joints. Detailed information about Mediapipe based pose extraction can be found [here](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker). The columns follow the format `landmark_LANDMARK_AXIS`, and the timestamps are in milli-seconds.

#### Commands Used:
 - `cd /home/Mediapipe-Pose`
 - `python mediapipe_pose.py --input_video_path INPUT_VIDEO_PATH --output_video_path OUTPUT_VIDEO_PATH --output_csv_path OUTPUT_CSV_PATH`

## OpenFace

OpenFace is used to extract the following:

- Eye gaze direction vectors for both eyes separately, as well as an average vector for the two eyes put together.
- Facial Action Units used to describe facial expressions.
- Head pose comprising the position and rotation information.

#### Command Used:

`/usr/local/bin/FeatureExtraction -f {video_path} -q -2Dfp -3Dfp -pose -aus -gaze -multi-view 1 -wild -out_dir {output_folder} -of {output_name}`