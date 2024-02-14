#! /usr/bin/env python

import sys
import os
from datetime import datetime
import pickle
import numpy as np
### this can be updated to create the different cfgs for each systematic
def makeAltCrabCfg(sample, year, systematic, dataset,dateTimeString):

	file_base = ""
	path_backtrack = ""
	extra_cfg_folderr = ""
	if "Suu" in sample:
		file_base = "signalCfgs/"
		path_backtrack = "../"
	if systematic == "":
		newCfg = open("allAltCrabCfgs/%scrab_clusteringAnalyzer_%s_%s_%scfg.py"%(file_base,sample,year, systematic),"w")
	else:
		newCfg = open("allAltCrabCfgs/%scrab_clusteringAnalyzer_%s_%s_%s_cfg.py"%(file_base,sample,year, systematic),"w")
   
	newCfg.write("from CRABClient.UserUtilities import config\n")
	newCfg.write("config = config()\n")
	newCfg.write("config.General.requestName = 'clustAlg_%s_%s_%s_AltDatasets_000'\n"%(sample,year,systematic))
	newCfg.write("config.General.workArea = 'crab_projects'\n")
	newCfg.write("config.General.transferOutputs = True\n")
	newCfg.write("config.JobType.allowUndistributedCMSSW = True\n")
	newCfg.write("config.JobType.pluginName = 'Analysis'\n")
	if systematic == "": 
		newCfg.write("config.JobType.psetName = '%s../allCfgs/%sclusteringAnalyzer_%s_%s_%scfg.py'\n"%(path_backtrack, file_base,sample,year, systematic))
	else:
		newCfg.write("config.JobType.psetName = '%s../allCfgs/%sclusteringAnalyzer_%s_%s_%s_cfg.py'\n"%(path_backtrack, file_base,sample,year, systematic))

	newCfg.write("config.Data.inputDataset = '%s'\n"%dataset.strip())
	newCfg.write("config.Data.publication = False\n")
	#if "data" in sample:
		#newCfg.write("config.Data.splitting = 'Automatic'\n")
	#else:
	newCfg.write("config.Data.splitting = 'FileBased'\n")
	if "TTTo" in sample:
		newCfg.write("config.Data.unitsPerJob = 10\n")
	elif "ST_" in sample:
		newCfg.write("config.Data.unitsPerJob = 10\n")
	else:
		newCfg.write("config.Data.unitsPerJob = 1\n")
	if "QCD" in sample:
		newCfg.write("config.JobType.maxMemoryMB = 2500 # might be necessary for some of the QCD jobs\n")
	if "data" in sample:
		newCfg.write("config.JobType.maxMemoryMB = 3000 # might be necessary for some of the QCD jobs\n")
	#### lumimask info: https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2#2018
	if "data" in sample:
		if year=="2015":
			newCfg.write("config.Data.lumiMask = '../lumimasks/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'\n")
		elif year=="2016":
			newCfg.write("config.Data.lumiMask = '../lumimasks/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'\n")
		elif year=="2017":
			newCfg.write("config.Data.lumiMask = '../lumimasks/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'\n")
		elif year=="2018":
			newCfg.write("config.Data.lumiMask = '../lumimasks/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'\n")

	newCfg.write("config.Data.outputDatasetTag = 'clustAlg_%s_%s_%s'\n"%(sample,year,systematic))
	newCfg.write("config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_%s'\n"%dateTimeString)
	newCfg.write("config.Site.storageSite = 'T3_US_FNALLPC'\n")




def main():



	lastCrabSubmission = open("lastCrabSubmission.txt", "a")

	current_time = datetime.now()
	dateTimeString = "%s%s%s_%s%s%s"%(current_time.year,current_time.month,current_time.day,current_time.hour,current_time.minute,current_time.second )
	lastCrabSubmission.write("/store/user/ecannaer/SuuToChiChi_AltDatasets_%s\n"%dateTimeString)
	years   = ["2015","2016","2017","2018"]

	systematics = ["JEC", "JER",



   ""]  # last one here is for the fully nominal cfg file
	datasets = {    '2015': { 'QCDMC1000to1500': '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'QCDMC1500to2000': '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'QCDMC2000toInf':  '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'TTToHadronicMC':  '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',  
							  'TTToSemiLeptonicMC': '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'TTToLeptonicMC': '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'ST_t-channel-top_inclMC':'/ST_t-channel_top_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'ST_t-channel-antitop_inclMC':'/ST_t-channel_antitop_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'ST_s-channel-hadronsMC':'/ST_s-channel_4f_hadronicDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',
							  'ST_s-channel-leptonsMC':'/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'ST_tW-antiTop_inclMC':'/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'ST_tW-top_inclMC':'/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'dataB-ver1': '/JetHT/Run2016B-ver1_HIPM_UL2016_MiniAODv2-v2/MINIAOD',
							  'dataB-ver2': '/JetHT/Run2016B-ver2_HIPM_UL2016_MiniAODv2-v2/MINIAOD',
							  'dataC-HIPM': '/JetHT/Run2016C-HIPM_UL2016_MiniAODv2-v2/MINIAOD',
							  'dataD-HIPM': '/JetHT/Run2016D-HIPM_UL2016_MiniAODv2-v2/MINIAOD',
							  'dataE-HIPM': '/JetHT/Run2016E-HIPM_UL2016_MiniAODv2-v2/MINIAOD',
								  'dataF-HIPM': '/JetHT/Run2016F-HIPM_UL2016_MiniAODv2-v2/MINIAOD'},
					'2016': { 'QCDMC1000to1500': '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
							  'QCDMC1500to2000': '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
							  'QCDMC2000toInf':  '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
							  'TTToHadronicMC':'/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',  
							  'TTToSemiLeptonicMC':'/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
							  'TTToLeptonicMC':'/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
							  'ST_t-channel-top_inclMC':'/ST_t-channel_top_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
							  'ST_t-channel-antitop_inclMC':'/ST_t-channel_antitop_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
							  'ST_s-channel-hadronsMC':'/ST_s-channel_4f_hadronicDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',
							  'ST_s-channel-leptonsMC':'/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
							  'ST_tW-antiTop_inclMC':'/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',
							  'ST_tW-top_inclMC':'/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',
							  'dataF': '/JetHT/Run2016F-UL2016_MiniAODv2-v2/MINIAOD',
							  'dataG': '/JetHT/Run2016G-UL2016_MiniAODv2-v2/MINIAOD',
							  'dataH': '/JetHT/Run2016H-UL2016_MiniAODv2-v2/MINIAOD'},

					   '2017': { 'QCDMC1000to1500': '/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',
								 'QCDMC1500to2000': '/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',
								 'QCDMC2000toInf':  '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',
								 'TTToHadronicMC':'/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',  
								 'TTToSemiLeptonicMC': '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM',
								 'TTToLeptonicMC':'/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM',
								  'ST_t-channel-top_inclMC':'/ST_t-channel_top_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM',
								  'ST_t-channel-antitop_inclMC':'/ST_t-channel_antitop_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',
								  'ST_s-channel-hadronsMC':'/ST_s-channel_4f_hadronicDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',
								  'ST_s-channel-leptonsMC':'/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM',
								  'ST_tW-antiTop_inclMC':'/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',
								  'ST_tW-top_inclMC':'/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',
								 'dataB': '/JetHT/Run2017B-UL2017_MiniAODv2-v1/MINIAOD',
								 'dataC': '/JetHT/Run2017C-UL2017_MiniAODv2-v1/MINIAOD',
								 'dataD': '/JetHT/Run2017D-UL2017_MiniAODv2-v1/MINIAOD',
								 'dataE': '/JetHT/Run2017E-UL2017_MiniAODv2-v1/MINIAOD',
								 'dataF': '/JetHT/Run2017F-UL2017_MiniAODv2-v1/MINIAOD'},
					'2018': { 'QCDMC1000to1500': '/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'QCDMC1500to2000': '/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'QCDMC2000toInf':  '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'TTToHadronicMC':'/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',  
							  'TTToSemiLeptonicMC':'/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'TTToLeptonicMC':'/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',
							  'ST_t-channel-top_inclMC':'/ST_t-channel_top_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',
							  'ST_t-channel-antitop_inclMC':'/ST_t-channel_antitop_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',
							  'ST_s-channel-hadronsMC':'/ST_s-channel_4f_hadronicDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'ST_s-channel-leptonsMC':'/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',
							  'ST_tW-antiTop_inclMC':'/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'ST_tW-top_inclMC':'/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'dataA': '/JetHT/Run2018A-UL2018_MiniAODv2_GT36-v1/MINIAOD',
							  'dataB': '/JetHT/Run2018B-UL2018_MiniAODv2_GT36-v1/MINIAOD',
							  'dataC': '/JetHT/Run2018C-UL2018_MiniAODv2_GT36-v1/MINIAOD',
							  'dataD': '/JetHT/Run2018D-UL2018_MiniAODv2_GT36-v1/MINIAOD'}

   }

	signal_datasets_pkl = open('signal_datasets.pkl', 'r')    
	datasets_signal = pickle.load(signal_datasets_pkl)  # there are 433 files (so far), so the dictionary construction is automated and loaded here


  	signal_samples_pkl = open('signal_samples.pkl', 'r')
  	signal_samples     = pickle.load(signal_samples_pkl)
	signal_samples = np.array(signal_samples)

  	num_files_created = 0
	for year in years:
		if year == "2015":
			samples = ["dataB-ver1","dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM" ,"dataF-HIPM","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTToHadronicMC", "TTToSemiLeptonicMC", "TTToLeptonicMC",
   
   "ST_t-channel-top_inclMC",
   "ST_t-channel-antitop_inclMC",
   "ST_s-channel-hadronsMC",
   "ST_s-channel-leptonsMC",
   "ST_tW-antiTop_inclMC",
   "ST_tW-top_inclMC"]
		elif year == "2016":
			samples = ["dataF","dataG","dataH","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTToHadronicMC","TTToSemiLeptonicMC","TTToLeptonicMC",
   "ST_t-channel-top_inclMC",
   "ST_t-channel-antitop_inclMC",
   "ST_s-channel-hadronsMC",
   "ST_s-channel-leptonsMC",
   "ST_tW-antiTop_inclMC",
   "ST_tW-top_inclMC"]
		elif year == "2017":
			samples = ["dataB","dataC","dataD","dataE","dataF","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTToHadronicMC","TTToSemiLeptonicMC","TTToLeptonicMC",
   "ST_t-channel-top_inclMC",
   "ST_t-channel-antitop_inclMC",
   "ST_s-channel-hadronsMC",
   "ST_s-channel-leptonsMC",
   "ST_tW-antiTop_inclMC",
   "ST_tW-top_inclMC" ]
		elif year == "2018":
			samples = ["dataA","dataB", "dataC", "dataD","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTToHadronicMC","TTToSemiLeptonicMC","TTToLeptonicMC",
   "ST_t-channel-top_inclMC",
   "ST_t-channel-antitop_inclMC",
   "ST_s-channel-hadronsMC",
   "ST_s-channel-leptonsMC",
   "ST_tW-antiTop_inclMC",
   "ST_tW-top_inclMC" ]
   		samples.extend(signal_samples)
		for iii, sample in enumerate(samples):
			for systematic in systematics:
				num_files_created+=1
				if "Suu" in sample:
					try:
						makeAltCrabCfg(sample, year, "", datasets_signal[year][sample],dateTimeString)   # need a different dataset for signal mass points, only make a single signal cfg file to
					except:
						print("Failed for sample %s."%sample)
				else:
					makeAltCrabCfg(sample, year, systematic, datasets[year][sample],dateTimeString)   
	print("Created %i cfg files."%num_files_created)
	return

if __name__ == "__main__":
	main()