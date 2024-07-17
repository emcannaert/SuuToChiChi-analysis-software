#! /usr/bin/env python

import sys
import os
import pickle
import numpy as np

def makeACfg(sample, year, jec_file_AK8, jec_file_AK4):


	# need to change trigger for yhears
	trigger = ""
	if year == "2018" or year == "2017":
		trigger = "HLT_PFHT1050_v"
	elif year == "2015" or year == "2016":
		trigger = "HLT_PFHT900_v"

	apply_pu_ID = True

	newCfg = open("createHistsForEfficiencyMaps_%s_%s_cfg.py"%(sample,year),"w")
	newCfg.write("import FWCore.ParameterSet.Config as cms\n")

	newCfg.write('process = cms.Process("analysis")\n')
	newCfg.write("from Configuration.AlCa.GlobalTag import GlobalTag\n")

	newCfg.write("process.load('Configuration.StandardSequences.Services_cff')\n")
	newCfg.write('process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")\n')
	newCfg.write("process.load('JetMETCorrections.Configuration.JetCorrectors_cff')\n")
	newCfg.write("process.load('JetMETCorrections.Configuration.CorrectedJetProducers_cff')\n")
	newCfg.write("process.load('JetMETCorrections.Configuration.CorrectedJetProducersDefault_cff')\n")
	newCfg.write('process.load("JetMETCorrections.Configuration.JetCorrectionServices_cff")\n')
	newCfg.write('process.load("JetMETCorrections.Configuration.JetCorrectionServicesAllAlgos_cff")\n')

	if not "data" in sample: 
		if year == "2018":
			newCfg.write("process.GlobalTag.globaltag = '106X_upgrade2018_realistic_v16_L1v1'\n")  
		elif year == "2017":
			newCfg.write("process.GlobalTag.globaltag = '106X_mc2017_realistic_v10'\n")
		elif year == "2016":
			newCfg.write("process.GlobalTag.globaltag = '106X_mcRun2_asymptotic_v17'\n")
		elif year == "2015":
			newCfg.write("process.GlobalTag.globaltag = '106X_mcRun2_asymptotic_v17'\n")

	newCfg.write("process.options = cms.untracked.PSet( allowUnscheduled = cms.untracked.bool(True) )\n")


	newCfg.write("from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD\n")

	if "data" in sample:
		newCfg.write("isData = True\n")
	else:
		newCfg.write("isData = False\n")
	newCfg.write("corrLabels = ['L1FastJet','L2Relative','L3Absolute']\n")
	newCfg.write("if isData:\n")
	newCfg.write("	corrs.append('L2L3Residuals')\n")
	newCfg.write("from PhysicsTools.PatAlgos.tools.jetTools import *\n")
	newCfg.write("from RecoBTag.ONNXRuntime.pfDeepBoostedJet_cff import *\n")



	newCfg.write("updateJetCollection(\n")
	newCfg.write("	process,\n")
	newCfg.write("	jetSource = cms.InputTag('slimmedJetsAK8'),\n")
	newCfg.write("	labelName = 'AK8',\n")
	newCfg.write("	jetCorrections = ('AK8PFPuppi', cms.vstring(corrLabels), 'None'), #previous corrections: 'L2Relative', 'L3Absolute', 'L2L3Residual'\n")
	newCfg.write("	postfix = 'UpdatedJEC',\n")
	newCfg.write("	printWarning = False\n")
	newCfg.write(")\n")
	newCfg.write("updateJetCollection(\n")
	newCfg.write("	process,\n")
	newCfg.write("	jetSource = cms.InputTag('slimmedJets'),\n")
	newCfg.write("	labelName = 'AK4',\n")
	newCfg.write("	jetCorrections = ('AK4PFchs', cms.vstring(corrLabels), 'None'), #previous corrections: 'L2Relative', 'L3Absolute', 'L2L3Residual'\n")
	newCfg.write("	postfix = 'UpdatedJEC',\n")
	newCfg.write("	printWarning = False\n")
	newCfg.write(")\n")

	if apply_pu_ID:
		newCfg.write("################# Jet PU ID ################\n")
		newCfg.write('from RecoJets.JetProducers.PileupJetID_cfi import pileupJetId\n')
		if year == "2016":
			newCfg.write('from RecoJets.JetProducers.PileupJetID_cfi import _chsalgos_106X_UL16	  #	  (or _chsalgos_106X_UL16APV for APV samples)\n')
		elif year == "2017":
			newCfg.write('from RecoJets.JetProducers.PileupJetID_cfi import _chsalgos_106X_UL17\n')
		elif year == "2018":
			newCfg.write('from RecoJets.JetProducers.PileupJetID_cfi import _chsalgos_106X_UL18\n')
		newCfg.write('process.load("RecoJets.JetProducers.PileupJetID_cfi")\n')
		newCfg.write('process.pileupJetIdUpdated = process.pileupJetId.clone( \n')
		newCfg.write('jets=cms.InputTag("selectedUpdatedPatJetsAK4UpdatedJEC"),		#should be the name of the post-JEC jet collection\n')
		newCfg.write('inputIsCorrected=True,\n')
		newCfg.write('applyJec=False,\n')
		newCfg.write('vertexes=cms.InputTag("offlineSlimmedPrimaryVertices"),\n')
		if year == "2016":
			newCfg.write('algos = cms.VPSet(_chsalgos_106X_UL16),\n')
		elif year == "2017":
			newCfg.write('algos = cms.VPSet(_chsalgos_106X_UL17),\n')
		elif year == "2018":
			newCfg.write('algos = cms.VPSet(_chsalgos_106X_UL18),\n')
		newCfg.write(')\n')

		newCfg.write('process.patAlgosToolsTask.add(process.pileupJetIdUpdated)\n')

		newCfg.write('updateJetCollection(	  # running in unscheduled mode, need to manually update collection\n')
		newCfg.write('	process,\n')
		newCfg.write('	labelName = "PileupJetID",\n')
		newCfg.write('	jetSource = cms.InputTag("selectedUpdatedPatJetsAK4UpdatedJEC"),\n')
		newCfg.write(')\n')
		newCfg.write('process.updatedPatJetsPileupJetID.userData.userInts.src = ["pileupJetIdUpdated:fullId"]\n')


	newCfg.write('process.hadronFilter = cms.EDFilter("hadronFilter_bTagSF",\n')
	newCfg.write('	fatJetCollection = cms.InputTag("selectedUpdatedPatJetsAK8UpdatedJEC"),\n')
	if apply_pu_ID:
		newCfg.write('	jetCollection = cms.InputTag("selectedUpdatedPatJetsPileupJetID"),\n')
	else:
		newCfg.write('	jetCollection = cms.InputTag("selectedUpdatedPatJetsAK4UpdatedJEC"),\n')
	newCfg.write('	bits = cms.InputTag("TriggerResults", "", "HLT"),\n')
	newCfg.write('	triggers = cms.string("%s"),\n'%trigger)
	newCfg.write('	systematicType = cms.string(""), \n ')
	newCfg.write('	year = cms.string("%s"), \n '%year)

	newCfg.write('	runType = cms.string("%s")	#types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTJetsMCHT1200to2500, TTJetsMCHT2500toInf, DataA, etc. , Suu8_chi3, etc.\n'%sample)
	newCfg.write(")\n")

	newCfg.write('process.calculateBtagEfficiencyMaps = cms.EDAnalyzer("calculateBtagEfficiencyMaps",\n')
	newCfg.write('	year = cms.string("%s"),\n'%year)
	
	newCfg.write('	runType = cms.string("%s"),	#types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTJetsMCHT1200to2500, TTJetsMCHT2500toInf, DataA, etc. , Suu8_chi3, etc.\n'%sample)
	newCfg.write('	fatJetCollection = cms.InputTag("selectedUpdatedPatJetsAK8UpdatedJEC"),\n')

	newCfg.write(' JECUncert_AK8_path = cms.FileInPath("%s"),\n'%jec_file_AK8)
	newCfg.write(' JECUncert_AK4_path = cms.FileInPath("%s"),\n'%jec_file_AK4)

	if apply_pu_ID:
		newCfg.write('	jetCollection = cms.InputTag("selectedUpdatedPatJetsPileupJetID"),\n')
	else:
		newCfg.write('	jetCollection = cms.InputTag("selectedUpdatedPatJetsAK4UpdatedJEC"),\n')
	newCfg.write('	systematicType = cms.string(""),\n')


	if apply_pu_ID:
		newCfg.write('	doPUID = cms.bool(True)\n')
	else:
		newCfg.write('	doPUID = cms.bool(False)\n')
	newCfg.write(")\n")


	newCfg.write('process.source = cms.Source("PoolSource",\n')

	####### NOTE: because this uses only 2018 file, all events will fail while testing on 2015 cfgs because of the trigger
	newCfg.write('fileNames = cms.untracked.vstring("/store/mc/RunIISummer20UL18MiniAODv2/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2520000/253E974C-8873-AA49-A1CD-2D03622F0A2E.root" #this is a dummy file!!\n')
	newCfg.write(")\n")
	newCfg.write(")\n")
	newCfg.write('process.TFileService = cms.Service("TFileService",fileName = cms.string("btagging_efficiencyMap_%s_%s_output.root")\n'%(sample,year))
	newCfg.write(")\n")

	newCfg.write("process.options = cms.untracked.PSet(\n")
	newCfg.write("	wantSummary = cms.untracked.bool(True),\n")
	newCfg.write(")\n")

	newCfg.write('process.load("FWCore.MessageLogger.MessageLogger_cfi")\n')
	newCfg.write("process.MessageLogger.cerr.FwkReport.reportEvery = 1000\n")


	newCfg.write("process.p = cms.Path( ")
	if apply_pu_ID:
		newCfg.write("process.pileupJetIdUpdated * \n")
	newCfg.write("process.hadronFilter *\n")
	newCfg.write(" process.calculateBtagEfficiencyMaps\n")
	newCfg.write(")\n")
	newCfg.write("from PhysicsTools.PatAlgos.tools.helpers  import getPatAlgosToolsTask\n")
	newCfg.write("process.patAlgosToolsTask = getPatAlgosToolsTask(process)\n")
	newCfg.write("process.pathRunPatAlgos = cms.Path(process.patAlgosToolsTask)\n")
	newCfg.close()

def main():

	years	= ["2015","2016","2017","2018"]

	signal_samples_pkl = open('../../signal_samples.pkl', 'r')
	signal_samples	  = pickle.load(signal_samples_pkl)
	signal_samples = np.array(signal_samples)


	# load in signal samples
	jec_file_AK4 = { '2015': { 'QCDMC1000to1500': 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC1500to2000': 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC2000toInf':  'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                       'TTToHadronicMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',  
                       'TTToSemiLeptonicMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',  
                       'TTToLeptonicMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',  
                       "TTJetsMCHT1200to2500": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt', 
                        "TTJetsMCHT2500toInf": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                       'ST_t-channel-top_inclMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                        'ST_t-channel-antitop_inclMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                        'ST_s-channel-hadronsMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                        'ST_s-channel-leptonsMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                        'ST_tW-antiTop_inclMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                        'ST_tW-top_inclMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                       'dataB-ver1': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                       'dataB-ver2': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                       'dataC-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                       'dataD-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                       'dataE-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunEF_V7_DATA_Uncertainty_AK4PFchs.txt',
                       'dataF-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunEF_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu8_chi3": 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu8_chi2": 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu8_chi1": 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu7_chi3": 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu7_chi2": 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu7_chi1": 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu6_chi2": 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu6_chi1p5": 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu6_chi1": 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu5_chi2": 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu5_chi1p5": 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu5_chi1": 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu4_chi1p5": 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu4_chi1": 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "signal": 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                           "WJetsMC_LNu-HT800to1200":  'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt' ,
                           "WJetsMC_LNu-HT1200to2500": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                           "WJetsMC_LNu-HT2500toInf":  'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                           "WJetsMC_QQ-HT800toInf":   'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                           "TTJetsMCHT800to1200": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                           "WW_MC": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt', 
                           "ZZ_MC": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                           'QCDMC_Pt15to7000':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt'

                       },
            '2016': { 'QCDMC1000to1500': 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC1500to2000': 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC2000toInf':  'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                       'TTToHadronicMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',  
                       'TTToSemiLeptonicMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',  
                       'TTToLeptonicMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',  
                        "TTJetsMCHT1200to2500": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt', 
                        "TTJetsMCHT2500toInf": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        'ST_t-channel-top_inclMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        'ST_t-channel-antitop_inclMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        'ST_s-channel-hadronsMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        'ST_s-channel-leptonsMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        'ST_tW-antiTop_inclMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        'ST_tW-top_inclMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                       'dataF': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK4PFchs.txt',
                       'dataG': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK4PFchs.txt',
                       'dataH': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu8_chi3": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        "Suu8_chi2": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        "Suu8_chi1": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        "Suu7_chi3": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        "Suu7_chi2": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        "Suu7_chi1": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        "Suu6_chi2": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        "Suu6_chi1p5": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        "Suu6_chi1": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        "Suu5_chi2": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        "Suu5_chi1p5": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        "Suu5_chi1": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        "Suu4_chi1p5": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        "Suu4_chi1": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                        "signal": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                           "WJetsMC_LNu-HT800to1200":   'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                           "WJetsMC_LNu-HT1200to2500": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                           "WJetsMC_LNu-HT2500toInf":  'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                           "WJetsMC_QQ-HT800toInf":   'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                           "TTJetsMCHT800to1200":'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                           "WW_MC": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt', 
                           "ZZ_MC": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                           'QCDMC_Pt15to7000':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt'},

'2017': { 'QCDMC1000to1500': 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC1500to2000': 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC2000toInf':  'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                       'TTToHadronicMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',  
                       'TTToSemiLeptonicMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',  
                       'TTToLeptonicMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt', 
                        "TTJetsMCHT1200to2500": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt', 
                        "TTJetsMCHT2500toInf": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt', 
                       'ST_t-channel-top_inclMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                        'ST_t-channel-antitop_inclMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                        'ST_s-channel-hadronsMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                        'ST_s-channel-leptonsMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                        'ST_tW-antiTop_inclMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                        'ST_tW-top_inclMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',

                       'dataB': 'data/JEC/2017_UL/data/Summer19UL17_RunB_V5_DATA_Uncertainty_AK4PFchs.txt',
                       'dataC': 'data/JEC/2017_UL/data/Summer19UL17_RunC_V5_DATA_Uncertainty_AK4PFchs.txt',
                       'dataD': 'data/JEC/2017_UL/data/Summer19UL17_RunD_V5_DATA_Uncertainty_AK4PFchs.txt',
                       'dataE': 'data/JEC/2017_UL/data/Summer19UL17_RunE_V5_DATA_Uncertainty_AK4PFchs.txt',
                       'dataF': 'data/JEC/2017_UL/data/Summer19UL17_RunF_V5_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu8_chi3": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "Suu8_chi2": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "Suu8_chi1": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "Suu7_chi3": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "Suu7_chi2": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "Suu7_chi1": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "Suu6_chi2": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "Suu6_chi1p5": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "Suu6_chi1": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "Suu5_chi2": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "Suu5_chi1p5": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "Suu5_chi1": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "Suu4_chi1p5": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "Suu4_chi1": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "signal": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                      "WJetsMC_LNu-HT800to1200":  'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt' ,
                     "WJetsMC_LNu-HT1200to2500": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "WJetsMC_LNu-HT2500toInf": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt' ,
                     "WJetsMC_QQ-HT800toInf":   'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "TTJetsMCHT800to1200": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     "WW_MC": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt', 
                     "ZZ_MC": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                     'QCDMC_Pt15to7000':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt'

                     },
'2018': { 'QCDMC1000to1500': 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC1500to2000': 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC2000toInf':  'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                       'TTToHadronicMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt', 
                       'TTToSemiLeptonicMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',  
                       'TTToLeptonicMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',  
                        "TTJetsMCHT1200to2500": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt', 
                        "TTJetsMCHT2500toInf": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                       'ST_t-channel-top_inclMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        'ST_t-channel-antitop_inclMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        'ST_s-channel-hadronsMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        'ST_s-channel-leptonsMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        'ST_tW-antiTop_inclMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        'ST_tW-top_inclMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                       'dataA': 'data/JEC/2018_UL/data/Summer19UL18_RunA_V5_DATA_Uncertainty_AK4PFPuppi.txt',
                       'dataB': 'data/JEC/2018_UL/data/Summer19UL18_RunB_V5_DATA_Uncertainty_AK4PFchs.txt',
                       'dataC': 'data/JEC/2018_UL/data/Summer19UL18_RunC_V5_DATA_Uncertainty_AK4PFchs.txt',
                       'dataD': 'data/JEC/2018_UL/data/Summer19UL18_RunD_V5_DATA_Uncertainty_AK4PFchs.txt',
                        "Suu8_chi3": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "Suu8_chi2": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "Suu8_chi1": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "Suu7_chi3": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "Suu7_chi2": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "Suu7_chi1": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "Suu6_chi2": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "Suu6_chi1p5": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "Suu6_chi1": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "Suu5_chi2": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "Suu5_chi1p5": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "Suu5_chi1": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "Suu4_chi1p5": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "Suu4_chi1": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "signal": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                         "WJetsMC_LNu-HT800to1200":  'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt' ,
                        "WJetsMC_LNu-HT1200to2500": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "WJetsMC_LNu-HT2500toInf":  'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "WJetsMC_QQ-HT800toInf":   'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "TTJetsMCHT800to1200":'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        "WW_MC": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt', 
                        "ZZ_MC": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                        'QCDMC_Pt15to7000': 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt'
                        }}

	jec_file_AK8 = { '2015': { 'QCDMC1000to1500': 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC1500to2000': 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC2000toInf':  'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                       'TTToHadronicMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',  
                       'TTToSemiLeptonicMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',  
                       'TTToLeptonicMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',  
                        "TTJetsMCHT1200to2500":'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt' , 
                        "TTJetsMCHT2500toInf": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                       'ST_t-channel-top_inclMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_t-channel-antitop_inclMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_s-channel-hadronsMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_s-channel-leptonsMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_tW-antiTop_inclMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_tW-top_inclMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                       'dataB-ver1': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataB-ver2': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataC-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataD-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataE-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunEF_V7_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataF-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunEF_V7_DATA_Uncertainty_AK8PFPuppi.txt',

                        "Suu8_chi3": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu8_chi2": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu8_chi1": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu7_chi3": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu7_chi2": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu7_chi1": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu6_chi2": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu6_chi1p5": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu6_chi1": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu5_chi2": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu5_chi1p5": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu5_chi1": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu4_chi1p5": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu4_chi1": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "signal": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',

                        "WJetsMC_LNu-HT800to1200":   'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "WJetsMC_LNu-HT1200to2500": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "WJetsMC_LNu-HT2500toInf": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "WJetsMC_QQ-HT800toInf":   'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "TTJetsMCHT800to1200": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "WW_MC": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt', 
                        "ZZ_MC": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        'QCDMC_Pt15to7000':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt'},


            '2016': { 'QCDMC1000to1500': 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC1500to2000': 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC2000toInf':  'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                       'TTToHadronicMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt', 
                       'TTToSemiLeptonicMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',  
                       'TTToLeptonicMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',  
                        "TTJetsMCHT1200to2500": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt', 
                        "TTJetsMCHT2500toInf": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                       'ST_t-channel-top_inclMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_t-channel-antitop_inclMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_s-channel-hadronsMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_s-channel-leptonsMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_tW-antiTop_inclMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_tW-top_inclMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt', 
                       'dataF': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataG': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataH': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK8PFPuppi.txt',
                        "Suu8_chi3": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu8_chi2": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu8_chi1": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu7_chi3": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu7_chi2": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu7_chi1": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu6_chi2": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu6_chi1p5": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu6_chi1": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu5_chi2": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu5_chi1p5": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu5_chi1": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu4_chi1p5": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu4_chi1": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "signal": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "WJetsMC_LNu-HT800to1200":   'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "WJetsMC_LNu-HT1200to2500": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "WJetsMC_LNu-HT2500toInf": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "WJetsMC_QQ-HT800toInf":  'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt' ,
                        "TTJetsMCHT800to1200":'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        "WW_MC": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt', 
                        "ZZ_MC": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                        'QCDMC_Pt15to7000': 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt'
                        },

'2017': { 'QCDMC1000to1500': 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC1500to2000': 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC2000toInf':  'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                       'TTToHadronicMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',  
                       'TTToSemiLeptonicMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',  
                       'TTToLeptonicMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt', 
                        "TTJetsMCHT1200to2500": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt', 
                        "TTJetsMCHT2500toInf": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                       'ST_t-channel-top_inclMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_t-channel-antitop_inclMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_s-channel-hadronsMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_s-channel-leptonsMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_tW-antiTop_inclMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_tW-top_inclMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt', 
                       'dataB': 'data/JEC/2017_UL/data/Summer19UL17_RunB_V5_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataC': 'data/JEC/2017_UL/data/Summer19UL17_RunC_V5_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataD': 'data/JEC/2017_UL/data/Summer19UL17_RunD_V5_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataE': 'data/JEC/2017_UL/data/Summer19UL17_RunE_V5_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataF': 'data/JEC/2017_UL/data/Summer19UL17_RunF_V5_DATA_Uncertainty_AK8PFPuppi.txt',
                        "Suu8_chi3": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu8_chi2": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu8_chi1": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu7_chi3": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu7_chi2": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu7_chi1": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu6_chi2": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu6_chi1p5": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu6_chi1": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu5_chi2": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu5_chi1p5": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu5_chi1": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu4_chi1p5": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "Suu4_chi1": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "signal": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "WJetsMC_LNu-HT800to1200":   'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "WJetsMC_LNu-HT1200to2500": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "WJetsMC_LNu-HT2500toInf":  'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "WJetsMC_QQ-HT800toInf":  'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt' ,
                        "TTJetsMCHT800to1200":'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        "WW_MC": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt', 
                        "ZZ_MC": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        'QCDMC_Pt15to7000': 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt'
                        },
'2018': { 'QCDMC1000to1500': 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC1500to2000': 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC2000toInf':  'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                       'TTToHadronicMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',  
                       'TTToSemiLeptonicMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',  
                       'TTToLeptonicMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',  
                        "TTJetsMCHT1200to2500": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt', 
                        "TTJetsMCHT2500toInf": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_t-channel-top_inclMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_t-channel-antitop_inclMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_s-channel-hadronsMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_s-channel-leptonsMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_tW-antiTop_inclMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                        'ST_tW-top_inclMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                       'dataA': 'data/JEC/2018_UL/data/Summer19UL18_RunA_V5_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataB': 'data/JEC/2018_UL/data/Summer19UL18_RunB_V5_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataC': 'data/JEC/2018_UL/data/Summer19UL18_RunC_V5_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataD': 'data/JEC/2018_UL/data/Summer19UL18_RunD_V5_DATA_Uncertainty_AK8PFPuppi.txt',
                          "Suu8_chi3": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "Suu8_chi2": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "Suu8_chi1": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "Suu7_chi3": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "Suu7_chi2": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "Suu7_chi1": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "Suu6_chi2": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "Suu6_chi1p5": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "Suu6_chi1": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "Suu5_chi2": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "Suu5_chi1p5": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "Suu5_chi1": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "Suu4_chi1p5": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "Suu4_chi1": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "signal": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "WJetsMC_LNu-HT800to1200":   'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "WJetsMC_LNu-HT1200to2500": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "WJetsMC_LNu-HT2500toInf":   'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "WJetsMC_QQ-HT800toInf":  'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt' ,
                     "TTJetsMCHT800to1200":'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "WW_MC": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt', 
                     "ZZ_MC": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                     "QCDMC_Pt15to7000": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt'}
}

	"""datafile = [ 
		"signalCfgs/UL_files_ALLDECAYS/Suu8TeV_chi3TeV_UL-ALLDECAY.root",
		"signalCfgs/UL_files_ALLDECAYS/Suu8TeV_chi2TeV_UL-ALLDECAY.root",
		"signalCfgs/UL_files_ALLDECAYS/Suu8TeV_chi1TeV_UL-ALLDECAY.root",
		"signalCfgs/UL_files_ALLDECAYS/Suu7TeV_chi3TeV_UL-ALLDECAY.root",
		"signalCfgs/UL_files_ALLDECAYS/Suu7TeV_chi2TeV_UL-ALLDECAY.root",
		"signalCfgs/UL_files_ALLDECAYS/Suu7TeV_chi1TeV_UL-ALLDECAY.root",
		"signalCfgs/UL_files_ALLDECAYS/Suu6TeV_chi2TeV_UL-ALLDECAY.root",
		"signalCfgs/UL_files_ALLDECAYS/Suu6TeV_chi1p5TeV_UL-ALLDECAY.root",
		"signalCfgs/UL_files_ALLDECAYS/Suu6TeV_chi1TeV_UL-ALLDECAY.root",
		"signalCfgs/UL_files_ALLDECAYS/Suu5TeV_chi2TeV_UL-ALLDECAY.root",
		"signalCfgs/UL_files_ALLDECAYS/Suu5TeV_chi1p5TeV_UL-ALLDECAY.root",
		"signalCfgs/UL_files_ALLDECAYS/Suu5TeV_chi1TeV_UL-ALLDECAY.root",
		"signalCfgs/UL_files_ALLDECAYS/Suu4TeV_chi1p5TeV_UL-ALLDECAY.root",
		"signalCfgs/UL_files_ALLDECAYS/Suu4TeV_chi1TeV_UL-ALLDECAY.root"]"""
	for year in years:
		if year == "2015":
			samples = ["dataB-ver1","dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM" ,"dataF-HIPM","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","QCDMC_Pt15to7000","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf", "TTToHadronicMC","TTToSemiLeptonicMC", "TTToLeptonicMC",
	"ST_t-channel-top_inclMC",
	"ST_t-channel-antitop_inclMC",
	"ST_s-channel-hadronsMC",
	"ST_s-channel-leptonsMC",
	"ST_tW-antiTop_inclMC",
	"ST_tW-top_inclMC"]
		elif year == "2016":
			samples = ["dataF","dataG","dataH","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","QCDMC_Pt15to7000","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf","TTToHadronicMC","TTToSemiLeptonicMC", "TTToLeptonicMC",
	"ST_t-channel-top_inclMC",
	"ST_t-channel-antitop_inclMC",
	"ST_s-channel-hadronsMC",
	"ST_s-channel-leptonsMC",
	"ST_tW-antiTop_inclMC",
	"ST_tW-top_inclMC"]
		elif year == "2017":
			samples = ["dataB","dataC","dataD","dataE","dataF","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","QCDMC_Pt15to7000","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf","TTToHadronicMC","TTToSemiLeptonicMC", "TTToLeptonicMC",
	"ST_t-channel-top_inclMC",
	"ST_t-channel-antitop_inclMC",
	"ST_s-channel-hadronsMC",
	"ST_s-channel-leptonsMC",
	"ST_tW-antiTop_inclMC",
	"ST_tW-top_inclMC" ]
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
			if "data" in sample:
				continue
			use_sample = sample
			if "Suu" in sample:
				use_sample = "signal"
			makeACfg(sample, year,jec_file_AK4[year][use_sample],jec_file_AK8[year][use_sample])
	return


if __name__ == "__main__":
	 main()
