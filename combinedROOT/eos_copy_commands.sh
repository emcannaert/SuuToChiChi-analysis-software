hadd -f Suu7_chi2p5_HTHT_2018_JEC1_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20241218_155211/SuuToChiChiToHTHTToJets_MSuu-7000_MChi-2500_TuneCP5_13TeV-madgraph-pythia8/clustAlg_Suu7_chi2p5_HTHT_2018_JEC1/241219_004501/0000 | grep "\.root"`
hadd -f Suu7_chi2p5_HTHT_2018_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20241218_155211/SuuToChiChiToHTHTToJets_MSuu-7000_MChi-2500_TuneCP5_13TeV-madgraph-pythia8/clustAlg_Suu7_chi2p5_HTHT_2018_nom/241219_004906/0000 | grep "\.root"`
hadd -f Suu5_chi2_HTZT_2018_JEC1_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20241218_155211/SuuToChiChiToHTZTToJets_MSuu-5000_MChi-2000_TuneCP5_13TeV-madgraph-pythia8/clustAlg_Suu5_chi2_HTZT_2018_JEC1/241219_001032/0000 | grep "\.root"`
hadd -f Suu5_chi2_HTZT_2018_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20241218_155211/SuuToChiChiToHTZTToJets_MSuu-5000_MChi-2000_TuneCP5_13TeV-madgraph-pythia8/clustAlg_Suu5_chi2_HTZT_2018_nom/241219_001649/0000 | grep "\.root"`
hadd -f Suu5_chi1p5_ZTZT_2018_JEC1_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20241218_155211/SuuToChiChiToZTZTToJets_MSuu-5000_MChi-1500_TuneCP5_13TeV-madgraph-pythia8/clustAlg_Suu5_chi1p5_ZTZT_2018_JEC1/241218_223217/0000 | grep "\.root"`
hadd -f Suu5_chi1p5_ZTZT_2018_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20241218_155211/SuuToChiChiToZTZTToJets_MSuu-5000_MChi-1500_TuneCP5_13TeV-madgraph-pythia8/clustAlg_Suu5_chi1p5_ZTZT_2018_nom/241218_223413/0000 | grep "\.root"`
hadd -f Suu6_chi2_ZTZT_2018_JEC1_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20241218_155211/SuuToChiChiToZTZTToJets_MSuu-6000_MChi-2000_TuneCP5_13TeV-madgraph-pythia8/clustAlg_Suu6_chi2_ZTZT_2018_JEC1/241218_230053/0000 | grep "\.root"`
hadd -f Suu6_chi2_ZTZT_2018_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20241218_155211/SuuToChiChiToZTZTToJets_MSuu-6000_MChi-2000_TuneCP5_13TeV-madgraph-pythia8/clustAlg_Suu6_chi2_ZTZT_2018_nom/241218_230252/0000 | grep "\.root"`
hadd -f Suu8_chi3_ZTZT_2018_JEC1_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20241218_155211/SuuToChiChiToZTZTToJets_MSuu-8000_MChi-3000_TuneCP5_13TeV-madgraph-pythia8/clustAlg_Suu8_chi3_ZTZT_2018_JEC1/241218_233810/0000 | grep "\.root"`
hadd -f Suu8_chi3_ZTZT_2018_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_20241218_155211/SuuToChiChiToZTZTToJets_MSuu-8000_MChi-3000_TuneCP5_13TeV-madgraph-pythia8/clustAlg_Suu8_chi3_ZTZT_2018_nom/241218_234424/0000 | grep "\.root"`
mv Suu5_chi1p5_ZTZT_2018_JEC1_combined_0.root Suu5_chi1p5_ZTZT_2018_JEC1_combined.root
mv Suu5_chi1p5_ZTZT_2018_nom_combined_0.root Suu5_chi1p5_ZTZT_2018_nom_combined.root
mv Suu8_chi3_ZTZT_2018_JEC1_combined_0.root Suu8_chi3_ZTZT_2018_JEC1_combined.root
mv Suu8_chi3_ZTZT_2018_nom_combined_0.root Suu8_chi3_ZTZT_2018_nom_combined.root
mv Suu6_chi2_ZTZT_2018_JEC1_combined_0.root Suu6_chi2_ZTZT_2018_JEC1_combined.root
mv Suu6_chi2_ZTZT_2018_nom_combined_0.root Suu6_chi2_ZTZT_2018_nom_combined.root
mv Suu5_chi2_HTZT_2018_JEC1_combined_0.root Suu5_chi2_HTZT_2018_JEC1_combined.root
mv Suu5_chi2_HTZT_2018_nom_combined_0.root Suu5_chi2_HTZT_2018_nom_combined.root
mv Suu7_chi2p5_HTHT_2018_JEC1_combined_0.root Suu7_chi2p5_HTHT_2018_JEC1_combined.root
mv Suu7_chi2p5_HTHT_2018_nom_combined_0.root Suu7_chi2p5_HTHT_2018_nom_combined.root
