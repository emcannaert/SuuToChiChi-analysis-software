from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_Suu5_chi1_WBHT_2016_nom_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../../allCfgs/signalCfgs/clusteringAnalyzer_Suu5_chi1_WBHT_2016_cfg.py'
config.Data.inputDataset = '/SuuToChiChiToWBHTToJets_MSuu-5000_MChi-1000_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outputDatasetTag = 'clustAlg_Suu5_chi1_WBHT_2016_nom'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2024224_20418'
config.Site.storageSite = 'T3_US_FNALLPC'