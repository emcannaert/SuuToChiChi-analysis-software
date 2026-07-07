def return_BR_SF(year=None,sample=None):


	scale_factor = None
	scale_factors = {

	"QCDMC1000to1500":{"2015":1.578683216,"2016":1.482632755,"2017":3.126481451,"2018":4.407417122},
	"QCDMC1500to2000":{"2015":0.2119142341,"2016":0.195224041,"2017":0.3197450474,"2018":0.5425809983},
	"QCDMC2000toInf":{"2015":0.08568186031,"2016":0.07572795371,"2017":0.14306915,"2018":0.2277769275},
	"TTToHadronicMC":{"2015":0.075592,"2016":0.05808655696,"2017":0.06651018525,"2018":0.06588049107},
	"TTToSemiLeptonicMC":{"2015":0.05395328118,"2016":0.05808655696,"2017":0.04264829286,"2018":0.04563489275},
	"TTToLeptonicMC":{"2015":0.0459517611,"2016":0.03401684391,"2017":0.03431532926,"2018":0.03617828025},


	"TTJetsMCHT800to1200":{"2015":0.002137308181,"2016": 0.001871995162,"2017":0.002223731308,"2018":0.003628684991},
	"TTJetsMCHT1200to2500":{"2015":0.002042984813,"2016":0.001692694262,"2017":0.002008181033,"2018": 0.002940685631},
	"TTJetsMCHT2500toInf" :{"2015":0.00004537431961,"2016":0.00004014592771,"2017":0.00004751010609,"2018": 0.00006717610111},

	"ST_t_channel_top_inclMC":{"2015":0.0409963154,"2016":0.03607115071,"2017":0.03494669125,"2018":0.03606630944},
	"ST_t_channel_antitop_inclMC":{"2015":0.05673857623,"2016":0.04102705994,"2017":0.04239405723,"2018":0.0432463179},
	"ST_s_channel_hadronsMC":{"2015":0.02950427234,"2016":0.0225317434,"2017":0.02519226684,"2018":0.02593083521},
	"ST_s_channel_leptonsMC":{"2015":0.01255463574,"2016":0.01090453116,"2017":0.0106045613,"2018":0.01096440571},
	"ST_tW_antiTop_inclMC":{"2015":0.2759109565,"2016":0.213975372,"2017":0.2376656327,"2018":0.2510095883},
	"ST_tW_top_inclMC":{"2015":0.2754017391,"2016":0.2189821357,"2017":0.2382768632,"2018":0.2440275892},

	"WJetsMC_LNu_HT800to1200":{"2015":0.03835596838,"2016":0.03889064865,"2017":0.04015548052,"2018":0.04033876768},
	"WJetsMC_LNu_HT1200to2500":{"2015":0.01068088067,"2016":0.00932744847,"2017":0.009642548403,"2018":0.01063395334},
	"WJetsMC_LNu_HT2500toInf":{"2015":0.000638718653,"2016":0.0006268975665,"2017":0.00092566562,"2018":0.0007547032677},
	"WJetsMC_QQ_HT800toInf":{"2015":0.072501767,"2016":0.07139611301,"2017":0.08198843981,"2018":0.128194465},

	"WW_MC":{"2015":0.09385207138,"2016":0.08101652866,"2017":0.2023058718,"2018":0.2909648256},
	"ZZ_MC":{"2015":0.1848461778,"2016":0.1773009557,"2017":0.1860928307,"2018":0.2059943846},

    "QCDMC_Pt_170to300":     {"2015":72.27560548, "2016":58.25025062, "2017":144.709, "2018":208.2638833},
    "QCDMC_Pt_300to470":     {"2015":2.455876959, "2016":2.070224016, "2017":5.087240079, "2018":7.056447936},
    "QCDMC_Pt_470to600":     {"2015":0.2118747588, "2016":0.1767988093, "2017":0.4499746487, "2018":0.63037786},
    "QCDMC_Pt_600to800":     {"2015":0.0493575163, "2016":0.04047024029, "2017":0.09517517327, "2018":0.1387891509},
    "QCDMC_Pt_800to1000":    {"2015":0.01442283334, "2016":0.01167917262, "2017":0.02940368664, "2018":0.04237689989},
    "QCDMC_Pt_1000to1400":   {"2015":0.007638349845, "2016":0.006308397848, "2017":0.01572930994, "2018":0.02274328434},
    "QCDMC_Pt_1400to1800":   {"2015":0.001151147636, "2016":0.001017034788, "2017":0.002421867564, "2018":0.003529762976},
    "QCDMC_Pt_1800to2400":   {"2015":0.0003239978715, "2016":0.0002804021008, "2017":0.0006628637026, "2018":0.0009495874158},
    "QCDMC_Pt_2400to3200":   {"2015":0.00003408677559, "2016":0.00003091080407, "2017":0.0000725380981, "2018":0.0001046476009},
    "QCDMC_Pt_3200toInf":    {"2015":0.000002639104, "2016":0.000002281839357, "2017":0.000005583208, "2018":0.000008071067},

	 }

	if year == None and sample==None:
		return scale_factors
	else:
		if "QCD" in sample:
			if "QCDMC_Pt" in sample:
				scale_factor = scale_factors[sample][year]
			elif "1000to1500" in sample:
				scale_factor = scale_factors["QCDMC1000to1500"][year]
			elif "1500to2000" in sample:
				scale_factor = scale_factors["QCDMC1500to2000"][year]
			elif "2000toInf" in sample:
				scale_factor = scale_factors["QCDMC2000toInf"][year]
			elif "QCD_Pt" in sample:
				sample = sample.replace("QCD_Pt","QCDMC_Pt")
				scale_factor = scale_factors[sample][year]
			else:
				print("ERROR in return_BR_SF: Sample name not found: %s"%sample)
				return
		elif "TTTo" in sample:
			if "Hadronic" in sample:
				scale_factor = scale_factors["TTToHadronicMC"][year]
			elif "SemiLeptonic" in sample:
				scale_factor = scale_factors["TTToSemiLeptonicMC"][year]
			elif "TTToLeptonic" in sample:
				scale_factor = scale_factors["TTToLeptonicMC"][year]
			else: 
				print("ERROR: Sample name not found: %s"%sample)
		elif "TTJets" in sample:

			if "1200to2500" in sample:
				scale_factor = scale_factors["TTJetsMCHT1200to2500"][year]
			elif "2500toInf" in sample:
				scale_factor = scale_factors["TTJetsMCHT2500toInf"][year]
			elif "800to1200" in sample:
				scale_factor = scale_factors["TTJetsMCHT800to1200"][year]
			else: 
				print("ERROR: Sample name not found: %s"%sample)
		elif "ST_" in sample:
			if "t_channel_top_incl" in sample:
				scale_factor = scale_factors["ST_t_channel_top_inclMC"][year]
			elif "t_channel_antitop_inc":
				scale_factor = scale_factors["ST_t_channel_antitop_inclMC"][year]
			elif "s_channel_hadrons":
				scale_factor = scale_factors["ST_s_channel_hadronsMC"][year]
			elif "s_channel_leptons":
				scale_factor = scale_factors["ST_s_channel_leptonsMC"][year]
			elif "tW_antiTop_incl":
				scale_factor = scale_factors["ST_tW_antiTop_inclMC"][year]
			elif "tW_top_incl":
				scale_factor = scale_factors["ST_tW_top_inclMC"][year]
			else:
				print("ERROR: Sample name not found: %s"%sample)
		elif "WJets" in sample:
			if  "WJetsMC_QQ_HT800toInf"      in sample: scale_factor = scale_factors["WJetsMC_QQ_HT800toInf"][year]
			elif  "WJetsMC_LNu_HT800to1200"  in sample: scale_factor = scale_factors["WJetsMC_LNu_HT800to1200"][year]
			elif  "WJetsMC_LNu_HT1200to2500" in sample: scale_factor = scale_factors["WJetsMC_LNu_HT1200to2500"][year]
			elif  "WJetsMC_LNu_HT2500toInf"  in sample: scale_factor = scale_factors["WJetsMC_LNu_HT2500toInf"][year]
			else: print("ERROR: didn't find %s in WJetsMC options"%(sample))
		elif "WW_MC" in sample:
			scale_factor =  scale_factors["WW_MC"][year]
		elif "ZZ_MC" in sample:
			scale_factor =  scale_factors["ZZ_MC"][year]

		else:
			print("MC sample type not found: %s"%sample, " - assumed to be data.")


		if not scale_factor: raise ValueError("ERROR: background label %s not recognized."%(sample))

		return scale_factor