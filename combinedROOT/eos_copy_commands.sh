hadd -f dataB-ver2_2015_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024214_133552/JetHT/clustAlg_dataB-ver2_2015_/240215_070646/0000 | grep "\.root"`
hadd -f dataB-ver2_2015_nom_combined_1.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024214_133552/JetHT/clustAlg_dataB-ver2_2015_/240215_070646/0001 | grep "\.root"`
hadd -f dataB-ver2_2015_JEC_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024214_133552/JetHT/clustAlg_dataB-ver2_2015_JEC/240215_065541/0000 | grep "\.root"`
hadd -f dataB-ver2_2015_JEC_combined_1.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024214_133552/JetHT/clustAlg_dataB-ver2_2015_JEC/240215_065541/0001 | grep "\.root"`
hadd -f dataC-HIPM_2015_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024214_133552/JetHT/clustAlg_dataC-HIPM_2015_/240215_070837/0000 | grep "\.root"`
hadd -f dataC-HIPM_2015_JEC_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024214_133552/JetHT/clustAlg_dataC-HIPM_2015_JEC/240215_065732/0000 | grep "\.root"`
hadd -f dataD-HIPM_2015_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024214_133552/JetHT/clustAlg_dataD-HIPM_2015_/240215_071027/0000 | grep "\.root"`
hadd -f dataD-HIPM_2015_JEC_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024214_133552/JetHT/clustAlg_dataD-HIPM_2015_JEC/240215_065923/0000 | grep "\.root"`
hadd -f dataE-HIPM_2015_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024214_133552/JetHT/clustAlg_dataE-HIPM_2015_/240215_071217/0000 | grep "\.root"`
hadd -f dataE-HIPM_2015_JEC_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024214_133552/JetHT/clustAlg_dataE-HIPM_2015_JEC/240215_070114/0000 | grep "\.root"`
hadd -f dataF-HIPM_2015_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024214_133552/JetHT/clustAlg_dataF-HIPM_2015_/240215_071408/0000 | grep "\.root"`
hadd -f dataF-HIPM_2015_JEC_combined_0.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_2024214_133552/JetHT/clustAlg_dataF-HIPM_2015_JEC/240215_070305/0000 | grep "\.root"`
mv dataC-HIPM_2015_JEC_combined_0.root dataC-HIPM_2015_JEC_combined.root
mv dataC-HIPM_2015_nom_combined_0.root dataC-HIPM_2015_nom_combined.root
hadd -f dataB-ver2_2015_JEC_combined.root  dataB-ver2_2015_JEC_combined_0.root dataB-ver2_2015_JEC_combined_1.root
hadd -f dataB-ver2_2015_nom_combined.root  dataB-ver2_2015_nom_combined_0.root dataB-ver2_2015_nom_combined_1.root
mv dataD-HIPM_2015_JEC_combined_0.root dataD-HIPM_2015_JEC_combined.root
mv dataD-HIPM_2015_nom_combined_0.root dataD-HIPM_2015_nom_combined.root
mv dataF-HIPM_2015_JEC_combined_0.root dataF-HIPM_2015_JEC_combined.root
mv dataF-HIPM_2015_nom_combined_0.root dataF-HIPM_2015_nom_combined.root
mv dataE-HIPM_2015_JEC_combined_0.root dataE-HIPM_2015_JEC_combined.root
mv dataE-HIPM_2015_nom_combined_0.root dataE-HIPM_2015_nom_combined.root
