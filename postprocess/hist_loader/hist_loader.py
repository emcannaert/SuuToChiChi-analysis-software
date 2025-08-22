import sys,os,time
import numpy as np
import ROOT
import ast
from math import sqrt
from write_cms_text import write_cms_text
import argparse
from return_BR_SF.return_BR_SF import return_BR_SF
import random

from math import isnan

ROOT.gErrorIgnoreLevel = ROOT.kError

class hist_loader:

	ROOT.TH1.SetDefaultSumw2()
	ROOT.TH2.SetDefaultSumw2()

	def __init__(self, year, technique_str, use_QCD_Pt = False, doHTdist = False, doSideband = False, doATxtb = False, includeTTJets800to1200 = False, includeTTTo = False, includeWJets = False, run_from_eos = False, WP=None):

		self.c = ROOT.TCanvas("","",1200,1000)
		self.BR_SF_scale = 1.0
		self.technique_str = technique_str
		self.year   = year
		self.run_from_eos = run_from_eos
		self.WP = WP 
		self.WP_str = ""
		self.use_QCD_Pt = use_QCD_Pt
		if self.WP: 

			
			if "AT" in self.WP: 
				self.WP_folder = self.WP[2:]
			else:
				self.WP = "WP" + self.WP
				self.WP_folder = self.WP

			self.WP_str = self.WP + "_"

		self.MC_root_file_home	  = 	os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFiles/"
		self.data_root_file_home	=   os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFiles/"

		self.eos_path = "root://cmseos.fnal.gov/"

		self.HT_distr_home = "HT_distributions/" # extra folder where output files are saved for HT distribution plots

		if self.WP:
			self.MC_root_file_home	    = "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/ATWP_study/%s/"%self.WP_folder
			self.data_root_file_home	=  "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/ATWP_study/%s/"%self.WP_folder



		if self.run_from_eos:
			self.MC_root_file_home	    =  self.eos_path + "/store/user/ecannaer/processedFiles/"
			self.data_root_file_home	=  self.eos_path + "/store/user/ecannaer/processedFiles/"

			if self.WP:
				self.MC_root_file_home	    =  self.eos_path + "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/ATWP_study/%s/"%self.WP_folder
				self.data_root_file_home	=  self.eos_path + "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/ATWP_study/%s/"%self.WP_folder



		## region options
		self.doSideband = doSideband
		self.doATxtb = doATxtb
		self.doHTdist = doHTdist    # use an HT distribution as the "final" distribution. Don't want to do the linearization process in this case
		if self.doSideband: self.doHTdist = False

		self.final_hist_name = "h_MSJ_mass_vs_MdSJ"
		if self.doHTdist: 
			self.final_hist_name = "h_totHT"
			self.final_hist_title = "Event H_{T}"

		### sample inclusion options
		self.includeWJets = includeWJets
		self.includeTTTo  = includeTTTo
		self.includeTTJets800to1200 = includeTTJets800to1200
		if "NN" in self.technique_str: self.doSideband = False

		self.index_file_home	 = os.getenv('CMSSW_BASE') + "/src/postprocess/binMaps/"
		self.output_file_home	= os.getenv('CMSSW_BASE') + "/src/postprocess/finalCombineFilesNewStats"
		self.final_plot_home	 = os.getenv('CMSSW_BASE') + "/src/postprocess/plots/finalCombinePlots"
		

		if self.WP:
			self.index_file_home	 = os.getenv('CMSSW_BASE') + "/src/postprocess/binMaps/WPStudy/%s/"%WP
			self.output_file_home	= os.getenv('CMSSW_BASE') + "/src/postprocess/finalCombineFilesNewStats/WPStudy/%s/"%WP
			self.final_plot_home	 = os.getenv('CMSSW_BASE') + "/src/postprocess/plots/finalCombinePlots/WPStudy/%s/"%WP


		self.data_systematics 	   = ["nom"]
		self.data_systematic_names = ["nom"]

		self.systematics 	  = ["nom",   "bTagSF_med",   "bTagSF_tight",     "bTagSF_med_corr",   "bTagSF_tight_corr",   "JER",	 "JEC",    "bTag_eventWeight_bc_T_corr", "bTag_eventWeight_light_T_corr", "bTag_eventWeight_bc_M_corr", "bTag_eventWeight_light_M_corr", "bTag_eventWeight_bc_T_year", "bTag_eventWeight_light_T_year", "bTag_eventWeight_bc_M_year", "bTag_eventWeight_light_M_year",		"JER_eta193",	 "JER_193eta25",	  "JEC_FlavorQCD",	"JEC_RelativeBal",		    "JEC_Absolute",	   "JEC_BBEC1_year",	 "JEC_Absolute_year",	  "JEC_RelativeSample_year",	 "PUSF",	 "topPt",	 "L1Prefiring",	     "pdf",	     "renorm",	  "fact",	  "JEC_AbsoluteCal",	  "JEC_AbsoluteTheory",        "JEC_AbsolutePU",	   "JEC_AbsoluteScale",		  "JEC_Fragmentation",	    "JEC_AbsoluteMPFBias",	   "JEC_RelativeFSR",       "scale"]   ## systematic namings as used in analyzer	 "bTagSF",   
		self.systematic_names = ["nom",  "CMS_bTagSF_M" , "CMS_bTagSF_T",    "CMS_bTagSF_M_corr" , "CMS_bTagSF_T_corr", "CMS_jer", "CMS_jec",   "CMS_bTagSF_bc_T_corr",	   "CMS_bTagSF_light_T_corr",	   "CMS_bTagSF_bc_M_corr",	   "CMS_bTagSF_light_M_corr",	  "CMS_bTagSF_bc_T_year",		"CMS_bTagSF_light_T_year",	  "CMS_bTagSF_bc_M_year",	   "CMS_bTagSF_light_M_year",		 "CMS_jer_eta193", "CMS_jer_193eta25",  "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal",   "CMS_jec_Absolute", "CMS_jec_BBEC1_year",	           "CMS_jec_Absolute_year",  "CMS_jec_RelativeSample_year", "CMS_pu", "CMS_topPt", "CMS_L1Prefiring",   "CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory",    "CMS_jec_AbsolutePU",   "CMS_jec_AbsoluteScale" ,   "CMS_jec_Fragmentation" , "CMS_jec_AbsoluteMPFBias",  "CMS_jec_RelativeFSR",  "CMS_scale"]  ## systematic namings for cards   "CMS_btagSF", 

		self.uncorrelated_systematics = ["CMS_jec", "CMS_jer","CMS_jer_eta193", "CMS_jer_193eta25", "CMS_L1Prefiring","CMS_bTagSF_M", "CMS_bTagSF_T", "CMS_bTagSF_bc_T_year", "CMS_bTagSF_light_T_year", "CMS_bTagSF_bc_M_year","CMS_bTagSF_light_M_year", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year", "CMS_jec_RelativeSample_year"] ## systematics that are correlated (will not have year appended to names)	 "CMS_btagSF",


		if self.WP:
			self.systematics 	  = ["nom"]   ## systematic namings as used in analyzer	 "bTagSF",   
			self.systematic_names = ["nom",  "CMS_bTagSF_M" , "CMS_bTagSF_T",    "CMS_bTagSF_M_corr" , "CMS_bTagSF_T_corr", "CMS_jer", "CMS_jec",   "CMS_bTagSF_bc_T_corr",	   "CMS_bTagSF_light_T_corr",	   "CMS_bTagSF_bc_M_corr",	   "CMS_bTagSF_light_M_corr",	  "CMS_bTagSF_bc_T_year",		"CMS_bTagSF_light_T_year",	  "CMS_bTagSF_bc_M_year",	   "CMS_bTagSF_light_M_year",		 "CMS_jer_eta193", "CMS_jer_193eta25",  "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal",   "CMS_jec_Absolute", "CMS_jec_BBEC1_year",	           "CMS_jec_Absolute_year",  "CMS_jec_RelativeSample_year", "CMS_pu", "CMS_topPt", "CMS_L1Prefiring",   "CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory",    "CMS_jec_AbsolutePU",   "CMS_jec_AbsoluteScale" ,   "CMS_jec_Fragmentation" , "CMS_jec_AbsoluteMPFBias",  "CMS_jec_RelativeFSR",  "CMS_scale"]  ## systematic namings for cards   "CMS_btagSF", 


		if self.WP:
			self.systematics 	  = ["nom"]   
			self.systematic_names = ["nom"] 




		### HT bin stuff
		self.HT_dist_superbins =   {"SR": [], "AT1b": [], "SB1b": [] }    ### these will store the HT superbins (bins that are merged to guarantee some minimum stat uncertainty)
		self.HT_dist_min_stat_uncert = 0.30  ## = 20% bin stat uncertainty



		### individual bins for SR

		if self.use_QCD_Pt:
			self.QCDMC_Pt_170to300_hist_SR 	= []
			self.QCDMC_Pt_300to470_hist_SR 	= []
			self.QCDMC_Pt_470to600_hist_SR 	= []
			self.QCDMC_Pt_600to800_hist_SR 	= []
			self.QCDMC_Pt_800to1000_hist_SR 	= []
			self.QCDMC_Pt_1000to1400_hist_SR 	= []
			self.QCDMC_Pt_1400to1800_hist_SR 	= []
			self.QCDMC_Pt_1800to2400_hist_SR 	= []
			self.QCDMC_Pt_2400to3200_hist_SR 	= []
			self.QCDMC_Pt_3200toInf_hist_SR 	= []


		else:

			self.QCD1000to1500_hist_SR 	= []
			self.QCD1500to2000_hist_SR 	= []
			self.QCD2000toInf_hist_SR 	= []






		self.TTJets1200to2500_hist_SR 	= []
		self.TTJets2500toInf_hist_SR 	= []

		self.ST_t_channel_top_hist_SR 		= []
		self.ST_t_channel_antitop_hist_SR 	= []
		self.ST_s_channel_hadrons_hist_SR 	= []
		self.ST_s_channel_leptons_hist_SR 	= []  
		self.ST_tW_antitop_hist_SR 			= []
		self.ST_tW_top_hist_SR 				= []

		if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_SR 		= []
		if self.includeTTTo:
			self.TTToHadronicMC_SR 				= []
			self.TTToSemiLeptonicMC_SR 			= []
			self.TTToLeptonicMC_SR 				= []

		if self.includeWJets:
			self.WJetsMC_LNu_HT800to1200_SR 	= []
			self.WJetsMC_LNu_HT1200to2500_SR 	= []
			self.WJetsMC_LNu_HT2500toInf_SR 	= []
			self.WJetsMC_QQ_HT800toInf_SR 		= []

		### individual bins for CR
		if self.use_QCD_Pt:
			self.QCDMC_Pt_170to300_hist_CR 	= []
			self.QCDMC_Pt_300to470_hist_CR 	= []
			self.QCDMC_Pt_470to600_hist_CR 	= []
			self.QCDMC_Pt_600to800_hist_CR 	= []
			self.QCDMC_Pt_800to1000_hist_CR 	= []
			self.QCDMC_Pt_1000to1400_hist_CR 	= []
			self.QCDMC_Pt_1400to1800_hist_CR 	= []
			self.QCDMC_Pt_1800to2400_hist_CR 	= []
			self.QCDMC_Pt_2400to3200_hist_CR 	= []
			self.QCDMC_Pt_3200toInf_hist_CR 	= []

		else:

			self.QCD1000to1500_hist_CR 	= []
			self.QCD1500to2000_hist_CR 	= []
			self.QCD2000toInf_hist_CR 	= []

		self.TTJets1200to2500_hist_CR 	= []
		self.TTJets2500toInf_hist_CR 	= []

		self.ST_t_channel_top_hist_CR 		= []
		self.ST_t_channel_antitop_hist_CR 	= []
		self.ST_s_channel_hadrons_hist_CR 	= []
		self.ST_s_channel_leptons_hist_CR 	= []  
		self.ST_tW_antitop_hist_CR 			= []
		self.ST_tW_top_hist_CR 				= []

		if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_CR 		= []
		if self.includeTTTo:
			self.TTToHadronicMC_CR 				= []
			self.TTToSemiLeptonicMC_CR 			= []
			self.TTToLeptonicMC_CR 				= []

		if self.includeWJets:
			self.WJetsMC_LNu_HT800to1200_CR 	= []
			self.WJetsMC_LNu_HT1200to2500_CR 	= []
			self.WJetsMC_LNu_HT2500toInf_CR 	= []
			self.WJetsMC_QQ_HT800toInf_CR 		= []


		### individual bins for AT1b

		if self.use_QCD_Pt:
			self.QCDMC_Pt_170to300_hist_AT1b 	= []
			self.QCDMC_Pt_300to470_hist_AT1b 	= []
			self.QCDMC_Pt_470to600_hist_AT1b 	= []
			self.QCDMC_Pt_600to800_hist_AT1b 	= []
			self.QCDMC_Pt_800to1000_hist_AT1b 	= []
			self.QCDMC_Pt_1000to1400_hist_AT1b 	= []
			self.QCDMC_Pt_1400to1800_hist_AT1b 	= []
			self.QCDMC_Pt_1800to2400_hist_AT1b 	= []
			self.QCDMC_Pt_2400to3200_hist_AT1b 	= []
			self.QCDMC_Pt_3200toInf_hist_AT1b 	= []


		else:

			self.QCD1000to1500_hist_AT1b 	= []
			self.QCD1500to2000_hist_AT1b 	= []
			self.QCD2000toInf_hist_AT1b 	= []

		self.TTJets1200to2500_hist_AT1b 	= []
		self.TTJets2500toInf_hist_AT1b 	= []

		self.ST_t_channel_top_hist_AT1b 		= []
		self.ST_t_channel_antitop_hist_AT1b 	= []
		self.ST_s_channel_hadrons_hist_AT1b 	= []
		self.ST_s_channel_leptons_hist_AT1b 	= []  
		self.ST_tW_antitop_hist_AT1b 			= []
		self.ST_tW_top_hist_AT1b 				= []

		if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_AT1b 		= []
		if self.includeTTTo:
			self.TTToHadronicMC_AT1b 				= []
			self.TTToSemiLeptonicMC_AT1b 			= []
			self.TTToLeptonicMC_AT1b 				= []

		if self.includeWJets:
			self.WJetsMC_LNu_HT800to1200_AT1b 	= []
			self.WJetsMC_LNu_HT1200to2500_AT1b 	= []
			self.WJetsMC_LNu_HT2500toInf_AT1b 	= []
			self.WJetsMC_QQ_HT800toInf_AT1b 		= []

		### individual bins for AT0b

		if self.use_QCD_Pt:
			self.QCDMC_Pt_170to300_hist_AT0b 	= []
			self.QCDMC_Pt_300to470_hist_AT0b 	= []
			self.QCDMC_Pt_470to600_hist_AT0b 	= []
			self.QCDMC_Pt_600to800_hist_AT0b 	= []
			self.QCDMC_Pt_800to1000_hist_AT0b 	= []
			self.QCDMC_Pt_1000to1400_hist_AT0b 	= []
			self.QCDMC_Pt_1400to1800_hist_AT0b 	= []
			self.QCDMC_Pt_1800to2400_hist_AT0b 	= []
			self.QCDMC_Pt_2400to3200_hist_AT0b 	= []
			self.QCDMC_Pt_3200toInf_hist_AT0b 	= []


		else:

			self.QCD1000to1500_hist_AT0b 	= []
			self.QCD1500to2000_hist_AT0b 	= []
			self.QCD2000toInf_hist_AT0b 	= []
		self.TTJets1200to2500_hist_AT0b 	= []
		self.TTJets2500toInf_hist_AT0b 	= []

		self.ST_t_channel_top_hist_AT0b 		= []
		self.ST_t_channel_antitop_hist_AT0b 	= []
		self.ST_s_channel_hadrons_hist_AT0b 	= []
		self.ST_s_channel_leptons_hist_AT0b 	= []  
		self.ST_tW_antitop_hist_AT0b 			= []
		self.ST_tW_top_hist_AT0b 				= []

		if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_AT0b 		= []
		if self.includeTTTo:
			self.TTToHadronicMC_AT0b 				= []
			self.TTToSemiLeptonicMC_AT0b 			= []
			self.TTToLeptonicMC_AT0b 				= []

		if self.includeWJets:
			self.WJetsMC_LNu_HT800to1200_AT0b 	= []
			self.WJetsMC_LNu_HT1200to2500_AT0b 	= []
			self.WJetsMC_LNu_HT2500toInf_AT0b 	= []
			self.WJetsMC_QQ_HT800toInf_AT0b 		= []

		if self.doATxtb:
			### individual bins for AT0tb

			self.QCD1000to1500_hist_AT0tb 	= []
			self.QCD1500to2000_hist_AT0tb 	= []
			self.QCD2000toInf_hist_AT0tb 	= []

			self.TTJets1200to2500_hist_AT0tb 	= []
			self.TTJets2500toInf_hist_AT0tb 	= []

			self.ST_t_channel_top_hist_AT0tb 		= []
			self.ST_t_channel_antitop_hist_AT0tb 	= []
			self.ST_s_channel_hadrons_hist_AT0tb 	= []
			self.ST_s_channel_leptons_hist_AT0tb 	= []  
			self.ST_tW_antitop_hist_AT0tb 			= []
			self.ST_tW_top_hist_AT0tb 				= []

			if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_AT0tb 		= []
			if self.includeTTTo:
				self.TTToHadronicMC_AT0tb 				= []
				self.TTToSemiLeptonicMC_AT0tb 			= []
				self.TTToLeptonicMC_AT0tb 				= []

			if self.includeWJets:
				self.WJetsMC_LNu_HT800to1200_AT0tb 	= []
				self.WJetsMC_LNu_HT1200to2500_AT0tb 	= []
				self.WJetsMC_LNu_HT2500toInf_AT0tb 	= []
				self.WJetsMC_QQ_HT800toInf_AT0tb 		= []

			### individual bins for AT1tb
			self.QCD1000to1500_hist_AT1tb 	= []
			self.QCD1500to2000_hist_AT1tb 	= []
			self.QCD2000toInf_hist_AT1tb 	= []

			self.TTJets1200to2500_hist_AT1tb 	= []
			self.TTJets2500toInf_hist_AT1tb 	= []

			self.ST_t_channel_top_hist_AT1tb 		= []
			self.ST_t_channel_antitop_hist_AT1tb 	= []
			self.ST_s_channel_hadrons_hist_AT1tb 	= []
			self.ST_s_channel_leptons_hist_AT1tb 	= []  
			self.ST_tW_antitop_hist_AT1tb 			= []
			self.ST_tW_top_hist_AT1tb 				= []

			if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_AT1tb 		= []
			if self.includeTTTo:
				self.TTToHadronicMC_AT1tb 				= []
				self.TTToSemiLeptonicMC_AT1tb 			= []
				self.TTToLeptonicMC_AT1tb 				= []

			if self.includeWJets:
				self.WJetsMC_LNu_HT800to1200_AT1tb 	= []
				self.WJetsMC_LNu_HT1200to2500_AT1tb 	= []
				self.WJetsMC_LNu_HT2500toInf_AT1tb 	= []
				self.WJetsMC_QQ_HT800toInf_AT1tb 		= []

		### individual bins for SB1b
		if self.doSideband:
			self.QCD1000to1500_hist_SB1b 	= []
			self.QCD1500to2000_hist_SB1b 	= []
			self.QCD2000toInf_hist_SB1b 	= []


			self.TTJets800to1200_hist_SB1b 	= []
			self.TTJets1200to2500_hist_SB1b 	= []

			self.ST_t_channel_top_hist_SB1b 		= []
			self.ST_t_channel_antitop_hist_SB1b 	= []
			self.ST_s_channel_hadrons_hist_SB1b 	= []
			self.ST_s_channel_leptons_hist_SB1b 	= []  
			self.ST_tW_antitop_hist_SB1b 			= []
			self.ST_tW_top_hist_SB1b 				= []

			if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_SB1b 		= []
			if self.includeTTTo:
				self.TTToHadronicMC_SB1b 				= []
				self.TTToSemiLeptonicMC_SB1b 			= []
				self.TTToLeptonicMC_SB1b 				= []

			if self.includeWJets:
				self.WJetsMC_LNu_HT800to1200_SB1b 	= []
				self.WJetsMC_LNu_HT1200to2500_SB1b 	= []
				self.WJetsMC_LNu_HT2500toInf_SB1b 	= []
				self.WJetsMC_QQ_HT800toInf_SB1b 		= []


			### individual bins for SB0b

			self.QCD1000to1500_hist_SB0b 	= []
			self.QCD1500to2000_hist_SB0b 	= []
			self.QCD2000toInf_hist_SB0b 	= []

			self.TTJets800to1200_hist_SB0b 	= []
			self.TTJets1200to2500_hist_SB0b 	= []

			self.ST_t_channel_top_hist_SB0b 		= []
			self.ST_t_channel_antitop_hist_SB0b 	= []
			self.ST_s_channel_hadrons_hist_SB0b 	= []
			self.ST_s_channel_leptons_hist_SB0b 	= []  
			self.ST_tW_antitop_hist_SB0b 			= []
			self.ST_tW_top_hist_SB0b 				= []

			if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_SB0b 		= []
			if self.includeTTTo:
				self.TTToHadronicMC_SB0b 				= []
				self.TTToSemiLeptonicMC_SB0b 			= []
				self.TTToLeptonicMC_SB0b 				= []

			if self.includeWJets:
				self.WJetsMC_LNu_HT800to1200_SB0b 	= []
				self.WJetsMC_LNu_HT1200to2500_SB0b 	= []
				self.WJetsMC_LNu_HT2500toInf_SB0b 	= []
				self.WJetsMC_QQ_HT800toInf_SB0b 		= []

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
			self.combined_linear_AT0tb   = []
			self.data_hist_AT0tb  	= []
			self.data_hist_AT1tb  	= []
		if self.doSideband:
			self.combined_linear_SB1b   = []
			self.combined_linear_SB0b   = []
			self.data_hist_SB1b  	= []
			self.data_hist_SB0b  	= []

		self.data_hist_SR 	= []
		self.data_hist_CR 	= []
		self.data_hist_AT0b  	= []
		self.data_hist_AT1b  	= []


		print("Loading data and background histograms.")
		doExtras = False

		for systematic in self.systematics:

			#####  INDIVIDUAL MC HISTOGRAMS
			## sideband Absolute JEC uncertainty names are currently different (change this when they are not)
			systematic_SB = systematic
			if systematic in ["Absolute", "AbsolutePU", "AbsoluteCal","AbsoluteTheory"] :
				systematic_SB = "JEC_" + systematic_SB	
			### SR
			
			#if systematic == "CMS_scale": print("Loading scale histograms.")

			if self.use_QCD_Pt:
				self.QCDMC_Pt_170to300_hist_SR.append(self.load_QCD_hists("SR",systematic,False,"QCDMC_Pt_170to300"))
				self.QCDMC_Pt_300to470_hist_SR.append(self.load_QCD_hists("SR",systematic,False,"QCDMC_Pt_300to470"))
				self.QCDMC_Pt_470to600_hist_SR.append(self.load_QCD_hists("SR",systematic,False,"QCDMC_Pt_470to600"))
				self.QCDMC_Pt_600to800_hist_SR.append(self.load_QCD_hists("SR",systematic,False,"QCDMC_Pt_600to800"))
				self.QCDMC_Pt_800to1000_hist_SR.append(self.load_QCD_hists("SR",systematic,False,"QCDMC_Pt_800to1000"))
				self.QCDMC_Pt_1000to1400_hist_SR.append(self.load_QCD_hists("SR",systematic,False,"QCDMC_Pt_1000to1400"))
				self.QCDMC_Pt_1400to1800_hist_SR.append(self.load_QCD_hists("SR",systematic,False,"QCDMC_Pt_1400to1800"))
				self.QCDMC_Pt_1800to2400_hist_SR.append(self.load_QCD_hists("SR",systematic,False,"QCDMC_Pt_1800to2400"))
				self.QCDMC_Pt_2400to3200_hist_SR.append(self.load_QCD_hists("SR",systematic,False,"QCDMC_Pt_2400to3200"))
				self.QCDMC_Pt_3200toInf_hist_SR.append(self.load_QCD_hists("SR",systematic,False,"QCDMC_Pt_3200toInf"))
			else:
				self.QCD1000to1500_hist_SR.append(self.load_QCD_hists("SR",systematic,False,"QCDMC1000to1500"))
				self.QCD1500to2000_hist_SR.append(self.load_QCD_hists("SR",systematic,False,"QCDMC1500to2000"))
				self.QCD2000toInf_hist_SR.append(self.load_QCD_hists("SR",systematic,False,"QCDMC2000toInf"))

			self.TTJets1200to2500_hist_SR.append(self.load_ttbar_hist("SR",systematic,False,"TTJetsMCHT1200to2500"))
			self.TTJets2500toInf_hist_SR.append(self.load_ttbar_hist("SR",systematic,False, "TTJetsMCHT2500toInf"))

			self.ST_t_channel_top_hist_SR.append(self.load_ST_hists("SR",systematic,False,"ST_t-channel-top_inclMC" ))
			self.ST_t_channel_antitop_hist_SR.append(self.load_ST_hists("SR",systematic, False,"ST_t-channel-antitop_inclMC"))
			self.ST_s_channel_hadrons_hist_SR.append(self.load_ST_hists("SR",systematic, False, "ST_s-channel-hadronsMC"))
			self.ST_s_channel_leptons_hist_SR.append(self.load_ST_hists("SR",systematic, False, "ST_s-channel-leptonsMC"))
			self.ST_tW_antitop_hist_SR.append(self.load_ST_hists("SR",systematic, False, "ST_tW-antiTop_inclMC"))
			self.ST_tW_top_hist_SR.append(self.load_ST_hists("SR",systematic, False, "ST_tW-top_inclMC"))


			if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_SR.append(self.load_ttbar_hist("SR",systematic,False,"TTJetsMCHT800to1200" ))
			if self.includeTTTo:
				self.TTToHadronicMC_SR.append(self.load_TTTo_hists("SR",systematic, False,"TTToHadronicMC"))
				self.TTToSemiLeptonicMC_SR.append(self.load_TTTo_hists("SR",systematic, False, "TTToSemiLeptonicMC"))
				self.TTToLeptonicMC_SR.append(self.load_TTTo_hists("SR",systematic, False, "TTToLeptonicMC"))
			if self.includeWJets:
				self.WJetsMC_LNu_HT800to1200_SR.append(self.load_WJets_hists("SR",systematic, False, "WJetsMC_LNu-HT800to1200"))
				self.WJetsMC_LNu_HT1200to2500_SR.append(self.load_WJets_hists("SR",systematic, False, "WJetsMC_LNu-HT1200to2500"))
				self.WJetsMC_LNu_HT2500toInf_SR.append(self.load_WJets_hists("SR",systematic, False, "WJetsMC_LNu-HT2500toInf"))
				self.WJetsMC_QQ_HT800toInf_SR.append(self.load_WJets_hists("SR",systematic, False, "WJetsMC_QQ-HT800toInf"))

			### CR

			if self.use_QCD_Pt:
				self.QCDMC_Pt_170to300_hist_CR.append(self.load_QCD_hists("CR",systematic,False,"QCDMC_Pt_170to300"))
				self.QCDMC_Pt_300to470_hist_CR.append(self.load_QCD_hists("CR",systematic,False,"QCDMC_Pt_300to470"))
				self.QCDMC_Pt_470to600_hist_CR.append(self.load_QCD_hists("CR",systematic,False,"QCDMC_Pt_470to600"))
				self.QCDMC_Pt_600to800_hist_CR.append(self.load_QCD_hists("CR",systematic,False,"QCDMC_Pt_600to800"))
				self.QCDMC_Pt_800to1000_hist_CR.append(self.load_QCD_hists("CR",systematic,False,"QCDMC_Pt_800to1000"))
				self.QCDMC_Pt_1000to1400_hist_CR.append(self.load_QCD_hists("CR",systematic,False,"QCDMC_Pt_1000to1400"))
				self.QCDMC_Pt_1400to1800_hist_CR.append(self.load_QCD_hists("CR",systematic,False,"QCDMC_Pt_1400to1800"))
				self.QCDMC_Pt_1800to2400_hist_CR.append(self.load_QCD_hists("CR",systematic,False,"QCDMC_Pt_1800to2400"))
				self.QCDMC_Pt_2400to3200_hist_CR.append(self.load_QCD_hists("CR",systematic,False,"QCDMC_Pt_2400to3200"))
				self.QCDMC_Pt_3200toInf_hist_CR.append(self.load_QCD_hists("CR",systematic,False,"QCDMC_Pt_3200toInf"))
			else:
				self.QCD1000to1500_hist_CR.append(self.load_QCD_hists("CR",systematic,False,"QCDMC1000to1500"))
				self.QCD1500to2000_hist_CR.append(self.load_QCD_hists("CR",systematic,False,"QCDMC1500to2000"))
				self.QCD2000toInf_hist_CR.append(self.load_QCD_hists("CR",systematic,False,"QCDMC2000toInf"))

			self.TTJets1200to2500_hist_CR.append(self.load_ttbar_hist("CR",systematic,False,"TTJetsMCHT1200to2500"))
			self.TTJets2500toInf_hist_CR.append(self.load_ttbar_hist("CR",systematic,False, "TTJetsMCHT2500toInf"))

			self.ST_t_channel_top_hist_CR.append(self.load_ST_hists("CR",systematic,False,"ST_t-channel-top_inclMC" ))
			self.ST_t_channel_antitop_hist_CR.append(self.load_ST_hists("CR",systematic, False,"ST_t-channel-antitop_inclMC"))
			self.ST_s_channel_hadrons_hist_CR.append(self.load_ST_hists("CR",systematic, False, "ST_s-channel-hadronsMC"))
			self.ST_s_channel_leptons_hist_CR.append(self.load_ST_hists("CR",systematic, False, "ST_s-channel-leptonsMC"))
			self.ST_tW_antitop_hist_CR.append(self.load_ST_hists("CR",systematic, False, "ST_tW-antiTop_inclMC"))
			self.ST_tW_top_hist_CR.append(self.load_ST_hists("CR",systematic, False, "ST_tW-top_inclMC"))

			if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_CR.append(self.load_ttbar_hist("CR",systematic,False,"TTJetsMCHT800to1200" ))
			if self.includeTTTo:
				self.TTToHadronicMC_CR.append(self.load_TTTo_hists("CR",systematic, False,"TTToHadronicMC"))
				self.TTToSemiLeptonicMC_CR.append(self.load_TTTo_hists("CR",systematic, False, "TTToSemiLeptonicMC"))
				self.TTToLeptonicMC_CR.append(self.load_TTTo_hists("CR",systematic, False, "TTToLeptonicMC"))
			if self.includeWJets:
				self.WJetsMC_LNu_HT800to1200_CR.append(self.load_WJets_hists("CR",systematic, False, "WJetsMC_LNu-HT800to1200"))
				self.WJetsMC_LNu_HT1200to2500_CR.append(self.load_WJets_hists("CR",systematic, False, "WJetsMC_LNu-HT1200to2500"))
				self.WJetsMC_LNu_HT2500toInf_CR.append(self.load_WJets_hists("CR",systematic, False, "WJetsMC_LNu-HT2500toInf"))
				self.WJetsMC_QQ_HT800toInf_CR.append(self.load_WJets_hists("CR",systematic, False, "WJetsMC_QQ-HT800toInf"))



			### AT1b

			if self.use_QCD_Pt:
				self.QCDMC_Pt_170to300_hist_AT1b.append(self.load_QCD_hists("AT1b",systematic,False,"QCDMC_Pt_170to300"))
				self.QCDMC_Pt_300to470_hist_AT1b.append(self.load_QCD_hists("AT1b",systematic,False,"QCDMC_Pt_300to470"))
				self.QCDMC_Pt_470to600_hist_AT1b.append(self.load_QCD_hists("AT1b",systematic,False,"QCDMC_Pt_470to600"))
				self.QCDMC_Pt_600to800_hist_AT1b.append(self.load_QCD_hists("AT1b",systematic,False,"QCDMC_Pt_600to800"))
				self.QCDMC_Pt_800to1000_hist_AT1b.append(self.load_QCD_hists("AT1b",systematic,False,"QCDMC_Pt_800to1000"))
				self.QCDMC_Pt_1000to1400_hist_AT1b.append(self.load_QCD_hists("AT1b",systematic,False,"QCDMC_Pt_1000to1400"))
				self.QCDMC_Pt_1400to1800_hist_AT1b.append(self.load_QCD_hists("AT1b",systematic,False,"QCDMC_Pt_1400to1800"))
				self.QCDMC_Pt_1800to2400_hist_AT1b.append(self.load_QCD_hists("AT1b",systematic,False,"QCDMC_Pt_1800to2400"))
				self.QCDMC_Pt_2400to3200_hist_AT1b.append(self.load_QCD_hists("AT1b",systematic,False,"QCDMC_Pt_2400to3200"))
				self.QCDMC_Pt_3200toInf_hist_AT1b.append(self.load_QCD_hists("AT1b",systematic,False,"QCDMC_Pt_3200toInf"))
			else:
				self.QCD1000to1500_hist_AT1b.append(self.load_QCD_hists("AT1b",systematic,False,"QCDMC1000to1500"))
				self.QCD1500to2000_hist_AT1b.append(self.load_QCD_hists("AT1b",systematic,False,"QCDMC1500to2000"))
				self.QCD2000toInf_hist_AT1b.append(self.load_QCD_hists("AT1b",systematic,False,"QCDMC2000toInf"))

			self.TTJets1200to2500_hist_AT1b.append(self.load_ttbar_hist("AT1b",systematic,False,"TTJetsMCHT1200to2500"))
			self.TTJets2500toInf_hist_AT1b.append(self.load_ttbar_hist("AT1b",systematic,False, "TTJetsMCHT2500toInf"))

			self.ST_t_channel_top_hist_AT1b.append(self.load_ST_hists("AT1b",systematic,False,"ST_t-channel-top_inclMC" ))
			self.ST_t_channel_antitop_hist_AT1b.append(self.load_ST_hists("AT1b",systematic, False,"ST_t-channel-antitop_inclMC"))
			self.ST_s_channel_hadrons_hist_AT1b.append(self.load_ST_hists("AT1b",systematic, False, "ST_s-channel-hadronsMC"))
			self.ST_s_channel_leptons_hist_AT1b.append(self.load_ST_hists("AT1b",systematic, False, "ST_s-channel-leptonsMC"))
			self.ST_tW_antitop_hist_AT1b.append(self.load_ST_hists("AT1b",systematic, False, "ST_tW-antiTop_inclMC"))
			self.ST_tW_top_hist_AT1b.append(self.load_ST_hists("AT1b",systematic, False, "ST_tW-top_inclMC"))

			if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_AT1b.append(self.load_ttbar_hist("AT1b",systematic,False,"TTJetsMCHT800to1200" ))
			if self.includeTTTo:
				self.TTToHadronicMC_AT1b.append(self.load_TTTo_hists("AT1b",systematic, False,"TTToHadronicMC"))
				self.TTToSemiLeptonicMC_AT1b.append(self.load_TTTo_hists("AT1b",systematic, False, "TTToSemiLeptonicMC"))
				self.TTToLeptonicMC_AT1b.append(self.load_TTTo_hists("AT1b",systematic, False, "TTToLeptonicMC"))
			if self.includeWJets:
				self.WJetsMC_LNu_HT800to1200_AT1b.append(self.load_WJets_hists("AT1b",systematic, False, "WJetsMC_LNu-HT800to1200"))
				self.WJetsMC_LNu_HT1200to2500_AT1b.append(self.load_WJets_hists("AT1b",systematic, False, "WJetsMC_LNu-HT1200to2500"))
				self.WJetsMC_LNu_HT2500toInf_AT1b.append(self.load_WJets_hists("AT1b",systematic, False, "WJetsMC_LNu-HT2500toInf"))
				self.WJetsMC_QQ_HT800toInf_AT1b.append(self.load_WJets_hists("AT1b",systematic, False, "WJetsMC_QQ-HT800toInf"))

			### AT0b

			if self.use_QCD_Pt:
				self.QCDMC_Pt_170to300_hist_AT0b.append(self.load_QCD_hists("AT0b",systematic,False,"QCDMC_Pt_170to300"))
				self.QCDMC_Pt_300to470_hist_AT0b.append(self.load_QCD_hists("AT0b",systematic,False,"QCDMC_Pt_300to470"))
				self.QCDMC_Pt_470to600_hist_AT0b.append(self.load_QCD_hists("AT0b",systematic,False,"QCDMC_Pt_470to600"))
				self.QCDMC_Pt_600to800_hist_AT0b.append(self.load_QCD_hists("AT0b",systematic,False,"QCDMC_Pt_600to800"))
				self.QCDMC_Pt_800to1000_hist_AT0b.append(self.load_QCD_hists("AT0b",systematic,False,"QCDMC_Pt_800to1000"))
				self.QCDMC_Pt_1000to1400_hist_AT0b.append(self.load_QCD_hists("AT0b",systematic,False,"QCDMC_Pt_1000to1400"))
				self.QCDMC_Pt_1400to1800_hist_AT0b.append(self.load_QCD_hists("AT0b",systematic,False,"QCDMC_Pt_1400to1800"))
				self.QCDMC_Pt_1800to2400_hist_AT0b.append(self.load_QCD_hists("AT0b",systematic,False,"QCDMC_Pt_1800to2400"))
				self.QCDMC_Pt_2400to3200_hist_AT0b.append(self.load_QCD_hists("AT0b",systematic,False,"QCDMC_Pt_2400to3200"))
				self.QCDMC_Pt_3200toInf_hist_AT0b.append(self.load_QCD_hists("AT0b",systematic,False,"QCDMC_Pt_3200toInf"))
			else:
				self.QCD1000to1500_hist_AT0b.append(self.load_QCD_hists("AT0b",systematic,False,"QCDMC1000to1500"))
				self.QCD1500to2000_hist_AT0b.append(self.load_QCD_hists("AT0b",systematic,False,"QCDMC1500to2000"))
				self.QCD2000toInf_hist_AT0b.append(self.load_QCD_hists("AT0b",systematic,False,"QCDMC2000toInf"))

			self.TTJets1200to2500_hist_AT0b.append(self.load_ttbar_hist("AT0b",systematic,False,"TTJetsMCHT1200to2500"))
			self.TTJets2500toInf_hist_AT0b.append(self.load_ttbar_hist("AT0b",systematic,False, "TTJetsMCHT2500toInf"))

			self.ST_t_channel_top_hist_AT0b.append(self.load_ST_hists("AT0b",systematic,False,"ST_t-channel-top_inclMC" ))
			self.ST_t_channel_antitop_hist_AT0b.append(self.load_ST_hists("AT0b",systematic, False,"ST_t-channel-antitop_inclMC"))
			self.ST_s_channel_hadrons_hist_AT0b.append(self.load_ST_hists("AT0b",systematic, False, "ST_s-channel-hadronsMC"))
			self.ST_s_channel_leptons_hist_AT0b.append(self.load_ST_hists("AT0b",systematic, False, "ST_s-channel-leptonsMC"))
			self.ST_tW_antitop_hist_AT0b.append(self.load_ST_hists("AT0b",systematic, False, "ST_tW-antiTop_inclMC"))
			self.ST_tW_top_hist_AT0b.append(self.load_ST_hists("AT0b",systematic, False, "ST_tW-top_inclMC"))
			
			if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_AT0b.append(self.load_ttbar_hist("AT0b",systematic,False,"TTJetsMCHT800to1200" ))
			if self.includeTTTo:
				self.TTToHadronicMC_AT0b.append(self.load_TTTo_hists("AT0b",systematic, False,"TTToHadronicMC"))
				self.TTToSemiLeptonicMC_AT0b.append(self.load_TTTo_hists("AT0b",systematic, False, "TTToSemiLeptonicMC"))
				self.TTToLeptonicMC_AT0b.append(self.load_TTTo_hists("AT0b",systematic, False, "TTToLeptonicMC"))
			if self.includeWJets:
				self.WJetsMC_LNu_HT800to1200_AT0b.append(self.load_WJets_hists("AT0b",systematic, False, "WJetsMC_LNu-HT800to1200"))
				self.WJetsMC_LNu_HT1200to2500_AT0b.append(self.load_WJets_hists("AT0b",systematic, False, "WJetsMC_LNu-HT1200to2500"))
				self.WJetsMC_LNu_HT2500toInf_AT0b.append(self.load_WJets_hists("AT0b",systematic, False, "WJetsMC_LNu-HT2500toInf"))
				self.WJetsMC_QQ_HT800toInf_AT0b.append(self.load_WJets_hists("AT0b",systematic, False, "WJetsMC_QQ-HT800toInf"))


			if self.doATxtb:
				self.QCD1000to1500_hist_AT1tb.append(self.load_QCD_hists("AT1tb",systematic,False,"QCDMC1000to1500"))
				self.QCD1500to2000_hist_AT1tb.append(self.load_QCD_hists("AT1tb",systematic,False,"QCDMC1500to2000"))
				self.QCD2000toInf_hist_AT1tb.append(self.load_QCD_hists("AT1tb",systematic,False,"QCDMC2000toInf"))

				self.TTJets1200to2500_hist_AT1tb.append(self.load_ttbar_hist("AT1tb",systematic,False,"TTJetsMCHT1200to2500"))
				self.TTJets2500toInf_hist_AT1tb.append(self.load_ttbar_hist("AT1tb",systematic,False, "TTJetsMCHT2500toInf"))

				self.ST_t_channel_top_hist_AT1tb.append(self.load_ST_hists("AT1tb",systematic,False,"ST_t-channel-top_inclMC" ))
				self.ST_t_channel_antitop_hist_AT1tb.append(self.load_ST_hists("AT1tb",systematic, False,"ST_t-channel-antitop_inclMC"))
				self.ST_s_channel_hadrons_hist_AT1tb.append(self.load_ST_hists("AT1tb",systematic, False, "ST_s-channel-hadronsMC"))
				self.ST_s_channel_leptons_hist_AT1tb.append(self.load_ST_hists("AT1tb",systematic, False, "ST_s-channel-leptonsMC"))
				self.ST_tW_antitop_hist_AT1tb.append(self.load_ST_hists("AT1tb",systematic, False, "ST_tW-antiTop_inclMC"))
				self.ST_tW_top_hist_AT1tb.append(self.load_ST_hists("AT1tb",systematic, False, "ST_tW-top_inclMC"))

				if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_AT1tb.append(self.load_ttbar_hist("AT1tb",systematic,False,"TTJetsMCHT800to1200" ))
				if self.includeTTTo:
					self.TTToHadronicMC_AT1tb.append(self.load_TTTo_hists("AT1tb",systematic, False,"TTToHadronicMC"))
					self.TTToSemiLeptonicMC_AT1tb.append(self.load_TTTo_hists("AT1tb",systematic, False, "TTToSemiLeptonicMC"))
					self.TTToLeptonicMC_AT1tb.append(self.load_TTTo_hists("AT1tb",systematic, False, "TTToLeptonicMC"))
				if self.includeWJets:
					self.WJetsMC_LNu_HT800to1200_AT1tb.append(self.load_WJets_hists("AT1tb",systematic, False, "WJetsMC_LNu-HT800to1200"))
					self.WJetsMC_LNu_HT1200to2500_AT1tb.append(self.load_WJets_hists("AT1tb",systematic, False, "WJetsMC_LNu-HT1200to2500"))
					self.WJetsMC_LNu_HT2500toInf_AT1tb.append(self.load_WJets_hists("AT1tb",systematic, False, "WJetsMC_LNu-HT2500toInf"))
					self.WJetsMC_QQ_HT800toInf_AT1tb.append(self.load_WJets_hists("AT1tb",systematic, False, "WJetsMC_QQ-HT800toInf"))

				self.QCD1000to1500_hist_AT0tb.append(self.load_QCD_hists("AT0tb",systematic,False,"QCDMC1000to1500"))
				self.QCD1500to2000_hist_AT0tb.append(self.load_QCD_hists("AT0tb",systematic,False,"QCDMC1500to2000"))
				self.QCD2000toInf_hist_AT0tb.append(self.load_QCD_hists("AT0tb",systematic,False,"QCDMC2000toInf"))

				self.TTJets1200to2500_hist_AT0tb.append(self.load_ttbar_hist("AT0tb",systematic,False,"TTJetsMCHT1200to2500"))
				self.TTJets2500toInf_hist_AT0tb.append(self.load_ttbar_hist("AT0tb",systematic,False, "TTJetsMCHT2500toInf"))

				self.ST_t_channel_top_hist_AT0tb.append(self.load_ST_hists("AT0tb",systematic,False,"ST_t-channel-top_inclMC" ))
				self.ST_t_channel_antitop_hist_AT0tb.append(self.load_ST_hists("AT0tb",systematic, False,"ST_t-channel-antitop_inclMC"))
				self.ST_s_channel_hadrons_hist_AT0tb.append(self.load_ST_hists("AT0tb",systematic, False, "ST_s-channel-hadronsMC"))
				self.ST_s_channel_leptons_hist_AT0tb.append(self.load_ST_hists("AT0tb",systematic, False, "ST_s-channel-leptonsMC"))
				self.ST_tW_antitop_hist_AT0tb.append(self.load_ST_hists("AT0tb",systematic, False, "ST_tW-antiTop_inclMC"))
				self.ST_tW_top_hist_AT0tb.append(self.load_ST_hists("AT0tb",systematic, False, "ST_tW-top_inclMC"))

				if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_AT0tb.append(self.load_ttbar_hist("AT0tb",systematic,False,"TTJetsMCHT800to1200" ))
				if self.includeTTTo:
					self.TTToHadronicMC_AT0tb.append(self.load_TTTo_hists("AT0tb",systematic, False,"TTToHadronicMC"))
					self.TTToSemiLeptonicMC_AT0tb.append(self.load_TTTo_hists("AT0tb",systematic, False, "TTToSemiLeptonicMC"))
					self.TTToLeptonicMC_AT0tb.append(self.load_TTTo_hists("AT0tb",systematic, False, "TTToLeptonicMC"))
				if self.includeWJets:
					self.WJetsMC_LNu_HT800to1200_AT0tb.append(self.load_WJets_hists("AT0tb",systematic, False, "WJetsMC_LNu-HT800to1200"))
					self.WJetsMC_LNu_HT1200to2500_AT0tb.append(self.load_WJets_hists("AT0tb",systematic, False, "WJetsMC_LNu-HT1200to2500"))
					self.WJetsMC_LNu_HT2500toInf_AT0tb.append(self.load_WJets_hists("AT0tb",systematic, False, "WJetsMC_LNu-HT2500toInf"))
					self.WJetsMC_QQ_HT800toInf_AT0tb.append(self.load_WJets_hists("AT0tb",systematic, False, "WJetsMC_QQ-HT800toInf"))


			## sideband
			if self.doSideband:
				self.QCD1000to1500_hist_SB0b.append(self.load_QCD_hists("SB0b",systematic_SB,False,"QCDMC1000to1500"))
				self.QCD1500to2000_hist_SB0b.append(self.load_QCD_hists("SB0b",systematic_SB,False,"QCDMC1500to2000"))

				self.TTJets800to1200_hist_SB0b.append(self.load_ttbar_hist("SB0b",systematic_SB,False, "TTJetsMCHT800to1200"))
				self.TTJets1200to2500_hist_SB0b.append(self.load_ttbar_hist("SB0b",systematic_SB,False,"TTJetsMCHT1200to2500"))

				self.ST_t_channel_top_hist_SB0b.append(self.load_ST_hists("SB0b",systematic_SB,False,"ST_t-channel-top_inclMC" ))
				self.ST_t_channel_antitop_hist_SB0b.append(self.load_ST_hists("SB0b",systematic_SB, False,"ST_t-channel-antitop_inclMC"))
				self.ST_s_channel_hadrons_hist_SB0b.append(self.load_ST_hists("SB0b",systematic_SB, False, "ST_s-channel-hadronsMC"))
				self.ST_s_channel_leptons_hist_SB0b.append(self.load_ST_hists("SB0b",systematic_SB, False, "ST_s-channel-leptonsMC"))
				self.ST_tW_antitop_hist_SB0b.append(self.load_ST_hists("SB0b",systematic_SB, False, "ST_tW-antiTop_inclMC"))
				self.ST_tW_top_hist_SB0b.append(self.load_ST_hists("SB0b",systematic_SB, False, "ST_tW-top_inclMC"))

				if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_SB0b.append(self.load_ttbar_hist("SB0b",systematic,False,"TTJetsMCHT800to1200" ))
				if self.includeTTTo:
					self.TTToHadronicMC_SB0b.append(self.load_TTTo_hists("SB0b",systematic, False,"TTToHadronicMC"))
					self.TTToSemiLeptonicMC_SB0b.append(self.load_TTTo_hists("SB0b",systematic, False, "TTToSemiLeptonicMC"))
					self.TTToLeptonicMC_SB0b.append(self.load_TTTo_hists("SB0b",systematic, False, "TTToLeptonicMC"))
				if self.includeWJets:
					self.WJetsMC_LNu_HT800to1200_SB0b.append(self.load_WJets_hists("SB0b",systematic, False, "WJetsMC_LNu-HT800to1200"))
					self.WJetsMC_LNu_HT1200to2500_SB0b.append(self.load_WJets_hists("SB0b",systematic, False, "WJetsMC_LNu-HT1200to2500"))
					self.WJetsMC_LNu_HT2500toInf_SB0b.append(self.load_WJets_hists("SB0b",systematic, False, "WJetsMC_LNu-HT2500toInf"))
					self.WJetsMC_QQ_HT800toInf_SB0b.append(self.load_WJets_hists("SB0b",systematic, False, "WJetsMC_QQ-HT800toInf"))


				self.QCD1000to1500_hist_SB1b.append(self.load_QCD_hists("SB1b",systematic_SB,False,"QCDMC1000to1500"))
				self.QCD1500to2000_hist_SB1b.append(self.load_QCD_hists("SB1b",systematic_SB,False,"QCDMC1500to2000"))

				self.TTJets800to1200_hist_SB1b.append(self.load_ttbar_hist("SB1b",systematic_SB,False, "TTJetsMCHT800to1200"))
				self.TTJets1200to2500_hist_SB1b.append(self.load_ttbar_hist("SB1b",systematic_SB,False,"TTJetsMCHT1200to2500"))

				self.ST_t_channel_top_hist_SB1b.append(self.load_ST_hists("SB1b",systematic_SB,False,"ST_t-channel-top_inclMC" ))
				self.ST_t_channel_antitop_hist_SB1b.append(self.load_ST_hists("SB1b",systematic_SB, False,"ST_t-channel-antitop_inclMC"))
				self.ST_s_channel_hadrons_hist_SB1b.append(self.load_ST_hists("SB1b",systematic_SB, False, "ST_s-channel-hadronsMC"))
				self.ST_s_channel_leptons_hist_SB1b.append(self.load_ST_hists("SB1b",systematic_SB, False, "ST_s-channel-leptonsMC"))
				self.ST_tW_antitop_hist_SB1b.append(self.load_ST_hists("SB1b",systematic_SB, False, "ST_tW-antiTop_inclMC"))
				self.ST_tW_top_hist_SB1b.append(self.load_ST_hists("SB1b",systematic_SB, False, "ST_tW-top_inclMC"))
				
				if self.includeTTJets800to1200: self.TTJetsMCHT800to1200_SB1b.append(self.load_ttbar_hist("SB1b",systematic,False,"TTJetsMCHT800to1200" ))
				if self.includeTTTo:
					self.TTToHadronicMC_SB1b.append(self.load_TTTo_hists("SB1b",systematic, False,"TTToHadronicMC"))
					self.TTToSemiLeptonicMC_SB1b.append(self.load_TTTo_hists("SB1b",systematic, False, "TTToSemiLeptonicMC"))
					self.TTToLeptonicMC_SB1b.append(self.load_TTTo_hists("SB1b",systematic, False, "TTToLeptonicMC"))
				if self.includeWJets:
					self.WJetsMC_LNu_HT800to1200_SB1b.append(self.load_WJets_hists("SB1b",systematic, False, "WJetsMC_LNu-HT800to1200"))
					self.WJetsMC_LNu_HT1200to2500_SB1b.append(self.load_WJets_hists("SB1b",systematic, False, "WJetsMC_LNu-HT1200to2500"))
					self.WJetsMC_LNu_HT2500toInf_SB1b.append(self.load_WJets_hists("SB1b",systematic, False, "WJetsMC_LNu-HT2500toInf"))
					self.WJetsMC_QQ_HT800toInf_SB1b.append(self.load_WJets_hists("SB1b",systematic, False, "WJetsMC_QQ-HT800toInf"))



			if systematic == "nom":
				sys_strs = [""]
			elif "topPt" in systematic:
				sys_strs = ["_up", "_down"]
			else:
				sys_strs = ["_up", "_down"]



		if not self.WP:

			for systematic in self.data_systematics:
				self.data_hist_SR.append(self.load_data_hists("SR",systematic))
				self.data_hist_CR.append(self.load_data_hists("CR",systematic))
				self.data_hist_AT0b.append(self.load_data_hists("AT0b",systematic))
				self.data_hist_AT1b.append(self.load_data_hists("AT1b",systematic))

				if self.doATxtb:
					self.data_hist_AT0tb.append(self.load_data_hists("AT0tb",systematic))
					self.data_hist_AT1tb.append(self.load_data_hists("AT1tb",systematic))
				if self.doSideband:
					self.data_hist_SB1b.append(self.load_data_hists("SB1b",systematic))
					self.data_hist_SB0b.append(self.load_data_hists("SB0b",systematic))

		print("Background and data hists loaded.")


		if self.doHTdist: 
			self.init_HT_dist_superbin_indices()
			self.merge_HT_dist_superbin_indices()

			self.print_superbins()

			#print("The merged SR superbin indices are %s."%self.HT_dist_superbins["SR"])
			#print("The merged AT1b superbin indices are %s."%self.HT_dist_superbins["AT1b"])
			#print("The merged SB1b superbin indices are %s."%self.HT_dist_superbins["SB1b"])



	def load_QCD_hists(self,region,systematic, forStats = False, hist_type = ""):
		ROOT.TH1.SetDefaultSumw2()
		ROOT.TH2.SetDefaultSumw2()
		#ROOT.TH2.SetDefaultSumw2()
		sys_suffix = [""]
		
		use_filepath = self.MC_root_file_home 

		if region in ["SB1b", "SB0b"]: use_filepath	  = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"

		if systematic == "nom":
			sys_updown = ["nom"]
		#elif systematic == "topPt":
		#	sys_updown = ["%s_up"%systematic]
		else:
			sys_updown = ["%s_up"%systematic,"%s_down"%systematic]

		SF_1000to1500 = {'2015': 1.578683216 ,   '2016':1.482632755 ,  '2017': 3.126481451,  '2018': 4.289571744   }
		SF_1500to2000 = {'2015': 0.2119142341,   '2016':0.195224041 ,  '2017': 0.3197450474, '2018': 0.4947703875  }
		SF_2000toInf  = {'2015': 0.08568186031 , '2016':0.07572795371, '2017': 0.14306915,   '2018': 0.2132134533  }

		if forStats:
			SF_1000to1500 = {'2015': 1 ,   '2016':1 ,  '2017': 1,  '2018': 1   }
			SF_1500to2000 = {'2015': 1,   '2016':1 ,  '2017': 1, '2018': 1  }
			SF_2000toInf  = {'2015': 1 , '2016':1, '2017': 1,   '2018': 1  }

		### make histogram paths
		hist_path_1000to1500 = use_filepath + "QCDMC1000to1500_%s_%sprocessed.root"%(self.year, self.WP_str)
		hist_path_1500to2000 = use_filepath + "QCDMC1500to2000_%s_%sprocessed.root"%(self.year, self.WP_str)

		if region not in ["SB1b", "SB0b"]: 
			hist_path_2000toInf  = use_filepath + "QCDMC2000toInf_%s_%sprocessed.root"%(self.year, self.WP_str)

		all_combined_QCD_hist = []
		for sys_str in sys_updown:

			if "topPt" in systematic and "down" in sys_str:
				hist_name = "nom/%s_%s%s"%(self.final_hist_name, self.technique_str ,region )
			else:
				hist_name = "%s/%s_%s%s"%(sys_str,self.final_hist_name,self.technique_str ,region )


			#if hist_type   == "QCDMC1000to1500": 
			#all_combined_QCD_hist.append( TH2_hist_1000to1500  )  #### THESE ARE UNSCALED!!!
			#elif hist_type == "QCDMC1500to2000": 
			#all_combined_QCD_hist.append( TH2_hist_1500to2000  )  #### THESE ARE UNSCALED!!!
			#elif hist_type == "QCDMC2000toInf" and region not in ["SB1b", "SB0b"] :  all_combined_QCD_hist.append( TH2_hist_2000toInf   )  #### THESE ARE UNSCALED!!!
  

			if "QCD" in hist_type:
				hist_path = use_filepath + "%s_%s_%sprocessed.root"%(hist_type, self.year, self.WP_str)
				#print("hist_name / file name = %s / %s"%(     hist_name,hist_path))
				TH2_file = ROOT.TFile.Open(hist_path,"READ")
				TH2_hist = self.clean_histogram(TH2_file.Get(hist_name), systematic, hist_type ) 
				TH2_hist.SetDirectory(0)
				all_combined_QCD_hist.append( TH2_hist  )  #### THESE ARE UNSCALED!!!

			## COMBINED PORTION BELOW IS NOT IMPLEMENTED FOR QCD_Pt hists
			elif hist_type == "":


				TH2_file_1000to1500 = ROOT.TFile.Open(hist_path_1000to1500,"READ")
				TH2_hist_1000to1500 = self.clean_histogram(TH2_file_1000to1500.Get(hist_name), systematic, "QCDMC1000to1500" )

				TH2_file_1500to2000 = ROOT.TFile.Open(hist_path_1500to2000,"READ")
				TH2_hist_1500to2000 = self.clean_histogram(TH2_file_1500to2000.Get(hist_name), systematic, "QCDMC1500to2000" )

				if region not in ["SB1b", "SB0b"] : 
					TH2_file_2000toInf = ROOT.TFile.Open(hist_path_2000toInf,"READ")
					TH2_hist_2000toInf = self.clean_histogram(TH2_file_2000toInf.Get(hist_name), systematic, "QCDMC2000toInf" )

				TH2_hist_1000to1500.SetDirectory(0)   # histograms lose their references when the file destructor is called
				TH2_hist_1500to2000.SetDirectory(0)   # histograms lose their references when the file destructor is called
				if region not in ["SB1b", "SB0b"] : TH2_hist_2000toInf.SetDirectory(0)   # histograms lose their references when the file destructor is called



				### return the COMBINED histograms

				### scale each histogram
				TH2_hist_1000to1500.Scale(self.BR_SF_scale*SF_1000to1500[self.year])
				TH2_hist_1500to2000.Scale(self.BR_SF_scale*SF_1500to2000[self.year])
				if region not in ["SB1b", "SB0b"] : 
					TH2_hist_2000toInf.Scale(self.BR_SF_scale*SF_2000toInf[self.year])



				if region in ["SB1b", "SB0b"] : combined_QCD_hist = ROOT.TH2F("combined_QCD_%s%s"%(self.technique_str ,sys_str), ("QCD (HT1000-Inf) Events in the %s (%s) (%s)"%(region, year, sys_str)), 15 ,0.0, 8000, 12, 0.0, 3000)
				else: 
					if self.doHTdist: combined_QCD_hist = ROOT.TH1F("combined_QCD_%s"%(region),"Event H_{T} (%s) (%s) (%s); H_{T} [GeV]; Events / 200 GeV"%(region, max(hist_type,"QCD"),  self.technique_str ),50,0.,10000)
					else: combined_QCD_hist = ROOT.TH2F("combined_QCD_%s%s"%(self.technique_str ,sys_str), ("QCD (HT1000-Inf) Events in the %s (%s) (%s)"%(region, year, sys_str)), 22,1250., 10000, 20, 500, 5000)
				combined_QCD_hist.Add(TH2_hist_1000to1500)
				combined_QCD_hist.Add(TH2_hist_1500to2000)
				if region not in ["SB1b", "SB0b"] : combined_QCD_hist.Add(TH2_hist_2000toInf)

				combined_QCD_hist.SetDirectory(0)   # histograms lose their references when the file destructor is called
				all_combined_QCD_hist.append(combined_QCD_hist)
			else: 
				print("ERROR in load_QCD_hists: hist_type=%s is not correct (options are : '', 'QCDMC1000to1500', 'QCDMC1500to2000', and 'QCDMC2000toInf' )"%hist_type)
				return []
		ROOT.TH1.AddDirectory(False)

		return all_combined_QCD_hist   # load in QCD histograms, scale them, add them together, and return their sum



	def load_WJets_hists(self,region,systematic, forStats = False, hist_type = ""):
			ROOT.TH1.SetDefaultSumw2()
			ROOT.TH2.SetDefaultSumw2()
			#ROOT.TH2.SetDefaultSumw2()

			use_filepath = self.MC_root_file_home 
			if region in ["SB1b", "SB0b"]: use_filepath	  = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"

			sys_suffix = [""]
			if systematic == "nom":
				sys_updown = ["nom"]
			elif "topPt" in systematic:
				sys_updown = ["%s_up"%systematic,"%s_down"%systematic ]
			else:
				sys_updown = ["%s_up"%systematic,"%s_down"%systematic]

			all_combined_WJets_hist = []
			for sys_str in sys_updown:

				if "topPt" in systematic and "down" in sys_str:
					hist_name_WJets = "nom/%s_%s%s"%(self.final_hist_name,self.technique_str ,region )
				else:
					hist_name_WJets = "%s/%s_%s%s"%(sys_str,self.final_hist_name,self.technique_str ,region )


				#if hist_type   == "WJetsMC_LNu-HT800to1200": all_combined_WJets_hist.append( TH2_hist_WJetsMC_LNu_HT800to1200  )
				#elif hist_type == "WJetsMC_LNu-HT1200to2500" : all_combined_WJets_hist.append( TH2_hist_WJetsMC_LNu_HT1200to2500  )
				#elif hist_type == "WJetsMC_LNu-HT2500toInf": all_combined_WJets_hist.append( TH2_hist_WJetsMC_LNu_HT2500toInf  )
				#elif hist_type == "WJetsMC_QQ-HT800toInf": all_combined_WJets_hist.append( TH2_hist_WJetsMC_QQ_HT800toInf  )


				if "WJets" in hist_type:
					hist_path = use_filepath + "%s_%s_%sprocessed.root"%(hist_type, self.year, self.WP_str)
					TH2_file = ROOT.TFile.Open(hist_path,"READ")
					TH2_hist = self.clean_histogram(TH2_file.Get(hist_name_WJets), systematic, hist_type ) 
					all_combined_WJets_hist.append( TH2_hist  )  #### THESE ARE UNSCALED!!!

				elif hist_type == "":


					hist_path_WJetsMC_LNu_HT800to1200 = use_filepath+ "WJetsMC_LNu-HT800to1200_%s_%sprocessed.root"%(self.year, self.WP_str)
					hist_path_WJetsMC_LNu_HT1200to2500 = use_filepath+ "WJetsMC_LNu-HT1200to2500_%s_%sprocessed.root"%(self.year, self.WP_str)
					hist_path_WJetsMC_LNu_HT2500toInf = use_filepath+ "WJetsMC_LNu-HT2500toInf_%s_%sprocessed.root"%(self.year, self.WP_str)
					hist_path_WJetsMC_QQ_HT800toInf= use_filepath+ "WJetsMC_QQ-HT800toInf_%s_%sprocessed.root"%(self.year, self.WP_str)

					SF_WJetsMC_LNu_HT800to1200  = return_BR_SF(self.year,"WJetsMC_LNu-HT800to1200") 
					SF_WJetsMC_LNu_HT1200to2500  = return_BR_SF(self.year,"WJetsMC_LNu-HT1200to2500") 
					SF_WJetsMC_LNu_HT2500toInf  = return_BR_SF(self.year,"WJetsMC_LNu-HT2500toInf") 
					SF_WJetsMC_QQ_HT800toInf  = return_BR_SF(self.year,"WJetsMC_QQ-HT800toInf") 

					TH2_file_WJetsMC_LNu_HT800to1200  = ROOT.TFile.Open(hist_path_WJetsMC_LNu_HT800to1200,"READ")
					TH2_file_WJetsMC_LNu_HT1200to2500 = ROOT.TFile.Open(hist_path_WJetsMC_LNu_HT1200to2500,"READ")
					TH2_file_WJetsMC_LNu_HT2500toInf  = ROOT.TFile.Open(hist_path_WJetsMC_LNu_HT2500toInf,"READ")
					TH2_file_WJetsMC_QQ_HT800toInf    = ROOT.TFile.Open(hist_path_WJetsMC_QQ_HT800toInf,"READ")

					TH2_hist_WJetsMC_LNu_HT800to1200     = self.clean_histogram(TH2_file_WJetsMC_LNu_HT800to1200.Get(hist_name_WJets) , systematic, "WJetsMC_LNu-HT800to1200" )
					TH2_hist_WJetsMC_LNu_HT1200to2500 = self.clean_histogram(TH2_file_WJetsMC_LNu_HT1200to2500.Get(hist_name_WJets) , systematic, "WJetsMC_LNu-HT1200to2500" )
					TH2_hist_WJetsMC_LNu_HT2500toInf     = self.clean_histogram(TH2_file_WJetsMC_LNu_HT2500toInf.Get(hist_name_WJets) , systematic, "WJetsMC_LNu-HT2500toInf" )
					TH2_hist_WJetsMC_QQ_HT800toInf     = self.clean_histogram(TH2_file_WJetsMC_QQ_HT800toInf.Get(hist_name_WJets) , systematic, "WJetsMC_QQ-HT800toInf" )


					TH2_file_WJetsMC_LNu_HT800to1200.Scale(self.BR_SF_scale*SF_WJetsMC_LNu_HT800to1200)
					TH2_file_WJetsMC_LNu_HT800to1200.SetDirectory(0)   # histograms lose their references when the file destructor is called

					TH2_file_WJetsMC_LNu_HT1200to2500.Scale(self.BR_SF_scale*SF_WJetsMC_LNu_HT1200to2500)
					TH2_file_WJetsMC_LNu_HT1200to2500.SetDirectory(0)   # histograms lose their references when the file destructor is called

					TH2_hist_WJetsMC_LNu_HT2500toInf.Scale(self.BR_SF_scale*SF_WJetsMC_LNu_HT2500toInf)
					TH2_hist_WJetsMC_LNu_HT2500toInf.SetDirectory(0)   # histograms lose their references when the file destructor is called

					TH2_hist_WJetsMC_QQ_HT800toInf.Scale(self.BR_SF_scale*SF_WJetsMC_QQ_HT800toInf)
					TH2_hist_WJetsMC_QQ_HT800toInf.SetDirectory(0)   # histograms lose their references when the file destructor is called

					### return the COMBINED histograms

					TH2_file_WJetsMC_LNu_HT800to1200.SetName("combined_WJets_%s%s"%(self.technique_str ,sys_str))
					TH2_file_WJetsMC_LNu_HT800to1200.SetTitle("combined WJets MC (%s) (%s) (%s)"%(self.year,region, sys_str))

					TH2_file_WJetsMC_LNu_HT800to1200.Add(TH2_file_WJetsMC_LNu_HT1200to2500)
					TH2_file_WJetsMC_LNu_HT800to1200.Add(TH2_hist_WJetsMC_LNu_HT2500toInf)
					TH2_file_WJetsMC_LNu_HT800to1200.Add(TH2_hist_WJetsMC_QQ_HT800toInf)

					all_combined_WJets_hist.append(TH2_file_WJetsMC_LNu_HT800to1200)
				else: 
					print("ERROR in load_WJets_hists: hist_type=%s is not correct (options are : '', 'WJetsMC_LNu_HT800to1200', 'WJetsMC_LNu_HT1200to2500', 'WJetsMC_LNu_HT2500toInf',  and 'WJetsMC_QQ_HT800toInf' )"%hist_type)
					return []
			return all_combined_WJets_hist  # load in WJets historam, scale it, and return this version






	def load_TTTo_hists(self,region,systematic, forStats = False, hist_type = ""):
		ROOT.TH1.SetDefaultSumw2()
		ROOT.TH2.SetDefaultSumw2()
		#ROOT.TH2.SetDefaultSumw2()

		use_filepath = self.MC_root_file_home 
		if region in ["SB1b", "SB0b"]: use_filepath	  = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"


		SF_TTToHadronic= {'2015':0.075592 , '2016':0.05808655696 , '2017':0.06651018525 , '2018': 0.06588049107 }
		SF_TTToSemiLeptonic= {'2015':0.05395328118 , '2016':0.04236184005 , '2017':0.04264829286 , '2018': 0.04563489275 }
		SF_TTToLeptonic= {'2015':0.0459517611 , '2016':0.03401684391 , '2017':0.03431532926 , '2018': 0.03617828025 }

		hist_path_TTToHadronic = use_filepath+ "TTToHadronicMC_%s_%sprocessed.root"%(self.year, self.WP_str)
		hist_path_TTToSemiLeptonic = use_filepath+ "TTToSemiLeptonicMC_%s_%sprocessed.root"%(self.year, self.WP_str)
		hist_path_TTToLeptonic = use_filepath+ "TTToLeptonicMC_%s_%sprocessed.root"%(self.year, self.WP_str)


		sys_suffix = [""]
		if systematic == "nom":
			sys_updown = ["nom"]
		elif "topPt" in systematic:
			sys_updown = ["%s_up"%systematic,"%s_down"%systematic ]
		else:
			sys_updown = ["%s_up"%systematic,"%s_down"%systematic]

		all_combined_TTbar_hist = []
		for sys_str in sys_updown:

			if "topPt" in systematic and "down" in sys_str:
				hist_name_TTbar = "nom/%s_%s%s"%(self.final_hist_name,self.technique_str ,region )
			else:
				hist_name_TTbar = "%s/%s_%s%s"%(sys_str,self.final_hist_name,self.technique_str ,region )



			#if hist_type   == "TTToHadronicMC": all_combined_TTbar_hist.append( TH2_hist_TTToHadronic  )
			#elif hist_type == "TTToSemiLeptonicMC" : all_combined_TTbar_hist.append( TH2_hist_TTToSemiLeptonic  )
			#elif hist_type == "TTToLeptonicMC": all_combined_TTbar_hist.append( TH2_hist_TTToLeptonic  )


			if "TTTo" in hist_type:
				hist_path = use_filepath + "%s_%s_%sprocessed.root"%(hist_type, self.year, self.WP_str)
				TH2_file = ROOT.TFile.Open(hist_path,"READ")
				TH2_hist = self.clean_histogram(TH2_file.Get(hist_name_TTbar), systematic, hist_type ) 
				all_combined_TTbar_hist.append( TH2_hist  )  #### THESE ARE UNSCALED!!!

			elif hist_type == "":

				TH2_file_TTToHadronic     = ROOT.TFile.Open(hist_path_TTToHadronic,"READ")
				TH2_file_TTToSemiLeptonic = ROOT.TFile.Open(hist_path_TTToSemiLeptonic,"READ")
				TH2_file_TTToLeptonic 	  = ROOT.TFile.Open(hist_path_TTToLeptonic,"READ")

				TH2_hist_TTToHadronic     = self.clean_histogram(TH2_file_TTToHadronic.Get(hist_name_TTbar) , systematic, "TTToHadronicMC" )
				TH2_hist_TTToSemiLeptonic = self.clean_histogram(TH2_file_TTToSemiLeptonic.Get(hist_name_TTbar) , systematic, "TTToSemiLeptonicMC" )
				TH2_hist_TTToLeptonic     = self.clean_histogram(TH2_file_TTToLeptonic.Get(hist_name_TTbar) , systematic, "TTToLeptonicMC" )


				TH2_hist_TTToHadronic.Scale(self.BR_SF_scale*SF_TTToHadronic[self.year])
				TH2_hist_TTToHadronic.SetDirectory(0)   # histograms lose their references when the file destructor is called

				TH2_hist_TTToSemiLeptonic.Scale(self.BR_SF_scale*SF_TTToSemiLeptonic[self.year])
				TH2_hist_TTToSemiLeptonic.SetDirectory(0)   # histograms lose their references when the file destructor is called

				TH2_hist_TTToLeptonic.Scale(self.BR_SF_scale*SF_TTToLeptonic[self.year])
				TH2_hist_TTToLeptonic.SetDirectory(0)   # histograms lose their references when the file destructor is called


				### return the COMBINED histograms

				TH2_hist_TTToHadronic.SetName("combined_TTbar_%s%s"%(self.technique_str ,sys_str))
				TH2_hist_TTToHadronic.SetTitle("combined TTbar MC (%s) (%s) (%s)"%(self.year,region, sys_str))

				TH2_hist_TTToHadronic.Add(TH2_hist_TTToSemiLeptonic)
				TH2_hist_TTToHadronic.Add(TH2_hist_TTToLeptonic)

				all_combined_TTbar_hist.append(TH2_hist_TTToHadronic)
			else: 
				print("ERROR in load_TTTo_hists: hist_type=%s is not correct (options are : '', 'TTToHadronicMC', 'TTToSemiLeptonicMC', and 'TTToLeptonic' )"%hist_type)
				return []
		return all_combined_TTbar_hist  # load in TTbar historam, scale it, and return this version




	def load_ttbar_hist(self,region,systematic, forStats = False, hist_type = ""):
		ROOT.TH1.SetDefaultSumw2()
		ROOT.TH2.SetDefaultSumw2()
		#ROOT.TH2.SetDefaultSumw2()

		use_filepath = self.MC_root_file_home 
		if region in ["SB1b", "SB0b"]: use_filepath	  = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"


		#SF_TTToHadronic= {'2015':0.075592 , '2016':0.05808655696 , '2017':0.06651018525 , '2018': 0.06588049107 }
		#SF_TTToSemiLeptonic= {'2015':0.05395328118 , '2016':0.04236184005 , '2017':0.04264829286 , '2018': 0.04563489275 }
		#SF_TTToLeptonic= {'2015':0.0459517611 , '2016':0.03401684391 , '2017':0.03431532926 , '2018': 0.03617828025 }

		SF_TTJetsMCHT800to1200  = {"2015":0.002884466085,"2016":0.002526405224,"2017":0.003001100916,"2018":0.004897196802}
		SF_TTJetsMCHT1200to2500 = {"2015":0.002722324842,"2016":0.002255554525,"2017":0.00267594799,"2018":0.003918532089}
		SF_TTJetsMCHT2500toInf = {"2015":0.000056798633,"2016":0.000050253843,"2017":0.00005947217,"2018":0.000084089656}

		if forStats:
			SF_TTJetsMCHT800to1200 = {"2015":1,"2016":1,"2017":1,"2018":1}
			SF_TTJetsMCHT1200to2500= {"2015":1,"2016":1,"2017":1,"2018":1}
			SF_TTJetsMCHT2500toInf = {"2015":1,"2016":1,"2017":1,"2018":1}


		#hist_path_TTToHadronic = use_filepath+ "TTToHadronicMC_%s_%sprocessed.root"%(self.year, self.WP_str)
		#hist_path_TTToSemiLeptonic = use_filepath+ "TTToSemiLeptonicMC_%s_%sprocessed.root"%(self.year, self.WP_str)
		#hist_path_TTToLeptonic = use_filepath+ "TTToLeptonicMC_%s_%sprocessed.root"%(self.year, self.WP_str)


		if self.doSideband or self.includeTTJets800to1200: hist_path_TTJetsMCHT800to1200 = use_filepath + "TTJetsMCHT800to1200_%s_%sprocessed.root"%(self.year, self.WP_str)
		hist_path_TTJetsMCHT1200to2500 = use_filepath + "TTJetsMCHT1200to2500_%s_%sprocessed.root"%(self.year, self.WP_str)
		if region not in ["SB1b", "SB0b"] :hist_path_TTJetsMCHT2500toInf  = use_filepath + "TTJetsMCHT2500toInf_%s_%sprocessed.root"%(self.year, self.WP_str)

		sys_suffix = [""]
		if systematic == "nom":
			sys_updown = ["nom"]
		elif "topPt" in systematic:
			sys_updown = ["%s_up"%systematic,"%s_down"%systematic ]
		else:
			sys_updown = ["%s_up"%systematic,"%s_down"%systematic]

		all_combined_TTbar_hist = []
		for sys_str in sys_updown:

			if "topPt" in systematic and "down" in sys_str:
				hist_name_TTbar = "nom/%s_%s%s"%(self.final_hist_name,self.technique_str ,region )
			else:
				hist_name_TTbar = "%s/%s_%s%s"%(sys_str,self.final_hist_name,self.technique_str ,region )


			#if hist_type   == "TTJetsMCHT1200to2500": all_combined_TTbar_hist.append( TH2_hist_TTJetsMCHT1200to2500  )
			#elif hist_type == "TTJetsMCHT2500toInf" and region not in ["SB1b", "SB0b"] : all_combined_TTbar_hist.append( TH2_hist_TTJetsMCHT2500toInf  )
			#elif hist_type == "TTJetsMCHT800to1200" and (self.includeTTJets800to1200 or self.doSideband): all_combined_TTbar_hist.append( TH2_hist_TTJetsMCHT800to1200  )
			
			if "TTJets" in hist_type:
				hist_path = use_filepath + "%s_%s_%sprocessed.root"%(hist_type, self.year, self.WP_str)
				TH2_file = ROOT.TFile.Open(hist_path,"READ")
				TH2_hist = self.clean_histogram(TH2_file.Get(hist_name_TTbar), systematic, hist_type ) 
				all_combined_TTbar_hist.append( TH2_hist  )  #### THESE ARE UNSCALED!!!

			elif hist_type == "":

				TH2_file_TTJetsMCHT1200to2500 = ROOT.TFile.Open(hist_path_TTJetsMCHT1200to2500,"READ")
				if region not in ["SB1b", "SB0b"]: TH2_file_TTJetsMCHT2500toInf  = ROOT.TFile.Open(hist_path_TTJetsMCHT2500toInf,"READ")
				if self.doSideband or self.includeTTJets800to1200: 
					hist_path_TTJetsMCHT800to1200 = use_filepath + "TTJetsMCHT800to1200_%s_%sprocessed.root"%(self.year, self.WP_str)
					TH2_file_TTJetsMCHT800to1200 = ROOT.TFile.Open(hist_path_TTJetsMCHT800to1200,"READ")
					TH2_hist_TTJetsMCHT800to1200  = self.clean_histogram(TH2_file_TTJetsMCHT800to1200.Get(hist_name_TTbar), systematic, "TTJetsMCHT800to1200") 

				TH2_hist_TTJetsMCHT1200to2500 = self.clean_histogram(TH2_file_TTJetsMCHT1200to2500.Get(hist_name_TTbar) , systematic, "TTJetsMCHT1200to2500" )
				if region not in ["SB1b", "SB0b"] :TH2_hist_TTJetsMCHT2500toInf  = self.clean_histogram(TH2_file_TTJetsMCHT2500toInf.Get(hist_name_TTbar), systematic, "TTJetsMCHT2500toInf" )

				TH2_hist_TTJetsMCHT1200to2500.Scale(self.BR_SF_scale*SF_TTJetsMCHT1200to2500[self.year])
				TH2_hist_TTJetsMCHT1200to2500.SetDirectory(0)   # histograms lose their references when the file destructor is called
				if region not in ["SB1b", "SB0b"] :
					TH2_hist_TTJetsMCHT2500toInf.Scale(self.BR_SF_scale*SF_TTJetsMCHT2500toInf[self.year])
					TH2_hist_TTJetsMCHT2500toInf.SetDirectory(0)   # histograms lose their references when the file destructor is called
				else:
					if self.doSideband or self.includeTTJets800to1200: 
						TH2_hist_TTJetsMCHT800to1200.Scale(self.BR_SF_scale*SF_TTJetsMCHT800to1200[self.year])
						TH2_hist_TTJetsMCHT800to1200.SetDirectory(0)   # histograms lose their references when the file destructor is called



				### return the COMBINED histograms

				if region not in ["SB1b", "SB0b"] :TH2_hist_TTJetsMCHT1200to2500.Add(TH2_hist_TTJetsMCHT2500toInf)
				else:
					if self.doSideband or self.includeTTJets800to1200: 
						TH2_hist_TTJetsMCHT1200to2500.Add(TH2_hist_TTJetsMCHT800to1200)
				TH2_hist_TTJetsMCHT1200to2500.SetName("combined_TTbar_%s%s"%(self.technique_str ,sys_str))
				TH2_hist_TTJetsMCHT1200to2500.SetTitle("combined TTbar MC (%s) (%s) (%s)"%(self.year,region, sys_str))
				all_combined_TTbar_hist.append(TH2_hist_TTJetsMCHT1200to2500)
			else: 
				print("ERROR in load_ttbar_hist: hist_type=%s is not correct (options are : '', TTJets800to1200, 'TTJets1200to2500', and 'TTJets2500toInf' )"%hist_type)
				return []
		return all_combined_TTbar_hist  # load in TTbar historam, scale it, and return this version
	def clean_histogram(self,hist,systematic,sample):
		#print("running for sample/year/systematic: %s/%s/%s"%(sample, self.year, systematic))
		ROOT.TH1.AddDirectory(False)
		for iii in range(1, hist.GetNbinsX()+1):
			for jjj in range(1,hist.GetNbinsY()+1):
				if (isnan(hist.GetBinContent(iii,jjj))) or (hist.GetBinContent(iii,jjj) == float("inf")) or (hist.GetBinContent(iii,jjj) == float("-inf")) or ( abs(hist.GetBinContent(iii,jjj))> 1e10) or ( hist.GetBinContent(iii,jjj) < 0 )  :
					print("Bad value in %s for %s/%s, value = %s in bin (%s,%s) of (%s/%s)"%(hist.GetName(), systematic, sample, hist.GetBinContent(iii,jjj), iii, jjj, hist.GetNbinsX(), hist.GetNbinsY()))
					hist.SetBinContent(iii,jjj,0)

		return hist
	
	def load_ST_hists(self,region,systematic, forStats=False, hist_type = ""):
		ROOT.TH2.SetDefaultSumw2()
		ROOT.TH1.SetDefaultSumw2()

		use_filepath = self.MC_root_file_home
		if region in ["SB1b", "SB0b"]: use_filepath	  = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"


		ST_t_channel_top_5f_SF 		= {'2015':0.0409963154,  '2016':0.03607115071, '2017':0.03494669125, '2018': 0.03859114659 }
		ST_t_channel_antitop_5f_SF	= {'2015':0.05673857623, '2016':0.04102705994, '2017':0.04238814865, '2018': 0.03606630944 }
		ST_s_channel_4f_hadrons_SF	= {'2015':0.04668187234, '2016':0.03564988679, '2017':0.03985938616, '2018': 0.04102795437 }
		ST_s_channel_4f_leptons_SF	= {'2015':0.01323030083, '2016':0.01149139097, '2017':0.01117527734, '2018': 0.01155448784 }
		ST_tW_antitop_5f_SF			= {'2015':0.2967888696,  '2016':0.2301666797,  '2017':0.2556495594,  '2018': 0.2700032391  }
		ST_tW_top_5f_SF				= {'2015':0.2962796522,  '2016':0.2355829386,  '2017':0.2563403788,  '2018': 0.2625270613  }

		if forStats:
			ST_t_channel_top_5f_SF 		= {'2015':1,  '2016':1, '2017':1, '2018': 1}
			ST_t_channel_antitop_5f_SF	= {'2015':1, '2016':1, '2017':1, '2018': 1 }
			ST_s_channel_4f_hadrons_SF	= {'2015':1, '2016':19, '2017':1, '2018': 1 }
			ST_s_channel_4f_leptons_SF	= {'2015':1, '2016':1, '2017':1, '2018': 1 }
			ST_tW_antitop_5f_SF			= {'2015':1,  '2016':1,  '2017':1,  '2018': 1  }
			ST_tW_top_5f_SF				= {'2015':1,  '2016':1,  '2017':1,  '2018': 1  }
		
		hist_path_ST_t_channel_top_5f 	  = use_filepath + "ST_t-channel-top_inclMC_%s_%sprocessed.root"%(self.year, self.WP_str)
		hist_path_ST_t_channel_antitop_5f = use_filepath + "ST_t-channel-antitop_inclMC_%s_%sprocessed.root"%(self.year, self.WP_str)
		hist_path_ST_s_channel_4f_hadrons = use_filepath + "ST_s-channel-hadronsMC_%s_%sprocessed.root"%(self.year, self.WP_str)
		hist_path_ST_s_channel_4f_leptons = use_filepath + "ST_s-channel-leptonsMC_%s_%sprocessed.root"%(self.year, self.WP_str)
		hist_path_ST_tW_antitop_5f		  = use_filepath + "ST_tW-antiTop_inclMC_%s_%sprocessed.root"%(self.year, self.WP_str)
		hist_path_ST_tW_top_5f 			  = use_filepath + "ST_tW-top_inclMC_%s_%sprocessed.root"%(self.year, self.WP_str)

		sys_suffix = [""]
		if systematic == "nom":
			sys_updown = ["nom"]
		#elif systematic == "topPt":
		#	sys_updown = ["%s_up"%systematic]
		else:
			sys_updown = ["%s_up"%systematic,"%s_down"%systematic]

		all_combined_ST_hist = []
		for sys_str in sys_updown:

			if "topPt" in systematic and "down" in sys_str:
				hist_name_ST = "nom/%s_%s%s"%(self.final_hist_name,self.technique_str ,region )
			else:
				hist_name_ST = "%s/%s_%s%s"%(sys_str,self.final_hist_name,self.technique_str ,region )


			#if hist_type   == "ST_t-channel-top_inclMC": all_combined_ST_hist.append( TH2_hist_ST_t_channel_top_5f  )
			#elif hist_type == "ST_t-channel-antitop_inclMC": all_combined_ST_hist.append( TH2_hist_ST_t_channel_antitop_5f  )
			#elif hist_type == "ST_s-channel-hadronsMC": all_combined_ST_hist.append( TH2_hist_ST_s_channel_4f_hadrons  )
			#elif hist_type == "ST_s-channel-leptonsMC": all_combined_ST_hist.append( TH2_hist_ST_s_channel_4f_leptons  )
			#lif hist_type == "ST_tW-antiTop_inclMC": all_combined_ST_hist.append( TH2_hist_ST_tW_antitop_5f  )
			#elif hist_type == "ST_tW-top_inclMC": all_combined_ST_hist.append( TH2_hist_ST_tW_top_5f  )

			if "ST_" in hist_type:
				hist_path = use_filepath + "%s_%s_%sprocessed.root"%(hist_type, self.year, self.WP_str)
				TH2_file = ROOT.TFile.Open(hist_path,"READ")
				TH2_hist = self.clean_histogram(TH2_file.Get(hist_name_ST), systematic, hist_type ) 
				all_combined_ST_hist.append( TH2_hist  )  #### THESE ARE UNSCALED!!!

			elif hist_type == "":

				#print("Loading Single top %s/%s/%s"%(region,systematic,self.year))
				TH2_file_ST_t_channel_top_5f 	 = ROOT.TFile.Open(hist_path_ST_t_channel_top_5f,"READ")
				TH2_file_ST_t_channel_antitop_5f = ROOT.TFile.Open(hist_path_ST_t_channel_antitop_5f,"READ")
				TH2_file_ST_s_channel_4f_hadrons = ROOT.TFile.Open(hist_path_ST_s_channel_4f_hadrons,"READ")
				TH2_file_ST_s_channel_4f_leptons = ROOT.TFile.Open(hist_path_ST_s_channel_4f_leptons,"READ")
				TH2_file_ST_tW_antitop_5f 		 = ROOT.TFile.Open(hist_path_ST_tW_antitop_5f,"READ")
				TH2_file_ST_tW_top_5f			 = ROOT.TFile.Open(hist_path_ST_tW_top_5f,"READ")

				#print("file name: %s, hist name: %s"%(hist_path_ST_t_channel_top_5f, hist_name_ST)  )

				TH2_hist_ST_t_channel_top_5f 	 = self.clean_histogram(TH2_file_ST_t_channel_top_5f.Get(hist_name_ST), systematic, "ST_t-channel-top_inclMC" )
				TH2_hist_ST_t_channel_antitop_5f = self.clean_histogram(TH2_file_ST_t_channel_antitop_5f.Get(hist_name_ST), systematic, "ST_t-channel-antitop_inclMC" )
				TH2_hist_ST_s_channel_4f_hadrons = self.clean_histogram(TH2_file_ST_s_channel_4f_hadrons.Get(hist_name_ST), systematic, "ST_s-channel-hadronsMC" )
				TH2_hist_ST_s_channel_4f_leptons = self.clean_histogram(TH2_file_ST_s_channel_4f_leptons.Get(hist_name_ST), systematic, "ST_s-channel-leptonsMC"  )
				TH2_hist_ST_tW_antitop_5f 		 = self.clean_histogram(TH2_file_ST_tW_antitop_5f.Get(hist_name_ST), systematic, "ST_tW-antiTop_inclMC" )
				TH2_hist_ST_tW_top_5f			 = self.clean_histogram(TH2_file_ST_tW_top_5f.Get(hist_name_ST), systematic, "ST_tW-top_inclMC" )

				TH2_hist_ST_t_channel_top_5f.Scale(self.BR_SF_scale*ST_t_channel_top_5f_SF[self.year])
				TH2_hist_ST_t_channel_top_5f.SetDirectory(0)   # histograms lose their references when the file destructor is called

				TH2_hist_ST_t_channel_antitop_5f.Scale(self.BR_SF_scale*ST_t_channel_antitop_5f_SF[self.year])
				TH2_hist_ST_t_channel_antitop_5f.SetDirectory(0)   # histograms lose their references when the file destructor is called

				TH2_hist_ST_s_channel_4f_hadrons.Scale(self.BR_SF_scale*ST_s_channel_4f_hadrons_SF[self.year])
				TH2_hist_ST_s_channel_4f_hadrons.SetDirectory(0)   # histograms lose their references when the file destructor is called
				
				TH2_hist_ST_s_channel_4f_leptons.Scale(self.BR_SF_scale*ST_s_channel_4f_leptons_SF[self.year])
				TH2_hist_ST_s_channel_4f_leptons.SetDirectory(0)   # histograms lose their references when the file destructor is called

				TH2_hist_ST_tW_antitop_5f.Scale(self.BR_SF_scale*ST_tW_antitop_5f_SF[self.year])
				TH2_hist_ST_tW_antitop_5f.SetDirectory(0)   # histograms lose their references when the file destructor is called

				TH2_hist_ST_tW_top_5f.Scale(self.BR_SF_scale*ST_tW_top_5f_SF[self.year])
				TH2_hist_ST_tW_top_5f.SetDirectory(0)   # histograms lose their references when the file destructor is called


				if region in ["SB1b", "SB0b"]: combined_ST_hist = ROOT.TH2F("combined_ST_%s"%region,"combined linearized Single Top (%s) (%s) (%s)"%(self.year,region,sys_str),15 ,0.0, 8000, 12, 0.0, 3000);  
				else: 
					if self.doHTdist: combined_ST_hist = ROOT.TH1F("combined_ST_%s"%(region),"Event H_{T} (%s) (%s) (%s); H_{T} [GeV]; Events / 200 GeV"%(region, hist_type,self.technique_str ),50,0.,10000);
					else: combined_ST_hist = ROOT.TH2F("combined_ST_%s"%region,"combined linearized Single Top (%s) (%s) (%s)"%(self.year,region,sys_str),22,1250., 10000, 20, 500, 5000)
						  
				combined_ST_hist.Add(TH2_hist_ST_t_channel_top_5f)
				combined_ST_hist.Add(TH2_hist_ST_t_channel_antitop_5f)
				combined_ST_hist.Add(TH2_hist_ST_s_channel_4f_hadrons)
				combined_ST_hist.Add(TH2_hist_ST_s_channel_4f_leptons)
				combined_ST_hist.Add(TH2_hist_ST_tW_antitop_5f)
				combined_ST_hist.Add(TH2_hist_ST_tW_top_5f)

				all_combined_ST_hist.append(combined_ST_hist)
			else: 
				print("ERROR in load_ST_hists: hist_type=%s is not correct (options are : '', 'ST_t_channel_top', 'ST_t_channel_antitop', 'ST_s_channel_hadrons', 'ST_s_channel_leptons',  'ST_tW_antitop',  and 'ST_tW_top' )"%hist_type)
				return []
		return all_combined_ST_hist  # load in TTbar historam, scale it, and return this version
	def load_data_hists(self, region, systematic):
		ROOT.TH1.SetDefaultSumw2()
		ROOT.TH2.SetDefaultSumw2()
		#ROOT.TH2.SetDefaultSumw2()
		data_blocks = []
		if self.year == "2015":
			data_blocks = ["dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM","dataF-HIPM"]
		elif self.year == "2016":
			data_blocks = ["dataF", "dataG", "dataH"]
		elif self.year == "2017":
			data_blocks = ["dataB","dataC","dataD","dataE", "dataF"]
		elif self.year == "2018":
			data_blocks = ["dataA","dataB","dataC","dataD"]

		use_filepath = self.MC_root_file_home
		if region in ["SB1b", "SB0b"]: use_filepath	  = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"

		sys_suffix = [""]
		if systematic != "nom":
			sys_updown = ["%s_up"%systematic,"%s_down"%systematic]
		elif systematic == "nom":
			sys_updown = ["nom"]

		all_combined_data_hist = []
		for sys_str in sys_updown:
			#print("Loading data hist %s/%s/%s"%(region,systematic,self.year))

			if region in ["SB1b","SB0b"]: combined_data_hist = ROOT.TH2F("combined_data_%s"%sys_str, ("data events in the %s (%s)"%(year,region)), 15 ,0.0, 8000, 12, 0.0, 3000)
			else:
				if self.doHTdist: combined_data_hist = ROOT.TH1F("combined_data_%s"%(region),"Event H_{T} (data_obs) (%s) (%s) (%s); H_{T} [GeV]; Events / 200 GeV"%(region ,self.technique_str, self.year ),50,0.,10000);
				else: combined_data_hist = ROOT.TH2F("combined_data_%s"%sys_str, ("data events in the %s (%s)"%(region,self.year)), 22,1250., 10000, 20, 500, 5000)
			#JetHT_"+ *dataBlock+"_"+*year+"_%sprocessed.root   -> naming, self.WP_str scheme 
			for data_block in data_blocks:
				#print("Looking for %s/%s/%s/%s"%(data_block,self.year,sys_str,region))
				hist_path_data = use_filepath + "%s_%s_%sprocessed.root"%(data_block,self.year,self.WP_str)
				TH2_file_data = ROOT.TFile.Open(hist_path_data,"READ")
				hist_name_data = "%s_%s%s"%(self.final_hist_name,self.technique_str, region )

				#print("Getting histogram %s from %s"%(hist_name_data,hist_path_data ))
				TH2_hist_data = TH2_file_data.Get(sys_str+"/"+hist_name_data) 
				combined_data_hist.Add(TH2_hist_data)

			ROOT.TH1.AddDirectory(False)
			combined_data_hist.SetDirectory(0)   # histograms lose their references when the file destructor is called
			all_combined_data_hist.append(combined_data_hist)
		return all_combined_data_hist  # load in TTbar historam, scale it, and return this version



	def kill_histograms(self):   ## many histograms to kill ... 

		all_hist_lists = [ self.TTJets1200to2500_hist_SR, self.TTJets2500toInf_hist_SR, self.ST_t_channel_top_hist_SR, 	self.ST_t_channel_antitop_hist_SR, self.ST_s_channel_hadrons_hist_SR, 
		self.ST_s_channel_leptons_hist_SR,   self.ST_tW_antitop_hist_SR, self.ST_tW_top_hist_SR, 	
		 self.TTJets1200to2500_hist_CR, self.TTJets2500toInf_hist_CR, self.ST_t_channel_top_hist_CR, 	self.ST_t_channel_antitop_hist_CR, 
		self.ST_s_channel_hadrons_hist_CR, self.ST_s_channel_leptons_hist_CR,   self.ST_tW_antitop_hist_CR, self.ST_tW_top_hist_CR, 	
		 self.TTJets1200to2500_hist_AT1b, self.TTJets2500toInf_hist_AT1b, 
		self.ST_t_channel_top_hist_AT1b, 	self.ST_t_channel_antitop_hist_AT1b, self.ST_s_channel_hadrons_hist_AT1b, self.ST_s_channel_leptons_hist_AT1b,   self.ST_tW_antitop_hist_AT1b, self.ST_tW_top_hist_AT1b, 	
		self.TTJets1200to2500_hist_AT0b, self.TTJets2500toInf_hist_AT0b, self.ST_t_channel_top_hist_AT0b, 	self.ST_t_channel_antitop_hist_AT0b, self.ST_s_channel_hadrons_hist_AT0b, self.ST_s_channel_leptons_hist_AT0b,   
		self.ST_tW_antitop_hist_AT0b, self.ST_tW_top_hist_AT0b ]
		
		if self.use_QCD_Pt:
			all_hist_lists.extend([
				self.QCDMC_Pt_170to300_hist_SR,
				self.QCDMC_Pt_300to470_hist_SR,
				self.QCDMC_Pt_470to600_hist_SR,
				self.QCDMC_Pt_600to800_hist_SR,
				self.QCDMC_Pt_800to1000_hist_SR,
				self.QCDMC_Pt_1000to1400_hist_SR,
				self.QCDMC_Pt_1400to1800_hist_SR,
				self.QCDMC_Pt_1800to2400_hist_SR,
				self.QCDMC_Pt_2400to3200_hist_SR,
				self.QCDMC_Pt_3200toInf_hist_SR])
		else:
			all_hist_lists.extend([
				self.QCD1000to1500_hist_SR, self.QCD1500to2000_hist_SR, self.QCD2000toInf_hist_SR,
				self.QCD1000to1500_hist_CR, self.QCD1500to2000_hist_CR, self.QCD2000toInf_hist_CR,
				self.QCD1000to1500_hist_AT1b, self.QCD1500to2000_hist_AT1b, self.QCD2000toInf_hist_AT1b,
				self.QCD1000to1500_hist_AT0b, self.QCD1500to2000_hist_AT0b, self.QCD2000toInf_hist_AT0b ])


		for hist_list in all_hist_lists:
			for hist in hist_list:
				del hist

		if self.doATxtb:
			ATxtb_hist_list = [ self.QCD1000to1500_hist_AT1tb, self.QCD1500to2000_hist_AT1tb, self.QCD2000toInf_hist_AT1tb, 
			self.TTJets1200to2500_hist_AT1tb, self.TTJets2500toInf_hist_AT1tb, self.ST_t_channel_top_hist_AT1tb, 	self.ST_t_channel_antitop_hist_AT1tb, self.ST_s_channel_hadrons_hist_AT1tb, self.ST_s_channel_leptons_hist_AT1tb,   
			self.ST_tW_antitop_hist_AT1tb, self.ST_tW_top_hist_AT1tb, 	
			self.QCD1000to1500_hist_AT0tb, self.QCD1500to2000_hist_AT0tb, self.QCD2000toInf_hist_AT0tb, 
			self.TTJets1200to2500_hist_AT0tb, self.TTJets2500toInf_hist_AT0tb, self.ST_t_channel_top_hist_AT0tb, 	self.ST_t_channel_antitop_hist_AT0tb, self.ST_s_channel_hadrons_hist_AT0tb, self.ST_s_channel_leptons_hist_AT0tb,   
			self.ST_tW_antitop_hist_AT0tb, self.ST_tW_top_hist_AT0tb ]
			for hist_list in ATxtb_hist_list:
				for hist in hist_list:
					del hist
		if self.doSideband:
			SB_hist_lists = [ self.QCD1000to1500_hist_SB0b, self.QCD1500to2000_hist_SB0b, self.TTJets800to1200_hist_SB0b, self.TTJets1200to2500_hist_SB0b,  self.ST_t_channel_top_hist_SB0b, 	self.ST_t_channel_antitop_hist_SB0b, self.ST_s_channel_hadrons_hist_SB0b, self.ST_s_channel_leptons_hist_SB0b,   
			self.ST_tW_antitop_hist_SB0b, self.ST_tW_top_hist_SB0b, self.QCD1000to1500_hist_SB1b, self.QCD1500to2000_hist_SB1b, self.TTJets800to1200_hist_SB1b, self.TTJets1200to2500_hist_SB1b,self.ST_t_channel_top_hist_SB1b, 	self.ST_t_channel_antitop_hist_SB1b, self.ST_s_channel_hadrons_hist_SB1b, self.ST_s_channel_leptons_hist_SB1b,   
			self.ST_tW_antitop_hist_SB1b, self.ST_tW_top_hist_SB1b ]
			for hist_list in SB_hist_lists:
				for hist in hist_list:
					del hist
		if self.includeWJets:
			WJets_hists = [  self.WJetsMC_LNu_HT800to1200_SR, self.WJetsMC_LNu_HT1200to2500_SR, self.WJetsMC_LNu_HT2500toInf_SR, self.WJetsMC_QQ_HT800toInf_SR,
			 self.WJetsMC_LNu_HT800to1200_CR, self.WJetsMC_LNu_HT1200to2500_CR, self.WJetsMC_LNu_HT2500toInf_CR, self.WJetsMC_QQ_HT800toInf_CR,
			  self.WJetsMC_LNu_HT800to1200_AT1b, self.WJetsMC_LNu_HT1200to2500_AT1b, self.WJetsMC_LNu_HT2500toInf_AT1b, self.WJetsMC_QQ_HT800toInf_AT1b,
			   self.WJetsMC_LNu_HT800to1200_AT0b, self.WJetsMC_LNu_HT1200to2500_AT0b, self.WJetsMC_LNu_HT2500toInf_AT0b, self.WJetsMC_QQ_HT800toInf_AT0b]

			if self.doSideband: WJets_hists.extend( [ self.WJetsMC_LNu_HT800to1200_SB1b, self.WJetsMC_LNu_HT1200to2500_SB1b, self.WJetsMC_LNu_HT2500toInf_SB1b, self.WJetsMC_QQ_HT800toInf_SB1b, self.WJetsMC_LNu_HT800to1200_SB0b, self.WJetsMC_LNu_HT1200to2500_SB0b, self.WJetsMC_LNu_HT2500toInf_SB0b, self.WJetsMC_QQ_HT800toInf_SB0b    ])
			if self.doATxtb:    WJets_hists.extend( [  self.WJetsMC_LNu_HT800to1200_AT1tb, self.WJetsMC_LNu_HT1200to2500_AT1tb, self.WJetsMC_LNu_HT2500toInf_AT1tb, self.WJetsMC_QQ_HT800toInf_AT1tb, self.WJetsMC_LNu_HT800to1200_AT0tb, self.WJetsMC_LNu_HT1200to2500_AT0tb, self.WJetsMC_LNu_HT2500toInf_AT0tb, self.WJetsMC_QQ_HT800toInf_AT0tb    ])

			for hist_list in WJets_hists:
				for hist in hist_list:
					del hist
		
		if self.includeTTJets800to1200:
			TTJets800to1200_hists = [ self.TTJetsMCHT800to1200_SR,   self.TTJetsMCHT800to1200_CR,  self.TTJetsMCHT800to1200_AT1b,  self.TTJetsMCHT800to1200_AT0b ] 
			if self.doSideband: WJets_hists.extend( [self.TTJetsMCHT800to1200_SB1b, self.TTJetsMCHT800to1200_SB0b] )
			if self.doATxtb:    WJets_hists.extend( [self.TTJetsMCHT800to1200_AT1tb, self.TTJetsMCHT800to1200_AT0tb] )
			for hist_list in TTJets800to1200_hists:
				for hist in hist_list:
					del hist

		if self.includeTTTo:
			TTTo_hists = [ self.TTToHadronicMC_SR, self.TTToSemiLeptonicMC_SR, self.TTToLeptonicMC_SR,  
						    self.TTToHadronicMC_CR, self.TTToSemiLeptonicMC_CR, self.TTToLeptonicMC_CR,
						     self.TTToHadronicMC_AT1b, self.TTToSemiLeptonicMC_AT1b, self.TTToLeptonicMC_AT1b,
						      self.TTToHadronicMC_AT0b, self.TTToSemiLeptonicMC_AT0b, self.TTToLeptonicMC_AT0b  ]

			if self.doSideband: TTTo_hists.extend(   [  self.TTToHadronicMC_SB1b, self.TTToSemiLeptonicMC_SB1b, self.TTToLeptonicMC_SB1b, self.TTToHadronicMC_SB0b, self.TTToSemiLeptonicMC_SB0b, self.TTToLeptonicMC_SB0b]   )
			if self.doATxtb:	TTTo_hists.extend(   [   self.TTToHadronicMC_AT1tb, self.TTToSemiLeptonicMC_AT1tb, self.TTToLeptonicMC_AT1tb, self.TTToHadronicMC_AT0tb, self.TTToSemiLeptonicMC_AT0tb, self.TTToLeptonicMC_AT0tb]   )      
			for hist_list in TTTo_hists:
				for hist in hist_list:
					del hist
		return


	### create superbin 
	def init_HT_dist_superbin_indices(self):

		self.HT_dist_superbins["SR"] = self.QCD1000to1500_hist_SR[0][0].GetNbinsX()*[0]
		self.HT_dist_superbins["AT1b"] = self.QCD1000to1500_hist_SR[0][0].GetNbinsX()*[0]
		if self.doSideband: self.HT_dist_superbins["SB1b"] = self.QCD1000to1500_hist_SR[0][0].GetNbinsX()*[0]

		for iii in range(0,self.QCD1000to1500_hist_SR[0][0].GetNbinsX()):    ## SETS THE BIN INDICES TO BE TRUE TO HISTOGRAM BINNING (1 to nBins+1) _____
			self.HT_dist_superbins["SR"][iii] = [iii+1]
			self.HT_dist_superbins["AT1b"][iii] = [iii+1]
			if self.doSideband: self.HT_dist_superbins["SB1b"][iii] == [iii+1]

	def get_superbin_uncert(self, superbin_num, region):   ## ASSUMES THE BIN INDICES ARE TRUE TO HISTOGRAM BINNING (1 to nBins+1)

		if region == "SR":   
			hist_QCD1000to1500  = self.QCD1000to1500_hist_SR[0][0]
			hist_QCD1500to2000  = self.QCD1500to2000_hist_SR[0][0]
			hist_QCD2000toInf   = self.QCD2000toInf_hist_SR[0][0]
		elif region == "AT1b":
			hist_QCD1000to1500  = self.QCD1000to1500_hist_AT1b[0][0]
			hist_QCD1500to2000  = self.QCD1500to2000_hist_AT1b[0][0]
			hist_QCD2000toInf   = self.QCD2000toInf_hist_AT1b[0][0]
		elif region == "SB1b":
			hist_QCD1000to1500  = self.QCD1000to1500_hist_SB1b[0][0]
			hist_QCD1500to2000  = self.QCD1500to2000_hist_SB1b[0][0]
			hist_QCD2000toInf   = self.QCD2000toInf_hist_SB1b[0][0]
		else: 
			print("ERROR: region %s not recognized (SR, AT1b, or SB1b accepted)."%(region))
			return


		sum_of_weights = 0
		scaled_counts  = 0

		#print("self.HT_dist_superbins is %s"%self.HT_dist_superbins)
		#print("self.HT_dist_superbins[%s] is %s"%(region, self.HT_dist_superbins)    )
		#print("self.HT_dist_superbins[%s][%s] is %s"%(region, superbin_num, self.HT_dist_superbins)  )

		for bin_number in self.HT_dist_superbins[region][superbin_num]:   # this is the looping over the bins in a superbin, this assumes the indices go from 1 - nSuperbins + 1

			#print("Using weights %s/%s/%s"%( return_BR_SF(self.year,"QCDMC1000to1500"),  return_BR_SF(self.year,"QCDMC1500to2000"),  return_BR_SF(self.year,"QCDMC2000toInf")))

			sum_of_weights += hist_QCD1000to1500.GetBinContent(bin_number)*pow( return_BR_SF(self.year,"QCDMC1000to1500"), 2)
			sum_of_weights += hist_QCD1500to2000.GetBinContent(bin_number)*pow( return_BR_SF(self.year,"QCDMC1500to2000"), 2)
			sum_of_weights += hist_QCD2000toInf.GetBinContent(bin_number)* pow( return_BR_SF(self.year,"QCDMC2000toInf" ), 2)

			scaled_counts += hist_QCD1000to1500.GetBinContent(bin_number)*pow( return_BR_SF(self.year,"QCDMC1000to1500"), 1)
			scaled_counts += hist_QCD1500to2000.GetBinContent(bin_number)*pow( return_BR_SF(self.year,"QCDMC1500to2000"), 1)
			scaled_counts += hist_QCD2000toInf.GetBinContent(bin_number) *pow( return_BR_SF(self.year,"QCDMC2000toInf" ), 1)

		#print("sum_of_weights/scaled_counts: %s/%s"%(sum_of_weights,scaled_counts))
		return sqrt(sum_of_weights) / scaled_counts

	def get_scaled_superbin_counts(self, superbin_num, region):   ## ASSUMES THE BIN INDICES ARE TRUE TO HISTOGRAM BINNING (1 to nBins+1)

		if region == "SR":   
			hist_QCD1000to1500  = self.QCD1000to1500_hist_SR[0][0]
			hist_QCD1500to2000  = self.QCD1500to2000_hist_SR[0][0]
			hist_QCD2000toInf   = self.QCD2000toInf_hist_SR[0][0]
		elif region == "AT1b":
			hist_QCD1000to1500  = self.QCD1000to1500_hist_AT1b[0][0]
			hist_QCD1500to2000  = self.QCD1500to2000_hist_AT1b[0][0]
			hist_QCD2000toInf   = self.QCD2000toInf_hist_AT1b[0][0]
		elif region == "SB1b":
			hist_QCD1000to1500  = self.QCD1000to1500_hist_SB1b[0][0]
			hist_QCD1500to2000  = self.QCD1500to2000_hist_SB1b[0][0]
			hist_QCD2000toInf   = self.QCD2000toInf_hist_SB1b[0][0]
		else: 
			print("ERROR: region %s not recognized (SR, AT1b, or SB1b accepted)."%(region))
			return

		scaled_counts  = 0

		#print("self.HT_dist_superbins is %s"%self.HT_dist_superbins)
		#print("self.HT_dist_superbins[%s] is %s"%(region, self.HT_dist_superbins)    )
		#print("self.HT_dist_superbins[%s][%s] is %s"%(region, superbin_num, self.HT_dist_superbins)  )


		for bin_number in self.HT_dist_superbins[region][superbin_num]:   # this is the looping over the bins in a superbin, this assumes the indices go from 1 - nSuperbins + 1
			#print("bin number is %s."%(bin_number))

			scaled_counts += hist_QCD1000to1500.GetBinContent(bin_number)*pow( return_BR_SF(self.year,"QCDMC1000to1500"), 1)
			scaled_counts += hist_QCD1500to2000.GetBinContent(bin_number)*pow( return_BR_SF(self.year,"QCDMC1500to2000"), 1)
			scaled_counts += hist_QCD2000toInf.GetBinContent(bin_number)*pow( return_BR_SF(self.year,"QCDMC2000toInf")  , 1)

		return scaled_counts




	def get_unscaled_superbin_counts(self, superbin_num, region):   ## ASSUMES THE BIN INDICES ARE TRUE TO HISTOGRAM BINNING (1 to nBins+1)

		if region == "SR":   
			hist_QCD1000to1500  = self.QCD1000to1500_hist_SR[0][0]
			hist_QCD1500to2000  = self.QCD1500to2000_hist_SR[0][0]
			hist_QCD2000toInf   = self.QCD2000toInf_hist_SR[0][0]
		elif region == "AT1b":
			hist_QCD1000to1500  = self.QCD1000to1500_hist_AT1b[0][0]
			hist_QCD1500to2000  = self.QCD1500to2000_hist_AT1b[0][0]
			hist_QCD2000toInf   = self.QCD2000toInf_hist_AT1b[0][0]
		elif region == "SB1b":
			hist_QCD1000to1500  = self.QCD1000to1500_hist_SB1b[0][0]
			hist_QCD1500to2000  = self.QCD1500to2000_hist_SB1b[0][0]
			hist_QCD2000toInf   = self.QCD2000toInf_hist_SB1b[0][0]
		else: 
			print("ERROR: region %s not recognized (SR, AT1b, or SB1b accepted)."%(region))
			return

		scaled_counts  = 0

		for bin_number in self.HT_dist_superbins[region][superbin_num]:   # this is the looping over the bins in a superbin, this assumes the indices go from 1 - nSuperbins + 1
			#print("bin number is %s."%(bin_number))

			scaled_counts += hist_QCD1000to1500.GetBinContent(bin_number)
			scaled_counts += hist_QCD1500to2000.GetBinContent(bin_number)
			scaled_counts += hist_QCD2000toInf.GetBinContent(bin_number)

		return scaled_counts



	## get list of bad bins (bins with stat uncertainty greater than 0.2 or yield of 0)
	def get_bad_bins(self, region):
		bad_bins = []

		# loop over superbins and create a list of bad superbins if stat uncertainty is too large or yield is 0
		for superbin_num in range(0, len(self.HT_dist_superbins[region]) ):
			#print("The scaled superbin count for bin %s is %s."%(superbin_num,self.get_scaled_superbin_counts(superbin_num, region)))
			#print(" self.get_scaled_superbin_counts(superbin_num, region) < 1e-10: %s"%( self.get_scaled_superbin_counts(superbin_num, region) < 1e-10))
			if self.get_scaled_superbin_counts(superbin_num, region) < 1e-10: 
				#print("Bin %s is bad due to counts: %s"%(superbin_num, self.get_scaled_superbin_counts(superbin_num, region)))
				bad_bins.append(superbin_num)
			elif self.get_superbin_uncert(superbin_num,region) > self.HT_dist_min_stat_uncert: 
				#print("Bin %s is bad due to stat uncert: %s"%(superbin_num, self.get_superbin_uncert(superbin_num,region)))

				bad_bins.append(superbin_num)

		#print("bad bins are %s."%(bad_bins))
		return bad_bins


	def there_are_bad_bins(self, region):
		return len(self.get_bad_bins(region)) > 0


	## merge with neighbor superbin with the highest stat uncertainty
	def highest_stat_uncertainty_neighbor(self, superbin_num, region ):

		highest_stat_uncert_value = -9999
		highest_stat_uncert_bin_num = -9999

		superbin_stat_uncert = dict()

		if superbin_num == 0: 
			return 1
		elif ( superbin_num + 1) == len(self.HT_dist_superbins[region]): 
			return (superbin_num - 1)
		else:
			if self.get_scaled_superbin_counts( superbin_num + 1, region   ) < 1e-10: superbin_stat_uncert[superbin_num + 1] = 5.0
			else: superbin_stat_uncert[superbin_num + 1] = self.get_superbin_uncert( superbin_num + 1, region )

			if self.get_scaled_superbin_counts( superbin_num - 1, region   ) < 1e-10: superbin_stat_uncert[superbin_num - 1] = 5.0
			else: superbin_stat_uncert[superbin_num - 1] = self.get_superbin_uncert( superbin_num - 1, region )
			
		highest_stat_uncert_bin_num = max(superbin_stat_uncert, key=superbin_stat_uncert.get)

		return highest_stat_uncert_bin_num


	def merge_HT_dist_superbin_indices(self):  

		random.seed(123456)

		counter = 1
		while self.there_are_bad_bins("SR") :


			bin_indices = list(  self.HT_dist_superbins["SR"]  )
			counter+=1 

			#print("=============================== Beginning SR merge round %s ================================. "%counter)
			#print("The current superbins are %s"%(bin_indices))

			## get list of bad bins
			bad_bins = self.get_bad_bins("SR")

			#print("Got bad bins.")
			## choose random bad bin
			random_superbin = random.choice(bad_bins)
			#print("Chose random superbin #%s: %s"%(random_superbin, bin_indices[random_superbin]))


			## merge with neighbor superbin with the highest stat uncertainty
			#print("Finding neighbor to merge with.")
			neighbor_index_to_merge = self.highest_stat_uncertainty_neighbor(random_superbin, "SR")
			#print("-----      Superbins for %s:    %s"%("SR", bin_indices))
			#print("#####      Will merge with neighbor bin #%s: %s"%( neighbor_index_to_merge, bin_indices[neighbor_index_to_merge]))
			#print("@@@@@      Then will remove %s."%bin_indices[neighbor_index_to_merge])

			"""
			for superbin_num in range(0,len(bin_indices)):
				if self.get_scaled_superbin_counts(superbin_num,"SR") > 0:
					print("Bin %s has yield %s and stat uncertainty %s."%(superbin_num, self.get_scaled_superbin_counts(superbin_num,"SR"),   self.get_superbin_uncert(superbin_num,"SR") ))
				else:
					print("Bin %s has yield %s and stat uncertainty 1 (from dividing by 0)."%(superbin_num, self.get_scaled_superbin_counts(superbin_num,"SR")))"""

			bin_indices[random_superbin].extend(  bin_indices[neighbor_index_to_merge]  )
			bin_indices.remove( bin_indices[neighbor_index_to_merge]  )


			#print("-------- SR: Merged bins %s and %s. Superbin indices now has length %s."%(random_superbin, neighbor_index_to_merge, len(bin_indices)))
			#print("Then removed %s."%bin_indices[neighbor_index_to_merge])
			#print("Superbin indices now look like: %s"%(bin_indices))
			## set new superbin index list for SR
			self.HT_dist_superbins["SR"]  =  bin_indices
 		


 		print("")
  		print("")
 		print("")
 		print("")
 		print("")
 		print("")
 		print("")

		print("merged SR HT bins.")
		random.seed(123456)

		counter =1 
		while self.there_are_bad_bins("AT1b") :
			bin_indices = list(  self.HT_dist_superbins["AT1b"]  )
			counter+=1 

			bad_bins = self.get_bad_bins("AT1b")
			random_superbin = random.choice(bad_bins)
			neighbor_index_to_merge = self.highest_stat_uncertainty_neighbor(random_superbin, "AT1b")
			bin_indices[random_superbin].extend(  bin_indices[neighbor_index_to_merge]  )
			bin_indices.remove( bin_indices[neighbor_index_to_merge]  )
			self.HT_dist_superbins["AT1b"]  =  bin_indices
 
 		#print("merged AT1b HT bins.")

		random.seed(123456)
		counter = 1
		if self.doSideband:
			while self.there_are_bad_bins("SB1b") :
				bin_indices = list(  self.HT_dist_superbins["SB1b"]  )
				counter+=1 

				bad_bins = self.get_bad_bins("SB1b")
				random_superbin = random.choice(bad_bins)
				neighbor_index_to_merge = self.highest_stat_uncertainty_neighbor(random_superbin, "SB1b")
				bin_indices[random_superbin].extend(  bin_indices[neighbor_index_to_merge]  )
				bin_indices.remove( bin_indices[neighbor_index_to_merge]  )
				self.HT_dist_superbins["SB1b"]  =  bin_indices
		#print("merged SB1B HT bins.")
		return

	def print_superbins(self):
		print("-------- SR bins ----------")
		for iii in range(0, len(self.HT_dist_superbins["SR"])):
			print("Superbin %s: %s scaled counts, %s unscaled counts, %s stat uncertainty."%(iii, self.get_scaled_superbin_counts( iii, "SR" ), self.get_unscaled_superbin_counts(iii, "SR"), self.get_superbin_uncert(iii, "SR")   ))
		print("")
		print("")
		print("")
		print("")
		print("-------- AT1b bins ----------")
		for iii in range(0, len(self.HT_dist_superbins["AT1b"])):
			print("Superbin %s: %s scaled counts, %s unscaled counts, %s stat uncertainty."%(iii, self.get_scaled_superbin_counts( iii, "AT1b" ), self.get_unscaled_superbin_counts(iii, "AT1b"), self.get_superbin_uncert(iii, "AT1b")   ))

		return

	def return_formatted_summary_str(self):

	 	BR_SFs = return_BR_SF()

		total_BR = sum([self.QCD1000to1500_hist_SR[0][0].Integral()*BR_SFs["QCDMC1000to1500"][self.year], self.QCD1500to2000_hist_SR[0][0].Integral()*BR_SFs["QCDMC1500to2000"][self.year], self.QCD2000toInf_hist_SR[0][0].Integral()*BR_SFs["QCDMC2000toInf"][self.year],

			self.ST_t_channel_top_hist_SR[0][0].Integral()*BR_SFs["ST_t_channel_top_inclMC"][self.year], 
			self.ST_t_channel_antitop_hist_SR[0][0].Integral()*BR_SFs["ST_t-channel-antitop_inclMC_incMC"][self.year], 
			self.ST_s_channel_hadrons_hist_SR[0][0].Integral()*BR_SFs["ST_s-channel-hadronsMCMC"][self.year], 
			self.ST_s_channel_leptons_hist_SR[0][0].Integral()*BR_SFs["ST_s-channel-leptonsMCMC"][self.year], 
			self.ST_tW_antitop_hist_SR[0][0].Integral()*BR_SFs["ST_tW-antiTop_inclMC_inclMC"][self.year], 
			self.ST_tW_top_hist_SR[0][0].Integral()*BR_SFs["ST_tW-top_inclMC_inclMC"][self.year], 

			self.TTToHadronicMC_SR[0][0].Integral()*BR_SFs["TTToHadronicMC"][self.year], 
			self.TTToSemiLeptonicMC_SR[0][0].Integral()*BR_SFs["TTToSemiLeptonicMC"][self.year], 
			self.TTToLeptonicMC_SR[0][0].Integral()*BR_SFs["TTToLeptonicMC"][self.year], 

			self.WJetsMC_LNu_HT800to1200_SR[0][0].Integral()*BR_SFs["WJetsMC_LNu-HT800to1200"][self.year], 
			self.WJetsMC_LNu_HT1200to2500_SR[0][0].Integral()*BR_SFs["WJetsMC_LNu-HT1200to2500"][self.year], 
			self.WJetsMC_LNu_HT2500toInf_SR[0][0].Integral()*BR_SFs["WJetsMC_LNu-HT2500toInf"][self.year], 
			self.WJetsMC_QQ_HT800toInf_SR[0][0].Integral()*BR_SFs["WJetsMC_QQ-HT800toInf"][self.year] ]  )

		summary_str = "%s"%(total_BR )

		return summary_str

	def return_formatted_AT1b_summary_str(self):

	 	BR_SFs = return_BR_SF()

		total_BR = sum([self.QCD1000to1500_hist_AT1b[0][0].Integral()*BR_SFs["QCDMC1000to1500"][self.year], self.QCD1500to2000_hist_AT1b[0][0].Integral()*BR_SFs["QCDMC1500to2000"][self.year], self.QCD2000toInf_hist_AT1b[0][0].Integral()*BR_SFs["QCDMC2000toInf"][self.year],

			self.ST_t_channel_top_hist_AT1b[0][0].Integral()*BR_SFs["ST_t_channel_top_inclMC"][self.year], 
			self.ST_t_channel_antitop_hist_AT1b[0][0].Integral()*BR_SFs["ST_t-channel-antitop_inclMC_incMC"][self.year], 
			self.ST_s_channel_hadrons_hist_AT1b[0][0].Integral()*BR_SFs["ST_s-channel-hadronsMCMC"][self.year], 
			self.ST_s_channel_leptons_hist_AT1b[0][0].Integral()*BR_SFs["ST_s-channel-leptonsMCMC"][self.year], 
			self.ST_tW_antitop_hist_AT1b[0][0].Integral()*BR_SFs["ST_tW-antiTop_inclMC_inclMC"][self.year], 
			self.ST_tW_top_hist_AT1b[0][0].Integral()*BR_SFs["ST_tW-top_inclMC_inclMC"][self.year], 

			self.TTToHadronicMC_AT1b[0][0].Integral()*BR_SFs["TTToHadronicMC"][self.year], 
			self.TTToSemiLeptonicMC_AT1b[0][0].Integral()*BR_SFs["TTToSemiLeptonicMC"][self.year], 
			self.TTToLeptonicMC_AT1b[0][0].Integral()*BR_SFs["TTToLeptonicMC"][self.year], 

			self.WJetsMC_LNu_HT800to1200_AT1b[0][0].Integral()*BR_SFs["WJetsMC_LNu-HT800to1200"][self.year], 
			self.WJetsMC_LNu_HT1200to2500_AT1b[0][0].Integral()*BR_SFs["WJetsMC_LNu-HT1200to2500"][self.year], 
			self.WJetsMC_LNu_HT2500toInf_AT1b[0][0].Integral()*BR_SFs["WJetsMC_LNu-HT2500toInf"][self.year], 
			self.WJetsMC_QQ_HT800toInf_AT1b[0][0].Integral()*BR_SFs["WJetsMC_QQ-HT800toInf"][self.year] ]  )

		summary_str = "%s"%(total_BR )

		return summary_str


