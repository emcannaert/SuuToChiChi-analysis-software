#! /usr/bin/env python

import sys
import os
from datetime import datetime
import pickle
import numpy as np
### this can be updated to create the different cfgs for each systematic
do_sideband = False
sideband_str = ""
if do_sideband: sideband_str = "_sideband"


jec_file_AK4 = { '2015': { 'BR': 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
					   "signal": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
				   'dataB-ver1': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
				   'dataB-ver2': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
				   'dataC-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
				   'dataD-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
				   'dataE-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunEF_V7_DATA_Uncertainty_AK4PFchs.txt',
				   'dataF-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunEF_V7_DATA_Uncertainty_AK4PFchs.txt'
				   },
		'2016': { 'BR': 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
				   'dataF': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK4PFchs.txt',
				   'dataG': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK4PFchs.txt',
				   'dataH': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK4PFchs.txt',
					"signal": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt'},

		'2017': {  'BR':	'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
	 			   "signal": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
				   'dataB': 'data/JEC/2017_UL/data/Summer19UL17_RunB_V5_DATA_Uncertainty_AK4PFchs.txt',
				   'dataC': 'data/JEC/2017_UL/data/Summer19UL17_RunC_V5_DATA_Uncertainty_AK4PFchs.txt',
				   'dataD': 'data/JEC/2017_UL/data/Summer19UL17_RunD_V5_DATA_Uncertainty_AK4PFchs.txt',
				   'dataE': 'data/JEC/2017_UL/data/Summer19UL17_RunE_V5_DATA_Uncertainty_AK4PFchs.txt',
				   'dataF': 'data/JEC/2017_UL/data/Summer19UL17_RunF_V5_DATA_Uncertainty_AK4PFchs.txt',
				
				 },
		'2018': { 'BR': 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
				   'dataA': 'data/JEC/2018_UL/data/Summer19UL18_RunA_V5_DATA_Uncertainty_AK4PFPuppi.txt',
				   'dataB': 'data/JEC/2018_UL/data/Summer19UL18_RunB_V5_DATA_Uncertainty_AK4PFchs.txt',
				   'dataC': 'data/JEC/2018_UL/data/Summer19UL18_RunC_V5_DATA_Uncertainty_AK4PFchs.txt',
				   'dataD': 'data/JEC/2018_UL/data/Summer19UL18_RunD_V5_DATA_Uncertainty_AK4PFchs.txt',
					"signal": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
					}}

jec_file_AK8 = { '2015': { 'BR': 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
					"signal":   'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
				   'dataB-ver1': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK8PFPuppi.txt',
				   'dataB-ver2': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK8PFPuppi.txt',
				   'dataC-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK8PFPuppi.txt',
				   'dataD-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK8PFPuppi.txt',
				   'dataE-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunEF_V7_DATA_Uncertainty_AK8PFPuppi.txt',
				   'dataF-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunEF_V7_DATA_Uncertainty_AK8PFPuppi.txt',},


				'2016': { 'BR':	'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
				   "signal": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
				   'dataF': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK8PFPuppi.txt',
				   'dataG': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK8PFPuppi.txt',
				   'dataH': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK8PFPuppi.txt',},

				'2017': { 'BR':	'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
	 					"signal": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
					   'dataB': 'data/JEC/2017_UL/data/Summer19UL17_RunB_V5_DATA_Uncertainty_AK8PFPuppi.txt',
					   'dataC': 'data/JEC/2017_UL/data/Summer19UL17_RunC_V5_DATA_Uncertainty_AK8PFPuppi.txt',
					   'dataD': 'data/JEC/2017_UL/data/Summer19UL17_RunD_V5_DATA_Uncertainty_AK8PFPuppi.txt',
					   'dataE': 'data/JEC/2017_UL/data/Summer19UL17_RunE_V5_DATA_Uncertainty_AK8PFPuppi.txt',
					   'dataF': 'data/JEC/2017_UL/data/Summer19UL17_RunF_V5_DATA_Uncertainty_AK8PFPuppi.txt',},
				'2018': { 'BR':	'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
	 					"signal": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
					   'dataA': 'data/JEC/2018_UL/data/Summer19UL18_RunA_V5_DATA_Uncertainty_AK8PFPuppi.txt',
					   'dataB': 'data/JEC/2018_UL/data/Summer19UL18_RunB_V5_DATA_Uncertainty_AK8PFPuppi.txt',
					   'dataC': 'data/JEC/2018_UL/data/Summer19UL18_RunC_V5_DATA_Uncertainty_AK8PFPuppi.txt',
					   'dataD': 'data/JEC/2018_UL/data/Summer19UL18_RunD_V5_DATA_Uncertainty_AK8PFPuppi.txt',
				 }}



def makeAltCrabCfg(sample, year, systematic, dataset,dateTimeString,useOptimalWP):

	if do_sideband: print("WARNING: RUNNING SIDEBAND REGION.")

	## SKIP DOING JEC FOR TTTo datasets (COULD WANT TO CHANGE THIS SOME DAY)
	#if "TTTo" in sample and "JEC" in systematic: return
	if "Suu" in sample and "JEC2" in systematic: return

	WP_str = ""
	if useOptimalWP: WP_str = "OptWP_"


	file_base = ""
	path_backtrack = ""
	extra_cfg_folderr = ""
	if "Suu" in sample:
		file_base = "signalCfgs/"
		path_backtrack = "../"
	if systematic == "nom":
		newCfg = open("../allAltCrabCfgs/%scrab_clusteringAnalyzer_%s_%s_cfg.py"%(file_base,sample,year),"w")
	else:
		newCfg = open("../allAltCrabCfgs/%scrab_clusteringAnalyzer_%s_%s_%s_cfg.py"%(file_base,sample,year, systematic),"w")
   
	newCfg.write("from CRABClient.UserUtilities import config\n")
	newCfg.write("config = config()\n")
	newCfg.write("config.General.requestName = 'clustAlg_%s_%s_%s_AltDatasets_000'\n"%(sample,year,systematic))
	newCfg.write("config.General.workArea = 'crab_projects%s'\n"%(sideband_str))
	newCfg.write("config.General.transferOutputs = True\n")
	newCfg.write("config.JobType.allowUndistributedCMSSW = True\n")
	newCfg.write("config.JobType.pluginName = 'Analysis'\n")
	if systematic == "nom": 
		newCfg.write("config.JobType.psetName = '%s../allCfgs/%sclusteringAnalyzer_%s_%s_cfg.py'\n"%(path_backtrack, file_base,sample,year))
	else:
		newCfg.write("config.JobType.psetName = '%s../allCfgs/%sclusteringAnalyzer_%s_%s_%s_cfg.py'\n"%(path_backtrack, file_base,sample,year, systematic))

	newCfg.write("config.Data.inputDataset = '%s'\n"%dataset.strip())
	newCfg.write("config.Data.publication = False\n")
	if "data" in sample:
		newCfg.write("config.Data.splitting = 'Automatic'\n")
	else:
		newCfg.write("config.Data.splitting = 'FileBased'\n")
		if "TTTo" in sample or "TTJets" in sample:
			newCfg.write("config.Data.unitsPerJob = 5\n")
		elif "ST_" in sample:
			newCfg.write("config.Data.unitsPerJob = 5\n")
		elif "WJets_" in sample:
			newCfg.write("config.Data.unitsPerJob = 10\n")
		elif "WW" in sample or "ZZ" in sample:
			newCfg.write("config.Data.unitsPerJob = 10\n")
		else:
			newCfg.write("config.Data.unitsPerJob = 1\n")

	if "Suu" in sample:
		if "JEC" in systematic : newCfg.write("config.JobType.maxMemoryMB = 5000 \n")
		else:	newCfg.write("config.JobType.maxMemoryMB = 4000 \n")

	elif "QCD" in sample:
		if "JEC" in systematic: 
			if "2000toInf" in sample:   newCfg.write("config.JobType.maxMemoryMB = 3500 \n")
			elif "1500to2000" in sample:   newCfg.write("config.JobType.maxMemoryMB = 3250 \n")
			elif "1000to1500" in sample:   newCfg.write("config.JobType.maxMemoryMB = 3000 \n")
			else: newCfg.write("config.JobType.maxMemoryMB = 3000 \n")
		elif systematic == "JER": newCfg.write("config.JobType.maxMemoryMB = 2500 \n")
		else: newCfg.write("config.JobType.maxMemoryMB = 2000 \n")
	elif "TTJets" in sample or "TTTo" in sample:
		if "JEC" in systematic: 
			if "800to1200" in sample: newCfg.write("config.JobType.maxMemoryMB = 3500 \n")
			elif "1200to2500" in sample: newCfg.write("config.JobType.maxMemoryMB = 3500 \n")
			elif "2500toInf" in sample: newCfg.write("config.JobType.maxMemoryMB = 3500 \n")
		elif systematic == "JER": newCfg.write("config.JobType.maxMemoryMB = 2500 \n")
		else: newCfg.write("config.JobType.maxMemoryMB = 2000 \n")
	elif "ST" in sample:
		if "JEC" in systematic: newCfg.write("config.JobType.maxMemoryMB = 3500 \n")
		else: newCfg.write("config.JobType.maxMemoryMB = 2000 \n")
	elif "WJets" in sample:
		if "JEC" in systematic: newCfg.write("config.JobType.maxMemoryMB = 3500 \n")
		if "JER" in systematic: newCfg.write("config.JobType.maxMemoryMB = 2500 \n")
		else: newCfg.write("config.JobType.maxMemoryMB = 2500 \n")
	elif "data" in sample:
		if "JEC" in systematic: newCfg.write("config.JobType.maxMemoryMB = 3000 \n")
		else: newCfg.write("config.JobType.maxMemoryMB = 2000 \n")

	## include all aux files
	inputFiles = []

	#### lumimask info: https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2#2018
	if "data" in sample:
		if year=="2015":
			newCfg.write("config.Data.lumiMask = '../data/lumimasks/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'\n")
			#inputFiles.append('data/lumimasks/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt')
		elif year=="2016":
			newCfg.write("config.Data.lumiMask = '../data/lumimasks/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'\n")
			#inputFiles.append('data/lumimasks/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt')
		elif year=="2017":
			newCfg.write("config.Data.lumiMask = '../data/lumimasks/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'\n")
			#inputFiles.append('data/lumimasks/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt')
		elif year=="2018":
			newCfg.write("config.Data.lumiMask = '../data/lumimasks/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'\n")
			#inputFiles.append('data/lumimasks/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt')

	newCfg.write("config.Data.outputDatasetTag = 'clustAlg_%s_%s_%s%s'\n"%(sample,year,WP_str, systematic))
	newCfg.write("config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_%s%s%s'\n"%(WP_str,dateTimeString,sideband_str))
	#newCfg.write("config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2025106_16330'\n")



	newCfg.write("config.Site.storageSite = 'T3_US_FNALLPC'\n")

	# jet veto map
	if "Suu" in sample:
		if year == "2015" or year == "2016":
			inputFiles.append("data/jetVetoMaps/hotjets-UL16.root")
		elif year == "2017":
			inputFiles.append("data/jetVetoMaps/hotjets-UL17_v2.root")
		elif year == "2018":
			inputFiles.append("data/jetVetoMaps/hotjets-UL18.root")


	# BEST model files
	inputFiles.append("data/BEST_models/constantgraph_combine.pb")
	inputFiles.append("data/BESTScalerParameters_all_mass_combine.txt")

	if "MC" in sample or "Suu" in sample: ## only valid for MC
		# PU weights
		if year == "2015":
			inputFiles.append("data/POG/LUM/2016preVFP_UL/puWeights.json")
		elif year == "2016":
			inputFiles.append("data/POG/LUM/2016postVFP_UL/puWeights.json")
		elif year == "2017":
			inputFiles.append("data/POG/LUM/2017_UL/puWeights.json")
		elif year == "2018":
			inputFiles.append("data/POG/LUM/2018_UL/puWeights.json")

		# btag files
		if "QCDMC" in sample:
			bTagSF_sample = "QCDMC"
		elif "TTTo" in sample or "TTJetsMC" in sample:
			bTagSF_sample = "TTbarMC"
		elif "ST_" in sample:
			bTagSF_sample = "STMC"
		elif "Suu" in sample:
			bTagSF_sample = "SuuToChiChi"
		elif "WJets" in sample:
			bTagSF_sample = "WJetsMC"
		elif "WW" in sample or "ZZ" in sample:
			bTagSF_sample = "TTbarMC"


		inputFiles.append("data/btaggingEffMaps/btag_efficiency_map_%s_combined_%s.root"%(bTagSF_sample,year))
		if year == "2015":
			inputFiles.append("data/bTaggingSFs/2016preVFP_UL/btagging.json")
		elif year == "2016":
			inputFiles.append("data/bTaggingSFs/2016postVFP_UL/btagging.json")
		elif year == "2017":
			inputFiles.append("data/bTaggingSFs/2017_UL/btagging.json")
		elif year == "2018":
			inputFiles.append("data/bTaggingSFs/2018_UL/btagging.json")


	# JEC files
	sample_type = "BR"
	if "Suu" in sample: sample_type = "signal"
	elif "data" in sample: sample_type = sample
	inputFiles.append(jec_file_AK8[year][sample_type])
	inputFiles.append(jec_file_AK4[year][sample_type])



	## include files that are needed 
	if "Suu" in sample:
		inputFile_str = "',\n'../../".join(inputFiles)
		newCfg.write("config.JobType.inputFiles = [ '../../%s' ]"%inputFile_str)

	else:
		inputFile_str = "',\n'../".join(inputFiles)
		newCfg.write("config.JobType.inputFiles = [ '../%s' ]"%inputFile_str)


def main():


	useOptimalWP = True




	lastCrabSubmission = open("lastCrabSubmission.txt", "a")

	current_time = datetime.now()
	dateTimeString = "%s%s%s_%s%s%s"%(current_time.year,current_time.month,current_time.day,current_time.hour,current_time.minute,current_time.second )
	if useOptimalWP: lastCrabSubmission.write("/store/user/ecannaer/SuuToChiChi_%s%s\n"%(dateTimeString,sideband_str))
	else: lastCrabSubmission.write("/store/user/ecannaer/SuuToChiChi_optWP_%s%s\n"%(dateTimeString,sideband_str))
	years   = ["2015","2016","2017","2018"]

   #systematics = [ "JEC_FlavorQCD", "JEC_RelativeBal", "JEC_HF", "JEC_BBEC1", "JEC_EC2", "JEC_Absolute", "JEC_BBEC1_year", "JEC_EC2_year", "JEC_Absolute_year", "JEC_HF_year", "JEC_RelativeSample_year", "JER_eta193", "JER_193eta25",  "JEC","JER","nom" ]

	systematics = [  "JEC1", "JEC2", "JER","nom" ]

	datasets = {	'2015': { 'QCDMC1000to1500': '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'QCDMC1500to2000': '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
							  'QCDMC2000toInf':  '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',
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
							  'dataF-HIPM': '/JetHT/Run2016F-HIPM_UL2016_MiniAODv2-v2/MINIAOD',
								  "WJetsMC_LNu-HT800to1200":  "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM"	,
							   "WJetsMC_LNu-HT1200to2500": "/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM"  ,
							   "WJetsMC_LNu-HT2500toInf":  "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM"  ,
							   "WJetsMC_QQ-HT800toInf":  "/WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM"   ,
							   "TTJetsMCHT800to1200":"/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM",
							   "WW_MC": "/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM"   ,
							   "ZZ_MC":  "/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM",

							   "QCDMC_Pt_170to300":   "/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM",
								"QCDMC_Pt_300to470":  "/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM",
								"QCDMC_Pt_470to600":  "/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM",
								"QCDMC_Pt_600to800":  "/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM",
								"QCDMC_Pt_800to1000": "/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM",
						   		"QCDMC_Pt_1000to1400":"/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM",
								"QCDMC_Pt_1400to1800":"/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM",
								"QCDMC_Pt_1800to2400":"/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM",
								"QCDMC_Pt_2400to3200":"/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM",
								"QCDMC_Pt_3200toInf": "/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM" 

							   },
					'2016': { 'QCDMC1000to1500': '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
							  'QCDMC1500to2000': '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
							  'QCDMC2000toInf':  '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
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
							  'dataH': '/JetHT/Run2016H-UL2016_MiniAODv2-v2/MINIAOD',
							   "WJetsMC_LNu-HT800to1200": "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM"	 ,
							   "WJetsMC_LNu-HT1200to2500": "/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM"  ,
							   "WJetsMC_LNu-HT2500toInf": "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM"   ,
							   "WJetsMC_QQ-HT800toInf": "/WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM"   ,
							   "TTJetsMCHT800to1200":	"/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM",
							   "WW_MC": "/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM",
							   "ZZ_MC": "/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM",

							   "QCDMC_Pt_170to300": "/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM",
								"QCDMC_Pt_300to470": "/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM",
								"QCDMC_Pt_470to600": "/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM",
								"QCDMC_Pt_600to800": "/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM",
								"QCDMC_Pt_800to1000":" /QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM",
						   		"QCDMC_Pt_1000to1400": "/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM",
								"QCDMC_Pt_1400to1800": "/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM",
								"QCDMC_Pt_1800to2400": "/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM",
								"QCDMC_Pt_2400to3200": "/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM",
								"QCDMC_Pt_3200toInf": "/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM"
							  },

					   '2017': { 'QCDMC1000to1500': '/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',
								 'QCDMC1500to2000': '/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',
								 'QCDMC2000toInf':  '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',
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
								 'dataF': '/JetHT/Run2017F-UL2017_MiniAODv2-v1/MINIAOD',
							   "WJetsMC_LNu-HT800to1200": "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM"	 ,
							   "WJetsMC_LNu-HT1200to2500": "/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM"  ,
							   "WJetsMC_LNu-HT2500toInf": "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM"  ,
							   "WJetsMC_QQ-HT800toInf":  "/WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM"   ,
							   "TTJetsMCHT800to1200": "/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM",
							   "WW_MC": "/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM",
							   "ZZ_MC": "/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM",
							   	"QCDMC_Pt_170to300": "/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM",
								"QCDMC_Pt_300to470": "/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM",
								"QCDMC_Pt_470to600": "/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM",
								"QCDMC_Pt_600to800": "/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM",
								"QCDMC_Pt_800to1000": "/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM",
						   		"QCDMC_Pt_1000to1400": "/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM",
								"QCDMC_Pt_1400to1800": "/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM",
								"QCDMC_Pt_1800to2400": "/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM",
								"QCDMC_Pt_2400to3200": "/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM",
								"QCDMC_Pt_3200toInf": "/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM"
								 },
					'2018': { 'QCDMC1000to1500': '/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'QCDMC1500to2000': '/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
							  'QCDMC2000toInf':  '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',
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
							  'dataD': '/JetHT/Run2018D-UL2018_MiniAODv2_GT36-v1/MINIAOD',
							  "WJetsMC_LNu-HT800to1200": "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM"	 ,
							   "WJetsMC_LNu-HT1200to2500":  "/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" ,
							   "WJetsMC_LNu-HT2500toInf": "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM"   ,
							   "WJetsMC_QQ-HT800toInf": "/WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM"	,
							   "TTJetsMCHT800to1200": "/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM",
							   "WW_MC": "/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
							   "ZZ_MC": "/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM",


								"QCDMC_Pt_170to300":  "/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
								"QCDMC_Pt_300to470":  "/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
								"QCDMC_Pt_470to600":  "/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
								"QCDMC_Pt_600to800":  "/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
								"QCDMC_Pt_800to1000": "/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
						   		"QCDMC_Pt_1000to1400": "/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
								"QCDMC_Pt_1400to1800": "/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
								"QCDMC_Pt_1800to2400": "/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
								"QCDMC_Pt_2400to3200": "/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM",
								"QCDMC_Pt_3200toInf": "/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM"
							  }
   }





	signal_datasets_pkl = open('../data/pkl/signal_datasets.pkl', 'r')	
	datasets_signal = pickle.load(signal_datasets_pkl)  # there are 456 signal datasets, so the dictionary construction is automated and loaded here


  	signal_samples_pkl = open('../data/pkl/signal_samples.pkl', 'r')
  	signal_samples	 = pickle.load(signal_samples_pkl)
	signal_samples = np.array(signal_samples)

  	num_files_created = 0
	for year in years:
		if year == "2015":
			samples = ["dataB-ver1","dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM" ,"dataF-HIPM","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT1200to2500",
	"TTJetsMCHT2500toInf",
	"TTToSemiLeptonicMC",
	 "TTToHadronicMC",
	"TTToLeptonicMC",
   "ST_t-channel-top_inclMC",
   "ST_t-channel-antitop_inclMC",
   "ST_s-channel-hadronsMC",
   "ST_s-channel-leptonsMC",
   "ST_tW-antiTop_inclMC",
   "ST_tW-top_inclMC",
   ### extras
   "WJetsMC_LNu-HT800to1200",
   "WJetsMC_LNu-HT1200to2500",
   "WJetsMC_LNu-HT2500toInf",
   "WJetsMC_QQ-HT800toInf",
   "TTJetsMCHT800to1200",
   "WW_MC",
   "ZZ_MC",
   "QCDMC_Pt_170to300",
	"QCDMC_Pt_300to470",
	"QCDMC_Pt_470to600",
	"QCDMC_Pt_600to800",
	"QCDMC_Pt_800to1000",
	"QCDMC_Pt_1000to1400",
	"QCDMC_Pt_1400to1800",
	"QCDMC_Pt_1800to2400",
	"QCDMC_Pt_2400to3200",
	"QCDMC_Pt_3200toInf"]
	   
		elif year == "2016":
			samples = ["dataF","dataG","dataH","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT1200to2500",
	"TTJetsMCHT2500toInf",
	"TTToSemiLeptonicMC",
	"TTToLeptonicMC",
	 "TTToHadronicMC",
   "ST_t-channel-top_inclMC",
   "ST_t-channel-antitop_inclMC",
   "ST_s-channel-hadronsMC",
   "ST_s-channel-leptonsMC",
   "ST_tW-antiTop_inclMC",
   "ST_tW-top_inclMC",
   ### extras
   "WJetsMC_LNu-HT800to1200",
   "WJetsMC_LNu-HT1200to2500",
   "WJetsMC_LNu-HT2500toInf",
   "WJetsMC_QQ-HT800toInf",
   "TTJetsMCHT800to1200",
   "WW_MC",
   "ZZ_MC",
   "QCDMC_Pt_170to300",
	"QCDMC_Pt_300to470",
	"QCDMC_Pt_470to600",
	"QCDMC_Pt_600to800",
	"QCDMC_Pt_800to1000",
	"QCDMC_Pt_1000to1400",
	"QCDMC_Pt_1400to1800",
	"QCDMC_Pt_1800to2400",
	"QCDMC_Pt_2400to3200",
	"QCDMC_Pt_3200toInf"
   ]
		elif year == "2017":
			samples = ["dataB","dataC","dataD","dataE","dataF","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf", "TTJetsMCHT1200to2500",
	"TTJetsMCHT2500toInf",
	"TTToSemiLeptonicMC",
	"TTToLeptonicMC",
	 "TTToHadronicMC",
   "ST_t-channel-top_inclMC",
   "ST_t-channel-antitop_inclMC",
   "ST_s-channel-hadronsMC",
   "ST_s-channel-leptonsMC",
   "ST_tW-antiTop_inclMC",
   "ST_tW-top_inclMC" ,
	 ### extras
   "WJetsMC_LNu-HT800to1200",
   "WJetsMC_LNu-HT1200to2500",
   "WJetsMC_LNu-HT2500toInf",
   "WJetsMC_QQ-HT800toInf",
   "TTJetsMCHT800to1200",
   "WW_MC",
   "ZZ_MC",
   "QCDMC_Pt_170to300",
	"QCDMC_Pt_300to470",
	"QCDMC_Pt_470to600",
	"QCDMC_Pt_600to800",
	"QCDMC_Pt_800to1000",
	"QCDMC_Pt_1000to1400",
	"QCDMC_Pt_1400to1800",
	"QCDMC_Pt_1800to2400",
	"QCDMC_Pt_2400to3200",
	"QCDMC_Pt_3200toInf"]
		elif year == "2018":
			samples = ["dataA","dataB", "dataC", "dataD","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT1200to2500",
   "TTJetsMCHT2500toInf",
   "TTToSemiLeptonicMC",
   "TTToLeptonicMC",
   "TTToHadronicMC",
   "ST_t-channel-top_inclMC",
   "ST_t-channel-antitop_inclMC",
   "ST_s-channel-hadronsMC",
   "ST_s-channel-leptonsMC",
   "ST_tW-antiTop_inclMC",
   "ST_tW-top_inclMC",
	### extras
   "WJetsMC_LNu-HT800to1200",
   "WJetsMC_LNu-HT1200to2500",
   "WJetsMC_LNu-HT2500toInf",
   "WJetsMC_QQ-HT800toInf",
   "TTJetsMCHT800to1200",
   "WW_MC",
   "ZZ_MC",
   "QCDMC_Pt_170to300",
	"QCDMC_Pt_300to470",
	"QCDMC_Pt_470to600",
	"QCDMC_Pt_600to800",
	"QCDMC_Pt_800to1000",
	"QCDMC_Pt_1000to1400",
	"QCDMC_Pt_1400to1800",
	"QCDMC_Pt_1800to2400",
	"QCDMC_Pt_2400to3200",
	"QCDMC_Pt_3200toInf"]
   		samples.extend(signal_samples)
		for iii, sample in enumerate(samples):
			for systematic in systematics:
				num_files_created+=1
				if "Suu" in sample:
					if systematic == "JER": continue
					try:
						makeAltCrabCfg(sample, year, systematic, datasets_signal[year][sample],dateTimeString, useOptimalWP)   # need a different dataset for signal mass points, only make a single signal cfg file to
					except:
						print("Failed for sample/year/systematic: %s/%s/%s."%(sample,year,systematic))
				elif "data" in sample and (systematic == "JER" or "JEC" in systematic): continue  # do NOT need to do these. Tons of extra calculations
				else:
					makeAltCrabCfg(sample, year, systematic, datasets[year][sample],dateTimeString,useOptimalWP)   
	print("Created %i cfg files."%num_files_created)
	return

if __name__ == "__main__":
	main()
