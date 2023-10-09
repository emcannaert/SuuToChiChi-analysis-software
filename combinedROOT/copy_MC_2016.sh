hadd QCD_HT1000to1500_2016_combined.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraph-pythia8/clustAlg_QCDMC1000to1500_2016_/230911_220045/0000  | grep '\.root'`

hadd  QCD_HT1500to2000_2016_combined.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/clustAlg_QCDMC1500to2000_2016_/230911_220230/0000 | grep '\.root'`
hadd  QCD_HT2000toInf_2016_combined.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraph-pythia8/clustAlg_QCDMC2000toInf_2016_/230911_220138/0000 | grep '\.root'`
hadd  TTToHadronic_2016_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452//TTToHadronic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTbarMC_2016_/230911_220322/0000 | grep '\.root'`
hadd  TTToHadronic_2016_combined_1.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452//TTToHadronic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTbarMC_2016_/230911_220322/0001 | grep '\.root'`
hadd  TTToHadronic_2016_combined_2.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452//TTToHadronic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTbarMC_2016_/230911_220322/0002 | grep '\.root'`

TTToHadronic_2016_combined.root TTToHadronic_2016_combined_0.root TTToHadronic_2016_combined_1.root TTToHadronic_2016_combined_2.root

