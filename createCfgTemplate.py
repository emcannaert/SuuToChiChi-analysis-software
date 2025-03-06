#! /usr/bin/env python

import sys
import os
import pickle
### this can be updated to create the different cfgs for each systematic
def makeACfg(sample, year, systematic__, datafile, jec_file_AK4, jec_file_AK8, all_systematics):


   includeAllBranches = False
   slimmedSelection  = True
   verbose        = False
   runSideband    = False
   doPDF = True

   if runSideband: print("WARNING: RUNNING SIDEBAND REGION.")

   if "data" in sample or "nom" not in systematic__:   # do not want to do pdf weights for data or for the JEC/JER variation runs
      doPDF = False
   isSignal = False
   if "Suu" in sample:
      isSignal = True
   systematic_ = [systematic__]
   if "Suu" in sample:
      if  systematic__ == "JEC2": return 
      elif systematic__ == "JER": return 
      #elif systematic__ == "JEC1": systematic_ = [ "JEC_FlavorQCD", "JEC_RelativeBal", "JEC_HF", "JEC_BBEC1", "JEC_EC2", "JEC_BBEC1_year", "JEC_EC2_year", "JEC_Absolute_year", "JEC_HF_year", "JEC_RelativeSample_year", "JEC"]
      #elif systematic__ == "nom": systematic_ =  ["nom", "JER_eta193", "JER_193eta25", "JER", "JEC_AbsoluteCal","JEC_AbsoluteTheory", "JEC_AbsolutePU", "JEC_Absolute" ]        #all_systematics


      ### COMMENT OUT THESE EVENTUALLY
      #elif systematic__ == "JEC1": systematic_ = [ "JEC_FlavorQCD", "JEC_RelativeBal", "JEC_HF", "JEC_BBEC1", "JEC_EC2", "JEC_BBEC1_year", "JEC_EC2_year", "JEC_Absolute_year", "JEC_HF_year", "JEC_RelativeSample_year", "JEC"]
      #elif systematic__ == "nom": systematic_ =  ["nom", "JER_eta193", "JER_193eta25", "JER", "JEC_AbsoluteCal","JEC_AbsoluteTheory", "JEC_AbsolutePU", "JEC_Absolute" ]        #all_systematics

      ### AND REPLACE WITH THESE
      elif systematic__ == "JEC1": systematic_ = [ "JEC_FlavorQCD", "JEC_RelativeBal",  "JEC_BBEC1_year",  "JEC_Absolute_year", "JEC_RelativeSample_year", "JEC", "JEC_AbsoluteScale", "JEC_Fragmentation", "JEC_AbsoluteTheory"]
      elif systematic__ == "nom": systematic_ =  ["nom", "JER_eta193", "JER_193eta25", "JER", "JEC_AbsoluteCal", "JEC_AbsolutePU", "JEC_Absolute", "JEC_AbsoluteMPFBias","JEC_RelativeFSR", "JEC_BBEC1" ]        #all_systematics

      else:        #elif systematic__ == "nom": systematic_ =  ["nom", "JER_eta193", "JER_193eta25", "JER" ]        #all_systematics
         print("ERROR: Suu systematic is neither JEC nor nom.")
         return

   ## comment these out eventually 
   #elif systematic__ == "JEC1": systematic_ =   [ "JEC_FlavorQCD", "JEC_RelativeBal", "JEC_HF", "JEC_BBEC1", "JEC_EC2", "JEC_BBEC1_year", "JEC_EC2_year"]
   #elif systematic__ == "JEC2":   systematic_ = ["JEC_Absolute_year", "JEC_HF_year", "JEC_RelativeSample_year", "JEC_AbsoluteCal","JEC_AbsoluteTheory", "JEC_AbsolutePU", "JEC_Absolute", "JEC"]

   # and replace with these 
   elif systematic__ == "JEC1": systematic_ =   [ "JEC_FlavorQCD", "JEC_RelativeBal","JEC_BBEC1_year",  "JEC_AbsoluteScale", "JEC_Fragmentation", "JEC_AbsoluteMPFBias","JEC_RelativeFSR","JEC_AbsoluteTheory" ]
   elif systematic__ == "JEC2": systematic_ =   [ "JEC_Absolute_year",  "JEC_RelativeSample_year", "JEC_AbsoluteCal", "JEC_AbsolutePU", "JEC_Absolute", "JEC_BBEC1", "JEC"]
   elif systematic__ == "JER":  systematic_ =   [  "JER_eta193", "JER_193eta25", "JER"] ## we aren't using JERs for eta > 2.5, so no need for the other 4 uncertainties

   apply_pu_ID = True
   doTopPtReweight = False
   if "TTJetsMC" in sample or "TTTo" in sample:
      doTopPtReweight = True
   # need to change trigger for yhears
   trigger = ""
   if year == "2018" or year == "2017":
      trigger = "HLT_PFHT1050_v"
   elif year == "2015" or year == "2016":
      trigger = "HLT_PFHT900_v"

   output_dir = ""
   if "Suu" in sample:
      output_dir = "allCfgs/signalCfgs"
   else:
      output_dir = "allCfgs"
   if isSignal:
      if "JEC" in systematic__:
         newCfg = open("%s/clusteringAnalyzer_%s_%s_%s_cfg.py"%(output_dir,sample,year,systematic__),"w")
      else: 
         newCfg = open("%s/clusteringAnalyzer_%s_%s_cfg.py"%(output_dir,sample,year),"w")
   elif systematic__ == "":
      newCfg = open("%s/clusteringAnalyzer_%s_%s_%scfg.py"%(output_dir,sample,year, systematic__),"w")
   elif systematic__ == "nom":
      newCfg = open("%s/clusteringAnalyzer_%s_%s_cfg.py"%(output_dir,sample,year),"w")
   else:
      newCfg = open("%s/clusteringAnalyzer_%s_%s_%s_cfg.py"%(output_dir,sample,year,systematic__),"w")
   if year == "2015" or year == "2016":
      jet_veto_map_name = "h2hot_ul16_plus_hbm2_hbp12_qie11"
      jet_veto_map_file = "data/jetVetoMaps/hotjets-UL16.root"
   elif year == "2017":
      jet_veto_map_name = "h2hot_ul17_plus_hep17_plus_hbpw89"
      jet_veto_map_file = "data/jetVetoMaps/hotjets-UL17_v2.root"
   elif year == "2018":
      jet_veto_map_name = "h2hot_ul18_plus_hem1516_and_hbp2m1"
      jet_veto_map_file = "data/jetVetoMaps/hotjets-UL18.root"

   newCfg.write("from PhysicsTools.PatAlgos.tools.helpers  import getPatAlgosToolsTask\n")
   newCfg.write("import FWCore.ParameterSet.Config as cms\n")

   newCfg.write('process = cms.Process("analysis")\n')
   newCfg.write("from Configuration.AlCa.GlobalTag import GlobalTag\n")  

   newCfg.write("process.patAlgosToolsTask = getPatAlgosToolsTask(process)\n")

   newCfg.write("process.load('Configuration.StandardSequences.Services_cff')\n")
   newCfg.write('process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")\n')
   newCfg.write("process.load('JetMETCorrections.Configuration.JetCorrectors_cff')\n")
   newCfg.write("process.load('JetMETCorrections.Configuration.CorrectedJetProducers_cff')\n")
   newCfg.write("process.load('JetMETCorrections.Configuration.CorrectedJetProducersDefault_cff')\n")
   newCfg.write('process.load("JetMETCorrections.Configuration.JetCorrectionServices_cff")\n')
   newCfg.write('process.load("JetMETCorrections.Configuration.JetCorrectionServicesAllAlgos_cff")\n')
   #if doTopPtReweight:
   #  newCfg.write('#top pt reweighting\n')
   #  newCfg.write('process.load("TopQuarkAnalysis.TopEventProducers.sequences.ttGenEvent_cff")\n')

   newCfg.write('from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection\n')
   """
    Data: 106X_dataRun2_v37
    MC 2016APV: 106X_mcRun2_asymptotic_v17
    MC 2016: 106X_mcRun2_asymptotic_v17
    MC 2017: 106X_mc2017_realistic_v10
    MC 2018: 106X_upgrade2018_realistic_v16_L1v1 
   """

   # global tags
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

   newCfg.write("from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD\n")




   
   newCfg.write("################# JEC ################\n")
   ######### AK8 jets #########
   if "data" in sample: newCfg.write("corrLabels = ['L2Relative', 'L3Absolute', 'L2L3Residual']\n")  ## ,'L3Absolute' -> should these be included?
   else: newCfg.write("corrLabels = ['L2Relative', 'L3Absolute']\n")  ## ,'L3Absolute' -> should these be included?
   newCfg.write("from PhysicsTools.PatAlgos.tools.jetTools import *\n")
   newCfg.write("from RecoBTag.ONNXRuntime.pfDeepBoostedJet_cff import *\n")
   newCfg.write("updateJetCollection(\n")
   newCfg.write(" process,\n")
   newCfg.write(" jetSource = cms.InputTag('slimmedJetsAK8'),\n")
   newCfg.write(" labelName = 'AK8',\n")
   newCfg.write(" jetCorrections = ('AK8PFPuppi', cms.vstring(corrLabels), 'None'), #previous corrections: 'L2Relative', 'L3Absolute', 'L2L3Residual'\n")
   newCfg.write(" postfix = 'UpdatedJEC',\n")
   newCfg.write(" printWarning = False\n")
   newCfg.write(")\n")
   ######### AK4 jets #########
   if "data" in sample:  newCfg.write("corrLabels_AK4 = ['L1FastJet', 'L2Relative', 'L3Absolute','L2L3Residual']\n") # 'L3Absolute'
   else: newCfg.write("corrLabels_AK4 = ['L1FastJet', 'L2Relative', 'L3Absolute']\n") # 'L3Absolute'
   newCfg.write("updateJetCollection(\n")
   newCfg.write(" process,\n")
   newCfg.write(" jetSource = cms.InputTag('slimmedJets'),\n")
   newCfg.write(" labelName = 'AK4',\n")
   newCfg.write(" jetCorrections = ('AK4PFchs', cms.vstring(corrLabels_AK4), 'None'),\n")
   newCfg.write(" postfix = 'UpdatedJEC',\n")
   newCfg.write(" printWarning = False\n")
   newCfg.write(")  \n")





   if apply_pu_ID:
      newCfg.write("################# Jet PU ID ################\n")
      newCfg.write('from RecoJets.JetProducers.PileupJetID_cfi import pileupJetId\n')
      if year == "2016":
         newCfg.write('from RecoJets.JetProducers.PileupJetID_cfi import _chsalgos_106X_UL16   #   (or _chsalgos_106X_UL16APV for APV samples)\n')
      elif year == "2017":
         newCfg.write('from RecoJets.JetProducers.PileupJetID_cfi import _chsalgos_106X_UL17\n')
      elif year == "2018":
         newCfg.write('from RecoJets.JetProducers.PileupJetID_cfi import _chsalgos_106X_UL18\n')
      newCfg.write('process.load("RecoJets.JetProducers.PileupJetID_cfi")\n')
      newCfg.write('process.pileupJetIdUpdated = process.pileupJetId.clone( \n')
      newCfg.write('jets=cms.InputTag("updatedPatJetsAK4UpdatedJEC"),  #should be the name of the post-JEC jet collection\n')
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
      newCfg.write('updateJetCollection(    # running in unscheduled mode, need to manually update collection\n')
      newCfg.write(' process,\n')
      newCfg.write(' labelName = "PileupJetID",\n')
      newCfg.write(' jetSource = cms.InputTag("updatedPatJetsAK4UpdatedJEC"),\n')
      newCfg.write(')\n')
      newCfg.write('process.updatedPatJetsPileupJetID.userData.userInts.src = ["pileupJetIdUpdated:fullId"]\n')

   newCfg.write('process.content = cms.EDAnalyzer("EventContentAnalyzer")\n')

   newCfg.write("##############################################################################\n")
   newCfg.write('process.leptonVeto = cms.EDFilter("leptonVeto",\n')
   newCfg.write(' muonCollection= cms.InputTag("slimmedMuons"),\n')
   newCfg.write(' electronCollection = cms.InputTag("slimmedElectrons"),\n')
   newCfg.write(' metCollection = cms.InputTag("slimmedMETs"),\n')
   newCfg.write(' tauCollection = cms.InputTag("slimmedTaus")\n')
   newCfg.write(")\n")





   ### prefiring weights
   if year == "2015":
      prefire_ecal_era = "UL2016preVFP"
      prefire_muon_era = "2016preVFP"
   elif year == "2016":
      prefire_ecal_era = "UL2016postVFP"
      prefire_muon_era = "2016postVFP"
   elif year == "2017":
      prefire_ecal_era = "UL2017BtoF"
      prefire_muon_era = "20172018"
   elif year == "2018":
      prefire_ecal_era = "None"
      prefire_muon_era = "20172018"

   newCfg.write("from PhysicsTools.PatUtils.l1PrefiringWeightProducer_cfi import l1PrefiringWeightProducer\n")
   newCfg.write("process.prefiringweight = l1PrefiringWeightProducer.clone(\n")

   if apply_pu_ID:
      newCfg.write("TheJets = cms.InputTag('updatedPatJetsPileupJetID'), #updatedPatJetsAK4UpdatedJEC \n")
   else:
      newCfg.write("TheJets = cms.InputTag('updatedPatJetsAK4UpdatedJEC'), #updatedPatJetsAK4UpdatedJEC \n")
   
   newCfg.write("DataEraECAL = cms.string('%s'), #Use 2016BtoH for 2016\n"%prefire_ecal_era)
   newCfg.write("DataEraMuon = cms.string('%s'), #Use 2016 for 2016\n"%prefire_muon_era)
   newCfg.write("UseJetEMPt = cms.bool(False),\n")
   newCfg.write("PrefiringRateSystematicUnctyECAL = cms.double(0.2),\n")
   newCfg.write("PrefiringRateSystematicUnctyMuon = cms.double(0.2)\n")
   newCfg.write(")\n")

   for systematic in systematic_:
      """
      # NO LONGER DOING HADRON FILTER, this messes with systematics 
      if not isSignal:  # do NOT run the hadron filter for signal, this messes with systematic stuff
         newCfg.write('process.hadronFilter_%s = cms.EDFilter("hadronFilter",\n'%systematic)
         newCfg.write(' year = cms.string("%s"),\n'%year)

         newCfg.write(' fatJetCollection = cms.InputTag("updatedPatJetsAK8UpdatedJEC"),\n')
         newCfg.write(' metCollection = cms.InputTag("slimmedMETs"),\n')
         if apply_pu_ID:
            newCfg.write(' jetCollection = cms.InputTag("selectedUpdatedPatJetsPileupJetID"),\n')
         else:
            newCfg.write(' jetCollection = cms.InputTag("updatedPatJetsAK4UpdatedJEC"),\n')
         newCfg.write(' bits = cms.InputTag("TriggerResults", "", "HLT"),\n')
         newCfg.write(' triggers = cms.string("%s"),\n'%trigger)
         newCfg.write(' systematicType = cms.string("%s"),\n'%systematic)
         newCfg.write(' JECUncert_AK4_path = cms.FileInPath("%s"),\n'%jec_file_AK4)
         if apply_pu_ID:
            newCfg.write(' doPUID = cms.bool(True),\n')
         else:
            newCfg.write(' doPUID = cms.bool(False),\n')
         newCfg.write(' runType = cms.string("%s")  #types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTToHadronicMC, TTToSemiLeptonic, TTToLeptonic, DataA, etc. , Suu8_chi3, etc.\n'%sample)
         newCfg.write(")\n")

      """
      systematicSuffices = ["_up", "_down"]
      for iii, suffix in enumerate(systematicSuffices):

         if systematic == "nom":  # want to have only one round of the analyzer run with no suffix to represent the case of all systematics being nominal
            if(iii>0):
               continue
            elif iii == 0:
               suffix = ""


         newCfg.write('process.clusteringAnalyzerAll_%s%s = cms.EDAnalyzer("clusteringAnalyzerAll",\n'%(systematic, suffix) )
         """
         if "QCD" in sample:
            newCfg.write(' runType = cms.string("QCDMC"), #types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTbarMC, DataA, etc. , Suu8_chi3, etc.\n')
         elif "TTbar" in sample:
            newCfg.write(' runType = cms.string("TTbarMC"),  #types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTbarMC, DataA, etc. , Suu8_chi3, etc.\n')
         elif "Suu" in sample:
            newCfg.write(' runType = cms.string("SigMC"), #types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTbarMC, DataA, etc. , Suu8_chi3, etc.\n')
         elif "data" in sample:
            newCfg.write(' runType = cms.string("Data"),  #types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTbarMC, DataA, etc. , Suu8_chi3, etc.\n')
         else:
            print("something failed with writing runType.", sample ) 
         """
         newCfg.write(' runType = cms.string("%s"), #types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTbarMC, DataA, etc. , Suu8_chi3, etc.\n'%sample)
         if "MC" in sample or "Suu" in sample:
            newCfg.write(' genPartCollection = cms.InputTag("prunedGenParticles"),\n')
            newCfg.write('  genParticles = cms.InputTag("genParticles"),\n')
            newCfg.write('  packedGenParticles = cms.InputTag("packedGenParticles"),\n')


         newCfg.write(" BESTname = cms.string('BESTGraph'),  BESTpath = cms.FileInPath('data/BEST_models/constantgraph_combine.pb'),\n")   #OLD constantgraph_%s.pb

         newCfg.write(" BESTscale = cms.FileInPath('data/BESTScalerParameters_all_mass_combine.txt'),\n") # OLD: BESTScalerParameters_all_mass_%s.txt
         if year == "2015":
            newCfg.write(" PUfile_path = cms.FileInPath('data/POG/LUM/2016preVFP_UL/puWeights.json'),\n")
         elif year == "2016":
            newCfg.write(" PUfile_path = cms.FileInPath('data/POG/LUM/2016postVFP_UL/puWeights.json'),\n")
         elif year == "2017":
            newCfg.write(" PUfile_path = cms.FileInPath('data/POG/LUM/2017_UL/puWeights.json'),\n")
         elif year == "2018":
            newCfg.write(" PUfile_path = cms.FileInPath('data/POG/LUM/2018_UL/puWeights.json'),\n")

         
         #should this be for data and MC?
         if "MC" in sample or "Suu" in sample:
            """
            if "TTTo" in sample or "ST_" in sample:
               bTagSF_sample = sample[:-2]
            elif "Suu" in sample:
               bTagSF_sample = "QCDMC2000toInf"  # for now use the QCD2000toInf efficiency maps in the b-tag SF calculation, don't have these yet for signal
            else:
               bTagSF_sample = sample
            """
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
            else:
               print("ERROR: b tagging SF sample is not found. Sample = %s"%sample)
               return


            newCfg.write(" bTagEff_path = cms.FileInPath('data/btaggingEffMaps/btag_efficiency_map_%s_combined_%s.root'),\n"%(bTagSF_sample,year))
            if year == "2015":
               newCfg.write(" bTagSF_path = cms.FileInPath('data/bTaggingSFs/2016preVFP_UL/btagging.json'),\n")
            elif year == "2016":
               newCfg.write(" bTagSF_path = cms.FileInPath('data/bTaggingSFs/2016postVFP_UL/btagging.json'),\n")
            elif year == "2017":
               newCfg.write(" bTagSF_path = cms.FileInPath('data/bTaggingSFs/2017_UL/btagging.json'),\n")
            elif year == "2018":
               newCfg.write(" bTagSF_path = cms.FileInPath('data/bTaggingSFs/2018_UL/btagging.json'),\n")

         newCfg.write(' JECUncert_AK8_path = cms.FileInPath("%s"),\n'%jec_file_AK8)
         newCfg.write(' JECUncert_AK4_path = cms.FileInPath("%s"),\n'%jec_file_AK4)

         newCfg.write(' fatJetCollection = cms.InputTag("updatedPatJetsAK8UpdatedJEC"),\n')
         if apply_pu_ID:
            newCfg.write(' jetCollection = cms.InputTag("updatedPatJetsPileupJetID"),\n') # CHANGED FROM selectedUpdatedPatJetsPileupJetID
         else:
            newCfg.write(' jetCollection = cms.InputTag("updatedPatJetsAK4UpdatedJEC"),\n')
         newCfg.write(' muonCollection= cms.InputTag("slimmedMuons"),\n')
         newCfg.write(' electronCollection = cms.InputTag("slimmedElectrons"),\n')
         newCfg.write(' metCollection = cms.InputTag("slimmedMETs"),\n')
         newCfg.write(' tauCollection = cms.InputTag("slimmedTaus"),\n')
         newCfg.write(' pileupCollection = cms.InputTag("slimmedAddPileupInfo"),\n')
         newCfg.write(' systematicType = cms.string("%s%s"),\n'%(systematic,suffix) )
         newCfg.write(' jetVetoMapFile = cms.FileInPath("%s"),\n'%(jet_veto_map_file) )
         newCfg.write(' jetVetoMapName = cms.string("%s"),\n'%(jet_veto_map_name) )
         newCfg.write(' includeAllBranches = cms.bool(%s),\n'%(includeAllBranches ))
         newCfg.write(' slimmedSelection   = cms.bool(%s),\n'%(slimmedSelection) )
         newCfg.write(' verbose            = cms.bool(%s),\n'%(verbose) )
         newCfg.write(' runSideband            = cms.bool(%s),\n'%(runSideband) )
         newCfg.write(' year = cms.string("%s"), #types: 2015,2016,2017,2018\n'%year)
         newCfg.write(' genEventInfoTag=cms.InputTag("generator"),\n')
         newCfg.write(' lheEventInfoTag=cms.InputTag("externalLHEProducer"),\n')
         newCfg.write(' bits = cms.InputTag("TriggerResults", "", "HLT"),\n')
         newCfg.write(' triggers = cms.string("%s"),\n'%trigger)
         if apply_pu_ID:
            newCfg.write(' doPUID = cms.bool(True),\n')
         else:
            newCfg.write(' doPUID = cms.bool(False),\n')
         newCfg.write('  doPDF = cms.bool(%s)\n'%doPDF)

         newCfg.write(")\n")

         # this didn't work, so unneeded
         #if doTopPtReweight:
         #  newCfg.write('# top pt reweighting stuff\n')
         #  newCfg.write('process.decaySubset.fillMode = cms.string("kME")\n')
         #  newCfg.write('process.clusteringAnalyzerAll_%s%s.ttGenEvent = cms.InputTag("genEvt")\n'%(systematic, suffix))



   newCfg.write('process.source = cms.Source("PoolSource",\n')

   ## this is going to be something that needs to be changed, but it would be a good amount of work
   newCfg.write('fileNames = cms.untracked.vstring("%s"\n'%datafile)
   newCfg.write(")\n")
   newCfg.write(")\n")



   use_syst = systematic__

   if "Suu" in sample:
      use_syst = ""
      if systematic == "nom":
         use_syst = "nom"
      newCfg.write('process.TFileService = cms.Service("TFileService",fileName = cms.string("%s_%s_combined.root")\n'%(sample,year))
   else:
      if systematic__ == "nom":
         use_syst = "nom"
      newCfg.write('process.TFileService = cms.Service("TFileService",fileName = cms.string("clusteringAnalyzer_%s_%s_%s_output.root")\n'%(sample,year,use_syst))

   newCfg.write(")\n")

   newCfg.write("process.options = cms.untracked.PSet(\n")
   newCfg.write(" wantSummary = cms.untracked.bool(True),\n")
   newCfg.write(")\n")

   newCfg.write('process.load("FWCore.MessageLogger.MessageLogger_cfi")\n')
   newCfg.write("process.MessageLogger.cerr.FwkReport.reportEvery = 1000\n")



   newCfg.write("process.p = cms.Path(  ")
   if apply_pu_ID:
      newCfg.write("process.pileupJetIdUpdated * ")
   #if doTopPtReweight:
   #  newCfg.write("process.makeGenEvt* ")
      
   newCfg.write("process.leptonVeto * process.prefiringweight  ")
            ########if you need to check the collections, add this to the path:  process.content
      
   for systematic in systematic_:

      for iii, suffix in enumerate(systematicSuffices):
         if systematic == "nom":
            if(iii>0):
               continue
            elif iii == 0:
               suffix = ""

         #if not isSignal:
         #  newCfg.write("process.hadronFilter * \n ")
         newCfg.write(" * process.clusteringAnalyzerAll_%s%s\n"%(systematic, suffix) )
   newCfg.write(")\n")
   newCfg.write("process.pathRunPatAlgos = cms.Path(process.patAlgosToolsTask)\n")




   newCfg.close()

def main():

   years = ["2015","2016","2017","2018"]

   ### uncertaintites for JEC
   ### FlavorQCD, RelativeBal, HF, BBEC1, EC2, Absolute, BBEC1_2018, EC2_2018, Absolute_2018, HF_2018, RelativeSample_2018

   #systematics = [ "JEC_FlavorQCD", "JEC_RelativeBal", "JEC_HF", "JEC_BBEC1", "JEC_EC2", "JEC_Absolute", "JEC_BBEC1_year", "JEC_EC2_year", "JEC_Absolute_year", "JEC_HF_year", "JEC_RelativeSample_year", "JER_eta193", "JER_193eta25",  "JEC","JER","nom" ]
   systematics = [  "JEC1","JEC2","JER","nom" ]

   # "bTagWeight",    //event weights
   # "PUweight",





     # last one here is for the fully nominal cfg file
   """datafile = [ 
      "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu8TeV_chi3TeV_UL-ALLDECAY.root",
      "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu8TeV_chi2TeV_UL-ALLDECAY.root",
      "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu8TeV_chi1TeV_UL-ALLDECAY.root",
      "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu7TeV_chi3TeV_UL-ALLDECAY.root",
      "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu7TeV_chi2TeV_UL-ALLDECAY.root",
      "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu7TeV_chi1TeV_UL-ALLDECAY.root",
      "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu6TeV_chi2TeV_UL-ALLDECAY.root",
      "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu6TeV_chi1p5TeV_UL-ALLDECAY.root",
      "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu6TeV_chi1TeV_UL-ALLDECAY.root",
      "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu5TeV_chi2TeV_UL-ALLDECAY.root",
      "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu5TeV_chi1p5TeV_UL-ALLDECAY.root",
      "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu5TeV_chi1TeV_UL-ALLDECAY.root",
      "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu4TeV_chi1p5TeV_UL-ALLDECAY.root",
      "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu4TeV_chi1TeV_UL-ALLDECAY.root"]"""

   datafiles = { '2015': { 'QCDMC1000to1500': '/store/mc/RunIISummer20UL16MiniAODAPVv2/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/3EE54B65-C726-1B48-BF34-8F36D2D2DE71.root',
                          'QCDMC1500to2000': '/store/mc/RunIISummer20UL16MiniAODAPVv2/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/0F22A9F0-4875-F645-9A1B-3D801E983B18.root',
                          'QCDMC2000toInf':  '/store/mc/RunIISummer20UL16MiniAODAPVv2/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/28F06C6D-2276-3541-9F09-1AD2E33A345F.root',
                          'TTToHadronicMC':'/store/mc/RunIISummer20UL16MiniAODAPVv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/0906FC97-9CF7-C64E-9CCB-89BAFAA9700E.root',  
                          'TTToSemiLeptonicMC': '/store/mc/RunIISummer20UL16MiniAODAPVv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/0906FC97-9CF7-C64E-9CCB-89BAFAA9700E.root',
                          'TTToLeptonicMC': '/store/mc/RunIISummer20UL16MiniAODAPVv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/0906FC97-9CF7-C64E-9CCB-89BAFAA9700E.root',
                          'ST_t-channel-top_inclMC':'/store/mc/RunIISummer20UL16MiniAODAPVv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/0906FC97-9CF7-C64E-9CCB-89BAFAA9700E.root',
                           'ST_t-channel-antitop_inclMC':'/store/mc/RunIISummer20UL16MiniAODAPVv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/0906FC97-9CF7-C64E-9CCB-89BAFAA9700E.root',
                           'ST_s-channel-hadronsMC':'/store/mc/RunIISummer20UL16MiniAODAPVv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/0906FC97-9CF7-C64E-9CCB-89BAFAA9700E.root',
                           'ST_s-channel-leptonsMC':'/store/mc/RunIISummer20UL16MiniAODAPVv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/0906FC97-9CF7-C64E-9CCB-89BAFAA9700E.root',
                           'ST_tW-antiTop_inclMC':'/store/mc/RunIISummer20UL16MiniAODAPVv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/0906FC97-9CF7-C64E-9CCB-89BAFAA9700E.root',
                           'ST_tW-top_inclMC':'/store/mc/RunIISummer20UL16MiniAODAPVv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/0906FC97-9CF7-C64E-9CCB-89BAFAA9700E.root',
                           "TTJetsMCHT1200to2500": '/store/mc/RunIISummer20UL16MiniAODAPVv2/TTJetsMC_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v2/2430000/036CEBD3-4911-DE4E-91BC-263C300210E1.root', 
                           "TTJetsMCHT2500toInf": '/store/mc/RunIISummer20UL16MiniAODAPVv2/TTJetsMC_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v2/40000/01142FB6-5BF4-9E47-BC22-A6269CC0CD32.root',
                          'dataB-ver1': '/store/data/Run2016B/JetHT/MINIAOD/ver1_HIPM_UL2016_MiniAODv2-v2/140000/1384A4D7-51E5-7049-838D-AC846072E52E.root',
                          'dataB-ver2': '/store/data/Run2016B/JetHT/MINIAOD/ver2_HIPM_UL2016_MiniAODv2-v2/120000/1C5D9138-0C43-574E-BD82-B7A1A4C8FAC4.root',
                          'dataC-HIPM': '/store/data/Run2016C/JetHT/MINIAOD/HIPM_UL2016_MiniAODv2-v2/120000/2BABA846-C55B-8742-90D8-4D971A93AE3E.root',
                          'dataD-HIPM': '/store/data/Run2016D/JetHT/MINIAOD/HIPM_UL2016_MiniAODv2-v2/120000/0B4800A5-2C27-4E4D-BC5A-913D639CC310.root',
                          'dataE-HIPM': '/store/data/Run2016E/JetHT/MINIAOD/HIPM_UL2016_MiniAODv2-v2/120000/0AF225D2-70D0-EE44-943A-7647DCF53526.root',
                          'dataF-HIPM': '/store/data/Run2016F/JetHT/MINIAOD/HIPM_UL2016_MiniAODv2-v2/130000/441955FA-E87A-664F-99D2-5C6631797F3D.root',
                           "Suu8_chi3": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu8TeV_chi3TeV_UL-ALLDECAY.root",
                           "Suu8_chi2":  "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu8TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu8_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu8TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu7_chi3": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu7TeV_chi3TeV_UL-ALLDECAY.root",
                           "Suu7_chi2": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu7TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu7_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu7TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu6_chi2": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu6TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu6_chi1p5":  "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu6TeV_chi1p5TeV_UL-ALLDECAY.root",
                           "Suu6_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu6TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu5_chi2":  "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu5TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu5_chi1p5": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu5TeV_chi1p5TeV_UL-ALLDECAY.root",
                           "Suu5_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu5TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu4_chi1p5": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu4TeV_chi1p5TeV_UL-ALLDECAY.root",
                           "Suu4_chi1" : "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu4TeV_chi1TeV_UL-ALLDECAY.root" ,
                            "WJetsMC_LNu-HT800to1200":  "/store/mc/RunIISummer20UL16MiniAODAPVv2/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/112568C4-56D6-0A40-8FD3-022F2C63130C.root" ,
                           "WJetsMC_LNu-HT1200to2500": "/store/mc/RunIISummer20UL16MiniAODAPVv2/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/120000/0F5E3868-A595-1C43-93FC-5550AC330918.root" ,
                           "WJetsMC_LNu-HT2500toInf": "/store/mc/RunIISummer20UL16MiniAODAPVv2/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v2/100000/1E29C378-733E-F84F-932F-0CE0B3BD3682.root" ,
                           "WJetsMC_QQ-HT800toInf" :"/store/mc/RunIISummer20UL16MiniAODAPVv2/WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v2/230000/023153B0-7563-8540-AEB8-7A7C980DD714.root"  ,
                           "TTJetsMCHT800to1200": "/store/mc/RunIISummer20UL16MiniAODAPVv2/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v2/2430000/45043110-263C-3447-B965-593802DEC8F9.root",
                           "WW_MC": "/store/mc/RunIISummer20UL16MiniAODAPVv2/WW_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/70000/76375D0A-3EEC-A34D-B12B-ED7D9DF0A04B.root",
                           "ZZ_MC": "/store/mc/RunIISummer20UL16MiniAODAPVv2/ZZ_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/70000/BFC826A3-5055-2F47-8C06-5B19FDF0BBBE.root"
                                    },

               '2016': { 'QCDMC1000to1500': '/store/mc/RunIISummer20UL16MiniAODv2/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/110000/17418062-EBE8-C947-8950-E797EC69F62B.root',
                          'QCDMC1500to2000': '/store/mc/RunIISummer20UL16MiniAODv2/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/110000/2DF4DD91-8FF2-AE45-AE33-40048C9E3E75.root',
                          'QCDMC2000toInf':  '/store/mc/RunIISummer20UL16MiniAODv2/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/120000/3517E0D8-3968-9240-B445-4DBB5CD69DBE.root',
                          'TTToHadronicMC':'/store/mc/RunIISummer20UL16MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/120000/00F39D0F-006F-5D45-A346-79EBA8D4354C.root',  
                          'TTToSemiLeptonicMC':'/store/mc/RunIISummer20UL16MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/120000/00F39D0F-006F-5D45-A346-79EBA8D4354C.root',
                          'TTToLeptonicMC':'/store/mc/RunIISummer20UL16MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/120000/00F39D0F-006F-5D45-A346-79EBA8D4354C.root',
                          "TTJetsMCHT1200to2500": '/store/mc/RunIISummer20UL16MiniAODv2/TTJetsMC_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v2/40000/01A08156-C2BE-F04A-9BE4-18B42897EC29.root', 
                           "TTJetsMCHT2500toInf": '/store/mc/RunIISummer20UL16MiniAODv2/TTJetsMC_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v2/2430000/0C16029D-16A7-474D-851C-BC8473113E46.root',
                          'ST_t-channel-top_inclMC':'/TTToHadronicMC_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
                           'ST_t-channel-antitop_inclMC':'/TTToHadronicMC_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
                           'ST_s-channel-hadronsMC':'/TTToHadronicMC_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
                           'ST_s-channel-leptonsMC':'/TTToHadronicMC_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
                           'ST_tW-antiTop_inclMC':'/TTToHadronicMC_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
                           'ST_tW-top_inclMC':'/TTToHadronicMC_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',
                          'dataF': '/store/data/Run2016F/JetHT/MINIAOD/UL2016_MiniAODv2-v2/140000/17267C16-E284-0D44-B0BB-D996C0CEBEB7.root',
                          'dataG': '/store/data/Run2016G/JetHT/MINIAOD/UL2016_MiniAODv2-v2/140000/003C0002-F991-6E48-8E96-2C4FD9EA8E3B.root',
                          'dataH': '/store/data/Run2016H/JetHT/MINIAOD/UL2016_MiniAODv2-v2/130000/8D2050E5-0F24-544B-A0E3-B187539117D6.root',
                          "Suu8_chi3": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu8TeV_chi3TeV_UL-ALLDECAY.root",
                           "Suu8_chi2":  "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu8TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu8_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu8TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu7_chi3": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu7TeV_chi3TeV_UL-ALLDECAY.root",
                           "Suu7_chi2": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu7TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu7_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu7TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu6_chi2": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu6TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu6_chi1p5":  "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu6TeV_chi1p5TeV_UL-ALLDECAY.root",
                           "Suu6_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu6TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu5_chi2":  "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu5TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu5_chi1p5": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu5TeV_chi1p5TeV_UL-ALLDECAY.root",
                           "Suu5_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu5TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu4_chi1p5": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu4TeV_chi1p5TeV_UL-ALLDECAY.root",
                           "Suu4_chi1" : "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu4TeV_chi1TeV_UL-ALLDECAY.root",
                           "WJetsMC_LNu-HT800to1200": "/store/mc/RunIISummer20UL16MiniAODv2/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/120000/79C21123-A36B-1F43-823C-2F2897754D77.root"   ,
                           "WJetsMC_LNu-HT1200to2500": "/store/mc/RunIISummer20UL16MiniAODv2/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/230000/CBA9B1F7-8AB0-404A-8964-FE973731302C.root" ,
                           "WJetsMC_LNu-HT2500toInf": "/store/mc/RunIISummer20UL16MiniAODv2/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v2/120000/79797602-9555-0F44-BD7D-8BD21DD23DAB.root"  ,
                           "WJetsMC_QQ-HT800toInf":  "/store/mc/RunIISummer20UL16MiniAODv2/WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v2/2430000/053EAB96-2CF5-9F4C-8B00-6A23FEECA72D.root"  ,
                           "TTJetsMCHT800to1200":  "/store/mc/RunIISummer20UL16MiniAODv2/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v2/2530000/06652515-959A-914C-BC31-B789F9E24E43.root",
                           "WW_MC": "/store/mc/RunIISummer20UL16MiniAODv2/WW_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/70000/E0BE095D-BCC7-864C-B70E-84D75AD77D32.root",
                           "ZZ_MC": "/store/mc/RunIISummer20UL16MiniAODv2/ZZ_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/280000/D5A40A37-7023-3248-9F06-883E9641D968.root"    },

   '2017': { 'QCDMC1000to1500': '/store/mc/RunIISummer20UL17MiniAODv2/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2520000/01272D1D-0108-7247-9F21-B2EB4EA22964.root',
                          'QCDMC1500to2000': '/store/mc/RunIISummer20UL17MiniAODv2/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2530000/0BC4C1BF-56C8-2C42-B288-9DE3DD3DB312.root',
                          'QCDMC2000toInf':  '/store/mc/RunIISummer20UL17MiniAODv2/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2530000/29268210-69DC-F945-BB15-4251DA417D0B.root',
                          'TTToHadronicMC':'/store/mc/RunIISummer20UL17MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/110000/0C1A975A-BE28-4644-BFCE-4494E9484C9D.root',  
                          'TTToSemiLeptonicMC': '/store/mc/RunIISummer20UL17MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/110000/0C1A975A-BE28-4644-BFCE-4494E9484C9D.root',
                          'TTToLeptonicMC':'/store/mc/RunIISummer20UL17MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/110000/0C1A975A-BE28-4644-BFCE-4494E9484C9D.root',
                          "TTJetsMCHT1200to2500": '/store/mc/RunIISummer20UL17MiniAODv2/TTJetsMC_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2530000/5B02E987-7D55-8F49-AE42-FFC0C9CDF5DA.root', 
                           "TTJetsMCHT2500toInf": '/store/mc/RunIISummer20UL17MiniAODv2/TTJetsMC_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2520000/F7E8C055-2623-8D4F-AA5F-C12D7E688D4C.root',
                          'ST_t-channel-top_inclMC':'/store/mc/RunIISummer20UL17MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/110000/0C1A975A-BE28-4644-BFCE-4494E9484C9D.root',
                           'ST_t-channel-antitop_inclMC':'/store/mc/RunIISummer20UL17MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/110000/0C1A975A-BE28-4644-BFCE-4494E9484C9D.root',
                           'ST_s-channel-hadronsMC':'/store/mc/RunIISummer20UL17MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/110000/0C1A975A-BE28-4644-BFCE-4494E9484C9D.root',
                           'ST_s-channel-leptonsMC':'/store/mc/RunIISummer20UL17MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/110000/0C1A975A-BE28-4644-BFCE-4494E9484C9D.root',
                           'ST_tW-antiTop_inclMC':'/store/mc/RunIISummer20UL17MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/110000/0C1A975A-BE28-4644-BFCE-4494E9484C9D.root',
                           'ST_tW-top_inclMC':'/store/mc/RunIISummer20UL17MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/110000/0C1A975A-BE28-4644-BFCE-4494E9484C9D.root',
                          'dataB': '/store/data/Run2017B/JetHT/MINIAOD/UL2017_MiniAODv2-v1/260000/11CD6855-708A-0F42-8087-28EA62F18E4B.root',
                          'dataC': '/store/data/Run2017C/JetHT/MINIAOD/UL2017_MiniAODv2-v1/260000/0925457A-3C64-BD4D-BDE4-6545610FB41C.root',
                          'dataD': '/store/data/Run2017D/JetHT/MINIAOD/UL2017_MiniAODv2-v1/260000/05C72CA9-9353-C74B-AA06-337BB5B25383.root',
                          'dataE': '/store/data/Run2017E/JetHT/MINIAOD/UL2017_MiniAODv2-v1/270000/027C7BEA-A5D2-3240-A4D0-37756BFAC7DD.root',
                          'dataF': '/store/data/Run2017F/JetHT/MINIAOD/UL2017_MiniAODv2-v1/260000/06019E27-BEE3-3A4C-8EA0-1E2914ED513A.root',
                          "Suu8_chi3": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu8TeV_chi3TeV_UL-ALLDECAY.root",
                           "Suu8_chi2":  "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu8TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu8_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu8TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu7_chi3": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu7TeV_chi3TeV_UL-ALLDECAY.root",
                           "Suu7_chi2": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu7TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu7_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu7TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu6_chi2": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu6TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu6_chi1p5":  "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu6TeV_chi1p5TeV_UL-ALLDECAY.root",
                           "Suu6_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu6TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu5_chi2":  "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu5TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu5_chi1p5": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu5TeV_chi1p5TeV_UL-ALLDECAY.root",
                           "Suu5_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu5TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu4_chi1p5": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu4TeV_chi1p5TeV_UL-ALLDECAY.root",
                           "Suu4_chi1" : "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu4TeV_chi1TeV_UL-ALLDECAY.root",
                           "WJetsMC_LNu-HT800to1200":  "/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120000/047D8A7F-D35C-774B-B5B5-B314EED4EE01.root"  ,
                           "WJetsMC_LNu-HT1200to2500": "/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/110000/0954A4E9-E6BB-644F-AB6E-D9C20C4209D8.root" ,
                           "WJetsMC_LNu-HT2500toInf":  "/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/230000/3A27F1F1-43D5-074E-B021-2B1D95C70BEF.root" ,
                           "WJetsMC_QQ-HT800toInf":   "/store/mc/RunIISummer20UL17MiniAODv2/WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/230000/045543C1-4163-CE4D-B9BA-105CFF3976F2.root" ,
                           "TTJetsMCHT800to1200": "/store/mc/RunIISummer20UL17MiniAODv2/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2530000/02D12EB2-34DC-6643-8A63-C7360E6AD401.root",
                           "WW_MC": "/store/mc/RunIISummer20UL17MiniAODv2/WW_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/280000/6817A6AE-CAC0-824B-99F8-CF4FA0717C33.root", 
                           "ZZ_MC": "/store/mc/RunIISummer20UL17MiniAODv2/ZZ_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/230000/66C883AB-FD5E-B34A-8D9E-66C1767BF42A.root"},
   '2018': { 'QCDMC1000to1500': '/store/mc/RunIISummer20UL18MiniAODv2/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2430000/0E582A57-8443-1D42-BBAB-85FF439FF1B3.root',
                          'QCDMC1500to2000': '/store/mc/RunIISummer20UL18MiniAODv2/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2820000/00BB6737-E608-494F-89BB-FE3D868AEDE3.root',
                          'QCDMC2000toInf':  '/store/mc/RunIISummer20UL18MiniAODv2/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2520000/081EFA0A-32E5-0040-B527-F3D5C40EB561.root',
                          'TTToHadronicMC':'/store/mc/RunIISummer20UL18MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/0706746B-319B-8B4C-9144-15786F03DC0B.root',  
                          'TTToSemiLeptonicMC':'/store/mc/RunIISummer20UL18MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/0706746B-319B-8B4C-9144-15786F03DC0B.root',
                          'TTToLeptonicMC':'/store/mc/RunIISummer20UL18MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/0706746B-319B-8B4C-9144-15786F03DC0B.root',
                          "TTJetsMCHT1200to2500": '/store/mc/RunIISummer20UL18MiniAODv2/TTJetsMC_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2430000/03B65E85-FA79-CD4C-8A63-86B611E211DF.root', 
                           "TTJetsMCHT2500toInf": '/store/mc/RunIISummer20UL18MiniAODv2/TTJetsMC_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/0C735F8D-6E99-3848-9C43-723FB97FD397.root',
                          'ST_t-channel-top_inclMC':'/store/mc/RunIISummer20UL18MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/0706746B-319B-8B4C-9144-15786F03DC0B.root',
                           'ST_t-channel-antitop_inclMC':'/store/mc/RunIISummer20UL18MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/0706746B-319B-8B4C-9144-15786F03DC0B.root',
                           'ST_s-channel-hadronsMC':'/store/mc/RunIISummer20UL18MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/0706746B-319B-8B4C-9144-15786F03DC0B.root',
                           'ST_s-channel-leptonsMC':'/store/mc/RunIISummer20UL18MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/0706746B-319B-8B4C-9144-15786F03DC0B.root',
                           'ST_tW-antiTop_inclMC':'/store/mc/RunIISummer20UL18MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/0706746B-319B-8B4C-9144-15786F03DC0B.root',
                           'ST_tW-top_inclMC':'/store/mc/RunIISummer20UL18MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/0706746B-319B-8B4C-9144-15786F03DC0B.root',
                          'dataA': '/store/data/Run2018A/JetHT/MINIAOD/UL2018_MiniAODv2-v1/260000/00B87525-94D1-C741-9B03-00528106D15A.root',
                          'dataB': '/store/data/Run2018B/JetHT/MINIAOD/UL2018_MiniAODv2-v1/260000/01CD6E06-A979-7448-AEAE-C2A1C862DE66.root',
                          'dataC': '/store/data/Run2018C/JetHT/MINIAOD/UL2018_MiniAODv2-v1/260000/091A1C55-0CB8-5440-B925-706D92C02FE1.root',
                          'dataD': '/store/data/Run2018D/JetHT/MINIAOD/UL2018_MiniAODv2-v1/250000/DAB917DB-036A-324D-88CA-6DD8AA4FEC0F.root',
                          "Suu8_chi3": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu8TeV_chi3TeV_UL-ALLDECAY.root",
                           "Suu8_chi2":  "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu8TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu8_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu8TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu7_chi3": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu7TeV_chi3TeV_UL-ALLDECAY.root",
                           "Suu7_chi2": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu7TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu7_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu7TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu6_chi2": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu6TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu6_chi1p5":  "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu6TeV_chi1p5TeV_UL-ALLDECAY.root",
                           "Suu6_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu6TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu5_chi2":  "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu5TeV_chi2TeV_UL-ALLDECAY.root",
                           "Suu5_chi1p5": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu5TeV_chi1p5TeV_UL-ALLDECAY.root",
                           "Suu5_chi1": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu5TeV_chi1TeV_UL-ALLDECAY.root",
                           "Suu4_chi1p5": "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu4TeV_chi1p5TeV_UL-ALLDECAY.root",
                           "Suu4_chi1" : "file:/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/signalData/UL_files_ALLDECAYS/Suu4TeV_chi1TeV_UL-ALLDECAY.root",
                           "WJetsMC_LNu-HT800to1200":  "/store/mc/RunIISummer20UL18MiniAODv2/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/1504731E-6070-D747-8E22-25C2D5D915DD.root" ,
                           "WJetsMC_LNu-HT1200to2500": "/store/mc/RunIISummer20UL18MiniAODv2/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/110000/0F35DDAD-A0A9-4146-AD82-61B14BE0F32B.root" ,
                           "WJetsMC_LNu-HT2500toInf":  "/store/mc/RunIISummer20UL18MiniAODv2/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2530000/48A4E234-7205-C640-B2AA-A623F67CC886.root" ,
                           "WJetsMC_QQ-HT800toInf":   "/store/mc/RunIISummer20UL18MiniAODv2/WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2550000/21E85713-18F9-5441-8A3C-906740E795E7.root" ,
                           "TTJetsMCHT800to1200":  "/store/mc/RunIISummer20UL18MiniAODv2/TTJets_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2430000/02D4F908-3886-C748-A054-428662AA6077.root" ,
                           "WW_MC": "/store/mc/RunIISummer20UL18MiniAODv2/WW_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/230000/0849192E-1894-4541-8A50-EE3FF4A77AF9.root",
                           "ZZ_MC": "/store/mc/RunIISummer20UL18MiniAODv2/ZZ_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2430000/A0F466AB-CC86-4B40-9E6E-80159DB164F2.root"
   }
}
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
                           "ZZ_MC": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK4PFchs.txt'

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
                           "ZZ_MC": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK4PFchs.txt'},

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
                     "ZZ_MC": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK4PFchs.txt'

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
                        "ZZ_MC": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt'
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
                        "ZZ_MC": 'data/JEC/2016_UL_preAPV/MC/Summer19UL16APV_V7_MC_Uncertainty_AK8PFPuppi.txt'},


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
                        "ZZ_MC": 'data/JEC/2016_UL_postAPV/MC/Summer19UL16_V7_MC_Uncertainty_AK8PFPuppi.txt'
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
                        "ZZ_MC": 'data/JEC/2017_UL/MC/Summer19UL17_V5_MC_Uncertainty_AK8PFPuppi.txt'
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
                     "ZZ_MC": 'data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt'}

}

   # signal_files.pkl
   signal_samples_pkl = open('data/pkl/signal_samples.pkl', 'r')
   signal_samples   = pickle.load(signal_samples_pkl)

   signal_files_pkl = open('data/pkl/signal_files.pkl', 'r')
   signal_files     = pickle.load(signal_files_pkl)

   num_files =0
   for year in years:
      if year == "2015":
         samples = ["dataB-ver1","dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM" ,"dataF-HIPM","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf", "TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf", "ST_t-channel-top_inclMC","ST_t-channel-antitop_inclMC","ST_s-channel-hadronsMC","ST_s-channel-leptonsMC","ST_tW-antiTop_inclMC","ST_tW-top_inclMC","TTToHadronicMC", "TTToSemiLeptonicMC", "TTToLeptonicMC", "TTToHadronicMC",    "WJetsMC_LNu-HT800to1200", "WJetsMC_LNu-HT1200to2500",  "WJetsMC_LNu-HT2500toInf", "WJetsMC_QQ-HT800toInf",  "TTJetsMCHT800to1200", "WW_MC", "ZZ_MC"]
      elif year == "2016":
         samples = ["dataF","dataG","dataH","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf","ST_t-channel-top_inclMC","ST_t-channel-antitop_inclMC","ST_s-channel-hadronsMC","ST_s-channel-leptonsMC","ST_tW-antiTop_inclMC","ST_tW-top_inclMC","TTToHadronicMC", "TTToSemiLeptonicMC", "TTToLeptonicMC", "TTToHadronicMC",    "WJetsMC_LNu-HT800to1200", "WJetsMC_LNu-HT1200to2500",  "WJetsMC_LNu-HT2500toInf", "WJetsMC_QQ-HT800toInf",  "TTJetsMCHT800to1200", "WW_MC", "ZZ_MC"]
      elif year == "2017":
         samples = ["dataB","dataC","dataD","dataE","dataF","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf","ST_t-channel-top_inclMC","ST_t-channel-antitop_inclMC","ST_s-channel-hadronsMC","ST_s-channel-leptonsMC","ST_tW-antiTop_inclMC","ST_tW-top_inclMC","TTToHadronicMC", "TTToSemiLeptonicMC", "TTToLeptonicMC" , "TTToHadronicMC",    "WJetsMC_LNu-HT800to1200", "WJetsMC_LNu-HT1200to2500",  "WJetsMC_LNu-HT2500toInf", "WJetsMC_QQ-HT800toInf",  "TTJetsMCHT800to1200", "WW_MC", "ZZ_MC"]
      elif year == "2018":
         samples = ["dataA","dataB", "dataC", "dataD","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf","ST_t-channel-top_inclMC","ST_t-channel-antitop_inclMC","ST_s-channel-hadronsMC","ST_s-channel-leptonsMC","ST_tW-antiTop_inclMC","ST_tW-top_inclMC","TTToHadronicMC", "TTToSemiLeptonicMC", "TTToLeptonicMC", "TTToHadronicMC",    "WJetsMC_LNu-HT800to1200", "WJetsMC_LNu-HT1200to2500",  "WJetsMC_LNu-HT2500toInf", "WJetsMC_QQ-HT800toInf",  "TTJetsMCHT800to1200", "WW_MC", "ZZ_MC" ]
      samples.extend(signal_samples)
      for iii, sample in enumerate(samples):
         for systematic in systematics:

            if "Suu" in sample:
               try:
                  JEC_sample = sample
                  if "Suu" in sample:
                     JEC_sample = "signal"

                  makeACfg(sample, year, systematic, signal_files[year][sample], jec_file_AK4[year][JEC_sample],jec_file_AK8[year][JEC_sample], systematics)   # change input to write systematic type
                  num_files+=1
               except:
                  
                  print("Failed on sample/year/systematic: %s/%s/%s"%(sample,year,systematic))
            else:
               makeACfg(sample, year, systematic, datafiles[year][sample], jec_file_AK4[year][sample],jec_file_AK8[year][sample], systematics)  # change input to write systematic type
               num_files+=1 
   print("Finished with %i files."%num_files )
   return


if __name__ == "__main__":
    main()
