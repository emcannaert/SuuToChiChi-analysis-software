import FWCore.ParameterSet.Config as cms

process = cms.Process("analysis")

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring("/store/mc/RunIISummer20UL18MiniAODv2/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/2540000/09D89A2C-53F2-504E-8087-66276CE2FC04.root")
)

process.maxEvents = cms.untracked.PSet(
   input = cms.untracked.int32(50)
)

process.options = cms.untracked.PSet(
   wantSummary = cms.untracked.bool(True),
)
#process.Tracer = cms.Service("Tracer")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
   src = cms.InputTag("prunedGenParticles"),
   printP4 = cms.untracked.bool(False),
   printPtEtaPhi = cms.untracked.bool(False),
   printVertex = cms.untracked.bool(False),
   printStatus = cms.untracked.bool(True),
   printIndex = cms.untracked.bool(False),
   #status = cms.untracked.vint32(3),
)

process.p = cms.Path(
   process.printTree
)


