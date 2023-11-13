from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_dataG_2016__AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_dataG_2016_cfg.py'
config.Data.inputDataset = '/JetHT/Run2016G-UL2016_MiniAODv2-v2/MINIAOD'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
config.JobType.maxMemoryMB = 5000 # might be necessary for some of the QCD jobs
config.Data.lumiMask = '../lumimasks/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
config.Data.outputDatasetTag = 'clustAlg_dataG_2016_'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2023116_13325'
config.Site.storageSite = 'T3_US_FNALLPC'
