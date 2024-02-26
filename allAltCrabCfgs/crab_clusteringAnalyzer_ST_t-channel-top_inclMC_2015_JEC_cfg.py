from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_ST_t-channel-top_inclMC_2015_JEC_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_ST_t-channel-top_inclMC_2015_JEC_cfg.py'
config.Data.inputDataset = '/ST_t-channel_top_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outputDatasetTag = 'clustAlg_ST_t-channel-top_inclMC_2015_JEC'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2024224_20418'
config.Site.storageSite = 'T3_US_FNALLPC'
