from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'TEST_QCDMC2000toInf_2018__000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_QCDMC2000toInf_2018_cfg.py'
config.Data.inputDataset = '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.JobType.maxMemoryMB = 2500 # might be necessary for some of the QCD jobs
config.Data.outputDatasetTag = 'TEST_QCDMC2000toInf_2018_'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_TEST'
config.Site.storageSite = 'T3_US_FNALLPC'