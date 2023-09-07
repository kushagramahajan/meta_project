import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import argparse

def plot_data(input_csv_path):
	df = pd.read_csv(input_csv_path)

	print('len(df): ', len(df))

	fig, ax = plt.subplots()

	def animate(i):


		## head
		j0_x = df['mediapipe_mouth_quest_head_recorder_joint7_x'][i]
		j0_y = df['mediapipe_mouth_quest_head_recorder_joint7_y'][i]
		j0_z = df['mediapipe_mouth_quest_head_recorder_joint7_z'][i]


		## left shoulder
		j1_x = df['mediapipe_left_shoulder_quest_left_scapula_recorder_joint9_x'][i]
		j1_y = df['mediapipe_left_shoulder_quest_left_scapula_recorder_joint9_y'][i]
		j1_z = df['mediapipe_left_shoulder_quest_left_scapula_recorder_joint9_z'][i]


		## right shoulder
		j2_x = df['mediapipe_right_shoulder_quest_right_scapula_recorder_joint14_x'][i]
		j2_y = df['mediapipe_right_shoulder_quest_right_scapula_recorder_joint14_y'][i]
		j2_z = df['mediapipe_right_shoulder_quest_right_scapula_recorder_joint14_z'][i]


		## left elbow
		j3_x = df['mediapipe_left_elbow_quest_left_arm_lower_recorder_joint11_x'][i]
		j3_y = df['mediapipe_left_elbow_quest_left_arm_lower_recorder_joint11_y'][i]
		j3_z = df['mediapipe_left_elbow_quest_left_arm_lower_recorder_joint11_z'][i]


		## right elbow
		j4_x = df['mediapipe_right_elbow_quest_right_arm_lower_recorder_joint16_x'][i]
		j4_y = df['mediapipe_right_elbow_quest_right_arm_lower_recorder_joint16_y'][i]
		j4_z = df['mediapipe_right_elbow_quest_right_arm_lower_recorder_joint16_z'][i]


		## left wrist
		j5_x = df['mediapipe_left_wrist_quest_left_hand_wrist_recorder_joint19_x'][i]
		j5_y = df['mediapipe_left_wrist_quest_left_hand_wrist_recorder_joint19_y'][i]
		j5_z = df['mediapipe_left_wrist_quest_left_hand_wrist_recorder_joint19_z'][i]


		## right wrist
		j6_x = df['mediapipe_right_wrist_quest_right_hand_wrist_recorder_joint45_x'][i]
		j6_y = df['mediapipe_right_wrist_quest_right_hand_wrist_recorder_joint45_y'][i]
		j6_z = df['mediapipe_right_wrist_quest_right_hand_wrist_recorder_joint45_z'][i]


		## hips
		j7_x = df['mediapipe_hip_quest_hip_recorder_joint1_x'][i]
		j7_y = df['mediapipe_hip_quest_hip_recorder_joint1_y'][i]
		j7_z = df['mediapipe_hip_quest_hip_recorder_joint1_z'][i]


		C = ["green", "black", "cyan", "blue", "violet", "pink", "grey", "yellow"]

		x = [j0_x, j1_x, j2_x, j3_x, j4_x, j5_x, j6_x, j7_x]
		y = [j0_y, j1_y, j2_y, j3_y, j4_y, j5_y, j6_y, j7_y]
		z = [j0_z, j1_z, j2_z, j3_z, j4_z, j5_z, j6_z, j7_z]
		
		ax.clear()
		ax.set_title("simple 2D scatter plot")
		ax.set_xlabel("X Axis")
		ax.set_ylabel("Y Axis")
		# ax.set_zlabel("Z Axis")

		ax.scatter(x, y, c = C)
		ax.set_aspect('equal', 'box')

		ax.set_xlim([-6.0, 1.0])
		ax.set_ylim([0, 5.2])
		

	ani = FuncAnimation(fig, animate, frames=4000, interval=100, repeat=False)

	plt.show()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_csv", type=str, required=True)
	
	args = parser.parse_args()

	plot_data(args.input_csv)
