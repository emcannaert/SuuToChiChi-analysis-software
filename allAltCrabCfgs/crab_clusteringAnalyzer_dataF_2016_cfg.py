from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_dataF_2016__AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_dataF_2016_cfg.py'
config.Data.inputDataset = '/JetHT/Run2016F-UL2016_MiniAODv2-v2/MINIAOD'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.JobType.maxMemoryMB = 4000 # might be necessary for some of the QCD jobs
config.Data.lumiMask = '../lumimasks/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
config.Data.outputDatasetTag = 'clustAlg_dataF_2016_'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_202426_233436'
config.Site.storageSite = 'T3_US_FNALLPC'
