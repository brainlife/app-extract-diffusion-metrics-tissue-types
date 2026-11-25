[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-brainlife.app.377-blue.svg)](https://doi.org/10.25663/brainlife.app.377)

# Extract diffusion metrics inside tissue types

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

**Computes the mean and standard deviation of diffusion (DTI, DKI, NODDI), quantitative MRI and myelin maps within gray matter, white matter, CSF and the whole brain defined by a 5-tissue-type mask, and outputs a CSV.**

Splits the 5-tissue-type image with MRtrix3 into gray matter, white matter and CSF maps binarised at 0.5, reslices each provided measure map to that grid with FreeSurfer mri_vol2vol (header-based, nearest neighbour), and writes per-tissue mean and SD of every measure to tissues.csv. Use it for a quick tissue-level summary of microstructure measures. Needs a 5-tissue-type mask and at least one of the tensor, NODDI, qMRI or myelin inputs, aligned to it. Note: in this branch the CSF mask is binarised from the gray matter map (convert.sh), so CSF values are not reliable.

Run it on brainlife.io: [https://doi.org/10.25663/brainlife.app.746](https://doi.org/10.25663/brainlife.app.746)

| Input | Datatype | Required | Description |
|---|---|---|---|
| `mask` | `neuro/mask` (5tt_masks) | yes | 5-tissue-type segmentation (MRtrix3 5tt format) defining gray matter, white matter and CSF. |
| `tensor` | `neuro/tensor` | yes | Optional tensor/kurtosis maps (fa, md, rd, ad, ga, ak, mk, rk). |
| `noddi` | `neuro/noddi` | no | Optional NODDI maps (ndi, isovf, odi). |
| `qt1` | `neuro/anat/qmri` | no | Optional quantitative MRI maps (t1, r1, m0, pd, mtv, vip, sir, wf). |
| `myelin` | `neuro/myelin-map` | no | Optional myelin map. |

| Output | Datatype | Description |
|---|---|---|
| `parc-stats` | `neuro/parc-stats` | tissues.csv with mean and SD of each measure in gray_matter, white_matter, csf and wholebrain. |
| `raw` | `raw` | Intermediate tissue masks and resliced measure maps. |

Runtime: container `brainlife/mrtrix3:3.0.0`; 1 CPUs; 20 GB memory; 0.5 h walltime; needs `FREESURFER_LICENSE`.

Please cite:
- Avesani P. et al. The open diffusion data derivatives. Sci Data 6, 69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)
- Woolrich M.W. et al. Bayesian analysis of neuroimaging data in FSL. NeuroImage 45:S173-86 (2009).
- Smith S.M. et al. Advances in functional and structural MR image analysis and implementation as FSL. NeuroImage 23(S1):208-19 (2004).

<!-- brainlife-app:end -->

This app will extract diffusion metrics mapped from the DTI and/or NODDI model within tissue type masks (i.e. csf, gm, wm). This app uses FSL and is intended to be used for a quick and dirty analysis of tissue type metrics.

### Authors

- Brad Caron (bacaron@utexas.edu) 

### Contributors

- Soichi Hayashi (shayashi@iu.edu)

### Funding Acknowledgement

brainlife.io is publicly funded and for the sustainability of the project it is helpful to Acknowledge the use of the platform. We kindly ask that you acknowledge the funding below in your publications and code reusing this code.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)

### Citations

We kindly ask that you cite the following articles when publishing papers and code using this code.

1. Avesani, P., McPherson, B., Hayashi, S. et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. Sci Data 6, 69 (2019). https://doi.org/10.1038/s41597-019-0073-y

2. M.W. Woolrich, S. Jbabdi, B. Patenaude, M. Chappell, S. Makni, T. Behrens, C. Beckmann, M. Jenkinson, S.M. Smith. Bayesian analysis of neuroimaging data in FSL. NeuroImage, 45:S173-86, 2009

3. S.M. Smith, M. Jenkinson, M.W. Woolrich, C.F. Beckmann, T.E.J. Behrens, H. Johansen-Berg, P.R. Bannister, M. De Luca, I. Drobnjak, D.E. Flitney, R. Niazy, J. Saunders, J. Vickers, Y. Zhang, N. De Stefano, J.M. Brady, and P.M. Matthews. Advances in functional and structural MR image analysis and implementation as FSL. NeuroImage, 23(S1):208-19, 2004

4. M. Jenkinson, C.F. Beckmann, T.E. Behrens, M.W. Woolrich, S.M. Smith. FSL. NeuroImage, 62:782-90, 2012

#### MIT Copyright (c) 2020 brainlife.io The University of Texas at Austin and Indiana University

## Running the App

### On Brainlife.io

You can submit this App online at [https://doi.org/10.25663/brainlife.app.377](https://doi.org/10.25663/brainlife.app.377) via the 'Execute' tab.

### Running Locally (on your machine)

1. git clone this repo

2. Inside the cloned directory, create `config.json` with something like the following content with paths to your input files.

```json
{
    "fa": "/input/tensor/fa.nii.gz",
    "md": "/input/tensor/md.nii.gz",
    "rd": "/input/tensor/rd.nii.gz",
    "ad": "/input/tensor/ad.nii.gz",
    "cl": "/input/tensor/cl.nii.gz",
    "cp": "/input/tensor/cp.nii.gz",
    "cs": "/input/tensor/cs.nii.gz",
    "tensors": "/input/tensor/tensors.nii.gz",
    "kurtosis": "/input/tensor/kurtosis.nii.gz",
    "dir": "/input/noddi/dir.nii.gz",
    "ndi": "/input/noddi/ndi.nii.gz",
    "isovf": "/input/noddi/isovf.nii.gz",
    "odi": "/input/noddi/odi.nii.gz",
    "mask": "/input/mask/mask.nii.gz"
}
```

### Sample Datasets

You can download sample datasets from Brainlife using [Brainlife CLI](https://github.com/brain-life/cli).

```
npm install -g brainlife
bl login
mkdir input
bl dataset download
```

3. Launch the App by executing 'main'

```bash
./main
```

## Output

The main output of this App is a raw datatype containing the volume files for each measure mapped within each tissue type, and a derivatives directory containing all of the derivatives generated from this app run

#### Product.json

The secondary output of this app is `product.json`. This file allows web interfaces, DB and API calls on the results of the processing.

### Dependencies

This App only requires [singularity](https://www.sylabs.io/singularity/) to run. If you don't have singularity, you will need to install following dependencies.   

- FSL: https://fsl.fmrib.ox.ac.uk/fsl/fslwiki

#### MIT Copyright (c) 2020 brainlife.io The University of Texas at Austin and Indiana University
