import FWCore.ParameterSet.Config as cms

process = cms.Process("analysis")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/data/Run2016F/JetHT/MINIAOD/UL2016_MiniAODv2-v2/140000/17267C16-E284-0D44-B0BB-D996C0CEBEB7.root')
)
process.EmptyJetIdParams = cms.PSet(
    Pt010_Loose = cms.vdouble(-999.0, -999.0, -999.0, -999.0),
    Pt010_Medium = cms.vdouble(-999.0, -999.0, -999.0, -999.0),
    Pt010_Tight = cms.vdouble(-999.0, -999.0, -999.0, -999.0),
    Pt1020_Loose = cms.vdouble(-999.0, -999.0, -999.0, -999.0),
    Pt1020_Medium = cms.vdouble(-999.0, -999.0, -999.0, -999.0),
    Pt1020_Tight = cms.vdouble(-999.0, -999.0, -999.0, -999.0),
    Pt2030_Loose = cms.vdouble(-999.0, -999.0, -999.0, -999.0),
    Pt2030_Medium = cms.vdouble(-999.0, -999.0, -999.0, -999.0),
    Pt2030_Tight = cms.vdouble(-999.0, -999.0, -999.0, -999.0),
    Pt3040_Loose = cms.vdouble(-999.0, -999.0, -999.0, -999.0),
    Pt3040_Medium = cms.vdouble(-999.0, -999.0, -999.0, -999.0),
    Pt3040_Tight = cms.vdouble(-999.0, -999.0, -999.0, -999.0),
    Pt4050_Loose = cms.vdouble(-999.0, -999.0, -999.0, -999.0),
    Pt4050_Medium = cms.vdouble(-999.0, -999.0, -999.0, -999.0),
    Pt4050_Tight = cms.vdouble(-999.0, -999.0, -999.0, -999.0)
)

process.HFRecalParameterBlock = cms.PSet(
    HFdepthOneParameterA = cms.vdouble(
        0.004123, 0.00602, 0.008201, 0.010489, 0.013379, 
        0.016997, 0.021464, 0.027371, 0.034195, 0.044807, 
        0.058939, 0.125497
    ),
    HFdepthOneParameterB = cms.vdouble(
        -4e-06, -2e-06, 0.0, 4e-06, 1.5e-05, 
        2.6e-05, 6.3e-05, 8.4e-05, 0.00016, 0.000107, 
        0.000425, 0.000209
    ),
    HFdepthTwoParameterA = cms.vdouble(
        0.002861, 0.004168, 0.0064, 0.008388, 0.011601, 
        0.014425, 0.018633, 0.023232, 0.028274, 0.035447, 
        0.051579, 0.086593
    ),
    HFdepthTwoParameterB = cms.vdouble(
        -2e-06, -0.0, -7e-06, -6e-06, -2e-06, 
        1e-06, 1.9e-05, 3.1e-05, 6.7e-05, 1.2e-05, 
        0.000157, -3e-06
    )
)

process.JetIdParams = cms.PSet(
    Pt010_Loose = cms.vdouble(0.0, 0.0, 0.0, 0.2),
    Pt010_Medium = cms.vdouble(0.2, 0.4, 0.2, 0.6),
    Pt010_Tight = cms.vdouble(0.5, 0.6, 0.6, 0.9),
    Pt1020_Loose = cms.vdouble(-0.4, -0.4, -0.4, 0.4),
    Pt1020_Medium = cms.vdouble(-0.3, 0.0, 0.0, 0.5),
    Pt1020_Tight = cms.vdouble(-0.2, 0.2, 0.2, 0.6),
    Pt2030_Loose = cms.vdouble(0.0, 0.0, 0.2, 0.6),
    Pt2030_Medium = cms.vdouble(0.2, 0.2, 0.5, 0.7),
    Pt2030_Tight = cms.vdouble(0.3, 0.4, 0.7, 0.8),
    Pt3040_Loose = cms.vdouble(0.0, 0.0, 0.6, 0.2),
    Pt3040_Medium = cms.vdouble(0.3, 0.2, 0.7, 0.8),
    Pt3040_Tight = cms.vdouble(0.5, 0.4, 0.8, 0.9),
    Pt4050_Loose = cms.vdouble(0.0, 0.0, 0.6, 0.2),
    Pt4050_Medium = cms.vdouble(0.3, 0.2, 0.7, 0.8),
    Pt4050_Tight = cms.vdouble(0.5, 0.4, 0.8, 0.9)
)

process.PhilV1 = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(0.0, 0.0, 0.0, 0.2),
        Pt010_Medium = cms.vdouble(0.2, 0.4, 0.2, 0.6),
        Pt010_Tight = cms.vdouble(0.5, 0.6, 0.6, 0.9),
        Pt1020_Loose = cms.vdouble(-0.4, -0.4, -0.4, 0.4),
        Pt1020_Medium = cms.vdouble(-0.3, 0.0, 0.0, 0.5),
        Pt1020_Tight = cms.vdouble(-0.2, 0.2, 0.2, 0.6),
        Pt2030_Loose = cms.vdouble(0.0, 0.0, 0.2, 0.6),
        Pt2030_Medium = cms.vdouble(0.2, 0.2, 0.5, 0.7),
        Pt2030_Tight = cms.vdouble(0.3, 0.4, 0.7, 0.8),
        Pt3040_Loose = cms.vdouble(0.0, 0.0, 0.6, 0.2),
        Pt3040_Medium = cms.vdouble(0.3, 0.2, 0.7, 0.8),
        Pt3040_Tight = cms.vdouble(0.5, 0.4, 0.8, 0.9),
        Pt4050_Loose = cms.vdouble(0.0, 0.0, 0.6, 0.2),
        Pt4050_Medium = cms.vdouble(0.3, 0.2, 0.7, 0.8),
        Pt4050_Tight = cms.vdouble(0.5, 0.4, 0.8, 0.9)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(False),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('philv1'),
    tmvaMethod = cms.string('JetID'),
    tmvaSpectators = cms.vstring(),
    tmvaVariables = cms.vstring(
        'nvtx', 
        'jetPt', 
        'jetEta', 
        'jetPhi', 
        'dZ', 
        'd0', 
        'beta', 
        'betaStar', 
        'nCharged', 
        'nNeutrals', 
        'dRMean', 
        'frac01', 
        'frac02', 
        'frac03', 
        'frac04', 
        'frac05'
    ),
    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/mva_JetID_v1.weights.xml.gz'),
    version = cms.int32(-1)
)

process.PuJetIdCutBased_wp = cms.PSet(
    Pt010_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
    Pt010_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
    Pt010_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
    Pt010_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.07),
    Pt010_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
    Pt010_RMSTight = cms.vdouble(0.06, 0.07, 0.04, 0.05),
    Pt1020_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
    Pt1020_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
    Pt1020_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
    Pt1020_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.07),
    Pt1020_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
    Pt1020_RMSTight = cms.vdouble(0.06, 0.07, 0.04, 0.05),
    Pt2030_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
    Pt2030_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
    Pt2030_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
    Pt2030_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
    Pt2030_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
    Pt2030_RMSTight = cms.vdouble(0.05, 0.07, 0.03, 0.045),
    Pt3040_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
    Pt3040_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
    Pt3040_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
    Pt3040_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
    Pt3040_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
    Pt3040_RMSTight = cms.vdouble(0.05, 0.06, 0.03, 0.04),
    Pt4050_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
    Pt4050_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
    Pt4050_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
    Pt4050_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
    Pt4050_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
    Pt4050_RMSTight = cms.vdouble(0.05, 0.06, 0.03, 0.04)
)

process.PuJetIdMinMVA_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.9, -0.9, -0.94, -0.9),
    Pt010_Medium = cms.vdouble(-0.73, -0.89, -0.89, -0.83),
    Pt010_Tight = cms.vdouble(-0.5, -0.2, -0.83, -0.7),
    Pt1020_Loose = cms.vdouble(-0.9, -0.9, -0.94, -0.9),
    Pt1020_Medium = cms.vdouble(-0.73, -0.89, -0.89, -0.83),
    Pt1020_Tight = cms.vdouble(-0.5, -0.2, -0.83, -0.7),
    Pt2030_Loose = cms.vdouble(-0.4, -0.85, -0.7, -0.6),
    Pt2030_Medium = cms.vdouble(0.1, -0.4, -0.5, -0.45),
    Pt2030_Tight = cms.vdouble(-0.2, 0.0, 0.0, 0.0),
    Pt3040_Loose = cms.vdouble(-0.4, -0.85, -0.7, -0.6),
    Pt3040_Medium = cms.vdouble(0.1, -0.4, -0.5, -0.45),
    Pt3040_Tight = cms.vdouble(-0.2, 0.0, 0.0, 0.0),
    Pt4050_Loose = cms.vdouble(-0.4, -0.85, -0.7, -0.6),
    Pt4050_Medium = cms.vdouble(0.1, -0.4, -0.5, -0.45),
    Pt4050_Tight = cms.vdouble(-0.2, 0.0, 0.0, 0.0)
)

process.PuJetIdOptMVA_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.9, -0.9, -0.9, -0.9),
    Pt010_Medium = cms.vdouble(-0.73, -0.89, -0.89, -0.83),
    Pt010_Tight = cms.vdouble(-0.5, -0.2, -0.83, -0.7),
    Pt1020_Loose = cms.vdouble(-0.9, -0.9, -0.9, -0.9),
    Pt1020_Medium = cms.vdouble(-0.73, -0.89, -0.89, -0.83),
    Pt1020_Tight = cms.vdouble(-0.5, -0.2, -0.83, -0.7),
    Pt2030_Loose = cms.vdouble(-0.4, -0.85, -0.7, -0.6),
    Pt2030_Medium = cms.vdouble(0.1, -0.4, -0.4, -0.45),
    Pt2030_Tight = cms.vdouble(-0.2, 0.0, 0.0, 0.0),
    Pt3040_Loose = cms.vdouble(-0.4, -0.85, -0.7, -0.6),
    Pt3040_Medium = cms.vdouble(0.1, -0.4, -0.4, -0.45),
    Pt3040_Tight = cms.vdouble(-0.2, 0.0, 0.0, 0.0),
    Pt4050_Loose = cms.vdouble(-0.4, -0.85, -0.7, -0.6),
    Pt4050_Medium = cms.vdouble(0.1, -0.4, -0.4, -0.45),
    Pt4050_Tight = cms.vdouble(-0.2, 0.0, 0.0, 0.0)
)

process.cutbased = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
        Pt010_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
        Pt010_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
        Pt010_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.07),
        Pt010_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
        Pt010_RMSTight = cms.vdouble(0.06, 0.07, 0.04, 0.05),
        Pt1020_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
        Pt1020_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
        Pt1020_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
        Pt1020_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.07),
        Pt1020_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
        Pt1020_RMSTight = cms.vdouble(0.06, 0.07, 0.04, 0.05),
        Pt2030_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
        Pt2030_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
        Pt2030_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
        Pt2030_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
        Pt2030_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
        Pt2030_RMSTight = cms.vdouble(0.05, 0.07, 0.03, 0.045),
        Pt3040_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
        Pt3040_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
        Pt3040_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
        Pt3040_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
        Pt3040_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
        Pt3040_RMSTight = cms.vdouble(0.05, 0.06, 0.03, 0.04),
        Pt4050_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
        Pt4050_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
        Pt4050_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
        Pt4050_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
        Pt4050_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
        Pt4050_RMSTight = cms.vdouble(0.05, 0.06, 0.03, 0.04)
    ),
    cutBased = cms.bool(True),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('cutbased')
)

process.full_102x_chs = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
        Pt010_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
        Pt010_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
        Pt1020_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
        Pt1020_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
        Pt1020_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
        Pt2030_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
        Pt2030_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
        Pt2030_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
        Pt3040_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
        Pt3040_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
        Pt3040_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01),
        Pt4050_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
        Pt4050_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
        Pt4050_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(True),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('full'),
    nEtaBins = cms.int32(4),
    tmvaMethod = cms.string('JetIDMVAHighPt'),
    tmvaSpectators = cms.vstring(
        'jetPt', 
        'jetEta'
    ),
    trainings = cms.VPSet(
        cms.PSet(
            jEtaMax = cms.double(2.5),
            jEtaMin = cms.double(0.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_102X_Eta0p0To2p5_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(2.75),
            jEtaMin = cms.double(2.5),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_102X_Eta2p5To2p75_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(3.0),
            jEtaMin = cms.double(2.75),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_102X_Eta2p75To3p0_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(5.0),
            jEtaMin = cms.double(3.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'nParticles', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_102X_Eta3p0To5p0_chs_BDT.weights.xml.gz')
        )
    ),
    version = cms.int32(-1)
)

process.full_102x_chs_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
    Pt010_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
    Pt010_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
    Pt1020_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
    Pt1020_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
    Pt1020_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
    Pt2030_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
    Pt2030_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
    Pt2030_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
    Pt3040_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
    Pt3040_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
    Pt3040_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01),
    Pt4050_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
    Pt4050_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
    Pt4050_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01)
)

process.full_106x_UL16APV_chs = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(0.71, -0.32, -0.3, -0.22),
        Pt010_Medium = cms.vdouble(0.2, -0.56, -0.43, -0.38),
        Pt010_Tight = cms.vdouble(-0.95, -0.7, -0.52, -0.49),
        Pt1020_Loose = cms.vdouble(0.71, -0.32, -0.3, -0.22),
        Pt1020_Medium = cms.vdouble(0.2, -0.56, -0.43, -0.38),
        Pt1020_Tight = cms.vdouble(-0.95, -0.7, -0.52, -0.49),
        Pt2030_Loose = cms.vdouble(0.87, -0.08, -0.16, -0.12),
        Pt2030_Medium = cms.vdouble(0.62, -0.39, -0.32, -0.29),
        Pt2030_Tight = cms.vdouble(-0.9, -0.57, -0.43, -0.42),
        Pt3040_Loose = cms.vdouble(0.94, 0.24, 0.05, 0.1),
        Pt3040_Medium = cms.vdouble(0.86, -0.1, -0.15, -0.08),
        Pt3040_Tight = cms.vdouble(-0.71, -0.36, -0.29, -0.23),
        Pt4050_Loose = cms.vdouble(0.97, 0.48, 0.26, 0.29),
        Pt4050_Medium = cms.vdouble(0.93, 0.19, 0.04, 0.12),
        Pt4050_Tight = cms.vdouble(-0.42, -0.09, -0.14, -0.02)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(True),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('full'),
    nEtaBins = cms.int32(4),
    tmvaMethod = cms.string('JetIDMVAHighPt'),
    tmvaSpectators = cms.vstring(
        'jetPt', 
        'jetEta'
    ),
    trainings = cms.VPSet(
        cms.PSet(
            jEtaMax = cms.double(2.5),
            jEtaMin = cms.double(0.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL16APV_Eta0p0To2p5_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(2.75),
            jEtaMin = cms.double(2.5),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL16APV_Eta2p5To2p75_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(3.0),
            jEtaMin = cms.double(2.75),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL16APV_Eta2p75To3p0_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(5.0),
            jEtaMin = cms.double(3.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'nParticles', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL16APV_Eta3p0To5p0_chs_BDT.weights.xml.gz')
        )
    ),
    version = cms.int32(-1)
)

process.full_106x_UL16APV_chs_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(0.71, -0.32, -0.3, -0.22),
    Pt010_Medium = cms.vdouble(0.2, -0.56, -0.43, -0.38),
    Pt010_Tight = cms.vdouble(-0.95, -0.7, -0.52, -0.49),
    Pt1020_Loose = cms.vdouble(0.71, -0.32, -0.3, -0.22),
    Pt1020_Medium = cms.vdouble(0.2, -0.56, -0.43, -0.38),
    Pt1020_Tight = cms.vdouble(-0.95, -0.7, -0.52, -0.49),
    Pt2030_Loose = cms.vdouble(0.87, -0.08, -0.16, -0.12),
    Pt2030_Medium = cms.vdouble(0.62, -0.39, -0.32, -0.29),
    Pt2030_Tight = cms.vdouble(-0.9, -0.57, -0.43, -0.42),
    Pt3040_Loose = cms.vdouble(0.94, 0.24, 0.05, 0.1),
    Pt3040_Medium = cms.vdouble(0.86, -0.1, -0.15, -0.08),
    Pt3040_Tight = cms.vdouble(-0.71, -0.36, -0.29, -0.23),
    Pt4050_Loose = cms.vdouble(0.97, 0.48, 0.26, 0.29),
    Pt4050_Medium = cms.vdouble(0.93, 0.19, 0.04, 0.12),
    Pt4050_Tight = cms.vdouble(-0.42, -0.09, -0.14, -0.02)
)

process.full_106x_UL16_chs = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(0.71, -0.32, -0.3, -0.22),
        Pt010_Medium = cms.vdouble(0.2, -0.56, -0.43, -0.38),
        Pt010_Tight = cms.vdouble(-0.95, -0.7, -0.52, -0.49),
        Pt1020_Loose = cms.vdouble(0.71, -0.32, -0.3, -0.22),
        Pt1020_Medium = cms.vdouble(0.2, -0.56, -0.43, -0.38),
        Pt1020_Tight = cms.vdouble(-0.95, -0.7, -0.52, -0.49),
        Pt2030_Loose = cms.vdouble(0.87, -0.08, -0.16, -0.12),
        Pt2030_Medium = cms.vdouble(0.62, -0.39, -0.32, -0.29),
        Pt2030_Tight = cms.vdouble(-0.9, -0.57, -0.43, -0.42),
        Pt3040_Loose = cms.vdouble(0.94, 0.24, 0.05, 0.1),
        Pt3040_Medium = cms.vdouble(0.86, -0.1, -0.15, -0.08),
        Pt3040_Tight = cms.vdouble(-0.71, -0.36, -0.29, -0.23),
        Pt4050_Loose = cms.vdouble(0.97, 0.48, 0.26, 0.29),
        Pt4050_Medium = cms.vdouble(0.93, 0.19, 0.04, 0.12),
        Pt4050_Tight = cms.vdouble(-0.42, -0.09, -0.14, -0.02)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(True),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('full'),
    nEtaBins = cms.int32(4),
    tmvaMethod = cms.string('JetIDMVAHighPt'),
    tmvaSpectators = cms.vstring(
        'jetPt', 
        'jetEta'
    ),
    trainings = cms.VPSet(
        cms.PSet(
            jEtaMax = cms.double(2.5),
            jEtaMin = cms.double(0.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL16_Eta0p0To2p5_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(2.75),
            jEtaMin = cms.double(2.5),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL16_Eta2p5To2p75_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(3.0),
            jEtaMin = cms.double(2.75),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL16_Eta2p75To3p0_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(5.0),
            jEtaMin = cms.double(3.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'nParticles', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL16_Eta3p0To5p0_chs_BDT.weights.xml.gz')
        )
    ),
    version = cms.int32(-1)
)

process.full_106x_UL16_chs_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(0.71, -0.32, -0.3, -0.22),
    Pt010_Medium = cms.vdouble(0.2, -0.56, -0.43, -0.38),
    Pt010_Tight = cms.vdouble(-0.95, -0.7, -0.52, -0.49),
    Pt1020_Loose = cms.vdouble(0.71, -0.32, -0.3, -0.22),
    Pt1020_Medium = cms.vdouble(0.2, -0.56, -0.43, -0.38),
    Pt1020_Tight = cms.vdouble(-0.95, -0.7, -0.52, -0.49),
    Pt2030_Loose = cms.vdouble(0.87, -0.08, -0.16, -0.12),
    Pt2030_Medium = cms.vdouble(0.62, -0.39, -0.32, -0.29),
    Pt2030_Tight = cms.vdouble(-0.9, -0.57, -0.43, -0.42),
    Pt3040_Loose = cms.vdouble(0.94, 0.24, 0.05, 0.1),
    Pt3040_Medium = cms.vdouble(0.86, -0.1, -0.15, -0.08),
    Pt3040_Tight = cms.vdouble(-0.71, -0.36, -0.29, -0.23),
    Pt4050_Loose = cms.vdouble(0.97, 0.48, 0.26, 0.29),
    Pt4050_Medium = cms.vdouble(0.93, 0.19, 0.04, 0.12),
    Pt4050_Tight = cms.vdouble(-0.42, -0.09, -0.14, -0.02)
)

process.full_106x_UL17_chs = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(-0.95, -0.72, -0.68, -0.47),
        Pt010_Medium = cms.vdouble(0.26, -0.33, -0.54, -0.37),
        Pt010_Tight = cms.vdouble(0.77, 0.38, -0.31, -0.21),
        Pt1020_Loose = cms.vdouble(-0.95, -0.72, -0.68, -0.47),
        Pt1020_Medium = cms.vdouble(0.26, -0.33, -0.54, -0.37),
        Pt1020_Tight = cms.vdouble(0.77, 0.38, -0.31, -0.21),
        Pt2030_Loose = cms.vdouble(-0.88, -0.55, -0.6, -0.43),
        Pt2030_Medium = cms.vdouble(0.68, -0.04, -0.43, -0.3),
        Pt2030_Tight = cms.vdouble(0.9, 0.6, -0.12, -0.13),
        Pt3040_Loose = cms.vdouble(-0.63, -0.18, -0.43, -0.24),
        Pt3040_Medium = cms.vdouble(0.9, 0.36, -0.16, -0.09),
        Pt3040_Tight = cms.vdouble(0.96, 0.82, 0.2, 0.09),
        Pt4050_Loose = cms.vdouble(-0.19, 0.22, -0.13, -0.03),
        Pt4050_Medium = cms.vdouble(0.96, 0.61, 0.14, 0.12),
        Pt4050_Tight = cms.vdouble(0.98, 0.92, 0.47, 0.29)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(True),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('full'),
    nEtaBins = cms.int32(4),
    tmvaMethod = cms.string('JetIDMVAHighPt'),
    tmvaSpectators = cms.vstring(
        'jetPt', 
        'jetEta'
    ),
    trainings = cms.VPSet(
        cms.PSet(
            jEtaMax = cms.double(2.5),
            jEtaMin = cms.double(0.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL17_Eta0p0To2p5_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(2.75),
            jEtaMin = cms.double(2.5),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL17_Eta2p5To2p75_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(3.0),
            jEtaMin = cms.double(2.75),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL17_Eta2p75To3p0_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(5.0),
            jEtaMin = cms.double(3.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'nParticles', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL17_Eta3p0To5p0_chs_BDT.weights.xml.gz')
        )
    ),
    version = cms.int32(-1)
)

process.full_106x_UL17_chs_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.95, -0.72, -0.68, -0.47),
    Pt010_Medium = cms.vdouble(0.26, -0.33, -0.54, -0.37),
    Pt010_Tight = cms.vdouble(0.77, 0.38, -0.31, -0.21),
    Pt1020_Loose = cms.vdouble(-0.95, -0.72, -0.68, -0.47),
    Pt1020_Medium = cms.vdouble(0.26, -0.33, -0.54, -0.37),
    Pt1020_Tight = cms.vdouble(0.77, 0.38, -0.31, -0.21),
    Pt2030_Loose = cms.vdouble(-0.88, -0.55, -0.6, -0.43),
    Pt2030_Medium = cms.vdouble(0.68, -0.04, -0.43, -0.3),
    Pt2030_Tight = cms.vdouble(0.9, 0.6, -0.12, -0.13),
    Pt3040_Loose = cms.vdouble(-0.63, -0.18, -0.43, -0.24),
    Pt3040_Medium = cms.vdouble(0.9, 0.36, -0.16, -0.09),
    Pt3040_Tight = cms.vdouble(0.96, 0.82, 0.2, 0.09),
    Pt4050_Loose = cms.vdouble(-0.19, 0.22, -0.13, -0.03),
    Pt4050_Medium = cms.vdouble(0.96, 0.61, 0.14, 0.12),
    Pt4050_Tight = cms.vdouble(0.98, 0.92, 0.47, 0.29)
)

process.full_106x_UL18_chs = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(-0.95, -0.72, -0.68, -0.47),
        Pt010_Medium = cms.vdouble(0.26, -0.33, -0.54, -0.37),
        Pt010_Tight = cms.vdouble(0.77, 0.38, -0.31, -0.21),
        Pt1020_Loose = cms.vdouble(-0.95, -0.72, -0.68, -0.47),
        Pt1020_Medium = cms.vdouble(0.26, -0.33, -0.54, -0.37),
        Pt1020_Tight = cms.vdouble(0.77, 0.38, -0.31, -0.21),
        Pt2030_Loose = cms.vdouble(-0.88, -0.55, -0.6, -0.43),
        Pt2030_Medium = cms.vdouble(0.68, -0.04, -0.43, -0.3),
        Pt2030_Tight = cms.vdouble(0.9, 0.6, -0.12, -0.13),
        Pt3040_Loose = cms.vdouble(-0.63, -0.18, -0.43, -0.24),
        Pt3040_Medium = cms.vdouble(0.9, 0.36, -0.16, -0.09),
        Pt3040_Tight = cms.vdouble(0.96, 0.82, 0.2, 0.09),
        Pt4050_Loose = cms.vdouble(-0.19, 0.22, -0.13, -0.03),
        Pt4050_Medium = cms.vdouble(0.96, 0.61, 0.14, 0.12),
        Pt4050_Tight = cms.vdouble(0.98, 0.92, 0.47, 0.29)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(True),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('full'),
    nEtaBins = cms.int32(4),
    tmvaMethod = cms.string('JetIDMVAHighPt'),
    tmvaSpectators = cms.vstring(
        'jetPt', 
        'jetEta'
    ),
    trainings = cms.VPSet(
        cms.PSet(
            jEtaMax = cms.double(2.5),
            jEtaMin = cms.double(0.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL18_Eta0p0To2p5_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(2.75),
            jEtaMin = cms.double(2.5),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL18_Eta2p5To2p75_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(3.0),
            jEtaMin = cms.double(2.75),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL18_Eta2p75To3p0_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(5.0),
            jEtaMin = cms.double(3.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'nParticles', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL18_Eta3p0To5p0_chs_BDT.weights.xml.gz')
        )
    ),
    version = cms.int32(-1)
)

process.full_106x_UL18_chs_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.95, -0.72, -0.68, -0.47),
    Pt010_Medium = cms.vdouble(0.26, -0.33, -0.54, -0.37),
    Pt010_Tight = cms.vdouble(0.77, 0.38, -0.31, -0.21),
    Pt1020_Loose = cms.vdouble(-0.95, -0.72, -0.68, -0.47),
    Pt1020_Medium = cms.vdouble(0.26, -0.33, -0.54, -0.37),
    Pt1020_Tight = cms.vdouble(0.77, 0.38, -0.31, -0.21),
    Pt2030_Loose = cms.vdouble(-0.88, -0.55, -0.6, -0.43),
    Pt2030_Medium = cms.vdouble(0.68, -0.04, -0.43, -0.3),
    Pt2030_Tight = cms.vdouble(0.9, 0.6, -0.12, -0.13),
    Pt3040_Loose = cms.vdouble(-0.63, -0.18, -0.43, -0.24),
    Pt3040_Medium = cms.vdouble(0.9, 0.36, -0.16, -0.09),
    Pt3040_Tight = cms.vdouble(0.96, 0.82, 0.2, 0.09),
    Pt4050_Loose = cms.vdouble(-0.19, 0.22, -0.13, -0.03),
    Pt4050_Medium = cms.vdouble(0.96, 0.61, 0.14, 0.12),
    Pt4050_Tight = cms.vdouble(0.98, 0.92, 0.47, 0.29)
)

process.full_53x = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(-0.95, -0.96, -0.94, -0.95),
        Pt010_MET = cms.vdouble(0.0, -0.6, -0.4, -0.4),
        Pt010_Medium = cms.vdouble(-0.83, -0.92, -0.9, -0.92),
        Pt010_Tight = cms.vdouble(-0.83, -0.81, -0.74, -0.81),
        Pt1020_Loose = cms.vdouble(-0.95, -0.96, -0.94, -0.95),
        Pt1020_MET = cms.vdouble(0.3, -0.2, -0.4, -0.4),
        Pt1020_Medium = cms.vdouble(-0.83, -0.92, -0.9, -0.92),
        Pt1020_Tight = cms.vdouble(-0.83, -0.81, -0.74, -0.81),
        Pt2030_Loose = cms.vdouble(-0.63, -0.6, -0.55, -0.45),
        Pt2030_MET = cms.vdouble(0.0, 0.0, 0.0, 0.0),
        Pt2030_Medium = cms.vdouble(0.1, -0.36, -0.54, -0.54),
        Pt2030_Tight = cms.vdouble(0.73, 0.05, -0.26, -0.42),
        Pt3040_Loose = cms.vdouble(-0.63, -0.6, -0.55, -0.45),
        Pt3040_MET = cms.vdouble(0.0, 0.0, -0.1, -0.2),
        Pt3040_Medium = cms.vdouble(0.1, -0.36, -0.54, -0.54),
        Pt3040_Tight = cms.vdouble(0.73, 0.05, -0.26, -0.42),
        Pt4050_Loose = cms.vdouble(-0.63, -0.6, -0.55, -0.45),
        Pt4050_MET = cms.vdouble(0.0, 0.0, -0.1, -0.2),
        Pt4050_Medium = cms.vdouble(0.1, -0.36, -0.54, -0.54),
        Pt4050_Tight = cms.vdouble(0.73, 0.05, -0.26, -0.42)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(False),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('full53x'),
    tmvaMethod = cms.string('JetIDMVAHighPt'),
    tmvaSpectators = cms.vstring(
        'jetPt', 
        'jetEta', 
        'jetPhi'
    ),
    tmvaVariables = cms.vstring(
        'nvtx', 
        'dZ', 
        'beta', 
        'betaStar', 
        'nCharged', 
        'nNeutrals', 
        'dR2Mean', 
        'ptD', 
        'frac01', 
        'frac02', 
        'frac03', 
        'frac04', 
        'frac05'
    ),
    tmvaWeights = cms.FileInPath('CondFormats/JetMETObjects/data/TMVAClassificationCategory_JetID_53X_Dec2012.weights.xml'),
    version = cms.int32(-1)
)

process.full_53x_chs = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(-0.95, -0.96, -0.94, -0.95),
        Pt010_Medium = cms.vdouble(-0.83, -0.92, -0.9, -0.92),
        Pt010_Tight = cms.vdouble(-0.83, -0.81, -0.74, -0.81),
        Pt1020_Loose = cms.vdouble(-0.95, -0.96, -0.94, -0.95),
        Pt1020_Medium = cms.vdouble(-0.83, -0.92, -0.9, -0.92),
        Pt1020_Tight = cms.vdouble(-0.83, -0.81, -0.74, -0.81),
        Pt2030_Loose = cms.vdouble(-0.15, -0.26, -0.16, -0.16),
        Pt2030_Medium = cms.vdouble(-0.07, -0.09, 0.0, -0.06),
        Pt2030_Tight = cms.vdouble(0.78, 0.5, 0.17, 0.17),
        Pt3040_Loose = cms.vdouble(-0.15, -0.26, -0.16, -0.16),
        Pt3040_Medium = cms.vdouble(-0.07, -0.09, 0.0, -0.06),
        Pt3040_Tight = cms.vdouble(0.78, 0.5, 0.17, 0.17),
        Pt4050_Loose = cms.vdouble(-0.15, -0.26, -0.16, -0.16),
        Pt4050_Medium = cms.vdouble(-0.07, -0.09, 0.0, -0.06),
        Pt4050_Tight = cms.vdouble(0.78, 0.5, 0.17, 0.17)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(False),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('full'),
    tmvaMethod = cms.string('JetIDMVAHighPt'),
    tmvaSpectators = cms.vstring(
        'jetPt', 
        'jetEta', 
        'jetPhi'
    ),
    tmvaVariables = cms.vstring(
        'nvtx', 
        'dZ', 
        'beta', 
        'betaStar', 
        'nCharged', 
        'nNeutrals', 
        'dR2Mean', 
        'ptD', 
        'frac01', 
        'frac02', 
        'frac03', 
        'frac04', 
        'frac05'
    ),
    tmvaWeights = cms.FileInPath('CondFormats/JetMETObjects/data/TMVAClassificationCategory_JetID_53X_chs_Dec2012.weights.xml'),
    version = cms.int32(-1)
)

process.full_53x_chs_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.95, -0.96, -0.94, -0.95),
    Pt010_Medium = cms.vdouble(-0.83, -0.92, -0.9, -0.92),
    Pt010_Tight = cms.vdouble(-0.83, -0.81, -0.74, -0.81),
    Pt1020_Loose = cms.vdouble(-0.95, -0.96, -0.94, -0.95),
    Pt1020_Medium = cms.vdouble(-0.83, -0.92, -0.9, -0.92),
    Pt1020_Tight = cms.vdouble(-0.83, -0.81, -0.74, -0.81),
    Pt2030_Loose = cms.vdouble(-0.15, -0.26, -0.16, -0.16),
    Pt2030_Medium = cms.vdouble(-0.07, -0.09, 0.0, -0.06),
    Pt2030_Tight = cms.vdouble(0.78, 0.5, 0.17, 0.17),
    Pt3040_Loose = cms.vdouble(-0.15, -0.26, -0.16, -0.16),
    Pt3040_Medium = cms.vdouble(-0.07, -0.09, 0.0, -0.06),
    Pt3040_Tight = cms.vdouble(0.78, 0.5, 0.17, 0.17),
    Pt4050_Loose = cms.vdouble(-0.15, -0.26, -0.16, -0.16),
    Pt4050_Medium = cms.vdouble(-0.07, -0.09, 0.0, -0.06),
    Pt4050_Tight = cms.vdouble(0.78, 0.5, 0.17, 0.17)
)

process.full_53x_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.95, -0.96, -0.94, -0.95),
    Pt010_MET = cms.vdouble(0.0, -0.6, -0.4, -0.4),
    Pt010_Medium = cms.vdouble(-0.83, -0.92, -0.9, -0.92),
    Pt010_Tight = cms.vdouble(-0.83, -0.81, -0.74, -0.81),
    Pt1020_Loose = cms.vdouble(-0.95, -0.96, -0.94, -0.95),
    Pt1020_MET = cms.vdouble(0.3, -0.2, -0.4, -0.4),
    Pt1020_Medium = cms.vdouble(-0.83, -0.92, -0.9, -0.92),
    Pt1020_Tight = cms.vdouble(-0.83, -0.81, -0.74, -0.81),
    Pt2030_Loose = cms.vdouble(-0.63, -0.6, -0.55, -0.45),
    Pt2030_MET = cms.vdouble(0.0, 0.0, 0.0, 0.0),
    Pt2030_Medium = cms.vdouble(0.1, -0.36, -0.54, -0.54),
    Pt2030_Tight = cms.vdouble(0.73, 0.05, -0.26, -0.42),
    Pt3040_Loose = cms.vdouble(-0.63, -0.6, -0.55, -0.45),
    Pt3040_MET = cms.vdouble(0.0, 0.0, -0.1, -0.2),
    Pt3040_Medium = cms.vdouble(0.1, -0.36, -0.54, -0.54),
    Pt3040_Tight = cms.vdouble(0.73, 0.05, -0.26, -0.42),
    Pt4050_Loose = cms.vdouble(-0.63, -0.6, -0.55, -0.45),
    Pt4050_MET = cms.vdouble(0.0, 0.0, -0.1, -0.2),
    Pt4050_Medium = cms.vdouble(0.1, -0.36, -0.54, -0.54),
    Pt4050_Tight = cms.vdouble(0.73, 0.05, -0.26, -0.42)
)

process.full_5x = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(-0.95, -0.97, -0.97, -0.97),
        Pt010_Medium = cms.vdouble(-0.83, -0.96, -0.95, -0.96),
        Pt010_Tight = cms.vdouble(-0.47, -0.92, -0.92, -0.94),
        Pt1020_Loose = cms.vdouble(-0.95, -0.97, -0.97, -0.97),
        Pt1020_Medium = cms.vdouble(-0.83, -0.96, -0.95, -0.96),
        Pt1020_Tight = cms.vdouble(-0.47, -0.92, -0.92, -0.94),
        Pt2030_Loose = cms.vdouble(-0.8, -0.85, -0.84, -0.85),
        Pt2030_Medium = cms.vdouble(-0.4, -0.74, -0.76, -0.81),
        Pt2030_Tight = cms.vdouble(0.32, -0.49, -0.61, -0.74),
        Pt3040_Loose = cms.vdouble(-0.8, -0.85, -0.84, -0.85),
        Pt3040_Medium = cms.vdouble(-0.4, -0.74, -0.76, -0.81),
        Pt3040_Tight = cms.vdouble(0.32, -0.49, -0.61, -0.74),
        Pt4050_Loose = cms.vdouble(-0.8, -0.85, -0.84, -0.85),
        Pt4050_Medium = cms.vdouble(-0.4, -0.74, -0.76, -0.81),
        Pt4050_Tight = cms.vdouble(0.32, -0.49, -0.61, -0.74)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(False),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('full'),
    tmvaMethod = cms.string('BDT_fullPlusRMS'),
    tmvaSpectators = cms.vstring(
        'jetPt', 
        'jetEta'
    ),
    tmvaVariables = cms.vstring(
        'frac01', 
        'frac02', 
        'frac03', 
        'frac04', 
        'frac05', 
        'dR2Mean', 
        'nvtx', 
        'nNeutrals', 
        'beta', 
        'betaStar', 
        'dZ', 
        'nCharged'
    ),
    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/TMVAClassificationCategory_JetID_MET_53X_Dec2012.weights.xml.gz'),
    version = cms.int32(-1)
)

process.full_5x_chs = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(-0.98, -0.95, -0.94, -0.94),
        Pt010_Medium = cms.vdouble(-0.94, -0.91, -0.91, -0.92),
        Pt010_Tight = cms.vdouble(-0.59, -0.75, -0.78, -0.8),
        Pt1020_Loose = cms.vdouble(-0.98, -0.95, -0.94, -0.94),
        Pt1020_Medium = cms.vdouble(-0.94, -0.91, -0.91, -0.92),
        Pt1020_Tight = cms.vdouble(-0.59, -0.75, -0.78, -0.8),
        Pt2030_Loose = cms.vdouble(-0.89, -0.77, -0.69, -0.75),
        Pt2030_Medium = cms.vdouble(-0.58, -0.65, -0.57, -0.67),
        Pt2030_Tight = cms.vdouble(0.41, -0.1, -0.2, -0.45),
        Pt3040_Loose = cms.vdouble(-0.89, -0.77, -0.69, -0.57),
        Pt3040_Medium = cms.vdouble(-0.58, -0.65, -0.57, -0.67),
        Pt3040_Tight = cms.vdouble(0.41, -0.1, -0.2, -0.45),
        Pt4050_Loose = cms.vdouble(-0.89, -0.77, -0.69, -0.57),
        Pt4050_Medium = cms.vdouble(-0.58, -0.65, -0.57, -0.67),
        Pt4050_Tight = cms.vdouble(0.41, -0.1, -0.2, -0.45)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(False),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('full'),
    tmvaMethod = cms.string('BDT_chsFullPlusRMS'),
    tmvaSpectators = cms.vstring(
        'jetPt', 
        'jetEta'
    ),
    tmvaVariables = cms.vstring(
        'frac01', 
        'frac02', 
        'frac03', 
        'frac04', 
        'frac05', 
        'dR2Mean', 
        'nvtx', 
        'nNeutrals', 
        'beta', 
        'betaStar', 
        'dZ', 
        'nCharged'
    ),
    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/TMVAClassification_5x_BDT_chsFullPlusRMS.weights.xml.gz'),
    version = cms.int32(-1)
)

process.full_5x_chs_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.98, -0.95, -0.94, -0.94),
    Pt010_Medium = cms.vdouble(-0.94, -0.91, -0.91, -0.92),
    Pt010_Tight = cms.vdouble(-0.59, -0.75, -0.78, -0.8),
    Pt1020_Loose = cms.vdouble(-0.98, -0.95, -0.94, -0.94),
    Pt1020_Medium = cms.vdouble(-0.94, -0.91, -0.91, -0.92),
    Pt1020_Tight = cms.vdouble(-0.59, -0.75, -0.78, -0.8),
    Pt2030_Loose = cms.vdouble(-0.89, -0.77, -0.69, -0.75),
    Pt2030_Medium = cms.vdouble(-0.58, -0.65, -0.57, -0.67),
    Pt2030_Tight = cms.vdouble(0.41, -0.1, -0.2, -0.45),
    Pt3040_Loose = cms.vdouble(-0.89, -0.77, -0.69, -0.57),
    Pt3040_Medium = cms.vdouble(-0.58, -0.65, -0.57, -0.67),
    Pt3040_Tight = cms.vdouble(0.41, -0.1, -0.2, -0.45),
    Pt4050_Loose = cms.vdouble(-0.89, -0.77, -0.69, -0.57),
    Pt4050_Medium = cms.vdouble(-0.58, -0.65, -0.57, -0.67),
    Pt4050_Tight = cms.vdouble(0.41, -0.1, -0.2, -0.45)
)

process.full_5x_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.95, -0.97, -0.97, -0.97),
    Pt010_Medium = cms.vdouble(-0.83, -0.96, -0.95, -0.96),
    Pt010_Tight = cms.vdouble(-0.47, -0.92, -0.92, -0.94),
    Pt1020_Loose = cms.vdouble(-0.95, -0.97, -0.97, -0.97),
    Pt1020_Medium = cms.vdouble(-0.83, -0.96, -0.95, -0.96),
    Pt1020_Tight = cms.vdouble(-0.47, -0.92, -0.92, -0.94),
    Pt2030_Loose = cms.vdouble(-0.8, -0.85, -0.84, -0.85),
    Pt2030_Medium = cms.vdouble(-0.4, -0.74, -0.76, -0.81),
    Pt2030_Tight = cms.vdouble(0.32, -0.49, -0.61, -0.74),
    Pt3040_Loose = cms.vdouble(-0.8, -0.85, -0.84, -0.85),
    Pt3040_Medium = cms.vdouble(-0.4, -0.74, -0.76, -0.81),
    Pt3040_Tight = cms.vdouble(0.32, -0.49, -0.61, -0.74),
    Pt4050_Loose = cms.vdouble(-0.8, -0.85, -0.84, -0.85),
    Pt4050_Medium = cms.vdouble(-0.4, -0.74, -0.76, -0.81),
    Pt4050_Tight = cms.vdouble(0.32, -0.49, -0.61, -0.74)
)

process.full_74x_chs = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(-0.8, -0.97, -0.97, -0.99),
        Pt010_Medium = cms.vdouble(-0.3, -0.87, -0.87, -0.99),
        Pt010_Tight = cms.vdouble(-0.1, -0.83, -0.83, -0.98),
        Pt1020_Loose = cms.vdouble(-0.8, -0.97, -0.97, -0.99),
        Pt1020_Medium = cms.vdouble(-0.3, -0.87, -0.87, -0.99),
        Pt1020_Tight = cms.vdouble(-0.1, -0.83, -0.83, -0.98),
        Pt2030_Loose = cms.vdouble(-0.8, -0.97, -0.97, -0.99),
        Pt2030_Medium = cms.vdouble(-0.3, -0.87, -0.87, -0.99),
        Pt2030_Tight = cms.vdouble(-0.1, -0.83, -0.83, -0.98),
        Pt3040_Loose = cms.vdouble(-0.8, -0.95, -0.97, -0.99),
        Pt3040_Medium = cms.vdouble(-0.6, -0.85, -0.85, -0.99),
        Pt3040_Tight = cms.vdouble(-0.5, -0.77, -0.8, -0.98),
        Pt4050_Loose = cms.vdouble(-0.8, -0.95, -0.97, -0.99),
        Pt4050_Medium = cms.vdouble(-0.6, -0.85, -0.85, -0.99),
        Pt4050_Tight = cms.vdouble(-0.5, -0.77, -0.8, -0.98)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(True),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('full'),
    nEtaBins = cms.int32(4),
    tmvaSpectators = cms.vstring(
        'jetPt', 
        'jetEta', 
        'nTrueInt', 
        'dRMatch'
    ),
    trainings = cms.VPSet(
        cms.PSet(
            jEtaMax = cms.double(2.0),
            jEtaMin = cms.double(0.0),
            tmvaVariables = cms.vstring(
                'dR2Mean', 
                'rho', 
                'nParticles', 
                'nCharged', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'beta', 
                'betaStar', 
                'pull', 
                'jetR', 
                'jetRchg'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/TMVAClassificationCategory_BDTG.weights_jteta_0_2_newNames.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(2.5),
            jEtaMin = cms.double(2.0),
            tmvaVariables = cms.vstring(
                'dR2Mean', 
                'rho', 
                'nParticles', 
                'nCharged', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'beta', 
                'betaStar', 
                'pull', 
                'jetR', 
                'jetRchg'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/TMVAClassificationCategory_BDTG.weights_jteta_2_2p5_newNames.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(3.0),
            jEtaMin = cms.double(2.5),
            tmvaVariables = cms.vstring(
                'dR2Mean', 
                'rho', 
                'nParticles', 
                'nCharged', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'beta', 
                'betaStar', 
                'pull', 
                'jetR', 
                'jetRchg'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/TMVAClassificationCategory_BDTG.weights_jteta_2p5_3_newNames.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(5.0),
            jEtaMin = cms.double(3.0),
            tmvaVariables = cms.vstring(
                'dR2Mean', 
                'rho', 
                'nParticles', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'pull', 
                'jetR'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/TMVAClassificationCategory_BDTG.weights_jteta_3_5_newNames.xml.gz')
        )
    ),
    version = cms.int32(-1)
)

process.full_74x_chs_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.8, -0.97, -0.97, -0.99),
    Pt010_Medium = cms.vdouble(-0.3, -0.87, -0.87, -0.99),
    Pt010_Tight = cms.vdouble(-0.1, -0.83, -0.83, -0.98),
    Pt1020_Loose = cms.vdouble(-0.8, -0.97, -0.97, -0.99),
    Pt1020_Medium = cms.vdouble(-0.3, -0.87, -0.87, -0.99),
    Pt1020_Tight = cms.vdouble(-0.1, -0.83, -0.83, -0.98),
    Pt2030_Loose = cms.vdouble(-0.8, -0.97, -0.97, -0.99),
    Pt2030_Medium = cms.vdouble(-0.3, -0.87, -0.87, -0.99),
    Pt2030_Tight = cms.vdouble(-0.1, -0.83, -0.83, -0.98),
    Pt3040_Loose = cms.vdouble(-0.8, -0.95, -0.97, -0.99),
    Pt3040_Medium = cms.vdouble(-0.6, -0.85, -0.85, -0.99),
    Pt3040_Tight = cms.vdouble(-0.5, -0.77, -0.8, -0.98),
    Pt4050_Loose = cms.vdouble(-0.8, -0.95, -0.97, -0.99),
    Pt4050_Medium = cms.vdouble(-0.6, -0.85, -0.85, -0.99),
    Pt4050_Tight = cms.vdouble(-0.5, -0.77, -0.8, -0.98)
)

process.full_76x_chs = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(-0.96, -0.62, -0.53, -0.49),
        Pt010_Medium = cms.vdouble(-0.58, -0.52, -0.4, -0.36),
        Pt010_Tight = cms.vdouble(0.09, -0.37, -0.24, -0.21),
        Pt1020_Loose = cms.vdouble(-0.96, -0.62, -0.53, -0.49),
        Pt1020_Medium = cms.vdouble(-0.58, -0.52, -0.4, -0.36),
        Pt1020_Tight = cms.vdouble(0.09, -0.37, -0.24, -0.21),
        Pt2030_Loose = cms.vdouble(-0.96, -0.62, -0.53, -0.49),
        Pt2030_Medium = cms.vdouble(-0.58, -0.52, -0.4, -0.36),
        Pt2030_Tight = cms.vdouble(0.09, -0.37, -0.24, -0.21),
        Pt3040_Loose = cms.vdouble(-0.93, -0.52, -0.39, -0.31),
        Pt3040_Medium = cms.vdouble(-0.2, -0.39, -0.24, -0.19),
        Pt3040_Tight = cms.vdouble(0.52, -0.19, -0.06, -0.03),
        Pt4050_Loose = cms.vdouble(-0.93, -0.52, -0.39, -0.31),
        Pt4050_Medium = cms.vdouble(-0.2, -0.39, -0.24, -0.19),
        Pt4050_Tight = cms.vdouble(0.52, -0.19, -0.06, -0.03)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(True),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('full'),
    nEtaBins = cms.int32(4),
    tmvaMethod = cms.string('JetIDMVAHighPt'),
    tmvaSpectators = cms.vstring(
        'jetPt', 
        'jetEta'
    ),
    trainings = cms.VPSet(
        cms.PSet(
            jEtaMax = cms.double(2.5),
            jEtaMin = cms.double(0.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'nParticles', 
                'nCharged', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'beta', 
                'pull', 
                'jetR', 
                'jetRchg'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_76x_Eta0to2p5_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(2.75),
            jEtaMin = cms.double(2.5),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'nParticles', 
                'nCharged', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'beta', 
                'pull', 
                'jetR', 
                'jetRchg'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_76x_Eta2p5to2p75_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(3.0),
            jEtaMin = cms.double(2.75),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'nParticles', 
                'nCharged', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'beta', 
                'pull', 
                'jetR', 
                'jetRchg'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_76x_Eta2p75to3_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(5.0),
            jEtaMin = cms.double(3.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'nParticles', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'pull', 
                'jetR'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_76x_Eta3to5_BDT.weights.xml.gz')
        )
    ),
    version = cms.int32(-1)
)

process.full_76x_chs_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.96, -0.62, -0.53, -0.49),
    Pt010_Medium = cms.vdouble(-0.58, -0.52, -0.4, -0.36),
    Pt010_Tight = cms.vdouble(0.09, -0.37, -0.24, -0.21),
    Pt1020_Loose = cms.vdouble(-0.96, -0.62, -0.53, -0.49),
    Pt1020_Medium = cms.vdouble(-0.58, -0.52, -0.4, -0.36),
    Pt1020_Tight = cms.vdouble(0.09, -0.37, -0.24, -0.21),
    Pt2030_Loose = cms.vdouble(-0.96, -0.62, -0.53, -0.49),
    Pt2030_Medium = cms.vdouble(-0.58, -0.52, -0.4, -0.36),
    Pt2030_Tight = cms.vdouble(0.09, -0.37, -0.24, -0.21),
    Pt3040_Loose = cms.vdouble(-0.93, -0.52, -0.39, -0.31),
    Pt3040_Medium = cms.vdouble(-0.2, -0.39, -0.24, -0.19),
    Pt3040_Tight = cms.vdouble(0.52, -0.19, -0.06, -0.03),
    Pt4050_Loose = cms.vdouble(-0.93, -0.52, -0.39, -0.31),
    Pt4050_Medium = cms.vdouble(-0.2, -0.39, -0.24, -0.19),
    Pt4050_Tight = cms.vdouble(0.52, -0.19, -0.06, -0.03)
)

process.full_80x_chs = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(-0.96, -0.64, -0.56, -0.54),
        Pt010_Medium = cms.vdouble(-0.49, -0.53, -0.44, -0.42),
        Pt010_Tight = cms.vdouble(0.26, -0.34, -0.24, -0.26),
        Pt1020_Loose = cms.vdouble(-0.96, -0.64, -0.56, -0.54),
        Pt1020_Medium = cms.vdouble(-0.49, -0.53, -0.44, -0.42),
        Pt1020_Tight = cms.vdouble(0.26, -0.34, -0.24, -0.26),
        Pt2030_Loose = cms.vdouble(-0.96, -0.64, -0.56, -0.54),
        Pt2030_Medium = cms.vdouble(-0.49, -0.53, -0.44, -0.42),
        Pt2030_Tight = cms.vdouble(0.26, -0.34, -0.24, -0.26),
        Pt3040_Loose = cms.vdouble(-0.92, -0.56, -0.44, -0.39),
        Pt3040_Medium = cms.vdouble(-0.06, -0.42, -0.3, -0.23),
        Pt3040_Tight = cms.vdouble(0.62, -0.21, -0.07, -0.03),
        Pt4050_Loose = cms.vdouble(-0.92, -0.56, -0.44, -0.39),
        Pt4050_Medium = cms.vdouble(-0.06, -0.42, -0.3, -0.23),
        Pt4050_Tight = cms.vdouble(0.62, -0.21, -0.07, -0.03)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(True),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('full'),
    nEtaBins = cms.int32(4),
    tmvaMethod = cms.string('JetIDMVAHighPt'),
    tmvaSpectators = cms.vstring(
        'jetPt', 
        'jetEta'
    ),
    trainings = cms.VPSet(
        cms.PSet(
            jEtaMax = cms.double(2.5),
            jEtaMin = cms.double(0.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'nParticles', 
                'nCharged', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'beta', 
                'pull', 
                'jetR', 
                'jetRchg'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80X_Eta0to2p5_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(2.75),
            jEtaMin = cms.double(2.5),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'nParticles', 
                'nCharged', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'beta', 
                'pull', 
                'jetR', 
                'jetRchg'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80X_Eta2p5to2p75_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(3.0),
            jEtaMin = cms.double(2.75),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'nParticles', 
                'nCharged', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'beta', 
                'pull', 
                'jetR', 
                'jetRchg'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80X_Eta2p75to3_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(5.0),
            jEtaMin = cms.double(3.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'nParticles', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'pull', 
                'jetR'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80X_Eta3to5_BDT.weights.xml.gz')
        )
    ),
    version = cms.int32(-1)
)

process.full_80x_chs_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.96, -0.64, -0.56, -0.54),
    Pt010_Medium = cms.vdouble(-0.49, -0.53, -0.44, -0.42),
    Pt010_Tight = cms.vdouble(0.26, -0.34, -0.24, -0.26),
    Pt1020_Loose = cms.vdouble(-0.96, -0.64, -0.56, -0.54),
    Pt1020_Medium = cms.vdouble(-0.49, -0.53, -0.44, -0.42),
    Pt1020_Tight = cms.vdouble(0.26, -0.34, -0.24, -0.26),
    Pt2030_Loose = cms.vdouble(-0.96, -0.64, -0.56, -0.54),
    Pt2030_Medium = cms.vdouble(-0.49, -0.53, -0.44, -0.42),
    Pt2030_Tight = cms.vdouble(0.26, -0.34, -0.24, -0.26),
    Pt3040_Loose = cms.vdouble(-0.92, -0.56, -0.44, -0.39),
    Pt3040_Medium = cms.vdouble(-0.06, -0.42, -0.3, -0.23),
    Pt3040_Tight = cms.vdouble(0.62, -0.21, -0.07, -0.03),
    Pt4050_Loose = cms.vdouble(-0.92, -0.56, -0.44, -0.39),
    Pt4050_Medium = cms.vdouble(-0.06, -0.42, -0.3, -0.23),
    Pt4050_Tight = cms.vdouble(0.62, -0.21, -0.07, -0.03)
)

process.full_81x_chs = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
        Pt010_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
        Pt010_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
        Pt1020_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
        Pt1020_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
        Pt1020_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
        Pt2030_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
        Pt2030_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
        Pt2030_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
        Pt3040_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
        Pt3040_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
        Pt3040_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01),
        Pt4050_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
        Pt4050_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
        Pt4050_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(True),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('full'),
    nEtaBins = cms.int32(4),
    tmvaMethod = cms.string('JetIDMVAHighPt'),
    tmvaSpectators = cms.vstring(
        'jetPt', 
        'jetEta'
    ),
    trainings = cms.VPSet(
        cms.PSet(
            jEtaMax = cms.double(2.5),
            jEtaMin = cms.double(0.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'nParticles', 
                'nCharged', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'beta', 
                'pull', 
                'jetR', 
                'jetRchg'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80XvarFix_Eta0to2p5_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(2.75),
            jEtaMin = cms.double(2.5),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'nParticles', 
                'nCharged', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'beta', 
                'pull', 
                'jetR', 
                'jetRchg'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80XvarFix_Eta2p5to2p75_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(3.0),
            jEtaMin = cms.double(2.75),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'nParticles', 
                'nCharged', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'beta', 
                'pull', 
                'jetR', 
                'jetRchg'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80XvarFix_Eta2p75to3_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(5.0),
            jEtaMin = cms.double(3.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'nParticles', 
                'majW', 
                'minW', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'ptD', 
                'pull', 
                'jetR'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80XvarFix_Eta3to5_BDT.weights.xml.gz')
        )
    ),
    version = cms.int32(-1)
)

process.full_81x_chs_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
    Pt010_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
    Pt010_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
    Pt1020_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
    Pt1020_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
    Pt1020_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
    Pt2030_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
    Pt2030_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
    Pt2030_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
    Pt3040_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
    Pt3040_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
    Pt3040_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01),
    Pt4050_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
    Pt4050_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
    Pt4050_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01)
)

process.full_94x_chs = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
        Pt010_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
        Pt010_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
        Pt1020_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
        Pt1020_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
        Pt1020_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
        Pt2030_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
        Pt2030_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
        Pt2030_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
        Pt3040_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
        Pt3040_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
        Pt3040_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01),
        Pt4050_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
        Pt4050_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
        Pt4050_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(True),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('full'),
    nEtaBins = cms.int32(4),
    tmvaMethod = cms.string('JetIDMVAHighPt'),
    tmvaSpectators = cms.vstring(
        'jetPt', 
        'jetEta'
    ),
    trainings = cms.VPSet(
        cms.PSet(
            jEtaMax = cms.double(2.5),
            jEtaMin = cms.double(0.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_94X_Eta0p0To2p5_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(2.75),
            jEtaMin = cms.double(2.5),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_94X_Eta2p5To2p75_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(3.0),
            jEtaMin = cms.double(2.75),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'beta', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'jetRchg', 
                'nParticles', 
                'nCharged', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_94X_Eta2p75To3p0_chs_BDT.weights.xml.gz')
        ), 
        cms.PSet(
            jEtaMax = cms.double(5.0),
            jEtaMin = cms.double(3.0),
            tmvaVariables = cms.vstring(
                'nvtx', 
                'dR2Mean', 
                'frac01', 
                'frac02', 
                'frac03', 
                'frac04', 
                'majW', 
                'minW', 
                'jetR', 
                'nParticles', 
                'ptD', 
                'pull'
            ),
            tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_94X_Eta3p0To5p0_chs_BDT.weights.xml.gz')
        )
    ),
    version = cms.int32(-1)
)

process.full_94x_chs_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
    Pt010_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
    Pt010_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
    Pt1020_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
    Pt1020_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
    Pt1020_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
    Pt2030_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
    Pt2030_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
    Pt2030_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
    Pt3040_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
    Pt3040_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
    Pt3040_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01),
    Pt4050_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
    Pt4050_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
    Pt4050_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01)
)

process.met_53x = cms.PSet(
    JetIdParams = cms.PSet(
        Pt010_Loose = cms.vdouble(-2, -2, -2, -2, -2),
        Pt010_MET = cms.vdouble(-0.2, -0.3, -0.5, -0.5),
        Pt010_Medium = cms.vdouble(-2, -2, -2, -2, -2),
        Pt010_Tight = cms.vdouble(-2, -2, -2, -2, -2),
        Pt1020_Loose = cms.vdouble(-2, -2, -2, -2, -2),
        Pt1020_MET = cms.vdouble(-0.2, -0.2, -0.5, -0.3),
        Pt1020_Medium = cms.vdouble(-2, -2, -2, -2, -2),
        Pt1020_Tight = cms.vdouble(-2, -2, -2, -2, -2),
        Pt2030_Loose = cms.vdouble(-2, -2, -2, -2, -2),
        Pt2030_MET = cms.vdouble(-0.2, -0.2, -0.2, 0.1),
        Pt2030_Medium = cms.vdouble(-2, -2, -2, -2, -2),
        Pt2030_Tight = cms.vdouble(-2, -2, -2, -2, -2),
        Pt3040_Loose = cms.vdouble(-2, -2, -2, -2, -2),
        Pt3040_MET = cms.vdouble(-0.2, -0.2, 0.0, 0.2),
        Pt3040_Medium = cms.vdouble(-2, -2, -2, -2, -2),
        Pt3040_Tight = cms.vdouble(-2, -2, -2, -2, -2),
        Pt4050_Loose = cms.vdouble(-2, -2, -2, -2, -2),
        Pt4050_MET = cms.vdouble(-0.2, -0.2, 0.0, 0.2),
        Pt4050_Medium = cms.vdouble(-2, -2, -2, -2, -2),
        Pt4050_Tight = cms.vdouble(-2, -2, -2, -2, -2)
    ),
    cutBased = cms.bool(False),
    etaBinnedWeights = cms.bool(False),
    impactParTkThreshold = cms.double(1.0),
    label = cms.string('met53x'),
    tmvaMethod = cms.string('JetIDMVAMET'),
    tmvaSpectators = cms.vstring(),
    tmvaVariables = cms.vstring(
        'nvtx', 
        'jetPt', 
        'jetEta', 
        'jetPhi', 
        'dZ', 
        'beta', 
        'betaStar', 
        'nCharged', 
        'nNeutrals', 
        'dR2Mean', 
        'ptD', 
        'frac01', 
        'frac02', 
        'frac03', 
        'frac04', 
        'frac05'
    ),
    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/TMVAClassificationCategory_JetID_MET_53X_Dec2012.weights.xml.gz'),
    version = cms.int32(-1)
)

process.met_53x_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-2, -2, -2, -2, -2),
    Pt010_MET = cms.vdouble(-0.2, -0.3, -0.5, -0.5),
    Pt010_Medium = cms.vdouble(-2, -2, -2, -2, -2),
    Pt010_Tight = cms.vdouble(-2, -2, -2, -2, -2),
    Pt1020_Loose = cms.vdouble(-2, -2, -2, -2, -2),
    Pt1020_MET = cms.vdouble(-0.2, -0.2, -0.5, -0.3),
    Pt1020_Medium = cms.vdouble(-2, -2, -2, -2, -2),
    Pt1020_Tight = cms.vdouble(-2, -2, -2, -2, -2),
    Pt2030_Loose = cms.vdouble(-2, -2, -2, -2, -2),
    Pt2030_MET = cms.vdouble(-0.2, -0.2, -0.2, 0.1),
    Pt2030_Medium = cms.vdouble(-2, -2, -2, -2, -2),
    Pt2030_Tight = cms.vdouble(-2, -2, -2, -2, -2),
    Pt3040_Loose = cms.vdouble(-2, -2, -2, -2, -2),
    Pt3040_MET = cms.vdouble(-0.2, -0.2, 0.0, 0.2),
    Pt3040_Medium = cms.vdouble(-2, -2, -2, -2, -2),
    Pt3040_Tight = cms.vdouble(-2, -2, -2, -2, -2),
    Pt4050_Loose = cms.vdouble(-2, -2, -2, -2, -2),
    Pt4050_MET = cms.vdouble(-0.2, -0.2, 0.0, 0.2),
    Pt4050_Medium = cms.vdouble(-2, -2, -2, -2, -2),
    Pt4050_Tight = cms.vdouble(-2, -2, -2, -2, -2)
)

process.metfull_53x_wp = cms.PSet(
    Pt010_MET = cms.vdouble(-0.2, -0.3, -0.5, -0.5),
    Pt1020_MET = cms.vdouble(-0.2, -0.2, -0.5, -0.3),
    Pt2030_MET = cms.vdouble(0.0, 0.0, 0.0, 0.0),
    Pt3040_MET = cms.vdouble(0.0, 0.0, -0.1, -0.2),
    Pt4050_MET = cms.vdouble(0.0, 0.0, -0.1, -0.2)
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.simple_5x_chs_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.98, -0.96, -0.94, -0.94),
    Pt010_Medium = cms.vdouble(-0.95, -0.94, -0.92, -0.91),
    Pt010_Tight = cms.vdouble(-0.6, -0.74, -0.78, -0.81),
    Pt1020_Loose = cms.vdouble(-0.98, -0.96, -0.94, -0.94),
    Pt1020_Medium = cms.vdouble(-0.95, -0.94, -0.92, -0.91),
    Pt1020_Tight = cms.vdouble(-0.6, -0.74, -0.78, -0.81),
    Pt2030_Loose = cms.vdouble(-0.89, -0.75, -0.72, -0.75),
    Pt2030_Medium = cms.vdouble(-0.59, -0.65, -0.56, -0.68),
    Pt2030_Tight = cms.vdouble(-0.47, -0.06, -0.23, -0.47),
    Pt3040_Loose = cms.vdouble(-0.89, -0.75, -0.72, -0.75),
    Pt3040_Medium = cms.vdouble(-0.59, -0.65, -0.56, -0.68),
    Pt3040_Tight = cms.vdouble(-0.47, -0.06, -0.23, -0.47),
    Pt4050_Loose = cms.vdouble(-0.89, -0.75, -0.72, -0.75),
    Pt4050_Medium = cms.vdouble(-0.59, -0.65, -0.56, -0.68),
    Pt4050_Tight = cms.vdouble(-0.47, -0.06, -0.23, -0.47)
)

process.simple_5x_wp = cms.PSet(
    Pt010_Loose = cms.vdouble(-0.95, -0.97, -0.96, -0.97),
    Pt010_Medium = cms.vdouble(-0.85, -0.96, -0.95, -0.96),
    Pt010_Tight = cms.vdouble(-0.54, -0.93, -0.93, -0.94),
    Pt1020_Loose = cms.vdouble(-0.95, -0.97, -0.96, -0.97),
    Pt1020_Medium = cms.vdouble(-0.85, -0.96, -0.95, -0.96),
    Pt1020_Tight = cms.vdouble(-0.54, -0.93, -0.93, -0.94),
    Pt2030_Loose = cms.vdouble(-0.8, -0.86, -0.8, -0.84),
    Pt2030_Medium = cms.vdouble(-0.4, -0.73, -0.74, -0.8),
    Pt2030_Tight = cms.vdouble(0.26, -0.54, -0.63, -0.74),
    Pt3040_Loose = cms.vdouble(-0.8, -0.86, -0.8, -0.84),
    Pt3040_Medium = cms.vdouble(-0.4, -0.73, -0.74, -0.8),
    Pt3040_Tight = cms.vdouble(0.26, -0.54, -0.63, -0.74),
    Pt4050_Loose = cms.vdouble(-0.8, -0.86, -0.8, -0.84),
    Pt4050_Medium = cms.vdouble(-0.4, -0.73, -0.74, -0.8),
    Pt4050_Tight = cms.vdouble(0.26, -0.54, -0.63, -0.74)
)

process.train = cms.PSet(
    jEtaMax = cms.double(5.0),
    jEtaMin = cms.double(3.0),
    tmvaVariables = cms.vstring(
        'nvtx', 
        'dR2Mean', 
        'frac01', 
        'frac02', 
        'frac03', 
        'frac04', 
        'majW', 
        'minW', 
        'jetR', 
        'nParticles', 
        'ptD', 
        'pull'
    ),
    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL16APV_Eta3p0To5p0_chs_BDT.weights.xml.gz')
)

process.ak10PFCHSL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak10PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak10PFCHSL1FastjetCorrector", "ak10PFCHSL2RelativeCorrector", "ak10PFCHSL3AbsoluteCorrector", "ak10PFCHSResidualCorrector")
)


process.ak10PFCHSL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak10PFCHSL1OffsetCorrector", "ak10PFCHSL2RelativeCorrector", "ak10PFCHSL3AbsoluteCorrector", "ak10PFCHSResidualCorrector")
)


process.ak10PFCHSL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak10PFCHSL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak10PFCHSL2RelativeCorrector", "ak10PFCHSL3AbsoluteCorrector")
)


process.ak10PFCHSL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak10PFCHSL2RelativeCorrector", "ak10PFCHSL3AbsoluteCorrector", "ak10PFCHSResidualCorrector")
)


process.ak10PFCHSL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK10PFchs'),
    level = cms.string('L2Relative')
)


process.ak10PFCHSL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK10PFchs'),
    level = cms.string('L3Absolute')
)


process.ak10PFCHSResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak10PFJetsL1FastL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak10PFL1FastL2L3Corrector"),
    src = cms.InputTag("ak10PFJets")
)


process.ak10PFJetsL1FastL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak10PFL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("ak10PFJets")
)


process.ak10PFJetsL1L2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak10PFL1L2L3Corrector"),
    src = cms.InputTag("ak10PFJets")
)


process.ak10PFJetsL1L2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak10PFL1L2L3ResidualCorrector"),
    src = cms.InputTag("ak10PFJets")
)


process.ak10PFJetsL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak10PFL2L3Corrector"),
    src = cms.InputTag("ak10PFJets")
)


process.ak10PFJetsL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak10PFL2L3ResidualCorrector"),
    src = cms.InputTag("ak10PFJets")
)


process.ak10PFL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak10PFL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak10PFL1FastjetCorrector", "ak10PFL2RelativeCorrector", "ak10PFL3AbsoluteCorrector", "ak10PFResidualCorrector")
)


process.ak10PFL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak10PFL1OffsetCorrector", "ak10PFL2RelativeCorrector", "ak10PFL3AbsoluteCorrector", "ak10PFResidualCorrector")
)


process.ak10PFL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak10PFL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak10PFL2RelativeCorrector", "ak10PFL3AbsoluteCorrector")
)


process.ak10PFL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak10PFL2RelativeCorrector", "ak10PFL3AbsoluteCorrector", "ak10PFResidualCorrector")
)


process.ak10PFL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK10PF'),
    level = cms.string('L2Relative')
)


process.ak10PFL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK10PF'),
    level = cms.string('L3Absolute')
)


process.ak10PFResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2L3Residual')
)


process.ak1PFCHSL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak1PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak1PFCHSL1FastjetCorrector", "ak1PFCHSL2RelativeCorrector", "ak1PFCHSL3AbsoluteCorrector", "ak1PFCHSResidualCorrector")
)


process.ak1PFCHSL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak1PFCHSL1OffsetCorrector", "ak1PFCHSL2RelativeCorrector", "ak1PFCHSL3AbsoluteCorrector", "ak1PFCHSResidualCorrector")
)


process.ak1PFCHSL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak1PFCHSL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak1PFCHSL2RelativeCorrector", "ak1PFCHSL3AbsoluteCorrector")
)


process.ak1PFCHSL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak1PFCHSL2RelativeCorrector", "ak1PFCHSL3AbsoluteCorrector", "ak1PFCHSResidualCorrector")
)


process.ak1PFCHSL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK1PFchs'),
    level = cms.string('L2Relative')
)


process.ak1PFCHSL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK1PFchs'),
    level = cms.string('L3Absolute')
)


process.ak1PFCHSResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak1PFJetsL1FastL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak1PFL1FastL2L3Corrector"),
    src = cms.InputTag("ak1PFJets")
)


process.ak1PFJetsL1FastL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak1PFL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("ak1PFJets")
)


process.ak1PFJetsL1L2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak1PFL1L2L3Corrector"),
    src = cms.InputTag("ak1PFJets")
)


process.ak1PFJetsL1L2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak1PFL1L2L3ResidualCorrector"),
    src = cms.InputTag("ak1PFJets")
)


process.ak1PFJetsL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak1PFL2L3Corrector"),
    src = cms.InputTag("ak1PFJets")
)


process.ak1PFJetsL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak1PFL2L3ResidualCorrector"),
    src = cms.InputTag("ak1PFJets")
)


process.ak1PFL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak1PFL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak1PFL1FastjetCorrector", "ak1PFL2RelativeCorrector", "ak1PFL3AbsoluteCorrector", "ak1PFResidualCorrector")
)


process.ak1PFL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak1PFL1OffsetCorrector", "ak1PFL2RelativeCorrector", "ak1PFL3AbsoluteCorrector", "ak1PFResidualCorrector")
)


process.ak1PFL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak1PFL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak1PFL2RelativeCorrector", "ak1PFL3AbsoluteCorrector")
)


process.ak1PFL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak1PFL2RelativeCorrector", "ak1PFL3AbsoluteCorrector", "ak1PFResidualCorrector")
)


process.ak1PFL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK1PF'),
    level = cms.string('L2Relative')
)


process.ak1PFL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK1PF'),
    level = cms.string('L3Absolute')
)


process.ak1PFResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2L3Residual')
)


process.ak2PFCHSL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak2PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak2PFCHSL1FastjetCorrector", "ak2PFCHSL2RelativeCorrector", "ak2PFCHSL3AbsoluteCorrector", "ak2PFCHSResidualCorrector")
)


process.ak2PFCHSL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak2PFCHSL1OffsetCorrector", "ak2PFCHSL2RelativeCorrector", "ak2PFCHSL3AbsoluteCorrector", "ak2PFCHSResidualCorrector")
)


process.ak2PFCHSL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak2PFCHSL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak2PFCHSL2RelativeCorrector", "ak2PFCHSL3AbsoluteCorrector")
)


process.ak2PFCHSL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak2PFCHSL2RelativeCorrector", "ak2PFCHSL3AbsoluteCorrector", "ak2PFCHSResidualCorrector")
)


process.ak2PFCHSL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK2PFchs'),
    level = cms.string('L2Relative')
)


process.ak2PFCHSL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK2PFchs'),
    level = cms.string('L3Absolute')
)


process.ak2PFCHSResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak2PFJetsL1FastL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak2PFL1FastL2L3Corrector"),
    src = cms.InputTag("ak2PFJets")
)


process.ak2PFJetsL1FastL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak2PFL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("ak2PFJets")
)


process.ak2PFJetsL1L2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak2PFL1L2L3Corrector"),
    src = cms.InputTag("ak2PFJets")
)


process.ak2PFJetsL1L2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak2PFL1L2L3ResidualCorrector"),
    src = cms.InputTag("ak2PFJets")
)


process.ak2PFJetsL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak2PFL2L3Corrector"),
    src = cms.InputTag("ak2PFJets")
)


process.ak2PFJetsL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak2PFL2L3ResidualCorrector"),
    src = cms.InputTag("ak2PFJets")
)


process.ak2PFL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak2PFL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak2PFL1FastjetCorrector", "ak2PFL2RelativeCorrector", "ak2PFL3AbsoluteCorrector", "ak2PFResidualCorrector")
)


process.ak2PFL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak2PFL1OffsetCorrector", "ak2PFL2RelativeCorrector", "ak2PFL3AbsoluteCorrector", "ak2PFResidualCorrector")
)


process.ak2PFL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak2PFL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak2PFL2RelativeCorrector", "ak2PFL3AbsoluteCorrector")
)


process.ak2PFL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak2PFL2RelativeCorrector", "ak2PFL3AbsoluteCorrector", "ak2PFResidualCorrector")
)


process.ak2PFL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK2PF'),
    level = cms.string('L2Relative')
)


process.ak2PFL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK2PF'),
    level = cms.string('L3Absolute')
)


process.ak2PFResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2L3Residual')
)


process.ak3PFCHSL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak3PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak3PFCHSL1FastjetCorrector", "ak3PFCHSL2RelativeCorrector", "ak3PFCHSL3AbsoluteCorrector", "ak3PFCHSResidualCorrector")
)


process.ak3PFCHSL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak3PFCHSL1OffsetCorrector", "ak3PFCHSL2RelativeCorrector", "ak3PFCHSL3AbsoluteCorrector", "ak3PFCHSResidualCorrector")
)


process.ak3PFCHSL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak3PFCHSL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak3PFCHSL2RelativeCorrector", "ak3PFCHSL3AbsoluteCorrector")
)


process.ak3PFCHSL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak3PFCHSL2RelativeCorrector", "ak3PFCHSL3AbsoluteCorrector", "ak3PFCHSResidualCorrector")
)


process.ak3PFCHSL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK3PFchs'),
    level = cms.string('L2Relative')
)


process.ak3PFCHSL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK3PFchs'),
    level = cms.string('L3Absolute')
)


process.ak3PFCHSResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak3PFJetsL1FastL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak3PFL1FastL2L3Corrector"),
    src = cms.InputTag("ak3PFJets")
)


process.ak3PFJetsL1FastL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak3PFL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("ak3PFJets")
)


process.ak3PFJetsL1L2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak3PFL1L2L3Corrector"),
    src = cms.InputTag("ak3PFJets")
)


process.ak3PFJetsL1L2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak3PFL1L2L3ResidualCorrector"),
    src = cms.InputTag("ak3PFJets")
)


process.ak3PFJetsL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak3PFL2L3Corrector"),
    src = cms.InputTag("ak3PFJets")
)


process.ak3PFJetsL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak3PFL2L3ResidualCorrector"),
    src = cms.InputTag("ak3PFJets")
)


process.ak3PFL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak3PFL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak3PFL1FastjetCorrector", "ak3PFL2RelativeCorrector", "ak3PFL3AbsoluteCorrector", "ak3PFResidualCorrector")
)


process.ak3PFL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak3PFL1OffsetCorrector", "ak3PFL2RelativeCorrector", "ak3PFL3AbsoluteCorrector", "ak3PFResidualCorrector")
)


process.ak3PFL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak3PFL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak3PFL2RelativeCorrector", "ak3PFL3AbsoluteCorrector")
)


process.ak3PFL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak3PFL2RelativeCorrector", "ak3PFL3AbsoluteCorrector", "ak3PFResidualCorrector")
)


process.ak3PFL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK3PF'),
    level = cms.string('L2Relative')
)


process.ak3PFL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK3PF'),
    level = cms.string('L3Absolute')
)


process.ak3PFResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2L3Residual')
)


process.ak4CaloJetsL1 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak4CaloL1FastjetCorrector"),
    src = cms.InputTag("ak4CaloJets")
)


process.ak4CaloJetsL1FastL2L3 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak4CaloL1FastL2L3Corrector"),
    src = cms.InputTag("ak4CaloJets")
)


process.ak4CaloJetsL1FastL2L3Residual = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak4CaloL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("ak4CaloJets")
)


process.ak4CaloJetsL1L2L3 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak4CaloL1L2L3Corrector"),
    src = cms.InputTag("ak4CaloJets")
)


process.ak4CaloJetsL1L2L3L6 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak4CaloL1L2L3L6Corrector"),
    src = cms.InputTag("ak4CaloJets")
)


process.ak4CaloJetsL1L2L3Residual = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak4CaloL1L2L3ResidualCorrector"),
    src = cms.InputTag("ak4CaloJets")
)


process.ak4CaloJetsL2 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak4CaloL2RelativeCorrector"),
    src = cms.InputTag("ak4CaloJets")
)


process.ak4CaloJetsL2L3 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak4CaloL2L3Corrector"),
    src = cms.InputTag("ak4CaloJets")
)


process.ak4CaloJetsL2L3L6 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak4CaloL2L3L6Corrector"),
    src = cms.InputTag("ak4CaloJets")
)


process.ak4CaloJetsL2L3Residual = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak4CaloL2L3ResidualCorrector"),
    src = cms.InputTag("ak4CaloJets")
)


process.ak4CaloL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1FastjetCorrector", "ak4CaloL2RelativeCorrector", "ak4CaloL3AbsoluteCorrector")
)


process.ak4CaloL1FastL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1FastjetCorrector", "ak4CaloL2RelativeCorrector", "ak4CaloL3AbsoluteCorrector", "ak4CaloL6SLBCorrector")
)


process.ak4CaloL1FastL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1FastjetCorrector", "ak4CaloL2RelativeCorrector", "ak4CaloL3AbsoluteCorrector", "ak4CaloResidualCorrector")
)


process.ak4CaloL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAllCalo")
)


process.ak4CaloL1L2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1OffsetCorrector", "ak4CaloL2RelativeCorrector", "ak4CaloL3AbsoluteCorrector")
)


process.ak4CaloL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1OffsetCorrector", "ak4CaloL2RelativeCorrector", "ak4CaloL3AbsoluteCorrector", "ak4CaloResidualCorrector")
)


process.ak4CaloL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak4CaloL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL2RelativeCorrector", "ak4CaloL3AbsoluteCorrector")
)


process.ak4CaloL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL2RelativeCorrector", "ak4CaloL3AbsoluteCorrector", "ak4CaloL6SLBCorrector")
)


process.ak4CaloL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL2RelativeCorrector", "ak4CaloL3AbsoluteCorrector", "ak4CaloResidualCorrector")
)


process.ak4CaloL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L2Relative')
)


process.ak4CaloL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L3Absolute')
)


process.ak4CaloL6SLBCorrector = cms.EDProducer("L6SLBCorrectorProducer",
    addMuonToJet = cms.bool(True),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("ak4CaloJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("ak4CaloJetsSoftMuonTagInfos")
)


process.ak4CaloResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L2L3Residual')
)


process.ak4JPTJetsL1 = cms.EDProducer("CorrectedJPTJetProducer",
    correctors = cms.VInputTag("ak4L1JPTFastjetCorrector"),
    src = cms.InputTag("JetPlusTrackZSPCorJetAntiKt4")
)


process.ak4JPTJetsL1FastL2L3 = cms.EDProducer("CorrectedJPTJetProducer",
    correctors = cms.VInputTag("ak4JPTL1FastL2L3Corrector"),
    src = cms.InputTag("JetPlusTrackZSPCorJetAntiKt4")
)


process.ak4JPTJetsL1FastL2L3Residual = cms.EDProducer("CorrectedJPTJetProducer",
    correctors = cms.VInputTag("ak4JPTL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("JetPlusTrackZSPCorJetAntiKt4")
)


process.ak4JPTJetsL1L2L3 = cms.EDProducer("CorrectedJPTJetProducer",
    correctors = cms.VInputTag("ak4JPTL1L2L3Corrector"),
    src = cms.InputTag("JetPlusTrackZSPCorJetAntiKt4")
)


process.ak4JPTJetsL1L2L3Residual = cms.EDProducer("CorrectedJPTJetProducer",
    correctors = cms.VInputTag("ak4JPTL1L2L3ResidualCorrector"),
    src = cms.InputTag("JetPlusTrackZSPCorJetAntiKt4")
)


process.ak4JPTJetsL2 = cms.EDProducer("CorrectedJPTJetProducer",
    correctors = cms.VInputTag("ak4JPTL2RelativeCorrector"),
    src = cms.InputTag("JetPlusTrackZSPCorJetAntiKt4")
)


process.ak4JPTJetsL2L3 = cms.EDProducer("CorrectedJPTJetProducer",
    correctors = cms.VInputTag("ak4JPTL2L3Corrector"),
    src = cms.InputTag("JetPlusTrackZSPCorJetAntiKt4")
)


process.ak4JPTJetsL2L3Residual = cms.EDProducer("CorrectedJPTJetProducer",
    correctors = cms.VInputTag("ak4JPTL2L3ResidualCorrector"),
    src = cms.InputTag("JetPlusTrackZSPCorJetAntiKt4")
)


process.ak4JPTL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1FastjetCorrector", "ak4L1JPTFastjetCorrector", "ak4JPTL2RelativeCorrector", "ak4JPTL3AbsoluteCorrector")
)


process.ak4JPTL1FastL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1FastjetCorrector", "ak4L1JPTFastjetCorrector", "ak4JPTL2RelativeCorrector", "ak4JPTL3AbsoluteCorrector", "ak4JPTResidualCorrector")
)


process.ak4JPTL1L2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1OffsetCorrector", "ak4L1JPTOffsetCorrector", "ak4JPTL2RelativeCorrector", "ak4JPTL3AbsoluteCorrector")
)


process.ak4JPTL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1OffsetCorrector", "ak4L1JPTOffsetCorrector", "ak4JPTL2RelativeCorrector", "ak4JPTL3AbsoluteCorrector", "ak4JPTResidualCorrector")
)


process.ak4JPTL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1OffsetCorrector", "ak4L1JPTOffsetCorrector", "ak4JPTL2RelativeCorrector", "ak4JPTL3AbsoluteCorrector")
)


process.ak4JPTL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1OffsetCorrector", "ak4L1JPTOffsetCorrector", "ak4JPTL2RelativeCorrector", "ak4JPTL3AbsoluteCorrector", "ak4JPTResidualCorrector")
)


process.ak4JPTL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4JPT'),
    level = cms.string('L2Relative')
)


process.ak4JPTL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4JPT'),
    level = cms.string('L3Absolute')
)


process.ak4JPTResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4JPT'),
    level = cms.string('L2L3Residual')
)


process.ak4L1JPTFastjetCorrector = cms.EDProducer("L1JPTOffsetCorrectorProducer",
    algorithm = cms.string('AK4JPT'),
    level = cms.string('L1JPTOffset'),
    offsetService = cms.InputTag("ak4CaloL1FastjetCorrector")
)


process.ak4L1JPTOffsetCorrector = cms.EDProducer("L1JPTOffsetCorrectorProducer",
    algorithm = cms.string('AK4JPT'),
    level = cms.string('L1JPTOffset'),
    offsetService = cms.InputTag("ak4CaloL1OffsetCorrector")
)


process.ak4PFCHSJetsL1 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak4PFCHSL1FastjetCorrector"),
    src = cms.InputTag("ak4PFJetsCHS")
)


process.ak4PFCHSJetsL1L2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak4PFCHSL1L2L3Corrector"),
    src = cms.InputTag("ak4PFJetsCHS")
)


process.ak4PFCHSJetsL2 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak4PFCHSL2RelativeCorrector"),
    src = cms.InputTag("ak4PFJetsCHS")
)


process.ak4PFCHSJetsL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak4PFCHSL2L3Corrector"),
    src = cms.InputTag("ak4PFJetsCHS")
)


process.ak4PFCHSL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFCHSL1FastjetCorrector", "ak4PFCHSL2RelativeCorrector", "ak4PFCHSL3AbsoluteCorrector")
)


process.ak4PFCHSL1FastL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFCHSL1FastjetCorrector", "ak4PFCHSL2RelativeCorrector", "ak4PFCHSL3AbsoluteCorrector", "ak4PFCHSResidualCorrector")
)


process.ak4PFCHSL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak4PFCHSL1L2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFCHSL1OffsetCorrector", "ak4PFCHSL2RelativeCorrector", "ak4PFCHSL3AbsoluteCorrector")
)


process.ak4PFCHSL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFCHSL1OffsetCorrector", "ak4PFCHSL2RelativeCorrector", "ak4PFCHSL3AbsoluteCorrector", "ak4PFCHSResidualCorrector")
)


process.ak4PFCHSL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak4PFCHSL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFCHSL2RelativeCorrector", "ak4PFCHSL3AbsoluteCorrector")
)


process.ak4PFCHSL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFCHSL2RelativeCorrector", "ak4PFCHSL3AbsoluteCorrector", "ak4PFCHSResidualCorrector")
)


process.ak4PFCHSL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L2Relative')
)


process.ak4PFCHSL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L3Absolute')
)


process.ak4PFCHSResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak4PFJetsL1 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak4PFL1FastjetCorrector"),
    src = cms.InputTag("ak4PFJets")
)


process.ak4PFJetsL1FastL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak4PFL1FastL2L3Corrector"),
    src = cms.InputTag("ak4PFJets")
)


process.ak4PFJetsL1FastL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak4PFL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("ak4PFJets")
)


process.ak4PFJetsL1L2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak4PFL1L2L3Corrector"),
    src = cms.InputTag("ak4PFJets")
)


process.ak4PFJetsL1L2L3L6 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak4PFL1L2L3L6Corrector"),
    src = cms.InputTag("ak4PFJets")
)


process.ak4PFJetsL1L2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak4PFL1L2L3ResidualCorrector"),
    src = cms.InputTag("ak4PFJets")
)


process.ak4PFJetsL2 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak4PFL2RelativeCorrector"),
    src = cms.InputTag("ak4PFJets")
)


process.ak4PFJetsL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak4PFL2L3Corrector"),
    src = cms.InputTag("ak4PFJets")
)


process.ak4PFJetsL2L3L6 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak4PFL2L3L6Corrector"),
    src = cms.InputTag("ak4PFJets")
)


process.ak4PFJetsL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak4PFL2L3ResidualCorrector"),
    src = cms.InputTag("ak4PFJets")
)


process.ak4PFL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL1FastjetCorrector", "ak4PFL2RelativeCorrector", "ak4PFL3AbsoluteCorrector")
)


process.ak4PFL1FastL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL1FastjetCorrector", "ak4PFL2RelativeCorrector", "ak4PFL3AbsoluteCorrector", "ak4PFL6SLBCorrector")
)


process.ak4PFL1FastL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL1FastjetCorrector", "ak4PFL2RelativeCorrector", "ak4PFL3AbsoluteCorrector", "ak4PFResidualCorrector")
)


process.ak4PFL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak4PFL1L2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL1OffsetCorrector", "ak4PFL2RelativeCorrector", "ak4PFL3AbsoluteCorrector")
)


process.ak4PFL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL1OffsetCorrector", "ak4PFL2RelativeCorrector", "ak4PFL3AbsoluteCorrector", "ak4PFResidualCorrector")
)


process.ak4PFL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak4PFL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL2RelativeCorrector", "ak4PFL3AbsoluteCorrector")
)


process.ak4PFL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL2RelativeCorrector", "ak4PFL3AbsoluteCorrector", "ak4PFL6SLBCorrector")
)


process.ak4PFL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL2RelativeCorrector", "ak4PFL3AbsoluteCorrector", "ak4PFResidualCorrector")
)


process.ak4PFL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2Relative')
)


process.ak4PFL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L3Absolute')
)


process.ak4PFL6SLBCorrector = cms.EDProducer("L6SLBCorrectorProducer",
    addMuonToJet = cms.bool(False),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("ak4PFJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("ak4PFJetsSoftMuonTagInfos")
)


process.ak4PFPuppiL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFPuppiL1FastjetCorrector", "ak4PFPuppiL2RelativeCorrector", "ak4PFPuppiL3AbsoluteCorrector")
)


process.ak4PFPuppiL1FastL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFPuppiL1FastjetCorrector", "ak4PFPuppiL2RelativeCorrector", "ak4PFPuppiL3AbsoluteCorrector", "ak4PFPuppiResidualCorrector")
)


process.ak4PFPuppiL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PFPuppi'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak4PFPuppiL1L2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFPuppiL1OffsetCorrector", "ak4PFPuppiL2RelativeCorrector", "ak4PFPuppiL3AbsoluteCorrector")
)


process.ak4PFPuppiL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFPuppiL1OffsetCorrector", "ak4PFPuppiL2RelativeCorrector", "ak4PFPuppiL3AbsoluteCorrector", "ak4PFPuppiResidualCorrector")
)


process.ak4PFPuppiL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PFPuppi'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak4PFPuppiL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFPuppiL2RelativeCorrector", "ak4PFPuppiL3AbsoluteCorrector")
)


process.ak4PFPuppiL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFPuppiL2RelativeCorrector", "ak4PFPuppiL3AbsoluteCorrector", "ak4PFPuppiResidualCorrector")
)


process.ak4PFPuppiL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFPuppi'),
    level = cms.string('L2Relative')
)


process.ak4PFPuppiL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFPuppi'),
    level = cms.string('L3Absolute')
)


process.ak4PFPuppiResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFPuppi'),
    level = cms.string('L2L3Residual')
)


process.ak4PFResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2L3Residual')
)


process.ak4TrackJetsL1 = cms.EDProducer("CorrectedTrackJetProducer",
    correctors = cms.VInputTag("ak4TrackL1FastjetCorrector"),
    src = cms.InputTag("ak4TrackJets")
)


process.ak4TrackJetsL2 = cms.EDProducer("CorrectedTrackJetProducer",
    correctors = cms.VInputTag("ak4TrackL2RelativeCorrector"),
    src = cms.InputTag("ak4TrackJets")
)


process.ak4TrackJetsL2L3 = cms.EDProducer("CorrectedTrackJetProducer",
    correctors = cms.VInputTag("ak4TrackL2L3Corrector"),
    src = cms.InputTag("ak4TrackJets")
)


process.ak4TrackL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1FastjetCorrector", "ak4TrackL2RelativeCorrector", "ak4TrackL3AbsoluteCorrector")
)


process.ak4TrackL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4TrackL2RelativeCorrector", "ak4TrackL3AbsoluteCorrector")
)


process.ak4TrackL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4TRK'),
    level = cms.string('L2Relative')
)


process.ak4TrackL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4TRK'),
    level = cms.string('L3Absolute')
)


process.ak5PFCHSL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak5PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak5PFCHSL1FastjetCorrector", "ak5PFCHSL2RelativeCorrector", "ak5PFCHSL3AbsoluteCorrector", "ak5PFCHSResidualCorrector")
)


process.ak5PFCHSL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak5PFCHSL1OffsetCorrector", "ak5PFCHSL2RelativeCorrector", "ak5PFCHSL3AbsoluteCorrector", "ak5PFCHSResidualCorrector")
)


process.ak5PFCHSL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak5PFCHSL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak5PFCHSL2RelativeCorrector", "ak5PFCHSL3AbsoluteCorrector")
)


process.ak5PFCHSL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak5PFCHSL2RelativeCorrector", "ak5PFCHSL3AbsoluteCorrector", "ak5PFCHSResidualCorrector")
)


process.ak5PFCHSL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK5PFchs'),
    level = cms.string('L2Relative')
)


process.ak5PFCHSL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK5PFchs'),
    level = cms.string('L3Absolute')
)


process.ak5PFCHSResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak5PFJetsL1FastL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak5PFL1FastL2L3Corrector"),
    src = cms.InputTag("ak5PFJets")
)


process.ak5PFJetsL1FastL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak5PFL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("ak5PFJets")
)


process.ak5PFJetsL1L2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak5PFL1L2L3Corrector"),
    src = cms.InputTag("ak5PFJets")
)


process.ak5PFJetsL1L2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak5PFL1L2L3ResidualCorrector"),
    src = cms.InputTag("ak5PFJets")
)


process.ak5PFJetsL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak5PFL2L3Corrector"),
    src = cms.InputTag("ak5PFJets")
)


process.ak5PFJetsL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak5PFL2L3ResidualCorrector"),
    src = cms.InputTag("ak5PFJets")
)


process.ak5PFL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak5PFL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak5PFL1FastjetCorrector", "ak5PFL2RelativeCorrector", "ak5PFL3AbsoluteCorrector", "ak5PFResidualCorrector")
)


process.ak5PFL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak5PFL1OffsetCorrector", "ak5PFL2RelativeCorrector", "ak5PFL3AbsoluteCorrector", "ak5PFResidualCorrector")
)


process.ak5PFL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak5PFL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak5PFL2RelativeCorrector", "ak5PFL3AbsoluteCorrector")
)


process.ak5PFL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak5PFL2RelativeCorrector", "ak5PFL3AbsoluteCorrector", "ak5PFResidualCorrector")
)


process.ak5PFL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK5PF'),
    level = cms.string('L2Relative')
)


process.ak5PFL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK5PF'),
    level = cms.string('L3Absolute')
)


process.ak5PFResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2L3Residual')
)


process.ak6PFCHSL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak6PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak6PFCHSL1FastjetCorrector", "ak6PFCHSL2RelativeCorrector", "ak6PFCHSL3AbsoluteCorrector", "ak6PFCHSResidualCorrector")
)


process.ak6PFCHSL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak6PFCHSL1OffsetCorrector", "ak6PFCHSL2RelativeCorrector", "ak6PFCHSL3AbsoluteCorrector", "ak6PFCHSResidualCorrector")
)


process.ak6PFCHSL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak6PFCHSL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak6PFCHSL2RelativeCorrector", "ak6PFCHSL3AbsoluteCorrector")
)


process.ak6PFCHSL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak6PFCHSL2RelativeCorrector", "ak6PFCHSL3AbsoluteCorrector", "ak6PFCHSResidualCorrector")
)


process.ak6PFCHSL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK6PFchs'),
    level = cms.string('L2Relative')
)


process.ak6PFCHSL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK6PFchs'),
    level = cms.string('L3Absolute')
)


process.ak6PFCHSResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak6PFJetsL1FastL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak6PFL1FastL2L3Corrector"),
    src = cms.InputTag("ak6PFJets")
)


process.ak6PFJetsL1FastL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak6PFL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("ak6PFJets")
)


process.ak6PFJetsL1L2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak6PFL1L2L3Corrector"),
    src = cms.InputTag("ak6PFJets")
)


process.ak6PFJetsL1L2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak6PFL1L2L3ResidualCorrector"),
    src = cms.InputTag("ak6PFJets")
)


process.ak6PFJetsL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak6PFL2L3Corrector"),
    src = cms.InputTag("ak6PFJets")
)


process.ak6PFJetsL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak6PFL2L3ResidualCorrector"),
    src = cms.InputTag("ak6PFJets")
)


process.ak6PFL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak6PFL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak6PFL1FastjetCorrector", "ak6PFL2RelativeCorrector", "ak6PFL3AbsoluteCorrector", "ak6PFResidualCorrector")
)


process.ak6PFL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak6PFL1OffsetCorrector", "ak6PFL2RelativeCorrector", "ak6PFL3AbsoluteCorrector", "ak6PFResidualCorrector")
)


process.ak6PFL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak6PFL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak6PFL2RelativeCorrector", "ak6PFL3AbsoluteCorrector")
)


process.ak6PFL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak6PFL2RelativeCorrector", "ak6PFL3AbsoluteCorrector", "ak6PFResidualCorrector")
)


process.ak6PFL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK6PF'),
    level = cms.string('L2Relative')
)


process.ak6PFL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK6PF'),
    level = cms.string('L3Absolute')
)


process.ak6PFResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2L3Residual')
)


process.ak7CaloJetsL1FastL2L3 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak7CaloL1FastL2L3Corrector"),
    src = cms.InputTag("ak7CaloJets")
)


process.ak7CaloJetsL1FastL2L3Residual = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak7CaloL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("ak7CaloJets")
)


process.ak7CaloJetsL1L2L3 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak7CaloL1L2L3Corrector"),
    src = cms.InputTag("ak7CaloJets")
)


process.ak7CaloJetsL1L2L3Residual = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak7CaloL1L2L3ResidualCorrector"),
    src = cms.InputTag("ak7CaloJets")
)


process.ak7CaloJetsL2L3 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak7CaloL2L3Corrector"),
    src = cms.InputTag("ak7CaloJets")
)


process.ak7CaloJetsL2L3Residual = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ak7CaloL2L3ResidualCorrector"),
    src = cms.InputTag("ak7CaloJets")
)


process.ak7CaloL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1FastjetCorrector", "ak7CaloL2RelativeCorrector", "ak7CaloL3AbsoluteCorrector")
)


process.ak7CaloL1FastL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7CaloL1OffsetCorrector", "ak7CaloL2RelativeCorrector", "ak7CaloL3AbsoluteCorrector", "ak7CaloL6SLBCorrector")
)


process.ak7CaloL1FastL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7CaloL1FastjetCorrector", "ak7CaloL2RelativeCorrector", "ak7CaloL3AbsoluteCorrector", "ak7CaloResidualCorrector")
)


process.ak7CaloL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAllCalo")
)


process.ak7CaloL1L2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7CaloL1OffsetCorrector", "ak7CaloL2RelativeCorrector", "ak7CaloL3AbsoluteCorrector")
)


process.ak7CaloL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7CaloL1OffsetCorrector", "ak7CaloL2RelativeCorrector", "ak7CaloL3AbsoluteCorrector", "ak7CaloResidualCorrector")
)


process.ak7CaloL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak7CaloL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7CaloL2RelativeCorrector", "ak7CaloL3AbsoluteCorrector")
)


process.ak7CaloL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7CaloL2RelativeCorrector", "ak7CaloL3AbsoluteCorrector", "ak7CaloL6SLBCorrector")
)


process.ak7CaloL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7CaloL2RelativeCorrector", "ak7CaloL3AbsoluteCorrector", "ak7CaloResidualCorrector")
)


process.ak7CaloL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK7Calo'),
    level = cms.string('L2Relative')
)


process.ak7CaloL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK7Calo'),
    level = cms.string('L3Absolute')
)


process.ak7CaloL6SLBCorrector = cms.EDProducer("L6SLBCorrectorProducer",
    addMuonToJet = cms.bool(True),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("ak7CaloJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("ak7CaloJetsSoftMuonTagInfos")
)


process.ak7CaloResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L2L3Residual')
)


process.ak7JPTL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7CaloL1FastjetCorrector", "ak7L1JPTFastjetCorrector", "ak7JPTL2RelativeCorrector", "ak7JPTL3AbsoluteCorrector")
)


process.ak7JPTL1FastL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7CaloL1FastjetCorrector", "ak7L1JPTFastjetCorrector", "ak7JPTL2RelativeCorrector", "ak7JPTL3AbsoluteCorrector", "ak7JPTResidualCorrector")
)


process.ak7JPTL1L2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7CaloL1OffsetCorrector", "ak7L1JPTOffsetCorrector", "ak7JPTL2RelativeCorrector", "ak7JPTL3AbsoluteCorrector")
)


process.ak7JPTL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7CaloL1OffsetCorrector", "ak7L1JPTOffsetCorrector", "ak7JPTL2RelativeCorrector", "ak7JPTL3AbsoluteCorrector", "ak7JPTResidualCorrector")
)


process.ak7JPTL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7CaloL1OffsetCorrector", "ak7L1JPTOffsetCorrector", "ak7JPTL2RelativeCorrector", "ak7JPTL3AbsoluteCorrector")
)


process.ak7JPTL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK7JPT'),
    level = cms.string('L2Relative')
)


process.ak7JPTL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK7JPT'),
    level = cms.string('L3Absolute')
)


process.ak7JPTL6SLBCorrector = cms.EDProducer("L6SLBCorrectorProducer",
    addMuonToJet = cms.bool(True),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("ak7JPTJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("ak7JPTJetsSoftMuonTagInfos")
)


process.ak7JPTResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L2L3Residual')
)


process.ak7L1JPTFastjetCorrector = cms.EDProducer("L1JPTOffsetCorrectorProducer",
    algorithm = cms.string('AK7JPT'),
    level = cms.string('L1JPTOffset'),
    offsetService = cms.InputTag("ak7CaloL1FastjetCorrector")
)


process.ak7L1JPTOffsetCorrector = cms.EDProducer("L1JPTOffsetCorrectorProducer",
    algorithm = cms.string('AK7JPT'),
    level = cms.string('L1JPTOffset'),
    offsetService = cms.InputTag("ak7CaloL1OffsetCorrector")
)


process.ak7PFCHSL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFCHSL1FastjetCorrector", "ak7PFCHSL2RelativeCorrector", "ak7PFCHSL3AbsoluteCorrector")
)


process.ak7PFCHSL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak7PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7PFCHSL1FastjetCorrector", "ak7PFCHSL2RelativeCorrector", "ak7PFCHSL3AbsoluteCorrector", "ak7PFCHSResidualCorrector")
)


process.ak7PFCHSL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7PFCHSL1OffsetCorrector", "ak7PFCHSL2RelativeCorrector", "ak7PFCHSL3AbsoluteCorrector", "ak7PFCHSResidualCorrector")
)


process.ak7PFCHSL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak7PFCHSL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7PFCHSL2RelativeCorrector", "ak7PFCHSL3AbsoluteCorrector")
)


process.ak7PFCHSL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7PFCHSL2RelativeCorrector", "ak7PFCHSL3AbsoluteCorrector", "ak7PFCHSResidualCorrector")
)


process.ak7PFCHSL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK7PFchs'),
    level = cms.string('L2Relative')
)


process.ak7PFCHSL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK7PFchs'),
    level = cms.string('L3Absolute')
)


process.ak7PFCHSResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak7PFJetsL1FastL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak7PFL1FastL2L3Corrector"),
    src = cms.InputTag("ak7PFJets")
)


process.ak7PFJetsL1FastL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak7PFL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("ak7PFJets")
)


process.ak7PFJetsL1L2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak7PFL1L2L3Corrector"),
    src = cms.InputTag("ak7PFJets")
)


process.ak7PFJetsL1L2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak7PFL1L2L3ResidualCorrector"),
    src = cms.InputTag("ak7PFJets")
)


process.ak7PFJetsL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak7PFL2L3Corrector"),
    src = cms.InputTag("ak7PFJets")
)


process.ak7PFJetsL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak7PFL2L3ResidualCorrector"),
    src = cms.InputTag("ak7PFJets")
)


process.ak7PFL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL1FastjetCorrector", "ak7PFL2RelativeCorrector", "ak7PFL3AbsoluteCorrector")
)


process.ak7PFL1FastL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL1FastjetCorrector", "ak7PFL2RelativeCorrector", "ak7PFL3AbsoluteCorrector", "ak7PFL6SLBCorrector")
)


process.ak7PFL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak7PFL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7PFL1FastjetCorrector", "ak7PFL2RelativeCorrector", "ak7PFL3AbsoluteCorrector", "ak7PFResidualCorrector")
)


process.ak7PFL1L2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7PFL1OffsetCorrector", "ak7PFL2RelativeCorrector", "ak7PFL3AbsoluteCorrector")
)


process.ak7PFL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7PFL1OffsetCorrector", "ak7PFL2RelativeCorrector", "ak7PFL3AbsoluteCorrector", "ak7PFResidualCorrector")
)


process.ak7PFL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak7PFL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7PFL2RelativeCorrector", "ak7PFL3AbsoluteCorrector")
)


process.ak7PFL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7PFL2RelativeCorrector", "ak7PFL3AbsoluteCorrector", "ak7PFL6SLBCorrector")
)


process.ak7PFL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak7PFL2RelativeCorrector", "ak7PFL3AbsoluteCorrector", "ak7PFResidualCorrector")
)


process.ak7PFL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK7PF'),
    level = cms.string('L2Relative')
)


process.ak7PFL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK7PF'),
    level = cms.string('L3Absolute')
)


process.ak7PFL6SLBCorrector = cms.EDProducer("L6SLBCorrectorProducer",
    addMuonToJet = cms.bool(False),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("ak7PFJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("ak7PFJetsSoftMuonTagInfos")
)


process.ak7PFResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2L3Residual')
)


process.ak8PFCHSL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak8PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak8PFCHSL1FastjetCorrector", "ak8PFCHSL2RelativeCorrector", "ak8PFCHSL3AbsoluteCorrector", "ak8PFCHSResidualCorrector")
)


process.ak8PFCHSL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak8PFCHSL1OffsetCorrector", "ak8PFCHSL2RelativeCorrector", "ak8PFCHSL3AbsoluteCorrector", "ak8PFCHSResidualCorrector")
)


process.ak8PFCHSL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak8PFCHSL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak8PFCHSL2RelativeCorrector", "ak8PFCHSL3AbsoluteCorrector")
)


process.ak8PFCHSL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak8PFCHSL2RelativeCorrector", "ak8PFCHSL3AbsoluteCorrector", "ak8PFCHSResidualCorrector")
)


process.ak8PFCHSL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK8PFchs'),
    level = cms.string('L2Relative')
)


process.ak8PFCHSL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK8PFchs'),
    level = cms.string('L3Absolute')
)


process.ak8PFCHSResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak8PFJetsL1FastL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak8PFL1FastL2L3Corrector"),
    src = cms.InputTag("ak8PFJets")
)


process.ak8PFJetsL1FastL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak8PFL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("ak8PFJets")
)


process.ak8PFJetsL1L2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak8PFL1L2L3Corrector"),
    src = cms.InputTag("ak8PFJets")
)


process.ak8PFJetsL1L2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak8PFL1L2L3ResidualCorrector"),
    src = cms.InputTag("ak8PFJets")
)


process.ak8PFJetsL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak8PFL2L3Corrector"),
    src = cms.InputTag("ak8PFJets")
)


process.ak8PFJetsL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak8PFL2L3ResidualCorrector"),
    src = cms.InputTag("ak8PFJets")
)


process.ak8PFL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak8PFL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak8PFL1FastjetCorrector", "ak8PFL2RelativeCorrector", "ak8PFL3AbsoluteCorrector", "ak8PFResidualCorrector")
)


process.ak8PFL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak8PFL1OffsetCorrector", "ak8PFL2RelativeCorrector", "ak8PFL3AbsoluteCorrector", "ak8PFResidualCorrector")
)


process.ak8PFL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak8PFL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak8PFL2RelativeCorrector", "ak8PFL3AbsoluteCorrector")
)


process.ak8PFL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak8PFL2RelativeCorrector", "ak8PFL3AbsoluteCorrector", "ak8PFResidualCorrector")
)


process.ak8PFL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK8PF'),
    level = cms.string('L2Relative')
)


process.ak8PFL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK8PF'),
    level = cms.string('L3Absolute')
)


process.ak8PFResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2L3Residual')
)


process.ak9PFCHSL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak9PFCHSL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak9PFCHSL1FastjetCorrector", "ak9PFCHSL2RelativeCorrector", "ak9PFCHSL3AbsoluteCorrector", "ak9PFCHSResidualCorrector")
)


process.ak9PFCHSL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak9PFCHSL1OffsetCorrector", "ak9PFCHSL2RelativeCorrector", "ak9PFCHSL3AbsoluteCorrector", "ak9PFCHSResidualCorrector")
)


process.ak9PFCHSL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak9PFCHSL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak9PFCHSL2RelativeCorrector", "ak9PFCHSL3AbsoluteCorrector")
)


process.ak9PFCHSL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak9PFCHSL2RelativeCorrector", "ak9PFCHSL3AbsoluteCorrector", "ak9PFCHSResidualCorrector")
)


process.ak9PFCHSL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK9PFchs'),
    level = cms.string('L2Relative')
)


process.ak9PFCHSL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK9PFchs'),
    level = cms.string('L3Absolute')
)


process.ak9PFCHSResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak9PFJetsL1FastL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak9PFL1FastL2L3Corrector"),
    src = cms.InputTag("ak9PFJets")
)


process.ak9PFJetsL1FastL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak9PFL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("ak9PFJets")
)


process.ak9PFJetsL1L2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak9PFL1L2L3Corrector"),
    src = cms.InputTag("ak9PFJets")
)


process.ak9PFJetsL1L2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak9PFL1L2L3ResidualCorrector"),
    src = cms.InputTag("ak9PFJets")
)


process.ak9PFJetsL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak9PFL2L3Corrector"),
    src = cms.InputTag("ak9PFJets")
)


process.ak9PFJetsL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ak9PFL2L3ResidualCorrector"),
    src = cms.InputTag("ak9PFJets")
)


process.ak9PFL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak9PFL1FastjetL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak9PFL1FastjetCorrector", "ak9PFL2RelativeCorrector", "ak9PFL3AbsoluteCorrector", "ak9PFResidualCorrector")
)


process.ak9PFL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak9PFL1OffsetCorrector", "ak9PFL2RelativeCorrector", "ak9PFL3AbsoluteCorrector", "ak9PFResidualCorrector")
)


process.ak9PFL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ak9PFL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak9PFL2RelativeCorrector", "ak9PFL3AbsoluteCorrector")
)


process.ak9PFL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak9PFL2RelativeCorrector", "ak9PFL3AbsoluteCorrector", "ak9PFResidualCorrector")
)


process.ak9PFL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK9PF'),
    level = cms.string('L2Relative')
)


process.ak9PFL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK9PF'),
    level = cms.string('L3Absolute')
)


process.ak9PFResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2L3Residual')
)


process.ic5CaloJetsL1FastL2L3 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ic5CaloL1FastL2L3Corrector"),
    src = cms.InputTag("iterativeCone5CaloJets")
)


process.ic5CaloJetsL1FastL2L3Residual = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ic5CaloL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("iterativeCone5CaloJets")
)


process.ic5CaloJetsL1L2L3 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ic5CaloL1L2L3Corrector"),
    src = cms.InputTag("iterativeCone5CaloJets")
)


process.ic5CaloJetsL1L2L3Residual = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ic5CaloL1L2L3ResidualCorrector"),
    src = cms.InputTag("iterativeCone5CaloJets")
)


process.ic5CaloJetsL2L3 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ic5CaloL2L3Corrector"),
    src = cms.InputTag("iterativeCone5CaloJets")
)


process.ic5CaloJetsL2L3Residual = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("ic5CaloL2L3ResidualCorrector"),
    src = cms.InputTag("iterativeCone5CaloJets")
)


process.ic5CaloL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1FastjetCorrector", "ic5CaloL2RelativeCorrector", "ic5CaloL3AbsoluteCorrector")
)


process.ic5CaloL1FastL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ic5CaloL1OffsetCorrector", "ic5CaloL2RelativeCorrector", "ic5CaloL3AbsoluteCorrector", "ic5CaloL6SLBCorrector")
)


process.ic5CaloL1FastL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ic5CaloL1FastjetCorrector", "ic5CaloL2RelativeCorrector", "ic5CaloL3AbsoluteCorrector", "ic5CaloResidualCorrector")
)


process.ic5CaloL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAllCalo")
)


process.ic5CaloL1L2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ic5CaloL1OffsetCorrector", "ic5CaloL2RelativeCorrector", "ic5CaloL3AbsoluteCorrector")
)


process.ic5CaloL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ic5CaloL1OffsetCorrector", "ic5CaloL2RelativeCorrector", "ic5CaloL3AbsoluteCorrector", "ic5CaloResidualCorrector")
)


process.ic5CaloL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ic5CaloL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ic5CaloL2RelativeCorrector", "ic5CaloL3AbsoluteCorrector")
)


process.ic5CaloL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ic5CaloL2RelativeCorrector", "ic5CaloL3AbsoluteCorrector", "ic5CaloL6SLBCorrector")
)


process.ic5CaloL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ic5CaloL2RelativeCorrector", "ic5CaloL3AbsoluteCorrector", "ic5CaloResidualCorrector")
)


process.ic5CaloL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('IC5Calo'),
    level = cms.string('L2Relative')
)


process.ic5CaloL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('IC5Calo'),
    level = cms.string('L3Absolute')
)


process.ic5CaloL6SLBCorrector = cms.EDProducer("L6SLBCorrectorProducer",
    addMuonToJet = cms.bool(True),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("ic5CaloJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("ic5CaloJetsSoftMuonTagInfos")
)


process.ic5CaloResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L2L3Residual')
)


process.ic5PFJetsL1FastL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ic5PFL1FastL2L3Corrector"),
    src = cms.InputTag("iterativeCone5PFJets")
)


process.ic5PFJetsL1FastL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ic5PFL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("iterativeCone5PFJets")
)


process.ic5PFJetsL1L2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ic5PFL1L2L3Corrector"),
    src = cms.InputTag("iterativeCone5PFJets")
)


process.ic5PFJetsL1L2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ic5PFL1L2L3ResidualCorrector"),
    src = cms.InputTag("iterativeCone5PFJets")
)


process.ic5PFJetsL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ic5PFL2L3Corrector"),
    src = cms.InputTag("iterativeCone5PFJets")
)


process.ic5PFJetsL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("ic5PFL2L3ResidualCorrector"),
    src = cms.InputTag("iterativeCone5PFJets")
)


process.ic5PFL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL1FastjetCorrector", "ic5PFL2RelativeCorrector", "ic5PFL3AbsoluteCorrector")
)


process.ic5PFL1FastL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL1FastjetCorrector", "ic5PFL2RelativeCorrector", "ic5PFL3AbsoluteCorrector", "ic5PFL6SLBCorrector")
)


process.ic5PFL1FastL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ic5PFL1FastjetCorrector", "ic5PFL2RelativeCorrector", "ic5PFL3AbsoluteCorrector", "ic5PFResidualCorrector")
)


process.ic5PFL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ic5PFL1L2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ic5PFL1OffsetCorrector", "ic5PFL2RelativeCorrector", "ic5PFL3AbsoluteCorrector")
)


process.ic5PFL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ic5PFL1OffsetCorrector", "ic5PFL2RelativeCorrector", "ic5PFL3AbsoluteCorrector", "ic5PFResidualCorrector")
)


process.ic5PFL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.ic5PFL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ic5PFL2RelativeCorrector", "ic5PFL3AbsoluteCorrector")
)


process.ic5PFL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ic5PFL2RelativeCorrector", "ic5PFL3AbsoluteCorrector", "ic5PFL6SLBCorrector")
)


process.ic5PFL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ic5PFL2RelativeCorrector", "ic5PFL3AbsoluteCorrector", "ic5PFResidualCorrector")
)


process.ic5PFL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('IC5PF'),
    level = cms.string('L2Relative')
)


process.ic5PFL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('IC5PF'),
    level = cms.string('L3Absolute')
)


process.ic5PFL6SLBCorrector = cms.EDProducer("L6SLBCorrectorProducer",
    addMuonToJet = cms.bool(False),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("ic5PFJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("ic5PFJetsSoftMuonTagInfos")
)


process.ic5PFResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2L3Residual')
)


process.kt4CaloJetsL1FastL2L3 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("kt4CaloL1FastL2L3Corrector"),
    src = cms.InputTag("kt4CaloJets")
)


process.kt4CaloJetsL1FastL2L3Residual = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("kt4CaloL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("kt4CaloJets")
)


process.kt4CaloJetsL1L2L3 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("kt4CaloL1L2L3Corrector"),
    src = cms.InputTag("kt4CaloJets")
)


process.kt4CaloJetsL1L2L3Residual = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("kt4CaloL1L2L3ResidualCorrector"),
    src = cms.InputTag("kt4CaloJets")
)


process.kt4CaloJetsL2L3 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("kt4CaloL2L3Corrector"),
    src = cms.InputTag("kt4CaloJets")
)


process.kt4CaloJetsL2L3Residual = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("kt4CaloL2L3ResidualCorrector"),
    src = cms.InputTag("kt4CaloJets")
)


process.kt4CaloL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1FastjetCorrector", "kt4CaloL2RelativeCorrector", "kt4CaloL3AbsoluteCorrector")
)


process.kt4CaloL1FastL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt4CaloL1OffsetCorrector", "kt4CaloL2RelativeCorrector", "kt4CaloL3AbsoluteCorrector", "kt4CaloL6SLBCorrector")
)


process.kt4CaloL1FastL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt4CaloL1FastjetCorrector", "kt4CaloL2RelativeCorrector", "kt4CaloL3AbsoluteCorrector", "kt4CaloResidualCorrector")
)


process.kt4CaloL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAllCalo")
)


process.kt4CaloL1L2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt4CaloL1OffsetCorrector", "kt4CaloL2RelativeCorrector", "kt4CaloL3AbsoluteCorrector")
)


process.kt4CaloL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt4CaloL1OffsetCorrector", "kt4CaloL2RelativeCorrector", "kt4CaloL3AbsoluteCorrector", "kt4CaloResidualCorrector")
)


process.kt4CaloL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.kt4CaloL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt4CaloL2RelativeCorrector", "kt4CaloL3AbsoluteCorrector")
)


process.kt4CaloL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt4CaloL2RelativeCorrector", "kt4CaloL3AbsoluteCorrector", "kt4CaloL6SLBCorrector")
)


process.kt4CaloL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt4CaloL2RelativeCorrector", "kt4CaloL3AbsoluteCorrector", "kt4CaloResidualCorrector")
)


process.kt4CaloL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('KT4Calo'),
    level = cms.string('L2Relative')
)


process.kt4CaloL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('KT4Calo'),
    level = cms.string('L3Absolute')
)


process.kt4CaloL6SLBCorrector = cms.EDProducer("L6SLBCorrectorProducer",
    addMuonToJet = cms.bool(True),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("kt4CaloJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("kt4CaloJetsSoftMuonTagInfos")
)


process.kt4CaloResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L2L3Residual')
)


process.kt4PFJetsL1FastL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("kt4PFL1FastL2L3Corrector"),
    src = cms.InputTag("kt4PFJets")
)


process.kt4PFJetsL1FastL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("kt4PFL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("kt4PFJets")
)


process.kt4PFJetsL1L2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("kt4PFL1L2L3Corrector"),
    src = cms.InputTag("kt4PFJets")
)


process.kt4PFJetsL1L2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("kt4PFL1L2L3ResidualCorrector"),
    src = cms.InputTag("kt4PFJets")
)


process.kt4PFJetsL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("kt4PFL2L3Corrector"),
    src = cms.InputTag("kt4PFJets")
)


process.kt4PFJetsL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("kt4PFL2L3ResidualCorrector"),
    src = cms.InputTag("kt4PFJets")
)


process.kt4PFL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL1FastjetCorrector", "kt4PFL2RelativeCorrector", "kt4PFL3AbsoluteCorrector")
)


process.kt4PFL1FastL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL1FastjetCorrector", "kt4PFL2RelativeCorrector", "kt4PFL3AbsoluteCorrector", "kt4PFL6SLBCorrector")
)


process.kt4PFL1FastL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt4PFL1FastjetCorrector", "kt4PFL2RelativeCorrector", "kt4PFL3AbsoluteCorrector", "kt4PFResidualCorrector")
)


process.kt4PFL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.kt4PFL1L2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt4PFL1OffsetCorrector", "kt4PFL2RelativeCorrector", "kt4PFL3AbsoluteCorrector")
)


process.kt4PFL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt4PFL1OffsetCorrector", "kt4PFL2RelativeCorrector", "kt4PFL3AbsoluteCorrector", "kt4PFResidualCorrector")
)


process.kt4PFL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.kt4PFL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt4PFL2RelativeCorrector", "kt4PFL3AbsoluteCorrector")
)


process.kt4PFL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt4PFL2RelativeCorrector", "kt4PFL3AbsoluteCorrector", "kt4PFL6SLBCorrector")
)


process.kt4PFL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt4PFL2RelativeCorrector", "kt4PFL3AbsoluteCorrector", "kt4PFResidualCorrector")
)


process.kt4PFL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('KT4PF'),
    level = cms.string('L2Relative')
)


process.kt4PFL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('KT4PF'),
    level = cms.string('L3Absolute')
)


process.kt4PFL6SLBCorrector = cms.EDProducer("L6SLBCorrectorProducer",
    addMuonToJet = cms.bool(False),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("kt4PFJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("kt4PFJetsSoftMuonTagInfos")
)


process.kt4PFResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2L3Residual')
)


process.kt6CaloJetsL1FastL2L3 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("kt6CaloL1FastL2L3Corrector"),
    src = cms.InputTag("kt6CaloJets")
)


process.kt6CaloJetsL1FastL2L3Residual = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("kt6CaloL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("kt6CaloJets")
)


process.kt6CaloJetsL1L2L3 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("kt6CaloL1L2L3Corrector"),
    src = cms.InputTag("kt6CaloJets")
)


process.kt6CaloJetsL1L2L3Residual = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("kt6CaloL1L2L3ResidualCorrector"),
    src = cms.InputTag("kt6CaloJets")
)


process.kt6CaloJetsL2L3 = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("kt6CaloL2L3Corrector"),
    src = cms.InputTag("kt6CaloJets")
)


process.kt6CaloJetsL2L3Residual = cms.EDProducer("CorrectedCaloJetProducer",
    correctors = cms.VInputTag("kt6CaloL2L3ResidualCorrector"),
    src = cms.InputTag("kt6CaloJets")
)


process.kt6CaloL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4CaloL1FastjetCorrector", "kt6CaloL2RelativeCorrector", "kt6CaloL3AbsoluteCorrector")
)


process.kt6CaloL1FastL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt6CaloL1OffsetCorrector", "kt6CaloL2RelativeCorrector", "kt6CaloL3AbsoluteCorrector", "kt6CaloL6SLBCorrector")
)


process.kt6CaloL1FastL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt6CaloL1FastjetCorrector", "kt6CaloL2RelativeCorrector", "kt6CaloL3AbsoluteCorrector", "kt6CaloResidualCorrector")
)


process.kt6CaloL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAllCalo")
)


process.kt6CaloL1L2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt6CaloL1OffsetCorrector", "kt6CaloL2RelativeCorrector", "kt6CaloL3AbsoluteCorrector")
)


process.kt6CaloL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt6CaloL1OffsetCorrector", "kt6CaloL2RelativeCorrector", "kt6CaloL3AbsoluteCorrector", "kt6CaloResidualCorrector")
)


process.kt6CaloL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.kt6CaloL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt6CaloL2RelativeCorrector", "kt6CaloL3AbsoluteCorrector")
)


process.kt6CaloL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt6CaloL2RelativeCorrector", "kt6CaloL3AbsoluteCorrector", "kt6CaloL6SLBCorrector")
)


process.kt6CaloL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt6CaloL2RelativeCorrector", "kt6CaloL3AbsoluteCorrector", "kt6CaloResidualCorrector")
)


process.kt6CaloL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('KT6Calo'),
    level = cms.string('L2Relative')
)


process.kt6CaloL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('KT6Calo'),
    level = cms.string('L3Absolute')
)


process.kt6CaloL6SLBCorrector = cms.EDProducer("L6SLBCorrectorProducer",
    addMuonToJet = cms.bool(True),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("kt6CaloJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("kt6CaloJetsSoftMuonTagInfos")
)


process.kt6CaloResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L2L3Residual')
)


process.kt6PFJetsL1FastL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("kt6PFL1FastL2L3Corrector"),
    src = cms.InputTag("kt6PFJets")
)


process.kt6PFJetsL1FastL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("kt6PFL1FastL2L3ResidualCorrector"),
    src = cms.InputTag("kt6PFJets")
)


process.kt6PFJetsL1L2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("kt6PFL1L2L3Corrector"),
    src = cms.InputTag("kt6PFJets")
)


process.kt6PFJetsL1L2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("kt6PFL1L2L3ResidualCorrector"),
    src = cms.InputTag("kt6PFJets")
)


process.kt6PFJetsL2L3 = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("kt6PFL2L3Corrector"),
    src = cms.InputTag("kt6PFJets")
)


process.kt6PFJetsL2L3Residual = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("kt6PFL2L3ResidualCorrector"),
    src = cms.InputTag("kt6PFJets")
)


process.kt6PFL1FastL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL1FastjetCorrector", "kt6PFL2RelativeCorrector", "kt6PFL3AbsoluteCorrector")
)


process.kt6PFL1FastL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("ak4PFL1FastjetCorrector", "kt6PFL2RelativeCorrector", "kt6PFL3AbsoluteCorrector", "kt6PFL6SLBCorrector")
)


process.kt6PFL1FastL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt6PFL1FastjetCorrector", "kt6PFL2RelativeCorrector", "kt6PFL3AbsoluteCorrector", "kt6PFResidualCorrector")
)


process.kt6PFL1FastjetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.kt6PFL1L2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt6PFL1OffsetCorrector", "kt6PFL2RelativeCorrector", "kt6PFL3AbsoluteCorrector")
)


process.kt6PFL1L2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt6PFL1OffsetCorrector", "kt6PFL2RelativeCorrector", "kt6PFL3AbsoluteCorrector", "kt6PFResidualCorrector")
)


process.kt6PFL1OffsetCorrector = cms.EDProducer("L1OffsetCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.InputTag("offlinePrimaryVertices")
)


process.kt6PFL2L3Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt6PFL2RelativeCorrector", "kt6PFL3AbsoluteCorrector")
)


process.kt6PFL2L3L6Corrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt6PFL2RelativeCorrector", "kt6PFL3AbsoluteCorrector", "kt6PFL6SLBCorrector")
)


process.kt6PFL2L3ResidualCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("kt6PFL2RelativeCorrector", "kt6PFL3AbsoluteCorrector", "kt6PFResidualCorrector")
)


process.kt6PFL2RelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('KT6PF'),
    level = cms.string('L2Relative')
)


process.kt6PFL3AbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('KT6PF'),
    level = cms.string('L3Absolute')
)


process.kt6PFL6SLBCorrector = cms.EDProducer("L6SLBCorrectorProducer",
    addMuonToJet = cms.bool(False),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("kt6PFJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("kt6PFJetsSoftMuonTagInfos")
)


process.kt6PFResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2L3Residual')
)


process.patJetCorrFactorsAK4UpdatedJEC = cms.EDProducer("JetCorrFactorsProducer",
    emf = cms.bool(False),
    extraJPTOffset = cms.string('L1FastJet'),
    flavorType = cms.string('J'),
    levels = cms.vstring(
        'L1FastJet', 
        'L2Relative', 
        'L3Absolute', 
        'L2L3Residual'
    ),
    payload = cms.string('AK4PFchs'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
    rho = cms.InputTag("fixedGridRhoFastjetAll"),
    src = cms.InputTag("slimmedJets"),
    useNPV = cms.bool(True),
    useRho = cms.bool(True)
)


process.patJetCorrFactorsAK8UpdatedJEC = cms.EDProducer("JetCorrFactorsProducer",
    emf = cms.bool(False),
    extraJPTOffset = cms.string('L1FastJet'),
    flavorType = cms.string('J'),
    levels = cms.vstring(
        'L2Relative', 
        'L3Absolute', 
        'L2L3Residual'
    ),
    payload = cms.string('AK8PFPuppi'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
    rho = cms.InputTag("fixedGridRhoFastjetAll"),
    src = cms.InputTag("slimmedJetsAK8"),
    useNPV = cms.bool(True),
    useRho = cms.bool(True)
)


process.pileupJetId = cms.EDProducer("PileupJetIdProducer",
    algos = cms.VPSet(
        cms.PSet(
            JetIdParams = cms.PSet(
                Pt010_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
                Pt010_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
                Pt010_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
                Pt1020_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
                Pt1020_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
                Pt1020_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
                Pt2030_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
                Pt2030_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
                Pt2030_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
                Pt3040_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
                Pt3040_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
                Pt3040_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01),
                Pt4050_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
                Pt4050_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
                Pt4050_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01)
            ),
            cutBased = cms.bool(False),
            etaBinnedWeights = cms.bool(True),
            impactParTkThreshold = cms.double(1.0),
            label = cms.string('full'),
            nEtaBins = cms.int32(4),
            tmvaMethod = cms.string('JetIDMVAHighPt'),
            tmvaSpectators = cms.vstring(
                'jetPt', 
                'jetEta'
            ),
            trainings = cms.VPSet(
                cms.PSet(
                    jEtaMax = cms.double(2.5),
                    jEtaMin = cms.double(0.0),
                    tmvaVariables = cms.vstring(
                        'nvtx', 
                        'dR2Mean', 
                        'nParticles', 
                        'nCharged', 
                        'majW', 
                        'minW', 
                        'frac01', 
                        'frac02', 
                        'frac03', 
                        'frac04', 
                        'ptD', 
                        'beta', 
                        'pull', 
                        'jetR', 
                        'jetRchg'
                    ),
                    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80XvarFix_Eta0to2p5_BDT.weights.xml.gz')
                ), 
                cms.PSet(
                    jEtaMax = cms.double(2.75),
                    jEtaMin = cms.double(2.5),
                    tmvaVariables = cms.vstring(
                        'nvtx', 
                        'dR2Mean', 
                        'nParticles', 
                        'nCharged', 
                        'majW', 
                        'minW', 
                        'frac01', 
                        'frac02', 
                        'frac03', 
                        'frac04', 
                        'ptD', 
                        'beta', 
                        'pull', 
                        'jetR', 
                        'jetRchg'
                    ),
                    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80XvarFix_Eta2p5to2p75_BDT.weights.xml.gz')
                ), 
                cms.PSet(
                    jEtaMax = cms.double(3.0),
                    jEtaMin = cms.double(2.75),
                    tmvaVariables = cms.vstring(
                        'nvtx', 
                        'dR2Mean', 
                        'nParticles', 
                        'nCharged', 
                        'majW', 
                        'minW', 
                        'frac01', 
                        'frac02', 
                        'frac03', 
                        'frac04', 
                        'ptD', 
                        'beta', 
                        'pull', 
                        'jetR', 
                        'jetRchg'
                    ),
                    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80XvarFix_Eta2p75to3_BDT.weights.xml.gz')
                ), 
                cms.PSet(
                    jEtaMax = cms.double(5.0),
                    jEtaMin = cms.double(3.0),
                    tmvaVariables = cms.vstring(
                        'nvtx', 
                        'dR2Mean', 
                        'nParticles', 
                        'majW', 
                        'minW', 
                        'frac01', 
                        'frac02', 
                        'frac03', 
                        'frac04', 
                        'ptD', 
                        'pull', 
                        'jetR'
                    ),
                    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80XvarFix_Eta3to5_BDT.weights.xml.gz')
                )
            ),
            version = cms.int32(-1)
        ), 
        cms.PSet(
            JetIdParams = cms.PSet(
                Pt010_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt010_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt010_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
                Pt010_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.07),
                Pt010_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
                Pt010_RMSTight = cms.vdouble(0.06, 0.07, 0.04, 0.05),
                Pt1020_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt1020_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt1020_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
                Pt1020_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.07),
                Pt1020_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
                Pt1020_RMSTight = cms.vdouble(0.06, 0.07, 0.04, 0.05),
                Pt2030_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt2030_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt2030_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
                Pt2030_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
                Pt2030_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
                Pt2030_RMSTight = cms.vdouble(0.05, 0.07, 0.03, 0.045),
                Pt3040_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt3040_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt3040_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
                Pt3040_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
                Pt3040_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
                Pt3040_RMSTight = cms.vdouble(0.05, 0.06, 0.03, 0.04),
                Pt4050_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt4050_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt4050_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
                Pt4050_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
                Pt4050_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
                Pt4050_RMSTight = cms.vdouble(0.05, 0.06, 0.03, 0.04)
            ),
            cutBased = cms.bool(True),
            impactParTkThreshold = cms.double(1.0),
            label = cms.string('cutbased')
        )
    ),
    applyJec = cms.bool(True),
    inputIsCorrected = cms.bool(False),
    jec = cms.string('AK4PFchs'),
    jetids = cms.InputTag(""),
    jets = cms.InputTag("ak4PFJetsCHS"),
    produceJetIds = cms.bool(True),
    residualsFromTxt = cms.bool(False),
    rho = cms.InputTag("fixedGridRhoFastjetAll"),
    runMvas = cms.bool(True),
    usePuppi = cms.bool(False),
    vertexes = cms.InputTag("offlinePrimaryVertices")
)


process.pileupJetIdCalculator = cms.EDProducer("PileupJetIdProducer",
    algos = cms.VPSet(cms.PSet(
        JetIdParams = cms.PSet(
            Pt010_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
            Pt010_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
            Pt010_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
            Pt010_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.07),
            Pt010_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
            Pt010_RMSTight = cms.vdouble(0.06, 0.07, 0.04, 0.05),
            Pt1020_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
            Pt1020_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
            Pt1020_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
            Pt1020_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.07),
            Pt1020_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
            Pt1020_RMSTight = cms.vdouble(0.06, 0.07, 0.04, 0.05),
            Pt2030_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
            Pt2030_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
            Pt2030_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
            Pt2030_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
            Pt2030_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
            Pt2030_RMSTight = cms.vdouble(0.05, 0.07, 0.03, 0.045),
            Pt3040_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
            Pt3040_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
            Pt3040_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
            Pt3040_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
            Pt3040_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
            Pt3040_RMSTight = cms.vdouble(0.05, 0.06, 0.03, 0.04),
            Pt4050_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
            Pt4050_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
            Pt4050_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
            Pt4050_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
            Pt4050_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
            Pt4050_RMSTight = cms.vdouble(0.05, 0.06, 0.03, 0.04)
        ),
        cutBased = cms.bool(True),
        impactParTkThreshold = cms.double(1.0),
        label = cms.string('cutbased')
    )),
    applyJec = cms.bool(True),
    inputIsCorrected = cms.bool(False),
    jec = cms.string('AK4PFchs'),
    jetids = cms.InputTag(""),
    jets = cms.InputTag("ak4PFJetsCHS"),
    produceJetIds = cms.bool(True),
    residualsFromTxt = cms.bool(False),
    rho = cms.InputTag("fixedGridRhoFastjetAll"),
    runMvas = cms.bool(False),
    usePuppi = cms.bool(False),
    vertexes = cms.InputTag("offlinePrimaryVertices")
)


process.pileupJetIdEvaluator = cms.EDProducer("PileupJetIdProducer",
    algos = cms.VPSet(
        cms.PSet(
            JetIdParams = cms.PSet(
                Pt010_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
                Pt010_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
                Pt010_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
                Pt1020_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
                Pt1020_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
                Pt1020_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
                Pt2030_Loose = cms.vdouble(-0.97, -0.68, -0.53, -0.47),
                Pt2030_Medium = cms.vdouble(0.18, -0.55, -0.42, -0.36),
                Pt2030_Tight = cms.vdouble(0.69, -0.35, -0.26, -0.21),
                Pt3040_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
                Pt3040_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
                Pt3040_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01),
                Pt4050_Loose = cms.vdouble(-0.89, -0.52, -0.38, -0.3),
                Pt4050_Medium = cms.vdouble(0.61, -0.35, -0.23, -0.17),
                Pt4050_Tight = cms.vdouble(0.86, -0.1, -0.05, -0.01)
            ),
            cutBased = cms.bool(False),
            etaBinnedWeights = cms.bool(True),
            impactParTkThreshold = cms.double(1.0),
            label = cms.string('full'),
            nEtaBins = cms.int32(4),
            tmvaMethod = cms.string('JetIDMVAHighPt'),
            tmvaSpectators = cms.vstring(
                'jetPt', 
                'jetEta'
            ),
            trainings = cms.VPSet(
                cms.PSet(
                    jEtaMax = cms.double(2.5),
                    jEtaMin = cms.double(0.0),
                    tmvaVariables = cms.vstring(
                        'nvtx', 
                        'dR2Mean', 
                        'nParticles', 
                        'nCharged', 
                        'majW', 
                        'minW', 
                        'frac01', 
                        'frac02', 
                        'frac03', 
                        'frac04', 
                        'ptD', 
                        'beta', 
                        'pull', 
                        'jetR', 
                        'jetRchg'
                    ),
                    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80XvarFix_Eta0to2p5_BDT.weights.xml.gz')
                ), 
                cms.PSet(
                    jEtaMax = cms.double(2.75),
                    jEtaMin = cms.double(2.5),
                    tmvaVariables = cms.vstring(
                        'nvtx', 
                        'dR2Mean', 
                        'nParticles', 
                        'nCharged', 
                        'majW', 
                        'minW', 
                        'frac01', 
                        'frac02', 
                        'frac03', 
                        'frac04', 
                        'ptD', 
                        'beta', 
                        'pull', 
                        'jetR', 
                        'jetRchg'
                    ),
                    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80XvarFix_Eta2p5to2p75_BDT.weights.xml.gz')
                ), 
                cms.PSet(
                    jEtaMax = cms.double(3.0),
                    jEtaMin = cms.double(2.75),
                    tmvaVariables = cms.vstring(
                        'nvtx', 
                        'dR2Mean', 
                        'nParticles', 
                        'nCharged', 
                        'majW', 
                        'minW', 
                        'frac01', 
                        'frac02', 
                        'frac03', 
                        'frac04', 
                        'ptD', 
                        'beta', 
                        'pull', 
                        'jetR', 
                        'jetRchg'
                    ),
                    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80XvarFix_Eta2p75to3_BDT.weights.xml.gz')
                ), 
                cms.PSet(
                    jEtaMax = cms.double(5.0),
                    jEtaMin = cms.double(3.0),
                    tmvaVariables = cms.vstring(
                        'nvtx', 
                        'dR2Mean', 
                        'nParticles', 
                        'majW', 
                        'minW', 
                        'frac01', 
                        'frac02', 
                        'frac03', 
                        'frac04', 
                        'ptD', 
                        'pull', 
                        'jetR'
                    ),
                    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_80XvarFix_Eta3to5_BDT.weights.xml.gz')
                )
            ),
            version = cms.int32(-1)
        ), 
        cms.PSet(
            JetIdParams = cms.PSet(
                Pt010_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt010_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt010_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
                Pt010_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.07),
                Pt010_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
                Pt010_RMSTight = cms.vdouble(0.06, 0.07, 0.04, 0.05),
                Pt1020_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt1020_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt1020_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
                Pt1020_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.07),
                Pt1020_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
                Pt1020_RMSTight = cms.vdouble(0.06, 0.07, 0.04, 0.05),
                Pt2030_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt2030_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt2030_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
                Pt2030_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
                Pt2030_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
                Pt2030_RMSTight = cms.vdouble(0.05, 0.07, 0.03, 0.045),
                Pt3040_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt3040_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt3040_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
                Pt3040_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
                Pt3040_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
                Pt3040_RMSTight = cms.vdouble(0.05, 0.06, 0.03, 0.04),
                Pt4050_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt4050_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt4050_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
                Pt4050_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
                Pt4050_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
                Pt4050_RMSTight = cms.vdouble(0.05, 0.06, 0.03, 0.04)
            ),
            cutBased = cms.bool(True),
            impactParTkThreshold = cms.double(1.0),
            label = cms.string('cutbased')
        )
    ),
    applyJec = cms.bool(True),
    inputIsCorrected = cms.bool(False),
    jec = cms.string('AK4PFchs'),
    jetids = cms.InputTag("pileupJetIdCalculator"),
    jets = cms.InputTag("ak4PFJetsCHS"),
    produceJetIds = cms.bool(False),
    residualsFromTxt = cms.bool(False),
    rho = cms.InputTag("fixedGridRhoFastjetAll"),
    runMvas = cms.bool(True),
    usePuppi = cms.bool(False),
    vertexes = cms.InputTag("offlinePrimaryVertices")
)


process.pileupJetIdUpdated = cms.EDProducer("PileupJetIdProducer",
    algos = cms.VPSet(
        cms.PSet(
            JetIdParams = cms.PSet(
                Pt010_Loose = cms.vdouble(0.71, -0.32, -0.3, -0.22),
                Pt010_Medium = cms.vdouble(0.2, -0.56, -0.43, -0.38),
                Pt010_Tight = cms.vdouble(-0.95, -0.7, -0.52, -0.49),
                Pt1020_Loose = cms.vdouble(0.71, -0.32, -0.3, -0.22),
                Pt1020_Medium = cms.vdouble(0.2, -0.56, -0.43, -0.38),
                Pt1020_Tight = cms.vdouble(-0.95, -0.7, -0.52, -0.49),
                Pt2030_Loose = cms.vdouble(0.87, -0.08, -0.16, -0.12),
                Pt2030_Medium = cms.vdouble(0.62, -0.39, -0.32, -0.29),
                Pt2030_Tight = cms.vdouble(-0.9, -0.57, -0.43, -0.42),
                Pt3040_Loose = cms.vdouble(0.94, 0.24, 0.05, 0.1),
                Pt3040_Medium = cms.vdouble(0.86, -0.1, -0.15, -0.08),
                Pt3040_Tight = cms.vdouble(-0.71, -0.36, -0.29, -0.23),
                Pt4050_Loose = cms.vdouble(0.97, 0.48, 0.26, 0.29),
                Pt4050_Medium = cms.vdouble(0.93, 0.19, 0.04, 0.12),
                Pt4050_Tight = cms.vdouble(-0.42, -0.09, -0.14, -0.02)
            ),
            cutBased = cms.bool(False),
            etaBinnedWeights = cms.bool(True),
            impactParTkThreshold = cms.double(1.0),
            label = cms.string('full'),
            nEtaBins = cms.int32(4),
            tmvaMethod = cms.string('JetIDMVAHighPt'),
            tmvaSpectators = cms.vstring(
                'jetPt', 
                'jetEta'
            ),
            trainings = cms.VPSet(
                cms.PSet(
                    jEtaMax = cms.double(2.5),
                    jEtaMin = cms.double(0.0),
                    tmvaVariables = cms.vstring(
                        'nvtx', 
                        'beta', 
                        'dR2Mean', 
                        'frac01', 
                        'frac02', 
                        'frac03', 
                        'frac04', 
                        'majW', 
                        'minW', 
                        'jetR', 
                        'jetRchg', 
                        'nParticles', 
                        'nCharged', 
                        'ptD', 
                        'pull'
                    ),
                    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL16_Eta0p0To2p5_chs_BDT.weights.xml.gz')
                ), 
                cms.PSet(
                    jEtaMax = cms.double(2.75),
                    jEtaMin = cms.double(2.5),
                    tmvaVariables = cms.vstring(
                        'nvtx', 
                        'beta', 
                        'dR2Mean', 
                        'frac01', 
                        'frac02', 
                        'frac03', 
                        'frac04', 
                        'majW', 
                        'minW', 
                        'jetR', 
                        'jetRchg', 
                        'nParticles', 
                        'nCharged', 
                        'ptD', 
                        'pull'
                    ),
                    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL16_Eta2p5To2p75_chs_BDT.weights.xml.gz')
                ), 
                cms.PSet(
                    jEtaMax = cms.double(3.0),
                    jEtaMin = cms.double(2.75),
                    tmvaVariables = cms.vstring(
                        'nvtx', 
                        'beta', 
                        'dR2Mean', 
                        'frac01', 
                        'frac02', 
                        'frac03', 
                        'frac04', 
                        'majW', 
                        'minW', 
                        'jetR', 
                        'jetRchg', 
                        'nParticles', 
                        'nCharged', 
                        'ptD', 
                        'pull'
                    ),
                    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL16_Eta2p75To3p0_chs_BDT.weights.xml.gz')
                ), 
                cms.PSet(
                    jEtaMax = cms.double(5.0),
                    jEtaMin = cms.double(3.0),
                    tmvaVariables = cms.vstring(
                        'nvtx', 
                        'dR2Mean', 
                        'frac01', 
                        'frac02', 
                        'frac03', 
                        'frac04', 
                        'majW', 
                        'minW', 
                        'jetR', 
                        'nParticles', 
                        'ptD', 
                        'pull'
                    ),
                    tmvaWeights = cms.FileInPath('RecoJets/JetProducers/data/pileupJetId_UL16_Eta3p0To5p0_chs_BDT.weights.xml.gz')
                )
            ),
            version = cms.int32(-1)
        ), 
        cms.PSet(
            JetIdParams = cms.PSet(
                Pt010_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt010_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt010_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
                Pt010_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.07),
                Pt010_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
                Pt010_RMSTight = cms.vdouble(0.06, 0.07, 0.04, 0.05),
                Pt1020_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt1020_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt1020_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
                Pt1020_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.07),
                Pt1020_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
                Pt1020_RMSTight = cms.vdouble(0.06, 0.07, 0.04, 0.05),
                Pt2030_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt2030_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt2030_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
                Pt2030_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
                Pt2030_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
                Pt2030_RMSTight = cms.vdouble(0.05, 0.07, 0.03, 0.045),
                Pt3040_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt3040_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt3040_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
                Pt3040_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
                Pt3040_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
                Pt3040_RMSTight = cms.vdouble(0.05, 0.06, 0.03, 0.04),
                Pt4050_BetaStarLoose = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt4050_BetaStarMedium = cms.vdouble(0.2, 0.3, 999.0, 999.0),
                Pt4050_BetaStarTight = cms.vdouble(0.15, 0.15, 999.0, 999.0),
                Pt4050_RMSLoose = cms.vdouble(0.06, 0.05, 0.05, 0.055),
                Pt4050_RMSMedium = cms.vdouble(0.06, 0.03, 0.03, 0.04),
                Pt4050_RMSTight = cms.vdouble(0.05, 0.06, 0.03, 0.04)
            ),
            cutBased = cms.bool(True),
            impactParTkThreshold = cms.double(1.0),
            label = cms.string('cutbased')
        )
    ),
    applyJec = cms.bool(False),
    inputIsCorrected = cms.bool(True),
    jec = cms.string('AK4PFchs'),
    jetids = cms.InputTag(""),
    jets = cms.InputTag("updatedPatJetsAK4UpdatedJEC"),
    produceJetIds = cms.bool(True),
    residualsFromTxt = cms.bool(False),
    rho = cms.InputTag("fixedGridRhoFastjetAll"),
    runMvas = cms.bool(True),
    usePuppi = cms.bool(False),
    vertexes = cms.InputTag("offlineSlimmedPrimaryVertices")
)


process.prefiringweight = cms.EDProducer("L1PrefiringWeightProducer",
    DataEraECAL = cms.string('UL2016postVFP'),
    DataEraMuon = cms.string('2016postVFP'),
    DoMuons = cms.bool(True),
    JetMaxMuonFraction = cms.double(0.5),
    L1Maps = cms.string('L1PrefiringMaps.root'),
    L1MuonParametrizations = cms.string('L1MuonPrefiringParametriations.root'),
    PrefiringRateSystematicUnctyECAL = cms.double(0.2),
    PrefiringRateSystematicUnctyMuon = cms.double(0.2),
    TheJets = cms.InputTag("updatedPatJetsPileupJetID"),
    TheMuons = cms.InputTag("slimmedMuons"),
    ThePhotons = cms.InputTag("slimmedPhotons"),
    UseJetEMPt = cms.bool(False)
)


process.randomEngineStateProducer = cms.EDProducer("RandomEngineStateProducer")


process.updatedPatJetsAK4UpdatedJEC = cms.EDProducer("PATJetUpdater",
    addBTagInfo = cms.bool(False),
    addDiscriminators = cms.bool(True),
    addJetCorrFactors = cms.bool(True),
    addTagInfos = cms.bool(False),
    discriminatorSources = cms.VInputTag(),
    jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsAK4UpdatedJEC")),
    jetSource = cms.InputTag("slimmedJets"),
    printWarning = cms.bool(False),
    sort = cms.bool(True),
    tagInfoSources = cms.VInputTag(),
    userData = cms.PSet(
        userCands = cms.PSet(
            src = cms.VInputTag("")
        ),
        userClasses = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFloats = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFunctionLabels = cms.vstring(),
        userFunctions = cms.vstring(),
        userInts = cms.PSet(
            src = cms.VInputTag("")
        )
    )
)


process.updatedPatJetsAK8UpdatedJEC = cms.EDProducer("PATJetUpdater",
    addBTagInfo = cms.bool(False),
    addDiscriminators = cms.bool(True),
    addJetCorrFactors = cms.bool(True),
    addTagInfos = cms.bool(False),
    discriminatorSources = cms.VInputTag(),
    jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsAK8UpdatedJEC")),
    jetSource = cms.InputTag("slimmedJetsAK8"),
    printWarning = cms.bool(False),
    sort = cms.bool(True),
    tagInfoSources = cms.VInputTag(),
    userData = cms.PSet(
        userCands = cms.PSet(
            src = cms.VInputTag("")
        ),
        userClasses = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFloats = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFunctionLabels = cms.vstring(),
        userFunctions = cms.vstring(),
        userInts = cms.PSet(
            src = cms.VInputTag("")
        )
    )
)


process.updatedPatJetsPileupJetID = cms.EDProducer("PATJetUpdater",
    addBTagInfo = cms.bool(False),
    addDiscriminators = cms.bool(True),
    addJetCorrFactors = cms.bool(False),
    addTagInfos = cms.bool(False),
    discriminatorSources = cms.VInputTag(),
    jetCorrFactorsSource = cms.VInputTag(cms.InputTag("updatedPatJetCorrFactors")),
    jetSource = cms.InputTag("updatedPatJetsAK4UpdatedJEC"),
    printWarning = cms.bool(True),
    sort = cms.bool(True),
    tagInfoSources = cms.VInputTag(),
    userData = cms.PSet(
        userCands = cms.PSet(
            src = cms.VInputTag("")
        ),
        userClasses = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFloats = cms.PSet(
            src = cms.VInputTag("")
        ),
        userFunctionLabels = cms.vstring(),
        userFunctions = cms.vstring(),
        userInts = cms.PSet(
            src = cms.VInputTag("pileupJetIdUpdated:fullId")
        )
    )
)


process.leptonVeto = cms.EDFilter("leptonVeto",
    electronCollection = cms.InputTag("slimmedElectrons"),
    metCollection = cms.InputTag("slimmedMETs"),
    muonCollection = cms.InputTag("slimmedMuons"),
    tauCollection = cms.InputTag("slimmedTaus")
)


process.selectedUpdatedPatJetsAK4UpdatedJEC = cms.EDFilter("PATJetSelector",
    cut = cms.string(''),
    cutLoose = cms.string(''),
    nLoose = cms.uint32(0),
    src = cms.InputTag("updatedPatJetsAK4UpdatedJEC")
)


process.selectedUpdatedPatJetsAK8UpdatedJEC = cms.EDFilter("PATJetSelector",
    cut = cms.string(''),
    cutLoose = cms.string(''),
    nLoose = cms.uint32(0),
    src = cms.InputTag("updatedPatJetsAK8UpdatedJEC")
)


process.selectedUpdatedPatJetsPileupJetID = cms.EDFilter("PATJetSelector",
    cut = cms.string(''),
    cutLoose = cms.string(''),
    nLoose = cms.uint32(0),
    src = cms.InputTag("updatedPatJetsPileupJetID")
)


process.clusteringAnalyzerAll_nom = cms.EDAnalyzer("clusteringAnalyzerAll",
    BESTname = cms.string('BESTGraph'),
    BESTpath = cms.FileInPath('data/BEST_models/constantgraph_2016.pb'),
    BESTscale = cms.FileInPath('data/BESTScalerParameters_all_mass_2016.txt'),
    JECUncert_AK4_path = cms.FileInPath('data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK4PFchs.txt'),
    JECUncert_AK8_path = cms.FileInPath('data/JEC/2016_UL_postAPV/data/Summer19UL16_RunFGH_V7_DATA_Uncertainty_AK8PFPuppi.txt'),
    PUfile_path = cms.FileInPath('data/POG/LUM/2016postVFP_UL/puWeights.json'),
    bits = cms.InputTag("TriggerResults","","HLT"),
    doPDF = cms.bool(False),
    doPUID = cms.bool(True),
    electronCollection = cms.InputTag("slimmedElectrons"),
    fatJetCollection = cms.InputTag("updatedPatJetsAK8UpdatedJEC"),
    genEventInfoTag = cms.InputTag("generator"),
    includeAllBranches = cms.bool(False),
    jetCollection = cms.InputTag("updatedPatJetsPileupJetID"),
    jetVetoMapFile = cms.FileInPath('data/jetVetoMaps/hotjets-UL16.root'),
    jetVetoMapName = cms.string('h2hot_ul16_plus_hbm2_hbp12_qie11'),
    lheEventInfoTag = cms.InputTag("externalLHEProducer"),
    metCollection = cms.InputTag("slimmedMETs"),
    muonCollection = cms.InputTag("slimmedMuons"),
    pileupCollection = cms.InputTag("slimmedAddPileupInfo"),
    runSideband = cms.bool(False),
    runType = cms.string('dataF'),
    slimmedSelection = cms.bool(True),
    systematicType = cms.string('nom'),
    tauCollection = cms.InputTag("slimmedTaus"),
    triggers = cms.string('HLT_PFHT900_v'),
    verbose = cms.bool(False),
    year = cms.string('2016')
)


process.content = cms.EDAnalyzer("EventContentAnalyzer")


process.DQMStore = cms.Service("DQMStore",
    LSbasedMode = cms.untracked.bool(False),
    collateHistograms = cms.untracked.bool(False),
    enableMultiThread = cms.untracked.bool(False),
    forceResetOnBeginLumi = cms.untracked.bool(False),
    referenceFileName = cms.untracked.string(''),
    saveByLumi = cms.untracked.bool(False),
    verbose = cms.untracked.int32(0),
    verboseQT = cms.untracked.int32(0)
)


process.MessageLogger = cms.Service("MessageLogger",
    FrameworkJobReport = cms.untracked.PSet(
        FwkJob = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000),
            optionalPSet = cms.untracked.bool(True)
        ),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        optionalPSet = cms.untracked.bool(True)
    ),
    categories = cms.untracked.vstring(
        'FwkJob', 
        'FwkReport', 
        'FwkSummary', 
        'Root_NoDictionary'
    ),
    cerr = cms.untracked.PSet(
        FwkJob = cms.untracked.PSet(
            limit = cms.untracked.int32(0),
            optionalPSet = cms.untracked.bool(True)
        ),
        FwkReport = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000),
            optionalPSet = cms.untracked.bool(True),
            reportEvery = cms.untracked.int32(1000)
        ),
        FwkSummary = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000),
            optionalPSet = cms.untracked.bool(True),
            reportEvery = cms.untracked.int32(1)
        ),
        INFO = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        Root_NoDictionary = cms.untracked.PSet(
            limit = cms.untracked.int32(0),
            optionalPSet = cms.untracked.bool(True)
        ),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000)
        ),
        noTimeStamps = cms.untracked.bool(False),
        optionalPSet = cms.untracked.bool(True),
        threshold = cms.untracked.string('INFO')
    ),
    cerr_stats = cms.untracked.PSet(
        optionalPSet = cms.untracked.bool(True),
        output = cms.untracked.string('cerr'),
        threshold = cms.untracked.string('WARNING')
    ),
    cout = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    debugModules = cms.untracked.vstring(),
    debugs = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    default = cms.untracked.PSet(

    ),
    destinations = cms.untracked.vstring(
        'warnings', 
        'errors', 
        'infos', 
        'debugs', 
        'cout', 
        'cerr'
    ),
    errors = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    ),
    fwkJobReports = cms.untracked.vstring('FrameworkJobReport'),
    infos = cms.untracked.PSet(
        Root_NoDictionary = cms.untracked.PSet(
            limit = cms.untracked.int32(0),
            optionalPSet = cms.untracked.bool(True)
        ),
        optionalPSet = cms.untracked.bool(True),
        placeholder = cms.untracked.bool(True)
    ),
    statistics = cms.untracked.vstring('cerr_stats'),
    suppressDebug = cms.untracked.vstring(),
    suppressInfo = cms.untracked.vstring(),
    suppressWarning = cms.untracked.vstring(),
    warnings = cms.untracked.PSet(
        placeholder = cms.untracked.bool(True)
    )
)


process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    CTPPSFastRecHits = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(1357987)
    ),
    LHCTransport = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(87654321)
    ),
    MuonSimHits = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(987346)
    ),
    VtxSmeared = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(98765432)
    ),
    ecalPreshowerRecHit = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(6541321)
    ),
    ecalRecHit = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(654321)
    ),
    externalLHEProducer = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(234567)
    ),
    famosPileUp = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(918273)
    ),
    fastSimProducer = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(13579)
    ),
    fastTrackerRecHits = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(24680)
    ),
    g4SimHits = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(11)
    ),
    generator = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(123456789)
    ),
    hbhereco = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(541321)
    ),
    hfreco = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(541321)
    ),
    hiSignal = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(123456789)
    ),
    hiSignalG4SimHits = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(11)
    ),
    hiSignalLHCTransport = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(88776655)
    ),
    horeco = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(541321)
    ),
    l1ParamMuons = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(6453209)
    ),
    mix = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(12345)
    ),
    mixData = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(12345)
    ),
    mixGenPU = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(918273)
    ),
    mixRecoTracks = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(918273)
    ),
    mixSimCaloHits = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(918273)
    ),
    paramMuons = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(54525)
    ),
    saveFileName = cms.untracked.string(''),
    simBeamSpotFilter = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(87654321)
    ),
    simMuonCSCDigis = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(11223344)
    ),
    simMuonDTDigis = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(1234567)
    ),
    simMuonRPCDigis = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(1234567)
    ),
    simSiStripDigiSimLink = cms.PSet(
        engineName = cms.untracked.string('MixMaxRng'),
        initialSeed = cms.untracked.uint32(1234567)
    )
)


process.TFileService = cms.Service("TFileService",
    fileName = cms.string('clusteringAnalyzer_dataF_2016_nom_output.root')
)


process.CastorDbProducer = cms.ESProducer("CastorDbProducer",
    appendToDataLabel = cms.string('')
)


process.EcalLaserCorrectionService = cms.ESProducer("EcalLaserCorrectionService")


process.SiStripRecHitMatcherESProducer = cms.ESProducer("SiStripRecHitMatcherESProducer",
    ComponentName = cms.string('StandardMatcher'),
    NSigmaInside = cms.double(3.0),
    PreFilter = cms.bool(False)
)


process.StripCPEfromTrackAngleESProducer = cms.ESProducer("StripCPEESProducer",
    ComponentName = cms.string('StripCPEfromTrackAngle'),
    ComponentType = cms.string('StripCPEfromTrackAngle'),
    parameters = cms.PSet(
        mLC_P0 = cms.double(-0.326),
        mLC_P1 = cms.double(0.618),
        mLC_P2 = cms.double(0.3),
        mTEC_P0 = cms.double(-1.885),
        mTEC_P1 = cms.double(0.471),
        mTIB_P0 = cms.double(-0.742),
        mTIB_P1 = cms.double(0.202),
        mTID_P0 = cms.double(-1.427),
        mTID_P1 = cms.double(0.433),
        mTOB_P0 = cms.double(-1.026),
        mTOB_P1 = cms.double(0.253),
        maxChgOneMIP = cms.double(6000.0),
        useLegacyError = cms.bool(False)
    )
)


process.ak10PFCHSL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK10PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak10PFCHSL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak10PFCHSL1Fastjet', 
        'ak10PFCHSL2Relative', 
        'ak10PFCHSL3Absolute', 
        'ak10PFCHSResidual'
    )
)


process.ak10PFCHSL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak10PFCHSL1Offset', 
        'ak10PFCHSL2Relative', 
        'ak10PFCHSL3Absolute', 
        'ak10PFCHSResidual'
    )
)


process.ak10PFCHSL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK10PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak10PFCHSL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak10PFCHSL2Relative', 
        'ak10PFCHSL3Absolute'
    )
)


process.ak10PFCHSL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak10PFCHSL2Relative', 
        'ak10PFCHSL3Absolute', 
        'ak10PFCHSResidual'
    )
)


process.ak10PFCHSL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK10PFchs'),
    level = cms.string('L2Relative')
)


process.ak10PFCHSL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK10PFchs'),
    level = cms.string('L3Absolute')
)


process.ak10PFCHSResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK10PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak10PFL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK10PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak10PFL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak10PFL1Fastjet', 
        'ak10PFL2Relative', 
        'ak10PFL3Absolute', 
        'ak10PFResidual'
    )
)


process.ak10PFL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak10PFL1Offset', 
        'ak10PFL2Relative', 
        'ak10PFL3Absolute', 
        'ak10PFResidual'
    )
)


process.ak10PFL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK10PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak10PFL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak10PFL2Relative', 
        'ak10PFL3Absolute'
    )
)


process.ak10PFL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak10PFL2Relative', 
        'ak10PFL3Absolute', 
        'ak10PFResidual'
    )
)


process.ak10PFL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK10PF'),
    level = cms.string('L2Relative')
)


process.ak10PFL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK10PF'),
    level = cms.string('L3Absolute')
)


process.ak10PFResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK10PF'),
    level = cms.string('L2L3Residual')
)


process.ak1PFCHSL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK1PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak1PFCHSL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak1PFCHSL1Fastjet', 
        'ak1PFCHSL2Relative', 
        'ak1PFCHSL3Absolute', 
        'ak1PFCHSResidual'
    )
)


process.ak1PFCHSL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak1PFCHSL1Offset', 
        'ak1PFCHSL2Relative', 
        'ak1PFCHSL3Absolute', 
        'ak1PFCHSResidual'
    )
)


process.ak1PFCHSL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK1PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak1PFCHSL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak1PFCHSL2Relative', 
        'ak1PFCHSL3Absolute'
    )
)


process.ak1PFCHSL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak1PFCHSL2Relative', 
        'ak1PFCHSL3Absolute', 
        'ak1PFCHSResidual'
    )
)


process.ak1PFCHSL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK1PFchs'),
    level = cms.string('L2Relative')
)


process.ak1PFCHSL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK1PFchs'),
    level = cms.string('L3Absolute')
)


process.ak1PFCHSResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK1PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak1PFL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK1PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak1PFL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak1PFL1Fastjet', 
        'ak1PFL2Relative', 
        'ak1PFL3Absolute', 
        'ak1PFResidual'
    )
)


process.ak1PFL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak1PFL1Offset', 
        'ak1PFL2Relative', 
        'ak1PFL3Absolute', 
        'ak1PFResidual'
    )
)


process.ak1PFL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK1PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak1PFL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak1PFL2Relative', 
        'ak1PFL3Absolute'
    )
)


process.ak1PFL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak1PFL2Relative', 
        'ak1PFL3Absolute', 
        'ak1PFResidual'
    )
)


process.ak1PFL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK1PF'),
    level = cms.string('L2Relative')
)


process.ak1PFL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK1PF'),
    level = cms.string('L3Absolute')
)


process.ak1PFResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK1PF'),
    level = cms.string('L2L3Residual')
)


process.ak2PFCHSL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK2PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak2PFCHSL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak2PFCHSL1Fastjet', 
        'ak2PFCHSL2Relative', 
        'ak2PFCHSL3Absolute', 
        'ak2PFCHSResidual'
    )
)


process.ak2PFCHSL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak2PFCHSL1Offset', 
        'ak2PFCHSL2Relative', 
        'ak2PFCHSL3Absolute', 
        'ak2PFCHSResidual'
    )
)


process.ak2PFCHSL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK2PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak2PFCHSL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak2PFCHSL2Relative', 
        'ak2PFCHSL3Absolute'
    )
)


process.ak2PFCHSL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak2PFCHSL2Relative', 
        'ak2PFCHSL3Absolute', 
        'ak2PFCHSResidual'
    )
)


process.ak2PFCHSL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK2PFchs'),
    level = cms.string('L2Relative')
)


process.ak2PFCHSL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK2PFchs'),
    level = cms.string('L3Absolute')
)


process.ak2PFCHSResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK2PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak2PFL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK2PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak2PFL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak2PFL1Fastjet', 
        'ak2PFL2Relative', 
        'ak2PFL3Absolute', 
        'ak2PFResidual'
    )
)


process.ak2PFL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak2PFL1Offset', 
        'ak2PFL2Relative', 
        'ak2PFL3Absolute', 
        'ak2PFResidual'
    )
)


process.ak2PFL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK2PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak2PFL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak2PFL2Relative', 
        'ak2PFL3Absolute'
    )
)


process.ak2PFL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak2PFL2Relative', 
        'ak2PFL3Absolute', 
        'ak2PFResidual'
    )
)


process.ak2PFL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK2PF'),
    level = cms.string('L2Relative')
)


process.ak2PFL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK2PF'),
    level = cms.string('L3Absolute')
)


process.ak2PFResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK2PF'),
    level = cms.string('L2L3Residual')
)


process.ak3PFCHSL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK3PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak3PFCHSL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak3PFCHSL1Fastjet', 
        'ak3PFCHSL2Relative', 
        'ak3PFCHSL3Absolute', 
        'ak3PFCHSResidual'
    )
)


process.ak3PFCHSL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak3PFCHSL1Offset', 
        'ak3PFCHSL2Relative', 
        'ak3PFCHSL3Absolute', 
        'ak3PFCHSResidual'
    )
)


process.ak3PFCHSL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK3PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak3PFCHSL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak3PFCHSL2Relative', 
        'ak3PFCHSL3Absolute'
    )
)


process.ak3PFCHSL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak3PFCHSL2Relative', 
        'ak3PFCHSL3Absolute', 
        'ak3PFCHSResidual'
    )
)


process.ak3PFCHSL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK3PFchs'),
    level = cms.string('L2Relative')
)


process.ak3PFCHSL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK3PFchs'),
    level = cms.string('L3Absolute')
)


process.ak3PFCHSResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK3PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak3PFL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK3PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak3PFL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak3PFL1Fastjet', 
        'ak3PFL2Relative', 
        'ak3PFL3Absolute', 
        'ak3PFResidual'
    )
)


process.ak3PFL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak3PFL1Offset', 
        'ak3PFL2Relative', 
        'ak3PFL3Absolute', 
        'ak3PFResidual'
    )
)


process.ak3PFL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK3PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak3PFL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak3PFL2Relative', 
        'ak3PFL3Absolute'
    )
)


process.ak3PFL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak3PFL2Relative', 
        'ak3PFL3Absolute', 
        'ak3PFResidual'
    )
)


process.ak3PFL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK3PF'),
    level = cms.string('L2Relative')
)


process.ak3PFL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK3PF'),
    level = cms.string('L3Absolute')
)


process.ak3PFResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK3PF'),
    level = cms.string('L2L3Residual')
)


process.ak4CaloL1FastL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4CaloL1Fastjet', 
        'ak4CaloL2Relative', 
        'ak4CaloL3Absolute'
    )
)


process.ak4CaloL1FastL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4CaloL1Fastjet', 
        'ak4CaloL2Relative', 
        'ak4CaloL3Absolute', 
        'ak4CaloL6SLB'
    )
)


process.ak4CaloL1FastL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4CaloL1Fastjet', 
        'ak4CaloL2Relative', 
        'ak4CaloL3Absolute', 
        'ak4CaloResidual'
    )
)


process.ak4CaloL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAllCalo")
)


process.ak4CaloL1L2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4CaloL1Offset', 
        'ak4CaloL2Relative', 
        'ak4CaloL3Absolute'
    )
)


process.ak4CaloL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4CaloL1Offset', 
        'ak4CaloL2Relative', 
        'ak4CaloL3Absolute', 
        'ak4CaloResidual'
    )
)


process.ak4CaloL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak4CaloL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4CaloL2Relative', 
        'ak4CaloL3Absolute'
    )
)


process.ak4CaloL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4CaloL2Relative', 
        'ak4CaloL3Absolute', 
        'ak4CaloL6SLB'
    )
)


process.ak4CaloL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4CaloL2Relative', 
        'ak4CaloL3Absolute', 
        'ak4CaloResidual'
    )
)


process.ak4CaloL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L2Relative')
)


process.ak4CaloL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L3Absolute')
)


process.ak4CaloL6SLB = cms.ESProducer("L6SLBCorrectionESProducer",
    addMuonToJet = cms.bool(True),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("ak4CaloJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("ak4CaloJetsSoftMuonTagInfos")
)


process.ak4CaloResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK5Calo'),
    level = cms.string('L2L3Residual')
)


process.ak4JPTL1FastL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4L1JPTFastjet', 
        'ak4JPTL2Relative', 
        'ak4JPTL3Absolute'
    )
)


process.ak4JPTL1FastL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4L1JPTFastjet', 
        'ak4JPTL2Relative', 
        'ak4JPTL3Absolute', 
        'ak4JPTResidual'
    )
)


process.ak4JPTL1L2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4L1JPTOffset', 
        'ak4JPTL2Relative', 
        'ak4JPTL3Absolute'
    )
)


process.ak4JPTL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4L1JPTOffset', 
        'ak4JPTL2Relative', 
        'ak4JPTL3Absolute', 
        'ak4JPTResidual'
    )
)


process.ak4JPTL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK4JPT'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak4JPTL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4L1JPTOffset', 
        'ak4JPTL2Relative', 
        'ak4JPTL3Absolute'
    )
)


process.ak4JPTL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4L1JPTOffset', 
        'ak4JPTL2Relative', 
        'ak4JPTL3Absolute', 
        'ak4JPTResidual'
    )
)


process.ak4JPTL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK4JPT'),
    level = cms.string('L2Relative')
)


process.ak4JPTL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK4JPT'),
    level = cms.string('L3Absolute')
)


process.ak4JPTResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK4JPT'),
    level = cms.string('L2L3Residual')
)


process.ak4L1JPTFastjet = cms.ESProducer("L1JPTOffsetCorrectionESProducer",
    algorithm = cms.string('AK4JPT'),
    level = cms.string('L1JPTOffset'),
    offsetService = cms.string('ak4CaloL1Fastjet')
)


process.ak4L1JPTOffset = cms.ESProducer("L1JPTOffsetCorrectionESProducer",
    algorithm = cms.string('AK4JPT'),
    level = cms.string('L1JPTOffset'),
    offsetService = cms.string('ak4CaloL1Offset')
)


process.ak4PFCHSL1FastL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFCHSL1Fastjet', 
        'ak4PFCHSL2Relative', 
        'ak4PFCHSL3Absolute'
    )
)


process.ak4PFCHSL1FastL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFCHSL1Fastjet', 
        'ak4PFCHSL2Relative', 
        'ak4PFCHSL3Absolute', 
        'ak4PFCHSResidual'
    )
)


process.ak4PFCHSL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak4PFCHSL1L2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFCHSL1Offset', 
        'ak4PFCHSL2Relative', 
        'ak4PFCHSL3Absolute'
    )
)


process.ak4PFCHSL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFCHSL1Offset', 
        'ak4PFCHSL2Relative', 
        'ak4PFCHSL3Absolute', 
        'ak4PFCHSResidual'
    )
)


process.ak4PFCHSL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak4PFCHSL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFCHSL2Relative', 
        'ak4PFCHSL3Absolute'
    )
)


process.ak4PFCHSL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFCHSL2Relative', 
        'ak4PFCHSL3Absolute', 
        'ak4PFCHSResidual'
    )
)


process.ak4PFCHSL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L2Relative')
)


process.ak4PFCHSL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L3Absolute')
)


process.ak4PFCHSResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK4PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak4PFL1FastL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL1Fastjet', 
        'ak4PFL2Relative', 
        'ak4PFL3Absolute'
    )
)


process.ak4PFL1FastL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL1Fastjet', 
        'ak4PFL2Relative', 
        'ak4PFL3Absolute', 
        'ak4PFL6SLB'
    )
)


process.ak4PFL1FastL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL1Fastjet', 
        'ak4PFL2Relative', 
        'ak4PFL3Absolute', 
        'ak4PFResidual'
    )
)


process.ak4PFL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak4PFL1L2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL1Offset', 
        'ak4PFL2Relative', 
        'ak4PFL3Absolute'
    )
)


process.ak4PFL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL1Offset', 
        'ak4PFL2Relative', 
        'ak4PFL3Absolute', 
        'ak4PFResidual'
    )
)


process.ak4PFL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak4PFL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL2Relative', 
        'ak4PFL3Absolute'
    )
)


process.ak4PFL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL2Relative', 
        'ak4PFL3Absolute', 
        'ak4PFL6SLB'
    )
)


process.ak4PFL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL2Relative', 
        'ak4PFL3Absolute', 
        'ak4PFResidual'
    )
)


process.ak4PFL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2Relative')
)


process.ak4PFL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L3Absolute')
)


process.ak4PFL6SLB = cms.ESProducer("L6SLBCorrectionESProducer",
    addMuonToJet = cms.bool(False),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("ak4PFJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("ak4PFJetsSoftMuonTagInfos")
)


process.ak4PFResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK4PF'),
    level = cms.string('L2L3Residual')
)


process.ak4TrackL1FastL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4CaloL1Fastjet', 
        'ak4TrackL2Relative', 
        'ak4TrackL3Absolute'
    )
)


process.ak4TrackL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4TrackL2Relative', 
        'ak4TrackL3Absolute'
    )
)


process.ak4TrackL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK5TRK'),
    level = cms.string('L2Relative')
)


process.ak4TrackL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK5TRK'),
    level = cms.string('L3Absolute')
)


process.ak5PFCHSL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK5PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak5PFCHSL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak5PFCHSL1Fastjet', 
        'ak5PFCHSL2Relative', 
        'ak5PFCHSL3Absolute', 
        'ak5PFCHSResidual'
    )
)


process.ak5PFCHSL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak5PFCHSL1Offset', 
        'ak5PFCHSL2Relative', 
        'ak5PFCHSL3Absolute', 
        'ak5PFCHSResidual'
    )
)


process.ak5PFCHSL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK5PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak5PFCHSL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak5PFCHSL2Relative', 
        'ak5PFCHSL3Absolute'
    )
)


process.ak5PFCHSL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak5PFCHSL2Relative', 
        'ak5PFCHSL3Absolute', 
        'ak5PFCHSResidual'
    )
)


process.ak5PFCHSL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK5PFchs'),
    level = cms.string('L2Relative')
)


process.ak5PFCHSL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK5PFchs'),
    level = cms.string('L3Absolute')
)


process.ak5PFCHSResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK5PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak5PFL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK5PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak5PFL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak5PFL1Fastjet', 
        'ak5PFL2Relative', 
        'ak5PFL3Absolute', 
        'ak5PFResidual'
    )
)


process.ak5PFL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak5PFL1Offset', 
        'ak5PFL2Relative', 
        'ak5PFL3Absolute', 
        'ak5PFResidual'
    )
)


process.ak5PFL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK5PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak5PFL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak5PFL2Relative', 
        'ak5PFL3Absolute'
    )
)


process.ak5PFL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak5PFL2Relative', 
        'ak5PFL3Absolute', 
        'ak5PFResidual'
    )
)


process.ak5PFL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK5PF'),
    level = cms.string('L2Relative')
)


process.ak5PFL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK5PF'),
    level = cms.string('L3Absolute')
)


process.ak5PFResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK5PF'),
    level = cms.string('L2L3Residual')
)


process.ak6PFCHSL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK6PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak6PFCHSL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak6PFCHSL1Fastjet', 
        'ak6PFCHSL2Relative', 
        'ak6PFCHSL3Absolute', 
        'ak6PFCHSResidual'
    )
)


process.ak6PFCHSL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak6PFCHSL1Offset', 
        'ak6PFCHSL2Relative', 
        'ak6PFCHSL3Absolute', 
        'ak6PFCHSResidual'
    )
)


process.ak6PFCHSL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK6PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak6PFCHSL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak6PFCHSL2Relative', 
        'ak6PFCHSL3Absolute'
    )
)


process.ak6PFCHSL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak6PFCHSL2Relative', 
        'ak6PFCHSL3Absolute', 
        'ak6PFCHSResidual'
    )
)


process.ak6PFCHSL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK6PFchs'),
    level = cms.string('L2Relative')
)


process.ak6PFCHSL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK6PFchs'),
    level = cms.string('L3Absolute')
)


process.ak6PFCHSResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK6PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak6PFL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK6PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak6PFL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak6PFL1Fastjet', 
        'ak6PFL2Relative', 
        'ak6PFL3Absolute', 
        'ak6PFResidual'
    )
)


process.ak6PFL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak6PFL1Offset', 
        'ak6PFL2Relative', 
        'ak6PFL3Absolute', 
        'ak6PFResidual'
    )
)


process.ak6PFL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK6PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak6PFL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak6PFL2Relative', 
        'ak6PFL3Absolute'
    )
)


process.ak6PFL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak6PFL2Relative', 
        'ak6PFL3Absolute', 
        'ak6PFResidual'
    )
)


process.ak6PFL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK6PF'),
    level = cms.string('L2Relative')
)


process.ak6PFL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK6PF'),
    level = cms.string('L3Absolute')
)


process.ak6PFResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK6PF'),
    level = cms.string('L2L3Residual')
)


process.ak7CaloL1FastL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4CaloL1Fastjet', 
        'ak7CaloL2Relative', 
        'ak7CaloL3Absolute'
    )
)


process.ak7CaloL1FastL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7CaloL1Offset', 
        'ak7CaloL2Relative', 
        'ak7CaloL3Absolute', 
        'ak7CaloL6SLB'
    )
)


process.ak7CaloL1FastL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7CaloL1Fastjet', 
        'ak7CaloL2Relative', 
        'ak7CaloL3Absolute', 
        'ak7CaloResidual'
    )
)


process.ak7CaloL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK7Calo'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAllCalo")
)


process.ak7CaloL1L2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7CaloL1Offset', 
        'ak7CaloL2Relative', 
        'ak7CaloL3Absolute'
    )
)


process.ak7CaloL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7CaloL1Offset', 
        'ak7CaloL2Relative', 
        'ak7CaloL3Absolute', 
        'ak7CaloResidual'
    )
)


process.ak7CaloL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK7Calo'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak7CaloL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7CaloL2Relative', 
        'ak7CaloL3Absolute'
    )
)


process.ak7CaloL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7CaloL2Relative', 
        'ak7CaloL3Absolute', 
        'ak7CaloL6SLB'
    )
)


process.ak7CaloL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7CaloL2Relative', 
        'ak7CaloL3Absolute', 
        'ak7CaloResidual'
    )
)


process.ak7CaloL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK7Calo'),
    level = cms.string('L2Relative')
)


process.ak7CaloL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK7Calo'),
    level = cms.string('L3Absolute')
)


process.ak7CaloL6SLB = cms.ESProducer("L6SLBCorrectionESProducer",
    addMuonToJet = cms.bool(True),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("ak7CaloJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("ak7CaloJetsSoftMuonTagInfos")
)


process.ak7CaloResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK7Calo'),
    level = cms.string('L2L3Residual')
)


process.ak7JPTL1FastL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7L1JPTFastjet', 
        'ak7JPTL2Relative', 
        'ak7JPTL3Absolute'
    )
)


process.ak7JPTL1FastL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7L1JPTFastjet', 
        'ak7JPTL2Relative', 
        'ak7JPTL3Absolute', 
        'ak7JPTResidual'
    )
)


process.ak7JPTL1L2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7L1JPTOffset', 
        'ak7JPTL2Relative', 
        'ak7JPTL3Absolute'
    )
)


process.ak7JPTL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7L1JPTOffset', 
        'ak7JPTL2Relative', 
        'ak7JPTL3Absolute', 
        'ak7JPTResidual'
    )
)


process.ak7JPTL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7L1JPTOffset', 
        'ak7JPTL2Relative', 
        'ak7JPTL3Absolute'
    )
)


process.ak7L1JPTFastjet = cms.ESProducer("L1JPTOffsetCorrectionESProducer",
    algorithm = cms.string('AK7JPT'),
    level = cms.string('L1JPTOffset'),
    offsetService = cms.string('ak7CaloL1Fastjet')
)


process.ak7L1JPTOffset = cms.ESProducer("L1JPTOffsetCorrectionESProducer",
    algorithm = cms.string('AK7JPT'),
    level = cms.string('L1JPTOffset'),
    offsetService = cms.string('ak7CaloL1Offset')
)


process.ak7PFCHSL1FastL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFCHSL1Fastjet', 
        'ak7PFCHSL2Relative', 
        'ak7PFCHSL3Absolute'
    )
)


process.ak7PFCHSL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK7PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak7PFCHSL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7PFCHSL1Fastjet', 
        'ak7PFCHSL2Relative', 
        'ak7PFCHSL3Absolute', 
        'ak7PFCHSResidual'
    )
)


process.ak7PFCHSL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7PFCHSL1Offset', 
        'ak7PFCHSL2Relative', 
        'ak7PFCHSL3Absolute', 
        'ak7PFCHSResidual'
    )
)


process.ak7PFCHSL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK7PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak7PFCHSL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7PFCHSL2Relative', 
        'ak7PFCHSL3Absolute'
    )
)


process.ak7PFCHSL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7PFCHSL2Relative', 
        'ak7PFCHSL3Absolute', 
        'ak7PFCHSResidual'
    )
)


process.ak7PFCHSL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK7PFchs'),
    level = cms.string('L2Relative')
)


process.ak7PFCHSL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK7PFchs'),
    level = cms.string('L3Absolute')
)


process.ak7PFCHSResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK7PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak7PFL1FastL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL1Fastjet', 
        'ak7PFL2Relative', 
        'ak7PFL3Absolute'
    )
)


process.ak7PFL1FastL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL1Fastjet', 
        'ak7PFL2Relative', 
        'ak7PFL3Absolute', 
        'ak7PFL6SLB'
    )
)


process.ak7PFL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK7PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak7PFL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7PFL1Fastjet', 
        'ak7PFL2Relative', 
        'ak7PFL3Absolute', 
        'ak7PFResidual'
    )
)


process.ak7PFL1L2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7PFL1Offset', 
        'ak7PFL2Relative', 
        'ak7PFL3Absolute'
    )
)


process.ak7PFL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7PFL1Offset', 
        'ak7PFL2Relative', 
        'ak7PFL3Absolute', 
        'ak7PFResidual'
    )
)


process.ak7PFL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK7PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak7PFL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7PFL2Relative', 
        'ak7PFL3Absolute'
    )
)


process.ak7PFL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7PFL2Relative', 
        'ak7PFL3Absolute', 
        'ak7PFL6SLB'
    )
)


process.ak7PFL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak7PFL2Relative', 
        'ak7PFL3Absolute', 
        'ak7PFResidual'
    )
)


process.ak7PFL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK7PF'),
    level = cms.string('L2Relative')
)


process.ak7PFL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK7PF'),
    level = cms.string('L3Absolute')
)


process.ak7PFL6SLB = cms.ESProducer("L6SLBCorrectionESProducer",
    addMuonToJet = cms.bool(False),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("ak7PFJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("ak7PFJetsSoftMuonTagInfos")
)


process.ak7PFResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK7PF'),
    level = cms.string('L2L3Residual')
)


process.ak8PFCHSL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK8PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak8PFCHSL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak8PFCHSL1Fastjet', 
        'ak8PFCHSL2Relative', 
        'ak8PFCHSL3Absolute', 
        'ak8PFCHSResidual'
    )
)


process.ak8PFCHSL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak8PFCHSL1Offset', 
        'ak8PFCHSL2Relative', 
        'ak8PFCHSL3Absolute', 
        'ak8PFCHSResidual'
    )
)


process.ak8PFCHSL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK8PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak8PFCHSL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak8PFCHSL2Relative', 
        'ak8PFCHSL3Absolute'
    )
)


process.ak8PFCHSL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak8PFCHSL2Relative', 
        'ak8PFCHSL3Absolute', 
        'ak8PFCHSResidual'
    )
)


process.ak8PFCHSL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK8PFchs'),
    level = cms.string('L2Relative')
)


process.ak8PFCHSL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK8PFchs'),
    level = cms.string('L3Absolute')
)


process.ak8PFCHSResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK8PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak8PFL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK8PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak8PFL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak8PFL1Fastjet', 
        'ak8PFL2Relative', 
        'ak8PFL3Absolute', 
        'ak8PFResidual'
    )
)


process.ak8PFL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak8PFL1Offset', 
        'ak8PFL2Relative', 
        'ak8PFL3Absolute', 
        'ak8PFResidual'
    )
)


process.ak8PFL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK8PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak8PFL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak8PFL2Relative', 
        'ak8PFL3Absolute'
    )
)


process.ak8PFL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak8PFL2Relative', 
        'ak8PFL3Absolute', 
        'ak8PFResidual'
    )
)


process.ak8PFL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK8PF'),
    level = cms.string('L2Relative')
)


process.ak8PFL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK8PF'),
    level = cms.string('L3Absolute')
)


process.ak8PFResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK8PF'),
    level = cms.string('L2L3Residual')
)


process.ak9PFCHSL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK9PFchs'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak9PFCHSL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak9PFCHSL1Fastjet', 
        'ak9PFCHSL2Relative', 
        'ak9PFCHSL3Absolute', 
        'ak9PFCHSResidual'
    )
)


process.ak9PFCHSL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak9PFCHSL1Offset', 
        'ak9PFCHSL2Relative', 
        'ak9PFCHSL3Absolute', 
        'ak9PFCHSResidual'
    )
)


process.ak9PFCHSL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK9PFchs'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak9PFCHSL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak9PFCHSL2Relative', 
        'ak9PFCHSL3Absolute'
    )
)


process.ak9PFCHSL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak9PFCHSL2Relative', 
        'ak9PFCHSL3Absolute', 
        'ak9PFCHSResidual'
    )
)


process.ak9PFCHSL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK9PFchs'),
    level = cms.string('L2Relative')
)


process.ak9PFCHSL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK9PFchs'),
    level = cms.string('L3Absolute')
)


process.ak9PFCHSResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK9PFchs'),
    level = cms.string('L2L3Residual')
)


process.ak9PFL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('AK9PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ak9PFL1FastjetL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak9PFL1Fastjet', 
        'ak9PFL2Relative', 
        'ak9PFL3Absolute', 
        'ak9PFResidual'
    )
)


process.ak9PFL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak9PFL1Offset', 
        'ak9PFL2Relative', 
        'ak9PFL3Absolute', 
        'ak9PFResidual'
    )
)


process.ak9PFL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('AK9PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ak9PFL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak9PFL2Relative', 
        'ak9PFL3Absolute'
    )
)


process.ak9PFL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak9PFL2Relative', 
        'ak9PFL3Absolute', 
        'ak9PFResidual'
    )
)


process.ak9PFL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK9PF'),
    level = cms.string('L2Relative')
)


process.ak9PFL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK9PF'),
    level = cms.string('L3Absolute')
)


process.ak9PFResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('AK9PF'),
    level = cms.string('L2L3Residual')
)


process.hcal_db_producer = cms.ESProducer("HcalDbProducer",
    dump = cms.untracked.vstring(''),
    file = cms.untracked.string('')
)


process.ic5CaloL1FastL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4CaloL1Fastjet', 
        'ic5CaloL2Relative', 
        'ic5CaloL3Absolute'
    )
)


process.ic5CaloL1FastL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ic5CaloL1Offset', 
        'ic5CaloL2Relative', 
        'ic5CaloL3Absolute', 
        'ic5CaloL6SLB'
    )
)


process.ic5CaloL1FastL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ic5CaloL1Fastjet', 
        'ic5CaloL2Relative', 
        'ic5CaloL3Absolute', 
        'ic5CaloResidual'
    )
)


process.ic5CaloL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('IC5Calo'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAllCalo")
)


process.ic5CaloL1L2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ic5CaloL1Offset', 
        'ic5CaloL2Relative', 
        'ic5CaloL3Absolute'
    )
)


process.ic5CaloL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ic5CaloL1Offset', 
        'ic5CaloL2Relative', 
        'ic5CaloL3Absolute', 
        'ic5CaloResidual'
    )
)


process.ic5CaloL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('IC5Calo'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ic5CaloL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ic5CaloL2Relative', 
        'ic5CaloL3Absolute'
    )
)


process.ic5CaloL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ic5CaloL2Relative', 
        'ic5CaloL3Absolute', 
        'ic5CaloL6SLB'
    )
)


process.ic5CaloL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ic5CaloL2Relative', 
        'ic5CaloL3Absolute', 
        'ic5CaloResidual'
    )
)


process.ic5CaloL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('IC5Calo'),
    level = cms.string('L2Relative')
)


process.ic5CaloL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('IC5Calo'),
    level = cms.string('L3Absolute')
)


process.ic5CaloL6SLB = cms.ESProducer("L6SLBCorrectionESProducer",
    addMuonToJet = cms.bool(True),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("ic5CaloJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("ic5CaloJetsSoftMuonTagInfos")
)


process.ic5CaloResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('IC5Calo'),
    level = cms.string('L2L3Residual')
)


process.ic5PFL1FastL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL1Fastjet', 
        'ic5PFL2Relative', 
        'ic5PFL3Absolute'
    )
)


process.ic5PFL1FastL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL1Fastjet', 
        'ic5PFL2Relative', 
        'ic5PFL3Absolute', 
        'ic5PFL6SLB'
    )
)


process.ic5PFL1FastL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ic5PFL1Fastjet', 
        'ic5PFL2Relative', 
        'ic5PFL3Absolute', 
        'ic5PFResidual'
    )
)


process.ic5PFL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('IC5PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.ic5PFL1L2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ic5PFL1Offset', 
        'ic5PFL2Relative', 
        'ic5PFL3Absolute'
    )
)


process.ic5PFL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ic5PFL1Offset', 
        'ic5PFL2Relative', 
        'ic5PFL3Absolute', 
        'ic5PFResidual'
    )
)


process.ic5PFL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('IC5PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.ic5PFL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ic5PFL2Relative', 
        'ic5PFL3Absolute'
    )
)


process.ic5PFL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ic5PFL2Relative', 
        'ic5PFL3Absolute', 
        'ic5PFL6SLB'
    )
)


process.ic5PFL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ic5PFL2Relative', 
        'ic5PFL3Absolute', 
        'ic5PFResidual'
    )
)


process.ic5PFL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('IC5PF'),
    level = cms.string('L2Relative')
)


process.ic5PFL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('IC5PF'),
    level = cms.string('L3Absolute')
)


process.ic5PFL6SLB = cms.ESProducer("L6SLBCorrectionESProducer",
    addMuonToJet = cms.bool(False),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("ic5PFJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("ic5PFJetsSoftMuonTagInfos")
)


process.ic5PFResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('IC5PF'),
    level = cms.string('L2L3Residual')
)


process.kt4CaloL1FastL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4CaloL1Fastjet', 
        'kt4CaloL2Relative', 
        'kt4CaloL3Absolute'
    )
)


process.kt4CaloL1FastL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt4CaloL1Offset', 
        'kt4CaloL2Relative', 
        'kt4CaloL3Absolute', 
        'kt4CaloL6SLB'
    )
)


process.kt4CaloL1FastL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt4CaloL1Fastjet', 
        'kt4CaloL2Relative', 
        'kt4CaloL3Absolute', 
        'kt4CaloResidual'
    )
)


process.kt4CaloL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('KT4Calo'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAllCalo")
)


process.kt4CaloL1L2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt4CaloL1Offset', 
        'kt4CaloL2Relative', 
        'kt4CaloL3Absolute'
    )
)


process.kt4CaloL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt4CaloL1Offset', 
        'kt4CaloL2Relative', 
        'kt4CaloL3Absolute', 
        'kt4CaloResidual'
    )
)


process.kt4CaloL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('KT4Calo'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.kt4CaloL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt4CaloL2Relative', 
        'kt4CaloL3Absolute'
    )
)


process.kt4CaloL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt4CaloL2Relative', 
        'kt4CaloL3Absolute', 
        'kt4CaloL6SLB'
    )
)


process.kt4CaloL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt4CaloL2Relative', 
        'kt4CaloL3Absolute', 
        'kt4CaloResidual'
    )
)


process.kt4CaloL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('KT4Calo'),
    level = cms.string('L2Relative')
)


process.kt4CaloL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('KT4Calo'),
    level = cms.string('L3Absolute')
)


process.kt4CaloL6SLB = cms.ESProducer("L6SLBCorrectionESProducer",
    addMuonToJet = cms.bool(True),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("kt4CaloJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("kt4CaloJetsSoftMuonTagInfos")
)


process.kt4CaloResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('KT4Calo'),
    level = cms.string('L2L3Residual')
)


process.kt4PFL1FastL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL1Fastjet', 
        'kt4PFL2Relative', 
        'kt4PFL3Absolute'
    )
)


process.kt4PFL1FastL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL1Fastjet', 
        'kt4PFL2Relative', 
        'kt4PFL3Absolute', 
        'kt4PFL6SLB'
    )
)


process.kt4PFL1FastL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt4PFL1Fastjet', 
        'kt4PFL2Relative', 
        'kt4PFL3Absolute', 
        'kt4PFResidual'
    )
)


process.kt4PFL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('KT4PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.kt4PFL1L2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt4PFL1Offset', 
        'kt4PFL2Relative', 
        'kt4PFL3Absolute'
    )
)


process.kt4PFL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt4PFL1Offset', 
        'kt4PFL2Relative', 
        'kt4PFL3Absolute', 
        'kt4PFResidual'
    )
)


process.kt4PFL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('KT4PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.kt4PFL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt4PFL2Relative', 
        'kt4PFL3Absolute'
    )
)


process.kt4PFL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt4PFL2Relative', 
        'kt4PFL3Absolute', 
        'kt4PFL6SLB'
    )
)


process.kt4PFL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt4PFL2Relative', 
        'kt4PFL3Absolute', 
        'kt4PFResidual'
    )
)


process.kt4PFL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('KT4PF'),
    level = cms.string('L2Relative')
)


process.kt4PFL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('KT4PF'),
    level = cms.string('L3Absolute')
)


process.kt4PFL6SLB = cms.ESProducer("L6SLBCorrectionESProducer",
    addMuonToJet = cms.bool(False),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("kt4PFJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("kt4PFJetsSoftMuonTagInfos")
)


process.kt4PFResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('KT4PF'),
    level = cms.string('L2L3Residual')
)


process.kt6CaloL1FastL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4CaloL1Fastjet', 
        'kt6CaloL2Relative', 
        'kt6CaloL3Absolute'
    )
)


process.kt6CaloL1FastL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt6CaloL1Offset', 
        'kt6CaloL2Relative', 
        'kt6CaloL3Absolute', 
        'kt6CaloL6SLB'
    )
)


process.kt6CaloL1FastL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt6CaloL1Fastjet', 
        'kt6CaloL2Relative', 
        'kt6CaloL3Absolute', 
        'kt6CaloResidual'
    )
)


process.kt6CaloL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('KT6Calo'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAllCalo")
)


process.kt6CaloL1L2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt6CaloL1Offset', 
        'kt6CaloL2Relative', 
        'kt6CaloL3Absolute'
    )
)


process.kt6CaloL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt6CaloL1Offset', 
        'kt6CaloL2Relative', 
        'kt6CaloL3Absolute', 
        'kt6CaloResidual'
    )
)


process.kt6CaloL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('KT6Calo'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.kt6CaloL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt6CaloL2Relative', 
        'kt6CaloL3Absolute'
    )
)


process.kt6CaloL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt6CaloL2Relative', 
        'kt6CaloL3Absolute', 
        'kt6CaloL6SLB'
    )
)


process.kt6CaloL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt6CaloL2Relative', 
        'kt6CaloL3Absolute', 
        'kt6CaloResidual'
    )
)


process.kt6CaloL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('KT6Calo'),
    level = cms.string('L2Relative')
)


process.kt6CaloL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('KT6Calo'),
    level = cms.string('L3Absolute')
)


process.kt6CaloL6SLB = cms.ESProducer("L6SLBCorrectionESProducer",
    addMuonToJet = cms.bool(True),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("kt6CaloJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("kt6CaloJetsSoftMuonTagInfos")
)


process.kt6CaloResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('KT6Calo'),
    level = cms.string('L2L3Residual')
)


process.kt6PFL1FastL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL1Fastjet', 
        'kt6PFL2Relative', 
        'kt6PFL3Absolute'
    )
)


process.kt6PFL1FastL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'ak4PFL1Fastjet', 
        'kt6PFL2Relative', 
        'kt6PFL3Absolute', 
        'kt6PFL6SLB'
    )
)


process.kt6PFL1FastL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt6PFL1Fastjet', 
        'kt6PFL2Relative', 
        'kt6PFL3Absolute', 
        'kt6PFResidual'
    )
)


process.kt6PFL1Fastjet = cms.ESProducer("L1FastjetCorrectionESProducer",
    algorithm = cms.string('KT6PF'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAll")
)


process.kt6PFL1L2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt6PFL1Offset', 
        'kt6PFL2Relative', 
        'kt6PFL3Absolute'
    )
)


process.kt6PFL1L2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt6PFL1Offset', 
        'kt6PFL2Relative', 
        'kt6PFL3Absolute', 
        'kt6PFResidual'
    )
)


process.kt6PFL1Offset = cms.ESProducer("L1OffsetCorrectionESProducer",
    algorithm = cms.string('KT6PF'),
    level = cms.string('L1Offset'),
    minVtxNdof = cms.int32(4),
    vertexCollection = cms.string('offlinePrimaryVertices')
)


process.kt6PFL2L3 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt6PFL2Relative', 
        'kt6PFL3Absolute'
    )
)


process.kt6PFL2L3L6 = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt6PFL2Relative', 
        'kt6PFL3Absolute', 
        'kt6PFL6SLB'
    )
)


process.kt6PFL2L3Residual = cms.ESProducer("JetCorrectionESChain",
    correctors = cms.vstring(
        'kt6PFL2Relative', 
        'kt6PFL3Absolute', 
        'kt6PFResidual'
    )
)


process.kt6PFL2Relative = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('KT6PF'),
    level = cms.string('L2Relative')
)


process.kt6PFL3Absolute = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('KT6PF'),
    level = cms.string('L3Absolute')
)


process.kt6PFL6SLB = cms.ESProducer("L6SLBCorrectionESProducer",
    addMuonToJet = cms.bool(False),
    algorithm = cms.string(''),
    level = cms.string('L6SLB'),
    srcBTagInfoElectron = cms.InputTag("kt6PFJetsSoftElectronTagInfos"),
    srcBTagInfoMuon = cms.InputTag("kt6PFJetsSoftMuonTagInfos")
)


process.kt6PFResidual = cms.ESProducer("LXXXCorrectionESProducer",
    algorithm = cms.string('KT6PF'),
    level = cms.string('L2L3Residual')
)


process.siPixelQualityESProducer = cms.ESProducer("SiPixelQualityESProducer",
    ListOfRecordToMerge = cms.VPSet(
        cms.PSet(
            record = cms.string('SiPixelQualityFromDbRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiPixelDetVOffRcd'),
            tag = cms.string('')
        )
    ),
    siPixelQualityLabel = cms.string('')
)


process.siStripBackPlaneCorrectionDepESProducer = cms.ESProducer("SiStripBackPlaneCorrectionDepESProducer",
    BackPlaneCorrectionDeconvMode = cms.PSet(
        label = cms.untracked.string('deconvolution'),
        record = cms.string('SiStripBackPlaneCorrectionRcd')
    ),
    BackPlaneCorrectionPeakMode = cms.PSet(
        label = cms.untracked.string('peak'),
        record = cms.string('SiStripBackPlaneCorrectionRcd')
    ),
    LatencyRecord = cms.PSet(
        label = cms.untracked.string(''),
        record = cms.string('SiStripLatencyRcd')
    )
)


process.siStripGainESProducer = cms.ESProducer("SiStripGainESProducer",
    APVGain = cms.VPSet(
        cms.PSet(
            Label = cms.untracked.string(''),
            NormalizationFactor = cms.untracked.double(1.0),
            Record = cms.string('SiStripApvGainRcd')
        ), 
        cms.PSet(
            Label = cms.untracked.string(''),
            NormalizationFactor = cms.untracked.double(1.0),
            Record = cms.string('SiStripApvGain2Rcd')
        )
    ),
    AutomaticNormalization = cms.bool(False),
    appendToDataLabel = cms.string(''),
    printDebug = cms.untracked.bool(False)
)


process.siStripLorentzAngleDepESProducer = cms.ESProducer("SiStripLorentzAngleDepESProducer",
    LatencyRecord = cms.PSet(
        label = cms.untracked.string(''),
        record = cms.string('SiStripLatencyRcd')
    ),
    LorentzAngleDeconvMode = cms.PSet(
        label = cms.untracked.string('deconvolution'),
        record = cms.string('SiStripLorentzAngleRcd')
    ),
    LorentzAnglePeakMode = cms.PSet(
        label = cms.untracked.string('peak'),
        record = cms.string('SiStripLorentzAngleRcd')
    )
)


process.siStripQualityESProducer = cms.ESProducer("SiStripQualityESProducer",
    ListOfRecordToMerge = cms.VPSet(
        cms.PSet(
            record = cms.string('SiStripDetVOffRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripDetCablingRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('RunInfoRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadChannelRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadFiberRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadModuleRcd'),
            tag = cms.string('')
        ), 
        cms.PSet(
            record = cms.string('SiStripBadStripRcd'),
            tag = cms.string('')
        )
    ),
    PrintDebugOutput = cms.bool(False),
    ReduceGranularity = cms.bool(False),
    ThresholdForReducedGranularity = cms.double(0.3),
    UseEmptyRunInfo = cms.bool(False),
    appendToDataLabel = cms.string('')
)


process.sistripconn = cms.ESProducer("SiStripConnectivity")


process.stripCPEESProducer = cms.ESProducer("StripCPEESProducer",
    ComponentName = cms.string('stripCPE'),
    ComponentType = cms.string('SimpleStripCPE'),
    parameters = cms.PSet(

    )
)


process.GlobalTag = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string(''),
        authenticationSystem = cms.untracked.int32(0),
        messageLevel = cms.untracked.int32(0),
        security = cms.untracked.string('')
    ),
    DumpStat = cms.untracked.bool(False),
    ReconnectEachRun = cms.untracked.bool(False),
    RefreshAlways = cms.untracked.bool(False),
    RefreshEachRun = cms.untracked.bool(False),
    RefreshOpenIOVs = cms.untracked.bool(False),
    connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
    globaltag = cms.string('106X_dataRun2_v37'),
    pfnPostfix = cms.untracked.string(''),
    pfnPrefix = cms.untracked.string(''),
    snapshotTime = cms.string(''),
    toGet = cms.VPSet()
)


process.HcalTimeSlewEP = cms.ESSource("HcalTimeSlewEP",
    appendToDataLabel = cms.string('HBHE'),
    timeSlewParametersM2 = cms.VPSet(
        cms.PSet(
            slope = cms.double(-3.178648),
            tmax = cms.double(16.0),
            tzero = cms.double(23.960177)
        ), 
        cms.PSet(
            slope = cms.double(-1.5610227),
            tmax = cms.double(10.0),
            tzero = cms.double(11.977461)
        ), 
        cms.PSet(
            slope = cms.double(-1.075824),
            tmax = cms.double(6.25),
            tzero = cms.double(9.109694)
        )
    ),
    timeSlewParametersM3 = cms.VPSet(
        cms.PSet(
            cap = cms.double(6.0),
            tspar0 = cms.double(12.2999),
            tspar0_siPM = cms.double(0.0),
            tspar1 = cms.double(-2.19142),
            tspar1_siPM = cms.double(0.0),
            tspar2 = cms.double(0.0),
            tspar2_siPM = cms.double(0.0)
        ), 
        cms.PSet(
            cap = cms.double(6.0),
            tspar0 = cms.double(15.5),
            tspar0_siPM = cms.double(0.0),
            tspar1 = cms.double(-3.2),
            tspar1_siPM = cms.double(0.0),
            tspar2 = cms.double(32.0),
            tspar2_siPM = cms.double(0.0)
        ), 
        cms.PSet(
            cap = cms.double(6.0),
            tspar0 = cms.double(12.2999),
            tspar0_siPM = cms.double(0.0),
            tspar1 = cms.double(-2.19142),
            tspar1_siPM = cms.double(0.0),
            tspar2 = cms.double(0.0),
            tspar2_siPM = cms.double(0.0)
        ), 
        cms.PSet(
            cap = cms.double(6.0),
            tspar0 = cms.double(12.2999),
            tspar0_siPM = cms.double(0.0),
            tspar1 = cms.double(-2.19142),
            tspar1_siPM = cms.double(0.0),
            tspar2 = cms.double(0.0),
            tspar2_siPM = cms.double(0.0)
        )
    )
)


process.HepPDTESSource = cms.ESSource("HepPDTESSource",
    pdtFileName = cms.FileInPath('SimGeneral/HepPDTESSource/data/pythiaparticle.tbl')
)


process.es_hardcode = cms.ESSource("HcalHardcodeCalibrations",
    GainWidthsForTrigPrims = cms.bool(False),
    HBRecalibration = cms.bool(False),
    HBmeanenergies = cms.FileInPath('CalibCalorimetry/HcalPlugins/data/meanenergiesHB.txt'),
    HBreCalibCutoff = cms.double(20.0),
    HERecalibration = cms.bool(False),
    HEmeanenergies = cms.FileInPath('CalibCalorimetry/HcalPlugins/data/meanenergiesHE.txt'),
    HEreCalibCutoff = cms.double(20.0),
    HFRecalParameterBlock = cms.PSet(
        HFdepthOneParameterA = cms.vdouble(
            0.004123, 0.00602, 0.008201, 0.010489, 0.013379, 
            0.016997, 0.021464, 0.027371, 0.034195, 0.044807, 
            0.058939, 0.125497
        ),
        HFdepthOneParameterB = cms.vdouble(
            -4e-06, -2e-06, 0.0, 4e-06, 1.5e-05, 
            2.6e-05, 6.3e-05, 8.4e-05, 0.00016, 0.000107, 
            0.000425, 0.000209
        ),
        HFdepthTwoParameterA = cms.vdouble(
            0.002861, 0.004168, 0.0064, 0.008388, 0.011601, 
            0.014425, 0.018633, 0.023232, 0.028274, 0.035447, 
            0.051579, 0.086593
        ),
        HFdepthTwoParameterB = cms.vdouble(
            -2e-06, -0.0, -7e-06, -6e-06, -2e-06, 
            1e-06, 1.9e-05, 3.1e-05, 6.7e-05, 1.2e-05, 
            0.000157, -3e-06
        )
    ),
    HFRecalibration = cms.bool(False),
    SiPMCharacteristics = cms.VPSet(
        cms.PSet(
            crosstalk = cms.double(0.0),
            nonlin1 = cms.double(1.0),
            nonlin2 = cms.double(0.0),
            nonlin3 = cms.double(0.0),
            pixels = cms.int32(36000)
        ), 
        cms.PSet(
            crosstalk = cms.double(0.0),
            nonlin1 = cms.double(1.0),
            nonlin2 = cms.double(0.0),
            nonlin3 = cms.double(0.0),
            pixels = cms.int32(2500)
        ), 
        cms.PSet(
            crosstalk = cms.double(0.17),
            nonlin1 = cms.double(1.00985),
            nonlin2 = cms.double(7.84089e-06),
            nonlin3 = cms.double(2.86282e-10),
            pixels = cms.int32(27370)
        ), 
        cms.PSet(
            crosstalk = cms.double(0.196),
            nonlin1 = cms.double(1.00546),
            nonlin2 = cms.double(6.40239e-06),
            nonlin3 = cms.double(1.27011e-10),
            pixels = cms.int32(38018)
        ), 
        cms.PSet(
            crosstalk = cms.double(0.17),
            nonlin1 = cms.double(1.00985),
            nonlin2 = cms.double(7.84089e-06),
            nonlin3 = cms.double(2.86282e-10),
            pixels = cms.int32(27370)
        ), 
        cms.PSet(
            crosstalk = cms.double(0.196),
            nonlin1 = cms.double(1.00546),
            nonlin2 = cms.double(6.40239e-06),
            nonlin3 = cms.double(1.27011e-10),
            pixels = cms.int32(38018)
        ), 
        cms.PSet(
            crosstalk = cms.double(0.0),
            nonlin1 = cms.double(1.0),
            nonlin2 = cms.double(0.0),
            nonlin3 = cms.double(0.0),
            pixels = cms.int32(0)
        )
    ),
    hb = cms.PSet(
        darkCurrent = cms.vdouble(0.0),
        doRadiationDamage = cms.bool(False),
        gain = cms.vdouble(0.19),
        gainWidth = cms.vdouble(0.0),
        mcShape = cms.int32(125),
        pedestal = cms.double(3.285),
        pedestalWidth = cms.double(0.809),
        photoelectronsToAnalog = cms.double(0.3305),
        qieOffset = cms.vdouble(-0.49, 1.8, 7.2, 37.9),
        qieSlope = cms.vdouble(0.912, 0.917, 0.922, 0.923),
        qieType = cms.int32(0),
        recoShape = cms.int32(105),
        zsThreshold = cms.int32(8)
    ),
    hbUpgrade = cms.PSet(
        darkCurrent = cms.vdouble(0.01, 0.015),
        doRadiationDamage = cms.bool(True),
        gain = cms.vdouble(0.0006252),
        gainWidth = cms.vdouble(0),
        mcShape = cms.int32(206),
        pedestal = cms.double(17.3),
        pedestalWidth = cms.double(1.5),
        photoelectronsToAnalog = cms.double(40.0),
        qieOffset = cms.vdouble(0.0, 0.0, 0.0, 0.0),
        qieSlope = cms.vdouble(0.05376, 0.05376, 0.05376, 0.05376),
        qieType = cms.int32(2),
        radiationDamage = cms.PSet(
            depVsNeutrons = cms.vdouble(5.543e-10, 8.012e-10),
            depVsTemp = cms.double(0.0631),
            intlumiOffset = cms.double(150),
            intlumiToNeutrons = cms.double(367000000.0),
            temperatureBase = cms.double(20),
            temperatureNew = cms.double(-5)
        ),
        recoShape = cms.int32(206),
        zsThreshold = cms.int32(16)
    ),
    he = cms.PSet(
        darkCurrent = cms.vdouble(0.0),
        doRadiationDamage = cms.bool(False),
        gain = cms.vdouble(0.23),
        gainWidth = cms.vdouble(0),
        mcShape = cms.int32(125),
        pedestal = cms.double(3.163),
        pedestalWidth = cms.double(0.9698),
        photoelectronsToAnalog = cms.double(0.3305),
        qieOffset = cms.vdouble(-0.38, 2.0, 7.6, 39.6),
        qieSlope = cms.vdouble(0.912, 0.916, 0.92, 0.922),
        qieType = cms.int32(0),
        recoShape = cms.int32(105),
        zsThreshold = cms.int32(9)
    ),
    heUpgrade = cms.PSet(
        darkCurrent = cms.vdouble(0.01, 0.015),
        doRadiationDamage = cms.bool(True),
        gain = cms.vdouble(0.0006252),
        gainWidth = cms.vdouble(0),
        mcShape = cms.int32(206),
        pedestal = cms.double(17.3),
        pedestalWidth = cms.double(1.5),
        photoelectronsToAnalog = cms.double(40.0),
        qieOffset = cms.vdouble(0.0, 0.0, 0.0, 0.0),
        qieSlope = cms.vdouble(0.05376, 0.05376, 0.05376, 0.05376),
        qieType = cms.int32(2),
        radiationDamage = cms.PSet(
            depVsNeutrons = cms.vdouble(5.543e-10, 8.012e-10),
            depVsTemp = cms.double(0.0631),
            intlumiOffset = cms.double(75),
            intlumiToNeutrons = cms.double(29200000.0),
            temperatureBase = cms.double(20),
            temperatureNew = cms.double(5)
        ),
        recoShape = cms.int32(206),
        zsThreshold = cms.int32(16)
    ),
    hf = cms.PSet(
        darkCurrent = cms.vdouble(0.0),
        doRadiationDamage = cms.bool(False),
        gain = cms.vdouble(0.14, 0.135),
        gainWidth = cms.vdouble(0.0, 0.0),
        mcShape = cms.int32(301),
        pedestal = cms.double(9.354),
        pedestalWidth = cms.double(2.516),
        photoelectronsToAnalog = cms.double(0.0),
        qieOffset = cms.vdouble(-0.87, 1.4, 7.8, -29.6),
        qieSlope = cms.vdouble(0.359, 0.358, 0.36, 0.367),
        qieType = cms.int32(0),
        recoShape = cms.int32(301),
        zsThreshold = cms.int32(-9999)
    ),
    hfUpgrade = cms.PSet(
        darkCurrent = cms.vdouble(0.0),
        doRadiationDamage = cms.bool(False),
        gain = cms.vdouble(0.14, 0.135),
        gainWidth = cms.vdouble(0.0, 0.0),
        mcShape = cms.int32(301),
        pedestal = cms.double(13.33),
        pedestalWidth = cms.double(3.33),
        photoelectronsToAnalog = cms.double(0.0),
        qieOffset = cms.vdouble(0.0697, -0.7405, 12.38, -671.9),
        qieSlope = cms.vdouble(0.297, 0.298, 0.298, 0.313),
        qieType = cms.int32(1),
        recoShape = cms.int32(301),
        zsThreshold = cms.int32(-9999)
    ),
    ho = cms.PSet(
        darkCurrent = cms.vdouble(0.0),
        doRadiationDamage = cms.bool(False),
        gain = cms.vdouble(0.006, 0.0087),
        gainWidth = cms.vdouble(0.0, 0.0),
        mcShape = cms.int32(201),
        pedestal = cms.double(12.06),
        pedestalWidth = cms.double(0.6285),
        photoelectronsToAnalog = cms.double(4.0),
        qieOffset = cms.vdouble(-0.44, 1.4, 7.1, 38.5),
        qieSlope = cms.vdouble(0.907, 0.915, 0.92, 0.921),
        qieType = cms.int32(0),
        recoShape = cms.int32(201),
        zsThreshold = cms.int32(24)
    ),
    iLumi = cms.double(-1.0),
    killHE = cms.bool(False),
    testHEPlan1 = cms.bool(False),
    testHFQIE10 = cms.bool(False),
    toGet = cms.untracked.vstring('GainWidths'),
    useHBUpgrade = cms.bool(False),
    useHEUpgrade = cms.bool(False),
    useHFUpgrade = cms.bool(False),
    useHOUpgrade = cms.bool(True),
    useIeta18depth1 = cms.bool(True),
    useLayer0Weight = cms.bool(False)
)


process.prefer("es_hardcode")

process.ak8PFCHSL1L2L3ResidualCorrectorTask = cms.Task(process.ak8PFCHSL1L2L3ResidualCorrector, process.ak8PFCHSL1OffsetCorrector, process.ak8PFCHSL2RelativeCorrector, process.ak8PFCHSL3AbsoluteCorrector, process.ak8PFCHSResidualCorrector)


process.ak4CaloL1FastL2L3CorrectorTask = cms.Task(process.ak4CaloL1FastL2L3Corrector, process.ak4CaloL1FastjetCorrector, process.ak4CaloL2RelativeCorrector, process.ak4CaloL3AbsoluteCorrector)


process.ic5PFL2L3L6CorrectorTask = cms.Task(process.ic5PFL2L3L6Corrector, process.ic5PFL6SLBCorrector, process.kt4PFL2L3Corrector)


process.ak6PFL1L2L3ResidualCorrectorTask = cms.Task(process.ak6PFL1L2L3ResidualCorrector, process.ak6PFL1OffsetCorrector, process.ak6PFL2RelativeCorrector, process.ak6PFL3AbsoluteCorrector, process.ak6PFResidualCorrector)


process.ak3PFCHSL2L3ResidualCorrectorTask = cms.Task(process.ak3PFCHSL2L3ResidualCorrector, process.ak3PFCHSL2RelativeCorrector, process.ak3PFCHSL3AbsoluteCorrector, process.ak3PFCHSResidualCorrector)


process.ak7CaloL2L3ResidualCorrectorTask = cms.Task(process.ak7CaloL2L3ResidualCorrector, process.ak7CaloL2RelativeCorrector, process.ak7CaloL3AbsoluteCorrector, process.ak7CaloResidualCorrector)


process.ak9PFCHSL1L2L3ResidualCorrectorTask = cms.Task(process.ak9PFCHSL1L2L3ResidualCorrector, process.ak9PFCHSL1OffsetCorrector, process.ak9PFCHSL2RelativeCorrector, process.ak9PFCHSL3AbsoluteCorrector, process.ak9PFCHSResidualCorrector)


process.ak6PFCHSL2L3ResidualCorrectorTask = cms.Task(process.ak6PFCHSL2L3ResidualCorrector, process.ak6PFCHSL2RelativeCorrector, process.ak6PFCHSL3AbsoluteCorrector, process.ak6PFCHSResidualCorrector)


process.ak6PFL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak6PFL1FastjetCorrector, process.ak6PFL1FastjetL2L3ResidualCorrector, process.ak6PFL2RelativeCorrector, process.ak6PFL3AbsoluteCorrector, process.ak6PFResidualCorrector)


process.kt4PFL2L3CorrectorTask = cms.Task(process.kt4PFL2L3Corrector, process.kt4PFL2RelativeCorrector, process.kt4PFL3AbsoluteCorrector)


process.ak9PFCHSL2L3ResidualCorrectorTask = cms.Task(process.ak9PFCHSL2L3ResidualCorrector, process.ak9PFCHSL2RelativeCorrector, process.ak9PFCHSL3AbsoluteCorrector, process.ak9PFCHSResidualCorrector)


process.ak4PFL1L2L3CorrectorTask = cms.Task(process.ak4PFL1L2L3Corrector, process.ak4PFL1OffsetCorrector, process.ak4PFL2RelativeCorrector, process.ak4PFL3AbsoluteCorrector)


process.ak2PFL1L2L3ResidualCorrectorTask = cms.Task(process.ak2PFL1L2L3ResidualCorrector, process.ak2PFL1OffsetCorrector, process.ak2PFL2RelativeCorrector, process.ak2PFL3AbsoluteCorrector, process.ak2PFResidualCorrector)


process.ak7PFL1L2L3ResidualCorrectorTask = cms.Task(process.ak7PFL1L2L3ResidualCorrector, process.ak7PFL1OffsetCorrector, process.ak7PFL2RelativeCorrector, process.ak7PFL3AbsoluteCorrector, process.ak7PFResidualCorrector)


process.ak9PFL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak9PFL1FastjetCorrector, process.ak9PFL1FastjetL2L3ResidualCorrector, process.ak9PFL2RelativeCorrector, process.ak9PFL3AbsoluteCorrector, process.ak9PFResidualCorrector)


process.ak2PFCHSL2L3CorrectorTask = cms.Task(process.ak2PFCHSL2L3Corrector, process.ak2PFCHSL2RelativeCorrector, process.ak2PFCHSL3AbsoluteCorrector)


process.ak4PFPuppiL1FastL2L3ResidualCorrectorTask = cms.Task(process.ak4PFPuppiL1FastL2L3ResidualCorrector, process.ak4PFPuppiL1FastjetCorrector, process.ak4PFPuppiL2RelativeCorrector, process.ak4PFPuppiL3AbsoluteCorrector, process.ak4PFPuppiResidualCorrector)


process.ak4PFL1FastL2L3CorrectorTask = cms.Task(process.ak4PFL1FastL2L3Corrector, process.ak4PFL1FastjetCorrector, process.ak4PFL2RelativeCorrector, process.ak4PFL3AbsoluteCorrector)


process.ak4TrackL2L3CorrectorTask = cms.Task(process.ak4TrackL2L3Corrector, process.ak4TrackL2RelativeCorrector, process.ak4TrackL3AbsoluteCorrector)


process.ak7CaloL1L2L3CorrectorTask = cms.Task(process.ak7CaloL1L2L3Corrector, process.ak7CaloL1OffsetCorrector, process.ak7CaloL2RelativeCorrector, process.ak7CaloL3AbsoluteCorrector)


process.kt6PFL1FastL2L3L6CorrectorTask = cms.Task(process.kt4PFL1FastL2L3Corrector, process.kt6PFL1FastL2L3L6Corrector, process.kt6PFL6SLBCorrector)


process.ak1PFCHSL2L3CorrectorTask = cms.Task(process.ak1PFCHSL2L3Corrector, process.ak1PFCHSL2RelativeCorrector, process.ak1PFCHSL3AbsoluteCorrector)


process.kt6CaloL2L3CorrectorTask = cms.Task(process.kt6CaloL2L3Corrector, process.kt6CaloL2RelativeCorrector, process.kt6CaloL3AbsoluteCorrector)


process.kt4CaloL2L3L6CorrectorTask = cms.Task(process.ak7CaloL2L3Corrector, process.kt4CaloL2L3L6Corrector, process.kt4CaloL6SLBCorrector)


process.ak3PFCHSL1L2L3ResidualCorrectorTask = cms.Task(process.ak3PFCHSL1L2L3ResidualCorrector, process.ak3PFCHSL1OffsetCorrector, process.ak3PFCHSL2RelativeCorrector, process.ak3PFCHSL3AbsoluteCorrector, process.ak3PFCHSResidualCorrector)


process.ak10PFL2L3ResidualCorrectorTask = cms.Task(process.ak10PFL2L3ResidualCorrector, process.ak10PFL2RelativeCorrector, process.ak10PFL3AbsoluteCorrector, process.ak10PFResidualCorrector)


process.kt4CaloL1L2L3ResidualCorrectorTask = cms.Task(process.kt4CaloL1L2L3ResidualCorrector, process.kt4CaloL1OffsetCorrector, process.kt4CaloL2RelativeCorrector, process.kt4CaloL3AbsoluteCorrector, process.kt4CaloResidualCorrector)


process.ak6PFCHSL2L3CorrectorTask = cms.Task(process.ak6PFCHSL2L3Corrector, process.ak6PFCHSL2RelativeCorrector, process.ak6PFCHSL3AbsoluteCorrector)


process.ic5PFL1FastL2L3L6CorrectorTask = cms.Task(process.ic5PFL1FastL2L3L6Corrector, process.ic5PFL6SLBCorrector, process.kt4PFL1FastL2L3Corrector)


process.ak9PFL2L3ResidualCorrectorTask = cms.Task(process.ak9PFL2L3ResidualCorrector, process.ak9PFL2RelativeCorrector, process.ak9PFL3AbsoluteCorrector, process.ak9PFResidualCorrector)


process.ic5CaloL1FastL2L3CorrectorTask = cms.Task(process.ak4CaloL1FastjetCorrector, process.ic5CaloL1FastL2L3Corrector, process.ic5CaloL2RelativeCorrector, process.ic5CaloL3AbsoluteCorrector)


process.ak4PFL1L2L3ResidualCorrectorTask = cms.Task(process.ak4PFL1L2L3ResidualCorrector, process.ak4PFL1OffsetCorrector, process.ak4PFL2RelativeCorrector, process.ak4PFL3AbsoluteCorrector, process.ak4PFResidualCorrector)


process.ak7PFL1L2L3CorrectorTask = cms.Task(process.ak7PFL1L2L3Corrector, process.ak7PFL1OffsetCorrector, process.ak7PFL2RelativeCorrector, process.ak7PFL3AbsoluteCorrector)


process.kt6CaloL1FastL2L3CorrectorTask = cms.Task(process.ak4CaloL1FastjetCorrector, process.kt6CaloL1FastL2L3Corrector, process.kt6CaloL2RelativeCorrector, process.kt6CaloL3AbsoluteCorrector)


process.ak5PFCHSL1L2L3ResidualCorrectorTask = cms.Task(process.ak5PFCHSL1L2L3ResidualCorrector, process.ak5PFCHSL1OffsetCorrector, process.ak5PFCHSL2RelativeCorrector, process.ak5PFCHSL3AbsoluteCorrector, process.ak5PFCHSResidualCorrector)


process.ic5CaloL2L3CorrectorTask = cms.Task(process.ic5CaloL2L3Corrector, process.ic5CaloL2RelativeCorrector, process.ic5CaloL3AbsoluteCorrector)


process.ak7CaloL1FastL2L3ResidualCorrectorTask = cms.Task(process.ak7CaloL1FastL2L3ResidualCorrector, process.ak7CaloL1FastjetCorrector, process.ak7CaloL2RelativeCorrector, process.ak7CaloL3AbsoluteCorrector, process.ak7CaloResidualCorrector)


process.kt4CaloL1FastL2L3CorrectorTask = cms.Task(process.ak4CaloL1FastjetCorrector, process.kt4CaloL1FastL2L3Corrector, process.kt4CaloL2RelativeCorrector, process.kt4CaloL3AbsoluteCorrector)


process.ak8PFL2L3CorrectorTask = cms.Task(process.ak8PFL2L3Corrector, process.ak8PFL2RelativeCorrector, process.ak8PFL3AbsoluteCorrector)


process.ak4PFCHSL1L2L3ResidualCorrectorTask = cms.Task(process.ak4PFCHSL1L2L3ResidualCorrector, process.ak4PFCHSL1OffsetCorrector, process.ak4PFCHSL2RelativeCorrector, process.ak4PFCHSL3AbsoluteCorrector, process.ak4PFCHSResidualCorrector)


process.ak4PFPuppiL2L3ResidualCorrectorTask = cms.Task(process.ak4PFPuppiL2L3ResidualCorrector, process.ak4PFPuppiL2RelativeCorrector, process.ak4PFPuppiL3AbsoluteCorrector, process.ak4PFPuppiResidualCorrector)


process.ak4PFPuppiL2L3CorrectorTask = cms.Task(process.ak4PFPuppiL2L3Corrector, process.ak4PFPuppiL2RelativeCorrector, process.ak4PFPuppiL3AbsoluteCorrector)


process.ak8PFCHSL2L3CorrectorTask = cms.Task(process.ak8PFCHSL2L3Corrector, process.ak8PFCHSL2RelativeCorrector, process.ak8PFCHSL3AbsoluteCorrector)


process.ak7PFL1FastL2L3CorrectorTask = cms.Task(process.ak4PFL1FastjetCorrector, process.ak7PFL1FastL2L3Corrector, process.ak7PFL2RelativeCorrector, process.ak7PFL3AbsoluteCorrector)


process.ak4CaloL1FastL2L3L6CorrectorTask = cms.Task(process.ak4CaloL1FastL2L3L6Corrector, process.ak4CaloL1FastjetCorrector, process.ak4CaloL2RelativeCorrector, process.ak4CaloL3AbsoluteCorrector, process.ak4CaloL6SLBCorrector)


process.ak2PFL2L3ResidualCorrectorTask = cms.Task(process.ak2PFL2L3ResidualCorrector, process.ak2PFL2RelativeCorrector, process.ak2PFL3AbsoluteCorrector, process.ak2PFResidualCorrector)


process.kt4PFL1L2L3ResidualCorrectorTask = cms.Task(process.kt4PFL1L2L3ResidualCorrector, process.kt4PFL1OffsetCorrector, process.kt4PFL2RelativeCorrector, process.kt4PFL3AbsoluteCorrector, process.kt4PFResidualCorrector)


process.ak9PFCHSL2L3CorrectorTask = cms.Task(process.ak9PFCHSL2L3Corrector, process.ak9PFCHSL2RelativeCorrector, process.ak9PFCHSL3AbsoluteCorrector)


process.kt6PFL1L2L3ResidualCorrectorTask = cms.Task(process.kt6PFL1L2L3ResidualCorrector, process.kt6PFL1OffsetCorrector, process.kt6PFL2RelativeCorrector, process.kt6PFL3AbsoluteCorrector, process.kt6PFResidualCorrector)


process.ak8PFCHSL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak8PFCHSL1FastjetCorrector, process.ak8PFCHSL1FastjetL2L3ResidualCorrector, process.ak8PFCHSL2RelativeCorrector, process.ak8PFCHSL3AbsoluteCorrector, process.ak8PFCHSResidualCorrector)


process.ic5CaloL2L3ResidualCorrectorTask = cms.Task(process.ic5CaloL2L3ResidualCorrector, process.ic5CaloL2RelativeCorrector, process.ic5CaloL3AbsoluteCorrector, process.ic5CaloResidualCorrector)


process.ak4PFL2L3L6CorrectorTask = cms.Task(process.ak4PFL2L3L6Corrector, process.ak4PFL2RelativeCorrector, process.ak4PFL3AbsoluteCorrector, process.ak4PFL6SLBCorrector)


process.ak7L1JPTOffsetCorrectorTask = cms.Task(process.ak7CaloL1OffsetCorrector, process.ak7L1JPTOffsetCorrector)


process.kt4PFL2L3ResidualCorrectorTask = cms.Task(process.kt4PFL2L3ResidualCorrector, process.kt4PFL2RelativeCorrector, process.kt4PFL3AbsoluteCorrector, process.kt4PFResidualCorrector)


process.ak4PFPuppiL1L2L3ResidualCorrectorTask = cms.Task(process.ak4PFPuppiL1L2L3ResidualCorrector, process.ak4PFPuppiL1OffsetCorrector, process.ak4PFPuppiL2RelativeCorrector, process.ak4PFPuppiL3AbsoluteCorrector, process.ak4PFPuppiResidualCorrector)


process.ak4L1JPTOffsetCorrectorTask = cms.Task(process.ak4CaloL1OffsetCorrector, process.ak4L1JPTOffsetCorrector)


process.kt6PFL2L3CorrectorTask = cms.Task(process.kt6PFL2L3Corrector, process.kt6PFL2RelativeCorrector, process.kt6PFL3AbsoluteCorrector)


process.ak3PFL2L3CorrectorTask = cms.Task(process.ak3PFL2L3Corrector, process.ak3PFL2RelativeCorrector, process.ak3PFL3AbsoluteCorrector)


process.kt6PFL2L3L6CorrectorTask = cms.Task(process.kt4PFL2L3Corrector, process.kt6PFL2L3L6Corrector, process.kt6PFL6SLBCorrector)


process.ic5PFL2L3CorrectorTask = cms.Task(process.ic5PFL2L3Corrector, process.ic5PFL2RelativeCorrector, process.ic5PFL3AbsoluteCorrector)


process.ak8PFL1L2L3ResidualCorrectorTask = cms.Task(process.ak8PFL1L2L3ResidualCorrector, process.ak8PFL1OffsetCorrector, process.ak8PFL2RelativeCorrector, process.ak8PFL3AbsoluteCorrector, process.ak8PFResidualCorrector)


process.ak7PFL2L3CorrectorTask = cms.Task(process.ak7PFL2L3Corrector, process.ak7PFL2RelativeCorrector, process.ak7PFL3AbsoluteCorrector)


process.ak10PFL1L2L3ResidualCorrectorTask = cms.Task(process.ak10PFL1L2L3ResidualCorrector, process.ak10PFL1OffsetCorrector, process.ak10PFL2RelativeCorrector, process.ak10PFL3AbsoluteCorrector, process.ak10PFResidualCorrector)


process.ak7PFCHSL2L3CorrectorTask = cms.Task(process.ak7PFCHSL2L3Corrector, process.ak7PFCHSL2RelativeCorrector, process.ak7PFCHSL3AbsoluteCorrector)


process.ak5PFL2L3CorrectorTask = cms.Task(process.ak5PFL2L3Corrector, process.ak5PFL2RelativeCorrector, process.ak5PFL3AbsoluteCorrector)


process.ak7PFL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak7PFL1FastjetCorrector, process.ak7PFL1FastjetL2L3ResidualCorrector, process.ak7PFL2RelativeCorrector, process.ak7PFL3AbsoluteCorrector, process.ak7PFResidualCorrector)


process.ak4L1JPTFastjetCorrectorTask = cms.Task(process.ak4CaloL1FastjetCorrector, process.ak4L1JPTFastjetCorrector)


process.ak7PFCHSL1FastL2L3CorrectorTask = cms.Task(process.ak4PFCHSL1FastjetCorrector, process.ak7PFCHSL1FastL2L3Corrector, process.ak7PFCHSL2RelativeCorrector, process.ak7PFCHSL3AbsoluteCorrector)


process.kt4CaloL1FastL2L3L6CorrectorTask = cms.Task(process.ak7CaloL1L2L3Corrector, process.kt4CaloL1FastL2L3L6Corrector, process.kt4CaloL6SLBCorrector)


process.ak4JPTL2L3CorrectorTask = cms.Task(process.ak4JPTL2L3Corrector, process.ak4JPTL2RelativeCorrector, process.ak4JPTL3AbsoluteCorrector, process.ak4L1JPTOffsetCorrectorTask)


process.ic5CaloL1L2L3ResidualCorrectorTask = cms.Task(process.ic5CaloL1L2L3ResidualCorrector, process.ic5CaloL1OffsetCorrector, process.ic5CaloL2RelativeCorrector, process.ic5CaloL3AbsoluteCorrector, process.ic5CaloResidualCorrector)


process.kt4PFL1L2L3CorrectorTask = cms.Task(process.kt4PFL1L2L3Corrector, process.kt4PFL1OffsetCorrector, process.kt4PFL2RelativeCorrector, process.kt4PFL3AbsoluteCorrector)


process.ak10PFCHSL2L3CorrectorTask = cms.Task(process.ak10PFCHSL2L3Corrector, process.ak10PFCHSL2RelativeCorrector, process.ak10PFCHSL3AbsoluteCorrector)


process.ak8PFL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak8PFL1FastjetCorrector, process.ak8PFL1FastjetL2L3ResidualCorrector, process.ak8PFL2RelativeCorrector, process.ak8PFL3AbsoluteCorrector, process.ak8PFResidualCorrector)


process.ak4JPTL1FastL2L3CorrectorTask = cms.Task(process.ak4JPTL1FastL2L3Corrector, process.ak4JPTL2RelativeCorrector, process.ak4JPTL3AbsoluteCorrector, process.ak4L1JPTFastjetCorrectorTask)


process.ak5PFCHSL2L3ResidualCorrectorTask = cms.Task(process.ak5PFCHSL2L3ResidualCorrector, process.ak5PFCHSL2RelativeCorrector, process.ak5PFCHSL3AbsoluteCorrector, process.ak5PFCHSResidualCorrector)


process.ak2PFCHSL1L2L3ResidualCorrectorTask = cms.Task(process.ak2PFCHSL1L2L3ResidualCorrector, process.ak2PFCHSL1OffsetCorrector, process.ak2PFCHSL2RelativeCorrector, process.ak2PFCHSL3AbsoluteCorrector, process.ak2PFCHSResidualCorrector)


process.ak4TrackL1FastL2L3CorrectorTask = cms.Task(process.ak4CaloL1FastjetCorrector, process.ak4TrackL1FastL2L3Corrector, process.ak4TrackL2RelativeCorrector, process.ak4TrackL3AbsoluteCorrector)


process.ak4PFL1FastL2L3ResidualCorrectorTask = cms.Task(process.ak4PFL1FastL2L3ResidualCorrector, process.ak4PFL1FastjetCorrector, process.ak4PFL2RelativeCorrector, process.ak4PFL3AbsoluteCorrector, process.ak4PFResidualCorrector)


process.ak3PFCHSL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak3PFCHSL1FastjetCorrector, process.ak3PFCHSL1FastjetL2L3ResidualCorrector, process.ak3PFCHSL2RelativeCorrector, process.ak3PFCHSL3AbsoluteCorrector, process.ak3PFCHSResidualCorrector)


process.ak8PFCHSL2L3ResidualCorrectorTask = cms.Task(process.ak8PFCHSL2L3ResidualCorrector, process.ak8PFCHSL2RelativeCorrector, process.ak8PFCHSL3AbsoluteCorrector, process.ak8PFCHSResidualCorrector)


process.ak1PFCHSL1L2L3ResidualCorrectorTask = cms.Task(process.ak1PFCHSL1L2L3ResidualCorrector, process.ak1PFCHSL1OffsetCorrector, process.ak1PFCHSL2RelativeCorrector, process.ak1PFCHSL3AbsoluteCorrector, process.ak1PFCHSResidualCorrector)


process.kt6CaloL2L3L6CorrectorTask = cms.Task(process.ak7CaloL2L3Corrector, process.kt6CaloL2L3L6Corrector, process.kt6CaloL6SLBCorrector)


process.kt4CaloL1L2L3CorrectorTask = cms.Task(process.kt4CaloL1L2L3Corrector, process.kt4CaloL1OffsetCorrector, process.kt4CaloL2RelativeCorrector, process.kt4CaloL3AbsoluteCorrector)


process.ic5PFL1FastL2L3CorrectorTask = cms.Task(process.ak4PFL1FastjetCorrector, process.ic5PFL1FastL2L3Corrector, process.ic5PFL2RelativeCorrector, process.ic5PFL3AbsoluteCorrector)


process.kt6PFL1FastL2L3CorrectorTask = cms.Task(process.ak4PFL1FastjetCorrector, process.kt6PFL1FastL2L3Corrector, process.kt6PFL2RelativeCorrector, process.kt6PFL3AbsoluteCorrector)


process.kt6PFL1FastL2L3ResidualCorrectorTask = cms.Task(process.kt6PFL1FastL2L3ResidualCorrector, process.kt6PFL1FastjetCorrector, process.kt6PFL2RelativeCorrector, process.kt6PFL3AbsoluteCorrector, process.kt6PFResidualCorrector)


process.ak7PFCHSL1L2L3ResidualCorrectorTask = cms.Task(process.ak7PFCHSL1L2L3ResidualCorrector, process.ak7PFCHSL1OffsetCorrector, process.ak7PFCHSL2RelativeCorrector, process.ak7PFCHSL3AbsoluteCorrector, process.ak7PFCHSResidualCorrector)


process.kt4CaloL1FastL2L3ResidualCorrectorTask = cms.Task(process.kt4CaloL1FastL2L3ResidualCorrector, process.kt4CaloL1FastjetCorrector, process.kt4CaloL2RelativeCorrector, process.kt4CaloL3AbsoluteCorrector, process.kt4CaloResidualCorrector)


process.ic5PFL1L2L3CorrectorTask = cms.Task(process.ic5PFL1L2L3Corrector, process.ic5PFL1OffsetCorrector, process.ic5PFL2RelativeCorrector, process.ic5PFL3AbsoluteCorrector)


process.ak4PFL2L3ResidualCorrectorTask = cms.Task(process.ak4PFL2L3ResidualCorrector, process.ak4PFL2RelativeCorrector, process.ak4PFL3AbsoluteCorrector, process.ak4PFResidualCorrector)


process.ak4PFL2L3CorrectorTask = cms.Task(process.ak4PFL2L3Corrector, process.ak4PFL2RelativeCorrector, process.ak4PFL3AbsoluteCorrector)


process.kt4PFL1FastL2L3CorrectorTask = cms.Task(process.ak4PFL1FastjetCorrector, process.kt4PFL1FastL2L3Corrector, process.kt4PFL2RelativeCorrector, process.kt4PFL3AbsoluteCorrector)


process.ak3PFL1L2L3ResidualCorrectorTask = cms.Task(process.ak3PFL1L2L3ResidualCorrector, process.ak3PFL1OffsetCorrector, process.ak3PFL2RelativeCorrector, process.ak3PFL3AbsoluteCorrector, process.ak3PFResidualCorrector)


process.ak4CaloL2L3ResidualCorrectorTask = cms.Task(process.ak4CaloL2L3ResidualCorrector, process.ak4CaloL2RelativeCorrector, process.ak4CaloL3AbsoluteCorrector, process.ak4CaloResidualCorrector)


process.ak1PFL1L2L3ResidualCorrectorTask = cms.Task(process.ak1PFL1L2L3ResidualCorrector, process.ak1PFL1OffsetCorrector, process.ak1PFL2RelativeCorrector, process.ak1PFL3AbsoluteCorrector, process.ak1PFResidualCorrector)


process.ak4PFCHSL1FastL2L3ResidualCorrectorTask = cms.Task(process.ak4PFCHSL1FastL2L3ResidualCorrector, process.ak4PFCHSL1FastjetCorrector, process.ak4PFCHSL2RelativeCorrector, process.ak4PFCHSL3AbsoluteCorrector, process.ak4PFCHSResidualCorrector)


process.ak3PFL2L3ResidualCorrectorTask = cms.Task(process.ak3PFL2L3ResidualCorrector, process.ak3PFL2RelativeCorrector, process.ak3PFL3AbsoluteCorrector, process.ak3PFResidualCorrector)


process.ak9PFCHSL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak9PFCHSL1FastjetCorrector, process.ak9PFCHSL1FastjetL2L3ResidualCorrector, process.ak9PFCHSL2RelativeCorrector, process.ak9PFCHSL3AbsoluteCorrector, process.ak9PFCHSResidualCorrector)


process.ak9PFL2L3CorrectorTask = cms.Task(process.ak9PFL2L3Corrector, process.ak9PFL2RelativeCorrector, process.ak9PFL3AbsoluteCorrector)


process.ak4JPTL1FastL2L3ResidualCorrectorTask = cms.Task(process.ak4JPTL1FastL2L3ResidualCorrector, process.ak4JPTL2RelativeCorrector, process.ak4JPTL3AbsoluteCorrector, process.ak4JPTResidualCorrector, process.ak4L1JPTFastjetCorrectorTask)


process.kt6CaloL1L2L3CorrectorTask = cms.Task(process.kt6CaloL1L2L3Corrector, process.kt6CaloL1OffsetCorrector, process.kt6CaloL2RelativeCorrector, process.kt6CaloL3AbsoluteCorrector)


process.ak1PFL2L3CorrectorTask = cms.Task(process.ak1PFL2L3Corrector, process.ak1PFL2RelativeCorrector, process.ak1PFL3AbsoluteCorrector)


process.ak5PFCHSL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak5PFCHSL1FastjetCorrector, process.ak5PFCHSL1FastjetL2L3ResidualCorrector, process.ak5PFCHSL2RelativeCorrector, process.ak5PFCHSL3AbsoluteCorrector, process.ak5PFCHSResidualCorrector)


process.kt4PFL1FastL2L3L6CorrectorTask = cms.Task(process.kt4PFL1FastL2L3Corrector, process.kt4PFL1FastL2L3L6Corrector, process.kt4PFL6SLBCorrector)


process.patAlgosToolsTask = cms.Task(process.patJetCorrFactorsAK4UpdatedJEC, process.patJetCorrFactorsAK8UpdatedJEC, process.pileupJetIdUpdated, process.selectedUpdatedPatJetsAK4UpdatedJEC, process.selectedUpdatedPatJetsAK8UpdatedJEC, process.selectedUpdatedPatJetsPileupJetID, process.updatedPatJetsAK4UpdatedJEC, process.updatedPatJetsAK8UpdatedJEC, process.updatedPatJetsPileupJetID)


process.ak4CaloL1L2L3CorrectorTask = cms.Task(process.ak4CaloL1L2L3Corrector, process.ak4CaloL1OffsetCorrector, process.ak4CaloL2RelativeCorrector, process.ak4CaloL3AbsoluteCorrector)


process.pileUpJetIDTask = cms.Task(process.pileupJetId, process.pileupJetIdCalculator, process.pileupJetIdEvaluator)


process.ic5CaloL1FastL2L3L6CorrectorTask = cms.Task(process.ak7CaloL1L2L3Corrector, process.ic5CaloL1FastL2L3L6Corrector, process.ic5CaloL6SLBCorrector)


process.ak7PFL2L3ResidualCorrectorTask = cms.Task(process.ak7PFL2L3ResidualCorrector, process.ak7PFL2RelativeCorrector, process.ak7PFL3AbsoluteCorrector, process.ak7PFResidualCorrector)


process.ak2PFCHSL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak2PFCHSL1FastjetCorrector, process.ak2PFCHSL1FastjetL2L3ResidualCorrector, process.ak2PFCHSL2RelativeCorrector, process.ak2PFCHSL3AbsoluteCorrector, process.ak2PFCHSResidualCorrector)


process.ic5PFL1FastL2L3ResidualCorrectorTask = cms.Task(process.ic5PFL1FastL2L3ResidualCorrector, process.ic5PFL1FastjetCorrector, process.ic5PFL2RelativeCorrector, process.ic5PFL3AbsoluteCorrector, process.ic5PFResidualCorrector)


process.ak5PFL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak5PFL1FastjetCorrector, process.ak5PFL1FastjetL2L3ResidualCorrector, process.ak5PFL2RelativeCorrector, process.ak5PFL3AbsoluteCorrector, process.ak5PFResidualCorrector)


process.kt4PFL1FastL2L3ResidualCorrectorTask = cms.Task(process.kt4PFL1FastL2L3ResidualCorrector, process.kt4PFL1FastjetCorrector, process.kt4PFL2RelativeCorrector, process.kt4PFL3AbsoluteCorrector, process.kt4PFResidualCorrector)


process.ak7CaloL2L3CorrectorTask = cms.Task(process.ak7CaloL2L3Corrector, process.ak7CaloL2RelativeCorrector, process.ak7CaloL3AbsoluteCorrector)


process.ak4PFPuppiL1L2L3CorrectorTask = cms.Task(process.ak4PFPuppiL1L2L3Corrector, process.ak4PFPuppiL1OffsetCorrector, process.ak4PFPuppiL2RelativeCorrector, process.ak4PFPuppiL3AbsoluteCorrector)


process.ak7CaloL1FastL2L3L6CorrectorTask = cms.Task(process.ak7CaloL1FastL2L3L6Corrector, process.ak7CaloL1L2L3Corrector, process.ak7CaloL6SLBCorrector)


process.ak5PFL1L2L3ResidualCorrectorTask = cms.Task(process.ak5PFL1L2L3ResidualCorrector, process.ak5PFL1OffsetCorrector, process.ak5PFL2RelativeCorrector, process.ak5PFL3AbsoluteCorrector, process.ak5PFResidualCorrector)


process.kt6CaloL1L2L3ResidualCorrectorTask = cms.Task(process.kt6CaloL1L2L3ResidualCorrector, process.kt6CaloL1OffsetCorrector, process.kt6CaloL2RelativeCorrector, process.kt6CaloL3AbsoluteCorrector, process.kt6CaloResidualCorrector)


process.ak3PFL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak3PFL1FastjetCorrector, process.ak3PFL1FastjetL2L3ResidualCorrector, process.ak3PFL2RelativeCorrector, process.ak3PFL3AbsoluteCorrector, process.ak3PFResidualCorrector)


process.ic5CaloL2L3L6CorrectorTask = cms.Task(process.ak7CaloL2L3Corrector, process.ic5CaloL2L3L6Corrector, process.ic5CaloL6SLBCorrector)


process.ak2PFL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak2PFL1FastjetCorrector, process.ak2PFL1FastjetL2L3ResidualCorrector, process.ak2PFL2RelativeCorrector, process.ak2PFL3AbsoluteCorrector, process.ak2PFResidualCorrector)


process.ak7PFCHSL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak7PFCHSL1FastjetCorrector, process.ak7PFCHSL1FastjetL2L3ResidualCorrector, process.ak7PFCHSL2RelativeCorrector, process.ak7PFCHSL3AbsoluteCorrector, process.ak7PFCHSResidualCorrector)


process.kt6CaloL2L3ResidualCorrectorTask = cms.Task(process.kt6CaloL2L3ResidualCorrector, process.kt6CaloL2RelativeCorrector, process.kt6CaloL3AbsoluteCorrector, process.kt6CaloResidualCorrector)


process.ak4CaloL1FastL2L3ResidualCorrectorTask = cms.Task(process.ak4CaloL1FastL2L3ResidualCorrector, process.ak4CaloL1FastjetCorrector, process.ak4CaloL2RelativeCorrector, process.ak4CaloL3AbsoluteCorrector, process.ak4CaloResidualCorrector)


process.ak4PFCHSL1FastL2L3CorrectorTask = cms.Task(process.ak4PFCHSL1FastL2L3Corrector, process.ak4PFCHSL1FastjetCorrector, process.ak4PFCHSL2RelativeCorrector, process.ak4PFCHSL3AbsoluteCorrector)


process.ak4CaloL2L3CorrectorTask = cms.Task(process.ak4CaloL2L3Corrector, process.ak4CaloL2RelativeCorrector, process.ak4CaloL3AbsoluteCorrector)


process.kt4CaloL2L3ResidualCorrectorTask = cms.Task(process.kt4CaloL2L3ResidualCorrector, process.kt4CaloL2RelativeCorrector, process.kt4CaloL3AbsoluteCorrector, process.kt4CaloResidualCorrector)


process.ak4JPTL1L2L3CorrectorTask = cms.Task(process.ak4JPTL1L2L3Corrector, process.ak4JPTL2RelativeCorrector, process.ak4JPTL3AbsoluteCorrector, process.ak4L1JPTOffsetCorrectorTask)


process.ak4PFCHSL2L3CorrectorTask = cms.Task(process.ak4PFCHSL2L3Corrector, process.ak4PFCHSL2RelativeCorrector, process.ak4PFCHSL3AbsoluteCorrector)


process.ak5PFCHSL2L3CorrectorTask = cms.Task(process.ak5PFCHSL2L3Corrector, process.ak5PFCHSL2RelativeCorrector, process.ak5PFCHSL3AbsoluteCorrector)


process.ak4PFL1FastL2L3L6CorrectorTask = cms.Task(process.ak4PFL1FastL2L3L6Corrector, process.ak4PFL1FastjetCorrector, process.ak4PFL2RelativeCorrector, process.ak4PFL3AbsoluteCorrector, process.ak4PFL6SLBCorrector)


process.ak1PFL2L3ResidualCorrectorTask = cms.Task(process.ak1PFL2L3ResidualCorrector, process.ak1PFL2RelativeCorrector, process.ak1PFL3AbsoluteCorrector, process.ak1PFResidualCorrector)


process.ic5CaloL1FastL2L3ResidualCorrectorTask = cms.Task(process.ic5CaloL1FastL2L3ResidualCorrector, process.ic5CaloL1FastjetCorrector, process.ic5CaloL2RelativeCorrector, process.ic5CaloL3AbsoluteCorrector, process.ic5CaloResidualCorrector)


process.kt6CaloL1FastL2L3L6CorrectorTask = cms.Task(process.ak7CaloL1L2L3Corrector, process.kt6CaloL1FastL2L3L6Corrector, process.kt6CaloL6SLBCorrector)


process.ak7CaloL1FastL2L3CorrectorTask = cms.Task(process.ak4CaloL1FastjetCorrector, process.ak7CaloL1FastL2L3Corrector, process.ak7CaloL2RelativeCorrector, process.ak7CaloL3AbsoluteCorrector)


process.ak1PFL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak1PFL1FastjetCorrector, process.ak1PFL1FastjetL2L3ResidualCorrector, process.ak1PFL2RelativeCorrector, process.ak1PFL3AbsoluteCorrector, process.ak1PFResidualCorrector)


process.kt6CaloL1FastL2L3ResidualCorrectorTask = cms.Task(process.kt6CaloL1FastL2L3ResidualCorrector, process.kt6CaloL1FastjetCorrector, process.kt6CaloL2RelativeCorrector, process.kt6CaloL3AbsoluteCorrector, process.kt6CaloResidualCorrector)


process.ak1PFCHSL2L3ResidualCorrectorTask = cms.Task(process.ak1PFCHSL2L3ResidualCorrector, process.ak1PFCHSL2RelativeCorrector, process.ak1PFCHSL3AbsoluteCorrector, process.ak1PFCHSResidualCorrector)


process.ak4PFCHSL2L3ResidualCorrectorTask = cms.Task(process.ak4PFCHSL2L3ResidualCorrector, process.ak4PFCHSL2RelativeCorrector, process.ak4PFCHSL3AbsoluteCorrector, process.ak4PFCHSResidualCorrector)


process.ak7CaloL1L2L3ResidualCorrectorTask = cms.Task(process.ak7CaloL1L2L3ResidualCorrector, process.ak7CaloL1OffsetCorrector, process.ak7CaloL2RelativeCorrector, process.ak7CaloL3AbsoluteCorrector, process.ak7CaloResidualCorrector)


process.ak4CaloL1L2L3ResidualCorrectorTask = cms.Task(process.ak4CaloL1L2L3ResidualCorrector, process.ak4CaloL1OffsetCorrector, process.ak4CaloL2RelativeCorrector, process.ak4CaloL3AbsoluteCorrector, process.ak4CaloResidualCorrector)


process.kt4PFL2L3L6CorrectorTask = cms.Task(process.kt4PFL2L3Corrector, process.kt4PFL2L3L6Corrector, process.kt4PFL6SLBCorrector)


process.ak1PFCHSL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak1PFCHSL1FastjetCorrector, process.ak1PFCHSL1FastjetL2L3ResidualCorrector, process.ak1PFCHSL2RelativeCorrector, process.ak1PFCHSL3AbsoluteCorrector, process.ak1PFCHSResidualCorrector)


process.ic5PFL1L2L3ResidualCorrectorTask = cms.Task(process.ic5PFL1L2L3ResidualCorrector, process.ic5PFL1OffsetCorrector, process.ic5PFL2RelativeCorrector, process.ic5PFL3AbsoluteCorrector, process.ic5PFResidualCorrector)


process.ak5PFL2L3ResidualCorrectorTask = cms.Task(process.ak5PFL2L3ResidualCorrector, process.ak5PFL2RelativeCorrector, process.ak5PFL3AbsoluteCorrector, process.ak5PFResidualCorrector)


process.ak4JPTL1L2L3ResidualCorrectorTask = cms.Task(process.ak4JPTL1L2L3ResidualCorrector, process.ak4JPTL2RelativeCorrector, process.ak4JPTL3AbsoluteCorrector, process.ak4JPTResidualCorrector, process.ak4L1JPTOffsetCorrectorTask)


process.ak8PFL2L3ResidualCorrectorTask = cms.Task(process.ak8PFL2L3ResidualCorrector, process.ak8PFL2RelativeCorrector, process.ak8PFL3AbsoluteCorrector, process.ak8PFResidualCorrector)


process.ak7JPTL2L3CorrectorTask = cms.Task(process.ak7JPTL2L3Corrector, process.ak7JPTL2RelativeCorrector, process.ak7JPTL3AbsoluteCorrector, process.ak7L1JPTOffsetCorrectorTask)


process.ak10PFCHSL2L3ResidualCorrectorTask = cms.Task(process.ak10PFCHSL2L3ResidualCorrector, process.ak10PFCHSL2RelativeCorrector, process.ak10PFCHSL3AbsoluteCorrector, process.ak10PFCHSResidualCorrector)


process.ak2PFL2L3CorrectorTask = cms.Task(process.ak2PFL2L3Corrector, process.ak2PFL2RelativeCorrector, process.ak2PFL3AbsoluteCorrector)


process.ak9PFL1L2L3ResidualCorrectorTask = cms.Task(process.ak9PFL1L2L3ResidualCorrector, process.ak9PFL1OffsetCorrector, process.ak9PFL2RelativeCorrector, process.ak9PFL3AbsoluteCorrector, process.ak9PFResidualCorrector)


process.kt4CaloL2L3CorrectorTask = cms.Task(process.kt4CaloL2L3Corrector, process.kt4CaloL2RelativeCorrector, process.kt4CaloL3AbsoluteCorrector)


process.ak7L1JPTFastjetCorrectorTask = cms.Task(process.ak7CaloL1FastjetCorrector, process.ak7L1JPTFastjetCorrector)


process.ak4CaloL2L3L6CorrectorTask = cms.Task(process.ak4CaloL2L3L6Corrector, process.ak4CaloL2RelativeCorrector, process.ak4CaloL3AbsoluteCorrector, process.ak4CaloL6SLBCorrector)


process.ak6PFCHSL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak6PFCHSL1FastjetCorrector, process.ak6PFCHSL1FastjetL2L3ResidualCorrector, process.ak6PFCHSL2RelativeCorrector, process.ak6PFCHSL3AbsoluteCorrector, process.ak6PFCHSResidualCorrector)


process.kt6PFL1L2L3CorrectorTask = cms.Task(process.kt6PFL1L2L3Corrector, process.kt6PFL1OffsetCorrector, process.kt6PFL2RelativeCorrector, process.kt6PFL3AbsoluteCorrector)


process.ak7JPTL1FastL2L3CorrectorTask = cms.Task(process.ak7JPTL1FastL2L3Corrector, process.ak7JPTL2RelativeCorrector, process.ak7JPTL3AbsoluteCorrector, process.ak7L1JPTFastjetCorrectorTask)


process.ak7CaloL2L3L6CorrectorTask = cms.Task(process.ak7CaloL2L3Corrector, process.ak7CaloL2L3L6Corrector, process.ak7CaloL6SLBCorrector)


process.ak4JPTL2L3ResidualCorrectorTask = cms.Task(process.ak4JPTL2L3ResidualCorrector, process.ak4JPTL2RelativeCorrector, process.ak4JPTL3AbsoluteCorrector, process.ak4JPTResidualCorrector, process.ak4L1JPTOffsetCorrectorTask)


process.ak6PFL2L3ResidualCorrectorTask = cms.Task(process.ak6PFL2L3ResidualCorrector, process.ak6PFL2RelativeCorrector, process.ak6PFL3AbsoluteCorrector, process.ak6PFResidualCorrector)


process.ak4PFPuppiL1FastL2L3CorrectorTask = cms.Task(process.ak4PFPuppiL1FastL2L3Corrector, process.ak4PFPuppiL1FastjetCorrector, process.ak4PFPuppiL2RelativeCorrector, process.ak4PFPuppiL3AbsoluteCorrector)


process.kt6PFL2L3ResidualCorrectorTask = cms.Task(process.kt6PFL2L3ResidualCorrector, process.kt6PFL2RelativeCorrector, process.kt6PFL3AbsoluteCorrector, process.kt6PFResidualCorrector)


process.ak7PFL2L3L6CorrectorTask = cms.Task(process.ak7PFL2L3Corrector, process.ak7PFL2L3L6Corrector, process.ak7PFL6SLBCorrector)


process.ic5PFL2L3ResidualCorrectorTask = cms.Task(process.ic5PFL2L3ResidualCorrector, process.ic5PFL2RelativeCorrector, process.ic5PFL3AbsoluteCorrector, process.ic5PFResidualCorrector)


process.ak6PFL2L3CorrectorTask = cms.Task(process.ak6PFL2L3Corrector, process.ak6PFL2RelativeCorrector, process.ak6PFL3AbsoluteCorrector)


process.ak10PFL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak10PFL1FastjetCorrector, process.ak10PFL1FastjetL2L3ResidualCorrector, process.ak10PFL2RelativeCorrector, process.ak10PFL3AbsoluteCorrector, process.ak10PFResidualCorrector)


process.ak3PFCHSL2L3CorrectorTask = cms.Task(process.ak3PFCHSL2L3Corrector, process.ak3PFCHSL2RelativeCorrector, process.ak3PFCHSL3AbsoluteCorrector)


process.ak4PFCHSL1L2L3CorrectorTask = cms.Task(process.ak4PFCHSL1L2L3Corrector, process.ak4PFCHSL1OffsetCorrector, process.ak4PFCHSL2RelativeCorrector, process.ak4PFCHSL3AbsoluteCorrector)


process.ak6PFCHSL1L2L3ResidualCorrectorTask = cms.Task(process.ak6PFCHSL1L2L3ResidualCorrector, process.ak6PFCHSL1OffsetCorrector, process.ak6PFCHSL2RelativeCorrector, process.ak6PFCHSL3AbsoluteCorrector, process.ak6PFCHSResidualCorrector)


process.ak7PFCHSL2L3ResidualCorrectorTask = cms.Task(process.ak7PFCHSL2L3ResidualCorrector, process.ak7PFCHSL2RelativeCorrector, process.ak7PFCHSL3AbsoluteCorrector, process.ak7PFCHSResidualCorrector)


process.ak2PFCHSL2L3ResidualCorrectorTask = cms.Task(process.ak2PFCHSL2L3ResidualCorrector, process.ak2PFCHSL2RelativeCorrector, process.ak2PFCHSL3AbsoluteCorrector, process.ak2PFCHSResidualCorrector)


process.ak10PFCHSL1FastjetL2L3ResidualCorrectorTask = cms.Task(process.ak10PFCHSL1FastjetCorrector, process.ak10PFCHSL1FastjetL2L3ResidualCorrector, process.ak10PFCHSL2RelativeCorrector, process.ak10PFCHSL3AbsoluteCorrector, process.ak10PFCHSResidualCorrector)


process.ak10PFL2L3CorrectorTask = cms.Task(process.ak10PFL2L3Corrector, process.ak10PFL2RelativeCorrector, process.ak10PFL3AbsoluteCorrector)


process.ak7JPTL1L2L3ResidualCorrectorTask = cms.Task(process.ak7JPTL1L2L3ResidualCorrector, process.ak7JPTL2RelativeCorrector, process.ak7JPTL3AbsoluteCorrector, process.ak7JPTResidualCorrector, process.ak7L1JPTOffsetCorrectorTask)


process.ic5CaloL1L2L3CorrectorTask = cms.Task(process.ic5CaloL1L2L3Corrector, process.ic5CaloL1OffsetCorrector, process.ic5CaloL2RelativeCorrector, process.ic5CaloL3AbsoluteCorrector)


process.ak7PFL1FastL2L3L6CorrectorTask = cms.Task(process.ak7CaloL1L2L3Corrector, process.ak7PFL1FastL2L3L6Corrector, process.ak7PFL6SLBCorrector)


process.ak10PFCHSL1L2L3ResidualCorrectorTask = cms.Task(process.ak10PFCHSL1L2L3ResidualCorrector, process.ak10PFCHSL1OffsetCorrector, process.ak10PFCHSL2RelativeCorrector, process.ak10PFCHSL3AbsoluteCorrector, process.ak10PFCHSResidualCorrector)


process.jetCorrectorsTask = cms.Task(process.ak4CaloL1FastL2L3CorrectorTask, process.ak4CaloL1FastL2L3L6CorrectorTask, process.ak4CaloL1FastL2L3ResidualCorrectorTask, process.ak4CaloL1L2L3CorrectorTask, process.ak4CaloL1L2L3ResidualCorrectorTask, process.ak4CaloL2L3CorrectorTask, process.ak4CaloL2L3L6CorrectorTask, process.ak4CaloL2L3ResidualCorrectorTask, process.ak4JPTL1FastL2L3CorrectorTask, process.ak4JPTL1FastL2L3ResidualCorrectorTask, process.ak4JPTL1L2L3CorrectorTask, process.ak4JPTL1L2L3ResidualCorrectorTask, process.ak4JPTL2L3CorrectorTask, process.ak4JPTL2L3ResidualCorrectorTask, process.ak4L1JPTFastjetCorrectorTask, process.ak4L1JPTOffsetCorrectorTask, process.ak4PFCHSL1FastL2L3CorrectorTask, process.ak4PFCHSL1FastL2L3ResidualCorrectorTask, process.ak4PFCHSL1L2L3CorrectorTask, process.ak4PFCHSL1L2L3ResidualCorrectorTask, process.ak4PFCHSL2L3CorrectorTask, process.ak4PFCHSL2L3ResidualCorrectorTask, process.ak4PFL1FastL2L3CorrectorTask, process.ak4PFL1FastL2L3L6CorrectorTask, process.ak4PFL1FastL2L3ResidualCorrectorTask, process.ak4PFL1L2L3CorrectorTask, process.ak4PFL1L2L3ResidualCorrectorTask, process.ak4PFL2L3CorrectorTask, process.ak4PFL2L3L6CorrectorTask, process.ak4PFL2L3ResidualCorrectorTask, process.ak4PFPuppiL1FastL2L3CorrectorTask, process.ak4PFPuppiL1FastL2L3ResidualCorrectorTask, process.ak4PFPuppiL1L2L3CorrectorTask, process.ak4PFPuppiL1L2L3ResidualCorrectorTask, process.ak4PFPuppiL2L3CorrectorTask, process.ak4PFPuppiL2L3ResidualCorrectorTask, process.ak4TrackL2L3CorrectorTask)


process.ak7JPTL1L2L3CorrectorTask = cms.Task(process.ak7JPTL1L2L3Corrector, process.ak7JPTL2RelativeCorrector, process.ak7JPTL3AbsoluteCorrector, process.ak7L1JPTOffsetCorrectorTask)


process.ak7JPTL1FastL2L3ResidualCorrectorTask = cms.Task(process.ak7JPTL1FastL2L3ResidualCorrector, process.ak7JPTL2RelativeCorrector, process.ak7JPTL3AbsoluteCorrector, process.ak7JPTResidualCorrector, process.ak7L1JPTFastjetCorrectorTask)


process.jetCorrectorsAllAlgosTask = cms.Task(process.ak10PFCHSL1FastjetL2L3ResidualCorrectorTask, process.ak10PFCHSL1L2L3ResidualCorrectorTask, process.ak10PFCHSL2L3CorrectorTask, process.ak10PFCHSL2L3ResidualCorrectorTask, process.ak10PFL1FastjetL2L3ResidualCorrectorTask, process.ak10PFL1L2L3ResidualCorrectorTask, process.ak10PFL2L3CorrectorTask, process.ak10PFL2L3ResidualCorrectorTask, process.ak1PFCHSL1FastjetL2L3ResidualCorrectorTask, process.ak1PFCHSL1L2L3ResidualCorrectorTask, process.ak1PFCHSL2L3CorrectorTask, process.ak1PFCHSL2L3ResidualCorrectorTask, process.ak1PFL1FastjetL2L3ResidualCorrectorTask, process.ak1PFL1L2L3ResidualCorrectorTask, process.ak1PFL2L3CorrectorTask, process.ak1PFL2L3ResidualCorrectorTask, process.ak2PFCHSL1FastjetL2L3ResidualCorrectorTask, process.ak2PFCHSL1L2L3ResidualCorrectorTask, process.ak2PFCHSL2L3CorrectorTask, process.ak2PFCHSL2L3ResidualCorrectorTask, process.ak2PFL1FastjetL2L3ResidualCorrectorTask, process.ak2PFL1L2L3ResidualCorrectorTask, process.ak2PFL2L3CorrectorTask, process.ak2PFL2L3ResidualCorrectorTask, process.ak3PFCHSL1FastjetL2L3ResidualCorrectorTask, process.ak3PFCHSL1L2L3ResidualCorrectorTask, process.ak3PFCHSL2L3CorrectorTask, process.ak3PFCHSL2L3ResidualCorrectorTask, process.ak3PFL1FastjetL2L3ResidualCorrectorTask, process.ak3PFL1L2L3ResidualCorrectorTask, process.ak3PFL2L3CorrectorTask, process.ak3PFL2L3ResidualCorrectorTask, process.ak4TrackL1FastL2L3CorrectorTask, process.ak5PFCHSL1FastjetL2L3ResidualCorrectorTask, process.ak5PFCHSL1L2L3ResidualCorrectorTask, process.ak5PFCHSL2L3CorrectorTask, process.ak5PFCHSL2L3ResidualCorrectorTask, process.ak5PFL1FastjetL2L3ResidualCorrectorTask, process.ak5PFL1L2L3ResidualCorrectorTask, process.ak5PFL2L3CorrectorTask, process.ak5PFL2L3ResidualCorrectorTask, process.ak6PFCHSL1FastjetL2L3ResidualCorrectorTask, process.ak6PFCHSL1L2L3ResidualCorrectorTask, process.ak6PFCHSL2L3CorrectorTask, process.ak6PFCHSL2L3ResidualCorrectorTask, process.ak6PFL1FastjetL2L3ResidualCorrectorTask, process.ak6PFL1L2L3ResidualCorrectorTask, process.ak6PFL2L3CorrectorTask, process.ak6PFL2L3ResidualCorrectorTask, process.ak7CaloL1FastL2L3CorrectorTask, process.ak7CaloL1FastL2L3L6CorrectorTask, process.ak7CaloL1FastL2L3ResidualCorrectorTask, process.ak7CaloL1L2L3CorrectorTask, process.ak7CaloL1L2L3ResidualCorrectorTask, process.ak7CaloL2L3CorrectorTask, process.ak7CaloL2L3L6CorrectorTask, process.ak7CaloL2L3ResidualCorrectorTask, process.ak7JPTL1FastL2L3ResidualCorrectorTask, process.ak7JPTL1L2L3CorrectorTask, process.ak7JPTL1L2L3ResidualCorrectorTask, process.ak7JPTL2L3CorrectorTask, process.ak7JPTL6SLBCorrector, process.ak7L1JPTFastjetCorrectorTask, process.ak7L1JPTOffsetCorrectorTask, process.ak7PFCHSL1FastL2L3CorrectorTask, process.ak7PFCHSL1FastjetL2L3ResidualCorrectorTask, process.ak7PFCHSL1L2L3ResidualCorrectorTask, process.ak7PFCHSL2L3CorrectorTask, process.ak7PFCHSL2L3ResidualCorrectorTask, process.ak7PFL1FastL2L3CorrectorTask, process.ak7PFL1FastL2L3L6CorrectorTask, process.ak7PFL1FastjetL2L3ResidualCorrectorTask, process.ak7PFL1L2L3CorrectorTask, process.ak7PFL1L2L3ResidualCorrectorTask, process.ak7PFL2L3CorrectorTask, process.ak7PFL2L3L6CorrectorTask, process.ak7PFL2L3ResidualCorrectorTask, process.ak8PFCHSL1FastjetL2L3ResidualCorrectorTask, process.ak8PFCHSL1L2L3ResidualCorrectorTask, process.ak8PFCHSL2L3CorrectorTask, process.ak8PFCHSL2L3ResidualCorrectorTask, process.ak8PFL1FastjetL2L3ResidualCorrectorTask, process.ak8PFL1L2L3ResidualCorrectorTask, process.ak8PFL2L3CorrectorTask, process.ak8PFL2L3ResidualCorrectorTask, process.ak9PFCHSL1FastjetL2L3ResidualCorrectorTask, process.ak9PFCHSL1L2L3ResidualCorrectorTask, process.ak9PFCHSL2L3CorrectorTask, process.ak9PFCHSL2L3ResidualCorrectorTask, process.ak9PFL1FastjetL2L3ResidualCorrectorTask, process.ak9PFL1L2L3ResidualCorrectorTask, process.ak9PFL2L3CorrectorTask, process.ak9PFL2L3ResidualCorrectorTask, process.ic5CaloL1FastL2L3CorrectorTask, process.ic5CaloL1FastL2L3L6CorrectorTask, process.ic5CaloL1FastL2L3ResidualCorrectorTask, process.ic5CaloL1L2L3CorrectorTask, process.ic5CaloL1L2L3ResidualCorrectorTask, process.ic5CaloL2L3CorrectorTask, process.ic5CaloL2L3L6CorrectorTask, process.ic5CaloL2L3ResidualCorrectorTask, process.ic5PFL1FastL2L3CorrectorTask, process.ic5PFL1FastL2L3L6CorrectorTask, process.ic5PFL1FastL2L3ResidualCorrectorTask, process.ic5PFL1L2L3CorrectorTask, process.ic5PFL1L2L3ResidualCorrectorTask, process.ic5PFL2L3CorrectorTask, process.ic5PFL2L3L6CorrectorTask, process.ic5PFL2L3ResidualCorrectorTask, process.jetCorrectorsTask, process.kt4CaloL1FastL2L3CorrectorTask, process.kt4CaloL1FastL2L3L6CorrectorTask, process.kt4CaloL1FastL2L3ResidualCorrectorTask, process.kt4CaloL1L2L3CorrectorTask, process.kt4CaloL1L2L3ResidualCorrectorTask, process.kt4CaloL2L3CorrectorTask, process.kt4CaloL2L3L6CorrectorTask, process.kt4CaloL2L3ResidualCorrectorTask, process.kt4PFL1FastL2L3CorrectorTask, process.kt4PFL1FastL2L3L6CorrectorTask, process.kt4PFL1FastL2L3ResidualCorrectorTask, process.kt4PFL1L2L3CorrectorTask, process.kt4PFL1L2L3ResidualCorrectorTask, process.kt4PFL2L3CorrectorTask, process.kt4PFL2L3L6CorrectorTask, process.kt4PFL2L3ResidualCorrectorTask, process.kt6CaloL1FastL2L3CorrectorTask, process.kt6CaloL1FastL2L3L6CorrectorTask, process.kt6CaloL1FastL2L3ResidualCorrectorTask, process.kt6CaloL1L2L3CorrectorTask, process.kt6CaloL1L2L3ResidualCorrectorTask, process.kt6CaloL2L3CorrectorTask, process.kt6CaloL2L3L6CorrectorTask, process.kt6CaloL2L3ResidualCorrectorTask, process.kt6PFL1FastL2L3CorrectorTask, process.kt6PFL1FastL2L3L6CorrectorTask, process.kt6PFL1FastL2L3ResidualCorrectorTask, process.kt6PFL1L2L3CorrectorTask, process.kt6PFL1L2L3ResidualCorrectorTask, process.kt6PFL2L3CorrectorTask, process.kt6PFL2L3L6CorrectorTask, process.kt6PFL2L3ResidualCorrectorTask)


process.kt4CaloL1FastL2L3ResidualCorrectorChain = cms.Sequence(process.kt4CaloL1FastL2L3ResidualCorrectorTask)


process.ak1PFL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak1PFL1L2L3ResidualCorrectorTask)


process.ak4L1JPTOffsetCorrectorChain = cms.Sequence(process.ak4L1JPTOffsetCorrectorTask)


process.ic5PFL2L3ResidualCorrectorChain = cms.Sequence(process.ic5PFL2L3ResidualCorrectorTask)


process.ak2PFL2L3CorrectorChain = cms.Sequence(process.ak2PFL2L3CorrectorTask)


process.ak8PFCHSL2L3CorrectorChain = cms.Sequence(process.ak8PFCHSL2L3CorrectorTask)


process.ak3PFL2L3CorrectorChain = cms.Sequence(process.ak3PFL2L3CorrectorTask)


process.ak4PFCHSL1FastL2L3ResidualCorrectorChain = cms.Sequence(process.ak4PFCHSL1FastL2L3ResidualCorrectorTask)


process.ak3PFL2L3ResidualCorrectorChain = cms.Sequence(process.ak3PFL2L3ResidualCorrectorTask)


process.ak4CaloL1L2L3CorrectorChain = cms.Sequence(process.ak4CaloL1L2L3CorrectorTask)


process.ak9PFCHSL2L3CorrectorChain = cms.Sequence(process.ak9PFCHSL2L3CorrectorTask)


process.ak5PFL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak5PFL1FastjetL2L3ResidualCorrectorTask)


process.ak2PFCHSL2L3ResidualCorrectorChain = cms.Sequence(process.ak2PFCHSL2L3ResidualCorrectorTask)


process.kt4CaloL1FastL2L3L6CorrectorChain = cms.Sequence(process.kt4CaloL1FastL2L3L6CorrectorTask)


process.ic5CaloL1FastL2L3CorrectorChain = cms.Sequence(process.ic5CaloL1FastL2L3CorrectorTask)


process.ak4PFL1FastL2L3CorrectorChain = cms.Sequence(process.ak4PFL1FastL2L3CorrectorTask)


process.ak10PFCHSL2L3ResidualCorrectorChain = cms.Sequence(process.ak10PFCHSL2L3ResidualCorrectorTask)


process.ak7PFL2L3ResidualCorrectorChain = cms.Sequence(process.ak7PFL2L3ResidualCorrectorTask)


process.ak3PFL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak3PFL1L2L3ResidualCorrectorTask)


process.ak9PFCHSL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak9PFCHSL1FastjetL2L3ResidualCorrectorTask)


process.ak10PFCHSL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak10PFCHSL1FastjetL2L3ResidualCorrectorTask)


process.ak2PFL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak2PFL1FastjetL2L3ResidualCorrectorTask)


process.ak4PFPuppiL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak4PFPuppiL1L2L3ResidualCorrectorTask)


process.ak2PFCHSL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak2PFCHSL1L2L3ResidualCorrectorTask)


process.ak4JPTL2L3CorrectorChain = cms.Sequence(process.ak4JPTL2L3CorrectorTask)


process.ak4PFL1FastL2L3ResidualCorrectorChain = cms.Sequence(process.ak4PFL1FastL2L3ResidualCorrectorTask)


process.kt6PFL1FastL2L3ResidualCorrectorChain = cms.Sequence(process.kt6PFL1FastL2L3ResidualCorrectorTask)


process.ak4JPTL1L2L3CorrectorChain = cms.Sequence(process.ak4JPTL1L2L3CorrectorTask)


process.ak7CaloL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak7CaloL1L2L3ResidualCorrectorTask)


process.ak1PFCHSL2L3ResidualCorrectorChain = cms.Sequence(process.ak1PFCHSL2L3ResidualCorrectorTask)


process.ak3PFCHSL2L3ResidualCorrectorChain = cms.Sequence(process.ak3PFCHSL2L3ResidualCorrectorTask)


process.ak7CaloL2L3ResidualCorrectorChain = cms.Sequence(process.ak7CaloL2L3ResidualCorrectorTask)


process.ic5CaloL2L3ResidualCorrectorChain = cms.Sequence(process.ic5CaloL2L3ResidualCorrectorTask)


process.ak4JPTL1FastL2L3CorrectorChain = cms.Sequence(process.ak4JPTL1FastL2L3CorrectorTask)


process.ak7JPTL1FastL2L3CorrectorChain = cms.Sequence(process.ak7JPTL1FastL2L3CorrectorTask)


process.kt6PFL1FastL2L3CorrectorChain = cms.Sequence(process.kt6PFL1FastL2L3CorrectorTask)


process.ak4PFCHSL2L3CorrectorChain = cms.Sequence(process.ak4PFCHSL2L3CorrectorTask)


process.ic5PFL1FastL2L3CorrectorChain = cms.Sequence(process.ic5PFL1FastL2L3CorrectorTask)


process.ak5PFCHSL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak5PFCHSL1FastjetL2L3ResidualCorrectorTask)


process.kt6CaloL1FastL2L3CorrectorChain = cms.Sequence(process.kt6CaloL1FastL2L3CorrectorTask)


process.ak10PFL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak10PFL1L2L3ResidualCorrectorTask)


process.kt6PFL1L2L3ResidualCorrectorChain = cms.Sequence(process.kt6PFL1L2L3ResidualCorrectorTask)


process.ak6PFL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak6PFL1FastjetL2L3ResidualCorrectorTask)


process.ak4PFL1FastL2L3L6CorrectorChain = cms.Sequence(process.ak4PFL1FastL2L3L6CorrectorTask)


process.ak9PFCHSL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak9PFCHSL1L2L3ResidualCorrectorTask)


process.ak8PFL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak8PFL1L2L3ResidualCorrectorTask)


process.ak2PFCHSL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak2PFCHSL1FastjetL2L3ResidualCorrectorTask)


process.ak6PFCHSL2L3ResidualCorrectorChain = cms.Sequence(process.ak6PFCHSL2L3ResidualCorrectorTask)


process.ak4JPTL1FastL2L3ResidualCorrectorChain = cms.Sequence(process.ak4JPTL1FastL2L3ResidualCorrectorTask)


process.ak4PFL2L3L6CorrectorChain = cms.Sequence(process.ak4PFL2L3L6CorrectorTask)


process.ak7L1JPTOffsetCorrectorChain = cms.Sequence(process.ak7L1JPTOffsetCorrectorTask)


process.kt4PFL2L3ResidualCorrectorChain = cms.Sequence(process.kt4PFL2L3ResidualCorrectorTask)


process.ak6PFCHSL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak6PFCHSL1FastjetL2L3ResidualCorrectorTask)


process.ak7CaloL1FastL2L3CorrectorChain = cms.Sequence(process.ak7CaloL1FastL2L3CorrectorTask)


process.kt4PFL1FastL2L3ResidualCorrectorChain = cms.Sequence(process.kt4PFL1FastL2L3ResidualCorrectorTask)


process.ic5CaloL2L3L6CorrectorChain = cms.Sequence(process.ic5CaloL2L3L6CorrectorTask)


process.ak7PFL2L3CorrectorChain = cms.Sequence(process.ak7PFL2L3CorrectorTask)


process.kt4CaloL2L3ResidualCorrectorChain = cms.Sequence(process.kt4CaloL2L3ResidualCorrectorTask)


process.kt6CaloL2L3L6CorrectorChain = cms.Sequence(process.kt6CaloL2L3L6CorrectorTask)


process.ic5CaloL1L2L3CorrectorChain = cms.Sequence(process.ic5CaloL1L2L3CorrectorTask)


process.kt6CaloL2L3CorrectorChain = cms.Sequence(process.kt6CaloL2L3CorrectorTask)


process.ak4CaloL1FastL2L3ResidualCorrectorChain = cms.Sequence(process.ak4CaloL1FastL2L3ResidualCorrectorTask)


process.ak5PFCHSL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak5PFCHSL1L2L3ResidualCorrectorTask)


process.ak4CaloL2L3L6CorrectorChain = cms.Sequence(process.ak4CaloL2L3L6CorrectorTask)


process.ak7PFCHSL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak7PFCHSL1L2L3ResidualCorrectorTask)


process.kt6CaloL2L3ResidualCorrectorChain = cms.Sequence(process.kt6CaloL2L3ResidualCorrectorTask)


process.ak7PFL2L3L6CorrectorChain = cms.Sequence(process.ak7PFL2L3L6CorrectorTask)


process.ak5PFL2L3CorrectorChain = cms.Sequence(process.ak5PFL2L3CorrectorTask)


process.kt4PFL1FastL2L3L6CorrectorChain = cms.Sequence(process.kt4PFL1FastL2L3L6CorrectorTask)


process.ic5PFL1FastL2L3ResidualCorrectorChain = cms.Sequence(process.ic5PFL1FastL2L3ResidualCorrectorTask)


process.ic5PFL2L3CorrectorChain = cms.Sequence(process.ic5PFL2L3CorrectorTask)


process.kt4CaloL1L2L3ResidualCorrectorChain = cms.Sequence(process.kt4CaloL1L2L3ResidualCorrectorTask)


process.ak6PFL2L3CorrectorChain = cms.Sequence(process.ak6PFL2L3CorrectorTask)


process.kt4PFL1L2L3ResidualCorrectorChain = cms.Sequence(process.kt4PFL1L2L3ResidualCorrectorTask)


process.ak9PFL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak9PFL1FastjetL2L3ResidualCorrectorTask)


process.kt4CaloL2L3L6CorrectorChain = cms.Sequence(process.kt4CaloL2L3L6CorrectorTask)


process.ak4TrackL1FastL2L3CorrectorChain = cms.Sequence(process.ak4TrackL1FastL2L3CorrectorTask)


process.ak8PFCHSL2L3ResidualCorrectorChain = cms.Sequence(process.ak8PFCHSL2L3ResidualCorrectorTask)


process.ak10PFL2L3CorrectorChain = cms.Sequence(process.ak10PFL2L3CorrectorTask)


process.ak7JPTL2L3CorrectorChain = cms.Sequence(process.ak7JPTL2L3CorrectorTask)


process.ak4PFPuppiL2L3CorrectorChain = cms.Sequence(process.ak4PFPuppiL2L3CorrectorTask)


process.ak8PFCHSL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak8PFCHSL1L2L3ResidualCorrectorTask)


process.ak4PFL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak4PFL1L2L3ResidualCorrectorTask)


process.ak4PFCHSL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak4PFCHSL1L2L3ResidualCorrectorTask)


process.ak4CaloL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak4CaloL1L2L3ResidualCorrectorTask)


process.ak7CaloL1FastL2L3ResidualCorrectorChain = cms.Sequence(process.ak7CaloL1FastL2L3ResidualCorrectorTask)


process.ak4PFL2L3ResidualCorrectorChain = cms.Sequence(process.ak4PFL2L3ResidualCorrectorTask)


process.ak4PFPuppiL1L2L3CorrectorChain = cms.Sequence(process.ak4PFPuppiL1L2L3CorrectorTask)


process.ak2PFCHSL2L3CorrectorChain = cms.Sequence(process.ak2PFCHSL2L3CorrectorTask)


process.ak6PFL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak6PFL1L2L3ResidualCorrectorTask)


process.ak10PFL2L3ResidualCorrectorChain = cms.Sequence(process.ak10PFL2L3ResidualCorrectorTask)


process.ak4L1JPTFastjetCorrectorChain = cms.Sequence(process.ak4L1JPTFastjetCorrectorTask)


process.kt6PFL2L3CorrectorChain = cms.Sequence(process.kt6PFL2L3CorrectorTask)


process.ak4PFL1L2L3CorrectorChain = cms.Sequence(process.ak4PFL1L2L3CorrectorTask)


process.ak4PFCHSL1FastL2L3CorrectorChain = cms.Sequence(process.ak4PFCHSL1FastL2L3CorrectorTask)


process.ic5CaloL1FastL2L3ResidualCorrectorChain = cms.Sequence(process.ic5CaloL1FastL2L3ResidualCorrectorTask)


process.ak9PFL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak9PFL1L2L3ResidualCorrectorTask)


process.ak7PFL1FastL2L3CorrectorChain = cms.Sequence(process.ak7PFL1FastL2L3CorrectorTask)


process.ak5PFL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak5PFL1L2L3ResidualCorrectorTask)


process.kt4PFL2L3L6CorrectorChain = cms.Sequence(process.kt4PFL2L3L6CorrectorTask)


process.ak10PFL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak10PFL1FastjetL2L3ResidualCorrectorTask)


process.ak2PFL2L3ResidualCorrectorChain = cms.Sequence(process.ak2PFL2L3ResidualCorrectorTask)


process.ak1PFCHSL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak1PFCHSL1L2L3ResidualCorrectorTask)


process.kt6PFL2L3ResidualCorrectorChain = cms.Sequence(process.kt6PFL2L3ResidualCorrectorTask)


process.ak7JPTL1L2L3CorrectorChain = cms.Sequence(process.ak7JPTL1L2L3CorrectorTask)


process.ak7PFL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak7PFL1FastjetL2L3ResidualCorrectorTask)


process.ak4TrackL2L3CorrectorChain = cms.Sequence(process.ak4TrackL2L3CorrectorTask)


process.ak6PFCHSL2L3CorrectorChain = cms.Sequence(process.ak6PFCHSL2L3CorrectorTask)


process.ak3PFCHSL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak3PFCHSL1L2L3ResidualCorrectorTask)


process.ak3PFL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak3PFL1FastjetL2L3ResidualCorrectorTask)


process.kt6CaloL1L2L3ResidualCorrectorChain = cms.Sequence(process.kt6CaloL1L2L3ResidualCorrectorTask)


process.ak7PFCHSL1FastL2L3CorrectorChain = cms.Sequence(process.ak7PFCHSL1FastL2L3CorrectorTask)


process.ak5PFCHSL2L3CorrectorChain = cms.Sequence(process.ak5PFCHSL2L3CorrectorTask)


process.ak4PFPuppiL1FastL2L3ResidualCorrectorChain = cms.Sequence(process.ak4PFPuppiL1FastL2L3ResidualCorrectorTask)


process.ak8PFL2L3ResidualCorrectorChain = cms.Sequence(process.ak8PFL2L3ResidualCorrectorTask)


process.ak7CaloL2L3CorrectorChain = cms.Sequence(process.ak7CaloL2L3CorrectorTask)


process.ak4PFCHSL2L3ResidualCorrectorChain = cms.Sequence(process.ak4PFCHSL2L3ResidualCorrectorTask)


process.ak1PFL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak1PFL1FastjetL2L3ResidualCorrectorTask)


process.ic5CaloL1FastL2L3L6CorrectorChain = cms.Sequence(process.ic5CaloL1FastL2L3L6CorrectorTask)


process.ak3PFCHSL2L3CorrectorChain = cms.Sequence(process.ak3PFCHSL2L3CorrectorTask)


process.ak1PFCHSL2L3CorrectorChain = cms.Sequence(process.ak1PFCHSL2L3CorrectorTask)


process.ak7CaloL1L2L3CorrectorChain = cms.Sequence(process.ak7CaloL1L2L3CorrectorTask)


process.ak7CaloL2L3L6CorrectorChain = cms.Sequence(process.ak7CaloL2L3L6CorrectorTask)


process.ak7JPTL1FastL2L3ResidualCorrectorChain = cms.Sequence(process.ak7JPTL1FastL2L3ResidualCorrectorTask)


process.ak8PFL2L3CorrectorChain = cms.Sequence(process.ak8PFL2L3CorrectorTask)


process.ak1PFL2L3ResidualCorrectorChain = cms.Sequence(process.ak1PFL2L3ResidualCorrectorTask)


process.ic5CaloL2L3CorrectorChain = cms.Sequence(process.ic5CaloL2L3CorrectorTask)


process.ak2PFL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak2PFL1L2L3ResidualCorrectorTask)


process.ak4CaloL1FastL2L3CorrectorChain = cms.Sequence(process.ak4CaloL1FastL2L3CorrectorTask)


process.kt4CaloL2L3CorrectorChain = cms.Sequence(process.kt4CaloL2L3CorrectorTask)


process.ak9PFL2L3CorrectorChain = cms.Sequence(process.ak9PFL2L3CorrectorTask)


process.ak10PFCHSL2L3CorrectorChain = cms.Sequence(process.ak10PFCHSL2L3CorrectorTask)


process.ak4JPTL2L3ResidualCorrectorChain = cms.Sequence(process.ak4JPTL2L3ResidualCorrectorTask)


process.kt4PFL1FastL2L3CorrectorChain = cms.Sequence(process.kt4PFL1FastL2L3CorrectorTask)


process.kt6CaloL1FastL2L3L6CorrectorChain = cms.Sequence(process.kt6CaloL1FastL2L3L6CorrectorTask)


process.ak4PFPuppiL2L3ResidualCorrectorChain = cms.Sequence(process.ak4PFPuppiL2L3ResidualCorrectorTask)


process.kt4CaloL1FastL2L3CorrectorChain = cms.Sequence(process.kt4CaloL1FastL2L3CorrectorTask)


process.ic5PFL1L2L3ResidualCorrectorChain = cms.Sequence(process.ic5PFL1L2L3ResidualCorrectorTask)


process.ak3PFCHSL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak3PFCHSL1FastjetL2L3ResidualCorrectorTask)


process.kt6CaloL1L2L3CorrectorChain = cms.Sequence(process.kt6CaloL1L2L3CorrectorTask)


process.ak4PFCHSL1L2L3CorrectorChain = cms.Sequence(process.ak4PFCHSL1L2L3CorrectorTask)


process.ak10PFCHSL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak10PFCHSL1L2L3ResidualCorrectorTask)


process.ak1PFCHSL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak1PFCHSL1FastjetL2L3ResidualCorrectorTask)


process.ak1PFL2L3CorrectorChain = cms.Sequence(process.ak1PFL2L3CorrectorTask)


process.ak8PFL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak8PFL1FastjetL2L3ResidualCorrectorTask)


process.ak7JPTL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak7JPTL1L2L3ResidualCorrectorTask)


process.kt6PFL1L2L3CorrectorChain = cms.Sequence(process.kt6PFL1L2L3CorrectorTask)


process.ic5PFL2L3L6CorrectorChain = cms.Sequence(process.ic5PFL2L3L6CorrectorTask)


process.ak4CaloL2L3CorrectorChain = cms.Sequence(process.ak4CaloL2L3CorrectorTask)


process.ak5PFL2L3ResidualCorrectorChain = cms.Sequence(process.ak5PFL2L3ResidualCorrectorTask)


process.ak4JPTL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak4JPTL1L2L3ResidualCorrectorTask)


process.ak7PFL1L2L3CorrectorChain = cms.Sequence(process.ak7PFL1L2L3CorrectorTask)


process.kt6PFL2L3L6CorrectorChain = cms.Sequence(process.kt6PFL2L3L6CorrectorTask)


process.ak4PFPuppiL1FastL2L3CorrectorChain = cms.Sequence(process.ak4PFPuppiL1FastL2L3CorrectorTask)


process.ak7PFCHSL2L3ResidualCorrectorChain = cms.Sequence(process.ak7PFCHSL2L3ResidualCorrectorTask)


process.ak7PFCHSL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak7PFCHSL1FastjetL2L3ResidualCorrectorTask)


process.ic5PFL1FastL2L3L6CorrectorChain = cms.Sequence(process.ic5PFL1FastL2L3L6CorrectorTask)


process.kt4CaloL1L2L3CorrectorChain = cms.Sequence(process.kt4CaloL1L2L3CorrectorTask)


process.ak7CaloL1FastL2L3L6CorrectorChain = cms.Sequence(process.ak7CaloL1FastL2L3L6CorrectorTask)


process.kt4PFL1L2L3CorrectorChain = cms.Sequence(process.kt4PFL1L2L3CorrectorTask)


process.ak7PFL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak7PFL1L2L3ResidualCorrectorTask)


process.ak5PFCHSL2L3ResidualCorrectorChain = cms.Sequence(process.ak5PFCHSL2L3ResidualCorrectorTask)


process.kt6PFL1FastL2L3L6CorrectorChain = cms.Sequence(process.kt6PFL1FastL2L3L6CorrectorTask)


process.kt6CaloL1FastL2L3ResidualCorrectorChain = cms.Sequence(process.kt6CaloL1FastL2L3ResidualCorrectorTask)


process.ic5PFL1L2L3CorrectorChain = cms.Sequence(process.ic5PFL1L2L3CorrectorTask)


process.ak6PFL2L3ResidualCorrectorChain = cms.Sequence(process.ak6PFL2L3ResidualCorrectorTask)


process.ak6PFCHSL1L2L3ResidualCorrectorChain = cms.Sequence(process.ak6PFCHSL1L2L3ResidualCorrectorTask)


process.ak7L1JPTFastjetCorrectorChain = cms.Sequence(process.ak7L1JPTFastjetCorrectorTask)


process.ak9PFL2L3ResidualCorrectorChain = cms.Sequence(process.ak9PFL2L3ResidualCorrectorTask)


process.ak4CaloL1FastL2L3L6CorrectorChain = cms.Sequence(process.ak4CaloL1FastL2L3L6CorrectorTask)


process.ak7PFCHSL2L3CorrectorChain = cms.Sequence(process.ak7PFCHSL2L3CorrectorTask)


process.ak7PFL1FastL2L3L6CorrectorChain = cms.Sequence(process.ak7PFL1FastL2L3L6CorrectorTask)


process.kt4PFL2L3CorrectorChain = cms.Sequence(process.kt4PFL2L3CorrectorTask)


process.ic5CaloL1L2L3ResidualCorrectorChain = cms.Sequence(process.ic5CaloL1L2L3ResidualCorrectorTask)


process.ak8PFCHSL1FastjetL2L3ResidualCorrectorChain = cms.Sequence(process.ak8PFCHSL1FastjetL2L3ResidualCorrectorTask)


process.ak4CaloL2L3ResidualCorrectorChain = cms.Sequence(process.ak4CaloL2L3ResidualCorrectorTask)


process.ak4PFL2L3CorrectorChain = cms.Sequence(process.ak4PFL2L3CorrectorTask)


process.ak9PFCHSL2L3ResidualCorrectorChain = cms.Sequence(process.ak9PFCHSL2L3ResidualCorrectorTask)


process.p = cms.Path(process.pileupJetIdUpdated+process.leptonVeto+process.prefiringweight+process.clusteringAnalyzerAll_nom)


process.pathRunPatAlgos = cms.Path(process.patAlgosToolsTask)


