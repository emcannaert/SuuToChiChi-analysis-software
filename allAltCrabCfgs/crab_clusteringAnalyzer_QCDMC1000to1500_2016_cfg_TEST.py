from CRABClient.UserUtilities import config
config = config()
config.General.requestName = 'clustAlg_QCDMC1000to1500_2016_nom_AltDatasets_TEST_000'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.JobType.allowUndistributedCMSSW = True
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../allCfgs/clusteringAnalyzer_QCDMC1000to1500_2016_cfg.py'
config.Data.inputDataset = '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM'
config.Data.publication = False
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.JobType.maxMemoryMB = 2500 # might be necessary for some of the QCD jobs
config.Data.outputDatasetTag = 'clustAlg_QCDMC1000to1500_2016_nom_TEST'
config.Data.outLFNDirBase = '/store/user/ecannaer/SuuToChiChi_202445_TEST'
config.Site.storageSite = 'T3_US_FNALLPC'
