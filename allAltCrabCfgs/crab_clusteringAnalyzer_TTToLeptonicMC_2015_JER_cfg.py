from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_TTToLeptonicMC_2015_JER_AltDatasets_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_TTToLeptonicMC_2015_JER_cfg.py'
config.Data.inputDataset = '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.outputDatasetTag = 'clustAlg_TTToLeptonicMC_2015_JER'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_2024129_131131'
config.Site.storageSite = 'T3_US_FNALLPC'