#!/usr/bin/env python3

import os,sys
import json
import pandas as pd
import numpy as np


def build_dataframe():

	df = pd.DataFrame(columns=['subjectID','structureID'])

	return df

def update_dataframe(df,results,measure_name,subjectID):

	tmp = pd.DataFrame()

	structures = ['gray_matter','white_matter','csf','wholebrain']

	tmp['subjectID'] = [ 'subjectID' for f in summary_measure ]
	tmp['structureID'] = structures
	tmp[measure_name+'_mean'] = results[[0,2,4,6]]
	tmp[measure_name+'_sd'] = results[[1,3,5,7]]

	df = df.append(tmp,on=['subjectID','structureID'])

	return df

def extract_summary_measures(gm,wm,csf,measure):

	mean_gm = np.mean(measure[gm>0])
	std_gm = np.std(measure[gm>0])

	mean_wm = np.mean(measure[wm>0])
	std_wm = np.std(measure[wm>0])

	mean_csf = np.mean(measure[csf>0])
	std_csf = np.std(measure[csf>0])

	mean_wb = np.mean(measure[measure>0])
	std_wb = np.std(measure[measure>0])

	return [mean_gm,std_gm,mean_wm,std_wm,mean_csf,std_csf,mean_wb,std_wb]
	
def main():

	# load config
	with open('config.json','r') as config_f:
		config = json.load(config_f)

	# parse inputs
	subjectID = config['_inputs'][0]['meta']['subject']
	gm = nib.load('gm.nii.gz')
	gm = gm.get_fdata()
	wm = nib.load('wm.nii.gz')
	wm = wm.get_fdata(0)
	csf = nib.load('csf.nii.gz')
	csf = csf.get_fdata()

	# identify measures
	df_measures = glob.glob('*.nii.gz')
	measure_path = [ f for f in df_measures if f not in ['gm.nii.gz','5tt.nii.gz','wm.nii.gz','csf.nii.gz'] ]
	
	# build initital dataframe
	df = build_dataframe()

	# loop through measures in measure_path; load data, extract summary measures, then update dataframe
	for meas in measure_path:
		measure_name = meas
		data = nib.load(meas)
		data = data.get_fdata()

		results = extract_summary_measures(gm,wm,csf,data)
		df = update_dataframe(df,results,measure_name,subjectID)

	# build output directories
	if not os.isdir('parc-stats'):
		os.mkdir('parc-stats')

	if not os.isdir('parc-stats/parc-stats'):
		os.mkdir('parc-stats/parc-stats')

	# save dataframe
	df.to_csv('parc-stats/parc-stats/tissues.csv',index=False)

if __name__ == '__main__':
	main()