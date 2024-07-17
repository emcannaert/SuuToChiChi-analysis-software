import os, sys




if __name__=="__main__":
	#try:

	# keeping track of how many copy commands have already been made for each of the samples and systematics

	nCommands	= {  "2015": { "QCDMC2000toInf": { 'JEC':0,'JER':0,'nom':0  },     #nCommands[year][sample][systematic]
					 "QCDMC1500to2000":{ 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToHadronic":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToSemiLeptonic":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToLeptonic":{ 'JEC':0,'JER':0,'nom':0  }, 
					 "ST_t-channel-antitop_incl":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_t-channel-top_incl":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-hadrons":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-leptons":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-antiTop_incl":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-top_incl":{ 'JEC':0,'JER':0,'nom':0  }  }, 
					 "2016": { "QCDMC2000toInf": { 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1500to2000":{ 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToHadronic":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToSemiLeptonic":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToLeptonic":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_t-channel-antitop_incl":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_t-channel-top_incl":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-hadrons":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-leptons":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-antiTop_incl":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-top_incl":{ 'JEC':0,'JER':0,'nom':0  }  } ,
					 "2017": { "QCDMC2000toInf": { 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1500to2000":{ 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToHadronic":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToSemiLeptonic":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToLeptonic":{ 'JEC':0,'JER':0,'nom':0    },
					  "ST_t-channel-antitop_incl":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_t-channel-top_incl":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-hadrons":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-leptons":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-antiTop_incl":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-top_incl":{ 'JEC':0,'JER':0,'nom':0  }  } ,
					 "2018": { "QCDMC2000toInf": { 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1500to2000":{ 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToHadronic":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToSemiLeptonic":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToLeptonic":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_t-channel-antitop_incl":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_t-channel-top_incl":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-hadrons":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_s-channel-leptons":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-antiTop_incl":{ 'JEC':0,'JER':0,'nom':0  },
					 "ST_tW-top_incl":{ 'JEC':0,'JER':0,'nom':0  }   } }
	all_files_made	= {  "2015": { "QCDMC2000toInf": { 'JEC':[],'JER':[],'nom':[]  },     #nCommands[year][sample][systematic]
					 "QCDMC1500to2000":{ 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToHadronic":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToSemiLeptonic":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToLeptonic":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_t-channel-antitop_incl":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_t-channel-top_incl":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-hadrons":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-leptons":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-antiTop_incl":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-top_incl":{ 'JEC':[],'JER':[],'nom':[]  }  }, 
					 "2016": { "QCDMC2000toInf": { 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1500to2000":{ 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToHadronic":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToSemiLeptonic":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToLeptonic":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_t-channel-antitop_incl":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_t-channel-top_incl":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-hadrons":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-leptons":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-antiTop_incl":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-top_incl":{ 'JEC':[],'JER':[],'nom':[]  }   } ,
					 "2017": { "QCDMC2000toInf": { 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1500to2000":{ 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToHadronic":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToSemiLeptonic":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToLeptonic":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_t-channel-antitop_incl":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_t-channel-top_incl":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-hadrons":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-leptons":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-antiTop_incl":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-top_incl":{ 'JEC':[],'JER':[],'nom':[]  }    } ,
					 "2018": { "QCDMC2000toInf": { 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1500to2000":{ 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToHadronic":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToSemiLeptonic":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToLeptonic":{ 'JEC':[],'JER':[],'nom':[]  } ,
					 "ST_t-channel-antitop_incl":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_t-channel-top_incl":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-antiTop_incl":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-hadrons":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_s-channel-leptons":{ 'JEC':[],'JER':[],'nom':[]  },
					 "ST_tW-top_incl":{ 'JEC':[],'JER':[],'nom':[]  }   } }


	samples = ["QCDMC2000toInf","QCDMC1500to2000","QCDMC1000to1500","TTToHadronic", "TTToLeptonic", "TTToSemiLeptonic","ST_t-channel-antitop_incl", "ST_t-channel-top_incl", "ST_tW-antiTop_incl","ST_tW-top_incl",
	"ST_s-channel-hadrons",
	"ST_s-channel-leptons"
	]
	years = ["2015","2016","2017","2018"]
	eos_path = open(sys.argv[1], "r")
	command_path = open("eos_copy_commands.sh", "w")
	for line in eos_path:
		if line.split() == "[]" or line == "\n" or line == "":
			continue
		num_str = ""
		year_str = ""
		sys_str = ""
		sample_str = ""
		for sample in samples:
			if sample in line:
				sample_str = sample
		if "JEC" in line:
			sys_str = "JEC"
		elif "JER" in line:
					sys_str = "JER"
		else:   #nominal systematic calculations
			sys_str = "nom"
		for year in years:
			if year in line:
				year_str = year		
		if sample_str == "" or year_str == "":
			print("Can't figure out what type of file this is (QCD,TTbar,etc.) or what the year is: ")
			print(line.strip())
			continue
		#print("num/year/sys/sample = %s/%s/%s/%s"%(num_str,year_str,sys_str,sample_str))
		num_str = "%s"%nCommands[year_str][sample_str][sys_str]
		all_files_made[year_str][sample_str][sys_str].append("%s_%s_%s_combined_%s_.root"%(sample_str, year_str, sys_str, num_str))

		pipe = '|'
		command_path.write(r'hadd  %s_%s_%s_combined_%s_.root `xrdfsls -u %s %s grep "\.root"`'%(sample_str, year_str, sys_str, num_str,line.strip(),pipe) + "\n")
		nCommands[year_str][sample_str][sys_str]+=1

	#print(all_files_made)
	### now add to this .sh script a section that combines all files together into a single "_combined.root", renames files to this if they don't need to be added together
	for year,year_dict in all_files_made.items():
		for sample, sample_dict in year_dict.items():
			for syst,syst_dict in sample_dict.items():
				combined_file_name = "%s_%s_%s_combined.root"%(sample, year, syst)
				if len(syst_dict) > 1:    # if there are actually files in this 
					command_path.write('hadd %s '%combined_file_name)
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
