import numpy as np
import pandas as pd
import argparse


## Function to convert the Openface AU weights to the Quest AU weights

## Removed AU25_r and AU45_r since there is no mapping to the Quest AUs

def transform(input_csv, output_csv):

	openface_to_quest_mapping = {
		'AU01_r' : 'inner_brow_raiser',
		'AU02_r' : 'outer_brow_raiser',
		'AU04_r' : 'brow_lowerer',
		'AU05_r' : 'upper_lid_raiser',
		'AU06_r' : 'cheek_raiser',
		'AU07_r' : 'lid_tightener',
		'AU09_r' : 'nose_wrinkler',
		'AU10_r' : 'upper_lip_raiser',
		'AU12_r' : 'lip_corner_puller',
		'AU14_r' : 'dimpler',
		'AU15_r' : 'lip_corner_depressor',
		'AU17_r' : 'chin_raiser',
		'AU20_r' : 'lip_stretcher',
		'AU23_r' : 'lip_tightener',
		'AU26_r' : 'jaw_drop',

	}


	df = pd.read_csv(input_csv)

	print('df.columns: ', df.columns)
	print('len(df): ', len(df))

	df_quest = pd.DataFrame()

	df_quest['timestamp'] = df['timestamp']

	for col_name in df.columns:
		if ('AU' in col_name and '_r' in col_name and 'AU25' not in col_name and 'AU45' not in col_name):
			df_quest['openface_' + col_name.strip() + '_quest_' + openface_to_quest_mapping[col_name.strip()]] = df[col_name] / 5.0

	df_quest.set_index('timestamp', inplace=True)

	df_quest.to_csv(output_csv)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_csv", type=str, required=True)
	parser.add_argument("--output_csv", type=str, required=True)
	
	args = parser.parse_args()

	transform(args.input_csv, args.output_csv)