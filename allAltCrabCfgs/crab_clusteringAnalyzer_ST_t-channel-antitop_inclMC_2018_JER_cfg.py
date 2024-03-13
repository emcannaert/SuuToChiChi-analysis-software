from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_ST_t-channel-antitop_inclMC_2018_JER_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_ST_t-channel-antitop_inclMC_2018_JER_cfg.py'
config.Data.inputDataset = '/ST_t-channel_antitop_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outputDatasetTag = 'clustAlg_ST_t-channel-antitop_inclMC_2018_JER'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_202436_202044'
config.Site.storageSite = 'T3_US_FNALLPC'
