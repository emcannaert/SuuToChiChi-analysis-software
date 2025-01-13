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
import networkx as nx

import argparse
####  calculateStatisticalUncertaintyBins.py
####  Written by Ethan Cannaert, September 2023, updated July 2024, updated again November 2024
####  Opens up a TH2 (22x20 bins, avg superjet mass vs diSuperjet mass)
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

	def __init__(self,year,region,technique_str,debug=False, dryRun=False):   #constructor will convert TH2 to a 2D array, do the optimized bin merging, and then return a TH2 with those associated bins

		self.year = year
		self.region = region
		self.technique_str = technique_str
		self.dryRun = dryRun
		self.max_stat_uncert = 0.20  ## maximum statistical uncertainty
		self.min_unscaled_QCD_bin_counts   = 0.0   ## the minimum number of unscaled QCD events required to be in each bin, better to make this 1 or more to prevent weird migration stuff
		self.min_scaled_QCD_bin_counts   = 0.0   ## the minimum number of unscaled QCD events required to be in each bin, better to make this 1 or more to prevent weird migration stuff


		self.includeTTJetsMCHT800to1200 = False
		self.includeWJets   			= False
		self.includeTTo 				= False

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

		self.bin_min_x = 3  ## start x bin in the 2D distribution (diSJ mass)
		self.bin_min_y = 1  ## start y bin in the 2D distribution (SJ mass)

		self.n_bins_x = 22
		self.n_bins_y = 20

		if region in ["SB1b","SB0b"]:


			self.bin_min_x = 0  ## start x bin in the 2D distribution (diSJ mass)
			self.bin_min_y = 0  ## start y bin in the 2D distribution (SJ mass)
			self.n_bins_x = 15
			self.n_bins_y = 12
			self.max_stat_uncert = 0.30  ## maximum statistical uncertainty
		self.all_hist_values =  histInfo.histInfo(year,region, self.bin_min_x, self.bin_min_y, self.n_bins_x, self.n_bins_y, self.technique_str, self.includeTTJetsMCHT800to1200, self.includeWJets, self.includeTTo,  debug)    #histInfo.histInfo(year,region) ## everywhere there is originally a sqrt, will need to call get_bin_total_uncert and get 
		self.superbin_indices = self.init_superbin_indices()     
		
		#if not self.dryRun: self.plot_before_syst_plot()   # plot the "before" image of counts and syst uncertainty 
 
		print("Starting the process of merging bins.")
		self.do_bin_merging()
		print("Finished with bin merging.")

		#self.superbin_indices = self.sort_bins_with_graphs() ## sorts bins by approximate location in 2D
		#self.superbin_indices = self.sort_bins_by_raw_distance() ## sort bins by their raw distance from the origin in the 2D place
		self.superbin_indices = self.sort_bins_by_descending_event_yield() ## sort bins by descending bin yield

		#self.print_final_hist()

		self.print_superbins()   ### print out scaled and unscaled counts in each superbin post merging
		self.print_summary()

	def print_final_hist(self):
		hist_map = [ [-999]*self.n_bins_y for i in range(self.bin_min_x, self.n_bins_x)]
		print("Histogram bin map:")
		for iii in range(self.bin_min_x,self.n_bins_x):
			for jjj in range(self.bin_min_y, self.n_bins_y):
				hist_map[iii][jjj] = self.get_superbin_number( (iii,jjj))

		print('\n'.join(' '.join(str(x) for x in row) for row in hist_map))

		print("Histogram bin statistical uncertainties")
		for iii in range(self.bin_min_x,self.n_bins_x):
			for jjj in range(self.bin_min_y, self.n_bins_y):
				if(  self.counts_in_superbin(self.get_superbin_number( (iii,jjj))) > 0  ):
					hist_map[iii][jjj] = self.all_hist_values.get_bin_total_uncert(self.superbin_indices[self.get_superbin_number( (iii,jjj))] ) #  1.0/sqrt(self.counts_in_superbin(self.get_superbin_number( (iii,jjj ) ) ) ) 
				else:
					hist_map[iii][jjj] = 0.0

		print('\n'.join(' '.join(str(x) for x in row) for row in hist_map))

		return

	def init_superbin_indices(self):
		_superbin_indices = []    # format [ [(x1,x2),(x2,x3),....], [(xi,yi), (xi+1,yi+1),.....], ...., [(xn-1,yn-1),(xn,yn)] ]     _superbin_indices[<superbin #>][<order bin was added>][<coordinate>]
		for iii in range(self.bin_min_x,self.n_bins_x):  ## from 1 (or bin_min_x) to n_bins_x
			for jjj in range( self.bin_min_y, self.n_bins_y):  
				_superbin_indices.append([(iii,jjj)])  
		return _superbin_indices
	def get_superbin_number(self, index_tuple): # given a tuple of coordinate indices (relative to the original TH2), return the superbin number this coordinate is a part of
		for iii, superbin in enumerate(self.superbin_indices):
			#print("The superbin is ", superbin)
			#print("Index tuple is ", index_tuple)
			if index_tuple in superbin:
				return iii
	def counts_in_superbin(self, superbin_number):  ### UNSCALED counts in superbin, you can get the scaled counts from the histInfo class get_scaled_superbin_counts method
		_sum = 0
		for _tuple in self.superbin_indices[superbin_number]:
			_sum+= self.all_hist_values.list_all_counts[_tuple[0]][_tuple[1]]          #self.hist_values[_tuple[0]][_tuple[1]]
		return _sum
	def all_bins_are_good(self):      ## check if all bins have start uncertainty that is too low or too few bin counts
		for iii, superbin in enumerate(self.superbin_indices):
			n_counts = self.counts_in_superbin(iii)
			if n_counts > 0: # don't want to divide by 0
				#print("Number of counts in superbin: ", n_counts)
				if self.all_hist_values.get_bin_total_uncert(self.superbin_indices[iii])  > self.max_stat_uncert: return False   # 1.0/sqrt(self.counts_in_superbin( iii ) )
				### check that the total bin yields
				if self.all_hist_values.get_unscaled_QCD_superbin_counts(self.superbin_indices[iii])  < self.min_unscaled_QCD_bin_counts: return False
				if self.all_hist_values.get_scaled_QCD_superbin_counts(self.superbin_indices[iii]    ) < self.min_scaled_QCD_bin_counts: return False
			else:
				return False
		return True
	def get_list_of_neighbors(self,_tuple):
		# return list of NON-EMPTY neighbor indices of all bins in this superbin  
		list_of_neighbors = [] # will be full of the superbin #s  
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
			if ( ( index_x-1 ) >= self.bin_min_x ):
				if  (index_x-1,index_y) not in self.superbin_indices[this_superbin_num ]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x-1,index_y)  )) > 0:
						list_of_neighbors.append((index_x-1,index_y))
			if ( ( index_y+1 )< self.n_bins_y ):
				if (index_x,index_y+1) not in self.superbin_indices[this_superbin_num ]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x,index_y+1)  )) > 0:
						list_of_neighbors.append((index_x,index_y+1))
			if ( ( index_y-1 ) >= self.bin_min_y ):
				if (index_x,index_y-1) not in self.superbin_indices[this_superbin_num]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x,index_y-1)  )) > 0:
						list_of_neighbors.append((index_x,index_y-1))
		list_of_neighbor_superbins = []
		# then convert this to a list of superbin #s 
		for neighbor_tuple in list_of_neighbors:
			if self.counts_in_superbin(self.get_superbin_number(neighbor_tuple)) ==0:
				continue
			neighbor_superbin_number = self.get_superbin_number(neighbor_tuple)
			if neighbor_superbin_number not in list_of_neighbor_superbins:
				list_of_neighbor_superbins.append(neighbor_superbin_number)
		return list_of_neighbor_superbins


		#### needs to be changed 
	def get_list_of_all_neighbors(self,_tuple):

		# return list of ALL neighbor indices of all bins in this superbin (empty or non-empty!!!)
		list_of_neighbors = [] # will be full of the superbin #s  
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
			if ( ( index_x-1 ) >= self.bin_min_x ):
				if  (index_x-1,index_y) not in self.superbin_indices[this_superbin_num ]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x-1,index_y)  )) > -1:
						list_of_neighbors.append((index_x-1,index_y))
			if ( ( index_y+1 )< self.n_bins_y ):
				if (index_x,index_y+1) not in self.superbin_indices[this_superbin_num ]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x,index_y+1)  )) > -1:
						list_of_neighbors.append((index_x,index_y+1))
			if ( ( index_y-1 ) >= self.bin_min_y ):
				if (index_x,index_y-1) not in self.superbin_indices[this_superbin_num]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x,index_y-1)  )) > -1:
						list_of_neighbors.append((index_x,index_y-1))
		list_of_neighbor_superbins = []
		# then convert this to a list of superbin #s 
		for neighbor_tuple in list_of_neighbors:
			neighbor_superbin_number = self.get_superbin_number(neighbor_tuple)
			if neighbor_superbin_number not in list_of_neighbor_superbins:
				list_of_neighbor_superbins.append(neighbor_superbin_number)
		return list_of_neighbor_superbins

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
					if self.all_hist_values.list_all_counts[index_x+1][index_y] == 0:                       #self.hist_values[index_x+1][index_y] == 0:		
						list_of_neighbors.append((index_x+1,index_y))
			if ( ( index_x-1 ) >= self.bin_min_x ):
				if not (index_x-1,index_y) in self.superbin_indices[self.get_superbin_number( _tuple ) ]:
					if self.all_hist_values.list_all_counts[index_x-1][index_y] == 0:                 #self.hist_values[index_x-1][index_y] == 0:
						list_of_neighbors.append((index_x-1,index_y))
			if ( ( index_y+1 )< self.n_bins_y ):
				if not (index_x,index_y+1) in self.superbin_indices[self.get_superbin_number( _tuple ) ]:
					if self.all_hist_values.list_all_counts[index_x][index_y+1] == 0:                        #self.hist_values[index_x][index_y+1] == 0:
						list_of_neighbors.append((index_x,index_y+1))
			if ( ( index_y-1 ) >= self.bin_min_y ):
				if not (index_x,index_y-1) in self.superbin_indices[self.get_superbin_number( _tuple ) ]:
					if self.all_hist_values.list_all_counts[index_x][index_y-1] == 0:                   #self.hist_values[index_x][index_y-1] == 0:
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
	def check_island_neighbors(self,superbin_number):
		start_time = time.time()
		#print("island superbin is %s"%self.superbin_indices[superbin_number])
		#print("island superbin is %s bins long"%len(self.superbin_indices[superbin_number]))
		for island_tuple in self.superbin_indices[superbin_number]:
			for adj_superbin in self.superbin_indices:
				if self.get_superbin_number(adj_superbin[0]) == superbin_number:
					continue # don't want this superbin to compare to itself.
				if self.counts_in_superbin(self.get_superbin_number(adj_superbin[0])) == 0:
					continue
				if (island_tuple[0]+1,island_tuple[1]) in adj_superbin:
					#print("check_island_neighbors took %s to run"%(time.time() - start_time))
					return False
				if (island_tuple[0]-1,island_tuple[1]) in adj_superbin:
					#print("check_island_neighbors took %s to run"%(time.time() - start_time))
					return False
				if (island_tuple[0],island_tuple[1]+1) in adj_superbin:
					#print("check_island_neighbors took %s to run"%(time.time() - start_time))
					return False
				if (island_tuple[0],island_tuple[1]-1) in adj_superbin:
					#print("check_island_neighbors took %s to run"%(time.time() - start_time))
					return False
		#print("check_island_neighbors took %s to run"%(time.time() - start_time))
		return True
	def find_empty_neighbors(self, superbin_tuple):
		start_time = time.time()
		list_of_empty_neighbors = []
		superbin = self.superbin_indices[self.get_superbin_number(superbin_tuple)]  ## the superbin of interest
		for tuple_ in superbin:
			if  (tuple_[0]+1,tuple_[1]) not in superbin:
				if (tuple_[0]+1) < self.n_bins_x:
					counts = self.counts_in_superbin(self.get_superbin_number( (tuple_[0]+1,tuple_[1])  ))
					if (counts is not None) and (counts == 0) and (self.get_superbin_number( (tuple_[0]+1,tuple_[1])  ) not in list_of_empty_neighbors) :
						list_of_empty_neighbors.append( self.get_superbin_number( (tuple_[0]+1,tuple_[1])  ) )
			if (tuple_[0]-1,tuple_[1]) not in superbin:
				if (tuple_[0]-1) >= self.bin_min_x: ## changed this to >= from >
					counts = self.counts_in_superbin(self.get_superbin_number( (tuple_[0]-1,tuple_[1])  ))
					if (counts is not None) and (counts == 0) and (self.get_superbin_number( (tuple_[0]-1,tuple_[1])  ) not in list_of_empty_neighbors) :
						list_of_empty_neighbors.append( self.get_superbin_number( (tuple_[0]-1,tuple_[1])  ) )
			if (tuple_[0],tuple_[1]+1) not in superbin:
				if (tuple_[1]+1) < self.n_bins_y:
					counts = self.counts_in_superbin(self.get_superbin_number( (tuple_[0],tuple_[1]+1)  ))
					if (counts is not None) and (counts == 0) and (self.get_superbin_number( (tuple_[0],tuple_[1]+1)  ) not in list_of_empty_neighbors) :
						list_of_empty_neighbors.append( self.get_superbin_number( (tuple_[0],tuple_[1]+1)  ) )
			if (tuple_[0],tuple_[1]-1) not in superbin:
				if (tuple_[1]-1) >= self.bin_min_y:
					counts = self.counts_in_superbin(self.get_superbin_number( (tuple_[0],tuple_[1]-1)  ))
					if (counts is not None) and (counts == 0) and (self.get_superbin_number( (tuple_[0],tuple_[1]-1)  ) not in list_of_empty_neighbors) :
						list_of_empty_neighbors.append( self.get_superbin_number( (tuple_[0],tuple_[1]-1)  ) )
		#rint("find_empty_neighbors took %s to run"%(time.time() - start_time))
		return list_of_empty_neighbors   # return list of empty nearby superbins

	def find_nearest_neighbor(self,empty_superbin, non_empty_superbins):

		empty_superbin_index = self.get_superbin_number(empty_superbin[0])

		empty_bin_x = self.superbin_indices[empty_superbin_index][0][0]
		empty_bin_y = self.superbin_indices[empty_superbin_index][0][1]

		nearest_index = None
		short_dist    = 1e10

		for non_empty_tuple in non_empty_superbins:
			non_empty_superbin = self.get_superbin_number( non_empty_tuple )
			for _bin in self.superbin_indices[non_empty_superbin]:
				distance = sqrt(pow(empty_bin_x - _bin[0],2)+pow(empty_bin_y - _bin[1],2))
				if distance	< short_dist:
					short_dist = distance
					nearest_index  = non_empty_superbin

		return nearest_index


	def fill_in_holes(self):

		## loop over all rows 
		# fill in holes within each superjet

		#for each row and column, store the max and min bin index 
		maxBin_row     = self.n_bins_x*[-9999]  #index refers to the maximum row index for column with this index
		maxBin_column = self.n_bins_y*[-9999]  #index refers to the maximum column index for row with this index 

		minBin_row     = self.n_bins_x*[9999]  #index refers to the min row index for column with this index
		minBin_column = self.n_bins_y*[9999]  #index refers to the min column index for 

		# go through all superbins, find these max indices for each row
		# go through the superbins, find any empty superbins with indices less than this and add them to adjacent non-empty superbins with fewest counts

		for superbin_index,superbin in enumerate(self.superbin_indices):
			for _tuple in superbin:

				if self.counts_in_superbin(superbin_index) == 0:
					continue   # only want to use the bin values from superbins that are actually full    ### test to make sure we get the correct values
				if _tuple[0] > maxBin_column[_tuple[1]]:
					maxBin_column[_tuple[1]] = _tuple[0]
				if _tuple[0] < minBin_column[_tuple[1]]:
					minBin_column[_tuple[1]] = _tuple[0]
				if _tuple[1] > maxBin_row[_tuple[0]]:
					maxBin_row[_tuple[0]]  = _tuple[1]
				if _tuple[1] < minBin_row[_tuple[0]]:
					minBin_row[_tuple[0]] = _tuple[1]

		for iii in range(0,self.n_bins_x):
			for jjj in range(0,self.n_bins_y):
				if maxBin_column[jjj] == -9999 or minBin_column[jjj] == 9999:
					continue
				if maxBin_row[iii] == -9999 or minBin_row[iii] == 9999:
					continue
				superbin_index = self.get_superbin_number((iii,jjj))
				if (iii <= maxBin_column[jjj]) and (iii >= minBin_column[jjj]) and self.counts_in_superbin(self.get_superbin_number((iii,jjj) )) == 0:
					list_of_neighbors = self.get_list_of_neighbors( (iii,jjj))
					neighbor_counts = [self.counts_in_superbin(neighbor_index) for neighbor_index in list_of_neighbors]
					mergeIndex = list_of_neighbors[neighbor_counts.index(min(neighbor_counts))] # add to the neighbor with the fewest counts
					print("merged hole %s with %s"%(self.superbin_indices[superbin_index],self.superbin_indices[mergeIndex] ) )
					self.superbin_indices[mergeIndex].extend(self.superbin_indices[superbin_index])
					self.superbin_indices.remove(self.superbin_indices[superbin_index])
				elif (jjj < maxBin_row[iii]) and (jjj > minBin_row[iii]) and self.counts_in_superbin(self.get_superbin_number((iii,jjj) )) == 0:
					list_of_neighbors = self.get_list_of_neighbors( (iii,jjj))
					neighbor_counts = [self.counts_in_superbin(neighbor_index) for neighbor_index in list_of_neighbors]
					mergeIndex = list_of_neighbors[neighbor_counts.index(min(neighbor_counts))] # add to the neighbor with the fewest counts
					print("merged hole %s with %s"%(self.superbin_indices[superbin_index],self.superbin_indices[mergeIndex] ) )
					self.superbin_indices[mergeIndex].extend(self.superbin_indices[superbin_index])
					self.superbin_indices.remove(self.superbin_indices[superbin_index])

		return


	def there_are_empty_superbins(self):
		for iii in range(0,len(self.superbin_indices)):
			if (self.counts_in_superbin(iii) == 0):
				return True
		return False

 
	def get_bad_superbins(self):    ## return list of superbins that have stat uncertainty greater than max threshold and scaled bin counts less than threshold  
		bad_superbins = []

		num_superbins = 0
		for iii,superbin in enumerate(self.superbin_indices):
			### check that the total bin stat uncertainty is less than max threshold allowed
			if self.counts_in_superbin( iii ) == 0: continue  #### don't want empty superbins 
			if self.all_hist_values.get_bin_total_uncert(superbin)  > self.max_stat_uncert: bad_superbins.append(iii)
				#print("Stat uncertainty in bin %s is %s."%(iii,self.all_hist_values.get_bin_total_uncert(superbin)))
			### check that the total scaled/unscaled bin yields are not less than defined minimum bin count threshold
			elif self.all_hist_values.get_unscaled_QCD_superbin_counts(superbin)  < self.min_unscaled_QCD_bin_counts: bad_superbins.append(iii)
			elif self.all_hist_values.get_scaled_QCD_superbin_counts(self.superbin_indices[iii]    ) < self.min_scaled_QCD_bin_counts: bad_superbins.append(iii)
			num_superbins+=1
		return bad_superbins

	def get_lowest_count_neighbor(self, superbin_numbers):    ## takes in a list of superbin numbers and returns superbin number that has the fewest overall scaled counts 
		index_fewest_counts = None
		fewest_counts = 1e15
		for superbin_number in superbin_numbers:
			#print("################    Checking counts: superbin number = %s, superbin_indices = %s, counts = %s, fewest counts = %s"%(superbin_number, self.superbin_indices[superbin_number],self.all_hist_values.get_scaled_superbin_counts( self.superbin_indices[superbin_number]   ), fewest_counts))
			if self.all_hist_values.get_scaled_superbin_counts( self.superbin_indices[superbin_number]   ) < fewest_counts:
				index_fewest_counts = superbin_number
				fewest_counts = self.all_hist_values.get_scaled_superbin_counts( self.superbin_indices[superbin_number]   )

		return index_fewest_counts

	def get_highest_stat_uncert_neighbor(self, superbin_numbers):    ## takes in a list of superbin numbers and returns superbin number that has the fewest overall scaled counts 
		index_highest_uncert = None
		highest_uncert = -1e15
		for superbin_number in superbin_numbers:
			#print("################    Checking counts: superbin number = %s, superbin_indices = %s, counts = %s, fewest counts = %s"%(superbin_number, self.superbin_indices[superbin_number],self.all_hist_values.get_scaled_superbin_counts( self.superbin_indices[superbin_number]   ), fewest_counts))
			if self.all_hist_values.get_bin_total_uncert( self.superbin_indices[superbin_number]   ) > highest_uncert:
				index_highest_uncert = superbin_number
				highest_uncert = self.all_hist_values.get_bin_total_uncert( self.superbin_indices[superbin_number]   )

		return index_highest_uncert


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
			random.seed(123456)
			random_bad_superbin = random.choice(bad_superbins)										### this is a random superbin number
			#print("Random bad superbin: ", random_bad_superbin)
			random.seed(123456)
			random_bad_superbin_tuple = random.choice( self.superbin_indices[random_bad_superbin] ) ### this is a tuple
			#print("Random bad tuple: ", random_bad_superbin_tuple)

			nearby_superbins = self.get_list_of_neighbors( random_bad_superbin_tuple   ) ## look for non-empty neighbors

			if len(nearby_superbins) == 0: 
				nearby_superbins = self.get_list_of_all_neighbors( random_bad_superbin_tuple    )   	### this is a list of superbin numbers				
			
			#print("Nearby superbins: ", nearby_superbins)
			## find superbin with fewest overall scaled counts

			### CHANGED 
			#lowest_count_neighbor_index = self.get_lowest_count_neighbor( nearby_superbins) 
			#print("Found lowest count neighbor_index, %s, with %s counts."%(lowest_count_neighbor_index, self.all_hist_values.get_scaled_superbin_counts(  self.superbin_indices[lowest_count_neighbor_index] )  ))
 
			highest_stat_uncert_neighbor_index = self.get_highest_stat_uncert_neighbor(nearby_superbins)

			### merge with neighbor with fewest overall counts

			### CHANGED
			#self.superbin_indices[lowest_count_neighbor_index].extend( self.superbin_indices[random_bad_superbin]   )
			highest_stat_uncert_neighbor_index
			self.superbin_indices[highest_stat_uncert_neighbor_index].extend( self.superbin_indices[random_bad_superbin]   )

			#print("extending superbins", self.superbin_indices)
			self.superbin_indices.remove( self.superbin_indices[random_bad_superbin] )
			#print("removing superbins", self.superbin_indices)
			######### get_list_of_all_neighbors is not working -> not returning anything

			### remove bad superbin from list
			bad_superbins.remove( random_bad_superbin )
			num_bad_superbins = len(bad_superbins)

			bad_superbins = self.get_bad_superbins() 
			num_bad_superbins = len(bad_superbins)

			iteration_count+=1


		print("Done with main merging.")


		##########################################################
		##################### FILL IN HOLES ######################
		###########################################################
		### choose superbin indices at random, get a list of the empty bins that they are adjacent to, randomly add one of those bins to the superbin
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
	
	def plot_before_syst_plot(self):
		# go over all_hist_values and plot them
		plot_path =  os.getenv('CMSSW_BASE') + "/src/postprocess/plots/statUncertaintyPlots/preMergedPlots"
		hist_expected_counts_unmerged = ROOT.TH2F("hist_expected_counts_unmerged_%s%s_%s"%(self.technique_str,region,year), ("Expected Background bin in the %s (%s); diSuperjet mass (GeV); avg superjet mass (GeV)"%(region, year)), self.n_bins_x,1250., 10000, self.n_bins_y, 500, 5000)  # 375 * 125
		for iii in range(0, self.n_bins_x):
			for jjj in range(0, self.n_bins_y):
				hist_expected_counts_unmerged.SetBinContent(iii+1,jjj+1, self.counts_in_superbin(self.get_superbin_number( (iii,jjj))))

		hist_unmerged_systUncert = ROOT.TH2F("hist_unmerged_systUncert_%s%s_%s"%(self.technique_str,region,year), ("Systematic Uncertainty per bin in the %s (%s); diSuperjet mass (GeV); avg superjet mass (GeV)"%(region, year)), self.n_bins_x,1250., 10000, self.n_bins_y, 500, 5000)  # 375 * 125

		for superbin in self.superbin_indices:
			for _tuple in superbin:
				hist_unmerged_systUncert.SetBinContent(_tuple[0]+1,_tuple[1]+1,self.all_hist_values.get_bin_total_uncert(superbin))

		c1 = ROOT.TCanvas("","",1200,1000)
		hist_expected_counts_unmerged.Draw("colz")
		c1.SaveAs("%s/counts_unmerged_%s%s_%s.png"%(plot_path,self.technique_str,region,year))
		hist_unmerged_systUncert.Draw("colz")
		c1.SaveAs("%s/systUncert_unmerged_%s%s_%s.png"%(plot_path,self.technique_str,region,year))

		return
	def print_superbins(self):
		for superbin_num in range(0,len(self.superbin_indices)):
			print("Superbin %s ---- UNSCALED counts = %s, UNSCALED -- QCD -- counts = %s,  SCALED counts = %s"%(superbin_num,self.counts_in_superbin(superbin_num),self.all_hist_values.get_unscaled_QCD_superbin_counts(self.superbin_indices[superbin_num]), self.all_hist_values.get_scaled_superbin_counts( self.superbin_indices[superbin_num]) ))
		return

	## returns the distance (sqrt(pow(bin_x,2) + pow(bin_y,2))) of the superbin center to the origin
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
		plt.savefig('plots/statUncertaintyPlots/postMergedPlots/post_merge_superbin_yields_%s_%s%s.png'%(self.year,self.technique_str,self.region))
		plt.close()



		return sorted_superbin_indices
	## sort bins by their raw distance (sqrt(pow(bin_x,2) + pow(bin_y,2))) to the origin 
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
	def sort_bins_with_graphs(self):   

		superbin_indices_copy = self.superbin_indices[:]

		superbin_yields = []   # format: [(super_bin_1, 100), (super_bin_2, 150), (super_bin_3, 120), ...]
		neighbors = {}     	   # format:	neighbors = { super_bin_1: [super_bin_2, super_bin_3], super_bin_2: [super_bin_1, super_bin_3], super_bin_3: [super_bin_1, super_bin_2], ... }
		for iii,superbin in enumerate(self.superbin_indices):

			## get yields of this superbin
			superbin_yields.append( ( iii, self.all_hist_values.get_scaled_superbin_counts( self.superbin_indices[iii]   )    )  )  
			## get neighbors of this superbin
			all_neighbor_superbin_indices = self.get_list_of_all_neighbors( self.superbin_indices[iii][0]  )

			neighbors[iii] = all_neighbor_superbin_indices
		arranged_bins = self.arrange_bins_optimized(superbin_yields, neighbors)  ## returns 
		new_superbin_indices = [ self.superbin_indices[ arranged_bins[iii][0]  ]  for iii in range(0,len(arranged_bins))     ]

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
		plt.savefig('plots/statUncertaintyPlots/postMergedPlots/post_merge_superbin_yields_%s_%s%s.png'%(self.year,self.technique_str,self.region))
		plt.close()

		return new_superbin_indices

	# Function to calculate the yield difference
	def calculate_yield_difference(self,bin_a, bin_b):
		return abs(bin_a[1] - bin_b[1])  # where bin_a[1] is the yield value

	def arrange_bins_optimized(self,super_bins_yields, neighbors):
		# Create a graph where each bin is a node and edges are the yield differences
		G = nx.Graph()
		
		# Add nodes to the graph
		for bin_id, yield_val in super_bins_yields:
		    G.add_node(bin_id, bin_yield=yield_val)  # Renamed 'yield' to 'bin_yield'
		
		# Add edges to the graph with weight as the yield difference
		for bin_id, neighbor_list in neighbors.iteritems():  # Change iteritems() for Python 2
		    for neighbor_id in neighbor_list:
		        if bin_id < neighbor_id:  # Avoid duplicate edges
		            yield_diff = self.calculate_yield_difference(
		                super_bins_yields[bin_id], super_bins_yields[neighbor_id])
		            G.add_edge(bin_id, neighbor_id, weight=yield_diff)

		# Find the minimum spanning tree (MST) using Prim's algorithm
		mst = nx.minimum_spanning_tree(G)

		# Traverse the MST to obtain the sorted bins in the optimal order
		arranged_bins = []
		visited = set()
		
		# Start from an arbitrary node (here we take the first bin using index 0)
		start_bin = max(super_bins_yields, key=lambda x: x[1])[0]    ###super_bins_yields[0][0]  # Index 0 for the first bin's id
		stack = [start_bin]
		
		while stack:
		    bin_id = stack.pop()
		    if bin_id not in visited:
		        visited.add(bin_id)
		        arranged_bins.append(super_bins_yields[bin_id])
		        
		        # Add unvisited neighbors to the stack
		        for neighbor in mst[bin_id]:
		            if neighbor not in visited:
		                stack.append(neighbor)

		# very artificial way of preventing last element from having large yield relative to neighbors
		if arranged_bins[-1][1] > 3*arranged_bins[-2][1] and arranged_bins[0][1] < 1.5*arranged_bins[-1][1]:
			arranged_bins.insert(0, arranged_bins[-1]) # place the last element at the beginning
			last_element = arranged_bins.pop()
		
		return arranged_bins

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
		print( "--------- Merged N_x/N_y = %s/%s original bins in the --- %s --- for year --- %s --- and --- %s --- technique into %s linearized bins. "%(self.n_bins_x,self.n_bins_y, self.region, self.year, technique_title, len(self.superbin_indices) ))
		print(" --------- Using original histogram bins x/y %s/%s and beyond."%(self.bin_min_x,self.bin_min_y))
		print( "--------- There were === %s === total counts in the original 2D histogram."%(total_counts_original_unscaled))
		print( "--------- There were === %s === total counts in the post-merged, linear histogram."%(total_counts_post_merge_unscaled))
		print("")
		print("")
		print("")
		print("")


if __name__=="__main__":

	debug = False
	dryRun = False

	print("Calculating bin groupings for best statistical uncertainties")
		
	binMap_path = os.getenv('CMSSW_BASE') + "/src/postprocess/binMaps"
	if not dryRun:
		os.system('rm %s/superbin_indices*.txt'%binMap_path)
		os.system('rm %s/superbin_indicesNN_*.txt'%binMap_path)

	years = ["2015","2016","2017","2018"]
	regions = ["SR","CR", "AT1b", "AT0b"  ]   # "AT0tb", "AT1tb", "SB1b", "SB0b"

	c = ROOT.TCanvas("c", "canvas", 1250, 1000)
	ROOT.gStyle.SetOptStat(0)

	hist_names = ["h_MSJ_mass_vs_MdSJ_","h_MSJ_mass_vs_MdSJ_NN_"]
	output_strs = ["", "NN_"]
	technique_strs = ["cut-based", "NN-based"]
	for region in regions:
		for year in years:
			for iii,hist_name in enumerate(hist_names):
				if region in ["SB1b","SB0b"] and "NN" in hist_name: continue

				text_output_path = os.getenv('CMSSW_BASE') + "/src/postprocess/binMaps/"
				
				if dryRun: 
					print("===============================================================================")
					print("===============================================================================")
					print("===============================================================================")
					print("===========================     WARNING !!    =================================")
					print("=========================   THIS IS A DRY RUN !!!!!   =========================")
					print("===============================================================================")
					print("===============================================================================")
					print("===============================================================================")

				if not dryRun:  out_txt_file = open("%s/superbin_indices%s_%s.txt"%(text_output_path,output_strs[iii],year),"a")
				print("Creating maps for %s/%s"%(region,year))

				TH2_hist_merged_name   = os.getenv('CMSSW_BASE') + "/src/postprocess/outputs/binMergingOutputs/postMergedFiles/allBR_statUncert_%s%s_%s_MERGED_BINS.root"%(output_strs[iii],region,year)
				TH2_hist_new_bins_name = os.getenv('CMSSW_BASE') + "/src/postprocess/outputs/binMergingOutputs/postMergedFiles/allBR_statUncert_%s%s_%s_NEW_BINS.root"%(output_strs[iii],region,year)
				out_file = ROOT.TFile.Open(TH2_hist_new_bins_name,"RECREATE")

				# give histogram to constructor
				testCase = combineHistBins(year, region, output_strs[iii], debug,dryRun)
				#create a dummy histogram with dimensions 20x22
				merged_bins = testCase.superbin_indices
				bin_map_hist = ROOT.TH2F("bin_map_hist%s"%output_strs[iii], ("Map of how bins were merged in %s for %s (%s); diSuperjet mass (GeV); avg superjet mass (GeV)"%(region, year,technique_strs[iii])), testCase.n_bins_x,1250., 10000, testCase.n_bins_y, 500, 5000)  # 375 * 125
				stat_uncert_hist = ROOT.TH2F("stat_uncert_hist%s"%output_strs[iii], ("Statistical Uncertainty (post bin merging) in the %s for %s (%s); diSuperjet mass (GeV); avg superjet mass (GeV)"%(region, year,technique_strs[iii])), testCase.n_bins_x,1250., 10000, testCase.n_bins_y, 500, 5000)  # 375 * 125
				merged_hist_count = ROOT.TH2F("merged_hist_count%s"%output_strs[iii], ("Unscaled Bin Counts (post bin merging) in the %s for %s (%s); diSuperjet mass (GeV); avg superjet mass (GeV)"%(region, year,technique_strs[iii])), testCase.n_bins_x,1250., 10000, testCase.n_bins_y, 500, 5000)  # 375 * 125
				R = ROOT.TRandom3()
				for superbin_index, superbin in enumerate(merged_bins):
					random.seed(54321)
					rndm = R.Uniform(0,10000)
					for smallbin in superbin:
						if testCase.counts_in_superbin(superbin_index) == 0:   # don't show indices for empty bins
							continue					
						bin_map_hist.SetBinContent(smallbin[0]+1,smallbin[1]+1,rndm)
						stat_uncert_hist.SetBinContent(smallbin[0]+1,smallbin[1]+1, testCase.all_hist_values.get_bin_total_uncert(testCase.superbin_indices[superbin_index]))    #   1.0/sqrt(testCase.counts_in_superbin(superbin_index))   
						merged_hist_count.SetBinContent(smallbin[0]+1,smallbin[1]+1, testCase.counts_in_superbin(superbin_index))

				if not dryRun:  
					out_txt_file.write("%s/%s/number of bins = %s/%s\n"%(year,region, len(testCase.superbin_indices), testCase.superbin_indices))
					out_txt_file.close()

				bin_map_hist.GetZaxis().SetRangeUser(0,10000)
				bin_map_hist.Draw("colz")
				c.SaveAs( os.getenv('CMSSW_BASE')+  "/src/postprocess/plots/statUncertaintyPlots/postMergedPlots/bin_map_%s%s_%s.png"%(output_strs[iii],region,year)) 
				
				stat_uncert_hist.Draw("colz")
				c.SaveAs(os.getenv('CMSSW_BASE')+  "/src/postprocess/plots/statUncertaintyPlots/postMergedPlots/stat_uncert_%s%s_%s.png"%(output_strs[iii],region,year)) 
				
				merged_hist_count.Draw("colz")
				c.SaveAs(os.getenv('CMSSW_BASE')+  "/src/postprocess/plots/statUncertaintyPlots/postMergedPlots/bin_counts_%s%s_%s.png"%(output_strs[iii],region,year)) 
				


