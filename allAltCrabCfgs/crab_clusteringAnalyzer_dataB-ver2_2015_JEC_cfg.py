from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_dataB-ver2_2015_JEC_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_dataB-ver2_2015_JEC_cfg.py'
config.Data.inputDataset = '/JetHT/Run2016B-ver2_HIPM_UL2016_MiniAODv2-v2/MINIAOD'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.JobType.maxMemoryMB = 4000 # might be necessary for some of the QCD jobs
config.Data.lumiMask = '../lumimasks/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
config.Data.outputDatasetTag = 'clustAlg_dataB-ver2_2015_JEC'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2024129_131131'
config.Site.storageSite = 'T3_US_FNALLPC'
