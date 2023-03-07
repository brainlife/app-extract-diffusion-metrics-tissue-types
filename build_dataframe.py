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

	df_measures = []
	
	# dti
	fa = config['fa']
	if os.path.isfile(fa):
		df_measures = df_measures+['ad','fa','md','rd']

	# dki
	ga = config['ga']
	if os.path.isfile(ga):
		df_measures = df_measures+['ga','ak','mk','rk']

	# noddi
	if 'odi' in config:
		odi = config['odi']
		if os.path.isfile(odi):
			df_measures = df_measures+['ndi','odi','isovf']
		
	# myelin-map
	if 'myelin' in config:
		myelin = config['myelin']
		if os.path.isfile(myelin):
			df_measures = df_measures+['myelin']
		
	# qmri
	if 'T1' in config:
		qmri = ["T1","R1","M0","PD","MTV","VIP","SIR","WF"]
		for i in qmri:
			test_met = config[i]
			if os.path.isfile(test_met):
				df_measures = df_measures+[i]
	
	measure_path = [ config[f] for f in df_measures ]

	df = build_dataframe()

	for meas in measure_path:
		measure_name = meas
		data = nib.load(meas)
		data = data.get_fdata()

		results = extract_summary_measures(gm,wm,csf,data)
		df = update_dataframe(df,results,measure_name,subjectID)

	if not os.isdir('parc-stats'):
		os.mkdir('parc-stats')

	if not os.isdir('parc-stats/parc-stats'):
		os.mkdir('parc-stats/parc-stats')

	df.to_csv('parc-stats/parc-stats/tissues.csv',index=False)


if __name__ == '__main__':
	main()