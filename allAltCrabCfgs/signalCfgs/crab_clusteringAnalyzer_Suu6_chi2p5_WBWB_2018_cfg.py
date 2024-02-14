from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_Suu6_chi2p5_WBWB_2018__AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../../allCfgs/signalCfgs/clusteringAnalyzer_Suu6_chi2p5_WBWB_2018_cfg.py'
config.Data.inputDataset = '/SuuToChiChiToWBWBToJets_MSuu-6000_MChi-2500_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outputDatasetTag = 'clustAlg_Suu6_chi2p5_WBWB_2018_'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_202426_233436'
config.Site.storageSite = 'T3_US_FNALLPC'
