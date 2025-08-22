import sys, os
import ROOT
from write_cms_text import write_cms_text

import ast

from math import sqrt



def load_superbin_indices(year,region, technique_str, use_QCD_Pt_str):	# load in the superbin indices (located in a text file )
	_superbin_indices = []
	bin_map_path		 = "binMaps/"
	open_file = open(bin_map_path+"%s_superbin_indices%s_%s.txt"%(use_QCD_Pt_str,technique_str,year),"r")
	#print("Got superbin index file %s."%( bin_map_path+"/superbin_indices%s_%s.txt"%(technique_str,year)  ))
	for line in open_file:
		columns = line.split('/')
		if columns[0] == year and columns[1] == region:
			_superbin_indices = columns[3]
	open_file.close()
	return ast.literal_eval(_superbin_indices)


def create_masks(use_1b_map=False, sig_to_BR_thresh = 0.8):
	#needs to loop over all mass points, needs one for each year

	region_mask_path 	 = "region_masks/"
	#-- new script

	c = ROOT.TCanvas("","",1200,1000)

	years = ["2015","2016","2017","2018"]

	# REMOVED "Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1","Suu5_chi1p5",
	mass_points = ["Suu5_chi2","Suu6_chi1","Suu6_chi1p5","Suu6_chi2","Suu6_chi2p5","Suu7_chi1", "Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3","Suu8_chi1","Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"]
	regions = ["SR","CR","AT1b","AT0b"]

	technique_strs = ["", "NN_"]
	technique_strs = [""]



	use_QCD_Pt_opts = [True,False]
	use_QCD_Pt_strs = ["QCDPT","QCDHT"]


	for jjj,use_QCD_Pt in enumerate(use_QCD_Pt_opts):


		linearized_file_path = "finalCombineFilesNewStats/%s/"%(use_QCD_Pt_strs[jjj])


		for year in years:
			bin_mask_file = open(region_mask_path+"%s_bin_masks_%s.txt"%(use_QCD_Pt_strs[jjj], year),"w")
			full_bin_mask_file = open(region_mask_path+"%s_full_bin_masks_%s.txt"%(use_QCD_Pt_strs[jjj], year),"w")


			for region in regions:
				for technique_str in technique_strs:

					region_to_use = region 
					if use_1b_map:
						if region in ["SR","CR"]: region_to_use = "SR"
						elif region in ["AT1b","AT0b"]: region_to_use = "AT1b"
					print("The region is %s, region_to_use is %s"%(region, region_to_use))

					technique_name = "cut-based"
					if "NN" in technique_str: technique_name = "NN-based"
		   			superbin_indices = load_superbin_indices(year,region_to_use, technique_str,use_QCD_Pt_strs[jjj])

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

						#print("The file is %s"%(linearized_file_path+linearized_file_name))
						#print("For year / region / technique : %s / %s / %s"%(year, region, technique_str))
						#print("The allBR_hist/sig_hist histogram has %s/%s  bins."%(allBR_hist.GetNbinsX(), sig_hist.GetNbinsX()))

						#print("superbin indices has size %s."%(len(superbin_indices)))
						#print("allBR_hist size is %s."%( allBR_hist.GetNbinsX() ))

						for iii in range(0,allBR_hist.GetNbinsX()):
							if  ( (sig_hist.GetBinContent(iii+1) / sqrt( allBR_hist.GetBinContent(iii+1))) > sig_to_BR_thresh ):
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
					print("For year %s, region %s, and technique_name %s,  bad bins are %s"%(year, region, technique_name, bad_bins_indices))
					
					bad_tuples = 0 
					#print("For year / region / technique : %s / %s / %s"%(year, region, technique_str))
					#print("The superbin indices are: %s"%superbin_indices)
					#print("bad_bins_indices are: %s"%bad_bins_indices)
					#print("Superbin indices have length %s, whereas bad_bins_indices has length %s."%(len(superbin_indices),len(bad_bins_indices)))

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
					c.SaveAs("plots/masks/%s_mask_%s_%s%s.png"%(use_QCD_Pt_strs[jjj],region, technique_str,year))

					full_hist_map.Draw("colz")
					c.SaveAs("plots/masks/%s_full_mask_%s_%s%s.png"%(use_QCD_Pt_strs[jjj],region, technique_str,year))


			bin_mask_file.close()
			full_bin_mask_file.close()

def get_masked_groups(groups, mask):
	mask_sorted = sorted(mask)
	removed_so_far = 0

	for m in mask_sorted:
		effective = m - removed_so_far
		new_groups = []
		for g in groups:
			new_g = []
			for idx in g:
				if idx == effective:
					# drop this bin
					continue
				elif idx > effective:
					new_g.append(idx - 1)
				else:
					new_g.append(idx)
			if new_g:
				new_groups.append(new_g)
		groups = new_groups
		removed_so_far += 1
	return groups


if __name__=="__main__":

	use_1b_map = True		# whether to use 1b map for 0b regions (i.e. SR map for CR and AT1b map for AT0b)
	sig_to_BR_thresh = 0.8   # threshold of signal-to-sqrt(BR) to mask


	## create mask
	create_masks(use_1b_map,sig_to_BR_thresh)
	print("Created masks.")



	## now 

	superbin_groups_dir  = "superbinGroups/"
	region_mask_dir = "region_masks/"

	#### You likely do not want to use this  ----> want 1b/0b regions to use the same superbin maps, but NOT the same masks (which is what this does)

	use_1b_maps_for_0b = True	# means the SR+CR / AT1b+AT0b regions use the same maps (1b and 0b use the same) 

	mask_dict = {}
	groups_dict = {}

	years = ["2015","2016","2017","2018"]
	regions = ["SR","CR","AT1b","AT0b"]
	techniques = ["NN_",""] ## currently not needed 



	if use_1b_maps_for_0b: _1b_map_translator = {"SR":"SR","CR":"SR","AT1b":"AT1b","AT0b":"AT1b"}
	else: _1b_map_translator = {"SR":"SR","CR":"CR","AT1b":"AT1b","AT0b":"AT0b"}

	use_QCD_Pt_opts = [True,False]
	use_QCD_Pt_strs = ["QCDPT","QCDHT"]


	for use_QCD_Pt_str in use_QCD_Pt_strs:


		for year in years:
			mask_path  = region_mask_dir + "%s_bin_masks_%s.txt"%(use_QCD_Pt_str,year)
			group_path = superbin_groups_dir + "%s_superbin_groups_%s.txt"%(use_QCD_Pt_str,year)
			output_group_name = superbin_groups_dir + "masked/%s_superbin_groups_%s.txt"%(use_QCD_Pt_str,year)
			
			## get masks 
			mask_dict[year] = {}
			for region in regions:
				mask_dict[year][region] = []


			with open(mask_path) as f:
				lines = f.readlines()
			for line in lines:
				_year,region,technique,mask = line.split("/")
				if "NN" in technique: continue # not dealing with this now
				mask = mask.strip()
				mask = ast.literal_eval(mask)
				mask_dict[_year][region] = mask


			## get groups
			groups_dict[year] = {}
			for region in regions:
				groups_dict[year][region] = []

			with open(group_path) as f:
				lines = f.readlines()
			for line in lines:
				_year,region,desc,groups = line.split("/")
				#print("groups are %s"%groups)
				groups = ast.literal_eval(groups)
				groups_dict[year][region] = groups


			# write out masked groups 

			outfile = open(output_group_name,"w")

			for region in regions:
				region_to_use = _1b_map_translator[region]
				groups = groups_dict[_year][region_to_use]  # if use_1b_maps_for_0b, this will use SR/AT1b instead of CR/AT0b groups 

				masked_groups = get_masked_groups(groups, mask_dict[_year][ region] )
				new_n_groups = len(masked_groups)
				desc = "number of superbin groups =%d"%( new_n_groups)
				outfile.write("%s/%s/%s/%s\n" % (_year, region, desc, masked_groups))			

			
			outfile.close()
			print("Wrote masked superbinGroup text files to %s."%(superbin_groups_dir + "masked/"))
			"""for line in lines:
				_year,region,desc,groups = line.split("/")

				desc_beg,_ = desc.split("=")
				groups = ast.literal_eval(groups)
				masked_groups = get_masked_groups(groups, mask_dict[_year][ _1b_map_translator[region]])

				new_n_groups = len(masked_groups)

				#print("%s/%s/%s = %s/%s\n"%(year,region, desc_beg,new_n_groups   ,masked_groups))
				outfile.write("%s/%s/%s=%d/%s\n" % (_year, region, desc_beg, new_n_groups, masked_groups))	 """	   
			
	print("Masked superbin groups.")






