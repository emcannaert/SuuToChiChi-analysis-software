
import sys,os,time
import numpy as np
import ROOT
from write_cms_text.write_cms_text import write_cms_text
from return_BR_SF.return_BR_SF import return_BR_SF
from combine_hists import combine_hists
import datetime

### Create plots comparing QCD superjet mass and disuperjet mass in the SR and CR regions
first_page = True
output_plot_path = "plots/SRCR_QCD_SJ_mass/"

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

output_pdf = os.path.join(output_plot_path, "QCD_SJ_mass_SRCR_comps_" +timestamp+ ".pdf")

def era_translator(year):
	if year == "2015": return "2016preAPV"
	elif year == "2016": return "2016postAPV"
	else: return year

def compare_SRCR_SJ_mass(year, hist_type ):   # year = year, hist_type = the name of the histogram to plot

	global first_page

	infile_path 	 = "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/"   # location of processed files 
	

	QCD_samples   = ["QCDMC_Pt_170to300","QCDMC_Pt_300to470","QCDMC_Pt_470to600","QCDMC_Pt_600to800","QCDMC_Pt_800to1000",
						 "QCDMC_Pt_1000to1400","QCDMC_Pt_1400to1800","QCDMC_Pt_1800to2400","QCDMC_Pt_2400to3200", "QCDMC_Pt_3200toInf" ]

	sample_lists = [ QCD_samples  ] # increasing order of yield for stack plot 

	BR_file_paths = [ { sample_type: "{}{}_{}_processed.root".format(infile_path,sample_type, year) for sample_type in sample_list } for sample_list in sample_lists	  ]
	BR_weights = [ { sample_type: return_BR_SF(year,sample_type.replace("-","_") ) for sample_type in sample_list}  for sample_list in sample_lists   ]
 
	hist_name = "nom/%s"%(hist_type)

	BR_hist_SR = combine_hists(
		sample_lists[0],
		BR_file_paths[0],
		hist_name + "_SR",
		hist_weights=BR_weights[0]
	) 

	BR_hist_CR = combine_hists(
		sample_lists[0],
		BR_file_paths[0],
		hist_name + "_CR",
		hist_weights=BR_weights[0]
	) 

	legend = ROOT.TLegend(0.70, 0.45, 0.85, 0.65)
	legend.SetNColumns(2)

	BR_hist_SR.Scale(1.0/BR_hist_SR.Integral())
	BR_hist_SR.SetMinimum(1e-4)
	BR_hist_SR.SetLineColor(ROOT.kBlue)
	legend.AddEntry(BR_hist_SR, "SR", "l")

	BR_hist_CR.Scale(1.0/BR_hist_CR.Integral())
	BR_hist_CR.SetMinimum(1e-4)
	BR_hist_CR.SetLineColor(ROOT.kRed+1)
	legend.AddEntry(BR_hist_CR, "CR", "l")

	#### create ratio plot and do the hist drawing

	c = ROOT.TCanvas("c", "c", 1200, 1200)
	if BR_hist_SR and BR_hist_CR:

		c.SetRightMargin(0.15)
		
		# Create a canvas and pads for upper and lower plots
		pad1 = ROOT.TPad("pad1", "Top pad", 0, 0.33, 1, 1.0)
		pad2 = ROOT.TPad("pad2", "Bottom pad", 0, 0.0, 1, 0.290)
		
		# Adjust margins
		pad1.SetTopMargin(0.1)  
		pad1.SetBottomMargin(0.01)  # Space between the top and bottom pad
		pad2.SetTopMargin(0.00)
		pad2.SetBottomMargin(0.4)  # Increase for better spacing in bottom pad

		pad1.Draw()
		pad2.Draw()

		# Draw the stack and h2 on the upper pad
		pad1.cd()
		pad1.SetLogy()

		# Determine which histogram has a larger maximum
		max_value = max( BR_hist_SR.GetMaximum(), BR_hist_CR.GetMaximum() )

		BR_hist_SR.SetLineWidth(4)

		plot_str = "Disuperjet Mass" if "disuper" in hist_name else "Average Superjet Mass"

		BR_hist_SR.SetTitle("%s SR-to-CR Shape Comparison (%s)"%(plot_str,year))

		BR_hist_SR.Draw("HIST")

		BR_hist_CR.SetLineWidth(4)
		BR_hist_CR.Draw("HIST,SAME")

		c.Update()

		# Draw the ratio on the lower pad
		pad2.cd()

		hRatio = BR_hist_SR.Clone("hRatio_data")

		hRatio.SetTitle("")
		hRatio.SetLineColor(ROOT.kBlack)
		hRatio.Divide( BR_hist_CR)  # Compute the ratio h2 / hStackTotal
		hRatio.GetYaxis().SetTitle(r"SR MC Shape / CR MC Shape")

		hRatio.GetYaxis().SetTitleSize(0.04)
		hRatio.GetYaxis().SetTitleOffset(1.0)
		hRatio.GetYaxis().SetLabelSize(0.08)
		hRatio.GetXaxis().SetTitleSize(0.12)
		hRatio.GetXaxis().SetLabelSize(0.1)

		hRatio.SetMinimum(0.05)
		hRatio.SetMaximum(3.0)

		hRatio.Draw()

		x_min = hRatio.GetXaxis().GetXmin()
		x_max = hRatio.GetXaxis().GetXmax()

		### create ratio lines at 0.8, 1.0, 1.2
		nom_line = ROOT.TLine(x_min, 1.0, x_max, 1.0)
		nom_line.SetLineStyle(1)  
		nom_line.Draw("same")

		nom_line_up = ROOT.TLine(x_min, 1.2, x_max, 1.2)
		nom_line_up.SetLineStyle(2)  # Dotted line style
		nom_line_up.Draw("same")


		nom_line_down = ROOT.TLine(x_min, 0.8, x_max, 0.8)
		nom_line_down.SetLineStyle(2)  # Dotted line style
		nom_line_down.Draw("same")


		# Add legend and TLatex text
		pad1.cd()



		legend.SetLineColor(0)
		legend.SetBorderSize(0)

		legend.Draw()

		obj_str = "Events"  #if "disuper" in hist_name else "Superjets"

		pad2.Update()
		c.Update()

		type_str = ""

		# Define the text
		text = ROOT.TLatex()
		text.SetTextSize(0.052)
		text.SetTextFont(62)
		text.SetTextAlign(22)  # Center alignment (horizontal and vertical)
		text.DrawLatexNDC(0.75, 0.80, "Era: %s"%(era_translator(year))) 
		text.DrawLatexNDC(0.75, 0.76, "Normalized") 

		write_cms_text(CMS_label_xpos=0.138, SIM_label_xpos=0.305,CMS_label_ypos = 0.925, SIM_label_ypos = 0.925, lumistuff_xpos=0.90, lumistuff_ypos=0.91, year = "", uses_data=True)
		png_path = os.path.join(output_plot_path, "QCD_" + hist_type + "_SRCR_shape_comp_%s.png"%year)

		c.SaveAs(png_path)

		if first_page:
			c.SaveAs(output_pdf + "[")
			first_page = False

		c.SaveAs(output_pdf)

	else:
		print("ERROR: invalid histograms.")
	del c 


if __name__ == "__main__":

	years = ["2015","2016","2017","2018"]

	hist_names = [ "h_SJ_mass", "h_disuperjet_mass" ]


	for year in years:
		for iii,hist_name in enumerate(hist_names):
			compare_SRCR_SJ_mass(year, hist_name )

c2 = ROOT.TCanvas("", "", 1200, 1200)
if not first_page:
    c2.SaveAs(output_pdf + "]")
    print "All plots written to", output_pdf
else:
    print "No plots created for", hist_name, ". PDF not generated."
del c2  

