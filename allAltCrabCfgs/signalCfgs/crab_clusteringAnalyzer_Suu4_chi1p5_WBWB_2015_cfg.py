from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_Suu4_chi1p5_WBWB_2015_nom_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../../allCfgs/signalCfgs/clusteringAnalyzer_Suu4_chi1p5_WBWB_2015_cfg.py'
config.Data.inputDataset = '/SuuToChiChiToWBWBToJets_MSuu-4000_MChi-1500_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outputDatasetTag = 'clustAlg_Suu4_chi1p5_WBWB_2015_nom'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2024219_25455'
config.Site.storageSite = 'T3_US_FNALLPC'
