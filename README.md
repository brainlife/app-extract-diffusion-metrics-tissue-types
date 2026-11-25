<h1 align="center">Extract summary measures within tissue types</h1>

<p align="center">
  A CSV of mean and standard deviation of diffusion, quantitative MRI and myelin measures in gray matter, white matter, CSF and the whole brain, from a 5-tissue-type mask.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.746"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.746-blue.svg" alt="Run on brainlife.io"></a>
  <a href="https://github.com/brainlife/app-extract-diffusion-metrics-tissue-types/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="MIT license"></a>
</p>

> 📍 **This branch, `output-csv-v1.0`, is the brainlife.io App Extract summary measures within tissue types** ([doi:10.25663/brainlife.app.746](https://doi.org/10.25663/brainlife.app.746)). The other Apps in this repository are listed under **Versions on brainlife.io** below.

This App summarises microstructure measures (DTI, DKI, NODDI, quantitative MRI and myelin maps) within tissue-type masks (gray matter, white matter, CSF). It is intended for a quick tissue-level analysis.

## 🧠 At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Computes the mean and standard deviation of diffusion (DTI, DKI, NODDI), quantitative MRI and myelin maps within gray matter, white matter, CSF and the whole brain defined by a 5-tissue-type mask, and outputs a CSV.**

Splits the 5-tissue-type image with MRtrix3 into gray matter, white matter and CSF maps binarised at 0.5, reslices each provided measure map to that grid with FreeSurfer mri_vol2vol (header-based, nearest neighbour), and writes per-tissue mean and SD of every measure to tissues.csv. Use it for a quick tissue-level summary of microstructure measures. Needs a 5-tissue-type mask and at least one of the tensor, NODDI, qMRI or myelin inputs, aligned to it. Note: in this branch the CSF mask is binarised from the gray matter map (convert.sh), so CSF values are not reliable.

| | |
|---|---|
| 📥 **Inputs** | `neuro/mask` · `neuro/tensor` · `neuro/noddi` (optional) · `neuro/anat/qmri` (optional) · `neuro/myelin-map` (optional) |
| 📤 **Outputs** | `neuro/parc-stats` · `raw` |
| 🐳 **Container** | `brainlife/mrtrix3:3.0.0` |
| ⚙️ **Resources** | 1 CPUs · 20 GB memory · 0.5 h walltime |
| 🔑 **Requires** | `FREESURFER_LICENSE` |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.746](https://doi.org/10.25663/brainlife.app.746) |

#### 📥 Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `mask` | `neuro/mask` (5tt_masks) | yes | 5-tissue-type segmentation (MRtrix3 5tt format) defining gray matter, white matter and CSF. |
| `tensor` | `neuro/tensor` | yes | Optional tensor/kurtosis maps (fa, md, rd, ad, ga, ak, mk, rk). |
| `noddi` | `neuro/noddi` | no | Optional NODDI maps (ndi, isovf, odi). |
| `qt1` | `neuro/anat/qmri` | no | Optional quantitative MRI maps (t1, r1, m0, pd, mtv, vip, sir, wf). |
| `myelin` | `neuro/myelin-map` | no | Optional myelin map. |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `parc-stats` | `neuro/parc-stats` | tissues.csv with mean and SD of each measure in gray_matter, white_matter, csf and wholebrain. |
| `raw` | `raw` | Intermediate tissue masks and resliced measure maps. |

<!-- brainlife-app:end -->

## 🏷️ Versions on brainlife.io

Each version is a separate App on brainlife.io, built from its own branch of this repository.

| Version | Output | Branch | Run it | Status |
|---|---|---|---|---|
| **Extract summary measures within tissue types** (this branch) | `neuro/parc-stats` CSV | [`output-csv-v1.0`](https://github.com/brainlife/app-extract-diffusion-metrics-tissue-types/tree/output-csv-v1.0) | [doi:10.25663/brainlife.app.746](https://doi.org/10.25663/brainlife.app.746) | current |
| Extract diffusion metrics inside tissue types | masked volumes (`raw`) | [`v1.0`](https://github.com/brainlife/app-extract-diffusion-metrics-tissue-types/tree/v1.0) | [doi:10.25663/brainlife.app.377](https://doi.org/10.25663/brainlife.app.377) | deprecated |

The deprecated `v1.0` App takes tensor (FA, MD, RD, AD) and NODDI (NDI, ODI, ISOVF) maps and writes each measure masked by each tissue type (for example `fa_wm.nii.gz`) instead of a table.

## 🚀 Running the App

### ☁️ On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.746](https://doi.org/10.25663/brainlife.app.746), choose a 5-tissue-type mask (`neuro/mask`, tag `5tt_masks`) and the measure datasets you want summarised (tensor, and optionally NODDI, quantitative MRI and a myelin map), aligned to the mask, then press **Execute**. The App archives a `neuro/parc-stats` dataset with the table and a `raw` dataset with the intermediate masks and resliced maps.

### 💻 Locally

You need [Singularity/Apptainer](https://apptainer.org/), [`jq`](https://jqlang.github.io/jq/) and a [FreeSurfer license](https://surfer.nmr.mgh.harvard.edu/registration.html). `main` uses the `brainlife/mrtrix3:3.0.0`, `brainlife/freesurfer:7.3.2` and `brainlife/dipy:1.4.1` containers.

1. Clone this repository and check out the registered version (`git checkout output-csv-v1.0`).
2. Create `config.json` with the mask and the measure maps you have. Measures whose file is missing are skipped. The subject ID written to the table is read from `_inputs[0].meta.subject`, which brainlife.io fills in:

   ```json
   {
       "mask": "input/mask/mask.nii.gz",
       "fa": "input/tensor/fa.nii.gz",
       "md": "input/tensor/md.nii.gz",
       "rd": "input/tensor/rd.nii.gz",
       "ad": "input/tensor/ad.nii.gz",
       "ndi": "input/noddi/ndi.nii.gz",
       "odi": "input/noddi/odi.nii.gz",
       "isovf": "input/noddi/isovf.nii.gz",
       "myelin": "input/myelin/map.nii.gz",
       "_inputs": [ { "meta": { "subject": "sub-01" } } ]
   }
   ```

   Other accepted keys: `ga`, `mk`, `ak`, `rk` (kurtosis) and `t1`, `r1`, `m0`, `pd`, `mtv`, `vip`, `sir`, `wf` (quantitative MRI).

3. Export your FreeSurfer license and run the App:

   ```bash
   export FREESURFER_LICENSE="$(cat ~/freesurfer/license.txt)"
   ./main
   ```

### 🔬 How it works

1. `convert.sh` (MRtrix3) splits the 5-tissue-type image into gray matter, white matter and CSF maps and binarises them at 0.5.
2. `move.sh` (FreeSurfer `mri_vol2vol`, header-based, nearest neighbour) reslices each measure map to the grid of the mask.
3. `build_dataframe.py` computes the mean and standard deviation of every measure in each tissue and in the whole brain (all non-zero voxels of the measure).

## 📦 Outputs

```text
parc-stats/parc-stats/
└── tissues.csv    subjectID, structureID (gray_matter, white_matter, csf, wholebrain), <measure>_mean, <measure>_sd
raw/               tissue masks and resliced measure maps (*.nii.gz)
```

## 🩺 Troubleshooting

- **`Please set FREESURFER_LICENSE in .bashrc`**: export your FreeSurfer license text in the `FREESURFER_LICENSE` environment variable before running `main`.
- **`something went wrong. check logs and derivatives`**: `tissues.csv` was not produced. Check the log and make sure the measure maps and the 5-tissue-type mask are aligned.
- **CSF values**: in the current code the CSF mask is binarised from the gray matter map (`convert.sh`), so the `csf` rows are not reliable.

## 📚 Citing

> [!TIP]
> If you use this App in your work, please cite the App, the software it builds on and brainlife.io (below). GitHub's **Cite this repository** button gives the App citation in APA and BibTeX.

- Woolrich MW, Jbabdi S, Patenaude B, Chappell M, Makni S, Behrens T, Beckmann C, Jenkinson M, Smith SM. Bayesian analysis of neuroimaging data in FSL. *NeuroImage* 45:S173–S186 (2009).
- Smith SM, Jenkinson M, Woolrich MW, Beckmann CF, Behrens TEJ, Johansen-Berg H, Bannister PR, De Luca M, Drobnjak I, Flitney DE, Niazy R, Saunders J, Vickers J, Zhang Y, De Stefano N, Brady JM, Matthews PM. Advances in functional and structural MR image analysis and implementation as FSL. *NeuroImage* 23(S1):208–219 (2004).
- Jenkinson M, Beckmann CF, Behrens TE, Woolrich MW, Smith SM. FSL. *NeuroImage* 62:782–790 (2012).
- Extract summary measures within tissue types. brainlife.io App. [doi:10.25663/brainlife.app.746](https://doi.org/10.25663/brainlife.app.746)
- Avesani P. et al. The open diffusion data derivatives. Sci Data 6, 69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)
- Woolrich M.W. et al. Bayesian analysis of neuroimaging data in FSL. NeuroImage 45:S173-86 (2009).
- Smith S.M. et al. Advances in functional and structural MR image analysis and implementation as FSL. NeuroImage 23(S1):208-19 (2004).
- Fischl. FreeSurfer. *NeuroImage* 62:774-781 (2012). [doi:10.1016/j.neuroimage.2012.01.021](https://doi.org/10.1016/j.neuroimage.2012.01.021)
- Jenkinson et al. FSL. *NeuroImage* 62:782-790 (2012). [doi:10.1016/j.neuroimage.2011.09.015](https://doi.org/10.1016/j.neuroimage.2011.09.015)
- Tournier et al. MRtrix3: A fast, flexible and open software framework for medical image processing and visualisation. *NeuroImage* 202:116137 (2019). [doi:10.1016/j.neuroimage.2019.116137](https://doi.org/10.1016/j.neuroimage.2019.116137)
- Zhang et al. NODDI: Practical in vivo neurite orientation dispersion and density imaging of the human brain. *NeuroImage* 61:1000-1016 (2012). [doi:10.1016/j.neuroimage.2012.03.072](https://doi.org/10.1016/j.neuroimage.2012.03.072)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)

## 👥 Authors

- Brad Caron

**Contributors:** Soichi Hayashi

## 💰 Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io is publicly funded, and acknowledging that support helps keep it running. This App was developed with support from Wellcome, the U.S. National Institutes of Health (including the BRAIN Initiative BRAIN CONNECTS program: The Axonal Projectome EXchange, U24NS140384, and the Center for Mesoscale Connectomics, UM1NS132207) and the U.S. National Science Foundation.</sub>

## ⚖️ License

MIT. Copyright (c) 2020 brainlife.io, The University of Texas at Austin and Indiana University.
