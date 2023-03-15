#!/bin/bash

# tissue type mask
mask=`jq -r '.mask' config.json`

# tensor
ad=`jq -r '.ad' config.json` #ad
fa=`jq -r '.fa' config.json` #fa
md=`jq -r '.md' config.json` #md
rd=`jq -r '.rd' config.json` #rd

# dki
ga=`jq -r '.ga' config.json` #ga
mk=`jq -r '.mk' config.json` #mk
ak=`jq -r '.ak' config.json` #ak
rk=`jq -r '.rk' config.json` #rk

# noddi
ndi=`jq -r '.ndi' config.json` #ndi
odi=`jq -r '.odi' config.json` #odi
isovf=`jq -r '.isovf' config.json` #isovf

# qt1
t1=`jq -r '.t1' config.json` #t1
r1=`jq -r '.r1' config.json` #r1
m0=`jq -r '.m0' config.json` #m0
pd=`jq -r '.pd' config.json` #pd
mtv=`jq -r '.mtv' config.json` #mtv
vip=`jq -r '.vip' config.json` #vip
sir=`jq -r '.sir' config.json` #sir
wf=`jq -r '.wf' config.json` #wf

# myelin
myelin=`jq -r '.myelin' config.json` #myelin

# measures to loop through
measures="ad fa md rd ga mk ak rk ndi odi isovf t1 r1 m0 pd mtv vip sir wf myelin"

for meas in $measures
do
	measure=$(eval "echo \${meas}")
	if [ -f ${measure} ]; then
		mri_vol2vol --mov ${measure} --targ 