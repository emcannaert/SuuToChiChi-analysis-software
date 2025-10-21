import sys,os,time
import numpy as np
import ROOT
import ast
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from return_signal_SF import return_signal_SF
from math import sqrt
from write_cms_text import write_cms_text
import argparse
from return_BR_SF.return_BR_SF import return_BR_SF
import random
from histLoaderSelectionStudier.histLoaderSelectionStudier import histLoaderSelectionStudier

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

	def __init__(self, year, mass_point, technique_str, all_BR_hists,  use_QCD_Pt=False, useMask=False, use_1b_bin_maps = False,run_from_eos = False, WP=None ,debug=False):

		self.c = ROOT.TCanvas("","",1200,1000)
		self.BR_SF_scale = 1.0
		self.sig_SF_scale = 1.0
		self.technique_str = technique_str
		self.year   = year
		self.run_from_eos = run_from_eos
		self.debug = debug
		self.use_1b_bin_maps = use_1b_bin_maps
		self.use_QCD_Pt = use_QCD_Pt

		self.useMask = useMask

		self.WP = WP

		self.MC_root_file_home	  = 	os.getenv('CMSSW_BASE') + "/src/SuuToChiChi_analysis_software/combinedROOT/selectionStudy/%s/"%WP
		self.data_root_file_home	=   os.getenv('CMSSW_BASE') + "/src/SuuToChiChi_analysis_software/combinedROOT/selectionStudy/%s/"%WP

		if "ET" in self.WP:
			self.MC_root_file_home	  = 	os.getenv('CMSSW_BASE') + "/src/SuuToChiChi_analysis_software/combinedROOT/selectionStudy/%s/"%WP
			self.data_root_file_home	=   os.getenv('CMSSW_BASE') + "/src/SuuToChiChi_analysis_software/combinedROOT/selectionStudy/%s/"%WP


		self.use_QCD_Pt_str = "QCDHT"
		if self.use_QCD_Pt: self.use_QCD_Pt_str = "QCDPT"

		self.eos_path = "root://cmseos.fnal.gov/"
		self.HT_distr_home = "/HT_distributions" # extra folder where output files are saved for HT distribution plots

		if self.run_from_eos:		## grab files from eos if they are not stored locally

			print("Using files stored on EOS.")
			self.MC_root_file_home	    =  self.eos_path + "/store/user/ecannaer/processedFiles/"
			self.data_root_file_home	=  self.eos_path + "/store/user/ecannaer/processedFiles/"



		if "ET" in self.WP:
			self.final_hist_name = "h_MSJ_mass_vs_MdSJ_"

		### sample inclusion options
		#self.includeWJets =           all_BR_hists.includeWJets
		#self.includeTTTo  =			  all_BR_hists.includeTTTo
		#self.includeTTJets800to1200 = all_BR_hists.includeTTJets800to1200




		self.index_file_home  = os.getenv('CMSSW_BASE') + "/src/SuuToChiChi_analysis_software/postprocess/binMaps/selectionStudy/%s/"%WP

		self.output_file_home	= os.getenv('CMSSW_BASE') + "/src/SuuToChiChi_analysis_software/postprocess/selectionStudy//finalCombineFilesNewStats/%s/%s/"%(self.use_QCD_Pt_str,self.WP)
		self.final_plot_home	 = os.getenv('CMSSW_BASE') + "/src/SuuToChiChi_analysis_software/postprocess/plots/selectionStudy/finalCombinePlots/%s/%s/"%(self.use_QCD_Pt_str,self.WP)

		if not os.path.exists(self.output_file_home):
			os.mkdir(self.output_file_home) 
		if not os.path.exists(self.final_plot_home):
			os.mkdir(self.final_plot_home) 



		self.create_directories()  ## make sure all above directories exist


		self.superbin_indices			  	  =   {region:self.load_superbin_indices(region) for region in ["postbTag","postSJTag"] }  

		if self.debug:																															

			self.output_file_home	= os.getenv('CMSSW_BASE') + "/src/SuuToChiChi_analysis_software/postprocess/selectionStudy/finalCombineFilesNewStats/test/"



		self.mass_point = mass_point   # label for the signal mass point

		self.data_systematics 	   = ["nom"]
		self.data_systematic_names = ["nom"]



		self.systematics 	  = ["nom",     "JEC",    	 "bTagSF_med"	  ]   ## systematic namings as used in analyzer	 "bTagSF",    "PUSF",
		self.systematic_names = ["nom",   "CMS_jec",    "CMS_bTagSF_M"   ]  ## systematic namings for cards   "CMS_btagSF",   "CMS_pu", 



		self.uncorrelated_systematics = [ "CMS_jec", "CMS_jer","CMS_jer_eta193", "CMS_jer_193eta25", "CMS_L1Prefiring","CMS_bTagSF_M", "CMS_bTagSF_T", "CMS_bTagSF_bc_T_year", "CMS_bTagSF_light_T_year", "CMS_bTagSF_bc_M_year","CMS_bTagSF_light_M_year", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year", "CMS_jec_RelativeSample_year"] ## systematics that are correlated (will not have year appended to names)	 "CMS_btagSF",
			## removed from uncorrelated uncertainties :  "CMS_pu"

		### HT bin stuff

		### individual bins for SR




		if self.use_QCD_Pt:
			#self.QCDMC_Pt_170to300_hist_postbTag 		= all_BR_hists.QCDMC_Pt_170to300_hist_postbTag
			self.QCDMC_Pt_300to470_hist_postbTag 		= all_BR_hists.QCDMC_Pt_300to470_hist_postbTag
			self.QCDMC_Pt_470to600_hist_postbTag 		= all_BR_hists.QCDMC_Pt_470to600_hist_postbTag
			self.QCDMC_Pt_600to800_hist_postbTag 		= all_BR_hists.QCDMC_Pt_600to800_hist_postbTag
			self.QCDMC_Pt_800to1000_hist_postbTag 	= all_BR_hists.QCDMC_Pt_800to1000_hist_postbTag
			self.QCDMC_Pt_1000to1400_hist_postbTag 	= all_BR_hists.QCDMC_Pt_1000to1400_hist_postbTag
			self.QCDMC_Pt_1400to1800_hist_postbTag 	= all_BR_hists.QCDMC_Pt_1400to1800_hist_postbTag
			self.QCDMC_Pt_1800to2400_hist_postbTag 	= all_BR_hists.QCDMC_Pt_1800to2400_hist_postbTag
			self.QCDMC_Pt_2400to3200_hist_postbTag 	= all_BR_hists.QCDMC_Pt_2400to3200_hist_postbTag
			self.QCDMC_Pt_3200toInf_hist_postbTag 	= all_BR_hists.QCDMC_Pt_3200toInf_hist_postbTag


			#self.QCDMC_Pt_170to300_hist_postSJTag 		= all_BR_hists.QCDMC_Pt_170to300_hist_postSJTag
			self.QCDMC_Pt_300to470_hist_postSJTag 		= all_BR_hists.QCDMC_Pt_300to470_hist_postSJTag
			self.QCDMC_Pt_470to600_hist_postSJTag 		= all_BR_hists.QCDMC_Pt_470to600_hist_postSJTag
			self.QCDMC_Pt_600to800_hist_postSJTag 		= all_BR_hists.QCDMC_Pt_600to800_hist_postSJTag
			self.QCDMC_Pt_800to1000_hist_postSJTag 	= all_BR_hists.QCDMC_Pt_800to1000_hist_postSJTag
			self.QCDMC_Pt_1000to1400_hist_postSJTag 	= all_BR_hists.QCDMC_Pt_1000to1400_hist_postSJTag
			self.QCDMC_Pt_1400to1800_hist_postSJTag 	= all_BR_hists.QCDMC_Pt_1400to1800_hist_postSJTag
			self.QCDMC_Pt_1800to2400_hist_postSJTag 	= all_BR_hists.QCDMC_Pt_1800to2400_hist_postSJTag
			self.QCDMC_Pt_2400to3200_hist_postSJTag 	= all_BR_hists.QCDMC_Pt_2400to3200_hist_postSJTag
			self.QCDMC_Pt_3200toInf_hist_postSJTag 	= all_BR_hists.QCDMC_Pt_3200toInf_hist_postSJTag


			for iii in range(len(self.systematics)):
				if self.debug:
					if iii > 0:

						print("--------- IN LINEARIZER: QCD integrals for systematic %s --------"%self.systematics[iii])
						print("------ self.QCDMC_Pt_300to470_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_300to470_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_300to470_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_300to470_hist_postbTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_470to600_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_470to600_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_470to600_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_470to600_hist_postbTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_600to800_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_600to800_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_600to800_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_600to800_hist_postbTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_800to1000_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_800to1000_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_800to1000_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_800to1000_hist_postbTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_1000to1400_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_1000to1400_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_1000to1400_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_1000to1400_hist_postbTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_1400to1800_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_1400to1800_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_1400to1800_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_1400to1800_hist_postbTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_1800to2400_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_1800to2400_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_1800to2400_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_1800to2400_hist_postbTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_2400to3200_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_2400to3200_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_2400to3200_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_2400to3200_hist_postbTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_3200toInf_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_3200toInf_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_3200toInf_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_3200toInf_hist_postbTag[iii][1].Integral())) 

						print("--------- IN LINEARIZER: QCD integrals for systematic %s --------"%self.systematics[iii])
						print("------ self.QCDMC_Pt_300to470_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_300to470_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_300to470_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_300to470_hist_postSJTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_470to600_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_470to600_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_470to600_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_470to600_hist_postSJTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_600to800_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_600to800_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_600to800_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_600to800_hist_postSJTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_800to1000_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_800to1000_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_800to1000_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_800to1000_hist_postSJTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_1000to1400_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_1000to1400_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_1000to1400_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_1000to1400_hist_postSJTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_1400to1800_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_1400to1800_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_1400to1800_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_1400to1800_hist_postSJTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_1800to2400_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_1800to2400_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_1800to2400_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_1800to2400_hist_postSJTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_2400to3200_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_2400to3200_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_2400to3200_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_2400to3200_hist_postSJTag[iii][1].Integral())) 
						print("------ self.QCDMC_Pt_3200toInf_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_3200toInf_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_3200toInf_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_3200toInf_hist_postSJTag[iii][1].Integral())) 



		else:
			self.QCD1000to1500_hist_postbTag 	= all_BR_hists.QCD1000to1500_hist_postbTag
			self.QCD1500to2000_hist_postbTag 	= all_BR_hists.QCD1500to2000_hist_postbTag
			self.QCD2000toInf_hist_postbTag 	= all_BR_hists.QCD2000toInf_hist_postbTag

			self.QCD1000to1500_hist_postSJTag 	= all_BR_hists.QCD1000to1500_hist_postSJTag
			self.QCD1500to2000_hist_postSJTag 	= all_BR_hists.QCD1500to2000_hist_postSJTag
			self.QCD2000toInf_hist_postSJTag 	= all_BR_hists.QCD2000toInf_hist_postSJTag


		self.TTJets1200to2500_hist_postbTag 	= all_BR_hists.TTJets1200to2500_hist_postbTag
		self.TTJets2500toInf_hist_postbTag 	= all_BR_hists.TTJets2500toInf_hist_postbTag

		self.TTJets1200to2500_hist_postSJTag 	= all_BR_hists.TTJets1200to2500_hist_postSJTag
		self.TTJets2500toInf_hist_postSJTag 	= all_BR_hists.TTJets2500toInf_hist_postSJTag


		self.signal_WBWB_hist_postbTag = []
		self.signal_HTHT_hist_postbTag = []
		self.signal_ZTZT_hist_postbTag = []
		self.signal_WBHT_hist_postbTag = []
		self.signal_WBZT_hist_postbTag = []
		self.signal_HTZT_hist_postbTag = []

		self.signal_WBWB_hist_postSJTag = []
		self.signal_HTHT_hist_postSJTag = []
		self.signal_ZTZT_hist_postSJTag = []
		self.signal_WBHT_hist_postSJTag = []
		self.signal_WBZT_hist_postSJTag = []
		self.signal_HTZT_hist_postSJTag = []


		if self.debug:
			print("Loading signal histograms.")

		# load signal hists 
		for iii,systematic in enumerate(self.systematics):
			self.signal_WBWB_hist_postbTag.append(self.load_signal_hist(systematic , "postbTag", "WBWB"))
			self.signal_HTHT_hist_postbTag.append(self.load_signal_hist(systematic , "postbTag","HTHT"))
			self.signal_ZTZT_hist_postbTag.append(self.load_signal_hist(systematic , "postbTag","ZTZT"))
			self.signal_WBHT_hist_postbTag.append(self.load_signal_hist(systematic , "postbTag","WBHT"))
			self.signal_WBZT_hist_postbTag.append(self.load_signal_hist(systematic , "postbTag","WBZT"))
			self.signal_HTZT_hist_postbTag.append(self.load_signal_hist(systematic , "postbTag","HTZT"))

			self.signal_WBWB_hist_postSJTag.append(self.load_signal_hist(systematic , "postSJTag", "WBWB"))
			self.signal_HTHT_hist_postSJTag.append(self.load_signal_hist(systematic , "postSJTag", "HTHT"))
			self.signal_ZTZT_hist_postSJTag.append(self.load_signal_hist(systematic , "postSJTag", "ZTZT"))
			self.signal_WBHT_hist_postSJTag.append(self.load_signal_hist(systematic , "postSJTag", "WBHT"))
			self.signal_WBZT_hist_postSJTag.append(self.load_signal_hist(systematic , "postSJTag", "WBZT"))
			self.signal_HTZT_hist_postSJTag.append(self.load_signal_hist(systematic , "postSJTag", "HTZT"))

			if self.debug:
				print("For systematic, %s, 2D signal WBWB/HTHT/ZTZT/WBHT/WBZT/HTZT integrals BEFORE scaling are: "%systematic)
				print("postbTag WBWB: %s"%(self.signal_WBWB_hist_postbTag[iii][0].Integral() )) ## only showing the up / nom uncertainty
				print("postbTag HTHT: %s"%(self.signal_HTHT_hist_postbTag[iii][0].Integral()  ))
				print("postbTag ZTZT: %s"%(self.signal_ZTZT_hist_postbTag[iii][0].Integral()  ))
				print("postbTag WBHT: %s"%(self.signal_WBHT_hist_postbTag[iii][0].Integral()  ))
				print("postbTag WBZT: %s"%(self.signal_WBZT_hist_postbTag[iii][0].Integral() ))
				print("postbTag HTZT: %s"%(self.signal_HTZT_hist_postbTag[iii][0].Integral() ))

				print("postSJTag WBWB: %s"%(self.signal_WBWB_hist_postSJTag[iii][0].Integral() )) ## only showing the up / nom uncertainty
				print("postSJTag HTHT: %s"%(self.signal_HTHT_hist_postSJTag[iii][0].Integral()  ))
				print("postSJTag ZTZT: %s"%(self.signal_ZTZT_hist_postSJTag[iii][0].Integral()  ))
				print("postSJTag WBHT: %s"%(self.signal_WBHT_hist_postSJTag[iii][0].Integral()  ))
				print("postSJTag WBZT: %s"%(self.signal_WBZT_hist_postSJTag[iii][0].Integral() ))
				print("postSJTag HTZT: %s"%(self.signal_HTZT_hist_postSJTag[iii][0].Integral() ))

		self.QCD_linear_postbTag    = []
		self.TTbar_linear_postbTag  = []
		self.signal_linear_postbTag = []

		self.QCD_linear_postSJTag 	 = []
		self.TTbar_linear_postSJTag  = []
		self.signal_linear_postSJTag = []




		if self.debug:
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


			if self.debug: 
				if not self.use_QCD_Pt:  print("iii / systematic are %s / %s, QCD1000to1500_hist_postbTag has length %s,  QCD1500to2000_hist_postbTag has length %s, QCD2000toInf_hist_postbTag has length %s."%(iii, systematic, len(self.QCD1000to1500_hist_postbTag),len(self.QCD1500to2000_hist_postbTag),len(self.QCD2000toInf_hist_postbTag))  )
				else:  print("iii / systematic are %s / %s, QCDMC_Pt_470to600_hist_postbTag has length %s,  QCDMC_Pt_600to800_hist_postbTag has length %s, QCDMC_Pt_800to1000_hist_postbTag has length %s."%(iii, systematic, len(self.QCDMC_Pt_470to600_hist_postbTag),len(self.QCDMC_Pt_600to800_hist_postbTag),len(self.QCDMC_Pt_800to1000_hist_postbTag))  )
				
				if not self.use_QCD_Pt:  print("iii / systematic are %s / %s, QCD1000to1500_hist_postSJTag has length %s,  QCD1500to2000_hist_postSJTag has length %s, QCD2000toInf_hist_postSJTag has length %s."%(iii, systematic, len(self.QCD1000to1500_hist_postSJTag),len(self.QCD1500to2000_hist_postSJTag),len(self.QCD2000toInf_hist_postSJTag))  )
				else:  print("iii / systematic are %s / %s, QCDMC_Pt_470to600_hist_postSJTag has length %s,  QCDMC_Pt_600to800_hist_postSJTag has length %s, QCDMC_Pt_800to1000_hist_postSJTag has length %s."%(iii, systematic, len(self.QCDMC_Pt_470to600_hist_postSJTag),len(self.QCDMC_Pt_600to800_hist_postSJTag),len(self.QCDMC_Pt_800to1000_hist_postSJTag))  )



			if "renorm" in systematic or "fact" in systematic: sample_type = "_QCD"
			if self.use_QCD_Pt:
				self.QCD_linear_postbTag.append(self.linearize_plot([],"QCD", "postbTag",  systematic + sample_type + year_str,"QCD", [ self.QCDMC_Pt_300to470_hist_postbTag[iii],  self.QCDMC_Pt_470to600_hist_postbTag[iii], self.QCDMC_Pt_600to800_hist_postbTag[iii], self.QCDMC_Pt_800to1000_hist_postbTag[iii], self.QCDMC_Pt_1000to1400_hist_postbTag[iii], self.QCDMC_Pt_1400to1800_hist_postbTag[iii], self.QCDMC_Pt_1800to2400_hist_postbTag[iii], self.QCDMC_Pt_2400to3200_hist_postbTag[iii],self.QCDMC_Pt_3200toInf_hist_postbTag[iii] ]))
				self.QCD_linear_postSJTag.append(self.linearize_plot([],"QCD", "postSJTag", systematic + sample_type + year_str,"QCD", [ self.QCDMC_Pt_300to470_hist_postSJTag[iii],  self.QCDMC_Pt_470to600_hist_postSJTag[iii], self.QCDMC_Pt_600to800_hist_postSJTag[iii], self.QCDMC_Pt_800to1000_hist_postSJTag[iii], self.QCDMC_Pt_1000to1400_hist_postSJTag[iii], self.QCDMC_Pt_1400to1800_hist_postSJTag[iii], self.QCDMC_Pt_1800to2400_hist_postSJTag[iii], self.QCDMC_Pt_2400to3200_hist_postSJTag[iii],self.QCDMC_Pt_3200toInf_hist_postSJTag[iii] ]))

			else:
				self.QCD_linear_postbTag.append(self.linearize_plot([],"QCD",  "postbTag", systematic + sample_type + year_str, "QCD", [ self.QCD1000to1500_hist_postbTag[iii], self.QCD1500to2000_hist_postbTag[iii],  self.QCD2000toInf_hist_postbTag[iii]]) )
				self.QCD_linear_postSJTag.append(self.linearize_plot([],"QCD", "postSJTag",systematic + sample_type + year_str, "QCD", [ self.QCD1000to1500_hist_postSJTag[iii], self.QCD1500to2000_hist_postSJTag[iii],  self.QCD2000toInf_hist_postSJTag[iii]]) )


			if "renorm" in systematic or "fact" in systematic: sample_type = "_TTbar"

			TTbar_hists_postbTag = [ self.TTJets1200to2500_hist_postbTag[iii], self.TTJets2500toInf_hist_postbTag[iii]]
			TTbar_hists_postSJTag = [ self.TTJets1200to2500_hist_postSJTag[iii], self.TTJets2500toInf_hist_postSJTag[iii]]


			self.TTbar_linear_postbTag.append(self.linearize_plot([],"TTbar", "postbTag", systematic + sample_type + year_str,"TTbar", TTbar_hists_postbTag ))
			self.TTbar_linear_postSJTag.append(self.linearize_plot([],"TTbar", "postSJTag", systematic + sample_type + year_str,"TTbar", TTbar_hists_postSJTag ))


			if "renorm" in systematic or "fact" in systematic: sample_type = "_sig"
			self.signal_linear_postbTag.append(self.linearize_plot([],"sig",  "postbTag",  systematic + sample_type + year_str,"sig", [ self.signal_WBWB_hist_postbTag[iii], self.signal_HTHT_hist_postbTag[iii], self.signal_ZTZT_hist_postbTag[iii], self.signal_WBHT_hist_postbTag[iii], self.signal_WBZT_hist_postbTag[iii], self.signal_HTZT_hist_postbTag[iii]] ))
			self.signal_linear_postSJTag.append(self.linearize_plot([],"sig", "postSJTag", systematic + sample_type + year_str,"sig", [ self.signal_WBWB_hist_postSJTag[iii], self.signal_HTHT_hist_postSJTag[iii], self.signal_ZTZT_hist_postSJTag[iii], self.signal_WBHT_hist_postSJTag[iii], self.signal_WBZT_hist_postSJTag[iii], self.signal_HTZT_hist_postSJTag[iii]] ))




		if self.debug:
			print("Writing histograms.")
		self.write_histograms()


		# kill the linearized hists and individual signal hists
		self.kill_histograms()



	def clean_histogram(self,hist,systematic,sample):
		ROOT.TH1.AddDirectory(False)
		for iii in range(1, hist.GetNbinsX()+1):
			for jjj in range(1,hist.GetNbinsY()+1):
				if (isnan(hist.GetBinContent(iii,jjj))) or (hist.GetBinContent(iii,jjj) == float("inf")) or (hist.GetBinContent(iii,jjj) == float("-inf")) or ( abs(hist.GetBinContent(iii,jjj))> 1e10) or ( hist.GetBinContent(iii,jjj) < 0 )  :
					print("Bad value in %s for %s/%s, value = %s in bin (%s,%s) of (%s/%s)"%(hist.GetName(), systematic, sample, hist.GetBinContent(iii,jjj), iii, jjj, hist.GetNbinsX(), hist.GetNbinsY()))
					hist.SetBinContent(iii,jjj,0)

		return hist
	def get_combined_histogram(self,file_names, hist_name,folder, weights,systematic):  ### for signal
		ROOT.TH1.AddDirectory(False)
		 
		#print("-------------------- start loading signal files (%s) (%s) (%s) (%s) (technique=%s) ---------------------"%(self.mass_point,self.year,folder,self.technique_str))
		
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
					print("ERROR: negative weight for signal histograms (%s/%s/%s/%s/%s)"%(file_names[iii],hist_name,folder,weights, systematic))
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
						print("ERROR: negative bin value (bin = %s, counts = %s) for signal histogram (%s/%s/%s/%s/%s)"%(h2.GetMinimum(),file_names[iii],hist_name,folder,weights, systematic))
					#print("Original histogram integral: %s with weight %s"%(h2.Integral(), weights[jjj])  )
					if weights[iii] < 0.0:
						print("ERROR: negative weight for signal histograms (%s/%s/%s/%s/%s)"%(file_names[iii],hist_name,folder,weights, systematic))
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


	def load_signal_hist(self,systematic, region, hist_type = ""):
		ROOT.TH2.SetDefaultSumw2()
		ROOT.TH1.SetDefaultSumw2()

		use_filepath = self.MC_root_file_home 

		decays = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]
		file_paths  = [ use_filepath+ "%s_%s_%s_processed.root"%(self.mass_point, decay, self.year) for decay in decays   ]

		sig_weights = [ self.sig_SF_scale*return_signal_SF.return_signal_SF(self.year,self.mass_point,decay) for decay in decays	 ]
		sig_weights_dict = { decay: self.sig_SF_scale*return_signal_SF.return_signal_SF(self.year,self.mass_point,decay) for decay in decays	}   

		sys_suffix = [""]
		if systematic == "nom":
			sys_updown = ["nom"]
		else:
			sys_updown = ["%s_up"%systematic,"%s_down"%systematic]
		all_combined_signal_hist = []

		for sys_str in sys_updown:

			hist_name_signal = "%s%s"%(self.final_hist_name,region)

			if hist_type == "":

				if "topPt" in systematic and "down" in sys_str:
					TH2_hist_signal = self.get_combined_histogram(file_paths, hist_name_signal, "nom", sig_weights, "nom")
				else:
					TH2_hist_signal = self.get_combined_histogram(file_paths, hist_name_signal, sys_str, sig_weights,systematic)

				TH2_hist_signal.SetDirectory(0)   # histograms lose their references when the file destructor is called
				TH2_hist_signal.SetTitle("combined Signal MC (%s) (%s)"%(self.year, sys_str))
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



				if debug: print("Tried to get hist %s from file %s."%(hist_name_signal, filepath))
				if not signal_hist: 
					signal_hist = ROOT.TH2F("h_MSJ_mass_vs_MdSJ_%s"%region,"Superjet mass vs diSuperjet mass (%s) (%s); diSuperjet mass [GeV];superjet mass"%( hist_type,self.technique_str ), 22,1250., 10000, 20, 500, 5000) # 375 * 125
					print("ERROR ---- SIGNAL HIST NOT VALID: %s / %s / %s / %s "%(self.year,systematic,sys_str, hist_type))

				if self.debug: print("signal hist integral for %s / %s / %s / %s is %s."%(self.year,systematic,sys_str,hist_type, signal_hist.Integral()))
				all_combined_signal_hist.append( signal_hist  )
		return all_combined_signal_hist  # load in TTbar historam, scale it, and return this version
	
	
	def linearize_plot(self,_hist,BR_type,region, systematic , hist_type="", split_up_hists_for_systematic = []): 
		ROOT.TH1.SetDefaultSumw2()
		ROOT.TH2.SetDefaultSumw2()

		mask_size = 0
		bin_mask = []

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

		use_indices = self.superbin_indices[region]

		linear_plot_size = len(use_indices)  - mask_size  ## subtract off mask size

		if self.useMask and systematic == "nom":
			print("--- year / technique : %s/%s ------ After applying the mask (size = %s bins) to the superbins (original size = %s),  hist has %s bins"%( self.year,self.technique_str,mask_size, len(use_indices), linear_plot_size)) 


		for iii,sys_str in enumerate(sys_updown):


			#print("BR_type/sys_str is %s/%s"%(BR_type,sys_str))

			linear_plot = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s (%s) (%s); bin; Events / bin"%(BR_type,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)

			linear_plot.GetYaxis().SetTitleOffset(1.48)

			num_masked_bins = 0 
			#print("Histogram name is %s."%linear_plot.GetName())
			if hist_type == "QCD":

				if self.use_QCD_Pt:

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
					linear_plots_QCD_Pt =  [  #ROOT.TH1D("%s%s"%("QCDMC_Pt_170to300",sys_str),"linearized %s (%s) (%s); bin; Events / bin"%( "QCDMC_Pt_170to300",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_300to470",sys_str),"linearized %s (%s) (%s); bin; Events / bin"%( "QCDMC_Pt_300to470",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_470to600",sys_str),"linearized %s (%s) (%s); bin; Events / bin"%(  "QCDMC_Pt_470to600",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_600to800",sys_str),"linearized %s  (%s) (%s); bin; Events / bin"%( "QCDMC_Pt_600to800",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_800to1000",sys_str),"linearized %s (%s) (%s); bin; Events / bin"%( "QCDMC_Pt_800to1000",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_1000to1400",sys_str),"linearized %s (%s) (%s); bin; Events / bin"%(  "QCDMC_Pt_1000to1400",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_1400to1800",sys_str),"linearized %s (%s) (%s); bin; Events / bin"%( "QCDMC_Pt_1400to1800",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_1800to2400",sys_str),"linearized %s (%s) (%s); bin; Events / bin"%( "QCDMC_Pt_1800to2400",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_2400to3200",sys_str),"linearized %s (%s) (%s); bin; Events / bin"%(  "QCDMC_Pt_2400to3200",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5),
					ROOT.TH1D("%s%s"%("QCDMC_Pt_3200toInf",sys_str),"linearized %s (%s) (%s); bin; Events / bin"%(  "QCDMC_Pt_3200toInf",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5) 
					] 

					for hist in linear_plots_QCD_Pt:
						hist.Sumw2()

					superbin_index = 0
					for superbin_counter,superbin in enumerate(use_indices):
						
						total_counts = [0]*len(linear_plots_QCD_Pt)

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


					linear_plot_QCD1000to1500 = ROOT.TH1D("%s%s"%("QCDMC1000to1500",sys_str),"linearized %s (%s) (%s); bin; Events / bin"%( "QCDMC1000to1500",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
					linear_plot_QCD1500to2000 = ROOT.TH1D("%s%s"%("QCDMC1500to2000",sys_str),"linearized %s  (%s) (%s); bin; Events / bin"%( "QCDMC1500to2000",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
					linear_plot_QCD2000toInf = ROOT.TH1D("%s%s"%("QCDMC2000toInf",sys_str),"linearized %s (%s) (%s); bin; Events / bin"%(  "QCDMC2000toInf",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)

					linear_plot_QCD1000to1500.Sumw2(); 
					linear_plot_QCD1500to2000.Sumw2(); 
					linear_plot_QCD2000toInf.Sumw2(); 

					####### INFO 
					#### split_up_hists_for_systematic[0] is the QCD1000to1500 histogram
					#### split_up_hists_for_systematic[1] is the QCD1500to2000 histogram
					#### split_up_hists_for_systematic[2] is the QCD2000toInf  histogram


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
							total_counts_QCD2000toInf+=split_up_hists_for_systematic[2][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
						#print("%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type,, systematic,superbin_index,  total_counts))
						linear_plot_QCD1000to1500.SetBinContent(superbin_index+1,total_counts_QCD1000to1500)
						linear_plot_QCD1000to1500.SetBinError(superbin_index+1,sqrt(total_counts_QCD1000to1500))
						linear_plot_QCD1500to2000.SetBinContent(superbin_index+1,total_counts_QCD1500to2000)
						linear_plot_QCD1500to2000.SetBinError(superbin_index+1,sqrt(total_counts_QCD1500to2000))
					
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
					linear_plot_QCD2000toInf.Scale( SF_2000toInf[self.year])

					### NOW add together with the weight information intact
					linear_plot.Add(linear_plot_QCD1000to1500)
					linear_plot.Add(linear_plot_QCD1500to2000)
					linear_plot.Add(linear_plot_QCD2000toInf)

					all_linear_plots.append(linear_plot)


			elif hist_type == "TTbar":
				SF_TTJetsMCHT800to1200  = {"2015":0.002884466085,"2016":0.002526405224,"2017":0.003001100916,"2018":0.004897196802}
				SF_TTJetsMCHT1200to2500 = {"2015":0.002722324842,"2016":0.002255554525,"2017":0.00267594799,"2018":0.003918532089}
				SF_TTJetsMCHT2500toInf = {"2015":0.000056798633,"2016":0.000050253843,"2017":0.00005947217,"2018":0.000084089656}


				### need to lineraize the histograms separately and THEN add them to linear_plot
				linear_plot_TTJets1200to2500 = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s (%s) (%s); bin; Events / bin"%( "TTJetsMCHT1200to2500",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_TTJets2500toInf  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s (%s) (%s); bin; Events / bin"%( "TTJetsMCHT2500toInf",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)

				linear_plot_TTJets1200to2500.Sumw2()
				linear_plot_TTJets2500toInf.Sumw2()

				####### INFO 				
				#### split_up_hists_for_systematic[0] is the TTJets1200to2500 histogram
				#### split_up_hists_for_systematic[1] is the TTJets2500toInf  histogram
				#### split_up_hists_for_systematic[1] is the TTJets800to1200  histogram ## ONLY IF self.includeTTJets800to1200 == True

				#### if self.doSideband
				#### split_up_hists_for_systematic[0] is the TTJets1200to2500 histogram
				#### split_up_hists_for_systematic[1] is the TTJets800to1200 histogram


				superbin_index = 0
				for superbin_counter,superbin in enumerate(use_indices):
					total_counts_TTJets1200to2500 = 0
					total_counts_TTJets2500toInf  = 0
					if superbin_counter in bin_mask:
						num_masked_bins+=1
						continue

					for _tuple in superbin:
						#if ( (split_up_hists_for_systematic[0][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0) or (split_up_hists_for_systematic[1][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0) ): ### need to verify if these need the +1 ...
						#	print("ERROR: negative histogram contribution when adding up superbins (bin = %s/%s,)"%(_tuple[0]+1, _tuple[1]+1,))
						

						total_counts_TTJets1200to2500+=split_up_hists_for_systematic[0][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
						total_counts_TTJets2500toInf+=split_up_hists_for_systematic[1][iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)

					#print("%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, systematic,superbin_index,  total_counts))


					linear_plot_TTJets1200to2500.SetBinContent(superbin_index+1,total_counts_TTJets1200to2500)
					linear_plot_TTJets1200to2500.SetBinError(superbin_index+1,sqrt(total_counts_TTJets1200to2500))
					linear_plot_TTJets2500toInf.SetBinContent(superbin_index+1,total_counts_TTJets2500toInf)
					linear_plot_TTJets2500toInf.SetBinError(superbin_index+1,sqrt(total_counts_TTJets2500toInf))
					superbin_index+=1




				linear_plot_TTJets1200to2500.Sumw2()
				linear_plot_TTJets2500toInf.Sumw2()
				linear_plot.Sumw2(); 

				## scale histograms 
				linear_plot_TTJets1200to2500.Scale( SF_TTJetsMCHT1200to2500[self.year] )
				linear_plot_TTJets2500toInf.Scale( SF_TTJetsMCHT2500toInf[self.year] )

				### NOW add together with the weight information intact
				linear_plot.Add(linear_plot_TTJets1200to2500)
				linear_plot.Add(linear_plot_TTJets2500toInf)
				all_linear_plots.append(linear_plot)

			


			elif hist_type == "sig":
				decays = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]
				sig_weights_dict = { decay: self.sig_SF_scale*return_signal_SF.return_signal_SF(self.year,self.mass_point,decay) for decay in decays	}   

				### need to lineraize the histograms separately and THEN add them to linear_plot
				linear_plot_WBWB = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s (%s) (%s); bin; Events / bin"%( "WBWB",year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_HTHT = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s (%s) (%s); bin; Events / bin"%( "HTHT" ,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_ZTZT  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s (%s) (%s); bin; Events / bin"%( "ZTZT" ,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_WBHT  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s (%s) (%s) ; bin; Events / bin"%( "WBHT" ,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_WBZT = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s (%s) (%s); bin; Events / bin"%( "WBZT" ,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)
				linear_plot_HTZT  = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s (%s) (%s); bin; Events / bin"%( "HTZT" ,year, " ".join(use_sys.split("_"))),linear_plot_size,-0.5,linear_plot_size-0.5)

				linear_plot_WBWB.Sumw2()
				linear_plot_HTHT.Sumw2()
				linear_plot_ZTZT.Sumw2()
				linear_plot_WBHT.Sumw2()
				linear_plot_WBZT.Sumw2()
				linear_plot_HTZT.Sumw2()


				if self.debug:
					print("2D signal WBWB/HTHT/ZTZT/WBHT/WBZT/HTZT integrals BEFORE scaling are: ")
					print("WBWB: %s"%(split_up_hists_for_systematic[0][iii].Integral() ))
					print("HTHT: %s"%(split_up_hists_for_systematic[1][iii].Integral()  ))
					print("ZTZT: %s"%(split_up_hists_for_systematic[2][iii].Integral()  ))
					print("WBHT: %s"%(split_up_hists_for_systematic[3][iii].Integral()  ))
					print("WBZT: %s"%(split_up_hists_for_systematic[4][iii].Integral()  ))
					print("HTZT: %s"%(split_up_hists_for_systematic[5][iii].Integral()  ))


				####### INFO 
				#### split_up_hists_for_systematic[0] is the WBWB histogram
				#### split_up_hists_for_systematic[1] is the HTHT  histogram
				#### split_up_hists_for_systematic[2] is the ZTZT  histogram
				#### split_up_hists_for_systematic[3] is the WBHT  histogram
				#### split_up_hists_for_systematic[4] is the WBZT  histogram
				#### split_up_hists_for_systematic[5] is the HTZT  histogram
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

					#print("%s/%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type,, systematic,superbin_index,  total_counts))
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
					linear_plot_WBWB.SetTitle("linearized %s (%s) (%s); bin; Events / bin"%( "sig_WBWB",year, " ".join(use_sys.split("_"))))

					linear_plot_HTHT = split_up_hists_for_systematic[1][iii]
					linear_plot_HTHT.SetName("%s%s"%("sig_HTHT",sys_str))
					linear_plot_HTHT.SetTitle("linearized %s (%s) (%s); bin; Events / bin"%( "sig_HTHT",year, " ".join(use_sys.split("_"))))

					linear_plot_ZTZT = split_up_hists_for_systematic[2][iii]
					linear_plot_ZTZT.SetName("%s%s"%("sig_ZTZT",sys_str))
					linear_plot_ZTZT.SetTitle("linearized %s (%s) (%s); bin; Events / bin"%( "sig_ZTZT",year, " ".join(use_sys.split("_"))))

					linear_plot_WBHT = split_up_hists_for_systematic[3][iii]
					linear_plot_WBHT.SetName("%s%s"%("sig_WBHT",sys_str))
					linear_plot_WBHT.SetTitle("linearized %s (%s) (%s); bin; Events / bin"%( "sig_WBHT",year, " ".join(use_sys.split("_"))))

					linear_plot_WBZT = split_up_hists_for_systematic[4][iii]
					linear_plot_WBZT.SetName("%s%s"%("sig_WBZT",sys_str))
					linear_plot_WBZT.SetTitle("linearized %s (%s) (%s); bin; Events / bin"%( "sig_WBZT",year, " ".join(use_sys.split("_"))))

					linear_plot_HTZT = split_up_hists_for_systematic[5][iii]
					linear_plot_HTZT.SetName("%s%s"%("sig_HTZT",sys_str))
					linear_plot_HTZT.SetTitle("linearized %s (%s) (%s); bin; Events / bin"%( "sig_HTZT",year, " ".join(use_sys.split("_"))))"""


				linear_plot_WBWB.Sumw2()
				linear_plot_HTHT.Sumw2()
				linear_plot_ZTZT.Sumw2()
				linear_plot_WBHT.Sumw2()
				linear_plot_WBZT.Sumw2()
				linear_plot_HTZT.Sumw2()
				linear_plot.Sumw2(); 



				if self.debug:
					print("Linear signal WBWB/HTHT/ZTZT/WBHT/WBZT/HTZT integrals BEFORE scaling are: ")
					print("WBWB: %s"%(linear_plot_WBWB.Integral() ))
					print("HTHT: %s"%(linear_plot_HTHT.Integral()  ))
					print("ZTZT: %s"%(linear_plot_ZTZT.Integral()  ))
					print("WBHT: %s"%(linear_plot_WBHT.Integral()  ))
					print("WBZT: %s"%(linear_plot_WBZT.Integral()  ))
					print("HTZT: %s"%(linear_plot_HTZT.Integral()  ))

				## scale histograms 
				linear_plot_WBWB.Scale( sig_weights_dict["WBWB"] )
				linear_plot_HTHT.Scale( sig_weights_dict["HTHT"] )
				linear_plot_ZTZT.Scale( sig_weights_dict["ZTZT"] )
				linear_plot_WBHT.Scale( sig_weights_dict["WBHT"] )				
				linear_plot_WBZT.Scale( sig_weights_dict["WBZT"] )
				linear_plot_HTZT.Scale( sig_weights_dict["HTZT"] )

				if self.debug:
					print("Signal WBWB/HTHT/ZTZT/WBHT/WBZT/HTZT MC scale factors are: ")
					print("WBWB: %s"%(sig_weights_dict["WBWB"] ))
					print("HTHT: %s"%(sig_weights_dict["HTHT"] ))
					print("ZTZT: %s"%(sig_weights_dict["ZTZT"] ))
					print("WBHT: %s"%(sig_weights_dict["WBHT"] ))
					print("WBZT: %s"%(sig_weights_dict["WBZT"] ))
					print("HTZT: %s"%(sig_weights_dict["HTZT"] ))

				### NOW add together with the weight information intact
				linear_plot.Add(linear_plot_WBWB)
				linear_plot.Add(linear_plot_HTHT)
				linear_plot.Add(linear_plot_ZTZT)
				linear_plot.Add(linear_plot_WBHT)				
				linear_plot.Add(linear_plot_WBZT)
				linear_plot.Add(linear_plot_HTZT)


					#print("sig had integral 0 for %s%s for year %s. Injected signal with integral %s."%(BR_type, sys_str, self.year, linear_plot.Integral()))
				all_linear_plots.append(linear_plot)
				
				if self.debug: print("Integral of signal hist for mass point / year / systematic = %s / %s / %s is %s."%(self.mass_point,self.year, systematic,linear_plot.Integral() ))
			else:  # return the FULL histogram (no weighting stuff), this is the old way we did this 

				superbin_index = 0
				for superbin_counter,superbin in enumerate(use_indices):
					if superbin_counter in bin_mask:
						num_masked_bins+=1
						continue

					total_counts = 0

					for _tuple in superbin:
						if (_hist[iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0): ### need to verify if these need the +1 ...
							print("ERROR: negative histogram contribution when adding up superbins (bin = %s/%s, counts = %s)"%(_tuple[0]+1, _tuple[1]+1,_hist[iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)))
						total_counts+=_hist[iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)
				
					#print("%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, systematic,superbin_index,  total_counts))
					linear_plot.SetBinContent(superbin_index+1,total_counts)
					try:
						linear_plot.SetBinError(superbin_index+1,sqrt(total_counts))
					except:
						print("ERROR: Failed setting bin error (superbin index = %s, counts = %s ) for %s/%s/%s"%(superbin_index+1,total_counts, self.year,BR_type,systematic))
					superbin_index+=1

				ROOT.TH1.AddDirectory(False)
				linear_plot.SetDirectory(0)   # histograms lose their references when the file destructor is called
				all_linear_plots.append(linear_plot)

		return all_linear_plots

	def write_histograms(self):

		combine_file_name = self.output_file_home + "/combine_%s_%s.root"%(year,mass_point)   

		# create the directory if it doesn't already exist

		combine_file = ROOT.TFile.Open(combine_file_name,"RECREATE")
		combine_file.cd()

		regions = ["postbTagCut", "postSJTag"]

		QCD_hists	 = [ self.QCD_linear_postbTag, self.QCD_linear_postSJTag ]
		TTbar_hists  = [ self.TTbar_linear_postbTag, self.TTbar_linear_postSJTag]
		signal_hists = [ self.signal_linear_postbTag,  self.signal_linear_postSJTag]

		max_index = 5

		for kkk, region in enumerate(regions):

			if kkk > max_index: continue
			### create folder for region
			combine_file.cd()
			ROOT.gDirectory.mkdir(region)
			combine_file.cd(region)

			systematics_ = self.systematic_names[:]

			for iii,systematic in enumerate(systematics_):


				
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

					if "stat" not in systematic:  
						signal_hists[kkk][iii][jjj].Write()

					TTbar_hists[kkk][iii][jjj].Write()


		return 
	def print_histograms(self):   #TODO: add signal and data plots here 

		CMS_label_pos = 0.152
		SIM_label_pos = 0.295

				# SR
		### create nom plots for each year, 
		self.QCD_linear_postbTag[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/QCD_linear_%s%s_%s_postbTag.png"%(self.technique_str,self.year,"nom"))

		self.TTbar_linear_postbTag[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/TTbar_linear_%s%s_%s_postbTag.png"%(self.technique_str,self.year,"nom"))

		self.signal_linear_postbTag[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/%s_linear_%s%s_%s_postbTag.png"%(self.mass_point, self.technique_str,self.year,"nom"))


				# SR
		### create nom plots for each year, 
		self.QCD_linear_postSJTag[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/QCD_linear_%s%s_%s_postSJTag.png"%(self.technique_str,self.year,"nom"))

		self.TTbar_linear_postSJTag[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/TTbar_linear_%s%s_%s_postSJTag.png"%(self.technique_str,self.year,"nom"))

		self.signal_linear_postSJTag[0][0].Draw()
		write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)
		c.SaveAs(self.final_plot_home+"/%s_linear_%s%s_%s_postSJTag.png"%(self.mass_point, self.technique_str,self.year,"nom"))


		return

	def load_superbin_indices(self,region):	
	# load in the superbin indices (located in a text file ), 
		_superbin_indices = []
		open_file = open(self.index_file_home+"/%s_superbin_indices%s_%s.txt"%(self.use_QCD_Pt_str, self.technique_str,self.year),"r")
		for line in open_file:
			columns = line.split('/')
			if columns[0] == self.year and region in columns[1]:
				_superbin_indices = columns[3]
				break
		open_file.close()


		superbins = ast.literal_eval(_superbin_indices)
		
		return superbins


	def kill_histograms(self):   ## kill the linearized and individual signal histograms

 		linear_hists = [ 
		self.QCD_linear_postbTag, self.TTbar_linear_postbTag , self.QCD_linear_postSJTag, self.TTbar_linear_postSJTag 
		]  

		for hist_list in linear_hists:
			for hist in hist_list:
				del hist

		signal_hists =  [ self.signal_WBWB_hist_postbTag,self.signal_HTHT_hist_postbTag,self.signal_ZTZT_hist_postbTag,self.signal_WBHT_hist_postbTag,self.signal_WBZT_hist_postbTag,self.signal_HTZT_hist_postbTag,
						  self.signal_WBWB_hist_postSJTag,self.signal_HTHT_hist_postSJTag,self.signal_ZTZT_hist_postSJTag,self.signal_WBHT_hist_postSJTag,self.signal_WBZT_hist_postSJTag,self.signal_HTZT_hist_postSJTag] 
		



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

	run_from_eos			 = False

	includeTTJets800to1200 	 = False
	includeTTTo              = False
	includeWJets             = False

	usMask        			 = False  
	use_1b_bin_maps 	     = True

	##################################################
	##################################################
	##################################################
	# get input year
	parser = argparse.ArgumentParser(description="Linearize 2D histograms in order to reach a minimum stat uncertainty and scaled/unscaled bin yield. ")
	parser.add_argument("-y", "--year", type=str, required=True, help="Input year on which to run. Use 'All' for all Run years.")

	args = parser.parse_args()
	

	mass_points = ["Suu4_chi1", "Suu4_chi1p5", 
				   "Suu5_chi1", "Suu5_chi1p5",  "Suu5_chi2", 
				   "Suu6_chi1", "Suu6_chi1p5", "Suu6_chi2", "Suu6_chi2p5",
				   "Suu7_chi1","Suu7_chi1p5","Suu7_chi2", "Suu7_chi2p5", "Suu7_chi3",
				   "Suu8_chi1", "Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3" ]


	if debug:
		mass_points = ["Suu4_chi1"]


	technique_strs  = [""] 
	technique_descr = ["cut-based"]

	use_QCD_Pt_opts = [False,True]
	use_QCD_Pt_strs = ["QCDHT","QCDPT"]

	if args.year == "all" or args.year == "All" or args.year == "ALL":
		years = ["2015","2016","2017","2018"]
	else:
		years = [args.year]


	WPs = []

	ET_cuts = ["200","300","400"]
	jet_HT_cuts = ["1600","1800","2000","2200"]
	nAK8_cuts   = ["2","3","4"]
	nHeavyAK8_cuts   = ["2","3"]


	for ET_cut in ET_cuts:
		for jet_HT_cut in jet_HT_cuts:
			for nAK8_cut in nAK8_cuts:
				for nHeavyAK8_cut in nHeavyAK8_cuts:
					WPs.append("ET%s_HT%s_nAK8%s_nHAK8%s"%(ET_cut,jet_HT_cut,nAK8_cut,nHeavyAK8_cut))


	for year in years:

		print("=============== Running for %s ===============."%year)

		for WP in WPs:

			for jjj,use_QCD_Pt in enumerate(use_QCD_Pt_opts):

				for iii,technique_str in enumerate(technique_strs):

					# create instance of histLoaderSelectionStudier (containing all BR histograms) for the year + technique str combination
					all_BR_hists  = histLoaderSelectionStudier(year, technique_str, use_QCD_Pt, includeTTJets800to1200, includeTTTo, includeWJets, run_from_eos, WP)

					for mass_point in mass_points:
						#try:

						print("Running for %s/%s/%s/useQCDPT = %s"%(year,mass_point,technique_descr[iii],use_QCD_Pt_strs[jjj] ))
						if usMask: final_plot = linearized_plot(year, mass_point, technique_str, all_BR_hists,use_QCD_Pt, True, use_1b_bin_maps,run_from_eos,WP, debug)   ### run with masked bins
						else: final_plot = linearized_plot(year, mass_point, technique_str, all_BR_hists, use_QCD_Pt, False, use_1b_bin_maps,run_from_eos, WP, debug)	### run without masked bins

						# write out the "effective" bin maps = bin maps that are actually being used, to binMaps/ 

						#except:
						#	print("Failed for %s/%s/%s"%(year,mass_point,technique_descr[iii]))
						del final_plot
					all_BR_hists.kill_histograms()
					del all_BR_hists  # free up a lot of memory 
				print("Script took %ss to run."%(	np.round(time.time() - start_time,4 )) )
