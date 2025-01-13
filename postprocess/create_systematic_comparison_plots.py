import numpy as np
import sys, os
import ROOT
from write_cms_text import write_cms_text
from return_BR_SF.return_BR_SF import return_BR_SF
from return_signal_SF.return_signal_SF import return_signal_SF

from math import isnan
# create +- ratio plots for a given histogram and systematic

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


def divide_histograms(hist1, hist2):
	# Create a new histogram to store the result
	result_hist = hist1.Clone()
	result_hist.Reset()

	# Loop over bins and divide contents
	for bin in range(1, hist1.GetNbinsX() + 1):
		content1 = hist1.GetBinContent(bin)
		content2 = hist2.GetBinContent(bin)

		# Check if content of second histogram is not zero
		if content2 > 1e-4:
			# Calculate ratio and set bin content
			ratio = content1 / content2
			result_hist.SetBinContent(bin, ratio)
		else:
			result_hist.SetBinContent(bin, 1.0)

	return result_hist
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

### this is needed for setting the ratio plot axes
def get_maxmin_bin_content(histogram):
	max_content = 0
	min_content = 1e15
	for i in range(1, histogram.GetNbinsX() + 1):
		bin_content = histogram.GetBinContent(i)
		if bin_content > max_content:
			max_content = bin_content

	for i in range(1, histogram.GetNbinsX() + 1):
		bin_content = histogram.GetBinContent(i)
		if bin_content < min_content:
			min_content = bin_content
	return max_content,min_content

def create_3_hist_ratio_plot(up_hist,nom_hist,down_hist, hist_type, systematic, year, sample_type, sample_description, isSignal=False):

	ROOT.TH1.AddDirectory(False)
	if isSignal:
		output_dir = "plots/systematic_comparison_plots/signal/"
	else:
		output_dir = "plots/systematic_comparison_plots/"
	output_plot_name = output_dir+"%s_%s_%s_SysComparison_RatioPlot_SR_%s.png"%(hist_name,sample_type, systematic,year)
	#### cms label stuff 
	CMS_label_pos = 0.152
	SIM_label_pos = 0.295

	up_hist = clean_histogram(up_hist, sample_type,systematic)
	down_hist = clean_histogram(down_hist, sample_type,systematic)
	nom_hist = clean_histogram(nom_hist, sample_type,systematic)


	canvas = ROOT.TCanvas("canvas", "Histograms", 1200, 1000)
	up_hist.SetTitle("%s MC %s in the SR for up/nom/down %s uncertainties (%s)"%(sample_description, hist_type, systematic,convert_year(year)))
	down_hist.SetTitle("%s MC %s in the SR for up/nom/down %s uncertainties (%s)"%(sample_description, hist_type, systematic,convert_year(year)))

	up_hist.SetLineWidth(3)
	nom_hist.SetLineWidth(5)
	down_hist.SetLineWidth(3)

	ROOT.gStyle.SetOptStat(0)

	# Create a canvas to plot histograms
	canvas.Divide(1, 2)  # Divide canvas into two pads

				   # xlow, ylow, xhigh, yhigh
	canvas.cd(1).SetPad(0.0, 0.3, 1.0, 1.0) 
	canvas.cd(2).SetPad(0.0, 0.0, 1.0, 0.3) 

	# Upper pad for histogram plots
	canvas.cd(1)
	up_hist.SetLineColor(ROOT.kRed)
	nom_hist.SetLineColor(ROOT.kBlack)
	down_hist.SetLineColor(ROOT.kBlue)
	up_hist.Draw("HIST")
	nom_hist.Draw("SAME,HIST")
	down_hist.Draw("SAME.HIST")
	legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
	legend.AddEntry(up_hist, "up systematic", "l")
	legend.AddEntry(nom_hist, "nom systematic", "l")
	legend.AddEntry(down_hist, "down systematic", "l")
	legend.Draw()

	## keep the histograms from being cut off
	max_bin_content = max(max(up_hist.GetMaximum(), nom_hist.GetMaximum()), down_hist.GetMaximum()   )
	up_hist.GetYaxis().SetRangeUser(0, max_bin_content * 1.1)

	#canvas.Update()

	write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)

	# Lower pad for ratio plots
	canvas.cd(2)

	ratio1_2 = up_hist.Clone("ratio1_2")



	ratio1_2 = divide_histograms(ratio1_2,nom_hist)

	ratio1_2.SetTitle(hist_type + " up and down systematics / nom systematic")
	ratio1_2.GetYaxis().SetTitle("Ratio")
	ratio1_2.SetLineColor(ROOT.kRed)
	ratio1_2.Draw("HIST")

	ratio1_3 = down_hist.Clone("ratio1_3")

	ratio1_3 = divide_histograms(ratio1_3,nom_hist)
	ratio1_3.SetTitle(hist_type + " up and down systematics / nom systematic")
	ratio1_3.GetYaxis().SetTitle("Ratio")
	#ratio1_3.Divide(up_hist)
	ratio1_3.SetLineColor(ROOT.kBlue)
	ratio1_3.Draw("SAME.HIST")

	max_content_r12, min_content_r12 = get_maxmin_bin_content(ratio1_2)
	max_content_r13, min_content_r13 = get_maxmin_bin_content(ratio1_3)
	max_bin_content_ratio = max(max_content_r12, max_content_r13)
	min_bin_content_ratio = min(min_content_r12, min_content_r13)
	

	if max_bin_content_ratio > 2.5:
		max_bin_content_ratio = 2.5

	if min_bin_content_ratio < 0.3:
		min_bin_content_ratio = 0.3

	canvas.cd(2)

	# Get the lower pad

	#print("--------------- The max/min y values are %s/%s"%(max_bin_content_ratio,min_bin_content_ratio))

	ratio1_2.GetYaxis().SetRangeUser(min_bin_content_ratio/0.8, max_bin_content_ratio*1.15)
	canvas.Update();

	#ratio1_2.GetYaxis().SetRangeUser(min_bin_content_ratio/0.8, max_bin_content_ratio*1.15)


	ratio1_2.SetMinimum(min_bin_content_ratio)
	ratio1_2.SetMaximum(max_bin_content_ratio)

	ratio1_2.GetYaxis().SetLimits(min_bin_content_ratio, max_bin_content_ratio)

	canvas.Update()

	legend_ratio = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
	legend_ratio.AddEntry(ratio1_2, "up/nom systematic", "l")
	legend_ratio.AddEntry(ratio1_3, "down/nom systematic", "l")
	legend_ratio.Draw()

	### create ratio lines at 0.8, 1.0, 1.2
	nom_line = ROOT.TLine(ratio1_2.GetXaxis().GetXmin(), 1.0, ratio1_2.GetXaxis().GetXmax(), 1.0)
	nom_line.SetLineStyle(2)  # Dotted line style
	nom_line.Draw("same")

	nom_line_up = ROOT.TLine(ratio1_2.GetXaxis().GetXmin(), 1.2, ratio1_2.GetXaxis().GetXmax(), 1.2)
	nom_line_up.SetLineStyle(2)  # Dotted line style
	nom_line_up.Draw("same")


	nom_line_down = ROOT.TLine(ratio1_2.GetXaxis().GetXmin(), 0.8, ratio1_2.GetXaxis().GetXmax(), 0.8)
	nom_line_down.SetLineStyle(2)  # Dotted line style
	nom_line_down.Draw("same")


	canvas.Update()

	canvas.SaveAs(output_plot_name)

	return


def create_systematic_comparison_plot(hist_name, hist_type,systematic, year,sample_type):

	ROOT.TH1.AddDirectory(False)
	input_file_dir = "../combinedROOT/processedFiles/"

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

	if(systematic != "topPt"):
		QCD_combined_down	= get_combined_histogram(QCD_file_names, hist_name, systematic+"_down", QCD_weights, systematic)
		QCD_combined_up		= get_combined_histogram(QCD_file_names, hist_name, systematic+"_up", QCD_weights, systematic)
	else:
		QCD_combined_up = QCD_combined_nom.Clone()
		QCD_combined_down = QCD_combined_nom.Clone()
		

	TTbar_combined_nom  = get_combined_histogram(TTbar_file_names, hist_name, 			   "nom", TTbar_weights, systematic)

	if(systematic != "topPt"):
		TTbar_combined_down = get_combined_histogram(TTbar_file_names, hist_name, systematic+"_down", TTbar_weights, systematic)
		TTbar_combined_up   = get_combined_histogram(TTbar_file_names, hist_name, systematic+"_up", TTbar_weights, systematic)
	else:
		TTbar_combined_down = TTbar_combined_nom.Clone()
		TTbar_combined_up = TTbar_combined_nom.Clone()


	ST_combined_nom 	= get_combined_histogram(ST_file_names, hist_name, 			  "nom", ST_weights, systematic)
	if(systematic != "topPt"):
		ST_combined_up 		= get_combined_histogram(ST_file_names, hist_name, systematic+"_up", ST_weights, systematic)
		ST_combined_down 	= get_combined_histogram(ST_file_names, hist_name, systematic+"_down", ST_weights, systematic)

	else:
		ST_combined_up = ST_combined_nom.Clone()
		ST_combined_down = ST_combined_nom.Clone()
	
	WJets_combined_nom  = get_combined_histogram(WJets_file_names, hist_name, 			   "nom", WJets_weights, systematic)

	if(systematic != "topPt"):
		WJets_combined_down = get_combined_histogram(WJets_file_names, hist_name, systematic+"_down", WJets_weights, systematic)
		WJets_combined_up   = get_combined_histogram(WJets_file_names, hist_name, systematic+"_up", WJets_weights, systematic)
	else:
		WJets_combined_down = WJets_combined_nom.Clone()
		WJets_combined_up = WJets_combined_nom.Clone()


	allBR_up  = QCD_combined_up
	allBR_up.Add(TTbar_combined_up)
	allBR_up.Add(WJets_combined_up)
	allBR_up.Add(ST_combined_up)

	allBR_nom = QCD_combined_nom
	allBR_nom.Add(TTbar_combined_nom)
	allBR_nom.Add(WJets_combined_nom)
	allBR_nom.Add(ST_combined_nom)	

	allBR_down = QCD_combined_down
	allBR_down.Add(TTbar_combined_down)
	allBR_down.Add(WJets_combined_down)
	allBR_down.Add(ST_combined_down)		

	### now make histograms

	create_3_hist_ratio_plot(allBR_up,allBR_nom,allBR_down, hist_type, systematic, year, "allBR", "Combined BR")


	## create the ratio plots for the partially-merged backgrounds

	create_3_hist_ratio_plot(QCD_combined_up,QCD_combined_nom,QCD_combined_down, hist_type, systematic, year, "QCD", "QCD")
	create_3_hist_ratio_plot(TTbar_combined_up,TTbar_combined_nom,TTbar_combined_down, hist_type, systematic, year, "TTbar","TTbar")
	create_3_hist_ratio_plot(WJets_combined_up,WJets_combined_nom,WJets_combined_down, hist_type, systematic, year, "WJets","WJets")
	create_3_hist_ratio_plot(ST_combined_up,ST_combined_nom,ST_combined_down, hist_type, systematic, year, "ST", "Single Top")

	return

def create_signal_systematic_comparison_plot(hist_name, hist_type, systematic, year,sample_type, masss_point):
	ROOT.TH1.AddDirectory(False)

	input_file_dir = "../combinedROOT/processedFiles/"

	decays = ["WBWB","ZTZT","HTHT","WBHT","WBZT","HTZT"]

	signal_file_names = [ input_file_dir+ mass_point + "_" + decay + "_" + year+  "_processed.root" for decay in decays   ]

	signal_weights 		= [ return_signal_SF(year,mass_point, decay) for decay in decays ]

	signal_nom		= get_combined_histogram(signal_file_names, hist_name, 			"nom", 	   signal_weights, systematic)
	signal_down		= get_combined_histogram(signal_file_names, hist_name, systematic+"_down", signal_weights, systematic)
	signal_up		= get_combined_histogram(signal_file_names, hist_name, systematic+"_up",   signal_weights, systematic)
	
	create_3_hist_ratio_plot(signal_up,signal_nom,signal_down, hist_type, systematic, year, mass_point, "Combined Signal (%s)"%mass_point)

	return

if __name__== "__main__":

	years 	= ["2015","2016","2017","2018"]
	systematics = ["nom",   "bTagSF_med",   "bTagSF_tight",     "bTagSF_med_corr",   "bTagSF_tight_corr",   "JER",	 "JEC",    "bTag_eventWeight_bc_T_corr", "bTag_eventWeight_light_T_corr", "bTag_eventWeight_bc_M_corr", "bTag_eventWeight_light_M_corr", "bTag_eventWeight_bc_T_year", "bTag_eventWeight_light_T_year", "bTag_eventWeight_bc_M_year", "bTag_eventWeight_light_M_year",		"JER_eta193",	 "JER_193eta25",	  "JEC_FlavorQCD",	"JEC_RelativeBal",		    "JEC_Absolute",	   "JEC_BBEC1_year",	 "JEC_Absolute_year",	  "JEC_RelativeSample_year",	 "PUSF",	 "topPt",	 "L1Prefiring",	     "pdf",	   "renorm",	 "fact",	 "JEC_AbsoluteCal",	     "JEC_AbsoluteTheory",	  "JEC_AbsolutePU",	     "JEC_AbsoluteScale",		  "JEC_Fragmentation",	     "JEC_AbsoluteMPFBias",	   "JEC_RelativeFSR" ]  # , "bTagSF_tight", "bTagSF_med" 

	hist_names = ["h_SJ_mass_SR", "h_disuperjet_mass_SR","h_SJ_mass_NN_SR", "h_disuperjet_mass_NN_SR"]  #histogram name for Getting
	hist_types = ["superjet mass (cut-based)", "diSuperjet mass (cut-based)", "superjet mass (NN-based)", "diSuperjet mass (NN-based)"]   # description of histogram

	mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1","Suu5_chi1p5","Suu5_chi2","Suu6_chi1","Suu6_chi1p5","Suu6_chi2","Suu6_chi2p5","Suu7_chi1","Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3","Suu8_chi1","Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"]

	#### don't want all mass points, will crash pc 
	#mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1p5","Suu6_chi2","Suu7_chi2p5", "Suu8_chi3"]


	for year in years:
		for iii,hist_name in enumerate(hist_names):
			for systematic in systematics:
				try:

					create_systematic_comparison_plot(hist_name, hist_types[iii], systematic, year, hist_types[iii])
				except:
					print("ERROR: Failed for %s, %s %s"%(hist_name,systematic,year))
	"""
	for year in years:
		for iii,hist_name in enumerate(hist_names):
			for systematic in systematics:
				if systematic == "topPt": continue
				for mass_point in mass_points:
					print("----- Making plot for %s/%s/%s/%s"%(mass_point,hist_name,systematic,year))
					create_signal_systematic_comparison_plot(hist_name, hist_types[iii], systematic, year, hist_types[iii],mass_point)
	"""




