import sys,os,time
import numpy as np
import ROOT
import ast
from return_signal_SF import return_signal_SF
from math import sqrt
from write_cms_text import write_cms_text
import argparse
from return_BR_SF.return_BR_SF import return_BR_SF
import random
from hist_loader.hist_loader import hist_loader

from math import isnan
### linearize_final_plots.py
### written by Ethan Cannaert, December 2024
### requires locations of input root files for each background/signal contribution (QCD1000to1500, QCD1500to2000, QCD2000toInf, TTbar, sig MC)

### open each file and get the histograms from each
### scale histograms relative to the appropriate luminosity 
### get superbin indices and find "center" of each superbin, sort bin by these centers 
### loop over each superbin and add together the corresponding histogram bins, this becomes an entry in a 1D ( 22x20 = 440 bin) distribution for each contribution that goes to Combine
### in the end there will be a histogram for QCD, TTbar, signal MC, and then data 

ROOT.gErrorIgnoreLevel = ROOT.kError
### change the lists to instead be dictionaries?
class linearized_plot:

	ROOT.TH1.SetDefaultSumw2()
	ROOT.TH2.SetDefaultSumw2()

	def __init__(self, year, mass_point, technique_str, all_BR_hists, useMask=False, createDummyChannel=False, run_from_eos = False, debug=False, WP=None):

		self.c = ROOT.TCanvas("","",1200,1000)
		self.BR_SF_scale = 1.0
		self.sig_SF_scale = 1.0
		self.technique_str = technique_str
		self.year   = year
		self.createDummyChannel = createDummyChannel
		self.run_from_eos = run_from_eos
		self.debug = debug

		self.WP = WP
		self.WP_folder = self.WP[2:]
		self.MC_root_file_home	  = 	os.getenv('CMSSW_BASE') + "/src/combinedROOT/ATWP_study/%s/"%self.WP_folder
		self.data_root_file_home	=   os.getenv('CMSSW_BASE') + "/src/combinedROOT/ATWP_study/%s/"%self.WP_folder

		self.eos_path = "root://cmseos.fnal.gov/"
		self.HT_distr_home = "/HT_distributions" # extra folder where output files are saved for HT distribution plots

		if self.run_from_eos:		## grab files from eos if they are not stored locally

			print("Using files stored on EOS.")
			self.MC_root_file_home	    =  self.eos_path + "/store/user/ecannaer/processedFiles/"
			self.data_root_file_home	=  self.eos_path + "/store/user/ecannaer/processedFiles/"

		## region options
		self.doSideband = all_BR_hists.doSideband
		self.doATxtb = 	  all_BR_hists.doATxtb
		self.doHTdist =   all_BR_hists.doHTdist
		self.useMask  =   useMask
		if self.doSideband: self.doHTdist = False

		self.final_hist_name = "h_MSJ_mass_vs_MdSJ"
		if self.doHTdist: 
			self.final_hist_name = "h_totHT"
			self.final_hist_title = "Event H_{T}"

		### sample inclusion options
		self.includeWJets =           all_BR_hists.includeWJets
		self.includeTTTo  =			  all_BR_hists.includeTTTo
		self.includeTTJets800to1200 = all_BR_hists.includeTTJets800to1200

		if "NN" in self.technique_str: self.doSideband = False

		self.index_file_home	 = os.getenv('CMSSW_BASE') + "/src/postprocess/binMaps/ATWPStudy/%s/"%self.WP_folder
		self.output_file_home	= os.getenv('CMSSW_BASE') + "/src/postprocess/ATWP_study/finalCombineFilesNewStats/%s/"%self.WP_folder
		self.final_plot_home	 = os.getenv('CMSSW_BASE') + "/src/postprocess/plots/ATWP_study/finalCombinePlots/%s/"%self.WP_folder

		if self.useMask: 
			self.output_file_home	 = os.getenv('CMSSW_BASE') + "/src/postprocess/finalCombineFilesNewStats/maskedFinalCombineFiles"
			self.final_plot_home	 = os.getenv('CMSSW_BASE') + "/src/postprocess/plots/finalCombinePlots/maskedFinalCombineFiles/"

		if self.useMask and self.doHTdist: return

		self.superbin_indices			  	  = self.load_superbin_indices()
		self.superbin_indices_AT			  = self.load_superbin_indices(region="AT1b")   ## change this to reflect which bin indices should be followed (AT1tb if you are using the tight WP in the SR)

		if  self.doSideband: 
			self.superbin_indices_SB1b = self.load_superbin_indices(region="SB1b")
			self.superbin_indices_SB0b = self.load_superbin_indices(region="SB1b")
 
		print("DEBUG: AT region is sorted into %s superbins."%(len(self.superbin_indices_AT)))

		if self.debug:
			self.output_file_home	= os.getenv('CMSSW_BASE') + "/src/postprocess/finalCombineFilesNewStats/test/"

		self.mass_point = mass_point   # label for the signal mass point

		self.data_systematics 	   = ["nom"]
		self.data_systematic_names = ["nom"]

		self.systematics 	  = ["nom"]   ## systematic namings as used in analyzer	 "bTagSF",   
		self.systematic_names = ["nom"]  ## systematic namings for cards   "CMS_btagSF", 

		self.uncorrelated_systematics = [ "CMS_jec", "CMS_jer","CMS_jer_eta193", "CMS_jer_193eta25", "CMS_L1Prefiring","CMS_bTagSF_M", "CMS_bTagSF_T", "CMS_bTagSF_bc_T_year", "CMS_bTagSF_light_T_year", "CMS_bTagSF_bc_M_year","CMS_bTagSF_light_M_year", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year", "CMS_jec_RelativeSample_year"] ## systematics that are correlated (will not have year appended to names)	 "CMS_btagSF",
			## removed from uncorrelated uncertainties :  "CMS_pu"

		### HT bin stuff
		if self.doHTdist: self.HT_dist_superbins =  all_BR_hists.HT_dist_superbins


		### individual bins for AT1b

		self.QCD1000to1500_hist_AT1b 	= all_BR_hists.QCD1000to1500_hist_AT1b
		self.QCD1500to2000_hist_AT1b 	= all_BR_hists.QCD1500to2000_hist_AT1b
		self.QCD2000toInf_hist_AT1b 	= all_BR_hists.QCD2000toInf_hist_AT1b

		self.TTJets1200to2500_hist_AT1b 	= all_BR_hists.TTJets1200to2500_hist_AT1b
		self.TTJets2500toInf_hist_AT1b 		= all_BR_hists.TTJets2500toInf_hist_AT1b

		self.ST_t_channel_top_hist_AT1b 		= all_BR_hists.ST_t_channel_top_hist_AT1b
		self.ST_t_channel_antitop_hist_AT1b 	= all_BR_hists.ST_t_channel_antitop_hist_AT1b
		self.ST_s_channel_hadrons_hist_AT1b 	= all_BR_hists.ST_s_channel_hadrons_hist_AT1b
		self.ST_s_channel_leptons_hist_AT1b 	= all_BR_hists.ST_s_channel_leptons_hist_AT1b
		self.ST_tW_antitop_hist_AT1b 			= all_BR_hists.ST_tW_antitop_hist_AT1b
		self.ST_tW_top_hist_AT1b 				= all_BR_hists.ST_tW_top_hist_AT1b

		if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_AT1b = all_BR_hists.TTJetsMCHT800to1200_AT1b
		if self.includeTTTo:
			self.TTToHadronicMC_AT1b 				= all_BR_hists.TTToHadronicMC_AT1b
			self.TTToSemiLeptonicMC_AT1b 			= all_BR_hists.TTToSemiLeptonicMC_AT1b
			self.TTToLeptonicMC_AT1b 				= all_BR_hists.TTToLeptonicMC_AT1b

		if self.includeWJets:
			self.WJetsMC_LNu_HT800to1200_AT1b 	= all_BR_hists.WJetsMC_LNu_HT800to1200_AT1b
			self.WJetsMC_LNu_HT1200to2500_AT1b 	= all_BR_hists.WJetsMC_LNu_HT1200to2500_AT1b
			self.WJetsMC_LNu_HT2500toInf_AT1b 	= all_BR_hists.WJetsMC_LNu_HT2500toInf_AT1b
			self.WJetsMC_QQ_HT800toInf_AT1b 	= all_BR_hists.WJetsMC_QQ_HT800toInf_AT1b

		self.signal_WBWB_hist_AT1b = []
		self.signal_HTHT_hist_AT1b = []
		self.signal_ZTZT_hist_AT1b = []
		self.signal_WBHT_hist_AT1b = []
		self.signal_WBZT_hist_AT1b = []
		self.signal_HTZT_hist_AT1b = []

		### individual bins for AT0b

		self.QCD1000to1500_hist_AT0b 	= all_BR_hists.QCD1000to1500_hist_AT0b
		self.QCD1500to2000_hist_AT0b 	= all_BR_hists.QCD1500to2000_hist_AT0b
		self.QCD2000toInf_hist_AT0b 	= all_BR_hists.QCD2000toInf_hist_AT0b

		self.TTJets1200to2500_hist_AT0b 	= all_BR_hists.TTJets1200to2500_hist_AT0b
		self.TTJets2500toInf_hist_AT0b 		= all_BR_hists.TTJets2500toInf_hist_AT0b

		self.ST_t_channel_top_hist_AT0b 		= all_BR_hists.ST_t_channel_top_hist_AT0b
		self.ST_t_channel_antitop_hist_AT0b 	= all_BR_hists.ST_t_channel_antitop_hist_AT0b
		self.ST_s_channel_hadrons_hist_AT0b 	= all_BR_hists.ST_s_channel_hadrons_hist_AT0b
		self.ST_s_channel_leptons_hist_AT0b 	= all_BR_hists. ST_s_channel_leptons_hist_AT0b
		self.ST_tW_antitop_hist_AT0b 			= all_BR_hists.ST_tW_antitop_hist_AT0b
		self.ST_tW_top_hist_AT0b 				= all_BR_hists.ST_tW_top_hist_AT0b

		if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_AT0b 	= all_BR_hists.TTJetsMCHT800to1200_AT0b
		if self.includeTTTo:
			self.TTToHadronicMC_AT0b 				= all_BR_hists.TTToHadronicMC_AT0b
			self.TTToSemiLeptonicMC_AT0b 			= all_BR_hists.TTToSemiLeptonicMC_AT0b
			self.TTToLeptonicMC_AT0b 				= all_BR_hists.TTToLeptonicMC_AT0b

		if self.includeWJets:
			self.WJetsMC_LNu_HT800to1200_AT0b 	= all_BR_hists.WJetsMC_LNu_HT800to1200_AT0b
			self.WJetsMC_LNu_HT1200to2500_AT0b 	= all_BR_hists.WJetsMC_LNu_HT1200to2500_AT0b
			self.WJetsMC_LNu_HT2500toInf_AT0b 	= all_BR_hists.WJetsMC_LNu_HT2500toInf_AT0b
			self.WJetsMC_QQ_HT800toInf_AT0b 	= all_BR_hists.WJetsMC_QQ_HT800toInf_AT0b

		self.signal_WBWB_hist_AT0b = []
		self.signal_HTHT_hist_AT0b = []
		self.signal_ZTZT_hist_AT0b = []
		self.signal_WBHT_hist_AT0b = []
		self.signal_WBZT_hist_AT0b = []
		self.signal_HTZT_hist_AT0b = []


		if self.doATxtb:
			### individual bins for AT0tb

			self.QCD1000to1500_hist_AT0tb 	= all_BR_hists.QCD1000to1500_hist_AT0tb
			self.QCD1500to2000_hist_AT0tb 	= all_BR_hists.QCD1500to2000_hist_AT0tb
			self.QCD2000toInf_hist_AT0tb 	= all_BR_hists.QCD2000toInf_hist_AT0tb

			self.TTJets1200to2500_hist_AT0tb 	= all_BR_hists.TTJets1200to2500_hist_AT0tb
			self.TTJets2500toInf_hist_AT0tb 	= all_BR_hists.TTJets2500toInf_hist_AT0tb

			self.ST_t_channel_top_hist_AT0tb 		= all_BR_hists.ST_t_channel_top_hist_AT0tb
			self.ST_t_channel_antitop_hist_AT0tb 	= all_BR_hists.ST_t_channel_antitop_hist_AT0tb
			self.ST_s_channel_hadrons_hist_AT0tb 	= all_BR_hists.ST_s_channel_hadrons_hist_AT0tb
			self.ST_s_channel_leptons_hist_AT0tb 	= all_BR_hists. ST_s_channel_leptons_hist_AT0tb
			self.ST_tW_antitop_hist_AT0tb 			= all_BR_hists.ST_tW_antitop_hist_AT0tb
			self.ST_tW_top_hist_AT0tb 				= all_BR_hists.ST_tW_top_hist_AT0tb

			if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_AT0tb 		= all_BR_hists.TTJetsMCHT800to1200_AT0tb
			if self.includeTTTo:
				self.TTToHadronicMC_AT0tb 				= all_BR_hists.TTToHadronicMC_AT0tb
				self.TTToSemiLeptonicMC_AT0tb 			= all_BR_hists.TTToSemiLeptonicMC_AT0tb
				self.TTToLeptonicMC_AT0tb 				= all_BR_hists.TTToLeptonicMC_AT0tb

			if self.includeWJets:
				self.WJetsMC_LNu_HT800to1200_AT0tb 		= all_BR_hists.WJetsMC_LNu_HT800to1200_AT0tb
				self.WJetsMC_LNu_HT1200to2500_AT0tb 	= all_BR_hists.WJetsMC_LNu_HT1200to2500_AT0tb
				self.WJetsMC_LNu_HT2500toInf_AT0tb 		= all_BR_hists.WJetsMC_LNu_HT2500toInf_AT0tb
				self.WJetsMC_QQ_HT800toInf_AT0tb 		= all_BR_hists.WJetsMC_QQ_HT800toInf_AT0tb

			self.signal_WBWB_hist_AT0tb = []
			self.signal_HTHT_hist_AT0tb = []
			self.signal_ZTZT_hist_AT0tb = []
			self.signal_WBHT_hist_AT0tb = []
			self.signal_WBZT_hist_AT0tb = []
			self.signal_HTZT_hist_AT0tb = []

			### individual bins for AT1tb
			self.QCD1000to1500_hist_AT1tb 	= all_BR_hists.QCD1000to1500_hist_AT1tb
			self.QCD1500to2000_hist_AT1tb 	= all_BR_hists.QCD1500to2000_hist_AT1tb
			self.QCD2000toInf_hist_AT1tb 	= all_BR_hists.QCD2000toInf_hist_AT1tb

			self.TTJets1200to2500_hist_AT1tb 	= all_BR_hists.TTJets1200to2500_hist_AT1tb
			self.TTJets2500toInf_hist_AT1tb 	= all_BR_hists.TTJets2500toInf_hist_AT1tb

			self.ST_t_channel_top_hist_AT1tb 		= all_BR_hists.ST_t_channel_top_hist_AT1tb
			self.ST_t_channel_antitop_hist_AT1tb 	= all_BR_hists.ST_t_channel_antitop_hist_AT1tb
			self.ST_s_channel_hadrons_hist_AT1tb 	= all_BR_hists.ST_s_channel_hadrons_hist_AT1tb
			self.ST_s_channel_leptons_hist_AT1tb 	= all_BR_hists.ST_s_channel_leptons_hist_AT1tb
			self.ST_tW_antitop_hist_AT1tb 			= all_BR_hists.ST_tW_antitop_hist_AT1tb
			self.ST_tW_top_hist_AT1tb 				= all_BR_hists.ST_tW_top_hist_AT1tb

			if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_AT1tb 	= all_BR_hists.TTJetsMCHT800to1200_AT1tb
			if self.includeTTTo:
				self.TTToHadronicMC_AT1tb 				= all_BR_hists.TTToHadronicMC_AT1tb
				self.TTToSemiLeptonicMC_AT1tb 			= all_BR_hists.TTToSemiLeptonicMC_AT1tb
				self.TTToLeptonicMC_AT1tb 				= all_BR_hists.TTToLeptonicMC_AT1tb

			if self.includeWJets:
				self.WJetsMC_LNu_HT800to1200_AT1tb 		= all_BR_hists.WJetsMC_LNu_HT800to1200_AT1tb
				self.WJetsMC_LNu_HT1200to2500_AT1tb 	= all_BR_hists.WJetsMC_LNu_HT1200to2500_AT1tb
				self.WJetsMC_LNu_HT2500toInf_AT1tb 		= all_BR_hists.WJetsMC_LNu_HT2500toInf_AT1tb
				self.WJetsMC_QQ_HT800toInf_AT1tb 		= all_BR_hists.WJetsMC_QQ_HT800toInf_AT1tb

			self.signal_WBWB_hist_AT1tb = []
			self.signal_HTHT_hist_AT1tb = []
			self.signal_ZTZT_hist_AT1tb = []
			self.signal_WBHT_hist_AT1tb = []
			self.signal_WBZT_hist_AT1tb = []
			self.signal_HTZT_hist_AT1tb = []

		### individual bins for SB1b
		if self.doSideband:
			self.QCD1000to1500_hist_SB1b 	= all_BR_hists.QCD1000to1500_hist_SB1b
			self.QCD1500to2000_hist_SB1b 	= all_BR_hists.QCD1500to2000_hist_SB1b
			self.QCD2000toInf_hist_SB1b 	= all_BR_hists.QCD2000toInf_hist_SB1b


			self.TTJets800to1200_hist_SB1b 		= all_BR_hists.TTJets800to1200_hist_SB1b
			self.TTJets1200to2500_hist_SB1b 	= all_BR_hists.TTJets1200to2500_hist_SB1b

			self.ST_t_channel_top_hist_SB1b 		= all_BR_hists.ST_t_channel_top_hist_SB1b
			self.ST_t_channel_antitop_hist_SB1b 	= all_BR_hists.ST_t_channel_antitop_hist_SB1b
			self.ST_s_channel_hadrons_hist_SB1b 	= all_BR_hists.ST_s_channel_hadrons_hist_SB1b
			self.ST_s_channel_leptons_hist_SB1b 	= all_BR_hists.ST_s_channel_leptons_hist_SB1b
			self.ST_tW_antitop_hist_SB1b 			= all_BR_hists.ST_tW_antitop_hist_SB1b
			self.ST_tW_top_hist_SB1b 				= all_BR_hists.ST_tW_top_hist_SB1b

			if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_SB1b 	= all_BR_hists.TTJetsMCHT800to1200_SB1b
			if self.includeTTTo:
				self.TTToHadronicMC_SB1b 				= all_BR_hists.TTToHadronicMC_SB1b
				self.TTToSemiLeptonicMC_SB1b 			= all_BR_hists.TTToSemiLeptonicMC_SB1b
				self.TTToLeptonicMC_SB1b 				= all_BR_hists.TTToLeptonicMC_SB1b

			if self.includeWJets:
				self.WJetsMC_LNu_HT800to1200_SB1b 	= all_BR_hists.WJetsMC_LNu_HT800to1200_SB1b
				self.WJetsMC_LNu_HT1200to2500_SB1b 	= all_BR_hists.WJetsMC_LNu_HT1200to2500_SB1b
				self.WJetsMC_LNu_HT2500toInf_SB1b 	= all_BR_hists.WJetsMC_LNu_HT2500toInf_SB1b
				self.WJetsMC_QQ_HT800toInf_SB1b 	= all_BR_hists.WJetsMC_QQ_HT800toInf_SB1b

			self.signal_WBWB_hist_SB1b = []
			self.signal_HTHT_hist_SB1b = []
			self.signal_ZTZT_hist_SB1b = []
			self.signal_WBHT_hist_SB1b = []
			self.signal_WBZT_hist_SB1b = []
			self.signal_HTZT_hist_SB1b = []


			### individual bins for SB0b

			self.QCD1000to1500_hist_SB0b 	= all_BR_hists.QCD1000to1500_hist_SB0b
			self.QCD1500to2000_hist_SB0b 	= all_BR_hists.QCD1500to2000_hist_SB0b
			self.QCD2000toInf_hist_SB0b 	= all_BR_hists.QCD2000toInf_hist_SB0b

			self.TTJets800to1200_hist_SB0b 	= all_BR_hists.TTJets800to1200_hist_SB0b
			self.TTJets1200to2500_hist_SB0b = all_BR_hists.TTJets1200to2500_hist_SB0b

			self.ST_t_channel_top_hist_SB0b 		= all_BR_hists.ST_t_channel_top_hist_SB0b
			self.ST_t_channel_antitop_hist_SB0b 	= all_BR_hists.ST_t_channel_antitop_hist_SB0b
			self.ST_s_channel_hadrons_hist_SB0b 	= all_BR_hists.ST_s_channel_hadrons_hist_SB0b
			self.ST_s_channel_leptons_hist_SB0b 	= all_BR_hists.ST_s_channel_leptons_hist_SB0b
			self.ST_tW_antitop_hist_SB0b 			= all_BR_hists.ST_tW_antitop_hist_SB0b
			self.ST_tW_top_hist_SB0b 				= all_BR_hists.ST_tW_top_hist_SB0b

			if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_SB0b 	= all_BR_hists.TTJetsMCHT800to1200_SB0b
			if self.includeTTTo:
				self.TTToHadronicMC_SB0b 				= all_BR_hists.TTToHadronicMC_SB0b
				self.TTToSemiLeptonicMC_SB0b 			= all_BR_hists.TTToSemiLeptonicMC_SB0b
				self.TTToLeptonicMC_SB0b 				= all_BR_hists.TTToLeptonicMC_SB0b

			if self.includeWJets:
				self.WJetsMC_LNu_HT800to1200_SB0b 	= all_BR_hists.WJetsMC_LNu_HT800to1200_SB0b
				self.WJetsMC_LNu_HT1200to2500_SB0b 	= all_BR_hists.WJetsMC_LNu_HT1200to2500_SB0b
				self.WJetsMC_LNu_HT2500toInf_SB0b 	= all_BR_hists.WJetsMC_LNu_HT2500toInf_SB0b
				self.WJetsMC_QQ_HT800toInf_SB0b 	= all_BR_hists.WJetsMC_QQ_HT800toInf_SB0b

			self.signal_WBWB_hist_SB0b = []
			self.signal_HTHT_hist_SB0b = []
			self.signal_ZTZT_hist_SB0b = []
			self.signal_WBHT_hist_SB0b = []
			self.signal_WBZT_hist_SB0b = []
			self.signal_HTZT_hist_SB0b = []

		self.all_combined_hists_SR = []
		self.all_combined_hists_CR = []
		self.all_combined_hists_AT1b = []
		self.all_combined_hists_AT0b = []
		self.all_combined_hists_SB1b = []
		self.all_combined_hists_SB0b = []



		self.combined_linear_SR	 = []
		self.combined_linear_CR	 = []
		self.combined_linear_AT1b   = []
		self.combined_linear_AT0b   = []
		if self.doATxtb:
			self.combined_linear_AT1tb   = []
			self.combined_linear_AT0tb   =[]
			self.data_hist_AT0tb  	= all_BR_hists.data_hist_AT0tb
			self.data_hist_AT1tb  	= all_BR_hists.data_hist_AT1tb
		if self.doSideband:
			self.combined_linear_SB1b   = []
			self.combined_linear_SB0b   = []
			self.data_hist_SB1b  	= all_BR_hists.data_hist_SB1b
			self.data_hist_SB0b  	= all_BR_hists.data_hist_SB0b

		self.data_hist_SR 	= all_BR_hists.data_hist_SR
		self.data_hist_CR 	= all_BR_hists.data_hist_CR
		self.data_hist_AT0b  	= all_BR_hists.data_hist_AT0b
		self.data_hist_AT1b  	= all_BR_hists.data_hist_AT1b



		print("Loading signal histograms.")
		doExtras = False


		# load signal hists 
		for systematic in self.systematics:

			### AT1b
			self.signal_WBWB_hist_AT1b.append(self.load_signal_hist("AT1b",systematic, False , "WBWB"))
			self.signal_HTHT_hist_AT1b.append(self.load_signal_hist("AT1b",systematic, False , "HTHT"))
			self.signal_ZTZT_hist_AT1b.append(self.load_signal_hist("AT1b",systematic, False , "ZTZT"))
			self.signal_WBHT_hist_AT1b.append(self.load_signal_hist("AT1b",systematic, False , "WBHT"))
			self.signal_WBZT_hist_AT1b.append(self.load_signal_hist("AT1b",systematic, False , "WBZT"))
			self.signal_HTZT_hist_AT1b.append(self.load_signal_hist("AT1b",systematic, False , "HTZT"))



			### AT0b
			self.signal_WBWB_hist_AT0b.append(self.load_signal_hist("AT0b",systematic, False , "WBWB"))
			self.signal_HTHT_hist_AT0b.append(self.load_signal_hist("AT0b",systematic, False , "HTHT"))
			self.signal_ZTZT_hist_AT0b.append(self.load_signal_hist("AT0b",systematic, False , "ZTZT"))
			self.signal_WBHT_hist_AT0b.append(self.load_signal_hist("AT0b",systematic, False , "WBHT"))
			self.signal_WBZT_hist_AT0b.append(self.load_signal_hist("AT0b",systematic, False , "WBZT"))
			self.signal_HTZT_hist_AT0b.append(self.load_signal_hist("AT0b",systematic, False , "HTZT"))






		self.QCD_linear_SR 	  = []
		self.TTbar_linear_SR  = []
		self.ST_linear_SR 	  = []
		self.data_linear_SR   = []
		self.signal_linear_SR = []

		self.QCD_linear_CR 	  = []
		self.TTbar_linear_CR  = []
		self.ST_linear_CR	 = []
		self.data_linear_CR   = []
		self.signal_linear_CR = []

		self.QCD_linear_AT0b	 = []
		self.TTbar_linear_AT0b   = []
		self.ST_linear_AT0b	  = []
		self.data_linear_AT0b	= []
		self.signal_linear_AT0b  = []

		self.QCD_linear_AT1b 	= []
		self.TTbar_linear_AT1b 	= []
		self.ST_linear_AT1b 	= []
		self.data_linear_AT1b 	= []
		self.signal_linear_AT1b = []

		if self.doATxtb:
			self.QCD_linear_AT1tb 	= []
			self.TTbar_linear_AT1tb = []
			self.ST_linear_AT1tb 	= []
			self.data_linear_AT1tb 	= []
			self.signal_linear_AT1tb = []

			self.QCD_linear_AT0tb 	= []
			self.TTbar_linear_AT0tb = []
			self.ST_linear_AT0tb 	= []
			self.data_linear_AT0tb 	= []
			self.signal_linear_AT0tb = []

			self.all_combined_linear_AT0tb = []
			self.all_combined_linear_AT1tb = []

		if self.doSideband:
			self.QCD_linear_SB1b 	= []
			self.TTbar_linear_SB1b 	= []
			self.ST_linear_SB1b 	= []
			self.data_linear_SB1b 	= []
			self.signal_linear_SB1b = []

			self.QCD_linear_SB0b 	= []
			self.TTbar_linear_SB0b 	= []
			self.ST_linear_SB0b 	= []
			self.data_linear_SB0b 	= []
			self.signal_linear_SB0b = []

			self.all_combined_linear_SB1b = []
			self.all_combined_linear_SB0b = []



		if self.includeTTTo:
			self.TTTo_linear_SR  		 = []
			self.TTTo_linear_CR  		 = []
			self.TTTo_linear_AT1b  		 = []
			self.TTTo_linear_AT0b  		 = []

			if self.doSideband:
				self.TTTo_linear_SB1b  		 = []
				self.TTTo_linear_SB0b  		 = []
			if self.doATxtb:
				self.TTTo_linear_AT1tb  		 = []
				self.TTTo_linear_AT0tb  		 = []

		if self.includeWJets:
			self.WJets_linear_SR  = []
			self.WJets_linear_CR  = []
			self.WJets_linear_AT1b  = []
			self.WJets_linear_AT0b  = []

			if self.doSideband:
				self.WJets_linear_SB1b  = []
				self.WJets_inear_SB0b  = []
			if self.doATxtb:
				self.WJets_linear_AT0tb  = []
				self.WJets_linear_AT1tb  = []

		self.all_combined_linear_SR   = []
		self.all_combined_linear_CR   = []
		self.all_combined_linear_AT1b = []
		self.all_combined_linear_AT0b = []



		if createDummyChannel:
			self.dummy_channel_SR   = []
			self.dummy_channel_CR   = []
			self.dummy_channel_AT1b = []
			self.dummy_channel_AT0b = []

			






		print("Linearizing histograms.")
		for iii,systematic_ in enumerate(self.systematic_names):   ### this was originally extending the
			systematic = systematic_

			sample_type = ""	
			year_str = ""

			if systematic_ in self.uncorrelated_systematics:
				if year == "2015":
					year_str = "16preAPV"
				else:
					year_str =  year[-2:]


			#if systematic == "CMS_scale": print("Linearizing scale histograms.")

			if "renorm" in systematic or "fact" in systematic: sample_type = "_QCD"
			self.QCD_linear_AT0b.append(self.linearize_plot([],"QCD","AT0b",systematic + sample_type + year_str,False, "QCD", [ self.QCD1000to1500_hist_AT0b[iii], self.QCD1500to2000_hist_AT0b[iii],  self.QCD2000toInf_hist_AT0b[iii]]))
			self.QCD_linear_AT1b.append(self.linearize_plot([],"QCD","AT1b",systematic + sample_type + year_str, False,"QCD", [ self.QCD1000to1500_hist_AT1b[iii], self.QCD1500to2000_hist_AT1b[iii],  self.QCD2000toInf_hist_AT1b[iii]]))

			if createDummyChannel:    ## create an empty, dummy channel for each region
				self.dummy_channel_AT1b.append(self.create_dummy_channel(self.QCD1000to1500_hist_SR[iii], "AT1b", systematic + sample_type + year_str))
				self.dummy_channel_AT0b.append(self.create_dummy_channel(self.QCD1000to1500_hist_SR[iii], "AT0b", systematic + sample_type + year_str))


				



			#if self.doSideband: self.QCD_linear_SB1b.append(self.linearize_plot([],"QCD","SB1b",systematic + sample_type + year_str))
			#if self.doSideband: self.QCD_linear_SB0b.append(self.linearize_plot([],"QCD","SB0b",systematic + sample_type + year_str))

			if "renorm" in systematic or "fact" in systematic: sample_type = "_TTbar"


			TTbar_hists_AT1b = [ self.TTJets1200to2500_hist_AT1b[iii], self.TTJets2500toInf_hist_AT1b[iii]]
			TTbar_hists_AT0b = [ self.TTJets1200to2500_hist_AT0b[iii], self.TTJets2500toInf_hist_AT0b[iii]]

			if self.doATxtb:
				TTbar_hists_AT1tb = [ self.TTJets1200to2500_hist_AT1tb[iii], self.TTJets2500toInf_hist_AT1tb[iii]]
				TTbar_hists_AT0tb = [ self.TTJets1200to2500_hist_AT0tb[iii], self.TTJets2500toInf_hist_AT0tb[iii]]
			if self.doSideband:
				TTbar_hists_SB1b = [ self.TTJets1200to2500_hist_SB1b[iii]]
				TTbar_hists_SB0b = [ self.TTJets1200to2500_hist_SB0b[iii]]

			if self.includeTTJets800to1200:
				TTbar_hists_AT1b.append( self.TTJetsMCHT800to1200_AT1b[iii])
				TTbar_hists_AT0b.append(  self.TTJetsMCHT800to1200_AT0b[iii])

			self.TTbar_linear_AT0b.append(self.linearize_plot([],"TTbar","AT0b",systematic + sample_type + year_str, False,"TTbar", TTbar_hists_AT0b))
			self.TTbar_linear_AT1b.append(self.linearize_plot([],"TTbar","AT1b",systematic + sample_type + year_str, False,"TTbar", TTbar_hists_AT1b))

			#if self.doSideband: self.TTbar_linear_SB1b.append(self.linearize_plot([],"TTbar","SB1b",systematic + sample_type + year_str))
			#if self.doSideband: self.TTbar_linear_SB0b.append(self.linearize_plot([],"TTbar","SB0b",systematic + sample_type + year_str))

			if "renorm" in systematic or "fact" in systematic: sample_type = "_sig"
			self.signal_linear_AT0b.append(self.linearize_plot([],"sig","AT0b",systematic + sample_type + year_str, False,"sig", [ self.signal_WBWB_hist_AT0b[iii], self.signal_HTHT_hist_AT0b[iii], self.signal_ZTZT_hist_AT0b[iii], self.signal_WBHT_hist_AT0b[iii], self.signal_WBZT_hist_AT0b[iii], self.signal_HTZT_hist_AT0b[iii]]))
			self.signal_linear_AT1b.append(self.linearize_plot([],"sig","AT1b",systematic + sample_type + year_str,  False,"sig", [ self.signal_WBWB_hist_AT1b[iii], self.signal_HTHT_hist_AT1b[iii], self.signal_ZTZT_hist_AT1b[iii], self.signal_WBHT_hist_AT1b[iii], self.signal_WBZT_hist_AT1b[iii], self.signal_HTZT_hist_AT1b[iii]]))

			#print("iii/systematic: %s/%s"%(iii,systematic))
			#print("self.signal_hist_SB1b is ", self.signal_hist_SB1b, self.doSideband, self.technique_str)

			#if self.doSideband: self.signal_linear_SB1b.append(self.linearize_plot([],"sig","SB1b",systematic + sample_type + year_str))
			#if self.doSideband: self.signal_linear_SB0b.append(self.linearize_plot([],"sig","SB0b",systematic + sample_type + year_str))

			if "renorm" in systematic or "fact" in systematic: sample_type = "_ST"
			self.ST_linear_AT0b.append(self.linearize_plot([],"ST","AT0b",systematic + sample_type + year_str, False,"ST", [ self.ST_t_channel_top_hist_AT0b[iii], self.ST_t_channel_antitop_hist_AT0b[iii], self.ST_s_channel_hadrons_hist_AT0b[iii], self.ST_s_channel_leptons_hist_AT0b[iii], self.ST_tW_antitop_hist_AT0b[iii],self.ST_tW_top_hist_AT0b[iii]] ))
			self.ST_linear_AT1b.append(self.linearize_plot([],"ST","AT1b",systematic + sample_type + year_str, False,"ST", [ self.ST_t_channel_top_hist_AT1b[iii], self.ST_t_channel_antitop_hist_AT1b[iii], self.ST_s_channel_hadrons_hist_AT1b[iii], self.ST_s_channel_leptons_hist_AT1b[iii], self.ST_tW_antitop_hist_AT1b[iii],self.ST_tW_top_hist_AT1b[iii]] ))


			## new stuff
			if self.includeWJets:
				if "renorm" in systematic or "fact" in systematic: sample_type = "_WJets"
				self.WJets_linear_AT0b.append(self.linearize_plot([],"WJets","AT0b",systematic + sample_type + year_str, False,"WJets", [ self.WJetsMC_LNu_HT800to1200_AT1b[iii], self.WJetsMC_LNu_HT1200to2500_AT1b[iii], self.WJetsMC_LNu_HT2500toInf_AT1b[iii], self.WJetsMC_QQ_HT800toInf_AT1b[iii] ] ))
				self.WJets_linear_AT1b.append(self.linearize_plot([],"WJets","AT1b",systematic + sample_type + year_str, False,"WJets", [	self.WJetsMC_LNu_HT800to1200_AT0b[iii], self.WJetsMC_LNu_HT1200to2500_AT0b[iii], self.WJetsMC_LNu_HT2500toInf_AT0b[iii], self.WJetsMC_QQ_HT800toInf_AT0b[iii] ] ))

			if self.includeTTTo:
				if "renorm" in systematic or "fact" in systematic: sample_type = "_TTbar" 
				self.TTTo_linear_AT0b.append(self.linearize_plot([],"TTTo","AT0b",systematic + sample_type + year_str, False,"TTTo", [ self.TTToHadronicMC_AT0b[iii], self.TTToSemiLeptonicMC_AT0b[iii], self.TTToLeptonicMC_AT0b[iii] ] ))
				self.TTTo_linear_AT1b.append(self.linearize_plot([],"TTTo","AT1b",systematic + sample_type + year_str, False,"TTTo", [ self.TTToHadronicMC_AT1b[iii], self.TTToSemiLeptonicMC_AT1b[iii], self.TTToLeptonicMC_AT1b[iii]] ))



		if not self.WP:
			for iii, systematic_ in enumerate(self.data_systematic_names):

				year_str = ""
				sample_type = ""
				systematic = systematic_
				if systematic_ in self.uncorrelated_systematics:
					if year == "2015":
						year_str = "16preAPV"
					else:
						year_str =  year[-2:]

				self.data_linear_AT0b.append(self.linearize_plot(self.data_hist_AT0b[iii],"data_obs","AT0b",systematic + sample_type + year_str))
				self.data_linear_AT1b.append(self.linearize_plot(self.data_hist_AT1b[iii],"data_obs","AT1b",systematic + sample_type + year_str))


		print("Creating combined histograms.")
		self.create_combined_linearized_hists()

		### add stat uncertainty variations to lists	
		print("Adding stat uncertainty information.")	
		#self.add_stat_uncertainties()


		print("Writing histograms.")
		self.write_histograms()
		if doExtras:
			self.print_histograms()


		# kill the linearized hists and individual signal hists
		self.kill_histograms()


	def create_combined_linearized_hists(self):


		for iii,systematic_hist_list in enumerate(self.QCD_linear_AT1b):
			self.all_combined_linear_AT1b.append( [  ] )
			systematic_name = self.systematic_names[iii]

			sample_type = ""	
			year_str = ""
			if systematic_name in self.uncorrelated_systematics:
				if self.year == "2015":
					year_str = "16preAPV"
				else:
					year_str =  year[-2:]

			systematic_name = systematic_name + sample_type + year_str

			if systematic_name in ["CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_scale"] :
				sample_str = "allBR"
				systematic_name += "_%s"%sample_str

			if systematic_name == "nom":	# 
				sys_updown = [""]
			else:
				sys_updown = ["_%sUp"%systematic_name,"_%sDown"%systematic_name]
			for jjj,sys_str in enumerate(sys_updown):
				combined_hist = self.QCD_linear_AT1b[iii][jjj].Clone("allBR%s"%sys_str)
				combined_hist.Sumw2()
				combined_hist.Add( self.TTbar_linear_AT1b[iii][jjj] )
				combined_hist.Add( self.ST_linear_AT1b[iii][jjj] )
				if self.includeWJets: combined_hist.Add( self.WJets_linear_AT1b[iii][jjj] )
				self.all_combined_linear_AT1b[iii].append( combined_hist  )


		for iii,systematic_hist_list in enumerate(self.QCD_linear_AT0b):
			self.all_combined_linear_AT0b.append( [  ] )
			systematic_name = self.systematic_names[iii]

			sample_type = ""	
			year_str = ""
			if systematic_name in self.uncorrelated_systematics:
				if self.year == "2015":
					year_str = "16preAPV"
				else:
					year_str =  year[-2:]

			systematic_name = systematic_name + sample_type + year_str

			if systematic_name in ["CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_scale"] :
				sample_str = "allBR"
				systematic_name += "_%s"%sample_str

			if systematic_name == "nom":	
				sys_updown = [""]
			else:
				sys_updown = ["_%sUp"%systematic_name,"_%sDown"%systematic_name]
			for jjj,sys_str in enumerate(sys_updown):
				combined_hist = self.QCD_linear_AT0b[iii][jjj].Clone("allBR%s"%sys_str)
				combined_hist.Sumw2()
				combined_hist.Add( self.TTbar_linear_AT0b[iii][jjj] )
				combined_hist.Add( self.ST_linear_AT0b[iii][jjj] )
				if self.includeWJets: combined_hist.Add( self.WJets_linear_AT0b[iii][jjj] )
				self.all_combined_linear_AT0b[iii].append( combined_hist  )


		if self.doATxtb:
			## AT0tb
			for iii,systematic_hist_list in enumerate(self.QCD_linear_AT0tb):
				self.all_combined_linear_AT0tb.append( [  ] )
				systematic_name = self.systematic_names[iii]

				sample_type = ""	
				year_str = ""
				if systematic_name in self.uncorrelated_systematics:
					if self.year == "2015":
						year_str = "16preAPV"
					else:
						year_str =  year[-2:]

				systematic_name = systematic_name + sample_type + year_str

				if systematic_name in ["CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_scale"] :
					sample_str = "allBR"
					systematic_name += "_%s"%sample_str

				if systematic_name == "nom":	
					sys_updown = [""] 
				else:
					sys_updown = ["_%sUp"%systematic_name,"_%sDown"%systematic_name]
				for jjj,sys_str in enumerate(sys_updown):
					combined_hist = self.QCD_linear_AT0tb[iii][jjj].Clone("allBR%s"%sys_str)
					combined_hist.Sumw2()
					combined_hist.Add( self.TTbar_linear_AT0tb[iii][jjj] )
					combined_hist.Add( self.ST_linear_AT0tb[iii][jjj] )
				if self.includeWJets: combined_hist.Add( self.WJets_linear_AT0tb[iii][jjj] )
				self.all_combined_linear_AT0tb[iii].append( combined_hist  )

			## AT1tb
			for iii,systematic_hist_list in enumerate(self.QCD_linear_AT1tb):
				self.all_combined_linear_AT1tb.append( [  ] )
				systematic_name = self.systematic_names[iii]

				sample_type = ""	
				year_str = ""
				if systematic_name in self.uncorrelated_systematics:
					if self.year == "2015":
						year_str = "16preAPV"
					else:
						year_str =  year[-2:]

				systematic_name = systematic_name + sample_type + year_str

				if systematic_name in ["CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_scale"] :
					sample_str = "allBR"
					systematic_name += "_%s"%sample_str

				if systematic_name == "nom":	
					sys_updown = [""]
				else:
					sys_updown = ["_%sUp"%systematic_name,"_%sDown"%systematic_name]
				for jjj,sys_str in enumerate(sys_updown):
					combined_hist = self.QCD_linear_AT1tb[iii][jjj].Clone("allBR%s"%sys_str)
					combined_hist.Sumw2()
					combined_hist.Add( self.TTbar_linear_AT1tb[iii][jjj] )
					combined_hist.Add( self.ST_linear_AT1tb[iii][jjj] )
				if self.includeWJets: combined_hist.Add( self.WJets_linear_AT1tb[iii][jjj] )
				self.all_combined_linear_AT1tb[iii].append( combined_hist  )

		if self.doSideband:
			## SB1b
			for iii,systematic_hist_list in enumerate(self.QCD_linear_SB1b):
				self.all_combined_linear_SB1b.append( [  ] )
				systematic_name = self.systematic_names[iii]

				sample_type = ""	
				year_str = ""
				if systematic_name in self.uncorrelated_systematics:
					if self.year == "2015":
						year_str = "16preAPV"
					else:
						year_str =  year[-2:]

				systematic_name = systematic_name + sample_type + year_str

				if systematic_name in ["CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_scale"] :
					sample_str = "allBR"
					systematic_name += "_%s"%sample_str

				if systematic_name == "nom":	
					sys_updown = [""]
				else:
					sys_updown = ["_%sUp"%systematic_name,"_%sDown"%systematic_name]
				for jjj,sys_str in enumerate(sys_updown):
					combined_hist = self.QCD_linear_SB1b[iii][jjj].Clone("allBR%s"%sys_str)
					combined_hist.Sumw2()
					combined_hist.Add( self.TTbar_linear_SB1b[iii][jjj] )
					combined_hist.Add( self.ST_linear_SB1b[iii][jjj] )
					if self.includeWJets: combined_hist.Add( self.WJets_linear_SB1b[iii][jjj] )
					self.all_combined_linear_SB1b[iii].append( combined_hist  )

			## SB0b
			for iii,systematic_hist_list in enumerate(self.QCD_linear_SB0b):
				self.all_combined_linear_SB0b.append( [  ] )
				systematic_name = self.systematic_names[iii]

				sample_type = ""	
				year_str = ""
				if systematic_name in self.uncorrelated_systematics:
					if self.year == "2015":
						year_str = "16preAPV"
					else:
						year_str =  year[-2:]

				systematic_name = systematic_name + sample_type + year_str

				if systematic_name in ["CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_scale"] :
					sample_str = "allBR"
					systematic_name += "_%s"%sample_str

				if systematic_name == "nom":	
					sys_updown = [""]
				else:
					sys_updown = ["_%sUp"%systematic_name,"_%sDown"%systematic_name]
				for jjj,sys_str in enumerate(sys_updown):
					combined_hist = self.QCD_linear_SB0b[iii][jjj].Clone("allBR%s"%sys_str)
					combined_hist.Sumw2()
					combined_hist.Add( self.TTbar_linear_SB0b[iii][jjj] )
					combined_hist.Add( self.ST_linear_SB0b[iii][jjj] )
					if self.includeWJets: combined_hist.Add( self.WJets_linear_SB0b[iii][jjj] )
					self.all_combined_linear_SB0b[iii].append( combined_hist  )
		return

	def add_stat_uncertainties(self ):
		### uses the combined linearized files to create stat uncertainty variation histograms and add them to the end of the linear histogram lists 

		### now calculate the stat uncertainty and add this branch to the final histogram  
			## step 1: calculate the total stat uncertainty in each superbin ( need to use the original, un-added histograms)

			## step 2: append a new list to each of linearized-hist-lists above with the up/down stat-uncertainty histograms 
				## these are created by taking the nom linear histogram and multiplying the each bin yield  by (1+sigma) and (1-sigma)

		year_str = ""
		if self.year == "2015":
			year_str = "16preAPV"
		else:
			year_str =  year[-2:]

		#### AT1b 	
		combined_hist_AT1b = self.QCD_linear_AT1b[0][0].Clone("combined_AT1b")
		combined_hist_AT1b.Sumw2()
		combined_hist_AT1b.Add( self.TTbar_linear_AT1b[0][0] )
		combined_hist_AT1b.Add( self.ST_linear_AT1b[0][0] )

		QCD_AT1b_stat_uncert_up = self.QCD_linear_AT1b[0][0].Clone("QCD_stat%sUp"%year_str)
		QCD_AT1b_stat_uncert_up.SetTitle("linearized QCD in the AT1b (%s) (statUp)"%self.year)
		QCD_AT1b_stat_uncert_up.Reset()
		QCD_AT1b_stat_uncert_down = self.QCD_linear_AT1b[0][0].Clone("QCD_stat%sDown"%year_str)
		QCD_AT1b_stat_uncert_down.SetTitle("linearized QCD in the AT1b (%s) (statDown)"%self.year)
		QCD_AT1b_stat_uncert_down.Reset()


		TTbar_AT1b_stat_uncert_up = self.TTbar_linear_AT1b[0][0].Clone("TTbar_stat%sUp"%year_str)
		TTbar_AT1b_stat_uncert_up.SetTitle("linearized TTbar in the AT1b (%s) (statUp)"%self.year)
		TTbar_AT1b_stat_uncert_up.Reset()
		TTbar_AT1b_stat_uncert_down = self.TTbar_linear_AT1b[0][0].Clone("TTbar_stat%sDown"%year_str)
		TTbar_AT1b_stat_uncert_down.SetTitle("linearized TTbar in the AT1b (%s) (statDown)"%self.year)

		TTbar_AT1b_stat_uncert_down.Reset()

		ST_AT1b_stat_uncert_up = self.ST_linear_AT1b[0][0].Clone("ST_stat%sUp"%year_str)
		ST_AT1b_stat_uncert_up.SetTitle("linearized ST in the AT1b (%s) (statUp)"%self.year)
		ST_AT1b_stat_uncert_up.Reset()
		ST_AT1b_stat_uncert_down = self.ST_linear_AT1b[0][0].Clone("ST_stat%sDown"%year_str)
		ST_AT1b_stat_uncert_down.SetTitle("linearized ST in the AT1b (%s) (statDown)"%self.year)
		ST_AT1b_stat_uncert_down.Reset()

		if self.includeTTTo:
			TTTo_AT1b_stat_uncert_up = self.TTTo_linear_AT1b[0][0].Clone("TTTo_stat%sUp"%year_str)
			TTTo_AT1b_stat_uncert_up.SetTitle("linearized TTTo in the SR (%s) (statUp)"%self.year)
			TTTo_AT1b_stat_uncert_up.Reset()
			TTTo_AT1b_stat_uncert_down = self.TTTo_linear_AT1b[0][0].Clone("ST_stat%sDown"%year_str)
			TTTo_AT1b_stat_uncert_down.SetTitle("linearized TTTo in the SR (%s) (statDown)"%self.year)
			TTTo_AT1b_stat_uncert_down.Reset()

		if self.includeWJets:
			WJets_AT1b_stat_uncert_up = self.WJets_linear_AT1b[0][0].Clone("WJets_stat%sUp"%year_str)
			WJets_AT1b_stat_uncert_up.SetTitle("linearized WJets in the AT1b (%s) (statUp)"%self.year)
			WJets_AT1b_stat_uncert_up.Reset()
			WJets_AT1b_stat_uncert_down = self.WJets_linear_AT1b[0][0].Clone("WJets_stat%sDown"%year_str)
			WJets_AT1b_stat_uncert_down.SetTitle("linearized WJets in the AT1b (%s) (statDown)"%self.year)
			WJets_AT1b_stat_uncert_down.Reset()

		allBR_stat_uncert_up = self.all_combined_linear_AT1b[0][0].Clone("allBR_stat%sUp"%year_str)
		allBR_stat_uncert_up.SetTitle("linearized allBR in the AT1b (%s) (statUp)"%self.year)
		allBR_stat_uncert_up.Reset()
		allBR_stat_uncert_down = self.all_combined_linear_AT1b[0][0].Clone("allBR_stat%sDown"%year_str)
		allBR_stat_uncert_down.SetTitle("linearized allBR in the AT1b (%s) (statDown)"%self.year)
		allBR_stat_uncert_down.Reset()

		allBR_stat_uncert_up_FULL = self.all_combined_linear_AT1b[0][0].Clone("dummyChannel_stat%sUp"%year_str)
		allBR_stat_uncert_up_FULL.SetTitle("linearized dummyChannel in the AT1b (%s) (statUp)"%self.year)
		allBR_stat_uncert_up_FULL.Reset()
		allBR_stat_uncert_down_FULL = self.all_combined_linear_AT1b[0][0].Clone("dummyChannel_stat%sDown"%year_str)
		allBR_stat_uncert_down_FULL.SetTitle("linearized dummyChannel in the AT1b (%s) (statDown)"%self.year)
		allBR_stat_uncert_down_FULL.Reset()


		for iii in range(1,self.QCD_linear_AT1b[0][0].GetNbinsX()+1):
			total_bin_stat_uncert = combined_hist_AT1b.GetBinError(iii)
			total_bin_nom_value   = combined_hist_AT1b.GetBinContent(iii)

			QCD_bin_nom_value	 = self.QCD_linear_AT1b[0][0].GetBinContent(iii)
			QCD_bin_nom_uncert	= self.QCD_linear_AT1b[0][0].GetBinError(iii) ## should be correctly calculated in linearize_plot()
			#print("AT1b QCD uncert is %s for bin %s with %s counts."%(QCD_bin_nom_uncert,iii,QCD_bin_nom_value))

			TTbar_bin_nom_value	 = self.TTbar_linear_AT1b[0][0].GetBinContent(iii)
			TTbar_bin_nom_uncert	= self.TTbar_linear_AT1b[0][0].GetBinError(iii)
			#print("AT1b TTbar uncert is %s for bin %s with %s counts."%(TTbar_bin_nom_uncert,iii,TTbar_bin_nom_value))

			ST_bin_nom_value	 = self.ST_linear_AT1b[0][0].GetBinContent(iii)
			ST_bin_nom_uncert	= self.ST_linear_AT1b[0][0].GetBinError(iii)

			if self.includeTTTo:
				TTTo_bin_nom_value	 = self.TTTo_linear_AT1b[0][0].GetBinContent(iii)
				TTTo_bin_nom_uncert	= self.TTTo_linear_AT1b[0][0].GetBinError(iii)
			if self.includeWJets:
				WJets_bin_nom_value	 = self.WJets_linear_AT1b[0][0].GetBinContent(iii)
				WJets_bin_nom_uncert	= self.WJets_linear_AT1b[0][0].GetBinError(iii)

			#print("AT1b ST uncert is %s for bin %s with %s counts."%(ST_bin_nom_uncert,iii,ST_bin_nom_value)
			#print("AT1b total_bin_stat_uncert is %s for bin %s with %s entries."%(total_bin_stat_uncert,iii, total_bin_nom_value))

			QCD_AT1b_stat_uncert_up.SetBinContent(iii, QCD_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
			QCD_AT1b_stat_uncert_up.SetBinError(iii, QCD_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
			QCD_AT1b_stat_uncert_down.SetBinContent(iii, QCD_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
			QCD_AT1b_stat_uncert_down.SetBinError(iii, QCD_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

			TTbar_AT1b_stat_uncert_up.SetBinContent(iii, TTbar_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
			TTbar_AT1b_stat_uncert_up.SetBinError(iii, TTbar_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
			TTbar_AT1b_stat_uncert_down.SetBinContent(iii, TTbar_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
			TTbar_AT1b_stat_uncert_down.SetBinError(iii, TTbar_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

			ST_AT1b_stat_uncert_up.SetBinContent(iii, ST_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
			ST_AT1b_stat_uncert_up.SetBinError(iii, ST_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
			ST_AT1b_stat_uncert_down.SetBinContent(iii, ST_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
			ST_AT1b_stat_uncert_down.SetBinError(iii, ST_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

			if self.includeTTTo:
				TTTo_AT1b_stat_uncert_up.SetBinContent(iii, TTTo_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				TTTo_AT1b_stat_uncert_up.SetBinError(iii, TTTo_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				TTTo_AT1b_stat_uncert_down.SetBinContent(iii, TTTo_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				TTTo_AT1b_stat_uncert_down.SetBinError(iii, TTTo_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))
			if self.includeWJets:
				WJets_AT1b_stat_uncert_up.SetBinContent(iii, WJets_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				WJets_AT1b_stat_uncert_up.SetBinError(iii, WJets_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				WJets_AT1b_stat_uncert_down.SetBinContent(iii, WJets_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				WJets_AT1b_stat_uncert_down.SetBinError(iii, WJets_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

			allBR_stat_uncert_up.SetBinContent(iii,(total_bin_stat_uncert/total_bin_nom_value)  )
			allBR_stat_uncert_up.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))
			allBR_stat_uncert_down.SetBinContent(iii, (total_bin_stat_uncert/total_bin_nom_value)  )
			allBR_stat_uncert_down.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))

			allBR_stat_uncert_up_FULL.SetBinContent(iii,1+(total_bin_stat_uncert/total_bin_nom_value)  )
			allBR_stat_uncert_up_FULL.SetBinError(iii, 1+(total_bin_stat_uncert/total_bin_nom_value))
			allBR_stat_uncert_down_FULL.SetBinContent(iii, 1-(total_bin_stat_uncert/total_bin_nom_value)  )
			allBR_stat_uncert_down_FULL.SetBinError(iii, 1-(total_bin_stat_uncert/total_bin_nom_value))



		self.QCD_linear_AT1b.append([QCD_AT1b_stat_uncert_up, QCD_AT1b_stat_uncert_down])
		self.TTbar_linear_AT1b.append([ TTbar_AT1b_stat_uncert_up, TTbar_AT1b_stat_uncert_down])
		self.ST_linear_AT1b.append([  ST_AT1b_stat_uncert_up, ST_AT1b_stat_uncert_down	 ])
		if self.includeWJets: self.WJets_linear_AT1b.append([  WJets_AT1b_stat_uncert_up, WJets_AT1b_stat_uncert_down	 ])
		if self.includeTTTo: self.TTTo_linear_AT1b.append([  TTTo_AT1b_stat_uncert_up, TTTo_AT1b_stat_uncert_down	 ]) 

		self.all_combined_linear_AT1b.append([ allBR_stat_uncert_up, allBR_stat_uncert_down	  ])
		if self.createDummyChannel: self.dummy_channel_AT1b.append([ allBR_stat_uncert_up_FULL, allBR_stat_uncert_down_FULL	  ])


		## kill unecessay histograms
		del QCD_AT1b_stat_uncert_up,  QCD_AT1b_stat_uncert_down, TTbar_AT1b_stat_uncert_up, TTbar_AT1b_stat_uncert_down, ST_AT1b_stat_uncert_up, ST_AT1b_stat_uncert_down, allBR_stat_uncert_up, allBR_stat_uncert_down
		if self.includeWJets: del WJets_AT1b_stat_uncert_up, WJets_AT1b_stat_uncert_down
		if self.includeTTTo:  del TTTo_AT1b_stat_uncert_up, TTTo_AT1b_stat_uncert_down
		#### AT0b 	
		combined_hist_AT0b = self.QCD_linear_AT0b[0][0].Clone("combined_AT0b")
		combined_hist_AT0b.Sumw2()
		combined_hist_AT0b.Add( self.TTbar_linear_AT0b[0][0] )
		combined_hist_AT0b.Add( self.ST_linear_AT0b[0][0] )

		QCD_AT0b_stat_uncert_up = self.QCD_linear_AT0b[0][0].Clone("QCD_stat%sUp"%year_str)
		QCD_AT0b_stat_uncert_up.SetTitle("linearized QCD in the AT0b (%s) (statUp)"%self.year)
		QCD_AT0b_stat_uncert_up.Reset()
		QCD_AT0b_stat_uncert_down = self.QCD_linear_AT0b[0][0].Clone("QCD_stat%sDown"%year_str)
		QCD_AT0b_stat_uncert_down.SetTitle("linearized QCD in the AT0b (%s) (statDown)"%self.year)
		QCD_AT0b_stat_uncert_down.Reset()


		TTbar_AT0b_stat_uncert_up = self.TTbar_linear_AT0b[0][0].Clone("TTbar_stat%sUp"%year_str)
		TTbar_AT0b_stat_uncert_up.SetTitle("linearized TTbar in the AT0b (%s) (statUp)"%self.year)
		TTbar_AT0b_stat_uncert_up.Reset()
		TTbar_AT0b_stat_uncert_down = self.TTbar_linear_AT0b[0][0].Clone("TTbar_stat%sDown"%year_str)
		TTbar_AT0b_stat_uncert_down.SetTitle("linearized TTbar in the AT0b (%s) (statDown)"%self.year)

		TTbar_AT0b_stat_uncert_down.Reset()

		ST_AT0b_stat_uncert_up = self.ST_linear_AT0b[0][0].Clone("ST_stat%sUp"%year_str)
		ST_AT0b_stat_uncert_up.SetTitle("linearized ST in the AT0b (%s) (statUp)"%self.year)
		ST_AT0b_stat_uncert_up.Reset()
		ST_AT0b_stat_uncert_down = self.ST_linear_AT0b[0][0].Clone("ST_stat%sDown"%year_str)
		ST_AT0b_stat_uncert_down.SetTitle("linearized ST in the AT0b (%s) (statDown)"%self.year)
		ST_AT0b_stat_uncert_down.Reset()

		if self.includeTTTo:
			TTTo_AT0b_stat_uncert_up = self.TTTo_linear_AT0b[0][0].Clone("TTTo_stat%sUp"%year_str)
			TTTo_AT0b_stat_uncert_up.SetTitle("linearized TTTo in the SR (%s) (statUp)"%self.year)
			TTTo_AT0b_stat_uncert_up.Reset()
			TTTo_AT0b_stat_uncert_down = self.TTTo_linear_AT0b[0][0].Clone("ST_stat%sDown"%year_str)
			TTTo_AT0b_stat_uncert_down.SetTitle("linearized TTTo in the SR (%s) (statDown)"%self.year)
			TTTo_AT0b_stat_uncert_down.Reset()
		if self.includeWJets:
			WJets_AT0b_stat_uncert_up = self.WJets_linear_AT0b[0][0].Clone("WJets_stat%sUp"%year_str)
			WJets_AT0b_stat_uncert_up.SetTitle("linearized WJets in the AT0b (%s) (statUp)"%self.year)
			WJets_AT0b_stat_uncert_up.Reset()
			WJets_AT0b_stat_uncert_down = self.WJets_linear_AT0b[0][0].Clone("WJets_stat%sDown"%year_str)
			WJets_AT0b_stat_uncert_down.SetTitle("linearized WJets in the AT0b (%s) (statDown)"%self.year)
			WJets_AT0b_stat_uncert_down.Reset()

		allBR_stat_uncert_up = self.all_combined_linear_AT0b[0][0].Clone("allBR_stat%sUp"%year_str)
		allBR_stat_uncert_up.SetTitle("linearized allBR in the AT0b (%s) (statUp)"%self.year)
		allBR_stat_uncert_up.Reset()
		allBR_stat_uncert_down = self.all_combined_linear_AT0b[0][0].Clone("allBR_stat%sDown"%year_str)
		allBR_stat_uncert_down.SetTitle("linearized allBR in the AT0b (%s) (statDown)"%self.year)
		allBR_stat_uncert_down.Reset()


		allBR_stat_uncert_up_FULL = self.all_combined_linear_AT0b[0][0].Clone("dummyChannel_stat%sUp"%year_str)
		allBR_stat_uncert_up_FULL.SetTitle("linearized dummyChannel in the AT0b (%s) (statUp)"%self.year)
		allBR_stat_uncert_up_FULL.Reset()
		allBR_stat_uncert_down_FULL = self.all_combined_linear_AT0b[0][0].Clone("dummyChannel_stat%sDown"%year_str)
		allBR_stat_uncert_down_FULL.SetTitle("linearized dummyChannel in the AT0b (%s) (statDown)"%self.year)
		allBR_stat_uncert_down_FULL.Reset()

		for iii in range(1,self.QCD_linear_AT0b[0][0].GetNbinsX()+1):
			total_bin_stat_uncert = combined_hist_AT0b.GetBinError(iii)
			total_bin_nom_value   = combined_hist_AT0b.GetBinContent(iii)

			QCD_bin_nom_value	 = self.QCD_linear_AT0b[0][0].GetBinContent(iii)
			QCD_bin_nom_uncert	= self.QCD_linear_AT0b[0][0].GetBinError(iii) ## should be correctly calculated in linearize_plot()
			#print("AT0b QCD uncert is %s for bin %s with %s counts."%(QCD_bin_nom_uncert,iii,QCD_bin_nom_value))

			TTbar_bin_nom_value	 = self.TTbar_linear_AT0b[0][0].GetBinContent(iii)
			TTbar_bin_nom_uncert	= self.TTbar_linear_AT0b[0][0].GetBinError(iii)
			#print("AT0b TTbar uncert is %s for bin %s with %s counts."%(TTbar_bin_nom_uncert,iii,TTbar_bin_nom_value))

			ST_bin_nom_value	 = self.ST_linear_AT0b[0][0].GetBinContent(iii)
			ST_bin_nom_uncert	= self.ST_linear_AT0b[0][0].GetBinError(iii)


			if self.includeTTTo:
				TTTo_bin_nom_value	 = self.TTTo_linear_AT0b[0][0].GetBinContent(iii)
				TTTo_bin_nom_uncert	= self.TTTo_linear_AT0b[0][0].GetBinError(iii)
			if self.includeWJets:
				WJets_bin_nom_value	 = self.WJets_linear_AT0b[0][0].GetBinContent(iii)
				WJets_bin_nom_uncert	= self.WJets_linear_AT0b[0][0].GetBinError(iii)

			#print("AT0b ST uncert is %s for bin %s with %s counts."%(ST_bin_nom_uncert,iii,ST_bin_nom_value))


			#print("AT0b total_bin_stat_uncert is %s for bin %s with %s entries."%(total_bin_stat_uncert,iii, total_bin_nom_value))

			QCD_AT0b_stat_uncert_up.SetBinContent(iii, QCD_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
			QCD_AT0b_stat_uncert_up.SetBinError(iii, QCD_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
			QCD_AT0b_stat_uncert_down.SetBinContent(iii, QCD_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
			QCD_AT0b_stat_uncert_down.SetBinError(iii, QCD_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

			TTbar_AT0b_stat_uncert_up.SetBinContent(iii, TTbar_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
			TTbar_AT0b_stat_uncert_up.SetBinError(iii, TTbar_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
			TTbar_AT0b_stat_uncert_down.SetBinContent(iii, TTbar_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
			TTbar_AT0b_stat_uncert_down.SetBinError(iii, TTbar_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

			ST_AT0b_stat_uncert_up.SetBinContent(iii, ST_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
			ST_AT0b_stat_uncert_up.SetBinError(iii, ST_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
			ST_AT0b_stat_uncert_down.SetBinContent(iii, ST_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
			ST_AT0b_stat_uncert_down.SetBinError(iii, ST_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

			if self.includeTTTo:
				TTTo_AT0b_stat_uncert_up.SetBinContent(iii, TTTo_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				TTTo_AT0b_stat_uncert_up.SetBinError(iii, TTTo_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				TTTo_AT0b_stat_uncert_down.SetBinContent(iii, TTTo_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				TTTo_AT0b_stat_uncert_down.SetBinError(iii, TTTo_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))
			if self.includeWJets:
				WJets_AT0b_stat_uncert_up.SetBinContent(iii, WJets_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				WJets_AT0b_stat_uncert_up.SetBinError(iii, WJets_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				WJets_AT0b_stat_uncert_down.SetBinContent(iii, WJets_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				WJets_AT0b_stat_uncert_down.SetBinError(iii, WJets_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

			allBR_stat_uncert_up.SetBinContent(iii,(total_bin_stat_uncert/total_bin_nom_value))
			allBR_stat_uncert_up.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))
			allBR_stat_uncert_down.SetBinContent(iii, (total_bin_stat_uncert/total_bin_nom_value))
			allBR_stat_uncert_down.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))

			allBR_stat_uncert_up_FULL.SetBinContent(iii,1+(total_bin_stat_uncert/total_bin_nom_value))
			allBR_stat_uncert_up_FULL.SetBinError(iii,1+(total_bin_stat_uncert/total_bin_nom_value))
			allBR_stat_uncert_down_FULL.SetBinContent(iii, 1-(total_bin_stat_uncert/total_bin_nom_value))
			allBR_stat_uncert_down_FULL.SetBinError(iii, 1-(total_bin_stat_uncert/total_bin_nom_value))



		self.QCD_linear_AT0b.append([QCD_AT0b_stat_uncert_up, QCD_AT0b_stat_uncert_down])
		self.TTbar_linear_AT0b.append([ TTbar_AT0b_stat_uncert_up, TTbar_AT0b_stat_uncert_down])
		self.ST_linear_AT0b.append([  ST_AT0b_stat_uncert_up, ST_AT0b_stat_uncert_down	 ])
		if self.includeWJets: self.WJets_linear_AT0b.append([  WJets_AT0b_stat_uncert_up, WJets_AT0b_stat_uncert_down	 ])
		if self.includeTTTo: self.TTTo_linear_AT0b.append([  TTTo_AT0b_stat_uncert_up, TTTo_AT0b_stat_uncert_down	 ]) 
		self.all_combined_linear_AT0b.append([ allBR_stat_uncert_up, allBR_stat_uncert_down	  ])
		if self.createDummyChannel:  self.dummy_channel_AT0b.append([ allBR_stat_uncert_up_FULL, allBR_stat_uncert_down_FULL	 ])


		## kill unecessay histograms
		del QCD_AT0b_stat_uncert_up,  QCD_AT0b_stat_uncert_down, TTbar_AT0b_stat_uncert_up, TTbar_AT0b_stat_uncert_down, ST_AT0b_stat_uncert_up, ST_AT0b_stat_uncert_down, allBR_stat_uncert_up, allBR_stat_uncert_down
		if self.includeWJets: del WJets_AT0b_stat_uncert_up, WJets_AT0b_stat_uncert_down
		if self.includeTTTo:  del TTTo_AT0b_stat_uncert_up, TTTo_AT0b_stat_uncert_down

		return



	def clean_histogram(self,hist,systematic,sample):
		ROOT.TH1.AddDirectory(False)
		for iii in range(1, hist.GetNbinsX()+1):
			for jjj in range(1,hist.GetNbinsY()+1):
				if (isnan(hist.GetBinContent(iii,jjj))) or (hist.GetBinContent(iii,jjj) == float("inf")) or (hist.GetBinContent(iii,jjj) == float("-inf")) or ( abs(hist.GetBinContent(iii,jjj))> 1e10) or ( hist.GetBinContent(iii,jjj) < 0 )  :
					print("Bad value in %s for %s/%s, value = %s in bin (%s,%s) of (%s/%s)"%(hist.GetName(), systematic, sample, hist.GetBinContent(iii,jjj), iii, jjj, hist.GetNbinsX(), hist.GetNbinsY()))
					hist.SetBinContent(iii,jjj,0)

		return hist
	def get_combined_histogram(self,file_names, hist_name,folder, weights,systematic,region):  ### for signal
		ROOT.TH1.AddDirectory(False)
		 
		#print("-------------------- start loading signal files (%s) (%s) (%s) (%s) (technique=%s) ---------------------"%(self.mass_point,self.year,folder,region,self.technique_str))
		
		for iii in range(0,len(file_names)):  ### keep looping over possible signal histograms until one is found to work
			nFailed_files = 0
			nFiles = len(file_names)
			total_integral = 0
			#print("-------> Weights are : ", weights)
			folder_name = folder+"/"+hist_name

			try:
				f1 = ROOT.TFile.Open(file_names[iii],"r")

				combined_hist = f1.Get(folder_name)
				#print("Original histogram integral: %s with weight %s"%(combined_hist.Integral(), weights[iii])  )
				#print("Looking for %s in %s."%(folder_name,file_names[0]) )
				combined_hist.Scale(weights[iii])
				if weights[iii] < 0.0:
					print("ERROR: negative weight for signal histograms (%s/%s/%s/%s/%s/%s)"%(file_names[iii],hist_name,folder,weights, systematic,region))
				#print("File %s with integral %s."%(file_names[iii],combined_hist.Integral() ))
				total_integral+=combined_hist.Integral()
				
			except:
				nFailed_files+=1
				print("ERROR in file/histogram %s/%s. File or histogram not found."%(folder_name,file_names[iii]))
				continue ## continue to next 
			
			for jjj in range(iii+1,len(file_names)):
				#print("Looking for %s in %s."%(folder_name,file_names[iii]) )
				
				try:

					#print("Looking for file %s"%(file_names[jjj]))
					#print("Trying to get histogram %s"%(folder_name))
					f2 = ROOT.TFile.Open(file_names[jjj],"r")
					h2 = self.clean_histogram( f2.Get(folder_name),systematic,file_names[iii] )
					if h2.GetMinimum() < 0.0:
						print("ERROR: negative bin value (bin = %s, counts = %s) for signal histogram (%s/%s/%s/%s/%s/%s)"%(h2.GetMinimum(),file_names[iii],hist_name,folder,weights, systematic,region))
					#print("Original histogram integral: %s with weight %s"%(h2.Integral(), weights[jjj])  )
					if weights[iii] < 0.0:
						print("ERROR: negative weight for signal histograms (%s/%s/%s/%s/%s/%s)"%(file_names[iii],hist_name,folder,weights, systematic,region))
						continue
					h2.Scale(weights[jjj])
					#print("File %s (%s) (%s) (%s) with integral %s."%(file_names[jjj],self.year, self.mass_point, systematic, h2.Integral() ))
					total_integral+=h2.Integral()
					combined_hist.Add(h2)
				except:
					print("ERROR in file/histogram %s/%s. File or histogram not found."%(folder_name,file_names[jjj]))
					nFailed_files+=1
					continue 
			#print("The total integral for %s/%s/%s is %s"%(self.year,self.mass_point,systematic,total_integral))
			


			if nFailed_files > 0:  print("There were %s total files of which %s failed."%(nFiles, nFailed_files))

			
			return combined_hist


	def load_signal_hist(self,region,systematic, forStats=False, hist_type = ""):
		ROOT.TH2.SetDefaultSumw2()
		ROOT.TH1.SetDefaultSumw2()

		use_filepath = self.MC_root_file_home 
		if region in ["SB1b", "SB0b"]: use_filepath	  = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"

		decays = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]
		
		file_paths  = [ use_filepath+ "%s_%s_%s_%s_processed.root"%(self.mass_point, decay, self.year, self.WP) for decay in decays   ]

		sig_weights = [ self.sig_SF_scale*return_signal_SF.return_signal_SF(self.year,self.mass_point,decay) for decay in decays	 ]
		sig_weights_dict = { decay: self.sig_SF_scale*return_signal_SF.return_signal_SF(self.year,self.mass_point,decay) for decay in decays	}   

		#### for a given signal mass point, need to get the FULL histogram with all decays
		if forStats:
			sig_weights = [1,1,1,1,1,1]

		sys_suffix = [""]
		if systematic == "nom":
			sys_updown = ["nom"]
		else:
			sys_updown = ["%s_up"%systematic,"%s_down"%systematic]
		all_combined_signal_hist = []

		for sys_str in sys_updown:

			hist_name_signal = "%s_%s%s"%(self.final_hist_name,self.technique_str,region)
			#print("Loading signal hist %s/%s/%s"%(region,systematic,self.year))

			if hist_type == "":

				if "topPt" in systematic and "down" in sys_str:
					TH2_hist_signal = self.get_combined_histogram(file_paths, hist_name_signal, "nom", sig_weights, "nom",region)
				else:
					TH2_hist_signal = self.get_combined_histogram(file_paths, hist_name_signal, sys_str, sig_weights,systematic,region)

				TH2_hist_signal.SetDirectory(0)   # histograms lose their references when the file destructor is called
				TH2_hist_signal.SetTitle("combined Signal MC (%s) (%s) (%s)"%(self.year,region, sys_str))
				all_combined_signal_hist.append(TH2_hist_signal)
			else:

				filepath = use_filepath+ "%s_%s_%s_%s_processed.root"%(self.mass_point, hist_type, self.year, self.WP)

				f1 = ROOT.TFile.Open( filepath  ,"r")
				if "topPt" in systematic and "down" in sys_str:
					hist_name = "nom/" + hist_name_signal
				else:
					hist_name = sys_str + "/" + hist_name_signal
				
				signal_hist = None
				if f1:  signal_hist = f1.Get(hist_name)

				if not signal_hist: 
					if self.doHTdist: signal_hist = ROOT.TH1F("h_totHT_%s"%(region),"Event H_{T} (%s) (%s) (%s); H_{T} [GeV]; Events / 200 GeV"%(region, max(hist_type, "sig"),self.technique_str ),50,0.,10000);
					else: signal_hist = ROOT.TH2F("h_MSJ_mass_vs_MdSJ_%s"%(region),"Superjet mass vs diSuperjet mass (%s) (%s) (%s); diSuperjet mass [GeV];superjet mass"%(region, hist_type,self.technique_str ), 22,1250., 10000, 20, 500, 5000) # 375 * 125

				all_combined_signal_hist.append( signal_hist  )


		return all_combined_signal_hist  # load in TTbar historam, scale it, and return this version
	

	def artificial_signal_injection(self, bin_num, num_bins):
		sigma = 3 # bins
		mu = 2* (num_bins - 1) / 3
		return 0.1*np.exp(-0.5 * ((bin_num - mu) / sigma) ** 2) / 200.



	def create_dummy_channel(self,  _hist,region,   systematic): ## creates a dummy histogram (with 0 yield) for every year, region, and systematic
		ROOT.TH1.SetDefaultSumw2()
		ROOT.TH2.SetDefaultSumw2()

		mask_size = 0
		bin_mask = []
		if self.useMask:
			bin_mask   = self.load_bin_masks(region) ## bin mask for this specific region
			mask_size  = len(bin_mask)

		if systematic in ["CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_scale"] :
			sample_str = "dummyChannel"
			if systematic == "CMS_pdf": sample_str = "misc"     ### IF THE systematic is pdf and sample is NOT TTTo or sig, create a combined uncertainty  
			systematic += "_%s"%sample_str
		sys_suffix = [""]
		use_sys = ""
		if "topPt" in systematic:
			sys_updown = ["_%sUp"%systematic,"_%sDown"%systematic]
			use_sys = "topPt"
		elif systematic == "nom":
			sys_updown = [""]
			use_sys = "nom"
		else:
			sys_updown = ["_%sUp"%systematic,"_%sDown"%systematic]
			use_sys = systematic

		all_linear_plots = []

		use_indices = self.superbin_indices

		if region in ["SR","CR"]: use_region = "SR"
		elif region in ["AT1b","AT0b","AT1tb","AT0tb"]: use_region = "AT1b"   ## THIS IS NOT QUITE RIGHT, WOULD WANT CUSTOM AT1tB REGION INDICES
		elif region in ["SB1b","SB0b"]: use_region = "SB0b"

		if self.doHTdist: use_indices = all_BR_hists.HT_dist_superbins[use_region]
		elif self.doSideband and region == "SB1b": use_indices = self.superbin_indices_SB1b
		elif self.doSideband and region == "SB0b": use_indices = self.superbin_indices_SB0b
		elif region in ["AT1b", "AT0b", "AT1tb", "AT0tb"]:  use_indices = self.superbin_indices_AT
		for iii,sys_str in enumerate(sys_updown):

			linear_plot_size = len(use_indices)  - mask_size  ## subtract off mask size

			if self.doHTdist: linear_plot = ROOT.TH1F("%s%s"%("dummyChannel",sys_str),"Event H_{T} (%s) (%s) (%s); H_{T} [GeV]; Events / 200 GeV"%(region, "dummyChannel", self.technique_str ),linear_plot_size,-0.5,linear_plot_size-0.5)
			else:             linear_plot = ROOT.TH1D("%s%s"%("dummyChannel",sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%("dummyChannel",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
		

			all_linear_plots.append(linear_plot) ## add an empty histogram for the dummy channel

		return all_linear_plots



	def linearize_plot(self,_hist,BR_type,region,systematic ,forStats=False, hist_type="", split_up_hists_for_systematic = []): 
		ROOT.TH1.SetDefaultSumw2()
		ROOT.TH2.SetDefaultSumw2()



		mask_size = 0
		bin_mask = []
		if self.useMask:
			bin_mask   = self.load_bin_masks(region) ## bin mask for this specific region
			mask_size  = len(bin_mask)


		#print("BR_type / systematic are : %s/%s/%s"%(BR_type, region,systematic))
		#print( "TTTo is in %s: %s."%(BR_type, "TTTo" in BR_type))
		if systematic in ["CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_scale"] :
			sample_str = BR_type
			if   BR_type == "sig":   sample_str = "sig"
			elif "TTTo" in BR_type:  sample_str = "TTbar"   ## these use a different pdf than 
			elif systematic == "CMS_pdf": sample_str = "misc"     ### IF THE systematic is pdf and sample is NOT TTTo or sig, create a combined uncertainty  
			systematic += "_%s"%sample_str
		#print("Now the BR_type / systematic is %s/%s."%(BR_type, systematic))
		sys_suffix = [""]
		use_sys = ""
		if "topPt" in systematic:
			sys_updown = ["_%sUp"%systematic,"_%sDown"%systematic]
			use_sys = "topPt"
		elif systematic == "nom":
			sys_updown = [""]
			use_sys = "nom"
		else:
			sys_updown = ["_%sUp"%systematic,"_%sDown"%systematic]
			use_sys = systematic


		all_linear_plots = []

		use_indices = self.superbin_indices

		if region in ["SR","CR"]: use_region = "SR"
		elif region in ["AT1b","AT0b","AT1tb","AT0tb"]: use_region = "AT1b"   ## THIS IS NOT QUITE RIGHT, WOULD WANT CUSTOM AT1tB REGION INDICES
		elif region in ["SB1b","SB0b"]: use_region = "SB0b"

		if self.doHTdist: use_indices = all_BR_hists.HT_dist_superbins[use_region]
		elif self.doSideband and region == "SB1b": use_indices = self.superbin_indices_SB1b
		elif self.doSideband and region == "SB0b": use_indices = self.superbin_indices_SB0b
		elif region in ["AT1b", "AT0b", "AT1tb", "AT0tb"]:  use_indices = self.superbin_indices_AT
		for iii,sys_str in enumerate(sys_updown):


			#print("BR_type/sys_str is %s/%s"%(BR_type,sys_str))
			linear_plot_size = len(use_indices)  - mask_size  ## subtract off mask size

			#print("For %s/%s/%s/%s/%s plots created to have %s bins (number of SRCR superbins= %s, number of AT superbins= %s)"%(BR_type, region, systematic,self.year,self.technique_str, linear_plot_size,len(self.superbin_indices),len(self.superbin_indices_AT) ))

			#print("Creating a linearized histogram for %s/%s with %s bins."%(self.year,region,linear_plot_size))
			if forStats:
				if self.doHTdist: linear_plot = ROOT.TH1F("%s%s"%(BR_type,sys_str),"Event H_{T} (%s) (%s) (%s) (%s (UNSCALED); H_{T} [GeV]; Events / 200 GeV"%(region, BR_type, self.technique_str, self.WP ),linear_plot_size,-0.5,linear_plot_size-0.5)
				else: linear_plot = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s) (%s )(UNSCALED); bin; Events / bin"%(BR_type,region,year, " ".join(use_sys.split("_")), self.WP),linear_plot_size,-0.5,linear_plot_size-0.5)
			else:
				if self.doHTdist: linear_plot = ROOT.TH1F("%s%s"%(BR_type,sys_str),"Event H_{T} (%s) (%s) (%s) (%s); H_{T} [GeV]; Events / 200 GeV"%(region, BR_type, self.technique_str, self.WP ),linear_plot_size,-0.5,linear_plot_size-0.5)
				else:  linear_plot = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s) (%s); bin; Events / bin"%(BR_type,region,year, " ".join(use_sys.split("_")), self.WP),linear_plot_size,-0.5,linear_plot_size-0.5)

			linear_plot.GetYaxis().SetTitleOffset(1.48)

			num_masked_bins = 0 
			#print("Histogram name is %s."%linear_plot.GetName())
			if hist_type == "QCD":

				SF_1000to1500 = {'2015': 1.578683216 ,   '2016':1.482632755 ,  '2017': 3.126481451,  '2018': 4.289571744   }
				SF_1500to2000 = {'2015': 0.2119142341,   '2016':0.195224041 ,  '2017': 0.3197450474, '2018': 0.4947703875  }
				SF_2000toInf  = {'2015': 0.08568186031 , '2016':0.07572795371, '2017': 0.14306915,   '2018': 0.2132134533  }

				### need to lineraize the histograms separately and THEN add them to linear_plot


				linear_plot_QCD1000to1500 = ROOT.TH1D("%s%s"%("QCDMC1000to1500",sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "QCDMC1000to1500",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_QCD1500to2000 = ROOT.TH1D("%s%s"%("QCDMC1500to2000",sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "QCDMC1500to2000",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_QCD2000toInf = ROOT.TH1D("%s%s"%("QCDMC2000toInf",sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%(  "QCDMC2000toInf",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)

				linear_plot_QCD1000to1500.Sumw2(); 
				linear_plot_QCD1500to2000.Sumw2(); 
				linear_plot_QCD2000toInf.Sumw2(); 

				####### INFO 
				#### split_up_hists_for_systematic[0] is the QCD1000to1500 histogram
				#### split_up_hists_for_systematic[1] is the QCD1500to2000 histogram
				#### split_up_hists_for_systematic[2] is the QCD2000toInf  histogram


				if not self.doHTdist:

					superbin_index = 0
					for superbin_counter,superbin in enumerate(use_indices):
						total_counts_QCD1000to1500 = 0
						total_counts_QCD1500to2000 = 0
						total_counts_QCD2000toInf  = 0  
						if superbin_counter in bin_mask: 
							num_masked_bins+=1
							continue
						for _tuple in superbin:

							#if ( (split_up_hists_for_systematic[0][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0) or (split_up_hists_for_systematic[1][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0) or (split_up_hists_for_systematic[2][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0) ): ### need to verify if these need the +1 ...
							#	print("ERROR: negative histogram contribution when adding up superbins (bin = %s/%s, counts = %s)"%(_tuple[0]+1, _tuple[1]+1 ))
							
							total_counts_QCD1000to1500+=split_up_hists_for_systematic[0][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_QCD1500to2000+=split_up_hists_for_systematic[1][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							if region not in ["SB1b","SB0b"]: total_counts_QCD2000toInf+=split_up_hists_for_systematic[2][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
						#print("%s/%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, region, systematic,superbin_index,  total_counts))
						linear_plot_QCD1000to1500.SetBinContent(superbin_index+1,total_counts_QCD1000to1500)
						linear_plot_QCD1000to1500.SetBinError(superbin_index+1,sqrt(total_counts_QCD1000to1500))
						linear_plot_QCD1500to2000.SetBinContent(superbin_index+1,total_counts_QCD1500to2000)
						linear_plot_QCD1500to2000.SetBinError(superbin_index+1,sqrt(total_counts_QCD1500to2000))
						if region not in ["SB1b","SB0b"]:
							linear_plot_QCD2000toInf.SetBinContent(superbin_index+1,total_counts_QCD2000toInf)
							linear_plot_QCD2000toInf.SetBinError(superbin_index+1,sqrt(total_counts_QCD2000toInf))
						superbin_index+=1
				else:
					superbin_index = 0 ## the number of superbins that are actually used (i.e. those not masked)
					for superbin_counter,superbin in enumerate(use_indices):
						total_counts_QCD1000to1500 = 0
						total_counts_QCD1500to2000 = 0
						total_counts_QCD2000toInf  = 0
						if superbin_counter in bin_mask:
							num_masked_bins+=1
							continue
						for bin_num in superbin:
							total_counts_QCD1000to1500+=split_up_hists_for_systematic[0][iii].GetBinContent(bin_num)
							total_counts_QCD1500to2000+=split_up_hists_for_systematic[1][iii].GetBinContent(bin_num)
							if region not in ["SB1b","SB0b"]: total_counts_QCD2000toInf+=split_up_hists_for_systematic[2][iii].GetBinContent(bin_num)
						#print("%s/%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, region, systematic,superbin_index,  total_counts))
						linear_plot_QCD1000to1500.SetBinContent(superbin_index+1,total_counts_QCD1000to1500)
						linear_plot_QCD1000to1500.SetBinError(superbin_index+1,sqrt(total_counts_QCD1000to1500))
						linear_plot_QCD1500to2000.SetBinContent(superbin_index+1,total_counts_QCD1500to2000)
						linear_plot_QCD1500to2000.SetBinError(superbin_index+1,sqrt(total_counts_QCD1500to2000))
						if region not in ["SB1b","SB0b"]:
							linear_plot_QCD2000toInf.SetBinContent(superbin_index+1,total_counts_QCD2000toInf)
							linear_plot_QCD2000toInf.SetBinError(superbin_index+1,sqrt(total_counts_QCD2000toInf))
						superbin_index+=1
					"""
					linear_plot_QCD1000to1500 = split_up_hists_for_systematic[0][iii]
					linear_plot_QCD1000to1500.SetName("%s%s"%("QCDMC1000to1500",sys_str))
					linear_plot_QCD1000to1500.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "QCDMC1000to1500",region,year, " ".join(use_sys.split("_"))))
					linear_plot_QCD1500to2000 = split_up_hists_for_systematic[1][iii]
					linear_plot_QCD1000to1500.SetName("%s%s"%("QCDMC1500to2000",sys_str))
					linear_plot_QCD1000to1500.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "QCDMC1500to2000",region,year, " ".join(use_sys.split("_"))))
					linear_plot_QCD2000toInf =  split_up_hists_for_systematic[2][iii]
					linear_plot_QCD1000to1500.SetName("%s%s"%("QCDMC2000toInf",sys_str))
					linear_plot_QCD1000to1500.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "QCDMC2000toInf",region,year, " ".join(use_sys.split("_"))))"""

				linear_plot_QCD1000to1500.Sumw2(); 
				linear_plot_QCD1500to2000.Sumw2(); 
				linear_plot_QCD2000toInf.Sumw2(); 
				linear_plot.Sumw2(); 

				## scale histograms 
				linear_plot_QCD1000to1500.Scale( SF_1000to1500[self.year] )
				linear_plot_QCD1500to2000.Scale( SF_1500to2000[self.year] )
				if region not in ["SB1b","SB0b"]: linear_plot_QCD2000toInf.Scale( SF_2000toInf[self.year])

				### NOW add together with the weight information intact
				linear_plot.Add(linear_plot_QCD1000to1500)
				linear_plot.Add(linear_plot_QCD1500to2000)
				if region not in ["SB1b","SB0b"]: linear_plot.Add(linear_plot_QCD2000toInf)

				all_linear_plots.append(linear_plot)


			elif hist_type == "TTbar":
				SF_TTJetsMCHT800to1200  = {"2015":0.002884466085,"2016":0.002526405224,"2017":0.003001100916,"2018":0.004897196802}
				SF_TTJetsMCHT1200to2500 = {"2015":0.002722324842,"2016":0.002255554525,"2017":0.00267594799,"2018":0.003918532089}
				SF_TTJetsMCHT2500toInf = {"2015":0.000056798633,"2016":0.000050253843,"2017":0.00005947217,"2018":0.000084089656}


				### need to lineraize the histograms separately and THEN add them to linear_plot
				linear_plot_TTJets800to1200  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "TTJetsMCHT800to1200", region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_TTJets1200to2500 = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "TTJetsMCHT1200to2500",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_TTJets2500toInf  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "TTJetsMCHT2500toInf" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)

				linear_plot_TTJets800to1200.Sumw2()
				linear_plot_TTJets1200to2500.Sumw2()
				linear_plot_TTJets2500toInf.Sumw2()

				####### INFO 				
				#### split_up_hists_for_systematic[0] is the TTJets1200to2500 histogram
				#### split_up_hists_for_systematic[1] is the TTJets2500toInf  histogram
				#### split_up_hists_for_systematic[1] is the TTJets800to1200  histogram ## ONLY IF self.includeTTJets800to1200 == True

				#### if self.doSideband
				#### split_up_hists_for_systematic[0] is the TTJets1200to2500 histogram
				#### split_up_hists_for_systematic[1] is the TTJets800to1200 histogram


				if not self.doHTdist:
					superbin_index = 0
					for superbin_counter,superbin in enumerate(use_indices):
						total_counts_TTJets800to1200  = 0
						total_counts_TTJets1200to2500 = 0
						total_counts_TTJets2500toInf  = 0
						if superbin_counter in bin_mask:
							num_masked_bins+=1
							continue

						for _tuple in superbin:
							#if ( (split_up_hists_for_systematic[0][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0) or (split_up_hists_for_systematic[1][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0) ): ### need to verify if these need the +1 ...
							#	print("ERROR: negative histogram contribution when adding up superbins (bin = %s/%s,)"%(_tuple[0]+1, _tuple[1]+1,))
							

							if region in ["SB1b","SB0b"]:  
								total_counts_TTJets800to1200+=split_up_hists_for_systematic[1][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
								total_counts_TTJets1200to2500+=split_up_hists_for_systematic[0][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							else:
								total_counts_TTJets1200to2500+=split_up_hists_for_systematic[0][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
								total_counts_TTJets2500toInf+=split_up_hists_for_systematic[1][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
								if self.includeTTJets800to1200: total_counts_TTJets800to1200+=split_up_hists_for_systematic[2][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)

						#print("%s/%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, region, systematic,superbin_index,  total_counts))

						if region in ["SB1b","SB0b"] or self.includeTTJets800to1200:
							linear_plot_TTJets800to1200.SetBinContent(superbin_index+1,total_counts_TTJets800to1200)
							linear_plot_TTJets800to1200.SetBinError(superbin_index+1,sqrt(total_counts_TTJets800to1200))
						linear_plot_TTJets1200to2500.SetBinContent(superbin_index+1,total_counts_TTJets1200to2500)
						linear_plot_TTJets1200to2500.SetBinError(superbin_index+1,sqrt(total_counts_TTJets1200to2500))
						if region not in ["SB1b","SB0b"]: 
							linear_plot_TTJets2500toInf.SetBinContent(superbin_index+1,total_counts_TTJets2500toInf)
							linear_plot_TTJets2500toInf.SetBinError(superbin_index+1,sqrt(total_counts_TTJets2500toInf))
						superbin_index+=1


				else:
					superbin_index = 0
					for superbin_counter,superbin in enumerate(use_indices):
						if superbin_counter in bin_mask:
							num_masked_bins+=1
							continue

						total_counts_TTJets800to1200  = 0
						total_counts_TTJets1200to2500 = 0
						total_counts_TTJets2500toInf  = 0

						for bin_num in superbin:
							#if ( (split_up_hists_for_systematic[0][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0) or (split_up_hists_for_systematic[1][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0) ): ### need to verify if these need the +1 ...
							#	print("ERROR: negative histogram contribution when adding up superbins (bin = %s/%s,)"%(_tuple[0]+1, _tuple[1]+1,))
							

							if region in ["SB1b","SB0b"]:  
								total_counts_TTJets800to1200+=split_up_hists_for_systematic[1][iii].GetBinContent(bin_num)
								total_counts_TTJets1200to2500+=split_up_hists_for_systematic[0][iii].GetBinContent(bin_num)
							else:
								total_counts_TTJets1200to2500+=split_up_hists_for_systematic[0][iii].GetBinContent(bin_num)
								total_counts_TTJets2500toInf+=split_up_hists_for_systematic[1][iii].GetBinContent(bin_num)
								if self.includeTTJets800to1200: total_counts_TTJets800to1200+=split_up_hists_for_systematic[2][iii].GetBinContent(bin_num)

						#print("%s/%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, region, systematic,superbin_index,  total_counts))

						if region in ["SB1b","SB0b"] or self.includeTTJets800to1200:
							linear_plot_TTJets800to1200.SetBinContent(superbin_index+1,total_counts_TTJets800to1200)
							linear_plot_TTJets800to1200.SetBinError(superbin_index+1,sqrt(total_counts_TTJets800to1200))
						linear_plot_TTJets1200to2500.SetBinContent(superbin_index+1,total_counts_TTJets1200to2500)
						linear_plot_TTJets1200to2500.SetBinError(superbin_index+1,sqrt(total_counts_TTJets1200to2500))
						if region not in ["SB1b","SB0b"]: 
							linear_plot_TTJets2500toInf.SetBinContent(superbin_index+1,total_counts_TTJets2500toInf)
							linear_plot_TTJets2500toInf.SetBinError(superbin_index+1,sqrt(total_counts_TTJets2500toInf))
						superbin_index+=1

					"""
					if region in ["SB1b","SB0b"] :
						linear_plot_TTJets800to1200 = split_up_hists_for_systematic[1][iii]
						linear_plot_TTJets800to1200.SetName("%s%s"%("TTJets800to1200",sys_str))
						linear_plot_TTJets800to1200.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "TTJets800to1200",region,year, " ".join(use_sys.split("_"))))

						linear_plot_TTJets1200to2500 = split_up_hists_for_systematic[0][iii]
						linear_plot_TTJets1200to2500.SetName("%s%s"%("TTJets1200to2500",sys_str))
						linear_plot_TTJets1200to2500.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "TTJets1200to2500",region,year, " ".join(use_sys.split("_"))))
					else: 

						linear_plot_TTJets1200to2500 = split_up_hists_for_systematic[0][iii]
						linear_plot_TTJets1200to2500.SetName("%s%s"%("TTJets1200to2500",sys_str))
						linear_plot_TTJets1200to2500.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "TTJets1200to2500",region,year, " ".join(use_sys.split("_"))))
						linear_plot_TTJets2500toInf =  split_up_hists_for_systematic[1][iii]
						linear_plot_TTJets2500toInf.SetName("%s%s"%("TTJets2500toInf",sys_str))
						linear_plot_TTJets2500toInf.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "TTJets2500toInf",region,year, " ".join(use_sys.split("_"))))
						if self.includeTTJets800to1200:
							linear_plot_TTJets800to1200 = split_up_hists_for_systematic[2][iii]
							linear_plot_TTJets800to1200.SetName("%s%s"%("TTJets800to1200",sys_str))
							linear_plot_TTJets800to1200.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "TTJets800to1200",region,year, " ".join(use_sys.split("_")))) """


				linear_plot_TTJets800to1200.Sumw2()
				linear_plot_TTJets1200to2500.Sumw2()
				linear_plot_TTJets2500toInf.Sumw2()
				linear_plot.Sumw2(); 

				## scale histograms 
				if region in ["SB1b","SB0b"]: linear_plot_TTJets800to1200.Scale( SF_TTJetsMCHT800to1200[self.year] )
				linear_plot_TTJets1200to2500.Scale( SF_TTJetsMCHT1200to2500[self.year] )
				if region not in ["SB1b","SB0b"]:  linear_plot_TTJets2500toInf.Scale( SF_TTJetsMCHT2500toInf[self.year] )

				### NOW add together with the weight information intact
				linear_plot.Add(linear_plot_TTJets1200to2500)
				linear_plot.Add(linear_plot_TTJets2500toInf)
				if region in ["SB1b","SB0b"]: linear_plot.Add(linear_plot_TTJets800to1200)
				all_linear_plots.append(linear_plot)

			elif hist_type == "ST":
				ST_t_channel_top_5f_SF 		= {'2015':0.0409963154,  '2016':0.03607115071, '2017':0.03494669125, '2018': 0.03859114659 }
				ST_t_channel_antitop_5f_SF	= {'2015':0.05673857623, '2016':0.04102705994, '2017':0.04238814865, '2018': 0.03606630944 }
				ST_s_channel_4f_hadrons_SF	= {'2015':0.04668187234, '2016':0.03564988679, '2017':0.03985938616, '2018': 0.04102795437 }
				ST_s_channel_4f_leptons_SF	= {'2015':0.01323030083, '2016':0.01149139097, '2017':0.01117527734, '2018': 0.01155448784 }
				ST_tW_antitop_5f_SF			= {'2015':0.2967888696,  '2016':0.2301666797,  '2017':0.2556495594,  '2018': 0.2700032391  }
				ST_tW_top_5f_SF				= {'2015':0.2962796522,  '2016':0.2355829386,  '2017':0.2563403788,  '2018': 0.2625270613  }

				####### INFO 
				#### split_up_hists_for_systematic[0] is the ST_t_channel_top_5f histogram
				#### split_up_hists_for_systematic[1] is the ST_t_channel_antitop_5f  histogram
				#### split_up_hists_for_systematic[2] is the ST_s_channel_4f_hadrons  histogram
				#### split_up_hists_for_systematic[3] is the ST_s_channel_4f_leptons  histogram
				#### split_up_hists_for_systematic[4] is the ST_tW_antitop_5f  histogram
				#### split_up_hists_for_systematic[5] is the ST_tW_top_5f  histogram

				### need to lineraize the histograms separately and THEN add them to linear_plot
				linear_plot_ST_t_channel_top_5f = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "ST_t_channel_top_5f",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_ST_t_channel_antitop_5f  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "ST_t_channel_antitop_5f" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_ST_s_channel_4f_hadrons  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "ST_s_channel_4f_hadrons" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_ST_s_channel_4f_leptons  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s) ; bin; Events / bin"%( "ST_s_channel_4f_leptons" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_ST_tW_antitop_5f  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "ST_tW_antitop_5f" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_ST_tW_top_5f  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "ST_tW_top_5f" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)


				linear_plot_ST_t_channel_top_5f.Sumw2()
				linear_plot_ST_t_channel_antitop_5f.Sumw2()
				linear_plot_ST_s_channel_4f_hadrons.Sumw2()
				linear_plot_ST_s_channel_4f_leptons.Sumw2()
				linear_plot_ST_tW_antitop_5f.Sumw2()
				linear_plot_ST_tW_top_5f.Sumw2()

				if not self.doHTdist:
					superbin_index = 0
					for superbin_counter,superbin in enumerate(use_indices):
						if superbin_counter in bin_mask:
							num_masked_bins+=1
							continue
						total_counts_ST_t_channel_top_5f = 0
						total_counts_ST_t_channel_antitop_5f  = 0
						total_counts_ST_s_channel_4f_hadrons = 0
						total_counts_ST_s_channel_4f_leptons  = 0					
						total_counts_ST_tW_antitop_5f = 0
						total_counts_ST_tW_top_5f  = 0

						for _tuple in superbin:
							#if ( (split_up_hists_for_systematic[0][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0) or (split_up_hists_for_systematic[1][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0) ): ### need to verify if these need the +1 ...
							#	print("ERROR: negative histogram contribution when adding up superbins (bin = %s/%s,)"%(_tuple[0]+1, _tuple[1]+1,))
							
							total_counts_ST_t_channel_top_5f+=split_up_hists_for_systematic[0][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_ST_t_channel_antitop_5f+=split_up_hists_for_systematic[1][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_ST_s_channel_4f_hadrons+=split_up_hists_for_systematic[2][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_ST_s_channel_4f_leptons+=split_up_hists_for_systematic[3][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_ST_tW_antitop_5f+=split_up_hists_for_systematic[4][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_ST_tW_top_5f+=split_up_hists_for_systematic[5][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)

						#print("%s/%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, region, systematic,superbin_index,  total_counts))
						linear_plot_ST_t_channel_top_5f.SetBinContent(superbin_index+1,total_counts_ST_t_channel_top_5f)
						linear_plot_ST_t_channel_antitop_5f.SetBinContent(superbin_index+1,total_counts_ST_t_channel_antitop_5f)
						linear_plot_ST_s_channel_4f_hadrons.SetBinContent(superbin_index+1,total_counts_ST_s_channel_4f_hadrons)
						linear_plot_ST_s_channel_4f_leptons.SetBinContent(superbin_index+1,total_counts_ST_s_channel_4f_leptons)					
						linear_plot_ST_tW_antitop_5f.SetBinContent(superbin_index+1,total_counts_ST_tW_antitop_5f)
						linear_plot_ST_tW_top_5f.SetBinContent(superbin_index+1,total_counts_ST_tW_top_5f)

						linear_plot_ST_t_channel_top_5f.SetBinError(superbin_index+1,sqrt(total_counts_ST_t_channel_top_5f))
						linear_plot_ST_t_channel_antitop_5f.SetBinError(superbin_index+1,sqrt(total_counts_ST_t_channel_antitop_5f))
						linear_plot_ST_s_channel_4f_hadrons.SetBinError(superbin_index+1,sqrt(total_counts_ST_s_channel_4f_hadrons))
						linear_plot_ST_s_channel_4f_leptons.SetBinError(superbin_index+1,sqrt(total_counts_ST_s_channel_4f_leptons))			
						linear_plot_ST_tW_antitop_5f.SetBinError(superbin_index+1,sqrt(total_counts_ST_tW_antitop_5f))
						linear_plot_ST_tW_top_5f.SetBinError(superbin_index+1,sqrt(total_counts_ST_tW_top_5f))
						superbin_index+=1

				else:
					superbin_index = 0
					for superbin_counter,superbin in enumerate(use_indices):
						if superbin_counter in bin_mask:
							num_masked_bins+=1
							continue
						total_counts_ST_t_channel_top_5f = 0
						total_counts_ST_t_channel_antitop_5f  = 0
						total_counts_ST_s_channel_4f_hadrons = 0
						total_counts_ST_s_channel_4f_leptons  = 0					
						total_counts_ST_tW_antitop_5f = 0
						total_counts_ST_tW_top_5f  = 0

						for bin_num in superbin:
							#if ( (split_up_hists_for_systematic[0][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0) or (split_up_hists_for_systematic[1][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0) ): ### need to verify if these need the +1 ...
							#	print("ERROR: negative histogram contribution when adding up superbins (bin = %s/%s,)"%(_tuple[0]+1, _tuple[1]+1,))
							
							total_counts_ST_t_channel_top_5f+=split_up_hists_for_systematic[0][iii].GetBinContent(bin_num)
							total_counts_ST_t_channel_antitop_5f+=split_up_hists_for_systematic[1][iii].GetBinContent(bin_num)
							total_counts_ST_s_channel_4f_hadrons+=split_up_hists_for_systematic[2][iii].GetBinContent(bin_num)
							total_counts_ST_s_channel_4f_leptons+=split_up_hists_for_systematic[3][iii].GetBinContent(bin_num)
							total_counts_ST_tW_antitop_5f+=split_up_hists_for_systematic[4][iii].GetBinContent(bin_num)
							total_counts_ST_tW_top_5f+=split_up_hists_for_systematic[5][iii].GetBinContent(bin_num)

						#print("%s/%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, region, systematic,superbin_index,  total_counts))
						linear_plot_ST_t_channel_top_5f.SetBinContent(superbin_index+1,total_counts_ST_t_channel_top_5f)
						linear_plot_ST_t_channel_antitop_5f.SetBinContent(superbin_index+1,total_counts_ST_t_channel_antitop_5f)
						linear_plot_ST_s_channel_4f_hadrons.SetBinContent(superbin_index+1,total_counts_ST_s_channel_4f_hadrons)
						linear_plot_ST_s_channel_4f_leptons.SetBinContent(superbin_index+1,total_counts_ST_s_channel_4f_leptons)					
						linear_plot_ST_tW_antitop_5f.SetBinContent(superbin_index+1,total_counts_ST_tW_antitop_5f)
						linear_plot_ST_tW_top_5f.SetBinContent(superbin_index+1,total_counts_ST_tW_top_5f)

						linear_plot_ST_t_channel_top_5f.SetBinError(superbin_index+1,sqrt(total_counts_ST_t_channel_top_5f))
						linear_plot_ST_t_channel_antitop_5f.SetBinError(superbin_index+1,sqrt(total_counts_ST_t_channel_antitop_5f))
						linear_plot_ST_s_channel_4f_hadrons.SetBinError(superbin_index+1,sqrt(total_counts_ST_s_channel_4f_hadrons))
						linear_plot_ST_s_channel_4f_leptons.SetBinError(superbin_index+1,sqrt(total_counts_ST_s_channel_4f_leptons))			
						linear_plot_ST_tW_antitop_5f.SetBinError(superbin_index+1,sqrt(total_counts_ST_tW_antitop_5f))
						linear_plot_ST_tW_top_5f.SetBinError(superbin_index+1,sqrt(total_counts_ST_tW_top_5f))
						superbin_index+=1

					"""linear_plot_ST_t_channel_top_5f = split_up_hists_for_systematic[0][iii]
					linear_plot_ST_t_channel_top_5f.SetName("%s%s"%("ST_t_channel_top_5f",sys_str))
					linear_plot_ST_t_channel_top_5f.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "ST_t_channel_top_5f",region,year, " ".join(use_sys.split("_"))))

					linear_plot_ST_t_channel_antitop_5f = split_up_hists_for_systematic[1][iii]
					linear_plot_ST_t_channel_antitop_5f.SetName("%s%s"%("ST_t_channel_antitop_5f",sys_str))
					linear_plot_ST_t_channel_antitop_5f.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "ST_t_channel_antitop_5f",region,year, " ".join(use_sys.split("_"))))

					linear_plot_ST_s_channel_4f_hadrons = split_up_hists_for_systematic[2][iii]
					linear_plot_ST_s_channel_4f_hadrons.SetName("%s%s"%("ST_s_channel_4f_hadrons",sys_str))
					linear_plot_ST_s_channel_4f_hadrons.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "ST_s_channel_4f_hadrons",region,year, " ".join(use_sys.split("_"))))

					linear_plot_ST_s_channel_4f_leptons = split_up_hists_for_systematic[3][iii]
					linear_plot_ST_s_channel_4f_leptons.SetName("%s%s"%("ST_s_channel_4f_leptons",sys_str))
					linear_plot_ST_s_channel_4f_leptons.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "ST_s_channel_4f_leptons",region,year, " ".join(use_sys.split("_"))))

					linear_plot_ST_tW_antitop_5f = split_up_hists_for_systematic[4][iii]
					linear_plot_ST_tW_antitop_5f.SetName("%s%s"%("ST_tW_antitop_5f",sys_str))
					linear_plot_ST_tW_antitop_5f.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "ST_tW_antitop_5f",region,year, " ".join(use_sys.split("_"))))

					linear_plot_ST_tW_top_5f = split_up_hists_for_systematic[5][iii]
					linear_plot_ST_tW_top_5f.SetName("%s%s"%("ST_tW_top_5f",sys_str))
					linear_plot_ST_tW_top_5f.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "ST_tW_top_5f",region,year, " ".join(use_sys.split("_"))))"""

				linear_plot_ST_t_channel_top_5f.Sumw2()
				linear_plot_ST_t_channel_antitop_5f.Sumw2()
				linear_plot_ST_s_channel_4f_hadrons.Sumw2()
				linear_plot_ST_s_channel_4f_leptons.Sumw2()
				linear_plot_ST_tW_antitop_5f.Sumw2()
				linear_plot_ST_tW_top_5f.Sumw2()
				linear_plot.Sumw2(); 

				## scale histograms
				linear_plot_ST_t_channel_top_5f.Scale( ST_t_channel_top_5f_SF[self.year] )
				linear_plot_ST_t_channel_antitop_5f.Scale( ST_t_channel_antitop_5f_SF[self.year] )
				linear_plot_ST_s_channel_4f_hadrons.Scale( ST_s_channel_4f_hadrons_SF[self.year] )
				linear_plot_ST_s_channel_4f_leptons.Scale( ST_s_channel_4f_leptons_SF[self.year] )				
				linear_plot_ST_tW_antitop_5f.Scale( ST_tW_antitop_5f_SF[self.year] )
				linear_plot_ST_tW_top_5f.Scale( ST_tW_top_5f_SF[self.year] )

				### NOW add together with the weight information intact
				linear_plot.Add(linear_plot_ST_t_channel_top_5f)
				linear_plot.Add(linear_plot_ST_t_channel_antitop_5f)
				linear_plot.Add(linear_plot_ST_s_channel_4f_hadrons)
				linear_plot.Add(linear_plot_ST_s_channel_4f_leptons)				
				linear_plot.Add(linear_plot_ST_tW_antitop_5f)
				linear_plot.Add(linear_plot_ST_tW_top_5f)

				all_linear_plots.append(linear_plot)



			elif hist_type == "WJets":
				SF_WJetsMC_LNu_HT800to1200  = return_BR_SF(self.year,"WJetsMC_LNu_HT800to1200") 
				SF_WJetsMC_LNu_HT1200to2500  = return_BR_SF(self.year,"WJetsMC_LNu_HT1200to2500") 
				SF_WJetsMC_LNu_HT2500toInf  = return_BR_SF(self.year,"WJetsMC_LNu_HT2500toInf") 
				SF_WJetsMC_QQ_HT800toInf  = return_BR_SF(self.year,"WJetsMC_QQ_HT800toInf") 

				### need to lineraize the histograms separately and THEN add them to linear_plot
				linear_plot_WJetsMC_LNu_HT800to1200 = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "WJetsMC_LNu_HT800to1200",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_WJetsMC_LNu_HT1200to2500 = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "WJetsMC_LNu_HT1200to2500" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_WJetsMC_LNu_HT2500toInf  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "WJetsMC_LNu_HT2500toInf" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_WJetsMC_QQ_HT800toInf  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s) ; bin; Events / bin"%( "WJetsMC_QQ_HT800toInf" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)

				linear_plot_WJetsMC_LNu_HT800to1200.Sumw2()
				linear_plot_WJetsMC_LNu_HT1200to2500.Sumw2()
				linear_plot_WJetsMC_LNu_HT2500toInf.Sumw2()
				linear_plot_WJetsMC_QQ_HT800toInf.Sumw2()

				####### INFO 
				#### split_up_hists_for_systematic[0] is the WJetsMC_LNu_HT800to1200 histogram
				#### split_up_hists_for_systematic[1] is the WJetsMC_LNu_HT1200to2500  histogram
				#### split_up_hists_for_systematic[2] is the WJetsMC_LNu_HT2500toInf  histogram
				#### split_up_hists_for_systematic[3] is the WJetsMC_QQ_HT800toInf  histogram


				if not self.doHTdist:
					superbin_index = 0
					for superbin_counter,superbin in enumerate(use_indices):
						if superbin_counter in bin_mask: 
							num_masked_bins+=1
							continue
						total_counts_WJetsMC_LNu_HT800to1200 = 0
						total_counts_WJetsMC_LNu_HT1200to2500 = 0
						total_counts_WJetsMC_LNu_HT2500toInf = 0
						total_counts_WJetsMC_QQ_HT800toInf  = 0					
						for _tuple in superbin:

							total_counts_WJetsMC_LNu_HT800to1200+=split_up_hists_for_systematic[0][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_WJetsMC_LNu_HT1200to2500+=split_up_hists_for_systematic[1][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_WJetsMC_LNu_HT2500toInf+=split_up_hists_for_systematic[2][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_WJetsMC_QQ_HT800toInf+=split_up_hists_for_systematic[3][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)

						#print("%s/%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, region, systematic,superbin_index,  total_counts))
						linear_plot_WJetsMC_LNu_HT800to1200.SetBinContent(superbin_index+1,total_counts_WJetsMC_LNu_HT800to1200)
						linear_plot_WJetsMC_LNu_HT1200to2500.SetBinContent(superbin_index+1,total_counts_WJetsMC_LNu_HT1200to2500)
						linear_plot_WJetsMC_LNu_HT2500toInf.SetBinContent(superbin_index+1,total_counts_WJetsMC_LNu_HT2500toInf)
						linear_plot_WJetsMC_QQ_HT800toInf.SetBinContent(superbin_index+1,total_counts_WJetsMC_QQ_HT800toInf)					

						linear_plot_WJetsMC_LNu_HT800to1200.SetBinError(superbin_index+1,sqrt(total_counts_WJetsMC_LNu_HT800to1200))
						linear_plot_WJetsMC_LNu_HT1200to2500.SetBinError(superbin_index+1,sqrt(total_counts_WJetsMC_LNu_HT1200to2500))
						linear_plot_WJetsMC_LNu_HT2500toInf.SetBinError(superbin_index+1,sqrt(total_counts_WJetsMC_LNu_HT2500toInf))
						linear_plot_WJetsMC_QQ_HT800toInf.SetBinError(superbin_index+1,sqrt(total_counts_WJetsMC_QQ_HT800toInf))
						superbin_index+=1

				else:
					superbin_index = 0
					for superbin_counter,superbin in enumerate(use_indices):
						if superbin_counter in bin_mask:
							num_masked_bins+=1
							continue
						total_counts_WJetsMC_LNu_HT800to1200 = 0
						total_counts_WJetsMC_LNu_HT1200to2500 = 0
						total_counts_WJetsMC_LNu_HT2500toInf = 0
						total_counts_WJetsMC_QQ_HT800toInf  = 0					


						for bin_num in superbin:

							total_counts_WJetsMC_LNu_HT800to1200+=split_up_hists_for_systematic[0][iii].GetBinContent(bin_num)
							total_counts_WJetsMC_LNu_HT1200to2500+=split_up_hists_for_systematic[1][iii].GetBinContent(bin_num)
							total_counts_WJetsMC_LNu_HT2500toInf+=split_up_hists_for_systematic[2][iii].GetBinContent(bin_num)
							total_counts_WJetsMC_QQ_HT800toInf+=split_up_hists_for_systematic[3][iii].GetBinContent(bin_num)

						#print("%s/%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, region, systematic,superbin_index,  total_counts))
						linear_plot_WJetsMC_LNu_HT800to1200.SetBinContent(superbin_index+1,total_counts_WJetsMC_LNu_HT800to1200)
						linear_plot_WJetsMC_LNu_HT1200to2500.SetBinContent(superbin_index+1,total_counts_WJetsMC_LNu_HT1200to2500)
						linear_plot_WJetsMC_LNu_HT2500toInf.SetBinContent(superbin_index+1,total_counts_WJetsMC_LNu_HT2500toInf)
						linear_plot_WJetsMC_QQ_HT800toInf.SetBinContent(superbin_index+1,total_counts_WJetsMC_QQ_HT800toInf)					

						linear_plot_WJetsMC_LNu_HT800to1200.SetBinError(superbin_index+1,sqrt(total_counts_WJetsMC_LNu_HT800to1200))
						linear_plot_WJetsMC_LNu_HT1200to2500.SetBinError(superbin_index+1,sqrt(total_counts_WJetsMC_LNu_HT1200to2500))
						linear_plot_WJetsMC_LNu_HT2500toInf.SetBinError(superbin_index+1,sqrt(total_counts_WJetsMC_LNu_HT2500toInf))
						linear_plot_WJetsMC_QQ_HT800toInf.SetBinError(superbin_index+1,sqrt(total_counts_WJetsMC_QQ_HT800toInf))	
						superbin_index+=1

					"""linear_plot_WJetsMC_LNu_HT800to1200 = split_up_hists_for_systematic[0][iii]
					linear_plot_WJetsMC_LNu_HT800to1200.SetName("%s%s"%("_WJetsMC_LNu_HT800to1200",sys_str))
					linear_plot_WJetsMC_LNu_HT800to1200.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "WJetsMC_LNu_HT800to1200",region,year, " ".join(use_sys.split("_"))))

					linear_plot_WJetsMC_LNu_HT1200to2500 = split_up_hists_for_systematic[1][iii]
					linear_plot_WJetsMC_LNu_HT1200to2500.SetName("%s%s"%("WJetsMC_LNu_HT1200to2500",sys_str))
					linear_plot_WJetsMC_LNu_HT1200to2500.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "WJetsMC_LNu_HT1200to2500",region,year, " ".join(use_sys.split("_"))))

					linear_plot_WJetsMC_LNu_HT2500toInf = split_up_hists_for_systematic[2][iii]
					linear_plot_WJetsMC_LNu_HT2500toInf.SetName("%s%s"%("WJetsMC_LNu_HT2500toInf",sys_str))
					linear_plot_WJetsMC_LNu_HT2500toInf.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "WJetsMC_LNu_HT2500toInf",region,year, " ".join(use_sys.split("_"))))

					linear_plot_WJetsMC_QQ_HT800toInf = split_up_hists_for_systematic[3][iii]
					linear_plot_WJetsMC_QQ_HT800toInf.SetName("%s%s"%("WJetsMC_QQ_HT800toInf",sys_str))
					linear_plot_WJetsMC_QQ_HT800toInf.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "WJetsMC_QQ_HT800toInf",region,year, " ".join(use_sys.split("_"))))"""


				linear_plot_WJetsMC_LNu_HT800to1200.Sumw2()
				linear_plot_WJetsMC_LNu_HT1200to2500.Sumw2()
				linear_plot_WJetsMC_LNu_HT2500toInf.Sumw2()
				linear_plot_WJetsMC_QQ_HT800toInf.Sumw2()
				linear_plot.Sumw2()

				## scale histograms
				linear_plot_WJetsMC_LNu_HT800to1200.Scale( SF_WJetsMC_LNu_HT800to1200 )
				linear_plot_WJetsMC_LNu_HT1200to2500.Scale( SF_WJetsMC_LNu_HT1200to2500 )
				linear_plot_WJetsMC_LNu_HT2500toInf.Scale( SF_WJetsMC_LNu_HT2500toInf )
				linear_plot_WJetsMC_QQ_HT800toInf.Scale( SF_WJetsMC_QQ_HT800toInf )				

				### NOW add together with the weight information intact
				linear_plot.Add(linear_plot_WJetsMC_LNu_HT800to1200)
				linear_plot.Add(linear_plot_WJetsMC_LNu_HT1200to2500)
				linear_plot.Add(linear_plot_WJetsMC_LNu_HT2500toInf)
				linear_plot.Add(linear_plot_WJetsMC_QQ_HT800toInf)				

				all_linear_plots.append(linear_plot)



			elif hist_type == "TTTo":


				SF_TTToHadronic  = return_BR_SF(self.year,"TTToHadronicMC") 
				SF_TTToSemiLeptonic  = return_BR_SF(self.year,"TTToSemiLeptonicMC") 
				SF_TTToLeptonic  = return_BR_SF(self.year,"TTToLeptonicMC") 


				### need to lineraize the histograms separately and THEN add them to linear_plot
				linear_plot_TTToHadronic = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "TTToHadronic",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_TTToSemiLeptonic = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "TTToSemiLeptonic" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_TTToLeptonic  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "TTToLeptonic" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)


				linear_plot_TTToHadronic.Sumw2()
				linear_plot_TTToSemiLeptonic.Sumw2()
				linear_plot_TTToLeptonic.Sumw2()


				####### INFO 
				#### split_up_hists_for_systematic[0] is the TTToHadronic histogram
				#### split_up_hists_for_systematic[1] is the TTToSemiLeptonic  histogram
				#### split_up_hists_for_systematic[2] is the TTToLeptonic  histogram


				if not self.doHTdist:
					superbin_index = 0
					for superbin_counter,superbin in enumerate(use_indices):
						if superbin_counter in bin_mask: 
							num_masked_bins+=1
							continue
						total_counts_TTToHadronic = 0
						total_counts_TTToSemiLeptonic = 0
						total_counts_TTToLeptonic = 0


						for _tuple in superbin:

							total_counts_TTToHadronic+=split_up_hists_for_systematic[0][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_TTToSemiLeptonic=split_up_hists_for_systematic[1][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_TTToLeptonic+=split_up_hists_for_systematic[2][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)

						#print("%s/%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, region, systematic,superbin_index,  total_counts))
						linear_plot_TTToHadronic.SetBinContent(superbin_index+1,total_counts_TTToHadronic)
						linear_plot_TTToSemiLeptonic.SetBinContent(superbin_index+1,total_counts_TTToSemiLeptonic)
						linear_plot_TTToLeptonic.SetBinContent(superbin_index+1,total_counts_TTToLeptonic)

						linear_plot_TTToHadronic.SetBinError(superbin_index+1,sqrt(total_counts_TTToHadronic))
						linear_plot_TTToSemiLeptonic.SetBinError(superbin_index+1,sqrt(total_counts_TTToSemiLeptonic))
						linear_plot_TTToLeptonic.SetBinError(superbin_index+1,sqrt(total_counts_TTToLeptonic))
						superbin_index+=1

				else:
					superbin_index = 0
					for superbin_counter,superbin in enumerate(use_indices):
						if superbin_counter in bin_mask:
							num_masked_bins+=1
							continue
						total_counts_TTToHadronic = 0
						total_counts_TTToSemiLeptonic = 0
						total_counts_TTToLeptonic = 0

						for bin_num in superbin:

							total_counts_TTToHadronic+=split_up_hists_for_systematic[0][iii].GetBinContent(bin_num)
							total_counts_TTToSemiLeptonic=split_up_hists_for_systematic[1][iii].GetBinContent(bin_num)
							total_counts_TTToLeptonic+=split_up_hists_for_systematic[2][iii].GetBinContent(bin_num)

						#print("%s/%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, region, systematic,superbin_index,  total_counts))
						linear_plot_TTToHadronic.SetBinContent(superbin_index+1,total_counts_TTToHadronic)
						linear_plot_TTToSemiLeptonic.SetBinContent(superbin_index+1,total_counts_TTToSemiLeptonic)
						linear_plot_TTToLeptonic.SetBinContent(superbin_index+1,total_counts_TTToLeptonic)

						linear_plot_TTToHadronic.SetBinError(superbin_index+1,sqrt(total_counts_TTToHadronic))
						linear_plot_TTToSemiLeptonic.SetBinError(superbin_index+1,sqrt(total_counts_TTToSemiLeptonic))
						linear_plot_TTToLeptonic.SetBinError(superbin_index+1,sqrt(total_counts_TTToLeptonic))
						superbin_index+=1

					"""linear_plot_TTToHadronic = split_up_hists_for_systematic[0][iii]
					linear_plot_TTToHadronic.SetName("%s%s"%("TTToHadronic",sys_str))
					linear_plot_TTToHadronic.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "TTToHadronic",region,year, " ".join(use_sys.split("_"))))

					linear_plot_TTToSemiLeptonic = split_up_hists_for_systematic[1][iii]
					linear_plot_TTToSemiLeptonic.SetName("%s%s"%("TTToSemiLeptonic",sys_str))
					linear_plot_TTToSemiLeptonic.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "lTTToSemiLeptonic",region,year, " ".join(use_sys.split("_"))))

					linear_plot_TTToLeptonic = split_up_hists_for_systematic[2][iii]
					linear_plot_TTToLeptonic.SetName("%s%s"%("TTToLeptonic",sys_str))
					linear_plot_TTToLeptonic.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "TTToLeptonic",region,year, " ".join(use_sys.split("_"))))"""


				linear_plot_TTToHadronic.Sumw2()
				linear_plot_TTToSemiLeptonic.Sumw2()
				linear_plot_TTToLeptonic.Sumw2()
				linear_plot.Sumw2(); 

				## scale histograms
				linear_plot_TTToHadronic.Scale( SF_TTToHadronic )
				linear_plot_TTToSemiLeptonic.Scale( SF_TTToSemiLeptonic )
				linear_plot_TTToLeptonic.Scale( SF_TTToLeptonic )				

				### NOW add together with the weight information intact
				linear_plot.Add(linear_plot_TTToHadronic)
				linear_plot.Add(linear_plot_TTToSemiLeptonic)
				linear_plot.Add(linear_plot_TTToLeptonic)				

				all_linear_plots.append(linear_plot)




			elif hist_type == "sig":
				decays = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]
				sig_weights_dict = { decay: self.sig_SF_scale*return_signal_SF.return_signal_SF(self.year,self.mass_point,decay) for decay in decays	}   

				### need to lineraize the histograms separately and THEN add them to linear_plot
				linear_plot_WBWB = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "WBWB",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_HTHT = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "HTHT" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_ZTZT  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "ZTZT" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_WBHT  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s) ; bin; Events / bin"%( "WBHT" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_WBZT = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "WBZT" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_HTZT  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "HTZT" ,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)

				linear_plot_WBWB.Sumw2()
				linear_plot_HTHT.Sumw2()
				linear_plot_ZTZT.Sumw2()
				linear_plot_WBHT.Sumw2()
				linear_plot_WBZT.Sumw2()
				linear_plot_HTZT.Sumw2()
				####### INFO 
				#### split_up_hists_for_systematic[0] is the WBWB histogram
				#### split_up_hists_for_systematic[1] is the HTHT  histogram
				#### split_up_hists_for_systematic[2] is the ZTZT  histogram
				#### split_up_hists_for_systematic[3] is the WBHT  histogram
				#### split_up_hists_for_systematic[4] is the WBZT  histogram
				#### split_up_hists_for_systematic[5] is the HTZT  histogram
				if not self.doHTdist:
					superbin_index = 0
					for superbin_counter,superbin in enumerate(use_indices):
						if superbin_counter in bin_mask: 
							num_masked_bins+=1
							continue
						total_counts_WBWB = 0
						total_counts_HTHT = 0
						total_counts_ZTZT = 0
						total_counts_WBHT  = 0					
						total_counts_WBZT = 0
						total_counts_HTZT  = 0

						for _tuple in superbin:
							total_counts_WBWB+=split_up_hists_for_systematic[0][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_HTHT+=split_up_hists_for_systematic[1][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_ZTZT+=split_up_hists_for_systematic[2][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_WBHT+=split_up_hists_for_systematic[3][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_WBZT+=split_up_hists_for_systematic[4][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
							total_counts_HTZT+=split_up_hists_for_systematic[5][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)

						#print("%s/%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, region, systematic,superbin_index,  total_counts))
						linear_plot_WBWB.SetBinContent(superbin_index+1,total_counts_WBWB)
						linear_plot_HTHT.SetBinContent(superbin_index+1,total_counts_HTHT)
						linear_plot_ZTZT.SetBinContent(superbin_index+1,total_counts_ZTZT)
						linear_plot_WBHT.SetBinContent(superbin_index+1,total_counts_WBHT)					
						linear_plot_WBZT.SetBinContent(superbin_index+1,total_counts_WBZT)
						linear_plot_HTZT.SetBinContent(superbin_index+1,total_counts_HTZT)
					
						linear_plot_WBWB.SetBinError(superbin_index+1,sqrt(total_counts_WBWB))
						linear_plot_HTHT.SetBinError(superbin_index+1,sqrt(total_counts_HTHT))
						linear_plot_ZTZT.SetBinError(superbin_index+1,sqrt(total_counts_ZTZT))
						linear_plot_WBHT.SetBinError(superbin_index+1,sqrt(total_counts_WBHT))					
						linear_plot_WBZT.SetBinError(superbin_index+1,sqrt(total_counts_WBZT))
						linear_plot_HTZT.SetBinError(superbin_index+1,sqrt(total_counts_HTZT))
						superbin_index+=1

				else:
					superbin_index = 0
					for superbin_counter,superbin in enumerate(use_indices):
						if superbin_counter in bin_mask:
							num_masked_bins+=1
							continue
						total_counts_WBWB = 0
						total_counts_HTHT = 0
						total_counts_ZTZT = 0
						total_counts_WBHT  = 0					
						total_counts_WBZT = 0
						total_counts_HTZT  = 0

						for bin_num in superbin:
							total_counts_WBWB+=split_up_hists_for_systematic[0][iii].GetBinContent(bin_num)
							total_counts_HTHT+=split_up_hists_for_systematic[1][iii].GetBinContent(bin_num)
							total_counts_ZTZT+=split_up_hists_for_systematic[2][iii].GetBinContent(bin_num)
							total_counts_WBHT+=split_up_hists_for_systematic[3][iii].GetBinContent(bin_num)
							total_counts_WBZT+=split_up_hists_for_systematic[4][iii].GetBinContent(bin_num)
							total_counts_HTZT+=split_up_hists_for_systematic[5][iii].GetBinContent(bin_num)

						#print("%s/%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, region, systematic,superbin_index,  total_counts))
						linear_plot_WBWB.SetBinContent(superbin_index+1,total_counts_WBWB)
						linear_plot_HTHT.SetBinContent(superbin_index+1,total_counts_HTHT)
						linear_plot_ZTZT.SetBinContent(superbin_index+1,total_counts_ZTZT)
						linear_plot_WBHT.SetBinContent(superbin_index+1,total_counts_WBHT)					
						linear_plot_WBZT.SetBinContent(superbin_index+1,total_counts_WBZT)
						linear_plot_HTZT.SetBinContent(superbin_index+1,total_counts_HTZT)
					
						linear_plot_WBWB.SetBinError(superbin_index+1,sqrt(total_counts_WBWB))
						linear_plot_HTHT.SetBinError(superbin_index+1,sqrt(total_counts_HTHT))
						linear_plot_ZTZT.SetBinError(superbin_index+1,sqrt(total_counts_ZTZT))
						linear_plot_WBHT.SetBinError(superbin_index+1,sqrt(total_counts_WBHT))					
						linear_plot_WBZT.SetBinError(superbin_index+1,sqrt(total_counts_WBZT))
						linear_plot_HTZT.SetBinError(superbin_index+1,sqrt(total_counts_HTZT))
						superbin_index+=1

					"""linear_plot_WBWB = split_up_hists_for_systematic[0][iii]
					linear_plot_WBWB.SetName("%s%s"%("sig_WBWB",sys_str))
					linear_plot_WBWB.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "sig_WBWB",region,year, " ".join(use_sys.split("_"))))

					linear_plot_HTHT = split_up_hists_for_systematic[1][iii]
					linear_plot_HTHT.SetName("%s%s"%("sig_HTHT",sys_str))
					linear_plot_HTHT.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "sig_HTHT",region,year, " ".join(use_sys.split("_"))))

					linear_plot_ZTZT = split_up_hists_for_systematic[2][iii]
					linear_plot_ZTZT.SetName("%s%s"%("sig_ZTZT",sys_str))
					linear_plot_ZTZT.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "sig_ZTZT",region,year, " ".join(use_sys.split("_"))))

					linear_plot_WBHT = split_up_hists_for_systematic[3][iii]
					linear_plot_WBHT.SetName("%s%s"%("sig_WBHT",sys_str))
					linear_plot_WBHT.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "sig_WBHT",region,year, " ".join(use_sys.split("_"))))

					linear_plot_WBZT = split_up_hists_for_systematic[4][iii]
					linear_plot_WBZT.SetName("%s%s"%("sig_WBZT",sys_str))
					linear_plot_WBZT.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "sig_WBZT",region,year, " ".join(use_sys.split("_"))))

					linear_plot_HTZT = split_up_hists_for_systematic[5][iii]
					linear_plot_HTZT.SetName("%s%s"%("sig_HTZT",sys_str))
					linear_plot_HTZT.SetTitle("linearized %s in the %s (%s) (%s); bin; Events / bin"%( "sig_HTZT",region,year, " ".join(use_sys.split("_"))))"""


				linear_plot_WBWB.Sumw2()
				linear_plot_HTHT.Sumw2()
				linear_plot_ZTZT.Sumw2()
				linear_plot_WBHT.Sumw2()
				linear_plot_WBZT.Sumw2()
				linear_plot_HTZT.Sumw2()
				linear_plot.Sumw2(); 

				## scale histograms 
				linear_plot_WBWB.Scale( sig_weights_dict["WBWB"] )
				linear_plot_HTHT.Scale( sig_weights_dict["HTHT"] )
				linear_plot_ZTZT.Scale( sig_weights_dict["ZTZT"] )
				linear_plot_WBHT.Scale( sig_weights_dict["WBHT"] )				
				linear_plot_WBZT.Scale( sig_weights_dict["WBZT"] )
				linear_plot_HTZT.Scale( sig_weights_dict["HTZT"] )

				### NOW add together with the weight information intact
				linear_plot.Add(linear_plot_WBWB)
				linear_plot.Add(linear_plot_HTHT)
				linear_plot.Add(linear_plot_ZTZT)
				linear_plot.Add(linear_plot_WBHT)				
				linear_plot.Add(linear_plot_WBZT)
				linear_plot.Add(linear_plot_HTZT)


				if linear_plot.Integral() < 1e-8:

					## check to see 

					## create artificial signal (integral 1)
					for iii in range(1,linear_plot.GetNbinsX()):
						artificial_sig_injection = self.artificial_signal_injection(iii, linear_plot.GetNbinsX()  )
						#print( "iii/injected value: %s/%s"%(iii, artificial_sig_injection))
						linear_plot.SetBinContent(iii, artificial_sig_injection)
						linear_plot.SetBinError(iii, sqrt(artificial_sig_injection))

					#print("sig had integral 0 for %s%s for year %s and region %s. Injected signal with integral %s."%(BR_type, sys_str, self.year, region, linear_plot.Integral()))
				all_linear_plots.append(linear_plot)



			else:  # return the FULL histogram (no weighting stuff), this is the old way we did this 

				superbin_index = 0
				for superbin_counter,superbin in enumerate(use_indices):
					if superbin_counter in bin_mask:
						num_masked_bins+=1
						continue

					total_counts = 0

					if not all_BR_hists.doHTdist:
						for _tuple in superbin:
							if (_hist[iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0): ### need to verify if these need the +1 ...
								print("ERROR: negative histogram contribution when adding up superbins (bin = %s/%s, counts = %s)"%(_tuple[0]+1, _tuple[1]+1,_hist[iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)))
							total_counts+=_hist[iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
					else:
						for bin_num in superbin:
							if (_hist[iii].GetBinContent(bin_num) < 0): ### need to verify if these need the +1 ...
								print("ERROR: negative histogram contribution when adding up superbins (bin = %s/%s, counts = %s)"%(_tuple[0]+1, _tuple[1]+1,_hist[iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)))
							total_counts+=_hist[iii].GetBinContent(bin_num)
					#print("%s/%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, region, systematic,superbin_index,  total_counts))
					linear_plot.SetBinContent(superbin_index+1,total_counts)
					try:
						linear_plot.SetBinError(superbin_index+1,sqrt(total_counts))
					except:
						print("ERROR: Failed setting bin error (superbin index = %s, counts = %s ) for %s/%s/%s/%s"%(superbin_index+1,total_counts, self.year,BR_type,region,systematic))
					superbin_index+=1

				ROOT.TH1.AddDirectory(False)
				linear_plot.SetDirectory(0)   # histograms lose their references when the file destructor is called
				#if BR_type == "sig"  and "SB" in region:   print(" @@@@@ The POST-linearized %s/%s/%s/%s signal histogram integral is %f"%(self.year,self.mass_point, systematic,region,linear_plot.Integral()))
				#print("superbin indices have size %s, linearized plot has size %s"%( len(self.superbin_indices), linear_plot.GetNbinsX()  )  )
				#print("The last linearized bin of %s/%s/%s/%s has content %s"%(BR_type, region, systematic, self.year,linear_plot.GetBinContent( linear_plot.GetNbinsX()  )))
				all_linear_plots.append(linear_plot)
			#if region == "AT1b": print("For year %s, sample type %s, region %s, and sytematic %s, a total of %s bins were masked out of %s in the mask file. "%(self.year, BR_type, region, sys_str, num_masked_bins, mask_size))
		"""
		for hist_list in split_up_hists_for_systematic: ## no longer need this 'split up' histograms	
			for hist in hist_list:
				del hist"""
		return all_linear_plots

	def write_histograms(self,forStats=False):

		if forStats:
			combine_file_name = self.output_file_home + "/combine_stats_%s%s_%s.root"%(self.technique_str, year,mass_point)   
		elif self.doHTdist:
			combine_file_name = self.output_file_home + self.HT_distr_home + "/combine_%s%s_%s.root"%(self.technique_str,year,mass_point)   
		else:
			combine_file_name = self.output_file_home + "/combine_%s%s_%s.root"%(self.technique_str,year,mass_point)   
		combine_file = ROOT.TFile.Open(combine_file_name,"RECREATE")
		combine_file.cd()

		regions = ["AT1b","AT0b"]
		if self.doATxtb:
			regions.append["AT1tb"]
			regions.append["AT0tb"]
		if self.doSideband:
			regions.append("SB1b")
			regions.append("SB0b")

		QCD_hists	 = [ self.QCD_linear_AT1b, self.QCD_linear_AT0b  ]
		TTbar_hists  = [ self.TTbar_linear_AT1b, self.TTbar_linear_AT0b]

		if self.includeWJets: WJets_hists	 = [self.WJets_linear_AT1b, self.WJets_linear_AT0b  ]
		if self.includeTTTo:  TTTo_hists	 = [self.TTTo_linear_AT1b, self.TTTo_linear_AT0b  ]
		ST_hists	 = [self.ST_linear_AT1b, self.ST_linear_AT0b]
		signal_hists = [self.signal_linear_AT1b, self.signal_linear_AT0b]
		data_hists   = [self.data_linear_AT1b, self.data_linear_AT0b]

		combined_hists 	   = [self.combined_linear_AT1b, self.combined_linear_AT0b ]  ### these are for writing unscaled histograms
		combined_hists_all = [self.all_combined_linear_AT1b, self.all_combined_linear_AT0b]  ### these are for writing fully scaled, combined BR histograms

		if forStats:
			systematics_ = ["nom"]

		if self.createDummyChannel:
			dummyHists = [self.dummy_channel_AT1b, self.dummy_channel_AT0b] 


		max_index = 2

		for kkk, region in enumerate(regions):

			if kkk > max_index: continue
			### create folder for region
			combine_file.cd()
			ROOT.gDirectory.mkdir(region)
			combine_file.cd(region)

			systematics_ = self.systematic_names[:]

			for iii,systematic in enumerate(systematics_):

				if forStats and kkk < 4:
					combined_hists[kkk][iii].Write()
				sys_suffix = [""]
				if systematic == "nom":
					sys_updown = ["nom"]
				elif "topPt" in systematic:
					sys_updown = ["%s_up"%systematic,"%s_down"%systematic]
				else:
					sys_updown = ["%s_up"%systematic,"%s_down"%systematic]

				for jjj,sys_str in enumerate(sys_updown):
					if "topPt" not in systematic: 
						QCD_hists[kkk][iii][jjj].Write()

						signal_hists[kkk][iii][jjj].Write()

						if "fact" not in systematic and "renorm" not in systematic and "CMS_scale" not in systematic:  
							ST_hists[kkk][iii][jjj].Write()
						if self.includeWJets: 
							WJets_hists[kkk][iii][jjj].Write()

					TTbar_hists[kkk][iii][jjj].Write()

					if self.includeTTTo: 
						TTTo_hists[kkk][iii][jjj].Write()
					if not forStats:
						combined_hists_all[kkk][iii][jjj].Write()

		combine_file.Close()
		return 
	def print_histograms(self):   #TODO: add signal and data olots here 


		CMS_label_pos = 0.152
		SIM_label_pos = 0.295

				# SR
		### create nom plots for each year, 
		self.QCD_linear_SR[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/QCD_linear_%s%s_%s_SR.png"%(self.technique_str,self.year,"nom"))

		self.TTbar_linear_SR[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/TTbar_linear_%s%s_%s_SR.png"%(self.technique_str,self.year,"nom"))
		
		self.ST_linear_SR[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/ST_linear_%s%s_%s_SR.png"%(self.technique_str,self.year,"nom"))

		self.signal_linear_SR[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/%s_linear_%s%s_%s_SR.png"%(self.mass_point, self.technique_str,self.year,"nom"))


		# CR
		self.QCD_linear_CR[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/QCD_linear_%s%s_%s_CR.png"%(self.technique_str,self.year,"nom"))

		self.TTbar_linear_CR[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/TTbar_linear_%s%s_%s_CR.png"%(self.technique_str,self.year,"nom"))

		self.ST_linear_CR[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/ST_linear_%s%s_%s_CR.png"%(self.technique_str,self.year,"nom"))

		self.signal_linear_CR[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/%s_linear_%s%s_%s_CR.png"%(self.mass_point, self.technique_str,self.year,"nom"))


		# 0b anti-tagged region
		self.QCD_linear_AT0b[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/QCD_linear_%s%s_%s_AT0b.png"%(self.technique_str,self.year,"nom"))

		self.TTbar_linear_AT0b[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/TTbar_linear_%s%s_%s_AT0b.png"%(self.technique_str,self.year,"nom"))

		self.ST_linear_AT0b[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/ST_linear_%s%s_%s_AT0b.png"%(self.technique_str,self.year,"nom"))

		self.signal_linear_AT0b[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/%s_linear_%s%s_%s_AT0b.png"%(self.mass_point, self.technique_str,self.year,"nom"))


		# 1b anti-tagged region
		self.QCD_linear_AT1b[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/QCD_linear_%s%s_%s_AT1b.png"%(self.technique_str,self.year,"nom"))

		self.TTbar_linear_AT1b[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/TTbar_linear_%s%s_%s_AT1b.png"%(self.technique_str,self.year,"nom"))

		self.ST_linear_AT1b[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/ST_linear_%s%s_%s_AT1b.png"%(self.technique_str,self.year,"nom"))

		self.signal_linear_AT1b[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/%s_linear_%s%s_%s_AT1b.png"%(self.mass_point, self.technique_str,self.year,"nom"))
	

		####################################
		############ side-band #############
		####################################
		if self.doSideband:
			# 1b side-band region
			self.QCD_linear_SB1b[0][0].Draw()
			write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
			c.SaveAs(self.final_plot_home+"/QCD_linear_%s%s_%s_SB1b.png"%(self.technique_str,self.year,"nom"))

			self.TTbar_linear_SB1b[0][0].Draw()
			write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
			c.SaveAs(self.final_plot_home+"/TTbar_linear_%s%s_%s_SB1b.png"%(self.technique_str,self.year,"nom"))

			self.ST_linear_SB1b[0][0].Draw()
			write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
			c.SaveAs(self.final_plot_home+"/ST_linear_%s%s_%s_SB1b.png"%(self.technique_str,self.year,"nom"))

			self.signal_linear_SB1b[0][0].Draw()
			write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
			c.SaveAs(self.final_plot_home+"/%s_linear_%s%s_%s_SB1b.png"%(self.mass_point, self.technique_str,self.year,"nom"))
		
			# 0b side-band region
			self.QCD_linear_SB0b[0][0].Draw()
			write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
			c.SaveAs(self.final_plot_home+"/QCD_linear_%s%s_%s_SB0b.png"%(self.technique_str,self.year,"nom"))

			self.TTbar_linear_SB0b[0][0].Draw()
			write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
			c.SaveAs(self.final_plot_home+"/TTbar_linear_%s%s_%s_SB0b.png"%(self.technique_str,self.year,"nom"))

			self.ST_linear_SB0b[0][0].Draw()
			write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
			c.SaveAs(self.final_plot_home+"/ST_linear_%s%s_%s_SB0b.png"%(self.technique_str,self.year,"nom"))

			self.signal_linear_SB0b[0][0].Draw()
			write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
			c.SaveAs(self.final_plot_home+"/%s_linear_%s%s_%s_SB0b.png"%(self.mass_point, self.technique_str,self.year,"nom"))
		
		return

	def load_superbin_indices(self,region="AT1b"):	# load in the superbin indices (located in a text file )
		_superbin_indices = []
		open_file = open(self.index_file_home+"/superbin_indices%s_%s.txt"%(self.technique_str,self.year),"r")
		for line in open_file:
			columns = line.split('/')
			if columns[0] == self.year and columns[1] == region:
				_superbin_indices = columns[3]
		open_file.close()
		return ast.literal_eval(_superbin_indices)


	def load_bin_masks(self,region):	# load in the superbin indices (located in a text file )
		_superbin_indices = []
		bin_map_path         = "region_masks/"
		open_file = open(bin_map_path+"/bin_masks_%s.txt"%(year),"r")
		#print("Got superbin index file %s."%( bin_map_path+"/superbin_indices%s_%s.txt"%(technique_str,year)  ))
		for line in open_file:
			columns = line.split('/')
			if columns[0] == self.year and columns[1] == region and columns[2] == self.technique_str:
				_superbin_indices = columns[3]
		open_file.close()
		return ast.literal_eval(_superbin_indices)


	## return string form of scaled signal contribution in SR
	def get_signal_counts_SR(self):



		decays = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]
		sig_weights_dict = { decay: self.sig_SF_scale*return_signal_SF.return_signal_SF(self.year,self.mass_point,decay) for decay in decays	}   





		signal_counts_SR = sum( [
			self.signal_WBWB_hist_AT1b[0][0].Integral()*sig_weights_dict["WBWB"], 
			self.signal_HTHT_hist_AT1b[0][0].Integral()*sig_weights_dict["HTHT"], 
			self.signal_ZTZT_hist_AT1b[0][0].Integral()*sig_weights_dict["ZTZT"], 
			self.signal_WBHT_hist_AT1b[0][0].Integral()*sig_weights_dict["WBHT"], 
			self.signal_WBZT_hist_AT1b[0][0].Integral()*sig_weights_dict["WBZT"], 
			self.signal_HTZT_hist_AT1b[0][0].Integral()*sig_weights_dict["HTZT"] ])
		return signal_counts_SR



	def kill_histograms(self):   ## kill the linearized and individual signal histograms

 		linear_hists = [ self.all_combined_hists_SR,self.all_combined_hists_CR,self.all_combined_hists_AT1b,self.all_combined_hists_AT0b,
		self.combined_linear_SR	,self.combined_linear_CR , self.combined_linear_AT1b  ,self.combined_linear_AT0b,
		self.QCD_linear_SR, self.TTbar_linear_SR ,self.ST_linear_SR, self.data_linear_SR  , 
		self.QCD_linear_CR 	 ,self.TTbar_linear_CR ,self.ST_linear_CR,self.data_linear_CR  ,
		self.QCD_linear_AT0b , self.TTbar_linear_AT0b  ,self.ST_linear_AT0b	 ,self.data_linear_AT0b, 
		self.QCD_linear_AT1b ,self.TTbar_linear_AT1b ,self.ST_linear_AT1b ,self.data_linear_AT1b , 
		self.all_combined_linear_SR  ,self.all_combined_linear_CR  ,self.all_combined_linear_AT1b,self.all_combined_linear_AT0b, self.signal_linear_SR,self.signal_linear_CR,self.signal_linear_AT0b ,self.signal_linear_AT1b]
		if self.includeWJets:  			  linear_hists.extend( [self.WJets_linear_SR, self.WJets_linear_CR, self.WJets_linear_AT1b, self.WJets_linear_AT0b ] ) 
		if self.includeTTTo:			  linear_hists.extend( [ self.TTTo_linear_SR, self.TTTo_linear_SR, self.TTTo_linear_AT1b, self.TTTo_linear_AT0b] )
		if self.doSideband: 
			linear_hists.extend( [ self.QCD_linear_SB1b, self.TTbar_linear_SB1b, self.ST_linear_SB1b, self.data_linear_SB1b, self.signal_linear_SB1b, self.QCD_linear_SB0b, self.TTbar_linear_SB0b, self.ST_linear_SB0b, self.data_linear_SB0b, self.signal_linear_SB0b   ]   )
			if self.includeWJets:  			  linear_hists.extend( [self.WJets_linear_SB1b, self.WJets_linear_SB0b] ) 
			if self.includeTTTo:			  linear_hists.extend( [ self.TTTo_linear_SB1b, self.TTTo_linear_SB0b] )
		if self.doATxtb:
			linear_hists.extend( [ self.QCD_linear_AT1tb, self.TTbar_linear_AT1tb, self.ST_linear_AT1tb, self.data_linear_AT1tb, self.signal_linear_AT1tb, self.QCD_linear_AT0tb, self.TTbar_linear_AT0tb, self.ST_linear_AT0tb, self.data_linear_AT0tb, self.signal_linear_AT0tb   ]   )
			if self.includeWJets:			 linear_hists.extend( [self.WJets_linear_AT1tb, self.WJets_linear_AT0tb] )
			if self.includeTTTo:			 linear_hists.extend( [self.TTTo_linear_AT1tb, self.TTTo_linear_AT0tb ] )

		for hist_list in linear_hists:
			for hist in hist_list:
				del hist

		signal_hists =  [self.signal_WBWB_hist_AT0b,self.signal_HTHT_hist_AT0b,self.signal_ZTZT_hist_AT0b,self.signal_WBHT_hist_AT0b,self.signal_WBZT_hist_AT0b,self.signal_HTZT_hist_AT0b, self.signal_WBWB_hist_AT1b,self.signal_HTHT_hist_AT1b,self.signal_ZTZT_hist_AT1b,
		self.signal_WBHT_hist_AT1b,self.signal_WBZT_hist_AT1b,self.signal_HTZT_hist_AT1b] 
		for hist_list in signal_hists:
			for hist in hist_list:
				del hist

		return


if __name__=="__main__":
	start_time = time.time()

	debug = False

	doHTdist   = False
	doSideband = False
	doATxtb	   = False
	run_from_eos 	   = False
	createDummyChannel = False

	# get input year
	parser = argparse.ArgumentParser(description="Linearize 2D histograms in order to reach a minimum stat uncertainty and scaled/unscaled bin yield. ")
	parser.add_argument("-y", "--year", type=str, required=True, help="Input year on which to run.")
	parser.add_argument( "--doHTdist",   default=False, action='store_true', required=False, help="Option to run on HT distributions instead of 2D plots.")
	parser.add_argument( "--doSideband",  default=False, action='store_true',  required=False, help="Option to run the sideband region (in addition to normal regions).")
	parser.add_argument( "--doATxtb",   default=False, action='store_true', required=False, help="Option to run over the AT1tb and AT0tb regions (in addition to normal regions).")

	args = parser.parse_args()
	year = args.year
	print("Running for year %s."%year)

	mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1","Suu5_chi1p5","Suu5_chi2","Suu6_chi1","Suu6_chi1p5","Suu6_chi2","Suu6_chi2p5","Suu7_chi1",
   "Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3","Suu8_chi1","Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"]

	print("doHTdist is %s."%doHTdist)

	if debug:
		mass_points = ["Suu4_chi1"]

	technique_strs = ["NN_"] 
	technique_descr = ["NN-based"]

	includeTTJets800to1200 = True
	includeTTTo            = True
	includeWJets           = True

	createMaskedFiles      = False ## don't need these now

	WPs = [0.05,0.10,0.125,0.15,0.175,0.20,0.25]

	output_event_summary = open("txt_files/AT_WP_study_yields/SR_event_summary_%s.txt"%(year),"w") ## file where once will write the number of BR/sig events per WP
	output_event_summary.write("#WP	N_BR_SR	N_Suu4_chi1_SR	N_Suu4_chi1p5_SR	N_Suu5_chi1_SR	N_Suu5_chi1p5_SR	N_Suu5_chi2_SR	N_Suu6_chi1_SR	N_Suu6_chi1p5_SR	N_Suu6_chi2_SR	N_Suu6_chi2p5_SR	N_Suu7_chi1_SR	N_Suu7_chi1p5_SR	N_Suu7_chi2_SR	N_Suu7_chi2p5_SR	N_Suu7_chi3_SR	N_Suu8_chi1_SR	N_Suu8_chi1p5_SR	N_Suu8_chi2_SR	N_Suu8_chi2p5_SR	N_Suu8_chi3_SR\n")


	for WP in WPs:

		WP_str = "ATWP" + "{:.2f}".format(WP).replace('.', 'p')
		for iii,technique_str in enumerate(technique_strs):

			if doHTdist and "NN" in technique_str: continue 


			# create instance of hist_loader (containing all BR histograms) for the year + technique str combination
			all_BR_hists  = hist_loader(year, technique_str, doHTdist, doSideband, doATxtb, includeTTJets800to1200, includeTTTo, includeWJets, run_from_eos, WP_str)


			summary_line = "%s %s "%(WP, all_BR_hists.return_formatted_summary_str() )

			for mass_point in mass_points:
				#try:
				print("Running for %s/%s/%s/%s"%(year,mass_point,technique_descr[iii],WP_str))
				if createMaskedFiles: final_plot = linearized_plot(year, mass_point, technique_str, all_BR_hists, True, createDummyChannel,run_from_eos, debug, WP_str)   ### run with masked bins
				else: final_plot = linearized_plot(year, mass_point, technique_str, all_BR_hists, False, createDummyChannel,run_from_eos,debug, WP_str)	### run without masked bins

				summary_line += " %s"%final_plot.get_signal_counts_SR()


				del final_plot
			all_BR_hists.kill_histograms()
			del all_BR_hists  # free up a lot of memory 

			summary_line+= "\n"
			output_event_summary.write(summary_line)

	output_event_summary.close()
	print("Script took %ss to run."%(	np.round(time.time() - start_time,4 )) )




#### THE SIGNAL IS NOT CORRECT IN THE FLATTENED 
#### check to see if these are fine in the processed
#### then check to see if the bin map is okay
