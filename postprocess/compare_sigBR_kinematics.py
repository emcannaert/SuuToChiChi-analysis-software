	
import sys,os,time
import numpy as np
import ROOT
from write_cms_text.write_cms_text import write_cms_text
from return_BR_SF.return_BR_SF import return_BR_SF
from return_signal_SF.return_signal_SF import return_signal_SF
from combine_hists import combine_hists

### Create plots comparing kinematic variables (normalized) for combined background and a few signal mass points

def era_translator(year):
	if year == "2015": return "2016preAPV"
	elif year == "2016": return "2016postAPV"
	else: return year

def compare_sigBR_kinematics(year, hist_type ):   # year = year, hist_type = the name of the histogram to plot


	infile_path 	 = "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/"   # location of processed files 
	output_plot_path = "plots/sig_BR_kinematics_comp/"

	QCD_samples   = ["QCDMC_Pt_170to300","QCDMC_Pt_300to470","QCDMC_Pt_470to600","QCDMC_Pt_600to800","QCDMC_Pt_800to1000",
						 "QCDMC_Pt_1000to1400","QCDMC_Pt_1400to1800","QCDMC_Pt_1800to2400","QCDMC_Pt_2400to3200", "QCDMC_Pt_3200toInf" ]
	TTbar_samples = ["TTJetsMCHT800to1200","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf"]
	WJets_samples = ["WJetsMC_LNu-HT800to1200", "WJetsMC_LNu-HT1200to2500",  "WJetsMC_LNu-HT2500toInf", "WJetsMC_QQ-HT800toInf"]
	ST_samples	= ["ST_t-channel-top_inclMC","ST_t-channel-antitop_inclMC","ST_s-channel-hadronsMC","ST_s-channel-leptonsMC","ST_tW-antiTop_inclMC","ST_tW-top_inclMC" ]

	BR_types  = ["Single Top", "W+Jets", r"t \bar{t}", "QCD"]
	sig_types = [ "Signal: M_{S_{uu}} = 4 \\text{ TeV}, M_{\\chi}= 1 \\text{ TeV}", 
		"Signal: M_{S_{uu}} = 5 \\text{ TeV}, M_{\\chi} = 1.5 \\text{ TeV}", 
		"Signal: M_{S_{uu}} = 6 \\text{ TeV}, M_{\\chi} = 2 \\text{ TeV}", 
		"Signal: M_{S_{uu}} = 7 \\text{ TeV}, M_{\\chi} = 2.5 \\text{ TeV}", 
		"Signal: M_{S_{uu}} = 8 \\text{ TeV}, M_{\\chi} = 3 \\text{ TeV}", 
	]

	sample_lists = [ ST_samples, WJets_samples, TTbar_samples, QCD_samples  ] # increasing order of yield for stack plot 

	BR_file_paths = [ { sample_type: "{}{}_{}_processed.root".format(infile_path,sample_type, year) for sample_type in sample_list } for sample_list in sample_lists	  ]
	BR_weights = [ { sample_type: return_BR_SF(year,sample_type.replace("-","_") ) for sample_type in sample_list}  for sample_list in sample_lists   ]
 
	hist_name = "nom/%s"%(hist_type)

	BR_hists = [   
	combine_hists(
		sample_list,
		BR_file_paths[iii],
		hist_name,
		hist_weights=BR_weights[iii]
		#hist_label = hist_name + "_" + year # can't remember what this does
	)  for iii,sample_list in enumerate(sample_lists)  ] 


	mass_points = ["Suu4_chi1", "Suu5_chi1p5", "Suu6_chi2","Suu7_chi2p5","Suu8_chi3"]
	decays	  = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]


	sig_sample_list = [ ["%s_%s"%(mass_point,decay) for decay in decays] for mass_point in mass_points ]

	sig_file_paths = [ { sample_type: "{}{}_{}_processed.root".format(infile_path,sample_type, year) for sample_type in sig_samples } for sig_samples in sig_sample_list	  ]

	#sig_weights = [ [  return_signal_SF(year,mass_point,decay) for decay in decays  ] for mass_point in mass_points   ]

	sig_weights = [ { "%s_%s"%(mass_point,decay): 1.0 for decay in decays  } for mass_point in mass_points   ]


	#print("sig_sample_list is %s"%sig_sample_list )

	sig_hists = [

		combine_hists(
		sample_list,
		sig_file_paths[iii],
		hist_name,
		hist_weights=sig_weights[iii]
		#hist_label = hist_name + "_" + year
		)  for iii,sample_list in enumerate(sig_sample_list)   ]


	# now create a stack plot

	fill_colors = [ROOT.kGreen, ROOT.kViolet, ROOT.kYellow, ROOT.kRed+1]
	line_colors = [ROOT.kBlack, ROOT.kCyan, ROOT.kMagenta, ROOT.kOrange, ROOT.kAzure]
	line_styles = [1, 2, 6, 7, 9]


	legend = ROOT.TLegend(0.4, 0.65, 0.9, 0.90)
	legend.SetNColumns(2)

	hs = ROOT.THStack("h_stack", "%s;%s;%s"%(BR_hists[0].GetTitle(), BR_hists[0].GetXaxis().GetTitle(), BR_hists[0].GetYaxis().GetTitle() )   )
	
	total_BR = 0
	for iii,BR_hist in enumerate(BR_hists):
		total_BR += BR_hist.Integral()

	for iii,BR_hist in enumerate(BR_hists):
		BR_hist.Scale(1.0/total_BR)
		BR_hist.SetFillColor(fill_colors[iii])
		BR_hist.SetMinimum(1e-4)
		BR_hist.SetLineColor(0)
		hs.Add(BR_hist)
		legend.AddEntry(BR_hist, BR_types[iii], "f")



	c1 = ROOT.TCanvas("","",1600,1200)

	hs.SetMinimum(1e-2)

	hs.SetMaximum(1e2 * hs.GetMaximum())

	hs.Draw("HIST")

	for iii,sig_hist in enumerate(sig_hists):

		sig_hist.Scale(1.0/sig_hist.Integral())
		sig_hist.SetLineColor(line_colors[iii])
		sig_hist.SetLineStyle(line_styles[iii])
		sig_hist.SetLineWidth(3)
		sig_hist.SetMinimum(1e-2)
		sig_hist.Draw("HIST, SAME")
		legend.AddEntry(sig_hist, sig_types[iii], "l")

	c1.Update()  # refresh canvas

	c1.SetLogy()

	# Add label under legend using TLatex or TText
	label = ROOT.TLatex()
	label.SetNDC()  # coordinates normalized to canvas
	label.SetTextSize(0.018)
	x_label = 0.4
	y_label = 0.55  # just below the legend
	#label.DrawLatex(x_label, y_label, r"#bf{Note: Combined background and individual signal samples are normalized}")

	legend.SetBorderSize(0)
	legend.SetFillStyle(0)
	legend.Draw()

	CMS_label_pos = 0.165
	SIM_label_pos = 0.342
	write_cms_text(CMS_label_pos, SIM_label_pos)


	# Define the text
	text = ROOT.TLatex()
	text.SetTextSize(0.032)
	text.SetTextFont(62)
	text.SetTextAlign(22)  # Center alignment (horizontal and vertical)
	text.DrawLatexNDC(0.25, 0.80, "Era: %s"%(era_translator(year))) 
	text.DrawLatexNDC(0.25, 0.76, "Normalized") 




	c1.SaveAs("%s/%s_sigBR_comparison_%s.png"%(output_plot_path,hist_type, year))


if __name__ == "__main__":

	years = ["2015","2016","2017","2018"]

	hist_names = [ "h_nAK4",
					"h_nAK4_pt50",
					"h_nAK4_pt75",
					"h_nAK4_pt100",
					"h_nAK4_pt150",
					"h_AK8_jet_mass",
					"h_AK8_jet_pt",
					"h_AK8_eta",
					"h_AK8_phi",
					"h_AK4_eta",
					"h_AK4_phi",
					"h_nCA4_100_1b",
					"h_nCA4_50_0b", 
					"h_SJ_mass",
					"h_disuperjet_mass"


					]


	for year in years:
		for iii,hist_name in enumerate(hist_names):
			compare_sigBR_kinematics(year, hist_name )



