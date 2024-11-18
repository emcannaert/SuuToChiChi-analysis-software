hadd -f dataA_2018_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/selectionStudy_2024112_134918/JetHT/selectionStudier_dataA_2018_nom/241103_032216/0000 | grep "\.root"`
hadd -f dataB_2018_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/selectionStudy_2024112_134918/JetHT/selectionStudier_dataB_2018_nom/241103_032856/0000 | grep "\.root"`
hadd -f dataC_2018_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/selectionStudy_2024112_134918/JetHT/selectionStudier_dataC_2018_nom/241103_034704/0000 | grep "\.root"`
hadd -f dataD_2018_nom_combined_0.root `xrdfsls -u /store/user/ecannaer/selectionStudy_2024112_134918/JetHT/selectionStudier_dataD_2018_nom/241103_035627/0000 | grep "\.root"`
mv dataD_2018_nom_combined_0.root dataD_2018_nom_combined.root
mv dataA_2018_nom_combined_0.root dataA_2018_nom_combined.root
mv dataC_2018_nom_combined_0.root dataC_2018_nom_combined.root
mv dataB_2018_nom_combined_0.root dataB_2018_nom_combined.root
