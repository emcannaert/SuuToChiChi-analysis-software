from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_TTJetsMCHT1200to2500_2017_nom_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_TTJetsMCHT1200to2500_2017_cfg.py'
config.Data.inputDataset = '/TTJets_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outputDatasetTag = 'clustAlg_TTJetsMCHT1200to2500_2017_nom'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2024410_202245'
config.Site.storageSite = 'T3_US_FNALLPC'
