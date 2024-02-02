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
process.hadronFilter = cms.EDFilter("hadronFilter",
   year = cms.string("2018"),
   fatJetCollection = cms.InputTag("selectedUpdatedPatJetsAK8UpdatedJEC"),
   metCollection = cms.InputTag("slimmedMETs"),
   jetCollection = cms.InputTag("selectedUpdatedPatJetsPileupJetID"),
   bits = cms.InputTag("TriggerResults", "", "HLT"),
   triggers = cms.string("HLT_PFHT1050_v"),
   systematicType = cms.string(""),
   JECUncert_AK4_path = cms.FileInPath("data/JEC/2018_UL/MC/Summer19UL18_V5_MC_Uncertainty_AK4PFchs.txt"),
   doPUID = cms.bool(True),
   runType = cms.string("Suu8_chi1")   #types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTToHadronicMC, TTToSemiLeptonic, TTToLeptonic, DataA, etc. , Suu8_chi3, etc.
)
process.clusteringAnalyzerAll_ = cms.EDAnalyzer("clusteringAnalyzerAll",
   runType = cms.string("Suu8_chi1"),   #types: QCDMC1000to1500, QCDMC1500to2000, QCDMC2000toInf, TTbarMC, DataA, etc. , Suu8_chi3, etc.
   genPartCollection = cms.InputTag("prunedGenParticles"),
   name = cms.string('BESTGraph'),   path = cms.FileInPath('data/constantgraph.pb'),
   means = cms.FileInPath('data/ScalerParameters_maxAbs_train.txt'),
   PUfile_path = cms.FileInPath('data/POG/LUM/2018_UL/puWeights.json'),
