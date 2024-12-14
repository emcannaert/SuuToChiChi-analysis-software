hadd -f WJetsMC_LNu-HT1200to2500_2015_JEC1_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_SuuToChiChi_SuuToChiChi_2024126_225952/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/clustAlg_WJetsMC_LNu-HT1200to2500_2015_JEC1/241214_031831/0000 | grep "\.root"`
hadd -f WJetsMC_LNu-HT1200to2500_2015_JEC2_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_SuuToChiChi_SuuToChiChi_2024126_225952/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/clustAlg_WJetsMC_LNu-HT1200to2500_2015_JEC2/241214_032228/0000 | grep "\.root"`
mv WJetsMC_LNu-HT1200to2500_2015_JEC2_combined_0.root WJetsMC_LNu-HT1200to2500_2015_JEC2_combined.root
mv WJetsMC_LNu-HT1200to2500_2015_JEC1_combined_0.root WJetsMC_LNu-HT1200to2500_2015_JEC1_combined.root
