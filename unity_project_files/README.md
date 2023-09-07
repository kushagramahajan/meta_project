# Unity Project Files

The following files have been modified for storing the Eye gaze, Body pose (includes Head pose), Facial action unit data in CSV files. These files are present within the project in `Assets/Oculus/VR/Scripts`. All angles provided by Quest such as for eye gaze orientation and body joint orientation are in Quaternion.

## Eye Gaze Data

- `OVREyeGaze.cs` is used for tracking and storing the eye gaze data. The frequency of data recoding is 17-20 data points per second. The timestamp is stored for each data point to help with synchronization. The position and orientation data for the 2 eyes is tracked and stored. 

- The position coordinates for the 2 eyes are fixed throughout since the frame of reference is the point between the 2 eyes. The orientation paramters change depending on the gaze direction. 

- The units for measuring the position is meters. The orientation is measured in Quaternion.

- Further details about eye tracking though Meta's Movement SDK can be found [here] (https://developer.oculus.com/documentation/unity/move-eye-tracking/). 

- The output CSV file has the filename of the form `TIMESTAMP_eyegaze_data.csv`. 


## Body Pose Data

- `OVRBody.cs` is used for tracking and storing the body pose (along with the head pose) data. The frequency of data recoding is 17-20 data points per second. There are a total of 70 body joints that are tracked by Quest. The timestamp is stored for each data point to help with synchronization.

- For each body joint, the position as well as the orientation are tracked. The units for measuring the position is meters. The origin the center of the floor which is set during the calibration of the Quest device. The orientation is measured in Quaternion.

- The head is a separate joint that is tracked as part of body tracking.

- Further details about body tracking though Meta's Movement SDK can be found [here] (https://developer.oculus.com/documentation/unity/move-body-tracking/). 

- The output CSV file has the filename of the form `TIMESTAMP_bodypose_data.csv`. 


## Facial Action Units

- `OVRFaceExpressions.cs` is used for tracking and storing the facial action unit data. The frequency of data recoding is 17-20 data points per second. There are a total of 63 facial action units that are tracked by Quest. The timestamp is stored for each data point to help with synchronization.

- A human wearing the headset will typically trigger multiple of these action units at the same time. The Quest face tracking API returns a weight corresponding to the strength of activation for each action unit (e.g., barely raising an eyebrow or an extreme raise of an eyebrow). This value is between 0 and 1.

- Further details about face tracking and the complete list of facial action units tracked though Meta's Movement SDK can be found [here] (https://developer.oculus.com/documentation/unity/move-face-tracking/). 

- The FACS - Quest Mapping for the facial action units can be found [here] (https://docs.google.com/document/d/10esqpRAtKHwiOf5CRSEoMb2DuYgDyzs0yjbKvxQcY6w/edit?usp=sharing).

- The output CSV file has the filename of the form `TIMESTAMP_faceexpressions_data.csv`.