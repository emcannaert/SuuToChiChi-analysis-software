from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_TTToHadronicMC_2017_JEC_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_TTToHadronicMC_2017_JEC_cfg.py'
config.Data.inputDataset = '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outputDatasetTag = 'clustAlg_TTToHadronicMC_2017_JEC'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_202436_202044'
config.Site.storageSite = 'T3_US_FNALLPC'
