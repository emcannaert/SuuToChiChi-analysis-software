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

cmsRun <your cfg selection>.py  

The output files will be in this main src directory.   
