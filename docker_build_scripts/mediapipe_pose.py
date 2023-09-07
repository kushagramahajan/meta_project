import argparse
import json
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
import csv

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

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

def get_video_writer(cap, H_new: int, W_new: int, output: Path):
	
	out = cv2.VideoWriter(
		str(output),
		cv2.VideoWriter_fourcc(*"MJPG"),
		cap.get(cv2.CAP_PROP_FPS),
		(W_new, H_new),
	)
	
	return out



def convert_video(path: Path, output: Path, output_csv_path: Path):
	all_x = []
	all_y = []
	all_z = []
	timestamps = []
	cap = cv2.VideoCapture(str(path))

	frame_width = int(cap.get(3))
	frame_height = int(cap.get(4))

	out = get_video_writer(
		cap, frame_height, frame_width, output
	)
	
	print('frame rate: ', cap.get(cv2.CAP_PROP_FPS))

	with mp_pose.Pose(
		min_detection_confidence=0.5,
		min_tracking_confidence=0.5) as pose:
		while cap.isOpened():
			success, image = cap.read()
			if not success:
				print("Ignoring empty camera frame.")
				# If loading a video, use 'break' instead of 'continue'.
				break

			# To improve performance, optionally mark the image as not writeable to
			# pass by reference.
			image.flags.writeable = False
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			results = pose.process(image)
			counter = 0
			current_x = []
			current_y = []
			current_z = []

			if results.pose_landmarks:
				for landmark in results.pose_landmarks.landmark:
					current_x.append(landmark.x)
					current_y.append(landmark.y)
					current_z.append(landmark.z)
					counter += 1
				timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC)/1000)
				all_x.append(current_x)
				all_y.append(current_y)
				all_z.append(current_z)
				# Draw the pose annotation on the image.
				image.flags.writeable = True
				image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
				mp_drawing.draw_landmarks(
					image,
					results.pose_landmarks,
					mp_pose.POSE_CONNECTIONS,
					landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

				# Flip the image horizontally for a selfie-view display.
				# cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
				out.write(image)
				# if cv2.waitKey(5) & 0xFF == 27:
				# 	break
	
	cap.release()
	out.release()
	
	with open(output_csv_path, "w") as myfile:
		writer = csv.writer(myfile, quoting=csv.QUOTE_ALL)

		field = ["timestamp"]
		for i in range(0, 33):
			field.append("landmark_" + mediapipe_landmark_name_mapping[i] + "_x")
			field.append("landmark_" + mediapipe_landmark_name_mapping[i] + "_y")
			field.append("landmark_" + mediapipe_landmark_name_mapping[i] + "_z")
		writer.writerow(field)
		all_rows = []
		for i in range(len(all_x)):
			row = [timestamps[i]]
			for j in range(33):
				row.append(all_x[i][j])
				row.append(all_y[i][j])
				row.append(all_z[i][j])
			all_rows.append(row)
		writer.writerows(all_rows)




if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_video_path", type=str, required=True)
	parser.add_argument("--output_video_path", type=str, required=True)
	parser.add_argument("--output_csv_path", type=str, required=True)
	
	args = parser.parse_args()

	video = Path(args.input_video_path)
	assert video.is_file(), video

	output = Path(args.output_video_path)

	convert_video(video, output, args.output_csv_path)
	