import FWCore.ParameterSet.Config as cms

process = cms.Process("analysis")

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring("/store/mc/RunIIAutumn18MiniAOD/TprimeTprime_M-1300_TuneCP5_PSweights_13TeV-madgraph-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v2/270000/054432FA-430C-2C4F-9E15-2019196FB8CC.root")
)

process.maxEvents = cms.untracked.PSet(
   input = cms.untracked.int32(10)
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


