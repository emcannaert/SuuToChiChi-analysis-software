#! /usr/bin/env python

import sys
import os
from datetime import datetime
import pickle
import numpy as np


def createCfg(sample,year,dataset,dateTimeString):
	newCrabCfg = open("crab/crab_CreateEfficiencyMapHists_%s_%s_cfg.py"%(sample,year),"w")
	newCrabCfg.write("from CRABClient.UserUtilities import config\n")
	newCrabCfg.write("config = config()\n")
	newCrabCfg.write("config.General.requestName = 'crab_CreateEfficiencyMapHists_%s_%s_001'\n"%(sample,year))
	newCrabCfg.write("config.General.workArea = 'crab_projects'\n")
	newCrabCfg.write("config.JobType.allowUndistributedCMSSW = True\n")
	newCrabCfg.write("config.JobType.pluginName = 'Analysis'\n")
	newCrabCfg.write("config.JobType.psetName = '../createHistsForEfficiencyMaps_%s_%s_cfg.py'\n"%(sample,year))
	newCrabCfg.write("config.Data.inputDataset = '%s'\n"%dataset.strip())
	newCrabCfg.write("config.Data.publication = False\n")

	if "QCD" in sample:
		newCrabCfg.write("config.JobType.maxMemoryMB = 3000 # might be necessary for some of the QCD jobs\n")
	newCrabCfg.write("config.Data.outLFNDirBase = '/store/user/ecannaer/bTaggingEffMaps_%s'\n"%dateTimeString)
	newCrabCfg.write("config.Data.splitting = 'FileBased'\n")
	if "TTTo" in sample or "TTJets" in sample:
		newCrabCfg.write("config.Data.unitsPerJob = 5\n")
	elif "ST_" in sample:
		newCrabCfg.write("config.Data.unitsPerJob = 10\n")
	else:
		newCrabCfg.write("config.Data.unitsPerJob = 1\n")
	newCrabCfg.write("config.Data.outputDatasetTag = 'CreateEfficiencyMapHists_%s_%s'\n"%(sample,year))

	newCrabCfg.write("config.Site.storageSite = 'T3_US_FNALLPC'\n")
	newCrabCfg.close()

def main():


	current_time = datetime.now()
	dateTimeString = "%s%s%s_%s%s%s"%(current_time.year,current_time.month,current_time.day,current_time.hour,current_time.minute,current_time.second )

	years   = ["2015","2016","2017","2018"]

	## load in signal dataset and signal sample
	signal_datasets_pkl = open('../../signal_datasets.pkl', 'r')    
	datasets_signal = pickle.load(signal_datasets_pkl)  # there are 433 files (so far), so the dictionary construction is automated and loaded here


	signal_samples_pkl = open('../../signal_samples.pkl', 'r')
	signal_samples     = pickle.load(signal_samples_pkl)
	signal_samples = np.array(signal_samples)

	datasets = {    '2015': { 'QCDMC1000to1500': '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'QCDMC1500to2000': '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'QCDMC2000toInf':  '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'QCDMC_Pt15to7000': '/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'TTToHadronicMC':  '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',  
							  'TTToSemiLeptonicMC': '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'TTToLeptonicMC': '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'TTJetsMCHT1200to2500': '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',
							  'TTJetsMCHT2500toInf': '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',
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
							  'QCDMC_Pt15to7000': '/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
							  'TTToHadronicMC':'/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',  
							  'TTToSemiLeptonicMC':'/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
							  'TTToLeptonicMC':'/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
							  'TTJetsMCHT1200to2500': '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',
							  'TTJetsMCHT2500toInf': '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',
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
								 'QCDMC_Pt15to7000':'/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',
								 'TTToHadronicMC':'/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',  
								 'TTToSemiLeptonicMC': '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM',
								 'TTToLeptonicMC':'/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM',
								 'TTJetsMCHT1200to2500': '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',
							  	 'TTJetsMCHT2500toInf': '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',
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
							  'QCDMC_Pt15to7000':'/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'TTToHadronicMC':'/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',  
							  'TTToSemiLeptonicMC':'/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'TTToLeptonicMC':'/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',
							  'TTJetsMCHT1200to2500': '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'TTJetsMCHT2500toInf': '/TTJets_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'ST_t-channel-top_inclMC':'/ST_t-channel_top_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',
							  'ST_t-channel-antitop_inclMC':'/ST_t-channel_antitop_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',
							  'ST_s-channel-hadronsMC':'/ST_s-channel_4f_hadronicDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'ST_s-channel-leptonsMC':'/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',
							  'ST_tW-antiTop_inclMC':'/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'ST_tW-top_inclMC':'/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'dataA': '/JetHT/Run2018A-UL2018_MiniAODv2_GT36-v1/MINIAOD',
							  'dataB': '/JetHT/Run2018B-UL2018_MiniAODv2_GT36-v1/MINIAOD',
							  'dataC': '/JetHT/Run2018C-UL2018_MiniAODv2_GT36-v1/MINIAOD',
							  'dataD': '/JetHT/Run2018D-UL2018_MiniAODv2_GT36-v1/MINIAOD'}   }

	for year in years:
		if year == "2015":
			samples = ["dataB-ver1","dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM" ,"dataF-HIPM","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","QCDMC_Pt15to7000","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf","TTToHadronicMC","TTToSemiLeptonicMC", "TTToLeptonicMC",
   "ST_t-channel-top_inclMC",
   "ST_t-channel-antitop_inclMC",
   "ST_s-channel-hadronsMC",
   "ST_s-channel-leptonsMC",
   "ST_tW-antiTop_inclMC",
   "ST_tW-top_inclMC"]
		elif year == "2016":
			samples = ["dataF","dataG","dataH","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf", "QCDMC_Pt15to7000","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf","TTToHadronicMC","TTToSemiLeptonicMC", "TTToLeptonicMC",
	"ST_t-channel-top_inclMC",
   "ST_t-channel-antitop_inclMC",
   "ST_s-channel-hadronsMC",
   "ST_s-channel-leptonsMC",
   "ST_tW-antiTop_inclMC",
   "ST_tW-top_inclMC" ]
		elif year == "2017":
			samples = ["dataB","dataC","dataD","dataE","dataF","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","QCDMC_Pt15to7000","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf","TTToHadronicMC","TTToSemiLeptonicMC", "TTToLeptonicMC",
   "ST_t-channel-top_inclMC",
   "ST_t-channel-antitop_inclMC",
   "ST_s-channel-hadronsMC",
   "ST_s-channel-leptonsMC",
   "ST_tW-antiTop_inclMC",
   "ST_tW-top_inclMC"]
		elif year == "2018":
			samples = ["dataA","dataB", "dataC", "dataD","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","QCDMC_Pt15to7000","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf","TTToHadronicMC","TTToSemiLeptonicMC", "TTToLeptonicMC",
   "ST_t-channel-top_inclMC",
   "ST_t-channel-antitop_inclMC",
   "ST_s-channel-hadronsMC",
   "ST_s-channel-leptonsMC",
   "ST_tW-antiTop_inclMC",
   "ST_tW-top_inclMC" ]

   		samples.extend(signal_samples)
		for iii, sample in enumerate(samples):
			if "data" in samples:
				continue
			if "Suu" in sample:   # don't yet have signal MC for this, and don't need to calculate these for data
				try:
					createCfg(sample, year, datasets_signal[year][sample],dateTimeString)
				except:
					print("Mass point failed: %s"%sample)
					continue
			else:
				createCfg(sample, year, datasets[year][sample],dateTimeString)
	return


if __name__ == "__main__":
	main()
