from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_dataB-ver1_2015__AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_dataB-ver1_2015_cfg.py'
config.Data.inputDataset = '/JetHT/Run2016B-ver1_HIPM_UL2016_MiniAODv2-v2/MINIAOD'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.JobType.maxMemoryMB = 4000 # might be necessary for some of the QCD jobs
config.Data.lumiMask = '../lumimasks/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
config.Data.outputDatasetTag = 'clustAlg_dataB-ver1_2015_'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_20231122_165353'
config.Site.storageSite = 'T3_US_FNALLPC'
