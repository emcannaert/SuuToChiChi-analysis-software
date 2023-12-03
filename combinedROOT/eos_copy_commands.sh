hadd  QCDMC1000to1500_2015_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20231127_23944/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/clustAlg_QCDMC1000to1500_2015_/231130_231204/0000 | grep "\.root"`
hadd  QCDMC1500to2000_2015_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20231127_23944/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/clustAlg_QCDMC1500to2000_2015_/231130_231438/0000 | grep "\.root"`
hadd  QCDMC2000toInf_2015_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20231127_23944/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/clustAlg_QCDMC2000toInf_2015_/231130_231321/0000 | grep "\.root"`
hadd  ST_s-channel-hadronsMC_2015_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20231127_23944/ST_s-channel_4f_hadronicDecays_TuneCP5_13TeV-amcatnlo-pythia8/clustAlg_ST_s-channel-hadronsMC_2015_/231130_230043/0000 | grep "\.root"`
hadd  ST_s-channel-leptonsMC_2015_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20231127_23944/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/clustAlg_ST_s-channel-leptonsMC_2015_/231130_230158/0000 | grep "\.root"`
hadd  ST_t-channel-antitop_inclMC_2015_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20231127_23944/ST_t-channel_antitop_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/clustAlg_ST_t-channel-antitop_inclMC_2015_/231130_230315/0000 | grep "\.root"`
hadd  ST_t-channel-top_inclMC_2015_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20231127_23944/ST_t-channel_top_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/clustAlg_ST_t-channel-top_inclMC_2015_/231130_230430/0000 | grep "\.root"`
hadd  ST_tW-antiTop_inclMC_2015_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20231127_23944/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/clustAlg_ST_tW-antiTop_inclMC_2015_/231130_230546/0000 | grep "\.root"`
hadd  ST_tW-top_inclMC_2015_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20231127_23944/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/clustAlg_ST_tW-top_inclMC_2015_/231130_230702/0000 | grep "\.root"`
hadd  TTToLeptonicMC_2015_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20231127_23944/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTToLeptonicMC_2015_/231130_230817/0000 | grep "\.root"`
hadd  TTToHadronicMC_2015_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20231127_23944/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTToHadronicMC_2015_/231130_230933/0000 | grep "\.root"`
hadd  TTToHadronicMC_2015_nom_combined_1_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20231127_23944/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTToHadronicMC_2015_/231130_230933/0001 | grep "\.root"`
hadd  TTToSemiLeptonicMC_2015_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20231127_23944/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8//clustAlg_TTToSemiLeptonicMC_2015_/231130_231048/0000 | grep "\.root"`
mv ST_t-channel-top_inclMC_2015_nom_combined_0_.root ST_t-channel-top_inclMC_2015_nom_combined.root
mv QCDMC1000to1500_2015_nom_combined_0_.root QCDMC1000to1500_2015_nom_combined.root
mv ST_tW-top_inclMC_2015_nom_combined_0_.root ST_tW-top_inclMC_2015_nom_combined.root
mv TTToLeptonicMC_2015_nom_combined_0_.root TTToLeptonicMC_2015_nom_combined.root
mv ST_t-channel-antitop_inclMC_2015_nom_combined_0_.root ST_t-channel-antitop_inclMC_2015_nom_combined.root
mv ST_tW-antiTop_inclMC_2015_nom_combined_0_.root ST_tW-antiTop_inclMC_2015_nom_combined.root
hadd TTToHadronicMC_2015_nom_combined.root  TTToHadronicMC_2015_nom_combined_0_.root TTToHadronicMC_2015_nom_combined_1_.root
mv ST_s-channel-leptonsMC_2015_nom_combined_0_.root ST_s-channel-leptonsMC_2015_nom_combined.root
mv QCDMC2000toInf_2015_nom_combined_0_.root QCDMC2000toInf_2015_nom_combined.root
mv TTToSemiLeptonicMC_2015_nom_combined_0_.root TTToSemiLeptonicMC_2015_nom_combined.root
mv ST_s-channel-hadronsMC_2015_nom_combined_0_.root ST_s-channel-hadronsMC_2015_nom_combined.root
mv QCDMC1500to2000_2015_nom_combined_0_.root QCDMC1500to2000_2015_nom_combined.root
