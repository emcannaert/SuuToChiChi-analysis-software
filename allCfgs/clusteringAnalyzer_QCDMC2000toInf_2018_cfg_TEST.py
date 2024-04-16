from PhysicsTools.PatAlgos.tools.helpers  import getPatAlgosToolsTask
import FWCore.ParameterSet.Config as cms
process = cms.Process("analysis")
from Configuration.AlCa.GlobalTag import GlobalTag
process.load('Configuration.StandardSequences.Services_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.load('JetMETCorrections.Configuration.JetCorrectors_cff')
process.load('JetMETCorrections.Configuration.CorrectedJetProducers_cff')
process.load('JetMETCorrections.Configuration.CorrectedJetProducersDefault_cff')
process.load("JetMETCorrections.Configuration.JetCorrectionServices_cff")
process.load("JetMETCorrections.Configuration.JetCorrectionServicesAllAlgos_cff")
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
process.GlobalTag.globaltag = '106X_upgrade2018_realistic_v16_L1v1'
process.options = cms.untracked.PSet( allowUnscheduled = cms.untracked.bool(True) )
isData = False
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
################# JEC ################
corrLabels = ['L1FastJet','L2Relative','L3Absolute']
if isData:
	corrLabels.append('L2L3Residual')
from PhysicsTools.PatAlgos.tools.jetTools import *
from RecoBTag.ONNXRuntime.pfDeepBoostedJet_cff import *
updateJetCollection(
   process,
   jetSource = cms.InputTag('slimmedJetsAK8'),
   labelName = 'AK8',
   jetCorrections = ('AK8PFPuppi', cms.vstring(corrLabels), 'None'), #previous corrections: 'L2Relative', 'L3Absolute', 'L2L3Residual'
   postfix = 'UpdatedJEC',
   printWarning = False
)
updateJetCollection(
   process,
   jetSource = cms.InputTag('slimmedJets'),
   labelName = 'AK4',
   jetCorrections = ('AK4PFchs', cms.vstring(corrLabels), 'None'),
   postfix = 'UpdatedJEC',
   printWarning = False
)  
################# Jet PU ID ################
from RecoJets.JetProducers.PileupJetID_cfi import pileupJetId
from RecoJets.JetProducers.PileupJetID_cfi import _chsalgos_106X_UL18
process.load("RecoJets.JetProducers.PileupJetID_cfi")
process.pileupJetIdUpdated = process.pileupJetId.clone( 
jets=cms.InputTag("selectedUpdatedPatJetsAK4UpdatedJEC"),      #should be the name of the post-JEC jet collection
inputIsCorrected=True,
applyJec=False,
vertexes=cms.InputTag("offlineSlimmedPrimaryVertices"),
algos = cms.VPSet(_chsalgos_106X_UL18),
)
process.patAlgosToolsTask.add(process.pileupJetIdUpdated)
updateJetCollection(     # running in unscheduled mode, need to manually update collection
   process,
   labelName = "PileupJetID",
   jetSource = cms.InputTag("selectedUpdatedPatJetsAK4UpdatedJEC"),
)
process.updatedPatJetsPileupJetID.userData.userInts.src = ["pileupJetIdUpdated:fullId"]
process.content = cms.EDAnalyzer("EventContentAnalyzer")
##############################################################################
process.leptonVeto = cms.EDFilter("leptonVeto",
   muonCollection= cms.InputTag("slimmedMuons"),
   electronCollection = cms.InputTag("slimmedElectrons"),
   metCollection = cms.InputTag("slimmedMETs"),
   tauCollection = cms.InputTag("slimmedTaus")
)
from PhysicsTools.PatUtils.l1PrefiringWeightProducer_cfi import l1PrefiringWeightProducer
process.prefiringweight = l1PrefiringWeightProducer.clone(
TheJets = cms.InputTag('selectedUpdatedPatJetsAK4UpdatedJEC'), #this should be the slimmedJets collection with up to date JECs 
DataEraECAL = cms.string('None'), #Use 2016BtoH for 2016
DataEraMuon = cms.string('20172018'), #Use 2016 for 2016
UseJetEMPt = cms.bool(False),
PrefiringRateSystematicUnctyECAL = cms.double(0.2),
PrefiringRateSystematicUnctyMuon = cms.double(0.2)
)
process.clusteringAnalyzerAll_nom = cms.EDAnalyzer("clusteringAnalyzerAll",
   runType = cms.string("QCDMC2000toInf"),   #types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTbarMC, DataA, etc. , Suu8_chi3, etc.
   genPartCollection = cms.InputTag("prunedGenParticles"),
      genParticles = cms.InputTag("genParticles"),
      packedGenParticles = cms.InputTag("packedGenParticles"),
   BESTname = cms.string('BESTGraph'),   BESTpath = cms.FileInPath('data/BEST_models/constantgraph_2018.pb'),
   BESTscale = cms.FileInPath('data/BESTScalerParameters_all_mass_2018.txt'),
   PUfile_path = cms.FileInPath('data/POG/LUM/2018_UL/puWeights.json'),
   bTagEff_path = cms.FileInPath('data/btaggingEffMaps/btag_efficiency_map_QCDMC_combined_2018.root'),
   bTagSF_path = cms.FileInPath('data/bTaggingSFs/2018_UL/btagging.json'),
   JECUncert_AK8_path = cms.FileInPath("data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK8PFPuppi.txt"),
   JECUncert_AK4_path = cms.FileInPath("data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt"),
   fatJetCollection = cms.InputTag("selectedUpdatedPatJetsAK8UpdatedJEC"),
   jetCollection = cms.InputTag("selectedUpdatedPatJetsPileupJetID"),
   muonCollection= cms.InputTag("slimmedMuons"),
   electronCollection = cms.InputTag("slimmedElectrons"),
   metCollection = cms.InputTag("slimmedMETs"),
   tauCollection = cms.InputTag("slimmedTaus"),
   pileupCollection = cms.InputTag("slimmedAddPileupInfo"),
   systematicType = cms.string("nom"),
   jetVetoMapFile = cms.FileInPath("data/jetVetoMaps/hotjets-UL18.root"),
   jetVetoMapName = cms.string("h2hot_ul18_plus_hem1516_and_hbp2m1"),
   includeAllBranches = cms.bool(False),
   slimmedSelection   = cms.bool(False),
   verbose            = cms.bool(False),
   year = cms.string("2018"),   #types: 2015,2016,2017,2018
   genEventInfoTag=cms.InputTag("generator"),
   lheEventInfoTag=cms.InputTag("externalLHEProducer"),
   bits = cms.InputTag("TriggerResults", "", "HLT"),
   triggers = cms.string("HLT_PFHT1050_v"),
   doPUID = cms.bool(True),
    doPDF = cms.bool(False)
)
process.source = cms.Source("PoolSource",
fileNames = cms.untracked.vstring( "/store/user/ecannaer/SuuToChiChi_test_gridpack/SuuToChiChiToHTZTToJets_MSuu_6000_MChi_2000_TEST_MiniAOD_000/240405_222207/0000/B2G-RunIISummer20UL18MiniAODv2-03659_32.root" #"/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIISummer19UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM" # "/store/mc/RunIISummer20UL18MiniAODv2/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/8FB0FF0F-8DCD-6B49-9FDB-730EB9CDA6D2.root"  #"/store/mc/RunIISummer20UL18MiniAODv2/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/110000/16A09334-E800-9F43-8660-52AC737FDBA0.root"
)
)
process.TFileService = cms.Service("TFileService",fileName = cms.string("clusteringAnalyzer_QCDMC2000toInf_2018_nom_output.root")
)
process.options = cms.untracked.PSet(
   wantSummary = cms.untracked.bool(True),
)
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.p = cms.Path(  process.pileupJetIdUpdated * process.leptonVeto * process.prefiringweight   * process.clusteringAnalyzerAll_nom
)
process.patAlgosToolsTask = getPatAlgosToolsTask(process)
process.pathRunPatAlgos = cms.Path(process.patAlgosToolsTask)
