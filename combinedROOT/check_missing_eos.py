import os, sys
import pickle
import numpy as np

def convert_to_bytes(size_str):
	# Define mapping of unit abbreviations to their corresponding multiplier


	try:
		file_size = float(size_str)
		return(file_size)
	except:

		units = {'B': 1, 'K': 1024, 'M': 1024**2, 'G': 1024**3, 'T': 1024**4}
		


		"""
		# Find the index where the unit abbreviation starts
		for i, char in enumerate(size_str):
			if not char.isdigit():
				break
		
		# Extract numeric value and unit abbreviation
		size = size_str[:i]
		unit = size_str[i:].strip()
		"""
		#### NOT ROBUST TO BYTES because this assumes the units are the last 2 characters
		unit = size_str[-1:]
		size = size_str[:-1]
		#rint(size_str)
		#print(size, unit)
		
		# Convert size to bytes using the appropriate multiplier
		bytes_size = float(size) * units[unit.upper()]
		
		return bytes_size



if __name__ == "__main__":


	with open("all_combined_eos_files.txt",'r') as f:
		all_files_combined = f.readlines()

	with open("all_skimmed_eos_files.txt", 'r') as f:
		all_files_skimmed = f.readlines()

	with open("all_processed_eos_files.txt", 'r') as f:
		all_files_processed = f.readlines()

	with open("all_eos_crab_files.txt",'r') as f:
		all_files_crab = f.readlines()


	with open("all_cutflow_eos_files.txt",'r') as f:
		all_files_cutflow = f.readlines()


	years = ["2015", "2016", "2017", "2018"]

	


	### all_files_combined   INDEX 4 is the file size   
	### all_skimmed_eos_files index 4 is file size
	### all_files_processed   index 4 is the file size
	### all_files_crab		index 3 is the file size


	data_samples = { "2015":["dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM" ,"dataF-HIPM"],   # "dataB-ver1"  has been blacklisted
					"2016": ["dataF","dataG"]  ,
					"2017": ["dataB","dataC","dataD","dataE","dataF"]  ,
					"2018": ["dataA","dataB", "dataC", "dataD"]}


	samples = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf",
	   "ST_t-channel-top_inclMC",
	   "ST_t-channel-antitop_inclMC",
	   "ST_s-channel-hadronsMC",
	   "ST_s-channel-leptonsMC",
	   "ST_tW-antiTop_inclMC",
	   "ST_tW-top_inclMC",
		"QCDMC_Pt_170to300",
            "QCDMC_Pt_300to470",
            "QCDMC_Pt_470to600",
            "QCDMC_Pt_600to800",
            "QCDMC_Pt_800to1000",
            "QCDMC_Pt_1000to1400",
            "QCDMC_Pt_1400to1800",
            "QCDMC_Pt_1800to2400",
            "QCDMC_Pt_2400to3200",
            "QCDMC_Pt_3200toInf" 

	    ]


	signal_samples_pkl = open('../data/pkl/signal_samples.pkl', 'r')
	signal_samples	 = pickle.load(signal_samples_pkl)
	signal_samples = np.array(signal_samples)
	samples.extend(signal_samples)

	output_file = open("missing_files.txt",'w')



	####### check missing crab eos files 

	print("Now checking the crab output eos directory.")
	missing_files_crab = 0
	total_files_crab = 0
	missing_files_crab_list = []

	output_file.write("####################  CRAB EOS FILES ###################  \n")
	for year in years:
		samples = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf",
	   "ST_t-channel-top_inclMC",
	   "ST_t-channel-antitop_inclMC",
	   "ST_s-channel-hadronsMC",
	   "ST_s-channel-leptonsMC",
	   "ST_tW-antiTop_inclMC",
	   "ST_tW-top_inclMC",
	   	"QCDMC_Pt_170to300",
            "QCDMC_Pt_300to470",
            "QCDMC_Pt_470to600",
            "QCDMC_Pt_600to800",
            "QCDMC_Pt_800to1000",
            "QCDMC_Pt_1000to1400",
            "QCDMC_Pt_1400to1800",
            "QCDMC_Pt_1800to2400",
            "QCDMC_Pt_2400to3200",
            "QCDMC_Pt_3200toInf"  ]
   		use_samples = samples
		use_samples.extend(data_samples[year])
		use_samples.extend( signal_samples )
		for sample in use_samples:
			systematics = ["nom","JEC1", "JEC2", "JER"]
			if "data" in sample:
				systematics = ["nom"]
			elif "Suu" in sample:
				systematics = ["nom","JEC1"]
			for systematic in systematics:
				total_files_crab+=1
				if "Suu" in sample:
					file_sample = "clustAlg_%s_%s_%s"%(sample, year,systematic)
				else:
					file_sample = "clustAlg_%s_%s_%s"%(sample, year, systematic)
				if len([file for file in all_files_crab if file_sample in file]) == 0:
					output_file.write("MISSING: %s\n"%file_sample)
					missing_files_crab_list.append(file_sample)
					missing_files_crab+=1



	print("For eos crab output: found %i missing files out of the expected %i files."%(missing_files_crab, total_files_crab) )
	print("Missing EOS Crab files:")
	for file in missing_files_crab_list:
		print("----- %s"%file)

	print("")
	print("")
	print("")
	output_file.write("\n")
	output_file.write("\n")
	output_file.write("\n")

	####### check missing combined files 
	missing_files_combined = 0
	total_files_combined = 0
	missing_files_list_combined = []
	bad_files_list_combined     = []
	output_file.write("####################  COMBINED FILES ###################  \n")
	for year in years:
		samples = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf",
	   "ST_t-channel-top_inclMC",
	   "ST_t-channel-antitop_inclMC",
	   "ST_s-channel-hadronsMC",
	   "ST_s-channel-leptonsMC",
	   "ST_tW-antiTop_inclMC",
	   "ST_tW-top_inclMC",
	   	"QCDMC_Pt_170to300",
            "QCDMC_Pt_300to470",
            "QCDMC_Pt_470to600",
            "QCDMC_Pt_600to800",
            "QCDMC_Pt_800to1000",
            "QCDMC_Pt_1000to1400",
            "QCDMC_Pt_1400to1800",
            "QCDMC_Pt_1800to2400",
            "QCDMC_Pt_2400to3200",
            "QCDMC_Pt_3200toInf"  ]
   		use_samples = samples
		use_samples.extend(data_samples[year])
		use_samples.extend( signal_samples )
		for sample in use_samples:
			systematics = ["nom","JEC1","JEC2", "JER"]
			if "data" in sample:
				systematics = ["nom"]
			if "Suu" in sample:
				systematics = ["nom","JEC1"]
			for systematic in systematics:
				total_files_combined+=1
				combined_file  = "%s_%s_%s_combined.root"%(sample, year, systematic)
				if len([file for file in all_files_combined if combined_file in file and convert_to_bytes(file.split()[4])>5000 ] )	 == 0:

					### try to see if the file size is very small
					output_file.write("MISSING: %s\n"%combined_file)
					missing_files_list_combined.append(combined_file)
					missing_files_combined+=1
				elif len([file for file in all_files_combined if combined_file in file and convert_to_bytes(file.split()[4]) < 5000 ] )   == 1:
					### try to see if the file size is very small
					output_file.write("BAD FILE: %s\n"%combined_file)
					bad_files_list_combined.append(combined_file)
					missing_files_combined+=1

	print("For combined files: found %i missing files out of the expected %i files."%(missing_files_combined, total_files_combined) )
	print("Missing/bad combined files:")
	for file in missing_files_list_combined:
		print("----- %s"%file)
	for file in bad_files_list_combined:
		print("BAD FILE ----- %s"%file)

	print("")
	print("")
	print("")
	output_file.write("\n")
	output_file.write("\n")
	output_file.write("\n")



	####### check missing skimmed files 
	print("Checking skimmed files.")
	output_file.write("####################  SKIMMED FILES ###################  \n")
	missing_files_list_skimmed = []
	bad_files_list_skimmed 	   = []

	missing_files_skimmed = 0
	total_files_skimmed = 0
	for year in years:
		samples = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf",
	   "ST_t-channel-top_inclMC",
	   "ST_t-channel-antitop_inclMC",
	   "ST_s-channel-hadronsMC",
	   "ST_s-channel-leptonsMC",
	   "ST_tW-antiTop_inclMC",
	   "ST_tW-top_inclMC",
	   	"QCDMC_Pt_170to300",
            "QCDMC_Pt_300to470",
            "QCDMC_Pt_470to600",
            "QCDMC_Pt_600to800",
            "QCDMC_Pt_800to1000",
            "QCDMC_Pt_1000to1400",
            "QCDMC_Pt_1400to1800",
            "QCDMC_Pt_1800to2400",
            "QCDMC_Pt_2400to3200",
            "QCDMC_Pt_3200toInf"  ]
		use_samples = samples
		use_samples.extend( signal_samples )
		use_samples.extend(data_samples[year])
		for sample in use_samples:
			systematics = ["nom","JEC1", "JEC2","JER"]
			if "data" in sample:
				systematics = ["nom"]
			if "Suu" in sample:
				systematics = ["nom","JEC"]
			for systematic in systematics:
				total_files_skimmed+=1
				skimmed_file   = "%s_%s_%s_SKIMMED.root"%(sample, year, systematic)
				if systematic == "nom" and "Suu" in sample: skimmed_file   = "%s_%s_SKIMMED.root"%(sample, year)
				if len([file for file in all_files_skimmed if skimmed_file in file and convert_to_bytes(file.split()[4]) > 1000 ]) == 0:
					output_file.write("MISSING: %s\n"%skimmed_file)
					missing_files_list_skimmed.append(skimmed_file)
					missing_files_skimmed+=1
				elif len([file for file in all_files_skimmed if skimmed_file in file and convert_to_bytes(file.split()[4]) < 1000  ]) == 1:
					output_file.write("BAD FILE: %s\n"%skimmed_file)
					bad_files_list_skimmed.append(skimmed_file)
					missing_files_skimmed+=1

	print("For skimmed files: found %i missing files out of the expected %i files."%(missing_files_skimmed, total_files_skimmed) )
	print("Missing/bad skimmed files:")
	for file in missing_files_list_skimmed:
		print("----- %s"%file)
	for file in bad_files_list_skimmed:
		print("BAD FILE ----- %s"%file)
	print("")
	print("")
	print("")
	output_file.write("\n")
	output_file.write("\n")
	output_file.write("\n")



	"""
	####### check cutflow files 
	print("Checking cutflow files.")
	output_file.write("####################  CUTFLOW FILES ###################  \n")
	missing_files_list_cutflow = []
	bad_files_list_cutflow 	   = []

	missing_files_cutflow = 0
	total_files_cutflow = 0
	for year in years:
		samples = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf",
	   "ST_t-channel-top_inclMC",
	   "ST_t-channel-antitop_inclMC",
	   "ST_s-channel-hadronsMC",
	   "ST_s-channel-leptonsMC",
	   "ST_tW-antiTop_inclMC",
	   "ST_tW-top_inclMC" ]
		use_samples = samples
		use_samples.extend( signal_samples )
		use_samples.extend(data_samples[year])
		for sample in use_samples:
			systematics = ["nom","JEC","JER"]
			if "data" in sample:
				systematics = ["nom","JEC"]
			if "Suu" in sample:
				systematics = ["nom","JEC"]
			for systematic in systematics:
				total_files_cutflow+=1
				cutflow_file   = "%s_%s_%s_CUTFLOW.root"%(sample, year, systematic)
				if len([file for file in all_files_cutflow if cutflow_file in file and convert_to_bytes(file.split()[4]) > 1000 ]) == 0:
					output_file.write("MISSING: %s\n"%cutflow_file)
					missing_files_list_cutflow.append(cutflow_file)
					missing_files_cutflow+=1
				elif len([file for file in all_files_cutflow if cutflow_file in file and convert_to_bytes(file.split()[4]) < 1000  ]) == 1:
					output_file.write("BAD FILE: %s\n"%cutflow_file)
					bad_files_list_cutflow.append(cutflow_file)
					missing_files_cutflow+=1

	print("For cutflow files: found %i missing files out of the expected %i files."%(missing_files_cutflow, total_files_cutflow) )
	print("Missing/bad cutflow files:")
	for file in missing_files_list_cutflow:
		print("----- %s"%file)
	for file in bad_files_list_cutflow:
		print("BAD FILE ----- %s"%file)
	print("")
	print("")
	print("")
	output_file.write("\n")
	output_file.write("\n")
	output_file.write("\n")
	"""





	####### check missing processed files 
	print("Checking processed files.")

	output_file.write("####################  PROCESSED FILES ###################  \n")
	missing_files_list_processed = []
	bad_files_list_processed = []
	missing_files_processed = 0
	total_files_processed = 0
	for year in years:
		samples = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf",
	   "ST_t-channel-top_inclMC",
	   "ST_t-channel-antitop_inclMC",
	   "ST_s-channel-hadronsMC",
	   "ST_s-channel-leptonsMC",
	   "ST_tW-antiTop_inclMC",
	   "ST_tW-top_inclMC",
	   	"QCDMC_Pt_170to300",
            "QCDMC_Pt_300to470",
            "QCDMC_Pt_470to600",
            "QCDMC_Pt_600to800",
            "QCDMC_Pt_800to1000",
            "QCDMC_Pt_1000to1400",
            "QCDMC_Pt_1400to1800",
            "QCDMC_Pt_1800to2400",
            "QCDMC_Pt_2400to3200",
            "QCDMC_Pt_3200toInf" ]
		use_samples = samples
		use_samples.extend( signal_samples )
		use_samples.extend(data_samples[year])
		for sample in use_samples:			
			total_files_processed+=1
			processed_file   = "%s_%s_processed.root"%(sample, year)
			if len([file for file in all_files_processed if (processed_file in file and convert_to_bytes(file.split()[4]) > 1000)  ]) == 0:
				output_file.write("MISSING: %s\n"%processed_file)
				missing_files_list_processed.append(processed_file)
				missing_files_processed+=1
			elif len([file for file in all_files_processed if (processed_file in file and convert_to_bytes(file.split()[4]) < 1000)  ]) == 1:
				output_file.write("BAD FILE: %s\n"%processed_file)
				bad_files_list_processed.append(processed_file)
				missing_files_processed+=1

	print("For processed files: found %i missing files out of the expected %i files."%(missing_files_processed, total_files_processed) )
	print("Missing/bad processsed files:")
	for file in missing_files_list_processed:
		print("MISSING  ----- %s"%file)
	for file in bad_files_list_processed:
		print("BAD FILE ----- %s"%file)




	print("")
	print("")
	print("")
	print("Finished.")


	output_file.close()


