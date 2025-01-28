import ROOT
from return_BR_SF.return_BR_SF import return_BR_SF
from return_data_samples.return_data_samples import return_data_samples
import numpy as np

def mmake_systematic_hT_comparison_plots(year):
	output_dir = "plots/dataMC/nom_systematic_comparisons/"

	data_samples = return_data_samples(year)
	samples = [  
		"QCDMC1000to1500",
		"QCDMC1500to2000",
		"QCDMC2000toInf",
		"TTToHadronicMC",
		"TTToSemiLeptonicMC",
		"TTToLeptonicMC",
	] 

	processed_file_dir = "../combinedROOT/processedFiles/"
	scale_factors = [return_BR_SF(year, sample) for sample in samples]

	MC_file_names = [processed_file_dir + sample + "_%s_processed.root" % year for sample in samples]
	data_file_names = [processed_file_dir + sample + "_%s_processed.root" % year for sample in data_samples]

	hist_names = [ 
		"h_totHT_unscaled",
		"h_totHT_prefiringToppt",
		"h_totHT_PU",
		"h_totHT_ScalePdf",
		"h_totHT_bTag"
	] 

	legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
	colors = [ROOT.kRed, ROOT.kBlue, ROOT.kOrange, ROOT.kViolet, ROOT.kGreen, ROOT.kBlack]
	combined_hists = [None] * len(hist_names)

	# Open MC files and fill histograms
	for iii, filename in enumerate(MC_file_names):
		print("Opening file %s" % filename)
		file_ = ROOT.TFile.Open(filename)
		if not file_ or file_.IsZombie():
			print("ERROR: file %s not opened correctly." % (filename))

		for jjj, hist_name in enumerate(hist_names):
			if iii == 0:
				combined_hists[jjj] = file_.Get("nom/" + hist_name)
				combined_hists[jjj].Scale(scale_factors[iii])
				combined_hists[jjj].SetDirectory(0)
			else:
				h2 = file_.Get("nom/" + hist_name)
				h2.Scale(scale_factors[iii])
				h2.SetDirectory(0)
				combined_hists[jjj].Add(h2)

	# Open data files and fill the data histogram
	combined_data = None
	for iii, filename in enumerate(data_file_names):
		file_ = ROOT.TFile.Open(filename)
		if not file_ or file_.IsZombie():
			print("ERROR: file %s not opened correctly." % (filename))
			return
		if iii == 0: 
			combined_data = file_.Get("nom/h_totHT")
			combined_data.SetDirectory(0)
		else: 
			combined_data.Add(file_.Get("nom/h_totHT"))

	# Add data histogram to the list
	combined_hists.extend([combined_data])
	hist_labels = ["uncorrected", "Prefiring+TopPt", "PU", "Scale+PDF", "b-tagging", "data"]

	# Create canvas and pads
	canvas = ROOT.TCanvas("canvas", "Canvas with Two Pads", 1200, 1000)
	pad1_height = 0.75
	pad2_height = 0.25
	ROOT.gStyle.SetOptStat(0)

	# Create the upper pad for the main histograms
	pad1 = ROOT.TPad("pad1", "Top Pad", 0, pad2_height, 1, 1)
	pad1.SetBottomMargin(0)
	pad1.Draw()

	# Create the lower pad for the ratio plots
	pad2 = ROOT.TPad("pad2", "Bottom Pad", 0, 0, 1, pad2_height)
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.3)
	pad2.Draw()


	# Switch to the upper pad and plot the histograms
	pad1.cd()
	pad1.SetLogy()
	for jjj, combined_hist in enumerate(combined_hists):
		combined_hist.SetLineWidth(2)
		combined_hist.SetLineColor(colors[jjj])
		if jjj == 0:
			combined_hist.SetTitle("Comparisons of Event H_{{T}} with various correction levels {0}".format(year))
			combined_hist.GetXaxis().SetLabelSize(0)  # Hide x-axis labels for the upper pad
			combined_hist.Draw("HIST")
		else:
			if jjj == len(combined_hists) -1: 
				combined_hist.Draw("SAME")
			else: 
				combined_hist.Draw("HIST SAME")
		legend.AddEntry(combined_hist, hist_labels[jjj], "l")

	legend.Draw()

	# Switch to the lower pad for the ratio plots
	pad2.cd()
	pad2.Clear()



	print("----------------------------- START %s ---------------------------------"%year)

	ratio_plots = [None] * (len(combined_hists) - 1)

	for jjj in range(0,len(combined_hists)-1):  # Exclude the last index (data)

		#unscaled_ratio = combined_hists[-1].Clone("ratio_unscaled_%s"%jjj)
		#unscaled_ratio.Divide( combined_hists[0]   )

		ratio_plots[jjj] = combined_hists[-1].Clone("ratio_plot_%s"%jjj)
		ratio_denom = combined_hists[jjj].Clone("ratio_denom_%s"%jjj)

		ratio_plots[jjj].Divide(ratio_denom)  # Divide MC by data, .Clone("ratio_plot_denom_%s"%(jjj)
		ratio_plots[jjj].SetLineWidth(1)
		ratio_plots[jjj].SetLineColor(colors[jjj])
		ratio_plots[jjj].SetDirectory(0)
		ratio_plots[jjj].SetTitle("")

		#ratio_plot.Divide( unscaled_ratio )

		print("Year: %s,     %s hist (%s) : "%(year, hist_labels[jjj],jjj))
		for iii in range(0,ratio_plots[jjj].GetNbinsX()):
			print("bin %s, contents = %s"%(iii, ratio_plots[jjj].GetBinContent(iii)))
		if jjj == 0:
			ratio_plots[jjj].GetYaxis().SetTitle("data/MC")
			ratio_plots[jjj].SetMaximum(1.25)
			ratio_plots[jjj].SetMinimum(0.75)
			ratio_plots[jjj].GetYaxis().SetNdivisions(505)
			ratio_plots[jjj].GetYaxis().SetTitleSize(0.1)
			ratio_plots[jjj].GetYaxis().SetTitleOffset(0.4)
			ratio_plots[jjj].GetYaxis().SetLabelSize(0.08)
			ratio_plots[jjj].GetXaxis().SetTitle("Event H_{T}")
			ratio_plots[jjj].GetXaxis().SetTitleSize(0.1)
			ratio_plots[jjj].GetXaxis().SetTitleOffset(1.0)
			ratio_plots[jjj].GetXaxis().SetLabelSize(0.08)
			#ratio_plots[jjj].Draw("HIST")
			print("Drawing hist jjj = %s with integral %s with color %s.     (draw option HIST)"%(jjj, ratio_plots[jjj].Integral(),colors[jjj]))
		else:
			#ratio_plots[jjj].Draw("HIST,SAME")
			print("Drawing hist jjj = %s with integral %s with color %s.     (draw option HIST,SAME)"%(jjj, ratio_plots[jjj].Integral(),colors[jjj]))
		print("finished with %s hist (%s) "%(hist_labels[jjj],jjj))

	ratio_plots[0].Draw("HIST")
	ratio_plots[1].Draw("HIST,SAME")
	ratio_plots[2].Draw("HIST,SAME")
	ratio_plots[3].Draw("HIST,SAME")
	ratio_plots[4].Draw("HIST,SAME")

	canvas.Update()
	canvas.SaveAs(output_dir + "totHT_comparisons_{0}.png".format(year))
	print("----------------------------- FINISHED %s ---------------------------------"%year)

if __name__ == "__main__":
	years = ["2015", "2016", "2017", "2018"]
	for year in years:
		mmake_systematic_hT_comparison_plots(year)