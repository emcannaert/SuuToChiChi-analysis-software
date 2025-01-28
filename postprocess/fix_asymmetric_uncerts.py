import ROOT
import sys,os
from math import sqrt


#### operates on the final, linearized files that go to combine in order to fix asymmetrix uncertainties, mainly JECs
#### the "fixed" outputs are written to the postprocess/finalCombineFiles/correctedFinalCombineFiles/

ROOT.gErrorIgnoreLevel = ROOT.kWarning


def fix_uncerts(samples,mass_point, all_uncerts,uncerts_to_fix, year, region, useMask=False, debug = False):
	ROOT.TH1.AddDirectory(False)
	ROOT.TH1.SetDefaultSumw2()
	ROOT.TH2.SetDefaultSumw2()



	###########################
	## meta variables to change
	###########################


	asymmetry_threshold              = 0.4     ## value below which symmetry will be forced for a NP. Set to some large value to force all NPs to be symmetrix 
	fix_small_sandwiched_uncerts     = False
	fix_opposite_sided_uncertainties = False
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

	infile_dir = "finalCombineFilesNewStats/"
	infile_name = infile_dir+ "combine_%s_%s.root"%(year,mass_point)

	outfile_dir = "finalCombineFilesNewStats/correctedFinalCombineFiles/"
	outfile_name = outfile_dir + "combine_%s_%s.root"%(year,mass_point)

	if useMask:
		infile_dir = "finalCombineFilesNewStats/maskedFinalCombineFiles/"
		infile_name = infile_dir+ "combine_%s_%s.root"%(year,mass_point)

		outfile_dir = "finalCombineFilesNewStats/maskedCorrectedFinalCombineFiles/"
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
				#if uncert_to_fix_ == "CMS_jec": continue # this is not set up
				if uncert_to_fix_ == "CMS_topPt" and sample not in ["allBR","TTbar", "TTTo"] : continue
				if uncert_to_fix_ not in ["nom"] and sample == "data_obs": continue # data_obs only has this one uncertainty 
				if (sample == "sig" or sample == "WJets"    )and "stat" in uncert_to_fix_: continue
				uncert_to_fix = uncert_to_fix_
				if uncert_to_fix in ["CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_scale"] :
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
					hist_nom.Write();
					continue # don't want to do any of the up/down stuff for nom hist

				else:
					## get up hist
					if debug: print("Looking for up histogram ", folder_name+hist_name+"Up" )
					hist_up = infile.Get(folder_name+hist_name+"Up")
					## get down hist
					if debug: print("Looking for down histogram ", folder_name+hist_name+"Down" )
					hist_down = infile.Get(folder_name+hist_name+"Down")



				#print("Cloning up and down histograms")
				#create doppelganger histograms to go into the "corrected" file
				hist_up_corr 	  = hist_up.Clone() ## could be some problem with multiple histograms having the same name?
				hist_down_corr    = hist_down.Clone()

				hist_up_corr.Sumw2()
				hist_down_corr.Sumw2()


				if debug: print("uncorrected hist names are %s/%s/%s."%(hist_nom.GetName(), hist_up.GetName(), hist_down.GetName() ))

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



						### ONLY DO THIS IF up/down ratios are less than define threshold
						if ( abs(distance_up)/abs(distance_down) < asymmetry_threshold) or (abs(distance_down)/abs(distance_up)  < asymmetry_threshold):

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

							hist_up_corr.SetBinError(iii, sqrt(abs(new_yield_up)) ) 
							hist_down_corr.SetBinError(iii, sqrt(abs(new_yield_down)) ) 

					## at this point, the up/down uncertainties should be matched pretty well
					## now go through the bins AGAIN now that they have been 'corrected' and check for large adjacent variations




					if fix_small_sandwiched_uncerts:
						for iii in range(1, hist_up.GetNbinsX()+1):

							## FIX UNCERTAINTY VARIATIONS THAT ARE VASTLY DIFFERENT TO NEIGHBORING BIN VARIATIONS

							####### up uncertainty
							## THREE CASES:

							direction_threshold = 0
							if fix_opposite_sided_uncertainties: direction_threshold = -5  

							yield_nom = hist_nom.GetBinContent(iii)
							new_yield_up = hist_up_corr.GetBinContent(iii)
							new_yield_down = hist_down_corr.GetBinContent(iii)

							variation_up_nom = abs( new_yield_up - yield_nom )


							direction_up_nom = 1
							if (new_yield_up - yield_nom) > 0:
								direction_up_nom = (new_yield_up - yield_nom) / abs( new_yield_up - yield_nom)   ## positive if it's a positive variation

							variation_down_nom = abs( yield_nom - new_yield_down   )
							direction_down_nom = 1
							if (yield_nom - new_yield_down) > 0:
								direction_down_nom = (new_yield_down - yield_nom) / abs( yield_nom - new_yield_down)   ## positive if it's a positive variation


							ratio_up_nom = 0
							ratio_down_nom = 0

							if yield_nom > 0:
								ratio_up_nom = variation_up_nom / yield_nom
								ratio_down_nom = variation_down_nom / yield_nom

							## by this we have variation = yield_nom + direction * variation

							## CASE 1: this is an 'internal' bin (not first or last)
							if iii != 1 and iii != hist_nom.GetNbinsX():

								####### up uncertainty 
								yield_nom_iplus1  = hist_nom.GetBinContent(iii+1)
								yield_up_iplus1  = hist_up_corr.GetBinContent(iii+1)

								yield_nom_iminus1  = hist_nom.GetBinContent(iii-1)
								yield_up_iminus1  = hist_up_corr.GetBinContent(iii-1)


								variation_up_nom_iplus1 = abs( yield_up_iplus1 - yield_nom_iplus1 )
								direction_up_nom_iplus1 = 1
								if abs(yield_up_iplus1 - yield_nom_iplus1) > 0:
									direction_up_nom_iplus1 = ( yield_up_iplus1 - yield_nom_iplus1) / abs(( yield_up_iplus1 - yield_nom_iplus1)  )

								variation_up_nom_iminus1 = abs( yield_up_iminus1 - yield_nom_iminus1 )
								direction_up_nom_iminus1 = 1
								if abs(yield_up_iminus1 - yield_nom_iminus1) > 0:
									direction_up_nom_iminus1 = ( yield_up_iminus1 - yield_nom_iminus1) / abs(( yield_up_iminus1 - yield_nom_iminus1)  )


								if (direction_up_nom_iplus1/direction_up_nom_iminus1) > direction_threshold:

									## get the up/nom variation ratios for the neighbor bins

									ratio_up_nom_iplus1 = 0.0
									if yield_nom_iplus1 > 0:
										ratio_up_nom_iplus1 = variation_up_nom_iplus1 / yield_nom_iplus1
									ratio_up_nom_iminus1 = 0.0
									if yield_nom_iplus1 > 0:
										ratio_up_nom_iminus1 =  variation_up_nom_iminus1 / yield_nom_iplus1


									if ratio_up_nom_iplus1 > 2.0 or ratio_up_nom_iminus1 >2.0: continue

									avg_ratio_plus_minus_1 = 0.0
									if (ratio_up_nom_iplus1 + ratio_up_nom_iminus1) > 0:
										avg_ratio_plus_minus_1 = ( ratio_up_nom_iplus1 + ratio_up_nom_iminus1 ) / 2.0


									iplus_sign = "+"
									if direction_up_nom_iplus1 < 0:
										iplus_sign = "-"
									i_sign = "+"
									if direction_up_nom < 0:
										i_sign = "-"
									iminus1_sign = "-"
									if direction_up_nom_iminus1 < 0:
										iminus1_sign = "-"

									if (avg_ratio_plus_minus_1 > 0 and ((ratio_up_nom / avg_ratio_plus_minus_1) < bin_variation_ratio_threshold)) or (fix_opposite_sided_uncertainties and direction_up_nom*direction_up_nom_iplus1 < 0 and direction_up_nom_iplus1*direction_up_nom_iminus1 > 0) : # if this, then there is a problem      and ( direction_up_nom * direction_up_nom_iplus1 > 0  )


										## set the new up variation to be equal to nom_yield + average_ratio_plus_minus_1 * direction_up_iplus1 * nom_yield
										new_yield_up = yield_nom + direction_up_nom_iplus1 * avg_ratio_plus_minus_1 * yield_nom

										if debug:
											print(" ------------------ Changing bin with up bin i variation --- %s --- when i+1/i-1 variations are ---- %s/%s ---- (%s/%s directions). Directions of bins i-1/i/i+1 go like $$$    %s%s%s     $$$    .Yield changed to ----- %s. "%(ratio_up_nom, ratio_up_nom_iplus1, ratio_up_nom_iminus1,direction_up_nom_iplus1,direction_up_nom_iminus1, iminus1_sign,i_sign,iplus_sign, new_yield_up   )  )
											print("yield_nom = %s  /  direction_up_nom_iplus1  = %s /  avg_ratio_plus_minus_1 = %s / yield_nom = %s."%( yield_nom, direction_up_nom_iplus1,avg_ratio_plus_minus_1 ,yield_nom))
									else:
										if debug: print("bin %s up variation NOT changed. Bin i variation --- %s --- when i+1/i-1 variations are ---- %s/%s ---- (%s/%s directions). Directions of bins i-1/i/i+1 go like $$$    %s%s%s     $$$     "%(iii,ratio_up_nom, ratio_up_nom_iplus1, ratio_up_nom_iminus1,direction_up_nom_iplus1,    direction_up_nom_iminus1,  iminus1_sign,i_sign,iplus_sign,   )  )



								####### down uncertainty 
								yield_nom_iplus1   = hist_nom.GetBinContent(iii+1)
								yield_down_iplus1  = hist_down_corr.GetBinContent(iii+1)

								yield_nom_iminus1  = hist_nom.GetBinContent(iii-1)
								yield_down_iminus1  = hist_down_corr.GetBinContent(iii-1)


								variation_down_nom_iplus1 = abs( yield_down_iplus1 - yield_nom_iplus1 )
								direction_down_nom_iplus1 = 1
								if abs(yield_down_iplus1 - yield_nom_iplus1) > 0:
									direction_down_nom_iplus1 = ( yield_down_iplus1 - yield_nom_iplus1) / abs(( yield_down_iplus1 - yield_nom_iplus1)  )

								variation_down_nom_iminus1 = abs( yield_down_iminus1 - yield_nom_iminus1 )
								direction_down_nom_iminus1 = 1
								if abs(yield_down_iminus1 - yield_nom_iminus1) > 0:
									direction_down_nom_iminus1 = ( yield_down_iminus1 - yield_nom_iminus1) / abs(( yield_down_iminus1 - yield_nom_iminus1)  )

								## make sure the plus and minus 1 variations are in the same direction

								if (direction_down_nom_iplus1/direction_down_nom_iminus1) > direction_threshold:

									## get the down/nom variation ratios for the neighbor bins

									ratio_down_nom_iplus1 = 0.0
									if yield_nom_iplus1 > 0:
										ratio_down_nom_iplus1 = variation_down_nom_iplus1 / yield_nom_iplus1
									ratio_down_nom_iminus1 = 0.0
									if yield_nom_iplus1 > 0:
										ratio_down_nom_iminus1 =  variation_down_nom_iminus1 / yield_nom_iplus1


									if ratio_down_nom_iplus1 > 2.0 or ratio_down_nom_iminus1 >2.0: continue


									avg_ratio_plus_minus_1 = 0.0
									if (ratio_down_nom_iplus1 + ratio_down_nom_iminus1) > 0:
										avg_ratio_plus_minus_1 = ( ratio_down_nom_iplus1 + ratio_down_nom_iminus1 ) / 2.0

									iplus_sign = "+"
									if direction_up_nom_iplus1 < 0:
										iplus_sign = "-"
									i_sign = "+"
									if direction_up_nom < 0:
										i_sign = "-"
									iminus1_sign = "-"
									if direction_up_nom_iminus1 < 0:
										iminus1_sign = "-"
									if (avg_ratio_plus_minus_1 > 0 and ((ratio_down_nom / avg_ratio_plus_minus_1) < bin_variation_ratio_threshold)) or (fix_opposite_sided_uncertainties and direction_down_nom*direction_down_nom_iplus1 < 0 and  direction_down_nom_iplus1*direction_down_nom_iminus1 > 0) : # if this, then there is a problem      and ( direction_down_nom * direction_down_nom_iplus1 > 0  )


										## set the new down variation to be equal to nom_yield + average_ratio_plus_minus_1 * direction_down_iplus1 * nom_yield


										new_yield_down = yield_nom + direction_down_nom_iplus1 * avg_ratio_plus_minus_1 * yield_nom
										if debug:
											print(" ------------------ Changing bin with down bin i variation --- %s --- when i+1/i-1 variations are ---- %s/%s ---- (%s/%s directions). Directions of bins i-1/i/i+1 go like $$$    %s%s%s     $$$    .Yield changed to ----- %s. "%(ratio_down_nom, ratio_down_nom_iplus1, ratio_down_nom_iminus1,direction_down_nom_iplus1,direction_down_nom_iminus1, iminus1_sign,i_sign,iplus_sign, new_yield_down   )  )
											print("yield_nom = %s  /  direction_down_nom_iplus1  = %s /  avg_ratio_plus_minus_1 = %s / yield_nom = %s."%( yield_nom, direction_down_nom_iplus1,avg_ratio_plus_minus_1 ,yield_nom))

									else:
										if debug: print("bin %s down variation NOT changed. Bin i variation --- %s --- when i+1/i-1 variations are ---- %s/%s ---- (%s/%s directions). Directions of bins i-1/i/i+1 go like $$$    %s%s%s     $$$     "%(iii,ratio_down_nom, ratio_down_nom_iplus1, ratio_down_nom_iminus1,direction_down_nom_iplus1,    direction_down_nom_iminus1,  iminus1_sign,i_sign,iplus_sign,   )  )

										#print("i variation ratio is %s, i+1/i-1 variation ratios are %s/%s. downdating new variation ratio to %s."% (ratio_down_nom, ratio_down_nom_iplus1, ratio_down_nom_iminus1, avg_ratio_plus_minus_1 ))

							"""## CASE 2: this is the first bin, so match the variation of bin 1
							elif iii == 1:

								yield_nom_iplus1 = hist_nom.GetBinContent(iii+1)
								yield_up_iplus1  = hist_up.GetBinContent(iii+1)

								yield_nom_iplus2 = hist_nom.GetBinContent(iii+2)
								yield_up_iplus2  = hist_up.GetBinContent(iii+2)

								## use linear function to estimate the new variations

							## CASE 3: this is the last bin, so match the varition of the second to last bin
							elif iii == hist_nom.GetNbinsX():

								yield_nom_iminus1  = hist_nom.GetBinContent(iii-1)
								yield_up_iminus1   = hist_up.GetBinContent(iii-1)

								yield_nom_iminus2  = hist_nom.GetBinContent(iii-2)
								yield_up_iminus2   = hist_up.GetBinContent(iii-2)"""


							## now set the corrected histogram bin values 


							new_yield_up = max(0, new_yield_up)   ## yields can never be 0
							new_yield_down = max(0,new_yield_down)

							hist_up_corr.SetBinContent(iii,new_yield_up)
							hist_down_corr.SetBinContent(iii,new_yield_down)

							hist_up_corr.SetBinError(iii, sqrt( abs(new_yield_up)) ) 
							hist_down_corr.SetBinError(iii, sqrt(abs(new_yield_down)) ) 	



						# now go over the corrected bins AGAIN and see make sure they are symmetric
								## use linear function to estimate the new variations
						for iii in range(1, hist_up.GetNbinsX()+1):
							## (1) find direction (relative to the nom) the furthest uncertainty is 
							## (2) set the other uncertainty to be in the opposite direction

							yield_nom = hist_nom.GetBinContent(iii)
							yield_up = hist_up_corr.GetBinContent(iii)
							yield_down = hist_down_corr.GetBinContent(iii)

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

							hist_up_corr.SetBinError(iii, sqrt(abs(new_yield_up)) ) 
							hist_down_corr.SetBinError(iii, sqrt( abs(new_yield_down)) ) 


				#print("fixed uncertainty")
				## write histogram to file 
				else:
					if debug: print("Not fixing %s."%(uncert_to_fix))


				if debug: print("corrected up/down hist names are %s/%s."%(hist_up_corr.GetName(), hist_down_corr.GetName() ))


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
	all_uncerts = ["nom",  "CMS_bTagSF_M" , "CMS_bTagSF_T", "CMS_jer", "CMS_jec",  "CMS_bTagSF_M_corr" , "CMS_bTagSF_T_corr",  "CMS_bTagSF_bc_T_corr",	   "CMS_bTagSF_light_T_corr",	   "CMS_bTagSF_bc_M_corr",	   "CMS_bTagSF_light_M_corr",	  "CMS_bTagSF_bc_T_year",		"CMS_bTagSF_light_T_year",	  "CMS_bTagSF_bc_M_year",	   "CMS_bTagSF_light_M_year",		 "CMS_jer_eta193", "CMS_jer_193eta25",  "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal",   "CMS_jec_Absolute", "CMS_jec_BBEC1_year",	"CMS_jec_Absolute_year",  "CMS_jec_RelativeSample_year", "CMS_pu", "CMS_topPt", "CMS_L1Prefiring", "CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory", "CMS_jec_AbsolutePU",   "CMS_jec_AbsoluteScale" ,   "CMS_jec_Fragmentation" , "CMS_jec_AbsoluteMPFBias",  "CMS_jec_RelativeFSR", "CMS_scale"]  ## systematic namings for cards   "CMS_btagSF", 
	#uncerts_to_fix = [ "CMS_jer",  "cms_jec",  "CMS_jer_eta193", "CMS_jer_193eta25","CMS_jec_HF", "CMS_jec_BBEC1", "CMS_jec_EC2", "CMS_jec_Absolute", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year", "CMS_jec_RelativeSample_year", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory", "CMS_jec_AbsolutePU", "CMS_bTagSF_bc_M_year",       "CMS_bTagSF_light_M_year",  "CMS_bTagSF_M",  "CMS_bTagSF_T" ]   # name of uncertainty to fix (proper name as written in the linearized root files)
	
	uncerts_to_fix =  [ "CMS_jer", "CMS_jec", "CMS_bTagSF_M" ,  "CMS_bTagSF_T",  "CMS_bTagSF_M_corr" , "CMS_bTagSF_T_corr",   "CMS_bTagSF_bc_T_corr", "CMS_bTagSF_light_T_corr",  "CMS_bTagSF_bc_M_corr", "CMS_bTagSF_light_M_corr", "CMS_bTagSF_bc_T_year",  "CMS_bTagSF_light_T_year",  
	     "CMS_bTagSF_bc_M_year",       "CMS_bTagSF_light_M_year",  "CMS_jer_eta193", "CMS_jer_193eta25", "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal",
	      "CMS_jec_HF", "CMS_jec_BBEC1", "CMS_jec_EC2", "CMS_jec_Absolute", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year",
	       "CMS_jec_RelativeSample_year", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory", "CMS_jec_AbsolutePU",  "CMS_pu",  "CMS_jec_AbsoluteScale" ,   "CMS_jec_Fragmentation" , "CMS_jec_AbsoluteMPFBias",  "CMS_jec_RelativeFSR"]  ## systematic namings for cards   "CMS_btagSF",  ,   "CMS_bTagSF_bc_T",      "CMS_bTagSF_light_T",       "CMS_bTagSF_bc_M",       "CMS_bTagSF_light_M", 



	#SOME DAY SWITCH TO THESE 
	#	self.systematic_names = ["nom",  "CMS_bTagSF_M" , "CMS_bTagSF_T", "CMS_jer", "CMS_jec",   "CMS_bTagSF_bc_T",       "CMS_bTagSF_light_T",       "CMS_bTagSF_bc_M",       "CMS_bTagSF_light_M",      "CMS_bTagSF_bc_T_year",        "CMS_bTagSF_light_T_year",      "CMS_bTagSF_bc_M_year",       "CMS_bTagSF_light_M_year",         "CMS_jer_eta193", "CMS_jer_193eta25",  "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal",   "CMS_jec_Absolute", "CMS_jec_BBEC1_year",    "CMS_jec_Absolute_year",       "CMS_jec_RelativeSample_year", "CMS_pu", "CMS_topPt", "CMS_L1Prefiring", "CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory", "CMS_jec_AbsolutePU",   "CMS_jec_AbsoluteScale" ,   "CMS_jec_Fragmentation" , "CMS_jec_AbsoluteMPFBias".  "CMS_jec_RelativeFSR"]  ## systematic namings for cards   "CMS_btagSF", 

	#uncerts_to_fix =  [ "CMS_jer", "cms_jec", "CMS_bTagSF_M" ,  "CMS_bTagSF_T",    "CMS_bTagSF_bc_T",      
	# "CMS_bTagSF_light_T",       "CMS_bTagSF_bc_M",       "CMS_bTagSF_light_M",      "CMS_bTagSF_bc_T_year",        "CMS_bTagSF_light_T_year",  
	#     "CMS_bTagSF_bc_M_year",       "CMS_bTagSF_light_M_year",         "CMS_jer_eta193", "CMS_jer_193eta25", "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal",
	#     "CMS_jec_Absolute", "CMS_jec_BBEC1_year",  "CMS_jec_Absolute_year",  "CMS_jec_AbsoluteScale" ,   "CMS_jec_Fragmentation" , "CMS_jec_AbsoluteMPFBias".  "CMS_jec_RelativeFSR",
	#       "CMS_jec_RelativeSample_year", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory", "CMS_jec_AbsolutePU", "stat"]  ## systematic namings for cards   "CMS_btagSF",  ,  


	years = ["2015","2016","2017","2018"]
	regions = ["SR","CR","AT1b","AT0b"]
	if include_ATxtb:    regions.extend( [ "AT1tb", "AT0tb" ]  )
	if include_sideband: regions.extend( [ "SB1b", "SB0b" ]  )

	samples = ["allBR", "QCD","TTbar", "ST", "sig", "WJets","data_obs"] 

	if include_WJets: samples.extend( ["WJets"] )
	if include_TTTo:  samples.extend( ["TTTo"] )

	mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1", "Suu5_chi1p5", "Suu5_chi2", "Suu6_chi1","Suu6_chi1p5","Suu6_chi2","Suu6_chi2p5","Suu7_chi1","Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3","Suu8_chi1","Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"]


	#### debugging stuff
	if debug:
		#uncerts_to_fix =  ["CMS_jec_AbsolutePU"] 
		years = ["2015"]
		#samples = ["QCD"]
		#regions = ["SR"]
		mass_points = ["Suu4_chi1"]


	for year in years:
			for mass_point in mass_points:
					#try:
					fix_uncerts( samples, mass_point, all_uncerts, uncerts_to_fix, year, regions, True, debug   )
					fix_uncerts( samples, mass_point, all_uncerts, uncerts_to_fix, year, regions, False, debug   )

					#except: 
					#print("ERROR: failed %s/%s"%(mass_point,year))



