import numpy as np
import sys, os
import ROOT
from write_cms_text import write_cms_text
from return_BR_SF.return_BR_SF import return_BR_SF
from return_signal_SF.return_signal_SF import return_signal_SF
from return_data_samples.return_data_samples import return_data_samples

from math import isnan


# this script opens the output files from readTree_test.C, grabs the h_totHT_1b histograms from within 

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


#### Takes in some file names, a numerator and denominator histogram name, and returns the combined, scaled, ratio histogrma from num/denom
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

		#except:
		#	print("ERROR with %s for %s/%s or %s/%s  "%(file_names[iii],hist_name_num,folder_name_num, hist_name_denom, folder_name_denom))
	
	#print("------------ Histogram %s (%s) (%s) from file %s has %s total scaled events."%(hist_name, folder,systematic, file_names, combined_hist.Integral() ))

	return combined_hist


def create_systematic_comparison_plot(year, hist_name_num, hist_name_denom, hist_type, debug=False):


	canvas = ROOT.TCanvas("","",1200,1000)

	output_dir = "plots/tagging_comparisons/"

	# Define the upper and lower pad sizes
	pad1 = ROOT.TPad("pad1", "Upper Pad", 0, 0.29, 1, 1)
	pad2 = ROOT.TPad("pad2", "Lower Pad", 0, 0, 1, 0.3)

	# Set margins
	pad1.SetBottomMargin(0.02)  # Reduce margin to align with lower pad
	pad2.SetTopMargin(0.02)
	pad2.SetBottomMargin(0.3)   # Increase bottom margin for ratio plot


	ROOT.TH1.AddDirectory(False)
	input_file_dir = "../combinedROOT/processedFiles/"


	### a rate is being calculator: # tagged SJs / total SJs, these hists represent that
	#hist_name_num    = "h_SJ_mass_tagged_SJs_ATSJ1"
	#hist_name_denom  = "h_SJ_mass_total_SJs_ATSJ1"
	hist_title = " Superjet tagging rate vs SJ mass (%s)"%hist_type



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


	######### numerator histograms
	QCD_weights 		= [all_weights["QCDMC1000to1500"][year],all_weights["QCDMC1500to2000"][year],all_weights["QCDMC2000toInf"][year] ]
	TTbar_weights 		= [all_weights["TTJetsMCHT1200to2500"][year],all_weights["TTJetsMCHT2500toInf"][year]]
	ST_weights			= [all_weights["ST_t_channel_top_inclMC"][year],all_weights["ST_t_channel_antitop_inclMC"][year],all_weights["ST_s_channel_hadronsMC"][year],all_weights["ST_s_channel_leptonsMC"][year],all_weights["ST_tW_antiTop_inclMC"][year],all_weights["ST_tW_top_inclMC"][year]]
	WJets_weights		= [all_weights["WJetsMC_LNu_HT800to1200"][year],all_weights["WJetsMC_LNu_HT1200to2500"][year],all_weights["WJetsMC_LNu_HT2500toInf"][year],all_weights["WJetsMC_QQ_HT800toInf"][year]]

	QCD_combined_nom_num	= get_combined_histogram(QCD_file_names, hist_name_num,			"nom", QCD_weights, "nom")
	TTbar_combined_nom_num  = get_combined_histogram(TTbar_file_names, hist_name_num,			   "nom", TTbar_weights, "nom")
	ST_combined_nom_num 	= get_combined_histogram(ST_file_names, hist_name_num,			  "nom", ST_weights, "nom")
	WJets_combined_nom_num  = get_combined_histogram(WJets_file_names, hist_name_num,			   "nom", WJets_weights, "nom")

	allBR_nom_num = QCD_combined_nom_num.Clone("allBR_nom_num")
	allBR_nom_num.Sumw2()
	allBR_nom_num.Add(TTbar_combined_nom_num)
	allBR_nom_num.Add(WJets_combined_nom_num)
	allBR_nom_num.Add(ST_combined_nom_num)	
	allBR_nom_num.SetTitle(hist_title)

	######### denominator histograms
	QCD_combined_nom_denom	= get_combined_histogram(QCD_file_names, hist_name_denom,			"nom", QCD_weights, "nom")
	TTbar_combined_nom_denom  = get_combined_histogram(TTbar_file_names, hist_name_denom,			   "nom", TTbar_weights, "nom")
	ST_combined_nom_denom 	= get_combined_histogram(ST_file_names, hist_name_denom,			  "nom", ST_weights, "nom")
	WJets_combined_nom_denom  = get_combined_histogram(WJets_file_names, hist_name_denom,			   "nom", WJets_weights, "nom")

	allBR_nom_denom = QCD_combined_nom_denom.Clone("allBR_nom_denom")
	allBR_nom_denom.Sumw2()
	allBR_nom_denom.Add(TTbar_combined_nom_denom)
	allBR_nom_denom.Add(WJets_combined_nom_denom)
	allBR_nom_denom.Add(ST_combined_nom_denom)	
	allBR_nom_denom.SetTitle(hist_title)

	allBR_nom = allBR_nom_num.Clone("allBR_nom")
	allBR_nom.Sumw2()
	allBR_nom.Divide(allBR_nom_denom)

	### get data histogram
	data_samples = return_data_samples(year)
	data_weights = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

	data_file_names 	 = [input_file_dir+ data_sample + "_"  + year + "_processed.root" for data_sample in data_samples]
	data_combined_num        = get_combined_histogram(data_file_names, hist_name_num,			"nom", data_weights, "nom")
	data_combined_denom        = get_combined_histogram(data_file_names, hist_name_denom,			"nom", data_weights, "nom")

	print("Data num has %s total events, denom has %s total events. "%(data_combined_num.Integral(),data_combined_denom.Integral()))

	data_combined = data_combined_num.Clone("data_combined")
	data_combined.Sumw2()
	data_combined.Divide(data_combined_denom)


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
		QCD_combined_up_num	   = get_combined_histogram(QCD_file_names, hist_name_num,			systematic+"_up" , QCD_weights, systematic+"_up")
		TTbar_combined_up_num  = get_combined_histogram(TTbar_file_names, hist_name_num,			   systematic+"_up" , TTbar_weights, systematic+"_up")
		ST_combined_up_num 	   = get_combined_histogram(ST_file_names, hist_name_num,			  systematic+"_up", ST_weights, systematic+"_up")
		WJets_combined_up_num  = get_combined_histogram(WJets_file_names, hist_name_num,			   systematic+"_up", WJets_weights, systematic+"_up")

		allBR_up_num = QCD_combined_up_num.Clone("allBR_var_up_num")
		allBR_up_num.Sumw2()
		allBR_up_num.Add(TTbar_combined_up_num)
		allBR_up_num.Add(WJets_combined_up_num)
		allBR_up_num.Add(ST_combined_up_num)	

		QCD_combined_up_denom	= get_combined_histogram(QCD_file_names, hist_name_denom,			systematic+"_up" , QCD_weights, systematic+"_up")
		TTbar_combined_up_denom  = get_combined_histogram(TTbar_file_names, hist_name_denom,			   systematic+"_up" , TTbar_weights, systematic+"_up")
		ST_combined_up_denom 	= get_combined_histogram(ST_file_names, hist_name_denom,			  systematic+"_up", ST_weights, systematic+"_up")
		WJets_combined_up_denom  = get_combined_histogram(WJets_file_names, hist_name_denom,			   systematic+"_up", WJets_weights, systematic+"_up")

		allBR_up_denom = QCD_combined_up_denom.Clone("allBR_var_up_denom")
		allBR_up_denom.Sumw2()
		allBR_up_denom.Add(TTbar_combined_up_denom)
		allBR_up_denom.Add(WJets_combined_up_denom)
		allBR_up_denom.Add(ST_combined_up_denom)	

		allBR_up = allBR_up_num.Clone("allBR_up")
		allBR_up.Sumw2()
		allBR_up.Divide(allBR_up_denom)




		### get the DOWN allBR histogram variations
		QCD_combined_down_num	= get_combined_histogram(QCD_file_names, hist_name_num,			systematic+"_down", QCD_weights, systematic+"_down")
		TTbar_combined_down_num  = get_combined_histogram(TTbar_file_names, hist_name_num,			   systematic+"_down", TTbar_weights, systematic+"_down")
		ST_combined_down_num 	= get_combined_histogram(ST_file_names, hist_name_num,			  systematic+"_down", ST_weights, systematic+"_down")
		WJets_combined_down_num  = get_combined_histogram(WJets_file_names, hist_name_num,			   systematic+"_down", WJets_weights, systematic+"_down")

		allBR_down_num = QCD_combined_down_num.Clone("allBR_var_up_num")
		allBR_down_num.Sumw2()
		allBR_down_num.Add(TTbar_combined_down_num)
		allBR_down_num.Add(WJets_combined_down_num)
		allBR_down_num.Add(ST_combined_down_num)	

		QCD_combined_down_denom	= get_combined_histogram(QCD_file_names, hist_name_denom,			systematic+"_down", QCD_weights, systematic+"_down")
		TTbar_combined_down_denom  = get_combined_histogram(TTbar_file_names, hist_name_denom,			   systematic+"_down", TTbar_weights, systematic+"_down")
		ST_combined_down_denom 	= get_combined_histogram(ST_file_names, hist_name_denom,			  systematic+"_down", ST_weights, systematic+"_down")
		WJets_combined_down_denom  = get_combined_histogram(WJets_file_names, hist_name_denom,			   systematic+"_down", WJets_weights, systematic+"_down")

		allBR_down_denom = QCD_combined_down_denom.Clone("allBR_var_up_denom")
		allBR_down_denom.Sumw2()
		allBR_down_denom.Add(TTbar_combined_down_denom)
		allBR_down_denom.Add(WJets_combined_down_denom)
		allBR_down_denom.Add(ST_combined_down_denom)	

		#print("----------------- systematic %s ,       up/nom/down NUM hist integrals are %s/%s/%s,  up/nom/down DENOM hist integrals are %s/%s/%s"%(systematic, allBR_up_num.Integral(), allBR_nom_num.Integral(), allBR_down_num.Integral(),  allBR_up_denom.Integral(), allBR_nom_denom.Integral(), allBR_down_denom.Integral()))




		allBR_down = allBR_down_num.Clone("allBR_down")
		allBR_down.Sumw2()
		allBR_down.Divide(allBR_down_denom)




		### delete hists that are no longer needed
		del QCD_combined_up_num, TTbar_combined_up_num, ST_combined_up_num, WJets_combined_up_num, allBR_up_num, QCD_combined_up_denom, TTbar_combined_up_denom
		del ST_combined_up_denom, WJets_combined_up_denom, allBR_up_denom, QCD_combined_down_num, TTbar_combined_down_num, ST_combined_down_num
		del WJets_combined_down_num, allBR_down_num, QCD_combined_down_denom, TTbar_combined_down_denom, ST_combined_down_denom, WJets_combined_down_denom
		del allBR_down_denom

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

		# find which one is more negative by finding the mean vs the nominal hist
		#if np.mean(up_hist_vars) > np.mean(down_hist_vars):
		#	neg_vars = -1*np.array(up_hist_vars)
		#	pos_vars =    np.array(up_hist_vars)
		#else:
		#	neg_vars = -1*np.array(down_hist_vars)
		#	pos_vars =    np.array(down_hist_vars)





		final_bin_vars_up   = np.zeros(allBR_nom.GetNbinsX(), dtype=np.float64)
		final_bin_vars_down = np.zeros(allBR_nom.GetNbinsX(), dtype=np.float64)


		## get largest variation in each bin
		for iii in range(0, allBR_nom.GetNbinsX()):
			final_bin_vars_up[iii] = max( abs(up_hist_vars[iii]), abs(down_hist_vars[iii])   )
			final_bin_vars_down[iii] = max( abs(up_hist_vars[iii]), abs(down_hist_vars[iii])   )


		## add these variations (eventually will be sqrted so each source is added in quadrature)

		#print("type(total_bin_vars_up) is %s."%(type(total_bin_vars_up)))
		#print("type(total_bin_vars_down) is %s."%(type(total_bin_vars_down)))


		#print("For systematic %s and year %s, pos_vars are %s, neg vars are %s."%(systematic,year,pos_vars,neg_vars))

		#total_bin_vars_up   += pow(pos_vars,2)
		#total_bin_vars_down += pow(neg_vars,2)

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

	allBR_nom.Draw("HIST")
	allBR_full_up_var.Draw("HIST,SAME")
	allBR_full_up_var.Draw("HIST,SAME")
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

	data_over_nom_MC.SetMaximum(1.10)
	data_over_nom_MC.SetMinimum(0.90)
	up_var_over_nom.SetMaximum(1.1)
	up_var_over_nom.SetMinimum(0.90)
	down_var_over_nom.SetMaximum(1.1)
	down_var_over_nom.SetMinimum(0.90)

	if "NN" in hist_name_num:
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
	canvas.SaveAs(output_dir+"SJ_tagging_rates_cutbased_%s_%s.png"%(hist_type, year))



	return


if __name__== "__main__":

	debug = False
	do_NN_plots = True
	years 	= ["2015","2016","2017","2018"]


	hist_name_nums   = ["h_SJ2_mass_tagged_SJs_ATSJ1","h_SJ2_mass_tagged_SJs_ATSJ1_1b","h_SJ2_mass_tagged_SJs_ATSJ1_0b", "h_SJ_mass_tagged_SJs_1b","h_SJ_mass_tagged_SJs_0b","h_SJ_mass_tagged_SJs"] 
	hist_name_denoms = ["h_SJ2_mass_total_SJs_ATSJ1","h_SJ2_mass_total_SJs_ATSJ1_1b","h_SJ2_mass_total_SJs_ATSJ1_0b","h_SJ_mass_total_SJs_1b","h_SJ_mass_total_SJs_0b","h_SJ_mass_total_SJs"] 
	hist_types       = ["AT","AT1b","AT0b","All_1b","All_0b","All"]


	if do_NN_plots:
		hist_name_nums.extend(["h_SJ_mass_tagged_SJs_NN", "h_SJ_mass_tagged_SJs_1b_NN", "h_SJ_mass_tagged_SJs_0b_NN","h_SJ2_mass_tagged_SJs_ATSJ1_1b_NN","h_SJ2_mass_tagged_SJs_ATSJ1_0b_NN","h_SJ2_mass_tagged_SJs_ATSJ1_NN"])
		hist_name_denoms.extend(["h_SJ_mass_total_SJs",      "h_SJ_mass_total_SJs_1b",    "h_SJ_mass_total_SJs_0b",   "h_SJ2_mass_total_SJs_ATSJ1_1b_NN", "h_SJ2_mass_total_SJs_ATSJ1_0b_NN", "h_SJ2_mass_total_SJs_ATSJ1_NN"])
		hist_types.extend(["All_NN", "All_NN_1b", "All_NN_0b","AT_NN_1b","AT_NN_0b","AT_NN"])




	#hist_names = [ "h_nCA4_300_0b" ]  
	#hist_types = [ "Number of SJ CA4 Jets (E > 300 GeV)"  ]   

	if debug:
		years =["2015"]
	for year in years:
		#for iii,hist_name in enumerate(hist_names):
		#try:
		for iii, hist_type in enumerate(hist_types):

			print("Running year %s and hist type %s"%(year,hist_type))
			hist_name_num = hist_name_nums[iii]
			hist_name_denom = hist_name_denoms[iii]
			create_systematic_comparison_plot(year, hist_name_num, hist_name_denom, hist_type)

		#except:
		#	print("ERROR: Failed for %s, %s %s"%(hist_name,year))




