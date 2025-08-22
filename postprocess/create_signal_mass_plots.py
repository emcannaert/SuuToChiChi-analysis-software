import sys, os
import ROOT

sys.path.append('../postprocess/')

from write_cms_text import write_cms_text
from return_signal_SF import return_signal_SF
import math
## (1) make plots of (1D) superjet mass, (1D) disuperjet mass, and (2D) average superjet vs disuperjet mass for some mass points for each year

## (2) make stack plots of signal for all different decays (SJ mass, diSJ mass, 2D mass)

## (3) make superimpose of signal and BR for SJ mass, diSJ mass, and 2D mass

bad_files = []
import ROOT
#ROOT.gErrorIgnoreLevel = ROOT.kError;
ROOT.gStyle.SetPalette(ROOT.kViridis)
ROOT.TColor.InvertPalette();

def take_square_root(hist):
    n_bins = hist.GetNbinsX()  # Get the number of bins along the X-axis

    for bin in range(1, n_bins + 1):
		content = hist.GetBinContent(bin)  # Get the content of the bin
		if content >= 0:  # Ensure the content is non-negative
		    hist.SetBinContent(bin, math.sqrt(content))  # Set the square root of the content
		else:
		    print("Warning: Negative bin content in bin %s"%(bin))

def make_BR_sig_superimposed( year, mass_point,tagging_type, tagging_str, hist_name, region, runEOS=False ):

	CMS_label_pos = 0.152;
	SIM_label_pos = 0.295;

	year_str = year
	if year == "2015": year_str = "2016preAPV"
	elif year == "2016": year_str = "2016postAPV"

	inFile_dir = "../combinedROOT/processedFiles/"
	if runEOS: inFile_dir = "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/"

	if "SB" in region:
		inFile_dir = "../combinedROOT/sideband_processedFiles/"
	plot_dir   = "plots/signal_mass_plots/sig_BR_ratios/"

	decays = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]
	folder_name = "nom/"

	mass_point_str = {
	    "Suu4_chi1": "M_{S_{uu}}= 4 TeV, M_{\\chi}=1 TeV", 
	    "Suu4_chi1p5": "M_{S_{uu}}= 4 TeV, M_{\\chi}=1.5 TeV", 
	    "Suu5_chi1": "M_{S_{uu}}= 5 TeV, M_{\\chi}=1 TeV", 
	    "Suu5_chi1p5": "M_{S_{uu}}= 5 TeV, M_{\\chi}=1.5 TeV", 
	    "Suu5_chi2": "M_{S_{uu}}= 5 TeV, M_{\\chi}=2 TeV", 
	    "Suu6_chi1": "M_{S_{uu}}= 6 TeV, M_{\\chi}=1 TeV", 
	    "Suu6_chi1p5": "M_{S_{uu}}= 6 TeV, M_{\\chi}=1.5 TeV", 
	    "Suu6_chi2": "M_{S_{uu}}= 6 TeV, M_{\\chi}=2 TeV", 
	    "Suu6_chi2p5": "M_{S_{uu}}= 6 TeV, M_{\\chi}=2.5 TeV", 
	    "Suu7_chi1": "M_{S_{uu}}= 7 TeV, M_{\\chi}=1 TeV", 
	    "Suu7_chi1p5": "M_{S_{uu}}= 7 TeV, M_{\\chi}=1.5 TeV", 
	    "Suu7_chi2": "M_{S_{uu}}= 7 TeV, M_{\\chi}=2 TeV", 
	    "Suu7_chi2p5": "M_{S_{uu}}= 7 TeV, M_{\\chi}=2.5 TeV", 
	    "Suu7_chi3": "M_{S_{uu}}= 7 TeV, M_{\\chi}=3 TeV", 
	    "Suu8_chi1": "M_{S_{uu}}= 8 TeV, M_{\\chi}=1 TeV", 
	    "Suu8_chi1p5": "M_{S_{uu}}= 8 TeV, M_{\\chi}=1.5 TeV", 
	    "Suu8_chi2": "M_{S_{uu}}= 8 TeV, M_{\\chi}=2 TeV", 
	    "Suu8_chi2p5": "M_{S_{uu}}= 8 TeV, M_{\\chi}=2.5 TeV", 
	    "Suu8_chi3": "M_{S_{uu}}= 8 TeV, M_{\\chi}=3 TeV"
	}

	hist_path = folder_name+ hist_name + tagging_type + "_" + region
	print("Looking for histogram %s"%hist_path)

	ROOT.TH1.AddDirectory(False)

	sig_hist = None

	for iii in range(0,len(decays)):
		inFileName2 = inFile_dir + "%s_%s_%s_processed.root"%(mass_point,decays[iii],year)
		#print("Looking for %s"%inFileName2)
		decay_SF = return_signal_SF.return_signal_SF(year,mass_point,decays[iii])

		try:
			f2 = ROOT.TFile.Open(inFileName2,"r")
			if sig_hist == None:
				#try to open file, get histogram and set this as the first hist
				sig_hist = f2.Get(hist_path).Clone()
				sig_hist.Scale(decay_SF)

			else:
				h2_sig = f2.Get(hist_path).Clone()
				h2_sig.SetDirectory(0)   # histograms lose their references when the file destructor is called
				h2_sig.Scale(decay_SF)
				sig_hist.Add(h2_sig.Clone())

		except: 
			print("ERROR: Failed finding histogram %s in file %s for %s/%s/%s/%s"%(hist_path,decays[iii], mass_point,year,region,tagging_str))
			if inFileName2 not in bad_files: bad_files.append(inFileName2)




	# Create the title using \mbox to separate math and text
	title = r"\mbox{Avg. SJ mass for Signal and Combined Backgrounds } (%s) \mbox{ (%s) } \mbox{(%s) } \mbox{(%s)}; Mass [GeV]; Events / 125 GeV" % (mass_point_str[mass_point], year_str, region, tagging_str.replace("_", "\\_"))

	# Check for specific histogram names and adjust titles as needed
	if "h_disuperjet_mass" in hist_name: title = r" \mbox{disuperjet mass for Signal and Combined Backgrounds } (%s) \mbox{ (%s) } \mbox{(%s) } \mbox{(%s) }; Mass [GeV]; Events / 200 GeV" % (mass_point_str[mass_point], year_str, region, tagging_str.replace("_", "\\_"))
	elif "h_MSJ_mass_vs_MdSJ" in hist_name: title = r"\mbox{Avg. SJ vs diSJ mass for Signal and Combined Backgrounds } (%s) \mbox{ (%s) } \mbox{(%s)} \mbox{(%s)}; disuperjet mass [GeV]; superjet mass [GeV]" % (mass_point_str[mass_point], year_str, region, tagging_str.replace("_", "\\_"))
	##### sig_hist now has all decays added together and is fully scaled


	##### get the MC files for this year 
	QCDMC1000to1500_filename = inFile_dir+ "QCDMC1000to1500"+ "_" + year + "_processed.root"
	QCDMC1500to2000_filename = inFile_dir+"QCDMC1500to2000"+ "_" + year + "_processed.root"
	QCDMC2000toInf_filename  = inFile_dir+"QCDMC2000toInf"+ "_" + year + "_processed.root"
	TTJetsMCHT1200to2500_filename = inFile_dir+"TTJetsMCHT1200to2500"+ "_" + year + "_processed.root"
	TTJetsMCHT2500toInf_filename = inFile_dir+"TTJetsMCHT2500toInf"+ "_" + year + "_processed.root"
	ST_t_channel_top_5f_filename = inFile_dir+"ST_t-channel-top_inclMC"+ "_" + year + "_processed.root"
	ST_t_channel_antitop_5f_filename = inFile_dir+"ST_t-channel-antitop_inclMC"+ "_" + year + "_processed.root"
	ST_s_channel_4f_hadrons_filename = inFile_dir+"ST_s-channel-hadronsMC"+ "_" + year + "_processed.root"
	ST_s_channel_4f_leptons_filename = inFile_dir+"ST_s-channel-leptonsMC"+ "_" + year + "_processed.root"
	ST_tW_antitop_5f_filename = inFile_dir+"ST_tW-antiTop_inclMC"+ "_" + year + "_processed.root"
	ST_tW_top_5f_filename = inFile_dir+"ST_tW-top_inclMC"+ "_" + year + "_processed.root"

	ST_t_channel_top_5f_SF 		= {'2015':0.0409963154,  '2016':0.03607115071, '2017':0.03494669125, '2018': 0.03859114659 }
	ST_t_channel_antitop_5f_SF	= {'2015':0.05673857623, '2016':0.04102705994, '2017':0.04238814865, '2018': 0.03606630944 }
	ST_s_channel_4f_hadrons_SF	= {'2015':0.04668187234, '2016':0.03564988679, '2017':0.03985938616, '2018': 0.04102795437 }
	ST_s_channel_4f_leptons_SF	= {'2015':0.01323030083, '2016':0.01149139097, '2017':0.01117527734, '2018': 0.01155448784 }
	ST_tW_antitop_5f_SF			= {'2015':0.2967888696,  '2016':0.2301666797,  '2017':0.2556495594,  '2018': 0.2700032391  }
	ST_tW_top_5f_SF				= {'2015':0.2962796522,  '2016':0.2355829386,  '2017':0.2563403788,  '2018': 0.2625270613  }

	SF_TTJetsMCHT1200to2500 = {"2015":0.002722324842,"2016":0.002255554525,"2017":0.00267594799,"2018":0.003918532089}
	SF_TTJetsMCHT2500toInf = {"2015":0.000056798633,"2016":0.000050253843,"2017":0.00005947217,"2018":0.000084089656}	

	SF_1000to1500 = {'2015': 1.578683216 ,   '2016':1.482632755 ,  '2017': 3.126481451,  '2018': 4.289571744   }
	SF_1500to2000 = {'2015': 0.2119142341,   '2016':0.195224041 ,  '2017': 0.3197450474, '2018': 0.4947703875  }
	SF_2000toInf  = {'2015': 0.08568186031 , '2016':0.07572795371, '2017': 0.14306915,   '2018': 0.2132134533  }

	QCDMC1000to1500_file= ROOT.TFile.Open(QCDMC1000to1500_filename, "READ")
	QCDMC1500to2000_file = ROOT.TFile.Open(QCDMC1500to2000_filename, "READ")
	QCDMC2000toInf_file  = ROOT.TFile.Open(QCDMC2000toInf_filename, "READ")

	TTJetsMCHT1200to2500_file  = ROOT.TFile.Open(TTJetsMCHT1200to2500_filename, "READ")
	TTJetsMCHT2500toInf_file   = ROOT.TFile.Open(TTJetsMCHT2500toInf_filename, "READ")

	ST_t_channel_top_5f_file  	   = ROOT.TFile.Open(ST_t_channel_top_5f_filename, "READ")
	ST_t_channel_antitop_5f_file   = ROOT.TFile.Open(ST_t_channel_antitop_5f_filename, "READ")
	ST_s_channel_4f_hadrons_file   = ROOT.TFile.Open(ST_s_channel_4f_hadrons_filename, "READ")
	ST_s_channel_4f_leptons_file   = ROOT.TFile.Open(ST_s_channel_4f_leptons_filename, "READ")
	ST_tW_antitop_5f_file  		= ROOT.TFile.Open(ST_tW_antitop_5f_filename, "READ")
	ST_tW_top_5f_file   		= ROOT.TFile.Open(ST_tW_top_5f_filename, "READ")

	QCDMC1000to1500_hist		  = QCDMC1000to1500_file.Get( hist_path  )
	QCDMC1500to2000_hist		  = QCDMC1500to2000_file.Get( hist_path  )
	QCDMC2000toInf_hist		   = QCDMC2000toInf_file.Get( hist_path  )
	TTJetsMCHT1200to2500_hist	 = TTJetsMCHT1200to2500_file.Get( hist_path  )
	TTJetsMCHT2500toInf_hist	  = TTJetsMCHT2500toInf_file.Get( hist_path  )
	ST_t_channel_top_5f__hist 	  = ST_t_channel_top_5f_file.Get( hist_path  )
	ST_t_channel_antitop_5f_hist  = ST_t_channel_antitop_5f_file.Get( hist_path  )
	ST_s_channel_4f_hadrons_hist  = ST_s_channel_4f_hadrons_file.Get( hist_path  )
	ST_s_channel_4f_leptons_hist = ST_s_channel_4f_leptons_file.Get( hist_path  )
	ST_tW_antitop_5f_hist 		  = ST_tW_antitop_5f_file.Get( hist_path  )
	ST_tW_top_5f_hist 			  = ST_tW_top_5f_file.Get( hist_path  )


	QCDMC1000to1500_hist.Scale(SF_1000to1500[year])
	QCDMC1500to2000_hist.Scale(SF_1500to2000[year])
	QCDMC2000toInf_hist.Scale(SF_2000toInf[year])
	TTJetsMCHT1200to2500_hist.Scale(SF_TTJetsMCHT1200to2500[year])
	TTJetsMCHT2500toInf_hist.Scale(SF_TTJetsMCHT2500toInf[year])
	ST_t_channel_top_5f__hist.Scale(ST_t_channel_top_5f_SF[year])
	ST_t_channel_antitop_5f_hist.Scale(ST_t_channel_antitop_5f_SF[year])
	ST_s_channel_4f_hadrons_hist.Scale(ST_s_channel_4f_hadrons_SF[year])
	ST_s_channel_4f_leptons_hist.Scale(ST_s_channel_4f_leptons_SF[year])
	ST_tW_antitop_5f_hist.Scale(ST_tW_antitop_5f_SF[year])
	ST_tW_top_5f_hist.Scale(ST_tW_top_5f_SF[year])
	
	colors = [ ROOT.TColor.GetColor(87, 144, 252), ROOT.TColor.GetColor(248, 156, 32), ROOT.TColor.GetColor(228, 37, 54), ROOT.TColor.GetColor(150, 74, 139), ROOT.TColor.GetColor(156, 156, 161), ROOT.TColor.GetColor(122, 33, 221)] 

	# combine backgrounds
	QCD_combined = QCDMC1000to1500_hist.Clone()
	QCD_combined.SetName("QCD_combined")
	QCD_combined.SetTitle("Combined QCD MC Background")
	QCD_combined.Add(QCDMC1500to2000_hist)
	QCD_combined.Add(QCDMC2000toInf_hist)
	QCD_combined.SetFillColor(colors[2])

	TTbar_combined = TTJetsMCHT1200to2500_hist.Clone()
	TTbar_combined.SetName("TTbar_combined")
	TTbar_combined.SetTitle("Combined TTbar MC Background")
	TTbar_combined.Add(TTJetsMCHT2500toInf_hist)
	TTbar_combined.SetFillColor(colors[0])

	ST_combined = ST_t_channel_top_5f__hist.Clone()
	ST_combined.SetName("ST_combined")
	ST_combined.SetTitle("Combined ST")
	ST_combined.Add(ST_t_channel_antitop_5f_hist)
	ST_combined.Add(ST_s_channel_4f_hadrons_hist)
	ST_combined.Add(ST_s_channel_4f_leptons_hist)
	ST_combined.Add(ST_tW_antitop_5f_hist)
	ST_combined.Add(ST_tW_top_5f_hist)
	ST_combined.SetFillColor(colors[1])

	canvas = ROOT.TCanvas("canvas", "Canvas with pads", 1200, 1000)



	BR_combined = QCD_combined.Clone()
	BR_combined.SetName("BR_combined")
	BR_combined.SetTitle(title)

	### for creating the ratio plot in the bottom pad showing sig / (sig + BR)
	h_ratio = sig_hist.Clone()
	h_ratio_denom = BR_combined.Clone()
	take_square_root(h_ratio_denom)
	#h_ratio_denom.Add(sig_hist)

	h_ratio.Divide(h_ratio_denom)

	BR_strs = ["Single Top", r"t\bar{t}", "QCD"]

	if "h_MSJ_mass_vs_MdSJ" in hist_name:
		# don't want to make a stack plot
		h_ratio.SetStats(0)
		h_ratio.Draw("colz") 

	else:



		upper_pad = ROOT.TPad("upper_pad", "upper_pad", 0, 0.3, 1, 1)
		lower_pad = ROOT.TPad("lower_pad", "lower_pad", 0, 0, 1, 0.275)
		

		upper_pad.SetLogy()

		upper_pad.SetBottomMargin(0.02)
		lower_pad.SetTopMargin(0.02)
		lower_pad.SetBottomMargin(0.3)
		
		upper_pad.Draw()
		lower_pad.Draw()

		### Backgrounds have been scaled, now create stack plot for BRs
		BR_stack = ROOT.THStack( "BR_stack", "%s"%(title))
		BR_stack.Add(ST_combined)
		BR_stack.Add(TTbar_combined)
		BR_stack.Add(QCD_combined)


		BR_max = BR_combined.GetMaximum();
		sig_max = sig_hist.GetMaximum();
		upper_pad.cd()


		BR_stack.Draw("HIST")
		BR_stack.GetXaxis().SetLabelSize(0)  # Hide x-axis labels in upper plot
		BR_stack.GetYaxis().SetTitleSize(0.04)
		BR_stack.GetYaxis().SetTitleOffset(1.4)
		if sig_max > BR_max:
			BR_stack.SetMaximum(1.2*sig_max)

		sig_hist.SetLineColor(ROOT.kBlack)
		sig_hist.SetLineStyle(2) ## dotted line
		sig_hist.SetLineWidth(6)
		sig_hist.Draw("SAME HIST")



		# Create and draw legend
		legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
		legend.AddEntry(sig_hist, mass_point_str[mass_point], "l")
		for i, hist in enumerate(BR_stack):
			legend.AddEntry(hist, BR_strs[i], "f")
		legend.Draw()

		# Draw lower pad (ratio plot)
		lower_pad.cd()
		
		h_ratio.SetStats(0)
		h_ratio.SetLineColor(ROOT.kBlack)
		h_ratio.SetLineWidth(2)
		h_ratio.SetTitle("")
		h_ratio.GetXaxis().SetTitleSize(0.1)
		h_ratio.GetXaxis().SetLabelSize(0.1)
		h_ratio.GetYaxis().SetTitle("Signal / #sqrt{BR}")
		h_ratio.GetYaxis().SetTitleSize(0.08)
		h_ratio.GetYaxis().SetTitleOffset(0.4)
		h_ratio.GetYaxis().SetLabelSize(0.08)
		h_ratio.SetMinimum(0)
		#h_ratio.SetMaximum(2)
		h_ratio.Draw("E")

		# Draw horizontal line at 1 on the ratio plot
		line = ROOT.TLine(h_ratio.GetXaxis().GetXmin(), 1, h_ratio.GetXaxis().GetXmax(), 1)
		line.SetLineColor(ROOT.kRed)
		line.SetLineStyle(2)
		line.Draw()

		# Update and show canvas
		canvas.Update()
		canvas.Draw()

	canvas.SaveAs(plot_dir + hist_name + "_" + mass_point + tagging_type + "_" +  region + "_" + year + ".png" )

	return





# end make_BR_sig_superimposed


#### for a given year type, Suu mass, and tagging type, create a plot of ALL relevant chi decay masses on one canvas
def create_superimposed_SJ_mass_plot_combined(year, MSuu, tagging_type, tagging_str, runEOS):

	regions  = ["SR","CR","AT1b","AT0b"]
	tagging_types = ["","_NN"]
	plot_types = ["h_SJ_mass","h_disuperjet_mass" ]
	decays = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]

	year_str = year
	if year == "2015": year_str = "2016preAPV"
	elif year == "2016": year_str = "2016postAPV"
	CMS_label_pos = 0.152;
	SIM_label_pos = 0.295;

	colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kCyan, ROOT.kOrange, ROOT.kViolet]

	inFile_dir = "../combinedROOT/processedFiles/"
	if runEOS: inFile_dir = "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/"

	plot_dir   = "plots/signal_mass_plots/all_signal_mass_superimposed/"
	
	#inFileName = inFile_dir + "%s_%s_%s_processed.root"%(mass_point,decays[0],year)

	c = ROOT.TCanvas("","", 1200,1000)
	#sig_file = ROOT.TFile.Open(inFileName,"READ")


	folder_name = "nom/"

	all_hists = []  # all histograms for a given year, decay, and mass point

	chi_masses = ["1","1p5"]
	if MSuu != "4":
		chi_masses.append("2")
		if MSuu != "5":
			chi_masses.append("2p5")
			if MSuu != "6":
				chi_masses.append("3")


	ROOT.TH1.AddDirectory(False)

	file_list = []
	for iii in range(0,len(decays)):      ### first index is the decay
		file_list.append([])
		for jjj,Mchi in enumerate(chi_masses):			  ### second index is the chi mass: [1, 1p5, 2, 2p5, 3]

			mass_point = "Suu%s_chi%s"%(MSuu,Mchi)
			inFileName2 = inFile_dir + "%s_%s_%s_processed.root"%(mass_point,decays[iii],year)
			file_list[iii].append(ROOT.TFile.Open(inFileName2,"r"))

	# this is going to be annoying, need to create another loop over all masses in the Mchi list

	for region in regions:  ## this should work, but otherwise can use normal indices 
		all_hists.append([])  #each region gets its own row where the columns are the ["h_SJ_mass","h_disuperjet_mass"] plots
		for plot_type in plot_types:
			all_hists[-1].append([])


			legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)  # Specify legend position (x1, y1, x2, y2)
			for jjj,Mchi in enumerate(chi_masses):

				### need to add together the histograms here 
				h1 = file_list[0][jjj].Get(folder_name+"%s%s_%s"%(plot_type, tagging_type, region) )
				#h1.Scale(return_signal_SF.return_signal_SF(year,mass_point,decays[0]))
				h1.SetDirectory(0)
				for iii in range(1,len(decays)):
					h2 = file_list[iii][jjj].Get(folder_name+"%s%s_%s"%(plot_type, tagging_type, region) )
					h2.Scale(return_signal_SF.return_signal_SF(year,mass_point,decays[iii]))
					h2.SetDirectory(0)
					h1.Add(h2)
				h1.SetLineWidth(6)
				#h1.Scale(sig_SF)
				h1.SetTitle("%s mass (allHad, %s, %s, %s, %s)"%(plot_type.split("_")[1] , r"#M_{S_{uu}}="+ "%s TeV#"%MSuu  ,year_str,tagging_str,region))
				all_hists[-1][-1].append(h1) # each plot type has two histograms: [ combined cutbased, combined NN ]

			## get the index of the tallest histogram
			max_val = -9999
			max_index = 9999
			for kkk,hist in enumerate(all_hists[-1][-1]):
				if hist.GetMaximum() > max_val:
					max_val = hist.GetMaximum()
					max_index = kkk
			all_hists[-1][-1][max_index].SetLineColor(colors[max_index])
			all_hists[-1][-1][max_index].Draw("HIST")
			legend.AddEntry(all_hists[-1][-1][max_index], r"#M_{S_{uu}}="+ "%s TeV#"%MSuu + r", M_{chi}="+ "%s TeV#"%(chi_masses[max_index]), "f")
			for kkk,hist in enumerate(all_hists[-1][-1]):
				if kkk != max_index:
					all_hists[-1][-1][kkk].SetLineColor(colors[kkk])
					hist.Draw("HIST,SAME")
					legend.AddEntry(all_hists[-1][-1][kkk], r"#M_{S_{uu}}=" + "%s TeV#"%MSuu + r", M_{chi}="+ "%s TeV#"%(chi_masses[kkk]), "f")

			legend.Draw()
			### do final nice plotting
			write_cms_text.write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.255,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)

			mass_point_str = "Suu%s"%(MSuu)
			c.SaveAs(plot_dir+"%s_allHad_%s_%s_%s%s_allChiMasses.png"%(plot_type,mass_point_str ,year, region, tagging_type))

	del all_hists
	del file_list
	return



# creates mass plot for a given year, mass point, tagging type for ALL decays.
def make_combined_plots( year, mass_point,tagging_type, tagging_str, runEOS = False ):

	CMS_label_pos = 0.152;
	SIM_label_pos = 0.295;

	year_str = year
	if year == "2015": year_str = "2016preAPV"
	elif year == "2016": year_str = "2016postAPV"

	inFile_dir = "../combinedROOT/processedFiles/"
	if runEOS: inFile_dir = "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/"
	plot_dir   = "plots/signal_mass_plots/combined_decays/"
	decays = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]
	folder_name = "nom/"
	c = ROOT.TCanvas("","", 1200,1000)

	inFileName = inFile_dir + "%s_%s_%s_processed.root"%(mass_point,decays[0],year)
	f1 = ROOT.TFile.Open(inFileName,"r")

	colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kCyan, ROOT.kOrange, ROOT.kViolet]

	print("Reading file %s."%inFileName)
	# init the 2D histograms (these won't become stack plots for obvious reasons)
	h_MSJ_mass_vs_MdSJ_SR 	= f1.Get(folder_name+"h_MSJ_mass_vs_MdSJ%s_SR"%tagging_type)
	h_MSJ_mass_vs_MdSJ_SR.Scale(return_signal_SF.return_signal_SF(year,mass_point,decays[0]))

	h_MSJ_mass_vs_MdSJ_CR  = f1.Get(folder_name+"h_MSJ_mass_vs_MdSJ%s_CR"%tagging_type)
	h_MSJ_mass_vs_MdSJ_CR.Scale(return_signal_SF.return_signal_SF(year,mass_point,decays[0]))

	h_MSJ_mass_vs_MdSJ_AT1b = f1.Get(folder_name+"h_MSJ_mass_vs_MdSJ%s_AT1b"%tagging_type)
	h_MSJ_mass_vs_MdSJ_AT1b.Scale(return_signal_SF.return_signal_SF(year,mass_point,decays[0]))

	h_MSJ_mass_vs_MdSJ_AT0b = f1.Get(folder_name+"h_MSJ_mass_vs_MdSJ%s_AT0b"%tagging_type)
	h_MSJ_mass_vs_MdSJ_AT0b.Scale(return_signal_SF.return_signal_SF(year,mass_point,decays[0]))



	# init stack plots
	h_SJ_mass_SR = ROOT.THStack( "h_SJ_mass_SR_stack", "SuuToChiChi signal superjet mass (combined) (%s) (%s) (SR) (%s); superjet mass [GeV]; events / 125 GeV"%(mass_point,year,tagging_str))
	h_disuperjet_mass_SR = ROOT.THStack( "h_disuperjet_mass_SR", "SuuToChiChi signal disuperjet mass (combined) (%s) (%s) (SR) (%s); disuperjet mass [GeV]; events / 200 GeV"%(mass_point,year,tagging_str));
	
	h_SJ_mass_CR = ROOT.THStack( "h_SJ_mass_CR", "SuuToChiChi signal superjet mass (combined) (%s) (%s) (CR) (%s); superjet mass [GeV]; events / 125 GeV"%(mass_point,year,tagging_str));
	h_disuperjet_mass_CR = ROOT.THStack( "h_disuperjet_mass_CR", "SuuToChiChi signal disuperjet mass (combined) (%s) (%s) (CR) (%s); disuperjet mass [GeV]; events / 200 GeV"%(mass_point,year,tagging_str));
	
	h_SJ_mass_AT1b = ROOT.THStack( "h_SJ_mass_AT1b","SuuToChiChi signal superjet mass (combined) (%s) (%s) (AT1B) (%s); superjet mass [GeV]; events / 125 GeV"%(mass_point,year,tagging_str));
	h_disuperjet_mass_AT1b = ROOT.THStack( "h_disuperjet_mass_AT1b", "SuuToChiChi signal disuperjet mass (combined) (%s) (%s) (AT1B) (%s); disuperjet mass [GeV]; events / 200 GeV"%(mass_point,year,tagging_str));

	h_SJ_mass_AT0b = ROOT.THStack( "h_SJ_mass_AT0b", "SuuToChiChi signal superjet mass (combined) (%s) (%s) (AT0b) (%s); superjet mass [GeV]; events / 125 GeV"%(mass_point,year,tagging_str));
	h_disuperjet_mass_AT0b = ROOT.THStack( "h_disuperjet_mass_AT0b", "SuuToChiChi signal disuperjet mass (combined) (%s) (%s) (AT0b) (%s); disuperjet mass [GeV]; events / 200 GeV"%(mass_point,year,tagging_str));


	legend_SJ_mass_SR 	= ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
	legend_diSJ_mass_SR = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
	legend_SJ_mass_CR 	= ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
	legend_diSJ_mass_CR = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
	legend_SJ_mass_AT1b = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
	legend_diSJ_mass_AT1b = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
	legend_SJ_mass_AT0b   = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
	legend_diSJ_mass_AT0b = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)




	print("Running year/mass_point/tagging_type/tagging_str:  %s/%s/%s/%s"%( year, mass_point,tagging_type, tagging_str) )
	for iii in range(0,len(decays)):

		CMS_label_xpos = 0.152
		SIM_label_xpos = 0.235
		CMS_label_ypos = 0.875
		SIM_label_ypos = 0.84

		decay_SF = return_signal_SF.return_signal_SF(year,mass_point,decays[iii])
		inFileName2 = inFile_dir + "%s_%s_%s_processed.root"%(mass_point,decays[iii],year)
		
		f2 = ROOT.TFile.Open(inFileName2,"r")

		if not f2 or not f2.IsOpen(): continue

		try:
			h2_SJ_mass_SR = f2.Get(folder_name+"h_SJ_mass%s_SR"%tagging_type).Clone()
			h2_disuperjet_mass_SR 	= f2.Get(folder_name+"h_disuperjet_mass%s_SR"%tagging_type).Clone()

			h2_SJ_mass_CR 			= f2.Get(folder_name+"h_SJ_mass%s_CR"%tagging_type).Clone()
			h2_disuperjet_mass_CR   = f2.Get(folder_name+"h_disuperjet_mass%s_CR"%tagging_type).Clone()

			h2_SJ_mass_AT1b 		 = f2.Get(folder_name+"h_SJ_mass%s_AT1b"%tagging_type).Clone()
			h2_disuperjet_mass_AT1b  = f2.Get(folder_name+"h_disuperjet_mass%s_AT1b"%tagging_type).Clone()

			h2_SJ_mass_AT0b 		 = f2.Get(folder_name+"h_SJ_mass%s_AT0b"%tagging_type).Clone()
			h2_disuperjet_mass_AT0b  = f2.Get(folder_name+"h_disuperjet_mass%s_AT0b"%tagging_type).Clone()
		except:
			print("failed for decay %s"%decays[iii])
			continue
		h2_SJ_mass_SR.SetDirectory(0)   # histograms lose their references when the file destructor is called
		h2_disuperjet_mass_SR.SetDirectory(0)
		h2_SJ_mass_CR.SetDirectory(0)
		h2_disuperjet_mass_CR.SetDirectory(0)
		h2_SJ_mass_AT1b.SetDirectory(0)
		h2_disuperjet_mass_AT1b.SetDirectory(0)
		h2_SJ_mass_AT0b.SetDirectory(0)
		h2_disuperjet_mass_AT0b.SetDirectory(0)

		if (iii > 0):   # only want to do this for files 2 and beyond 
			h_MSJ_mass_vs_MdSJ_SR_temp 	= f2.Get(folder_name+"h_MSJ_mass_vs_MdSJ%s_SR"%tagging_type)
			h_MSJ_mass_vs_MdSJ_CR_temp  = f2.Get(folder_name+"h_MSJ_mass_vs_MdSJ%s_CR"%tagging_type)
			h_MSJ_mass_vs_MdSJ_AT1b_temp = f2.Get(folder_name+"h_MSJ_mass_vs_MdSJ%s_AT1b"%tagging_type)
			h_MSJ_mass_vs_MdSJ_AT0b_temp = f2.Get(folder_name+"h_MSJ_mass_vs_MdSJ%s_AT0b"%tagging_type)
			h_MSJ_mass_vs_MdSJ_SR_temp.Scale(decay_SF)
			h_MSJ_mass_vs_MdSJ_CR_temp.Scale(decay_SF)
			h_MSJ_mass_vs_MdSJ_AT1b_temp.Scale(decay_SF)
			h_MSJ_mass_vs_MdSJ_AT0b_temp.Scale(decay_SF)
			h_MSJ_mass_vs_MdSJ_SR.Add(h_MSJ_mass_vs_MdSJ_SR_temp)
			h_MSJ_mass_vs_MdSJ_CR.Add(h_MSJ_mass_vs_MdSJ_CR_temp)
			h_MSJ_mass_vs_MdSJ_AT1b.Add(h_MSJ_mass_vs_MdSJ_AT1b_temp)
			h_MSJ_mass_vs_MdSJ_AT0b.Add(h_MSJ_mass_vs_MdSJ_AT0b_temp)

		ROOT.TH1.AddDirectory(False)

		h2_SJ_mass_SR.Scale(decay_SF)
		h2_SJ_mass_SR.SetFillColor(colors[iii])

		h2_disuperjet_mass_SR.Scale(decay_SF)
		h2_disuperjet_mass_SR.SetFillColor(colors[iii])

		h2_SJ_mass_CR.Scale(decay_SF)
		h2_SJ_mass_CR.SetFillColor(colors[iii])

		h2_disuperjet_mass_CR.Scale(decay_SF)
		h2_disuperjet_mass_CR.SetFillColor(colors[iii])

		h2_SJ_mass_AT1b.Scale(decay_SF)
		h2_SJ_mass_AT1b.SetFillColor(colors[iii])

		h2_disuperjet_mass_AT1b.Scale(decay_SF)
		h2_disuperjet_mass_AT1b.SetFillColor(colors[iii])

		h2_SJ_mass_AT0b.Scale(decay_SF)
		h2_SJ_mass_AT0b.SetFillColor(colors[iii])

		h2_disuperjet_mass_AT0b.Scale(decay_SF)
		h2_disuperjet_mass_AT0b.SetFillColor(colors[iii])
		


		h_SJ_mass_SR.Add(h2_SJ_mass_SR.Clone())
		h_disuperjet_mass_SR.Add(h2_disuperjet_mass_SR.Clone())
		
		h_SJ_mass_CR.Add(h2_SJ_mass_CR.Clone())
		h_disuperjet_mass_CR.Add(h2_disuperjet_mass_CR.Clone())
	
		h_SJ_mass_AT1b.Add(h2_SJ_mass_AT1b.Clone())
		h_disuperjet_mass_AT1b.Add(h2_disuperjet_mass_AT1b.Clone())
		
		h_SJ_mass_AT0b.Add(h2_SJ_mass_AT0b.Clone())
		h_disuperjet_mass_AT0b.Add(h2_disuperjet_mass_AT0b.Clone())


	if h_MSJ_mass_vs_MdSJ_SR: print("For signal mass %s in the %s for year %s, there %s events expected."%(mass_point,"SR",  year, h_MSJ_mass_vs_MdSJ_SR.Integral()))
	if h_MSJ_mass_vs_MdSJ_CR: print("For signal mass %s in the %s for year %s, there %s events expected."%(mass_point,"CR",  year, h_MSJ_mass_vs_MdSJ_CR.Integral()))
	if h_MSJ_mass_vs_MdSJ_AT1b: print("For signal mass %s in the %s for year %s, there %s events expected."%(mass_point,"AT1b",  year, h_MSJ_mass_vs_MdSJ_AT1b.Integral()))
	if h_MSJ_mass_vs_MdSJ_AT0b: print("For signal mass %s in the %s for year %s, there %s events expected."%(mass_point,"AT0b",  year, h_MSJ_mass_vs_MdSJ_AT0b.Integral()))


	## create legends 
	hist_list1 =	h_SJ_mass_SR.GetHists()
	hist_list2 =	h_disuperjet_mass_SR.GetHists()
	hist_list3 =	h_SJ_mass_CR.GetHists()
	hist_list4 =	h_disuperjet_mass_CR.GetHists()
	hist_list5 =	h_SJ_mass_AT1b.GetHists()
	hist_list6 =	h_disuperjet_mass_AT1b.GetHists()
	hist_list7 =	h_SJ_mass_AT0b.GetHists()
	hist_list8 =	h_disuperjet_mass_AT0b.GetHists()
	for iii in range(0,len(hist_list1)):
		legend_SJ_mass_SR.AddEntry(hist_list1[iii], decays[iii], "f")
		legend_diSJ_mass_SR.AddEntry(hist_list2[iii], decays[iii], "f")
		legend_SJ_mass_CR.AddEntry(hist_list3[iii], decays[iii], "f")
		legend_diSJ_mass_CR.AddEntry(hist_list4[iii], decays[iii], "f")
		legend_SJ_mass_AT1b.AddEntry(hist_list5[iii], decays[iii], "f")
		legend_diSJ_mass_AT1b.AddEntry(hist_list6[iii], decays[iii], "f")
		legend_SJ_mass_AT0b.AddEntry(hist_list7[iii], decays[iii], "f")
		legend_diSJ_mass_AT0b.AddEntry(hist_list8[iii], decays[iii], "f")


	mass_point_str = {
	    "Suu4_chi1": "M_{S_{uu}} = 4 TeV, M_{\\chi}=1 TeV", 
	    "Suu4_chi1p5": "M_{S_{uu}} = 4 TeV, M_{\\chi}=1.5 TeV", 
	    "Suu5_chi1": "M_{S_{uu}}= 5 TeV, M_{\\chi}=1 TeV", 
	    "Suu5_chi1p5": "M_{S_{uu}} = 5 TeV, M_{\\chi}=1.5 TeV", 
	    "Suu5_chi2": "M_{S_{uu}} = 5 TeV, M_{\\chi}=2 TeV", 
	    "Suu6_chi1": "M_{S_{uu}} = 6 TeV, M_{\\chi}=1 TeV", 
	    "Suu6_chi1p5": "M_{S_{uu}} = 6 TeV, M_{\\chi}=1.5 TeV", 
	    "Suu6_chi2": "M_{S_{uu}} = 6 TeV, M_{\\chi}=2 TeV", 
	    "Suu6_chi2p5": "M_{S_{uu}} = 6 TeV, M_{\\chi}=2.5 TeV", 
	    "Suu7_chi1": "M_{S_{uu}} = 7 TeV, M_{\\chi}=1 TeV", 
	    "Suu7_chi1p5": "M_{S_{uu}} = 7 TeV, M_{\\chi}=1.5 TeV", 
	    "Suu7_chi2": "M_{S_{uu}} = 7 TeV, M_{\\chi}=2 TeV", 
	    "Suu7_chi2p5": "M_{S_{uu}} = 7 TeV, M_{\\chi}=2.5 TeV", 
	    "Suu7_chi3": "M_{S_{uu}} = 7 TeV, M_{\\chi}=3 TeV", 
	    "Suu8_chi1": "M_{S_{uu}} = 8 TeV, M_{\\chi}=1 TeV", 
	    "Suu8_chi1p5": "M_{S_{uu}} = 8 TeV, M_{\\chi}=1.5 TeV", 
	    "Suu8_chi2": "M_{S_{uu}} = 8 TeV, M_{\\chi}=2 TeV", 
	    "Suu8_chi2p5": "M_{S_{uu}} = 8 TeV, M_{\\chi}=2.5 TeV", 
	    "Suu8_chi3": "M_{S_{uu}} = 8 TeV, M_{\\chi}=3 TeV"
	}



	r"\mbox{Avg. SJ mass for Signal and Combined Backgrounds } (%s) \mbox{ (%s) } \mbox{(%s) } \mbox{(%s)}; Mass [GeV]; Events / 125 GeV"


	mass_point_str_to_use_ = mass_point_str[mass_point].split(",")
	Suu_mass = mass_point_str_to_use_[0].split("=")
	chi_mass = mass_point_str_to_use_[1].split("=")

	Suu_mass_point_str_to_use = Suu_mass[0] + " = "  +  r"\mbox{" + Suu_mass[1] + ",}"
	chi_mass_point_str_to_use = chi_mass[0] + " = "  +  r"\mbox{" + chi_mass[1] + "}"

	#title_SR = r"\mbox{Signal avg. SJ mass vs disuperjet mass} (%s) \mbox{ (%s) } \mbox{(%s) } \mbox{(%s)}; " % (mass_point_str_to_use, year_str, region, tagging_str.replace("_", "\\_"))
	#title_CR = r"\mbox{Signal avg. SJ mass vs disuperjet mass } (%s) \mbox{ (%s) } \mbox{(%s) } \mbox{(%s)};" % (mass_point_str_to_use, year_str, region, tagging_str.replace("_", "\\_"))
	#title_AT1b = r"\mbox{Signal SJ mass vs disuperjet mass of signal-tagged SJ } (%s) \mbox{ (%s) } \mbox{(%s) } \mbox{(%s)};" % (mass_point_str_to_use, year_str, region, tagging_str.replace("_", "\\_"))
	#title_AT0b = r"\mbox{Signal SJ mass vs disuperjet mass of signal-tagged SJ } (%s) \mbox{ (%s) } \mbox{(%s) } \mbox{(%s)};" % (mass_point_str_to_use, year_str, region, tagging_str.replace("_", "\\_"))


	title_SR   = " Avg. SJ mass vs disuperjet mass for signal (%s) (SR) (%s)"%(year_str,tagging_str)
	title_CR   = "Avg. SJ mass vs disuperjet mass for signal (%s) (CR) (%s)"%(year_str,tagging_str)
	title_AT1b = "SJ mass vs disuperjet mass of tagged SJ for signal (%s) (AT1b) (%s)"%(year_str,tagging_str)
	title_AT0b = "SJ mass vs disuperjet mass of tagged SJ for signal (%s) (AT0b) (%s)"%(year_str,tagging_str)


	# Define the text
	text = ROOT.TLatex()
	text.SetTextSize(0.04)
	text.SetTextFont(62)
	text.SetTextAlign(22)  # Center alignment (horizontal and vertical)
	

	h_MSJ_mass_vs_MdSJ_SR.SetTitle(title_SR) #"Signal avg. SJ mass vs disuperjet mass (%s) (%s) (SR) (%s)"%(mass_point_str_to_use,year_str,tagging_str)
	h_MSJ_mass_vs_MdSJ_CR.SetTitle(title_CR) #"Signal avg. SJ mass vs disuperjet mass (%s) (%s) (CR) (%s)"%(mass_point_str_to_use,year_str,tagging_str)
	h_MSJ_mass_vs_MdSJ_AT1b.SetTitle(title_AT1b) # "Signal SJ mass vs disuperjet mass of signal-tagged SJ (%s) (%s) (AT1b) (%s)"%(mass_point_str_to_use,year_str,tagging_str)
	h_MSJ_mass_vs_MdSJ_AT0b.SetTitle(title_AT0b)  # "Signal SJ mass vs disuperjet mass of signal-tagged SJ (%s) (%s) (AT0b) (%s)"%(mass_point_str_to_use,year_str,tagging_str)

	h_MSJ_mass_vs_MdSJ_SR.GetZaxis().SetTitle("Events")
	h_MSJ_mass_vs_MdSJ_SR.GetZaxis().SetTitleOffset(1.35)
	h_MSJ_mass_vs_MdSJ_SR.GetZaxis().SetTitleSize(0.035)
	h_MSJ_mass_vs_MdSJ_SR.GetZaxis().SetLabelSize(0.035)
	h_MSJ_mass_vs_MdSJ_SR.GetZaxis().SetLabelOffset(0.005)

	h_MSJ_mass_vs_MdSJ_CR.GetZaxis().SetTitle("Events")
	h_MSJ_mass_vs_MdSJ_CR.GetZaxis().SetTitleOffset(1.35)
	h_MSJ_mass_vs_MdSJ_CR.GetZaxis().SetTitleSize(0.035)
	h_MSJ_mass_vs_MdSJ_CR.GetZaxis().SetLabelSize(0.035)
	h_MSJ_mass_vs_MdSJ_CR.GetZaxis().SetLabelOffset(0.005)

	h_MSJ_mass_vs_MdSJ_AT1b.GetZaxis().SetTitle("Events")
	h_MSJ_mass_vs_MdSJ_AT1b.GetZaxis().SetTitleOffset(1.35)
	h_MSJ_mass_vs_MdSJ_AT1b.GetZaxis().SetTitleSize(0.035)
	h_MSJ_mass_vs_MdSJ_AT1b.GetZaxis().SetLabelSize(0.035)
	h_MSJ_mass_vs_MdSJ_AT1b.GetZaxis().SetLabelOffset(0.005)

	h_MSJ_mass_vs_MdSJ_AT0b.GetZaxis().SetTitle("Events")
	h_MSJ_mass_vs_MdSJ_AT0b.GetZaxis().SetTitleOffset(1.35)
	h_MSJ_mass_vs_MdSJ_AT0b.GetZaxis().SetTitleSize(0.035)
	h_MSJ_mass_vs_MdSJ_AT0b.GetZaxis().SetLabelSize(0.035)
	h_MSJ_mass_vs_MdSJ_AT0b.GetZaxis().SetLabelOffset(0.005)



	h_MSJ_mass_vs_MdSJ_SR.GetYaxis().SetTitle(h_MSJ_mass_vs_MdSJ_SR.GetYaxis().GetTitle() + " [GeV]")
	h_MSJ_mass_vs_MdSJ_CR.GetYaxis().SetTitle(h_MSJ_mass_vs_MdSJ_CR.GetYaxis().GetTitle() + " [GeV]")
	h_MSJ_mass_vs_MdSJ_AT1b.GetYaxis().SetTitle(h_MSJ_mass_vs_MdSJ_AT1b.GetYaxis().GetTitle() + " [GeV]")
	h_MSJ_mass_vs_MdSJ_AT0b.GetYaxis().SetTitle(h_MSJ_mass_vs_MdSJ_AT0b.GetYaxis().GetTitle() + " [GeV]")


	c.SetRightMargin(0.05)

	h_SJ_mass_SR.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos, SIM_label_xpos,CMS_label_ypos, SIM_label_ypos, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	legend_SJ_mass_SR.Draw()
	c.SaveAs(plot_dir+"h_SJ_mass_%s_allHadDecays_%s_SR%s.png"%(mass_point,year,tagging_type))

	h_disuperjet_mass_SR.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos, SIM_label_xpos,CMS_label_ypos, SIM_label_ypos, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	legend_diSJ_mass_SR.Draw()
	c.SaveAs(plot_dir+"h_disuperjet_mass_%s_allHadDecays_%s_SR%s.png"%(mass_point,year,tagging_type))


	h_SJ_mass_CR.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos, SIM_label_xpos,CMS_label_ypos, SIM_label_ypos, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	legend_SJ_mass_CR.Draw()
	c.SaveAs(plot_dir+"h_SJ_mass_%s_allHadDecays_%s_CR%s.png"%(mass_point,year,tagging_type))

	h_disuperjet_mass_CR.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos, SIM_label_xpos,CMS_label_ypos, SIM_label_ypos, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	legend_diSJ_mass_CR.Draw()
	c.SaveAs(plot_dir+"h_disuperjet_mass_%s_allHadDecays_%s_CR%s.png"%(mass_point,year,tagging_type))


	h_SJ_mass_AT1b.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos, SIM_label_xpos,CMS_label_ypos, SIM_label_ypos, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	legend_SJ_mass_AT1b.Draw()
	c.SaveAs(plot_dir+"h_SJ_mass_%s_allHadDecays_%s_AT1b%s.png"%(mass_point,year,tagging_type))

	h_disuperjet_mass_AT1b.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos, SIM_label_xpos,CMS_label_ypos, SIM_label_ypos, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	legend_diSJ_mass_AT1b.Draw()
	c.SaveAs(plot_dir+"h_disuperjet_mass_%s_allHadDecays_%s_AT1b%s.png"%(mass_point,year,tagging_type))


	h_SJ_mass_AT0b.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos, SIM_label_xpos,CMS_label_ypos, SIM_label_ypos, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	legend_SJ_mass_AT0b.Draw()
	c.SaveAs(plot_dir+"h_SJ_mass_%s_allHadDecays_%s_AT0b%s.png"%(mass_point,year,tagging_type))

	h_disuperjet_mass_AT0b.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos, SIM_label_xpos,CMS_label_ypos, SIM_label_ypos, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	legend_diSJ_mass_AT0b.Draw()
	c.SaveAs(plot_dir+"h_disuperjet_mass_%s_allHadDecays_%s_AT0b%s.png"%(mass_point,year,tagging_type))


	c.SetRightMargin(0.16)

	h_MSJ_mass_vs_MdSJ_SR.GetYaxis().SetTitleOffset(1.5)
	h_MSJ_mass_vs_MdSJ_SR.Draw("colz")
	write_cms_text.write_cms_text(CMS_label_xpos, SIM_label_xpos,CMS_label_ypos, SIM_label_ypos, lumistuff_xpos=0.84, lumistuff_ypos=0.91, year = "", uses_data=False)
	text.DrawLatexNDC(0.235, 0.75, Suu_mass_point_str_to_use)
	text.DrawLatexNDC(0.235, 0.70, chi_mass_point_str_to_use)
	c.Update()
	c.SaveAs(plot_dir+"h_MSJ_mass_vs_MdSJ_%s_allHadDecays_%s_SR%s.png"%(mass_point,year,tagging_type))

	h_MSJ_mass_vs_MdSJ_CR.GetYaxis().SetTitleOffset(1.5)
	h_MSJ_mass_vs_MdSJ_CR.Draw("colz")
	write_cms_text.write_cms_text(CMS_label_xpos, SIM_label_xpos,CMS_label_ypos, SIM_label_ypos, lumistuff_xpos=0.84, lumistuff_ypos=0.91, year = "", uses_data=False)
	text.DrawLatexNDC(0.235, 0.75, Suu_mass_point_str_to_use)
	text.DrawLatexNDC(0.235, 0.70, chi_mass_point_str_to_use)
	c.Update()
	c.SaveAs(plot_dir+"h_MSJ_mass_vs_MdSJ_%s_allHadDecays_%s_CR%s.png"%(mass_point,year,tagging_type))

	h_MSJ_mass_vs_MdSJ_AT1b.GetYaxis().SetTitleOffset(1.5)
	h_MSJ_mass_vs_MdSJ_AT1b.Draw("colz")
	write_cms_text.write_cms_text(CMS_label_xpos, SIM_label_xpos,CMS_label_ypos, SIM_label_ypos, lumistuff_xpos=0.84, lumistuff_ypos=0.91, year = "", uses_data=False)
	text.DrawLatexNDC(0.235, 0.75, Suu_mass_point_str_to_use)
	text.DrawLatexNDC(0.235, 0.70, chi_mass_point_str_to_use)
	c.Update()
	c.SaveAs(plot_dir+"h_MSJ_mass_vs_MdSJ_%s_allHadDecays_%s_AT1b%s.png"%(mass_point,year,tagging_type))

	h_MSJ_mass_vs_MdSJ_AT0b.GetYaxis().SetTitleOffset(1.5)
	h_MSJ_mass_vs_MdSJ_AT0b.Draw("colz")
	write_cms_text.write_cms_text(CMS_label_xpos, SIM_label_xpos,CMS_label_ypos, SIM_label_ypos, lumistuff_xpos=0.84, lumistuff_ypos=0.91, year = "", uses_data=False)
	text.DrawLatexNDC(0.235, 0.75, Suu_mass_point_str_to_use)
	text.DrawLatexNDC(0.235, 0.70, chi_mass_point_str_to_use)
	c.Update()
	c.SaveAs(plot_dir+"h_MSJ_mass_vs_MdSJ_%s_allHadDecays_%s_AT0b%s.png"%(mass_point,year,tagging_type))

	return
	



#### this seems to create signal plots (in all regions) for a given year AND a given decay. Decays are plotted separately (probably won't use this )
def make_plots(inFileName, year,decay,mass_point, tagging_type, tagging_str):


	CMS_label_pos = 0.152;
	SIM_label_pos = 0.295;

	plot_dir   = "plots/signal_mass_plots/separate_decays/"
	c = ROOT.TCanvas("","", 1200,1000)
	print("Getting root file %s"%inFileName)
	sig_file = ROOT.TFile.Open(inFileName,"READ")
	folder_name = "nom/"

	year_str = year
	if year == "2015": year_str = "2016preAPV"
	elif year == "2016": year_str = "2016postAPV"

	h_SJ_mass_SR 					= sig_file.Get(folder_name+"h_SJ_mass%s_SR"%tagging_type)
	h_diSJ_mass_SR 					= sig_file.Get(folder_name+"h_disuperjet_mass%s_SR"%tagging_type)
	h_MSJ_mass_vs_MdSJ_SR		 	= sig_file.Get(folder_name+"h_MSJ_mass_vs_MdSJ%s_SR"%tagging_type)

	h_SJ_mass_CR 					= sig_file.Get(folder_name+"h_SJ_mass%s_CR"%tagging_type)
	h_diSJ_mass_CR 					= sig_file.Get(folder_name+"h_disuperjet_mass%s_CR"%tagging_type)
	h_MSJ_mass_vs_MdSJ_CR		 	= sig_file.Get(folder_name+"h_MSJ_mass_vs_MdSJ%s_CR"%tagging_type)

	h_SJ_mass_AT1b 						= sig_file.Get(folder_name+"h_SJ_mass%s_AT1b"%tagging_type)
	h_diSJ_mass_AT1b 					= sig_file.Get(folder_name+"h_disuperjet_mass%s_AT1b"%tagging_type)
	h_MSJ_mass_vs_MdSJ_AT1b		 	= sig_file.Get(folder_name+"h_MSJ_mass_vs_MdSJ%s_AT1b"%tagging_type)

	h_SJ_mass_AT0b 						= sig_file.Get(folder_name+"h_SJ_mass%s_AT0b"%tagging_type)
	h_diSJ_mass_AT0b 					= sig_file.Get(folder_name+"h_disuperjet_mass%s_AT0b"%tagging_type)

	print("Getting histograms from root file: %s"%(folder_name+"h_MSJ_mass_vs_MdSJ%sAT0b"%tagging_type))

	h_MSJ_mass_vs_MdSJ_AT0b		 	= sig_file.Get(folder_name+"h_MSJ_mass_vs_MdSJ%s_AT0b"%tagging_type)

	h_totHT 							= sig_file.Get(folder_name+"h_totHT")

	_____
	# scale all histograms 
	sig_SF = return_signal_SF.return_signal_SF(year,mass_point,decay)

	h_SJ_mass_SR.Scale(sig_SF)
	h_diSJ_mass_SR.Scale(sig_SF)
	h_MSJ_mass_vs_MdSJ_SR.Scale(sig_SF)
	h_SJ_mass_CR.Scale(sig_SF)
	h_diSJ_mass_CR.Scale(sig_SF)
	h_MSJ_mass_vs_MdSJ_CR.Scale(sig_SF)
	h_SJ_mass_AT1b.Scale(sig_SF)
	h_diSJ_mass_AT1b.Scale(sig_SF)
	h_MSJ_mass_vs_MdSJ_AT1b.Scale(sig_SF)
	h_SJ_mass_AT0b.Scale(sig_SF)
	h_diSJ_mass_AT0b.Scale(sig_SF)
	h_MSJ_mass_vs_MdSJ_AT0b.Scale(sig_SF)
	h_totHT.Scale(sig_SF)

	h_SJ_mass_SR.SetTitle("Superjet mass (%s, %s, %s, %s, SR)"%(decay,mass_point,year_str,tagging_str))
	h_diSJ_mass_SR.SetTitle("disuperjet mass (%s, %s, %s, %s, SR)"%(decay,mass_point,year_str,tagging_str))
	h_MSJ_mass_vs_MdSJ_SR.SetTitle("avg. superjet mass vs disuperjet mass (%s, %s, %s, %s, SR)"%(decay,mass_point,year_str,tagging_str))

	h_SJ_mass_CR.SetTitle("Superjet mass (%s, %s, %s, %s, CR)"%(decay,mass_point,year_str,tagging_str))
	h_diSJ_mass_CR.SetTitle("disuperjet mass (%s, %s, %s, %s, CR)"%(decay,mass_point,year_str,tagging_str))
	h_MSJ_mass_vs_MdSJ_CR.SetTitle("avg. superjet mass vs disuperjet mass (%s, %s, %s, %s, CR)"%(decay,mass_point,year_str,tagging_str))

	h_SJ_mass_AT1b.SetTitle("Superjet mass (%s, %s, %s, %s, AT1b)"%(decay,mass_point,year_str,tagging_str))
	h_diSJ_mass_AT1b.SetTitle("disuperjet mass (%s, %s, %s, %s, AT1b)"%(decay,mass_point,year_str,tagging_str))
	h_MSJ_mass_vs_MdSJ_AT1b.SetTitle("tagged superjet mass vs disuperjet mass (%s, %s, %s, %s, AT1b)"%(decay,mass_point,year_str,tagging_str))

	h_SJ_mass_AT0b.SetTitle("Superjet mass (%s, %s, %s, %s, AT0b)"%(decay,mass_point,year_str,tagging_str))
	h_diSJ_mass_AT0b.SetTitle("disuperjet mass (%s, %s, %s, %s, AT0b)"%(decay,mass_point,year_str,tagging_str))
	h_MSJ_mass_vs_MdSJ_AT0b.SetTitle("tagged superjet mass vs disuperjet mass (%s, %s, %s, %s, AT0b)"%(decay,mass_point,year_str,tagging_str))

	h_totHT.SetTitle("Tot HT (%s, %s, %s)"%(decay,mass_point,year_str))
	write_cms_text.write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.255,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	h_totHT.Draw("HIST")
	c.SaveAs(plot_dir+"h_totHT_%s_%s_%s.png"%(decay,mass_point,year))

	h_SJ_mass_SR.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.255,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	c.SaveAs(plot_dir+"h_SJ_mass_%s_%s_%s_SR%s.png"%(decay,mass_point,year,tagging_type)) 
	h_diSJ_mass_SR.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.255,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	c.SaveAs(plot_dir+"h_diSJ_mass_%s_%s_%s_SR%s.png"%(decay,mass_point,year,tagging_type))
	h_MSJ_mass_vs_MdSJ_SR.Draw("colz")
	write_cms_text.write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.255,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	c.SaveAs(plot_dir+"h_SJ_mass_vs_diSJ_mass_%s_%s_%s_SR%s.png"%(decay,mass_point,year,tagging_type))


	h_SJ_mass_CR.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.255,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	c.SaveAs(plot_dir+"h_SJ_mass_%s_%s_%s_CR%s.png"%(decay,mass_point,year,tagging_type))
	h_diSJ_mass_CR.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.255,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	c.SaveAs(plot_dir+"h_diSJ_mass_%s_%s_%s_CR%s.png"%(decay,mass_point,year,tagging_type))
	h_MSJ_mass_vs_MdSJ_CR.Draw("colz")
	write_cms_text.write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.255,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	c.SaveAs(plot_dir+"h_SJ_mass_vs_diSJ_mass_%s_%s_%s_CR%s.png"%(decay,mass_point,year,tagging_type))


	h_SJ_mass_AT1b.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.255,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	c.SaveAs(plot_dir+"h_SJ_mass_%s_%s_%s_AT1b%s.png"%(decay,mass_point,year,tagging_type))
	h_diSJ_mass_AT1b.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.255,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	c.SaveAs(plot_dir+"h_diSJ_mass_%s_%s_%s_AT1b%s.png"%(decay,mass_point,year,tagging_type))
	h_MSJ_mass_vs_MdSJ_AT1b.Draw("colz")
	write_cms_text.write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.255,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	c.SaveAs(plot_dir+"h_SJ_mass_vs_diSJ_mass_%s_%s_%s_AT1b%s.png"%(decay,mass_point,year,tagging_type))

	h_SJ_mass_AT0b.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.255,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	c.SaveAs(plot_dir+"h_SJ_mass_%s_%s_%s_AT0b%s.png"%(decay,mass_point,year,tagging_type))
	h_diSJ_mass_AT0b.Draw("HIST")
	write_cms_text.write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.255,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	c.SaveAs(plot_dir+"h_diSJ_mass_%s_%s_%s_AT0b%s.png"%(decay,mass_point,year,tagging_type))
	h_MSJ_mass_vs_MdSJ_AT0b.Draw("colz")
	write_cms_text.write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.255,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
	c.SaveAs(plot_dir+"h_SJ_mass_vs_diSJ_mass_%s_%s_%s_AT0b%s.png"%(decay,mass_point,year,tagging_type))



#for each Suu mass, create a plot that contains all superjet/ disuperjet masses for that mass point ## this is done per year and per chi mass point 
#for each Suu/chi mass point, create a plot comparing the cut-based and NN-based superjet/disuperjet mass   # this can be done for each year and mass point
		## make these plots for both combined and separate decays
	return
if __name__=="__main__":
	runEOS = True
	debug  = False 
	years = ["2015","2016","2017","2018"]
	decays = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]
	#mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1", "Suu5_chi1p5", "Suu5_chi2", "Suu6_chi1","Suu6_chi1p5", "Suu6_chi2", "Suu6_chi2p5", "Suu7_chi1","Suu7_chi1p5","Suu7_chi2", "Suu7_chi2p5", "Suu7_chi3","Suu8_chi1", "Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3" ]   ## copy this from the LPC 

	mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1", "Suu5_chi1p5", "Suu5_chi2", "Suu6_chi1",  "Suu6_chi1p5", "Suu6_chi2", "Suu6_chi2p5", "Suu7_chi1", "Suu7_chi2", "Suu7_chi2p5",  "Suu8_chi1", "Suu8_chi2", "Suu8_chi3" ]   ## use smaller list so you don't crash pc

	Suu_masses = ["4","5","6","7","8"]
	#### need to change this to open up the processed files
						#cutbased  NN 
	tagging_types = [ "", "_NN"]  # "_NN"]
	tagging_str  = ["cut-based", "NN-based"] #, "NN tagger"]

	hist_names = ["h_SJ_mass", "h_disuperjet_mass", "h_MSJ_mass_vs_MdSJ"]
	regions    = ["SR","CR","AT1b","AT0b"]

	if debug: 
		years = ["2015"]
		mass_points = ["Suu4_chi1"]
		tagging_types = [""]


	for year in years:
		for mass_point in mass_points:

			# uncomment this out when you have the NN tagging up and running
			
			#try:
			#	make_cutbased_NN_comparison_plots_combined(year, mass_point)
			#except:
			#	print("Failed making combined tagging plots.")
			
			for iii, tagging_type in enumerate(tagging_types):


				# create superimposed sig / BR plots
				for hist_name in hist_names:
					for region in regions:
						make_BR_sig_superimposed( year, mass_point,tagging_type, tagging_str[iii], hist_name, region , runEOS)
 
				# create combined Suu mass plots (all decay modes)
				#try:
				make_combined_plots(year, mass_point, tagging_type, tagging_str[iii],runEOS ) 
				#except:
				#	print("ERROR: Failed to create the combined plot for %s + %s"%(mass_point,year))
				

		"""
		#uncomment this out when testing is done
		for MSuu in Suu_masses:   # create the superimposed SJ mass plots for multiple mass points
			for iii, tagging_type in enumerate(tagging_types):

				try:
					create_superimposed_SJ_mass_plot_combined(year, MSuu, tagging_type, tagging_str[iii] ) 
				except:
					print("ERROR: failed create_superimposed_SJ_mass_plot_combined with %s/%s/%s/%s"%(year, MSuu, tagging_type, tagging_str[iii], runEOS))

		"""
	bad_files_file = open('files_create_signal_mass_plots_did_not_find.txt','w')
	for bad_file in bad_files:
		bad_files_file.write("%s\n"%bad_file)
	bad_files_file.close()
	
