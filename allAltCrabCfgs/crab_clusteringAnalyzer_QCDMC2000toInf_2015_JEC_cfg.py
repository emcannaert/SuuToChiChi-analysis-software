from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_QCDMC2000toInf_2015_JEC_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_QCDMC2000toInf_2015_JEC_cfg.py'
config.Data.inputDataset = '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.JobType.maxMemoryMB = 3000 # might be necessary for some of the QCD jobs
config.Data.outputDatasetTag = 'clustAlg_QCDMC2000toInf_2015_JEC'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_20231122_165353'
config.Site.storageSite = 'T3_US_FNALLPC'
