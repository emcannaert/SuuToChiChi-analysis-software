import ROOT
import sys,os
from math import sqrt


#### operates on the final, linearized files that go to combine in order to fix asymmetrix uncertainties, mainly JECs
#### the "fixed" outputs are written to the postprocess/finalCombineFiles/correctedFinalCombineFiles/











##### THIS DOES NOT WORK DUE TO ROOT LIMITATIONS











ROOT.gErrorIgnoreLevel = ROOT.kWarning

def load_bin_masks(year,region, technique_str):	# load in the superbin indices (located in a text file )
	_superbin_indices = []
	bin_map_path         = "region_masks/"
	open_file = open(bin_map_path+"/full_bin_masks_%s.txt"%(year),"r")
	#print("Got superbin index file %s."%( bin_map_path+"/superbin_indices%s_%s.txt"%(technique_str,year)  ))
	for line in open_file:
		columns = line.split('/')
		if columns[0] == year and columns[1] == region and columns[2] == technique_str:
			_superbin_indices = columns[3]
	open_file.close()
	return ast.literal_eval(_superbin_indices)



def fix_uncerts(samples,mass_point, all_uncerts, regions_to_mask, year, region, technique_str, fixCorrected = False, debug = False):
	ROOT.TH1.AddDirectory(False)
	ROOT.TH1.SetDefaultSumw2()
	ROOT.TH2.SetDefaultSumw2()


	###########################
	## meta variables to change
	###########################
	fix_small_sandwiched_uncerts     = True
	fix_opposite_sided_uncertainties = True
	bin_variation_ratio_threshold     = 0.15 # the ratio of bin_i variation / bin_i+-1 variation that determines if a bin needs to be changed manually


	## list of uncorrelated systematics to the correct hist name is grabbed
	uncorrelated_systematics = [ "CMS_pu",  "CMS_jec", "CMS_jer","CMS_jer_eta193", "CMS_jer_193eta25", "CMS_L1Prefiring","CMS_bTagSF_M", "CMS_bTagSF_T", "CMS_bTagSF_bc_T_year", "CMS_bTagSF_light_T_year", "CMS_bTagSF_bc_M_year","CMS_bTagSF_light_M_year", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year", "CMS_jec_RelativeSample_year", "stat"] ## systematics that are correlated (will not have year appended to names)     "CMS_btagSF",


	year_str = "16preAPV"
	if year == "2016":
		year_str = "16"
	elif year == "2017":
		year_str = "17"
	elif year == "2018":
		year_str = "18"

	if fixCorrected: 
		infile_dir =  "finalCombineFilesNewStats/correctedFinalCombineFiles/"
		outfile_dir = "finalCombineFilesNewStats/maskedCorrectedFinalCombineFiles/"
	else: 
		infile_dir = "finalCombineFilesNewStats/"
		outfile_dir = "finalCombineFilesNewStats/maskedFinalCombineFiles/"


	infile_name  = infile_dir  + "combine_%s%s_%s.root"%(year,technique_str, mass_point)
	outfile_name = outfile_dir + "combine_%s%s_%s.root"%(year,technique_str, mass_point)

	print("Looking for file %s"%(infile_name))

	## open root file
	infile = ROOT.TFile(infile_name,"r")
	outfile = ROOT.TFile(outfile_name,"RECREATE")


	for region in regions:

		## create a folder in the root file and CD into it
		region_folder = outfile.mkdir(region);
		region_folder.cd() ## cd into the new folder (matching the structure of the input file)


		for sample in samples: # name of BR type to fix
			folder_name = region + "/"

			## get nom histogram for this region and sample
			#print("Getting nominal histogram ", folder_name + sample )


			
			for uncert_to_fix_ in all_uncerts: 

				bin_mask = load_bin_masks(year,region, technique_str)

				### things to skip
				#if uncert_to_fix_ == "CMS_jec": continue # this is not set up
				if uncert_to_fix_ == "CMS_topPt" and sample not in ["allBR","TTbar", "TTTo"] : continue
				if uncert_to_fix_ not in ["nom"] and sample == "data_obs": continue # data_obs only has this one uncertainty 
				if (sample == "sig" or sample == "WJets"    )and "stat" in uncert_to_fix_: continue
				uncert_to_fix = uncert_to_fix_
				if uncert_to_fix == "CMS_pdf" or uncert_to_fix == "CMS_renorm" or uncert_to_fix == "CMS_fact":
					if sample == "QCD": uncert_to_fix+= "_QCD"
					elif  "TTTo" in sample: uncert_to_fix+= "_TTbar"
					elif sample == "TTbar": uncert_to_fix+= "_TTbar"
					elif sample == "WJets": uncert_to_fix+= "_WJets"
					elif sample == "ST": continue
					elif sample == "allBR": uncert_to_fix+= "_allBR"
					elif sample == "sig": uncert_to_fix+= "_sig"

				#try: 
				## get the histogram for this uncert/year/sample/region

				if debug: print("-----running %s/%s/%s/%s"%(sample, region, uncert_to_fix,year))
				uncert_to_fix_str = uncert_to_fix
				if uncert_to_fix in uncorrelated_systematics: uncert_to_fix_str += year_str
				hist_name = "%s_%s"%(sample, uncert_to_fix_str)

				if uncert_to_fix == "nom":
					#print("Getting nom histogram.")


					hist_nom = infile.Get(folder_name + sample )


					hist_nom.Write();








				else:
					## get up hist
					if debug: print("Looking for up histogram ", folder_name+hist_name+"Up" )
					hist_up = infile.Get(folder_name+hist_name+"Up")
					## get down hist
					if debug: print("Looking for down histogram ", folder_name+hist_name+"Down" )
					hist_down = infile.Get(folder_name+hist_name+"Down")


					# get the bin mask


					### create new histogram here with the correct dimensions


					up_hist_main_title   = hist_up.GetTitle()
					down_hist_main_title = hist_down.GetTitle()

					new_hist_xaxis_title = hist_up.GetXaxis().GetTitle()
					new_hist_yaxis_title = hist_up.GetYaxis().GetTitle()

					new_hist_nbins = hist_up.GetNbinsX()
					new_hist_xmin = hist_up.GetXaxis().GetXmin()
					new_hist_xmax = hist_up.GetXaxis().GetXmax()

					#print("Cloning up and down histograms")
					#create doppelganger histograms to go into the "corrected" file
					hist_up_corr 	  = #hist_up.Clone() ## could be some problem with multiple histograms having the same name?
					hist_down_corr    = #hist_down.Clone()

					hist_up_corr.Sumw2()
					hist_down_corr.Sumw2()
			
					hist_up_corr.Write();
					hist_down_corr.Write();


				#print("wrote histograms")
				#except: 
				#	print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$     Failed for %s/%s/%s/%s/%s"%(sample,uncert_to_fix,mass_point,year,region))
		# cd to outside folder of root file to move onto a new systematic
		outfile.cd()					
	print("Wrote histograms to %s"%outfile_dir)
	## close all histograms
	infile.Close()
	outfile.Close()


if __name__=="__main__":
	
	debug = False
	include_ATxtb    = False
	include_sideband = False

	include_WJets    = True
	include_TTTo     = True
	all_uncerts = ["nom",  "CMS_bTagSF_M" , "CMS_bTagSF_T", "CMS_jer", "CMS_jec",  "CMS_bTagSF_M_corr" , "CMS_bTagSF_T_corr",  "CMS_bTagSF_bc_T_corr",	   "CMS_bTagSF_light_T_corr",	   "CMS_bTagSF_bc_M_corr",	   "CMS_bTagSF_light_M_corr",	  "CMS_bTagSF_bc_T_year",		"CMS_bTagSF_light_T_year",	  "CMS_bTagSF_bc_M_year",	   "CMS_bTagSF_light_M_year",		 "CMS_jer_eta193", "CMS_jer_193eta25",  "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal",   "CMS_jec_Absolute", "CMS_jec_BBEC1_year",	"CMS_jec_Absolute_year",  "CMS_jec_RelativeSample_year", "CMS_pu", "CMS_topPt", "CMS_L1Prefiring", "CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory", "CMS_jec_AbsolutePU",   "CMS_jec_AbsoluteScale" ,   "CMS_jec_Fragmentation" , "CMS_jec_AbsoluteMPFBias",  "CMS_jec_RelativeFSR"]  ## systematic namings for cards   "CMS_btagSF", 
	#uncerts_to_fix = [ "CMS_jer",  "cms_jec",  "CMS_jer_eta193", "CMS_jer_193eta25","CMS_jec_HF", "CMS_jec_BBEC1", "CMS_jec_EC2", "CMS_jec_Absolute", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year", "CMS_jec_RelativeSample_year", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory", "CMS_jec_AbsolutePU", "CMS_bTagSF_bc_M_year",       "CMS_bTagSF_light_M_year",  "CMS_bTagSF_M",  "CMS_bTagSF_T" ]   # name of uncertainty to fix (proper name as written in the linearized root files)



	#SOME DAY SWITCH TO THESE 
	#	self.systematic_names = ["nom",  "CMS_bTagSF_M" , "CMS_bTagSF_T", "CMS_jer", "CMS_jec",   "CMS_bTagSF_bc_T",       "CMS_bTagSF_light_T",       "CMS_bTagSF_bc_M",       "CMS_bTagSF_light_M",      "CMS_bTagSF_bc_T_year",        "CMS_bTagSF_light_T_year",      "CMS_bTagSF_bc_M_year",       "CMS_bTagSF_light_M_year",         "CMS_jer_eta193", "CMS_jer_193eta25",  "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal",   "CMS_jec_Absolute", "CMS_jec_BBEC1_year",    "CMS_jec_Absolute_year",       "CMS_jec_RelativeSample_year", "CMS_pu", "CMS_topPt", "CMS_L1Prefiring", "CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory", "CMS_jec_AbsolutePU",   "CMS_jec_AbsoluteScale" ,   "CMS_jec_Fragmentation" , "CMS_jec_AbsoluteMPFBias".  "CMS_jec_RelativeFSR"]  ## systematic namings for cards   "CMS_btagSF", 

	#uncerts_to_fix =  [ "CMS_jer", "cms_jec", "CMS_bTagSF_M" ,  "CMS_bTagSF_T",    "CMS_bTagSF_bc_T",      
	# "CMS_bTagSF_light_T",       "CMS_bTagSF_bc_M",       "CMS_bTagSF_light_M",      "CMS_bTagSF_bc_T_year",        "CMS_bTagSF_light_T_year",  
	#     "CMS_bTagSF_bc_M_year",       "CMS_bTagSF_light_M_year",         "CMS_jer_eta193", "CMS_jer_193eta25", "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal",
	#     "CMS_jec_Absolute", "CMS_jec_BBEC1_year",  "CMS_jec_Absolute_year",  "CMS_jec_AbsoluteScale" ,   "CMS_jec_Fragmentation" , "CMS_jec_AbsoluteMPFBias".  "CMS_jec_RelativeFSR",
	#       "CMS_jec_RelativeSample_year", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory", "CMS_jec_AbsolutePU", "stat"]  ## systematic namings for cards   "CMS_btagSF",  ,  

	regions_to_mask = ["AT1b"]

	years = ["2015","2016","2017","2018"]
	regions = ["SR","CR","AT1b","AT0b"]
	if include_ATxtb:    regions.extend( [ "AT1tb", "AT0tb" ]  )
	if include_sideband: regions.extend( [ "SB1b", "SB0b" ]  )

	samples = ["allBR", "QCD","TTbar", "ST", "sig", "WJets","data_obs"] 

	if include_WJets: samples.extend( ["WJets"] )
	if include_TTTo:  samples.extend( ["TTTo"] )

	mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1", "Suu5_chi1p5", "Suu5_chi2", "Suu6_chi1","Suu6_chi1p5","Suu6_chi2","Suu6_chi2p5","Suu7_chi1","Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3","Suu8_chi1","Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"]
	technique_strs = ["","NN_"]

	#### debugging stuff
	if debug:
		#uncerts_to_fix =  ["CMS_jec_AbsolutePU"] 
		years = ["2015"]
		#samples = ["QCD"]
		#regions = ["SR"]
		mass_points = ["Suu4_chi1"]




	for year in years:
			for mass_point in mass_points:
				for technique_str in technique_strs:
						#try:


						fix_uncerts( samples, mass_point, all_uncerts, regions_to_mask, year, regions, technique_str, False, debug   )  ## mask the uncorrected files
						if "NN" not in technique_str: fix_uncerts( samples, mass_point, all_uncerts, regions_to_mask, year, regions, technique_str, True,  debug   )   ## mask the corrected files

						#except: 
						#print("ERROR: failed %s/%s"%(mass_point,year))



