from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_dataB_2017_JER_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_dataB_2017_JER_cfg.py'
config.Data.inputDataset = '/JetHT/Run2017B-UL2017_MiniAODv2-v1/MINIAOD'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 2
config.JobType.maxMemoryMB = 5000 # might be necessary for some of the QCD jobs
config.Data.lumiMask = '../lumimasks/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'
config.Data.outputDatasetTag = 'clustAlg_dataB_2017_JER'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2023116_13325'
config.Site.storageSite = 'T3_US_FNALLPC'