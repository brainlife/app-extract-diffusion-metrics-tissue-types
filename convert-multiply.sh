#!/bin/bash

ad=`jq -r '.ad' config.json`
fa=`jq -r '.fa' config.json`
md=`jq -r '.md' config.json`
rd=`jq -r '.rd' config.json`
ndi=`jq -r '.ndi' config.json`
odi=`jq -r '.odi' config.json`
isovf=`jq -r '.isovf' config.json`

measures="ad fa md rd ndi odi isovf"
types="gm wm csf"

mkdir -p output

[ ! -f gm.nii.gz ] && mrconvert -coord 3 0 5tt.nii.gz gm.nii.gz && fslmaths gm.nii.gz -thr 0.5 -bin gm_bin.nii.gz
[ ! -f csf.nii.gz ] && mrconvert -coord 3 3 5tt.nii.gz csf.nii.gz && fslmaths gm.nii.gz -thr 0.5 -bin csf_bin.nii.gz
[ ! -f wm.nii.gz ] && mrconvert --coord 3 2 5tt.nii.gz wm.nii.gz && fslmaths wm.nii.gz -thr 0.5 -bin wm_bin.nii.gz

for MEAS in ${measures}
do
	measure=$(eval "echo \$${MEAS}")
	for TYPES in ${types}
	do
		[ ! -f ./output/${MEAS}_${TYPES}.nii.gz ] && fslmaths ${measure} -mas ${TYPES}.nii.gz ./output/${MEAS}_${TYPES}.nii.gz
	done
done

if [ -f ./output/isovf_csf.nii.gz ]; then
	mkdir -p raw
	mv *.nii.gz ./raw/
	echo "complete"
	exit 0
else
	echo "something failed. check derivatives and logs"
	exit 1
fi
