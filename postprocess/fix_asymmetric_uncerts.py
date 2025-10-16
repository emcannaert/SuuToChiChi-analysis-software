import ROOT
import sys,os
from math import sqrt
import ast

#### operates on the final, linearized files that go to combine in order to fix asymmetrix uncertainties, mainly JECs
#### the "fixed" outputs are written to the postprocess/finalCombineFiles/correctedFinalCombineFiles/

ROOT.gErrorIgnoreLevel = ROOT.kWarning


def load_superbin_neighbors(year, region,technique_str="",debug=False):

	if debug: print("--- LOADING SUPERBIN NEIGHBORS FOR %s/%s/%s"%(year,region,technique_str))
	region_to_use = "SR"
	if region in ["AT1b", "AT0b"]: region_to_use = "AT1b"

	_superbin_indices = []
	open_file = open("superbinNeighbors/superbin_neighbors%s_%s.txt"%(technique_str,year),"r")
	for line in open_file:
		columns = line.split('/')
		if columns[0] == year and columns[1] == region_to_use:
			_superbin_indices = columns[3]
	open_file.close()

	return ast.literal_eval(_superbin_indices)


def create_directories(dirs_to_create):

	for dir_to_create in dirs_to_create:
		if not os.path.exists(dir_to_create):
			os.makedirs(dir_to_create)


def fix_uncerts(samples,mass_point, all_uncerts,uncerts_to_fix, year, region, technique_str, useMask=False, use_QCD_Pt=False, debug = False):
	ROOT.TH1.AddDirectory(False)
	ROOT.TH1.SetDefaultSumw2()
	ROOT.TH2.SetDefaultSumw2()



	###########################
	## meta variables to change
	###########################




	asymmetry_threshold              = 0.4     ## value below which symmetry will be forced for a NP. Set to some large value to force all NPs to be symmetrix 
	fix_small_sandwiched_uncerts     = True
	fix_opposite_sided_uncertainties = False
	bin_variation_ratio_threshold     = 0.20 # the ratio of bin_i variation / bin_i+-1 variation that determines if a bin needs to be changed manually




	## list of uncorrelated systematics to the correct hist name is grabbed
	uncorrelated_systematics = ["CMS_jec", "CMS_jer","CMS_jer_eta193", "CMS_jer_193eta25", "CMS_L1Prefiring","CMS_bTagSF_M", "CMS_bTagSF_T", "CMS_bTagSF_bc_T_year", "CMS_bTagSF_light_T_year", "CMS_bTagSF_bc_M_year","CMS_bTagSF_light_M_year", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year", "CMS_jec_RelativeSample_year", "stat"] ## systematics that are correlated (will not have year appended to names)     "CMS_btagSF",

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

	infile_dir = "finalCombineFilesNewStats/%s/"%(use_QCD_Pt_str)
	infile_name = infile_dir+ "combine_%s%s_%s.root"%(technique_str,year,mass_point)

	outfile_dir = "finalCombineFilesNewStats/%s/correctedFinalCombineFiles/"%(use_QCD_Pt_str)
	outfile_name = outfile_dir + "combine_%s%s_%s.root"%(technique_str,year,mass_point)

	if useMask:
		infile_dir = "finalCombineFilesNewStats/%s/maskedFinalCombineFiles/"%(use_QCD_Pt_str)
		infile_name = infile_dir+ "combine_%s%s_%s.root"%(technique_str,year,mass_point)

		outfile_dir = "finalCombineFilesNewStats/%s/maskedCorrectedFinalCombineFiles/"%(use_QCD_Pt_str)
		outfile_name = outfile_dir + "combine_%s%s_%s.root"%(technique_str,year,mass_point)

	create_directories([infile_dir,outfile_dir])

	print("Looking for file %s"%(infile_name))
	## open root file

	infile = ROOT.TFile(infile_name,"r")
	outfile = ROOT.TFile(outfile_name,"RECREATE")


	for region in regions:

		superbin_neighbors = load_superbin_neighbors(year, region, technique_str,debug)

		## create a folder in the root file and CD into it

		region_folder = outfile.mkdir(region);
		region_folder.cd() ## cd into the new folder (matching the structure of the input file)


		for sample in samples: # name of BR type to fix


			folder_name = region + "/"

			## get nom histogram for this region and sample
			#print("Getting nominal histogram ", folder_name + sample )
			hist_nom = infile.Get(folder_name + sample )

			#print("nom hist is called %s in file %s."%(folder_name + sample, infile))
			
			for uncert_to_fix_ in all_uncerts: 


				uncert_to_fix_use = uncert_to_fix_
				if "shape" in uncert_to_fix_:
					uncert_to_fix_use = uncert_to_fix_[:] # will have the shape suffix
					uncert_to_fix_ = uncert_to_fix_[:-6]
					if debug: 
						print("uncert_to_fix_use is %s."%(uncert_to_fix_use))
						print("uncert_to_fix_ is %s."%uncert_to_fix_)

				if debug: print("Running uncertainty %s for %s/%s."%(uncert_to_fix_,sample,region))
				### things to skip
				#if uncert_to_fix_ == "CMS_jec": continue # this is not set up
				if uncert_to_fix_ == "CMS_topPt" and sample not in ["allBR","TTbar", "TTTo"] : continue
				if uncert_to_fix_ not in ["nom"] and sample == "data_obs": continue # data_obs only has this one uncertainty 
				if (sample == "sig" or sample == "WJets" or sample == "TTTo"   )and "stat" in uncert_to_fix_: continue
				uncert_to_fix = uncert_to_fix_
				if uncert_to_fix in ["CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_scale"] :
					if   sample == "sig":   
						uncert_to_fix+= "_sig"
						uncert_to_fix_use+= "_sig"
					elif "TTbar" in sample and uncert_to_fix == "CMS_pdf": 
						uncert_to_fix += "_misc"
						uncert_to_fix_use += "_misc"
					elif "TTbar" in sample: 
						uncert_to_fix+= "_TTbar" 
						uncert_to_fix_use+="_TTbar"
					elif "TTTo" in sample:  
						uncert_to_fix+= "_TTbar"
						uncert_to_fix_use +="_TTbar"
					elif sample == "allBR": 
						uncert_to_fix+= "_allBR"
						uncert_to_fix_use+= "_allBR"
					elif uncert_to_fix == "CMS_pdf" and sample in ["QCD","WJets", "TTbar"]: 
						uncert_to_fix += "_misc"     ### IF THE systematic is pdf and sample is NOT TTTo or sig, create a combined uncertainty  
						uncert_to_fix_use += "_misc"
					elif sample == "QCD": 
						uncert_to_fix+= "_QCD"
						uncert_to_fix_use += "_QCD"
					elif sample == "TTTo": 
						uncert_to_fix+= "_TTbar"
						uncert_to_fix_use += "_TTbar"
					elif sample == "WJets": 
						uncert_to_fix+= "_WJets"
						uncert_to_fix_use += "_WJets"
					elif sample == "ST": continue


				#try: 
				## get the histogram for this uncert/year/sample/region

				if debug: print("-----running %s/%s/%s/%s"%(sample, region, uncert_to_fix,year))
				uncert_to_fix_str = uncert_to_fix
				
				if uncert_to_fix in uncorrelated_systematics: 
					uncert_to_fix_str += year_str
					uncert_to_fix_use += year_str
				if debug: print("The uncert_to_fix is %s, is this uncorrelated? %s"%(uncert_to_fix,uncert_to_fix in uncorrelated_systematics))
				hist_name = "%s_%s"%(sample, uncert_to_fix_str)

				if uncert_to_fix == "nom":
					#print("Getting nom histogram.")
					hist_nom.Write();
					continue # don't want to do any of the up/down stuff for nom hist

				else:
					## get up hist
					if debug: print("Looking for up histogram %s in file %s."%(folder_name+hist_name+"Up", infile_name ) )
					hist_up = infile.Get(folder_name+hist_name+"Up")
					
					hist_up.SetName(sample + "_" + uncert_to_fix_use+"Up")  #### setting the name with "shape" if this is one of the normalized, shape versions
					if debug: print("Set the name of the output up hist to %s"%(hist_up.GetName()) )

					
					## get down hist
					if debug: print("Looking for down histogram %s in file %s."%(folder_name+hist_name+"Down",infile_name  ) )
					hist_down = infile.Get(folder_name+hist_name+"Down")
					hist_down.SetName(sample + "_" +uncert_to_fix_use+"Down")  #### setting the name with "shape" if this is one of the normalized, shape versions
					if debug: print("Set the name of the output up hist to %s"%(hist_down.GetName()) )



				#print("Cloning up and down histograms")
				#create doppelganger histograms to go into the "corrected" file
				hist_up_corr 	  = hist_up.Clone() ## could be some problem with multiple histograms having the same name?
				hist_down_corr    = hist_down.Clone()

				hist_up_corr.Sumw2()
				hist_down_corr.Sumw2()

				#print("hist_nom/hist_up/hist_down have sizes %s/%s/%s."%(hist_nom.GetNbinsX(),hist_up.GetNbinsX(),hist_down.GetNbinsX()))
				if debug: print("uncorrected hist names are %s/%s/%s."%(hist_nom.GetName(), hist_up.GetName(), hist_down.GetName() ))

				## if this systematic is one to fix ...
				#print("Fixing uncertainties")
				if uncert_to_fix_ in uncerts_to_fix:
					## loop over all bins

					for iii in range(1, hist_up.GetNbinsX()+1):
						## (1) find direction (relative to the nom) the furthest uncertainty is 
						## (2) set the other uncertainty to be in the opposite direction

						yield_nom = hist_nom.GetBinContent(iii)
						yield_up = hist_up.GetBinContent(iii)
						yield_down = hist_down.GetBinContent(iii)

						distance_up   = yield_up - yield_nom

						#print("iii = %s, first instance of distance_up is %s"%(iii, distance_up))
						distance_down = yield_down - yield_nom

						if distance_up > 0: sign_up_var   = distance_up/abs(distance_up)
						else: sign_up_var = 0
						if distance_down > 0: sign_down_var = distance_down/abs(distance_down)
						else: sign_down_var = 0

						### ONLY DO THIS IF up/down ratios are less than define threshold

						"""if (  (abs(distance_up) > 0)   and  (abs(distance_down) < 1e-8)      ):

						elif (  (abs(distance_up) < 1e-8)   and  (abs(distance_down) > 0)      ): """

						if (   (abs(distance_down ) > 0) and ( abs(distance_up) > 0   ) and     (( abs(distance_up)/abs(distance_down) < asymmetry_threshold) or (abs(distance_down)/abs(distance_up)  < asymmetry_threshold)) or (  (distance_up *distance_down)  > 0     ) ):

							## find which uncertainty is further from nom ( abs(up - nom) / abs(nom - down)   )
							

							var_ratio = abs(distance_up) / abs(distance_down)

							if var_ratio > 0.50:

								avg_var = (abs(distance_up) + abs(distance_down))/2.0

								distance_up   = avg_var * distance_up / abs(distance_up) # same direction as up
								distance_down = -1*distance_up

							else:
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





					"""

					if not useMask:

						for iii in range(1, hist_up.GetNbinsX()+1):

							yield_nom  = hist_nom.GetBinContent(iii)
							yield_up   = hist_up_corr.GetBinContent(iii)
							yield_down = hist_down_corr.GetBinContent(iii)

							if yield_nom < 1e-9: continue

							distance_up   = yield_up - yield_nom
							distance_down = yield_down - yield_nom

							if abs(distance_up) > 0:
								sign_up_var   = distance_up / abs(distance_up)
							else: sign_up_var = 1
							if abs(distance_down) > 0:
								sign_down_var = distance_down / abs(distance_down)
							else: sign_down_var = -1

							if debug: print("@@@@@ distance_up us %s"%distance_up)
							if debug: print("@@@@@ distance_down us %s"%distance_down)

							if debug: print("hist_nom has %s entires."%(hist_nom.GetNbinsX()))
							if debug: print("Looking at bin %s of histogram. There are %s entries in superbin_neighbors."%(iii,len(superbin_neighbors)))
							#### try to remove large spikes amongst neighbors in the 2D plane  ______
							if debug: print("sample/year/region/mass_point/technique/uncertainty: %s/%s/%s/%s/%s ----- Looking at bin %s, superbin_neighbors has size %s"%(sample, year, region, mass_point, uncert_to_fix,  iii,len(superbin_neighbors)))
							neighbor_superbin_indices = superbin_neighbors[iii-1] # get indexing right
							if debug: print("Bin %s has superbin neighbors: %s"%(iii, neighbor_superbin_indices))

							avg_neighbor_superbin_up   = 0  # sum of the signed value of the up variations 
							avg_neighbor_superbin_down = 0 # sum of the signed value of the down variations 

							avg_neighbor_superbin_absolute_up = 0     # sum of the absolute value of the up variations 
							avg_neighbor_superbin_absolute_down = 0   # sum of the absolute value of the down variations 


							### GET AVERAGE NEIGHBOR VARIATIONS
							num_nonzero_neighbors = 0
							for neighbor_superbin_index in neighbor_superbin_indices:

								neighbor_yield_nom  = hist_nom.GetBinContent(neighbor_superbin_index+1)
								neighbor_yield_up   = hist_up_corr.GetBinContent(neighbor_superbin_index+1)      ## use the versions that were just corrected above
								neighbor_yield_down = hist_down_corr.GetBinContent(neighbor_superbin_index+1)


								if debug: print("hist_nom/hist_up_corr/hist_down_corr have %s/%s/%s total bins."%(hist_nom.GetNbinsX(),hist_up_corr.GetNbinsX(),hist_down_corr.GetNbinsX()  ))

								if debug: print("for bin %s and superbin neighbor index %s, neighbor_yield_nom  is %s."%(iii,neighbor_superbin_index,neighbor_yield_nom))
								if debug: print("for bin %s and superbin neighbor index %s, neighbor_yield_up   is %s."%(iii,neighbor_superbin_index,neighbor_yield_up))
								if debug: print("for bin %s and superbin neighbor index %s, neighbor_yield_down is %s."%(iii,neighbor_superbin_index,neighbor_yield_down))


								if neighbor_yield_nom > 0:
									neighbor_up_var   = (neighbor_yield_up - neighbor_yield_nom) / neighbor_yield_nom
									neighbor_down_var = (neighbor_yield_down - neighbor_yield_nom) / neighbor_yield_nom

									if debug: print("neighbor_up_var/neighbor_down_var are %s/%s"%(neighbor_up_var,neighbor_down_var))


									avg_neighbor_superbin_up   += neighbor_up_var
									avg_neighbor_superbin_down += neighbor_down_var
									avg_neighbor_superbin_absolute_up   += abs(neighbor_up_var)
									avg_neighbor_superbin_absolute_down += abs(neighbor_down_var)

									num_nonzero_neighbors+=1
	


							if num_nonzero_neighbors >0:
								avg_neighbor_superbin_up /= num_nonzero_neighbors
								avg_neighbor_superbin_down /= num_nonzero_neighbors
								avg_neighbor_superbin_absolute_up /= num_nonzero_neighbors
								avg_neighbor_superbin_absolute_down /= num_nonzero_neighbors

							else: this was very artificial, so removing

								## if there are nonzero neighbors, don't even both with the rest of this process
								## just check if the uncertainty is greater than 25% and cut it off if so
								if yield_nom > 0:
									var_up_old    = distance_up / yield_nom
									var_down_old  = distance_down / yield_nom

									## cut uncertainties off at 20% 

									if var_up_old > 0.25:
										hist_up_corr.SetBinContent(iii,  (1+0.25)*yield_nom)
										hist_up_corr.SetBinError(iii,   sqrt(abs((1+0.25)*yield_nom  )) ) 
									if var_down_old > 0.25: 
										hist_down_corr.SetBinContent(iii,(1-0.25)*yield_nom)
										hist_down_corr.SetBinError(iii, sqrt(abs((1-0.25)*yield_nom)) ) 
									## otherwise, just ignore this 
								continue

							#print("Bin %s has abs up var average %s and abs down var average %s."%(iii,avg_neighbor_superbin_absolute_up,avg_neighbor_superbin_absolute_down ))





							## calculate the old variations 
							if yield_nom > 0:
								var_up_old    = distance_up / yield_nom
								var_down_old  = distance_down / yield_nom

								var_up_corr   = distance_up / yield_nom
								var_down_corr = distance_down / yield_nom
							#elif (abs(var_up_corr) > 0) or (abs(var_down_corr) > 0):
							#	var_up_old = 1.0
							#	var_down_old = 1.0
							else:
								#print("nom yield is 0: %s, so variations are set to 0"%(yield_nom))
								var_up_old = 0.0
								var_down_old = 0.0

							if debug: print("Old variatons: var_up_old/var_down_old are %s/%s"%(var_up_old,var_down_old))
							if debug: print("Neighbor variations: avg_neighbor_superbin_up/avg_neighbor_superbin_down %s/%s"%(avg_neighbor_superbin_up,avg_neighbor_superbin_down))



							if ((abs(var_up_old > 0.15)) or (abs(var_down_old) > 0.15)):



								#print("distance_up: ", var_up_old, ", yield_nom: ", yield_nom)
								## check to se if the abs(up_var) is significantly larger or smaller than the neighbor superbins
								#print("var_up_old is ", var_up_old)
								# if this uncertainty is more than twice as large as the average of neighbor superjets

								if abs(var_up_corr)    > 0.25: 
									if "sig" in sample: continue 
									if debug: print("----- CHANGED:  var_up_corr > 0.25: %s, setting to %s"%(var_up_corr, (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0) )
									#var_up_corr = min( 0.2, (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0   ) #CHANGED 29/08/2025
									var_up_corr = (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0    #CHANGED 29/08/2025

								if abs(var_down_corr) > 0.25: 
									#var_down_corr = min( 0.2, (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0   ) #CHANGED 29/08/2025
									var_down_corr = (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0   #CHANGED 29/08/2025

									if debug: print("----- CHANGED:  var_down_corr > 0.25: %s, setting to %s"%(var_down_corr,(avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0))


								if (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down) > 0:
									#### CHECK TO SEE IF SUPERBIN IS TOO LARGE RELATIVE TO NEIGHBORS
									if (abs(var_up_corr)) > 1.25*( avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down): # a factor of 2* canceled out wih the /2 of the denom
										if debug: print("----- CHANGED:  BAD VAR: var_up_old = %s, average of neighbors is %s."%(var_up_corr, (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0))
										var_up_corr = (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0
										#print("var_up_old was found to be too large relative to neighbors: var_up_old = %s, avg_neighbor = %s"%(var_up_old,  (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0 ))
									if (abs(var_down_corr)) > 1.25*( avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down): # a factor of 2* canceled out wih the /2 of the denom
										if debug: print("----- CHANGED:  BAD VAR: var_down_corr = %s, average of neighbors is %s."%(var_down_corr, (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0))
										var_down_corr = (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0

									#print("var_down_old was found to be too large relative to neighbors: var_down_old = %s, avg_neighbor = %s"%(var_down_old,  (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0 ))

								
								if 4*abs(var_up_old) < ( avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down): # a factor of 2* canceled out wih the /2 of the denom
									var_up_corr = (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0
									print("var_up_corr was found to be too small relative to neighbors: var_up_old = %s, avg_neighbor = %s"%(var_up_corr,  (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0 ))

								if 4*abs(var_down_old) < ( avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down): # a factor of 2* canceled out wih the /2 of the denom
									var_down_corr = (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0
									print("var_down_old was found to be too small relative to neighbors: var_down_old = %s, avg_neighbor = %s"%(var_down_old,  (avg_neighbor_superbin_absolute_up + avg_neighbor_superbin_absolute_down)/2.0 ))
								

								## now make sure the up and down are still fairly symmetric
								if (abs(var_up_corr )> 0.12)  or (abs(var_up_corr) > 0.12) :
									if abs(var_up_corr) > 1.5*abs(var_down_corr): 
										if debug: print("----- CHANGED:  var_up_corr > 1.5*var_down_corr: %s/%s"%(var_up_corr,var_down_corr))
										var_down_corr = -var_up_corr
									elif 1.5*abs(var_up_corr) < abs(var_down_corr): 
										if debug: print("----- CHANGED:  1.5*var_up_corr < var_down_corr: %s/%s"%(var_up_corr,var_down_corr))
										var_up_corr = -var_down_corr







								var_up_corr  *=sign_up_var
								var_down_corr*= -sign_down_var  # making sure these are in opposite directions
								if var_up_corr*var_down_corr > 0: var_down_corr = -var_up_corr
								if debug: print("sign_up_var/sign_down_var= %s/%s"%(sign_up_var,sign_down_var))

								if (abs(var_up_corr > 0.25)) or (abs(var_down_corr )> 0.25):
									if debug: print("=========================== ERROR: large up/down variation was not fixed: %s / %s"%(var_up_corr,var_down_corr))

								## now apply the new, average uncertainties 
								hist_up_corr.SetBinContent(iii,  (1+var_up_corr)*yield_nom)
								hist_down_corr.SetBinContent(iii,(1+var_down_corr)*yield_nom)

								hist_up_corr.SetBinError(iii,   sqrt(abs((1+var_up_corr)*yield_nom  )) ) 
								hist_down_corr.SetBinError(iii, sqrt(abs((1+var_down_corr)*yield_nom)) ) 

								## if these have changed, print 
								if (abs( var_up_old - var_up_corr) > 0) or (abs( var_down_old - var_down_corr) > 0):
									if debug: print("For bin %s %s/%s/%s/%s changed var_up_old=%s   ---> var_up_corr=%s."%(iii,year,region,sample,uncert_to_fix, var_up_old,var_up_corr))
									if debug: print("For bin %s %s/%s/%s/%s changed var_down_old=%s ---> var_down_corr=%s."%(iii,year,region,sample,uncert_to_fix,var_down_old,var_down_corr))
								if debug:   
									print("#######################################################################")
									print("#######################################################################")
									print("##  In the end, for bin %s, var_up_corr = %s, var_down_corr = %s  ##"%(var_up_corr,var_down_corr))
									print("#######################################################################")
									print("#######################################################################") """

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


				if "shape" in uncert_to_fix_use:
					hist_up_corr.Scale(1.0/hist_up_corr.Integral())
					hist_down_corr.Scale(1.0/hist_down_corr.Integral())

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
	
	debug 			 = False
	include_ATxtb    = False
	include_sideband = False

	include_WJets    = True
	include_TTTo     = True
	useMask 		 = False

	if useMask:
		toMask   		 = [True,False]
	else:
		toMask   		 = [False]
	all_uncerts = [ "CMS_scale_shape", "CMS_pdf_shape","nom",  "CMS_bTagSF_M" ,  "CMS_jer", "CMS_jec", "CMS_bTagSF_M_corr" ,  "CMS_bTagSF_bc_M_corr",	   "CMS_bTagSF_light_M_corr",		  "CMS_bTagSF_bc_M_year",	   "CMS_bTagSF_light_M_year",		 "CMS_jer_eta193", "CMS_jer_193eta25",  "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal",   "CMS_jec_Absolute", "CMS_jec_BBEC1_year",	"CMS_jec_Absolute_year",  "CMS_jec_RelativeSample_year", "CMS_pu", "CMS_topPt", "CMS_L1Prefiring", "CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory", "CMS_jec_AbsolutePU",   "CMS_jec_AbsoluteScale" ,   "CMS_jec_Fragmentation" , "CMS_jec_AbsoluteMPFBias",  "CMS_jec_RelativeFSR", "CMS_scale", "stat"]  ## systematic namings for cards   "CMS_btagSF", 
	#all_uncerts = [  "nom",    "CMS_jer", "CMS_jec",  "CMS_bTagSF_M" ,   "CMS_bTagSF_bc_M_corr",	        "CMS_bTagSF_light_M_corr",	  	 "CMS_bTagSF_bc_M_year",	   "CMS_bTagSF_light_M_year",		 "CMS_jer_eta193", "CMS_jer_193eta25",  "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal",   "CMS_jec_Absolute", "CMS_jec_BBEC1_year",	 "CMS_jec_Absolute_year",  "CMS_jec_RelativeSample_year", "CMS_pu",    "CMS_L1Prefiring",   "CMS_pdf", "CMS_renorm", "CMS_fact", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory",    "CMS_jec_AbsolutePU",   "CMS_jec_AbsoluteScale" ,   "CMS_jec_Fragmentation" , "CMS_jec_AbsoluteMPFBias",  "CMS_jec_RelativeFSR",  "CMS_scale", ]  ## systematic namings for cards   "CMS_btagSF", 

	#"CMS_bTagSF_T", "CMS_bTagSF_T_corr",   "CMS_bTagSF_bc_T_corr",  "CMS_bTagSF_light_T_corr",   "CMS_bTagSF_bc_T_year",		"CMS_bTagSF_light_T_year",

	uncerts_to_fix =  [ "CMS_jer", "CMS_jec", "CMS_bTagSF_M" ,  "CMS_bTagSF_T",  "CMS_bTagSF_M_corr" , "CMS_bTagSF_T_corr",   "CMS_bTagSF_bc_T_corr", "CMS_bTagSF_light_T_corr",  "CMS_bTagSF_bc_M_corr", "CMS_bTagSF_light_M_corr", "CMS_bTagSF_bc_T_year",  "CMS_bTagSF_light_T_year",  
	     "CMS_bTagSF_bc_M_year",       "CMS_bTagSF_light_M_year",  "CMS_jer_eta193", "CMS_jer_193eta25", "CMS_jec_FlavorQCD", "CMS_jec_RelativeBal",
	      "CMS_jec_HF", "CMS_jec_BBEC1", "CMS_jec_EC2", "CMS_jec_Absolute", "CMS_jec_BBEC1_year", "CMS_jec_EC2_year", "CMS_jec_Absolute_year", "CMS_jec_HF_year",
	       "CMS_jec_RelativeSample_year", "CMS_jec_AbsoluteCal", "CMS_jec_AbsoluteTheory", "CMS_jec_AbsolutePU",  "CMS_pu",  "CMS_jec_AbsoluteScale" ,   "CMS_jec_Fragmentation" , "CMS_jec_AbsoluteMPFBias",  "CMS_jec_RelativeFSR", "CMS_pdf", "CMS_scale_shape", "CMS_pdf_shape"]  ## systematic namings for cards   "CMS_btagSF",  ,   "CMS_bTagSF_bc_T",      "CMS_bTagSF_light_T",       "CMS_bTagSF_bc_M",       "CMS_bTagSF_light_M", 



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

	technique_strs = ["NN_",""]

	technique_strs = [""]

	#### debugging stuff
	if debug:
		#uncerts_to_fix =  ["CMS_jec_AbsolutePU"] 
		years = ["2015"]
		#samples = ["QCD"]
		#regions = ["SR"]
		mass_points = ["Suu4_chi1"]


	use_QCD_Pt_opts = [True,False]
	use_QCD_Pt_strs = ["QCDPT","QCDHT"]


	for jjj,use_QCD_Pt in enumerate(use_QCD_Pt_opts):

		for mask_opt in toMask:
			for technique_str in technique_strs:
				for year in years:
						for mass_point in mass_points:
								#try:
								#fix_uncerts( samples, mass_point, all_uncerts, uncerts_to_fix, year, regions, True, debug   )
								fix_uncerts( samples, mass_point, all_uncerts, uncerts_to_fix, year, regions, technique_str, mask_opt, use_QCD_Pt, debug   )

								#except: 
								#print("ERROR: failed %s/%s"%(mass_point,year))



