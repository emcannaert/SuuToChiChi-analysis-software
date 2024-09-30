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

	def __init__(self, year, region, n_bins_x, n_bins_y, technique_str, debug=False):
		ROOT.TH1.AddDirectory(False)
		self.region = region
		self.year   = year
		self.technique_str = technique_str
		self.n_bins_x = n_bins_x
		self.n_bins_y = n_bins_y
		self.doSideband = False
		if self.region in ["SB1b", "SB0b"]: self.doSideband = True
		hist_name = "h_MSJ_mass_vs_MdSJ_%s%s"%(self.technique_str,self.region )
		print("Looking for hist name %s"%hist_name)
		if debug:  ### create dummy histograms

			#### sample,mean_x,mean_y,sigma_x,sigma_y,nentries
			self.hist_1000to1500 			= self.fill_dummy_data("QCD1000to1500",1500,1000,400,500,250)
			self.hist_1500to2000 			= self.fill_dummy_data("QCD1500to2000",2000,1200,500,500,3000)
			self.hist_2000toInf   			= self.fill_dummy_data("QCD2000toInf",2500,1500,600,700,3000)
			self.hist_TTJetsMCHT1200to2500  = self.fill_dummy_data("TTJetsMCHT1200to2500",2400,800,500,500,500)
			self.hist_TTJetsMCHT2500toInf   = self.fill_dummy_data("TTJetsMCHT2500toInf",3000,1500,1000,500,100)

			self.hist_ST_t_channel_top_inclMC	   = self.fill_dummy_data("ST_t-channel-top_inclMC",1800,1000,700,300,100)
			self.hist_ST_t_channel_antitop_inclMC   = self.fill_dummy_data("ST_t-channel-antitop_inclMC",1000,1200,700,300,100)
			self.hist_ST_s_channel_hadronsMC	   = self.fill_dummy_data("ST_s-channel-hadronsMC",1800,1000,700,300,100)
			self.hist_ST_s_channel_leptonsMC	   = self.fill_dummy_data("ST_s-channel-leptonsMC",1800,1000,700,300,100)
			self.hist_ST_tW_antiTop_inclMC		   = self.fill_dummy_data("ST_tW-antiTop_inclMC",1800,1000,700,300,100)
			self.hist_ST_tW_antiTop_inclMC		   = self.fill_dummy_data("ST_tW-top_inclMC",1800,1000,700,300,100)

			self.hist_data 					= self.fill_dummy_data("data",1500,1500,500,250,1200)

			self.all_hist_counts = self.hist_1000to1500.Clone()
			self.all_hist_counts.Add(self.hist_1500to2000)
			self.all_hist_counts.Add(self.hist_2000toInf   	)
			self.all_hist_counts.Add(self.hist_TTJetsMCHT1200to2500)
			self.all_hist_counts.Add(self.hist_TTJetsMCHT2500toInf)

			self.all_hist_counts.Add(self.hist_ST_t_channel_top_inclMC)
			self.all_hist_counts.Add(self.hist_ST_t_channel_antitop_inclMC)
			self.all_hist_counts.Add(self.hist_ST_s_channel_hadronsMC)
			self.all_hist_counts.Add(self.hist_ST_s_channel_leptonsMC)
			self.all_hist_counts.Add(self.hist_ST_tW_antiTop_inclMC)
			self.all_hist_counts.Add(self.hist_ST_tW_antiTop_inclMC)

			#self.all_hist_counts.Add()
		else:	
			self.hist_1000to1500 = self.load_hist("QCDMC1000to1500")
			self.hist_1500to2000 = self.load_hist("QCDMC1500to2000")
			if not self.doSideband: self.hist_2000toInf  = self.load_hist("QCDMC2000toInf")
			self.hist_TTJetsMCHT1200to2500 = self.load_hist("TTJetsMCHT1200to2500")
			if not self.doSideband: self.hist_TTJetsMCHT2500toInf  = self.load_hist("TTJetsMCHT2500toInf")

			if self.doSideband:
				self.hist_TTJetsMCHT800to1200 = self.load_hist("TTJetsMCHT800to1200")

			self.hist_ST_t_channel_top_inclMC      = self.load_hist("ST_t-channel-top_inclMC")
			self.hist_ST_t_channel_antitop_inclMC  = self.load_hist("ST_t-channel-antitop_inclMC")
			self.hist_ST_s_channel_hadronsMC  	   = self.load_hist("ST_s-channel-hadronsMC")
			self.hist_ST_s_channel_leptonsMC  	   = self.load_hist("ST_s-channel-leptonsMC")
			self.hist_ST_tW_antiTop_inclMC         = self.load_hist("ST_tW-antiTop_inclMC")
			self.hist_ST_tW_antiTop_inclMC         = self.load_hist("ST_tW-top_inclMC")

			#self.hist_TTToHadronicMC = self.load_hist("TTToHadronicMC")
			#self.hist_TTToSemiLeptonicMC = self.load_hist("TTToSemiLeptonicMC")
			#self.hist_TTToLeptonicMC = self.load_hist("TTToLeptonicMC")

			self.hist_data       = self.load_data_hists()
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
		if not self.doSideband:print("hist_TTJetsMCHT2500toInf counts: %s"%self.hist_TTJetsMCHT2500toInf.Integral())
		if self.doSideband:  print("hist_TTJetsMCHT800to1200 counts: %s"%self.hist_TTJetsMCHT800to1200.Integral())
		print("hist_TTJetsMCHT1200to2500 counts: %s"%self.hist_TTJetsMCHT1200to2500.Integral())
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
		self.list_TTJetsMCHT1200to2500 = self.convert_TH2(self.hist_TTJetsMCHT1200to2500)
		if not self.doSideband: self.list_TTJetsMCHT2500toInf = self.convert_TH2(self.hist_TTJetsMCHT2500toInf)

		self.list_ST_t_channel_top_inclMC = self.convert_TH2(self.hist_ST_t_channel_top_inclMC)
		self.list_ST_t_channel_antitop_inclMC = self.convert_TH2(self.hist_ST_t_channel_antitop_inclMC)
		self.list_ST_s_channel_hadronsMC = self.convert_TH2(self.hist_ST_s_channel_hadronsMC)
		self.list_ST_s_channel_leptonsMC = self.convert_TH2(self.hist_ST_s_channel_leptonsMC)
		self.list_ST_tW_antiTop_inclMC = self.convert_TH2(self.hist_ST_tW_antiTop_inclMC)
		self.list_ST_tW_top_inclMC = self.convert_TH2(self.hist_ST_tW_antiTop_inclMC)





		#self.list_TTToHadronicMC = self.convert_TH2(self.hist_TTToHadronicMC)
		#self.list_TTToSemiLeptonicMC = self.convert_TH2(self.hist_TTToSemiLeptonicMC)
		#self.list_TTToLeptonicMC = self.convert_TH2(self.hist_TTToLeptonicMC)

		self.list_all_counts = self.convert_TH2(self.all_hist_counts)
	def fill_dummy_data(self,sample,mean_x,mean_y,sigma_x,sigma_y,nentries):
		ROOT.TH1.AddDirectory(False)

		hist = ROOT.TH2F("total_counts_%s_%s_%s"%(sample,self.year,self.region), "Total Counts (%s) (%s) (%s)"%(sample,self.region,self.year), self.n_bins_x, 1250., 10000, self.n_bins_y, 500, 4000);

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

		else:
			print("ERROR: wrong contribution type")



		"""	
		elif contribution == "TTToHadronicMC":
			return self.list_TTToHadronicMC[iii][jjj]
		elif contribution == "TTToSemiLeptonicMC":
			return self.list_TTToSemiLeptonicMC[iii][jjj]
		elif contribution == "TTToLeptonicMC":
			return self.list_TTToLeptonicMC[iii][jjj]
		"""


		return

	def get_contribution_uncert(self, contribution, iii,jjj):
		if contribution == "QCDMC1000to1500":
			return sqrt(self.list_1000to1500[iii][jjj])
		elif contribution == "QCDMC1500to2000":
			return sqrt(self.list_1500to2000[iii][jjj])
		elif contribution == "QCDMC2000toInf":
			return sqrt(self.list_2000toInf[iii][jjj])

		elif contribution == "TTJetsMCHT1200to2500":
			return sqrt(self.list_TTJetsMCHT1200to2500[iii][jjj])
		elif contribution == "TTJetsMCHT2500toInf":
			return sqrt(self.list_TTJetsMCHT2500toInf[iii][jjj])


		elif contribution == "ST_t-channel-top_inclMC":
			return sqrt(self.list_ST_t_channel_top_inclMC[iii][jjj])
		elif contribution == "ST_t-channel-antitop_inclMC":
			return sqrt(self.list_ST_t_channel_antitop_inclMC[iii][jjj])
		elif contribution == "ST_s-channel-hadronsMC":
			return sqrt(self.list_ST_s_channel_hadronsMC[iii][jjj])
		elif contribution == "ST_s-channel-leptonsMC":
			return sqrt(self.list_ST_s_channel_leptonsMC[iii][jjj])
		elif contribution == "ST_tW-antiTop_inclMC":
			return sqrt(self.list_ST_tW_antiTop_inclMC[iii][jjj])
		elif contribution == "ST_tW-top_inclMC":
			return sqrt(self.list_ST_tW_top_inclMC[iii][jjj])

		elif contribution == "TTJetsMCHT800to1200":
			return sqrt(self.list_TTJetsMCHT800to1200[iii][jjj])



		"""
		elif contribution == "TTToHadronicMC":
			return sqrt(self.hist_TTToHadronicMC[iii][jjj])
		elif contribution == "TTToSemiLeptonicMC":
			return sqrt(self.hist_TTToSemiLeptonicMC[iii][jjj])
		elif contribution == "TTToLeptonicMC":
			return sqrt(self.hist_TTToLeptonicMC[iii][jjj]) """

	def get_bin_total_uncert(self, superbin):   # give a list of tuples that represent all the bins in your superbin

		total_1000to1500 = 0
		total_1500to2000 = 0
		total_2000toInf = 0
		total_TTJetsMCHT800to1200 = 0
		total_TTJetsMCHT1200to2500 = 0
		total_TTJetsMCHT2500toInf  = 0

		total_TTToHadronicMC = 0
		total_TTToSemiLeptonicMC = 0
		total_TTToLeptonicMC = 0

		total_ST_t_channel_top_inclMC = 0
		total_ST_t_channel_antitop_inclMC = 0
		total_ST_s_channel_hadronsMC = 0
		total_ST_s_channel_leptonsMC = 0
		total_ST_tW_antiTop_inclMC = 0
		total_ST_tW_top_inclMC = 0



		#print("The superbin looks like %s"%superbin )
		for _bin in superbin:


			total_1000to1500+= self.get_contribution_count("QCDMC1000to1500", _bin[0],_bin[1])
			total_1500to2000+= self.get_contribution_count("QCDMC1500to2000", _bin[0],_bin[1])
			if not self.doSideband: total_2000toInf+= self.get_contribution_count("QCDMC2000toInf", _bin[0],_bin[1])
			if self.doSideband: total_TTJetsMCHT800to1200+= self.get_contribution_count("TTJetsMCHT800to1200", _bin[0],_bin[1])
			total_TTJetsMCHT1200to2500+= self.get_contribution_count("TTJetsMCHT1200to2500", _bin[0],_bin[1])
			if not self.doSideband: total_TTJetsMCHT2500toInf+= self.get_contribution_count("TTJetsMCHT2500toInf", _bin[0],_bin[1])

			total_ST_t_channel_top_inclMC+= self.get_contribution_count("ST_t-channel-top_inclMC", _bin[0],_bin[1])
			total_ST_t_channel_antitop_inclMC+= self.get_contribution_count("ST_t-channel-antitop_inclMC", _bin[0],_bin[1])
			total_ST_s_channel_hadronsMC+= self.get_contribution_count("ST_s-channel-hadronsMC", _bin[0],_bin[1])
			total_ST_s_channel_leptonsMC+= self.get_contribution_count("ST_s-channel-leptonsMC", _bin[0],_bin[1])
			total_ST_tW_antiTop_inclMC+= self.get_contribution_count("ST_tW-antiTop_inclMC", _bin[0],_bin[1])
			total_ST_tW_top_inclMC+= self.get_contribution_count("ST_tW-top_inclMC", _bin[0],_bin[1])

			#total_TTToHadronicMC+= self.get_contribution_count("TTToHadronicMC", _bin[0],_bin[1])
			#total_TTToSemiLeptonicMC+= self.get_contribution_count("TTToSemiLeptonicMC", _bin[0],_bin[1])
			#total_TTToLeptonicMC+= self.get_contribution_count("TTToLeptonicMC", _bin[0],_bin[1])

		# once all bins are looped over, square each contribution and add them in quadrature
		total_counts_in_superbin = total_1000to1500*return_BR_SF(self.year,"QCDMC1000to1500") + total_1500to2000*return_BR_SF(self.year,"QCDMC1500to2000") + total_2000toInf*return_BR_SF(self.year,"QCDMC2000toInf") + total_TTJetsMCHT800to1200*return_BR_SF(self.year, "TTJetsMCHT800to1200") * total_TTJetsMCHT1200to2500*return_BR_SF(self.year,"TTJetsMCHT1200to2500") + total_TTJetsMCHT2500toInf*return_BR_SF(self.year,"TTJetsMCHT2500toInf") + total_ST_t_channel_top_inclMC*return_BR_SF(self.year,"ST_t_channel_top_inclMC") + total_ST_t_channel_antitop_inclMC*return_BR_SF(self.year,"ST_t_channel_antitop_inclMC") + total_ST_s_channel_leptonsMC*return_BR_SF(self.year,"ST_s_channel_leptonsMC") +  total_ST_tW_antiTop_inclMC*return_BR_SF(self.year,"ST_tW_antiTop_inclMC") + total_ST_tW_top_inclMC*return_BR_SF(self.year,"ST_tW_top_inclMC")   #total_TTToHadronicMC + total_TTToSemiLeptonicMC + total_TTToLeptonicMC
		if total_counts_in_superbin == 0:
			return 0.0



		# get scaled fraction of each contribution to the whole expected bin value
		frac_1000to1500 = total_1000to1500  *return_BR_SF(self.year,"QCDMC1000to1500") / total_counts_in_superbin
		frac_1500to2000 = total_1500to2000  *return_BR_SF(self.year,"QCDMC1500to2000") / total_counts_in_superbin
		frac_2000toInf = total_2000toInf    *return_BR_SF(self.year,"QCDMC2000toInf") / total_counts_in_superbin


		frac_TTJets800to1200 = total_TTJetsMCHT800to1200 *return_BR_SF(self.year,"TTJetsMCHT800to1200") / total_counts_in_superbin
		frac_TTJets1200to2500 = total_TTJetsMCHT1200to2500 *return_BR_SF(self.year,"TTJetsMCHT1200to2500") / total_counts_in_superbin
		frac_TTJets2500toInf  = total_TTJetsMCHT2500toInf  *return_BR_SF(self.year,"TTJetsMCHT2500toInf") / total_counts_in_superbin


		frac_ST_t_channel_top_inclMC =  total_ST_t_channel_antitop_inclMC	   *return_BR_SF(self.year,"ST_t_channel_top_inclMC") / total_counts_in_superbin
		frac_ST_t_channel_antitop_inclMC  =  total_ST_t_channel_antitop_inclMC *return_BR_SF(self.year,"ST_t_channel_antitop_inclMC") / total_counts_in_superbin
		frac_ST_s_channel_hadronsMC =  total_ST_s_channel_hadronsMC			   *return_BR_SF(self.year,"ST_s_channel_hadronsMC") / total_counts_in_superbin
		frac_ST_s_channel_leptonsMC =  total_ST_s_channel_leptonsMC            *return_BR_SF(self.year,"ST_s_channel_leptonsMC") / total_counts_in_superbin
		frac_ST_tW_antiTop_inclMC =  total_ST_tW_antiTop_inclMC                *return_BR_SF(self.year,"ST_tW_antiTop_inclMC") / total_counts_in_superbin
		frac_ST_tW_top_inclMC =  total_ST_tW_top_inclMC                        *return_BR_SF(self.year,"ST_tW_top_inclMC") / total_counts_in_superbin



		#frac_TTToHadronicMC = total_TTToHadronicMC / total_counts_in_superbin
		#frac_TTToSemiLeptonicMC = total_TTToSemiLeptonicMC / total_counts_in_superbin
		#frac_TTToLeptonicMC = total_TTToLeptonicMC / total_counts_in_superbin



		stat_uncert_1000to1500 = 0
		stat_uncert_1500to2000 = 0
		stat_uncert_2000toInf = 0
		stat_uncert_TTJets800to1200 = 0
		stat_uncert_TTJets1200to2500 = 0
		stat_uncert_TTJets2500toInf  = 0

		stat_uncert_ST_t_channel_top_inclMC = 0
		stat_uncert_ST_t_channel_antitop_inclMC = 0
		stat_uncert_ST_s_channel_hadronsMC = 0
		stat_uncert_ST_s_channel_leptonsMC = 0
		stat_uncert_ST_tW_antiTop_inclMC = 0
		stat_uncert_ST_tW_top_inclMC = 0

		#stat_uncert_TTToHadronicMC = 0
		#stat_uncert_TTToSemiLeptonicMC = 0
		#stat_uncert_TTToLeptonicMC = 0

		if total_1000to1500 > 0:
			stat_uncert_1000to1500   = 1.0/sqrt(total_1000to1500)
		if total_1500to2000 > 0:
			stat_uncert_1500to2000   = 1.0/sqrt(total_1500to2000)
		if total_2000toInf > 0:
			stat_uncert_2000toInf    = 1.0/sqrt(total_2000toInf)

		if total_TTJetsMCHT800to1200 > 0:
			stat_uncert_TTJets800to1200    = 1.0/sqrt(total_TTJetsMCHT800to1200)	
		if total_TTJetsMCHT1200to2500 > 0:
			stat_uncert_TTJets1200to2500    = 1.0/sqrt(total_TTJetsMCHT1200to2500)		
		if total_TTJetsMCHT2500toInf > 0:
			stat_uncert_TTJets2500toInf    = 1.0/sqrt(total_TTJetsMCHT2500toInf)

		if total_ST_t_channel_top_inclMC > 0:
			stat_uncert_ST_t_channel_top_inclMC    	  = 1.0/sqrt(total_ST_t_channel_top_inclMC)
		if total_ST_t_channel_antitop_inclMC > 0:
			stat_uncert_ST_t_channel_antitop_inclMC    = 1.0/sqrt(total_ST_t_channel_antitop_inclMC)
		if total_ST_s_channel_hadronsMC > 0:
			stat_uncert_ST_s_channel_hadronsMC    	  = 1.0/sqrt(total_ST_s_channel_hadronsMC)
		if total_ST_s_channel_leptonsMC > 0:
			stat_uncert_ST_s_channel_leptonsMC        = 1.0/sqrt(total_ST_s_channel_leptonsMC)
		if total_ST_tW_antiTop_inclMC > 0:
			stat_uncert_ST_tW_antiTop_inclMC          = 1.0/sqrt(total_ST_tW_antiTop_inclMC)
		if total_ST_tW_top_inclMC > 0:
			stat_uncert_ST_tW_top_inclMC    		  = 1.0/sqrt(total_ST_tW_top_inclMC)

		#if total_TTToHadronicMC > 0:
		#	stat_uncert_TTToHadronicMC = 1.0/sqrt(total_TTToHadronicMC)
		#if total_TTToSemiLeptonicMC > 0:
		#	stat_uncert_TTToSemiLeptonicMC = 1.0/sqrt(total_TTToSemiLeptonicMC)
		#if total_TTToLeptonicMC > 0:
		#	stat_uncert_TTToLeptonicMC = 1.0/sqrt(total_TTToLeptonicMC)


		#print("stat_uncert_1000to1500: %s"%stat_uncert_1000to1500)
		#print("stat_uncert_1500to2000: %s"%stat_uncert_1500to2000)
		#print("stat_uncert_2000toInf: %s"%stat_uncert_2000toInf)
		#print("stat_uncert_TTToHadronicMC: %s"%stat_uncert_TTToHadronicMC)

		total_stat_uncert = sqrt(pow(frac_1000to1500*stat_uncert_1000to1500,2) + pow(frac_1500to2000*stat_uncert_1500to2000,2)+pow(frac_2000toInf*stat_uncert_2000toInf,2)+ pow(frac_TTJets800to1200*stat_uncert_TTJets800to1200,2) +  pow(frac_TTJets1200to2500*stat_uncert_TTJets1200to2500,2) + pow(frac_TTJets2500toInf*stat_uncert_TTJets2500toInf,2)    )  + pow(stat_uncert_ST_t_channel_top_inclMC*frac_ST_t_channel_top_inclMC , 2) + pow(stat_uncert_ST_t_channel_antitop_inclMC*frac_ST_t_channel_antitop_inclMC,2) + pow(stat_uncert_ST_s_channel_hadronsMC*frac_ST_s_channel_hadronsMC,2) + pow(stat_uncert_ST_s_channel_leptonsMC*frac_ST_s_channel_leptonsMC,2) + pow(stat_uncert_ST_tW_antiTop_inclMC*frac_ST_tW_antiTop_inclMC,2) + pow(stat_uncert_ST_tW_top_inclMC*frac_ST_tW_top_inclMC,2) # pow(frac_TTToHadronicMC*stat_uncert_TTToHadronicMC,2)+ pow(frac_TTToSemiLeptonicMC*stat_uncert_TTToSemiLeptonicMC,2)+pow(frac_TTToLeptonicMC*stat_uncert_TTToLeptonicMC,2)



		#print("Total counts in superbin %s. (%s/%s/%s/%s)"%(total_counts_in_superbin,total_1000to1500,total_1500to2000,total_2000toInf,total_TTToHadronicMC) ) 
		#print("total stat uncertainty: %s"%total_stat_uncert)


		#print(total_stat_uncert)
		#print("get_bin_total_uncert took %s to run"%(time.time() - start_time))

		return total_stat_uncert


	def print_all_contributions_scaled_counts(self,superbin_indices):
		## loop over all superbins, add up counts from each contribution, then scale them and print them out


		total_1000to1500 = 0
		total_1500to2000 = 0
		total_2000toInf = 0
		total_TTJetsMCHT1200to2500 = 0
		total_TTJetsMCHT2500toInf  = 0

		total_ST_t_channel_top_inclMC = 0
		total_ST_t_channel_antitop_inclMC = 0
		total_ST_s_channel_hadronsMC = 0
		total_ST_s_channel_leptonsMC = 0
		total_ST_tW_antiTop_inclMC = 0
		total_ST_tW_top_inclMC = 0

		for iii,superbin in enumerate(superbin_indices):
			for _bin in superbin:
				total_1000to1500 += self.get_contribution_count("QCDMC1000to1500", _bin[0],_bin[1])
				total_1500to2000 += self.get_contribution_count("QCDMC1500to2000", _bin[0],_bin[1])
				total_2000toInf += self.get_contribution_count("QCDMC2000toInf", _bin[0],_bin[1])

				total_TTJetsMCHT1200to2500 += self.get_contribution_count("TTJetsMCHT1200to2500", _bin[0],_bin[1])
				total_TTJetsMCHT2500toInf += self.get_contribution_count("TTJetsMCHT2500toInf", _bin[0],_bin[1])

				total_ST_t_channel_top_inclMC += self.get_contribution_count("ST_t-channel-top_inclMC", _bin[0],_bin[1])
				total_ST_t_channel_antitop_inclMC += self.get_contribution_count("ST_t-channel-antitop_inclMC", _bin[0],_bin[1])
				total_ST_s_channel_hadronsMC += self.get_contribution_count("ST_s-channel-hadronsMC", _bin[0],_bin[1])
				total_ST_s_channel_leptonsMC += self.get_contribution_count("ST_s-channel-leptonsMC", _bin[0],_bin[1])
				total_ST_tW_antiTop_inclMC += self.get_contribution_count("ST_tW-antiTop_inclMC", _bin[0],_bin[1])
				total_ST_tW_top_inclMC += self.get_contribution_count("ST_tW-top_inclMC", _bin[0],_bin[1])


		print("Total counts from each contribution --- ")
		print("QCDMC1000to1500: %s"%(total_1000to1500*return_BR_SF(self.year,"QCDMC1000to1500")))
		print("QCDMC1500to2000: %s"%(total_1500to2000*return_BR_SF(self.year,"QCDMC1500to2000")))
		print("QCDMC2000toInf: %s"%(total_2000toInf*return_BR_SF(self.year,"QCDMC2000toInf")))

		print("TTJetsMCHT1200to2500: %s"%(total_TTJetsMCHT1200to2500*return_BR_SF(self.year,"TTJetsMCHT1200to2500")))
		print("TTJetsMCHT2500toInf: %s"%(total_TTJetsMCHT2500toInf*return_BR_SF(self.year,"TTJetsMCHT2500toInf")))

		print("ST_t-channel-top_inclMC: %s"%(total_ST_t_channel_top_inclMC*return_BR_SF(self.year,"ST_t-channel-top_inclMC")))
		print("ST_t-channel-antitop_inclMC: %s"%(total_ST_t_channel_antitop_inclMC*return_BR_SF(self.year,"ST_t-channel-antitop_inclMC")))
		print("ST_s-channel-hadronsMC: %s"%(total_ST_s_channel_hadronsMC*return_BR_SF(self.year,"ST_s-channel-hadronsMC")))
		print("ST_s-channel-leptonsMC: %s"%(total_ST_s_channel_leptonsMC*return_BR_SF(self.year,"ST_s-channel-leptonsMC")))
		print("ST_tW-antiTop_inclMC: %s"%(total_ST_tW_antiTop_inclMC*return_BR_SF(self.year,"ST_tW-antiTop_inclMC")))
		print("ST_tW-top_inclMC: %s"%(total_ST_tW_top_inclMC*return_BR_SF(self.year,"ST_tW-top_inclMC")))

	def get_scaled_superbin_counts(self, superbin):   ### return the SCALED number of counts in a specific superbin

		total_counts_in_superbin = 0

		total_1000to1500 = 0
		total_1500to2000 = 0
		total_2000toInf = 0
		total_TTJetsMCHT800to1200 = 0
		total_TTJetsMCHT1200to2500 = 0
		total_TTJetsMCHT2500toInf  = 0

		total_TTToHadronicMC = 0
		total_TTToSemiLeptonicMC = 0
		total_TTToLeptonicMC = 0

		total_ST_t_channel_top_inclMC = 0
		total_ST_t_channel_antitop_inclMC = 0
		total_ST_s_channel_hadronsMC = 0
		total_ST_s_channel_leptonsMC = 0
		total_ST_tW_antiTop_inclMC = 0
		total_ST_tW_top_inclMC = 0

		#print("The superbin looks like %s"%superbin )
		for _bin in superbin:

			total_1000to1500+= self.get_contribution_count("QCDMC1000to1500", _bin[0],_bin[1])
			total_1500to2000+= self.get_contribution_count("QCDMC1500to2000", _bin[0],_bin[1])
			if not self.doSideband: total_2000toInf+= self.get_contribution_count("QCDMC2000toInf", _bin[0],_bin[1])
			if self.doSideband: total_TTJetsMCHT800to1200+= self.get_contribution_count("TTJetsMCHT800to1200", _bin[0],_bin[1])
			total_TTJetsMCHT1200to2500+= self.get_contribution_count("TTJetsMCHT1200to2500", _bin[0],_bin[1])
			if not self.doSideband: total_TTJetsMCHT2500toInf+= self.get_contribution_count("TTJetsMCHT2500toInf", _bin[0],_bin[1])

			total_ST_t_channel_top_inclMC+= self.get_contribution_count("ST_t-channel-top_inclMC", _bin[0],_bin[1])
			total_ST_t_channel_antitop_inclMC+= self.get_contribution_count("ST_t-channel-antitop_inclMC", _bin[0],_bin[1])
			total_ST_s_channel_hadronsMC+= self.get_contribution_count("ST_s-channel-hadronsMC", _bin[0],_bin[1])
			total_ST_s_channel_leptonsMC+= self.get_contribution_count("ST_s-channel-leptonsMC", _bin[0],_bin[1])
			total_ST_tW_antiTop_inclMC+= self.get_contribution_count("ST_tW-antiTop_inclMC", _bin[0],_bin[1])
			total_ST_tW_top_inclMC+= self.get_contribution_count("ST_tW-top_inclMC", _bin[0],_bin[1])

		"""
		print("----- superbin UNSCALED contributions ------- ")
		print("QCDMC1000to1500: %s"%(total_1000to1500))
		print("QCDMC1500to2000: %s"%(total_1500to2000))
		print("QCDMC2000toInf: %s"%(total_2000toInf))

		print("TTJetsMCHT1200to2500: %s"%(total_TTJetsMCHT1200to2500))
		print("TTJetsMCHT2500toInf: %s"%(total_TTJetsMCHT2500toInf))

		print("ST_t-channel-top_inclMC: %s"%(total_ST_t_channel_top_inclMC))
		print("ST_t-channel-antitop_inclMC: %s"%(total_ST_t_channel_antitop_inclMC))
		print("ST_s-channel-hadronsMC: %s"%(total_ST_s_channel_hadronsMC))
		print("ST_s-channel-leptonsMC: %s"%(total_ST_s_channel_leptonsMC))
		print("ST_tW-antiTop_inclMC: %s"%(total_ST_tW_antiTop_inclMC))
		print("ST_tW-top_inclMC: %s"%(total_ST_tW_top_inclMC))


		print("----- superbin SCALED contributions ------- ")
		print("QCDMC1000to1500: %s"%(total_1000to1500*return_BR_SF(self.year,"QCDMC1000to1500")))
		print("QCDMC1500to2000: %s"%(total_1500to2000*return_BR_SF(self.year,"QCDMC1500to2000")))
		print("QCDMC2000toInf: %s"%(total_2000toInf*return_BR_SF(self.year,"QCDMC2000toInf")))

		print("TTJetsMCHT1200to2500: %s"%(total_TTJetsMCHT1200to2500*return_BR_SF(self.year,"TTJetsMCHT1200to2500")))
		print("TTJetsMCHT2500toInf: %s"%(total_TTJetsMCHT2500toInf*return_BR_SF(self.year,"TTJetsMCHT2500toInf")))

		print("ST_t-channel-top_inclMC: %s"%(total_ST_t_channel_top_inclMC*return_BR_SF(self.year,"ST_t-channel-top_inclMC")))
		print("ST_t-channel-antitop_inclMC: %s"%(total_ST_t_channel_antitop_inclMC*return_BR_SF(self.year,"ST_t-channel-antitop_inclMC")))
		print("ST_s-channel-hadronsMC: %s"%(total_ST_s_channel_hadronsMC*return_BR_SF(self.year,"ST_s-channel-hadronsMC")))
		print("ST_s-channel-leptonsMC: %s"%(total_ST_s_channel_leptonsMC*return_BR_SF(self.year,"ST_s-channel-leptonsMC")))
		print("ST_tW-antiTop_inclMC: %s"%(total_ST_tW_antiTop_inclMC*return_BR_SF(self.year,"ST_tW-antiTop_inclMC")))
		print("ST_tW-top_inclMC: %s"%(total_ST_tW_top_inclMC*return_BR_SF(self.year,"ST_tW-top_inclMC")))
		"""

		total_counts_in_superbin = total_1000to1500*return_BR_SF(self.year,"QCDMC1000to1500") + total_1500to2000*return_BR_SF(self.year,"QCDMC1500to2000") + total_2000toInf*return_BR_SF(self.year,"QCDMC2000toInf") + total_TTJetsMCHT800to1200*return_BR_SF(self.year, "TTJetsMCHT800to1200") * total_TTJetsMCHT1200to2500*return_BR_SF(self.year,"TTJetsMCHT1200to2500") + total_TTJetsMCHT2500toInf*return_BR_SF(self.year,"TTJetsMCHT2500toInf") + total_ST_t_channel_top_inclMC*return_BR_SF(self.year,"ST_t_channel_top_inclMC") + total_ST_t_channel_antitop_inclMC*return_BR_SF(self.year,"ST_t_channel_antitop_inclMC") + total_ST_s_channel_leptonsMC*return_BR_SF(self.year,"ST_s_channel_leptonsMC") +  total_ST_tW_antiTop_inclMC*return_BR_SF(self.year,"ST_tW_antiTop_inclMC") + total_ST_tW_top_inclMC*return_BR_SF(self.year,"ST_tW_top_inclMC")   #total_TTToHadronicMC + total_TTToSemiLeptonicMC + total_TTToLeptonicMC
		return total_counts_in_superbin

	def load_hist(self,dataset_type):

		processed_file_path = os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFiles/"
		if self.region in ["SB1b", "SB0b"]: processed_file_path = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"
		ROOT.TH1.AddDirectory(False)
		if "TTToHadronicMC" in dataset_type:
			hist_path = processed_file_path + "%s_%s_processed.root"%(dataset_type,self.year)
		elif "TTToSemiLeptonicMC" in dataset_type:
			hist_path = processed_file_path + "%s_%s_processed.root"%(dataset_type,self.year)
		elif "TTToLeptonicMC" in dataset_type:
			hist_path = processed_file_path + "%s_%s_processed.root"%(dataset_type,self.year)
		else:
			hist_path = processed_file_path + "%s_%s_processed.root"%(dataset_type,self.year)
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


		processed_file_path = os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFiles/"
		combined_data = ROOT.TH2F("data_combined_%s"%(self.region),"Double Tagged Superjet mass vs diSuperjet mass (%s) (data combined) (%s); diSuperjet mass [GeV];superjet mass"%(self.region, self.year), self.n_bins_x,1250., 10000, self.n_bins_y, 500, 4000) #375 * 125

		if self.region in ["SB1b", "SB0b"]: 
			processed_file_path = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"
			combined_data = ROOT.TH2F("data_combined_%s"%(self.region),"Double Tagged Superjet mass vs diSuperjet mass (%s) (data combined) (%s); diSuperjet mass [GeV];superjet mass"%(self.region, self.year), self.n_bins_x ,0.0, 8000, self.n_bins_y, 0.0, 2500)


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
			hist_path = processed_file_path + "%s_%s_processed.root"%(prefix,self.year)
			TH2_file = ROOT.TFile.Open(hist_path,"READ")
			TH2_hist = TH2_file.Get("nom/"+hist_name) 
			combined_data.Add(TH2_hist)

		combined_data.SetDirectory(0)   # histograms lose their references when the file destructor is called
		ROOT.TH1.AddDirectory(False)
		return combined_data

	def convert_TH2(self,hist_):
		converted_hist = [ [0]*self.n_bins_y for i in range(self.n_bins_x)]
		for iii in range(self.n_bins_x):
			for jjj in range(self.n_bins_y):
				converted_hist[iii][jjj] = hist_.GetBinContent(iii+1,jjj+1)
		return converted_hist
