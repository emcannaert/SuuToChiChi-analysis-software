hadd QCD_HT1000to1500_2015_combined.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraph-pythia8/clustAlg_QCDMC1000to1500_2015_/230911_215711/0000  | grep '\.root'`

hadd  QCD_HT1500to2000_2015_combined.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/clustAlg_QCDMC1500to2000_2015_/230911_215858/0000 | grep '\.root'`

hadd  QCD_HT2000toInf_2015_combined.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraph-pythia8/clustAlg_QCDMC2000toInf_2015_/230911_215805/0000 | grep '\.root'`

hadd  TTToHadronic_2015_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452//TTToHadronic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTbarMC_2015_/230911_215952/0000 | grep '\.root'`
hadd  TTToHadronic_2015_combined_1.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452//TTToHadronic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTbarMC_2015_/230911_215952/0001 | grep '\.root'`

hadd TTToHadronic_2015_combined.root TTToHadronic_2015_combined_0.root TTToHadronic_2015_combined_1.root

