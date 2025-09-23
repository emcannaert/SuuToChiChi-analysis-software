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

	def __init__(self, year, mass_point, technique_str, all_BR_hists,output_map_file,  use_QCD_Pt=False, useMask=False, use_1b_bin_maps = False, createDummyChannel=False, run_from_eos = False, runCorrected = False, debug=False):

		self.c = ROOT.TCanvas("","",1200,1000)
		self.BR_SF_scale = 1.0
		self.sig_SF_scale = 1.0
		self.technique_str = technique_str
		self.year   = year
		self.createDummyChannel = createDummyChannel
		self.run_from_eos = run_from_eos
		self.debug = debug
		self.use_1b_bin_maps = use_1b_bin_maps
		self.use_QCD_Pt = use_QCD_Pt

		self.runCorrected = runCorrected
		

		self.MC_root_file_home	  = 	os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFiles/"
		self.data_root_file_home	=   os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFiles/"
		if self.runCorrected:
			self.MC_root_file_home	  = 	os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFilesCorrected/"
			self.data_root_file_home	=   os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFilesCorrected/"


		self.use_QCD_Pt_str = "QCDHT"
		if self.use_QCD_Pt: self.use_QCD_Pt_str = "QCDPT"


		self.output_map_file = output_map_file

		self.eos_path = "root://cmseos.fnal.gov/"
		self.HT_distr_home = "/HT_distributions" # extra folder where output files are saved for HT distribution plots

		if self.run_from_eos:		## grab files from eos if they are not stored locally

			print("Using files stored on EOS.")
			self.MC_root_file_home	    =  self.eos_path + "/store/user/ecannaer/processedFiles/"
			self.data_root_file_home	=  self.eos_path + "/store/user/ecannaer/processedFiles/"
			if self.runCorrected:
				self.MC_root_file_home	    =  self.eos_path + "/store/user/ecannaer/processedFilesCorrected/"
				self.data_root_file_home	=  self.eos_path + "/store/user/ecannaer/processedFilesCorrected/"

		## region options
		self.doSideband = all_BR_hists.doSideband
		self.doATxtb = 	  all_BR_hists.doATxtb
		self.doHTdist =   all_BR_hists.doHTdist
		self.useMask = useMask
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

		self.index_file_home	 = os.getenv('CMSSW_BASE') + "/src/postprocess/binMaps/"
		self.output_file_home	= os.getenv('CMSSW_BASE') + "/src/postprocess/finalCombineFilesNewStats/%s/"%self.use_QCD_Pt_str
		self.final_plot_home	 = os.getenv('CMSSW_BASE') + "/src/postprocess/plots/finalCombinePlots/%s/"%(self.use_QCD_Pt_str)

		if self.useMask: 
			if self.use_QCD_Pt: 
				self.output_file_home	 = os.getenv('CMSSW_BASE') + "/src/postprocess/finalCombineFilesNewStats/%s/maskedFinalCombineFiles/"%(self.use_QCD_Pt_str)
				self.final_plot_home	 = os.getenv('CMSSW_BASE') + "/src/postprocess/plots/finalCombinePlots/%s/maskedFinalCombineFiles/"%(self.use_QCD_Pt_str)

		if self.useMask and self.doHTdist: return

		self.create_directories()  ## make sure all above directories exist


		if self.use_1b_bin_maps:  
			_1b_map = { "SR":"SR", "CR":"SR", "AT1b":"AT1b", "AT0b":"AT1b"   }  
			self.superbin_indices_dict			  	  =  {  region: self.load_superbin_indices(_1b_map[region], region) for region in ["SR","CR","AT1b","AT0b"]}  ## order: SR, CR, AT1b, AT0b
		else: 
			self.superbin_indices_dict			  	  =  {  region: self.load_superbin_indices(region,region) for region in ["SR","CR","AT1b","AT0b"]}  ## order: SR, CR, AT1b, AT0b
		


		#self.superbin_indices_AT			  = self.load_superbin_indices(self.region)   ## change this to reflect which bin indices should be followed (AT1tb if you are using the tight WP in the SR)
		#if  self.doSideband: 
		#	self.superbin_indices_SB1b = self.load_superbin_indices(region="SB1b")
		#	self.superbin_indices_SB0b = self.load_superbin_indices(region="SB1b")

 
		print("DEBUG: SR is sorted into %s superbins."%(len(self.superbin_indices_dict["SR"])))
		print("DEBUG: CR is sorted into %s superbins."%(len(self.superbin_indices_dict["CR"])))
		print("DEBUG: AT1b is sorted into %s superbins."%(len(self.superbin_indices_dict["AT1b"])))
		print("DEBUG: AT0b is sorted into %s superbins."%(len(self.superbin_indices_dict["AT0b"])))


		if self.debug:
			self.output_file_home	= os.getenv('CMSSW_BASE') + "/src/postprocess/finalCombineFilesNewStats/test/"



		self.mass_point = mass_point   # label for the signal mass point

		self.data_systematics 	   = ["nom"]
		self.data_systematic_names = ["nom"]

		## this was replaced by the below
		#self.systematics 	  = ["nom",   "bTagSF_med",   "bTagSF_tight",	  "JER",	 "JEC",  "bTag_eventWeight_bc_T", "bTag_eventWeight_light_T", "bTag_eventWeight_bc_M", "bTag_eventWeight_light_M", "bTag_eventWeight_bc_T_year", "bTag_eventWeight_light_T_year", "bTag_eventWeight_bc_M_year", "bTag_eventWeight_light_M_year",	   "JER_eta193",	 "JER_193eta25",	  "JEC_FlavorQCD",	"JEC_RelativeBal",	   "Absolute",	 "JEC_BBEC1_year",		"JEC_Absolute_year",	  "JEC_RelativeSample_year",	"PUSF",	"topPt",	 "L1Prefiring",	       "pdf",	 "renorm",	 "fact",	  "AbsoluteCal",		    "AbsoluteTheory",	     "AbsolutePU"     ]   ## systematic namings as used in analyzer   removed:  "bTagSF",			  "JEC_HF",	 "JEC_BBEC1",	 "JEC_EC2",	 "JEC_EC2_year",		 "JEC_HF_year",	
		#self.systematic_names = ["nom",  "CMS_bTagSF_M" , "CMS_bTagSF_T",	"CMS_jer", "CMS_jec",   "CMS_bTagSF_bc_T",	   "CMS_bTagSF_light_T",	   "CMS_bTagSF_bc_M",	   "CMS_bTagSF_light_M",	  "CMS_bTagSF_bc_T_year",		"CMS_bTagSF_light_T_year",	  "CMS_bTagSF_bc_M_year",	   "CMS_bTagSF_light_M_year",		"CMS_jer_eta193",  "CMS_jer_193eta25",  "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal", "CMS_jec_Absolute", "CMS_jec_BBEC1_year", "CMS_jec_Absolute_year", "CMS_jec_RelativeSample_year", "CMS_pu", "CMS_topPt", "CMS_L1Prefiring", "CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory", "CMS_jec_AbsolutePU"]  ## systematic namings for cards   "CMS_btagSF",  "CMS_jer",	 "CMS_jec_HF", "CMS_jec_BBEC1", "CMS_jec_EC2",   "CMS_jec_EC2_year",   "CMS_jec_HF_year",   
		
		self.systematics 	  = ["nom",      "JER",	    "JEC",    "bTag_eventWeight_bc_M_corr", "bTag_eventWeight_light_M_corr",  "bTag_eventWeight_bc_M_year", "bTag_eventWeight_light_M_year",		"JER_eta193",	 "JER_193eta25",	  "JEC_FlavorQCD",	"JEC_RelativeBal",		    "JEC_Absolute",	   "JEC_BBEC1_year",	   "JEC_Absolute_year",	     "JEC_RelativeSample_year",	   "PUSF",		 "L1Prefiring",	        "pdf",	   "renorm",	 "fact",	  "JEC_AbsoluteCal",    "JEC_AbsoluteTheory",       "JEC_AbsolutePU",	    "JEC_AbsoluteScale",		  "JEC_Fragmentation",	    "JEC_AbsoluteMPFBias",	   "JEC_RelativeFSR",     "scale"   ]   ## systematic namings as used in analyzer	 "bTagSF",   
		self.systematic_names = ["nom",    "CMS_jer", "CMS_jec",    "CMS_bTagSF_bc_M_corr",	        "CMS_bTagSF_light_M_corr",	  	 "CMS_bTagSF_bc_M_year",	   "CMS_bTagSF_light_M_year",		 "CMS_jer_eta193", "CMS_jer_193eta25",  "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal",   "CMS_jec_Absolute", "CMS_jec_BBEC1_year",	 "CMS_jec_Absolute_year",  "CMS_jec_RelativeSample_year", "CMS_pu",    "CMS_L1Prefiring",   "CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory",    "CMS_jec_AbsolutePU",   "CMS_jec_AbsoluteScale" ,   "CMS_jec_Fragmentation" , "CMS_jec_AbsoluteMPFBias",  "CMS_jec_RelativeFSR",  "CMS_scale"]  ## systematic namings for cards   "CMS_btagSF", 

		if not self.runCorrected:
			self.systematics.extend([ "bTagSF_med",    "bTagSF_med_corr",   "topPt"])
			self.systematic_names.extend(["CMS_bTagSF_M" ,  "CMS_bTagSF_M_corr" , "CMS_topPt"])
			


		self.uncorrelated_systematics = [ "CMS_jec", "CMS_jer","CMS_jer_eta193", "CMS_jer_193eta25", "CMS_L1Prefiring","CMS_bTagSF_M", "CMS_bTagSF_T", "CMS_bTagSF_bc_T_year", "CMS_bTagSF_light_T_year", "CMS_bTagSF_bc_M_year","CMS_bTagSF_light_M_year", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year", "CMS_jec_RelativeSample_year"] ## systematics that are correlated (will not have year appended to names)	 "CMS_btagSF",
			## removed from uncorrelated uncertainties :  "CMS_pu"

		### HT bin stuff
		if self.doHTdist: self.HT_dist_superbins =  all_BR_hists.HT_dist_superbins

		### individual bins for SR

		if self.use_QCD_Pt:
			self.QCDMC_Pt_170to300_hist_SR 		= all_BR_hists.QCDMC_Pt_170to300_hist_SR
			self.QCDMC_Pt_300to470_hist_SR 		= all_BR_hists.QCDMC_Pt_300to470_hist_SR
			self.QCDMC_Pt_470to600_hist_SR 		= all_BR_hists.QCDMC_Pt_470to600_hist_SR
			self.QCDMC_Pt_600to800_hist_SR 		= all_BR_hists.QCDMC_Pt_600to800_hist_SR
			self.QCDMC_Pt_800to1000_hist_SR 	= all_BR_hists.QCDMC_Pt_800to1000_hist_SR
			self.QCDMC_Pt_1000to1400_hist_SR 	= all_BR_hists.QCDMC_Pt_1000to1400_hist_SR
			self.QCDMC_Pt_1400to1800_hist_SR 	= all_BR_hists.QCDMC_Pt_1400to1800_hist_SR
			self.QCDMC_Pt_1800to2400_hist_SR 	= all_BR_hists.QCDMC_Pt_1800to2400_hist_SR
			self.QCDMC_Pt_2400to3200_hist_SR 	= all_BR_hists.QCDMC_Pt_2400to3200_hist_SR
			self.QCDMC_Pt_3200toInf_hist_SR 	= all_BR_hists.QCDMC_Pt_3200toInf_hist_SR

		else:
			self.QCD1000to1500_hist_SR 	= all_BR_hists.QCD1000to1500_hist_SR
			self.QCD1500to2000_hist_SR 	= all_BR_hists.QCD1500to2000_hist_SR
			self.QCD2000toInf_hist_SR 	= all_BR_hists.QCD2000toInf_hist_SR


		self.TTJets1200to2500_hist_SR 	= all_BR_hists.TTJets1200to2500_hist_SR
		self.TTJets2500toInf_hist_SR 	= all_BR_hists.TTJets2500toInf_hist_SR

		self.ST_t_channel_top_hist_SR 		= all_BR_hists.ST_t_channel_top_hist_SR
		self.ST_t_channel_antitop_hist_SR 	= all_BR_hists.ST_t_channel_antitop_hist_SR
		self.ST_s_channel_hadrons_hist_SR 	= all_BR_hists.ST_s_channel_hadrons_hist_SR
		self.ST_s_channel_leptons_hist_SR 	= all_BR_hists.ST_s_channel_leptons_hist_SR
		self.ST_tW_antitop_hist_SR 			= all_BR_hists.ST_tW_antitop_hist_SR
		self.ST_tW_top_hist_SR 				= all_BR_hists.ST_tW_top_hist_SR

		if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_SR  = all_BR_hists.TTJetsMCHT800to1200_SR
		if self.includeTTTo:
			self.TTToHadronicMC_SR 				= all_BR_hists.TTToHadronicMC_SR
			self.TTToSemiLeptonicMC_SR 			= all_BR_hists.TTToSemiLeptonicMC_SR
			self.TTToLeptonicMC_SR 				= all_BR_hists.TTToLeptonicMC_SR

		if self.includeWJets:
			self.WJetsMC_LNu_HT800to1200_SR 	= all_BR_hists.WJetsMC_LNu_HT800to1200_SR
			self.WJetsMC_LNu_HT1200to2500_SR 	= all_BR_hists.WJetsMC_LNu_HT1200to2500_SR
			self.WJetsMC_LNu_HT2500toInf_SR 	= all_BR_hists.WJetsMC_LNu_HT2500toInf_SR
			self.WJetsMC_QQ_HT800toInf_SR 		= all_BR_hists.WJetsMC_QQ_HT800toInf_SR

		self.signal_WBWB_hist_SR = []
		self.signal_HTHT_hist_SR = []
		self.signal_ZTZT_hist_SR = []
		self.signal_WBHT_hist_SR = []
		self.signal_WBZT_hist_SR = []
		self.signal_HTZT_hist_SR = []


		### individual bins for CR

		if self.use_QCD_Pt:
			self.QCDMC_Pt_170to300_hist_CR 		= all_BR_hists.QCDMC_Pt_170to300_hist_CR
			self.QCDMC_Pt_300to470_hist_CR 		= all_BR_hists.QCDMC_Pt_300to470_hist_CR
			self.QCDMC_Pt_470to600_hist_CR 		= all_BR_hists.QCDMC_Pt_470to600_hist_CR
			self.QCDMC_Pt_600to800_hist_CR 		= all_BR_hists.QCDMC_Pt_600to800_hist_CR
			self.QCDMC_Pt_800to1000_hist_CR 	= all_BR_hists.QCDMC_Pt_800to1000_hist_CR
			self.QCDMC_Pt_1000to1400_hist_CR 	= all_BR_hists.QCDMC_Pt_1000to1400_hist_CR
			self.QCDMC_Pt_1400to1800_hist_CR 	= all_BR_hists.QCDMC_Pt_1400to1800_hist_CR
			self.QCDMC_Pt_1800to2400_hist_CR 	= all_BR_hists.QCDMC_Pt_1800to2400_hist_CR
			self.QCDMC_Pt_2400to3200_hist_CR 	= all_BR_hists.QCDMC_Pt_2400to3200_hist_CR
			self.QCDMC_Pt_3200toInf_hist_CR 	= all_BR_hists.QCDMC_Pt_3200toInf_hist_CR

		else:
			self.QCD1000to1500_hist_CR 	= all_BR_hists.QCD1000to1500_hist_CR
			self.QCD1500to2000_hist_CR 	= all_BR_hists.QCD1500to2000_hist_CR
			self.QCD2000toInf_hist_CR 	= all_BR_hists.QCD2000toInf_hist_CR

		self.TTJets1200to2500_hist_CR 	= all_BR_hists.TTJets1200to2500_hist_CR
		self.TTJets2500toInf_hist_CR 	= all_BR_hists.TTJets2500toInf_hist_CR

		self.ST_t_channel_top_hist_CR 		= all_BR_hists.ST_t_channel_top_hist_CR
		self.ST_t_channel_antitop_hist_CR 	= all_BR_hists.ST_t_channel_antitop_hist_CR
		self.ST_s_channel_hadrons_hist_CR 	= all_BR_hists.ST_s_channel_hadrons_hist_CR
		self.ST_s_channel_leptons_hist_CR 	= all_BR_hists.ST_s_channel_leptons_hist_CR
		self.ST_tW_antitop_hist_CR 			= all_BR_hists.ST_tW_antitop_hist_CR
		self.ST_tW_top_hist_CR 				= all_BR_hists.ST_tW_top_hist_CR

		if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_CR = all_BR_hists.TTJetsMCHT800to1200_CR
		if self.includeTTTo:
			self.TTToHadronicMC_CR 				= all_BR_hists.TTToHadronicMC_CR
			self.TTToSemiLeptonicMC_CR 			= all_BR_hists.TTToSemiLeptonicMC_CR
			self.TTToLeptonicMC_CR 				= all_BR_hists.TTToLeptonicMC_CR

		if self.includeWJets:
			self.WJetsMC_LNu_HT800to1200_CR 	= all_BR_hists.WJetsMC_LNu_HT800to1200_CR
			self.WJetsMC_LNu_HT1200to2500_CR 	= all_BR_hists.WJetsMC_LNu_HT1200to2500_CR
			self.WJetsMC_LNu_HT2500toInf_CR 	= all_BR_hists.WJetsMC_LNu_HT2500toInf_CR
			self.WJetsMC_QQ_HT800toInf_CR 		= all_BR_hists.WJetsMC_QQ_HT800toInf_CR

		self.signal_WBWB_hist_CR = []
		self.signal_HTHT_hist_CR = []
		self.signal_ZTZT_hist_CR = []
		self.signal_WBHT_hist_CR = []
		self.signal_WBZT_hist_CR = []
		self.signal_HTZT_hist_CR = []


		### individual bins for AT1b

		if self.use_QCD_Pt:
			self.QCDMC_Pt_170to300_hist_AT1b 		= all_BR_hists.QCDMC_Pt_170to300_hist_AT1b
			self.QCDMC_Pt_300to470_hist_AT1b 		= all_BR_hists.QCDMC_Pt_300to470_hist_AT1b
			self.QCDMC_Pt_470to600_hist_AT1b 		= all_BR_hists.QCDMC_Pt_470to600_hist_AT1b
			self.QCDMC_Pt_600to800_hist_AT1b 		= all_BR_hists.QCDMC_Pt_600to800_hist_AT1b
			self.QCDMC_Pt_800to1000_hist_AT1b 	= all_BR_hists.QCDMC_Pt_800to1000_hist_AT1b
			self.QCDMC_Pt_1000to1400_hist_AT1b 	= all_BR_hists.QCDMC_Pt_1000to1400_hist_AT1b
			self.QCDMC_Pt_1400to1800_hist_AT1b 	= all_BR_hists.QCDMC_Pt_1400to1800_hist_AT1b
			self.QCDMC_Pt_1800to2400_hist_AT1b 	= all_BR_hists.QCDMC_Pt_1800to2400_hist_AT1b
			self.QCDMC_Pt_2400to3200_hist_AT1b 	= all_BR_hists.QCDMC_Pt_2400to3200_hist_AT1b
			self.QCDMC_Pt_3200toInf_hist_AT1b 	= all_BR_hists.QCDMC_Pt_3200toInf_hist_AT1b

		else:
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

		if self.use_QCD_Pt:
			self.QCDMC_Pt_170to300_hist_AT0b 		= all_BR_hists.QCDMC_Pt_170to300_hist_AT0b
			self.QCDMC_Pt_300to470_hist_AT0b 		= all_BR_hists.QCDMC_Pt_300to470_hist_AT0b
			self.QCDMC_Pt_470to600_hist_AT0b 		= all_BR_hists.QCDMC_Pt_470to600_hist_AT0b
			self.QCDMC_Pt_600to800_hist_AT0b 		= all_BR_hists.QCDMC_Pt_600to800_hist_AT0b
			self.QCDMC_Pt_800to1000_hist_AT0b 	= all_BR_hists.QCDMC_Pt_800to1000_hist_AT0b
			self.QCDMC_Pt_1000to1400_hist_AT0b 	= all_BR_hists.QCDMC_Pt_1000to1400_hist_AT0b
			self.QCDMC_Pt_1400to1800_hist_AT0b 	= all_BR_hists.QCDMC_Pt_1400to1800_hist_AT0b
			self.QCDMC_Pt_1800to2400_hist_AT0b 	= all_BR_hists.QCDMC_Pt_1800to2400_hist_AT0b
			self.QCDMC_Pt_2400to3200_hist_AT0b 	= all_BR_hists.QCDMC_Pt_2400to3200_hist_AT0b
			self.QCDMC_Pt_3200toInf_hist_AT0b 	= all_BR_hists.QCDMC_Pt_3200toInf_hist_AT0b

		else:
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
			self.signal_WBWB_hist_SR.append(self.load_signal_hist("SR",systematic, False , "WBWB"))
			self.signal_HTHT_hist_SR.append(self.load_signal_hist("SR",systematic, False , "HTHT"))
			self.signal_ZTZT_hist_SR.append(self.load_signal_hist("SR",systematic, False , "ZTZT"))
			self.signal_WBHT_hist_SR.append(self.load_signal_hist("SR",systematic, False , "WBHT"))
			self.signal_WBZT_hist_SR.append(self.load_signal_hist("SR",systematic, False , "WBZT"))
			self.signal_HTZT_hist_SR.append(self.load_signal_hist("SR",systematic, False , "HTZT"))


			### CR
			self.signal_WBWB_hist_CR.append(self.load_signal_hist("CR",systematic, False , "WBWB"))
			self.signal_HTHT_hist_CR.append(self.load_signal_hist("CR",systematic, False , "HTHT"))
			self.signal_ZTZT_hist_CR.append(self.load_signal_hist("CR",systematic, False , "ZTZT"))
			self.signal_WBHT_hist_CR.append(self.load_signal_hist("CR",systematic, False , "WBHT"))
			self.signal_WBZT_hist_CR.append(self.load_signal_hist("CR",systematic, False , "WBZT"))
			self.signal_HTZT_hist_CR.append(self.load_signal_hist("CR",systematic, False , "HTZT"))

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



			if self.doATxtb:

				self.signal_WBWB_hist_AT1tb.append(self.load_signal_hist("AT1tb",systematic, False , "WBWB"))
				self.signal_HTHT_hist_AT1tb.append(self.load_signal_hist("AT1tb",systematic, False , "HTHT"))
				self.signal_ZTZT_hist_AT1tb.append(self.load_signal_hist("AT1tb",systematic, False , "ZTZT"))
				self.signal_WBHT_hist_AT1tb.append(self.load_signal_hist("AT1tb",systematic, False , "WBHT"))
				self.signal_WBZT_hist_AT1tb.append(self.load_signal_hist("AT1tb",systematic, False , "WBZT"))
				self.signal_HTZT_hist_AT1tb.append(self.load_signal_hist("AT1tb",systematic, False , "HTZT"))

				self.signal_WBWB_hist_AT0tb.append(self.load_signal_hist("AT0tb",systematic, False , "WBWB"))
				self.signal_HTHT_hist_AT0tb.append(self.load_signal_hist("AT0tb",systematic, False , "HTHT"))
				self.signal_ZTZT_hist_AT0tb.append(self.load_signal_hist("AT0tb",systematic, False , "ZTZT"))
				self.signal_WBHT_hist_AT0tb.append(self.load_signal_hist("AT0tb",systematic, False , "WBHT"))
				self.signal_WBZT_hist_AT0tb.append(self.load_signal_hist("AT0tb",systematic, False , "WBZT"))
				self.signal_HTZT_hist_AT0tb.append(self.load_signal_hist("AT0tb",systematic, False , "HTZT"))


			## sideband
			if self.doSideband:

				self.signal_WBWB_hist_SB0b.append(self.load_signal_hist("SB0b",systematic_SB, False , "WBWB"))
				self.signal_HTHT_hist_SB0b.append(self.load_signal_hist("SB0b",systematic_SB, False , "HTHT"))
				self.signal_ZTZT_hist_SB0b.append(self.load_signal_hist("SB0b",systematic_SB, False , "ZTZT"))
				self.signal_WBHT_hist_SB0b.append(self.load_signal_hist("SB0b",systematic_SB, False , "WBHT"))
				self.signal_WBZT_hist_SB0b.append(self.load_signal_hist("SB0b",systematic_SB, False , "WBZT"))
				self.signal_HTZT_hist_SB0b.append(self.load_signal_hist("SB0b",systematic_SB, False , "HTZT"))

				self.signal_WBWB_hist_SB1b.append(self.load_signal_hist("SB1b",systematic_SB, False , "WBWB"))
				self.signal_HTHT_hist_SB1b.append(self.load_signal_hist("SB1b",systematic_SB, False , "HTHT"))
				self.signal_ZTZT_hist_SB1b.append(self.load_signal_hist("SB1b",systematic_SB, False , "ZTZT"))
				self.signal_WBHT_hist_SB1b.append(self.load_signal_hist("SB1b",systematic_SB, False , "WBHT"))
				self.signal_WBZT_hist_SB1b.append(self.load_signal_hist("SB1b",systematic_SB, False , "WBZT"))
				self.signal_HTZT_hist_SB1b.append(self.load_signal_hist("SB1b",systematic_SB, False , "HTZT"))



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
			if self.use_QCD_Pt:
				self.QCD_linear_SR.append(self.linearize_plot([],"QCD","SR",systematic + sample_type + year_str, False,"QCD", [ self.QCDMC_Pt_170to300_hist_SR[iii], self.QCDMC_Pt_300to470_hist_SR[iii],  self.QCDMC_Pt_470to600_hist_SR[iii], self.QCDMC_Pt_600to800_hist_SR[iii], self.QCDMC_Pt_800to1000_hist_SR[iii], self.QCDMC_Pt_1000to1400_hist_SR[iii], self.QCDMC_Pt_1400to1800_hist_SR[iii], self.QCDMC_Pt_1800to2400_hist_SR[iii], self.QCDMC_Pt_2400to3200_hist_SR[iii], self.QCDMC_Pt_3200toInf_hist_SR[iii] ]))
				self.QCD_linear_CR.append(self.linearize_plot([],"QCD","CR",systematic + sample_type + year_str, False,"QCD", [ self.QCDMC_Pt_170to300_hist_CR[iii], self.QCDMC_Pt_300to470_hist_CR[iii],  self.QCDMC_Pt_470to600_hist_CR[iii], self.QCDMC_Pt_600to800_hist_CR[iii], self.QCDMC_Pt_800to1000_hist_CR[iii], self.QCDMC_Pt_1000to1400_hist_CR[iii], self.QCDMC_Pt_1400to1800_hist_CR[iii], self.QCDMC_Pt_1800to2400_hist_CR[iii], self.QCDMC_Pt_2400to3200_hist_CR[iii], self.QCDMC_Pt_3200toInf_hist_CR[iii] ]))
				self.QCD_linear_AT0b.append(self.linearize_plot([],"QCD","AT0b",systematic + sample_type + year_str, False,"QCD", [ self.QCDMC_Pt_170to300_hist_AT0b[iii], self.QCDMC_Pt_300to470_hist_AT0b[iii],  self.QCDMC_Pt_470to600_hist_AT0b[iii], self.QCDMC_Pt_600to800_hist_AT0b[iii], self.QCDMC_Pt_800to1000_hist_AT0b[iii], self.QCDMC_Pt_1000to1400_hist_AT0b[iii], self.QCDMC_Pt_1400to1800_hist_AT0b[iii], self.QCDMC_Pt_1800to2400_hist_AT0b[iii], self.QCDMC_Pt_2400to3200_hist_AT0b[iii], self.QCDMC_Pt_3200toInf_hist_AT0b[iii] ]))
				self.QCD_linear_AT1b.append(self.linearize_plot([],"QCD","AT1b",systematic + sample_type + year_str, False,"QCD", [ self.QCDMC_Pt_170to300_hist_AT1b[iii], self.QCDMC_Pt_300to470_hist_AT1b[iii],  self.QCDMC_Pt_470to600_hist_AT1b[iii], self.QCDMC_Pt_600to800_hist_AT1b[iii], self.QCDMC_Pt_800to1000_hist_AT1b[iii], self.QCDMC_Pt_1000to1400_hist_AT1b[iii], self.QCDMC_Pt_1400to1800_hist_AT1b[iii], self.QCDMC_Pt_1800to2400_hist_AT1b[iii], self.QCDMC_Pt_2400to3200_hist_AT1b[iii], self.QCDMC_Pt_3200toInf_hist_AT1b[iii] ]))
			else:
				self.QCD_linear_SR.append(self.linearize_plot([],"QCD","SR",systematic + sample_type + year_str, False, "QCD", [ self.QCD1000to1500_hist_SR[iii], self.QCD1500to2000_hist_SR[iii],  self.QCD2000toInf_hist_SR[iii]]) )
				self.QCD_linear_CR.append(self.linearize_plot([],"QCD","CR",systematic + sample_type + year_str, False,"QCD", [ self.QCD1000to1500_hist_CR[iii], self.QCD1500to2000_hist_CR[iii],  self.QCD2000toInf_hist_CR[iii]]))
				self.QCD_linear_AT0b.append(self.linearize_plot([],"QCD","AT0b",systematic + sample_type + year_str,False, "QCD", [ self.QCD1000to1500_hist_AT0b[iii], self.QCD1500to2000_hist_AT0b[iii],  self.QCD2000toInf_hist_AT0b[iii]]))
				self.QCD_linear_AT1b.append(self.linearize_plot([],"QCD","AT1b",systematic + sample_type + year_str, False,"QCD", [ self.QCD1000to1500_hist_AT1b[iii], self.QCD1500to2000_hist_AT1b[iii],  self.QCD2000toInf_hist_AT1b[iii]]))

			if self.doATxtb:
				self.QCD_linear_AT1tb.append(self.linearize_plot([],"QCD","AT1tb",systematic + sample_type + year_str, False,"QCD", [ self.QCD1000to1500_hist_AT1tb[iii], self.QCD1500to2000_hist_AT1tb[iii],  self.QCD2000toInf_hist_AT1tb[iii]]))
				self.QCD_linear_AT0tb.append(self.linearize_plot([],"QCD","AT0tb",systematic + sample_type + year_str, False,"QCD", [ self.QCD1000to1500_hist_AT0tb[iii], self.QCD1500to2000_hist_AT0tb[iii],  self.QCD2000toInf_hist_AT0tb[iii]]))
			if self.doSideband:
				self.QCD_linear_SB0b.append(self.linearize_plot([],"QCD","SB0b",systematic + sample_type + year_str, False,"QCD", [ self.QCD1000to1500_hist_SB0b[iii], self.QCD1500to2000_hist_SB0b[iii]]))
				self.QCD_linear_SB1b.append(self.linearize_plot([],"QCD","SB1b",systematic + sample_type + year_str, False,"QCD", [ self.QCD1000to1500_hist_SB1b[iii], self.QCD1500to2000_hist_SB1b[iii]]))


			if createDummyChannel:    ## create an empty, dummy channel for each region
				self.dummy_channel_SR.append(self.create_dummy_channel(  self.QCD1000to1500_hist_SR[iii], "SR",   systematic + sample_type + year_str)) ## pass in QCD hist to get right length
				self.dummy_channel_CR.append(self.create_dummy_channel(  self.QCD1000to1500_hist_SR[iii], "CR",   systematic + sample_type + year_str))
				self.dummy_channel_AT1b.append(self.create_dummy_channel(self.QCD1000to1500_hist_SR[iii], "AT1b", systematic + sample_type + year_str))
				self.dummy_channel_AT0b.append(self.create_dummy_channel(self.QCD1000to1500_hist_SR[iii], "AT0b", systematic + sample_type + year_str))


				



			#if self.doSideband: self.QCD_linear_SB1b.append(self.linearize_plot([],"QCD","SB1b",systematic + sample_type + year_str))
			#if self.doSideband: self.QCD_linear_SB0b.append(self.linearize_plot([],"QCD","SB0b",systematic + sample_type + year_str))

			if "renorm" in systematic or "fact" in systematic: sample_type = "_TTbar"


			TTbar_hists_SR = [ self.TTJets1200to2500_hist_SR[iii], self.TTJets2500toInf_hist_SR[iii]]
			TTbar_hists_CR = [ self.TTJets1200to2500_hist_CR[iii], self.TTJets2500toInf_hist_CR[iii]]
			TTbar_hists_AT1b = [ self.TTJets1200to2500_hist_AT1b[iii], self.TTJets2500toInf_hist_AT1b[iii]]
			TTbar_hists_AT0b = [ self.TTJets1200to2500_hist_AT0b[iii], self.TTJets2500toInf_hist_AT0b[iii]]

			if self.doATxtb:
				TTbar_hists_AT1tb = [ self.TTJets1200to2500_hist_AT1tb[iii], self.TTJets2500toInf_hist_AT1tb[iii]]
				TTbar_hists_AT0tb = [ self.TTJets1200to2500_hist_AT0tb[iii], self.TTJets2500toInf_hist_AT0tb[iii]]
			if self.doSideband:
				TTbar_hists_SB1b = [ self.TTJets1200to2500_hist_SB1b[iii]]
				TTbar_hists_SB0b = [ self.TTJets1200to2500_hist_SB0b[iii]]

			if self.includeTTJets800to1200:
				TTbar_hists_SR.append( self.TTJetsMCHT800to1200_SR[iii] )
				TTbar_hists_CR.append( self.TTJetsMCHT800to1200_CR[iii]  )
				TTbar_hists_AT1b.append( self.TTJetsMCHT800to1200_AT1b[iii])
				TTbar_hists_AT0b.append(  self.TTJetsMCHT800to1200_AT0b[iii])
				if self.doATxtb:
					TTbar_hists_AT1tb.append( self.TTJetsMCHT800to1200_AT1tb[iii])
					TTbar_hists_AT0tb.append( self.TTJetsMCHT800to1200_AT0tb[iii])
				if self.doSideband:
					TTbar_hists_SB1b.append(  self.TTJetsMCHT800to1200_SB1b[iii])
					TTbar_hists_SB0b.append(  self.TTJetsMCHT800to1200_SB0b[iii])

			self.TTbar_linear_SR.append(self.linearize_plot([],"TTbar","SR",systematic + sample_type + year_str, False,"TTbar", TTbar_hists_SR ))
			self.TTbar_linear_CR.append(self.linearize_plot([],"TTbar","CR",systematic + sample_type + year_str, False,"TTbar", TTbar_hists_CR))
			self.TTbar_linear_AT0b.append(self.linearize_plot([],"TTbar","AT0b",systematic + sample_type + year_str, False,"TTbar", TTbar_hists_AT0b))
			self.TTbar_linear_AT1b.append(self.linearize_plot([],"TTbar","AT1b",systematic + sample_type + year_str, False,"TTbar", TTbar_hists_AT1b))
			if self.doATxtb:
				self.TTbar_linear_AT1tb.append(self.linearize_plot([],"TTbar","AT1tb",systematic + sample_type + year_str, False,"TTbar", TTbar_hists_AT1tb))
				self.TTbar_linear_AT0tb.append(self.linearize_plot([],"TTbar","AT0tb",systematic + sample_type + year_str, False,"TTbar", TTbar_hists_AT0tb))
			if self.doSideband:
				self.TTbar_linear_SB1b.append(self.linearize_plot([],"TTbar","SB1b",systematic + sample_type + year_str, False,"TTbar", TTbar_hists_SB1b))
				self.TTbar_linear_SB0b.append(self.linearize_plot([],"TTbar","SB0b",systematic + sample_type + year_str, False,"TTbar", TTbar_hists_SB0b ))

			#if self.doSideband: self.TTbar_linear_SB1b.append(self.linearize_plot([],"TTbar","SB1b",systematic + sample_type + year_str))
			#if self.doSideband: self.TTbar_linear_SB0b.append(self.linearize_plot([],"TTbar","SB0b",systematic + sample_type + year_str))

			if "renorm" in systematic or "fact" in systematic: sample_type = "_sig"
			self.signal_linear_SR.append(self.linearize_plot([],"sig","SR",systematic + sample_type + year_str, False,"sig", [ self.signal_WBWB_hist_SR[iii], self.signal_HTHT_hist_SR[iii], self.signal_ZTZT_hist_SR[iii], self.signal_WBHT_hist_SR[iii], self.signal_WBZT_hist_SR[iii], self.signal_HTZT_hist_SR[iii]] ))
			self.signal_linear_CR.append(self.linearize_plot([],"sig","CR",systematic + sample_type + year_str, False,"sig", [ self.signal_WBWB_hist_CR[iii], self.signal_HTHT_hist_CR[iii], self.signal_ZTZT_hist_CR[iii], self.signal_WBHT_hist_CR[iii], self.signal_WBZT_hist_CR[iii], self.signal_HTZT_hist_CR[iii]]))
			self.signal_linear_AT0b.append(self.linearize_plot([],"sig","AT0b",systematic + sample_type + year_str, False,"sig", [ self.signal_WBWB_hist_AT0b[iii], self.signal_HTHT_hist_AT0b[iii], self.signal_ZTZT_hist_AT0b[iii], self.signal_WBHT_hist_AT0b[iii], self.signal_WBZT_hist_AT0b[iii], self.signal_HTZT_hist_AT0b[iii]]))
			self.signal_linear_AT1b.append(self.linearize_plot([],"sig","AT1b",systematic + sample_type + year_str,  False,"sig", [ self.signal_WBWB_hist_AT1b[iii], self.signal_HTHT_hist_AT1b[iii], self.signal_ZTZT_hist_AT1b[iii], self.signal_WBHT_hist_AT1b[iii], self.signal_WBZT_hist_AT1b[iii], self.signal_HTZT_hist_AT1b[iii]]))
			if self.doATxtb:
				self.signal_linear_AT1tb.append(self.linearize_plot([],"sig","AT1tb",systematic + sample_type + year_str,  False,"sig", [ self.signal_WBWB_hist_AT1tb[iii], self.signal_HTHT_hist_AT1tb[iii], self.signal_ZTZT_hist_AT1tb[iii], self.signal_WBHT_hist_AT1tb[iii], self.signal_WBZT_hist_AT1tb[iii], self.signal_HTZT_hist_AT1tb[iii]]))
				self.signal_linear_AT0tb.append(self.linearize_plot([],"sig","AT0tb",systematic + sample_type + year_str,  False,"sig", [ self.signal_WBWB_hist_AT0tb[iii], self.signal_HTHT_hist_AT0tb[iii], self.signal_ZTZT_hist_AT0tb[iii], self.signal_WBHT_hist_AT0tb[iii], self.signal_WBZT_hist_AT0tb[iii], self.signal_HTZT_hist_AT0tb[iii]]))
			if self.doSideband:
				self.signal_linear_SB1b.append(self.linearize_plot([],"sig","SB1b",systematic + sample_type + year_str,  False,"sig", [ self.signal_WBWB_hist_SB1b[iii], self.signal_HTHT_hist_SB1b[iii], self.signal_ZTZT_hist_SB1b[iii], self.signal_WBHT_hist_SB1b[iii], self.signal_WBZT_hist_SB1b[iii], self.signal_HTZT_hist_SB1b[iii]]))
				self.signal_linear_SB0b.append(self.linearize_plot([],"sig","SB0b",systematic + sample_type + year_str,  False,"sig", [ self.signal_WBWB_hist_SB0b[iii], self.signal_HTHT_hist_SB0b[iii], self.signal_ZTZT_hist_SB0b[iii], self.signal_WBHT_hist_SB0b[iii], self.signal_WBZT_hist_SB0b[iii], self.signal_HTZT_hist_SB0b[iii]]))

			#print("iii/systematic: %s/%s"%(iii,systematic))
			#print("self.signal_hist_SB1b is ", self.signal_hist_SB1b, self.doSideband, self.technique_str)

			#if self.doSideband: self.signal_linear_SB1b.append(self.linearize_plot([],"sig","SB1b",systematic + sample_type + year_str))
			#if self.doSideband: self.signal_linear_SB0b.append(self.linearize_plot([],"sig","SB0b",systematic + sample_type + year_str))

			if "renorm" in systematic or "fact" in systematic: sample_type = "_ST"
			self.ST_linear_SR.append(self.linearize_plot([],"ST","SR",systematic + sample_type + year_str, False,"ST", [ self.ST_t_channel_top_hist_SR[iii], self.ST_t_channel_antitop_hist_SR[iii], self.ST_s_channel_hadrons_hist_SR[iii], self.ST_s_channel_leptons_hist_SR[iii], self.ST_tW_antitop_hist_SR[iii],self.ST_tW_top_hist_SR[iii]]  ))
			self.ST_linear_CR.append(self.linearize_plot([],"ST","CR",systematic + sample_type + year_str, False,"ST", [ self.ST_t_channel_top_hist_CR[iii], self.ST_t_channel_antitop_hist_CR[iii], self.ST_s_channel_hadrons_hist_CR[iii], self.ST_s_channel_leptons_hist_CR[iii], self.ST_tW_antitop_hist_CR[iii],self.ST_tW_top_hist_CR[iii]] ))
			self.ST_linear_AT0b.append(self.linearize_plot([],"ST","AT0b",systematic + sample_type + year_str, False,"ST", [ self.ST_t_channel_top_hist_AT0b[iii], self.ST_t_channel_antitop_hist_AT0b[iii], self.ST_s_channel_hadrons_hist_AT0b[iii], self.ST_s_channel_leptons_hist_AT0b[iii], self.ST_tW_antitop_hist_AT0b[iii],self.ST_tW_top_hist_AT0b[iii]] ))
			self.ST_linear_AT1b.append(self.linearize_plot([],"ST","AT1b",systematic + sample_type + year_str, False,"ST", [ self.ST_t_channel_top_hist_AT1b[iii], self.ST_t_channel_antitop_hist_AT1b[iii], self.ST_s_channel_hadrons_hist_AT1b[iii], self.ST_s_channel_leptons_hist_AT1b[iii], self.ST_tW_antitop_hist_AT1b[iii],self.ST_tW_top_hist_AT1b[iii]] ))
			if self.doATxtb:
				self.ST_linear_AT1tb.append(self.linearize_plot([],"ST","AT1tb",systematic + sample_type + year_str, False,"ST", [ self.ST_t_channel_top_hist_AT1tb[iii], self.ST_t_channel_antitop_hist_AT1tb[iii], self.ST_s_channel_hadrons_hist_AT1tb[iii], self.ST_s_channel_leptons_hist_AT1tb[iii], self.ST_tW_antitop_hist_AT1tb[iii],self.ST_tW_top_hist_AT1tb[iii]] ))
				self.ST_linear_AT0tb.append(self.linearize_plot([],"ST","AT0tb",systematic + sample_type + year_str, False,"ST", [ self.ST_t_channel_top_hist_AT0tb[iii], self.ST_t_channel_antitop_hist_AT0tb[iii], self.ST_s_channel_hadrons_hist_AT0tb[iii], self.ST_s_channel_leptons_hist_AT0tb[iii], self.ST_tW_antitop_hist_AT0tb[iii],self.ST_tW_top_hist_AT0tb[iii]] ))
			if self.doSideband:
				self.ST_linear_SB1b.append(self.linearize_plot([],"ST","SB1b",systematic + sample_type + year_str, False,"ST", [ self.ST_t_channel_top_hist_SB1b[iii], self.ST_t_channel_antitop_hist_SB1b[iii], self.ST_s_channel_hadrons_hist_SB1b[iii], self.ST_s_channel_leptons_hist_SB1b[iii], self.ST_tW_antitop_hist_SB1b[iii],self.ST_tW_top_hist_SB1b[iii]] ))
				self.ST_linear_SB0b.append(self.linearize_plot([],"ST","SB0b",systematic + sample_type + year_str, False,"ST", [ self.ST_t_channel_top_hist_SB0b[iii], self.ST_t_channel_antitop_hist_SB0b[iii], self.ST_s_channel_hadrons_hist_SB0b[iii], self.ST_s_channel_leptons_hist_SB0b[iii], self.ST_tW_antitop_hist_SB0b[iii],self.ST_tW_top_hist_SB0b[iii]] ))


			## new stuff
			if self.includeWJets:
				if "renorm" in systematic or "fact" in systematic: sample_type = "_WJets"
				self.WJets_linear_SR.append(self.linearize_plot([],"WJets","SR",systematic + sample_type + year_str, False,"WJets", [ self.WJetsMC_LNu_HT800to1200_SR[iii], self.WJetsMC_LNu_HT1200to2500_SR[iii], self.WJetsMC_LNu_HT2500toInf_SR[iii], self.WJetsMC_QQ_HT800toInf_SR[iii] ]  ))
				self.WJets_linear_CR.append(self.linearize_plot([],"WJets","CR",systematic + sample_type + year_str, False,"WJets", [ self.WJetsMC_LNu_HT800to1200_CR[iii], self.WJetsMC_LNu_HT1200to2500_CR[iii], self.WJetsMC_LNu_HT2500toInf_CR[iii], self.WJetsMC_QQ_HT800toInf_CR[iii]] ))
				self.WJets_linear_AT0b.append(self.linearize_plot([],"WJets","AT0b",systematic + sample_type + year_str, False,"WJets", [ self.WJetsMC_LNu_HT800to1200_AT1b[iii], self.WJetsMC_LNu_HT1200to2500_AT1b[iii], self.WJetsMC_LNu_HT2500toInf_AT1b[iii], self.WJetsMC_QQ_HT800toInf_AT1b[iii] ] ))
				self.WJets_linear_AT1b.append(self.linearize_plot([],"WJets","AT1b",systematic + sample_type + year_str, False,"WJets", [	self.WJetsMC_LNu_HT800to1200_AT0b[iii], self.WJetsMC_LNu_HT1200to2500_AT0b[iii], self.WJetsMC_LNu_HT2500toInf_AT0b[iii], self.WJetsMC_QQ_HT800toInf_AT0b[iii] ] ))
				if self.doATxtb:
					self.WJets_linear_AT1tb.append(self.linearize_plot([],"WJets","AT1tb",systematic + sample_type + year_str, False,"WJets", [	self.WJetsMC_LNu_HT800to1200_AT1tb[iii], self.WJetsMC_LNu_HT1200to2500_AT1tb[iii], self.WJetsMC_LNu_HT2500toInf_AT1tb[iii], self.WJetsMC_QQ_HT800toInf_AT1tb[iii] ] ))
					self.WJets_linear_AT0tb.append(self.linearize_plot([],"WJets","AT0tb",systematic + sample_type + year_str, False,"WJets", [ self.WJetsMC_LNu_HT800to1200_AT0tb[iii], self.WJetsMC_LNu_HT1200to2500_AT0tb[iii], self.WJetsMC_LNu_HT2500toInf_AT0tb[iii], self.WJetsMC_QQ_HT800toInf_AT0tb[iii] ] ))
				if self.doSideband:
					self.WJets_linear_SB1b.append(self.linearize_plot([],"WJets","SB1b",systematic + sample_type + year_str, False,"WJets", [  self.WJetsMC_LNu_HT800to1200_ST1b[iii], self.WJetsMC_LNu_HT1200to2500_ST1b[iii], self.WJetsMC_LNu_HT2500toInf_ST1b[iii], self.WJetsMC_QQ_HT800toInf_ST1b[iii]] ))
					self.WJets_linear_SB0b.append(self.linearize_plot([],"WJets","SB0b",systematic + sample_type + year_str, False,"WJets", [ self.WJetsMC_LNu_HT800to1200_SB0b[iii], self.WJetsMC_LNu_HT1200to2500_SB0b[iii], self.WJetsMC_LNu_HT2500toInf_SB0b[iii], self.WJetsMC_QQ_HT800toInf_SB0b[iii]] ))


			if self.includeTTTo:
				if "renorm" in systematic or "fact" in systematic: sample_type = "_TTbar" 
				self.TTTo_linear_SR.append(self.linearize_plot([],"TTTo","SR",systematic + sample_type + year_str, False,"TTTo", [ self.TTToHadronicMC_SR[iii], self.TTToSemiLeptonicMC_SR[iii], self.TTToLeptonicMC_SR[iii] ]  ))
				self.TTTo_linear_CR.append(self.linearize_plot([],"TTTo","CR",systematic + sample_type + year_str, False,"TTTo", [ self.TTToHadronicMC_CR[iii], self.TTToSemiLeptonicMC_CR[iii], self.TTToLeptonicMC_CR[iii]] ))
				self.TTTo_linear_AT0b.append(self.linearize_plot([],"TTTo","AT0b",systematic + sample_type + year_str, False,"TTTo", [ self.TTToHadronicMC_AT0b[iii], self.TTToSemiLeptonicMC_AT0b[iii], self.TTToLeptonicMC_AT0b[iii] ] ))
				self.TTTo_linear_AT1b.append(self.linearize_plot([],"TTTo","AT1b",systematic + sample_type + year_str, False,"TTTo", [ self.TTToHadronicMC_AT1b[iii], self.TTToSemiLeptonicMC_AT1b[iii], self.TTToLeptonicMC_AT1b[iii]] ))
				if self.doATxtb:
					self.TTTo_linear_AT1tb.append(self.linearize_plot([],"TTTo","AT1tb",systematic + sample_type + year_str, False,"TTTo", [ self.TTToHadronicMC_AT1tb[iii], self.TTToSemiLeptonicMC_AT1tb[iii], self.TTToLeptonicMC_AT1tb[iii]] ))
					self.TTTo_linear_AT0tb.append(self.linearize_plot([],"TTTo","AT0tb",systematic + sample_type + year_str, False,"TTTo", [ self.TTToHadronicMC_AT0tb[iii], self.TTToSemiLeptonicMC_AT0tb[iii], self.TTToLeptonicMC_AT0tb[iii]] ))
				if self.doSideband:
					self.TTTo_linear_SB1b.append(self.linearize_plot([],"TTTo","SB1b",systematic + sample_type + year_str, False,"TTTo", [ self.TTToHadronicMC_SB1b[iii], self.TTToSemiLeptonicMC_SB1b[iii], self.TTToLeptonicMC_SB1b[iii]] ))
					self.TTTo_linear_SB0b.append(self.linearize_plot([],"TTTo","SB0b",systematic + sample_type + year_str, False,"TTTo", [ self.TTToHadronicMC_SB0b[iii], self.TTToSemiLeptonicMC_SB0b[iii], self.TTToLeptonicMC_SB0b[iii] ] ))


		for iii, systematic_ in enumerate(self.data_systematic_names):

			year_str = ""
			sample_type = ""
			systematic = systematic_
			if systematic_ in self.uncorrelated_systematics:
				if year == "2015":
					year_str = "16preAPV"
				else:
					year_str =  year[-2:]

			self.data_linear_SR.append(self.linearize_plot(self.data_hist_SR[iii],"data_obs","SR",systematic + sample_type + year_str)) 
			self.data_linear_CR.append(self.linearize_plot(self.data_hist_CR[iii],"data_obs","CR",systematic + sample_type + year_str))
			self.data_linear_AT0b.append(self.linearize_plot(self.data_hist_AT0b[iii],"data_obs","AT0b",systematic + sample_type + year_str))
			self.data_linear_AT1b.append(self.linearize_plot(self.data_hist_AT1b[iii],"data_obs","AT1b",systematic + sample_type + year_str))
			if self.doATxtb:
				self.data_linear_AT1tb.append(self.linearize_plot(self.data_hist_AT1tb[iii],"data_obs","AT1tb",systematic + sample_type + year_str))
				self.data_linear_AT0tb.append(self.linearize_plot(self.data_hist_AT0tb[iii],"data_obs","AT0tb",systematic + sample_type + year_str))
			if self.doSideband: 
				self.data_linear_SB1b.append(self.linearize_plot(self.data_hist_SB1b[iii],"data_obs","SB1b",systematic + sample_type + year_str))
				self.data_linear_SB0b.append(self.linearize_plot(self.data_hist_SB0b[iii],"data_obs","SB0b",systematic + sample_type + year_str))



		print("Creating combined histograms.")
		self.create_combined_linearized_hists()

		### add stat uncertainty variations to lists	
		print("Adding stat uncertainty information.")	
		self.add_stat_uncertainties()


		print("Writing histograms.")
		self.write_histograms()
		if doExtras:
			self.print_histograms()


		# kill the linearized hists and individual signal hists
		self.kill_histograms()


	def create_combined_linearized_hists(self):

		for iii,systematic_hist_list in enumerate(self.QCD_linear_SR):
			self.all_combined_linear_SR.append( [  ] )
			systematic_name = self.systematic_names[iii] ### 


			sample_type = ""	
			year_str = ""
			if systematic_name in self.uncorrelated_systematics:
				if self.year == "2015":
					year_str = "16preAPV"
				else:
					year_str =  year[-2:]

			systematic_name = systematic_name + sample_type + year_str


			#print("systematic name is %s"%(systematic_name))
			if systematic_name in ["CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_scale"] :   
				sample_str = "allBR"
				systematic_name += "_%s"%sample_str
			if systematic_name == "nom": 
				sys_updown = [""]
			else:
				sys_updown = ["_%sUp"%systematic_name,"_%sDown"%systematic_name]


			for jjj,sys_str in enumerate(sys_updown):
				combined_hist = self.QCD_linear_SR[iii][jjj].Clone("allBR%s"%sys_str)
				combined_hist.Sumw2()
				combined_hist.Add( self.TTbar_linear_SR[iii][jjj] ) #
				#else: combined_hist.Add( self.TTTo_linear_SR[iii][jjj] )
				combined_hist.Add( self.ST_linear_SR[iii][jjj] )
				if self.includeWJets: combined_hist.Add( self.WJets_linear_SR[iii][jjj] )

				self.all_combined_linear_SR[iii].append( combined_hist  )


		for iii,systematic_hist_list in enumerate(self.QCD_linear_CR):
			self.all_combined_linear_CR.append( [ ] )
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
				combined_hist = self.QCD_linear_CR[iii][jjj].Clone("allBR%s"%sys_str)
				combined_hist.Sumw2()
				combined_hist.Add( self.TTbar_linear_CR[iii][jjj] )
				combined_hist.Add( self.ST_linear_CR[iii][jjj] )
				if self.includeWJets: combined_hist.Add( self.WJets_linear_CR[iii][jjj] )

				self.all_combined_linear_CR[iii].append( combined_hist  )

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

		#### SR 	
		combined_hist_SR = self.QCD_linear_SR[0][0].Clone("combined_SR")
		combined_hist_SR.Sumw2()
		combined_hist_SR.Add( self.TTbar_linear_SR[0][0] )
		combined_hist_SR.Add( self.ST_linear_SR[0][0] )

		QCD_SR_stat_uncert_up = self.QCD_linear_SR[0][0].Clone("QCD_stat%sUp"%year_str)
		QCD_SR_stat_uncert_up.SetTitle("linearized QCD in the SR (%s) (statUp)"%self.year)
		QCD_SR_stat_uncert_up.Reset()
		QCD_SR_stat_uncert_down = self.QCD_linear_SR[0][0].Clone("QCD_stat%sDown"%year_str)
		QCD_SR_stat_uncert_down.SetTitle("linearized QCD in the SR (%s) (statDown)"%self.year)
		QCD_SR_stat_uncert_down.Reset()


		TTbar_SR_stat_uncert_up = self.TTbar_linear_SR[0][0].Clone("TTbar_stat%sUp"%year_str)
		TTbar_SR_stat_uncert_up.SetTitle("linearized TTbar in the SR (%s) (statUp)"%self.year)
		TTbar_SR_stat_uncert_up.Reset()
		TTbar_SR_stat_uncert_down = self.TTbar_linear_SR[0][0].Clone("TTbar_stat%sDown"%year_str)
		TTbar_SR_stat_uncert_down.SetTitle("linearized TTbar in the SR (%s) (statDown)"%self.year)

		TTbar_SR_stat_uncert_down.Reset()

		ST_SR_stat_uncert_up = self.ST_linear_SR[0][0].Clone("ST_stat%sUp"%year_str)
		ST_SR_stat_uncert_up.SetTitle("linearized ST in the SR (%s) (statUp)"%self.year)
		ST_SR_stat_uncert_up.Reset()
		ST_SR_stat_uncert_down = self.ST_linear_SR[0][0].Clone("ST_stat%sDown"%year_str)
		ST_SR_stat_uncert_down.SetTitle("linearized ST in the SR (%s) (statDown)"%self.year)
		ST_SR_stat_uncert_down.Reset()

		if self.includeTTTo:
			TTTo_SR_stat_uncert_up = self.TTTo_linear_SR[0][0].Clone("TTTo_stat%sUp"%year_str)
			TTTo_SR_stat_uncert_up.SetTitle("linearized TTTo in the SR (%s) (statUp)"%self.year)
			TTTo_SR_stat_uncert_up.Reset()
			TTTo_SR_stat_uncert_down = self.TTTo_linear_SR[0][0].Clone("ST_stat%sDown"%year_str)
			TTTo_SR_stat_uncert_down.SetTitle("linearized TTTo in the SR (%s) (statDown)"%self.year)
			TTTo_SR_stat_uncert_down.Reset()

		if self.includeWJets:
			WJets_SR_stat_uncert_up = self.WJets_linear_SR[0][0].Clone("WJets_stat%sUp"%year_str)
			WJets_SR_stat_uncert_up.SetTitle("linearized WJets in the SR (%s) (statUp)"%self.year)
			WJets_SR_stat_uncert_up.Reset()
			WJets_SR_stat_uncert_down = self.WJets_linear_SR[0][0].Clone("WJets_stat%sDown"%year_str)
			WJets_SR_stat_uncert_down.SetTitle("linearized WJets in the SR (%s) (statDown)"%self.year)
			WJets_SR_stat_uncert_down.Reset()

		allBR_stat_uncert_up = self.all_combined_linear_SR[0][0].Clone("allBR_stat%sUp"%year_str)
		allBR_stat_uncert_up.SetTitle("linearized allBR in the SR (%s) (statUp)"%self.year)
		allBR_stat_uncert_up.Reset()
		allBR_stat_uncert_down = self.all_combined_linear_SR[0][0].Clone("allBR_stat%sDown"%year_str)
		allBR_stat_uncert_down.SetTitle("linearized allBR in the SR (%s) (statDown)"%self.year)
		allBR_stat_uncert_down.Reset()


		allBR_stat_uncert_up_FULL = self.all_combined_linear_SR[0][0].Clone("dummyChannel_stat%sUp"%year_str)
		allBR_stat_uncert_up_FULL.SetTitle("linearized dummyChannel in the SR (%s) (statUp)"%self.year)
		allBR_stat_uncert_up_FULL.Reset()
		allBR_stat_uncert_down_FULL = self.all_combined_linear_SR[0][0].Clone("dummyChannel_stat%sDown"%year_str)
		allBR_stat_uncert_down_FULL.SetTitle("linearized dummyChannel in the SR (%s) (statDown)"%self.year)
		allBR_stat_uncert_down_FULL.Reset()



		for iii in range(1,self.QCD_linear_SR[0][0].GetNbinsX()+1):
			total_bin_stat_uncert = combined_hist_SR.GetBinError(iii)
			total_bin_nom_value   = combined_hist_SR.GetBinContent(iii)

			QCD_bin_nom_value	 = self.QCD_linear_SR[0][0].GetBinContent(iii)
			QCD_bin_nom_uncert	= self.QCD_linear_SR[0][0].GetBinError(iii) ## should be correctly calculated in linearize_plot()
			#print("SR QCD uncert is %s for bin %s with %s counts."%(QCD_bin_nom_uncert,iii,QCD_bin_nom_value))

			TTbar_bin_nom_value	 = self.TTbar_linear_SR[0][0].GetBinContent(iii)
			TTbar_bin_nom_uncert	= self.TTbar_linear_SR[0][0].GetBinError(iii)
			#print("SR TTbar uncert is %s for bin %s with %s counts."%(TTbar_bin_nom_uncert,iii,TTbar_bin_nom_value))

			ST_bin_nom_value	 = self.ST_linear_SR[0][0].GetBinContent(iii)
			ST_bin_nom_uncert	= self.ST_linear_SR[0][0].GetBinError(iii)

			if self.includeTTTo:
				TTTo_bin_nom_value	 = self.TTTo_linear_SR[0][0].GetBinContent(iii)
				TTTo_bin_nom_uncert	 = self.TTTo_linear_SR[0][0].GetBinError(iii)
			if self.includeWJets:
				WJets_bin_nom_value	    = self.WJets_linear_SR[0][0].GetBinContent(iii)
				WJets_bin_nom_uncert	= self.WJets_linear_SR[0][0].GetBinError(iii)

			#print("SR ST uncert is %s for bin %s with %s counts."%(ST_bin_nom_uncert,iii,ST_bin_nom_value))


			#print("SR total_bin_stat_uncert is %s for bin %s with %s entries."%(total_bin_stat_uncert,iii, total_bin_nom_value))

			QCD_SR_stat_uncert_up.SetBinContent(iii, QCD_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
			QCD_SR_stat_uncert_up.SetBinError(iii, QCD_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
			QCD_SR_stat_uncert_down.SetBinContent(iii, QCD_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
			QCD_SR_stat_uncert_down.SetBinError(iii, QCD_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

			TTbar_SR_stat_uncert_up.SetBinContent(iii, TTbar_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
			TTbar_SR_stat_uncert_up.SetBinError(iii, TTbar_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
			TTbar_SR_stat_uncert_down.SetBinContent(iii, TTbar_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
			TTbar_SR_stat_uncert_down.SetBinError(iii, TTbar_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

			ST_SR_stat_uncert_up.SetBinContent(iii, ST_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
			ST_SR_stat_uncert_up.SetBinError(iii, ST_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
			ST_SR_stat_uncert_down.SetBinContent(iii, ST_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
			ST_SR_stat_uncert_down.SetBinError(iii, ST_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))
			
			if self.includeTTTo:
				TTTo_SR_stat_uncert_up.SetBinContent(iii, TTTo_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				TTTo_SR_stat_uncert_up.SetBinError(iii, TTTo_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				TTTo_SR_stat_uncert_down.SetBinContent(iii, TTTo_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				TTTo_SR_stat_uncert_down.SetBinError(iii, TTTo_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))
			if self.includeWJets:
				WJets_SR_stat_uncert_up.SetBinContent(iii, WJets_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				WJets_SR_stat_uncert_up.SetBinError(iii, WJets_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				WJets_SR_stat_uncert_down.SetBinContent(iii, WJets_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				WJets_SR_stat_uncert_down.SetBinError(iii, WJets_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

			allBR_stat_uncert_up.SetBinContent(iii,(total_bin_stat_uncert/total_bin_nom_value)  )
			allBR_stat_uncert_up.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))
			allBR_stat_uncert_down.SetBinContent(iii, (total_bin_stat_uncert/total_bin_nom_value)  )
			allBR_stat_uncert_down.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))


			allBR_stat_uncert_up_FULL.SetBinContent(iii,(1 +total_bin_stat_uncert/total_bin_nom_value)  )
			allBR_stat_uncert_up_FULL.SetBinError(iii, (1 + total_bin_stat_uncert/total_bin_nom_value))
			allBR_stat_uncert_down_FULL.SetBinContent(iii, 1 - (total_bin_stat_uncert/total_bin_nom_value)  )
			allBR_stat_uncert_down_FULL.SetBinError(iii, 1 - (total_bin_stat_uncert/total_bin_nom_value))




		self.QCD_linear_SR.append([QCD_SR_stat_uncert_up, QCD_SR_stat_uncert_down])
		self.TTbar_linear_SR.append([ TTbar_SR_stat_uncert_up, TTbar_SR_stat_uncert_down])
		self.ST_linear_SR.append([  ST_SR_stat_uncert_up, ST_SR_stat_uncert_down	 ])
		if self.includeWJets: self.WJets_linear_SR.append([  WJets_SR_stat_uncert_up, WJets_SR_stat_uncert_down	 ])
		if self.includeTTTo: self.TTTo_linear_SR.append([  TTTo_SR_stat_uncert_up, TTTo_SR_stat_uncert_down	 ]) 
		if self.createDummyChannel: 
			self.dummy_channel_SR.append([ allBR_stat_uncert_up_FULL, allBR_stat_uncert_down_FULL	  ])
		self.all_combined_linear_SR.append([ allBR_stat_uncert_up, allBR_stat_uncert_down	  ])


		## kill unecessay histograms
		del QCD_SR_stat_uncert_up,  QCD_SR_stat_uncert_down, TTbar_SR_stat_uncert_up, TTbar_SR_stat_uncert_down, ST_SR_stat_uncert_up, ST_SR_stat_uncert_down, allBR_stat_uncert_up, allBR_stat_uncert_down
		if self.includeWJets: del WJets_SR_stat_uncert_up, WJets_SR_stat_uncert_down
		if self.includeTTTo:  del TTTo_SR_stat_uncert_up, TTTo_SR_stat_uncert_down
		#### CR 	
		combined_hist_CR = self.QCD_linear_CR[0][0].Clone("combined_CR")
		combined_hist_CR.Sumw2()
		combined_hist_CR.Add( self.TTbar_linear_CR[0][0] )
		combined_hist_CR.Add( self.ST_linear_CR[0][0] )

		QCD_CR_stat_uncert_up = self.QCD_linear_CR[0][0].Clone("QCD_stat%sUp"%year_str)
		QCD_CR_stat_uncert_up.SetTitle("linearized QCD in the CR (%s) (statUp)"%self.year)
		QCD_CR_stat_uncert_up.Reset()
		QCD_CR_stat_uncert_down = self.QCD_linear_CR[0][0].Clone("QCD_stat%sDown"%year_str)
		QCD_CR_stat_uncert_down.SetTitle("linearized QCD in the CR (%s) (statDown)"%self.year)
		QCD_CR_stat_uncert_down.Reset()


		TTbar_CR_stat_uncert_up = self.TTbar_linear_CR[0][0].Clone("TTbar_stat%sUp"%year_str)
		TTbar_CR_stat_uncert_up.SetTitle("linearized TTbar in the CR (%s) (statUp)"%self.year)
		TTbar_CR_stat_uncert_up.Reset()
		TTbar_CR_stat_uncert_down = self.TTbar_linear_CR[0][0].Clone("TTbar_stat%sDown"%year_str)
		TTbar_CR_stat_uncert_down.SetTitle("linearized TTbar in the CR (%s) (statDown)"%self.year)
		TTbar_CR_stat_uncert_down.Reset()

		ST_CR_stat_uncert_up = self.ST_linear_CR[0][0].Clone("ST_stat%sUp"%year_str)
		ST_CR_stat_uncert_up.SetTitle("linearized ST in the CR (%s) (statUp)"%self.year)
		ST_CR_stat_uncert_up.Reset()
		ST_CR_stat_uncert_down = self.ST_linear_CR[0][0].Clone("ST_stat%sDown"%year_str)
		ST_CR_stat_uncert_down.SetTitle("linearized ST in the CR (%s) (statDown)"%self.year)
		ST_CR_stat_uncert_down.Reset()

		if self.includeTTTo:
			TTTo_CR_stat_uncert_up = self.TTTo_linear_SR[0][0].Clone("TTTo_stat%sUp"%year_str)
			TTTo_CR_stat_uncert_up.SetTitle("linearized TTTo in the SR (%s) (statUp)"%self.year)
			TTTo_CR_stat_uncert_up.Reset()
			TTTo_CR_stat_uncert_down = self.TTTo_linear_SR[0][0].Clone("ST_stat%sDown"%year_str)
			TTTo_CR_stat_uncert_down.SetTitle("linearized TTTo in the SR (%s) (statDown)"%self.year)
			TTTo_CR_stat_uncert_down.Reset()
		if self.includeWJets:
			WJets_CR_stat_uncert_up = self.WJets_linear_CR[0][0].Clone("WJets_stat%sUp"%year_str)
			WJets_CR_stat_uncert_up.SetTitle("linearized WJets in the CR (%s) (statUp)"%self.year)
			WJets_CR_stat_uncert_up.Reset()
			WJets_CR_stat_uncert_down = self.WJets_linear_CR[0][0].Clone("WJets_stat%sDown"%year_str)
			WJets_CR_stat_uncert_down.SetTitle("linearized WJets in the CR (%s) (statDown)"%self.year)
			WJets_CR_stat_uncert_down.Reset()

		allBR_stat_uncert_up = self.all_combined_linear_CR[0][0].Clone("allBR_stat%sUp"%year_str)
		allBR_stat_uncert_up.SetTitle("linearized allBR in the CR (%s) (statUp)"%self.year)
		allBR_stat_uncert_up.Reset()
		allBR_stat_uncert_down = self.all_combined_linear_CR[0][0].Clone("allBR_stat%sDown"%year_str)
		allBR_stat_uncert_down.SetTitle("linearized allBR in the CR (%s) (statDown)"%self.year)
		allBR_stat_uncert_down.Reset()

		allBR_stat_uncert_up_FULL = self.all_combined_linear_CR[0][0].Clone("dummyChannel_stat%sUp"%year_str)
		allBR_stat_uncert_up_FULL.SetTitle("linearized allBR in the CR (%s) (statUp)"%self.year)
		allBR_stat_uncert_up_FULL.Reset()
		allBR_stat_uncert_down_FULL = self.all_combined_linear_CR[0][0].Clone("dummyChannel_stat%sDown"%year_str)
		allBR_stat_uncert_down_FULL.SetTitle("linearized allBR in the CR (%s) (statDown)"%self.year)
		allBR_stat_uncert_down_FULL.Reset()


		for iii in range(1,self.QCD_linear_CR[0][0].GetNbinsX()+1):
			total_bin_stat_uncert = combined_hist_CR.GetBinError(iii)
			total_bin_nom_value   = combined_hist_CR.GetBinContent(iii)

			QCD_bin_nom_value	 = self.QCD_linear_CR[0][0].GetBinContent(iii)
			QCD_bin_nom_uncert	= self.QCD_linear_CR[0][0].GetBinError(iii) ## should be correctly calculated in linearize_plot()
			#print("CR QCD uncert is %s for bin %s with %s counts."%(QCD_bin_nom_uncert,iii,QCD_bin_nom_value))

			TTbar_bin_nom_value	 = self.TTbar_linear_CR[0][0].GetBinContent(iii)
			TTbar_bin_nom_uncert	= self.TTbar_linear_CR[0][0].GetBinError(iii)
			#print("CR TTbar uncert is %s for bin %s with %s counts."%(TTbar_bin_nom_uncert,iii,TTbar_bin_nom_value))

			ST_bin_nom_value	 = self.ST_linear_CR[0][0].GetBinContent(iii)
			ST_bin_nom_uncert	= self.ST_linear_CR[0][0].GetBinError(iii)

			if self.includeTTTo:
				TTTo_bin_nom_value	 = self.TTTo_linear_CR[0][0].GetBinContent(iii)
				TTTo_bin_nom_uncert	= self.TTTo_linear_CR[0][0].GetBinError(iii)
			if self.includeWJets:
				WJets_bin_nom_value	 = self.WJets_linear_CR[0][0].GetBinContent(iii)
				WJets_bin_nom_uncert	= self.WJets_linear_CR[0][0].GetBinError(iii)

			#print("CR ST uncert is %s for bin %s with %s counts."%(ST_bin_nom_uncert,iii,ST_bin_nom_value))


			#print("CR total_bin_stat_uncert is %s for bin %s with %s entries."%(total_bin_stat_uncert,iii, total_bin_nom_value))

			QCD_CR_stat_uncert_up.SetBinContent(iii, QCD_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
			QCD_CR_stat_uncert_up.SetBinError(iii, QCD_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
			QCD_CR_stat_uncert_down.SetBinContent(iii, QCD_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
			QCD_CR_stat_uncert_down.SetBinError(iii, QCD_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

			TTbar_CR_stat_uncert_up.SetBinContent(iii, TTbar_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
			TTbar_CR_stat_uncert_up.SetBinError(iii, TTbar_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
			TTbar_CR_stat_uncert_down.SetBinContent(iii, TTbar_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
			TTbar_CR_stat_uncert_down.SetBinError(iii, TTbar_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

			ST_CR_stat_uncert_up.SetBinContent(iii, ST_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
			ST_CR_stat_uncert_up.SetBinError(iii, ST_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
			ST_CR_stat_uncert_down.SetBinContent(iii, ST_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
			ST_CR_stat_uncert_down.SetBinError(iii, ST_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))
			
			if self.includeTTTo:
				TTTo_CR_stat_uncert_up.SetBinContent(iii, TTTo_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				TTTo_CR_stat_uncert_up.SetBinError(iii, TTTo_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				TTTo_CR_stat_uncert_down.SetBinContent(iii, TTTo_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				TTTo_CR_stat_uncert_down.SetBinError(iii, TTTo_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))
			if self.includeWJets:
				WJets_CR_stat_uncert_up.SetBinContent(iii, WJets_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				WJets_CR_stat_uncert_up.SetBinError(iii, WJets_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				WJets_CR_stat_uncert_down.SetBinContent(iii, WJets_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				WJets_CR_stat_uncert_down.SetBinError(iii, WJets_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

			allBR_stat_uncert_up.SetBinContent(iii,(total_bin_stat_uncert/total_bin_nom_value)  )
			allBR_stat_uncert_up.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))
			allBR_stat_uncert_down.SetBinContent(iii, (total_bin_stat_uncert/total_bin_nom_value)  )
			allBR_stat_uncert_down.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))

			allBR_stat_uncert_up.SetBinContent(iii,1+(total_bin_stat_uncert/total_bin_nom_value)  )
			allBR_stat_uncert_up.SetBinError(iii, 1+(total_bin_stat_uncert/total_bin_nom_value))
			allBR_stat_uncert_down.SetBinContent(iii, 1 - (total_bin_stat_uncert/total_bin_nom_value)  )
			allBR_stat_uncert_down.SetBinError(iii, 1 - (total_bin_stat_uncert/total_bin_nom_value))



		self.QCD_linear_CR.append([QCD_CR_stat_uncert_up, QCD_CR_stat_uncert_down])
		self.TTbar_linear_CR.append([ TTbar_CR_stat_uncert_up, TTbar_CR_stat_uncert_down])
		self.ST_linear_CR.append([  ST_CR_stat_uncert_up, ST_CR_stat_uncert_down	 ])
		if self.includeWJets: self.WJets_linear_CR.append([  WJets_CR_stat_uncert_up, WJets_CR_stat_uncert_down	 ])
		if self.includeTTTo: self.TTTo_linear_CR.append([  TTTo_CR_stat_uncert_up, TTTo_CR_stat_uncert_down	 ]) 

		self.all_combined_linear_CR.append([ allBR_stat_uncert_up, allBR_stat_uncert_down	  ])
		if self.createDummyChannel: self.dummy_channel_CR.append([ allBR_stat_uncert_up_FULL, allBR_stat_uncert_down_FULL  ])


		## kill unecessay histograms
		del QCD_CR_stat_uncert_up,  QCD_CR_stat_uncert_down, TTbar_CR_stat_uncert_up, TTbar_CR_stat_uncert_down, ST_CR_stat_uncert_up, ST_CR_stat_uncert_down, allBR_stat_uncert_up, allBR_stat_uncert_down
		if self.includeWJets: del WJets_CR_stat_uncert_up, WJets_CR_stat_uncert_down
		if self.includeTTTo:  del TTTo_CR_stat_uncert_up, TTTo_CR_stat_uncert_down
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


		if self.doATxtb:
					#### AT0tb 	
			combined_hist_AT0tb = self.QCD_linear_AT0tb[0][0].Clone("combined_AT0tb")
			combined_hist_AT0tb.Sumw2()
			combined_hist_AT0tb.Add( self.TTbar_linear_AT0tb[0][0] )
			combined_hist_AT0tb.Add( self.ST_linear_AT0tb[0][0] )

			QCD_AT0tb_stat_uncert_up = self.QCD_linear_AT0tb[0][0].Clone("QCD_stat%sUp"%year_str)
			QCD_AT0tb_stat_uncert_up.SetTitle("linearized QCD in the AT0tb (%s) (statUp)"%self.year)
			QCD_AT0tb_stat_uncert_up.Reset()
			QCD_AT0tb_stat_uncert_down = self.QCD_linear_AT0tb[0][0].Clone("QCD_stat%sDown"%year_str)
			QCD_AT0tb_stat_uncert_down.SetTitle("linearized QCD in the AT0tb (%s) (statDown)"%self.year)
			QCD_AT0tb_stat_uncert_down.Reset()


			TTbar_AT0tb_stat_uncert_up = self.TTbar_linear_AT0tb[0][0].Clone("TTbar_stat%sUp"%year_str)
			TTbar_AT0tb_stat_uncert_up.SetTitle("linearized TTbar in the AT0tb (%s) (statUp)"%self.year)
			TTbar_AT0tb_stat_uncert_up.Reset()
			TTbar_AT0tb_stat_uncert_down = self.TTbar_linear_AT0tb[0][0].Clone("TTbar_stat%sDown"%year_str)
			TTbar_AT0tb_stat_uncert_down.SetTitle("linearized TTbar in the AT0tb (%s) (statDown)"%self.year)

			TTbar_AT0tb_stat_uncert_down.Reset()

			ST_AT0tb_stat_uncert_up = self.ST_linear_AT0tb[0][0].Clone("ST_stat%sUp"%year_str)
			ST_AT0tb_stat_uncert_up.SetTitle("linearized ST in the AT0tb (%s) (statUp)"%self.year)
			ST_AT0tb_stat_uncert_up.Reset()
			ST_AT0tb_stat_uncert_down = self.ST_linear_AT0tb[0][0].Clone("ST_stat%sDown"%year_str)
			ST_AT0tb_stat_uncert_down.SetTitle("linearized ST in the AT0tb (%s) (statDown)"%self.year)
			ST_AT0tb_stat_uncert_down.Reset()

			if self.includeTTTo:
				TTTo_AT0tb_stat_uncert_up = self.TTTo_linear_AT0tb[0][0].Clone("TTTo_stat%sUp"%year_str)
				TTTo_AT0tb_stat_uncert_up.SetTitle("linearized TTTo in the SR (%s) (statUp)"%self.year)
				TTTo_AT0tb_stat_uncert_up.Reset()
				TTTo_AT0tb_stat_uncert_down = self.TTTo_linear_AT0tb[0][0].Clone("ST_stat%sDown"%year_str)
				TTTo_AT0tb_stat_uncert_down.SetTitle("linearized TTTo in the SR (%s) (statDown)"%self.year)
				TTTo_AT0tb_stat_uncert_down.Reset()
			if self.includeWJets:
				WJets_AT0tb_stat_uncert_up = self.WJets_linear_AT0tb[0][0].Clone("WJets_stat%sUp"%year_str)
				WJets_AT0tb_stat_uncert_up.SetTitle("linearized WJets in the AT0tb (%s) (statUp)"%self.year)
				WJets_AT0tb_stat_uncert_up.Reset()
				WJets_AT0tb_stat_uncert_down = self.WJets_linear_AT0tb[0][0].Clone("WJets_stat%sDown"%year_str)
				WJets_AT0tb_stat_uncert_down.SetTitle("linearized WJets in the AT0tb (%s) (statDown)"%self.year)
				WJets_AT0tb_stat_uncert_down.Reset()

			allBR_stat_uncert_up = self.all_combined_linear_AT0tb[0][0].Clone("allBR_stat%sUp"%year_str)
			allBR_stat_uncert_up.SetTitle("linearized allBR in the AT0tb (%s) (statUp)"%self.year)
			allBR_stat_uncert_up.Reset()
			allBR_stat_uncert_down = self.all_combined_linear_AT0tb[0][0].Clone("allBR_stat%sDown"%year_str)
			allBR_stat_uncert_down.SetTitle("linearized allBR in the AT0tb (%s) (statDown)"%self.year)
			allBR_stat_uncert_down.Reset()
			for iii in range(1,self.QCD_linear_AT0tb[0][0].GetNbinsX()+1):
				total_bin_stat_uncert = combined_hist_AT0tb.GetBinError(iii)
				total_bin_nom_value   = combined_hist_AT0tb.GetBinContent(iii)

				QCD_bin_nom_value	 = self.QCD_linear_AT0tb[0][0].GetBinContent(iii)
				QCD_bin_nom_uncert	= self.QCD_linear_AT0tb[0][0].GetBinError(iii) ## should be correctly calculated in linearize_plot()
				#print("AT0tb QCD uncert is %s for bin %s with %s counts."%(QCD_bin_nom_uncert,iii,QCD_bin_nom_value))

				TTbar_bin_nom_value	 = self.TTbar_linear_AT0tb[0][0].GetBinContent(iii)
				TTbar_bin_nom_uncert	= self.TTbar_linear_AT0tb[0][0].GetBinError(iii)
				#print("AT0tb TTbar uncert is %s for bin %s with %s counts."%(TTbar_bin_nom_uncert,iii,TTbar_bin_nom_value))

				ST_bin_nom_value	 = self.ST_linear_AT0tb[0][0].GetBinContent(iii)
				ST_bin_nom_uncert	= self.ST_linear_AT0tb[0][0].GetBinError(iii)

				if self.includeTTTo:
					TTTo_bin_nom_value	 = self.TTTo_linear_AT0tb[0][0].GetBinContent(iii)
					TTTo_bin_nom_uncert	= self.TTTo_linear_AT0tb[0][0].GetBinError(iii)
				if self.includeWJets:
					WJets_bin_nom_value	 = self.WJets_linear_AT0tb[0][0].GetBinContent(iii)
					WJets_bin_nom_uncert	= self.WJets_linear_AT0tb[0][0].GetBinError(iii)

				#print("AT0tb ST uncert is %s for bin %s with %s counts."%(ST_bin_nom_uncert,iii,ST_bin_nom_value))


				#print("AT0tb total_bin_stat_uncert is %s for bin %s with %s entries."%(total_bin_stat_uncert,iii, total_bin_nom_value))

				QCD_AT0tb_stat_uncert_up.SetBinContent(iii, QCD_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				QCD_AT0tb_stat_uncert_up.SetBinError(iii, QCD_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				QCD_AT0tb_stat_uncert_down.SetBinContent(iii, QCD_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				QCD_AT0tb_stat_uncert_down.SetBinError(iii, QCD_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				TTbar_AT0tb_stat_uncert_up.SetBinContent(iii, TTbar_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				TTbar_AT0tb_stat_uncert_up.SetBinError(iii, TTbar_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				TTbar_AT0tb_stat_uncert_down.SetBinContent(iii, TTbar_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				TTbar_AT0tb_stat_uncert_down.SetBinError(iii, TTbar_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				ST_AT0tb_stat_uncert_up.SetBinContent(iii, ST_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				ST_AT0tb_stat_uncert_up.SetBinError(iii, ST_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				ST_AT0tb_stat_uncert_down.SetBinContent(iii, ST_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				ST_AT0tb_stat_uncert_down.SetBinError(iii, ST_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				if self.includeTTTo:
					TTTo_AT0tb_stat_uncert_up.SetBinContent(iii, TTTo_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
					TTTo_AT0tb_stat_uncert_up.SetBinError(iii, TTTo_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
					TTTo_AT0tb_stat_uncert_down.SetBinContent(iii, TTTo_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
					TTTo_AT0tb_stat_uncert_down.SetBinError(iii, TTTo_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))
				if self.includeWJets:
					WJets_AT0tb_stat_uncert_up.SetBinContent(iii, WJets_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
					WJets_AT0tb_stat_uncert_up.SetBinError(iii, WJets_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
					WJets_AT0tb_stat_uncert_down.SetBinContent(iii, WJets_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
					WJets_AT0tb_stat_uncert_down.SetBinError(iii, WJets_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				allBR_stat_uncert_up.SetBinContent(iii,(total_bin_stat_uncert/total_bin_nom_value)  )
				allBR_stat_uncert_up.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))
				allBR_stat_uncert_down.SetBinContent(iii, (total_bin_stat_uncert/total_bin_nom_value)  )
				allBR_stat_uncert_down.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))

			self.QCD_linear_AT0tb.append([QCD_AT0tb_stat_uncert_up, QCD_AT0tb_stat_uncert_down])
			self.TTbar_linear_AT0tb.append([ TTbar_AT0tb_stat_uncert_up, TTbar_AT0tb_stat_uncert_down])
			self.ST_linear_AT0tb.append([  ST_AT0tb_stat_uncert_up, ST_AT0tb_stat_uncert_down	 ])
			if self.includeWJets:  self.WJets_linear_AT0tb.append([  WJets_AT0tb_stat_uncert_up, WJets_AT0tb_stat_uncert_down	 ])
			if self.includeTTTo: self.TTTo_linear_AT0tb.append([  TTTo_AT0tb_stat_uncert_up, TTTo_AT0tb_stat_uncert_down	 ]) 
			self.all_combined_linear_AT0tb.append([ allBR_stat_uncert_up, allBR_stat_uncert_down	  ])


			## kill unecessay histograms
			del QCD_AT0tb_stat_uncert_up,  QCD_AT0tb_stat_uncert_down, TTbar_AT0tb_stat_uncert_up, TTbar_AT0tb_stat_uncert_down, ST_AT0tb_stat_uncert_up, ST_AT0tb_stat_uncert_down, allBR_stat_uncert_up, allBR_stat_uncert_down
			if self.includeWJets: del WJets_AT0tb_stat_uncert_up, WJets_AT0tb_stat_uncert_down
			if self.includeTTTo:  del TTTo_AT0tb_stat_uncert_up, TTTo_AT0tb_stat_uncert_down

			#### AT1tb 	
			combined_hist_AT1tb = self.QCD_linear_AT1tb[0][0].Clone("combined_AT1tb")
			combined_hist_AT1tb.Sumw2()
			combined_hist_AT1tb.Add( self.TTbar_linear_AT1tb[0][0] )
			combined_hist_AT1tb.Add( self.ST_linear_AT1tb[0][0] )

			QCD_AT1tb_stat_uncert_up = self.QCD_linear_AT1tb[0][0].Clone("QCD_stat%sUp"%year_str)
			QCD_AT1tb_stat_uncert_up.SetTitle("linearized QCD in the AT1tb (%s) (statUp)"%self.year)
			QCD_AT1tb_stat_uncert_up.Reset()
			QCD_AT1tb_stat_uncert_down = self.QCD_linear_AT1tb[0][0].Clone("QCD_stat%sDown"%year_str)
			QCD_AT1tb_stat_uncert_down.SetTitle("linearized QCD in the AT1tb (%s) (statDown)"%self.year)
			QCD_AT1tb_stat_uncert_down.Reset()


			TTbar_AT1tb_stat_uncert_up = self.TTbar_linear_AT1tb[0][0].Clone("TTbar_stat%sUp"%year_str)
			TTbar_AT1tb_stat_uncert_up.SetTitle("linearized TTbar in the AT1tb (%s) (statUp)"%self.year)
			TTbar_AT1tb_stat_uncert_up.Reset()
			TTbar_AT1tb_stat_uncert_down = self.TTbar_linear_AT1tb[0][0].Clone("TTbar_stat%sDown"%year_str)
			TTbar_AT1tb_stat_uncert_down.SetTitle("linearized TTbar in the AT1tb (%s) (statDown)"%self.year)

			TTbar_AT1tb_stat_uncert_down.Reset()

			ST_AT1tb_stat_uncert_up = self.ST_linear_AT1tb[0][0].Clone("ST_stat%sUp"%year_str)
			ST_AT1tb_stat_uncert_up.SetTitle("linearized ST in the AT1tb (%s) (statUp)"%self.year)
			ST_AT1tb_stat_uncert_up.Reset()
			ST_AT1tb_stat_uncert_down = self.ST_linear_AT1tb[0][0].Clone("ST_stat%sDown"%year_str)
			ST_AT1tb_stat_uncert_down.SetTitle("linearized ST in the AT1tb (%s) (statDown)"%self.year)
			ST_AT1tb_stat_uncert_down.Reset()

			if self.includeTTTo:
				TTTo_AT1tb_stat_uncert_up = self.TTTo_linear_AT1tb[0][0].Clone("TTTo_stat%sUp"%year_str)
				TTTo_AT1tb_stat_uncert_up.SetTitle("linearized TTTo in the SR (%s) (statUp)"%self.year)
				TTTo_AT1tb_stat_uncert_up.Reset()
				TTTo_AT1tb_stat_uncert_down = self.TTTo_linear_AT1tb[0][0].Clone("ST_stat%sDown"%year_str)
				TTTo_AT1tb_stat_uncert_down.SetTitle("linearized TTTo in the SR (%s) (statDown)"%self.year)
				TTTo_AT1tb_stat_uncert_down.Reset()
			if self.includeWJets:
				WJets_AT1tb_stat_uncert_up = self.WJets_linear_AT1tb[0][0].Clone("WJets_stat%sUp"%year_str)
				WJets_AT1tb_stat_uncert_up.SetTitle("linearized WJets in the AT1tb (%s) (statUp)"%self.year)
				WJets_AT1tb_stat_uncert_up.Reset()
				WJets_AT1tb_stat_uncert_down = self.WJets_linear_AT1tb[0][0].Clone("WJets_stat%sDown"%year_str)
				WJets_AT1tb_stat_uncert_down.SetTitle("linearized WJets in the AT1tb (%s) (statDown)"%self.year)
				WJets_AT1tb_stat_uncert_down.Reset()

			allBR_stat_uncert_up = self.all_combined_linear_AT1tb[0][0].Clone("allBR_stat%sUp"%year_str)
			allBR_stat_uncert_up.SetTitle("linearized allBR in the AT1tb (%s) (statUp)"%self.year)
			allBR_stat_uncert_up.Reset()
			allBR_stat_uncert_down = self.all_combined_linear_AT1tb[0][0].Clone("allBR_stat%sDown"%year_str)
			allBR_stat_uncert_down.SetTitle("linearized allBR in the AT1tb (%s) (statDown)"%self.year)
			allBR_stat_uncert_down.Reset()
			for iii in range(1,self.QCD_linear_AT1tb[0][0].GetNbinsX()+1):
				total_bin_stat_uncert = combined_hist_AT1tb.GetBinError(iii)
				total_bin_nom_value   = combined_hist_AT1tb.GetBinContent(iii)

				QCD_bin_nom_value	 = self.QCD_linear_AT1tb[0][0].GetBinContent(iii)
				QCD_bin_nom_uncert	= self.QCD_linear_AT1tb[0][0].GetBinError(iii) ## should be correctly calculated in linearize_plot()
				#print("AT1tb QCD uncert is %s for bin %s with %s counts."%(QCD_bin_nom_uncert,iii,QCD_bin_nom_value))

				TTbar_bin_nom_value	 = self.TTbar_linear_AT1tb[0][0].GetBinContent(iii)
				TTbar_bin_nom_uncert	= self.TTbar_linear_AT1tb[0][0].GetBinError(iii)
				#print("AT1tb TTbar uncert is %s for bin %s with %s counts."%(TTbar_bin_nom_uncert,iii,TTbar_bin_nom_value))

				ST_bin_nom_value	 = self.ST_linear_AT1tb[0][0].GetBinContent(iii)
				ST_bin_nom_uncert	= self.ST_linear_AT1tb[0][0].GetBinError(iii)


				if self.includeTTTo:
					TTTo_bin_nom_value	 = self.TTTo_linear_AT1tb[0][0].GetBinContent(iii)
					TTTo_bin_nom_uncert	= self.TTTo_linear_AT1tb[0][0].GetBinError(iii)
				if self.includeWJets:
					WJets_bin_nom_value	 = self.WJets_linear_AT1tb[0][0].GetBinContent(iii)
					WJets_bin_nom_uncert	= self.WJets_linear_AT1tb[0][0].GetBinError(iii)

				#print("AT1tb ST uncert is %s for bin %s with %s counts."%(ST_bin_nom_uncert,iii,ST_bin_nom_value))


				#print("AT1tb total_bin_stat_uncert is %s for bin %s with %s entries."%(total_bin_stat_uncert,iii, total_bin_nom_value))

				QCD_AT1tb_stat_uncert_up.SetBinContent(iii, QCD_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				QCD_AT1tb_stat_uncert_up.SetBinError(iii, QCD_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				QCD_AT1tb_stat_uncert_down.SetBinContent(iii, QCD_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				QCD_AT1tb_stat_uncert_down.SetBinError(iii, QCD_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				TTbar_AT1tb_stat_uncert_up.SetBinContent(iii, TTbar_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				TTbar_AT1tb_stat_uncert_up.SetBinError(iii, TTbar_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				TTbar_AT1tb_stat_uncert_down.SetBinContent(iii, TTbar_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				TTbar_AT1tb_stat_uncert_down.SetBinError(iii, TTbar_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				ST_AT1tb_stat_uncert_up.SetBinContent(iii, ST_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				ST_AT1tb_stat_uncert_up.SetBinError(iii, ST_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				ST_AT1tb_stat_uncert_down.SetBinContent(iii, ST_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				ST_AT1tb_stat_uncert_down.SetBinError(iii, ST_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				if self.includeTTTo:
					TTTo_AT1tb_stat_uncert_up.SetBinContent(iii, TTTo_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
					TTTo_AT1tb_stat_uncert_up.SetBinError(iii, TTTo_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
					TTTo_AT1tb_stat_uncert_down.SetBinContent(iii, TTTo_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
					TTTo_AT1tb_stat_uncert_down.SetBinError(iii, TTTo_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))
				if self.includeWJets:
					WJets_AT1tb_stat_uncert_up.SetBinContent(iii, WJets_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
					WJets_AT1tb_stat_uncert_up.SetBinError(iii, WJets_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
					WJets_AT1tb_stat_uncert_down.SetBinContent(iii, WJets_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
					WJets_AT1tb_stat_uncert_down.SetBinError(iii, WJets_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				allBR_stat_uncert_up.SetBinContent(iii,(total_bin_stat_uncert/total_bin_nom_value)  )
				allBR_stat_uncert_up.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))
				allBR_stat_uncert_down.SetBinContent(iii, (total_bin_stat_uncert/total_bin_nom_value)  )
				allBR_stat_uncert_down.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))

			self.QCD_linear_AT1tb.append([QCD_AT1tb_stat_uncert_up, QCD_AT1tb_stat_uncert_down])
			self.TTbar_linear_AT1tb.append([ TTbar_AT1tb_stat_uncert_up, TTbar_AT1tb_stat_uncert_down])
			self.ST_linear_AT1tb.append([  ST_AT1tb_stat_uncert_up, ST_AT1tb_stat_uncert_down	 ])
			if self.includeWJets: self.WJets_linear_AT1tb.append([  WJets_AT1tb_stat_uncert_up, WJets_AT1tb_stat_uncert_down	 ])
			if self.includeTTTo: self.TTTo_linear_AT1tb.append([  TTTo_AT1tb_stat_uncert_up, TTTo_AT1tb_stat_uncert_down	 ]) 
			self.all_combined_linear_AT1tb.append([ allBR_stat_uncert_up, allBR_stat_uncert_down	  ])


			## kill unecessay histograms
			del QCD_AT1tb_stat_uncert_up,  QCD_AT1tb_stat_uncert_down, TTbar_AT1tb_stat_uncert_up, TTbar_AT1tb_stat_uncert_down, ST_AT1tb_stat_uncert_up, ST_AT1tb_stat_uncert_down, allBR_stat_uncert_up, allBR_stat_uncert_down,WJets_AT1tb_stat_uncert_up, WJets_AT1tb_stat_uncert_down
			if self.includeWJets: del WJets_AT1tb_stat_uncert_up, WJets_AT1tb_stat_uncert_down
			if self.includeTTTo:  del TTTo_AT1tb_stat_uncert_up, TTTo_AT1tb_stat_uncert_down

		#### SB1b 	

		if self.doSideband:
			#### SB1b 	
			combined_hist_SB1b = self.QCD_linear_SB1b[0][0].Clone("combined_SB1b")
			combined_hist_SB1b.Sumw2()
			combined_hist_SB1b.Add( self.TTbar_linear_SB1b[0][0] )
			combined_hist_SB1b.Add( self.ST_linear_SB1b[0][0] )

			QCD_SB1b_stat_uncert_up = self.QCD_linear_SB1b[0][0].Clone("QCD_stat%sUp"%year_str)
			QCD_SB1b_stat_uncert_up.SetTitle("linearized QCD in the SB1b (%s) (statUp)"%self.year)
			QCD_SB1b_stat_uncert_up.Reset()
			QCD_SB1b_stat_uncert_down = self.QCD_linear_SB1b[0][0].Clone("QCD_stat%sDown"%year_str)
			QCD_SB1b_stat_uncert_down.SetTitle("linearized QCD in the SB1b (%s) (statDown)"%self.year)
			QCD_SB1b_stat_uncert_down.Reset()

			TTbar_SB1b_stat_uncert_up = self.TTbar_linear_SB1b[0][0].Clone("TTbar_stat%sUp"%year_str)
			TTbar_SB1b_stat_uncert_up.SetTitle("linearized TTbar in the SB1b (%s) (statUp)"%self.year)
			TTbar_SB1b_stat_uncert_up.Reset()
			TTbar_SB1b_stat_uncert_down = self.TTbar_linear_SB1b[0][0].Clone("TTbar_stat%sDown"%year_str)
			TTbar_SB1b_stat_uncert_down.SetTitle("linearized TTbar in the SB1b (%s) (statDown)"%self.year)
			TTbar_SB1b_stat_uncert_down.Reset()

			ST_SB1b_stat_uncert_up = self.ST_linear_SB1b[0][0].Clone("ST_stat%sUp"%year_str)
			ST_SB1b_stat_uncert_up.SetTitle("linearized ST in the SB1b (%s) (statUp)"%self.year)
			ST_SB1b_stat_uncert_up.Reset()
			ST_SB1b_stat_uncert_down = self.ST_linear_SB1b[0][0].Clone("ST_stat%sDown"%year_str)
			ST_SB1b_stat_uncert_down.SetTitle("linearized ST in the SB1b (%s) (statDown)"%self.year)
			ST_SB1b_stat_uncert_down.Reset()

			if self.includeTTTo:
				TTTo_SB1b_stat_uncert_up = self.TTTo_linear_SB1b[0][0].Clone("TTTo_stat%sUp"%year_str)
				TTTo_SB1b_stat_uncert_up.SetTitle("linearized TTTo in the SB1b (%s) (statUp)"%self.year)
				TTTo_SB1b_stat_uncert_up.Reset()
				TTTo_SB1b_stat_uncert_down = self.TTTo_linear_SB1b[0][0].Clone("TTTo_stat%sDown"%year_str)
				TTTo_SB1b_stat_uncert_down.SetTitle("linearized TTTo in the SB1b (%s) (statDown)"%self.year)
				TTTo_SB1b_stat_uncert_down.Reset()
			if self.includeWJets:
				WJets_SB1b_stat_uncert_up = self.WJets_linear_SB1b[0][0].Clone("WJets_stat%sUp"%year_str)
				WJets_SB1b_stat_uncert_up.SetTitle("linearized WJets in the SB1b (%s) (statUp)"%self.year)
				WJets_SB1b_stat_uncert_up.Reset()
				WJets_SB1b_stat_uncert_down = self.WJets_linear_SB1b[0][0].Clone("WJets_stat%sDown"%year_str)
				WJets_SB1b_stat_uncert_down.SetTitle("linearized WJets in the SB1b (%s) (statDown)"%self.year)
				WJets_SB1b_stat_uncert_down.Reset()

			allBR_stat_uncert_up = self.all_combined_linear_SB1b[0][0].Clone("allBR_stat%sUp"%year_str)
			allBR_stat_uncert_up.SetTitle("linearized allBR in the SB1b (%s) (statUp)"%self.year)
			allBR_stat_uncert_up.Reset()
			allBR_stat_uncert_down = self.all_combined_linear_SB1b[0][0].Clone("allBR_stat%sDown"%year_str)
			allBR_stat_uncert_down.SetTitle("linearized allBR in the SB1b (%s) (statDown)"%self.year)
			allBR_stat_uncert_down.Reset()
			for iii in range(1,self.QCD_linear_SB1b[0][0].GetNbinsX()+1):
				total_bin_stat_uncert = combined_hist_SB1b.GetBinError(iii)
				total_bin_nom_value   = combined_hist_SB1b.GetBinContent(iii)

				QCD_bin_nom_value	 = self.QCD_linear_SB1b[0][0].GetBinContent(iii)
				QCD_bin_nom_uncert	= self.QCD_linear_SB1b[0][0].GetBinError(iii) ## should be correctly calculated in linearize_plot()
				#print("SB1b QCD uncert is %s for bin %s with %s counts."%(QCD_bin_nom_uncert,iii,QCD_bin_nom_value))

				TTbar_bin_nom_value	 = self.TTbar_linear_SB1b[0][0].GetBinContent(iii)
				TTbar_bin_nom_uncert	= self.TTbar_linear_SB1b[0][0].GetBinError(iii)
				#print("SB1b TTbar uncert is %s for bin %s with %s counts."%(TTbar_bin_nom_uncert,iii,TTbar_bin_nom_value))

				ST_bin_nom_value	 = self.ST_linear_SB1b[0][0].GetBinContent(iii)
				ST_bin_nom_uncert	= self.ST_linear_SB1b[0][0].GetBinError(iii)


				if self.includeTTTo:
					TTTo_bin_nom_value	 = self.TTTo_linear_SB1b[0][0].GetBinContent(iii)
					TTTo_bin_nom_uncert	= self.TTTo_linear_SB1b[0][0].GetBinError(iii)
				if self.includeWJets:
					WJets_bin_nom_value	 = self.WJets_linear_SB1b[0][0].GetBinContent(iii)
					WJets_bin_nom_uncert	= self.WJets_linear_SB1b[0][0].GetBinError(iii)

				#print("SB1b ST uncert is %s for bin %s with %s counts."%(ST_bin_nom_uncert,iii,ST_bin_nom_value))


				#print("SB1b total_bin_stat_uncert is %s for bin %s with %s entries."%(total_bin_stat_uncert,iii, total_bin_nom_value))

				QCD_SB1b_stat_uncert_up.SetBinContent(iii, QCD_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				QCD_SB1b_stat_uncert_up.SetBinError(iii, QCD_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				QCD_SB1b_stat_uncert_down.SetBinContent(iii, QCD_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				QCD_SB1b_stat_uncert_down.SetBinError(iii, QCD_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				TTbar_SB1b_stat_uncert_up.SetBinContent(iii, TTbar_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				TTbar_SB1b_stat_uncert_up.SetBinError(iii, TTbar_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				TTbar_SB1b_stat_uncert_down.SetBinContent(iii, TTbar_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				TTbar_SB1b_stat_uncert_down.SetBinError(iii, TTbar_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				ST_SB1b_stat_uncert_up.SetBinContent(iii, ST_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				ST_SB1b_stat_uncert_up.SetBinError(iii, ST_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				ST_SB1b_stat_uncert_down.SetBinContent(iii, ST_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				ST_SB1b_stat_uncert_down.SetBinError(iii, ST_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))


				if self.includeTTTo:
					TTTo_SB1b_stat_uncert_up.SetBinContent(iii, TTTo_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
					TTTo_SB1b_stat_uncert_up.SetBinError(iii, TTTo_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
					TTTo_SB1b_stat_uncert_down.SetBinContent(iii, TTTo_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
					TTTo_SB1b_stat_uncert_down.SetBinError(iii, TTTo_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				if self.includeWJets:
					WJets_SB1b_stat_uncert_up.SetBinContent(iii, WJets_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
					WJets_SB1b_stat_uncert_up.SetBinError(iii, WJets_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
					WJets_SB1b_stat_uncert_down.SetBinContent(iii, WJets_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
					WJets_SB1b_stat_uncert_down.SetBinError(iii, WJets_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				allBR_stat_uncert_up.SetBinContent(iii,(total_bin_stat_uncert/total_bin_nom_value)  )
				allBR_stat_uncert_up.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))
				allBR_stat_uncert_down.SetBinContent(iii, (total_bin_stat_uncert/total_bin_nom_value)  )
				allBR_stat_uncert_down.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))

			self.QCD_linear_SB1b.append([QCD_SB1b_stat_uncert_up, QCD_SB1b_stat_uncert_down])
			self.TTbar_linear_SB1b.append([ TTbar_SB1b_stat_uncert_up, TTbar_SB1b_stat_uncert_down])
			self.ST_linear_SB1b.append([  ST_SB1b_stat_uncert_up, ST_SB1b_stat_uncert_down	 ])
			if self.includeWJets: self.WJets_linear_SB1b.append([  WJets_SB1b_stat_uncert_up, WJets_SB1b_stat_uncert_down	 ])
			if self.includeTTTo: self.TTTo_linear_SB1b.append([  TTTo_SB1b_stat_uncert_up, TTTo_SB1b_stat_uncert_down	 ]) 
			self.all_combined_linear_SB1b.append([ allBR_stat_uncert_up, allBR_stat_uncert_down	  ])


			## kill unecessay histograms
			del QCD_SB1b_stat_uncert_up,  QCD_SB1b_stat_uncert_down, TTbar_SB1b_stat_uncert_up, TTbar_SB1b_stat_uncert_down, ST_SB1b_stat_uncert_up, ST_SB1b_stat_uncert_down, allBR_stat_uncert_up, allBR_stat_uncert_down
			if self.includeWJets: del WJets_SB1b_stat_uncert_up, WJets_SB1b_stat_uncert_down
			if self.includeTTTo:  del TTTo_SB1b_stat_uncert_up, TTTo_SB1b_stat_uncert_down
					#### SB0b 	
			combined_hist_SB0b = self.QCD_linear_SB0b[0][0].Clone("combined_SB0b")
			combined_hist_SB0b.Sumw2()
			combined_hist_SB0b.Add( self.TTbar_linear_SB0b[0][0] )
			combined_hist_SB0b.Add( self.ST_linear_SB0b[0][0] )

			QCD_SB0b_stat_uncert_up = self.QCD_linear_SB0b[0][0].Clone("QCD_stat%sUp"%year_str)
			QCD_SB0b_stat_uncert_up.SetTitle("linearized QCD in the SB0b (%s) (statUp)"%self.year)
			QCD_SB0b_stat_uncert_up.Reset()
			QCD_SB0b_stat_uncert_down = self.QCD_linear_SB0b[0][0].Clone("QCD_stat%sDown"%year_str)
			QCD_SB0b_stat_uncert_down.SetTitle("linearized QCD in the SB0b (%s) (statDown)"%self.year)
			QCD_SB0b_stat_uncert_down.Reset()


			TTbar_SB0b_stat_uncert_up = self.TTbar_linear_SB0b[0][0].Clone("TTbar_stat%sUp"%year_str)
			TTbar_SB0b_stat_uncert_up.SetTitle("linearized TTbar in the SB0b (%s) (statUp)"%self.year)
			TTbar_SB0b_stat_uncert_up.Reset()
			TTbar_SB0b_stat_uncert_down = self.TTbar_linear_SB0b[0][0].Clone("TTbar_stat%sDown"%year_str)
			TTbar_SB0b_stat_uncert_down.SetTitle("linearized TTbar in the SB0b (%s) (statDown)"%self.year)

			TTbar_SB0b_stat_uncert_down.Reset()

			ST_SB0b_stat_uncert_up = self.ST_linear_SB0b[0][0].Clone("ST_stat%sUp"%year_str)
			ST_SB0b_stat_uncert_up.SetTitle("linearized ST in the SB0b (%s) (statUp)"%self.year)
			ST_SB0b_stat_uncert_up.Reset()
			ST_SB0b_stat_uncert_down = self.ST_linear_SB0b[0][0].Clone("ST_stat%sDown"%year_str)
			ST_SB0b_stat_uncert_down.SetTitle("linearized ST in the SB0b (%s) (statDown)"%self.year)
			ST_SB0b_stat_uncert_down.Reset()

			if self.includeTTo:
				TTTo_SB0b_stat_uncert_up = self.TTTo_linear_SB0b[0][0].Clone("TTTo_stat%sUp"%year_str)
				TTTo_SB0b_stat_uncert_up.SetTitle("linearized TTTo in the SB0b (%s) (statUp)"%self.year)
				TTTo_SB0b_stat_uncert_up.Reset()
				TTTo_SB0b_stat_uncert_down = self.TTTo_linear_SB0b[0][0].Clone("TTTo_stat%sDown"%year_str)
				TTTo_SB0b_stat_uncert_down.SetTitle("linearized TTTo in the SB0b (%s) (statDown)"%self.year)
				TTTo_SB0b_stat_uncert_down.Reset()

			if self.includeWJets:
				WJets_SB0b_stat_uncert_up = self.WJets_linear_SB0b[0][0].Clone("WJets_stat%sUp"%year_str)
				WJets_SB0b_stat_uncert_up.SetTitle("linearized WJets in the SB0b (%s) (statUp)"%self.year)
				WJets_SB0b_stat_uncert_up.Reset()
				WJets_SB0b_stat_uncert_down = self.WJets_linear_SB0b[0][0].Clone("WJets_stat%sDown"%year_str)
				WJets_SB0b_stat_uncert_down.SetTitle("linearized WJets in the SB0b (%s) (statDown)"%self.year)
				WJets_SB0b_stat_uncert_down.Reset()

			allBR_stat_uncert_up = self.all_combined_linear_SB0b[0][0].Clone("allBR_stat%sUp"%year_str)
			allBR_stat_uncert_up.SetTitle("linearized allBR in the SB0b (%s) (statUp)"%self.year)
			allBR_stat_uncert_up.Reset()
			allBR_stat_uncert_down = self.all_combined_linear_SB0b[0][0].Clone("allBR_stat%sDown"%year_str)
			allBR_stat_uncert_down.SetTitle("linearized allBR in the SB0b (%s) (statDown)"%self.year)
			allBR_stat_uncert_down.Reset()
			for iii in range(1,self.QCD_linear_SB0b[0][0].GetNbinsX()+1):
				total_bin_stat_uncert = combined_hist_SB0b.GetBinError(iii)
				total_bin_nom_value   = combined_hist_SB0b.GetBinContent(iii)

				QCD_bin_nom_value	 = self.QCD_linear_SB0b[0][0].GetBinContent(iii)
				QCD_bin_nom_uncert	= self.QCD_linear_SB0b[0][0].GetBinError(iii) ## should be correctly calculated in linearize_plot()
				#print("SB0b QCD uncert is %s for bin %s with %s counts."%(QCD_bin_nom_uncert,iii,QCD_bin_nom_value))

				TTbar_bin_nom_value	 = self.TTbar_linear_SB0b[0][0].GetBinContent(iii)
				TTbar_bin_nom_uncert	= self.TTbar_linear_SB0b[0][0].GetBinError(iii)
				#print("SB0b TTbar uncert is %s for bin %s with %s counts."%(TTbar_bin_nom_uncert,iii,TTbar_bin_nom_value))

				ST_bin_nom_value	 = self.ST_linear_SB0b[0][0].GetBinContent(iii)
				ST_bin_nom_uncert	= self.ST_linear_SB0b[0][0].GetBinError(iii)

				if self.includeTTTo:
					TTTo_bin_nom_value	 = self.TTTo_linear_SB0b[0][0].GetBinContent(iii)
					TTTo_bin_nom_uncert	= self.TTTo_linear_SB0b[0][0].GetBinError(iii)
				if self.includeWJets:
					WJets_bin_nom_value	 = self.WJets_linear_SB0b[0][0].GetBinContent(iii)
					WJets_bin_nom_uncert	= self.WJets_linear_SB0b[0][0].GetBinError(iii)

				#print("SB0b ST uncert is %s for bin %s with %s counts."%(ST_bin_nom_uncert,iii,ST_bin_nom_value))


				#print("SB0b total_bin_stat_uncert is %s for bin %s with %s entries."%(total_bin_stat_uncert,iii, total_bin_nom_value))

				QCD_SB0b_stat_uncert_up.SetBinContent(iii, QCD_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				QCD_SB0b_stat_uncert_up.SetBinError(iii, QCD_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				QCD_SB0b_stat_uncert_down.SetBinContent(iii, QCD_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				QCD_SB0b_stat_uncert_down.SetBinError(iii, QCD_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				TTbar_SB0b_stat_uncert_up.SetBinContent(iii, TTbar_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				TTbar_SB0b_stat_uncert_up.SetBinError(iii, TTbar_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				TTbar_SB0b_stat_uncert_down.SetBinContent(iii, TTbar_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				TTbar_SB0b_stat_uncert_down.SetBinError(iii, TTbar_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				ST_SB0b_stat_uncert_up.SetBinContent(iii, ST_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
				ST_SB0b_stat_uncert_up.SetBinError(iii, ST_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
				ST_SB0b_stat_uncert_down.SetBinContent(iii, ST_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
				ST_SB0b_stat_uncert_down.SetBinError(iii, ST_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				if self.includeTTTo:
					TTTo_SB0b_stat_uncert_up.SetBinContent(iii, TTTo_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
					TTTo_SB0b_stat_uncert_up.SetBinError(iii, TTTo_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
					TTTo_SB0b_stat_uncert_down.SetBinContent(iii, TTTo_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
					TTTo_SB0b_stat_uncert_down.SetBinError(iii, TTTo_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				if self.includeWJets:
					WJets_SB0b_stat_uncert_up.SetBinContent(iii, WJets_bin_nom_value* (1+total_bin_stat_uncert/total_bin_nom_value)  )
					WJets_SB0b_stat_uncert_up.SetBinError(iii, WJets_bin_nom_uncert * (1+total_bin_stat_uncert/total_bin_nom_value))
					WJets_SB0b_stat_uncert_down.SetBinContent(iii, WJets_bin_nom_value* (1 - total_bin_stat_uncert/total_bin_nom_value)  )
					WJets_SB0b_stat_uncert_down.SetBinError(iii, WJets_bin_nom_uncert * (1 - total_bin_stat_uncert/total_bin_nom_value))

				allBR_stat_uncert_up.SetBinContent(iii,(total_bin_stat_uncert/total_bin_nom_value)  )
				allBR_stat_uncert_up.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))
				allBR_stat_uncert_down.SetBinContent(iii, (total_bin_stat_uncert/total_bin_nom_value)  )
				allBR_stat_uncert_down.SetBinError(iii, (total_bin_stat_uncert/total_bin_nom_value))

			self.QCD_linear_SB0b.append([QCD_SB0b_stat_uncert_up, QCD_SB0b_stat_uncert_down])
			self.TTbar_linear_SB0b.append([ TTbar_SB0b_stat_uncert_up, TTbar_SB0b_stat_uncert_down])
			self.ST_linear_SB0b.append([  ST_SB0b_stat_uncert_up, ST_SB0b_stat_uncert_down	 ])
			if self.includeWJets: self.WJets_linear_SB0b.append([  WJets_SB0b_stat_uncert_up, WJets_SB0b_stat_uncert_down	 ])
			if self.includeTTTo: self.TTTo_linear_SB0b.append([  TTTo_SB0b_stat_uncert_up, TTTo_SB0b_stat_uncert_down	 ]) 
			self.all_combined_linear_SB0b.append([ allBR_stat_uncert_up, allBR_stat_uncert_down	  ])


			## kill unecessay histograms
			del QCD_SB0b_stat_uncert_up,  QCD_SB0b_stat_uncert_down, TTbar_SB0b_stat_uncert_up, TTbar_SB0b_stat_uncert_down, ST_SB0b_stat_uncert_up, ST_SB0b_stat_uncert_down, allBR_stat_uncert_up, allBR_stat_uncert_down,WJets_SB0b_stat_uncert_up, WJets_SB0b_stat_uncert_down
			if self.includeWJets: del WJets_SB0b_stat_uncert_up, WJets_SB0b_stat_uncert_down
			if self.includeTTTo:  del TTTo_SB0b_stat_uncert_up, TTTo_SB0b_stat_uncert_down

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
		file_paths  = [ use_filepath+ "%s_%s_%s_processed.root"%(self.mass_point, decay, self.year) for decay in decays   ]

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


				### hist_type here is the decay: open this file and get this single histogram out. Do NOT scale it because this is done later
				
				filepath = use_filepath+ "%s_%s_%s_processed.root"%(self.mass_point, hist_type, self.year)

				#print("TESTING FOR SIGNAL %s: opening file %s"%(hist_type,filepath))
				#try:
				# try to get file and grab histogram from it
				f1 = ROOT.TFile.Open( filepath  ,"r")
				if "topPt" in systematic and "down" in sys_str:
					hist_name = "nom/" + hist_name_signal
				else:
					hist_name = sys_str + "/" + hist_name_signal
				#print("TESTING FOR SIGNAL: hist_name is %s"%(hist_name))
				
				signal_hist = None
				if f1:  signal_hist = f1.Get(hist_name)

				#print("TESTING FOR SIGNAL: unscaled integral is %s for decay %s"%(signal_hist.Integral(), hist_type))
				


				#signal_hist.Scale(sig_weights_dict[hist_type])



				#print("-----TESTING FOR SIGNAL: scaled integral is %s for decay %s"%(signal_hist.Integral(), hist_type))


				# if this doesn't work, append an empty histogram
				#except:
				#	print("ERROR: failed on file %s for %s"%(filepath, sys_str))
				#	signal_hist = ROOT.TH2F("h_MSJ_mass_vs_MdSJ_%s"%(region),"Superjet mass vs diSuperjet mass (%s) (cut-based); diSuperjet mass [GeV];superjet mass"%(region), 22,1250., 10000, 20, 500, 5000) # 375 * 125
				if not signal_hist: 
					if self.doHTdist: signal_hist = ROOT.TH1F("h_totHT_%s"%(region),"Event H_{T} (%s) (%s) (%s); H_{T} [GeV]; Events / 200 GeV"%(region, max(hist_type, "sig"),self.technique_str ),50,0.,10000);
					else: signal_hist = ROOT.TH2F("h_MSJ_mass_vs_MdSJ_%s"%(region),"Superjet mass vs diSuperjet mass (%s) (%s) (%s); diSuperjet mass [GeV];superjet mass"%(region, hist_type,self.technique_str ), 22,1250., 10000, 20, 500, 5000) # 375 * 125

				all_combined_signal_hist.append( signal_hist  )

				"""if hist_type   == "WBWB": all_combined_signal_hist.append( TH2_hist_ST_t_channel_top_5f  )
				elif hist_type == "HTHT": all_combined_signal_hist.append( TH2_hist_ST_t_channel_antitop_5f  )
				elif hist_type == "ZTZT": all_combined_signal_hist.append( TH2_hist_ST_s_channel_4f_hadrons  )
				elif hist_type == "WBHT": all_combined_signal_hist.append( TH2_hist_ST_s_channel_4f_leptons  )
				elif hist_type == "WBZT": all_combined_signal_hist.append( TH2_hist_ST_tW_antitop_5f  )
				elif hist_type == "HTZT": all_combined_signal_hist.append( TH2_hist_ST_tW_top_5f  )"""

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

		use_indices = self.superbin_indices_dict[region]

		if region in ["SR","CR"]: use_region = "SR"
		elif region in ["AT1b","AT0b","AT1tb","AT0tb"]: use_region = "AT1b"   ## THIS IS NOT QUITE RIGHT, WOULD WANT CUSTOM AT1tB REGION INDICES
		elif region in ["SB1b","SB0b"]: use_region = "SB0b"

		if self.doHTdist: use_indices = all_BR_hists.HT_dist_superbins[use_region]
		#elif self.doSideband and region == "SB1b": use_indices = self.superbin_indices_SB1b
		#elif self.doSideband and region == "SB0b": use_indices = self.superbin_indices_SB0b
		#elif region in ["AT1b", "AT0b", "AT1tb", "AT0tb"]:  use_indices = self.superbin_indices_AT
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

		use_indices = self.superbin_indices_dict[region]

		linear_plot_size = len(use_indices)  - mask_size  ## subtract off mask size

		if self.useMask and systematic == "nom":
			print("--- year / region / technique : %s/%s/%s ------ After applying the mask (size = %s bins) to the superbins (original size = %s),  hist has %s bins"%( self.year,region,self.technique_str,mask_size, len(use_indices), linear_plot_size)) 



		#if region in ["SR","CR"]: use_region = "SR"
		#elif region in ["AT1b","AT0b","AT1tb","AT0tb"]: use_region = "AT1b"   ## THIS IS NOT QUITE RIGHT, WOULD WANT CUSTOM AT1tB REGION INDICES
		#elif region in ["SB1b","SB0b"]: use_region = "SB0b"
		use_region = region

		if self.doHTdist: use_indices = all_BR_hists.HT_dist_superbins[use_region]
		#elif self.doSideband and region == "SB1b": use_indices = self.superbin_indices_SB1b
		#elif self.doSideband and region == "SB0b": use_indices = self.superbin_indices_SB0b
		#elif region in ["AT1b", "AT0b", "AT1tb", "AT0tb"]:  use_indices = self.superbin_indices_AT
		for iii,sys_str in enumerate(sys_updown):


			#print("BR_type/sys_str is %s/%s"%(BR_type,sys_str))

			#print("For %s/%s/%s/%s/%s plots created to have %s bins (number of SRCR superbins= %s, number of AT superbins= %s)"%(BR_type, region, systematic,self.year,self.technique_str, linear_plot_size,len(self.superbin_indices),len(self.superbin_indices_AT) ))

			#print("Creating a linearized histogram for %s/%s with %s bins."%(self.year,region,linear_plot_size))
			if forStats:
				if self.doHTdist: linear_plot = ROOT.TH1F("%s%s"%(BR_type,sys_str),"Event H_{T} (%s) (%s) (%s) (UNSCALED); H_{T} [GeV]; Events / 200 GeV"%(region, BR_type, self.technique_str ),linear_plot_size,-0.5,linear_plot_size-0.5)
				else: linear_plot = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s) (UNSCALED); bin; Events / bin"%(BR_type,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
			else:
				if self.doHTdist: linear_plot = ROOT.TH1F("%s%s"%(BR_type,sys_str),"Event H_{T} (%s) (%s) (%s); H_{T} [GeV]; Events / 200 GeV"%(region, BR_type, self.technique_str ),linear_plot_size,-0.5,linear_plot_size-0.5)
				else:  linear_plot = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%(BR_type,region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)

			linear_plot.GetYaxis().SetTitleOffset(1.48)

			num_masked_bins = 0 
			#print("Histogram name is %s."%linear_plot.GetName())
			if hist_type == "QCD":

				if self.use_QCD_Pt:

					if self.doSideband or self.doHTdist or self.doATxtb: continue # didn't implement these, shouldn't need

					SFs_QCDMC_Pt = [  {"2015":72.27560548, "2016":58.13790684, "2017":144.0132837, "2018":208.6671047},
				    {"2015":2.464537119, "2016":2.077524247, "2017":5.087240079, "2018":7.056447936},
				    {"2015":0.2122207081, "2016":0.1770874866, "2017":0.4500561659, "2018":0.6298074855},
				    {"2015":0.04929452011, "2016":0.04041858714, "2017":0.09634485522, "2018":0.1387005244},
				    {"2015":0.01443931658, "2016":0.01169252025, "2017":0.02954986175, "2018":0.04231249731},
				    {"2015":0.007643465954, "2016":0.006312623165, "2017":0.01566430413, "2018":0.0226523112},
				    {"2015":0.001150615273, "2016":0.001016564447, "2017":0.00244639185, "2018":0.003532486979},
				    {"2015":0.000324331737, "2016":0.0002806910428, "2017":0.0006608229592, "2018":0.000952638299},
				    {"2015":0.00003408026676, "2016":0.00003090490169, "2017":0.00007246889556, "2018":0.0001045278212},
				    {"2015":0.000002648864, "2016":0.000002290278112, "2017":0.000005628836, "2018":0.000008118931} ]

					### need to lineraize the histograms separately and THEN add them to linear_plot
					linear_plots_QCD_Pt =  [ROOT.TH1D("%s%s"%("QCDMC_Pt_170to300",sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "QCDMC_Pt_170to300",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_300to470",sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "QCDMC_Pt_300to470",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_470to600",sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%(  "QCDMC_Pt_470to600",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_600to800",sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "QCDMC_Pt_600to800",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_800to1000",sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "QCDMC_Pt_800to1000",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_1000to1400",sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%(  "QCDMC_Pt_1000to1400",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_1400to1800",sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "QCDMC_Pt_1400to1800",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_1800to2400",sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%( "QCDMC_Pt_1800to2400",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_2400to3200",sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%(  "QCDMC_Pt_2400to3200",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_3200toInf",sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%(  "QCDMC_Pt_3200toInf",region,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5) ] 

					for hist in linear_plots_QCD_Pt:
						hist.Sumw2()

					superbin_index = 0
					for superbin_counter,superbin in enumerate(use_indices):
						
						total_counts = [0]*10

						if superbin_counter in bin_mask: 
							num_masked_bins+=1
							continue
						for _tuple in superbin:
							for jjj in range(len(total_counts)):
								total_counts[jjj] +=split_up_hists_for_systematic[jjj][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)


						for jjj in range(len(total_counts)):
							linear_plots_QCD_Pt[jjj].SetBinContent(superbin_index+1,total_counts[jjj])
							linear_plots_QCD_Pt[jjj].SetBinError(superbin_index+1,sqrt(total_counts[jjj]))

						superbin_index+=1
					

					for hist in linear_plots_QCD_Pt:
						hist.Sumw2(); 
					linear_plot.Sumw2(); 

					## scale histograms 
					for jjj in range(len(linear_plots_QCD_Pt)):
						linear_plots_QCD_Pt[jjj].Scale( SFs_QCDMC_Pt[jjj][self.year] )

						### NOW add together with the weight information intact
						linear_plot.Add(linear_plots_QCD_Pt[jjj])

					all_linear_plots.append(linear_plot)


				else: 
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

		# create the directory if it doesn't already exist

		combine_file = ROOT.TFile.Open(combine_file_name,"RECREATE")
		combine_file.cd()

		regions = ["SR","CR","AT1b","AT0b"]
		if self.doATxtb:
			regions.append["AT1tb"]
			regions.append["AT0tb"]
		if self.doSideband:
			regions.append("SB1b")
			regions.append("SB0b")

		QCD_hists	 = [ self.QCD_linear_SR, self.QCD_linear_CR, self.QCD_linear_AT1b, self.QCD_linear_AT0b  ]
		TTbar_hists  = [ self.TTbar_linear_SR, self.TTbar_linear_CR, self.TTbar_linear_AT1b, self.TTbar_linear_AT0b]

		if self.includeWJets: WJets_hists	 = [ self.WJets_linear_SR, self.WJets_linear_CR, self.WJets_linear_AT1b, self.WJets_linear_AT0b  ]
		if self.includeTTTo:  TTTo_hists	 = [ self.TTTo_linear_SR, self.TTTo_linear_CR, self.TTTo_linear_AT1b, self.TTTo_linear_AT0b  ]
		ST_hists	 = [ self.ST_linear_SR, self.ST_linear_CR, self.ST_linear_AT1b, self.ST_linear_AT0b]
		signal_hists = [ self.signal_linear_SR, self.signal_linear_CR, self.signal_linear_AT1b, self.signal_linear_AT0b]
		data_hists   = [ self.data_linear_SR, self.data_linear_CR, self.data_linear_AT1b, self.data_linear_AT0b]

		combined_hists 	   = [ self.combined_linear_SR, self.combined_linear_CR, self.combined_linear_AT1b, self.combined_linear_AT0b ]  ### these are for writing unscaled histograms
		combined_hists_all = [ self.all_combined_linear_SR,self.all_combined_linear_CR, self.all_combined_linear_AT1b, self.all_combined_linear_AT0b]  ### these are for writing fully scaled, combined BR histograms

		if self.doATxtb:
			QCD_hists.extend( [self.QCD_linear_AT1tb, self.QCD_linear_AT0tb]  )
			TTbar_hists.extend([ self.TTbar_linear_AT1tb, self.TTbar_linear_AT0tb])
			ST_hists.extend( [self.ST_linear_AT1tb, self.ST_linear_AT0tb])
			signal_hists.extend([self.signal_linear_AT1tb, self.signal_linear_AT0tb])
			data_hists.extend( [ self.data_linear_AT1tb, self.data_linear_AT0tb])

			if self.includeWJets: WJets_hists.extend( [ self.WJets_linear_AT1tb, self.WJets_linear_AT0tb  ])
			if self.includeTTTo:  TTTo_hists.extend( [ self.TTTo_linear_AT1tb, self.TTTo_linear_AT0tb ])
			combined_hists.extend( [self.combined_linear_AT1tb, self.combined_linear_AT0tb] )
			combined_hists_all.extend( [self.all_combined_linear_AT1tb, self.all_combined_linear_AT0tb])
		if self.doSideband:
			QCD_hists.extend( [self.QCD_linear_SB1b, self.QCD_linear_SB0b]  )
			TTbar_hists.extend([self.TTbar_linear_SB1b, self.TTbar_linear_SB0b]  )
			ST_hists.extend( [self.ST_linear_SB1b, self.ST_linear_SB0b]  )
			signal_hists.extend([self.signal_linear_SB1b, self.signal_linear_SB0b]  )
			data_hists.extend( [self.data_linear_SB1b,self.data_linear_SB0b]  )

			if self.includeWJets: WJets_hists.extend( [ self.WJets_linear_SB1b, self.WJets_linear_SB0b  ])
			if self.includeTTTo:  TTTo_hists.extend( [ self.TTTo_linear_SB1b, self.TTTo_linear_SB0b ])

			combined_hists.extend( [self.combined_linear_SB1b, self.combined_linear_SB0b ]  )
			combined_hists_all.extend( [self.all_combined_linear_SB1b, self.all_combined_linear_SB0b]  )

		if forStats:
			systematics_ = ["nom"]

		if self.createDummyChannel:
			dummyHists = [self.dummy_channel_SR, self.dummy_channel_CR,self.dummy_channel_AT1b, self.dummy_channel_AT0b] 


		max_index = 5
		if self.doSideband: max_index +=2
		if self.doATxtb:    max_index +=2
		for kkk, region in enumerate(regions):

			if kkk > max_index: continue
			### create folder for region
			combine_file.cd()
			ROOT.gDirectory.mkdir(region)
			combine_file.cd(region)

			systematics_ = self.systematic_names[:]
			systematics_.extend( ["stat"]) 

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
						#if systematic == "CMS_scale": print("Writing scale histogram: %s"%(QCD_hists[kkk][iii][jjj].GetName()))

						if "stat" not in systematic:  
							signal_hists[kkk][iii][jjj].Write()
							#if systematic == "CMS_scale": print("Writing scale histogram: %s"%(signal_hists[kkk][iii][jjj].GetName()))

						if "fact" not in systematic and "renorm" not in systematic and "CMS_scale" not in systematic:  
							ST_hists[kkk][iii][jjj].Write()
						if self.includeWJets: 
							WJets_hists[kkk][iii][jjj].Write()
							#if systematic == "CMS_scale": print("Writing scale histogram: %s"%(WJets_hists[kkk][iii][jjj].GetName()))

					TTbar_hists[kkk][iii][jjj].Write()
					#if systematic == "CMS_scale": print("Writing scale histogram: %s"%(TTbar_hists[kkk][iii][jjj].GetName()))

					if self.includeTTTo: 
						TTTo_hists[kkk][iii][jjj].Write()
						#if systematic == "CMS_scale": print("Writing scale histogram: %s"%(TTTo_hists[kkk][iii][jjj].GetName()))
					if not forStats:
						combined_hists_all[kkk][iii][jjj].Write()
						#f systematic == "CMS_scale": print("Writing scale histogram: %s"%(combined_hists_all[kkk][iii][jjj].GetName()))
					
					if self.createDummyChannel and not forStats:
						#print("ABOUT TO WRITE DUMMY CHANNEL:")
						#print("kkk/iii/jjj is %s/%s/%s"%(kkk,iii,jjj))
						#print("dummyHists has size (number of regions) %s"%len(dummyHists[kkk]))
						#print("dummyHists[%s] has size (number of systematics) %s"%(kkk,  len(dummyHists[kkk]))  )
 						#print("dummyHists[%s][%s] has size (number of systematics) %s"%(kkk, iii, len(dummyHists[kkk][iii]))  )

 						#print("Meanwhile, for the QCD linearized hists - ")
 						#print("QCD_hists has size (number of regions) %s"%len(QCD_hists[kkk]))
						#print("QCD_hists[%s] has size (number of systematics) %s"%(kkk,  len(QCD_hists[kkk]))  )
 						#print("QCD_hists[%s][%s] has size (number of systematics) %s"%(kkk, iii, len(QCD_hists[kkk][iii]))  )

						if kkk < 4:  ## didn't bother to make these regions outside SR/CR/AT1b/AT0b
							#print("Passed k < 4 ")
							dummyHists[kkk][iii][jjj].Write()
							#print("Wrote dummyHists[kkk][iii][jjj], %s/%s/%s"%(kkk,iii,jjj))




			systematics_ = self.data_systematics[:]
			if forStats:
				systematics_ = ["nom"]

			for iii,systematic in enumerate(systematics_):

				sys_suffix = [""]
				if systematic == "nom":
					sys_updown = ["nom"]
				elif systematic == "topPt":
					sys_updown = ["%s_up"%systematic]
				else:
					sys_updown = ["%s_up"%systematic,"%s_down"%systematic]

				for jjj,sys_str in enumerate(sys_updown):
					data_hists[kkk][iii][jjj].Write()

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

	def load_superbin_indices(self,region, true_region):	
	# load in the superbin indices (located in a text file ), true region means the actual region this represents, not the region whose bin map is used
		_superbin_indices = []
		open_file = open(self.index_file_home+"/%s_superbin_indices%s_%s.txt"%(self.use_QCD_Pt_str, self.technique_str,self.year),"r")
		for line in open_file:
			columns = line.split('/')
			if columns[0] == self.year and columns[1] == region:
				_superbin_indices = columns[3]
				break
		open_file.close()


		superbins = ast.literal_eval(_superbin_indices)
		
		if output_map_file and mass_point == "Suu4_chi1":   # only want to do this once per region / year
			print("writing actual superbin indices for %s/%s/%s to text file."%(self.year,region,self.technique_str))
			output_map_file.write("%s/%s/%s/number of superbins=%s/%s\n"%(self.year,true_region,self.technique_str, len(superbins), superbins))

		return superbins


	def load_bin_masks(self,region):	# load in the superbin indices (located in a text file )
		_superbin_indices = []
		bin_map_path         = "region_masks/"
		open_file = open(bin_map_path+"/%s_bin_masks_%s.txt"%(self.use_QCD_Pt_str, year),"r")

		if self.debug: print("Loading bin mask %s for year / region / technique %s/%s/%s:"%(bin_map_path+"/bin_masks_%s.txt"%(year), self.year, region, self.technique_str ))

		#print("Got superbin index file %s."%( bin_map_path+"/superbin_indices%s_%s.txt"%(technique_str,year)  ))
		if self.debug: print("Bin mask:    ")
		for line in open_file:
			columns = line.split('/')
			if columns[0] == self.year and columns[1] == region and columns[2] == self.technique_str:
				_superbin_indices = columns[3]
				if self.debug: print("%s"%line)
		open_file.close()
		return ast.literal_eval(_superbin_indices)


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
		self.signal_WBHT_hist_AT1b,self.signal_WBZT_hist_AT1b,self.signal_HTZT_hist_AT1b,self.signal_WBWB_hist_CR,self.signal_HTHT_hist_CR,self.signal_ZTZT_hist_CR,self.signal_WBHT_hist_CR,self.signal_WBZT_hist_CR,self.signal_HTZT_hist_CR,
		self.signal_WBWB_hist_SR,self.signal_HTHT_hist_SR,self.signal_ZTZT_hist_SR,self.signal_WBHT_hist_SR,self.signal_WBZT_hist_SR,self.signal_HTZT_hist_SR] 
		if self.doSideband: signal_hists.extend(  [    self.signal_WBWB_hist_SB0b,self.signal_HTHT_hist_SB0b,self.signal_ZTZT_hist_SB0b,self.signal_WBHT_hist_SB0b,self.signal_WBZT_hist_SB0b,
			self.signal_HTZT_hist_SB0b,self.signal_WBWB_hist_SB1b,self.signal_HTHT_hist_SB1b,self.signal_ZTZT_hist_SB1b,self.signal_WBHT_hist_SB1b,self.signal_WBZT_hist_SB1b,self.signal_HTZT_hist_SB1b ])
		if self.doATxtb:signal_hists.extend( [ self.signal_WBWB_hist_AT0tb,self.signal_HTHT_hist_AT0tb,self.signal_ZTZT_hist_AT0tb,self.signal_WBHT_hist_AT0tb,self.signal_WBZT_hist_AT0tb,self.signal_HTZT_hist_AT0tb,
			self.signal_WBWB_hist_AT1tb, self.signal_HTHT_hist_AT1tb,self.signal_ZTZT_hist_AT1tb,self.signal_WBHT_hist_AT1tb,self.signal_WBZT_hist_AT1tb,self.signal_HTZT_hist_AT1tb]   )
		for hist_list in signal_hists:
			for hist in hist_list:
				del hist

		return

	def create_directories(self):

		dirs_to_create = [ self.output_file_home , self.final_plot_home    ]

		for dir_to_create in dirs_to_create:
			if not os.path.exists(dir_to_create):
				print("Creating directory %s."%(dir_to_create))
				os.makedirs(dir_to_create)

if __name__=="__main__":
	start_time = time.time()

	##################################################
	##############  Options to change  ###############
	##################################################
	debug 					 = False

	doHTdist   				 = False
	doSideband 				 = False
	doATxtb	   				 = False
	run_from_eos			 = True
	createDummyChannel 		 = False

	includeTTJets800to1200 	 = True
	includeTTTo              = True
	includeWJets             = True

	usMask        			 = False  
	use_1b_bin_maps 	     = True


	runCorrected			 = False # use the "corrected" versions of the uncertainties stored in processedFilesCorrected, these have the fixed scale and pdf uncertainties for QCDPT

	##################################################
	##################################################
	##################################################
	# get input year
	parser = argparse.ArgumentParser(description="Linearize 2D histograms in order to reach a minimum stat uncertainty and scaled/unscaled bin yield. ")
	parser.add_argument("-y", "--year", type=str, required=True, help="Input year on which to run. Use 'All' for all Run years.")
	parser.add_argument( "--doHTdist",   default=False, action='store_true', required=False, help="Option to run on HT distributions instead of 2D plots.")
	parser.add_argument( "--doSideband",  default=False, action='store_true',  required=False, help="Option to run the sideband region (in addition to normal regions).")
	parser.add_argument( "--doATxtb",   default=False, action='store_true', required=False, help="Option to run over the AT1tb and AT0tb regions (in addition to normal regions).")

	args = parser.parse_args()
	

	mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1","Suu5_chi1p5","Suu5_chi2","Suu6_chi1","Suu6_chi1p5","Suu6_chi2","Suu6_chi2p5","Suu7_chi1",
   "Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3","Suu8_chi1","Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"]

	print("doHTdist is %s."%doHTdist)

	if debug:
		mass_points = ["Suu4_chi1"]

	technique_strs  = ["","NN_"] 
	technique_descr = ["cut-based", "NN-based"]

	technique_strs  = [""] 
	technique_descr = ["cut-based"]

	use_QCD_Pt_opts = [True,False]
	use_QCD_Pt_strs = ["QCDPT","QCDHT"]

	if args.year == "all" or args.year == "All" or args.year == "ALL":
		years = ["2015","2016","2017","2018"]
	else:
		years = [args.year]

	for year in years:

		print("=============== Running for %s ===============."%year)

		for jjj,use_QCD_Pt in enumerate(use_QCD_Pt_opts):

			#remove the old "used binMap" file 
			if not doHTdist:   ## write out the bin maps that are actually used
				output_map_file_name = "binMaps/actual/%s_used_superbin_indices_%s.txt"%(use_QCD_Pt_strs[jjj],  year) # meaning the ACTUAL bin maps used in merging (for verification)
				if os.path.exists(output_map_file_name):
				    os.remove(output_map_file_name)
				    print("Deleted:", output_map_file_name)
				output_map_file = open(output_map_file_name,"w")  
				output_map_file.write("##### THESE ARE THE SUPERBINS THAT ARE ACTUALLY USED IN MERGING. THIS IS SOLELY FOR VERIFICATION \n")
			else: output_map_file = None
			for iii,technique_str in enumerate(technique_strs):

				if doHTdist and "NN" in technique_str: continue 

				# create instance of hist_loader (containing all BR histograms) for the year + technique str combination
				all_BR_hists  = hist_loader(year, technique_str, use_QCD_Pt, doHTdist, doSideband, doATxtb, includeTTJets800to1200, includeTTTo, includeWJets, run_from_eos, runCorrected, None)

				for mass_point in mass_points:
					#try:

					print("Running for %s/%s/%s/useQCDPT = %s"%(year,mass_point,technique_descr[iii],use_QCD_Pt_strs[jjj] ))
					if usMask: final_plot = linearized_plot(year, mass_point, technique_str, all_BR_hists, output_map_file,use_QCD_Pt, True, use_1b_bin_maps, createDummyChannel,run_from_eos, runCorrected, debug)   ### run with masked bins
					else: final_plot = linearized_plot(year, mass_point, technique_str, all_BR_hists, output_map_file, use_QCD_Pt, False, use_1b_bin_maps ,createDummyChannel,run_from_eos, runCorrected, debug)	### run without masked bins

					# write out the "effective" bin maps = bin maps that are actually being used, to binMaps/ 

					#except:
					#	print("Failed for %s/%s/%s"%(year,mass_point,technique_descr[iii]))
					del final_plot
				all_BR_hists.kill_histograms()
				del all_BR_hists  # free up a lot of memory 
			output_map_file.close()
			print("Script took %ss to run."%(	np.round(time.time() - start_time,4 )) )
