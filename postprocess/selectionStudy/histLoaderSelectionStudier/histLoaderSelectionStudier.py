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

class histLoaderSelectionStudier:

	ROOT.TH1.SetDefaultSumw2()
	ROOT.TH2.SetDefaultSumw2()

	def __init__(self, year, technique_str, use_QCD_Pt = False, includeTTJets800to1200 = False, includeTTTo = False, includeWJets = False, run_from_eos = False, WP=None, debug=False):

		self.c = ROOT.TCanvas("","",1200,1000)
		self.BR_SF_scale = 1.0
		self.technique_str = technique_str
		self.year   = year
		self.run_from_eos = run_from_eos
		self.WP = WP 
		self.WP_str = ""
		self.use_QCD_Pt = use_QCD_Pt
		self.debug = debug
		if self.WP: 

			if "ET" in self.WP:
				self.WP_folder = "selectionStudy/%s/"%WP
			else:
				if "AT" in self.WP: 
					self.WP_folder = self.WP[2:]
				else:
					self.WP = "WP" + self.WP
					self.WP_folder = self.WP

				self.WP_str = self.WP + "_"

		self.MC_root_file_home	  = 	os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFiles/"
		self.data_root_file_home	=   os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFiles/"

		self.eos_path = "root://cmseos.fnal.gov/"


		if self.WP:

			if "ET" in self.WP:
				self.MC_root_file_home		= "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/SuuToChiChi_analysis_software/combinedROOT/%s/"%self.WP_folder
				self.data_root_file_home	=  "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/SuuToChiChi_analysis_software/combinedROOT/%s/"%self.WP_folder
			else:
				self.MC_root_file_home		= "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/SuuToChiChi_analysis_software/combinedROOT/ATWP_study/%s/"%self.WP_folder
				self.data_root_file_home	=  "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/SuuToChiChi_analysis_software/combinedROOT/ATWP_study/%s/"%self.WP_folder


		if self.run_from_eos:

			self.MC_root_file_home		=  self.eos_path + "/store/user/ecannaer/processedFiles/"
			self.data_root_file_home	=  self.eos_path + "/store/user/ecannaer/processedFiles/"

			if self.WP:
				self.MC_root_file_home		=  self.eos_path + "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/SuuToChiChi_analysis_software/combinedROOT/ATWP_study/%s/"%self.WP_folder
				self.data_root_file_home	=  self.eos_path + "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/SuuToChiChi_analysis_software/combinedROOT/ATWP_study/%s/"%self.WP_folder


		self.final_hist_name = "h_MSJ_mass_vs_MdSJ_"


		### sample inclusion options
		#self.includeWJets = includeWJets
		#self.includeTTTo  = includeTTTo
		#self.includeTTJets800to1200 = includeTTJets800to1200

		


		self.index_file_home	 = os.getenv('CMSSW_BASE') + "/src/postprocess/binMaps/%s/"%WP


		self.systematics 	  = ["nom",     "JEC",    	  "bTagSF_med"	]   ## systematic namings as used in analyzer	 "bTagSF",   
		self.systematic_names = ["nom",   "CMS_jec",    "CMS_bTagSF_M"  ]  ## systematic namings for cards   "CMS_btagSF", 

		self.uncorrelated_systematics = ["CMS_jec", "CMS_jer","CMS_jer_eta193", "CMS_jer_193eta25", "CMS_L1Prefiring","CMS_bTagSF_M", "CMS_bTagSF_T", "CMS_bTagSF_bc_T_year", "CMS_bTagSF_light_T_year", "CMS_bTagSF_bc_M_year","CMS_bTagSF_light_M_year", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year", "CMS_jec_RelativeSample_year"] ## systematics that are correlated (will not have year appended to names)	 "CMS_btagSF",


		self.systematics 	  = ["nom",  "JEC",			"bTagSF_med" ]
		self.systematic_names = ["nom",   "CMS_jec",    "CMS_bTagSF_M" ]  



		### individual bins for SR

		if self.use_QCD_Pt:
			#self.QCDMC_Pt_170to300_hist_postbTag 	= []
			self.QCDMC_Pt_300to470_hist_postbTag 	= []
			self.QCDMC_Pt_470to600_hist_postbTag 	= []
			self.QCDMC_Pt_600to800_hist_postbTag 	= []
			self.QCDMC_Pt_800to1000_hist_postbTag 	= []
			self.QCDMC_Pt_1000to1400_hist_postbTag 	= []
			self.QCDMC_Pt_1400to1800_hist_postbTag 	= []
			self.QCDMC_Pt_1800to2400_hist_postbTag 	= []
			self.QCDMC_Pt_2400to3200_hist_postbTag 	= []
			self.QCDMC_Pt_3200toInf_hist_postbTag 	= []

			#self.QCDMC_Pt_170to300_hist_postSJTag 	= []
			self.QCDMC_Pt_300to470_hist_postSJTag 	= []
			self.QCDMC_Pt_470to600_hist_postSJTag 	= []
			self.QCDMC_Pt_600to800_hist_postSJTag 	= []
			self.QCDMC_Pt_800to1000_hist_postSJTag 	= []
			self.QCDMC_Pt_1000to1400_hist_postSJTag 	= []
			self.QCDMC_Pt_1400to1800_hist_postSJTag 	= []
			self.QCDMC_Pt_1800to2400_hist_postSJTag 	= []
			self.QCDMC_Pt_2400to3200_hist_postSJTag 	= []
			self.QCDMC_Pt_3200toInf_hist_postSJTag 	= []



		else:

			self.QCD1000to1500_hist_postbTag 	= []
			self.QCD1500to2000_hist_postbTag 	= []
			self.QCD2000toInf_hist_postbTag 	= []

			self.QCD1000to1500_hist_postSJTag 	= []
			self.QCD1500to2000_hist_postSJTag 	= []
			self.QCD2000toInf_hist_postSJTag 	= []

		self.TTJets1200to2500_hist_postbTag 	= []
		self.TTJets2500toInf_hist_postbTag 	= []

		self.TTJets1200to2500_hist_postSJTag 	= []
		self.TTJets2500toInf_hist_postSJTag 	= []

		if self.debug: print("Loading data and background histograms.")
		doExtras = False

		for iii,systematic in enumerate(self.systematics):

			#####  INDIVIDUAL MC HISTOGRAMS
			## sideband Absolute JEC uncertainty names are currently different (change this when they are not)
			systematic_SB = systematic
			if systematic in ["Absolute", "AbsolutePU", "AbsoluteCal","AbsoluteTheory"] :
				systematic_SB = "JEC_" + systematic_SB	
			### SR
			
			#if systematic == "CMS_scale": print("Loading scale histograms.")

			if self.use_QCD_Pt:
				#self.QCDMC_Pt_170to300_hist_postbTag.append(self.load_QCD_hists(systematic,False,"QCD_Pt_170to300"))
				self.QCDMC_Pt_300to470_hist_postbTag.append(self.load_QCD_hists(systematic, "postbTag", False,"QCD_Pt_300to470"))
				self.QCDMC_Pt_470to600_hist_postbTag.append(self.load_QCD_hists(systematic, "postbTag",False,"QCD_Pt_470to600"))
				self.QCDMC_Pt_600to800_hist_postbTag.append(self.load_QCD_hists(systematic, "postbTag",False,"QCD_Pt_600to800"))
				self.QCDMC_Pt_800to1000_hist_postbTag.append(self.load_QCD_hists(systematic, "postbTag",False,"QCD_Pt_800to1000"))
				self.QCDMC_Pt_1000to1400_hist_postbTag.append(self.load_QCD_hists(systematic, "postbTag",False,"QCD_Pt_1000to1400"))
				self.QCDMC_Pt_1400to1800_hist_postbTag.append(self.load_QCD_hists(systematic, "postbTag",False,"QCD_Pt_1400to1800"))
				self.QCDMC_Pt_1800to2400_hist_postbTag.append(self.load_QCD_hists(systematic, "postbTag",False,"QCD_Pt_1800to2400"))
				self.QCDMC_Pt_2400to3200_hist_postbTag.append(self.load_QCD_hists(systematic, "postbTag",False,"QCD_Pt_2400to3200"))
				self.QCDMC_Pt_3200toInf_hist_postbTag.append(self.load_QCD_hists(systematic, "postbTag",False,"QCD_Pt_3200toInf"))


				#self.QCDMC_Pt_170to300_hist_postSJTag.append(self.load_QCD_hists(systematic,False,"QCD_Pt_170to300"))
				self.QCDMC_Pt_300to470_hist_postSJTag.append(self.load_QCD_hists(systematic,"postSJTag",False,"QCD_Pt_300to470"))
				self.QCDMC_Pt_470to600_hist_postSJTag.append(self.load_QCD_hists(systematic,"postSJTag",False,"QCD_Pt_470to600"))
				self.QCDMC_Pt_600to800_hist_postSJTag.append(self.load_QCD_hists(systematic,"postSJTag",False,"QCD_Pt_600to800"))
				self.QCDMC_Pt_800to1000_hist_postSJTag.append(self.load_QCD_hists(systematic,"postSJTag",False,"QCD_Pt_800to1000"))
				self.QCDMC_Pt_1000to1400_hist_postSJTag.append(self.load_QCD_hists(systematic,"postSJTag",False,"QCD_Pt_1000to1400"))
				self.QCDMC_Pt_1400to1800_hist_postSJTag.append(self.load_QCD_hists(systematic,"postSJTag",False,"QCD_Pt_1400to1800"))
				self.QCDMC_Pt_1800to2400_hist_postSJTag.append(self.load_QCD_hists(systematic,"postSJTag",False,"QCD_Pt_1800to2400"))
				self.QCDMC_Pt_2400to3200_hist_postSJTag.append(self.load_QCD_hists(systematic,"postSJTag",False,"QCD_Pt_2400to3200"))
				self.QCDMC_Pt_3200toInf_hist_postSJTag.append(self.load_QCD_hists(systematic,"postSJTag",False,"QCD_Pt_3200toInf"))

				if self.debug:
					if iii > 0:
						print("--------- QCD integrals for systematic %s --------"%systematic)
						print("self.QCDMC_Pt_300to470_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_300to470_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_300to470_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_300to470_hist_postbTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_470to600_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_470to600_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_470to600_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_470to600_hist_postbTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_600to800_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_600to800_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_600to800_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_600to800_hist_postbTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_800to1000_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_800to1000_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_800to1000_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_800to1000_hist_postbTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_1000to1400_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_1000to1400_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_1000to1400_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_1000to1400_hist_postbTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_1400to1800_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_1400to1800_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_1400to1800_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_1400to1800_hist_postbTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_1800to2400_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_1800to2400_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_1800to2400_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_1800to2400_hist_postbTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_2400to3200_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_2400to3200_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_2400to3200_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_2400to3200_hist_postbTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_3200toInf_hist_postbTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_3200toInf_hist_postbTag[iii][0].Integral(),self.QCDMC_Pt_3200toInf_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_3200toInf_hist_postbTag[iii][1].Integral())) 

						print("--------- QCD integrals for systematic %s --------"%systematic)
						print("self.QCDMC_Pt_300to470_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_300to470_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_300to470_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_300to470_hist_postSJTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_470to600_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_470to600_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_470to600_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_470to600_hist_postSJTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_600to800_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_600to800_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_600to800_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_600to800_hist_postSJTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_800to1000_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_800to1000_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_800to1000_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_800to1000_hist_postSJTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_1000to1400_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_1000to1400_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_1000to1400_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_1000to1400_hist_postSJTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_1400to1800_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_1400to1800_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_1400to1800_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_1400to1800_hist_postSJTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_1800to2400_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_1800to2400_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_1800to2400_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_1800to2400_hist_postSJTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_2400to3200_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_2400to3200_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_2400to3200_hist_postSJTag[0][0].Integral(),self.QCDMC_Pt_2400to3200_hist_postSJTag[iii][1].Integral())) 
						print("self.QCDMC_Pt_3200toInf_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCDMC_Pt_3200toInf_hist_postSJTag[iii][0].Integral(),self.QCDMC_Pt_3200toInf_hist_postbTag[0][0].Integral(),self.QCDMC_Pt_3200toInf_hist_postSJTag[iii][1].Integral())) 


			else:
				self.QCD1000to1500_hist_postbTag.append(self.load_QCD_hists(systematic,"postbTag",False,"QCDMC1000to1500"))
				self.QCD1500to2000_hist_postbTag.append(self.load_QCD_hists(systematic,"postbTag",False,"QCDMC1500to2000"))
				self.QCD2000toInf_hist_postbTag.append(self.load_QCD_hists(systematic, "postbTag",False,"QCDMC2000toInf"))

				self.QCD1000to1500_hist_postSJTag.append(self.load_QCD_hists(systematic,"postSJTag",False,"QCDMC1000to1500"))
				self.QCD1500to2000_hist_postSJTag.append(self.load_QCD_hists(systematic,"postSJTag",False,"QCDMC1500to2000"))
				self.QCD2000toInf_hist_postSJTag.append(self.load_QCD_hists(systematic, "postSJTag",False,"QCDMC2000toInf"))

				if self.debug:
					if iii > 0:
						print("--------- QCD integrals for systematic %s --------"%systematic)

						print("self.QCD1000to1500_hist_postbTag:  UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCD1000to1500_hist_postbTag[iii][0].Integral(),self.QCD1000to1500_hist_postbTag[0][0].Integral(),self.QCD1000to1500_hist_postbTag[iii][1].Integral())) 
						print("self.QCD1500to2000_hist_postbTag:  UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCD1500to2000_hist_postbTag[iii][0].Integral(),self.QCD1500to2000_hist_postbTag[0][0].Integral(),self.QCD1500to2000_hist_postbTag[iii][1].Integral())) 
						print("self.QCD2000toInf_hist_postbTag:   UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCD2000toInf_hist_postbTag[iii][0].Integral(),self.QCD2000toInf_hist_postbTag[0][0].Integral(),self.QCD2000toInf_hist_postbTag[iii][1].Integral())) 
						print("self.QCD1000to1500_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCD1000to1500_hist_postSJTag[iii][0].Integral(),self.QCD1000to1500_hist_postSJTag[0][0].Integral(),self.QCD1000to1500_hist_postSJTag[iii][1].Integral())) 
						print("self.QCD1500to2000_hist_postSJTag: UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCD1500to2000_hist_postSJTag[iii][0].Integral(),self.QCD1500to2000_hist_postSJTag[0][0].Integral(),self.QCD1500to2000_hist_postSJTag[iii][1].Integral())) 
						print("self.QCD2000toInf_hist_postSJTag:  UP integral is %s, NOM integral is %s, DOWN integral is %s"%(self.QCD2000toInf_hist_postSJTag[iii][0].Integral(),self.QCD2000toInf_hist_postSJTag[0][0].Integral(),self.QCD2000toInf_hist_postSJTag[iii][1].Integral())) 


			self.TTJets1200to2500_hist_postbTag.append(self.load_ttbar_hist(systematic,"postbTag",False,"TTJetsMCHT1200to2500"))
			self.TTJets2500toInf_hist_postbTag.append(self.load_ttbar_hist(systematic, "postbTag",False, "TTJetsMCHT2500toInf"))

			self.TTJets1200to2500_hist_postSJTag.append(self.load_ttbar_hist(systematic,"postSJTag",False,"TTJetsMCHT1200to2500"))
			self.TTJets2500toInf_hist_postSJTag.append(self.load_ttbar_hist(systematic, "postSJTag",False, "TTJetsMCHT2500toInf"))


			if systematic == "nom":
				sys_strs = [""]
			elif "topPt" in systematic:
				sys_strs = ["_up", "_down"]
			else:
				sys_strs = ["_up", "_down"]

		if self.debug: print("Background and data hists loaded.")

	def load_QCD_hists(self,systematic, region,forStats = False, hist_type = ""):
		ROOT.TH1.SetDefaultSumw2()
		ROOT.TH2.SetDefaultSumw2()
		#ROOT.TH2.SetDefaultSumw2()
		sys_suffix = [""]
		
		use_filepath = self.MC_root_file_home 

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
		hist_path_2000toInf  = use_filepath + "QCDMC2000toInf_%s_%sprocessed.root"%(self.year, self.WP_str)

		all_combined_QCD_hist = []
		for sys_str in sys_updown:

			if "topPt" in systematic and "down" in sys_str:
				hist_name = "nom/%s%s"%(self.final_hist_name,region)
			else:
				hist_name = "%s/%s%s"%(sys_str,self.final_hist_name,region )

			if "QCD" in hist_type:
				hist_path = use_filepath + "%s_%s_%sprocessed.root"%(hist_type, self.year, self.WP_str)
				if self.debug: print("For QCD hists, looking for hist %s in file %s."%(hist_name, hist_path))
				

				TH2_file = ROOT.TFile.Open(hist_path,"READ")
				TH2_hist = self.clean_histogram(TH2_file.Get(hist_name), systematic, hist_type ) 

				if self.debug: print("hist_name / file name / integral is = %s / %s / %s"%(	 hist_name,hist_path,TH2_hist.Integral()))


				TH2_hist.SetDirectory(0)
				all_combined_QCD_hist.append( TH2_hist  )  #### THESE ARE UNSCALED!!!

			## COMBINED PORTION BELOW IS NOT IMPLEMENTED FOR QCD_Pt hists
			elif hist_type == "":


				TH2_file_1000to1500 = ROOT.TFile.Open(hist_path_1000to1500,"READ")
				TH2_hist_1000to1500 = self.clean_histogram(TH2_file_1000to1500.Get(hist_name), systematic, "QCDMC1000to1500" )

				TH2_file_1500to2000 = ROOT.TFile.Open(hist_path_1500to2000,"READ")
				TH2_hist_1500to2000 = self.clean_histogram(TH2_file_1500to2000.Get(hist_name), systematic, "QCDMC1500to2000" )

				TH2_file_2000toInf = ROOT.TFile.Open(hist_path_2000toInf,"READ")
				TH2_hist_2000toInf = self.clean_histogram(TH2_file_2000toInf.Get(hist_name), systematic, "QCDMC2000toInf" )

				TH2_hist_1000to1500.SetDirectory(0)   # histograms lose their references when the file destructor is called
				TH2_hist_1500to2000.SetDirectory(0)   # histograms lose their references when the file destructor is called
				TH2_hist_2000toInf.SetDirectory(0)   # histograms lose their references when the file destructor is called



				### return the COMBINED histograms

				### scale each histogram
				TH2_hist_1000to1500.Scale(self.BR_SF_scale*SF_1000to1500[self.year])
				TH2_hist_1500to2000.Scale(self.BR_SF_scale*SF_1500to2000[self.year])
				TH2_hist_2000toInf.Scale(self.BR_SF_scale*SF_2000toInf[self.year])



				combined_QCD_hist = ROOT.TH2F("combined_QCD_%s%s"%(self.technique_str ,sys_str), ("QCD (HT1000-Inf) Events (%s) (%s)"%(year, sys_str)), 22,1250., 10000, 20, 500, 5000)
				combined_QCD_hist.Add(TH2_hist_1000to1500)
				combined_QCD_hist.Add(TH2_hist_1500to2000)
				combined_QCD_hist.Add(TH2_hist_2000toInf)

				combined_QCD_hist.SetDirectory(0)   # histograms lose their references when the file destructor is called
				all_combined_QCD_hist.append(combined_QCD_hist)
			else: 
				print("ERROR in load_QCD_hists: hist_type=%s is not correct (options are : '', 'QCDMC1000to1500', 'QCDMC1500to2000', and 'QCDMC2000toInf' )"%hist_type)
				return []
		ROOT.TH1.AddDirectory(False)

		return all_combined_QCD_hist   # load in QCD histograms, scale them, add them together, and return their sum



	
	def load_ttbar_hist(self,systematic, region, forStats = False, hist_type = ""):
		ROOT.TH1.SetDefaultSumw2()
		ROOT.TH2.SetDefaultSumw2()
		#ROOT.TH2.SetDefaultSumw2()

		use_filepath = self.MC_root_file_home 


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


		hist_path_TTJetsMCHT1200to2500 = use_filepath + "TTJetsMCHT1200to2500_%s_%sprocessed.root"%(self.year, self.WP_str)
		hist_path_TTJetsMCHT2500toInf  = use_filepath + "TTJetsMCHT2500toInf_%s_%sprocessed.root"%(self.year, self.WP_str)

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
				hist_name_TTbar = "nom/%s%s"%(self.final_hist_name,region)
			else:
				hist_name_TTbar = "%s/%s%s"%(sys_str,self.final_hist_name,region)


			if "TTJets" in hist_type:
				hist_path = use_filepath + "%s_%s_%sprocessed.root"%(hist_type, self.year, self.WP_str)
				TH2_file = ROOT.TFile.Open(hist_path,"READ")
				TH2_hist = self.clean_histogram(TH2_file.Get(hist_name_TTbar), systematic, hist_type ) 
				all_combined_TTbar_hist.append( TH2_hist  )  #### THESE ARE UNSCALED!!!

			elif hist_type == "":

				TH2_file_TTJetsMCHT1200to2500 = ROOT.TFile.Open(hist_path_TTJetsMCHT1200to2500,"READ")
				TH2_file_TTJetsMCHT2500toInf  = ROOT.TFile.Open(hist_path_TTJetsMCHT2500toInf,"READ")

				TH2_hist_TTJetsMCHT1200to2500 = self.clean_histogram(TH2_file_TTJetsMCHT1200to2500.Get(hist_name_TTbar) , systematic, "TTJetsMCHT1200to2500" )
				TH2_hist_TTJetsMCHT2500toInf  = self.clean_histogram(TH2_file_TTJetsMCHT2500toInf.Get(hist_name_TTbar), systematic, "TTJetsMCHT2500toInf" )

				TH2_hist_TTJetsMCHT1200to2500.Scale(self.BR_SF_scale*SF_TTJetsMCHT1200to2500[self.year])
				TH2_hist_TTJetsMCHT1200to2500.SetDirectory(0)   # histograms lose their references when the file destructor is called
				
				TH2_hist_TTJetsMCHT2500toInf.Scale(self.BR_SF_scale*SF_TTJetsMCHT2500toInf[self.year])
				TH2_hist_TTJetsMCHT2500toInf.SetDirectory(0)   # histograms lose their references when the file destructor is called


				### return the COMBINED histograms

				TH2_hist_TTJetsMCHT1200to2500.Add(TH2_hist_TTJetsMCHT2500toInf)
				TH2_hist_TTJetsMCHT1200to2500.SetName("combined_TTbar_%s%s"%(self.technique_str ,sys_str))
				TH2_hist_TTJetsMCHT1200to2500.SetTitle("combined TTbar MC (%s) (%s)"%(self.year, sys_str))
				all_combined_TTbar_hist.append(TH2_hist_TTJetsMCHT1200to2500)
			else: 
				print("ERROR in load_ttbar_hist: hist_type=%s is not correct (options are : '', 'TTJets1200to2500', and 'TTJets2500toInf' )"%hist_type)
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
	
	
	def kill_histograms(self):   ## many histograms to kill ... 

		all_hist_lists = [ self.TTJets1200to2500_hist_postbTag, self.TTJets2500toInf_hist_postbTag, self.TTJets1200to2500_hist_postSJTag, self.TTJets2500toInf_hist_postSJTag ]
	

		if self.use_QCD_Pt:
			all_hist_lists.extend([
				#self.QCDMC_Pt_170to300_hist_postbTag,
				self.QCDMC_Pt_300to470_hist_postbTag,
				self.QCDMC_Pt_470to600_hist_postbTag,
				self.QCDMC_Pt_600to800_hist_postbTag,
				self.QCDMC_Pt_800to1000_hist_postbTag,
				self.QCDMC_Pt_1000to1400_hist_postbTag,
				self.QCDMC_Pt_1400to1800_hist_postbTag,
				self.QCDMC_Pt_1800to2400_hist_postbTag,
				self.QCDMC_Pt_2400to3200_hist_postbTag,
				self.QCDMC_Pt_3200toInf_hist_postbTag,
				#self.QCDMC_Pt_170to300_hist_postSJTag,
				self.QCDMC_Pt_300to470_hist_postSJTag,
				self.QCDMC_Pt_470to600_hist_postSJTag,
				self.QCDMC_Pt_600to800_hist_postSJTag,
				self.QCDMC_Pt_800to1000_hist_postSJTag,
				self.QCDMC_Pt_1000to1400_hist_postSJTag,
				self.QCDMC_Pt_1400to1800_hist_postSJTag,
				self.QCDMC_Pt_1800to2400_hist_postSJTag,
				self.QCDMC_Pt_2400to3200_hist_postSJTag,
				self.QCDMC_Pt_3200toInf_hist_postSJTag
				])
		else:
			all_hist_lists.extend([
				self.QCD1000to1500_hist_postbTag, self.QCD1500to2000_hist_postbTag, self.QCD2000toInf_hist_postbTag])


		for hist_list in all_hist_lists:
			for hist in hist_list:
				del hist

		return

