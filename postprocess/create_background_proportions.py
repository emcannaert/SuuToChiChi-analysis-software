import numpy as np
import sys, os
import ROOT
from write_cms_text import write_cms_text
from return_BR_SF.return_BR_SF import return_BR_SF
from return_signal_SF.return_signal_SF import return_signal_SF

from math import isnan



# this script opens the output files from readTree_test.C, grabs the h_totHT_1b histograms from within 

ROOT.TH1.SetDefaultSumw2()
ROOT.TH2.SetDefaultSumw2()

def convert_year(year):
	year_dict = {"2015":"2016preAPV", "2016":"2016postAPV", "2017":"2017","2018":"2018"}
	return year_dict[year]

def clean_histogram(hist, sample, systematic):
	ROOT.TH1.AddDirectory(False)
	for iii in range(1, hist.GetNbinsX()+1):
		if (isnan(hist.GetBinContent(iii))) or (hist.GetBinContent(iii) == float("inf")) or (hist.GetBinContent(iii) == float("-inf")) or ( abs(hist.GetBinContent(iii))> 1e10) :
			print("Bad value in %s/%s"%(sample,systematic))
			hist.SetBinContent(iii,0)

	return hist
def get_combined_histogram(file_names, hist_name,folder, weights,systematic):

	ROOT.TH1.AddDirectory(False)
	f1 = ROOT.TFile(file_names[0],"r")

	folder_name = folder+"/"+hist_name
	print("Looking for TFile %s and histogram name %s"%(file_names[0],folder_name))
	combined_hist = f1.Get(folder_name)
	combined_hist.Scale(weights[0])
	for iii in range(1,len(file_names)):

		#print("Looking at %s"%file_names[iii])

		try:
			f2 = ROOT.TFile(file_names[iii],"r")
			h2 = clean_histogram( f2.Get(folder+"/"+hist_name), file_names[iii], systematic)
			h2.Scale(weights[iii])
			combined_hist.Add(h2)
		except:
			print("ERROR with %s/%s/%s"%(file_names[iii],hist_name,folder))
	return combined_hist


def create_systematic_comparison_plot(hist_name, hist_type,systematic, year,sample_type):

	ROOT.TH1.AddDirectory(False)
	input_file_dir = "../combinedROOT/processedFiles/test/"

	QCD_samples = ["QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_"]
	TTbar_samples = ["TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_"]
	ST_samples = ["ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"]	
	WJets_samples = ["WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"]	

	QCD_file_names 	 = [input_file_dir+ QCD_sample  + year + "_processed.root" for QCD_sample in QCD_samples]
	TTbar_file_names = [input_file_dir+ TTbar_sample   + year + "_processed.root" for TTbar_sample in TTbar_samples]
	ST_file_names 	 = [input_file_dir+ ST_sample   + year + "_processed.root" for ST_sample in ST_samples]
	WJets_file_names 	 = [input_file_dir+ WJets_sample   + year + "_processed.root" for WJets_sample in WJets_samples]

	# get QCD histograms

	all_weights = return_BR_SF()

	QCD_weights 		= [all_weights["QCDMC1000to1500"][year],all_weights["QCDMC1500to2000"][year],all_weights["QCDMC2000toInf"][year] ]
	TTbar_weights 		= [all_weights["TTJetsMCHT1200to2500"][year],all_weights["TTJetsMCHT2500toInf"][year]]
	ST_weights			= [all_weights["ST_t_channel_top_inclMC"][year],all_weights["ST_t_channel_antitop_incMC"][year],all_weights["ST_s_channel_hadronsMC"][year],all_weights["ST_s_channel_leptonsMC"][year],all_weights["ST_tW_antiTop_inclMC"][year],all_weights["ST_tW_top_inclMC"][year]]
	WJets_weights		= [all_weights["WJetsMC_LNu_HT800to1200"][year],all_weights["WJetsMC_LNu_HT1200to2500"][year],all_weights["WJetsMC_LNu_HT2500toInf"][year],all_weights["WJetsMC_QQ_HT800toInf"][year]]


	QCD_combined_nom	= get_combined_histogram(QCD_file_names, hist_name, 			"nom", QCD_weights, systematic)
	TTbar_combined_nom  = get_combined_histogram(TTbar_file_names, hist_name, 			   "nom", TTbar_weights, systematic)
	ST_combined_nom 	= get_combined_histogram(ST_file_names, hist_name, 			  "nom", ST_weights, systematic)
	WJets_combined_nom  = get_combined_histogram(WJets_file_names, hist_name, 			   "nom", WJets_weights, systematic)



	allBR_nom = QCD_combined_nom.Clone("allBR_nom")
	allBR_nom.Add(TTbar_combined_nom)
	allBR_nom.Add(WJets_combined_nom)
	allBR_nom.Add(ST_combined_nom)	

	output_text_name = "txt_files/background_proporitons_%s_%s.txt"%(hist_name,year)
	output_file = open(output_text_name,"w")
	output_file.write("bin     HT_center    QCD_frac     TTbar_frac     WJets_frac     ST_frac \n")

	for iii in range(1,allBR_nom.GetNbinsX()+1):
		total_bin_yield  = allBR_nom.GetBinContent(iii)
		if total_bin_yield < 1e-10:
			QCD_proportion       = 0
			TTbar_proportion     = 0
			WJets_proportion     = 0
			ST_proportion        = 0
		else:
			QCD_proportion   = QCD_combined_nom.GetBinContent(iii)   / total_bin_yield
			TTbar_proportion = TTbar_combined_nom.GetBinContent(iii) / total_bin_yield
			WJets_proportion = WJets_combined_nom.GetBinContent(iii) / total_bin_yield
			ST_proportion    = ST_combined_nom.GetBinContent(iii)    / total_bin_yield

		output_file.write("%s     %s     %s     %s     %s     %s\n"%( iii, allBR_nom.GetBinCenter(iii), QCD_proportion, TTbar_proportion,  WJets_proportion,  ST_proportion))

	output_file.close()

	return


if __name__== "__main__":

	years 	= ["2015","2016","2017","2018"]

	hist_names = [ "h_totHT_1b" ]  
	hist_types = [ "Event H_{T} (1b region)"  ]   

	for year in years:
		for iii,hist_name in enumerate(hist_names):
			#try:
			create_systematic_comparison_plot(hist_name, hist_types[iii], "nom", year, hist_types[iii])
			#except:
			#	print("ERROR: Failed for %s, %s %s"%(hist_name,year))




