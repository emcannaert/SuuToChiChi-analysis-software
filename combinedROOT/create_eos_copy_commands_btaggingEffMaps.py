import os, sys
import pickle
import numpy as np



if __name__=="__main__":
	#try:
	"""
	# keeping track of how many copy commands have already been made for each of the samples and systematics
	nCommands	= {  "2015": { "QCDMC2000toInf": { 'JEC':0,'JER':0,'nom':0  },     #nCommands[year][sample][systematic]
					 "QCDMC1500to2000":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-hadronsMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToHadronicMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToSemiLeptonicMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToLeptonicMC":{ 'JEC':0,'JER':0,'nom':0  }, 
					 "TTbarMCHT1200to2500":{ 'JEC':0,'JER':0,'nom':0 },
					 "TTbarMCHT2500toInf":{ 'JEC':0,'JER':0,'nom':0 },
					 "ST_t-channel-antitop_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_t-channel-top_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-leptonsMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-antiTop_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-top_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "dataB-ver2":{'JEC':0,'JER':0,'nom':0 } ,
					 "dataC-HIPM":{ 'JEC':0,'JER':0,'nom':0 } ,
					 "dataD-HIPM":{'JEC':0,'JER':0,'nom':0 } ,
					 "dataF-HIPM":{'JEC':0,'JER':0,'nom':0 } , 
					 "dataE-HIPM":{ 'JEC':0,'JER':0,'nom':0  }} , 
					 "2016": { "QCDMC2000toInf": { 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1500to2000":{ 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToHadronicMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToSemiLeptonicMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToLeptonicMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTbarMCHT1200to2500":{ 'JEC':0,'JER':0,'nom':0 },
					 "TTbarMCHT2500toInf":{ 'JEC':0,'JER':0,'nom':0 },
					 "ST_t-channel-antitop_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_t-channel-top_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-hadronsMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-leptonsMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-antiTop_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-top_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					  "dataF":{ 'JEC':0,'JER':0,'nom':0  } ,
					 "dataG":{ 'JEC':0,'JER':0,'nom':0  } ,
					 "dataH":{ 'JEC':0,'JER':0,'nom':0  }  } ,
					 "2017": { "QCDMC2000toInf": { 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1500to2000":{ 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToHadronicMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToSemiLeptonicMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToLeptonicMC":{ 'JEC':0,'JER':0,'nom':0    },
					 "TTbarMCHT1200to2500":{'JEC':0,'JER':0,'nom':0 },
					 "TTbarMCHT2500toInf":{'JEC':0,'JER':0,'nom':0 },
					  "ST_t-channel-antitop_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_t-channel-top_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-hadronsMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-leptonsMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-antiTop_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-top_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "dataB":{ 'JEC':0,'JER':0,'nom':0  } ,
					 "dataC":{ 'JEC':0,'JER':0,'nom':0   } ,
					 "dataD":{ 'JEC':0,'JER':0,'nom':0  } ,
					 "dataE":{ 'JEC':0,'JER':0,'nom':0  } , 
					 "dataF":{ 'JEC':0,'JER':0,'nom':0  }  } ,
					 "2018": { "QCDMC2000toInf": { 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1500to2000":{ 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToHadronicMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToSemiLeptonicMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToLeptonicMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTbarMCHT1200to2500":{ 'JEC':0,'JER':0,'nom':0 },
					 "TTbarMCHT2500toInf":{ 'JEC':0,'JER':0,'nom':0 },
					 "ST_t-channel-antitop_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_t-channel-top_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-hadronsMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-leptonsMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-antiTop_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-top_inclMC":{ 'JEC':0,'JER':0,'nom':0  },
					  "dataA":{ 'JEC':0,'JER':0,'nom':0  }   ,
					 "dataB":{ 'JEC':0,'JER':0,'nom':0  } ,
					 "dataC":{ 'JEC':0,'JER':0,'nom':0  } ,
					 "dataD":{'JEC':0,'JER':0,'nom':0  }  } }
	all_files_made	= {  "2015": { "QCDMC2000toInf": { 'JEC':[],'JER':[],'nom':[]  },     #nCommands[year][sample][systematic]
					 "QCDMC1500to2000":{ 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToHadronicMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToSemiLeptonicMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToLeptonicMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTbarMCHT1200to2500":{'JEC':[],'JER':[],'nom':[] },
					 "TTbarMCHT2500toInf":{'JEC':[],'JER':[],'nom':[] },
					 "ST_t-channel-antitop_inclMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_t-channel-top_inclMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-hadronsMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-leptonsMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-antiTop_inclMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-top_inclMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "dataB-ver2":{ 'JEC':[],'JER':[],'nom':[]  } ,
					 "dataC-HIPM":{ 'JEC':[],'JER':[],'nom':[]  } ,
					 "dataD-HIPM":{ 'JEC':[],'JER':[],'nom':[]  } ,
					 "dataE-HIPM":{ 'JEC':[],'JER':[],'nom':[]  } , 
					 "dataF-HIPM":{ 'JEC':[],'JER':[],'nom':[]  }  }, 
					 "2016": { "QCDMC2000toInf": { 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1500to2000":{ 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToHadronicMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToSemiLeptonicMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToLeptonicMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTbarMCHT1200to2500":{'JEC':[],'JER':[],'nom':[] },
					 "TTbarMCHT2500toInf":{'JEC':[],'JER':[],'nom':[] },
					 "ST_t-channel-antitop_inclMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_t-channel-top_inclMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-hadronsMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-leptonsMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-antiTop_inclMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-top_inclMC":{ 'JEC':[],'JER':[],'nom':[]  } ,
					 "dataF":{ 'JEC':[],'JER':[],'nom':[]  } ,
					 "dataG":{ 'JEC':[],'JER':[],'nom':[]  } ,
					 "dataH":{ 'JEC':[],'JER':[],'nom':[]  } } ,
					 "2017": { "QCDMC2000toInf": { 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1500to2000":{ 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToHadronicMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToSemiLeptonicMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToLeptonicMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTbarMCHT1200to2500":{'JEC':[],'JER':[],'nom':[] },
					 "TTbarMCHT2500toInf":{'JEC':[],'JER':[],'nom':[] },
					 "ST_t-channel-antitop_inclMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_t-channel-top_inclMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-hadronsMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-leptonsMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-antiTop_inclMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-top_inclMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "dataB":{ 'JEC':[],'JER':[],'nom':[]  } ,
					 "dataC":{ 'JEC':[],'JER':[],'nom':[]  } ,
					 "dataD":{ 'JEC':[],'JER':[],'nom':[]  } ,
					 "dataE":{ 'JEC':[],'JER':[],'nom':[]  } , 
					 "dataF":{ 'JEC':[],'JER':[],'nom':[]  } } ,

					 "2018": { "QCDMC2000toInf": { 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1500to2000":{ 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToHadronicMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToSemiLeptonicMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToLeptonicMC":{ 'JEC':[],'JER':[],'nom':[]  } ,
					 "TTbarMCHT1200to2500":{'JEC':[],'JER':[],'nom':[] },
					 "TTbarMCHT2500toInf":{'JEC':[],'JER':[],'nom':[] },
					 "ST_t-channel-antitop_inclMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_t-channel-top_inclMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-antiTop_inclMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-hadronsMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-leptonsMC":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-top_inclMC":{ 'JEC':[],'JER':[],'nom':[]  }  , 
					 "dataA":{ 'JEC':[],'JER':[],'nom':[]  }   ,
					 "dataB":{ 'JEC':[],'JER':[],'nom':[]  } ,
					 "dataC":{ 'JEC':[],'JER':[],'nom':[]  } ,
					 "dataD":{ 'JEC':[],'JER':[],'nom':[]  } }}"""

	nCommands	= {  
				
					"2015": 
					{ "QCDMC": { 'JEC':0,'JER':0,'nom':0  },     #nCommands[year][sample][systematic]
					 "TTbarMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "STMC":{ 'JEC':0,'JER':0,'nom':0  }
					 },
					 "2016": 
					{ "QCDMC": { 'JEC':0,'JER':0,'nom':0  },     #nCommands[year][sample][systematic]
					 "TTbarMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "STMC":{ 'JEC':0,'JER':0,'nom':0  }
					 },
					 "2017": 
					{ "QCDMC": { 'JEC':0,'JER':0,'nom':0  },     #nCommands[year][sample][systematic]
					 "TTbarMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "STMC":{ 'JEC':0,'JER':0,'nom':0  }
					 },
					 "2018": 
					{ "QCDMC": { 'JEC':0,'JER':0,'nom':0  },     #nCommands[year][sample][systematic]
					 "TTbarMC":{ 'JEC':0,'JER':0,'nom':0  },
					 "STMC":{ 'JEC':0,'JER':0,'nom':0  }
					 }

			}


	all_files_made	= {  
					"2015": 
					 { 
					 "QCDMC": { 'JEC':[],'JER':[],'nom':[]  },
					 "TTbarMC":{ 'JEC':[],'JER':[],'nom':[] },
					 "STMC":{ 'JEC':[],'JER':[],'nom':[]  }
					 },
					 "2016": 
					 { 
					 "QCDMC": { 'JEC':[],'JER':[],'nom':[]  },
					 "TTbarMC":{ 'JEC':[],'JER':[],'nom':[] },
					 "STMC":{ 'JEC':[],'JER':[],'nom':[]  }
					 } ,
					 "2017": 
					 { 
					 "QCDMC": { 'JEC':[],'JER':[],'nom':[]  },
					 "TTbarMC":{ 'JEC':[],'JER':[],'nom':[] },
					 "STMC":{ 'JEC':[],'JER':[],'nom':[]  }
					 },
					 "2018": 
					 { 
					  "QCDMC": { 'JEC':[],'JER':[],'nom':[]  },
					 "TTbarMC":{ 'JEC':[],'JER':[],'nom':[] },
					 "STMC":{ 'JEC':[],'JER':[],'nom':[]  }
					 } 
				}
	#samples = ["QCD", "TTbar_HT","ST_"] 
	samples = ["QCDMC", "TTbarMC","STMC"] 

	
	
	

	signal_samples_pkl = open('../signal_samples.pkl', 'r')
  	signal_samples     = pickle.load(signal_samples_pkl)
	signal_samples = np.array(signal_samples)

  	signal_nCommands_pkl = open('../signal_nCommands.pkl', 'r')
  	signal_nCommands     = pickle.load(signal_nCommands_pkl)
	signal_nCommands["2015"]["SuuToChiChi"] = {'JEC':0,'JER':0,'nom':0  }
	signal_nCommands["2016"]["SuuToChiChi"] = {'JEC':0,'JER':0,'nom':0  }
	signal_nCommands["2017"]["SuuToChiChi"] = {'JEC':0,'JER':0,'nom':0  }
	signal_nCommands["2018"]["SuuToChiChi"] = {'JEC':0,'JER':0,'nom':0  }

	signal_files_made_pkl = open('../signal_files_made.pkl', 'r')
  	signal_files_made     = pickle.load(signal_files_made_pkl)

  	signal_files_made["2015"]["SuuToChiChi"] = { 'JEC':[],'JER':[],'nom':[]  }
  	signal_files_made["2016"]["SuuToChiChi"] = { 'JEC':[],'JER':[],'nom':[]  }
  	signal_files_made["2017"]["SuuToChiChi"] = { 'JEC':[],'JER':[],'nom':[]  }
  	signal_files_made["2018"]["SuuToChiChi"] = { 'JEC':[],'JER':[],'nom':[]  }



	years = ["2015","2016","2017","2018"]
	eos_path = open(sys.argv[1], "r")
	command_path = open("eos_copy_commands_btagging.sh", "w")
	for line in eos_path:
		if line.split() == "[]" or line == "\n" or line == "":
			continue
		num_str = ""
		year_str = ""
		sys_str = ""
		sample_str = ""
		if "QCD" in line:
			sample_str = "QCDMC"
		elif "TTJets_HT" in line:
			sample_str = "TTbarMC"
		elif "TTTo" in line:
			sample_str = "TTbarMC"
		elif "ST_" in line:
			sample_str = "STMC"
		for sample in signal_samples:
			if sample in line:
				sample_str = "SuuToChiChi"
		if "JEC" in line:
			sys_str = "JEC"
		elif "JER" in line:
					sys_str = "JER"
		else:   #nominal systematic calculations
			sys_str = "nom"
		if sys_str	!= "nom":
			print("ERROR: systematic should be 'nom' for b tagging eff maps. Skipping")
			continue
		for year in years:
			if "_%s/"%year in line:
				year_str = year		
		if sample_str == "" or year_str == "":
			print("ERROR: (Found %s, %s)Can't figure out what type of file this is (QCD,TTbar,etc.) or what the year is: "%(year_str,sample_str))
			print(line.strip())
			continue

		if "Suu" in sample_str:
			num_str = "%s"%(signal_nCommands[year_str][sample_str][sys_str])
			#print("num/year/sys/sample = %s/%s/%s/%s"%(num_str,year_str,sys_str,sample_str))
			signal_files_made[year_str][sample_str][sys_str].append("btagging_efficiencyMap_%s_combined_%s_%s.root"%(sample_str, year_str, num_str))
			signal_nCommands[year_str][sample_str][sys_str]+=1
		else:
			num_str = "%s"%(nCommands[year_str][sample_str][sys_str])
			all_files_made[year_str][sample_str][sys_str].append("btagging_efficiencyMap_%s_combined_%s_%s.root"%(sample_str, year_str, num_str))
			nCommands[year_str][sample_str][sys_str]+=1
		pipe = '|'
		command_path.write(r'hadd -f btagging_efficiencyMap_%s_combined_%s_%s.root `xrdfsls -u %s %s grep "\.root"`'%(sample_str, year_str, num_str,line.strip(),pipe) + "\n")

	### now add to this .sh script a section that combines all files together into a single "_combined.root", renames files to this if they don't need to be added together
	for year,year_dict in all_files_made.items():
		for sample, sample_dict in year_dict.items():
			for syst,syst_dict in sample_dict.items():
				combined_file_name = "btagging_efficiencyMap_RAW_%s_combined_%s.root"%(sample, year)
				if len(syst_dict) > 1:    # if there are actually files in this 
					command_path.write('hadd -f %s '%combined_file_name)
					for iii,one_file in enumerate(syst_dict):
						command_path.write(" %s"%one_file.strip()) 
						if iii == (len(syst_dict)-1):
							command_path.write("\n")
				elif len(syst_dict) == 1:
					## rename the one file 
					command_path.write("mv %s %s\n"%(syst_dict[0], combined_file_name) )

	## merge together the signal files
	for year,year_dict in signal_files_made.items():
		for sample, sample_dict in year_dict.items():
			for syst,syst_dict in sample_dict.items():
				combined_file_name = "btagging_efficiencyMap_RAW_%s_combined_%s.root"%(sample, year)

				if len(syst_dict) > 1:    # if there are actually files in this 
					command_path.write('hadd -f %s '%combined_file_name)
					for iii,one_file in enumerate(syst_dict):
						command_path.write(" %s"%one_file.strip()) 
						if iii == (len(syst_dict)-1):
							command_path.write("\n")
				elif len(syst_dict) == 1:
					## rename the one file 
					command_path.write("mv %s %s\n"%(syst_dict[0], combined_file_name) )

	#except:
	#	print("Enter in a valid text file with a list of the files you want to copy from EOS (no spaces in between)")
	#	pass
