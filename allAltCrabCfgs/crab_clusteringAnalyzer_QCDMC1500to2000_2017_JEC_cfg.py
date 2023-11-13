from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_QCDMC1500to2000_2017_JEC_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_QCDMC1500to2000_2017_JEC_cfg.py'
config.Data.inputDataset = '/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
config.JobType.maxMemoryMB = 3000 # might be necessary for some of the QCD jobs
config.Data.outputDatasetTag = 'clustAlg_QCDMC1500to2000_2017_JEC'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2023116_13325'
config.Site.storageSite = 'T3_US_FNALLPC'
