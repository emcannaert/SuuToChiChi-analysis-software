hadd  QCD_HT1000to1500_2017_combined.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraph-pythia8/clustAlg_QCDMC1000to1500_2017_/230911_220415/0000 | grep '\.root'`
hadd  QCD_HT1500to2000_2017_combined.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/clustAlg_QCDMC1500to2000_2017_/230911_220600/0000 | grep '\.root'`
hadd  QCD_HT2000toInf_2017_combined.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraph-pythia8/clustAlg_QCDMC2000toInf_2017_/230911_220508/0000 | grep '\.root'`
hadd  TTToHadronic_2017_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452//TTToHadronic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTbarMC_2017_/230911_220653/0000 | grep '\.root'`
hadd  TTToHadronic_2017_combined_1.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023911_165452//TTToHadronic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTbarMC_2017_/230911_220653/0001 | grep '\.root'`
hadd  TTToHadronic_2017_combined_2.root `xrdfsls -u  /store/user/ecannaer/SuuToChiChi_2023911_165452//TTToHadronic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTbarMC_2017_/230911_220653/0002 | grep '\.root'`

TTToHadronic_2017_combined.root TTToHadronic_2017_combined_0.root TTToHadronic_2017_combined_1.root TTToHadronic_2017_combined_2.root

