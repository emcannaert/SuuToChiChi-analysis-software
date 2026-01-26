import ROOT 
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from write_cms_text import write_cms_text
import datetime
from combine_hists import combine_hists
from return_BR_SF.return_BR_SF import return_BR_SF
from return_signal_SF.return_signal_SF import return_signal_SF


# makes a comparison of 2D shifted and unshifted signal and background.
# This is to see what is causing the limits so different between the two.
# also makes 1D comparison plots

## ERROR, I suspect the denominator or numberator of the comparison is the BR when the sig is wanted ...  


timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

years = ["2015","2016","2017","2018"]
mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1","Suu5_chi1p5","Suu5_chi2","Suu6_chi1","Suu6_chi1p5",
"Suu6_chi2","Suu6_chi2p5","Suu7_chi1", "Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3","Suu8_chi1","Suu8_chi1p5",
"Suu8_chi2","Suu8_chi2p5","Suu8_chi3"]

QCD_samples   = ["QCDMC_Pt_170to300","QCDMC_Pt_300to470","QCDMC_Pt_470to600","QCDMC_Pt_600to800","QCDMC_Pt_800to1000",
					 "QCDMC_Pt_1000to1400","QCDMC_Pt_1400to1800","QCDMC_Pt_1800to2400","QCDMC_Pt_2400to3200", "QCDMC_Pt_3200toInf" ]
TTbar_samples = ["TTJetsMCHT800to1200","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf"]
WJets_samples = ["WJetsMC_LNu-HT800to1200", "WJetsMC_LNu-HT1200to2500",  "WJetsMC_LNu-HT2500toInf", "WJetsMC_QQ-HT800toInf"]
ST_samples	= ["ST_t-channel-top_inclMC","ST_t-channel-antitop_inclMC","ST_s-channel-hadronsMC","ST_s-channel-leptonsMC","ST_tW-antiTop_inclMC","ST_tW-top_inclMC" ]

BR_types  = ["Single Top", "W+Jets", r"t \bar{t}", "QCD"]
sig_types = [ "Signal: 4 TeV, M_{\\chi}=1 TeV", 
	"Signal: M_{S_{uu}}= 5 TeV, M_{\\chi}=1.5 TeV", 
	"Signal: M_{S_{uu}}= 6 TeV, M_{\\chi}=2 TeV", 
	"Signal: M_{S_{uu}}= 7 TeV, M_{\\chi}=2.5 TeV", 
	"Signal: M_{S_{uu}}= 7 TeV, M_{\\chi}=3 TeV", 
	"Signal: M_{S_{uu}}= 8 TeV, M_{\\chi}=3 TeV"
]

sample_lists_nested = [ ST_samples, WJets_samples, TTbar_samples, QCD_samples  ] # increasing order of yield for stack plot 
sample_list = [sample for samples in sample_lists_nested for sample in samples]

mass_points = ["Suu4_chi1", "Suu5_chi1p5", "Suu6_chi2","Suu7_chi2p5","Suu8_chi3"]
decays	  = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]


def compare_2D_shifted():

	plot_dir = "../plots/2D_shift_comparisons/"

	output_pdf = os.path.join(plot_dir,  "shifted_vs_unshifted_2D_%s.pdf"%timestamp)
	first_page = True



	for year in years:
		for mass_point in mass_points:

			sig_sample_list = [ "%s_%s"%(mass_point,decay) for decay in decays] 


			dir_unshifted = "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/"
			dir_shifted  = "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles_shiftedMass/"

			file_name = "combine_%s_%s.root"%(year,mass_point)
			hist_name = "nom/h_MSJ_mass_vs_MdSJ_SR" # + hist type

			BR_file_paths_unshifted	 = { sample_type: "{}{}_{}_processed.root".format(dir_unshifted,sample_type, year) for sample_type in sample_list } 
			BR_file_paths_shifted	   = { sample_type: "{}{}_{}_processed.root".format(dir_shifted,  sample_type, year) for sample_type in sample_list } 
			BR_weights		   		= { sample_type: return_BR_SF(year,sample_type.replace("-","_") ) for sample_type in sample_list}

			sig_file_paths_unshifted =  { sample_type: "{}{}_{}_processed.root".format(dir_unshifted,sample_type, year) for sample_type in sig_sample_list }
			sig_file_paths_shifted   =  { sample_type: "{}{}_{}_processed.root".format(dir_shifted,  sample_type, year) for sample_type in sig_sample_list } 
			sig_weights = {"%s_%s"%(mass_point,decay):  return_signal_SF(year,mass_point,decay) for decay in decays }

			hist_sig_unshifted = combine_hists(
				sig_sample_list,
				sig_file_paths_unshifted,
				hist_name,
				sig_weights
			) 

			hist_sig_shifted = combine_hists(
				sig_sample_list,
				sig_file_paths_shifted,
				hist_name,
				sig_weights
			) 

			hist_BR_unshifted = combine_hists(
				sample_list,
				BR_file_paths_unshifted,
				hist_name,
				BR_weights
			) 

			hist_BR_shifted = combine_hists(
				sample_list,
				BR_file_paths_shifted,
				hist_name,
				BR_weights
			) 


			if mass_point == "Suu4_chi1":
				hists = [(hist_sig_unshifted,hist_sig_shifted,"Signal","Signal"),(hist_BR_unshifted,hist_BR_shifted,"Combined BR","BR")] ## order is unshifted, shifted
			else:
				hists = [(hist_sig_unshifted,hist_sig_shifted,"Signal","Signal")] ## order is unshifted, shifted

			#### create plots
			for unshifted_hist, shifted_hist, title, short_title in hists:

				c1 = ROOT.TCanvas("","",1600,1200)
				#c1.SetLogz()

				max_val = max(unshifted_hist.GetMaximum(),shifted_hist.GetMaximum() )
				unshifted_hist.SetMaximum(1.2*max_val)
				shifted_hist.SetMaximum(1.2*max_val)

				shifted_hist.SetMinimum(1e-2)
				unshifted_hist.SetMinimum(1e-2)


				unshifted_integral =  unshifted_hist.Integral()


				title_str = mass_point if "Signal" in title else title

				unshifted_hist.SetTitle("%s (Unshifted Mass) (%s) (%s)"%(unshifted_hist.GetTitle(), year, title_str))
				shifted_hist.SetTitle("%s (Shifted Mass) (%s) (%s)"%(unshifted_hist.GetTitle(), year, title_str))

				unshifted_hist.Draw("COLZ")
				c1.SaveAs("%s/2D_unshifted_mass_%s_%s_%s.png"%(plot_dir, mass_point,year,short_title))

				shifted_hist.Draw("COLZ")
				c1.SaveAs("%s/2D_shifted_mass_%s_%s_%s.png"%(plot_dir, mass_point,year,short_title))

				shifted_integral   =  shifted_hist.Integral()

				unshifted_hist.SetTitle("Shifted / Unshifted Linearized Avg. SJ Mass vs DiSJ Mass for %s (%s) (%s)"%(title,mass_point,year))
				shifted_hist.SetTitle("Shifted / Unshifted Linearized Avg. SJ Mass vs DiSJ Mass for %s (%s) (%s)"%(title,mass_point,year))

				#unshifted_hist.Draw("HIST")
				shifted_hist.Divide(unshifted_hist)
				shifted_hist.Draw("COLZ")

				text = ROOT.TText()
				text.SetNDC(True)  
				text.SetTextSize(0.025)
				text.DrawText(0.4, 0.85, "Unshifted Integral = %s"%(unshifted_integral))
				text.DrawText(0.4, 0.82, "Shifted Integral = %s"%( shifted_integral ))

				write_cms_text.write_cms_text(CMS_label_xpos=0.138, SIM_label_xpos=0.345,CMS_label_ypos = 0.925, SIM_label_ypos = 0.925, lumistuff_xpos=0.90, lumistuff_ypos=0.91, year = "", uses_data=True)

				c1.SaveAs("%s/2D_shifted_mass_comparison_%s_%s_%s.png"%(plot_dir, mass_point,year,short_title))

				if first_page:
					c1.SaveAs(output_pdf + "[")
					first_page = False

				c1.SaveAs(output_pdf)
				
	c2 = ROOT.TCanvas("", "", 1200, 1200)
	if not first_page:
		c2.SaveAs(output_pdf + "]")
		print "All plots written to", output_pdf
	else:
		print "No plots created for", hist_name, ". PDF not generated."
	del c2  

	return

def compare_1D_shifted():

	ROOT.gStyle.SetOptStat(0)

	plot_dir = "../plots/1D_shift_comparisons/"

	output_pdf = os.path.join(plot_dir,  "shifted_vs_unshifted_1D_%s.pdf"%timestamp)
	first_page = True

	output_pdf_1D = os.path.join(plot_dir,  "shifted_and_unshifted_1D_%s.pdf"%timestamp)
	first_page_1D = True

	hist_types = ["h_SJ_mass_SR","h_disuperjet_mass_SR"]

	for year in years:
		for mass_point in mass_points:
			for hist_type in hist_types:

				sig_sample_list = [ "%s_%s"%(mass_point,decay) for decay in decays] 

				dir_unshifted = "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/"
				dir_shifted  = "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles_shiftedMass/"

				file_name = "combine_%s_%s.root"%(year,mass_point)
				hist_name = "nom/%s"%hist_type # + hist type

				BR_file_paths_unshifted	 = { sample_type: "{}{}_{}_processed.root".format(dir_unshifted,sample_type, year) for sample_type in sample_list } 
				BR_file_paths_shifted	   = { sample_type: "{}{}_{}_processed.root".format(dir_shifted,  sample_type, year) for sample_type in sample_list } 
				BR_weights		   		= { sample_type: return_BR_SF(year,sample_type.replace("-","_") ) for sample_type in sample_list}

				sig_file_paths_unshifted =  { sample_type: "{}{}_{}_processed.root".format(dir_unshifted,sample_type, year) for sample_type in sig_sample_list }
				sig_file_paths_shifted   =  { sample_type: "{}{}_{}_processed.root".format(dir_shifted,  sample_type, year) for sample_type in sig_sample_list } 
				sig_weights = {"%s_%s"%(mass_point,decay):  return_signal_SF(year,mass_point,decay) for decay in decays }

				hist_sig_unshifted = combine_hists(
					sig_sample_list,
					sig_file_paths_unshifted,
					hist_name,
					sig_weights
				) 

				hist_sig_shifted = combine_hists(
					sig_sample_list,
					sig_file_paths_shifted,
					hist_name,
					sig_weights
				) 

				hist_BR_unshifted = combine_hists(
					sample_list,
					BR_file_paths_unshifted,
					hist_name,
					BR_weights
				) 

				hist_BR_shifted = combine_hists(
					sample_list,
					BR_file_paths_shifted,
					hist_name,
					BR_weights
				) 


				if mass_point == "Suu4_chi1":
					hists = [(hist_sig_unshifted,hist_sig_shifted,"Signal","Signal"),(hist_BR_unshifted,hist_BR_shifted,"Combined BR","BR")] ## order is unshifted, shifted
				else:
					hists = [(hist_sig_unshifted,hist_sig_shifted,"Signal","Signal")] ## order is unshifted, shifted

				#### create plots
				for unshifted_hist, shifted_hist, title, short_title in hists:

					c1 = ROOT.TCanvas("","",1600,1200)
					c1.SetLogy(False)

					unshifted_hist.SetName(unshifted_hist.GetName() + "_unshifted")
					shifted_hist.SetName(shifted_hist.GetName() + "_shifted")

					max_val = max(unshifted_hist.GetMaximum(),shifted_hist.GetMaximum() )
					unshifted_hist.SetMaximum(1.2*max_val)
					shifted_hist.SetMaximum(1.2*max_val)

					shifted_hist.SetMinimum(1e-2)
					unshifted_hist.SetMinimum(1e-2)

					unshifted_hist.SetLineColor(ROOT.kBlack)
					shifted_hist.SetLineColor(ROOT.kRed)

					unshifted_hist.SetLineWidth(3)
					shifted_hist.SetLineWidth(3)

					if "Signal" in title:
						legend = ROOT.TLegend(0.15, 0.650, 0.3, 0.75)
					else:
						legend = ROOT.TLegend(0.15, 0.650, 0.3, 0.75)
					legend.AddEntry(unshifted_hist, "Unshifted %s"%(title), "l")
					legend.AddEntry(shifted_hist,   "Shifted %s"%(title), "l")

					legend.SetFillStyle(0)
					legend.SetBorderSize(0)


					unshifted_integral =  unshifted_hist.Integral()

					title_str = mass_point if "Signal" in title else title

					unshifted_hist.SetTitle("%s (Unshifted Mass) (%s) (%s)"%(unshifted_hist.GetTitle(), year, title_str))
					shifted_hist.SetTitle("%s (Shifted Mass) (%s) (%s)"%(unshifted_hist.GetTitle(), year, title_str))


					### do breit-wigner fits:
					max_hist_val = 5000 if "SJ_mass" in hist_type else 10000

					max_mass_unshifted = min(max_hist_val,unshifted_hist.GetMean() + 2.5* unshifted_hist.GetRMS() )
					max_mass_shifted  = min(max_hist_val,shifted_hist.GetMean() + 2.5* unshifted_hist.GetRMS() )

					min_mass_unshifted = max(0,unshifted_hist.GetMean() - 2.5* unshifted_hist.GetRMS() )
					min_mass_shifted = max(0,shifted_hist.GetMean() - 2.5* unshifted_hist.GetRMS() )

					bw_unshifted = ROOT.TF1(
						"bw_unshifted",
						"[0] * TMath::BreitWigner(x, [1], [2])",
						min_mass_unshifted, max_mass_unshifted
					)
					bw_unshifted.SetParameters(
						unshifted_hist.GetMaximum(),
						unshifted_hist.GetMean(), 
						unshifted_hist.GetRMS()   
					)
					unshifted_hist.Fit(bw_unshifted, "R")  

					bw_shifted = ROOT.TF1(
						"bw_shifted",
						"[0] * TMath::BreitWigner(x, [1], [2])",
						min_mass_shifted, max_mass_shifted
					)
					bw_shifted.SetParameters(
						shifted_hist.GetMaximum(), 
						shifted_hist.GetMean(),
						shifted_hist.GetRMS()
					)
					shifted_hist.Fit(bw_shifted, "R")  

					unshifted_hist.Draw("HIST")
					shifted_hist.Draw("HIST SAME")
					#bw_unshifted.Draw("SAME")
					#bw_shifted.Draw("SAME")

					# Custom text
					latex = ROOT.TLatex()
					latex.SetNDC(True)
					latex.SetTextSize(0.0175)

					latex.DrawLatex(0.333, 0.85, "Unshifted Hist")
					latex.DrawLatex(
						0.333, 0.815,
						"M = %.2f, RMS = %.2f GeV" % (
							#bw_unshifted.GetParameter(1),
							#bw_unshifted.GetParError(1)
							unshifted_hist.GetMean(),
							unshifted_hist.GetRMS()
						)
					)

					latex.DrawLatex(0.666, 0.85, "Shifted Hist")
					latex.DrawLatex(
						0.666, 0.815,
						"M = %.2f, RMS = %.2f GeV" % (
							#bw_shifted.GetParameter(1),
							#bw_shifted.GetParError(1)
							shifted_hist.GetMean(),
							shifted_hist.GetRMS()
						)
					)


					legend.Draw()


					c1.SaveAs("%s/%s_shifted_mass_%s_%s_%s.png"%(plot_dir, hist_type, mass_point,year,short_title))

					if first_page_1D:
						c1.SaveAs(output_pdf_1D + "[")
						first_page_1D = False

					c1.SaveAs(output_pdf_1D)


					shifted_integral   =  shifted_hist.Integral()

					c1.SetLogy(True)
					#unshifted_hist.SetTitle("Shifted / Unshifted Linearized Avg. SJ Mass vs DiSJ Mass for %s (%s) (%s)"%(title,mass_point,year))
					#shifted_hist.SetTitle("Shifted / Unshifted Linearized Avg. SJ Mass vs DiSJ Mass for %s (%s) (%s)"%(title,mass_point,year))

					unshifted_hist.SetTitle("Shifted / Unshifted " + unshifted_hist.GetTitle())
					shifted_hist.SetTitle(  "Shifted / Unshifted " + shifted_hist.GetTitle())

					#unshifted_hist.Draw("HIST")
					shifted_hist.Divide(unshifted_hist)
					shifted_hist.SetMaximum(1.2*shifted_hist.GetMaximum())
					shifted_hist.Draw("HIST")

					legend.Draw()

					text = ROOT.TText()
					text.SetNDC(True)  
					text.SetTextSize(0.025)
					text.DrawText(0.4, 0.85, "Unshifted Integral = %s"%(unshifted_integral))
					text.DrawText(0.4, 0.82, "Shifted Integral = %s"%( shifted_integral ))

					write_cms_text.write_cms_text(CMS_label_xpos=0.138, SIM_label_xpos=0.345,CMS_label_ypos = 0.925, SIM_label_ypos = 0.925, lumistuff_xpos=0.90, lumistuff_ypos=0.91, year = "", uses_data=True)

					c1.SaveAs("%s/%s_shifted_mass_comparison_%s_%s_%s.png"%(plot_dir, hist_type, mass_point,year,short_title))

					if first_page:
						c1.SaveAs(output_pdf + "[")
						first_page = False

					c1.SaveAs(output_pdf)
				
	c2 = ROOT.TCanvas("", "", 1200, 1200)
	if not first_page:
		c2.SaveAs(output_pdf + "]")
		print "All plots written to", output_pdf
	else:
		print "No plots created for", hist_name, ". PDF not generated."
	del c2  

	return

	c3 = ROOT.TCanvas("", "", 1200, 1200)
	if not first_page_1D:
		c3.SaveAs(output_pdf_1D + "]")
		print "All plots written to", output_pdf_1D
	else:
		print "No plots created for", hist_name, ". PDF not generated."
	del c3 

	return



if __name__=="__main__":
	compare_1D_shifted()
	compare_2D_shifted()
