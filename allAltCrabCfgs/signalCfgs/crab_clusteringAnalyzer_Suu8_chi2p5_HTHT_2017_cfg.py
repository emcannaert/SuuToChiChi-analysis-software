from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_Suu8_chi2p5_HTHT_2017_nom_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../../allCfgs/signalCfgs/clusteringAnalyzer_Suu8_chi2p5_HTHT_2017_cfg.py'
config.Data.inputDataset = '/SuuToChiChiToHTHTToJets_MSuu-8000_MChi-2500_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outputDatasetTag = 'clustAlg_Suu8_chi2p5_HTHT_2017_nom'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2024224_20418'
config.Site.storageSite = 'T3_US_FNALLPC'
