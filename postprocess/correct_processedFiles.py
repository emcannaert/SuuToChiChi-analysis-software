import ROOT
import sys,os
from math import sqrt
import ast
import random
from array import array

from combine_hists import combine_hists
from return_BR_SF.return_BR_SF import return_BR_SF



#### operates on the TH2F to fix asymmetrix uncertainties, mainly JECs
#### the "fixed" outputs are written to combinedROOT/processedFilesCorected
#### comparisons of the new variations to the nom are printed to pdfs

ROOT.gErrorIgnoreLevel = ROOT.kWarning


useEOS  = True
infile_path  = "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/" if useEOS else "../combinedROOT/processedFiles/"
outfile_path = "root://cmseos.fnal.gov//store/user/ecannaer/processedFilesCorrected/" if useEOS else "../combinedROOT/processedFilesCorrected/"

BR_SFs = return_BR_SF()

n_colors = 5
stops  = array('d', [0.0, 0.25, 0.5, 0.75, 1.0])  # positions along palette
red	= array('d', [0.0, 0.0, 1.0, 1.0, 0.5])
green  = array('d', [0.0, 0.0, 1.0, 0.0, 0.0])
blue   = array('d', [1.0, 1.0, 1.0, 0.0, 0.0])

ROOT.TColor.CreateGradientColorTable(n_colors, stops, red, green, blue, 255)
ROOT.gStyle.SetNumberContours(255)



def find_nearest_nonzero_bins(hist_var, hist_nom, i, j, n=4):
	"""
	Find the n nearest nonzero bins to bin (i,j) in a ROOT TH2F.
	Returns a list of (binx, biny, distance, content).
	"""
	nx = hist_var.GetNbinsX()
	ny = hist_var.GetNbinsY()
	nom_results = []
	var_results = []

	# expand search radius until enough bins are found
	for radius in range(1, nx + ny):
		for dx in range(-radius, radius + 1):
			for dy in range(-radius, radius + 1):
				if abs(dx) + abs(dy) != radius:   # only the "Manhattan shell"
					continue
				bx = i + dx
				by = j + dy
				if bx < 1 or bx > nx or by < 1 or by > ny:
					continue
				content = hist_var.GetBinContent(bx, by)
				if content > 0:
					dist = sqrt(dx*dx + dy*dy)  # Euclidean distance
					var_results.append( content )  # (bx, by, dist, content)
					nom_results.append( hist_nom.GetBinContent(bx,by) )
		if len(var_results) >= n:
			break

	# sort by distance
	#results.sort(key=lambda x: x[2])

	return var_results[:n], nom_results[:n]

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
									
### helper for a given variation QCDHT up/down his, QCDHT nom hist, and QCDPT var hist (which should just be nom) , return the corresponding variation QCDPT hist
def get_QCDPT_var_hist(  region, year, uncert, var, technique_str, QCDPT_hist_nom):
	### get QCDHT_hist_var

	sample_list = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf"]

	file_paths = { sample_type: "{}{}_{}_processed.root".format(infile_path,sample_type, year) for sample_type in sample_list   }
	hist_weights = { sample_type: BR_SFs[sample_type.replace("-","_")][year] for sample_type in sample_list }
 
	hist_name_var = "%s_%s/h_MSJ_mass_vs_MdSJ_%s"%( uncert,var, region)
	hist_name_nom = "nom/h_MSJ_mass_vs_MdSJ_%s"%( region)

	### get QCDHT hist var
	QCDHT_hist_var = combine_hists(
		sample_list,
		file_paths,
		hist_name_var,
		hist_weights=hist_weights,
		hist_label = hist_name_var + "_" + year
	)
	### get QCDHT hist nom
	QCDHT_hist_nom = combine_hists(
		sample_list,
		file_paths,
		hist_name_nom,
		hist_weights=hist_weights,
		hist_label = hist_name_nom + "_" + year
	)

	QCDPT_hist_var = QCDPT_hist_nom.Clone() #QCDPT_hist_nom.GetName() + "_" + uncert + "_" + var
	QCDPT_hist_var.Reset()

	## verify that all hists have same size
	if QCDHT_hist_var.GetNbinsX() != QCDPT_hist_nom.GetNbinsX() or QCDHT_hist_nom.GetNbinsX() != QCDPT_hist_nom.GetNbinsX():
		raise ValueError("ERROR: the QCDPT and QCDHT hists don't \
		 have same size: len_x(%s) = %s, len_x(%s) = %s, len_x(%s) = %s, len_y(%s) = %s, \
		 len_y(%s) = %s, len_y(%s) = %s,  "%(QCDHT_hist_var.GetName(), QCDHT_hist_var.GetNbinsX(),  
		 	QCDHT_hist_nom.GetName(), QCDHT_hist_nom.GetNbinsX(),  
		 	QCDPT_hist_var.GetName(), QCDPT_hist_var.GetNbinsX(),
			QCDHT_hist_var.GetName(), QCDHT_hist_var.GetNbinsY(),  
		 	QCDHT_hist_nom.GetName(), QCDHT_hist_nom.GetNbinsY(),  
		 	QCDPT_hist_var.GetName(), QCDPT_hist_var.GetNbinsY() ))


	# now go through all bins to get the fractional variation in QCDHT
	for iii in range(1,QCDHT_hist_var.GetNbinsX()+1):
		for jjj in range(1,QCDHT_hist_var.GetNbinsY()+1):

			nom_QCDPT_yield = QCDPT_hist_nom.GetBinContent(iii,jjj)
			if nom_QCDPT_yield < 1e-10: continue


			nom_QCDHT_yield = QCDHT_hist_nom.GetBinContent(iii,jjj)
			var_QCDHT_yield = QCDHT_hist_var.GetBinContent(iii,jjj)

			if var_QCDHT_yield < 1e-10 or nom_QCDHT_yield < 1e-10:
				## get nearest yields from four nearest nonzero bins 
				var_neighbors, nom_neighbors =  find_nearest_nonzero_bins(QCDHT_hist_var, QCDHT_hist_nom, iii, jjj,n=6)
				var_QCDHT_yield = sum(var_neighbors)/ float(sum(nom_neighbors))

			frac_var = var_QCDHT_yield/nom_QCDHT_yield if nom_QCDHT_yield > 0 else 1.0

			QCDPT_hist_var.SetBinContent(iii,jjj, frac_var *  nom_QCDPT_yield  )

	## should be corrected now, but need to extrapolate where nom bins are non-zero and vars are zero
	QCDPT_hist_var.SetDirectory(0)  # -->pointer to original hist, do I want to do this?

	QCDPT_hist_var = extrapolate_var(QCDPT_hist_nom, QCDPT_hist_var)

	return QCDPT_hist_var
def extrapolate_var(QCDPT_hist_nom, QCDPT_hist_var,  max_neighbors=5):
	nbinsX = QCDPT_hist_nom.GetNbinsX()
	nbinsY = QCDPT_hist_nom.GetNbinsY()

	up_excl   = 0.60
	down_excl = -0.60

	#print("inside extrapolate var")
	for ix in range(1, nbinsX+1):
		for iy in range(1, nbinsY+1):

			nom_val = QCDPT_hist_nom.GetBinContent(ix, iy)
			var_val = QCDPT_hist_var.GetBinContent(ix, iy)


			if nom_val > 0 and abs(nom_val - var_val) < 1e-9:

				#print("attempting to fix (%s, %s)"%(ix,iy))
				neighbors = []

				# search outward until we find enough filled neighbors
				radius = 1
				while len(neighbors) < max_neighbors and radius < max(nbinsX, nbinsY):
					for dx in range(-radius, radius+1):
						for dy in range(-radius, radius+1):
							if dx == 0 and dy == 0:
								continue
							nx, ny = ix+dx, iy+dy
							if 1 <= nx <= nbinsX and 1 <= ny <= nbinsY:
								neighbor_nom =  QCDPT_hist_nom.GetBinContent(nx, ny)
								neighbor_updown = QCDPT_hist_var.GetBinContent(nx, ny)
								#print("For bin (%s, %s), the var value is %s, the nom is %s."%(nx, ny, neighbor_updown, neighbor_nom))
								if neighbor_nom > 0:
									if abs(neighbor_updown - neighbor_nom) > 1e-9:
										neigh_var =  neighbor_updown / neighbor_nom if neighbor_nom > 0 else 0
										if neigh_var != 0 and ( (neigh_var - 1.0) < up_excl and (neigh_var - 1.0) > down_excl):
											neighbors.append(neigh_var)
					radius += 1

				#print("tried to fix")
				#print("neighbors is %s"%neighbors)
				if neighbors:
					avg_var = sum(neighbors[:max_neighbors]) / float(len(neighbors[:max_neighbors]))  # 
					#print("The average variation is %s."%avg_var)

					new_val = avg_var * nom_val
					#print("Fixed bin (%s/%s): old value %s changed val to %s"%(ix,iy, QCDPT_hist_var.GetBinContent(ix,iy),new_val))
					QCDPT_hist_var.SetBinContent(ix, iy, new_val)

	return QCDPT_hist_var
def regularize_hist(var, var_nom, threshold=0.5):
	"""
	Regularize a TH2 histogram variation ("up" or "down") against its nominal.

	Parameters
	----------
	var : TH2
		The varied histogram (up or down).
	var_nom : TH2
		The nominal histogram.
	threshold : float
		Maximum allowed difference between bin fractional variation
		and average neighbor fractional variation.

	Returns
	-------
	new_hist : TH2
		The regularized histogram.
	"""
	new_hist = var.Clone(var.GetName())
	nx, ny = new_hist.GetNbinsX(), new_hist.GetNbinsY()

	# 8-connected neighbors (includes diagonals)
	neighbor_offsets = [
		(-1, -1), (-1, 0), (-1, 1),
		( 0, -1),		  ( 0, 1),
		( 1, -1), ( 1, 0), ( 1, 1) ]

	for i in range(1, nx+1):
		for j in range(1, ny+1):
			nom = var_nom.GetBinContent(i, j)

			if var.GetBinContent(i, j) < 1e-10:
				var.SetBinContent(i, j, 0)
			if nom < 1e-10:  # skip empty bins completely
				continue

			var_val = var.GetBinContent(i, j)
			frac_var = (var_val - nom) / nom

			neighbors = []
			for dx, dy in neighbor_offsets:
				ii, jj = i + dx, j + dy
				if ii < 1 or ii > nx or jj < 1 or jj > ny:
					continue
				nom_nb = var_nom.GetBinContent(ii, jj)
				if nom_nb < 1e-10:
					continue
				var_nb = var.GetBinContent(ii, jj)
				neighbors.append((var_nb - nom_nb) / nom_nb)

			if not neighbors:
				continue

			avg_frac = sum(neighbors) / len(neighbors)

			if abs(frac_var - avg_frac) > threshold and nom > 0:

				#print("Fixing bin %s/%s for %s"%(i,j, var.GetName()))

				new_val = nom * (1 + avg_frac)
				new_hist.SetBinContent(i, j, new_val)

	new_hist.SetDirectory(0)
	return new_hist



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
	bin_variation_ratio_threshold	 = 0.30 # the ratio of bin_i variation / bin_i+-1 variation that determines if a bin needs to be changed manually


	# symmetry strategies
	sym_strat = "equal"
	#sym_strat = "avg"


	## list of uncorrelated systematics to the correct hist name is grabbed
	uncorrelated_systematics = [ "bTagSF_med", "bTag_eventWeight_bc_M_corr", "bTag_eventWeight_light_M_corr", 
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
	################

	create_directories([infile_path,outfile_path])

	print("Looking for file %s"%(infile_name))
	## open root file
	infile = ROOT.TFile.Open(infile_name,"r")
	outfile = ROOT.TFile.Open(outfile_name,"RECREATE")

	### loop over the different systematics (folders of the root file)
	for uncert_count,_uncert in enumerate(all_uncerts): 

		### things to skip
		if _uncert == "topPt" and BR_type not in [ "TTTo", "TTJets"] : continue
		if _uncert != "nom" and BR_type == "data_obs": continue
		if (BR_type == "sig" or BR_type == "WJets" or BR_type == "TTTo"   ) and "stat" in _uncert: continue
		
		uncert = _uncert

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


			## if this is scale, pdf, renorm, fact, get the extrapolated hists from QCDHT
			if debug: print('uncert is %s, is it in  ["scale", "fact","renorm", "pdf"]?: %s.'%(uncert, uncert in ["scale", "fact","renorm", "pdf"]))

			if "QCDMC_Pt" in sample and uncert in ["scale", "fact","renorm", "pdf"]: old_hist_up = get_QCDPT_var_hist( region, year, uncert, "up", technique_str, old_hist_nom)
			new_hist_up   	= old_hist_up.Clone()

			if uncert != "topPt":
				old_hist_down = infile.Get(hist_name_down)
				if "QCDMC_Pt" in sample and uncert in ["scale", "fact","renorm", "pdf"]: old_hist_down = get_QCDPT_var_hist(region, year, uncert, "down", technique_str, old_hist_nom)
				new_hist_down 	= old_hist_down.Clone()
				new_hist_down.SetDirectory(0)

			if uncert in uncerts_to_fix and "topPt" not in uncert:  # topPt should never make it in here
				if debug: print("FIXING UNCERTAINTIES.")

				new_hist_up = regularize_hist(new_hist_up, old_hist_nom, threshold=0.5)
				new_hist_down = regularize_hist(new_hist_down, old_hist_nom, threshold=0.5)

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
	import math

	infile_name = outfile_path + "%s_%s_processed.root" % (sample, year)
	if debug: print("Opening file %s" % infile_name)
	infile = ROOT.TFile.Open(infile_name, "READ")
	if not infile or infile.IsZombie():
		print("Error: could not open %s" % infile_name)
		return

	create_directories(["pdf"])
	create_directories(["pdf/separate_samples"])

	pdf_name = "pdf/%s_%s_sepBR_uncert_diagnostics.pdf" % (sample, year)
	c = ROOT.TCanvas("c", "c", 1600, 900)
	c.SetRightMargin(0.15)

	systematics_to_draw = [u for u in all_uncerts if u != "nom"]

	canvas = ROOT.TCanvas("","",1600,1400)
	canvas.SetLeftMargin(0.10)
	canvas.SetRightMargin(0.15)
	canvas.SetTopMargin(0.07)
	canvas.SetBottomMargin(0.12)


	if debug: print("systematics_to_draw is %s."%systematics_to_draw)

	pad_counter = 0
	first_page = True
	histograms = []

	# collect all histograms first
	for region in regions:
		for uncert in systematics_to_draw:
			h_nom_name  = "nom/h_MSJ_mass_vs_MdSJ_%s" % region
			h_up_name   = "%s_up/h_MSJ_mass_vs_MdSJ_%s" % (uncert, region)
			h_down_name = "%s_down/h_MSJ_mass_vs_MdSJ_%s" % (uncert, region)

			h_nom  = infile.Get(h_nom_name)
			h_up   = infile.Get(h_up_name)
			h_down = infile.Get(h_down_name)
			if not h_nom or not h_up or not h_down:
				if uncert != "topPt" and "data" not in sample: print("Skipping %s/%s: missing histograms" % (region, uncert))
				continue
			h_nom.SetDirectory(0)
			h_up.SetDirectory(0)
			h_down.SetDirectory(0)

			h_up_frac = h_up.Clone("frac_%s_UP_%s" % (uncert, region))
			h_down_frac = h_down.Clone("frac_%s_DOWN_%s" % (uncert, region))

			nx, ny = h_nom.GetNbinsX(), h_nom.GetNbinsY()
			for i in range(1, nx+1):
				for j in range(1, ny+1):
					nom_val = h_nom.GetBinContent(i,j)
					if nom_val > 1e-10:
						h_up_frac.SetBinContent(i,j, (h_up.GetBinContent(i,j)-nom_val)/nom_val)
						h_down_frac.SetBinContent(i,j, (h_down.GetBinContent(i,j)-nom_val)/nom_val)
					else:
						h_up_frac.SetBinContent(i,j, 0.0)
						h_down_frac.SetBinContent(i,j, 0.0)

			histograms.append((h_up_frac, "UP", region, uncert))
			histograms.append((h_down_frac, "DOWN", region, uncert))

	# draw histograms
	for idx, (hist, var_label, region, uncert) in enumerate(histograms):
		pad_idx = (idx % 8) + 1
		if pad_idx == 1:
			c.Clear()
			c.Divide(4,2)
			ROOT.gPad.Update()
		c.cd(pad_idx)
		ROOT.gPad.SetLeftMargin(0.10)
		ROOT.gPad.SetRightMargin(0.15)
		ROOT.gPad.SetTopMargin(0.07)
		ROOT.gPad.SetBottomMargin(0.12)

		#hist.SetTitle("")
		hist.GetYaxis().SetTitle( "avg. superjet mass [GeV]")
		hist.GetZaxis().SetTitle("(var-nom)/nom")
		hist.GetZaxis().SetTitleSize(0.035)
		hist.GetZaxis().SetLabelSize(0.025)
		hist.GetXaxis().SetLabelSize(0.025)
		hist.GetYaxis().SetLabelSize(0.025)
		hist.SetStats(0)

		# Set consistent z-axis
		hist.SetMinimum(-1.0)
		hist.SetMaximum(1.0)


		# TEXT: only for non-zero bins, round to 2 decimals
		hist.Draw("COLZ")  # draw the color
		nx, ny = hist.GetNbinsX(), hist.GetNbinsY()
		# Draw bin content numbers
		for i in range(1, nx+1):
			for j in range(1, ny+1):
				val = hist.GetBinContent(i,j)
				if abs(val) > 1e-10:
					tbin = ROOT.TText()
					tbin.SetTextSize(0.015)
					tbin.SetTextAlign(22)  # center
					x = hist.GetXaxis().GetBinCenter(i)
					y = hist.GetYaxis().GetBinCenter(j)
					tbin.DrawText(x, y, "%.2f" % val)


		# TText top-right
		t = ROOT.TText()
		t.SetNDC()
		t.SetTextSize(0.025)
		x_offset = 0.2
		y_start = 0.85
		t.DrawText(x_offset, y_start, "Sample: %s" % sample)
		t.DrawText(x_offset, y_start-0.03, "Year: %s" % year)
		t.DrawText(x_offset, y_start-0.06, "Region: %s" % region)
		t.DrawText(x_offset, y_start-0.09, "Systematic: %s" % uncert)
		t.DrawText(x_offset, y_start-0.12, "Variation: %s" % var_label)


		# print page if pad_idx == 8 or last histogram
		if pad_idx == 8 or idx == len(histograms)-1:
			if first_page:
				c.Print(pdf_name + "[")
				first_page = False
			c.Print(pdf_name)



		## draw the png
		canvas.cd()

		canvas.Clear()	 # important: start fresh
		hist.Draw("COLZ")  # draw the color
		for i in range(1, nx+1):
			for j in range(1, ny+1):
				val = hist.GetBinContent(i,j)
				if abs(val) > 1e-10:
					tbin2 = ROOT.TText()
					tbin2.SetTextSize(0.015)
					tbin2.SetTextAlign(22)  # center
					x = hist.GetXaxis().GetBinCenter(i)
					y = hist.GetYaxis().GetBinCenter(j)
					tbin2.DrawText(x, y, "%.2f" % val)

		t2 = ROOT.TText()
		t2.SetNDC()
		t2.SetTextSize(0.025)
		x_offset = 0.2
		y_start = 0.85
		t2.DrawText(x_offset, y_start, "Sample: %s" % sample)
		t2.DrawText(x_offset, y_start-0.03, "Year: %s" % year)
		t2.DrawText(x_offset, y_start-0.06, "Region: %s" % region)
		t2.DrawText(x_offset, y_start-0.09, "Systematic: %s" % uncert)
		t2.DrawText(x_offset, y_start-0.12, "Variation: %s" % var_label)

		png_name = "plots/correctedProcessedUncertComparisons/uncert_comp_sepBR_%s_%s_%sNOM_%s_%s.png"%(sample, uncert,var_label, region, year )

		canvas.Modified()
		canvas.Update()
		canvas.SaveAs(png_name)

	c.Print(pdf_name + "]")


	infile.Close()
	print("Diagnostic plots written to %s" % pdf_name)


def draw_uncerts_combined_BR(all_uncerts, year, regions, technique_str="", use_QCD_Pt=False, debug=False):
	import math

	samples = ["TTJetsMCHT800to1200", "TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf",
				"ST_t-channel-top_inclMC","ST_t-channel-antitop_inclMC","ST_s-channel-hadronsMC","ST_s-channel-leptonsMC",
					 "ST_tW-antiTop_inclMC","ST_tW-top_inclMC", "WJetsMC_LNu-HT800to1200", "WJetsMC_LNu-HT1200to2500",  
					 "WJetsMC_LNu-HT2500toInf", "WJetsMC_QQ-HT800toInf","QCDMC_Pt_170to300",
					  "QCDMC_Pt_300to470","QCDMC_Pt_470to600","QCDMC_Pt_600to800","QCDMC_Pt_800to1000",
						"QCDMC_Pt_1000to1400","QCDMC_Pt_1400to1800","QCDMC_Pt_1800to2400","QCDMC_Pt_2400to3200","QCDMC_Pt_3200toInf"] # all process types 



	create_directories(["pdf"])
	create_directories(["pdf/combined_samples"])

	pdf_name = "pdf/allBR_%s_combinedBR_uncert_diagnostics.pdf" % ( year)
	c = ROOT.TCanvas("c", "c", 1600, 900)
	c.SetRightMargin(0.15)

	systematics_to_draw = [u for u in all_uncerts if u != "nom"]

	canvas = ROOT.TCanvas("","",1600,1400)
	canvas.SetLeftMargin(0.10)
	canvas.SetRightMargin(0.15)
	canvas.SetTopMargin(0.07)
	canvas.SetBottomMargin(0.12)

	if debug: print("systematics_to_draw is %s."%systematics_to_draw)

	pad_counter = 0
	first_page = True
	histograms = []

	# collect all histograms first
	for region in regions:
		for uncert in systematics_to_draw:

			file_paths   = { sample_type: "{}{}_{}_processed.root".format(outfile_path,sample_type, year) for sample_type in samples   }
			hist_weights = { sample_type: BR_SFs[sample_type.replace("-","_")][year] for sample_type in samples }

			h_nom_name  = "nom/h_MSJ_mass_vs_MdSJ_%s" % region
			h_up_name   = "%s_up/h_MSJ_mass_vs_MdSJ_%s" % (uncert, region)
			h_down_name = "%s_down/h_MSJ_mass_vs_MdSJ_%s" % (uncert, region)

			if uncert == "topPt": continue
			
			h_nom = combine_hists(
				samples,
				file_paths,
				h_nom_name,
				hist_weights=hist_weights,
				hist_label = h_nom_name + "_" + year
			)
			h_up = combine_hists(
				samples,
				file_paths,
				h_up_name,
				hist_weights=hist_weights,
				hist_label = h_up_name + "_" + year
			)
			h_down = combine_hists(
				samples,
				file_paths,
				h_down_name,
				hist_weights=hist_weights,
				hist_label = h_down_name + "_" + year
			)
			if not h_nom or not h_up or not h_down:
				if uncert != "topPt": print("Skipping %s/%s: missing histograms" % (region, uncert))
				continue

			h_nom.SetDirectory(0)
			h_up.SetDirectory(0)
			h_down.SetDirectory(0)

			h_up_frac = h_up.Clone("frac_%s_UP_%s" % (uncert, region))
			h_down_frac = h_down.Clone("frac_%s_DOWN_%s" % (uncert, region))

			nx, ny = h_nom.GetNbinsX(), h_nom.GetNbinsY()
			for i in range(1, nx+1):
				for j in range(1, ny+1):
					nom_val = h_nom.GetBinContent(i,j)
					if nom_val > 1e-10:
						h_up_frac.SetBinContent(i,j, (h_up.GetBinContent(i,j)-nom_val)/nom_val)
						h_down_frac.SetBinContent(i,j, (h_down.GetBinContent(i,j)-nom_val)/nom_val)
					else:
						h_up_frac.SetBinContent(i,j, 0.0)
						h_down_frac.SetBinContent(i,j, 0.0)

			histograms.append((h_up_frac, "UP", region, uncert))
			histograms.append((h_down_frac, "DOWN", region, uncert))

	# draw histograms
	for idx, (hist, var_label, region, uncert) in enumerate(histograms):
		pad_idx = (idx % 8) + 1
		if pad_idx == 1:
			c.Clear()
			c.Divide(4,2)
			ROOT.gPad.Update()
		c.cd(pad_idx)
		ROOT.gPad.SetLeftMargin(0.10)
		ROOT.gPad.SetRightMargin(0.15)
		ROOT.gPad.SetTopMargin(0.07)
		ROOT.gPad.SetBottomMargin(0.12)

		#hist.SetTitle("")
		hist.GetYaxis().SetTitle( "avg. superjet mass [GeV]")
		hist.GetZaxis().SetTitle("(var-nom)/nom")
		hist.GetZaxis().SetTitleSize(0.035)
		hist.GetZaxis().SetLabelSize(0.025)
		hist.GetXaxis().SetLabelSize(0.025)
		hist.GetYaxis().SetLabelSize(0.025)
		hist.SetStats(0)

		# Set consistent z-axis
		hist.SetMinimum(-1.0)
		hist.SetMaximum(1.0)


		# TEXT: only for non-zero bins, round to 2 decimals
		hist.Draw("COLZ")  # draw the color
		nx, ny = hist.GetNbinsX(), hist.GetNbinsY()
		# Draw bin content numbers
		for i in range(1, nx+1):
			for j in range(1, ny+1):
				val = hist.GetBinContent(i,j)
				if abs(val) > 1e-10:
					tbin = ROOT.TText()
					tbin.SetTextSize(0.015)
					tbin.SetTextAlign(22)  # center
					x = hist.GetXaxis().GetBinCenter(i)
					y = hist.GetYaxis().GetBinCenter(j)
					tbin.DrawText(x, y, "%.2f" % val)


		# TText top-right
		t = ROOT.TText()
		t.SetNDC()
		t.SetTextSize(0.025)
		x_offset = 0.2
		y_start = 0.85
		t.DrawText(x_offset, y_start-0.03, "Year: %s" % year)
		t.DrawText(x_offset, y_start-0.06, "Region: %s" % region)
		t.DrawText(x_offset, y_start-0.09, "Systematic: %s" % uncert)
		t.DrawText(x_offset, y_start-0.12, "Variation: %s" % var_label)


		# print page if pad_idx == 8 or last histogram
		if pad_idx == 8 or idx == len(histograms)-1:
			if first_page:
				c.Print(pdf_name + "[")
				first_page = False
			c.Print(pdf_name)





		## draw the png
		canvas.cd()

		canvas.Clear()	 # important: start fresh
		hist.Draw("COLZ")  # draw the color
		for i in range(1, nx+1):
			for j in range(1, ny+1):
				val = hist.GetBinContent(i,j)
				if abs(val) > 1e-10:
					tbin2 = ROOT.TText()
					tbin2.SetTextSize(0.015)
					tbin2.SetTextAlign(22)  # center
					x = hist.GetXaxis().GetBinCenter(i)
					y = hist.GetYaxis().GetBinCenter(j)
					tbin2.DrawText(x, y, "%.2f" % val)

		t2 = ROOT.TText()
		t2.SetNDC()
		t2.SetTextSize(0.025)
		x_offset = 0.2
		y_start = 0.85
		t2.DrawText(x_offset, y_start-0.03, "Year: %s" % year)
		t2.DrawText(x_offset, y_start-0.06, "Region: %s" % region)
		t2.DrawText(x_offset, y_start-0.09, "Systematic: %s" % uncert)
		t2.DrawText(x_offset, y_start-0.12, "Variation: %s" % var_label)

		png_name = "plots/correctedProcessedUncertComparisons/uncert_comp_combinedBR_allBR_%s_%sNOM_%s_%s.png"%(uncert,var_label, region, year )

		canvas.Modified()
		canvas.Update()
		canvas.SaveAs(png_name)

	c.Print(pdf_name + "]")

	print("Diagnostic plots written to %s" % pdf_name)

if __name__=="__main__":
	
	debug = True

	all_uncerts = [ "scale", "pdf", "fact", "renorm",   "bTag_eventWeight_bc_M_corr", "bTag_eventWeight_light_M_corr", "bTag_eventWeight_bc_M_year", "bTag_eventWeight_light_M_year",  "JER", "JER_eta193", "JER_193eta25", "JEC", "JEC_FlavorQCD", "JEC_RelativeBal",  "JEC_Absolute", "JEC_AbsoluteCal",  "JEC_AbsoluteScale", "JEC_Fragmentation", "JEC_AbsoluteMPFBias","JEC_RelativeFSR", "JEC_AbsoluteTheory", "JEC_AbsolutePU", "JEC_BBEC1_year",  "JEC_Absolute_year",  "JEC_RelativeSample_year", "PUSF", "topPt", "L1Prefiring"]  ## systematic namings for cards   "btagSF", 
	
	uncerts_to_fix =  ["bTagSF_med", "bTag_eventWeight_bc_M_corr", "bTag_eventWeight_light_M_corr", 
	 "bTag_eventWeight_bc_M_year", "bTag_eventWeight_light_M_year",  "JER", "JER_eta193", 
	  "JER_193eta25", "JEC", "JEC_FlavorQCD", "JEC_RelativeBal",  "JEC_Absolute", "JEC_AbsoluteCal",  "JEC_AbsoluteScale", 
	  "JEC_Fragmentation", "JEC_AbsoluteMPFBias","JEC_RelativeFSR", "JEC_AbsoluteTheory", "JEC_AbsolutePU", "JEC_BBEC1_year",
		"JEC_Absolute_year",  "JEC_RelativeSample_year", "PUSF", "L1Prefiring"]  ## systematic namings for cards   "btagSF",  ,   "bTagSF_bc_T",	  "bTagSF_light_T",	   "bTagSF_bc_M",	   "bTagSF_light_M", 


	# skip "nom" here, but just write it for the first interation of uncertainties 


	years = ["2015","2016","2017","2018"]
	regions = ["SR","CR","AT1b","AT0b"]

	samples = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT800to1200",
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

		all_uncerts = [ "scale", "pdf", "fact", "renorm", "JEC_Absolute"]  ## systematic namings for cards   "btagSF", 
		samples = [ "QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","QCDMC_Pt_170to300",
		  "QCDMC_Pt_300to470","QCDMC_Pt_470to600","QCDMC_Pt_600to800","QCDMC_Pt_800to1000",
			"QCDMC_Pt_1000to1400","QCDMC_Pt_1400to1800","QCDMC_Pt_1800to2400","QCDMC_Pt_2400to3200","QCDMC_Pt_3200toInf"] 

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

				if debug: samples = [ "QCDMC_Pt_3200toInf"]   # ,"QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","QCDMC_Pt_170to300","QCDMC_Pt_300to470","QCDMC_Pt_470to600","QCDMC_Pt_600to800","QCDMC_Pt_800to1000","QCDMC_Pt_1000to1400","QCDMC_Pt_1400to1800","QCDMC_Pt_1800to2400","QCDMC_Pt_2400to3200"

				for sample in samples:
					fix_uncerts( sample, all_uncerts, uncerts_to_fix, year, regions, technique_str, use_QCD_Pt, debug   )
				
				draw_uncerts_combined_BR(all_uncerts, year, regions, technique_str,use_QCD_Pt, debug)

				for sample in samples:
					draw_uncerts(all_uncerts, sample, year, regions, technique_str,use_QCD_Pt,debug)
