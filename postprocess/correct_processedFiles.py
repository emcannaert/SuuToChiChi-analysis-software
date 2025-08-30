import ROOT
import sys,os
from math import sqrt
import ast
import random

#### operates on the final, linearized files that go to combine in order to fix asymmetrix uncertainties, mainly JECs
#### the "fixed" outputs are written to the postprocess/finalCombineFiles/correctedFinalCombineFiles/

ROOT.gErrorIgnoreLevel = ROOT.kWarning


useEOS  = True
infile_path  = "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/" if useEOS else "../combinedROOT/processedFiles/"
outfile_path = "root://cmseos.fnal.gov//store/user/ecannaer/processedFilesCorrected/" if useEOS else "../combinedROOT/processedFilesCorrected/"


def create_directories(dirs_to_create):

	for dir_to_create in dirs_to_create:
		if not os.path.exists(dir_to_create):
			os.makedirs(dir_to_create)

def neighbor_average(hist, i, j):
	neighbors = []
	for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
		nb = hist.GetBinContent(i+dx, j+dy)
		if nb > 0:
			neighbors.append(nb)
	return sum(neighbors)/len(neighbors) if neighbors else hist.GetBinContent(i,j)
									
def regularize_down_hist(var_down, var_nom, threshold=0.5):
	new_down = var_down.Clone(var_down.GetName()) #+"_reg"
	nx, ny = new_down.GetNbinsX(), new_down.GetNbinsY()

	for i in range(1, nx+1):
		for j in range(1, ny+1):
			nom = var_nom.GetBinContent(i, j)
			if nom < 1e-10:  # skip empty bins
				continue

			var = var_down.GetBinContent(i, j)
			frac_var = (var - nom)/nom

			# collect neighbor fractional variations
			neighbors = []
			for (ii, jj) in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
				if ii < 1 or ii > nx or jj < 1 or jj > ny: 
					continue
				nom_nb = var_nom.GetBinContent(ii, jj)
				if nom_nb < 1e-10: 
					continue
				var_nb = var_down.GetBinContent(ii, jj)
				neighbors.append((var_nb - nom_nb)/nom_nb)

			if not neighbors:
				continue

			avg_frac = sum(neighbors)/len(neighbors)

			# check if this bin is an outlier
			if abs(frac_var - avg_frac) > threshold:
				new_val = nom * (1 + avg_frac)
				new_down.SetBinContent(i, j, new_val)
	new_down.SetDirectory(0)
	return new_down
def regularize_up_hist(var_up, var_nom, threshold=0.5):
	new_up = var_up.Clone(var_up.GetName()) #+"_reg"
	nx, ny = new_up.GetNbinsX(), new_up.GetNbinsY()

	for i in range(1, nx+1):
		for j in range(1, ny+1):
			nom = var_nom.GetBinContent(i, j)
			if nom < 1e-10:  # skip empty bins
				continue

			var = var_up.GetBinContent(i, j)
			frac_var = (var - nom)/nom

			# collect neighbor fractional variations
			neighbors = []
			for (ii, jj) in [(i-1,j), (i+1,j), (i,j-1), (i,j+1)]:
				if ii < 1 or ii > nx or jj < 1 or jj > ny: 
					continue
				nom_nb = var_nom.GetBinContent(ii, jj)
				if nom_nb < 1e-10: 
					continue
				var_nb = var_up.GetBinContent(ii, jj)
				neighbors.append((var_nb - nom_nb)/nom_nb)

			if not neighbors:
				continue

			avg_frac = sum(neighbors)/len(neighbors)

			# check if this bin is an outlier
			if abs(frac_var - avg_frac) > threshold:
				new_val = nom * (1 + avg_frac)
				new_up.SetBinContent(i, j, new_val)
	new_up.SetDirectory(0)
	return new_up

def fix_uncerts(sample,   all_uncerts,   uncerts_to_fix,year, regions, technique_str, use_QCD_Pt=False, debug = False):
	ROOT.TH1.AddDirectory(False)
	ROOT.TH1.SetDefaultSumw2()
	ROOT.TH2.SetDefaultSumw2()



	###########################
	## meta variables to change
	###########################

	asymmetry_threshold			  = 0.4	 ## value below which symmetry will be forced for a NP. Set to some large value to force all NPs to be symmetrix 
	fix_small_sandwiched_uncerts	 = True
	fix_opposite_sided_uncertainties = False
	bin_variation_ratio_threshold	 = 0.20 # the ratio of bin_i variation / bin_i+-1 variation that determines if a bin needs to be changed manually


	# symmetry strategies
	sym_strat = "equal"
	#sym_strat = "avg"


	## list of uncorrelated systematics to the correct hist name is grabbed
	uncorrelated_systematics = [  "bTagSF_med", "bTag_eventWeight_bc_M_corr", "bTag_eventWeight_light_M_corr", 
	 "bTag_eventWeight_bc_M_year", "bTag_eventWeight_light_M_year",  "JER", "JER_eta193", 
	  "JER_193eta25", "JEC", "JEC_FlavorQCD", "JEC_RelativeBal",  "JEC_Absolute", "JEC_AbsoluteCal",  "JEC_AbsoluteScale", 
	  "JEC_Fragmentation", "JEC_AbsoluteMPFBias","JEC_RelativeFSR", "JEC_AbsoluteTheory", "JEC_AbsolutePU", "JEC_BBEC1_year",
		"JEC_Absolute_year",  "JEC_RelativeSample_year", "PUSF", "L1Prefiring"] 

	use_QCD_Pt_str = "QCDHT"
	if use_QCD_Pt:
		use_QCD_Pt_str = "QCDPT"


	year_str = "16preAPV"
	if year == "2016":
		year_str = "16"
	elif year == "2017":
		year_str = "17"
	elif year == "2018":
		year_str = "18"



	if "QCD" in sample:   BR_type = "QCD" 
	elif "TTTo" in sample: BR_type = "TTbar"
	elif "TTJets" in sample: BR_type = "TTJets"
	elif "WJets" in sample: BR_type = "WJets"
	elif "ST_" in sample: BR_type = "ST"
	elif "data" in sample: BR_type = "data_obs"
	else:
		print("ERROR: cannot tell BR type: %s. Options are [QCD,TTbar,TTJets,WJets,ST]."%(sample))
		return


	################ TO CHANGE
	infile_name  = infile_path  + "%s_%s_processed.root"%(sample, year,)
	outfile_name = outfile_path + "%s_%s_processed.root"%(sample, year,)
	#################

	create_directories([infile_path,outfile_path])

	print("Looking for file %s"%(infile_name))
	## open root file
	infile = ROOT.TFile.Open(infile_name,"r")
	outfile = ROOT.TFile.Open(outfile_name,"RECREATE")

	### loop over the different systematics (folders of the root file)
	for uncert_count,_uncert in enumerate(all_uncerts): 

		### things to skip
		if _uncert == "topPt" and BR_type not in ["TTbar", "TTTo"] : continue
		if _uncert != "nom" and BR_type == "data_obs": continue
		if (BR_type == "sig" or BR_type == "WJets" or BR_type == "TTTo"   ) and "stat" in _uncert: continue
		
		uncert = _uncert

		# these uncerts are split by process (all are correlated)
		"""if uncert in ["pdf", "renorm", "fact", "scale"] :
			if   BR_type == "sig":   uncert+= "_sig"
			elif "TTbar" in BR_type and uncert == "pdf": uncert += "_misc"
			elif "TTTo" in BR_type:  uncert+= "_TTbar"
			elif BR_type == "allBR": uncert+= "_allBR"
			elif uncert == "pdf" and BR_type in ["QCD","WJets"]: uncert += "_misc"	
			elif BR_type == "QCD": uncert+= "_QCD"
			elif BR_type == "TTbar": uncert+= "_TTbar"
			elif BR_type == "WJets": uncert+= "_WJets"
			elif BR_type == "ST": continue
		if sum( [ uncorr_uncert in uncert for uncorr_uncert in uncorrelated_systematics	]) > 0 : 
			uncert += year_str"""

		out_dir_up_name   = uncert + "_up"
		out_dir_down_name = uncert + "_down"

		out_dir_up   = outfile.Get(out_dir_up_name)
		out_dir_down = outfile.Get(out_dir_down_name)

		if not out_dir_up:
			out_dir_up = outfile.mkdir(out_dir_up_name)
		if not out_dir_down:
			out_dir_down = outfile.mkdir(out_dir_down_name)

		for region in regions:

			if debug: print("-----running %s/%s/%s/%s"%(sample, region, uncert,year))

			# define histogram to correct
			hist_name_up   = "%s_up/h_MSJ_mass_vs_MdSJ_%s"%(uncert, region)
			hist_name_nom = "nom/h_MSJ_mass_vs_MdSJ_%s"%( region)
			hist_name_down = "%s_down/h_MSJ_mass_vs_MdSJ_%s"%(uncert, region)
			
			if debug: print("Getting hist %s from file %s."%(hist_name_up,infile_name))
			if debug: print("Getting hist %s from file %s."%(hist_name_nom,infile_name))
			if debug: print("Getting hist %s from file %s."%(hist_name_down,infile_name))

			old_hist_up = infile.Get(hist_name_up)
			old_hist_up.SetDirectory(0)
			old_hist_nom = infile.Get(hist_name_nom)
			old_hist_nom.SetDirectory(0)


			new_hist_up   	= old_hist_up.Clone()


			if uncert != "topPt":
				old_hist_down = infile.Get(hist_name_down)
				new_hist_down 	= old_hist_down.Clone()
				new_hist_down.SetDirectory(0)

			if uncert in uncerts_to_fix:  # topPt should never make it in here

				if "topPt" in uncert: continue
				if debug: print("FIXING UNCERTAINTIES.")

				new_hist_up = regularize_up_hist(new_hist_up, old_hist_nom, threshold=0.5)
				new_hist_down = regularize_down_hist(new_hist_down, old_hist_nom, threshold=0.5)

				###############################
				##### Make Symmetric Vars #####
				###############################
				for iii in range(1,new_hist_up.GetNbinsX()+1):
					for jjj in range(1,new_hist_down.GetNbinsY()+1 ):
						yield_up   = old_hist_up.GetBinContent(iii,jjj)
						yield_nom  = old_hist_nom.GetBinContent(iii,jjj)
						yield_down = old_hist_down.GetBinContent(iii,jjj)

						if yield_nom < 1e-10: continue # don't bother if there are no counts

						distance_up = abs(yield_up-yield_nom)
						sign_up	 = distance_up/(yield_up-yield_nom) if abs(yield_up-yield_up) > 1e-10 else -1

						distance_down = abs(yield_down-yield_nom)
						sign_down	 = distance_down/(yield_down-yield_nom) if abs(yield_down-yield_nom) > 1e-10 else -1

						# check if variations are very different

						frac_var_up   = distance_up  /yield_nom
						frac_var_down = distance_down/yield_nom

						if frac_var_up < 1e-10 and frac_var_down > 1e-10: frac_var_up = frac_var_down
						elif frac_var_down < 1e-10 and frac_var_up > 1e-10: frac_var_down = frac_var_up
						elif frac_var_down < 1e-10 and frac_var_up < 1e-10: continue
						if (frac_var_up/frac_var_down < asymmetry_threshold):
							if sym_strat == "equal":
								frac_var_up = frac_var_down 
							elif sym_strat == "avg":
								frac_var_up = (frac_var_up + frac_var_down)/2.0
								frac_var_down = frac_var_up
						elif (frac_var_down/frac_var_up < asymmetry_threshold):
							if sym_strat == "equal":
								frac_var_down = frac_var_up 
							elif sym_strat == "avg":
								frac_var_up = (frac_var_up + frac_var_down)/2.0
								frac_var_down = frac_var_up

						new_yield_up = yield_nom * (1 + sign_up*frac_var_up)
						new_yield_down = yield_nom * (1 - sign_up*frac_var_down)

						new_hist_up.SetBinContent(iii,jjj, new_yield_up)
						new_hist_down.SetBinContent(iii,jjj, new_yield_down)

			# make sure one is in the correct output root folder
			# write new histogram there
			out_dir_up.cd()
			new_hist_up.Write()

			if uncert != "topPt":
				out_dir_down.cd()
				new_hist_down.Write()

			if uncert_count == 0: # write the nom hist, only do this once
				
				out_dir_nom   = outfile.Get("nom")
				if not out_dir_nom:
					out_dir_nom = outfile.mkdir("nom")
				out_dir_nom.cd()
				old_hist_nom.Write()



	print("Wrote histograms to %s"%(outfile_name))
	## close all histograms
	infile.Close()
	outfile.Close()



def draw_uncerts(all_uncerts, sample, year, regions, technique_str="", use_QCD_Pt=False, debug=False):
	"""
	Draws fractional differences (up/nom, down/nom) side-by-side in a 2x4 grid per page,
	and saves a multi-page PDF per sample/year.
	"""
	infile_name = outfile_path + "%s_%s_processed.root" % (sample, year)
	if debug:
		print "Opening file %s" % infile_name
	infile = ROOT.TFile.Open(infile_name, "READ")
	if not infile or infile.IsZombie():
		print "Error: could not open %s" % infile_name
		return

	pdf_name = "pdfs/%s_%s_uncert_diagnostics.pdf" % (sample, year)
	c = ROOT.TCanvas("c", "c", 1600, 900)
	c.Divide(4, 2)  # 4 columns x 2 rows = 8 pads per page

	chunk_size = 4  # 4 uncertainties per page
	for region in regions:
		# Filter out "nom"
		uncert_list = [u for u in all_uncerts if u != "nom"]

		for i in range(0, len(uncert_list), chunk_size):
			uncert_chunk = uncert_list[i:i+chunk_size]

			c.Clear()
			c.Divide(4, 2)

			for j, uncert in enumerate(uncert_chunk):
				# Histogram names
				h_nom_name  = "nom/h_MSJ_mass_vs_MdSJ_%s" % region
				h_up_name   = "%s_up/h_MSJ_mass_vs_MdSJ_%s" % (uncert, region)
				h_down_name = "%s_down/h_MSJ_mass_vs_MdSJ_%s" % (uncert, region)

				h_nom  = infile.Get(h_nom_name)
				h_up   = infile.Get(h_up_name)
				h_down = infile.Get(h_down_name)

				if not h_nom or not h_up or not h_down:
					if debug:
						print "Skipping %s/%s (missing histograms)" % (region, uncert)
					continue

				h_nom.SetDirectory(0)
				h_up.SetDirectory(0)
				h_down.SetDirectory(0)

				# Fractional variations
				h_up_frac = h_up.Clone("frac_%s_UP" % uncert)
				h_down_frac = h_down.Clone("frac_%s_DOWN" % uncert)
				nx, ny = h_nom.GetNbinsX(), h_nom.GetNbinsY()
				for ix in range(1, nx+1):
					for iy in range(1, ny+1):
						nom_val = h_nom.GetBinContent(ix, iy)
						if nom_val > 1e-10:
							h_up_frac.SetBinContent(ix, iy, (h_up.GetBinContent(ix, iy) - nom_val)/nom_val)
							h_down_frac.SetBinContent(ix, iy, (h_down.GetBinContent(ix, iy) - nom_val)/nom_val)
						else:
							h_up_frac.SetBinContent(ix, iy, 0.0)
							h_down_frac.SetBinContent(ix, iy, 0.0)

				# Draw up in top row
				c.cd(j+1)
				ROOT.gPad.SetLeftMargin(0.05)
				ROOT.gPad.SetRightMargin(0.05)
				ROOT.gPad.SetTopMargin(0.07)
				ROOT.gPad.SetBottomMargin(0.12)
				h_up_frac.SetTitle("UP")
				h_up_frac.GetZaxis().SetTitle("(var-nom)/nom")
				h_up_frac.Draw("COLZ")

				t = ROOT.TText()
				t.SetNDC()
				t.SetTextSize(0.025)
				t.DrawText(0.05, 0.92, "Sample: %s" % sample)
				t.DrawText(0.05, 0.87, "Year: %s" % year)
				t.DrawText(0.05, 0.82, "Region: %s" % region)
				t.DrawText(0.05, 0.77, "Systematic: %s" % uncert)
				t.DrawText(0.05, 0.72, "UP / TOP ROW")

				# Draw down in bottom row
				c.cd(j+5)
				ROOT.gPad.SetLeftMargin(0.05)
				ROOT.gPad.SetRightMargin(0.05)
				ROOT.gPad.SetTopMargin(0.07)
				ROOT.gPad.SetBottomMargin(0.12)
				h_down_frac.SetMarkerColor(ROOT.kRed)
				h_down_frac.SetLineColor(ROOT.kRed)
				h_down_frac.SetTitle("DOWN")
				h_down_frac.GetZaxis().SetTitle("(var-nom)/nom")
				h_down_frac.Draw("COLZ")

				t.DrawText(0.05, 0.92, "Sample: %s" % sample)
				t.DrawText(0.05, 0.87, "Year: %s" % year)
				t.DrawText(0.05, 0.82, "Region: %s" % region)
				t.DrawText(0.05, 0.77, "Systematic: %s" % uncert)
				t.DrawText(0.05, 0.72, "DOWN / BOTTOM ROW")

			# Print page
			c.Print(pdf_name)

	infile.Close()
	print "Diagnostic plots written to %s" % pdf_name

if __name__=="__main__":
	
	debug = True

	all_uncerts = [  "scale",  "bTag_eventWeight_bc_M_corr", "bTag_eventWeight_light_M_corr", "bTag_eventWeight_bc_M_year", "bTag_eventWeight_light_M_year",  "JER", "JER_eta193", "JER_193eta25", "JEC", "JEC_FlavorQCD", "JEC_RelativeBal",  "JEC_Absolute", "JEC_AbsoluteCal",  "JEC_AbsoluteScale", "JEC_Fragmentation", "JEC_AbsoluteMPFBias","JEC_RelativeFSR", "JEC_AbsoluteTheory", "JEC_AbsolutePU", "JEC_BBEC1_year",  "JEC_Absolute_year",  "JEC_RelativeSample_year", "PUSF", "topPt", "L1Prefiring", "pdf","renorm", "fact"]  ## systematic namings for cards   "btagSF", 
	
	uncerts_to_fix =  [ "bTagSF_med", "bTag_eventWeight_bc_M_corr", "bTag_eventWeight_light_M_corr", 
	 "bTag_eventWeight_bc_M_year", "bTag_eventWeight_light_M_year",  "JER", "JER_eta193", 
	  "JER_193eta25", "JEC", "JEC_FlavorQCD", "JEC_RelativeBal",  "JEC_Absolute", "JEC_AbsoluteCal",  "JEC_AbsoluteScale", 
	  "JEC_Fragmentation", "JEC_AbsoluteMPFBias","JEC_RelativeFSR", "JEC_AbsoluteTheory", "JEC_AbsolutePU", "JEC_BBEC1_year",
		"JEC_Absolute_year",  "JEC_RelativeSample_year", "PUSF", "L1Prefiring"]  ## systematic namings for cards   "btagSF",  ,   "bTagSF_bc_T",	  "bTagSF_light_T",	   "bTagSF_bc_M",	   "bTagSF_light_M", 


	# skip "nom" here, but just write it for the first interation of uncertainties 


	years = ["2015","2016","2017","2018"]
	regions = ["SR","CR","AT1b","AT0b"]

	samples = [ "dataA","dataB","dataC","dataD","QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT800to1200",
	"TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf","TTToHadronicMC", "TTToSemiLeptonicMC", "TTToLeptonicMC",
		 "ST_t-channel-top_inclMC","ST_t-channel-antitop_inclMC","ST_s-channel-hadronsMC","ST_s-channel-leptonsMC",
		 "ST_tW-antiTop_inclMC","ST_tW-top_inclMC", "WJetsMC_LNu-HT800to1200", "WJetsMC_LNu-HT1200to2500",  
		 "WJetsMC_LNu-HT2500toInf", "WJetsMC_QQ-HT800toInf","ZZ_MC", "WW_MC","QCDMC_Pt_170to300",
		  "QCDMC_Pt_300to470","QCDMC_Pt_470to600","QCDMC_Pt_600to800","QCDMC_Pt_800to1000",
			"QCDMC_Pt_1000to1400","QCDMC_Pt_1400to1800","QCDMC_Pt_1800to2400","QCDMC_Pt_2400to3200","QCDMC_Pt_3200toInf"] # all process types 

	technique_strs = ["NN_",""]

	technique_strs = [""]

	#### debugging stuff
	if debug:
		years = ["2015"]

		mass_points = ["Suu4_chi1"]


	use_QCD_Pt_opts = [True,False]
	use_QCD_Pt_strs = ["QCDPT","QCDHT"]


	for jjj,use_QCD_Pt in enumerate(use_QCD_Pt_opts):
		for technique_str in technique_strs:
			for year in years:
				samples = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT800to1200",
				"TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf","TTToHadronicMC", "TTToSemiLeptonicMC", "TTToLeptonicMC",
					 "ST_t-channel-top_inclMC","ST_t-channel-antitop_inclMC","ST_s-channel-hadronsMC","ST_s-channel-leptonsMC",
					 "ST_tW-antiTop_inclMC","ST_tW-top_inclMC", "WJetsMC_LNu-HT800to1200", "WJetsMC_LNu-HT1200to2500",  
					 "WJetsMC_LNu-HT2500toInf", "WJetsMC_QQ-HT800toInf","ZZ_MC", "WW_MC","QCDMC_Pt_170to300",
					  "QCDMC_Pt_300to470","QCDMC_Pt_470to600","QCDMC_Pt_600to800","QCDMC_Pt_800to1000",
						"QCDMC_Pt_1000to1400","QCDMC_Pt_1400to1800","QCDMC_Pt_1800to2400","QCDMC_Pt_2400to3200","QCDMC_Pt_3200toInf"] # all process types 


				if year == "2015":   samples.extend( ["dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM","dataF-HIPM"] )
				elif year == "2015": samples.extend( ["dataF","dataG","dataH"] )
				elif year == "2015": samples.extend( ["dataB","dataC","dataD","dataE"] )
				elif year == "2015": samples.extend( ["dataA","dataB","dataC","dataD"] )

				for sample in samples:
						fix_uncerts( sample, all_uncerts, uncerts_to_fix, year, regions, technique_str, use_QCD_Pt, debug   )
						draw_uncerts(all_uncerts, sample, year, regions, technique_str, use_QCD_Pt, debug)
