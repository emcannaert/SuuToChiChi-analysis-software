from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_Suu5_chi1_ZTZT_2017_nom_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../../allCfgs/signalCfgs/clusteringAnalyzer_Suu5_chi1_ZTZT_2017_cfg.py'
config.Data.inputDataset = '/SuuToChiChiToZTZTToJets_MSuu-5000_MChi-1000_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.JobType.maxMemoryMB = 3500 
config.Data.outputDatasetTag = 'clustAlg_Suu5_chi1_ZTZT_2017_nom'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2024927_193854'
config.Site.storageSite = 'T3_US_FNALLPC'
