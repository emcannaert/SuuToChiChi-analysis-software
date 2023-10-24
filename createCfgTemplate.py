#! /usr/bin/env python

import sys
import os

### this can be updated to create the different cfgs for each systematic
def makeACfg(sample, year, systematic, datafile, jec_file_AK4, jec_file_AK8):


   # need to change trigger for yhears
   trigger = ""
   if year == "2018" or year == "2017":
      trigger = "HLT_PFHT1050_v"
   elif year == "2015" or year == "2016":
      trigger = "HLT_PFHT900_v"

   if systematic == "":
      newCfg = open("allCfgs/clusteringAnalyzer_%s_%s_%scfg.py"%(sample,year, systematic),"w")
   else:
      newCfg = open("allCfgs/clusteringAnalyzer_%s_%s_%s_cfg.py"%(sample,year,systematic),"w")
   

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


   """
    Data: 106X_dataRun2_v37
    MC 2016APV: 106X_mcRun2_asymptotic_v17
    MC 2016: 106X_mcRun2_asymptotic_v17
    MC 2017: 106X_mc2017_realistic_v10
    MC 2018: 106X_upgrade2018_realistic_v16_L1v1 
   """

   ##### updated 28 August 2023
   #OLD: global tags found here https://twiki.cern.ch/twiki/bin/view/CMSPublic/GTsAfter2019#Global_tag_for_2020_UL_MC_p_AN34 for Summer20 UL campaigns
   #NEW and what is in use: https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun2LegacyAnalysis
   if not "data" in sample: 
      if year == "2018":
         newCfg.write("process.GlobalTag.globaltag = '106X_upgrade2018_realistic_v16_L1v1'\n")  
      elif year == "2017":
         newCfg.write("process.GlobalTag.globaltag = '106X_mc2017_realistic_v10'\n")
      elif year == "2016":
         newCfg.write("process.GlobalTag.globaltag = '106X_mcRun2_asymptotic_v17'\n")
      elif year == "2015":
         newCfg.write("process.GlobalTag.globaltag = '106X_mcRun2_asymptotic_v17'\n")
   elif "data" in sample:
      newCfg.write("process.GlobalTag.globaltag = '106X_dataRun2_v37'\n")  
   else: 
      print("Something wrong with sample and the global tag designation.")

   newCfg.write("process.options = cms.untracked.PSet( allowUnscheduled = cms.untracked.bool(True) )\n")

   if "data" in sample:
      newCfg.write("isData = True\n")
   else:
      newCfg.write("isData = False\n")      

   newCfg.write("from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD\n")

   newCfg.write("################# JEC ################\n")

   newCfg.write("corrLabels = ['L1FastJet','L2Relative','L3Absolute']\n")
   newCfg.write("if isData:\n")
   newCfg.write("	corrLabels.append('L2L3Residuals')\n")
   newCfg.write("from PhysicsTools.PatAlgos.tools.jetTools import *\n")
   newCfg.write("from RecoBTag.ONNXRuntime.pfDeepBoostedJet_cff import *\n")
   newCfg.write("updateJetCollection(\n")
   newCfg.write("   process,\n")
   newCfg.write("   jetSource = cms.InputTag('slimmedJetsAK8'),\n")
   newCfg.write("   labelName = 'AK8',\n")
   newCfg.write("   jetCorrections = ('AK8PFPuppi', cms.vstring(corrLabels), 'None'), #previous corrections: 'L2Relative', 'L3Absolute', 'L2L3Residual'\n")
   newCfg.write("   postfix = 'UpdatedJEC',\n")
   newCfg.write("   printWarning = False\n")
   newCfg.write(")\n")
   newCfg.write("updateJetCollection(\n")
   newCfg.write("   process,\n")
   newCfg.write("   jetSource = cms.InputTag('slimmedJets'),\n")
   newCfg.write("   labelName = 'AK4',\n")
   newCfg.write("   jetCorrections = ('AK4PFchs', cms.vstring(corrLabels), 'None'),\n")
   newCfg.write("   postfix = 'UpdatedJEC',\n")
   newCfg.write("   printWarning = False\n")
   newCfg.write(")  \n")
   newCfg.write('process.content = cms.EDAnalyzer("EventContentAnalyzer")\n')


   newCfg.write("##############################################################################\n")
   newCfg.write('process.leptonVeto = cms.EDFilter("leptonVeto",\n')
   newCfg.write('   muonCollection= cms.InputTag("slimmedMuons"),\n')
   newCfg.write('   electronCollection = cms.InputTag("slimmedElectrons"),\n')
   newCfg.write('   metCollection = cms.InputTag("slimmedMETs"),\n')
   newCfg.write('   tauCollection = cms.InputTag("slimmedTaus")\n')
   newCfg.write(")\n")

   newCfg.write('process.hadronFilter = cms.EDFilter("hadronFilter",\n')
   newCfg.write('   year = cms.string("%s"),\n'%year)

   newCfg.write('   fatJetCollection = cms.InputTag("selectedUpdatedPatJetsAK8UpdatedJEC"),\n')
   newCfg.write('   metCollection = cms.InputTag("slimmedMETs"),\n')
   newCfg.write('   jetCollection = cms.InputTag("selectedUpdatedPatJetsAK4UpdatedJEC"),\n')
   newCfg.write('   bits = cms.InputTag("TriggerResults", "", "HLT"),\n')
   newCfg.write('   triggers = cms.string("%s"),\n'%trigger)
   newCfg.write('   systematicType = cms.string("%s"),\n'%systematic)
   newCfg.write('   JECUncert_AK4_path = cms.FileInPath("%s"),\n'%jec_file_AK4)

   newCfg.write('   runType = cms.string("%s")   #types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTbarMC, DataA, etc. , Suu8_chi3, etc.\n'%sample)
   newCfg.write(")\n")



   systematicSuffices = ["_up", "_down"]
   for iii, suffix in enumerate(systematicSuffices):

      if systematic == "":  # want to have only one round of the analyzer run with no suffix to represent the case of all systematics being nominal
         if(iii>0):
            continue
         elif iii == 0:
            suffix = ""


      newCfg.write('process.clusteringAnalyzerAll_%s%s = cms.EDAnalyzer("clusteringAnalyzerAll",\n'%(systematic, suffix) )
      """
      if "QCD" in sample:
         newCfg.write('   runType = cms.string("QCDMC"),   #types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTbarMC, DataA, etc. , Suu8_chi3, etc.\n')
      elif "TTbar" in sample:
         newCfg.write('   runType = cms.string("TTbarMC"),   #types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTbarMC, DataA, etc. , Suu8_chi3, etc.\n')
      elif "Suu" in sample:
         newCfg.write('   runType = cms.string("SigMC"),   #types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTbarMC, DataA, etc. , Suu8_chi3, etc.\n')
      elif "data" in sample:
         newCfg.write('   runType = cms.string("Data"),   #types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTbarMC, DataA, etc. , Suu8_chi3, etc.\n')
      else:
         print("something failed with writing runType.", sample ) 
      """
      newCfg.write('   runType = cms.string("%s"),   #types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTbarMC, DataA, etc. , Suu8_chi3, etc.\n'%sample)
      newCfg.write('   genPartCollection = cms.InputTag("prunedGenParticles"),\n')
      newCfg.write("   name = cms.string('BESTGraph'),   path = cms.FileInPath('data/constantgraph.pb'),\n")
      newCfg.write("   means = cms.FileInPath('data/ScalerParameters_maxAbs_train.txt'),\n")
      if year == "2015":
         newCfg.write("   PUfile_path = cms.FileInPath('data/POG/LUM/2016preVFP_UL/puWeights.json'),\n")
      elif year == "2016":
         newCfg.write("   PUfile_path = cms.FileInPath('data/POG/LUM/2016postVFP_UL/puWeights.json'),\n")
      elif year == "2017":
         newCfg.write("   PUfile_path = cms.FileInPath('data/POG/LUM/2017_UL/puWeights.json'),\n")
      elif year == "2018":
         newCfg.write("   PUfile_path = cms.FileInPath('data/POG/LUM/2018_UL/puWeights.json'),\n")

      #should this be for data and MC?
      if "MC" in sample:
         newCfg.write("   bTagEff_path = cms.FileInPath('data/btaggingEffMaps/btag_efficiency_map_%s_%s.root'),\n"%(sample,year))
         if year == "2015":
            newCfg.write("   bTagSF_path = cms.FileInPath('data/bTaggingSFs/2016preVFP_UL/btagging.json'),\n")
         elif year == "2016":
            newCfg.write("   bTagSF_path = cms.FileInPath('data/bTaggingSFs/2016postVFP_UL/btagging.json'),\n")
         elif year == "2017":
            newCfg.write("   bTagSF_path = cms.FileInPath('data/bTaggingSFs/2017_UL/btagging.json'),\n")
         elif year == "2018":
            newCfg.write("   bTagSF_path = cms.FileInPath('data/bTaggingSFs/2018_UL/btagging.json'),\n")

      newCfg.write('   JECUncert_AK8_path = cms.FileInPath("%s"),\n'%jec_file_AK8)
      newCfg.write('   JECUncert_AK4_path = cms.FileInPath("%s"),\n'%jec_file_AK4)

      newCfg.write('   fatJetCollection = cms.InputTag("selectedUpdatedPatJetsAK8UpdatedJEC"),\n')
      newCfg.write('   jetCollection = cms.InputTag("selectedUpdatedPatJetsAK4UpdatedJEC"),\n')
      newCfg.write('   bits = cms.InputTag("TriggerResults", "", "HLT"),\n')
      newCfg.write('   muonCollection= cms.InputTag("slimmedMuons"),\n')
      newCfg.write('   electronCollection = cms.InputTag("slimmedElectrons"),\n')
      newCfg.write('   metCollection = cms.InputTag("slimmedMETs"),\n')
      newCfg.write('   tauCollection = cms.InputTag("slimmedTaus"),\n')
      newCfg.write('   pileupCollection = cms.InputTag("slimmedAddPileupInfo"),\n')
      newCfg.write('   systematicType = cms.string("%s%s"),\n'%(systematic,suffix) )
      newCfg.write('   year = cms.string("%s")   #types: 2015,2016,2017,2018\n'%year)
      newCfg.write(")\n")

   newCfg.write('process.source = cms.Source("PoolSource",\n')

   ## this is going to be something that needs to be changed, but it would be a good amount of work
   newCfg.write('fileNames = cms.untracked.vstring("%s"\n'%datafile)
   newCfg.write(")\n")
   newCfg.write(")\n")
   newCfg.write('process.TFileService = cms.Service("TFileService",fileName = cms.string("clusteringAnalyzer_%s_%s_%s_output.root")\n'%(sample,year,systematic))
   newCfg.write(")\n")

   newCfg.write("process.options = cms.untracked.PSet(\n")
   newCfg.write("   wantSummary = cms.untracked.bool(True),\n")
   newCfg.write(")\n")

   newCfg.write('process.load("FWCore.MessageLogger.MessageLogger_cfi")\n')
   newCfg.write("process.MessageLogger.cerr.FwkReport.reportEvery = 1000\n")



   newCfg.write("process.p = cms.Path( process.leptonVeto * process.hadronFilter\n")

   for iii, suffix in enumerate(systematicSuffices):
      if systematic == "":
         if(iii>0):
            continue
         elif iii == 0:
            suffix = ""
      newCfg.write(" * process.clusteringAnalyzerAll_%s%s\n"%(systematic, suffix) )
   newCfg.write(")\n")
   newCfg.write("from PhysicsTools.PatAlgos.tools.helpers  import getPatAlgosToolsTask\n")
   newCfg.write("process.patAlgosToolsTask = getPatAlgosToolsTask(process)\n")
   newCfg.write("process.pathRunPatAlgos = cms.Path(process.patAlgosToolsTask)\n")




   newCfg.close()

def main():

   years   = ["2015","2016","2017","2018"]

   systematics = ["JEC", "JER",
   # "bTagWeight",    //event weights
   # "PUweight",





   ""]  # last one here is for the fully nominal cfg file

   datafiles = { '2015': { 'QCDMC1000to1500': '/store/mc/RunIISummer20UL16MiniAODAPVv2/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/3EE54B65-C726-1B48-BF34-8F36D2D2DE71.root',
                          'QCDMC1500to2000': '/store/mc/RunIISummer20UL16MiniAODAPVv2/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/0F22A9F0-4875-F645-9A1B-3D801E983B18.root',
                          'QCDMC2000toInf':  '/store/mc/RunIISummer20UL16MiniAODAPVv2/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/28F06C6D-2276-3541-9F09-1AD2E33A345F.root',
                          'TTbarMC':'/store/mc/RunIISummer20UL16MiniAODAPVv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/0906FC97-9CF7-C64E-9CCB-89BAFAA9700E.root',  
                          'dataB-ver1': '/store/data/Run2016B/JetHT/MINIAOD/ver1_HIPM_UL2016_MiniAODv2-v2/140000/1384A4D7-51E5-7049-838D-AC846072E52E.root',
                          'dataB-ver2': '/store/data/Run2016B/JetHT/MINIAOD/ver2_HIPM_UL2016_MiniAODv2-v2/120000/1C5D9138-0C43-574E-BD82-B7A1A4C8FAC4.root',
                          'dataC-HIPM': '/store/data/Run2016C/JetHT/MINIAOD/HIPM_UL2016_MiniAODv2-v2/120000/2BABA846-C55B-8742-90D8-4D971A93AE3E.root',
                          'dataD-HIPM': '/store/data/Run2016D/JetHT/MINIAOD/HIPM_UL2016_MiniAODv2-v2/120000/0B4800A5-2C27-4E4D-BC5A-913D639CC310.root',
                          'dataE-HIPM': '/store/data/Run2016E/JetHT/MINIAOD/HIPM_UL2016_MiniAODv2-v2/120000/0AF225D2-70D0-EE44-943A-7647DCF53526.root',
                          'dataF-HIPM': '/store/data/Run2016F/JetHT/MINIAOD/HIPM_UL2016_MiniAODv2-v2/130000/441955FA-E87A-664F-99D2-5C6631797F3D.root'},
               '2016': { 'QCDMC1000to1500': '/store/mc/RunIISummer20UL16MiniAODv2/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/110000/17418062-EBE8-C947-8950-E797EC69F62B.root',
                          'QCDMC1500to2000': '/store/mc/RunIISummer20UL16MiniAODv2/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/110000/2DF4DD91-8FF2-AE45-AE33-40048C9E3E75.root',
                          'QCDMC2000toInf':  '/store/mc/RunIISummer20UL16MiniAODv2/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/120000/3517E0D8-3968-9240-B445-4DBB5CD69DBE.root',
                          'TTbarMC':'/store/mc/RunIISummer20UL16MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/120000/00F39D0F-006F-5D45-A346-79EBA8D4354C.root',  
                          'dataF': '/store/data/Run2016F/JetHT/MINIAOD/UL2016_MiniAODv2-v2/140000/17267C16-E284-0D44-B0BB-D996C0CEBEB7.root',
                          'dataG': '/store/data/Run2016G/JetHT/MINIAOD/UL2016_MiniAODv2-v2/140000/003C0002-F991-6E48-8E96-2C4FD9EA8E3B.root',
                          'dataH': '/store/data/Run2016H/JetHT/MINIAOD/UL2016_MiniAODv2-v2/130000/8D2050E5-0F24-544B-A0E3-B187539117D6.root'},

   '2017': { 'QCDMC1000to1500': '/store/mc/RunIISummer20UL17MiniAODv2/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2520000/01272D1D-0108-7247-9F21-B2EB4EA22964.root',
                          'QCDMC1500to2000': '/store/mc/RunIISummer20UL17MiniAODv2/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2530000/0BC4C1BF-56C8-2C42-B288-9DE3DD3DB312.root',
                          'QCDMC2000toInf':  '/store/mc/RunIISummer20UL17MiniAODv2/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2530000/29268210-69DC-F945-BB15-4251DA417D0B.root',
                          'TTbarMC':'/store/mc/RunIISummer20UL17MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/110000/0C1A975A-BE28-4644-BFCE-4494E9484C9D.root',  
                          'dataB': '/store/data/Run2017B/JetHT/MINIAOD/UL2017_MiniAODv2-v1/260000/11CD6855-708A-0F42-8087-28EA62F18E4B.root',
                          'dataC': '/store/data/Run2017C/JetHT/MINIAOD/UL2017_MiniAODv2-v1/260000/0925457A-3C64-BD4D-BDE4-6545610FB41C.root',
                          'dataD': '/store/data/Run2017D/JetHT/MINIAOD/UL2017_MiniAODv2-v1/260000/05C72CA9-9353-C74B-AA06-337BB5B25383.root',
                          'dataE': '/store/data/Run2017E/JetHT/MINIAOD/UL2017_MiniAODv2-v1/270000/027C7BEA-A5D2-3240-A4D0-37756BFAC7DD.root',
                          'dataF': '/store/data/Run2017F/JetHT/MINIAOD/UL2017_MiniAODv2-v1/260000/06019E27-BEE3-3A4C-8EA0-1E2914ED513A.root'},
   '2018': { 'QCDMC1000to1500': '/store/mc/RunIISummer20UL18MiniAODv2/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2430000/0E582A57-8443-1D42-BBAB-85FF439FF1B3.root',
                          'QCDMC1500to2000': '/store/mc/RunIISummer20UL18MiniAODv2/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2820000/00BB6737-E608-494F-89BB-FE3D868AEDE3.root',
                          'QCDMC2000toInf':  '/store/mc/RunIISummer20UL18MiniAODv2/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2520000/081EFA0A-32E5-0040-B527-F3D5C40EB561.root',
                          'TTbarMC':'/store/mc/RunIISummer20UL18MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/0706746B-319B-8B4C-9144-15786F03DC0B.root',  
                          'dataA': '/store/data/Run2018A/JetHT/MINIAOD/UL2018_MiniAODv2-v1/260000/00B87525-94D1-C741-9B03-00528106D15A.root',
                          'dataB': '/store/data/Run2018B/JetHT/MINIAOD/UL2018_MiniAODv2-v1/260000/01CD6E06-A979-7448-AEAE-C2A1C862DE66.root',
                          'dataC': '/store/data/Run2018C/JetHT/MINIAOD/UL2018_MiniAODv2-v1/260000/091A1C55-0CB8-5440-B925-706D92C02FE1.root',
                          'dataD': '/store/data/Run2018D/JetHT/MINIAOD/UL2018_MiniAODv2-v1/250000/DAB917DB-036A-324D-88CA-6DD8AA4FEC0F.root'}

   }


   jec_file_AK4 = { '2015': { 'QCDMC1000to1500': 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC1500to2000': 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC2000toInf':  'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',
                       'TTbarMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt',  
                       'dataB-ver1': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                       'dataB-ver2': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                       'dataC-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                       'dataD-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK4PFchs.txt',
                       'dataE-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunEF_V7_DATA_Uncertainty_AK4PFchs.txt',
                       'dataF-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunEF_V7_DATA_Uncertainty_AK4PFchs.txt'},
            '2016': { 'QCDMC1000to1500': 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC1500to2000': 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC2000toInf':  'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',
                       'TTbarMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt',  
                       'dataF': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK4PFchs.txt',
                       'dataG': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK4PFchs.txt',
                       'dataH': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK4PFchs.txt'},

'2017': { 'QCDMC1000to1500': 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC1500to2000': 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC2000toInf':  'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',
                       'TTbarMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt',  
                       'dataB': 'data/JEC/2017_UL/data/Summer19UL17_RunB_V5_DATA_Uncertainty_AK4PFchs.txt',
                       'dataC': 'data/JEC/2017_UL/data/Summer19UL17_RunC_V5_DATA_Uncertainty_AK4PFchs.txt',
                       'dataD': 'data/JEC/2017_UL/data/Summer19UL17_RunD_V5_DATA_Uncertainty_AK4PFchs.txt',
                       'dataE': 'data/JEC/2017_UL/data/Summer19UL17_RunE_V5_DATA_Uncertainty_AK4PFchs.txt',
                       'dataF': 'data/JEC/2017_UL/data/Summer19UL17_RunF_V5_DATA_Uncertainty_AK4PFchs.txt'},
'2018': { 'QCDMC1000to1500': 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC1500to2000': 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                       'QCDMC2000toInf':  'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',
                       'TTbarMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt',  
                       'dataA': 'data/JEC/2018_UL/data/Summer19UL18_RunA_V5_DATA_UncertaintySources_AK4PFchs.txt',
                       'dataB': 'data/JEC/2018_UL/data/Summer19UL18_RunB_V5_DATA_Uncertainty_AK4PFchs.txt',
                       'dataC': 'data/JEC/2018_UL/data/Summer19UL18_RunC_V5_DATA_Uncertainty_AK4PFchs.txt',
                       'dataD': 'data/JEC/2018_UL/data/Summer19UL18_RunD_V5_DATA_Uncertainty_AK4PFchs.txt'}

}

   jec_file_AK8 = { '2015': { 'QCDMC1000to1500': 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC1500to2000': 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC2000toInf':  'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',
                       'TTbarMC':'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt',  
                       'dataB-ver1': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataB-ver2': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataC-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataD-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunBCD_V7_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataE-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunEF_V7_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataF-HIPM': 'data/JEC/2016_UL_preAPV/data/Summer19UL16APV_RunEF_V7_DATA_Uncertainty_AK8PFPuppi.txt'},
            '2016': { 'QCDMC1000to1500': 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC1500to2000': 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC2000toInf':  'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',
                       'TTbarMC':'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt',  
                       'dataF': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataG': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataH': 'data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK8PFPuppi.txt'},

'2017': { 'QCDMC1000to1500': 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC1500to2000': 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC2000toInf':  'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',
                       'TTbarMC':'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt',  
                       'dataB': 'data/JEC/2017_UL/data/Summer19UL17_RunB_V5_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataC': 'data/JEC/2017_UL/data/Summer19UL17_RunC_V5_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataD': 'data/JEC/2017_UL/data/Summer19UL17_RunD_V5_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataE': 'data/JEC/2017_UL/data/Summer19UL17_RunE_V5_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataF': 'data/JEC/2017_UL/data/Summer19UL17_RunF_V5_DATA_Uncertainty_AK8PFPuppi.txt'},
'2018': { 'QCDMC1000to1500': 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC1500to2000': 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                       'QCDMC2000toInf':  'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',
                       'TTbarMC':'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt',  
                       'dataA': 'data/JEC/2018_UL/data/Summer19UL18_RunA_V5_DATA_UncertaintySources_AK8PFPuppi.txt',
                       'dataB': 'data/JEC/2018_UL/data/Summer19UL18_RunB_V5_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataC': 'data/JEC/2018_UL/data/Summer19UL18_RunC_V5_DATA_Uncertainty_AK8PFPuppi.txt',
                       'dataD': 'data/JEC/2018_UL/data/Summer19UL18_RunD_V5_DATA_Uncertainty_AK8PFPuppi.txt'}

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
         samples = ["dataB-ver1","dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM" ,"dataF-HIPM","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTbarMC",
   "Suu8_chi3",
   "Suu8_chi2",
   "Suu8_chi1",
   "Suu7_chi3",
   "Suu7_chi2",
   "Suu7_chi1",
   "Suu6_chi2",
   "Suu6_chi1p5",
   "Suu6_chi1",
   "Suu5_chi2",
   "Suu5_chi1p5",
   "Suu5_chi1",
   "Suu4_chi1p5",
   "Suu4_chi1" ]
      elif year == "2016":
         samples = ["dataF","dataG","dataH","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTbarMC",
   "Suu8_chi3",
   "Suu8_chi2",
   "Suu8_chi1",
   "Suu7_chi3",
   "Suu7_chi2",
   "Suu7_chi1",
   "Suu6_chi2",
   "Suu6_chi1p5",
   "Suu6_chi1",
   "Suu5_chi2",
   "Suu5_chi1p5",
   "Suu5_chi1",
   "Suu4_chi1p5",
   "Suu4_chi1" ]
      elif year == "2017":
         samples = ["dataB","dataC","dataD","dataE","dataF","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTbarMC",
   "Suu8_chi3",
   "Suu8_chi2",
   "Suu8_chi1",
   "Suu7_chi3",
   "Suu7_chi2",
   "Suu7_chi1",
   "Suu6_chi2",
   "Suu6_chi1p5",
   "Suu6_chi1",
   "Suu5_chi2",
   "Suu5_chi1p5",
   "Suu5_chi1",
   "Suu4_chi1p5",
   "Suu4_chi1" ]
      elif year == "2018":
         samples = ["dataA","dataB", "dataC", "dataD","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTbarMC",
   "Suu8_chi3",
   "Suu8_chi2",
   "Suu8_chi1",
   "Suu7_chi3",
   "Suu7_chi2",
   "Suu7_chi1",
   "Suu6_chi2",
   "Suu6_chi1p5",
   "Suu6_chi1",
   "Suu5_chi2",
   "Suu5_chi1p5",
   "Suu5_chi1",
   "Suu4_chi1p5",
   "Suu4_chi1" ]

      for iii, sample in enumerate(samples):
         for systematic in systematics:
            if "Suu" in sample:
               continue
            makeACfg(sample, year, systematic, datafiles[year][sample], jec_file_AK4[year][sample],jec_file_AK8[year][sample])   # change input to write systematic type
   return


if __name__ == "__main__":
    main()