import os, sys
import pickle
import numpy as np
if __name__ == "__main__":


	with open("all_eos_files.txt",'r') as f:
		all_files = f.readlines()

	with open("all_eos_crab_files.txt",'r') as f:
		all_files_crab = f.readlines()
	years = ["2015", "2016", "2017", "2018"]

	
	data_samples = { "2015":["dataB-ver1","dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM" ,"dataF-HIPM"],
					"2016": ["dataF","dataG"]  ,
					"2017": ["dataB","dataC","dataD","dataE","dataF"]  ,
					"2018": ["dataA","dataB", "dataC", "dataD"]}

	signal_samples_pkl = open('../signal_samples.pkl', 'r')
	signal_samples     = pickle.load(signal_samples_pkl)
	signal_samples = np.array(signal_samples)
	mising_files_list = []
	#samples.extend(signal_samples)
	missing_files = 0
	total_files = 0
	output_file = open("missing_eos_files.txt",'w')
	for year in years:
		
		samples = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTToHadronicMC","TTToSemiLeptonicMC","TTToLeptonicMC",
   "ST_t-channel-top_inclMC",
   "ST_t-channel-antitop_inclMC",
   "ST_s-channel-hadronsMC",
   "ST_s-channel-leptonsMC",
   "ST_tW-antiTop_inclMC",
   "ST_tW-top_inclMC" ]
   		use_samples = samples
		use_samples.extend(data_samples[year])
		for sample in use_samples:
			systematics = ["nom","JEC","JER"]
			if "data" in sample:
				systematics = ["nom","JEC"]
			for systematic in systematics:
				total_files+=1
				file_sample = "%s_%s_%s_combined.root"%(sample, year, systematic)
				if len([file for file in all_files if file_sample in file]) == 0:
					output_file.write("MISSING: %s\n"%file_sample)
					mising_files_list.append(file_sample)
					missing_files+=1

	print("For combinedROOT: found %i missing files out of the expected %i files."%(missing_files, total_files) )
	print("Missing files:")
	print(mising_files_list)
	output_file.close()

	print("Now checking the crab output eos directory.")

	missing_files_crab = 0
	total_files_crab = 0
	missing_files_crab_list = []
	output_file_crab = open("missing_eos_crab_files.txt",'w')
	for year in years:
		
		samples = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTToHadronicMC","TTToSemiLeptonicMC","TTToLeptonicMC",
   "ST_t-channel-top_inclMC",
   "ST_t-channel-antitop_inclMC",
   "ST_s-channel-hadronsMC",
   "ST_s-channel-leptonsMC",
   "ST_tW-antiTop_inclMC",
   "ST_tW-top_inclMC" ]
   		use_samples = samples
		use_samples.extend(data_samples[year])
		for sample in use_samples:
			systematics = ["nom","JEC","JER"]
			if "data" in sample:
				systematics = ["nom","JEC"]
			for systematic in systematics:
				total_files_crab+=1
				use_systematic = systematic
				if systematic == "nom":
					use_systematic = ""
				if "Suu" in sample:
					file_sample = "clustAlg_%s_%s"%(sample, year)
				else:
					file_sample = "clustAlg_%s_%s_%s"%(sample, year, use_systematic)
				if len([file for file in all_files_crab if file_sample in file]) == 0:
					output_file_crab.write("MISSING: %s\n"%file_sample)
					missing_files_crab_list.append(file_sample)
					missing_files_crab+=1
	print("For eos crab output: found %i missing files out of the expected %i files."%(missing_files_crab, total_files_crab) )
	print(missing_files_crab_list)
	output_file_crab.close()
#clustAlg_Suu8_chi2_WBZT_2018_    #signal
#clustAlg_TTToHadronicMC_2016_



