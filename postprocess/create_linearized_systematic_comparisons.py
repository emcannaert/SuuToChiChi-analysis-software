import numpy as np
import sys, os
import ROOT
from write_cms_text import write_cms_text
import array
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
	#print("Looking for TFile %s and histogram name %s"%(file_names[0],folder_name))
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

def create_3_hist_ratio_plot(up_hist,nom_hist,down_hist, hist_type, systematic, year, sample_type, sample_description, mass_point, technique_str,region, run_corrected, QCD_type, isSignal=False, ):

	ROOT.TH1.AddDirectory(False)

	output_dir = "plots/linearized_systematic_comparisons/%s/"%QCD_type
	if run_corrected: output_dir+= "correctedSystematics/"

	technique_folder = "cutbased"
	if "NN" in technique_str: technique_folder = "NN_based"

	if not os.path.exists(output_dir+"background/%s/%s"%(region,technique_folder)):
		os.makedirs(output_dir+"background/%s/%s"%(region,technique_folder)  ) 
	output_plot_name = output_dir+"background/%s/%s/linearized_%s%s_%s_SysComparison_RatioPlot_%s_%s.png"%(region,technique_folder,technique_str,hist_type,region, systematic,year)
	if isSignal: 
		

		if not os.path.exists(output_dir+"signal/%s/%s/%s/"%(region, technique_folder, mass_point)):
			os.makedirs(output_dir+"signal/%s/%s/%s/"%(region, technique_folder, mass_point))
		output_plot_name = output_dir+"signal/%s/%s/%s/linearized_%s%s_%s_%s_SysComparison_RatioPlot_%s_%s.png"%(region, technique_folder, mass_point, technique_str,mass_point,hist_type,region, systematic,year)
	#### cms label stuff 
	CMS_label_pos = 0.152
	SIM_label_pos = 0.295

	up_hist = clean_histogram(up_hist, sample_type,systematic)
	down_hist = clean_histogram(down_hist, sample_type,systematic)
	nom_hist = clean_histogram(nom_hist, sample_type,systematic)

	technique_type = "cut-based"
	if technique_str == "NN_":
		technique_type = "NN-based"

	canvas = ROOT.TCanvas("canvas", "Histograms", 1250, 1000)

	up_hist.SetTitle("Linearized %s MC in the %s for the up/nom/down %s uncertainty (%s) (%s)"%(sample_description,region, systematic,convert_year(year),technique_type))
	down_hist.SetTitle("Linearized %s MC in the %s for the up/nom/down %s uncertainty (%s) (%s)"%(sample_description,region,systematic,convert_year(year),technique_type))

	if isSignal:
		up_hist.SetTitle("Linearized %s MC in the %s for the up/nom/down %s uncertainty (%s) (%s) (%s)"%(sample_description,region, systematic,convert_year(year),mass_point,technique_type))
		down_hist.SetTitle("Linearized %s MC in the %s for the up/nom/down %s uncertainty (%s) (%s) (%s)"%(sample_description,region,systematic,convert_year(year),mass_point,technique_type))

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

	pad1 = canvas.GetPad(1)
	#pad1.SetLogy(1)

	#max_bin_content = max(up_hist.GetMaximum(), nom_hist.GetMaximum(), down_hist.GetMaximum())
	#min_bin_content = min(up_hist.GetMinimum(), nom_hist.GetMinimum(), down_hist.GetMinimum())

	# Force all histograms to use the same Y-axis range
	#up_hist.SetMaximum(1000)
	#up_hist.SetMinimum(1e-2)

	#nom_hist.SetMaximum(1000)
	#nom_hist.SetMinimum(1e-2)

	#down_hist.SetMaximum(1000)
	#down_hist.SetMinimum(1e-2)

	up_hist.Draw("HIST")
	nom_hist.Draw("SAME,HIST")
	down_hist.Draw("SAME.HIST")

	pad1.Update()  # Force the upper pad to redraw

	legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
	legend.AddEntry(up_hist, "up systematic", "l")
	legend.AddEntry(nom_hist, "nom systematic", "l")
	legend.AddEntry(down_hist, "down systematic", "l")
	legend.Draw()

	## keep the histograms from being cut off
	max_bin_content = max(max(up_hist.GetMaximum(), nom_hist.GetMaximum()), down_hist.GetMaximum()   )
	up_hist.GetYaxis().SetRangeUser(0, max_bin_content * 1.1)


	write_cms_text.write_cms_text(CMS_label_xpos=0.132, SIM_label_xpos=0.243,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)

	# Lower pad for ratio plots
	canvas.cd(2)

	ratio1_2 = up_hist.Clone("ratio1_2")
	ratio1_2 = divide_histograms(ratio1_2,nom_hist)

	ratio1_2.SetTitle("") #hist_type + " up and down systematics / nom systematic"
	ratio1_2.GetYaxis().SetTitle("Variation / Nominal")

	ratio1_2.GetYaxis().SetTitleSize(0.1)
	ratio1_2.GetYaxis().SetTitleOffset(0.4)
	ratio1_2.GetYaxis().SetLabelSize(0.08)
	ratio1_2.GetXaxis().SetTitleSize(0.12)
	ratio1_2.GetXaxis().SetLabelSize(0.1)

	ratio1_2.SetLineColor(ROOT.kRed)
	ratio1_2.Draw("HIST")

	ratio1_3 = down_hist.Clone("ratio1_3")

	ratio1_3.GetYaxis().SetTitleSize(0.1)
	ratio1_3.GetYaxis().SetTitleOffset(0.4)
	ratio1_3.GetYaxis().SetLabelSize(0.08)
	ratio1_3.GetXaxis().SetTitleSize(0.12)
	ratio1_3.GetXaxis().SetLabelSize(0.1)



	ratio1_3 = divide_histograms(ratio1_3,nom_hist)
	ratio1_3.SetTitle("")  #hist_type + " up and down systematics / nom systematic"
	ratio1_3.GetYaxis().SetTitle("Variation / Nominal")
	#ratio1_3.Divide(up_hist)
	ratio1_3.SetLineColor(ROOT.kBlue)
	ratio1_3.Draw("SAME,HIST")

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
	ratio1_2.GetYaxis().SetRangeUser(min_bin_content_ratio/0.8, max_bin_content_ratio*1.15)
	canvas.Update();

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


	# Define the text
	text = ROOT.TLatex()
	text.SetTextSize(0.058)
	text.SetTextFont(62)
	text.SetTextAlign(22)  # Center alignment (horizontal and vertical)
	


	technique_desc = "cut-based"
	if technique_str == "_NN":
		technique_desc = "NN-based"

	canvas.cd(1)

	# Draw the text lines
	text.DrawLatexNDC(0.42, 0.82, sample_type + ", " + convert_year(year))
	text.DrawLatexNDC(0.42, 0.77, systematic)
	text.DrawLatexNDC(0.42, 0.72, technique_desc) 




	canvas.Update()

	canvas.SaveAs(output_plot_name)

	return




def create_systematic_comparison_plot(year, mass_point,histname,systematic, year_str, technique_str,region,QCD_type ,run_corrected = False ):

	if systematic == "CMS_topPt" and histname not in ["allBR", "TTbar"]: return # skip these
	if systematic == "stat" and histname == "sig": return

	technique_desc = "cut-based"
	if technique_str == "_NN":
		technique_desc = "NN-based"

	inputFile = "finalCombineFilesNewStats/%s/combine_%s%s_%s.root"%(QCD_type, technique_str, year,mass_point) 

	if run_corrected: inputFile = "finalCombineFilesNewStats/%s/correctedFinalCombineFiles/combine_%s%s_%s.root"%(QCD_type, technique_str, year,mass_point) 

	print("Opening file %s"%(inputFile))

	finput = ROOT.TFile(inputFile)
 	
	c = ROOT.TCanvas("c","",1250,1000)

	sample_type = ""	


	"""
	systematic_names = ["CMS_btagSFbc", "CMS_pu", "CMS_jec", "CMS_jer", "CMS_topPt", "CMS_L1Prefiring", "CMS_pdf", "CMS_renorm", "CMS_fact"]  ## systematic namings for cards
	for syst in systematic_names:
		if systematic in syst:
			systematic = syst
			break """


	uncorrelated_systematics = [  "CMS_jec", "CMS_jer","CMS_jer_eta193", "CMS_jer_193eta25", "CMS_L1Prefiring","CMS_bTagSF_M", "CMS_bTagSF_T", "CMS_bTagSF_bc_T_year", "CMS_bTagSF_light_T_year", "CMS_bTagSF_bc_M_year","CMS_bTagSF_light_M_year", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year", "CMS_jec_RelativeSample_year", "stat"] ## systematics that are correlated (will not have year appended to names)	 "CMS_btagSF",

	year_str = ""			
	if systematic in uncorrelated_systematics:
		if year == "2015":
			year_str = "16preAPV"
		elif year == "2016":
			year_str = "16" # can change this to be "postAPV" if needed
		else:
			year_str =  year[-2:]
	if "renorm" in systematic or "fact" in systematic:
		sample_str = histname
		if histname == "sig":
			sample_str = "sig"
		sample_type = "_%s"%sample_str


	print("Systematic is %s, histname is %s, year is %s, technique_str is %s"%(systematic, histname, year_str, technique_str))

	if systematic in ["CMS_pdf", "CMS_renorm","CMS_fact", "CMS_scale" ]:
		sample_str = histname
		if histname == "sig":
			sample_str = "sig"
		elif systematic == "CMS_pdf" and histname in ["QCD","WJets", "TTbar"]: sample_str = "misc"
		elif systematic == "CMS_pdf" and histname in ["TTTo"]: sample_str = "TTbar"
		systematic += "_%s"%sample_str



	histname_up = histname + "_" + systematic + year_str + "Up"
	histname_nom = histname 
	histname_down = histname + "_" + systematic + year_str + "Down"

	print("histname_up/histname_nom/histname_down: %s/%s/%s"%(histname_up,histname_nom,histname_down))

	#print("up histogram name is %s"%histname_up)
	#print("nom histogram name is %s"%histname_nom)
	#print("down histogram name is %s"%histname_down)
	#print("Running for year/mass_point/histname/systematic/technique_str/region: %s/%s/%s/%s/%s%s"%(year,mass_point,histname,systematic,technique_str,region))

	#print("Getting up histogram ", histname_up )
	up_hist = finput.Get(region+"/"+histname_up)
	#print("Getting nom histogram ", histname_nom )

	nom_hist = finput.Get(region+"/"+histname)
	#print("Getting down histogram ", histname_down )

	down_hist = finput.Get(region+"/"+histname_down)
	#down_hist.Sumw2()


	#### add the NP yield changes to text file

	if run_corrected: yield_impact_text = open("txt_files/NP_yield_impacts_corrected.txt","a")
	else: yield_impact_text = open("txt_files/NP_yield_impacts.txt","a")
	yield_impact_text.write("%s	 %s	 %s	 %s	 %s	 %s	 %s	 %s	 %s	%s\n"%(year, histname, region, systematic,   np.round(nom_hist.Integral(),4), np.round(up_hist.Integral(),4), np.round(down_hist.Integral(),4),  np.round(up_hist.Integral()/nom_hist.Integral() - 1.0,4), np.round(down_hist.Integral()/nom_hist.Integral() - 1.0,4),  np.round(max( abs(up_hist.Integral()/nom_hist.Integral() - 1.0), abs(down_hist.Integral()/nom_hist.Integral() - 1.0)	 )   ,4) ) )
	yield_impact_text.close()


	#shape_impact_text_corrected.write("year	 NP_name	 mean_var_up	 mean_var_down	 max_var_up	 var_stddev_up	 var_stddev_down	 max_var_down\n")




	### need to loop overall bins and count up the variations

	### these will contain the 1 - var / nom values
	vars_up  = np.array([])
	vars_down = np.array([])

	for iii in range(1,nom_hist.GetNbinsX()+1):
		nom_yield = nom_hist.GetBinContent(iii)
		up_yield  = up_hist.GetBinContent(iii)
		down_yield = down_hist.GetBinContent(iii)

		if nom_yield > 0:
			up_var = 1.0 - up_yield/nom_yield
			down_var = 1.0 - down_yield/nom_yield
		else: 
			up_var = 1.0
			down_var = 1.0


		vars_up = np.append(vars_up, up_var)
		vars_down = np.append(vars_down, down_var)

	mean_var_up = np.round(np.mean(vars_up),4)
	mean_var_down = np.round(np.mean(vars_down),4)

	var_stddev_up = np.round(np.std(vars_up),4)
	var_stddev_down = np.round(np.std(vars_down),4)

	max_var_up = np.round(np.max(vars_up),4)
	max_var_down = np.round(np.max(vars_down),4)

	min_var_up   =  np.round(np.min(vars_up),4)
	min_var_down =  np.round(np.min(vars_down),4)


	max_var_up = max( abs(max_var_up), abs(min_var_up)	)
	max_var_down = max( abs(max_var_down), abs(min_var_down)	)

	abs_vars_up   = np.array([ abs(a_var_up)  for a_var_up in vars_up  ])
	abs_vars_down = np.array([ abs(a_var_down)  for a_var_down in vars_down  ])

	mean_abs_var_up	  =  np.round(  np.mean(  abs_vars_up	),4)
	mean_abs_var_down	=  np.round(  np.mean(  abs_vars_down  ),4)

	max_var_abs =   np.round(max( max( max(  abs(max_var_up)	 ,  abs(max_var_down)   ),  abs(min_var_up)	  ),  abs(min_var_down)	 ),4)

	if run_corrected: shape_impact_text = open("txt_files/NP_shape_impacts_corrected.txt","a")
	else: shape_impact_text = open("txt_files/NP_shape_impacts.txt","a")
	shape_impact_text.write("%s	 %s	 %s	 %s	 %s	 %s	%s	 %s	 %s	 %s	 %s	 %s	 %s\n"%(year, histname, region, systematic,   mean_var_up,	 mean_var_down,  mean_abs_var_up, mean_abs_var_down,   var_stddev_up,	 var_stddev_down ,	max_var_up,	 max_var_down,	   max_var_abs	  ))
	shape_impact_text.close()


	#print("up hist name is ", region+"/"+histname_up)
	up_hist.SetTitle("Linearized %s in the %s for different %s values (%s) (%s)"%(histname,region, systematic,year,technique_desc ))
	nom_hist.SetTitle("Linearized %s in the %s for different %s values (%s) (%s)"%(histname,region, systematic,year,technique_desc ))
	down_hist.SetTitle("Linearized %s in the %s for different %s values (%s) (%s)"%(histname,region, systematic,year,technique_desc ))
	

	if histname == "sig":
		create_3_hist_ratio_plot(up_hist,nom_hist,down_hist, histname, systematic, year, histname, histname, mass_point, technique_str, region, run_corrected, QCD_type, True)
	else:
		create_3_hist_ratio_plot(up_hist,nom_hist,down_hist, histname, systematic, year, histname, histname, mass_point, technique_str,region, run_corrected, QCD_type)

def create_2_hist_ratio_plot(year, technique_str,sample_type,QCD_type):   #### hist1 will be CR hist, hist2 will be SR hist
	# Create a canvas


	input_path = "finalCombineFilesNewStats/%s/"%QCD_type 
	output_path = "plots/SRCR_shape_comparisons/"
	inputFile = input_path+ "combine_%s%s_Suu4_chi1.root"%(technique_str, year) 
	finput = ROOT.TFile(inputFile)

	histname_CR = "CR/%s"%sample_type
	histname_SR = "SR/%s"%sample_type

	hist1 = finput.Get(histname_CR)
	hist2 = finput.Get(histname_SR)

	print("Looking for %s in file %s."%(histname_CR,  inputFile ))
	hist1.Scale(1.0/hist1.Integral()) if hist1.Integral() > 0 else None
	print("Looking for %s in file %s."%( histname_SR, inputFile  ))
	hist2.Scale(1.0/hist2.Integral()) if hist2.Integral() > 0 else None



	canvas = ROOT.TCanvas("canvas", "Canvas", 1000, 1200)
	

	ROOT.gStyle.SetOptStat(0)

	# Upper pad for histograms
	upper_pad = ROOT.TPad("upper_pad", "upper_pad", 0, 0.3, 1, 1.0)
	upper_pad.SetBottomMargin(0)  # Upper and lower plot will be joined
	upper_pad.Draw()
	upper_pad.cd()  # Upper pad becomes the current pad

	# Draw the histograms on the upper pad
	hist1.SetLineColor(ROOT.kRed)
	hist1.SetLineWidth(4)
	technique_type = "cut-based"
	if "NN" in technique_str:
		technique_type = "NN-based"
	hist1.SetTitle("Comparison of the SR and CR shapes for %s (%s) (%s)"%(sample_type,year,technique_type))
	hist1.Draw("HIST")
	hist2.SetLineColor(ROOT.kBlue)
	hist2.SetLineWidth(4)

	hist2.Draw("HIST,SAME")

	# Add legend
	legend = ROOT.TLegend(0.7, 0.8, 0.9, 0.9)
	legend.AddEntry(hist1, "CR shape", "l")
	legend.AddEntry(hist2, "SR shape", "l")
	legend.Draw()

	# Lower pad for the ratio plot
	canvas.cd()  # Go back to the main canvas before defining the lower pad
	lower_pad = ROOT.TPad("lower_pad", "lower_pad", 0, 0.05, 1, 0.3)
	lower_pad.SetTopMargin(0)
	lower_pad.SetBottomMargin(0.2)
	lower_pad.Draw()
	lower_pad.cd()  # Lower pad becomes the current pad

	# Create the ratio histogram
	ratio_hist = hist2.Clone("ratio_hist")
	ratio_hist.SetLineColor(ROOT.kRed)
	ratio_hist.SetTitle("")  # Remove the title
	ratio_hist.SetMinimum(0)  # Define Y
	ratio_hist.SetMaximum(2)  # ...range
	ratio_hist.Sumw2()
	ratio_hist.Divide(hist1)

	# Draw the ratio plot
	ratio_hist.SetStats(0)  # No statistics box
	ratio_hist.Draw("E")

	# Draw a line at y = 1 for reference
	line = ROOT.TLine(ratio_hist.GetXaxis().GetXmin(), 1, ratio_hist.GetXaxis().GetXmax(), 1)
	#line.SetLineColor(ROOT.kRed)
	line.SetLineStyle(2)
	line.Draw()

	# Draw a line at y = 1 for reference
	line_1p2 = ROOT.TLine(ratio_hist.GetXaxis().GetXmin(), 1.2, ratio_hist.GetXaxis().GetXmax(), 1.2)
	#line_1p2.SetLineColor(ROOT.kRed)
	line_1p2.SetLineStyle(2)
	line_1p2.Draw()

	# Draw a line at y = 1 for reference
	line_0p8 = ROOT.TLine(ratio_hist.GetXaxis().GetXmin(),0.8, ratio_hist.GetXaxis().GetXmax(), 0.8)
	#line_0p8.SetLineColor(ROOT.kRed)
	line_0p8.SetLineStyle(2)
	line_0p8.Draw()



	# Configure the X axis of the ratio plot
	ratio_hist.SetLineWidth(4)
	ratio_hist.GetXaxis().SetTitle("linearized bin number")
	ratio_hist.GetXaxis().SetLabelSize(0.1)
	ratio_hist.GetXaxis().SetTitleSize(0.12)
	ratio_hist.GetXaxis().SetTitleOffset(1.0)

	# Configure the Y axis of the ratio plot
	ratio_hist.GetYaxis().SetTitle("SR shape /CR shape")
	#ratio_hist.GetYaxis().SetNdivisions(505)
	ratio_hist.GetYaxis().SetLabelSize(0.1)
	ratio_hist.GetYaxis().SetTitleSize(0.12)
	ratio_hist.GetYaxis().SetTitleOffset(0.5)

	# Update the canvas to draw everything
	canvas.Update()

	canvas.SaveAs(output_path + "linearized_SRCR_comparison_%s_%s%s.png"%(sample_type,technique_str,year))


#### create plots comparing the shape of the linearized SR QCD and CR QCD
def create_linear_SRCR_plots(year, technique_str, QCD_type ):

	print("Creating SRCR plot for %s/%s"%(year, technique_str))

	create_2_hist_ratio_plot(year, technique_str,"QCD",QCD_type)
	create_2_hist_ratio_plot(year, technique_str,"TTbar",QCD_type)
	create_2_hist_ratio_plot(year, technique_str,"ST",QCD_type)
	create_2_hist_ratio_plot(year, technique_str,"allBR",QCD_type)

	return



if __name__== "__main__":

	###########
	debug     = False
	runSignal = False
	###########
	#systematics = ["btagSFbc", "jec" ,"jer","pu", "pdf","fact", "renorm" ]
	#"nom",  
	systematics = ["CMS_bTagSF_M" , 	"CMS_bTagSF_M_corr" , "CMS_bTagSF_T_corr", "CMS_jer", "CMS_jec",   "CMS_bTagSF_bc_T_corr",	   "CMS_bTagSF_light_T_corr",	   "CMS_bTagSF_bc_M_corr",	   "CMS_bTagSF_light_M_corr",	  "CMS_bTagSF_bc_T_year",		"CMS_bTagSF_light_T_year",	  "CMS_bTagSF_bc_M_year",	   "CMS_bTagSF_light_M_year",		 "CMS_jer_eta193", "CMS_jer_193eta25",  "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal",   "CMS_jec_Absolute", "CMS_jec_BBEC1_year",		   "CMS_jec_Absolute_year",  "CMS_jec_RelativeSample_year", "CMS_pu", "CMS_topPt", "CMS_L1Prefiring", "CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory", "CMS_jec_AbsolutePU",   "CMS_jec_AbsoluteScale" ,   "CMS_jec_Fragmentation" , "CMS_jec_AbsoluteMPFBias",  "CMS_jec_RelativeFSR", "CMS_scale"]  ## systematic namings for cards   "CMS_btagSF", "CMS_bTagSF_T",
	regions = ["SR","CR","AT1b","AT0b"]

	histnames = ["allBR","QCD","TTbar"] ## "ST"
	if runSignal: histnames.append("sig")
	#mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1", "Suu5_chi1p5", "Suu5_chi2", "Suu6_chi1","Suu6_chi1p5", "Suu6_chi2", "Suu6_chi2p5", "Suu7_chi1","Suu7_chi1p5","Suu7_chi2", "Suu7_chi2p5", "Suu7_chi3","Suu8_chi1", "Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"]
	mass_points = ["Suu4_chi1",  "Suu4_chi1p5", "Suu5_chi1p5","Suu5_chi2","Suu6_chi1", "Suu6_chi2", "Suu7_chi2p5", "Suu8_chi2","Suu8_chi3"]

	## reduced mass points
	mass_points = ["Suu4_chi1",  "Suu5_chi1p5", "Suu6_chi2", "Suu7_chi2p5", "Suu8_chi3"]


	years = ["2015","2016","2017","2018"]
	year_str = ["15","16","17","18"]
	technique_strs = [""] #"NN_",

	QCD_types = ["QCDPT","QCDHT"]

	QCD_types = ["QCDPT"]


	for QCD_type in QCD_types:

		#technique_strs = [""]

		#### REMAKE TEXT FILEs:
		yield_impact_text = open("txt_files/NP_%s_yield_impacts.txt"%QCD_type,"w")
		yield_impact_text.write("year	 sample_type	 region	 NP_name	 nom_yield	 up_yield	 down_yield	 up_var	 down_var	max_var\n")
		yield_impact_text.close()

		yield_impact_text_corrected = open("txt_files/NP_%s_yield_impacts_corrected.txt"%QCD_type,"w")
		yield_impact_text_corrected.write("year	 sample_type	 region	 NP_name	 nom_yield	 up_yield	 down_yield	 up_var	 down_var	max_var\n")
		yield_impact_text_corrected.close()





		shape_impact_text = open("txt_files/NP_%s_shape_impacts.txt"%QCD_type,"w")
		shape_impact_text.write("year   sample_type   region   NP_name   mean_var_up   mean_var_down   mean_abs_var_up   mean_abs_var_down   var_stddev_up   var_stddev_down   max_var_up   max_var_down   max_var_abs\n") #  max_var_up   max_var_down   min_var_up   min_var_down
		shape_impact_text.close()

		shape_impact_text_corrected = open("txt_files/NP_%s_shape_impacts_corrected.txt"%QCD_type,"w")
		shape_impact_text_corrected.write("year   sample_type   region   NP_name   mean_var_up   mean_var_down   mean_abs_var_up   mean_abs_var_down   var_stddev_up   var_stddev_down   max_var_up   max_var_down   max_var_abs\n") # max_var_up   max_var_down   min_var_up   min_var_down 
		shape_impact_text_corrected.close()


		if debug:
			histnames = ["QCD"] ## "ST"
			mass_points = ["Suu4_chi1"]
			years = ["2017"]
			year_str = ["17"]
			systematics = ["CMS_jec_AbsolutePU"]  ## systematic namings for cards   "CMS_btagSF",
			regions = ["SR"]
		for iii,year in enumerate(years):
			for technique_str in technique_strs:
				create_linear_SRCR_plots(year,technique_str,QCD_type)




		## run for the "corrected" systematic plots
		print("Running for corrected systematic plots.")
		for iii,year in enumerate(years):
			for technique_str in technique_strs:
				for mass_point in mass_points:
					for histname in histnames:
						for systematic in systematics:
							for region in regions:
								#try:
								"""	if debug:
										print("============================================")
										print("============================================")
										print("========== WARNING: in debug mode ==========")
										print("============================================")
										print("============================================")"""

								if histname in ["allBR","QCD","TTbar"] and mass_point != "Suu4_chi1": continue ## only want to run once for these
								create_systematic_comparison_plot(year,mass_point,histname,systematic, year_str[iii], technique_str,region,QCD_type, True )
								#except:
								#	print("Failed %s/%s/%s/%s/%s/%s"%(year,technique_str,mass_point,histname,systematic,region))


		print("Running for raw (=uncorrected systematic plots).")
		for iii,year in enumerate(years):
			for technique_str in technique_strs:
				for mass_point in mass_points:
					for histname in histnames:
						for systematic in systematics:
							for region in regions:
								#try:
								"""if debug:
										print("============================================")
										print("============================================")
										print("========== WARNING: in debug mode ==========")
										print("============================================")
										print("============================================")"""
								if histname in ["allBR","QCD","TTbar"] and mass_point != "Suu4_chi1": continue ## only want to run once for these
								create_systematic_comparison_plot(year,mass_point,histname,systematic, year_str[iii], technique_str,region,QCD_type, False )
								#except:
								#	print("Failed %s/%s/%s/%s/%s/%s"%(year,technique_str,mass_point,histname,systematic,region)) 





