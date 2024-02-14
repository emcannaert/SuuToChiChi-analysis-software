import sys, os
import numpy as np
import pickle
if __name__=="__main__":
	Suu_mass_ =  list(map(str, map(int, 1000*np.array(range(4,9)))))
	chi_mass_ = list(map(str,map(int,1000*np.array(range(2,7))/2.0)))

	Suu_mass = []
	chi_mass = []

	years = {"UL16MiniAODAPVv2": "2015" ,
			 "UL16MiniAODv2":  "2016" ,
			 "UL17MiniAODv2": "2017" ,
			 "UL18MiniAODv2":  "2018"
		}

	Suu_mass = {"MSuu-4000":  "Suu4",
				"MSuu-5000":  "Suu5",
				"MSuu-6000":  "Suu6",
				"MSuu-7000":  "Suu7",
				"MSuu-8000":  "Suu8"
		}
	chi_mass = {"MChi-1000":  "chi1",
				"MChi-1500":  "chi1p5",
				"MChi-2000":  "chi2",
				"MChi-2500":  "chi2p5",
				"MChi-3000":  "chi3"
		}


	data_files = {"2015": "/store/mc/RunIISummer20UL16MiniAODAPVv2/SuuToChiChiToHTHTToJets_MSuu-4000_MChi-1000_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/60000/EF8D3226-9665-FF42-8F73-20E1B71B2703.root" ,
				  "2016": "/store/mc/RunIISummer20UL16MiniAODv2/SuuToChiChiToHTHTToJets_MSuu-4000_MChi-1000_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v1/2550000/AC2EE404-F819-CE4D-AB22-7BE35E278E18.root" ,
				  "2017": "/store/mc/RunIISummer20UL17MiniAODv2/SuuToChiChiToHTHTToJets_MSuu-4000_MChi-1000_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v3/50000/5734DEE6-8D26-704A-BFA9-E8976034C7F0.root",
				  "2018": "/store/mc/RunIISummer20UL18MiniAODv2/SuuToChiChiToHTHTToJets_MSuu-4000_MChi-1000_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/2550000/73C711C9-0871-1143-9C3E-D2EA21C33C71.root" 
	}


	decays = ["WBWB", "HTHT", "ZTZT", "WBHT","WBZT", "HTZT"]

	with open("allAltCrabCfgs/signal_files.txt", "r") as f:
		lines = f.readlines()

	signal_samples = []
	signal_datasets = dict()
	signal_files = dict()
	signal_files_made = dict()
	signal_nCommands = dict()
	num_files = 0
	for iii,line in enumerate(lines):
		
		if(line.split() == []):
			continue
		year_ = ""
		Suu_mass_ = ""
		chi_mass_ = ""
		decay_ = ""
		for long_year, year in years.items():
			if long_year in line:
				year_ = years[long_year]
		for long_Suu_mass, MSuu in Suu_mass.items():
			if long_Suu_mass in line:
				Suu_mass_ = Suu_mass[long_Suu_mass]
		for long_chi_mass, MChi in chi_mass.items():
			if long_chi_mass in line:
				chi_mass_ = chi_mass[long_chi_mass]
		for decay in decays:
			if decay in line:
				decay_ = decay
		any_failed = [ year_ == "", Suu_mass_ == "", chi_mass_ == "", decay_ == ""   ]
		if True in any_failed:
			print("ERROR: found bad line - %s. year/Suu mass/chi mass/decay: %s/%s/%s/%s"%(line, year_,Suu_mass_,chi_mass_,decay_))
			continue
		num_files+=1
		mass_label = "%s_%s_%s"%(Suu_mass_,chi_mass_,decay_)
		

		if mass_label not in signal_samples:
			signal_samples.append(mass_label)
		if year_ not in signal_datasets.keys():
			signal_datasets[year_] = dict()
		if mass_label not in  signal_datasets[year_].keys():
			signal_datasets[year_][mass_label] = dict()
		signal_datasets[year_][mass_label] = line


		if year_ not in signal_files.keys():
			signal_files[year_] = dict()
		if mass_label not in  signal_files[year_].keys():
			signal_files[year_][mass_label] = dict()
		signal_files[year_][mass_label] = data_files[year_]

		if year_ not in signal_nCommands.keys():
			signal_nCommands[year_] = dict()
		if mass_label not in  signal_nCommands[year_].keys():
			signal_nCommands[year_][mass_label] = {'JEC':0,'JER':0,'nom':0 }

		if year_ not in signal_files_made.keys():
			signal_files_made[year_] = dict()
		if mass_label not in  signal_files_made[year_].keys():
			signal_files_made[year_][mass_label] = {'JEC':[],'JER':[],'nom':[] }

	#print(signal_samples)

	print("Added %i files to the dictionary."%num_files)
	for signal_sample in signal_samples:
		print(signal_sample)

	dbfile = open('signal_datasets.pkl', 'w')
	pickle.dump(signal_datasets, dbfile)                    
	dbfile.close()

	dbfile2 = open('signal_samples.pkl', 'w')
	pickle.dump(signal_samples, dbfile2)                    
	dbfile2.close()
	
	dbfile3 = open('signal_files.pkl', 'w')
	pickle.dump(signal_files, dbfile3)                    
	dbfile3.close()

	dbfile4 = open('signal_nCommands.pkl', 'w')
	pickle.dump(signal_nCommands, dbfile4)                    
	dbfile4.close()

	dbfile5 = open('signal_files_made.pkl', 'w')
	pickle.dump(signal_files_made, dbfile5)                    
	dbfile5.close()
	

	


