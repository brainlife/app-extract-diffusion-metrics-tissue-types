#!/bin/bash

# parse inputs
mask=`jq -r '.mask' config.json`
types="gm wm csf"

# convert mask into tissue type images
[ ! -f 5tt.nii.gz ] && mrconvert ${mask} 5tt.nii.gz
[ ! -f gm.nii.gz ] && mrconvert -coord 3 0 5tt.nii.gz gm.nii.gz && fslmaths gm.nii.gz -thr 0.5 -bin gm_bin.nii.gz
[ ! -f csf.nii.gz ] && mrconvert -coord 3 3 5tt.nii.gz csf.nii.gz && fslmaths gm.nii.gz -thr 0.5 -bin csf_bin.nii.gz
[ ! -f wm.nii.gz ] && mrconvert --coord 3 2 5tt.nii.gz wm.nii.gz && fslmaths wm.nii.gz -thr 0.5 -bin wm_bin.nii.gz

# final check
if [ -f 5tt.nii.gz ]; then
	echo "complete"
else
	echo "something failed. check derivatives and logs"
	exit 1
fi
