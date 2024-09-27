import sys,os,time
import numpy as np
import ROOT
import ast
from return_signal_SF import return_signal_SF
from math import sqrt
from write_cms_text import write_cms_text


from math import isnan
### linearize_final_plots.py
### written by Ethan Cannaert, October 2023
### requires locations of input root files for each background/signal contribution (QCD1000to1500, QCD1500to2000, QCD2000toInf, TTbar, sig MC)

### open each file and get the histograms from each
### scale histograms relative to the appropriate luminosity 
### get superbin indices and find "center" of each superbin, sort bin by these centers 
### loop over each superbin and add together the corresponding histogram bins, this becomes an entry in a 1D ( 22x20 = 440 bin) distribution for each contribution that goes to Combine
### in the end there will be a histogram for QCD, TTbar, signal MC, and then data 


### change the lists to instead be dictionaries?
class linearized_plot:
	n_bins_x = 22
	n_bins_y = 20


	def __init__(self, year,mass_point, technique_str):

		self.c = ROOT.TCanvas("","",1200,1000)
		self.BR_SF_scale = 1.0
		self.sig_SF_scale = 1.0
		self.technique_str = technique_str
		self.year   = year
		self.MC_root_file_home      = 	os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFiles/"
		self.data_root_file_home    =   os.getenv('CMSSW_BASE') + "/src/combinedROOT/processedFiles/"

		self.doSideband = True
		if "NN" in self.technique_str: self.doSideband = False
		self.index_file_home     = os.getenv('CMSSW_BASE') + "/src/postprocess/binMaps/"
		self.output_file_home    = os.getenv('CMSSW_BASE') + "/src/postprocess/finalCombineFiles"
		self.final_plot_home     = os.getenv('CMSSW_BASE') + "/src/postprocess/plots/finalCombinePlots"
		
		self.superbin_indices        	  = self.load_superbin_indices()
		if  self.doSideband: 
			self.superbin_indices_SB1b = self.load_superbin_indices(region="SB1b")
			self.superbin_indices_SB0b = self.load_superbin_indices(region="SB1b")

		self.mass_point = mass_point   # label for the signal mass point

		self.non_data_systematics = [ "PUSF", "JER", "topPt", "pdf", "renorm", "fact"] # "bTagSF", ### removed BtagSF until other files are processed 
		self.data_systematics = ["nom", "L1Prefiring"]
		self.data_systematic_names = ["nom", "CMS_L1Prefiring"]

		#self.systematics = ["nom","JER","JEC"] ### NEEDS TO BE CHANGED BACK
		self.systematics 	  = ["nom",   "bTagSF_med",   "bTagSF_tight", "bTag_eventWeight_bc_T", "bTag_eventWeight_light_T", "bTag_eventWeight_bc_M", "bTag_eventWeight_light_M", "bTag_eventWeight_bc_T_year", "bTag_eventWeight_light_T_year", "bTag_eventWeight_bc_M_year", "bTag_eventWeight_light_M_year",   "JER",        "JER_eta193",     "JER_193eta25",       "JEC_FlavorQCD",    "JEC_RelativeBal",      "JEC_HF",     "JEC_BBEC1",     "JEC_EC2",     "JEC_Absolute",     "JEC_BBEC1_year",     "JEC_EC2_year",    "JEC_Absolute_year",       "JEC_HF_year",    "JEC_RelativeSample_year",    "PUSF",    "topPt",     "L1Prefiring",     "pdf",     "renorm",     "fact" ]   ## systematic namings as used in analyzer     "bTagSF", 
		self.systematic_names = ["nom",  "CMS_bTagSF_M" ,  "CMS_bTagSF_T",    "CMS_bTagSF_bc_T",       "CMS_bTagSF_light_T",       "CMS_bTagSF_bc_M",       "CMS_bTagSF_light_M",      "CMS_bTagSF_bc_T_year",        "CMS_bTagSF_light_T_year",      "CMS_bTagSF_bc_M_year",       "CMS_bTagSF_light_M_year",    "CMS_jer",    "CMS_jer_eta193", "CMS_jer_193eta25",  "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal", "CMS_jec_HF", "CMS_jec_BBEC1", "CMS_jec_EC2", "CMS_jec_Absolute", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year", "CMS_jec_RelativeSample_year", "CMS_pu", "CMS_topPt", "CMS_L1Prefiring", "CMS_pdf", "CMS_renorm", "CMS_fact"]  ## systematic namings for cards   "CMS_btagSF",
		self.uncorrelated_systematics = [ "CMS_pu",  "CMS_jec", "CMS_jer","CMS_jer_eta193", "CMS_jer_193eta25", "CMS_L1Prefiring","CMS_bTagSF_M", "CMS_bTagSF_T", "CMS_bTagSF_bc_T_year", "CMS_bTagSF_light_T_year", "CMS_bTagSF_bc_M_year","CMS_bTagSF_light_M_year", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year", "CMS_jec_RelativeSample_year"] ## systematics that are correlated (will not have year appended to names)     "CMS_btagSF",
		self.QCD_hist_SR = []
		self.TTbar_hist_SR 	= []
		self.ST_hist_SR 	= []
		self.data_hist_SR 	= []
		self.signal_hist_SR = []

		self.QCD_hist_CR 	= []
		self.TTbar_hist_CR 	= []
		self.ST_hist_CR 	= []
		self.data_hist_CR 	= []
		self.signal_hist_CR = []

		self.TTbar_hist_AT0b 	= []
		self.ST_hist_AT0b	 	= []
		self.QCD_hist_AT0b   	= []
		self.data_hist_AT0b  	= []
		self.signal_hist_AT0b  	= []

		self.TTbar_hist_AT1b 	= []
		self.ST_hist_AT1b 		= []
		self.QCD_hist_AT1b   	= []
		self.data_hist_AT1b  	= []
		self.signal_hist_AT1b 	= []

		self.TTbar_hist_SB1b 	= []
		self.ST_hist_SB1b 		= []
		self.QCD_hist_SB1b   	= []
		self.data_hist_SB1b  	= []
		self.signal_hist_SB1b 	= []		

		self.TTbar_hist_SB0b 	= []
		self.ST_hist_SB0b 		= []
		self.QCD_hist_SB0b   	= []
		self.data_hist_SB0b  	= []
		self.signal_hist_SB0b 	= []	

		self.all_combined_hists_SR = []
		self.all_combined_hists_CR = []
		self.all_combined_hists_AT1b = []
		self.all_combined_hists_AT0b = []
		self.all_combined_hists_SB1b = []
		self.all_combined_hists_SB0b = []

		self.combined_linear_SR     = []
		self.combined_linear_CR     = []
		self.combined_linear_AT1b   = []
		self.combined_linear_AT0b   = []
		self.combined_linear_SB1b   = []
		self.combined_linear_SB0b   = []


		doExtras = False
		for systematic in self.systematics:
			self.QCD_hist_SR.append(self.load_QCD_hists("SR",systematic))
			self.TTbar_hist_SR.append(self.load_ttbar_hist("SR",systematic))
			self.ST_hist_SR.append(self.load_ST_hists("SR",systematic))
			self.signal_hist_SR.append(self.load_signal_hist("SR",systematic))

			self.QCD_hist_CR.append(self.load_QCD_hists("CR",systematic))
			self.TTbar_hist_CR.append(self.load_ttbar_hist("CR",systematic))
			self.ST_hist_CR.append(self.load_ST_hists("CR",systematic))
			self.signal_hist_CR.append(self.load_signal_hist("CR",systematic))

			self.QCD_hist_AT0b.append(self.load_QCD_hists("AT0b",systematic))
			self.TTbar_hist_AT0b.append(self.load_ttbar_hist("AT0b",systematic))
			self.ST_hist_AT0b.append(self.load_ST_hists("AT0b",systematic))
			self.signal_hist_AT0b.append(self.load_signal_hist("AT0b",systematic))

			self.QCD_hist_AT1b.append(self.load_QCD_hists("AT1b",systematic))
			self.TTbar_hist_AT1b.append(self.load_ttbar_hist("AT1b",systematic))
			self.ST_hist_AT1b.append(self.load_ST_hists("AT1b",systematic))
			self.signal_hist_AT1b.append(self.load_signal_hist("AT1b",systematic))

			if self.doSideband:
				self.QCD_hist_SB1b.append(self.load_QCD_hists("SB1b",systematic))
				self.TTbar_hist_SB1b.append(self.load_ttbar_hist("SB1b",systematic))
				self.ST_hist_SB1b.append(self.load_ST_hists("SB1b",systematic))
				self.signal_hist_SB1b.append(self.load_signal_hist("SB1b",systematic))
				if(  len(self.signal_hist_SB1b) < 1  ):
					print("signal_hist_SB1b was empty: %s/%s"%(self.year,systematic))
				self.QCD_hist_SB0b.append(self.load_QCD_hists("SB0b",systematic))
				self.TTbar_hist_SB0b.append(self.load_ttbar_hist("SB0b",systematic))
				self.ST_hist_SB0b.append(self.load_ST_hists("SB0b",systematic))
				self.signal_hist_SB0b.append(self.load_signal_hist("SB0b",systematic))

			if systematic == "nom":
				sys_strs = [""]
			elif "topPt" in systematic:
				sys_strs = ["_up", "_down"]
			else:
				sys_strs = ["_up", "_down"]

			self.all_combined_hists_SR.append( [] )
			self.all_combined_hists_CR.append( [] )
			self.all_combined_hists_AT1b.append( [] )
			self.all_combined_hists_AT0b.append( [] )
			self.all_combined_hists_SB1b.append( [] )
			self.all_combined_hists_SB0b.append( [] )

			for iii,sys_str in enumerate(sys_strs):
				self.all_combined_hists_SR[-1].append(self.QCD_hist_SR[-1][iii].Clone())
				self.all_combined_hists_CR[-1].append(self.QCD_hist_CR[-1][iii].Clone())
				self.all_combined_hists_AT1b[-1].append(self.QCD_hist_AT1b[-1][iii].Clone())
				self.all_combined_hists_AT0b[-1].append(self.QCD_hist_AT0b[-1][iii].Clone())
				if self.doSideband:
					self.all_combined_hists_SB1b[-1].append(self.QCD_hist_SB1b[-1][iii].Clone())
					self.all_combined_hists_SB0b[-1].append(self.QCD_hist_SB0b[-1][iii].Clone())

				self.all_combined_hists_SR[-1][iii].Add(self.TTbar_hist_SR[-1][iii].Clone())
				self.all_combined_hists_SR[-1][iii].Add(self.ST_hist_SR[-1][iii].Clone())
				self.all_combined_hists_SR[-1][iii].SetName("allBR_%s"%(systematic+ sys_str))
				self.all_combined_hists_SR[-1][iii].SetName("Combined Backgrounds (%s) (SR) (%s)"%(year, systematic+ sys_str))

				self.all_combined_hists_CR[-1][iii].Add(self.TTbar_hist_CR[-1][iii].Clone())
				self.all_combined_hists_CR[-1][iii].Add(self.ST_hist_CR[-1][iii].Clone())
				self.all_combined_hists_CR[-1][iii].SetName("allBR_%s"%(systematic+ sys_str))
				self.all_combined_hists_CR[-1][iii].SetName("Combined Backgrounds (%s) (CR) (%s)"%(year, systematic+ sys_str))

				self.all_combined_hists_AT1b[-1][iii].Add(self.TTbar_hist_AT1b[-1][iii].Clone())
				self.all_combined_hists_AT1b[-1][iii].Add(self.ST_hist_AT1b[-1][iii].Clone())
				self.all_combined_hists_AT1b[-1][iii].SetName("allBR_%s"%(systematic+ sys_str))
				self.all_combined_hists_AT1b[-1][iii].SetName("Combined Backgrounds (%s) (AT1b) (%s)"%(year, systematic+ sys_str))

				self.all_combined_hists_AT0b[-1][iii].Add(self.TTbar_hist_AT0b[-1][iii].Clone())
				self.all_combined_hists_AT0b[-1][iii].Add(self.ST_hist_AT0b[-1][iii].Clone())
				self.all_combined_hists_AT0b[-1][iii].SetName("allBR_%s"%(systematic+ sys_str))
				self.all_combined_hists_AT0b[-1][iii].SetName("Combined Backgrounds (%s) (AT0b) (%s)"%(year, systematic+ sys_str))

				if self.doSideband:
					self.all_combined_hists_SB1b[-1][iii].Add(self.TTbar_hist_SB1b[-1][iii].Clone())
					self.all_combined_hists_SB1b[-1][iii].Add(self.ST_hist_SB1b[-1][iii].Clone())
					self.all_combined_hists_SB1b[-1][iii].SetName("allBR_%s"%(systematic+ sys_str))
					self.all_combined_hists_SB1b[-1][iii].SetName("Combined Backgrounds (%s) (SB1b) (%s)"%(year, systematic+ sys_str))

					self.all_combined_hists_SB0b[-1][iii].Add(self.TTbar_hist_SB0b[-1][iii].Clone())
					self.all_combined_hists_SB0b[-1][iii].Add(self.ST_hist_SB0b[-1][iii].Clone())
					self.all_combined_hists_SB0b[-1][iii].SetName("allBR_%s"%(systematic+ sys_str))
					self.all_combined_hists_SB0b[-1][iii].SetName("Combined Backgrounds (%s) (SB0b) (%s)"%(year, systematic+ sys_str))

		for systematic in self.data_systematics:
			self.data_hist_SR.append(self.load_data_hists("SR",systematic))
			self.data_hist_CR.append(self.load_data_hists("CR",systematic))
			self.data_hist_AT0b.append(self.load_data_hists("AT0b",systematic))
			self.data_hist_AT1b.append(self.load_data_hists("AT1b",systematic))
			if self.doSideband:
				self.data_hist_SB1b.append(self.load_data_hists("SB1b",systematic))
				self.data_hist_SB0b.append(self.load_data_hists("SB0b",systematic))


		self.combined_hist_SR = self.load_ttbar_hist("SR","nom")[0]
		self.combined_hist_SR.Add(self.load_QCD_hists("SR","nom")[0])
		self.combined_hist_SR.Add(self.load_ST_hists("SR","nom")[0])

		self.combined_hist_CR =  self.load_ttbar_hist("CR","nom")[0]
		self.combined_hist_CR.Add(self.load_QCD_hists("CR","nom")[0])
		self.combined_hist_CR.Add(self.load_ST_hists("CR","nom")[0])

		self.combined_hist_AT0b =  self.load_ttbar_hist("AT0b","nom")[0]
		self.combined_hist_AT0b.Add(self.load_QCD_hists("AT0b","nom")[0])
		self.combined_hist_AT0b.Add(self.load_ST_hists("AT0b","nom")[0])

		self.combined_hist_AT1b =  self.load_ttbar_hist("AT1b","nom")[0]
		self.combined_hist_AT1b.Add(self.load_QCD_hists("AT1b","nom")[0])
		self.combined_hist_AT1b.Add(self.load_ST_hists("AT1b","nom")[0])
		if self.doSideband:
			self.combined_hist_SB1b =  self.load_ttbar_hist("SB1b","nom")[0]
			self.combined_hist_SB1b.Add(self.load_QCD_hists("SB1b","nom")[0])
			self.combined_hist_SB1b.Add(self.load_ST_hists("SB1b","nom")[0])

			self.combined_hist_SB0b =  self.load_ttbar_hist("SB0b","nom")[0]
			self.combined_hist_SB0b.Add(self.load_QCD_hists("SB0b","nom")[0])
			self.combined_hist_SB0b.Add(self.load_ST_hists("SB0b","nom")[0])
			#now create linear plots that have all systematic plots inside

		self.QCD_linear_SR 	  = []
		self.TTbar_linear_SR  = []
		self.ST_linear_SR 	  = []
		self.data_linear_SR   = []
		self.signal_linear_SR = []

		self.QCD_linear_CR 	  = []
		self.TTbar_linear_CR  = []
		self.ST_linear_CR     = []
		self.data_linear_CR   = []
		self.signal_linear_CR = []

		self.QCD_linear_AT0b     = []
		self.TTbar_linear_AT0b   = []
		self.ST_linear_AT0b      = []
		self.data_linear_AT0b    = []
		self.signal_linear_AT0b  = []

		self.QCD_linear_AT1b 	= []
		self.TTbar_linear_AT1b 	= []
		self.ST_linear_AT1b 	= []
		self.data_linear_AT1b 	= []
		self.signal_linear_AT1b = []

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

		self.all_combined_linear_SR   = []
		self.all_combined_linear_CR   = []
		self.all_combined_linear_AT1b = []
		self.all_combined_linear_AT0b = []
		self.all_combined_linear_SB1b = []
		self.all_combined_linear_SB0b = []
		#print("------------------ linearizing histograms ------------------------ %s/%s"%(self.year, self.technique_str))

		for iii,systematic_ in enumerate(self.systematic_names):   ### this was originally extending the
			systematic = systematic_

			sample_type = ""	
			year_str = ""

			if systematic_ in self.uncorrelated_systematics:
				if year == "2015":
					year_str = "16preVFP"
				else:
					year_str =  year[-2:]

			if "renorm" in systematic or "fact" in systematic: sample_type = "_QCD"
			self.QCD_linear_SR.append(self.linearize_plot(self.QCD_hist_SR[iii],"QCD","SR",systematic + sample_type + year_str))
			self.QCD_linear_CR.append(self.linearize_plot(self.QCD_hist_CR[iii],"QCD","CR",systematic + sample_type + year_str))
			self.QCD_linear_AT0b.append(self.linearize_plot(self.QCD_hist_AT0b[iii],"QCD","AT0b",systematic + sample_type + year_str))
			self.QCD_linear_AT1b.append(self.linearize_plot(self.QCD_hist_AT1b[iii],"QCD","AT1b",systematic + sample_type + year_str))
			if self.doSideband: self.QCD_linear_SB1b.append(self.linearize_plot(self.QCD_hist_SB1b[iii],"QCD","SB1b",systematic + sample_type + year_str))
			if self.doSideband: self.QCD_linear_SB0b.append(self.linearize_plot(self.QCD_hist_SB0b[iii],"QCD","SB0b",systematic + sample_type + year_str))

			if "renorm" in systematic or "fact" in systematic: sample_type = "_TTbar"
			self.TTbar_linear_SR.append(self.linearize_plot(self.TTbar_hist_SR[iii],"TTbar","SR",systematic + sample_type + year_str))
			self.TTbar_linear_CR.append(self.linearize_plot(self.TTbar_hist_CR[iii],"TTbar","CR",systematic + sample_type + year_str))
			self.TTbar_linear_AT0b.append(self.linearize_plot(self.TTbar_hist_AT0b[iii],"TTbar","AT0b",systematic + sample_type + year_str))
			self.TTbar_linear_AT1b.append(self.linearize_plot(self.TTbar_hist_AT1b[iii],"TTbar","AT1b",systematic + sample_type + year_str))
			if self.doSideband: self.TTbar_linear_SB1b.append(self.linearize_plot(self.TTbar_hist_SB1b[iii],"TTbar","SB1b",systematic + sample_type + year_str))
			if self.doSideband: self.TTbar_linear_SB0b.append(self.linearize_plot(self.TTbar_hist_SB0b[iii],"TTbar","SB0b",systematic + sample_type + year_str))

			if "renorm" in systematic or "fact" in systematic: sample_type = "_sig"
			self.signal_linear_SR.append(self.linearize_plot(self.signal_hist_SR[iii],"sig","SR",systematic + sample_type + year_str))
			self.signal_linear_CR.append(self.linearize_plot(self.signal_hist_CR[iii],"sig","CR",systematic + sample_type + year_str))
			self.signal_linear_AT0b.append(self.linearize_plot(self.signal_hist_AT0b[iii],"sig","AT0b",systematic + sample_type + year_str))
			self.signal_linear_AT1b.append(self.linearize_plot(self.signal_hist_AT1b[iii],"sig","AT1b",systematic + sample_type + year_str))

			#print("iii/systematic: %s/%s"%(iii,systematic))
			#print("self.signal_hist_SB1b is ", self.signal_hist_SB1b, self.doSideband, self.technique_str)

			if self.doSideband: self.signal_linear_SB1b.append(self.linearize_plot(self.signal_hist_SB1b[iii],"sig","SB1b",systematic + sample_type + year_str))
			if self.doSideband: self.signal_linear_SB0b.append(self.linearize_plot(self.signal_hist_SB0b[iii],"sig","SB0b",systematic + sample_type + year_str))

			if "renorm" in systematic or "fact" in systematic: sample_type = "_ST"
			self.ST_linear_SR.append(self.linearize_plot(self.ST_hist_SR[iii],"ST","SR",systematic + sample_type + year_str))
			self.ST_linear_CR.append(self.linearize_plot(self.ST_hist_CR[iii],"ST","CR",systematic + sample_type + year_str))
			self.ST_linear_AT0b.append(self.linearize_plot(self.ST_hist_AT0b[iii],"ST","AT0b",systematic + sample_type + year_str))
			self.ST_linear_AT1b.append(self.linearize_plot(self.ST_hist_AT1b[iii],"ST","AT1b",systematic + sample_type + year_str))
			if self.doSideband: self.ST_linear_SB1b.append(self.linearize_plot(self.ST_hist_SB1b[iii],"ST","SB1b",systematic + sample_type + year_str))
			if self.doSideband: self.ST_linear_SB0b.append(self.linearize_plot(self.ST_hist_SB0b[iii],"ST","SB0b",systematic + sample_type + year_str))

			if "renorm" in systematic or "fact" in systematic: sample_type = "_allBR"
			self.all_combined_linear_SR.append(self.linearize_plot(self.all_combined_hists_SR[iii],"allBR","SR",systematic + sample_type + year_str))
			self.all_combined_linear_CR.append(self.linearize_plot(self.all_combined_hists_CR[iii],"allBR","CR",systematic + sample_type + year_str))
			self.all_combined_linear_AT1b.append(self.linearize_plot(self.all_combined_hists_AT1b[iii],"allBR","AT1b",systematic + sample_type + year_str))
			self.all_combined_linear_AT0b.append(self.linearize_plot(self.all_combined_hists_AT0b[iii],"allBR","AT0b",systematic + sample_type + year_str))
			if self.doSideband: self.all_combined_linear_SB1b.append(self.linearize_plot(self.all_combined_hists_SB1b[iii],"allBR","SB1b",systematic + sample_type + year_str))
			if self.doSideband: self.all_combined_linear_SB0b.append(self.linearize_plot(self.all_combined_hists_SB0b[iii],"allBR","SB0b",systematic + sample_type + year_str))

		for iii, systematic_ in enumerate(self.data_systematic_names):

			year_str = ""
			sample_type = ""
			systematic = systematic_
			if systematic_ in self.uncorrelated_systematics:
				if year == "2015":
					year_str = "16"
				else:
					year_str =  year[-2:]

			self.data_linear_SR.append(self.linearize_plot(self.data_hist_SR[iii],"data_obs","SR",systematic + sample_type + year_str)) 
			self.data_linear_CR.append(self.linearize_plot(self.data_hist_CR[iii],"data_obs","CR",systematic + sample_type + year_str))
			self.data_linear_AT0b.append(self.linearize_plot(self.data_hist_AT0b[iii],"data_obs","AT0b",systematic + sample_type + year_str))
			self.data_linear_AT1b.append(self.linearize_plot(self.data_hist_AT1b[iii],"data_obs","AT1b",systematic + sample_type + year_str))
			if self.doSideband: self.data_linear_SB1b.append(self.linearize_plot(self.data_hist_SB1b[iii],"data_obs","SB1b",systematic + sample_type + year_str))
			if self.doSideband: self.data_linear_SB0b.append(self.linearize_plot(self.data_hist_SB0b[iii],"data_obs","SB0b",systematic + sample_type + year_str))

		#self.print_dataMC_ratio_plots()

		self.write_histograms()
		if doExtras:
			self.print_histograms()


		self.kill_histograms()
		################################################################################################################
		################################################################################################################
		####################### create unscaled linear histograms for stat uncertainty purposees #######################
		################################################################################################################
		################################################################################################################

		#print("------------ Creating stat uncertainty plots ------------")

		self.QCD_hist_SR = [self.load_QCD_hists("SR","nom",True)]
		self.TTbar_hist_SR = [self.load_ttbar_hist("SR","nom",True)]
		self.ST_hist_SR = [self.load_ST_hists("SR","nom",True)]
		self.signal_hist_SR = [self.load_signal_hist("SR","nom",True)]

		self.QCD_hist_CR = [self.load_QCD_hists("CR","nom",True)]
		self.TTbar_hist_CR = [self.load_ttbar_hist("CR","nom",True)]
		self.ST_hist_CR = [self.load_ST_hists("CR","nom",True)]
		self.signal_hist_CR = [self.load_signal_hist("CR","nom",True)]

		self.QCD_hist_AT0b = [self.load_QCD_hists("AT0b","nom",True)]
		self.TTbar_hist_AT0b = [self.load_ttbar_hist("AT0b","nom",True)]
		self.ST_hist_AT0b = [self.load_ST_hists("AT0b","nom",True)]
		self.signal_hist_AT0b = [self.load_signal_hist("AT0b","nom",True)]

		self.QCD_hist_AT1b = [self.load_QCD_hists("AT1b","nom",True)]
		self.TTbar_hist_AT1b = [self.load_ttbar_hist("AT1b","nom",True)]
		self.ST_hist_AT1b = [self.load_ST_hists("AT1b","nom",True)]
		self.signal_hist_AT1b = [self.load_signal_hist("AT1b","nom",True)]

		if self.doSideband:
			self.QCD_hist_SB1b = [self.load_QCD_hists("SB1b","nom",True)]
			self.TTbar_hist_SB1b = [self.load_ttbar_hist("SB1b","nom",True)]
			self.ST_hist_SB1b = [self.load_ST_hists("SB1b","nom",True)]
			self.signal_hist_SB1b = [self.load_signal_hist("SB1b","nom",True)]

			self.QCD_hist_SB0b = [self.load_QCD_hists("SB0b","nom",True)]
			self.TTbar_hist_SB0b = [self.load_ttbar_hist("SB0b","nom",True)]
			self.ST_hist_SB0b = [self.load_ST_hists("SB0b","nom",True)]
			self.signal_hist_SB0b = [self.load_signal_hist("SB0b","nom",True)]

		self.data_hist_SR = [self.load_data_hists("SR","nom")]
		self.data_hist_CR = [self.load_data_hists("CR","nom")]
		self.data_hist_AT0b = [self.load_data_hists("AT0b","nom")]
		self.data_hist_AT1b = [self.load_data_hists("AT1b","nom")]
		if self.doSideband:
			self.data_hist_SB1b = [self.load_data_hists("SB1b","nom")]
			self.data_hist_SB0b = [self.load_data_hists("SB0b","nom")]

		combined_hist_SR_ = self.load_ttbar_hist("SR","nom",True)[0]
		combined_hist_SR_.Add(self.load_QCD_hists("SR","nom",True)[0])
		combined_hist_SR_.Add(self.load_ST_hists("SR","nom",True)[0])

		combined_hist_CR_ =  self.load_ttbar_hist("CR","nom",True)[0]
		combined_hist_CR_.Add(self.load_QCD_hists("CR","nom",True)[0])
		combined_hist_CR_.Add(self.load_ST_hists("CR","nom",True)[0])

		combined_hist_AT0b_ =  self.load_ttbar_hist("AT0b","nom",True)[0]
		combined_hist_AT0b_.Add(self.load_QCD_hists("AT0b","nom",True)[0])
		combined_hist_AT0b_.Add(self.load_ST_hists("AT0b","nom",True)[0])

		combined_hist_AT1b_ =  self.load_ttbar_hist("AT1b","nom",True)[0]
		combined_hist_AT1b_.Add(self.load_QCD_hists("AT1b","nom",True)[0])
		combined_hist_AT1b_.Add(self.load_ST_hists("AT1b","nom",True)[0])

		if self.doSideband:
			combined_hist_SB1b_ =  self.load_ttbar_hist("SB1b","nom",True)[0]
			combined_hist_SB1b_.Add(self.load_QCD_hists("SB1b","nom",True)[0])
			combined_hist_SB1b_.Add(self.load_ST_hists("SB1b","nom",True)[0])

			combined_hist_SB0b_ =  self.load_ttbar_hist("SB0b","nom",True)[0]
			combined_hist_SB0b_.Add(self.load_QCD_hists("SB0b","nom",True)[0])
			combined_hist_SB0b_.Add(self.load_ST_hists("SB0b","nom",True)[0])

		self.combined_hist_SR = [[combined_hist_SR_]]
		self.combined_hist_CR = [[combined_hist_CR_]]
		self.combined_hist_AT0b = [[combined_hist_AT0b_]]
		self.combined_hist_AT1b = [[combined_hist_AT1b_]]
		if self.doSideband:
			self.combined_hist_SB1b = [[combined_hist_SB1b_]]
			self.combined_hist_SB0b = [[combined_hist_SB0b_]]

		self.QCD_linear_SR    = [self.linearize_plot(self.QCD_hist_SR[0],"QCD","SR","nom",True)]
		self.TTbar_linear_SR  = [self.linearize_plot(self.TTbar_hist_SR[0],"TTbar","SR","nom",True)]
		self.ST_linear_SR     = [self.linearize_plot(self.ST_hist_SR[0],"ST","SR","nom",True)]
		self.signal_linear_SR = [self.linearize_plot(self.signal_hist_SR[0],"sig","SR","nom",True)]

		self.QCD_linear_CR    = [self.linearize_plot(self.QCD_hist_CR[0],"QCD","CR","nom",True)]
		self.TTbar_linear_CR  = [self.linearize_plot(self.TTbar_hist_CR[0],"TTbar","CR","nom",True)]
		self.ST_linear_CR     = [self.linearize_plot(self.ST_hist_CR[0],"ST","CR","nom",True)]
		self.signal_linear_CR = [self.linearize_plot(self.signal_hist_CR[0],"sig","CR","nom",True)]


		self.QCD_linear_AT0b    = [self.linearize_plot(self.QCD_hist_AT0b[0],"QCD","AT0b","nom",True)]
		self.TTbar_linear_AT0b  = [self.linearize_plot(self.TTbar_hist_AT0b[0],"TTbar","AT0b","nom",True)]
		self.ST_linear_AT0b     = [self.linearize_plot(self.ST_hist_AT0b[0],"ST","AT0b","nom",True)]
		self.signal_linear_AT0b = [self.linearize_plot(self.signal_hist_AT0b[0],"sig","AT0b","nom",True)]

		self.QCD_linear_AT1b    = [self.linearize_plot(self.QCD_hist_AT1b[0],"QCD","AT1b","nom",True)]
		self.TTbar_linear_AT1b  = [self.linearize_plot(self.TTbar_hist_AT1b[0],"TTbar","AT1b","nom",True)]
		self.ST_linear_AT1b     = [self.linearize_plot(self.ST_hist_AT1b[0],"ST","AT1b","nom",True)]
		self.signal_linear_AT1b = [self.linearize_plot(self.signal_hist_AT1b[0],"sig","AT1b","nom",True)]

		if self.doSideband:
			self.QCD_linear_SB1b    = [self.linearize_plot(self.QCD_hist_SB1b[0],"QCD","SB1b","nom",True)]
			self.TTbar_linear_SB1b  = [self.linearize_plot(self.TTbar_hist_SB1b[0],"TTbar","SB1b","nom",True)]
			self.ST_linear_SB1b     = [self.linearize_plot(self.ST_hist_SB1b[0],"ST","SB1b","nom",True)]
			self.signal_linear_Sb1b = [self.linearize_plot(self.signal_hist_SB1b[0],"sig","SB1b","nom",True)]

			self.QCD_linear_SB0b    = [self.linearize_plot(self.QCD_hist_SB0b[0],"QCD","SB0b","nom",True)]
			self.TTbar_linear_SB0b  = [self.linearize_plot(self.TTbar_hist_SB0b[0],"TTbar","SB0b","nom",True)]
			self.ST_linear_SB0b     = [self.linearize_plot(self.ST_hist_SB0b[0],"ST","SB0b","nom",True)]
			self.signal_linear_Sb0b = [self.linearize_plot(self.signal_hist_SB0b[0],"sig","SB0b","nom",True)]

		self.data_linear_SR   = [self.linearize_plot(self.data_hist_SR[0],"data_obs","SR","nom",True)]
		self.data_linear_CR   = [self.linearize_plot(self.data_hist_CR[0],"data_obs","CR","nom",True)]
		self.data_linear_AT0b = [self.linearize_plot(self.data_hist_AT0b[0],"data_obs","AT0b","nom",True)]
		self.data_linear_AT1b = [self.linearize_plot(self.data_hist_AT1b[0],"data_obs","AT1b","nom",True)]
		if self.doSideband:
			self.data_linear_SB1b = [self.linearize_plot(self.data_hist_SB1b[0],"data_obs","SB1b","nom",True)]
			self.data_linear_SB0b = [self.linearize_plot(self.data_hist_SB0b[0],"data_obs","SB0b","nom",True)]

		self.combined_linear_SR   = self.linearize_plot(self.combined_hist_SR[0],"Combined","SR","nom",True)
		self.combined_linear_CR   = self.linearize_plot(self.combined_hist_CR[0],"Combined","CR","nom",True)
		self.combined_linear_AT1b = self.linearize_plot(self.combined_hist_AT1b[0],"Combined","AT1b","nom",True)
		self.combined_linear_AT0b = self.linearize_plot(self.combined_hist_AT0b[0],"Combined","AT0b","nom",True)
		if self.doSideband:
			self.combined_linear_SB1b = self.linearize_plot(self.combined_hist_SB1b[0],"Combined","SB1b","nom",True)
			self.combined_linear_SB0b = self.linearize_plot(self.combined_hist_SB0b[0],"Combined","Sb0b","nom",True)
		#self.print_dataMC_ratio_plots()

		self.write_histograms(True)

		self.kill_histograms()
		#print("---------------------------------------- finished %s -----------------------------------------"%self.mass_point)
	def load_QCD_hists(self,region,systematic, forStats = False):
		ROOT.TH1.SetDefaultSumw2()
		ROOT.TH2.SetDefaultSumw2()
		#ROOT.TH2.SetDefaultSumw2()
		sys_suffix = [""]
		
		use_filepath = self.MC_root_file_home 

		if region in ["SB1b", "SB0b"]: use_filepath      = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"

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
		hist_path_1000to1500 = use_filepath + "QCDMC1000to1500_%s_processed.root"%(self.year)
		hist_path_1500to2000 = use_filepath + "QCDMC1500to2000_%s_processed.root"%(self.year)
		if region not in ["SB1b", "SB0b"] : hist_path_2000toInf  = use_filepath + "QCDMC2000toInf_%s_processed.root"%(self.year)

		all_combined_QCD_hist = []
		for sys_str in sys_updown:

			### get each histogram

			#print("Looking for systematic %s"%sys_str )

			if "topPt" in systematic and "down" in sys_str:
				hist_name = "nom/h_MSJ_mass_vs_MdSJ_%s%s"%(self.technique_str ,region )
			else:
				hist_name = "%s/h_MSJ_mass_vs_MdSJ_%s%s"%(sys_str,self.technique_str ,region )

			#print("Loading QCD %s/%s/%s"%(region,systematic,self.year))

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

			### scale each histogram
			TH2_hist_1000to1500.Scale(self.BR_SF_scale*SF_1000to1500[self.year])
			TH2_hist_1500to2000.Scale(self.BR_SF_scale*SF_1500to2000[self.year])
			if region not in ["SB1b", "SB0b"] : 
				TH2_hist_2000toInf.Scale(self.BR_SF_scale*SF_2000toInf[self.year])

			if region in ["SB1b", "SB0b"] : combined_QCD_hist = ROOT.TH2F("combined_QCD_%s%s"%(self.technique_str ,sys_str), ("QCD (HT1000-Inf) Events in the %s (%s) (%s)"%(region, year, sys_str)), 15 ,0.0, 8000, 12, 0.0, 2500)
			else: combined_QCD_hist = ROOT.TH2F("combined_QCD_%s%s"%(self.technique_str ,sys_str), ("QCD (HT1000-Inf) Events in the %s (%s) (%s)"%(region, year, sys_str)), 22,1250., 10000, 20, 500, 4000)
			combined_QCD_hist.Add(TH2_hist_1000to1500)
			combined_QCD_hist.Add(TH2_hist_1500to2000)
			if region not in ["SB1b", "SB0b"] : combined_QCD_hist.Add(TH2_hist_2000toInf)

			combined_QCD_hist.SetDirectory(0)   # histograms lose their references when the file destructor is called
			all_combined_QCD_hist.append(combined_QCD_hist)

		ROOT.TH1.AddDirectory(False)

		return all_combined_QCD_hist   # load in QCD histograms, scale them, add them together, and return their sum
	def load_ttbar_hist(self,region,systematic, forStats = False):
		ROOT.TH1.SetDefaultSumw2()
		ROOT.TH2.SetDefaultSumw2()
		#ROOT.TH2.SetDefaultSumw2()

		use_filepath = self.MC_root_file_home 
		if region in ["SB1b", "SB0b"]: use_filepath      = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"


		#SF_TTToHadronic= {'2015':0.075592 , '2016':0.05808655696 , '2017':0.06651018525 , '2018': 0.06588049107 }
		#SF_TTToSemiLeptonic= {'2015':0.05395328118 , '2016':0.04236184005 , '2017':0.04264829286 , '2018': 0.04563489275 }
		#SF_TTToLeptonic= {'2015':0.0459517611 , '2016':0.03401684391 , '2017':0.03431532926 , '2018': 0.03617828025 }

		SF_TTJetsMCHT800to1200  = {"2015":0.002884466085,"2016":0.002526405224,"2017":0.003001100916,"2018":0.004897196802}
		SF_TTJetsMCHT1200to2500 = {"2015":0.002722324842,"2016":0.002255554525,"2017":0.00267594799,"2018":0.003918532089}

		if region not in ["SB1b", "SB0b"] :SF_TTJetsMCHT2500toInf = {"2015":0.000056798633,"2016":0.000050253843,"2017":0.00005947217,"2018":0.000084089656}

		if forStats:
			SF_TTJetsMCHT800to1200 = {"2015":1,"2016":1,"2017":1,"2018":1}
			SF_TTJetsMCHT1200to2500= {"2015":1,"2016":1,"2017":1,"2018":1}
			SF_TTJetsMCHT2500toInf = {"2015":1,"2016":1,"2017":1,"2018":1}


		#hist_path_TTToHadronic = use_filepath+ "TTToHadronicMC_%s_processed.root"%(self.year)
		#hist_path_TTToSemiLeptonic = use_filepath+ "TTToSemiLeptonicMC_%s_processed.root"%(self.year)
		#hist_path_TTToLeptonic = use_filepath+ "TTToLeptonicMC_%s_processed.root"%(self.year)


		if self.doSideband: hist_path_TTJetsMCHT800to1200 = use_filepath + "TTJetsMCHT800to1200_%s_processed.root"%(self.year)
		hist_path_TTJetsMCHT1200to2500 = use_filepath + "TTJetsMCHT1200to2500_%s_processed.root"%(self.year)
		if region not in ["SB1b", "SB0b"] :hist_path_TTJetsMCHT2500toInf  = use_filepath + "TTJetsMCHT2500toInf_%s_processed.root"%(self.year)

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
				hist_name_TTbar = "nom/h_MSJ_mass_vs_MdSJ_%s%s"%(self.technique_str ,region )
			else:
				hist_name_TTbar = "%s/h_MSJ_mass_vs_MdSJ_%s%s"%(sys_str,self.technique_str ,region )

			#TH2_file_TTToHadronic = ROOT.TFile.Open(hist_path_TTToHadronic,"READ")
			#TH2_file_TTToSemiLeptonic = ROOT.TFile.Open(hist_path_TTToSemiLeptonic,"READ")
			#TH2_file_TTToLeptonic = ROOT.TFile.Open(hist_path_TTToLeptonic,"READ")

			TH2_file_TTJetsMCHT1200to2500 = ROOT.TFile.Open(hist_path_TTJetsMCHT1200to2500,"READ")
			if region not in ["SB1b", "SB0b"] :TH2_file_TTJetsMCHT2500toInf  = ROOT.TFile.Open(hist_path_TTJetsMCHT2500toInf,"READ")
			else:
				if self.doSideband: 
					hist_path_TTJetsMCHT800to1200 = use_filepath + "TTJetsMCHT800to1200_%s_processed.root"%(self.year)
					TH2_file_TTJetsMCHT800to1200 = ROOT.TFile.Open(hist_path_TTJetsMCHT800to1200,"READ")
					#print("Loading TTbar %s/%s/%s"%(region,systematic,self.year))
					TH2_hist_TTJetsMCHT800to1200  = self.clean_histogram(TH2_file_TTJetsMCHT800to1200.Get(hist_name_TTbar), systematic, "TTJets800to1200") 
			#TH2_hist_TTToHadronic = TH2_file_TTToHadronic.Get(hist_name_TTbar) 
			#TH2_hist_TTToSemiLeptonic = TH2_file_TTToSemiLeptonic.Get(hist_name_TTbar) 
			#TH2_hist_TTToLeptonic = TH2_file_TTToLeptonic.Get(hist_name_TTbar) 

			TH2_hist_TTJetsMCHT1200to2500 = self.clean_histogram(TH2_file_TTJetsMCHT1200to2500.Get(hist_name_TTbar) , systematic, "TTJets1200to2500" )
			if region not in ["SB1b", "SB0b"] :TH2_hist_TTJetsMCHT2500toInf  = self.clean_histogram(TH2_file_TTJetsMCHT2500toInf.Get(hist_name_TTbar), systematic, "TTJets2500toInf" )

			TH2_hist_TTJetsMCHT1200to2500.Scale(self.BR_SF_scale*SF_TTJetsMCHT1200to2500[self.year])
			TH2_hist_TTJetsMCHT1200to2500.SetDirectory(0)   # histograms lose their references when the file destructor is called
			if region not in ["SB1b", "SB0b"] :
				TH2_hist_TTJetsMCHT2500toInf.Scale(self.BR_SF_scale*SF_TTJetsMCHT2500toInf[self.year])
				TH2_hist_TTJetsMCHT2500toInf.SetDirectory(0)   # histograms lose their references when the file destructor is called
			else:
				if self.doSideband: 
					TH2_hist_TTJetsMCHT800to1200.Scale(self.BR_SF_scale*SF_TTJetsMCHT800to1200[self.year])
					TH2_hist_TTJetsMCHT800to1200.SetDirectory(0)   # histograms lose their references when the file destructor is called


			#TH2_hist_TTToHadronic.Scale(SF_TTToHadronic[self.year])
			#TH2_hist_TTToHadronic.SetDirectory(0)   # histograms lose their references when the file destructor is called

			#TH2_hist_TTToSemiLeptonic.Scale(SF_TTToSemiLeptonic[self.year])
			#TH2_hist_TTToSemiLeptonic.SetDirectory(0)   # histograms lose their references when the file destructor is called

			#TH2_hist_TTToLeptonic.Scale(SF_TTToLeptonic[self.year])
			#TH2_hist_TTToLeptonic.SetDirectory(0)   # histograms lose their references when the file destructor is called
			
			if region not in ["SB1b", "SB0b"] :TH2_hist_TTJetsMCHT1200to2500.Add(TH2_hist_TTJetsMCHT2500toInf)
			else:
				if self.doSideband: 
					TH2_hist_TTJetsMCHT1200to2500.Add(TH2_hist_TTJetsMCHT800to1200)
			TH2_hist_TTJetsMCHT1200to2500.SetName("combined_TTbar_%s%s"%(self.technique_str ,sys_str))
			TH2_hist_TTJetsMCHT1200to2500.SetTitle("combined TTbar MC (%s) (%s) (%s)"%(self.year,region, sys_str))
			all_combined_TTbar_hist.append(TH2_hist_TTJetsMCHT1200to2500)

		return all_combined_TTbar_hist  # load in TTbar historam, scale it, and return this version
	def clean_histogram(self,hist,systematic,sample):
		ROOT.TH1.AddDirectory(False)
		for iii in range(1, hist.GetNbinsX()+1):
			for jjj in range(1,hist.GetNbinsY()+1):
				if (isnan(hist.GetBinContent(iii,jjj))) or (hist.GetBinContent(iii,jjj) == float("inf")) or (hist.GetBinContent(iii,jjj) == float("-inf")) or ( abs(hist.GetBinContent(iii,jjj))> 1e10) or ( hist.GetBinContent(iii,jjj) < 0 )  :
					print("Bad value in %s for %s/%s, value = %s in bin (%s,%s) of (%s/%s)"%(hist.GetName(), systematic, sample, hist.GetBinContent(iii,jjj), iii, jjj, hist.GetNbinsX(), hist.GetNbinsY()))
					hist.SetBinContent(iii,jjj,0)

		return hist
	def get_combined_histogram(self,file_names, hist_name,folder, weights,systematic,region):
		ROOT.TH1.AddDirectory(False)
		 
		#print("-------------------- start loading signal files (%s) (%s) (%s) (%s) (technique=%s) ---------------------"%(self.mass_point,self.year,folder,region,self.technique_str))
		
		for iii in range(0,len(file_names)):  ### keep looping over possible signal histograms until one is found to work
			nFailed_files = 0
			nFiles = len(file_names)
			total_integral = 0
			#print("-------> Weights are : ", weights)
			folder_name = folder+"/"+hist_name

			try:
				f1 = ROOT.TFile(file_names[iii],"r")
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
					f2 = ROOT.TFile(file_names[jjj],"r")
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
	def load_signal_hist(self,region,systematic, forStats=False):

		use_filepath = self.MC_root_file_home
		if region in ["SB1b", "SB0b"]: use_filepath      = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"

		decays = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]
		file_paths  = [ use_filepath+ "%s_%s_%s_processed.root"%(self.mass_point, decay, self.year) for decay in decays   ]

		sig_weights = [ self.sig_SF_scale*return_signal_SF.return_signal_SF(self.year,self.mass_point,decay) for decay in decays     ]
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

			hist_name_signal = "h_MSJ_mass_vs_MdSJ_%s%s"%(self.technique_str,region)
			#print("Loading signal hist %s/%s/%s"%(region,systematic,self.year))

			if "topPt" in systematic and "down" in sys_str:
				TH2_hist_signal = self.get_combined_histogram(file_paths, hist_name_signal, "nom", sig_weights, "nom",region)
			else:
				TH2_hist_signal = self.get_combined_histogram(file_paths, hist_name_signal, sys_str, sig_weights,systematic,region)
			TH2_hist_signal.SetDirectory(0)   # histograms lose their references when the file destructor is called
			TH2_hist_signal.SetTitle("combined Signal MC (%s) (%s) (%s)"%(self.year,region, sys_str))
			all_combined_signal_hist.append(TH2_hist_signal)
		return all_combined_signal_hist  # load in TTbar historam, scale it, and return this version
	def load_ST_hists(self,region,systematic, forStats=False):
		ROOT.TH2.SetDefaultSumw2()
		ROOT.TH1.SetDefaultSumw2()
		linear_plot_size = len(self.superbin_indices)


		use_filepath = self.MC_root_file_home
		if region in ["SB1b", "SB0b"]: use_filepath      = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"


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
		
		hist_path_ST_t_channel_top_5f 	  = use_filepath + "ST_t-channel-top_inclMC_%s_processed.root"%(self.year)
		hist_path_ST_t_channel_antitop_5f = use_filepath + "ST_t-channel-antitop_inclMC_%s_processed.root"%(self.year)
		hist_path_ST_s_channel_4f_hadrons = use_filepath + "ST_s-channel-hadronsMC_%s_processed.root"%(self.year)
		hist_path_ST_s_channel_4f_leptons = use_filepath + "ST_s-channel-leptonsMC_%s_processed.root"%(self.year)
		hist_path_ST_tW_antitop_5f		  = use_filepath + "ST_tW-antiTop_inclMC_%s_processed.root"%(self.year)
		hist_path_ST_tW_top_5f 			  = use_filepath + "ST_tW-top_inclMC_%s_processed.root"%(self.year)

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
				hist_name_ST = "nom/h_MSJ_mass_vs_MdSJ_%s%s"%(self.technique_str ,region )
			else:
				hist_name_ST = "%s/h_MSJ_mass_vs_MdSJ_%s%s"%(sys_str,self.technique_str ,region )

			#print("Loading Single top %s/%s/%s"%(region,systematic,self.year))
			TH2_file_ST_t_channel_top_5f 	 = ROOT.TFile.Open(hist_path_ST_t_channel_top_5f,"READ")
			TH2_file_ST_t_channel_antitop_5f = ROOT.TFile.Open(hist_path_ST_t_channel_antitop_5f,"READ")
			TH2_file_ST_s_channel_4f_hadrons = ROOT.TFile.Open(hist_path_ST_s_channel_4f_hadrons,"READ")
			TH2_file_ST_s_channel_4f_leptons = ROOT.TFile.Open(hist_path_ST_s_channel_4f_leptons,"READ")
			TH2_file_ST_tW_antitop_5f 		 = ROOT.TFile.Open(hist_path_ST_tW_antitop_5f,"READ")
			TH2_file_ST_tW_top_5f			 = ROOT.TFile.Open(hist_path_ST_tW_top_5f,"READ")

			TH2_hist_ST_t_channel_top_5f 	 = self.clean_histogram(TH2_file_ST_t_channel_top_5f.Get(hist_name_ST), systematic, "ST_t_channel_top" )
			TH2_hist_ST_t_channel_antitop_5f = self.clean_histogram(TH2_file_ST_t_channel_antitop_5f.Get(hist_name_ST), systematic, "ST_t_channel_antitop" )
			TH2_hist_ST_s_channel_4f_hadrons = self.clean_histogram(TH2_file_ST_s_channel_4f_hadrons.Get(hist_name_ST), systematic, "ST_s_channel_hadrons" )
			TH2_hist_ST_s_channel_4f_leptons = self.clean_histogram(TH2_file_ST_s_channel_4f_leptons.Get(hist_name_ST), systematic, "ST_s_channel_leptons"  )
			TH2_hist_ST_tW_antitop_5f 		 = self.clean_histogram(TH2_file_ST_tW_antitop_5f.Get(hist_name_ST), systematic, "ST_tW_antitop" )
			TH2_hist_ST_tW_top_5f			 = self.clean_histogram(TH2_file_ST_tW_top_5f.Get(hist_name_ST), systematic, "ST_tW_top" )

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

			if region in ["SB1b", "SB0b"]: combined_ST_hist = ROOT.TH2F("combined_ST_%s"%region,"combined linearized Single Top (%s) (%s) (%s)"%(self.year,region,sys_str),15 ,0.0, 8000, 12, 0.0, 2500);  
			else: combined_ST_hist = ROOT.TH2F("combined_ST_%s"%region,"combined linearized Single Top (%s) (%s) (%s)"%(self.year,region,sys_str),22,1250., 10000, 20, 500, 4000)
			combined_ST_hist.Add(TH2_hist_ST_t_channel_top_5f)
			combined_ST_hist.Add(TH2_hist_ST_t_channel_antitop_5f)
			combined_ST_hist.Add(TH2_hist_ST_s_channel_4f_hadrons)
			combined_ST_hist.Add(TH2_hist_ST_s_channel_4f_leptons)
			combined_ST_hist.Add(TH2_hist_ST_tW_antitop_5f)
			combined_ST_hist.Add(TH2_hist_ST_tW_top_5f)

			all_combined_ST_hist.append(combined_ST_hist)

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
		if region in ["SB1b", "SB0b"]: use_filepath      = os.getenv('CMSSW_BASE') + "/src/combinedROOT/sideband_processedFiles/"

		sys_suffix = [""]
		if systematic != "nom":
			sys_updown = ["%s_up"%systematic,"%s_down"%systematic]
		elif systematic == "nom":
			sys_updown = ["nom"]

		all_combined_data_hist = []
		for sys_str in sys_updown:
			#print("Loading data hist %s/%s/%s"%(region,systematic,self.year))

			if region in ["SB1b","SB0b"]: combined_data_hist = ROOT.TH2F("combined_data_%s"%sys_str, ("data events in the %s (%s)"%(year,region)), 15 ,0.0, 8000, 12, 0.0, 2500)
			else:  combined_data_hist = ROOT.TH2F("combined_data_%s"%sys_str, ("data events in the %s (%s)"%(year,region)), 22,1250., 10000, 20, 500, 4000)
			#JetHT_"+ *dataBlock+"_"+*year+"_processed.root   -> naming scheme
			for data_block in data_blocks:
				#print("Looking for %s/%s/%s/%s"%(data_block,self.year,sys_str,region))
				hist_path_data = use_filepath + "%s_%s_processed.root"%(data_block,self.year)
				TH2_file_data = ROOT.TFile.Open(hist_path_data,"READ")
				hist_name_data = "h_MSJ_mass_vs_MdSJ_%s%s"%(self.technique_str, region )
				TH2_hist_data = TH2_file_data.Get(sys_str+"/"+hist_name_data) 
				combined_data_hist.Add(TH2_hist_data)

			ROOT.TH1.AddDirectory(False)
			combined_data_hist.SetDirectory(0)   # histograms lose their references when the file destructor is called
			all_combined_data_hist.append(combined_data_hist)
		return all_combined_data_hist  # load in TTbar historam, scale it, and return this version

	def linearize_plot(self,_hist,BR_type,region,systematic, forStats=False): 

		if systematic == "CMS_pdf" or systematic == "CMS_renorm" or systematic == "CMS_fact":
			sample_str = BR_type
			if BR_type == "sig":
				sample_str = "sig"
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
		if self.doSideband and region == "SB1b": use_indices = self.superbin_indices_SB1b
		elif self.doSideband and region == "SB0b": use_indices = self.superbin_indices_SB0b
		for iii,sys_str in enumerate(sys_updown):

			#if BR_type == "sig" and "SB" in region: print(" $$$$$$$$$$$$$$$$$$$$$$$$$ The PRE-linearized %s/%s/%s/%s signal histogram integral is %f"%(self.year,self.mass_point, systematic,region,_hist[iii].Integral()))

			#if BR_type == "sig" and "SB" in region and year in ["2016","2017","2018"] and systematic == "nom":
			#	_hist[0].Draw("colz")
			#	self.c.SaveAs("%s_%s_%s_%s_%s.png"%(self.mass_point,BR_type,region,systematic, self.year))

			linear_plot_size = len(use_indices)  
			#print("Creating a linearized histogram for %s/%s with %s bins."%(self.year,region,linear_plot_size))
			if forStats:
				linear_plot = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s) (UNSCALED); bin; Events / bin"%(BR_type,region,year, " ".join(use_sys.split("_"))),linear_plot_size,0,linear_plot_size)
				linear_plot.GetYaxis().SetTitleOffset(1.48)
			else:
				linear_plot = ROOT.TH1D("%s%s"%(BR_type,sys_str),"linearized %s in the %s (%s) (%s); bin; Events / bin"%(BR_type,region,year, " ".join(use_sys.split("_"))),linear_plot_size,0,linear_plot_size)
				linear_plot.GetYaxis().SetTitleOffset(1.48)
			for superbin_index,superbin in enumerate(use_indices):
				total_counts = 0
				for _tuple in superbin:

 
					if (_hist[iii].GetBinContent(_tuple[0]+1,_tuple[1]+1) < 0): ### need to verify if these need the +1 ...
						print("ERROR: negative histogram contribution when adding up superbins (bin = %s/%s, counts = %s)"%(_tuple[0]+1, _tuple[1]+1,_hist[iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)))
					total_counts+=_hist[iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)


					#if BR_type == "sig" and "SB" in region:
					#   print("Tuple %s yield is %f"%(_tuple, _hist[iii].GetBinContent(_tuple[0]+1,_tuple[1]+1)))
				#if BR_type == "sig" and "SB" in region:  print("------ superbin %s yield is %f"%(superbin_index,total_counts))

				#print("%s/%s/%s/%s ---- Superbin %s counts: %s"%(self.year, BR_type, region, systematic,superbin_index,  total_counts))
				linear_plot.SetBinContent(superbin_index+1,total_counts)
				try:
					linear_plot.SetBinError(superbin_index+1,sqrt(total_counts))
				except:
					print("ERROR: Failed setting bin error (superbin index = %s, counts = %s ) for %s/%s/%s/%s"%(superbin_index+1,total_counts, self.year,BR_type,region,systematic))
			ROOT.TH1.AddDirectory(False)
			linear_plot.SetDirectory(0)   # histograms lose their references when the file destructor is called
			#if BR_type == "sig"  and "SB" in region:   print(" @@@@@ The POST-linearized %s/%s/%s/%s signal histogram integral is %f"%(self.year,self.mass_point, systematic,region,linear_plot.Integral()))
			#print("superbin indices have size %s, linearized plot has size %s"%( len(self.superbin_indices), linear_plot.GetNbinsX()  )  )
			#print("The last linearized bin of %s/%s/%s/%s has content %s"%(BR_type, region, systematic, self.year,linear_plot.GetBinContent( linear_plot.GetNbinsX()  )))
			all_linear_plots.append(linear_plot)


		return all_linear_plots

	def write_histograms(self,forStats=False):

		if forStats:
			combine_file_name = self.output_file_home + "/combine_stats_%s%s_%s.root"%(self.technique_str, year,mass_point)   

		else:
			combine_file_name = self.output_file_home + "/combine_%s%s_%s.root"%(self.technique_str,year,mass_point)   
		combine_file = ROOT.TFile(combine_file_name,"RECREATE")
		combine_file.cd()

		regions = ["SR","CR","AT1b","AT0b"]
		if self.doSideband:
			regions.append("SB1b")
			regions.append("SB0b")

		QCD_hists    = [ self.QCD_linear_SR, self.QCD_linear_CR, self.QCD_linear_AT1b, self.QCD_linear_AT0b, self.QCD_linear_SB1b, self.QCD_linear_SB0b ]
		TTbar_hists  = [ self.TTbar_linear_SR, self.TTbar_linear_CR, self.TTbar_linear_AT1b, self.TTbar_linear_AT0b, self.TTbar_linear_SB1b, self.TTbar_linear_SB0b]
		ST_hists     = [ self.ST_linear_SR, self.ST_linear_CR, self.ST_linear_AT1b, self.ST_linear_AT0b,self.ST_linear_SB1b, self.ST_linear_SB0b]
		signal_hists = [ self.signal_linear_SR, self.signal_linear_CR, self.signal_linear_AT1b, self.signal_linear_AT0b, self.signal_linear_SB1b, self.signal_linear_SB0b]
		data_hists   = [ self.data_linear_SR, self.data_linear_CR, self.data_linear_AT1b, self.data_linear_AT0b,self.data_linear_SB1b,self.data_linear_SB0b ]

		combined_hists 	   = [ self.combined_linear_SR, self.combined_linear_CR, self.combined_linear_AT1b, self.combined_linear_AT0b, self.combined_linear_SB1b, self.combined_linear_SB0b ]  ### these are for writing unscaled histograms
		combined_hists_all = [ self.all_combined_linear_SR,self.all_combined_linear_CR, self.all_combined_linear_AT1b, self.all_combined_linear_AT0b, self.all_combined_linear_SB1b, self.all_combined_linear_SB0b]  ### these are for writing fully scaled, combined BR histograms

		max_index = 3
		if self.doSideband: max_index = 5
		for kkk, region in enumerate(regions):

			if kkk > max_index: continue
			### create folder for region
			combine_file.cd()
			ROOT.gDirectory.mkdir(region)
			combine_file.cd(region)

			systematics_ = self.systematic_names
			if forStats:
				systematics_ = ["nom"]

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

						if "fact" not in systematic and "renorm" not in systematic: 
							ST_hists[kkk][iii][jjj].Write()
					TTbar_hists[kkk][iii][jjj].Write()

					if not forStats:
						combined_hists_all[kkk][iii][jjj].Write()
					
			


			systematics_ = self.data_systematics
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

		"""for iii,systematic in enumerate(self.systematics):
			sys_suffix = [""]
			if systematic == "nom":
				sys_updown = ["nom"]
			elif systematic == "topPt":
				sys_updown = ["%s_up"%systematic]
			else:
				sys_updown = ["%s_up"%systematic,"%s_down"%systematic]

			for jjj,sys_str in enumerate(sys_updown):"""

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

	def load_superbin_indices(self,region="SR"):    # load in the superbin indices (located in a text file )
		_superbin_indices = []
		open_file = open(self.index_file_home+"/superbin_indices%s_%s.txt"%(self.technique_str,self.year),"r")
		for line in open_file:
			columns = line.split('/')
			if columns[0] == self.year and columns[1] == region:
				_superbin_indices = columns[3]
		open_file.close()
		return ast.literal_eval(_superbin_indices)

	def print_dataMC_ratio_plots(self):
		"""
			self.QCD_linear_SR.extend(self.linearize_plot(self.QCD_hist_SR[iii],"QCD","SR",systematic))
			self.TTbar_linear_SR.extend(self.linearize_plot(self.TTbar_hist_SR[iii],"TTbar","SR",systematic))

			self.QCD_linear_CR.extend(self.linearize_plot(self.QCD_hist_CR[iii],"QCD","CR",systematic))
			self.TTbar_linear_CR.extend(self.linearize_plot(self.TTbar_hist_CR[iii],"TTbar","CR",systematic))

			self.data_linear_SR.extend(self.linearize_plot(self.data_hist_SR[iii],"data","SR",systematic))
			self.data_linear_CR.extend(self.linearize_plot(self.data_hist_CR[iii],"data","CR",systematic))


		"""


		plot_home = os.getenv('CMSSW_BASE') + "/src/postprocess/plots/ratioPlots/"
		linear_plot_size = len(self.superbin_indices) 
		combined_BR_SR = ROOT.TH1D("combined_BR_SR","linearized BR in the SR (%s)"%(year),linear_plot_size,0,linear_plot_size)

		combined_BR_SR.Add(self.QCD_linear_SR[0])
		combined_BR_SR.Add(self.TTbar_linear_SR[0])


		combined_BR_CR = ROOT.TH1D("combined_BR_CR","linearized BR in the CR (%s)"%(year),linear_plot_size,0,linear_plot_size)

		combined_BR_CR.Add(self.QCD_linear_CR[0])
		combined_BR_CR.Add(self.TTbar_linear_CR[0])

		combined_BR_AT0b = ROOT.TH1D("combined_BR_AT0b","linearized BR in the antiTag (0b) CR (%s)"%(year),linear_plot_size,0,linear_plot_size)

		combined_BR_AT0b.Add(self.QCD_linear_AT0b[0])
		combined_BR_AT0b.Add(self.TTbar_linear_AT0b[0])

		combined_BR_AT1b = ROOT.TH1D("combined_BR_AT1b","linearized BR in the antiTag 1b CR (%s)"%(year),linear_plot_size,0,linear_plot_size)

		combined_BR_AT1b.Add(self.QCD_linear_AT1b[0])
		combined_BR_AT1b.Add(self.TTbar_linear_AT1b[0])


		combined_BR_SR.SetLineColor(ROOT.kRed)
		combined_BR_CR.SetLineColor(ROOT.kRed)
		combined_BR_AT0b.SetLineColor(ROOT.kRed)
		combined_BR_AT1b.SetLineColor(ROOT.kRed)

		self.data_linear_SR[0].SetLineColor(ROOT.kBlue)
		self.data_linear_CR[0].SetLineColor(ROOT.kBlue)
		self.data_linear_AT0b[0].SetLineColor(ROOT.kBlue)
		self.data_linear_AT1b[0].SetLineColor(ROOT.kBlue)

		rp_dataMC_SR = ROOT.TRatioPlot(self.data_linear_SR[0],combined_BR_SR);   ## data , MC
		rp_dataMC_CR = ROOT.TRatioPlot(self.data_linear_CR[0],combined_BR_CR);   ## data , MC

		rp_dataMC_AT0b = ROOT.TRatioPlot(self.data_linear_AT0b[0],combined_BR_AT0b);   ## data , MC
		rp_dataMC_AT1b = ROOT.TRatioPlot(self.data_linear_AT1b[0],combined_BR_AT1b);   ## data , MC

		rp_dataMC_SR.Draw("HIST")
		rp_dataMC_SR.GetLowerRefYaxis().SetTitle("data/MC ratio")
		rp_dataMC_SR.GetLowerRefGraph().SetMaximum(2.)
		rp_dataMC_SR.GetUpperRefYaxis().SetTitle("Events")
		c.SaveAs(plot_home+"rp_dataMC_SR.png")
		rp_dataMC_CR.Draw("HIST")
		rp_dataMC_CR.GetLowerRefYaxis().SetTitle("data/MC ratio")
		rp_dataMC_CR.GetLowerRefGraph().SetMaximum(2.)
		rp_dataMC_CR.GetUpperRefYaxis().SetTitle("Events")
		c.SaveAs(plot_home+"rp_dataMC_CR.png")
		rp_dataMC_AT0b.Draw("HIST")
		rp_dataMC_AT0b.GetLowerRefYaxis().SetTitle("data/MC ratio")
		rp_dataMC_AT0b.GetLowerRefGraph().SetMaximum(2.)
		rp_dataMC_AT0b.GetUpperRefYaxis().SetTitle("Events")
		c.SaveAs(plot_home+"rp_dataMC_AT0b.png")
		rp_dataMC_AT1b.Draw("HIST")
		rp_dataMC_AT1b.GetLowerRefYaxis().SetTitle("data/MC ratio")
		rp_dataMC_AT1b.GetLowerRefGraph().SetMaximum(2.)
		rp_dataMC_AT1b.GetUpperRefYaxis().SetTitle("Events")
		c.SaveAs(plot_home+"rp_dataMC_AT1b.png")


		# make ratio plots of the comparison of shapes of SR/CR and AT0b/AT1b in MC/data


		# normalized data
		data_linear_AT1b_norm = self.data_linear_AT1b[0].Clone()
		data_linear_AT1b_norm.SetTitle("normalized 1b anti-tag to 0b anti-tag comparison")
		data_linear_AT1b_norm.Scale(1/data_linear_AT1b_norm.Integral())

		data_linear_AT0b_norm = self.data_linear_AT0b[0].Clone()
		data_linear_AT0b_norm.SetTitle("normalized 1b anti-tag to 0b anti-tag comparison")
		data_linear_AT0b_norm.Scale(1.0/data_linear_AT0b_norm.Integral())
		data_linear_AT0b_norm.SetLineColor(ROOT.kRed)

		data_linear_CR_norm = self.data_linear_CR[0].Clone()
		data_linear_CR_norm.SetTitle("normalized SR CR comparison")
		data_linear_CR_norm.Scale(1.0/data_linear_CR_norm.Integral())
		data_linear_CR_norm.SetLineColor(ROOT.kRed)

		data_linear_SR_norm = self.data_linear_SR[0].Clone()
		data_linear_SR_norm.SetTitle("normalized SR CR comparison")
		data_linear_SR_norm.Scale(1.0/data_linear_SR_norm.Integral())


		# combined_BR_CR  combined_BR_SR  combined_BR_AT0b  combined_BR_AT1b

		#normalized MC
		combined_BR_CR_norm = combined_BR_CR.Clone()
		combined_BR_CR_norm.Scale(1.0/combined_BR_CR_norm.Integral())
		combined_BR_CR_norm.SetLineColor(ROOT.kRed)

		combined_BR_SR_norm= combined_BR_SR.Clone()
		combined_BR_SR_norm.Scale(1.0/combined_BR_SR_norm.Integral())

		combined_BR_AT0b_norm = combined_BR_AT0b.Clone()
		combined_BR_AT0b_norm.Scale(1.0/combined_BR_AT0b_norm.Integral())
		combined_BR_AT0b_norm.SetLineColor(ROOT.kRed)

		combined_BR_AT1b_norm = combined_BR_AT1b.Clone()
		combined_BR_AT1b_norm.Scale(1.0/combined_BR_AT1b_norm.Integral())

		rp_dataShape_antiTag = ROOT.TRatioPlot(data_linear_AT1b_norm,data_linear_AT0b_norm)  
		rp_MCShape_antiTag   = ROOT.TRatioPlot(combined_BR_AT1b_norm,combined_BR_AT0b_norm)  

		rp_dataShape_SRCR = ROOT.TRatioPlot(data_linear_SR_norm,data_linear_CR_norm)
		rp_MCShape_SRCR   = ROOT.TRatioPlot(combined_BR_SR_norm,combined_BR_CR_norm)   


		rp_dataShape_antiTag.Draw("HIST")
		rp_dataShape_antiTag.GetLowerRefYaxis().SetTitle("1b region/0b region ratio")
		rp_dataShape_antiTag.GetLowerRefGraph().SetMaximum(2.)
		rp_dataShape_antiTag.GetUpperRefYaxis().SetTitle("Events")
		c.SaveAs(plot_home+"rp_dataShape_antiTag.png")

		rp_MCShape_antiTag.Draw("HIST")
		rp_MCShape_antiTag.GetLowerRefYaxis().SetTitle("1b region MC / 0b region MC")
		rp_MCShape_antiTag.GetLowerRefGraph().SetMaximum(2.)
		rp_MCShape_antiTag.GetUpperRefYaxis().SetTitle("Events")
		c.SaveAs(plot_home+"rp_MCShape_antiTag.png")

		rp_dataShape_SRCR.Draw("HIST")
		rp_dataShape_SRCR.GetLowerRefYaxis().SetTitle("SR/CR")
		rp_dataShape_SRCR.GetLowerRefGraph().SetMaximum(2.)
		rp_dataShape_SRCR.GetUpperRefYaxis().SetTitle("Events")
		c.SaveAs(plot_home+"rp_dataShape_SRCR.png")

		rp_MCShape_SRCR.Draw("HIST")
		rp_MCShape_SRCR.GetLowerRefYaxis().SetTitle("SR MC /CR MC")
		rp_MCShape_SRCR.GetLowerRefGraph().SetMaximum(2.)
		rp_MCShape_SRCR.GetUpperRefYaxis().SetTitle("Events")
		c.SaveAs(plot_home+"rp_MCShape_SRCR.png")
		# modify this to make ratio plots of the shapes of the AT0b and AT1b regions
		# do a scaled SR / CR plot ... see how well the shapes match between the regions
		# do a comparison of MC shapes in the SR and CR 
	def kill_histograms(self):
		all_hist_lists = [self.TTbar_hist_SR ,self.ST_hist_SR ,self.data_hist_SR ,self.signal_hist_SR,self.QCD_hist_CR ,self.TTbar_hist_CR ,self.ST_hist_CR ,self.data_hist_CR ,
		self.signal_hist_CR,self.TTbar_hist_AT0b ,self.ST_hist_AT0b	 ,self.QCD_hist_AT0b   ,self.data_hist_AT0b  ,self.signal_hist_AT0b  ,self.TTbar_hist_AT1b ,self.ST_hist_AT1b,
		self.QCD_hist_AT1b   ,self.data_hist_AT1b  ,self.signal_hist_AT1b ,self.all_combined_hists_SR,self.all_combined_hists_CR,self.all_combined_hists_AT1b,self.all_combined_hists_AT0b,
		self.combined_linear_SR    ,self.combined_linear_CR , self.combined_linear_AT1b  ,self.combined_linear_AT0b,self.QCD_linear_SR, self.TTbar_linear_SR ,self.ST_linear_SR,
		self.data_linear_SR  ,self.signal_linear_SR,self.QCD_linear_CR 	 ,self.TTbar_linear_CR ,self.ST_linear_CR    ,self.data_linear_CR  ,self.signal_linear_CR,self.QCD_linear_AT0b ,
		self.TTbar_linear_AT0b  ,self.ST_linear_AT0b     ,self.data_linear_AT0b   ,self.signal_linear_AT0b ,self.QCD_linear_AT1b ,self.TTbar_linear_AT1b ,self.ST_linear_AT1b ,self.data_linear_AT1b ,
		self.signal_linear_AT1b,self.all_combined_linear_SR  ,self.all_combined_linear_CR  ,self.all_combined_linear_AT1b,self.all_combined_linear_AT0b]

		for hist_list in all_hist_lists:
			for hist in hist_list:
				del hist
		return

if __name__=="__main__":
	start_time = time.time()
	mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1","Suu5_chi1p5","Suu5_chi2","Suu6_chi1","Suu6_chi1p5","Suu6_chi2","Suu6_chi2p5","Suu7_chi1",
   "Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3","Suu8_chi1","Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"]
	years = ["2015","2016","2017","2018"]
	regions = ["SR","CR","SB1b","SB0b"] # 

	technique_strs = ["","NN_"]
	technique_strs = [""]

	technique_descr = ["cut-based", "NN-based"]
	for year in years:
		for mass_point in mass_points:
			for iii,technique_str in enumerate(technique_strs):
				#try:
				print("Running for %s/%s/%s"%(year,mass_point,technique_str))
				final_plot = linearized_plot(year, mass_point, technique_str)
				#print("final_plot value for QCD %s %s : %s"%(year, region,final_plot.QCD_hist.GetBinContent( final_plot.QCD_hist.GetMaximumBin() )) )
				#print("final_plot value for TTbar %s %s : %s"%(year, region,final_plot.TTbar_hist.GetBinContent( final_plot.TTbar_hist.GetMaximumBin() ))   )
				#print("%s/%s/%s: the superbin indices have size %s"%(technique_descr[iii],year, mass_point,len(final_plot.superbin_indices)))
				#except:
				#	print("Failed for %s/%s/%s"%(year,mass_point,technique_descr[iii]))
	print("Script took %ss to run."%(	np.round(time.time() - start_time,4 )) )

# create one root file for each year containing all the systematics = another level of folders
#   syst_suffix/region/hists
#   JEC_up/SR/QCD



