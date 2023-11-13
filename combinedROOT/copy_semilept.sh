hadd TTToSemiLeptonic_0000.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_semileptonictest/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTToSemiLeptonic_2018_/231110_214906/0000  | grep '\.root'`

hadd TTToSemiLeptonic_0001.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_semileptonictest/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTToSemiLeptonic_2018_/231110_214906/0001  | grep '\.root'`
hadd TTToSemiLeptonic_0002.root `xrdfsls -u /store/user/ecannaer/SuuToChiChi_semileptonictest/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/clustAlg_TTToSemiLeptonic_2018_/231110_214906/0002  | grep '\.root'`

hadd TTToSemiLeptonic_combined.root TTToSemiLeptonic_0000.root TTToSemiLeptonic_0001.root TTToSemiLeptonic_0002.root
rm TTToSemiLeptonic_0000.root TTToSemiLeptonic_0001.root TTToSemiLeptonic_0002.root
