#!/usr/bin/env python3

import os,sys
import json
import glob
import pandas as pd
import numpy as np
import nibabel as nib


def build_dataframe():

	df = pd.DataFrame(columns=['subjectID','structureID'])

	return df

def update_dataframe(df,mean,sd,measure_name,subjectID):

	tmp = pd.DataFrame()

	structures = ['gray_matter','white_matter','csf','wholebrain']

	tmp['subjectID'] = [ subjectID for f in structures ]
	tmp['structureID'] = structures
	tmp[measure_name+'_mean'] = mean
	tmp[measure_name+'_sd'] = sd

	if df.empty:
		df = pd.concat([df,tmp])
	else:
		df = df.merge(tmp,on=['subjectID','structureID'])

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

	mean_meas = [mean_gm,mean_wm,mean_csf,mean_wb]
	sd_meas = [std_gm,std_wm,std_csf,std_wb]

	return mean_meas, sd_meas
	
def main():

	# load config
	with open('config.json','r') as config_f:
		config = json.load(config_f)

	# parse inputs
	subjectID = config['_inputs'][0]['meta']['subject']
	gm = nib.load('gm_bin.nii.gz')
	gm = gm.get_fdata()
	wm = nib.load('wm_bin.nii.gz')
	wm = wm.get_fdata()
	csf = nib.load('csf_bin.nii.gz')
	csf = csf.get_fdata()

	# identify measures
	df_measures = glob.glob('*.nii.gz')
	measure_path = [ f for f in df_measures if f not in ['gm.nii.gz','5tt.nii.gz','wm.nii.gz','csf.nii.gz','gm_bin.nii.gz','wm_bin.nii.gz','csf_bin.nii.gz'] ]
	
	# build initital dataframe
	df = build_dataframe()

	# loop through measures in measure_path; load data, extract summary measures, then update dataframe
	for meas in measure_path:
		measure_name = meas.split('.')[0]
		data = nib.load(meas)
		data = data.get_fdata()

		mean,sd = extract_summary_measures(gm,wm,csf,data)
		df = update_dataframe(df,mean,sd,measure_name,subjectID)

	# build output directories
	if not os.isdir('parc-stats'):
		os.mkdir('parc-stats')

	if not os.isdir('parc-stats/parc-stats'):
		os.mkdir('parc-stats/parc-stats')

	# save dataframe
	df.to_csv('parc-stats/parc-stats/tissues.csv',index=False)

if __name__ == '__main__':
	main()