from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_QCDMC2000toInf_2017__AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_QCDMC2000toInf_2017_cfg.py'
config.Data.inputDataset = '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.JobType.maxMemoryMB = 2500 # might be necessary for some of the QCD jobs
config.Data.outputDatasetTag = 'clustAlg_QCDMC2000toInf_2017_'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_20231127_23944'
config.Site.storageSite = 'T3_US_FNALLPC'
