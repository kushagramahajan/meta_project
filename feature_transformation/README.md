# Feature Transformation to Quest-Like Features

The below sections show how to transform features like facial action units, body pose and eye gaze from openface and mediapipe to the Quest format.


## Facial Action Units

- `AU_openface_to_quest.py` is used to transform the intensity of facial action units obtained. from openface into quest-like format.

- Openface produces intensity values on a scale of 0 to 5, while Quest provides the intensity values on a scale of 0 to 1. So, we normalize the openface output such that the values are between 0 and 1.

- The column names in the output file indicate the mapping between Action Units (AUs) in openface and their corresponding AUs produced by Quest. The naming follows the convention `openface_AU-NUMBER_r_quest_AU-NAME`.

- Also, AU25 and AU45 are omitted since there is no mapping between between them and the Quest AUs.

#### Command Used:

`python AU_openface_to_quest.py --input_csv INPUT_CSV --output_csv OUTPUT_CSV`


## Body Pose

- `bodypose_mediapipe_to_quest_transform.py` is used to convert the body pose landmarks from the Mediapipe format to the Quest format.

- Mediapipe uses the top-left corner of the image as the origin. For each pose landmark, it produced the pixel based `x`, `y` coordinates which are normalized by the image width and height respectively. For the set of 33 landmarks which are not visible in the image, Mediapipe produces an estimate of their location based on the landmarks that are detected. Their normalized `x` and `y` position values may however be greater than 1 since they are technically *outside* the image. 

- Quest produces position and rotation information of 70 joints. The position values are in absolute **meters**. The origin is the center of the floor since the floor level is caliibrated in Quest before beginning any operations. 

- For converting pixels to meters, we set the distance between the 2 eyes as 8cm using the variable `fixed_eye_distance`. This is a hyperparameter that can be changed. The mean pixel distance between the left and the right eye produced by Mediapipe is used approximate the height and width of a pixel.

- Since Mediapipe does not provide the coordinates for the floor (unlike Quest), we assume the produced `y` coordinates of the farthest foot as an approximation for the floor to transform the `y` coordinates from the Mediapipe to Quest scale. This is because Mediapipe detects left heel, right heel, left foot index, right foot index.

- To transform the `x` coordinate from the Mediapipe format to Quest format, we simply subtract 0.5 from the x-coordinates to center the x-axis. 

- The z-coordinates are **not** transformed.

- Only a subset of the pose joints produced by mediapipe find exact matches in body joints produced by Quest. The mediapipe pose joints which have matched in Quest are: left shoulder, right shoulder, left elbow, right elbow, left wrist, right wrist, left pinky finger, right pinky finger, left index finger, right index finger, left thumb, right thumb, hip.

- The columns in the generated CSV file follow the format `mediapipe_MEDIAPIPE-JOINT_quest_QUEST-JOINT_recorder_RECORDER-JOINT_AXIS`.

#### Command Used:

`python bodypose_mediapipe_to_quest_transform.py --input_video INPUT_VIDEO --input_csv INPUT_CSV --output_csv OUTPUT_CSV`


## Eye gaze

- Openface produces `gaze_0_x`, `gaze_0_y`, `gaze_0_z` as direction vector in world coordinates for eye 0, and `gaze_1_x`, `gaze_1_y`, `gaze_1_z` as direction vector in world coordinates for eye 1. In addition, it gives `gaze_angle_x`, `gaze_angle_y` as the eye gaze directions in radians in world coordinates averaged for both eyes. Quest, however, gives the `rotation_l_x`, `rotation_l_y`, `rotation_l_z`, `rotation_l_w` as the Quaternion angles for the left eye and corresponding angles for the right eye as well.

- `eyegaze_openface_to_quest.py` is used to convert the Euler angles (produced by Openface) into Quaternion angles (produced by Quest).

- We also produce `gaze_angle_x_Quaternion` and `gaze_angle_y_Quaternion` for the averaged Quaternion `x` and `y` angles respectively between the left and the right eyes.


#### Command Used:

`python eyegaze_openface_to_quest.py --input_csv INPUT_CSV --output_csv OUTPUT_CSV`



# Plotting Quest Body Pose Features

- `quest_feature_plot.py` is used for plotting a subset of the Quest body landmarks. This is used for qualitative analysis and verification of the body pose data obtained after transforming the mediapipe pose data to Quest format.

- The current list of body joints that we have plotted are: head, left shoulder, right shoulder, left elbow, right elbow, left wrist, right wrist and hip. However, these can be modified to plot any other joints as well.


#### Command Used:

`python quest_bodypose_feature_plot.py --input_csv INPUT_CSV`
