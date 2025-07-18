import ROOT
import sys, os
from math import sqrt, exp
import random
from random import uniform, shuffle
import pdb
import time

from return_BR_SF.return_BR_SF import return_BR_SF
### histInfo.py - contains a class that carries information from multiple histograms 
### for calculating statistal uncertainties
### Written by Ethan Cannaert, September 2023

class histInfo:    # this needs to be initialized for every new region + year, use when looping over the superbin_indices and filling out the uncertainties

	def __init__(self, year, region, bin_min_x, bin_min_y, n_bins_x, n_bins_y, technique_str, includeTTJetsMCHT800to1200, includeWJets, includeTTo, debug=False, runEos = False, WP=None):
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


		self.eos_path = "root://cmseos.fnal.gov/"

		self.processed_file_path = os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFiles/"
		if runEos:  self.processed_file_path =  self.eos_path + "/store/user/ecannaer/processedFiles/"
		if WP: 
			if "AT" in WP: WP_folder = WP[2:]
			else: WP_folder = WP
			self.processed_file_path = os.getenv('CMSSW_BASE') + "/src/combinedROOT/ATWP_study/%s/"%WP_folder

		self.includeTTJetsMCHT800to1200 = includeTTJetsMCHT800to1200
		self.includeWJets = includeWJets
		self.includeTTo = includeTTo

		if self.region in ["SB1b", "SB0b"]: self.doSideband = True
		hist_name = "h_MSJ_mass_vs_MdSJ_%s%s"%(self.technique_str,self.region )
		print("Looking for hist name %s"%hist_name)

		self.hist_1000to1500 = self.load_hist("QCDMC1000to1500")
		self.hist_1500to2000 = self.load_hist("QCDMC1500to2000")
		if not self.doSideband: self.hist_2000toInf  = self.load_hist("QCDMC2000toInf")
		self.hist_TTJetsMCHT1200to2500 = self.load_hist("TTJetsMCHT1200to2500")
		if not self.doSideband: self.hist_TTJetsMCHT2500toInf  = self.load_hist("TTJetsMCHT2500toInf")

		if self.doSideband or self.includeTTJetsMCHT800to1200:
			self.hist_TTJetsMCHT800to1200 = self.load_hist("TTJetsMCHT800to1200")

		self.hist_ST_t_channel_top_inclMC      = self.load_hist("ST_t-channel-top_inclMC")
		self.hist_ST_t_channel_antitop_inclMC  = self.load_hist("ST_t-channel-antitop_inclMC")
		self.hist_ST_s_channel_hadronsMC  	   = self.load_hist("ST_s-channel-hadronsMC")
		self.hist_ST_s_channel_leptonsMC  	   = self.load_hist("ST_s-channel-leptonsMC")
		self.hist_ST_tW_antiTop_inclMC         = self.load_hist("ST_tW-antiTop_inclMC")
		self.hist_ST_tW_antiTop_inclMC         = self.load_hist("ST_tW-top_inclMC")

		if self.includeTTo:
			self.hist_TTToHadronicMC = self.load_hist("TTToHadronicMC")
			self.hist_TTToSemiLeptonicMC = self.load_hist("TTToSemiLeptonicMC")
			self.hist_TTToLeptonicMC = self.load_hist("TTToLeptonicMC")

		if self.includeWJets:
			self.hist_WJetsMC_LNu_HT800to1200 = self.load_hist("WJetsMC_LNu_HT800to1200")
			self.hist_WJetsMC_LNu_HT1200to2500 = self.load_hist("WJetsMC_LNu_HT1200to2500")
			self.hist_WJetsMC_LNu_HT2500toInf  = self.load_hist("WJetsMC_LNu_HT2500toInf")
			self.hist_WJetsMC_QQ_HT800toInf    = self.load_hist("WJetsMC_QQ_HT800toInf")

		if not self.WP: self.hist_data       = self.load_data_hists()
		print("--------------------------------------------------------------------")
		print("region/year are %s/%s"%(region,year))
		self.all_hist_counts = self.hist_1000to1500.Clone()
		#print("grabbed 1000to1500 ")
		self.all_hist_counts.Add(self.hist_1500to2000)
		#print("added 1500to2000 ")
		if not self.doSideband:
			self.all_hist_counts.Add(self.hist_2000toInf   	)
			#print("added 2000toInf ")
		self.all_hist_counts.Add(self.hist_TTJetsMCHT1200to2500)
		#print("added TTJets1 ")
		if not self.doSideband:
			self.all_hist_counts.Add(self.hist_TTJetsMCHT2500toInf)
			#print("added TTJets2 ")

		if self.doSideband:
			self.all_hist_counts.Add(self.hist_TTJetsMCHT800to1200)

		self.all_hist_counts.Add(self.hist_ST_t_channel_top_inclMC)
		self.all_hist_counts.Add(self.hist_ST_t_channel_antitop_inclMC)
		self.all_hist_counts.Add(self.hist_ST_s_channel_hadronsMC)
		self.all_hist_counts.Add(self.hist_ST_s_channel_leptonsMC)
		self.all_hist_counts.Add(self.hist_ST_tW_antiTop_inclMC)
		self.all_hist_counts.Add(self.hist_ST_tW_antiTop_inclMC)


		print("----------   %s/%s   ----------"%(year,region))
		print("hist_1000to1500 counts: %s"%self.hist_1000to1500.Integral())
		print("hist_1500to2000 counts: %s"%self.hist_1500to2000.Integral())
		if not self.doSideband:print("hist_2000toInf counts: %s"%self.hist_2000toInf.Integral())

		if not self.includeTTo:
			if self.doSideband or self.includeTTJetsMCHT800to1200:  print("hist_TTJetsMCHT800to1200 counts: %s"%self.hist_TTJetsMCHT800to1200.Integral())
			print("hist_TTJetsMCHT1200to2500 counts: %s"%self.hist_TTJetsMCHT1200to2500.Integral())
			if not self.doSideband:print("hist_TTJetsMCHT2500toInf counts: %s"%self.hist_TTJetsMCHT2500toInf.Integral())
		else:
			print("hist_WJetsMC_LNu_HT1200to2500 counts: %s"%self.hist_WJetsMC_LNu_HT1200to2500.Integral())
			print("hist_WJetsMC_LNu_HT1200to2500 counts: %s"%self.hist_WJetsMC_LNu_HT1200to2500.Integral())
			print("hist_WJetsMC_LNu_HT2500toInf counts: %s"%self.hist_WJetsMC_LNu_HT2500toInf.Integral())
			print("hist_WJetsMC_QQ_HT800toInf counts: %s"%self.hist_WJetsMC_QQ_HT800toInf.Integral())

		print("hist_ST_t_channel_top_inclMC counts: %s"%self.hist_ST_t_channel_top_inclMC.Integral())
		print("hist_ST_t_channel_antitop_inclMC counts: %s"%self.hist_ST_t_channel_antitop_inclMC.Integral())
		print("hist_ST_s_channel_hadronsMC counts: %s"%self.hist_ST_s_channel_hadronsMC.Integral())
		print("hist_ST_s_channel_leptonsMC counts: %s"%self.hist_ST_s_channel_leptonsMC.Integral())
		print("hist_ST_tW_antiTop_inclMC counts: %s"%self.hist_ST_tW_antiTop_inclMC.Integral())
		print("hist_ST_tW_antiTop_inclMC counts: %s"%self.hist_ST_tW_antiTop_inclMC.Integral())

		#print("##############################################")
		#print("Printing the original contribution histograms ")
		#print("##############################################")

		if self.doSideband: self.list_TTJetsMCHT800to1200   = self.convert_TH2(self.hist_TTJetsMCHT800to1200)
		self.list_1000to1500   = self.convert_TH2(self.hist_1000to1500)
		#print('\n'.join(' '.join(str(x) for x in row) for row in self.list_1000to1500))
		self.list_1500to2000   = self.convert_TH2(self.hist_1500to2000)
		#print('\n'.join(' '.join(str(x) for x in row) for row in self.list_1500to2000))
		if not self.doSideband: self.list_2000toInf    = self.convert_TH2(self.hist_2000toInf)
		"""
		for iii in range(0, 22):
			for jjj in range(0,20):
				if self.list_2000toInf[iii][jjj] > 0:
					print("2000toInf bin value from histInfo is %s"%self.list_2000toInf[iii][jjj])
		"""


		if self.includeTTJetsMCHT800to1200: self.list_TTJetsMCHT800to1200 = self.convert_TH2(self.hist_TTJetsMCHT800to1200)
		self.list_TTJetsMCHT1200to2500 = self.convert_TH2(self.hist_TTJetsMCHT1200to2500)
		if not self.doSideband: self.list_TTJetsMCHT2500toInf = self.convert_TH2(self.hist_TTJetsMCHT2500toInf)

		self.list_ST_t_channel_top_inclMC = self.convert_TH2(self.hist_ST_t_channel_top_inclMC)
		self.list_ST_t_channel_antitop_inclMC = self.convert_TH2(self.hist_ST_t_channel_antitop_inclMC)
		self.list_ST_s_channel_hadronsMC = self.convert_TH2(self.hist_ST_s_channel_hadronsMC)
		self.list_ST_s_channel_leptonsMC = self.convert_TH2(self.hist_ST_s_channel_leptonsMC)
		self.list_ST_tW_antiTop_inclMC = self.convert_TH2(self.hist_ST_tW_antiTop_inclMC)
		self.list_ST_tW_top_inclMC = self.convert_TH2(self.hist_ST_tW_antiTop_inclMC)


		if self.includeTTo:
			self.list_TTToHadronicMC     = self.convert_TH2(self.hist_TTToHadronicMC)
			self.list_TTToSemiLeptonicMC = self.convert_TH2(self.hist_TTToSemiLeptonicMC)
			self.list_TTToLeptonicMC     = self.convert_TH2(self.hist_TTToLeptonicMC)

		if self.includeWJets:
			self.list_WJetsMC_LNu_HT800to1200 = self.convert_TH2(self.hist_WJetsMC_LNu_HT800to1200)
			self.list_WJetsMC_LNu_HT1200to2500 = self.convert_TH2(self.hist_WJetsMC_LNu_HT1200to2500)
			self.list_WJetsMC_LNu_HT2500toInf  = self.convert_TH2(self.hist_WJetsMC_LNu_HT2500toInf)
			self.list_WJetsMC_QQ_HT800toInf    = self.convert_TH2(self.hist_WJetsMC_QQ_HT800toInf)


		self.list_all_counts = self.convert_TH2(self.all_hist_counts)
	def fill_dummy_data(self,sample,mean_x,mean_y,sigma_x,sigma_y,nentries):
		ROOT.TH1.AddDirectory(False)

		hist = ROOT.TH2F("total_counts_%s_%s_%s"%(sample,self.year,self.region), "Total Counts (%s) (%s) (%s)"%(sample,self.region,self.year), self.n_bins_x, 1250., 10000, self.n_bins_y, 500, 5000);

		gaussian_func = ROOT.TF2("gaussian_func", "TMath::Gaus(x, [0], [1])*TMath::Gaus(y, [2], [3])",-5, 5, -5, 5)
		gaussian_func.SetParameters(mean_x, sigma_x, mean_y, sigma_y)
		hist.FillRandom("gaussian_func", nentries)

		return hist



	def get_contribution_count(self, contribution, iii,jjj):  #### return the (unscaled) counts in the iii,jjjth bin of contribution type
		if contribution == "QCDMC1000to1500":
			return self.list_1000to1500[iii][jjj]
		elif contribution == "QCDMC1500to2000":
			return self.list_1500to2000[iii][jjj]
		elif contribution == "QCDMC2000toInf":
			return self.list_2000toInf[iii][jjj]

		elif contribution == "TTJetsMCHT1200to2500":
			return self.list_TTJetsMCHT1200to2500[iii][jjj]
		elif contribution == "TTJetsMCHT2500toInf":
			return self.list_TTJetsMCHT2500toInf[iii][jjj]

		elif contribution == "ST_t-channel-top_inclMC":
			return self.list_ST_t_channel_top_inclMC[iii][jjj]
		elif contribution == "ST_t-channel-antitop_inclMC":
			return self.list_ST_t_channel_antitop_inclMC[iii][jjj]
		elif contribution == "ST_s-channel-hadronsMC":
			return self.list_ST_s_channel_hadronsMC[iii][jjj]
		elif contribution == "ST_s-channel-leptonsMC":
			return self.list_ST_s_channel_leptonsMC[iii][jjj]
		elif contribution == "ST_tW-antiTop_inclMC":
			return self.list_ST_tW_antiTop_inclMC[iii][jjj]
		elif contribution == "ST_tW-top_inclMC":
			return self.list_ST_tW_top_inclMC[iii][jjj]

		elif contribution == "TTJetsMCHT800to1200":
			return self.list_TTJetsMCHT800to1200[iii][jjj]

		elif contribution == "WJetsMC_LNu_HT800to1200":
			return self.list_WJetsMC_LNu_HT800to1200[iii][jjj]

		elif contribution == "WJetsMC_LNu_HT1200to2500":
			return self.list_WJetsMC_LNu_HT1200to2500[iii][jjj]

		elif contribution == "WJetsMC_LNu_HT2500toInf":
			return self.list_WJetsMC_LNu_HT2500toInf[iii][jjj]

		elif contribution == "WJetsMC_QQ_HT800toInf":
			return self.list_WJetsMC_QQ_HT800toInf[iii][jjj]

		elif contribution == "TTToHadronicMC":
			return self.list_TTToHadronicMC[iii][jjj]
		elif contribution == "TTToSemiLeptonicMC":
			return self.list_TTToSemiLeptonicMC[iii][jjj]
		elif contribution == "TTToLeptonicMC":
			return self.list_TTToLeptonicMC[iii][jjj]

		else:
			print("ERROR: wrong contribution type")


		return

	def get_bin_total_uncert(self, superbin):   # give a list of tuples that represent all the bins in your superbin

		### calculates the bin stat uncertainty as the sum of weights / total scaled bin yield

		total_1000to1500 = 0
		total_1500to2000 = 0
		total_2000toInf  = 0


		total_TTJets800to1200  = 0
		total_TTJets1200to2500 = 0
		total_TTJets2500toInf  = 0

		total_TTToHadronicMC = 0 
		total_TTToSemiLeptonicMC = 0 
		total_TTToLeptonicMC = 0

		total_ST_t_channel_top_inclMC = 0
		total_ST_t_channel_antitop_inclMC = 0
		total_ST_s_channel_hadronsMC = 0
		total_ST_s_channel_leptonsMC = 0
		total_ST_tW_antiTop_inclMC = 0
		total_ST_tW_top_inclMC = 0

		total_WJetsMC_LNu_HT800to1200 = 0
		total_WJetsMC_LNu_HT1200to2500 = 0
		total_WJetsMC_LNu_HT2500toInf = 0
		total_WJetsMC_QQ_HT800toInf = 0

		## go through each bin in superbin and count the total number of each of these events in the entire supebin




		## get scale factors for each BR process
		SF_1000to1500 = return_BR_SF(self.year,"QCDMC1000to1500")
		SF_1500to2000 = return_BR_SF(self.year,"QCDMC1500to2000")
		SF_2000toInf  = return_BR_SF(self.year,"QCDMC2000toInf") 

		SF_TTJets800to1200  = return_BR_SF(self.year,"TTJetsMCHT800to1200")
		SF_TTJets1200to2500 = return_BR_SF(self.year,"TTJetsMCHT1200to2500")
		SF_TTJets2500toInf  = return_BR_SF(self.year,"TTJetsMCHT2500toInf")

		SF_ST_t_channel_top_inclMC 		= return_BR_SF(self.year,"ST_t_channel_top_inclMC")
		SF_ST_t_channel_antitop_inclMC  =  return_BR_SF(self.year,"ST_t_channel_antitop_inclMC")
		SF_ST_s_channel_hadronsMC 		=  return_BR_SF(self.year,"ST_s_channel_hadronsMC")
		SF_ST_s_channel_leptonsMC 		=  return_BR_SF(self.year,"ST_s_channel_leptonsMC")
		SF_ST_tW_antiTop_inclMC		    =  return_BR_SF(self.year,"ST_tW_antiTop_inclMC")
		SF_ST_tW_top_inclMC 			=  return_BR_SF(self.year,"ST_tW_top_inclMC")
 
		SF_WJetsMC_LNu_HT800to1200     = return_BR_SF(self.year,"WJetsMC_LNu_HT800to1200")
		SF_WJetsMC_LNu_HT1200to2500    = return_BR_SF(self.year,"WJetsMC_LNu_HT1200to2500")
		SF_WJetsMC_LNu_HT2500toInf     = return_BR_SF(self.year,"WJetsMC_LNu_HT2500toInf")
		SF_WJetsMC_QQ_HT800toInf       = return_BR_SF(self.year,"WJetsMC_QQ_HT800toInf")

		SF_TTToHadronic					 = return_BR_SF(self.year,"TTToHadronicMC")
		SF_TTToSemiLeptonic				 = return_BR_SF(self.year,"TTToSemiLeptonicMC")
		SF_TTToSemiLeptonic				 = return_BR_SF(self.year,"TTToLeptonicMC")

		for _bin in superbin:
			total_1000to1500+= self.get_contribution_count("QCDMC1000to1500", _bin[0],_bin[1])
			total_1500to2000+= self.get_contribution_count("QCDMC1500to2000", _bin[0],_bin[1])
			if not self.doSideband: total_2000toInf+= self.get_contribution_count("QCDMC2000toInf", _bin[0],_bin[1])

			if not self.includeTTo:
				if self.doSideband or self.includeTTJetsMCHT800to1200: total_TTJets800to1200+= self.get_contribution_count("TTJetsMCHT800to1200", _bin[0],_bin[1])
				total_TTJets1200to2500+= self.get_contribution_count("TTJetsMCHT1200to2500", _bin[0],_bin[1])
				if not self.doSideband: total_TTJets2500toInf+= self.get_contribution_count("TTJetsMCHT2500toInf", _bin[0],_bin[1])

			total_ST_t_channel_top_inclMC+= self.get_contribution_count("ST_t-channel-top_inclMC", _bin[0],_bin[1])
			total_ST_t_channel_antitop_inclMC+= self.get_contribution_count("ST_t-channel-antitop_inclMC", _bin[0],_bin[1])
			total_ST_s_channel_hadronsMC+= self.get_contribution_count("ST_s-channel-hadronsMC", _bin[0],_bin[1])
			total_ST_s_channel_leptonsMC+= self.get_contribution_count("ST_s-channel-leptonsMC", _bin[0],_bin[1])
			total_ST_tW_antiTop_inclMC+= self.get_contribution_count("ST_tW-antiTop_inclMC", _bin[0],_bin[1])
			total_ST_tW_top_inclMC+= self.get_contribution_count("ST_tW-top_inclMC", _bin[0],_bin[1])

			if self.includeTTo:
				total_TTToHadronicMC+= self.get_contribution_count("TTToHadronicMC", _bin[0],_bin[1])
				total_TTToSemiLeptonicMC+= self.get_contribution_count("TTToSemiLeptonicMC", _bin[0],_bin[1])
				total_TTToLeptonicMC+= self.get_contribution_count("TTToLeptonicMC", _bin[0],_bin[1])


			if self.includeWJets:
				total_WJetsMC_LNu_HT800to1200 += self.get_contribution_count("WJetsMC_LNu_HT800to1200", _bin[0],_bin[1])
				total_WJetsMC_LNu_HT1200to2500 += self.get_contribution_count("WJetsMC_LNu_HT1200to2500", _bin[0],_bin[1])
				total_WJetsMC_LNu_HT2500toInf += self.get_contribution_count("WJetsMC_LNu_HT2500toInf", _bin[0],_bin[1])
				total_WJetsMC_QQ_HT800toInf += self.get_contribution_count("WJetsMC_QQ_HT800toInf", _bin[0],_bin[1])



		total_scaled_event_content =  total_1000to1500*pow(SF_1000to1500,1) +  total_1500to2000*pow(SF_1500to2000,1) + total_2000toInf*pow(SF_2000toInf,1) +    total_ST_t_channel_top_inclMC*pow(SF_ST_t_channel_top_inclMC,1)  + total_ST_t_channel_antitop_inclMC*pow(SF_ST_t_channel_antitop_inclMC,1)  +  total_ST_s_channel_hadronsMC*pow(SF_ST_s_channel_hadronsMC,1)  +  total_ST_s_channel_leptonsMC*pow(SF_ST_s_channel_leptonsMC,1) +  total_ST_tW_antiTop_inclMC*pow(SF_ST_tW_antiTop_inclMC,1)  +  total_ST_tW_top_inclMC*pow(SF_ST_tW_top_inclMC,1)  + 		total_WJetsMC_LNu_HT800to1200*pow(SF_WJetsMC_LNu_HT800to1200,1) + total_WJetsMC_LNu_HT1200to2500*pow(SF_WJetsMC_LNu_HT1200to2500,1) + total_WJetsMC_LNu_HT2500toInf*pow(SF_WJetsMC_LNu_HT2500toInf,1) + total_WJetsMC_QQ_HT800toInf*pow(SF_WJetsMC_QQ_HT800toInf,1)
		
		if not self.includeTTo: total_scaled_event_content += (total_TTJets800to1200*pow(SF_TTJets800to1200,1) +  total_TTJets1200to2500*pow(SF_TTJets1200to2500,1)  +  total_TTJets2500toInf*pow(SF_TTJets2500toInf,1) )
		else: total_scaled_event_content +=  (total_TTToHadronicMC*pow(SF_TTToHadronic,1) + total_TTToSemiLeptonicMC*pow(SF_TTToSemiLeptonic,1) + total_TTToLeptonicMC*pow(SF_TTToSemiLeptonic,1) ) 
		sum_of_weights  =  total_1000to1500*pow(SF_1000to1500,2) +  total_1500to2000*pow(SF_1500to2000,2) + total_2000toInf*pow(SF_2000toInf,2) +  total_TTJets800to1200*pow(SF_TTJets800to1200,2) +  total_TTJets1200to2500*pow(SF_TTJets1200to2500,2)  +  total_TTJets2500toInf*pow(SF_TTJets2500toInf,2)  +   total_ST_t_channel_top_inclMC*pow(SF_ST_t_channel_top_inclMC,2)  + total_ST_t_channel_antitop_inclMC*pow(SF_ST_t_channel_antitop_inclMC,2)  +  total_ST_s_channel_hadronsMC*pow(SF_ST_s_channel_hadronsMC,2)  +  total_ST_s_channel_leptonsMC*pow(SF_ST_s_channel_leptonsMC,2) +  total_ST_tW_antiTop_inclMC*pow(SF_ST_tW_antiTop_inclMC,2)  +  total_ST_tW_top_inclMC*pow(SF_ST_tW_top_inclMC,2)  + 		total_WJetsMC_LNu_HT800to1200*pow(SF_WJetsMC_LNu_HT800to1200,2) + total_WJetsMC_LNu_HT1200to2500*pow(SF_WJetsMC_LNu_HT1200to2500,2) + total_WJetsMC_LNu_HT2500toInf*pow(SF_WJetsMC_LNu_HT2500toInf,2) + total_WJetsMC_QQ_HT800toInf*pow(SF_WJetsMC_QQ_HT800toInf,2)
		if not self.includeTTo: sum_of_weights+= (total_TTJets800to1200*pow(SF_TTJets800to1200,2) +  total_TTJets1200to2500*pow(SF_TTJets1200to2500,2)  +  total_TTJets2500toInf*pow(SF_TTJets2500toInf,2)   )
		else: sum_of_weights+= ( total_TTToHadronicMC*pow(SF_TTToHadronic,2) + total_TTToSemiLeptonicMC*pow(SF_TTToSemiLeptonic,2) + total_TTToLeptonicMC*pow(SF_TTToSemiLeptonic,2) )
		sum_of_weights = sqrt(sum_of_weights)

		if total_scaled_event_content == 0: return 1.0
		total_stat_uncert = sum_of_weights / total_scaled_event_content

		return total_stat_uncert


	def get_scaled_superbin_counts(self, superbin):   ### return the SCALED number of counts in a specific superbin

		total_counts_in_superbin = 0

		total_1000to1500 = 0
		total_1500to2000 = 0
		total_2000toInf  = 0


		total_TTJets800to1200  = 0
		total_TTJets1200to2500 = 0
		total_TTJets2500toInf  = 0

		total_TTToHadronicMC = 0 
		total_TTToSemiLeptonicMC = 0 
		total_TTToLeptonicMC = 0

		total_ST_t_channel_top_inclMC = 0
		total_ST_t_channel_antitop_inclMC = 0
		total_ST_s_channel_hadronsMC = 0
		total_ST_s_channel_leptonsMC = 0
		total_ST_tW_antiTop_inclMC = 0
		total_ST_tW_top_inclMC = 0

		total_WJetsMC_LNu_HT800to1200 = 0
		total_WJetsMC_LNu_HT1200to2500 = 0
		total_WJetsMC_LNu_HT2500toInf = 0
		total_WJetsMC_QQ_HT800toInf = 0

		for _bin in superbin:
			total_1000to1500+= self.get_contribution_count("QCDMC1000to1500", _bin[0],_bin[1])
			total_1500to2000+= self.get_contribution_count("QCDMC1500to2000", _bin[0],_bin[1])
			if not self.doSideband: total_2000toInf+= self.get_contribution_count("QCDMC2000toInf", _bin[0],_bin[1])

			if not self.includeTTo:
				if self.doSideband or self.includeTTJetsMCHT800to1200: total_TTJets800to1200+= self.get_contribution_count("TTJetsMCHT800to1200", _bin[0],_bin[1])
				total_TTJets1200to2500+= self.get_contribution_count("TTJetsMCHT1200to2500", _bin[0],_bin[1])
				if not self.doSideband: total_TTJets2500toInf+= self.get_contribution_count("TTJetsMCHT2500toInf", _bin[0],_bin[1])

			total_ST_t_channel_top_inclMC+= self.get_contribution_count("ST_t-channel-top_inclMC", _bin[0],_bin[1])
			total_ST_t_channel_antitop_inclMC+= self.get_contribution_count("ST_t-channel-antitop_inclMC", _bin[0],_bin[1])
			total_ST_s_channel_hadronsMC+= self.get_contribution_count("ST_s-channel-hadronsMC", _bin[0],_bin[1])
			total_ST_s_channel_leptonsMC+= self.get_contribution_count("ST_s-channel-leptonsMC", _bin[0],_bin[1])
			total_ST_tW_antiTop_inclMC+= self.get_contribution_count("ST_tW-antiTop_inclMC", _bin[0],_bin[1])
			total_ST_tW_top_inclMC+= self.get_contribution_count("ST_tW-top_inclMC", _bin[0],_bin[1])

			if self.includeTTo:
				total_TTToHadronicMC+= self.get_contribution_count("TTToHadronicMC", _bin[0],_bin[1])
				total_TTToSemiLeptonicMC+= self.get_contribution_count("TTToSemiLeptonicMC", _bin[0],_bin[1])
				total_TTToLeptonicMC+= self.get_contribution_count("TTToLeptonicMC", _bin[0],_bin[1])

			if self.includeWJets:
				total_WJetsMC_LNu_HT800to1200 += self.get_contribution_count("WJetsMC_LNu_HT800to1200", _bin[0],_bin[1])
				total_WJetsMC_LNu_HT1200to2500 += self.get_contribution_count("WJetsMC_LNu_HT1200to2500", _bin[0],_bin[1])
				total_WJetsMC_LNu_HT2500toInf += self.get_contribution_count("WJetsMC_LNu_HT2500toInf", _bin[0],_bin[1])
				total_WJetsMC_QQ_HT800toInf += self.get_contribution_count("WJetsMC_QQ_HT800toInf", _bin[0],_bin[1])

		total_counts_in_superbin = total_1000to1500*return_BR_SF(self.year,"QCDMC1000to1500") + total_1500to2000*return_BR_SF(self.year,"QCDMC1500to2000") + total_2000toInf*return_BR_SF(self.year,"QCDMC2000toInf") + total_TTJets800to1200*return_BR_SF(self.year, "TTJetsMCHT800to1200") * total_TTJets1200to2500*return_BR_SF(self.year,"TTJetsMCHT1200to2500") + total_TTJets2500toInf*return_BR_SF(self.year,"TTJetsMCHT2500toInf") + total_ST_t_channel_top_inclMC*return_BR_SF(self.year,"ST_t_channel_top_inclMC") + total_ST_t_channel_antitop_inclMC*return_BR_SF(self.year,"ST_t_channel_antitop_inclMC") + total_ST_s_channel_leptonsMC*return_BR_SF(self.year,"ST_s_channel_leptonsMC") +  total_ST_tW_antiTop_inclMC*return_BR_SF(self.year,"ST_tW_antiTop_inclMC") + total_ST_tW_top_inclMC*return_BR_SF(self.year,"ST_tW_top_inclMC")   #total_TTToHadronicMC + total_TTToSemiLeptonicMC + total_TTToLeptonicMC
		return total_counts_in_superbin

	def get_unscaled_QCD_superbin_counts(self, superbin):   ### return the UNSCALED number of QCD counts in a specific superbin
		
		total_counts_in_superbin = 0

		total_1000to1500 = 0
		total_1500to2000 = 0
		total_2000toInf = 0

		for _bin in superbin:  
			total_1000to1500+= self.get_contribution_count("QCDMC1000to1500", _bin[0],_bin[1])
			total_1500to2000+= self.get_contribution_count("QCDMC1500to2000", _bin[0],_bin[1])
			if not self.doSideband: total_2000toInf+= self.get_contribution_count("QCDMC2000toInf", _bin[0],_bin[1])

		total_QCD_counts_in_superbin = total_1000to1500 + total_1500to2000 + total_2000toInf
		return total_QCD_counts_in_superbin


	def get_scaled_QCD_superbin_counts(self, superbin):   ### return the SCALED number of QCD counts in a specific superbin
		total_counts_in_superbin = 0

		total_1000to1500 = 0
		total_1500to2000 = 0
		total_2000toInf = 0

		SF_1000to1500 = return_BR_SF(self.year,"QCDMC1000to1500")
		SF_1500to2000 = return_BR_SF(self.year,"QCDMC1500to2000")
		SF_2000toInf  = return_BR_SF(self.year,"QCDMC2000toInf")  

		for _bin in superbin:  
			total_1000to1500+= self.get_contribution_count("QCDMC1000to1500", _bin[0],_bin[1])
			total_1500to2000+= self.get_contribution_count("QCDMC1500to2000", _bin[0],_bin[1])
			if not self.doSideband: total_2000toInf+= self.get_contribution_count("QCDMC2000toInf", _bin[0],_bin[1])

		total_scaled_QCD_counts_in_superbin = SF_1000to1500*total_1000to1500 + SF_1500to2000*total_1500to2000 + SF_2000toInf*total_2000toInf
		return total_scaled_QCD_counts_in_superbin



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
		print("hist name is: %s in file %s"%(hist_name,hist_path)  )

		#print("hist_name", hist_name)

		TH2_file = ROOT.TFile.Open(hist_path,"READ")
		TH2_hist = TH2_file.Get("nom/"+hist_name) 
		TH2_hist.SetDirectory(0)   # histograms lose their references when the file destructor is called

		print("The %s histogram has %f entries"%(dataset_type, TH2_hist.Integral()))
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
