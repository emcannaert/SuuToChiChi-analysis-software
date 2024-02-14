from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_Suu6_chi1_HTZT_2016__AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../../allCfgs/signalCfgs/clusteringAnalyzer_Suu6_chi1_HTZT_2016_cfg.py'
config.Data.inputDataset = '/SuuToChiChiToHTZTToJets_MSuu-6000_MChi-1000_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outputDatasetTag = 'clustAlg_Suu6_chi1_HTZT_2016_'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_202426_233436'
config.Site.storageSite = 'T3_US_FNALLPC'
