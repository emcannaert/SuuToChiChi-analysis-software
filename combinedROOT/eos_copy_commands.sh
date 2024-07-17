hadd -f dataB_2017_JEC_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024710_12747/JetHT/clustAlg_dataB_2017_JEC/240710_174305/0000 | grep "\.root"`
hadd -f dataB_2017_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024710_12747/JetHT/clustAlg_dataB_2017_nom/240710_175141/0000 | grep "\.root"`
hadd -f dataC_2017_JEC_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024710_12747/JetHT/clustAlg_dataC_2017_JEC/240710_174449/0000 | grep "\.root"`
hadd -f dataC_2017_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024710_12747/JetHT/clustAlg_dataC_2017_nom/240710_175322/0000 | grep "\.root"`
hadd -f dataD_2017_JEC_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024710_12747/JetHT/clustAlg_dataD_2017_JEC/240710_174631/0000 | grep "\.root"`
hadd -f dataD_2017_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024710_12747/JetHT/clustAlg_dataD_2017_nom/240710_175506/0000 | grep "\.root"`
hadd -f dataE_2017_JEC_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024710_12747/JetHT/clustAlg_dataE_2017_JEC/240710_174816/0000 | grep "\.root"`
hadd -f dataE_2017_JEC_combined_1.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024710_12747/JetHT/clustAlg_dataE_2017_JEC/240710_174816/0001 | grep "\.root"`
hadd -f dataE_2017_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024710_12747/JetHT/clustAlg_dataE_2017_nom/240710_175647/0000 | grep "\.root"`
hadd -f dataE_2017_nom_combined_1.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024710_12747/JetHT/clustAlg_dataE_2017_nom/240710_175647/0001 | grep "\.root"`
hadd -f dataF_2017_JEC_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024710_12747/JetHT/clustAlg_dataF_2017_JEC/240710_174957/0000 | grep "\.root"`
hadd -f dataF_2017_JEC_combined_1.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024710_12747/JetHT/clustAlg_dataF_2017_JEC/240710_174957/0001 | grep "\.root"`
hadd -f dataF_2017_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024710_12747/JetHT/clustAlg_dataF_2017_nom/240710_175829/0000 | grep "\.root"`
hadd -f dataF_2017_nom_combined_1.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024710_12747/JetHT/clustAlg_dataF_2017_nom/240710_175829/0001 | grep "\.root"`
hadd -f dataE_2017_JEC_combined.root  dataE_2017_JEC_combined_0.root dataE_2017_JEC_combined_1.root
hadd -f dataE_2017_nom_combined.root  dataE_2017_nom_combined_0.root dataE_2017_nom_combined_1.root
mv dataD_2017_JEC_combined_0.root dataD_2017_JEC_combined.root
mv dataD_2017_nom_combined_0.root dataD_2017_nom_combined.root
hadd -f dataF_2017_JEC_combined.root  dataF_2017_JEC_combined_0.root dataF_2017_JEC_combined_1.root
hadd -f dataF_2017_nom_combined.root  dataF_2017_nom_combined_0.root dataF_2017_nom_combined_1.root
mv dataC_2017_JEC_combined_0.root dataC_2017_JEC_combined.root
mv dataC_2017_nom_combined_0.root dataC_2017_nom_combined.root
mv dataB_2017_JEC_combined_0.root dataB_2017_JEC_combined.root
mv dataB_2017_nom_combined_0.root dataB_2017_nom_combined.root
