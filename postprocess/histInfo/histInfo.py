import ROOT
import sys, os
from math import sqrt, exp
import random
from random import uniform, shuffle
import pdb
import time
import numpy as np

from return_BR_SF.return_BR_SF import return_BR_SF
### histInfo.py - contains a class that carries information from multiple histograms 
### for calculating statistal uncertainties
### Written by Ethan Cannaert, September 2023

class histInfo:    # this needs to be initialized for every new region + year, use when looping over the superbin_indices and filling out the uncertainties
	def __init__(self, year, region, bin_min_x, bin_min_y,n_bins_x,n_bins_y,technique_str,includeTTJetsMCHT800to1200,includeWJets,useTTTo,useQCDHT,runShifted,debug=False,runEos = False, WP=None, useOptWP=False):
		ROOT.TH1.AddDirectory(False)
		self.region = region
		self.year   = year
		self.WP     = WP
		self.technique_str = technique_str
		self.bin_min_x = bin_min_x
		self.bin_min_y = bin_min_y
		self.n_bins_x = n_bins_x
		self.n_bins_y = n_bins_y
		self.doSideband = False
		self.useQCDHT = useQCDHT
		self.runShifted = runShifted
		self.useOptWP    = useOptWP
		self.eos_path = "root://cmseos.fnal.gov/"

		self.processed_file_path = os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFiles/"
		if self.useOptWP:
			self.processed_file_path = os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFiles_optWP/"

		if runEos:  
			if self.useOptWP: self.processed_file_path =  self.eos_path + "/store/user/ecannaer/processedFiles_optWP/"
			else: self.processed_file_path =  self.eos_path + "/store/user/ecannaer/processedFiles/"
			if self.runShifted:  self.processed_file_path = self.eos_path + "/store/user/ecannaer/processedFiles_shiftedMass/"
		if WP: 
			if "AT" in WP: WP_folder = WP[2:]
			else: WP_folder = WP
			self.processed_file_path = os.getenv('CMSSW_BASE') + "/src/combinedROOT/ATWP_study/%s/"%WP_folder

		self.includeTTJetsMCHT800to1200 = includeTTJetsMCHT800to1200
		self.includeWJets = includeWJets
		self.useTTTo = useTTTo

		if self.region in ["SB1b", "SB0b"]: self.doSideband = True
		hist_name = "h_MSJ_mass_vs_MdSJ_%s%s"%(self.technique_str,self.region )

		### load histograms

		### QCD 
		self.QCD_hists = {}
		self.lists_QCD = {}
		self.QCD_samples = ["QCDMC1000to1500","QCDMC1500to2000"]
		
		if self.useQCDHT:
			self.hist_1000to1500 = self.load_hist("QCDMC1000to1500")
			self.hist_1500to2000 = self.load_hist("QCDMC1500to2000")
			self.QCD_hists["QCDMC1000to1500"] = self.hist_1000to1500
			self.QCD_hists["QCDMC1500to2000"] = self.hist_1500to2000

			if not self.doSideband: 
				self.hist_2000toInf  = self.load_hist("QCDMC2000toInf")
				if self.useQCDHT: self.QCD_hists["QCDMC2000toInf"] =  self.hist_2000toInf 
				self.QCD_samples.append("QCDMC2000toInf")
		else: 
			self.QCD_samples = [ "QCDMC_Pt_170to300","QCDMC_Pt_300to470","QCDMC_Pt_470to600", "QCDMC_Pt_600to800","QCDMC_Pt_800to1000" ,"QCDMC_Pt_1000to1400","QCDMC_Pt_1400to1800","QCDMC_Pt_1800to2400","QCDMC_Pt_2400to3200","QCDMC_Pt_3200toInf" ]
			for QCD_type in self.QCD_samples:
				self.QCD_hists[QCD_type] =  self.load_hist(QCD_type)


		for QCD_sample,QCD_hist in self.QCD_hists.items():
				self.lists_QCD[QCD_sample] = self.convert_TH2(QCD_hist)


		### TTbar 
		self.TTbar_hists = {}
		self.lists_TTbar = {}
		self.TTbar_samples = ["TTToHadronicMC","TTToSemiLeptonicMC","TTToLeptonicMC"]
		if self.useTTTo:
			for TTbar_sample in self.TTbar_samples:
				self.TTbar_hists[TTbar_sample] = self.load_hist( TTbar_sample)
		else:

			self.TTbar_samples = ["TTJetsMCHT1200to2500"]

			self.TTbar_hists["TTJetsMCHT1200to2500"] = self.load_hist("TTJetsMCHT1200to2500")
			if not self.doSideband: 
				self.TTbar_hists["TTJetsMCHT2500toInf"] = self.load_hist("TTJetsMCHT2500toInf")
				self.TTbar_samples.append("TTJetsMCHT2500toInf")
			if self.doSideband or self.includeTTJetsMCHT800to1200: 
				self.TTbar_hists["TTJetsMCHT800to1200"] = self.load_hist("TTJetsMCHT800to1200")
				self.TTbar_samples.append("TTJetsMCHT800to1200")
		
		for TTbar_sample,TTbar_hist in self.TTbar_hists.items():
			self.lists_TTbar[TTbar_sample] = self.convert_TH2(TTbar_hist)

		### ST 
		self.ST_hists = {}
		self.lists_ST = {}
		self.ST_samples = ["ST_t-channel-top_inclMC","ST_t-channel-antitop_inclMC","ST_s-channel-hadronsMC", "ST_s-channel-leptonsMC","ST_tW-antiTop_inclMC","ST_tW-top_inclMC"]

		for ST_sample in self.ST_samples: 
			self.ST_hists[ST_sample] = self.load_hist( ST_sample)
		for ST_sample,ST_hist in self.ST_hists.items():
			self.lists_ST[ST_sample] = self.convert_TH2(ST_hist)

		### W+Jets
		self.WJets_hists = {}
		self.lists_WJets = {}
		self.WJets_samples = []
		if self.includeWJets:
			self.WJets_samples = ["WJetsMC_LNu_HT800to1200","WJetsMC_LNu_HT1200to2500","WJetsMC_LNu_HT2500toInf","WJetsMC_QQ_HT800toInf" ]
			for WJets_sample in self.WJets_samples: 
				self.WJets_hists[WJets_sample] = self.load_hist( WJets_sample)
			for WJets_sample,WJets_hist in self.WJets_hists.items():
				self.lists_WJets[WJets_sample] = self.convert_TH2(WJets_hist)


		n_rows  = len(self.lists_QCD[self.lists_QCD.keys()[0]])        # <-- 22
		n_cols  = len(self.lists_QCD[self.lists_QCD.keys()[0]][0])     # <-- 20

		self.list_all_counts = [ [0]*n_cols for _ in range(n_rows) ]
		self.all_hist_counts = self.QCD_hists[ self.QCD_hists.keys()[0] ].Clone()

		for QCD_sample, QCD_hist in self.QCD_hists.items():
			if QCD_sample == self.QCD_hists.keys()[0]: continue # do not double count!
			self.all_hist_counts.Add(QCD_hist)
		for TTbar_sample, TTbar_hist in self.TTbar_hists.items():
			self.all_hist_counts.Add(TTbar_hist)
		for ST_sample, ST_hist in self.ST_hists.items():
			self.all_hist_counts.Add(ST_hist)
		for WJets_sample, WJets_hist in self.WJets_hists.items():
			self.all_hist_counts.Add(WJets_hist)


		for iii in range(n_rows):
			for jjj in range(n_cols):

				#print("iii/jjj: %s/%s,   sample_list x/y lengths are %s/%s, list_all_counts x/y lengths are %s/%s."%(iii,jjj,len(self.lists_QCD),len(self.lists_QCD[self.lists_QCD.keys()[0]]), len(self.list_all_counts), len(self.list_all_counts[0])    ))
				for sample,sample_list in self.lists_QCD.items():
					#print("iii/jjj: %s/%s,   sample list dims are (%s,%s),    sample_list dims are (%s,%s)"%(iii,jjj,len(self.list_all_counts),len(self.list_all_counts[0]), len(sample_list), len(sample_list[0])   ))
					self.list_all_counts[iii][jjj] += sample_list[iii][jjj]
				for sample,sample_list in self.lists_TTbar.items():
					self.list_all_counts[iii][jjj] += sample_list[iii][jjj]
				for sample,sample_list in self.lists_ST.items():
					self.list_all_counts[iii][jjj] += sample_list[iii][jjj]
				if includeWJets:
					for sample,sample_list in self.lists_WJets.items():
						self.list_all_counts[iii][jjj] += sample_list[iii][jjj]

		if not self.WP: self.hist_data       = self.load_data_hists()

		
	def fill_dummy_data(self,sample,mean_x,mean_y,sigma_x,sigma_y,nentries):
		ROOT.TH1.AddDirectory(False)

		hist = ROOT.TH2F("total_counts_%s_%s_%s"%(sample,self.year,self.region), "Total Counts (%s) (%s) (%s)"%(sample,self.region,self.year), self.n_bins_x, 1250., 10000, self.n_bins_y, 500, 5000);

		gaussian_func = ROOT.TF2("gaussian_func", "TMath::Gaus(x, [0], [1])*TMath::Gaus(y, [2], [3])",-5, 5, -5, 5)
		gaussian_func.SetParameters(mean_x, sigma_x, mean_y, sigma_y)
		hist.FillRandom("gaussian_func", nentries)

		return hist

	def get_contribution_count(self, contribution, iii,jjj):  #### return the (unscaled) counts in the iii,jjjth bin of sample type "contribution"

		if "QCD" in contribution:
			return self.lists_QCD[contribution][iii][jjj]
		elif "TTbar" in contribution or "TTTo" in contribution or "TTJets" in contribution:
			return self.lists_TTbar[contribution][iii][jjj]
		elif "WJets" in contribution:
			return self.lists_WJets[contribution][iii][jjj]
		elif "ST" in contribution:
			return self.lists_ST[contribution][iii][jjj]
		else:
			print("ERROR: wrong sample type: %s. Valid samle types are %s, %s, %s, %s"%(contribution, " ".join(self.lists_QCD.keys() )," ".join(self.lists_TTbar.keys() )," ".join(self.lists_ST.keys() ), " ".join(self.lists_WJets.keys() )  ))
		return

	def get_bin_total_uncert(self, superbin):   # give a list of tuples that represent all the bins in your superbin

		### calculates the bin stat uncertainty as the sum of weights / total scaled bin yield

		totals_QCD 	 = [0]*len(self.QCD_samples)
		totals_TTbar = [0]*len(self.TTbar_samples)
		totals_ST    = [0]*len(self.ST_samples)
		totals_WJets = [0]*len(self.WJets_samples)

		SFs_QCD   = [return_BR_SF(self.year,sample) for sample in self.QCD_samples]
		SFs_TTbar = [return_BR_SF(self.year,sample) for sample in self.TTbar_samples]
		SFs_ST 	  = [return_BR_SF(self.year,sample) for sample in self.ST_samples]
		SFs_WJets = [return_BR_SF(self.year,sample) for sample in self.WJets_samples]

	
		for _bin in superbin:
			for iii,QCD_sample in enumerate(self.QCD_samples):
				totals_QCD[iii] += self.get_contribution_count(QCD_sample, _bin[0],_bin[1])
			for iii,TTbar_sample in enumerate(self.TTbar_samples):
				totals_TTbar[iii] += self.get_contribution_count(TTbar_sample, _bin[0],_bin[1])
			for iii,ST_sample in enumerate(self.ST_samples):
				totals_ST[iii] += self.get_contribution_count(ST_sample, _bin[0],_bin[1])
			if self.includeWJets:
				for iii,WJets_sample in enumerate(self.WJets_samples):
					totals_WJets[iii] += self.get_contribution_count(WJets_sample, _bin[0],_bin[1])

		QCD_scaled_event_content = np.array([ totals_QCD[iii]*SFs_QCD[iii] for iii in range(len(totals_QCD))   ])
		TTbar_scaled_event_content = np.array([ totals_TTbar[iii]*SFs_TTbar[iii] for iii in range(len(totals_TTbar))   ])
		ST_scaled_event_content = np.array([ totals_ST[iii]*SFs_ST[iii] for iii in range(len(totals_ST))   ])
		WJets_scaled_event_content = np.array([ totals_WJets[iii]*SFs_WJets[iii] for iii in range(len(totals_WJets))   ])

		total_scaled_event_content =  sum(QCD_scaled_event_content)+ sum(TTbar_scaled_event_content)+ sum(ST_scaled_event_content)+ sum(WJets_scaled_event_content) 
		
		QCD_sow = np.array([ totals_QCD[iii]*pow(SFs_QCD[iii],2) for iii in range(len(totals_QCD))   ])
		TTbar_sow = np.array([ totals_TTbar[iii]*pow(SFs_TTbar[iii],2) for iii in range(len(totals_TTbar))   ])
		ST_sow = np.array([ totals_ST[iii]*pow(SFs_ST[iii],2) for iii in range(len(totals_ST))   ])
		WJets_sow = np.array([ totals_WJets[iii]*pow(SFs_WJets[iii],2) for iii in range(len(totals_WJets))   ])

		sum_of_weights =  sqrt(sum( QCD_sow)+ sum(TTbar_sow)+ sum(ST_sow)+ sum(WJets_sow  ))

		if total_scaled_event_content == 0: return 1.0
		total_stat_uncert = sum_of_weights / total_scaled_event_content

		return total_stat_uncert


	def get_scaled_superbin_counts(self, superbin):   ### return the SCALED number of counts in a specific superbin given the actual superbin indices (not superbin num)

		### calculates the bin stat uncertainty as the sum of weights / total scaled bin yield

		totals_QCD 	 = [0]*len(self.QCD_samples)
		totals_TTbar = [0]*len(self.TTbar_samples)
		totals_ST    = [0]*len(self.ST_samples)
		totals_WJets = [0]*len(self.WJets_samples)

		SFs_QCD   = [return_BR_SF(self.year,sample) for sample in self.QCD_samples]
		SFs_TTbar = [return_BR_SF(self.year,sample) for sample in self.TTbar_samples]
		SFs_ST 	  = [return_BR_SF(self.year,sample) for sample in self.ST_samples]
		SFs_WJets = [return_BR_SF(self.year,sample) for sample in self.WJets_samples]

		for _bin in superbin:
			for iii,QCD_sample in enumerate(self.QCD_samples):
				totals_QCD[iii] += self.get_contribution_count(QCD_sample, _bin[0],_bin[1])
			for iii,TTbar_sample in enumerate(self.TTbar_samples):
				totals_TTbar[iii] += self.get_contribution_count(TTbar_sample, _bin[0],_bin[1])
			for iii,ST_sample in enumerate(self.ST_samples):
				totals_ST[iii] += self.get_contribution_count(ST_sample, _bin[0],_bin[1])
			if self.includeWJets:
				for iii,WJets_sample in enumerate(self.WJets_samples):
					totals_WJets[iii] += self.get_contribution_count(WJets_sample, _bin[0],_bin[1])

		QCD_scaled_event_content = np.array([ totals_QCD[iii]*SFs_QCD[iii] for iii in range(len(totals_QCD))   ])
		TTbar_scaled_event_content = np.array([ totals_TTbar[iii]*SFs_TTbar[iii] for iii in range(len(totals_TTbar))   ])
		ST_scaled_event_content = np.array([ totals_ST[iii]*SFs_ST[iii] for iii in range(len(totals_ST))   ])
		WJets_scaled_event_content = np.array([ totals_WJets[iii]*SFs_WJets[iii] for iii in range(len(totals_WJets))   ])

		total_scaled_event_content =  sum(QCD_scaled_event_content)+ sum(TTbar_scaled_event_content)+ sum(ST_scaled_event_content)+ sum(WJets_scaled_event_content)  
		
		return total_scaled_event_content

	def get_unscaled_QCD_superbin_counts(self, superbin):   ### return the UNSCALED number of QCD counts in a specific superbin
		
		totals_QCD 	 = np.array([0]*len(self.QCD_samples))
		for _bin in superbin:
			for iii,QCD_sample in enumerate(self.QCD_samples):
				totals_QCD[iii] += self.get_contribution_count(QCD_sample, _bin[0],_bin[1])

		return sum(totals_QCD)


	def get_scaled_QCD_superbin_counts(self, superbin):   ### return the SCALED number of QCD counts in a specific superbin

		totals_QCD 	 = [0]*len(self.QCD_samples)
		SFs_QCD   = [return_BR_SF(self.year,sample) for sample in self.QCD_samples]

		for _bin in superbin:
			for iii,QCD_sample in enumerate(self.QCD_samples):
				totals_QCD[iii] += self.get_contribution_count(QCD_sample, _bin[0],_bin[1])

		QCD_scaled_event_content = np.array([ totals_QCD[iii]*SFs_QCD[iii] for iii in range(len(totals_QCD))   ])

		return sum(QCD_scaled_event_content)



	def load_hist(self,dataset_type): ## returns the designated UNSCALED histogram 

		WP_prefix = ""
		WP_name_str = WP_prefix
		if self.WP: 
			WP_prefix =  self.WP + "_"
			#WP_name_str =  WP_prefix[2:]
			WP_name_str = WP_prefix


		#self.processed_file_path = os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFiles/"
		if self.region in ["SB1b", "SB0b"]: self.processed_file_path = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"
		ROOT.TH1.AddDirectory(False)
		if "TTToHadronicMC" in dataset_type:
			hist_path = self.processed_file_path + "%s_%s_%sprocessed.root"%(dataset_type,self.year,WP_name_str)
		elif "TTToSemiLeptonicMC" in dataset_type:
			hist_path = self.processed_file_path + "%s_%s_%sprocessed.root"%(dataset_type,self.year,WP_name_str)
		elif "TTToLeptonicMC" in dataset_type:
			hist_path = self.processed_file_path + "%s_%s_%sprocessed.root"%(dataset_type,self.year,WP_name_str)
		elif dataset_type == "WJetsMC_LNu_HT1200to2500":
			hist_path = self.processed_file_path + "WJetsMC_LNu-HT1200to2500_%s_%sprocessed.root"%(self.year,WP_name_str)
		elif dataset_type == "WJetsMC_LNu_HT2500toInf":
			hist_path = self.processed_file_path + "WJetsMC_LNu-HT2500toInf_%s_%sprocessed.root"%(self.year,WP_name_str)
		elif dataset_type == "WJetsMC_LNu_HT800to1200":
			hist_path = self.processed_file_path + "WJetsMC_LNu-HT800to1200_%s_%sprocessed.root"%(self.year,WP_name_str)
		elif dataset_type == "WJetsMC_QQ_HT800toInf":
			hist_path = self.processed_file_path + "WJetsMC_QQ-HT800toInf_%s_%sprocessed.root"%(self.year,WP_name_str)
		else:
			hist_path = self.processed_file_path + "%s_%s_%sprocessed.root"%(dataset_type,self.year,WP_name_str)
		#print("hist_path", hist_path)
		hist_name = "h_MSJ_mass_vs_MdSJ_%s%s"%(self.technique_str,self.region)   # need to find what the name of this histogram
		print("Loaded hist %s in file %s."%(hist_name,hist_path)  )

		#print("hist_name", hist_name)

		TH2_file = ROOT.TFile.Open(hist_path,"READ")
		TH2_hist = TH2_file.Get("nom/"+hist_name) 
		TH2_hist.SetDirectory(0)   # histograms lose their references when the file destructor is called

		print("------ histogram (%s) has %f integrated events."%(dataset_type, TH2_hist.Integral()))
		return TH2_hist

	def load_data_hists(self):
		data_strings = []


		WP_prefix = ""
		if self.WP: WP_prefix = self.WP + "_"

		#self.processed_file_path = os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFiles/"
		combined_data = ROOT.TH2F("data_combined_%s"%(self.region),"Double Tagged Superjet mass vs diSuperjet mass (%s) (data combined) (%s); diSuperjet mass [GeV];superjet mass"%(self.region, self.year), self.n_bins_x,1250., 10000, self.n_bins_y, 500, 5000) #375 * 125

		if self.region in ["SB1b", "SB0b"]: 
			self.processed_file_path = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"
			combined_data = ROOT.TH2F("data_combined_%s"%(self.region),"Double Tagged Superjet mass vs diSuperjet mass (%s) (data combined) (%s); diSuperjet mass [GeV];superjet mass"%(self.region, self.year), self.n_bins_x ,0.0, 8000, self.n_bins_y, 0.0, 3000)


		hist_name = "h_MSJ_mass_vs_MdSJ_%s%s"%(self.technique_str,self.region )  # need to find what the name of this histogram
		if self.year == "2015":
			data_strings = ["dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM","dataF-HIPM"] ## will have to remove dataB-ver1
		elif self.year == "2016":
			data_strings = ["dataF","dataG","dataH"]
		elif self.year == "2017":
			data_strings = ["dataB","dataC","dataD","dataE","dataF"]
		elif self.year == "2018":
			data_strings = ["dataA","dataB","dataC","dataD"]
		for prefix in data_strings:
			hist_path = self.processed_file_path + "%s_%s_%sprocessed.root"%(prefix,self.year, WP_prefix)
			TH2_file = ROOT.TFile.Open(hist_path,"READ")
			TH2_hist = TH2_file.Get("nom/"+hist_name) 
			combined_data.Add(TH2_hist)

		combined_data.SetDirectory(0)   # histograms lose their references when the file destructor is called
		ROOT.TH1.AddDirectory(False)
		return combined_data

	def convert_TH2(self,hist_):
		converted_hist = [ [0]*self.n_bins_y for i in range(self.n_bins_x)]
		for iii in range(0,self.n_bins_x):
			for jjj in range(0,self.n_bins_y):
				converted_hist[iii][jjj] = hist_.GetBinContent(iii+1,jjj+1)
		return converted_hist
