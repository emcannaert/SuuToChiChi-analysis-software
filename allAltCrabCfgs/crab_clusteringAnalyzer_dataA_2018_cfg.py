from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_dataA_2018__AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_dataA_2018_cfg.py'
config.Data.inputDataset = '/JetHT/Run2018A-UL2018_MiniAODv2_GT36-v1/MINIAOD'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.JobType.maxMemoryMB = 4000 # might be necessary for some of the QCD jobs
config.Data.lumiMask = '../lumimasks/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
config.Data.outputDatasetTag = 'clustAlg_dataA_2018_'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_20231127_23944'
config.Site.storageSite = 'T3_US_FNALLPC'
