from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_ST_tW-antiTop_inclMC_2018_JEC_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_ST_tW-antiTop_inclMC_2018_JEC_cfg.py'
config.Data.inputDataset = '/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outputDatasetTag = 'clustAlg_ST_tW-antiTop_inclMC_2018_JEC'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_202426_233436'
config.Site.storageSite = 'T3_US_FNALLPC'
