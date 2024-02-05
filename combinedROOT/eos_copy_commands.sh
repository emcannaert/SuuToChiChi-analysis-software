hadd  QCDMC1000to1500_2018_JEC_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024129_131131/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/clustAlg_QCDMC1000to1500_2018_JEC/240202_234159/0000 | grep "\.root"`
hadd  QCDMC1500to2000_2018_JEC_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024129_131131/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/clustAlg_QCDMC1500to2000_2018_JEC/240202_234521/0000 | grep "\.root"`
hadd  QCDMC2000toInf_2018_JEC_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024129_131131/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/clustAlg_QCDMC2000toInf_2018_JEC/240202_234340/0000 | grep "\.root"`
hadd  ST_s-channel-hadronsMC_2018_JEC_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024129_131131/ST_s-channel_4f_hadronicDecays_TuneCP5_13TeV-amcatnlo-pythia8/clustAlg_ST_s-channel-hadronsMC_2018_JEC/240202_232647/0000 | grep "\.root"`
hadd  ST_s-channel-leptonsMC_2018_JEC_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024129_131131/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/clustAlg_ST_s-channel-leptonsMC_2018_JEC/240202_232827/0000 | grep "\.root"`
hadd  ST_t-channel-antitop_inclMC_2018_JEC_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024129_131131/ST_t-channel_antitop_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/clustAlg_ST_t-channel-antitop_inclMC_2018_JEC/240202_233007/0000 | grep "\.root"`
hadd  ST_t-channel-top_inclMC_2018_JEC_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024129_131131/ST_t-channel_top_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/clustAlg_ST_t-channel-top_inclMC_2018_JEC/240202_233150/0000 | grep "\.root"`
hadd  ST_tW-antiTop_inclMC_2018_JEC_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024129_131131/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/clustAlg_ST_tW-antiTop_inclMC_2018_JEC/240202_233332/0000 | grep "\.root"`
hadd  ST_tW-top_inclMC_2018_JEC_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024129_131131/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/clustAlg_ST_tW-top_inclMC_2018_JEC/240202_233514/0000 | grep "\.root"`
hadd  TTToLeptonicMC_2018_JEC_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024129_131131/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTToLeptonicMC_2018_JEC/240202_233837/0000 | grep "\.root"`
hadd  TTToHadronicMC_2018_JEC_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024129_131131/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTToHadronicMC_2018_JEC/240202_233656/0000 | grep "\.root"`
hadd  TTToHadronicMC_2018_JEC_combined_1_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024129_131131/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTToHadronicMC_2018_JEC/240202_233656/0001 | grep "\.root"`
hadd  TTToSemiLeptonicMC_2018_JEC_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024129_131131/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTToSemiLeptonicMC_2018_JEC/240202_234019/0000 | grep "\.root"`
hadd  TTToSemiLeptonicMC_2018_JEC_combined_1_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024129_131131/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTToSemiLeptonicMC_2018_JEC/240202_234019/0001 | grep "\.root"`
hadd  TTToSemiLeptonicMC_2018_JEC_combined_2_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024129_131131/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTToSemiLeptonicMC_2018_JEC/240202_234019/0002 | grep "\.root"`
mv ST_t-channel-antitop_inclMC_2018_JEC_combined_0_.root ST_t-channel-antitop_inclMC_2018_JEC_combined.root
mv ST_t-channel-top_inclMC_2018_JEC_combined_0_.root ST_t-channel-top_inclMC_2018_JEC_combined.root
mv ST_tW-antiTop_inclMC_2018_JEC_combined_0_.root ST_tW-antiTop_inclMC_2018_JEC_combined.root
mv QCDMC1000to1500_2018_JEC_combined_0_.root QCDMC1000to1500_2018_JEC_combined.root
mv ST_tW-top_inclMC_2018_JEC_combined_0_.root ST_tW-top_inclMC_2018_JEC_combined.root
hadd TTToHadronicMC_2018_JEC_combined.root  TTToHadronicMC_2018_JEC_combined_0_.root TTToHadronicMC_2018_JEC_combined_1_.root
mv ST_s-channel-leptonsMC_2018_JEC_combined_0_.root ST_s-channel-leptonsMC_2018_JEC_combined.root
mv QCDMC2000toInf_2018_JEC_combined_0_.root QCDMC2000toInf_2018_JEC_combined.root
hadd TTToSemiLeptonicMC_2018_JEC_combined.root  TTToSemiLeptonicMC_2018_JEC_combined_0_.root TTToSemiLeptonicMC_2018_JEC_combined_1_.root TTToSemiLeptonicMC_2018_JEC_combined_2_.root
mv ST_s-channel-hadronsMC_2018_JEC_combined_0_.root ST_s-channel-hadronsMC_2018_JEC_combined.root
mv QCDMC1500to2000_2018_JEC_combined_0_.root QCDMC1500to2000_2018_JEC_combined.root
mv TTToLeptonicMC_2018_JEC_combined_0_.root TTToLeptonicMC_2018_JEC_combined.root
