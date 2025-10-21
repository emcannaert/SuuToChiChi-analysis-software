	
import sys,os,time
import numpy as np
import ROOT
from write_cms_text.write_cms_text import write_cms_text
from return_BR_SF.return_BR_SF import return_BR_SF
from return_signal_SF.return_signal_SF import return_signal_SF


### creates plots of initial selection variables (directly before their corresponding cut is applied) 
### for combined BRs (as stack) and a few signal mass points

def create_initial_selction_plots(year: str, hist_type: str, hist_cut ):   # year = year, hist_type = the name of the histogram to plot, hist_cut = where to draw red line


	infile_path 	 = "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/"   # location of processed files 
	output_plot_path = "plots/initial_selection/"

	QCD_samples   = ["QCDMC_Pt_170to300_","QCDMC_Pt_300to470_","QCDMC_Pt_470to600_","QCDMC_Pt_600to800_","QCDMC_Pt_800to1000_",
        				 "QCDMC_Pt_1000to1400_","QCDMC_Pt_1400to1800_","QCDMC_Pt_1800to2400_","QCDMC_Pt_2400to3200_", "QCDMC_Pt_3200toInf_" ]
	TTbar_samples = ["TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_"]
	WJets_samples = ["WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"]
	ST_samples    = ["ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_" ]

	BR_types  = ["Single Top", "W+Jets", r"t \bar{t}", "QCD"]
	sig_types = [ "Signal: 4 TeV, M_{\\chi}=1 TeV", 
	    "Signal: M_{S_{uu}}= 5 TeV, M_{\\chi}=1.5 TeV", 
	    "Signal: M_{S_{uu}}= 6 TeV, M_{\\chi}=2 TeV", 
	    "Signal: M_{S_{uu}}= 7 TeV, M_{\\chi}=2.5 TeV", 
	    "Signal: M_{S_{uu}}= 7 TeV, M_{\\chi}=3 TeV", 
	    "Signal: M_{S_{uu}}= 8 TeV, M_{\\chi}=3 TeV"
	]

	sample_lists = [ ST_samples, WJets_samples, TTbar_samples, QCD_samples  ] # increasing order of yield for stack plot 

	BR_file_paths = [ { sample_type: "{}{}_{}_processed.root".format(infile_path,sample_type, year) for sample_type in sample_list for sample_list in sample_lists	}  ]
	BR_weights = [ { sample_type: BR_SFs[sample_type.replace("-","_")][year] for sample_type in sample_list for sample_list in sample_lists }  ]
 
	hist_name = "nom/%s"%(hist_type)

	BR_hists = [   
	combine_hists(
		sample_list,
		sample_lists[iii],
		hist_name,
		hist_weights=BR_weights[iii]
		#hist_label = hist_name + "_" + year # can't remember what this does
	)  for iii,sample_list in enumerate(sample_lists)  ] 


	mass_points = ["Suu4_chi1", "Suu5_chi1p5", "Suu6_chi2","Suu7_chi2p5","Suu8_chi3"]
	decays      = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]


	sig_samples = [ ["%s_%s"%(mass_point,decay) for decay in decays] for mass_point in mass_points ]
	#sig_weights = [ [  return_signal_SF(year,mass_point,decay) for decay in decays  ] for mass_point in mass_points   ]

	sig_weights = [ [  1.0 for decay in decays  ] for mass_point in mass_points   ]


	sig_hists = [

		combine_hists(
		sample_list,
		sig_samples[iii],
		hist_name,
		hist_weights=sig_weights[iii]
		#hist_label = hist_name + "_" + year
		)  for iii,sample_list in enumerate(sig_samples)   ]


	# now create a stack plot

	fill_colors = [ROOT.kGreen, ROOT.kViolet, ROOT.KYellow, ROOT.kRed]
	line_colors = [ROOT.kBlack, ROOT.kCyan, ROOT.KMagenta, ROOT.kOrange]
	line_styles = [1, 2, 6, 7, 9]


    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)


    hs = ROOT.THStack("h_stack", "%s;%s;%s"%(BR_hists[0].GetTitle(), BR_hists[0].GetXaxis().GetTitle(). BR_hists[0].GetYaxis().GetTitle() )   )
    
    for iii,BR_hist in enumerate(BR_hists):
    	BR_hist.SetFillColor(fill_colors[iii])
    	hs.Add(BR_hist)
    	legend.AddEntry(BR_hist, BR_types[iii], "f")

    c1 = ROOT.TCanvas("","",1600,1200)


    hs.Draw("HIST")

    for iii,sig_hist in enumerate(sig_hists):
    	sig_hist.SetLineColor(line_colors[iii])
    	sig_hist.SetLineStyle(line_styles[iii])
    	sig_hist.Draw("HIST, SAME")
    	legend.AddEntry(sig_hist, sig_types[iii], "l")


    # Draw line where cut is put in place
	line = ROOT.TLine(hist_cut, 0, hist_cut, BR_hists[0].GetMaximum())
	line.SetLineColor(ROOT.kRed+3)
	line.SetLineWidth(2)  # Optional: make the line thicker
	line.SetLineStyle(2)  # Optional: dashed line (1 = solid, 2 = dashed, 3 = dotted, etc.)

	# Draw the line on the same canvas
	line.Draw("same")
	legend.Draw()

	CMS_label_pos = 0.152
	SIM_label_pos = 0.295
	write_cms_text(CMS_label_pos, SIM_label_pos)

	c1.SaveAs("%s/%s_sigBR_comparison_%s.png"%(output_plot_path,hist_name, year))


if __name__ == "__main__":

	years = ["2015","2016","2017","2018"]

	hist_names = ["h_totHT", "h_nfatjets", "h_nfatjets_pre", "h_dijet_mass", "h_nCA4_300_1b"]
	hist_cuts = [1600., 3, 2, 1000., 2]

	for year in years:
		for iii,hist_name in enumerate(hist_names):
			create_initial_selction_plots(year, hist_name, hist_cuts[iii] )



