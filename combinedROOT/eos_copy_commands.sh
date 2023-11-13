hadd  ST_t-channel_antitop_2018_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023116_13325/ST_t-channel_antitop_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/clustAlg_ST_t-channel-antitop_2018_/231113_061207/0000 | grep "\.root"`
hadd  ST_t-channel_top_2018_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023116_13325/ST_t-channel_top_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/clustAlg_ST_t-channel-top_2018_/231113_061055/0000 | grep "\.root"`
hadd  ST_tW_antitop_2018_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023116_13325/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/clustAlg_ST_tW-antiTop_2018_/231113_061318/0000 | grep "\.root"`
hadd  ST_tW_top_2018_nom_combined_0_.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2023116_13325/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/clustAlg_ST_tW-top_2018_/231113_061429/0000 | grep "\.root"`
mv ST_t-channel_antitop_2018_nom_combined_0_.root ST_t-channel_antitop_2018_nom_combined.root
mv ST_tW_top_2018_nom_combined_0_.root ST_tW_top_2018_nom_combined.root
mv ST_t-channel_top_2018_nom_combined_0_.root ST_t-channel_top_2018_nom_combined.root
mv ST_tW_antitop_2018_nom_combined_0_.root ST_tW_antitop_2018_nom_combined.root
