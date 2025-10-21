import ROOT
import os
from return_BR_SF.return_BR_SF import return_BR_SF
from return_signal_SF.return_signal_SF import return_signal_SF
from write_cms_text import write_cms_text
import numpy as np
import argparse
import datetime
ROOT.gROOT.SetBatch(True)


##### creates comparisons of the b-tagging efficiency as a function of AK4 jet pt 

def make_plots(file_dir,output_dir, masks): # split_BRs

	year_translator = {"2015":"2016preAPV", "2016":"2016postAPV","2017":"2017","2018":"2018"}
	sig_decays 		= ["WBWB","ZTZT","HTHT","WBHT","WBZT","HTZT"]
	sig_mass_points = ["Suu4_chi1","Suu6_chi2","Suu8_chi3"]

	legend_translator = {"ST_":"Single Top", "TTJets":r"t \bar{t}","WJets":"W+Jets","QCD":"QCD"}

	hist_types = ["b","c","Light"]

	if not file_dir:
		file_dir	=  "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/"

	years = ["2015", "2016", "2017", "2018"]

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	color_hexes = [
		"#D73027",  # Deep Red
		"#1A9850",  # Emerald Green
		"#A6D96A",  # Light Cyan
		"#762A83",  # Deep Violet
		"#FEE08B",  # Golden Yellow
		"#3288BD",  # Ocean Blue
		"#F46D43",  # Coral Pink



		"#C51B7D",  # Mauve Pink

		"#FC8D59",  # Bright Orange
		"#D9EF8B",  # Light Olive
		"#91CF60",  # Teal Green
		"#66BD63",  # Sky Blue
		"#9E0142",  # Soft Purple
		"#666666",  # Slate Gray
		"#5E4FA2",  # Cool Blue
		"#006837",  # Forest Green

		# Additional 10 hex colors
		"#E31A1C",  # Crimson Red
		"#FF7F00",  # Vivid Orange
		"#FDBF6F",  # Pale Orange
		"#CAB2D6",  # Lavender
		"#6A3D9A",  # Grape Purple
		"#A6CEE3",  # Light Blue
		"#1F78B4",  # Medium Blue
		"#33A02C",  # Lime Green
		"#B2DF8A",  # Mint Green
	]

	colors = [ROOT.TColor.GetColor(hex_code) for hex_code in color_hexes]

	BR_samples = ["ST_s-channel-hadronsMC",
	"ST_s-channel-leptonsMC",
	"ST_t-channel-antitop_inclMC",
	"ST_t-channel-top_inclMC",
	"ST_tW-antiTop_inclMC",
	"ST_tW-top_inclMC",
	"WJetsMC_LNu-HT1200to2500",
	"WJetsMC_LNu-HT2500toInf",
	 "WJetsMC_LNu-HT800to1200",
	"WJetsMC_QQ-HT800toInf",
	"TTJetsMCHT800to1200",
	"TTJetsMCHT1200to2500",
	"TTJetsMCHT2500toInf",
	#  "TTToLeptonicMC",
	# "TTToSemiLeptonicMC",
	# "TTToHadronicMC",
	#"QCDMC1000to1500",
	#"QCDMC1500to2000",
	#"QCDMC2000toInf"

	"QCDMC_Pt_170to300",
	"QCDMC_Pt_300to470",
	"QCDMC_Pt_470to600",
	"QCDMC_Pt_600to800",
	"QCDMC_Pt_800to1000",
	"QCDMC_Pt_1000to1400",
	"QCDMC_Pt_1400to1800",
	"QCDMC_Pt_1800to2400",
	"QCDMC_Pt_2400to3200",
	"QCDMC_Pt_3200toInf"

	] 

	group_colors = {"ST_":0, "WJets":1, "TTJets":2, "QCD":3, "Suu4_chi1":4,"Suu6_chi2":5,"Suu8_chi3":6}


	for sig_mass_point in sig_mass_points:
		for sig_decay in sig_decays:
			BR_samples.append(sig_mass_point + "_" + sig_decay)

	timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

	output_pdf = os.path.join(output_dir, "btagging_efficiency_"+timestamp+ ".pdf")
	first_page = True

	for hist_type in hist_types: 

		region = "preselected"

		cand_regions = ["AT1b","AT0b","CR","SR","ADT1b","ADT0b"]

		hist_name_num   = "h_true%s_jets_med_b_tagged_by_pt"%hist_type
		hist_name_denom = "h_true%s_jets_by_pt"%hist_type

		## try to interpret the region from the hist name
		for cand_region in cand_regions:
			if cand_region in hist_name_num: 
				region = cand_region
				break

		print("For hist %s, interpreted region as %s."%(hist_name_num,region))


		for year in years:


			year_str = year
			if year == "2015": year_str = "2016preAPV"
			if year == "2016": year_str = "2016postAPV"

			BR_hists				= []
			BR_hists_denom			= []

			qcd_samples = {

				"ST_s-channel-hadronsMC": return_BR_SF(year, "ST_s-channel-hadronsMC".replace("-","_")),
				"ST_s-channel-leptonsMC": return_BR_SF(year, "ST_s-channel-leptonsMC".replace("-","_")),
				"ST_t-channel-antitop_inclMC": return_BR_SF(year, "ST_t-channel-antitop_inclMC".replace("-","_")),
				"ST_t-channel-top_inclMC": return_BR_SF(year, "ST_t-channel-top_inclMC".replace("-","_")),
				"ST_tW-antiTop_inclMC": return_BR_SF(year, "ST_tW-antiTop_inclMC".replace("-","_")),
				"ST_tW-top_inclMC": return_BR_SF(year, "ST_tW-top_inclMC".replace("-","_")),

				"WJetsMC_LNu-HT1200to2500": return_BR_SF(year, "WJetsMC_LNu-HT1200to2500".replace("-","_")),
				"WJetsMC_LNu-HT2500toInf": return_BR_SF(year, "WJetsMC_LNu-HT2500toInf".replace("-","_")),
				"WJetsMC_LNu-HT800to1200": return_BR_SF(year, "WJetsMC_LNu-HT800to1200".replace("-","_")),
				"WJetsMC_QQ-HT800toInf": return_BR_SF(year, "WJetsMC_QQ-HT800toInf".replace("-","_")) ,

				"TTJetsMCHT800to1200": return_BR_SF(year, "TTJetsMCHT800to1200"),
				"TTJetsMCHT1200to2500": return_BR_SF(year, "TTJetsMCHT1200to2500"),
				"TTJetsMCHT2500toInf": return_BR_SF(year, "TTJetsMCHT2500toInf"),

				"QCDMC1000to1500": return_BR_SF(year, "TTJetsMCHT1200to2500"),
				"QCDMC1500to2000": return_BR_SF(year, "QCD1500to2000"),
				"QCDMC2000toInf": return_BR_SF(year, "QCD2000toInf"),


				"QCDMC_Pt_170to300":   return_BR_SF(year, "QCDMC_Pt_170to300"),
				"QCDMC_Pt_300to470":	return_BR_SF(year, "QCDMC_Pt_300to470"),
				"QCDMC_Pt_470to600":	 return_BR_SF(year, "QCDMC_Pt_470to600"),
				"QCDMC_Pt_600to800":	return_BR_SF(year, "QCDMC_Pt_600to800"),
				"QCDMC_Pt_800to1000":   return_BR_SF(year, "QCDMC_Pt_800to1000"),
				"QCDMC_Pt_1000to1400":   return_BR_SF(year, "QCDMC_Pt_1000to1400"),
				"QCDMC_Pt_1400to1800":  return_BR_SF(year, "QCDMC_Pt_1400to1800"),
				"QCDMC_Pt_1800to2400":  return_BR_SF(year, "QCDMC_Pt_1800to2400"),
				"QCDMC_Pt_2400to3200":  return_BR_SF(year, "QCDMC_Pt_2400to3200"),
				"QCDMC_Pt_3200toInf":   return_BR_SF(year, "QCDMC_Pt_3200toInf")
		
			}

			for sig_mass_point in sig_mass_points:
				for sig_decay in sig_decays:
					qcd_samples[sig_mass_point + "_" + sig_decay] = return_signal_SF( year, sig_mass_point, sig_decay)

			#if split_BRs:
			#	BR_types = BR_samples
			#else: 
			BR_types = ["ST_", "WJets", "TTJets", "QCD", "Suu4_chi1","Suu6_chi2","Suu8_chi3" ]
			BR_groups = {BR_type: None for BR_type in BR_types}

			BR_groups_denom = {BR_type: None for BR_type in BR_types}

			for iii,sample in enumerate(BR_samples):
				scale = qcd_samples[sample]

				# find out which type of BR this is
				BR_type = ""
				for _BR_type in BR_types:
					if _BR_type in sample: 
						BR_type = _BR_type
						break


				file_name = sample + "_" + year + "_processed.root"
				file_path = os.path.join(file_dir, file_name)


				if not "cmseos" in file_dir:
					if not os.path.exists(file_path):
						print "  WARNING: File not found:", file_path
						continue

				f = ROOT.TFile.Open(file_path)
				if not f or f.IsZombie():
					print "  ERROR: Could not open:", file_path
					continue


				hist_num   = f.Get("nom/" + hist_name_num)
				hist_denom = f.Get("nom/" + hist_name_denom)

				if not hist_num:
					print "  ERROR: Histogram not found:", hist_name_num, "in", file_path
					f.Close()
					continue
				if not hist_denom:
					print "  ERROR: Histogram not found:", hist_denom, "in", file_path
					f.Close()
					continue


				hist_num.Scale(scale)
				hist_denom.Scale(scale)

				hist_num.SetDirectory(0)

				hist_num.SetTitle("True %s jet b-tagging efficiency (%s) (%s)"%(hist_type, year_translator[year], region))
				hist_num.GetXaxis().SetTitle("Jet p_{T} [GeV]" )
				hist_num.GetYaxis().SetTitle("Tagging Efficiency")


				#hist.SetMinimum(1e-2)
				#hist_num.SetFillColor(colors[iii])
				hist_num.SetLineColor(colors[group_colors[BR_type]])
				hist_num.SetLineWidth(3)
				hist_num.SetStats(0)

				if BR_groups[BR_type] is None:
					BR_groups[BR_type] = hist_num.Clone("combined_hist_%s"%BR_type)
					BR_groups[BR_type].SetDirectory(0)

					BR_groups_denom[BR_type] = hist_denom.Clone("combined_hist_%s_denom"%BR_type)
					BR_groups_denom[BR_type].SetDirectory(0)

				else:
					BR_groups[BR_type].Add(hist_num)
					BR_groups_denom[BR_type].Add(hist_denom)

				hist_num.SetDirectory(0)
				f.Close()


			found_samples = []
			# Now add these to a combined BR hist and the stack plot
			combined_hist_BR = None
			combined_hist_BR_denom = None

			


			## for each background, create the plot of b-tagging efficiency vs pt


			c = ROOT.TCanvas("c", "c", 1600, 1200)
			c.SetRightMargin(0.1)

			"""if split_BRs:
				legend = ROOT.TLegend(0.155, 0.70, 0.80, 0.88)
				legend.SetNColumns(4);  
				legend.SetTextSize(0.01) 
				legend.SetBorderSize(0)
				legend.SetFillStyle(0) """
			#else:
			if hist_type == "b": legend = ROOT.TLegend(0.2, 0.2, 0.35, 0.4)
			else: legend = ROOT.TLegend(0.2, 0.6, 0.40, 0.80)
			legend.SetBorderSize(0)
			legend.SetFillStyle(0)
			legend.SetFillColor(0)

			jjj = 0
			for BR_type in BR_types:



				hist 	   = BR_groups[BR_type]
				hist_denom = BR_groups_denom[BR_type]

				if not hist: 
					print("ERROR: Histogram not found: %s, %s, %s"%(BR_type,hist_name_num, year))
					continue

				if not hist_denom: 
					print("ERROR: Denom histogram not found: %s, %s, %s"%(BR_type,hist_name_num, year))
					continue


				hist.Divide(hist_denom)

				BR_hists.append(hist)
				found_samples.append(BR_type)


				if jjj == 0: 
					#print("hist is %s, title is %s"%(hist.GetName(),hist.GetTitle()))
					hist.Draw("HIST")
				else:
					hist.Draw("HIST,SAME")

				c.Update()


				jjj+=1


			#if not split_BRs:
			#	for kkk,found_sample in enumerate(found_samples):
			#		legend.AddEntry(BR_hists[kkk], legend_translator[found_sample], "f")
			for kkk,found_sample in enumerate(found_samples):
				legend.AddEntry(BR_hists[kkk], found_sample)

			legend.Draw()	

			write_cms_text.write_cms_text(CMS_label_xpos=0.138, SIM_label_xpos=0.33,CMS_label_ypos = 0.925, SIM_label_ypos = 0.925, lumistuff_xpos=0.90, lumistuff_ypos=0.91, year = "", uses_data=False)
			png_path = os.path.join(output_dir, "btaggingEffByPt_true" + hist_type + "_" + BR_type + "_" + year + "_"+ region + ".png")

			c.SaveAs(png_path)

			if first_page:
				c.SaveAs(output_pdf + "[")
				first_page = False

			c.SaveAs(output_pdf)

			del c 

	c2 = ROOT.TCanvas("", "", 1600, 1200)
	if not first_page:
		c2.SaveAs(output_pdf + "]")
		print "All plots written to", output_pdf
	else:
		print "No plots created for", hist_name_num, ". PDF not generated."
	del c2  



if __name__=="__main__":

	file_dir = None
	output_dir = "plots/btagging/"
	masks = None

	#parser = argparse.ArgumentParser(description="Parse input ROOT file and histogram names.")
	#parser.add_argument("--split_BRs",	 action="store_true" , help="Option to combine like backgrounds into processes.")

	#args = parser.parse_args()


	make_plots(file_dir, output_dir, masks ) #args.split_BRs



