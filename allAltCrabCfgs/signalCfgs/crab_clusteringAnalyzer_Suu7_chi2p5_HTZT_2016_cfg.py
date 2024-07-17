from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_Suu7_chi2p5_HTZT_2016_nom_AltDatasets_000'
config.General.workArea = 'crab_projects_sideband'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../../allCfgs/signalCfgs/clusteringAnalyzer_Suu7_chi2p5_HTZT_2016_cfg.py'
config.Data.inputDataset = '/SuuToChiChiToHTZTToJets_MSuu-7000_MChi-2500_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outputDatasetTag = 'clustAlg_Suu7_chi2p5_HTZT_2016_nom'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2024716_122143_sideband'
config.Site.storageSite = 'T3_US_FNALLPC'
