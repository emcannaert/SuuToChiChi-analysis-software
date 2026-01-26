import sys,os,time
import numpy as np
import ROOT
from write_cms_text.write_cms_text import write_cms_text
from return_BR_SF.return_BR_SF import return_BR_SF
from return_signal_SF.return_signal_SF import return_signal_SF
from combine_hists import combine_hists

# plotter for the signal kinematics for a few mass points

def create_signal_kin_plots(year, hist_type, hist_cut ):   # year = year, hist_type = the name of the histogram to plot, hist_cut = where to draw red line


	infile_path 	 = "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles_optWP/"   # location of processed files 
	output_plot_path = "plots/signal_kinematics/"

	sig_types = [ "Signal: 4 TeV, M_{\\chi}=1 TeV", 
		"Signal: M_{S_{uu}}= 5 TeV, M_{\\chi}=1.5 TeV", 
		"Signal: M_{S_{uu}}= 6 TeV, M_{\\chi}=2 TeV", 
		"Signal: M_{S_{uu}}= 7 TeV, M_{\\chi}=2.5 TeV", 
		"Signal: M_{S_{uu}}= 7 TeV, M_{\\chi}=3 TeV", 
		"Signal: M_{S_{uu}}= 8 TeV, M_{\\chi}=3 TeV"
	]

	mass_points = ["Suu4_chi1", "Suu5_chi1p5", "Suu6_chi2","Suu7_chi2p5","Suu8_chi3"]
	decays	  = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]


	sig_sample_list = [ ["%s_%s"%(mass_point,decay) for decay in decays] for mass_point in mass_points ]

	sig_file_paths = [ { sample_type: "{}{}_{}_processed.root".format(infile_path,sample_type, year) for sample_type in sig_samples } for sig_samples in sig_sample_list	  ]

	sig_weights = [ { "%s_%s"%(mass_point,decay): 1.0 for decay in decays  } for mass_point in mass_points   ]


	sig_hists = [

		combine_hists(
		sig_sample_list,
		sig_file_paths[iii],
		hist_name,
		hist_weights=sig_weights[iii]
		#hist_label = hist_name + "_" + year
		)  for iii,sample_list in enumerate(sig_sample_list)   ]

	fill_colors = [ROOT.kGreen, ROOT.kViolet, ROOT.kYellow, ROOT.kRed+1]
	line_colors = [ROOT.kBlack, ROOT.kCyan, ROOT.kMagenta, ROOT.kOrange, ROOT.kAzure]
	line_styles = [1, 2, 6, 7, 9]


	legend = ROOT.TLegend(0.53, 0.70, 0.9, 0.90)
	legend.SetNColumns(2)
	
	c1 = ROOT.TCanvas("","",1600,1200)

	hs.SetMinimum(1e-2)

	hs.SetMaximum(1e2 * hs.GetMaximum())

	hs.Draw("HIST")

	for iii,sig_hist in enumerate(sig_hists):
		sig_hist.SetLineColor(line_colors[iii])
		sig_hist.SetLineStyle(line_styles[iii])
		sig_hist.SetLineWidth(3)
		sig_hist.SetMinimum(1e-2)
		sig_hist.Draw("HIST, SAME")
		legend.AddEntry(sig_hist, sig_types[iii], "l")


	# Draw line where cut is put in place
	line = ROOT.TLine(hist_cut-0.5, 0, hist_cut-0.5, 1e2 * hs.GetMaximum() )
	line.SetLineColor(ROOT.kRed)
	line.SetLineWidth(4)  # Optional: make the line thicker
	line.SetLineStyle(1)  # Optional: dashed line (1 = solid, 2 = dashed, 3 = dotted, etc.)

	# Draw the line on the same canvas
	line.Draw("SAME")

	c1.Update()  # refresh canvas

	# Add text along the line
	text = ROOT.TText()
	text.SetTextAngle(90)      # rotate 90 degrees along vertical line
	text.SetTextAlign(22)      # centered
	text.SetTextSize(0.015)     # normalized size
	text.SetTextColor(ROOT.kBlack)
	#offset_val = 1.05 if hist_cut > 10 else 1.025
	text.DrawText((1.075)*(hist_cut-0.5), BR_hists[0].GetMaximum()*0.002, "Selection cut applied")


	# Add label under legend using TLatex or TText
	label = ROOT.TLatex()
	label.SetNDC()  # coordinates normalized to canvas
	label.SetTextSize(0.018)
	x_label = 0.65
	y_label = 0.68  # just below the legend
	label.DrawLatex(x_label, y_label, r"#bf{Note: signal is unscaled}")

	legend.SetBorderSize(0)
	legend.SetFillStyle(0)
	legend.Draw()

	CMS_label_pos = 0.165
	SIM_label_pos = 0.342
	write_cms_text(CMS_label_pos, SIM_label_pos)


	c1.SetLogy()
	c1.SaveAs("%s/%s_sigBR_comparison_%s.png"%(output_plot_path,hist_type, year))


if __name__ == "__main__":

	years = ["2015","2016","2017","2018"]

	hist_names = ["h_totHT", "h_nfatjets", "h_nfatjets_pre", "h_dijet_mass", "h_nMedBTags", "h_nCA4_300_1b"]
	hist_cuts = [1600., 3, 2, 1000., 2,1]

	for year in years:
		for iii,hist_name in enumerate(hist_names):
			create_signal_kin_plots(year, hist_name, hist_cuts[iii] )



