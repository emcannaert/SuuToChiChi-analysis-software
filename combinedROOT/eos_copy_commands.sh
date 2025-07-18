hadd -f root://cmseos.fnal.gov/$EOSHOME/combinedROOT_temp/dataA_2018_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2025310_13562/JetHT/clustAlg_dataA_2018_nom/250707_202418/0000 | grep "\.root"`
hadd -f root://cmseos.fnal.gov/$EOSHOME/combinedROOT_temp/dataB_2018_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2025310_13562/JetHT/clustAlg_dataB_2018_nom/250707_203136/0000 | grep "\.root"`
hadd -f root://cmseos.fnal.gov/$EOSHOME/combinedROOT_temp/dataC_2018_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2025310_13562/JetHT/clustAlg_dataC_2018_nom/250707_203702/0000 | grep "\.root"`
hadd -f root://cmseos.fnal.gov/$EOSHOME/combinedROOT_temp/dataD_2018_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2025310_13562/JetHT/clustAlg_dataD_2018_nom/250707_204228/0000 | grep "\.root"`
eosmv $EOSHOME/combinedROOT_temp/dataD_2018_nom_combined_0.root $EOSHOME/combinedROOT/dataD_2018_nom_combined.root
eosmv $EOSHOME/combinedROOT_temp/dataA_2018_nom_combined_0.root $EOSHOME/combinedROOT/dataA_2018_nom_combined.root
eosmv $EOSHOME/combinedROOT_temp/dataC_2018_nom_combined_0.root $EOSHOME/combinedROOT/dataC_2018_nom_combined.root
eosmv $EOSHOME/combinedROOT_temp/dataB_2018_nom_combined_0.root $EOSHOME/combinedROOT/dataB_2018_nom_combined.root
