import FWCore.ParameterSet.Config as cms

process = cms.Process("analysis")

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.GlobalTag.globaltag = '92X_dataRun2_Prompt_v4'

process.genPartFilter = cms.EDFilter("genPartFilter",
genPartCollection = cms.InputTag("prunedGenParticles")
)
process.leptonVeto = cms.EDFilter("leptonVeto",
   muonCollection= cms.InputTag("slimmedMuons"),
   electronCollection = cms.InputTag("slimmedElectrons"),
   tauCollection = cms.InputTag("slimmedTaus")
)
process.hadronFilter = cms.EDFilter("hadronFilter",
   fatJetCollection = cms.InputTag("slimmedJetsAK8"),
   jetCollection = cms.InputTag("slimmedJets"),
   bits = cms.InputTag("TriggerResults", "", "HLT"),
)
process.clusteringAnalyzer = cms.EDAnalyzer("clusteringAnalyzer",
 
   fatJetCollection = cms.InputTag("slimmedJetsAK8"),
   genPartCollection = cms.InputTag("prunedGenParticles"),
   jetCollection = cms.InputTag("slimmedJets"),
   bits = cms.InputTag("TriggerResults", "", "HLT"),
   muonCollection= cms.InputTag("slimmedMuons"),
   electronCollection = cms.InputTag("slimmedElectrons"),
   tauCollection = cms.InputTag("slimmedTaus")
)

process.source = cms.Source("PoolSource",
fileNames = cms.untracked.vstring("file:UL_files_ALLDECAYS/Suu5TeV_chi1p5TeV_UL-ALLDECAY.root")
#"file:chi850GeV_Suu4TeV_MINIAOD.root")
   #fileNames = cms.untracked.vstring("file:Suu4TeV_chi850GeV.root")
   #fileNames = cms.untracked.vstring("/store/mc/RunIIAutumn18MiniAOD/
)
process.TFileService = cms.Service("TFileService",fileName = cms.string("ClusteringAlgorithm_Suu4TeV_chi850GeV_output.root")
)

process.maxEvents = cms.untracked.PSet(
   input = cms.untracked.int32(5000000)
)

process.options = cms.untracked.PSet(
   wantSummary = cms.untracked.bool(True),
)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

"""process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
   src = cms.InputTag("prunedGenParticles"),
   printP4 = cms.untracked.bool(False),
   printPtEtaPhi = cms.untracked.bool(False),
   printVertex = cms.untracked.bool(False),
   printStatus = cms.untracked.bool(True),
   printIndex = cms.untracked.bool(False),
   #status = cms.untracked.vint32(3),
)
"""
process.p = cms.Path( process.leptonVeto* process.hadronFilter* process.clusteringAnalyzer  #process.leptonVeto* process.hadronFilter  * 
#process.clusteringAnalyzer  #needs star  process.genPartFilter*
   #  
)
