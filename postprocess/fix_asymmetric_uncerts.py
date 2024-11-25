import ROOT
import sys,os
from math import sqrt


#### operates on the final, linearized files that go to combine in order to fix asymmetrix uncertainties, mainly JECs
#### the "fixed" outputs are written to the postprocess/finalCombineFiles/correctedFinalCombineFiles/

ROOT.gErrorIgnoreLevel = ROOT.kWarning

def fix_uncerts(samples,mass_point, all_uncerts,uncerts_to_fix, year, region):
	ROOT.TH1.AddDirectory(False)
	ROOT.TH1.SetDefaultSumw2()
	ROOT.TH2.SetDefaultSumw2()

	## list of uncorrelated systematics to the correct hist name is grabbed
	uncorrelated_systematics = [ "CMS_pu",  "CMS_jec", "CMS_jer","CMS_jer_eta193", "CMS_jer_193eta25", "CMS_L1Prefiring","CMS_bTagSF_M", "CMS_bTagSF_T", "CMS_bTagSF_bc_T_year", "CMS_bTagSF_light_T_year", "CMS_bTagSF_bc_M_year","CMS_bTagSF_light_M_year", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year", "CMS_jec_RelativeSample_year", "stat"] ## systematics that are correlated (will not have year appended to names)     "CMS_btagSF",


	year_str = "16preAPV"
	if year == "2016":
		year_str = "16"
	elif year == "2017":
		year_str = "17"
	elif year == "2018":
		year_str = "18"

	infile_dir = "finalCombineFilesNewStats/"
	infile_name = infile_dir+ "combine_%s_%s.root"%(year,mass_point)

	outfile_dir = "finalCombineFilesNewStats/correctedFinalCombineFiles/"
	outfile_name = outfile_dir + "combine_%s_%s.root"%(year,mass_point)

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
			hist_nom = infile.Get(folder_name + sample )


			
			for uncert_to_fix_ in all_uncerts: 


				### things to skip
				if uncert_to_fix_ == "CMS_jec": continue # this is not set up
				if uncert_to_fix_ == "CMS_topPt" and sample != "TTbar": continue
				if uncert_to_fix_ not in ["nom"] and sample == "data_obs": continue # data_obs only has this one uncertainty 
				if sample == "sig" and "stat" in uncert_to_fix_: continue
				uncert_to_fix = uncert_to_fix_
				if uncert_to_fix == "CMS_pdf" or uncert_to_fix == "CMS_renorm" or uncert_to_fix == "CMS_fact":
					if sample == "QCD": uncert_to_fix+= "_QCD"
					elif sample == "TTbar": uncert_to_fix+= "_TTbar"
					elif sample == "ST": continue
					elif sample == "allBR": uncert_to_fix+= "_allBR"
					elif sample == "sig": uncert_to_fix+= "_sig"

				#try: 
				## get the histogram for this uncert/year/sample/region

				print("-----running %s/%s/%s/%s"%(sample, region, uncert_to_fix,year))
				uncert_to_fix_str = uncert_to_fix
				if uncert_to_fix in uncorrelated_systematics: uncert_to_fix_str += year_str
				hist_name = "%s_%s"%(sample, uncert_to_fix_str)

				if uncert_to_fix == "nom":
					#print("Getting nom histogram.")
					hist_nom.Write();
					continue # don't want to do any of the up/down stuff for nom hist

				else:
					## get up hist
					print("Looking for up histogram ", folder_name+hist_name+"Up" )
					hist_up = infile.Get(folder_name+hist_name+"Up")
					## get down hist
					print("Looking for down histogram ", folder_name+hist_name+"Down" )
					hist_down = infile.Get(folder_name+hist_name+"Down")



				#print("Cloning up and down histograms")
				#create doppelganger histograms to go into the "corrected" file
				hist_up_corr 	  = hist_up.Clone() ## could be some problem with multiple histograms having the same name?
				hist_down_corr    = hist_down.Clone()


				## if this systematic is one to fix ...
				#print("Fixing uncertainties")
				if uncert_to_fix in uncerts_to_fix:
					## loop over all bins
					for iii in range(1, hist_up.GetNbinsX()+1):
						## (1) find direction (relative to the nom) the furthest uncertainty is 
						## (2) set the other uncertainty to be in the opposite direction

						yield_nom = hist_nom.GetBinContent(iii)
						yield_up = hist_up.GetBinContent(iii)
						yield_down = hist_down.GetBinContent(iii)

						distance_up   = yield_up - yield_nom
						distance_down = yield_down - yield_nom

						## find which uncertainty is further from nom ( abs(up - nom) / abs(nom - down)   )
						if abs(distance_up) > abs(distance_down): 
							distance_down = -1*distance_up

						else:
							distance_up = -1*distance_down


						## set bin content (and bin error) for the new, "corrected" histogram 

						new_yield_up = max(0, yield_nom + distance_up)
						new_yield_down = max(0,yield_nom + distance_down)
						hist_up_corr.SetBinContent(iii,new_yield_up)
						hist_down_corr.SetBinContent(iii,new_yield_down)

						hist_up_corr.SetBinError(iii, sqrt(new_yield_up) ) 
						hist_down_corr.SetBinError(iii, sqrt(new_yield_down) ) 
				#print("fixed uncertainty")
				## write histogram to file 
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
	

	all_uncerts =  ["nom",  "CMS_bTagSF_M" ,  "CMS_bTagSF_T",    "CMS_bTagSF_bc_T",       "CMS_bTagSF_light_T",       "CMS_bTagSF_bc_M",       "CMS_bTagSF_light_M",      "CMS_bTagSF_bc_T_year",        "CMS_bTagSF_light_T_year",      "CMS_bTagSF_bc_M_year",       "CMS_bTagSF_light_M_year",         "CMS_jer_eta193", "CMS_jer_193eta25", "CMS_jec",  "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal", "CMS_jec_HF", "CMS_jec_BBEC1", "CMS_jec_EC2", "CMS_jec_Absolute", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year", "CMS_jec_RelativeSample_year", "CMS_pu", "CMS_topPt", "CMS_L1Prefiring", "CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory", "CMS_jec_AbsolutePU", "stat"]  ## systematic namings for cards   "CMS_btagSF",  "CMS_jer",  
	uncerts_to_fix = [ "CMS_jer",    "CMS_jer_eta193", "CMS_jer_193eta25","CMS_jec_HF", "CMS_jec_BBEC1", "CMS_jec_EC2", "CMS_jec_Absolute", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year", "CMS_jec_RelativeSample_year", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory", "CMS_jec_AbsolutePU", "CMS_bTagSF_bc_M_year",       "CMS_bTagSF_light_M_year"]   # name of uncertainty to fix (proper name as written in the linearized root files)
	years = ["2015","2016","2017","2018"]
	regions = ["SR","CR","AT1b","AT0b"]
	samples = ["allBR", "QCD","TTbar", "ST", "sig", "data_obs"] 
	mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1", "Suu5_chi1p5", "Suu5_chi2", "Suu6_chi1","Suu6_chi1p5","Suu6_chi2","Suu6_chi2p5","Suu7_chi1","Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3","Suu8_chi1","Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"]

	for year in years:
			for mass_point in mass_points:
					#try:
					fix_uncerts( samples, mass_point, all_uncerts, uncerts_to_fix, year, regions   )
					#except: 
					#print("ERROR: failed %s/%s"%(mass_point,year))



