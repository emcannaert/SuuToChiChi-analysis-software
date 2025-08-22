import ROOT
import sys, os
import matplotlib
matplotlib.use('Agg')  # Use 'Agg' backend for non-interactive plotting

import matplotlib.pyplot as plt
from math import sqrt, exp
import random
from random import uniform, shuffle, choice
import numpy as np
import pdb
import time
from histInfo import histInfo
#import networkx as nx
from write_cms_text.write_cms_text import write_cms_text
import argparse
import array

ROOT.TColor.InvertPalette()
ROOT.gStyle.SetPalette(ROOT.kViridis)

####  calculateStatisticalUncertaintyBins.py
####  Written by Ethan Cannaert, September 2023, updated July 2024, updated again November 2024
####  Opens up a TH2 (22x20 bins, avg superjet mass vs disuperjet mass)
####  Merges bins into "superbins" until superbin systematic uncertainties are below 25% ( or desired value) and/or scaled superbin yields are above some threshold.
####  Creates histograms showing the bin mappings, final superbin counts, and superbin statistical uncertainties
####  The main output of this are text files (superbin_indices*.txt in the binMaps/ directory) that list the merged superbin mappings
####  This script expects input TH2s with dimensions self.n_bins_x X self.n_bins_y (default 22x20)
####  The input files are searched for in the $CMSSW_BASE/src/combinedROOT/processedFiles folder with naming scheme <dataset type>_<year>_processed.root
####  The combineHistBins class uses the histInfo class to store TH2F information, so methods from this class are often used.

### NOTE: 
### format of tuples superbin indices goes like array binning, e.g. from 0 to n_bins_x - 1. Therefore tuples_x + 1 and tuple_y + 1 should be used to get histogram values
### format of superbin indices themselves goes from 0 to N_superbins

class combineHistBins:

	def __init__(self,year,region,technique_str, useQCDHT, debug=False, dryRun=False, runEos=False):   #constructor will convert TH2 to a 2D array, do the optimized bin merging, and then return a TH2 with those associated bins

		self.year = year
		self.region = region
		self.technique_str = technique_str
		self.dryRun = dryRun ## perform a "dry run" where text files are not made
		


		#### characteristic thresholds for merging process ----- CHANGE THESE -----
		self.max_stat_uncert 	 		= 0.175  ## maximum statistical uncertainty
		self.distance_threshold  		= 6.0
		self.superbin_size_threshold	= 20


		if "NN" in self.technique_str: self.max_stat_uncert = 0.30  ## maximum statistical uncertainty for NN method
		
		self.min_unscaled_QCD_bin_counts   = 2.0   ## the minimum number of unscaled QCD events required to be in each bin, better to make this 1 or more to prevent weird "migration" stuff
		self.min_scaled_QCD_bin_counts   = 0.0   ## the minimum number of scaled QCD events required to be in each bin, better to make this 1 or more to prevent weird "migration" stuff


		## options for which MCs to include
		self.includeTTJetsMCHT800to1200 = True
		self.includeWJets   			= True
		self.includeTTo 				= False 

		self.useQCDHT = useQCDHT
		self.QCD_str = "QCDPT"
		if self.useQCDHT: self.QCD_str = "QCDHT"

		if self.min_unscaled_QCD_bin_counts > 0:
			print("")
			print("")
			print("")
			print("===============================================")
			print("===============================================")
			print("WARNING: min_unscaled_QCD_bin_counts set to %s."%self.min_unscaled_QCD_bin_counts)
			print("===============================================")
			print("===============================================")
			print("")
			print("")
			print("")
		if self.min_scaled_QCD_bin_counts > 0:
			print("")
			print("")
			print("")
			print("===============================================")
			print("===============================================")
			print("  WARNING: min_scaled_QCD_bin_counts set to %s."%self.min_scaled_QCD_bin_counts)
			print("===============================================")
			print("===============================================")
			print("")
			print("")
			print("")

		self.bin_min_x = 3  ## start x bin in the 2D distribution (diSJ mass) --> this is chosen for analysis purposes
		self.bin_min_y = 1  ## start y bin in the 2D distribution (SJ mass)   --> this is chosen for analysis purposes

		self.n_bins_x = 22
		self.n_bins_y = 20

		if region in ["SB1b","SB0b"]:

			self.bin_min_x = 0  ## start x bin in the 2D distribution (diSJ mass)
			self.bin_min_y = 0  ## start y bin in the 2D distribution (SJ mass)
			self.n_bins_x = 15
			self.n_bins_y = 12

			self.max_stat_uncert = 0.30  ## maximum statistical uncertainty
		
		## get container that holds all histogram values
		self.all_hist_values =  histInfo.histInfo(year,region, self.bin_min_x, self.bin_min_y, self.n_bins_x, self.n_bins_y, self.technique_str, self.includeTTJetsMCHT800to1200, self.includeWJets, self.includeTTo, self.useQCDHT,  debug, runEos, False)	#histInfo.histInfo(year,region) ## everywhere there is originally a sqrt, will need to call get_bin_total_uncert and get 
		
		## initialize list of all superbin indices
		self.superbin_indices = self.init_superbin_indices()	 
 
		print("Starting the process of merging bins.")
		self.do_bin_merging()
		print("Finished with bin merging for %s."%(self.QCD_str))


		## different options for how to order superbins (used for linearizing later in analysis pipeline)
		#self.superbin_indices = self.sort_bins_with_graphs() ## sorts bins by approximate location in 2D
		#self.superbin_indices = self.sort_bins_by_raw_distance() ## sort bins by their raw distance from the origin in the 2D place
		self.superbin_indices = self.sort_bins_by_descending_event_yield() ## sort bins by descending bin yield
		#self.superbin_indices = self.sort_bins_by_ascending_sigBR() ## sort bins by ascending sig/sqrt(BR) ---> this would work only for a specific mass point ...



		self.print_superbins()   ### print out scaled and unscaled counts in each superbin post merging

		self.superbin_groups = self.create_superbin_groups()

		self.print_summary()

		## used later on in analysis pipeline (for bin-by-bin uncertainty parameters that are shared by superbin groups)
		self.superbin_neighbors = self.get_list_of_all_superbin_neighbors()

		if debug: print("The final superbin groups are %s."%self.superbin_groups)

	#####################################################
	######### superbin group helper functions ###########
	#####################################################

	def get_list_of_all_superbin_neighbors(self):
		superbin_neighbor_list = []
		for superbin_index,superbin in enumerate(self.superbin_indices):
			superbin_neighbor_list.append( self.get_list_of_neighbor_superbins(superbin[0]) )
		return superbin_neighbor_list


	def create_superbin_groups(self): 

		superbin_groups = [ [superbin_number] for superbin_number in range(0,len(self.superbin_indices) )  ]

		random.seed(12345)
		random.shuffle(superbin_groups)   ## randomize list so there isn't one area that is preferred

		there_are_ungrouped_superbins = True
		while there_are_ungrouped_superbins:

			## create copy of groups
			superbin_groups_temp = list(superbin_groups[:])	   ##   [ [1], [2,4,5], [3], ..... [N]   ]

			runContingency = False

			## get list of ungrouped superbins
			ungrouped_superbin_numbers = [   superbin[0] for superbin in  superbin_groups_temp if len(superbin) == 1  ]	 # [ [1], ... [i], ...,   [N]	]
			if debug: print("ungrouped_superbin_numbers: %s."%(ungrouped_superbin_numbers))
			cand_superbin_index = random.choice(ungrouped_superbin_numbers)
			cand_superbin_index_num = superbin_groups_temp.index( [cand_superbin_index] )	  ## the location of this ungrouped superbin in ungrouped_superbin_numbers 
			cand_superbin_yield = self.all_hist_values.get_scaled_QCD_superbin_counts(self.superbin_indices[ cand_superbin_index ]) 

			if debug: print("Randomly chose superbin %s (superbin number %s in superbin_groups_temp) with yield %s."%(cand_superbin_index, cand_superbin_index_num, cand_superbin_yield))

			## check to see if cand superbin has > 50 events
			if  cand_superbin_yield > 50: 

				## update superbin_groups
				superbin_groups  			  = list(superbin_groups_temp[:])
				there_are_ungrouped_superbins = self.check_for_ungrouped_superbins(superbin_groups)

				continue

			## get list of neighboring bins
			neighbor_superbins = self.get_list_of_neighbor_superbins(  self.superbin_indices[cand_superbin_index][0] )   ## takes a tuple in the superbin, returns list of neighboring superbin indices

			if debug: print("cand_superbin_index %s has neighbors %s."%(cand_superbin_index, neighbor_superbins))

			good_neighbor_superbins = []

			# remove superbins that are already in groups 
			for neighbor_superbin_index,neighbor_superbin in enumerate(neighbor_superbins):
				for superbin_group in superbin_groups_temp:

					if (neighbor_superbin in superbin_group)   and (len(superbin_group) > 1 ): continue # skip neighbor superbins that are in groups of two or more
					elif (neighbor_superbin in superbin_group) and (len(superbin_group) == 1): good_neighbor_superbins.append(neighbor_superbin)

			if len(good_neighbor_superbins) > 0: 

				## get scaled yields of ungrouped neighboring bins
				good_neighbor_superbin_yield_diff = []
				for neighbor_superbin_index in good_neighbor_superbins:

					good_neighbor_superbin_yield_diff.append(  abs( cand_superbin_yield  -   self.all_hist_values.get_scaled_QCD_superbin_counts(self.superbin_indices[ neighbor_superbin_index ])  ) )

				paired_lists = zip(good_neighbor_superbins, good_neighbor_superbin_yield_diff)
				sorted_pairs = sorted(paired_lists, key=lambda x: x[1], reverse=False)
				good_neighbor_superbin_yield_diff_sorted_temp, sorted_neighbor_bin_yiel_diff = zip(*sorted_pairs)
				good_neighbor_superbin_yield_diff_sorted = list(good_neighbor_superbin_yield_diff_sorted_temp)  ## list of neighbor superbin indices sorted by increasing order of bin yields

				if debug: print("Neighboring ungrouped superbins are %s."%good_neighbor_superbin_yield_diff_sorted)
				if debug: print("sorted_neighbor_bin_yiel_diff is ",sorted_neighbor_bin_yiel_diff)
				#if debug: print("Neighboring ungrouped sueprbin yields are %s."%sorted_neighbor_bin_yiel_diff)


				## create group with at most two neighboring bins with lowest yields
				new_group_mates = []
				if len(good_neighbor_superbin_yield_diff_sorted) > 1:
					new_group_mates.append(good_neighbor_superbin_yield_diff_sorted[0])
					new_group_mates.append(good_neighbor_superbin_yield_diff_sorted[1])	
					
					if debug:
						print("new_group_mates[0] is %s."%good_neighbor_superbin_yield_diff_sorted[0])
						print("new_group_mates[1] is %s."%good_neighbor_superbin_yield_diff_sorted[1])
						print("------- Before the merge ------")
						print("superbin_groups_temp is %s."%superbin_groups_temp)

					superbin_groups_temp[cand_superbin_index_num].extend( [new_group_mates[0],new_group_mates[1]]	)
					superbin_groups_temp.remove( [new_group_mates[0]] )
					superbin_groups_temp.remove( [new_group_mates[1]] )
					
					if debug:
						print("------- After the merge ------")
						print("superbin_groups_temp is %s."%superbin_groups_temp)

				elif len(good_neighbor_superbin_yield_diff_sorted) > 0:
					new_group_mates.append(good_neighbor_superbin_yield_diff_sorted[0])


					if debug:
						print("new_group_mates[0] is %s."%good_neighbor_superbin_yield_diff_sorted[0])
						print("------- Before the merge ------")
						print("superbin_groups_temp is %s."%superbin_groups_temp)
					
					if debug:
						print("------- After the merge ------")
						print("superbin_groups_temp is %s."%superbin_groups_temp)


					superbin_groups_temp[cand_superbin_index_num].extend( [new_group_mates[0]]	)
					superbin_groups_temp.remove( [new_group_mates[0]] )
				else: 
					print("Need to run contingency plan")
					runContingency = True
			else: 
				print("Need to run contingency plan")
				runContingency = True

			if runContingency:

				if debug: print("Found no unpaired neighbor bins.")
				neighbor_superbin_avg_yield_differences = []
				neighbor_superbin_groups = []
						# if neighboring bins list is empty, find neighboring group with lowest closest average bin counts and add to that group
				for neighbor_superbin_index in neighbor_superbins:
					# for each neighbor superbin, get the group this superbin is associated with
					neighbor_superbin_groups.append( self.get_superbin_group_by_superbin_index( neighbor_superbin_index,  superbin_groups_temp  ) )  # create list of the full neighbor superbin groups. For example: [  [2,4,3], [1,5], ...   ]


				for neighbor_superbin_group_num,neighbor_superbin_group in enumerate(neighbor_superbin_groups):

						# loop over superbin group
						avg_of_difference = 0
						for superbin_index in neighbor_superbin_group:
							avg_of_difference +=  abs(  self.all_hist_values.get_scaled_QCD_superbin_counts(self.superbin_indices[ superbin_index ])  -  cand_superbin_yield) 

						avg_of_difference /= len(neighbor_superbin_group) ##
						neighbor_superbin_avg_yield_differences.append(avg_of_difference)


				## now find the neighbor group with the lowest average yield difference and add this superbin to that	
				paired_lists = zip(neighbor_superbin_groups, neighbor_superbin_avg_yield_differences)
				sorted_pairs = sorted(paired_lists, key=lambda x: x[1], reverse=False)
				neighbor_superbin_groups, sorted_list_B = zip(*sorted_pairs)
				
				best_neighbor_superbin_group = list(neighbor_superbin_groups[0]) ## should be the superbin group that is closest in average yield


				best_neighbor_superbin_group_num = superbin_groups_temp.index( best_neighbor_superbin_group  )  ## find which superbin group this belongs to 
				superbin_groups_temp[best_neighbor_superbin_group_num].extend([cand_superbin_index])
				superbin_groups_temp.remove([cand_superbin_index])

			## update superbin_groups
			superbin_groups  			  = list(superbin_groups_temp[:])
			there_are_ungrouped_superbins = self.check_for_ungrouped_superbins(superbin_groups)

			## remove this eventually 
			highest_SB_group_SB_index_cand = max(max(SB_index) for SB_index in superbin_groups)
			nSuperbins = len(self.superbin_indices)


			if (highest_SB_group_SB_index_cand + 1) != nSuperbins:
				raise ValueError("ERROR: highest SB group index higher than the total number of superbin indices :     %s vs %s"%(highest_SB_group_SB_index_cand, nSuperbins))

			if debug: print("there_are_ungrouped_superbins: %s."%there_are_ungrouped_superbins)

		return superbin_groups

	def get_superbin_group_by_superbin_index(self, superbin_index_to_locate, superbin_groups_temp):
		for superbin_group in superbin_groups_temp:	# superbin_group here would look like this: [ [1,3,4], [2,6], ... ]
			if superbin_index_to_locate in superbin_group:
				return superbin_group
		print("ERROR: did not find superbin %s in list of superbin groups %s"%(superbin_index_to_locate,superbin_groups_temp))
		return None


	def check_for_ungrouped_superbins(self,superbin_groups):
		n_ungrouped_superbins = 0
		for superbin_group in superbin_groups:
			if len(superbin_group) == 1: 
				if  self.all_hist_values.get_scaled_QCD_superbin_counts(self.superbin_indices[ superbin_group[0] ] ) < 50:  
					n_ungrouped_superbins+=1

		if n_ungrouped_superbins > 0: return True
		else: return False

	#####################################################
	####### END superbin group helper functions #########
	#####################################################


	def init_superbin_indices(self):
		_superbin_indices = []	# format [ [(x1,x2),(x2,x3),....], [(xi,yi), (xi+1,yi+1),.....], ...., [(xn-1,yn-1),(xn,yn)] ]	 _superbin_indices[<superbin #>][<order bin was added>][<coordinate>]
		for iii in range(self.bin_min_x,self.n_bins_x):  ## from 1 (or bin_min_x) to n_bins_x
			for jjj in range( self.bin_min_y, self.n_bins_y):  
				_superbin_indices.append([(iii,jjj)])  
		return _superbin_indices


	# given a tuple of coordinate indices (relative to the original TH2), return the superbin number (index) this coordinate is a part of
	def get_superbin_number(self, index_tuple): 
		for iii, superbin in enumerate(self.superbin_indices):
			if index_tuple in superbin:
				return iii

	# return the UNSCALED counts in superbin, you can get the scaled counts from the histInfo class get_scaled_superbin_counts method
	def counts_in_superbin(self, superbin_number):  
		_sum = 0
		for _tuple in self.superbin_indices[superbin_number]:
			_sum+= self.all_hist_values.list_all_counts[_tuple[0]][_tuple[1]]		  #self.hist_values[_tuple[0]][_tuple[1]]
		return _sum

	# return list of NON-EMPTY neighbor indices of all superbins in this superbin, in decreasing order of stat uncertainty
	def get_list_of_neighbor_superbins(self,_tuple):
		list_of_neighbors = [] # will be full of the superbin #s  
		neighbor_stat_uncert = []
		this_superbin_num = self.get_superbin_number( _tuple )
		for superbin_tuples in self.superbin_indices[this_superbin_num ]: # 

			# check to see if the hist_values neighbors of the superbin_tuples are already in this superbin
			# have to check up,down, right, left, have to check the indices are valid
			index_x = superbin_tuples[0] #_tuple[0]
			index_y = superbin_tuples[1] #_tuple[1]

			if ( ( index_x+1 ) < self.n_bins_x ):
				if (index_x+1,index_y) not in self.superbin_indices[this_superbin_num ]:   
					if self.counts_in_superbin(self.get_superbin_number(  (index_x+1,index_y)  )) > 0:
						list_of_neighbors.append((index_x+1,index_y))
						neighbor_stat_uncert.append( self.all_hist_values.get_bin_total_uncert( self.superbin_indices[self.get_superbin_number(  (index_x+1,index_y)  )]   ) )
			if ( ( index_x-1 ) >= self.bin_min_x ):
				if  (index_x-1,index_y) not in self.superbin_indices[this_superbin_num ]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x-1,index_y)  )) > 0:
						list_of_neighbors.append((index_x-1,index_y))
						neighbor_stat_uncert.append( self.all_hist_values.get_bin_total_uncert( self.superbin_indices[self.get_superbin_number(  (index_x-1,index_y)  )] ))
			if ( ( index_y+1 )< self.n_bins_y ):
				if (index_x,index_y+1) not in self.superbin_indices[this_superbin_num ]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x,index_y+1)  )) > 0:
						list_of_neighbors.append((index_x,index_y+1))
						neighbor_stat_uncert.append( self.all_hist_values.get_bin_total_uncert( self.superbin_indices[self.get_superbin_number(  (index_x,index_y+1)  )] ))
			if ( ( index_y-1 ) >= self.bin_min_y ):
				if (index_x,index_y-1) not in self.superbin_indices[this_superbin_num]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x,index_y-1)  )) > 0:
						list_of_neighbors.append((index_x,index_y-1))
						neighbor_stat_uncert.append( self.all_hist_values.get_bin_total_uncert( self.superbin_indices[self.get_superbin_number(  (index_x,index_y-1)  )] ))
		list_of_neighbor_superbins = []
		# then convert this to a list of superbin #s 
		for neighbor_tuple in list_of_neighbors:
			if self.counts_in_superbin(self.get_superbin_number(neighbor_tuple)) ==0:
				continue
			neighbor_superbin_number = self.get_superbin_number(neighbor_tuple)
			if neighbor_superbin_number not in list_of_neighbor_superbins:
				list_of_neighbor_superbins.append(neighbor_superbin_number)
		
		pairs = zip(list_of_neighbor_superbins, neighbor_stat_uncert)
		pairs_sorted = sorted(pairs, key=lambda x: x[1], reverse=True)
		list_of_neighbors_sorted = [p[0] for p in pairs_sorted]

		return list_of_neighbors_sorted


	# return list of ALL neighbor indices of all bins in this superbin (empty or non-empty!!!)
	def get_list_of_all_neighbors(self,_tuple):

		list_of_neighbors = [] # will be full of the superbin #s  
		neighbor_stat_uncert = []

		this_superbin_num = self.get_superbin_number( _tuple )
		for superbin_tuples in self.superbin_indices[this_superbin_num ]: # 

			# check to see if the hist_values neighbors of the superbin_tuples are already in this superbin
			# have to check up,down, right, left, have to check the indices are valid
			index_x = superbin_tuples[0] #_tuple[0]
			index_y = superbin_tuples[1] #_tuple[1]

			if ( ( index_x+1 ) < self.n_bins_x ):
				if (index_x+1,index_y) not in self.superbin_indices[this_superbin_num ]:   
					if self.counts_in_superbin(self.get_superbin_number(  (index_x+1,index_y)  )) > -1:
						list_of_neighbors.append((index_x+1,index_y))
						neighbor_stat_uncert.append( self.all_hist_values.get_bin_total_uncert(  self.superbin_indices[self.get_superbin_number(  (index_x+1,index_y)  )]  ))
			if ( ( index_x-1 ) >= self.bin_min_x ):
				if  (index_x-1,index_y) not in self.superbin_indices[this_superbin_num ]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x-1,index_y)  )) > -1:
						list_of_neighbors.append((index_x-1,index_y))
						neighbor_stat_uncert.append( self.all_hist_values.get_bin_total_uncert( self.superbin_indices[self.get_superbin_number(  (index_x-1,index_y))]  ))
			if ( ( index_y+1 )< self.n_bins_y ):
				if (index_x,index_y+1) not in self.superbin_indices[this_superbin_num ]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x,index_y+1)  )) > -1:
						list_of_neighbors.append((index_x,index_y+1))
						neighbor_stat_uncert.append( self.all_hist_values.get_bin_total_uncert(self.superbin_indices[self.get_superbin_number(  (index_x,index_y+1))] ))
			if ( ( index_y-1 ) >= self.bin_min_y ):
				if (index_x,index_y-1) not in self.superbin_indices[this_superbin_num]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x,index_y-1)  )) > -1:
						list_of_neighbors.append((index_x,index_y-1))
						neighbor_stat_uncert.append( self.all_hist_values.get_bin_total_uncert(self.superbin_indices[self.get_superbin_number(  (index_x,index_y-1))] ))
		list_of_neighbor_superbins = []
		# then convert this to a list of superbin #s 
		for neighbor_tuple in list_of_neighbors:
			neighbor_superbin_number = self.get_superbin_number(neighbor_tuple)
			if neighbor_superbin_number not in list_of_neighbor_superbins:
				list_of_neighbor_superbins.append(neighbor_superbin_number)

		pairs = zip(list_of_neighbor_superbins, neighbor_stat_uncert)
		pairs_sorted = sorted(pairs, key=lambda x: x[1], reverse=True)
		list_of_neighbors_sorted = [p[0] for p in pairs_sorted]

		return list_of_neighbors_sorted


	def get_list_of_empty_neighbors(self,_tuple):
		start_time = time.time()
		# get only superbins in the direction of the nearest non-empty superbin

		list_of_neighbors = [] # will be full of the superbin #s  
		for superbin_tuples in self.superbin_indices[self.get_superbin_number( _tuple ) ]: # all superbin tuples in superbin 

			# check to see if the hist_values neighbors of the superbin_tuples are already in this superbin
			# have to check up,down, right, left, have to check the indices are valid
			index_x = superbin_tuples[0]
			index_y = superbin_tuples[1]

			#print("search x/y: %s/%s"%(search_x,search_y))
			#### check adjacent bins
			if ( ( index_x+1 )< self.n_bins_x ):
				if not (index_x+1,index_y) in self.superbin_indices[self.get_superbin_number( _tuple ) ]:
					if self.all_hist_values.list_all_counts[index_x+1][index_y] == 0:					   #self.hist_values[index_x+1][index_y] == 0:		
						list_of_neighbors.append((index_x+1,index_y))
			if ( ( index_x-1 ) >= self.bin_min_x ):
				if not (index_x-1,index_y) in self.superbin_indices[self.get_superbin_number( _tuple ) ]:
					if self.all_hist_values.list_all_counts[index_x-1][index_y] == 0:				 #self.hist_values[index_x-1][index_y] == 0:
						list_of_neighbors.append((index_x-1,index_y))
			if ( ( index_y+1 )< self.n_bins_y ):
				if not (index_x,index_y+1) in self.superbin_indices[self.get_superbin_number( _tuple ) ]:
					if self.all_hist_values.list_all_counts[index_x][index_y+1] == 0:						#self.hist_values[index_x][index_y+1] == 0:
						list_of_neighbors.append((index_x,index_y+1))
			if ( ( index_y-1 ) >= self.bin_min_y ):
				if not (index_x,index_y-1) in self.superbin_indices[self.get_superbin_number( _tuple ) ]:
					if self.all_hist_values.list_all_counts[index_x][index_y-1] == 0:				   #self.hist_values[index_x][index_y-1] == 0:
						list_of_neighbors.append((index_x,index_y-1))
		list_of_neighbor_superbins = []
		# then convert this to a list of superbin #s 
		for neighbor_tuple in list_of_neighbors:
			neighbor_superbin_number = self.get_superbin_number(neighbor_tuple)
			if self.counts_in_superbin(neighbor_superbin_number) > 0: # double checking these are empty
				continue
			if neighbor_superbin_number not in list_of_neighbor_superbins:
				list_of_neighbor_superbins.append(neighbor_superbin_number)
		#print("get_list_of_empty_neighbors took %s to run"%(time.time() - start_time))
		return list_of_neighbor_superbins


	### attempt to use the "weighting" method to prevent gerrymandering
	def find_nearest_neighbor(self,empty_superbin, non_empty_superbins):

		empty_superbin_index = self.get_superbin_number(empty_superbin[0])

		empty_bin_x = self.superbin_indices[empty_superbin_index][0][0]
		empty_bin_y = self.superbin_indices[empty_superbin_index][0][1]

		nearest_index = None
		short_dist	= 1e10

		for non_empty_tuple in non_empty_superbins:
			non_empty_superbin = self.get_superbin_number( non_empty_tuple )
			for _bin in self.superbin_indices[non_empty_superbin]:
				distance = sqrt(pow(empty_bin_x - _bin[0],2)+pow(empty_bin_y - _bin[1],2))
				if distance	< short_dist:
					short_dist = distance
					nearest_index  = non_empty_superbin

		return nearest_index


	def there_are_empty_superbins(self):
		for iii in range(0,len(self.superbin_indices)):
			if (self.counts_in_superbin(iii) == 0):
				return True
		return False

 
	def get_bad_superbins(self):	## return list of superbins that have stat uncertainty greater than max threshold and scaled bin counts less than threshold  
		bad_superbins = []
		bad_superbins_uncert = []

		num_superbins = 0
		for iii,superbin in enumerate(self.superbin_indices):
			### check that the total bin stat uncertainty is less than max threshold allowed
			if self.counts_in_superbin( iii ) == 0: continue  #### don't want empty superbins 
			if self.all_hist_values.get_bin_total_uncert(superbin)  > self.max_stat_uncert: 
				bad_superbins.append(iii)
				bad_superbins_uncert.append( self.all_hist_values.get_bin_total_uncert(superbin) )
				#print("Stat uncertainty in bin %s is %s."%(iii,self.all_hist_values.get_bin_total_uncert(superbin)))
			### check that the total scaled/unscaled bin yields are not less than defined minimum bin count threshold
			elif self.all_hist_values.get_unscaled_QCD_superbin_counts(superbin)  < self.min_unscaled_QCD_bin_counts: 
				bad_superbins.append(iii)
				bad_superbins_uncert.append( self.all_hist_values.get_bin_total_uncert(superbin) )
			elif self.all_hist_values.get_scaled_QCD_superbin_counts(self.superbin_indices[iii]	) < self.min_scaled_QCD_bin_counts: 
				bad_superbins.append(iii)
				bad_superbins_uncert.append( self.all_hist_values.get_bin_total_uncert(superbin) )

			num_superbins+=1

		pairs = zip(bad_superbins, bad_superbins_uncert)
		pairs_sorted = sorted(pairs, key=lambda x: x[1], reverse=True)
		bad_superbins_sorted = [p[0] for p in pairs_sorted]

		return bad_superbins_sorted

	def get_lowest_count_neighbor(self, superbin_numbers):	## takes in a list of superbin numbers and returns superbin number that has the fewest overall scaled counts 
		index_fewest_counts = None
		fewest_counts = 1e15
		for superbin_number in superbin_numbers:
			#print("################	Checking counts: superbin number = %s, superbin_indices = %s, counts = %s, fewest counts = %s"%(superbin_number, self.superbin_indices[superbin_number],self.all_hist_values.get_scaled_superbin_counts( self.superbin_indices[superbin_number]   ), fewest_counts))
			if self.all_hist_values.get_scaled_superbin_counts( self.superbin_indices[superbin_number]   ) < fewest_counts:
				index_fewest_counts = superbin_number
				fewest_counts = self.all_hist_values.get_scaled_superbin_counts( self.superbin_indices[superbin_number]   )

		return index_fewest_counts

	def get_highest_stat_uncert_neighbor(self, superbin_numbers):	## takes in a list of superbin numbers and returns superbin number that has the fewest overall scaled counts 
		index_highest_uncert = None
		highest_uncert = -1e15
		for superbin_number in superbin_numbers:
			#print("################	Checking counts: superbin number = %s, superbin_indices = %s, counts = %s, fewest counts = %s"%(superbin_number, self.superbin_indices[superbin_number],self.all_hist_values.get_scaled_superbin_counts( self.superbin_indices[superbin_number]   ), fewest_counts))
			if self.all_hist_values.get_bin_total_uncert( self.superbin_indices[superbin_number]   ) > highest_uncert:
				index_highest_uncert = superbin_number
				highest_uncert = self.all_hist_values.get_bin_total_uncert( self.superbin_indices[superbin_number]   )

		return index_highest_uncert



	def centroid(self,superbin_num):

	    total_x = sum(x for x, y in self.superbin_indices[superbin_num])
	    total_y = sum(y for x, y in self.superbin_indices[superbin_num])
	    n = float(len( self.superbin_indices[superbin_num]))
	    return (total_x / n, total_y / n)


	def get_neighbor_distance_to_bad_bin(self,superbin_A_num, superbin_B_num):

	    cx_A, cy_A = self.centroid(superbin_A_num)
	    cx_B, cy_B = self.centroid(superbin_B_num)
	    return sqrt((cx_A - cx_B)**2 + (cy_A - cy_B)**2)


	def get_num_holes(self):
		num_holes = 0
		for superbin in self.superbin_indices: 
			if len(superbin) == 1 and abs(self.all_hist_values.get_scaled_superbin_counts( superbin)) < 1e-12: num_holes+=1

		return num_holes

	def do_bin_merging(self):
		all_bins_good = False
		iteration_count = 0


		################################
		#### new bin merging scheme ####  
		################################
		#  - get list of all bad superbins (that are not empty!)
		#  - choose a random bad superbin
		#  - get list of all neighbors to bad superbin
		#  - merge with neighbor with the fewest overall scaled counts
		#  - repeat until no bad superbins remain
		#  - fill in holes


		num_bad_superbins = 1e10
		while num_bad_superbins > 0:

			if iteration_count%10 ==0: print("Starting on run-through %i"%(iteration_count+1))

			### debug tool: check the total integrals from all BR contributions

			bad_superbins = self.get_bad_superbins()   ### get list of superbins that have stat uncertainty greater than max threshold and scaled bin counts less than threshold, ONLY for non-zero superbins
			#print("Bad superbins: ", bad_superbins)
			

			#random.seed(654321)
			#random_bad_superbin = random.choice(bad_superbins)	### this is a random superbin number

			bad_superbin = bad_superbins[0]
			bad_superbin_tuple = self.superbin_indices[bad_superbin][0]

			#print("Random bad superbin: ", random_bad_superbin)
			
			#random.seed(654321)
			#random_bad_superbin_tuple = random.choice( self.superbin_indices[random_bad_superbin] ) ### this is a tuple

			#print("Random bad tuple: ", random_bad_superbin_tuple)

			nearby_superbins = self.get_list_of_neighbor_superbins( bad_superbin_tuple   ) ## look for non-empty neighbors, decreasing order of stat uncertainty 

			if len(nearby_superbins) == 0: 
				nearby_superbins = self.get_list_of_all_neighbors( bad_superbin_tuple	)   	### this is a list of superbin numbers				


			#highest_stat_uncert_neighbor_index = self.get_highest_stat_uncert_neighbor(nearby_superbins)
			
			nearby_superbins_new = []
			to_move = []

			for nearby_superbin in nearby_superbins:
			    if (self.get_neighbor_distance_to_bad_bin(bad_superbin, nearby_superbin) > self.distance_threshold
			        or len(self.superbin_indices[nearby_superbin]) > self.superbin_size_threshold):
			        to_move.append(nearby_superbin)     
			    else:
			        nearby_superbins_new.append(nearby_superbin)    

			nearby_superbins = nearby_superbins_new + to_move 


			## check if neighbor index is already very large and far away
				## if some criteria are not passed, get a different neighbor
			#### TO DO ##########


			highest_stat_uncert_neighbor_index = nearby_superbins[0]


			### merge with neighbor with highest stat uncertainty

			self.superbin_indices[highest_stat_uncert_neighbor_index].extend( self.superbin_indices[bad_superbin]   )

			#print("extending superbins", self.superbin_indices)
			self.superbin_indices.pop( bad_superbin )
			#print("removing superbins", self.superbin_indices)

			## recalculate bad superbins
			bad_superbins = self.get_bad_superbins() 
			num_bad_superbins = len(bad_superbins)

			iteration_count+=1


		print("Done with main merging.")


		##########################################################
		##################### FILL IN HOLES ######################
		###########################################################
		### choose superbin indices at random, get a list of the empty bins that they are adjacent to, randomly add one of those bins to the superbin
		

		"""merge_empty_num = 0
		random.seed(654321)

		non_empty_superbins = []
		for iii, superbin_index in enumerate(self.superbin_indices):
					superbin_counts = self.counts_in_superbin(iii) 
					if superbin_counts > 0:
						non_empty_superbins.append( (self.superbin_indices[iii][0][0],self.superbin_indices[iii][0][1] ))


		print("Filling in holes.")
		while self.there_are_empty_superbins():   # need to make this function
			if merge_empty_num%100 == 0: 
				print("Starting run-through %s."%merge_empty_num)
				print("There are %s empty bins that need to be combined."%(self.get_num_holes()))
			
			# want smallest superbin that actually has neighbors

			#random_superbin = random.choice(non_empty_superbins)  ## need to choose from the non-empty superbins 
			#superbin_number = self.get_superbin_number( random_superbin  )

			#print("%s"%([superbin for superbin in non_empty_superbins]))

			non_empty_superbin_nums  = [ self.get_superbin_number( superbin  )	    for superbin in non_empty_superbins if len(self.get_list_of_empty_neighbors( superbin)) > 0 ]   
			non_empty_superbin_sizes = [ len(self.superbin_indices[ superbin_num ]) for superbin_num in non_empty_superbin_nums if len(self.get_list_of_empty_neighbors( self.superbin_indices[superbin_num][0] )) > 0]

			paired_lists = zip(non_empty_superbin_nums, non_empty_superbin_sizes)
			sorted_pairs = sorted(paired_lists, key=lambda x: x[1], reverse=True)
			non_empty_superbin_nums_sorted = [p[0] for p in sorted_pairs]
			
			non_empty_superbin_num = non_empty_superbin_nums_sorted[0] # smallest (by superbin constituents) non-empty superbin that actually has empty neighbors
			non_empty_superbin_tuple = self.superbin_indices[non_empty_superbin_num][0]

			nearby_bins = np.array(self.get_list_of_empty_neighbors( non_empty_superbin_tuple  ) )
			nearby_empty_bins = [  superbin_num for superbin_num in nearby_bins if (( abs(self.counts_in_superbin(superbin_num)) < 1e-12 ) ) ]  # and len(self.superbin_indices[superbin_num]) == 1
			
			if len(nearby_empty_bins) > 0:
				random_empty_neighbor = random.choice( nearby_empty_bins )
				self.superbin_indices[non_empty_superbin_num].append(  self.superbin_indices[random_empty_neighbor][0] )
				self.superbin_indices.remove( self.superbin_indices[random_empty_neighbor] )

			merge_empty_num+=1"""
		merge_empty_num = 0
		random.seed(123456)

		non_empty_superbins = []
		for iii, superbin_index in enumerate(self.superbin_indices):
					superbin_counts = self.counts_in_superbin(iii) 
					if superbin_counts > 0:
						non_empty_superbins.append( (self.superbin_indices[iii][0][0],self.superbin_indices[iii][0][1] ))


		print("Filling in holes.")
		while self.there_are_empty_superbins():   # need to make this function
			if merge_empty_num%100 == 0: print("Starting run-through %s."%merge_empty_num)
			random_superbin = random.choice(non_empty_superbins)  ## need to choose from the non-empty superbins 
			superbin_number = self.get_superbin_number( random_superbin  )

			nearby_bins = np.array(self.get_list_of_empty_neighbors( random_superbin  ) )
			nearby_empty_bins = [  superbin_num for superbin_num in nearby_bins if ((self.counts_in_superbin(superbin_num) < 1e-12 ) ) ]  # and len(self.superbin_indices[superbin_num]) == 1
			if len(nearby_empty_bins) > 0:
				random_empty_neighbor = random.choice( nearby_empty_bins )
				self.superbin_indices[superbin_number].append(  self.superbin_indices[random_empty_neighbor][0] )
				self.superbin_indices.remove( self.superbin_indices[random_empty_neighbor] )
			merge_empty_num+=1
		return
	

	def print_superbins(self):
		for superbin_num in range(0,len(self.superbin_indices)):
			print("Superbin %s ---- UNSCALED counts = %s, UNSCALED -- QCD -- counts = %s,  SCALED counts = %s"%(superbin_num,self.counts_in_superbin(superbin_num),self.all_hist_values.get_unscaled_QCD_superbin_counts(self.superbin_indices[superbin_num]), self.all_hist_values.get_scaled_superbin_counts( self.superbin_indices[superbin_num]) ))
		return



	## returns the distance (sqrt(pow(bin_x,2) + pow(bin_y,2))) of the superbin center to the origin, used for an alternate superbin ordering method
	def get_superbin_distance(self, superbin):
		avg_x = 0
		avg_y = 0
		n_bins_in_superbin =0
		for _tuple in superbin:
			avg_x += _tuple[0]
			avg_y += _tuple[1]
			n_bins_in_superbin+=1
		return sqrt( pow(avg_x/n_bins_in_superbin,2) + pow(avg_y/n_bins_in_superbin,2))

	## sort bins by descending event yield
	def sort_bins_by_descending_event_yield(self): 
		superbin_indices_copy = self.superbin_indices[:]

		superbin_indices_and_yields = [ ]

		for iii,superbin in enumerate(superbin_indices_copy):
			superbin_indices_and_yields.append( (iii, self.all_hist_values.get_scaled_superbin_counts( self.superbin_indices[iii]   )   ) )

		indices_and_dists_by_decr_yield = sorted(superbin_indices_and_yields, key=lambda x: x[1], reverse=True)
		indices_by_decreasing_yield = [index for index, _ in indices_and_dists_by_decr_yield]

		sorted_superbin_indices = []
		for superbin_index in indices_by_decreasing_yield:
			sorted_superbin_indices.append( self.superbin_indices[superbin_index] )


		# Create a plot of the superbin yields as a function of the final superbin number
		final_superbin_numbers = range(len(sorted_superbin_indices))
		final_yields = [yield_val for _, yield_val in indices_and_dists_by_decr_yield]

		plt.figure(figsize=(10, 6))
		plt.plot(final_superbin_numbers, final_yields, marker='o', linestyle='-', color='b')
		plt.title('Superbin Yields as a Function of Superbin Number (sorted by decreasing superbin yield)')
		plt.xlabel('Final Superbin Number')
		plt.ylabel('Superbin Yield')
		plt.grid(True)
		plt.tight_layout()

		# Save the plot to a file 
		plt.savefig('plots/statUncertaintyPlots/postMergedPlots/%s_post_merge_superbin_yields_%s_%s%s.png'%( self.QCD_str, self.year,self.technique_str,self.region))
		plt.close()



		return sorted_superbin_indices
	## sort bins by their raw distance (sqrt(pow(bin_x,2) + pow(bin_y,2))) to the origin, used for an alternate superbin ordering method 
	def sort_bins_by_raw_distance(self):
		superbin_indices_copy = self.superbin_indices[:]

		superbin_indices_and_distances = [ ]

		for iii,superbin in enumerate(superbin_indices_copy):
			superbin_indices_and_distances.append( (iii, self.get_superbin_distance(superbin)  ) )

		print("superbin_indices_and_distances is ", superbin_indices_and_distances)

		## sort list

		indices_and_dists_by_decr_dist = sorted(superbin_indices_and_distances, key=lambda x: x[1], reverse=False)
		indices_by_decreasing_distance = [index for index, _ in indices_and_dists_by_decr_dist]

		print("indices_by_decreasing_distance is ", indices_by_decreasing_distance)

		sorted_superbin_indices = []
		for superbin_index in indices_by_decreasing_distance:
			sorted_superbin_indices.append( self.superbin_indices[superbin_index] )


		return sorted_superbin_indices
	## sorts bins by making each superbin a graph node with edges connecting to neighbor superbins, and creating a "traveling salesman" problem
	## used for an alternate superbin ordering method
	def sort_bins_with_graphs(self):   

		superbin_indices_copy = self.superbin_indices[:]

		superbin_yields = []   # format: [(super_bin_1, 100), (super_bin_2, 150), (super_bin_3, 120), ...]
		neighbors = {}	 	   # format:	neighbors = { super_bin_1: [super_bin_2, super_bin_3], super_bin_2: [super_bin_1, super_bin_3], super_bin_3: [super_bin_1, super_bin_2], ... }
		for iii,superbin in enumerate(self.superbin_indices):

			## get yields of this superbin
			superbin_yields.append( ( iii, self.all_hist_values.get_scaled_superbin_counts( self.superbin_indices[iii]   )	)  )  
			## get neighbors of this superbin
			all_neighbor_superbin_indices = self.get_list_of_all_neighbors( self.superbin_indices[iii][0]  )

			neighbors[iii] = all_neighbor_superbin_indices
		arranged_bins = self.arrange_bins_optimized(superbin_yields, neighbors)  ## returns 
		new_superbin_indices = [ self.superbin_indices[ arranged_bins[iii][0]  ]  for iii in range(0,len(arranged_bins))	 ]

		# Create a plot of the superbin yields as a function of the final superbin number
		final_superbin_numbers = range(len(arranged_bins))
		final_yields = [yield_val for _, yield_val in arranged_bins]

		plt.figure(figsize=(10, 6))
		plt.plot(final_superbin_numbers, final_yields, marker='o', linestyle='-', color='b')
		plt.title('Superbin Yields as a Function of Superbin Number')
		plt.xlabel('Final Superbin Number')
		plt.ylabel('Superbin Yield')
		plt.grid(True)
		plt.tight_layout()

		# Save the plot to a file
		plt.savefig('plots/statUncertaintyPlots/postMergedPlots/%s_post_merge_superbin_yields_%s_%s%s.png'%(self.QCD_str,self.year,self.technique_str,self.region))
		plt.close()

		return new_superbin_indices


	def print_summary(self): # check the total integral of the PRE-merged distribution and the post-merged, linearized distribution to make sure they are the same

		total_counts_post_merge_unscaled = 0
		total_counts_original_unscaled = self.all_hist_values.all_hist_counts.Integral()  # 

		for iii,_ in enumerate(self.superbin_indices):
			total_counts_post_merge_unscaled += self.counts_in_superbin(iii)

		technique_title = "cut-based"
		if "NN" in self.technique_str:
			technique_title = "NN-based"


		print("===============================================================")
		print("===============================================================")
		print("--------------------------- SUMMARY ---------------------------")
		print("===============================================================")
		print("===============================================================")
		print("")
		print("")
		print("")
		print( "--------- Merged N_x/N_y = %s/%s original bins in the --- %s --- for year --- %s --- and --- %s --- technique  ------ QCD type:  %s -------- into %s linearized bins. "%(self.n_bins_x,self.n_bins_y, self.region, self.year, technique_title, self.QCD_str , len(self.superbin_indices) ))
		print(" --------- There were %s superbin groups (containing %s total superbins.)"%(len(self.superbin_groups), max( max( SB_index)  for SB_index in self.superbin_groups  ) + 1  ))
		print(" --------- Using original histogram bins x/y %s/%s and beyond."%(self.bin_min_x,self.bin_min_y))
		print( "--------- There were === %s === total counts in the original 2D histogram."%(total_counts_original_unscaled))
		print( "--------- There were === %s === total counts in the post-merged, linear histogram."%(total_counts_post_merge_unscaled))
		print("")
		print("")
		print("")
		print("")

		return


if __name__=="__main__":

	debug    = False
	dryRun   = False
	runEos 	 = True


	print("Calculating bin groupings for best statistical uncertainties")
		


	useQCDHT_opts = [True,False] # true = use HT-binned QCD, false means use Pt-binned QCD
	useQCDHT_strs  = ["QCDHT", "QCDPT"]

	years = ["2015","2016","2017","2018"]
	regions = ["SR","CR", "AT1b", "AT0b"  ]   # "AT0tb", "AT1tb", "SB1b", "SB0b"

	c = ROOT.TCanvas("c", "canvas", 1250, 1000)
	ROOT.gStyle.SetOptStat(0)

	hist_names = ["h_MSJ_mass_vs_MdSJ_","h_MSJ_mass_vs_MdSJ_NN_"]

	output_strs = ["", "NN_"]
	technique_strs = ["cut-based", "NN-based"]
	hist_names = ["h_MSJ_mass_vs_MdSJ_"]
	technique_strs = ["cut-based"]

	output_strs = [""]

	if debug:
		years = ["2015"]
		output_strs = [""]
		technique_strs = ["cut-based"]
		hist_names = ["h_MSJ_mass_vs_MdSJ_"]
		useQCDHT_opts= [True]



	for jjj,useQCDHT_opt in enumerate(useQCDHT_opts):
			

		text_output_path  = os.getenv('CMSSW_BASE') + "/src/postprocess/binMaps/"   #output_map_file_name
		group_output_path = os.getenv('CMSSW_BASE') + "/src/postprocess/superbinGroups/"
		neighbor_output_path = os.getenv('CMSSW_BASE') + "/src/postprocess/superbinNeighbors/"


		if not dryRun:
			SB_index_CB_cmd = 'rm %s/%s_superbin_indices_*.txt'%( text_output_path,useQCDHT_strs[jjj])
			SB_index_NN_cmd = 'rm %s/%s_superbin_indicesNN_*.txt'%(useQCDHT_strs[jjj],text_output_path)

			SB_group_CB_cmd    = 'rm %s/%s_superbin_groups_*.txt'%(group_output_path,useQCDHT_strs[jjj])
			SB_group_NN_cmd    = 'rm %s/%s_superbin_groupsNN_*.txt'%(group_output_path,useQCDHT_strs[jjj]) 

			SB_neighbors_CB_cmd = 'rm %s/%s_superbin_neighbor_*.txt'%(neighbor_output_path,useQCDHT_strs[jjj])
			SB_neighbors_NN_cmd = 'rm %s/%s_superbin_neighborsNN_*.txt'%(neighbor_output_path,useQCDHT_strs[jjj])

			os.system(SB_index_CB_cmd )
			os.system(SB_index_NN_cmd ) 
			os.system(SB_group_CB_cmd )
			os.system(SB_group_NN_cmd)
			os.system( SB_neighbors_CB_cmd)
			os.system( SB_neighbors_NN_cmd)


		for region in regions:
			for year in years:
				for iii,hist_name in enumerate(hist_names):
					if region in ["SB1b","SB0b"] and "NN" in hist_name: continue

					year_str = "2016preAPV"
					if year == "2016":  year_str = "2016postAPV"
					if year == "2017":  year_str = "2017"
					if year == "2018":  year_str = "2018"

					if dryRun: 
						print("===============================================================================")
						print("===============================================================================")
						print("===============================================================================")
						print("===========================	 WARNING !!	=================================")
						print("=========================   THIS IS A DRY RUN !!!!!   =========================")
						print("===============================================================================")
						print("===============================================================================")
						print("===============================================================================")

					if not dryRun:  
						out_txt_file = open("%s/%s_superbin_indices%s_%s.txt"%(text_output_path, useQCDHT_strs[jjj],output_strs[iii],year),"a")
						superbin_group_txt_file = open("%s/%s_superbin_groups%s_%s.txt"%(group_output_path, useQCDHT_strs[jjj], output_strs[iii],year),"a")
						superbin_neighbor_txt_file = open("%s/%s_superbin_neighbors%s_%s.txt"%(neighbor_output_path,useQCDHT_strs[jjj],output_strs[iii],year),"a")


					print("Creating maps for %s/%s/useQCDHT = %s"%(region,year,useQCDHT_strs[jjj]))

					TH2_hist_merged_name   = os.getenv('CMSSW_BASE') + "/src/postprocess/outputs/binMergingOutputs/postMergedFiles/allBR_statUncert_%s%s_%s_MERGED_BINS.root"%(output_strs[iii],region,year)
					TH2_hist_new_bins_name = os.getenv('CMSSW_BASE') + "/src/postprocess/outputs/binMergingOutputs/postMergedFiles/allBR_statUncert_%s%s_%s_NEW_BINS.root"%(output_strs[iii],region,year)
					out_file = ROOT.TFile.Open(TH2_hist_new_bins_name,"RECREATE")

					# give histogram to constructor
					testCase = combineHistBins(year, region, output_strs[iii], useQCDHT_opt, debug,dryRun,runEos)
					#create a dummy histogram with dimensions 20x22
					merged_bins = testCase.superbin_indices
					bin_map_hist = ROOT.TH2F("bin_map_hist%s"%output_strs[iii], ("Superbin Map for the %s for %s (%s); disuperjet mass (GeV); avg. superjet mass (GeV)"%(region, year_str,technique_strs[iii])), testCase.n_bins_x,1250., 10000, testCase.n_bins_y, 500, 5000)  # 375 * 125
					stat_uncert_hist = ROOT.TH2F("stat_uncert_hist%s"%output_strs[iii], ("Superbin Statistical Uncertainty in the %s for %s (%s); disuperjet mass (GeV); avg. superjet mass (GeV)"%(region, year_str,technique_strs[iii])), testCase.n_bins_x,1250., 10000, testCase.n_bins_y, 500, 5000)  # 375 * 125
					merged_hist_count = ROOT.TH2F("merged_hist_count%s"%output_strs[iii], ("Unscaled Superbin Event Yields (post bin merging) in the %s for %s (%s); disuperjet mass (GeV); avg. superjet mass (GeV)"%(region, year_str,technique_strs[iii])), testCase.n_bins_x,1250., 10000, testCase.n_bins_y, 500, 5000)  # 375 * 125
					bin_map_hist.GetYaxis().SetTitleOffset(1.5)
					stat_uncert_hist.GetYaxis().SetTitleOffset(1.5)
					merged_hist_count.GetYaxis().SetTitleOffset(1.5)

					stat_uncert_hist.GetZaxis().SetTitle("Stat. Uncertainty")
					stat_uncert_hist.GetZaxis().SetTitleOffset(1.35)
					stat_uncert_hist.GetZaxis().SetTitleSize(0.035)
					stat_uncert_hist.GetZaxis().SetLabelSize(0.035)
					stat_uncert_hist.GetZaxis().SetLabelOffset(0.005)

					merged_hist_count.GetZaxis().SetTitle("Events")
					merged_hist_count.GetZaxis().SetTitleOffset(1.35)
					merged_hist_count.GetZaxis().SetTitleSize(0.035)
					merged_hist_count.GetZaxis().SetLabelSize(0.035)
					merged_hist_count.GetZaxis().SetLabelOffset(0.005)



					
					# Set up random, visible colors
					n_colors = len(merged_bins)
					#n_colors = min(n_colors, 10000)  # Cap to avoid too many colors

					color_indices = array.array('i')  # C-style int array for ROOT
					for i in range(2,n_colors+2):
						r = random.uniform(0.2, 1.0)
						g = random.uniform(0.2, 1.0)
						b = random.uniform(0.2, 1.0)
						color_index =  i   # avoid collision with default color table
						ROOT.TColor(color_index, r, g, b)
						color_indices.append(color_index)

					ROOT.gStyle.SetPalette(n_colors, color_indices)



					R = ROOT.TRandom3()
					superbin_groups  = testCase.superbin_groups

					# Build lookup: superbin index to group number
					superbin_to_group = {}
					for group_idx, sb_list in enumerate(superbin_groups):
						for sb_idx in sb_list:
							superbin_to_group[sb_idx] = group_idx

					# TLatex for drawing text
					latex = ROOT.TLatex()
					latex.SetTextSize(0.03)
					latex.SetTextAlign(22)  # center alignment
					latex.SetNDC(False)

					random.seed(54321)
					superbin_color_map = {}
					rand_list = list(range(2,len(merged_bins)+2 ))
					random.shuffle(rand_list)

					for superbin_index in range(len(merged_bins)):
						superbin_color_map[superbin_index] = rand_list[superbin_index]

					index_counter = 0
					for superbin_index, superbin in enumerate(merged_bins):

						superbin_color = superbin_color_map[superbin_index]

						for smallbin in superbin:
							if testCase.counts_in_superbin(superbin_index) == 0:
								continue					

							bin_map_hist.SetBinContent(smallbin[0]+1,smallbin[1]+1, superbin_color + 0.5)
							stat_uncert_hist.SetBinContent(smallbin[0]+1,smallbin[1]+1, testCase.all_hist_values.get_bin_total_uncert(testCase.superbin_indices[superbin_index]))	#   1.0/sqrt(testCase.counts_in_superbin(superbin_index))   
							merged_hist_count.SetBinContent(smallbin[0]+1,smallbin[1]+1, testCase.counts_in_superbin(superbin_index))
						index_counter+=1

						
					if not dryRun:  



						#print("Writing outputs for QCD type = %s/%s/%s/%s/"%(useQCDHT_strs[jjj],region,year,hist_name))

						out_txt_file.write("%s/%s/number of bins = %s/%s\n"%(year,region, len(testCase.superbin_indices), testCase.superbin_indices))
						out_txt_file.close()


						highest_SB_group_SB_index = max(max(SB_index) for SB_index in testCase.superbin_groups)
						if (highest_SB_group_SB_index + 1) != len(testCase.superbin_indices): 
							raise ValueError("ERROR: %s / %s ---------------> Number of superbins in SB groups is different from the number of superbins: %s vs %s respectively."%( year, region, highest_SB_group_SB_index, len(testCase.superbin_indices)))

						superbin_group_txt_file.write("%s/%s/number of superbin groups = %s/%s\n"%(year,region, len(testCase.superbin_groups), testCase.superbin_groups))
						superbin_group_txt_file.close()

						superbin_neighbor_txt_file.write("%s/%s/number of superbin neighbors = %s/%s\n"%(year,region, len(testCase.superbin_neighbors), testCase.superbin_neighbors))
						superbin_neighbor_txt_file.close()
						


					#ROOT.gStyle.SetPalette(0)  # Suppress default palette
					bin_map_hist.GetZaxis().SetRangeUser(2,len(merged_bins)+ 1 )
					bin_map_hist.Draw("col")

					label = ROOT.TLatex()
					label.SetNDC(True)  
					label.SetTextSize(0.02)
					label.SetTextAlign(13) 
					label.DrawLatex(0.25, 0.85, "Numbers = Superbin Group IDs")

					nSuperbins_text = ROOT.TLatex()
					nSuperbins_text.SetNDC(True)  
					nSuperbins_text.SetTextSize(0.03)       
					nSuperbins_text.SetTextAlign(11)        # left-aligned, bottom
					nSuperbins_text.SetTextFont(62)         
					nSuperbins_text.DrawLatex(0.15, 0.02, 
					    "Number of superbins: %s" % (len(merged_bins)))

					for superbin_index, superbin in enumerate(merged_bins):

						x_vals = []
						y_vals = []

						# print superbin group number at centroid 
						if superbin_index not in superbin_to_group:
							continue
						group_id = superbin_to_group[superbin_index]

						# Compute geometric center
						x_vals = [bin_map_hist.GetXaxis().GetBinCenter(ix+1) for (ix, iy) in superbin]
						y_vals = [bin_map_hist.GetYaxis().GetBinCenter(iy+1) for (ix, iy) in superbin]
						x_avg = sum(x_vals) / len(x_vals)
						y_avg = sum(y_vals) / len(y_vals)

						# Find actual bin center in this superbin closest to (x_avg, y_avg)
						best_bin = None
						best_dist = float("inf")
						for (ix, iy) in superbin:
							x = bin_map_hist.GetXaxis().GetBinCenter(ix+1)
							y = bin_map_hist.GetYaxis().GetBinCenter(iy+1)
							dist2 = (x - x_avg)**2 + (y - y_avg)**2
							if dist2 < best_dist:
								best_dist = dist2
								best_bin = (x, y)

						# Draw label at the best bin center
						if best_bin:
							x_text, y_text = best_bin
							latex.DrawLatex(x_text, y_text, str(group_id))


					write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.31,CMS_label_ypos = 0.92, SIM_label_ypos = 0.918, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
					c.SaveAs( os.getenv('CMSSW_BASE')+  "/src/postprocess/plots/statUncertaintyPlots/postMergedPlots/%s_bin_map_%s%s_%s.png"%(useQCDHT_strs[jjj], output_strs[iii],region,year)) 
					

					ROOT.gStyle.SetPalette(ROOT.kViridis)
					c.SetRightMargin(0.18)

					stat_uncert_hist.Draw("colz")
					write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.31,CMS_label_ypos = 0.92, SIM_label_ypos = 0.918, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
					c.SaveAs(os.getenv('CMSSW_BASE')+  "/src/postprocess/plots/statUncertaintyPlots/postMergedPlots/%s_stat_uncert_%s%s_%s.png"%(useQCDHT_strs[jjj],output_strs[iii],region,year)) 

					ROOT.gStyle.SetPalette(ROOT.kViridis)

					merged_hist_count.Draw("colz")
					write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.31,CMS_label_ypos = 0.92, SIM_label_ypos = 0.918, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False)
					c.SaveAs(os.getenv('CMSSW_BASE')+  "/src/postprocess/plots/statUncertaintyPlots/postMergedPlots/%s_bin_counts_%s%s_%s.png"%(useQCDHT_strs[jjj],output_strs[iii],region,year)) 
					
					c.SetRightMargin(0.05)


