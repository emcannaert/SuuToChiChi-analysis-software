from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_ST_s-channel-hadronsMC_2017_JER_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_ST_s-channel-hadronsMC_2017_JER_cfg.py'
config.Data.inputDataset = '/ST_s-channel_4f_hadronicDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outputDatasetTag = 'clustAlg_ST_s-channel-hadronsMC_2017_JER'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2024410_202245'
config.Site.storageSite = 'T3_US_FNALLPC'
