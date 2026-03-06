import sys,os,time

import argparse



if __name__=="__main__":



	parser = argparse.ArgumentParser(description="Set the bin map settings to desired version to use in master_linearizer.py. \
										Usage: python set_bin_map.py --folder <bin map setting folder>,\
									 where <bin map setting folder> is the desired one in binMaps/oldBinMaps/")
	parser.add_argument("-f", "--folder", type=str, required=True, help="The desired bin map setting folder in binMaps/oldBinMaps/ \
																		to use in master_linearizer.py.")
	args = parser.parse_args()

	folder =args.folder

	text_output_path 	 = os.getenv('CMSSW_BASE') + "/src/SuuToChiChi_analysis_software/postprocess/binMaps/"
	group_output_path    = os.getenv('CMSSW_BASE') + "/src/SuuToChiChi_analysis_software/postprocess/superbinGroups/"
	neighbor_output_path = os.getenv('CMSSW_BASE') + "/src/SuuToChiChi_analysis_software/postprocess/superbinNeighbors/"

	text_output_copy_path 	  = os.getenv('CMSSW_BASE') + "/src/SuuToChiChi_analysis_software/postprocess/binMaps/oldBinMaps/" + folder
	group_output_copy_path    = os.getenv('CMSSW_BASE') + "/src/SuuToChiChi_analysis_software/postprocess/superbinGroups/oldBinGroups/" + folder
	neighbor_output_copy_path = os.getenv('CMSSW_BASE') + "/src/SuuToChiChi_analysis_software/postprocess/superbinNeighbors/oldNeighbors/" + folder


	bin_map_copy_cmd = 'cp %s/*_superbin_indices_*.txt %s'%( text_output_copy_path,text_output_path)
	os.system(bin_map_copy_cmd)
	print("Copied superbin map settings from binMaps/%s"%args.folder)

	bin_map_copy_cmd = 'cp %s/*_superbin_groups_*.txt %s'%(group_output_copy_path,group_output_path )
	os.system(bin_map_copy_cmd)
	print("Copied superbin group settings from binMaps/%s"%args.folder)

	bin_map_copy_cmd = 'cp %s/*_superbin_neighbors_*.txt %s'%( neighbor_output_copy_path, neighbor_output_path)
	os.system(bin_map_copy_cmd)
	print("Copied superbin neighbor settings from binMaps/%s"%args.folder)


	settings_file = open(text_output_path + "/current_settings.txt","w")
	settings_file.write("Current settings in folder binMaps/%s"%(folder))
	settings_file.close()


