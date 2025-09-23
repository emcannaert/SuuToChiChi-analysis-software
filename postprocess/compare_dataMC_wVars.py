import numpy as np
import sys, os
import ROOT
from write_cms_text import write_cms_text
from return_BR_SF.return_BR_SF import return_BR_SF
from return_signal_SF.return_signal_SF import return_signal_SF
from return_data_samples.return_data_samples import return_data_samples

from math import isnan


# creates comparison of data/MC with jet variations for NN scores for combined samples



ROOT.TH1.SetDefaultSumw2()
ROOT.TH2.SetDefaultSumw2()

def convert_year(year):
	year_dict = {"2015":"2016preAPV", "2016":"2016postAPV", "2017":"2017","2018":"2018"}
	return year_dict[year]

def clean_histogram(hist, sample, systematic):
	ROOT.TH1.AddDirectory(False)
	hist.Sumw2()
	for iii in range(1, hist.GetNbinsX()+1):
		if (isnan(hist.GetBinContent(iii))) or (hist.GetBinContent(iii) == float("inf")) or (hist.GetBinContent(iii) == float("-inf")) or ( abs(hist.GetBinContent(iii))> 1e10) :
			print("Bad value in %s/%s"%(sample,systematic))
			hist.SetBinContent(iii,0)

	return hist


def get_combined_histogram(file_names, hist_name ,folder, weights,systematic):

	ROOT.TH1.AddDirectory(False)
	f1 = ROOT.TFile(file_names[0],"r")

	folder_name   = folder+"/"+hist_name

	print("Looking for TFile %s and histogram names %s"%(file_names[0],folder_name))

	combined_hist = f1.Get(folder_name)
	combined_hist.Sumw2()
	combined_hist.Scale(weights[0])


	for iii in range(1,len(file_names)):
		#try:

		#print("Getting file %s."%file_names[iii])
		f2 = ROOT.TFile(file_names[iii],"r")

		h2 = clean_histogram( f2.Get(folder+"/"+hist_name), file_names[iii], systematic)
		h2.Sumw2()
		h2.Scale(weights[iii])

		combined_hist.Add(h2)

	return combined_hist


def create_systematic_comparison_plot(year, hist_name, hist_title, debug=False):


	canvas = ROOT.TCanvas("","",1200,1000)

	output_dir = "plots/hist_comparisons/"
	input_file_dir = "../combinedROOT/processedFiles/"

	# Define the upper and lower pad sizes
	pad1 = ROOT.TPad("pad1", "Upper Pad", 0, 0.29, 1, 1)
	pad2 = ROOT.TPad("pad2", "Lower Pad", 0, 0, 1, 0.3)

	# Set margins
	pad1.SetBottomMargin(0.02)  # Reduce margin to align with lower pad
	pad2.SetTopMargin(0.02)
	pad2.SetBottomMargin(0.3)   # Increase bottom margin for ratio plot


	ROOT.TH1.AddDirectory(False)




	QCD_samples = ["QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_"]
	TTbar_samples = ["TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_"]
	ST_samples = ["ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"]	
	WJets_samples = ["WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"]	

	QCD_file_names 	 = [input_file_dir+ QCD_sample  + year + "_processed.root" for QCD_sample in QCD_samples]
	TTbar_file_names = [input_file_dir+ TTbar_sample   + year + "_processed.root" for TTbar_sample in TTbar_samples]
	ST_file_names 	 = [input_file_dir+ ST_sample   + year + "_processed.root" for ST_sample in ST_samples]
	WJets_file_names 	 = [input_file_dir+ WJets_sample   + year + "_processed.root" for WJets_sample in WJets_samples]

	# get QCD histograms

	all_weights = return_BR_SF()

	QCD_weights 		= [all_weights["QCDMC1000to1500"][year],all_weights["QCDMC1500to2000"][year],all_weights["QCDMC2000toInf"][year] ]
	TTbar_weights 		= [all_weights["TTJetsMCHT800to1200"][year],all_weights["TTJetsMCHT1200to2500"][year],all_weights["TTJetsMCHT2500toInf"][year]]
	ST_weights			= [all_weights["ST_t_channel_top_inclMC"][year],all_weights["ST_t_channel_antitop_inclMC"][year],all_weights["ST_s_channel_hadronsMC"][year],all_weights["ST_s_channel_leptonsMC"][year],all_weights["ST_tW_antiTop_inclMC"][year],all_weights["ST_tW_top_inclMC"][year]]
	WJets_weights		= [all_weights["WJetsMC_LNu_HT800to1200"][year],all_weights["WJetsMC_LNu_HT1200to2500"][year],all_weights["WJetsMC_LNu_HT2500toInf"][year],all_weights["WJetsMC_QQ_HT800toInf"][year]]

	QCD_combined_nom	= get_combined_histogram(QCD_file_names, hist_name,			"nom", QCD_weights, "nom")
	TTbar_combined_nom  = get_combined_histogram(TTbar_file_names, hist_name,			   "nom", TTbar_weights, "nom")
	ST_combined_nom 	= get_combined_histogram(ST_file_names, hist_name,			  "nom", ST_weights, "nom")
	WJets_combined_nom  = get_combined_histogram(WJets_file_names, hist_name,			   "nom", WJets_weights, "nom")

	allBR_nom = QCD_combined_nom.Clone("allBR_nom")
	allBR_nom.Sumw2()
	allBR_nom.Add(TTbar_combined_nom)
	allBR_nom.Add(WJets_combined_nom)
	allBR_nom.Add(ST_combined_nom)	
	allBR_nom.SetTitle(hist_title)



	### get data histogram
	data_samples = return_data_samples(year)
	data_weights = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

	data_file_names 	 = [input_file_dir+ data_sample + "_"  + year + "_processed.root" for data_sample in data_samples]
	data_combined        = get_combined_histogram(data_file_names, hist_name,			"nom", data_weights, "nom")

	print("Data has %s total events,  "%(data_combined.Integral()))

	jet_systematics = [   
	 "JER_eta193",
	 "JER_193eta25",

	 "JEC_FlavorQCD",
	 "JEC_RelativeBal",
	 "JEC_BBEC1_year",
	 "JEC_AbsoluteScale",
	 "JEC_Fragmentation",
	 "JEC_AbsoluteMPFBias",
	 "JEC_RelativeFSR",
	 "JEC_Absolute_year",
	 "JEC_RelativeSample_year",
	 "JEC_AbsoluteCal",
	  "JEC_AbsolutePU" ]    # 	"JEC_AbsoluteCal",
							


	# 	 "JEC_Absolute"   
	#    "JEC_AbsolutePU",
  	#    "CMS_bTagSF_bc_M_year",
	#    "CMS_bTagSF_light_M_year",
	#    "CMS_bTagSF_bc_M_corr",
	#    "CMS_bTagSF_light_M_corr",

	### loop over the systematics

	#total_bin_vars_up   = np.array([0]*allBR_nom.GetNbinsX()   )
	#total_bin_vars_down = np.array([0]*allBR_nom.GetNbinsX()   )

	total_bin_vars_up   = np.zeros(allBR_nom.GetNbinsX(), dtype=np.float64)
	total_bin_vars_down = np.zeros(allBR_nom.GetNbinsX(), dtype=np.float64)

	for systematic in jet_systematics:

		### get the UP allBR histogram variations
		QCD_combined_up	   = get_combined_histogram(QCD_file_names, hist_name,			systematic+"_up" , QCD_weights, systematic+"_up")
		TTbar_combined_up  = get_combined_histogram(TTbar_file_names, hist_name,			   systematic+"_up" , TTbar_weights, systematic+"_up")
		ST_combined_up 	   = get_combined_histogram(ST_file_names, hist_name,			  systematic+"_up", ST_weights, systematic+"_up")
		WJets_combined_up  = get_combined_histogram(WJets_file_names, hist_name,			   systematic+"_up", WJets_weights, systematic+"_up")

		allBR_up = QCD_combined_up.Clone("allBR_var_up")
		allBR_up.Sumw2()
		allBR_up.Add(TTbar_combined_up)
		allBR_up.Add(WJets_combined_up)
		allBR_up.Add(ST_combined_up)	

		allBR_up.Sumw2()

		### get the DOWN allBR histogram variations
		QCD_combined_down	= get_combined_histogram(QCD_file_names, hist_name,			systematic+"_down", QCD_weights, systematic+"_down")
		TTbar_combined_down  = get_combined_histogram(TTbar_file_names, hist_name,			   systematic+"_down", TTbar_weights, systematic+"_down")
		ST_combined_down 	= get_combined_histogram(ST_file_names, hist_name,			  systematic+"_down", ST_weights, systematic+"_down")
		WJets_combined_down  = get_combined_histogram(WJets_file_names, hist_name,			   systematic+"_down", WJets_weights, systematic+"_down")

		allBR_down = QCD_combined_down.Clone("allBR_var_down")
		allBR_down.Sumw2()
		allBR_down.Add(TTbar_combined_down)
		allBR_down.Add(WJets_combined_down)
		allBR_down.Add(ST_combined_down)	



		### delete hists that are no longer needed
		del QCD_combined_up, TTbar_combined_up, ST_combined_up, WJets_combined_up
		del QCD_combined_down, TTbar_combined_down, ST_combined_down, WJets_combined_down

		up_hist_vars = []
		down_hist_vars = []

		for iii in range(1,allBR_nom.GetNbinsX()+1):
			if abs(allBR_nom.GetBinContent(iii)) > 0 :

				#print("For bin %s, nom hist has rate = %s, up hist has rate %s, giving a difference %s and fractional difference %s."%(iii, allBR_nom.GetBinContent(iii),  allBR_up.GetBinContent(iii) ,allBR_up.GetBinContent(iii)-  allBR_nom.GetBinContent(iii), (allBR_up.GetBinContent(iii)-  allBR_nom.GetBinContent(iii))/ allBR_nom.GetBinContent(iii) ))
				#print("For bin %s, nom hist has rate = %s, down hist has rate %s, giving a difference %s and fractional difference %s."%(iii, allBR_nom.GetBinContent(iii),  allBR_down.GetBinContent(iii) ,allBR_down.GetBinContent(iii)-  allBR_nom.GetBinContent(iii), (allBR_down.GetBinContent(iii)-  allBR_nom.GetBinContent(iii))/ allBR_nom.GetBinContent(iii) ))

				up_hist_vars.append(  abs(allBR_up.GetBinContent(iii)-allBR_nom.GetBinContent(iii))/ allBR_nom.GetBinContent(iii)  )  ### subtract up_hist bin value from the nom_hist value
				down_hist_vars.append( abs(allBR_down.GetBinContent(iii)-allBR_nom.GetBinContent(iii)) / allBR_nom.GetBinContent(iii)     )  ### subtract down_hist bin value from the nom_hist value
			else:
				up_hist_vars.append(0) 
				down_hist_vars.append(0) 


		final_bin_vars_up   = np.zeros(allBR_nom.GetNbinsX(), dtype=np.float64)
		final_bin_vars_down = np.zeros(allBR_nom.GetNbinsX(), dtype=np.float64)


		## get largest variation in each bin
		for iii in range(0, allBR_nom.GetNbinsX()):
			final_bin_vars_up[iii] = max( abs(up_hist_vars[iii]), abs(down_hist_vars[iii])   )
			final_bin_vars_down[iii] = max( abs(up_hist_vars[iii]), abs(down_hist_vars[iii])   )


		total_bin_vars_up   += pow(final_bin_vars_up,2)
		total_bin_vars_down += pow(final_bin_vars_down,2)


		del allBR_up, allBR_down



	## get the full variation values added in quadrature
	total_bin_vars_up   = np.sqrt(total_bin_vars_up)
	total_bin_vars_down = np.sqrt(total_bin_vars_down)

	#print("Mean total variation for %s and AT (inclusive) region is up/down: %s/%s "%(year, total_bin_vars_up,total_bin_vars_down))
	



	### now should have the full variations for each bin, now create new histograms that have these values and draw them
	allBR_full_up_var   = allBR_nom.Clone("allBR_full_up_var")
	allBR_full_up_var.Sumw2()
	allBR_full_down_var = allBR_nom.Clone("allBR_full_down_var")
	allBR_full_down_var.Sumw2()

	allBR_nom.SetTitle(hist_title)
	allBR_full_up_var.SetTitle(hist_title)
	allBR_full_down_var.SetTitle(hist_title)

	for iii in range(0,allBR_nom.GetNbinsX()):
		allBR_full_up_var.SetBinContent(iii+1,( 1+total_bin_vars_up[iii]) *  allBR_nom.GetBinContent(iii+1)   )
		allBR_full_down_var.SetBinContent(iii+1, (1 - total_bin_vars_down[iii]) *  allBR_nom.GetBinContent(iii+1)    )



	# Draw pads
	pad1.Draw()
	pad2.Draw()

	allBR_nom.SetLineWidth(4)
	allBR_full_up_var.SetLineWidth(2)
	allBR_full_down_var.SetLineWidth(2)

	allBR_full_up_var.SetLineColor(ROOT.kRed)
	allBR_full_down_var.SetLineColor(ROOT.kBlue)

	pad1.cd()
	allBR_nom.SetStats(0)
	allBR_full_up_var.SetStats(0)
	allBR_full_up_var.SetStats(0)
	data_combined.SetStats(0)
	allBR_nom.SetLineColor(ROOT.kBlack)



	allBR_nom.SetMaximum(1.5*allBR_nom.GetMaximum())
	allBR_full_up_var.SetMaximum(1.5*allBR_full_up_var.GetMaximum())
	allBR_full_down_var.SetMaximum(1.5*allBR_full_down_var.GetMaximum())
	data_combined.SetMaximum(1.5*data_combined.GetMaximum())

	allBR_nom.Draw("HIST")
	allBR_full_up_var.Draw("HIST,SAME")
	allBR_full_down_var.Draw("HIST,SAME")
	data_combined.Draw("SAME")
	

	up_var_over_nom   = allBR_full_up_var.Clone("up_var_over_nom")
	up_var_over_nom.Sumw2()
	down_var_over_nom = allBR_full_down_var.Clone("down_var_over_nom")
	down_var_over_nom.Sumw2()
	up_var_over_nom.Divide(allBR_nom)
	down_var_over_nom.Divide(allBR_nom)

	data_over_nom_MC  = data_combined.Clone("data_over_nom_MC")
	data_over_nom_MC.Sumw2()
	data_over_nom_MC.Divide(allBR_nom)


	data_over_nom_MC.SetTitle("")

	data_over_nom_MC.SetMaximum(1.50)
	data_over_nom_MC.SetMinimum(0.5)
	up_var_over_nom.SetMaximum(1.5)
	up_var_over_nom.SetMinimum(0.50)
	down_var_over_nom.SetMaximum(1.5)
	down_var_over_nom.SetMinimum(0.50)

	if "NN" in hist_name:
		data_over_nom_MC.SetMaximum(1.5)
		data_over_nom_MC.SetMinimum(0.5)
		up_var_over_nom.SetMaximum(1.5)
		up_var_over_nom.SetMinimum(0.5)
		down_var_over_nom.SetMaximum(1.5)
		down_var_over_nom.SetMinimum(0.5)

	data_over_nom_MC.GetYaxis().SetTitle("Ratio to nom MC")
	data_over_nom_MC.GetYaxis().SetTitleSize(0.1)
	data_over_nom_MC.GetYaxis().SetLabelSize(0.08)
	data_over_nom_MC.GetYaxis().SetNdivisions(505)
	data_over_nom_MC.GetXaxis().SetLabelSize(0.1)


	pad2.cd()

	data_over_nom_MC.SetStats(0)
	down_var_over_nom.SetStats(0)
	up_var_over_nom.SetStats(0)


	data_over_nom_MC.Draw()
	down_var_over_nom.Draw("HIST SAME")
	up_var_over_nom.Draw("HIST SAME")

	x_min = allBR_nom.GetXaxis().GetXmin()
	x_max = allBR_nom.GetXaxis().GetXmax()

	# Draw a horizontal line at y=1
	line_nom = ROOT.TLine(x_min, 1, x_max, 1)
	#line_nom.SetLineStyle(2)
	line_nom.Draw("SAME")

	line_up = ROOT.TLine(x_min, 1.05, x_max, 1.05)
	line_up.SetLineStyle(2)
	line_up.Draw("SAME")

	line_down = ROOT.TLine(x_min, 0.95, x_max, 0.95)
	line_down.SetLineStyle(2)
	line_down.Draw("SAME")

	canvas.Update()
	canvas.SaveAs(output_dir+"%s_%s_dataMC_wVars.png"%(hist_name, year))



	#### MAKE SHAPE COMPARISONS
	canvas.Clear()



	# Define the upper and lower pad sizes
	pad1 = ROOT.TPad("pad1", "Upper Pad", 0, 0.29, 1, 1)
	pad2 = ROOT.TPad("pad2", "Lower Pad", 0, 0, 1, 0.3)

	# Set margins
	pad1.SetBottomMargin(0.02)  # Reduce margin to align with lower pad
	pad2.SetTopMargin(0.02)
	pad2.SetBottomMargin(0.3)   # Increase bottom margin for ratio plot

	# Draw pads
	pad1.Draw()
	pad2.Draw()

	allBR_full_up_var.Scale(1.0/allBR_nom.Integral())
	allBR_full_down_var.Scale(1.0/allBR_nom.Integral())

	allBR_nom.Scale(1.0/allBR_nom.Integral())

	data_combined.Scale(1.0/data_combined.Integral())

	print("The integral of allBR_full_up_var is %s, the integral of ")

	pad1.cd()
	
	allBR_nom.Draw("HIST")
	allBR_full_up_var.Draw("HIST,SAME")
	allBR_full_down_var.Draw("HIST,SAME")
	data_combined.Draw("SAME")

	up_var_over_nom   = allBR_full_up_var.Clone("up_var_over_nom")
	up_var_over_nom.Sumw2()
	down_var_over_nom = allBR_full_down_var.Clone("down_var_over_nom")
	down_var_over_nom.Sumw2()
	up_var_over_nom.Divide(allBR_nom)
	down_var_over_nom.Divide(allBR_nom)

	data_over_nom_MC  = data_combined.Clone("data_over_nom_MC")
	data_over_nom_MC.Sumw2()
	data_over_nom_MC.Divide(allBR_nom)

	data_over_nom_MC.SetTitle("")

	data_over_nom_MC.SetMaximum(1.50)
	data_over_nom_MC.SetMinimum(0.5)
	up_var_over_nom.SetMaximum(1.5)
	up_var_over_nom.SetMinimum(0.50)
	down_var_over_nom.SetMaximum(1.5)
	down_var_over_nom.SetMinimum(0.50)

	if "NN" in hist_name:
		data_over_nom_MC.SetMaximum(1.5)
		data_over_nom_MC.SetMinimum(0.5)
		up_var_over_nom.SetMaximum(1.5)
		up_var_over_nom.SetMinimum(0.5)
		down_var_over_nom.SetMaximum(1.5)
		down_var_over_nom.SetMinimum(0.5)

	data_over_nom_MC.GetYaxis().SetTitle("Ratio to nom MC")
	data_over_nom_MC.GetYaxis().SetTitleSize(0.1)
	data_over_nom_MC.GetYaxis().SetLabelSize(0.08)
	data_over_nom_MC.GetYaxis().SetNdivisions(505)
	data_over_nom_MC.GetXaxis().SetLabelSize(0.1)


	pad2.cd()

	data_over_nom_MC.SetStats(0)
	down_var_over_nom.SetStats(0)
	up_var_over_nom.SetStats(0)

	data_over_nom_MC.Draw()
	down_var_over_nom.Draw("HIST SAME")
	up_var_over_nom.Draw("HIST SAME")

	x_min = allBR_nom.GetXaxis().GetXmin()
	x_max = allBR_nom.GetXaxis().GetXmax()

	# Draw a horizontal line at y=1
	line_nom = ROOT.TLine(x_min, 1, x_max, 1)
	#line_nom.SetLineStyle(2)
	line_nom.Draw("SAME")

	line_up = ROOT.TLine(x_min, 1.05, x_max, 1.05)
	line_up.SetLineStyle(2)
	line_up.Draw("SAME")

	line_down = ROOT.TLine(x_min, 0.95, x_max, 0.95)
	line_down.SetLineStyle(2)
	line_down.Draw("SAME")

	canvas.Update()
	canvas.SaveAs(output_dir+"/shape/" + "%s_%s_dataMC_SHAPE_wVars.png"%(hist_name, year))



	return


if __name__== "__main__":

	debug = False
	do_NN_plots = True
	years 	= ["2015","2016","2017","2018"]


	hist_names   = [
	"h_SJ1_BEST_sig_score",
	"h_SJ1_BEST_Top_score",
	"h_SJ1_BEST_QCD_score",
	"h_SJ2_BEST_sig_score",
	"h_SJ2_BEST_Top_score",
	"h_SJ2_BEST_QCD_score",
	"h_SJ1_decision",
	"h_SJ2_decision",
	"h_SJ2_BEST_sig_score_1b_SJ1AT",
	"h_SJ2_BEST_Top_score_1b_SJ1AT",
	"h_SJ2_BEST_QCD_score_1b_SJ1AT",
	"h_SJ2_BEST_sig_score_0b_SJ1AT",
	"h_SJ2_BEST_Top_score_0b_SJ1AT",
	"h_SJ2_BEST_QCD_score_0b_SJ1AT",
	"h_SJ2_BEST_sig_score_SJ1AT",
	"h_SJ2_BEST_Top_score_SJ1AT",
	"h_SJ2_BEST_QCD_score_SJ1AT",
	"h_SJ2_decision_1b_SJ1AT",
	"h_SJ2_decision_0b_SJ1AT",
	"h_SJ2_decision_SJ1AT"
	#"h_SJ_mass_tagged_SJs_1b_NN",
	#"h_SJ_mass_tagged_SJs_0b_NN",
	#"h_SJ_mass_tagged_SJs_NN",
	#"h_SJ2_mass_tagged_SJs_ATSJ1_1b_NN",
	#"h_SJ2_mass_tagged_SJs_ATSJ1_0b_NN",
	#"h_SJ2_mass_tagged_SJs_ATSJ1_NN",
	#"h_SJ2_mass_total_SJs_ATSJ1_1b_NN",
	#"h_SJ2_mass_total_SJs_ATSJ1_0b_NN",
	#"h_SJ2_mass_total_SJs_ATSJ1_NN"
	 ] 
	hist_types       = ["SJ1 BEST SIGNAL score",
	"SJ1 BEST TOP score",
	"SJ1 BEST QCD score",
	"SJ2 BEST SIGNAL score",
	"SJ2 BEST TOP score",
	"SJ2 BEST QCD score",
	"SJ1 decision",
	"SJ2 decision",
	"SJ2 BEST SIGNAL score (1b, SJ1 antitagged)",
	"SJ2 BEST TOP score (1b, SJ1 antitagged)",
	"SJ2 BEST QCD score (1b, SJ1 antitagged)",
	"SJ2 BEST SIGNAL score (0b, SJ1 antitagged)",
	"SJ2 BEST TOP score (0b, SJ1 antitagged)",
	"SJ2 BEST QCD score (0b, SJ1 antitagged)",
	"SJ2 BEST SIGNAL score (SJ1 antitagged)",
	"SJ2 BEST TOP score (SJ1 antitagged)",
	"SJ2 BEST QCD score (SJ1 antitagged)",
	"SJ2 decision (1b, SJ1 antitagged)",
	"SJ2 decision (0b SJ1 antitagged)",
	"SJ2 decision (SJ1 antitagged)" 
	#"SJ mass (tagged SJs) (1b) (NN-tagged)",
	#"SJ mass (tagged SJs) (0b) (NN-tagged)",
	#"SJ mass (tagged SJs) (NN-tagged)",
	#"SJ2 mass (tagged SJs) (ATSJ1) (1b) (NN-based)",
	#"SJ2_mass (tagged SJs) (ATSJ1) (0b) (NN-based)",
	#"SJ2 mass (tagged_SJs_ATSJ1_NN",
	#"SJ2 mass total_SJs_ATSJ1_1b_NN",
	#"SJ2 mass total_SJs_ATSJ1_0b_NN",
	#"SJ2 mass total_SJs_ATSJ1_NN"



	]

	if do_NN_plots:
		hist_names.extend([])
		hist_types.extend([])




	#hist_names = [ "h_nCA4_300_0b" ]  
	#hist_types = [ "Number of SJ CA4 Jets (E > 300 GeV)"  ]   

	if debug:
		years =["2015"]
	for year in years:
		#for iii,hist_name in enumerate(hist_names):
		#try:
		for iii, hist_type in enumerate(hist_types):

			print("Running year %s and hist type %s"%(year,hist_type))
			hist_name = hist_names[iii]
			create_systematic_comparison_plot(year, hist_name, hist_type)

		#except:
		#	print("ERROR: Failed for %s, %s %s"%(hist_name,year))




