# SuuToChiChi-analysis-software


Code in the CMSSW software framework (EDAnalyzer, ROOT base) used for the fully hadronic diquark (Suu) to vector-like quark pair analysis on the CMS Experiment at CERN. This code is normally stored and run on the Fermilab LHC Physics Cluster (LPC). Code is written by Ethan Cannaert with some contributions from the UC Davis Boosted Event Shape Tagger (BEST) group for the neural network implementation.  

To run this, you must first have a valid installation of CMSSW, in particular CMSSW_10_6_30. From the lpc   

mkdir analysis   
scram p CMSSW_10_6_30  
cd CMSSW_10_6_30/src  
git clone https://github.com/emcannaert/SuuToChiChi-analysis-software.git  
scram b   
cmsenv  


To run the main analyzer, create the cfg files with   

python createCfgTemplate.py  

and run one with   

cmsRun (your cfg selection).py  

The output files will be in this main src directory.   


The full pipeline for the analysis looks like this - 

1.	create cfg files createCfgTemplate.py
2.	create crab cfg files createAltCrabCfg.py
3.	submit crab files
4.	get EOS paths to outputs, go to combinedROOT, feed in text file and run create_eos_copy_commands.py
5.	run eos_copy_commands.sh to copy EOS files to combinedROOT folder 
6.	change the file paths in combinedROOT/readTreeApplySelection.C to run over the samples, years, systematics you want
7.	run readTreeApplySelection.C to get the skimmed root files
8.	delete combined ROOT files
9.	copy skimmed ROOT files locally
10.	run readTreeMC.C, readTreeMCBR.C, or readTreeData.C to do final selection
11.	create plots from this with script of your choice (the files will be under rootFiles/processeRootFiles), or move on to bin merging
12.	run bin merging script
13.	run script to create final combine plots with these binnings
14.	run this output in Higgs Combine 
