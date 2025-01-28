import sys, os
import ROOT
from write_cms_text import write_cms_text

import ast

from math import sqrt



def load_superbin_indices(year,region, technique_str):	# load in the superbin indices (located in a text file )
	_superbin_indices = []
	bin_map_path         = "binMaps/"
	open_file = open(bin_map_path+"/superbin_indices%s_%s.txt"%(technique_str,year),"r")
	#print("Got superbin index file %s."%( bin_map_path+"/superbin_indices%s_%s.txt"%(technique_str,year)  ))
	for line in open_file:
		columns = line.split('/')
		if columns[0] == year and columns[1] == region:
			_superbin_indices = columns[3]
	open_file.close()
	return ast.literal_eval(_superbin_indices)


def create_masks():
	#needs to loop over all mass points, needs one for each year

	linearized_file_path = "finalCombineFilesNewStats/"
	region_mask_path 	 = "region_masks/"
	#-- new script

	c = ROOT.TCanvas("","",1200,1000)

	years = ["2015","2016","2017","2018"]
	mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1","Suu5_chi1p5","Suu5_chi2","Suu6_chi1","Suu6_chi1p5","Suu6_chi2","Suu6_chi2p5","Suu7_chi1", "Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3","Suu8_chi1","Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"]
	regions = ["SR","CR","AT1b","AT0b"]
	technique_strs = ["", "NN_"]

	for year in years:
		bin_mask_file = open(region_mask_path+"bin_masks_%s.txt"%( year),"w")
		full_bin_mask_file = open(region_mask_path+"full_bin_masks_%s.txt"%( year),"w")




		for region in regions:
			for technique_str in technique_strs:

				if region in ["SR","CR"]: region_to_use = "SR"
				elif region in ["AT1b","AT0b"]: region_to_use = "AT1b"

				technique_name = "cut-based"
				if "NN" in technique_str: technique_name = "NN-based"
	   			superbin_indices = load_superbin_indices(year,region_to_use, technique_str)

				bad_bins_indices = []

				hist_map = ROOT.TH2F("h_bin_map_%s_%s%s"%(region,technique_str,year),"bin map (%s) (%s) (%s); diSuperjet mass [GeV];superjet mass"%(region, year, technique_name ), 22,1250., 10000, 20, 500, 5000) # 375 * 125
				hist_map.SetDirectory(0)
				hist_map.SetStats(0)

				full_hist_map = ROOT.TH2F("h_full_bin_map_%s_%s%s"%(region,technique_str,year),"full bin map (%s) (%s) (%s); diSuperjet mass [GeV];superjet mass"%(region, year, technique_name ), 22,1250., 10000, 20, 500, 5000) # 375 * 125
				full_hist_map.SetDirectory(0)
				full_hist_map.SetStats(0)
				for mass_point in mass_points:

	   				#open up input root file
	   				linearized_file_name = "combine_%s%s_%s.root"%(technique_str,year,mass_point)
					
	   				#print("Looking at file %s."%(linearized_file_name))

	   				BR_hist_name = "%s/allBR"%(region,)
	   				sig_hist_name = "%s/sig"%(region)

	   				#print("Looking for histograms %s / %s."%(BR_hist_name, sig_hist_name))

					linearized_file = ROOT.TFile.Open(linearized_file_path+linearized_file_name)

					allBR_hist = linearized_file.Get(BR_hist_name)
					sig_hist   = linearized_file.Get(sig_hist_name)

					#print("superbin indices has size %s."%(len(superbin_indices)))
					#print("allBR_hist size is %s."%( allBR_hist.GetNbinsX() ))

					for iii in range(0,allBR_hist.GetNbinsX()):
						if  ((sig_hist.GetBinContent(iii+1) / sqrt( allBR_hist.GetBinContent(iii+1))) > 2.0 ):
							if iii not in bad_bins_indices:
								bad_bins_indices.append(iii)


					#	get superbin indices

					#		loop over bins:
					#			compare sig to allBR, save bins over 1 sigma

					#	loop over masked superbins
					#		get bin indices associated with that superbin
					#		fill these in for the TH2F

					#	draw TH2F 
					#	save TH2F
				if region == "AT1b": print("For year %s, region %s, and technique_name %s,  bad bins are %s"%(year, region, technique_name, bad_bins_indices))
				bad_tuples = 0 
				for bad_bin in bad_bins_indices:
					TH2F_bins = superbin_indices[bad_bin]
					for _tuple in TH2F_bins:
						hist_map.SetBinContent( _tuple[0], _tuple[1], 1)
						bad_tuples+=1
				#t("For year %s, region %s, and technique_name %s, filled in %s bins."%(year, region, technique_name, bad_tuples))
				

				## mask all TH2 indices within the rectangle of the original bad indices:

				max_TH2_index_x = -1e9
				min_TH2_index_x = 1e9
				max_TH2_index_y = -1e9
				min_TH2_index_y = 1e9

				for bad_bin_index in bad_bins_indices:
					for _tuple in superbin_indices[bad_bin_index]:
						x_tuple = int(_tuple[0])
						y_tuple = int(_tuple[1])

						if x_tuple < min_TH2_index_x: min_TH2_index_x = x_tuple
						if y_tuple < min_TH2_index_y: min_TH2_index_y = y_tuple

						if x_tuple > max_TH2_index_x: max_TH2_index_x = x_tuple
						if y_tuple > max_TH2_index_y: max_TH2_index_y = y_tuple

				#print("max/min x indices are: %s/%s, max/min y indices are: %s/%s"%(max_TH2_index_x,min_TH2_index_x,max_TH2_index_y,min_TH2_index_y ))


				full_mask_bad_bin_indices = []
				full_mask_bad_bins = []

				for superbin_index,superbin in enumerate(superbin_indices):
					# find superbins that have 
					for _tuple in superbin:
						x_tuple = int(_tuple[0])
						y_tuple = int(_tuple[1])
						if (x_tuple <= max_TH2_index_x) and (y_tuple <= max_TH2_index_y) and (x_tuple >= min_TH2_index_x) and (y_tuple >= min_TH2_index_y):
							if superbin_index not in full_mask_bad_bin_indices:  
								full_mask_bad_bin_indices.append(superbin_index)
								full_mask_bad_bins.append(superbin)
							full_hist_map.SetBinContent(x_tuple , y_tuple,1)

				full_bin_mask_file.write("%s/%s/%s/%s/%s   \n"%(year, region, technique_str, full_mask_bad_bins, bad_bins_indices))

				bin_mask_file.write("%s/%s/%s/%s   \n"%(year, region, technique_str,bad_bins_indices))
				hist_map.Draw("colz")
				c.SaveAs("plots/masks/mask_%s_%s%s.png"%(region, technique_str,year))

				full_hist_map.Draw("colz")
				c.SaveAs("plots/masks/full_mask_%s_%s%s.png"%(region, technique_str,year))


		bin_mask_file.close()
		full_bin_mask_file.close()


		## what to do possibly:
		## create a box that contains all the TH2F bins that need to be masked
		## mask all superbins that include these TH2F bins 


	# them go back through the bins and remove any that are in the mask

	#new utility similar to fix_asymmetric_uncerts.py that iteratively goes through all folders, copies them to new, masked file
	#	- for AT1b region, create new versions of each histogram with size (original size - mask_length) that skips the masked bins 



if __name__=="__main__":
	create_masks()