from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_dataF_2017_JER_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_dataF_2017_JER_cfg.py'
config.Data.inputDataset = '/JetHT/Run2017F-UL2017_MiniAODv2-v1/MINIAOD'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.JobType.maxMemoryMB = 3000 # might be necessary for some of the QCD jobs
config.Data.lumiMask = '../lumimasks/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'
config.Data.outputDatasetTag = 'clustAlg_dataF_2017_JER'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2024224_20418'
config.Site.storageSite = 'T3_US_FNALLPC'
