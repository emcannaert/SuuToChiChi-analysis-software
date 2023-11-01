import os, sys




if __name__=="__main__":
	#try:
	# keeping track of how many copy commands have already been made for each of the samples and systematics

	nCommands	= {  "2015": { 
					"JetHT_dataB-ver1": { 'JEC':0,'JER':0,'nom':0  },     #nCommands[year][sample][systematic]
					 "JetHT_dataB-ver2":{ 'JEC':0,'JER':0,'nom':0  },
					 "JetHT_dataC-HIPM":{ 'JEC':0,'JER':0,'nom':0  },
					 "JetHT_dataD-HIPM":{ 'JEC':0,'JER':0,'nom':0  }, 
					 "JetHT_dataE-HIPM":{ 'JEC':0,'JER':0,'nom':0  },
					 "JetHT_dataF-HIPM":{ 'JEC':0,'JER':0,'nom':0  } ,
					"QCDMC2000toInf": { 'JEC':0,'JER':0,'nom':0  },     #nCommands[year][sample][systematic]
					 "QCDMC1500to2000":{ 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToHadronic":{ 'JEC':0,'JER':0,'nom':0  }   }, 
					 "2016": { 
					 "JetHT_dataF": { 'JEC':0,'JER':0,'nom':0  },
					 "JetHT_dataG":{ 'JEC':0,'JER':0,'nom':0  },
					 "JetHT_dataH":{ 'JEC':0,'JER':0,'nom':0  } ,
					 "QCDMC2000toInf": { 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1500to2000":{ 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToHadronic":{ 'JEC':0,'JER':0,'nom':0  }   } ,
					 "2017": { 
					 "JetHT_dataB": { 'JEC':0,'JER':0,'nom':0  },
					 "JetHT_dataC":{ 'JEC':0,'JER':0,'nom':0  },
					 "JetHT_dataD":{ 'JEC':0,'JER':0,'nom':0  },
					 "JetHT_dataE":{ 'JEC':0,'JER':0,'nom':0  },
					 "JetHT_dataF":{ 'JEC':0,'JER':0,'nom':0  } ,
					 "QCDMC2000toInf": { 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1500to2000":{ 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToHadronic":{ 'JEC':0,'JER':0,'nom':0  }   } ,
					 "2018": { 
					 "JetHT_dataA": { 'JEC':0,'JER':0,'nom':0  },
					 "JetHT_dataB":{ 'JEC':0,'JER':0,'nom':0  },
					 "JetHT_dataC":{ 'JEC':0,'JER':0,'nom':0  },
					 "JetHT_dataD":{ 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC2000toInf": { 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1500to2000":{ 'JEC':0,'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC':0,'JER':0,'nom':0  },
					 "TTToHadronic":{ 'JEC':0,'JER':0,'nom':0  }   }   }
	all_files_made	= {  "2015": { 
					"JetHT_dataB-ver1": { 'JEC':[],'JER':[],'nom':[] },     #nCommands[year][sample][systematic]
					 "JetHT_dataB-ver2":{ 'JEC':[],'JER':[],'nom':[] },
					 "JetHT_dataC-HIPM":{ 'JEC':[],'JER':[],'nom':[] },
					 "JetHT_dataD-HIPM":{ 'JEC':[],'JER':[],'nom':[] }, 
					 "JetHT_dataE-HIPM":{ 'JEC':[],'JER':[],'nom':[] },
					 "JetHT_dataF-HIPM":{ 'JEC':[],'JER':[],'nom':[] } ,
					"QCDMC2000toInf": { 'JEC':[],'JER':[],'nom':[]  },     #nCommands[year][sample][systematic]
					 "QCDMC1500to2000":{ 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToHadronic":{ 'JEC':[],'JER':[],'nom':[]  }   }, 
					 "2016": {
					 "JetHT_dataF": { 'JEC':[],'JER':[],'nom':[] },
					 "JetHT_dataG":{ 'JEC':[],'JER':[],'nom':[] },
					 "JetHT_dataH":{ 'JEC':[],'JER':[],'nom':[] },
					  "QCDMC2000toInf": { 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1500to2000":{ 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToHadronic":{ 'JEC':[],'JER':[],'nom':[]  }   } ,
					 "2017": { 
					  "JetHT_dataB": { 'JEC':[],'JER':[],'nom':[] },
					 "JetHT_dataC":{ 'JEC':[],'JER':[],'nom':[] },
					 "JetHT_dataD":{ 'JEC':[],'JER':[],'nom':[] },
					 "JetHT_dataE":{ 'JEC':[],'JER':[],'nom':[] },
					 "JetHT_dataF":{ 'JEC':[],'JER':[],'nom':[] } ,
					 "QCDMC2000toInf": { 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1500to2000":{ 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToHadronic":{ 'JEC':[],'JER':[],'nom':[]  }   } ,
					 "2018": { 
					 "JetHT_dataA": { 'JEC':[],'JER':[],'nom':[] },
					 "JetHT_dataB":{ 'JEC':[],'JER':[],'nom':[] },
					 "JetHT_dataC":{ 'JEC':[],'JER':[],'nom':[] },
					 "JetHT_dataD":{ 'JEC':[],'JER':[],'nom':[] } ,
					 "QCDMC2000toInf": { 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1500to2000":{ 'JEC':[],'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC':[],'JER':[],'nom':[]  },
					 "TTToHadronic":{ 'JEC':[],'JER':[],'nom':[]  }   }   }


	samples = ["QCDMC2000toInf","QCDMC1500to2000","QCDMC1000to1500","TTToHadronic", "dataB-ver1","dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM","dataF-HIPM","dataF","dataG","dataH","dataB","dataC","dataD","dataE","dataF","dataA","dataB","dataC","dataD"]
	samples_data = ["dataB-ver1","dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM","dataF-HIPM","dataF","dataG","dataH","dataB","dataC","dataD","dataE","dataF","dataA","dataB","dataC","dataD"]
	years = ["2015","2016","2017","2018"]
	eos_path = open(sys.argv[1], "r")	

	command_path = open("eos_copy_commands.sh", "w")
	for line in eos_path:
		if line.split() == "[]" or line == "\n" or line == "":
			"Line found to be empty"
			continue
		num_str = ""
		year_str = ""
		sys_str = ""
		sample_str = ""
		for sample in samples:
			if sample in line and (len(sample_str) < len(sample)):   # this should guarantee that dataB doesn't overwrite dataB-vers-1
				sample_str = sample
		if sample_str in samples_data:
			sample_str = "JetHT_%s"%sample_str
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
