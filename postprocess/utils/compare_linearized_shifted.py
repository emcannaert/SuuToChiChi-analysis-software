import ROOT 
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from write_cms_text import write_cms_text
import datetime
# makes a comparison of linarized shifted and unshifted signal and background.
# This is to see what is causing the limits so different between the two.


timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")




def compare_lin_shifted():


	plot_dir = "../plots/linearized_shift_comparisons/"


	output_pdf = os.path.join(plot_dir,  "shifted_vs_unshifted_linearized_%s.pdf"%timestamp)
	first_page = True


	years = ["2015","2016","2017","2018"]
	mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1","Suu5_chi1p5","Suu5_chi2","Suu6_chi1","Suu6_chi1p5",
	"Suu6_chi2","Suu6_chi2p5","Suu7_chi1", "Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3","Suu8_chi1","Suu8_chi1p5",
	"Suu8_chi2","Suu8_chi2p5","Suu8_chi3"]

	for year in years:
		for mass_point in mass_points:

			dir_unshifted = "../finalCombineFilesNewStats/QCDPT/correctedFinalCombineFiles/"
			dir_shifted  = "root://cmseos.fnal.gov//store/user/ecannaer/finalCombineFilesNewStats_shiftedMass_corrected/"

			file_name = "combine_%s_%s.root"%(year,mass_point)
			hist_folder = "SR/" # + hist type

			file_unshifted = ROOT.TFile.Open("%s/%s"%(dir_unshifted,file_name),"READ")
			file_shifted   = ROOT.TFile.Open("%s/%s"%(dir_shifted,file_name),"READ")

			hist_sig_unshifted = file_unshifted.Get("%s/sig_yuu2p0_yx2p0_WBBR0p5_HTBR0p25_ZTBR0p25"%(hist_folder))
			hist_sig_shifted   = file_shifted.Get("%s/sig_yuu2p0_yx2p0_WBBR0p5_HTBR0p25_ZTBR0p25"%(hist_folder))

			hist_BR_unshifted = file_unshifted.Get("%s/allBR"%(hist_folder))
			hist_BR_shifted   = file_shifted.Get("%s/allBR"%(hist_folder))


			if mass_point == "Suu4_chi1":
				hists = [(hist_sig_unshifted,hist_sig_shifted,"Signal","Signal"),(hist_BR_unshifted,hist_BR_shifted,"Combined BR","BR")] ## order is unshifted, shifted
			else:
				hists = [(hist_sig_unshifted,hist_sig_shifted,"Signal","Signal")] ## order is unshifted, shifted

			#### create plots
			for unshifted_hist, shifted_hist, title, short_title in hists:

				c1 = ROOT.TCanvas("","",1600,1200)

				max_val = max(unshifted_hist.GetMaximum(),shifted_hist.GetMaximum() )
				unshifted_hist.SetMaximum(max_val)
				shifted_hist.SetMaximum(max_val)

				unshifted_hist.SetLineColor(ROOT.kBlack)
				shifted_hist.SetLineColor(ROOT.kRed)

				unshifted_hist.SetLineWidth(3)
				shifted_hist.SetLineWidth(3)

				unshifted_hist.SetTitle("Shifted vs Unshifted Linearized Avg. SJ Mass vs DiSJ Mass for %s (%s) (%s)"%(title,mass_point,year))
				shifted_hist.SetTitle("Shifted vs Unshifted Linearized Avg. SJ Mass vs DiSJ Mass for %s (%s) (%s)"%(title,mass_point,year))

				if "Signal" in title:
					legend = ROOT.TLegend(0.22, 0.550, 0.48, 0.7)
				else:
					legend = ROOT.TLegend(0.62, 0.550, 0.88, 0.7)
				legend.AddEntry(unshifted_hist, "Unshifted %s"%(title), "l")
				legend.AddEntry(shifted_hist,   "Shifted %s"%(title), "l")


				unshifted_hist.Draw("HIST")
				shifted_hist.Draw("HIST SAME")

				legend.Draw()

				text = ROOT.TText()
				text.SetNDC(True)  
				text.SetTextSize(0.025)
				text.DrawText(0.4, 0.85, "Unshifted Integral = %s"%( unshifted_hist.Integral() ))
				text.DrawText(0.4, 0.82, "Shifted Integral = %s"%(shifted_hist.Integral() ))

				write_cms_text.write_cms_text(CMS_label_xpos=0.138, SIM_label_xpos=0.345,CMS_label_ypos = 0.925, SIM_label_ypos = 0.925, lumistuff_xpos=0.90, lumistuff_ypos=0.91, year = "", uses_data=True)

				c1.SaveAs("%s/linearized_shifted_mass_comparison_%s_%s_%s.png"%(plot_dir, mass_point,year,short_title))


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




if __name__=="__main__":
	compare_lin_shifted()



