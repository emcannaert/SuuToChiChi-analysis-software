# 
SuuToChiChi-analysis-software: A CMS Analysis searching for the Diquark (Suu) → Vector-Like Quarks (χχ) → All-Hadronic Final State

This repository contains the full workflow for a CMS search for a diquark (**Suu**) decaying to vector-like quarks (**χ**) in the all-hadronic final state.  
It is organized as a CMSSW package under `${CMSSW_BASE}/src`.

---

## Directory Layout
CMSSW_BASE/src/
|-- selectionStudier/     # Utilities for initial selection cut optimization studies
|-- AN_data/              # Supplementary correction, model, etc. data
|-- postprocess/          # Post TTree-to-Histogram plotting and processing utilities
|-- package/              # Headers and src EDAnalyzer files (NTuplizer code)
|-- data/                 # Main correction, model, etc. data
|-- templates/            # Python cmsRun and crab cfg templates
|-- allAltCrabCfgs/       # Storage for crab cfg templates (signal cfgs in signal/ folder)
|-- allCfgs/              # Storage for cmsRun cfg templates (signal cfgs in signal/ folder)
|-- btagging/             # B-tagging study utilities
`-- combinedROOT/         # Scripts/utilities for processing NTuples into histograms for the stat analysis

---

## Main Analysis Workflow

The analysis proceeds through the following key scripts/utilities (in execution order):

1. **NTuple Production**
   - `package/src/clusteringAlgorithmAll.cc`  
     Main NTuplizer EDAnalyzer producing ROOT NTuples.
   - `templates/createCfgTemplate.py`  
     Generates cmsRun cfg templates for the NTuplizer.
   - `templates/createAltCrabTemplate_Cfg.py`  
     Generates crab cfg templates for large-scale NTuplizer submission.

2. **NTuple Merging and Skimming**
   - `combinedROOT/utils/merge_eos_files.sh`  
     Merge EOS crab output files.  
     **Usage:**  
     ```
     source merge_eos_files.sh <EOS_folder_with_crab_files> <era>
     ```  
     Merged files are stored in  
     ```
     /store/user/ecannaer/combinedROOT
     ```
   - `combinedROOT/rootSkimmer.C`  
     Applies initial selection cuts to merged files and saves skimmed outputs in  
     ```
     /store/user/ecannaer/skimmedFiles
     ```

3. **Histogram Production**
   - `combinedROOT/rootProcessor.C`  
     Processes skimmed files to produce histograms for all samples, eras, and systematic variations.  
     Output histograms are stored in  
     ```
     /store/user/ecannaer/processedFiles
     ```

4. **Post-Processing**
   - `postprocess/calculateStatisticalUncertaintyBins.py`  
     Creates **TH2F→TH1F bin maps** that guarantee a target fractional statistical uncertainty per bin.  
     Maps are stored in  
     ```
     postprocess/binMaps/
     ```
   - `postprocess/master_linearizer.py`  
     Applies the bin maps to produce linearized TH1F histograms.  
     Output ROOT files are stored in  
     ```
     postprocess/finalCombineFilesNewStats/
     ```  
     Each file contains histograms saved as  
     ```
     <region>/<sample>_<uncertainty+variation>
     ```  
     **Usage:**  
     ```
     python master_linearizer.py <year=2015,2016,2017,2018,ALL>
     ```
   - `postprocess/fix_asymmetric_uncerts.py`  
     Corrects noisy or one-sided template variations in the linearized histograms.  
     Corrected outputs are stored in  
     ```
     postprocess/finalCombineFilesNewStats/<QCD type>/correctedFinalCombineFiles/
     ```  
     These corrected ROOT files are the **direct inputs** to the statistical analysis.

---

## Combine Analysis

The final corrected ROOT files produced by `fix_asymmetric_uncerts.py` are the inputs to the Combine framework.  
The corresponding Combine repository is hosted here: [suutochichi_combine](https://gitlab.cern.ch/ecannaer/suutochichi_combine)

---

## Quick Start

1. Set up your CMSSW release and environment:
```
cmsrel CMSSW_10_6_30
cd CMSSW_10_6_30/src
cmsenv
```
2. Clone this repository into `src/` and build:
```
git clone https://github.com/emcannaert/SuuToChiChi-analysis-software.git
scram b
```
3. Follow the workflow above to produce NTuples, histograms, and final combine files.