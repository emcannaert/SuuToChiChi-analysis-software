def get_file_info(file_name):
	sample_str = ""
	year_str =  ""
	syst_str =  ""
	samples = ["QCDMC2000toInf","QCDMC1500to2000","QCDMC1000to1500","TTToHadronic", "QCD2000toInf","QCD1500to2000","QCD1000to1500","QCDMC_HT2000toInf","QCDMC_HT1000to1500","QCDMC_HT1500to2000","TTTohadronic","QCDMCHT2000toInf", "TTToHadronic", "TTToSemiLeptonic", "TTToLeptonic", 
	"ST_t-channel-top_incl",
	"ST_t-channel-antitop_incl",
	"ST_s-channel-hadrons",
	"ST_s-channel-leptons",
	"ST_tW-antiTop_incl",
	"ST_tW-top_incl",
	"ST_MC_All",
	"TTbarMC_All",
	"QCDMC_All",
	"dataA",
	"dataB",
	"dataC",
	"dataD",
	"dataE",
	"dataF",
	"dataG",
	"dataH",
	"QCDMC_combined",
	"STMC_combined",
	"TTbarMC_combined",
	"SuuToChiChi"]
	years = ["2015","2016","2017","2018"]
	systematics = ["JEC","JER","nom"]
	for sample in samples:
		if sample in file_name:
			sample_str = sample
	for year in years:
		if year in file_name:
			year_str = year
	for systematic in systematics:
		if systematic in file_name:
			syst_str = systematic
	return year_str,sample_str,syst_str
