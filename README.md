# SuuToChiChi-analysis-software


Code in the CMSSW software framework (EDAnalyzer, ROOT base) used for the fully hadronic diquark (Suu) to vector-like quark pair analysis on the CMS Experiment at CERN. This code is normally stored and run on the Fermilab LHC Physics Cluster (LPC). Code is written by Ethan Cannaert with some contributions from the UC Davis Boosted Event Shape Tagger (BEST) group for the neural network implementation.  

To run this, you must first have a valid installation of CMSSW, in particular CMSSW_10_6_30. From the lpc   
```
mkdir analysis   
scram p CMSSW_10_6_30  
cd CMSSW_10_6_30/src  
git clone https://github.com/emcannaert/SuuToChiChi-analysis-software.git  
scram b   
cmsenv  
```

To run the main analyzer, create the cfg files with   
```
python createCfgTemplate.py  
```

and run one with   
```
cmsRun <your cfg selection>.py  
```
The output files will be in this main src directory.   


The full pipeline for the analysis looks like this - 

1.	create cfg files createCfgTemplate.py
2.	create crab cfg files createAltCrabCfg.py
3.	submit crab files
4.	run ``` combinedROOT/merge_eos_files.sh <eos output folder> ``` to merge crab N-tuples and save them to EOS 
5.	run ``` combinedROOT/readTreeApplySelection.C ```  to get output root files that have been skimmed by the analysis initial selection 
6.	run ``` combinedROOT readTree.C ``` to create histograms for the statistical analysis
7.	copy processed histograms locally
8.	(Locally) get stat-uncertainty-optimized bin maps for 2D histograms by running calculateStatisticalUncertaintyBins.py
9.	(Locally) linearize 2D histograms with linearize_final_plots.py
10.	copy linearized plots to combine workspace

The combine workspace constituting the individual RooFit workspaces and Combine data cards is saved at https://gitlab.cern.ch/ecannaer/suutochichi_combine . 
