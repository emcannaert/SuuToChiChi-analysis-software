def return_BR_SF(year=None,sample=None):


	scale_factor = None
	scale_factors = {

	"QCDMC1000to1500":{"2015":1.578683216,"2016":1.482632755,"2017":3.126481451,"2018":4.407417122},
	"QCDMC1500to2000":{"2015":0.2119142341,"2016":0.195224041,"2017":0.3197450474,"2018":0.5425809983},
	"QCDMC2000toInf":{"2015":0.08568186031,"2016":0.07572795371,"2017":0.14306915,"2018":0.2277769275},
	"TTToHadronicMC":{"2015":0.075592,"2016":0.05808655696,"2017":0.06651018525,"2018":0.06588049107},
	"TTToSemiLeptonicMC":{"2015":0.05395328118,"2016":0.05808655696,"2017":0.04264829286,"2018":0.04563489275},
	"TTToLeptonicMC":{"2015":0.0459517611,"2016":0.03401684391,"2017":0.03431532926,"2018":0.03617828025},


	"TTJetsMCHT800to1200":{"2015":0.002884466085,"2016": 0.002526405224,"2017":0.003001100916,"2018":0.004897196802},
	"TTJetsMCHT1200to2500":{"2015":0.002722324842,"2016":0.002255554525,"2017":0.00267594799,"2018": 0.003918532089},
	"TTJetsMCHT2500toInf" :{"2015":0.000056798633,"2016":0.000050253843,"2017":0.00005947217,"2018": 0.000084089656},

	"ST_t_channel_top_inclMC":{"2015":0.0409963154,"2016":0.03607115071,"2017":0.03494669125,"2018":0.03859114659},
	"ST_t_channel_antitop_inclMC":{"2015":0.05673857623,"2016":0.04102705994,"2017":0.04238814865,"2018":0.03606630944},
	
	"ST_s_channel_hadronsMC":{"2015":0.04668187234,"2016":0.03564988679,"2017":0.03985938616,"2018":0.04102795437},
	"ST_s_channel_leptonsMC":{"2015":0.01323030083,"2016":0.01149139097,"2017":0.01117527734,"2018":0.01155448784},
	"ST_tW_antiTop_inclMC":{"2015":0.2967888696,"2016":0.2301666797,"2017":0.2556495594,"2018":0.2700032391},
	"ST_tW_top_inclMC":{"2015":0.2962796522,"2016":0.2355829386,"2017":0.2563403788,"2018":0.2625270613},

	"WJetsMC_LNu_HT800to1200":{"2015":0.04172270958,"2016":0.04230432205,"2017":0.04374224695,"2018":0.04394190568},
	"WJetsMC_LNu_HT1200to2500":{"2015":0.01068088067,"2016":0.00932744847,"2017":0.009709510545,"2018":0.01070780024},
	"WJetsMC_LNu_HT2500toInf":{"2015":0.0001931363546,"2016":0.0001895618832,"2017":0.0002799036518,"2018":0.0007547032677},
	"WJetsMC_QQ_HT800toInf":{"2015":0.072501767,"2016":0.07139611301,"2017":0.08100232455,"2018":0.128194465},

	"WW_MC":{"2015":0.09385207138,"2016":0.08101652866,"2017":0.2023058718,"2018":0.2909648256},
	"ZZ_MC":{"2015":0.1848461778,"2016":0.1773009557,"2017":0.1860928307,"2018":0.2059943846},

    "QCDMC_Pt_170to300":     {"2015":72.27560548, "2016":58.13790684, "2017":144.0132837, "2018":208.6671047},
    "QCDMC_Pt_300to470":     {"2015":2.464537119, "2016":2.077524247, "2017":5.087240079, "2018":7.056447936},
    "QCDMC_Pt_470to600":     {"2015":0.2122207081, "2016":0.1770874866, "2017":0.4500561659, "2018":0.6298074855},
    "QCDMC_Pt_600to800":     {"2015":0.04929452011, "2016":0.04041858714, "2017":0.09634485522, "2018":0.1387005244},
    "QCDMC_Pt_800to1000":    {"2015":0.01443931658, "2016":0.01169252025, "2017":0.02954986175, "2018":0.04231249731},
    "QCDMC_Pt_1000to1400":   {"2015":0.007643465954, "2016":0.006312623165, "2017":0.01566430413, "2018":0.0226523112},
    "QCDMC_Pt_1400to1800":   {"2015":0.001150615273, "2016":0.001016564447, "2017":0.00244639185, "2018":0.003532486979},
    "QCDMC_Pt_1800to2400":   {"2015":0.000324331737, "2016":0.0002806910428, "2017":0.0006608229592, "2018":0.000952638299},
    "QCDMC_Pt_2400to3200":   {"2015":0.00003408026676, "2016":0.00003090490169, "2017":0.00007246889556, "2018":0.0001045278212},
    "QCDMC_Pt_3200toInf":    {"2015":0.000002648864, "2016":0.000002290278112, "2017":0.000005628836, "2018":0.000008118931},

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