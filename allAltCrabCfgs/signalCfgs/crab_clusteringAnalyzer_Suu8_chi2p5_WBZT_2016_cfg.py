from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_Suu8_chi2p5_WBZT_2016_nom_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../../allCfgs/signalCfgs/clusteringAnalyzer_Suu8_chi2p5_WBZT_2016_cfg.py'
config.Data.inputDataset = '/SuuToChiChiToWBZTToJets_MSuu-8000_MChi-2500_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.JobType.maxMemoryMB = 3500 
config.Data.outputDatasetTag = 'clustAlg_Suu8_chi2p5_WBZT_2016_nom'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2024927_193854'
config.Site.storageSite = 'T3_US_FNALLPC'
