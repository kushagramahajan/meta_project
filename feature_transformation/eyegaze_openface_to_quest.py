import numpy as np
import pandas as pd
import argparse


def get_quaternion_from_euler(roll, pitch, yaw):
    """
    Convert an Euler angle to a quaternion.

    Input
    :param roll: The roll (rotation around x-axis) angle in radians.
    :param pitch: The pitch (rotation around y-axis) angle in radians.
    :param yaw: The yaw (rotation around z-axis) angle in radians.

    Output
    :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
    """
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

    return [qx, qy, qz, qw]

## Function to convert the gazze angles to Quaternion

def transform(input_csv, output_csv):

    df = pd.read_csv(input_csv)

    print('len(df): ', len(df))
    print('df.columns: ', df.columns)

    gaze_0_x_quat_arr = []
    gaze_0_y_quat_arr = []
    gaze_0_z_quat_arr = []
    gaze_0_w_quat_arr = []

    gaze_1_x_quat_arr = []
    gaze_1_y_quat_arr = []
    gaze_1_z_quat_arr = []
    gaze_1_w_quat_arr = []

    for i in range(len(df)):
        gaze_0_x_quat, gaze_0_y_quat, gaze_0_z_quat, gaze_0_w_quat = get_quaternion_from_euler(df['gaze_0_x'][i], df['gaze_0_y'][i], df['gaze_0_z'][i])
        
        gaze_0_x_quat_arr.append(gaze_0_x_quat)
        gaze_0_y_quat_arr.append(gaze_0_y_quat)
        gaze_0_z_quat_arr.append(gaze_0_z_quat)
        gaze_0_w_quat_arr.append(gaze_0_w_quat)

        gaze_1_x_quat, gaze_1_y_quat, gaze_1_z_quat, gaze_1_w_quat = get_quaternion_from_euler(df['gaze_1_x'][i], df['gaze_1_y'][i], df['gaze_1_z'][i])

        gaze_1_x_quat_arr.append(gaze_1_x_quat)
        gaze_1_y_quat_arr.append(gaze_1_y_quat)
        gaze_1_z_quat_arr.append(gaze_1_z_quat)
        gaze_1_w_quat_arr.append(gaze_1_w_quat)


    df_quest = pd.DataFrame()

    df_quest['timestamp'] = df['timestamp']

    df_quest['openface_euler_gaze_0_x_quest_quaternion'] = gaze_0_x_quat_arr
    df_quest['openface_euler_gaze_0_y_quest_quaternion'] = gaze_0_y_quat_arr
    df_quest['openface_euler_gaze_0_z_quest_quaternion'] = gaze_0_z_quat_arr
    df_quest['openface_euler_gaze_0_w_quest_quaternion'] = gaze_0_w_quat_arr

    df_quest['openface_euler_gaze_1_x_quest_quaternion'] = gaze_1_x_quat_arr
    df_quest['openface_euler_gaze_1_y_quest_quaternion'] = gaze_1_y_quat_arr
    df_quest['openface_euler_gaze_1_z_quest_quaternion'] = gaze_1_z_quat_arr
    df_quest['openface_euler_gaze_1_w_quest_quaternion'] = gaze_1_w_quat_arr

    df_quest['openface_euler_gaze_angle_x_quest_quaternion'] = (df_quest['openface_euler_gaze_0_x_quest_quaternion'] + df_quest['openface_euler_gaze_1_x_quest_quaternion']) / 2
    df_quest['openface_euler_gaze_angle_y_quest_quaternion'] = (df_quest['openface_euler_gaze_0_y_quest_quaternion'] + df_quest['openface_euler_gaze_1_y_quest_quaternion']) / 2

    df_quest.set_index('timestamp', inplace=True)

    df_quest.to_csv(output_csv)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv", type=str, required=True)
    parser.add_argument("--output_csv", type=str, required=True)
    
    args = parser.parse_args()

    transform(args.input_csv, args.output_csv)

