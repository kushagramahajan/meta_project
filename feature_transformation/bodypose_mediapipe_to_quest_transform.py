import numpy as np
import pandas as pd
import cv2
import argparse


mediapipe_landmark_name_mapping = {
	0: "nose",
	1: "left_eye_inner",
	2: "left_eye",
	3: "left_eye_outer",
	4: "right_eye_inner",
	5: "right_eye",
	6: "right_eye_outer",
	7: "left_ear",
	8: "right_ear",
	9: "mouth_left",
	10: "mouth_right",
	11: "left_shoulder",
	12: "right_shoulder",
	13: "left_elbow",
	14: "right_elbow",
	15: "left_wrist",
	16: "right_wrist",
	17: "left_pinky",
	18: "right_pinky",
	19: "left_index",
	20: "right_index",
	21: "left_thumb",
	22: "right_thumb",
	23: "left_hip",
	24: "right_hip",
	25: "left_knee",
	26: "right_knee",
	27: "left_ankle",
	28: "right_ankle",
	29: "left_heel",
	30: "right_heel",
	31: "left_foot_index",
	32: "right_foot_index"
}


mediapipe_landmark_to_quest_mapping = {
	"mouth": "head",
	"left_shoulder": "left_scapula",
	"right_shoulder": "right_scapula",
	"left_elbow": "left_arm_lower",
	"right_elbow": "right_arm_lower",
	"left_wrist": "left_hand_wrist",
	"right_wrist": "right_hand_wrist",
	"left_pinky": "left_hand_little_tip",
	"right_pinky": "right_hand_little_tip",
	"left_index": "left_hand_index_tip",	
	"right_index": "right_hand_index_tip",
	"left_thumb": "left_hand_thumb_tip",
	"right_thumb": "right_hand_thumb_tip",
	"hip": "hip"
}

quest_to_recorder_mapping = {
	"hip": "joint1",
	"head": "joint7",
	"left_scapula": "joint9",
	"right_scapula": "joint14",
	"left_arm_lower": "joint11",
	"right_arm_lower": "joint16",
	"left_hand_wrist": "joint19",
	"right_hand_wrist": "joint45",
	"left_hand_little_tip": "joint43",
	"right_hand_little_tip": "joint69",
	"left_hand_index_tip": "joint28",
	"right_hand_index_tip": "joint54",
	"left_hand_thumb_tip": "joint23",
	"right_hand_thumb_tip": "joint49"
}


def transform(input_csv, input_video, output_csv):
	df = pd.read_csv(input_csv)
	vcap = cv2.VideoCapture(input_video)

	print('len(df): ', len(df))
	
	max_y = -100

	## changing the x-axis reference to the middle of the frame and the y-axis reference to the bottom of the image

	for i in range(33):
	    pos_col_y = 'landmark_' + mediapipe_landmark_name_mapping[i] + '_y'
	    max_col = df[pos_col_y].max()
	    # print(max_col)
	    if (max_y < max_col):
	    	max_y = max_col

	# print('max_y: ', max_y)

	for i in range(33):
		pos_col_x = 'landmark_' + mediapipe_landmark_name_mapping[i] + '_x'
		pos_col_y = 'landmark_' + mediapipe_landmark_name_mapping[i] + '_y'

		df[pos_col_x] = df[pos_col_x] - 0.5

		df[pos_col_y] = (max_y - df[pos_col_y])/max_y


	## find average pixels between eye centers. This is used as an estimate to determine the
	## pixel height and width.

	if vcap.isOpened():
		width  = vcap.get(3)
		height = vcap.get(4)

	
	pos_righteye_col_x = 'landmark_right_eye_x'
	pos_lefteye_col_x = 'landmark_left_eye_x'
		
	avg_pixel_distance = (df[pos_lefteye_col_x] - df[pos_righteye_col_x]).mean() * width

	max_pixel_distance = (df[pos_lefteye_col_x] - df[pos_righteye_col_x]).max() * width

	print('avg_pixel_distance: ', avg_pixel_distance)
	print('max_pixel_distance: ', max_pixel_distance)

	fixed_eye_distance = 0.08

	## pixel height and with in meters
	pixel_height_width = fixed_eye_distance / max_pixel_distance
	
	
	for i in range(33):
		pos_col_x = 'landmark_' + mediapipe_landmark_name_mapping[i] + '_x'
		pos_col_y = 'landmark_' + mediapipe_landmark_name_mapping[i] + '_y'
		pos_col_z = 'landmark_' + mediapipe_landmark_name_mapping[i] + '_z'

		df[pos_col_x] = df[pos_col_x] * width * pixel_height_width

		df[pos_col_y] = df[pos_col_y] * height * pixel_height_width

	
	df_quest = pd.DataFrame()

	df_quest['timestamp'] = df['timestamp']

	for i in mediapipe_landmark_to_quest_mapping.keys():
		pos_col_x = 'landmark_' + i + '_x'
		pos_col_x_new = 'mediapipe_' + i + "_quest_" + mediapipe_landmark_to_quest_mapping[i] + '_recorder_' + quest_to_recorder_mapping[mediapipe_landmark_to_quest_mapping[i]] + '_x'

		pos_col_y = 'landmark_' + i + '_y'
		pos_col_y_new = 'mediapipe_' + i + "_quest_" + mediapipe_landmark_to_quest_mapping[i] + '_recorder_' + quest_to_recorder_mapping[mediapipe_landmark_to_quest_mapping[i]] + '_y'

		pos_col_z = 'landmark_' + i + '_z'
		pos_col_z_new = 'mediapipe_' + i + "_quest_" + mediapipe_landmark_to_quest_mapping[i] + '_recorder_' + quest_to_recorder_mapping[mediapipe_landmark_to_quest_mapping[i]] + '_z'

		if i == 'mouth':
			df_quest[pos_col_x_new] = (df['landmark_mouth_left_x'] + df['landmark_mouth_right_x'])/2
			df_quest[pos_col_y_new] = (df['landmark_mouth_left_y'] + df['landmark_mouth_right_y'])/2
			df_quest[pos_col_z_new] = (df['landmark_mouth_left_z'] + df['landmark_mouth_right_z'])/2
			continue

		if i == 'hip':
			df_quest[pos_col_x_new] = (df['landmark_left_hip_x'] + df['landmark_right_hip_x'])/2
			df_quest[pos_col_y_new] = (df['landmark_left_hip_y'] + df['landmark_right_hip_y'])/2
			df_quest[pos_col_z_new] = (df['landmark_left_hip_z'] + df['landmark_right_hip_z'])/2
			continue


		df_quest[pos_col_x_new] = df[pos_col_x]
		df_quest[pos_col_y_new] = df[pos_col_y]
		df_quest[pos_col_z_new] = df[pos_col_z]

	df_quest.set_index('timestamp', inplace=True)

	df_quest.to_csv(output_csv)



if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_video", type=str, required=True)
	parser.add_argument("--input_csv", type=str, required=True)
	parser.add_argument("--output_csv", type=str, required=True)
	
	args = parser.parse_args()

	transform(args.input_csv, args.input_video, args.output_csv)

