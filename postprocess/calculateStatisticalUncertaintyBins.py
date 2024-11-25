import ROOT
import sys, os
from math import sqrt, exp
import random
from random import uniform, shuffle, choice
import numpy as np
import pdb
import time
from histInfo import histInfo

####  calculateStatisticalUncertaintyBins.py
####  Written by Ethan Cannaert, 24 September 2023, updated 27 July 2024
####  Opens up a TH2 (22x20 bins, avg superjet mass vs diSuperjet mass)
####  Merges bins into "superbins" until superbin systematic uncertainties are below 25% ( or desired value) and/or scaled superbin yields are above some threshold.
####  Creates histograms showing the bin mappings, final superbin counts, and superbin statistical uncertainties
####  The main output of this are text files (superbin_indices*.txt in the binMaps/ directory) that list the merged superbin mappings
####  This script expects input TH2s with dimensions self.n_bins_x X self.n_bins_y (default 22x20)
####  The input files are searched for in the $CMSSW_BASE/src/combinedROOT/processedFiles folder with naming scheme <dataset type>_<year>_processed.root
####  The combineHistBins class uses the histInfo class to store TH2F information, so methods from this class are often used.




class combineHistBins:

	def __init__(self,year,region,technique_str,debug=False, dryRun=False):   #constructor will convert TH2 to a 2D array, do the optimized bin merging, and then return a TH2 with those associated bins

		#self.TH2_hist = TH2_hist
		self.year = year
		self.region = region
		self.technique_str = technique_str
		self.dryRun = dryRun
		self.max_stat_uncert = 0.20  ## maximum statistical uncertainty
		self.min_unscaled_QCD_bin_counts   = 4.0   ## the minimum number of unscaled QCD events required to be in each bin, better to make this 1 or more to prevent weird migration stuff

		self.n_bins_x = 22
		self.n_bins_y = 20

		if region in ["SB1b","SB0b"]:
			self.n_bins_x = 15
			self.n_bins_y = 12
		self.all_hist_values =  histInfo.histInfo(year,region, self.n_bins_x, self.n_bins_y, self.technique_str, debug)    #histInfo.histInfo(year,region) ## everywhere there is originally a sqrt, will need to call get_bin_total_uncert and get 
		self.superbin_indices = self.init_superbin_indices()     
		
		#if not self.dryRun: self.plot_before_syst_plot()   # plot the "before" image of counts and syst uncertainty 
 
		print("Starting the process of merging bins.")
		self.do_bin_merging()
		print("Finished with bin merging.")
		#self.print_final_hist()
		#self.fill_in_holes()

		self.print_superbins()   ### print out scaled and unscaled counts in each superbin post merging



	def test_hist(self):
		test_hist = [
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0.2,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0.2,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0.2,0,0,0,0,0.2,0,0.2,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0.2,0.2,0.2,0,0.2,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0.2,0,0,0,0.2,0.2,0.2,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0,0,0,0,0,0,0,0,0],
		[0,0,0,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0,0,0,0,0,0,0,0,0,0],
		[0,1,1,1,1,1,1,1,1,0.2,0.2,0.2,0.2,0.2,0.2,0,0,0,0,0,0,0],
		[0,2,2,2,2,5,5,5,2,5,2,2,2,1,1,0.2,0.2,0.2,0.2,0,0,0],
		[0,5,5,5,5,5,5,10,10,5,10,10,5,5,5,1,1,0.2,0.2,0.2,0,0],
		[0,10,10,10,10,10,10,10,10,10,10,5,5,5,5,1,1,0.2,0.2,0,0,0],
		[0,10,10,10,10,10,10,10,10,10,10,5,5,5,5,5,1,1,0,0,0,0],
		[0,20,20,20,20,20,20,20,20,10,10,10,10,10,10,0.2,0.2,0,0,0,0,0],
		[0,20,20,20,20,20,20,20,20,10,10,10,5,5,1,1,0.2,0.2,0,0,0,0],
		[0,20,20,20,20,20,20,20,20,10,10,10,5,5,1,1,0.2,0.2,0,0,0,0],
		[0,20,20,20,20,20,20,20,20,10,10,10,5,5,1,1,0.2,0.2,0,0,0,0],
		[0,20,20,20,20,20,20,20,20,10,10,10,5,5,1,1,0.2,0.2,0,0,0,0],
		[0,20,20,20,20,20,20,20,10,10,10,5,5,5,1,1,0.2,0.2,0,0,0,0],
		[0,20,20,20,20,20,20,20,10,10,10,5,5,5,1,1,0.2,0.2,0,0,0,0],
		[0,20,20,20,20,20,20,20,10,10,10,5,5,5,1,1,0.2,0.2,0,0,0,0]]
		return test_hist
	def test_hist2(self):
		test_hist = [
		[0,0,0,0,0],
		[0,0,0.5,0,0],
		[0,0,0,0,0],
		[0,1,2,3,0],
		[0,1,2,3,0]]
		return test_hist
	def print_final_hist(self):
		hist_map = [ [-999]*self.n_bins_y for i in range(self.n_bins_x)]
		print("Histogram bin map:")
		for iii in range(0,self.n_bins_x):
			for jjj in range(0, self.n_bins_y):
				hist_map[iii][jjj] = self.get_superbin_number( (iii,jjj))

		print('\n'.join(' '.join(str(x) for x in row) for row in hist_map))

		print("Histogram bin statistical uncertainties")
		for iii in range(0,self.n_bins_x):
			for jjj in range(0, self.n_bins_y):
				if(  self.counts_in_superbin(self.get_superbin_number( (iii,jjj))) > 0  ):
					hist_map[iii][jjj] = self.all_hist_values.get_bin_total_uncert(self.superbin_indices[self.get_superbin_number( (iii,jjj))] ) #  1.0/sqrt(self.counts_in_superbin(self.get_superbin_number( (iii,jjj ) ) ) ) 
				else:
					hist_map[iii][jjj] = 0.0

		print('\n'.join(' '.join(str(x) for x in row) for row in hist_map))

		return

	def fill_random_values(self):

		converted_hist = [ [0]*self.n_bins_y for i in range(self.n_bins_x)]
		for iii in range(0,self.n_bins_x):
			for jjj in range(0,self.n_bins_y):
				random.seed(54321)
				converted_hist[iii][jjj] = uniform(0.0,20.0)

		print("original histogram looks like: ")
		print('\n'.join(' '.join(str(x) for x in row) for row in converted_hist))
		return converted_hist
	def calculate_bin_weight(self, superbin_index, cand_superbin_index ):
		avg_xbin = 0
		avg_ybin = 0
		nBins = 0
		counts_in_cand_bin = self.counts_in_superbin(cand_superbin_index)
		for _tuple in self.superbin_indices[superbin_index]:
			avg_xbin+=_tuple[0]
			avg_ybin+= _tuple[1]
			nBins +=1
		avg_xbin/=nBins
		avg_ybin/=nBins
		cand_avg_xbin = 0
		cand_avg_ybin = 0
		cand_nbins = 0
		for _tuple in self.superbin_indices[cand_superbin_index]:
			cand_avg_xbin+=_tuple[0]
			cand_avg_ybin+= _tuple[1]
			cand_nbins+=1
		cand_avg_xbin/= cand_nbins
		cand_avg_ybin/= cand_nbins
		# distance should be distance between candidate superbin center and current superbin center
		distance = sqrt(pow(int(cand_avg_xbin- avg_xbin),2)+pow(int(cand_avg_ybin- avg_ybin),2))
		return (exp(5*distance/1.0) + 2.0*counts_in_cand_bin)

	def init_superbin_indices(self):
		_superbin_indices = []    # format [ [(x1,x2),(x2,x3),....], [(xi,yi), (xi+1,yi+1),.....], ...., [(xn-1,yn-1),(xn,yn)] ]     _superbin_indices[<superbin #>][<order bin was added>][<coordinate>]
		for iii in range(0,self.n_bins_x):
			for jjj in range(0, self.n_bins_y):
				_superbin_indices.append([(iii,jjj)])    # superbin # and add # don't matter
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
				if self.all_hist_values.get_bin_total_uncert(self.superbin_indices[iii])  > self.max_stat_uncert:    # 1.0/sqrt(self.counts_in_superbin( iii ) )
					return False
				### check that the total bin yields
				if self.all_hist_values.get_unscaled_QCD_superbin_counts(self.superbin_indices[iii])  < self.min_unscaled_QCD_bin_counts: 
					return False
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
			if ( ( index_x-1 ) >= 0 ):
				if  (index_x-1,index_y) not in self.superbin_indices[this_superbin_num ]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x-1,index_y)  )) > 0:
						list_of_neighbors.append((index_x-1,index_y))
			if ( ( index_y+1 )< self.n_bins_y ):
				if (index_x,index_y+1) not in self.superbin_indices[this_superbin_num ]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x,index_y+1)  )) > 0:
						list_of_neighbors.append((index_x,index_y+1))
			if ( ( index_y-1 ) >= 0 ):
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
			if ( ( index_x-1 ) >= 0 ):
				if  (index_x-1,index_y) not in self.superbin_indices[this_superbin_num ]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x-1,index_y)  )) > -1:
						list_of_neighbors.append((index_x-1,index_y))
			if ( ( index_y+1 )< self.n_bins_y ):
				if (index_x,index_y+1) not in self.superbin_indices[this_superbin_num ]:
					if self.counts_in_superbin(self.get_superbin_number(  (index_x,index_y+1)  )) > -1:
						list_of_neighbors.append((index_x,index_y+1))
			if ( ( index_y-1 ) >= 0 ):
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
			if ( ( index_x-1 ) >= 0 ):
				if not (index_x-1,index_y) in self.superbin_indices[self.get_superbin_number( _tuple ) ]:
					if self.all_hist_values.list_all_counts[index_x-1][index_y] == 0:                 #self.hist_values[index_x-1][index_y] == 0:
						list_of_neighbors.append((index_x-1,index_y))
			if ( ( index_y+1 )< self.n_bins_y ):
				if not (index_x,index_y+1) in self.superbin_indices[self.get_superbin_number( _tuple ) ]:
					if self.all_hist_values.list_all_counts[index_x][index_y+1] == 0:                        #self.hist_values[index_x][index_y+1] == 0:
						list_of_neighbors.append((index_x,index_y+1))
			if ( ( index_y-1 ) >= 0 ):
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
				if (tuple_[0]-1) > 0:
					counts = self.counts_in_superbin(self.get_superbin_number( (tuple_[0]-1,tuple_[1])  ))
					if (counts is not None) and (counts == 0) and (self.get_superbin_number( (tuple_[0]-1,tuple_[1])  ) not in list_of_empty_neighbors) :
						list_of_empty_neighbors.append( self.get_superbin_number( (tuple_[0]-1,tuple_[1])  ) )
			if (tuple_[0],tuple_[1]+1) not in superbin:
				if (tuple_[1]+1) < self.n_bins_y:
					counts = self.counts_in_superbin(self.get_superbin_number( (tuple_[0],tuple_[1]+1)  ))
					if (counts is not None) and (counts == 0) and (self.get_superbin_number( (tuple_[0],tuple_[1]+1)  ) not in list_of_empty_neighbors) :
						list_of_empty_neighbors.append( self.get_superbin_number( (tuple_[0],tuple_[1]+1)  ) )
			if (tuple_[0],tuple_[1]-1) not in superbin:
				if (tuple_[1]-1) >= 0:
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
			if self.all_hist_values.get_bin_total_uncert(superbin)  > self.max_stat_uncert: 
				bad_superbins.append(iii)
				#print("Stat uncertainty in bin %s is %s."%(iii,self.all_hist_values.get_bin_total_uncert(superbin)))
			### check that the total bin yields are not less than defined minimum bin count threshold
			elif self.all_hist_values.get_unscaled_QCD_superbin_counts(superbin)  < self.min_unscaled_QCD_bin_counts: 
				bad_superbins.append(iii)

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
			##self.all_hist_values.print_all_contributions_scaled_counts( self.superbin_indices 

			bad_superbins = self.get_bad_superbins()   ### get list of superbins that have stat uncertainty greater than max threshold and scaled bin counts less than threshold, ONLY for non-zero superbins
			#print("Bad superbins: ", bad_superbins)
			random_bad_superbin = random.choice(bad_superbins)										### this is a random superbin number
			#print("Random bad superbin: ", random_bad_superbin)
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

		""" 
		#### this method is no longer used!! ####
		while not all_bins_good:

			print("Starting on run-through %i"%(iteration_count+1))

			if(iteration_count == 100): # don't want this going on forever
				break 

			#################################
			###### Do main bin merging ######
			#################################
			for iii in reversed(range(0,self.n_bins_x)):
				for jjj in reversed(range(0, self.n_bins_y)):

					#print("superbin is %s"%self.superbin_indices[self.get_superbin_number((iii,jjj))])
					#print("total bin uncertainty %s (%s): %s"%(self.get_superbin_number((iii,jjj)),self.superbin_indices[self.get_superbin_number((iii,jjj))], self.all_hist_values.get_bin_total_uncert(self.superbin_indices[self.get_superbin_number((iii,jjj))])))
					#print("doing bin merging on (%s,%s) "%(iii,jjj))
					other_iii = self.n_bins_x - (iii+1)
					other_jjj = self.n_bins_y - (jjj+1)

					######################################
					#### starting at top-right corner ####
					######################################

					superbin_number   = self.get_superbin_number( (iii,jjj))
					superbin_counts = self.counts_in_superbin(superbin_number)
					if (superbin_counts == 0):  
						continue
					if ( ( self.all_hist_values.get_bin_total_uncert(self.superbin_indices[self.get_superbin_number( (iii,jjj))] )  )  < self.max_stat_uncert):  #     1.0/sqrt(self.counts_in_superbin(self.get_superbin_number( (iii,jjj ) ) ) )
						#print("This bin has low enough statistical uncertainty. Skipped.")
						continue

					#print("Looking at bin %s"%self.get_superbin_number( (iii,jjj)) )
					list_of_neighbors = self.get_list_of_neighbors( (iii,jjj) ) # all neighbors of this bin and all bins in its parent superbin 
					#neighbor_counts   = [ self.counts_in_superbin(neighbor_index) for neighbor_index in list_of_neighbors]
					neighbor_weights   =  [ self.calculate_bin_weight(superbin_number, neighbor_index) for neighbor_index in list_of_neighbors]   #[ self.counts_in_superbin(neighbor_index) for neighbor_index in list_of_neighbors]

					if len(list_of_neighbors) == 0:
						continue
					mergeIndex = list_of_neighbors[neighbor_weights.index(min(neighbor_weights))] # add to the neighbor with the fewest counts
					#print("Merging %s with %s"% ( self.superbin_indices[mergeIndex],self.superbin_indices[superbin_number]   ))
					self.superbin_indices[mergeIndex].extend(self.superbin_indices[superbin_number])
					self.superbin_indices.remove(self.superbin_indices[superbin_number])

					##########################################
					#### starting from bottom-left corner ####
					##########################################

					superbin_number   = self.get_superbin_number( (other_iii,other_jjj))
					superbin_counts = self.counts_in_superbin(superbin_number)
					if (superbin_counts == 0):
						continue

					if ( self.all_hist_values.get_bin_total_uncert(self.superbin_indices[self.get_superbin_number( (other_iii,other_jjj))] )   < self.max_stat_uncert     ):   #   # 1.0/sqrt(self.counts_in_superbin(self.get_superbin_number( (other_iii,other_jjj ) ) ) )
						continue

					list_of_neighbors = self.get_list_of_neighbors( (other_iii,other_jjj) ) # all neighbors of this bin and all bins in its parent superbin 
					neighbor_weights   = [ self.calculate_bin_weight(superbin_number, neighbor_index) for neighbor_index in list_of_neighbors] #[ self.counts_in_superbin(neighbor_index) for neighbor_index in list_of_neighbors] #   #
					if len(list_of_neighbors) == 0:
						continue
					mergeIndex = list_of_neighbors[neighbor_weights.index(min(neighbor_weights))] # add to the neighbor with the fewest counts
					#print("Merging %s with %s"% ( self.superbin_indices[mergeIndex],self.superbin_indices[superbin_number]   ))
					self.superbin_indices[mergeIndex].extend(self.superbin_indices[superbin_number])
					self.superbin_indices.remove(self.superbin_indices[superbin_number])

			#################################
			####### Eliminate Islands #######
			#################################
			# loop over all bins in a superbin and see if it's an island
			# if there are no neighbor bins that are not in the superbin, it's an island
			### do this in a random order
			
			range_x = list(range(0,self.n_bins_x))
			range_y = list(range(0,self.n_bins_y))
			random.seed(123456)
			shuffle(range_x)
			shuffle(range_y)
			for iii in range_x:
				for jjj in range_y:

					#print("checking islands (%s,%s)"%(iii,jjj))
					superbin_num = self.get_superbin_number((iii,jjj))
					superbin_counts = self.counts_in_superbin( superbin_num)
					superbin = self.superbin_indices[superbin_num]
					if ( (superbin_counts == 0) ):
						continue
					if (      (  self.all_hist_values.get_bin_total_uncert(self.superbin_indices[self.get_superbin_number( (iii,jjj))] )    < self.max_stat_uncert )   ):   #  1.0/sqrt(self.counts_in_superbin(self.get_superbin_number( (iii,jjj ) ) ) )
						continue
					if ( (iii > 0) and (jjj > 0) and (iii < (self.n_bins_x)) and (jjj < (self.n_bins_y)) ):
						#find superbin neighbors
						is_an_island = True

						is_an_island = self.check_island_neighbors(superbin_num)
						if not (len(self.get_list_of_neighbors( (iii,jjj) )) ==0 ):   # are there any neighbors with counts greater than 0? if so, this is not an island
							is_an_island = False
						if is_an_island:
							empty_neighbor_indices = self.find_empty_neighbors((iii,jjj))
							empty_neighbor_superbins = [self.superbin_indices[empty_index] for empty_index in empty_neighbor_indices]
							for empty_neighbor_superbin in empty_neighbor_superbins:
								empty_neighbor_index = self.get_superbin_number(empty_neighbor_superbin[0])
								island_index = self.get_superbin_number((iii,jjj))
								if empty_neighbor_index in self.superbin_indices[island_index]:
									continue
								self.superbin_indices[island_index].extend(self.superbin_indices[empty_neighbor_index])
								self.superbin_indices.remove(self.superbin_indices[empty_neighbor_index])

			iteration_count+=1
			all_bins_good = self.all_bins_are_good()
		"""

		######################################################################################################
		######################################################################################################
		### 							assign all empty bins to superbins --- NO LONGER USED
		######################################################################################################
		######################################################################################################

		"""
		### find the remaining empty bins, randomize them, and then add them to the nearest superbin
		### loop over all superbins, check to see if lone bins have zero events 
		### for each of these bins, find the closest nearby superbin 
		### find 

		non_empty_superbins = []
		empty_superbins     = []

		for iii, superbin_index in enumerate(self.superbin_indices):
			#superbin_x = superbin_index[0]
			#superbin_y = superbin_index[1]
			#superbin_number = 
			superbin_counts = self.counts_in_superbin(iii) 
			if superbin_counts > 0:

				#### add the first bin tuple entry of each superjet

				non_empty_superbins.append( (self.superbin_indices[iii][0][0],self.superbin_indices[iii][0][1] ))
			else:
				empty_superbins.append( (self.superbin_indices[iii][0][0],self.superbin_indices[iii][0][1] ))
		shuffle(empty_superbins)

		### loop over all empty superbins, get the updated superbin number, find the nearest neighbor, add bin to the nearest non-empty superbin, then delete empty bin superbin
		for empty_tuple in empty_superbins:
			nearest_index = self.find_nearest_neighbor(superbin_index, non_empty_superbins)
			empty_sb_number = self.get_superbin_number( (empty_tuple[0],empty_tuple[1] ) ) 
			### now add this bin to the nearest non-empty superbin

			#print("empty tuple is ", empty_tuple)
			#print("superbin_indices[nearest_index] is ",self.superbin_indices[nearest_index])
			self.superbin_indices[nearest_index].append( empty_tuple  )
			self.superbin_indices.remove( [empty_tuple] )
		"""




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

			print("Superbin %s ---- UNSCALED counts = %s, SCALED counts = %s"%(superbin_num,self.counts_in_superbin(superbin_num),self.all_hist_values.get_scaled_superbin_counts( self.superbin_indices[superbin_num]) ))
		return
if __name__=="__main__":

	debug = False
	dryRun = False

	print("Calculating bin groupings for best statistical uncertainties")
		
	binMap_path = os.getenv('CMSSW_BASE') + "/src/postprocess/binMaps"
	if not dryRun:
		os.system('rm %s/superbin_indices*.txt'%binMap_path)
		os.system('rm %s/superbin_indicesNN_*.txt'%binMap_path)

	years = ["2015","2016","2017","2018"]

	regions = ["SR","CR", "SB1b", "SB0b"] 

	#regions = [ "ADT1b", "ADT0b"] 

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
				"""if debug:
					TH2_hist = ROOT.TH2F("dummy_hist", "Total Counts" , 22, 1250., 10000, 20, 500, 4000);
				else:
					hist_name = hist_name +region
					TH2_file = ROOT.TFile.Open(hist_path,"READ")
					TH2_hist = TH2_file.Get(hist_name)"""

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
					random.seed(12345)
					rndm = R.Uniform(0,10000)
					for smallbin in superbin:
						if testCase.counts_in_superbin(superbin_index) == 0:   # don't show indices for empty bins
							continue					
						bin_map_hist.SetBinContent(smallbin[0]+1,smallbin[1]+1,rndm)
						stat_uncert_hist.SetBinContent(smallbin[0]+1,smallbin[1]+1, testCase.all_hist_values.get_bin_total_uncert(testCase.superbin_indices[superbin_index]))    #   1.0/sqrt(testCase.counts_in_superbin(superbin_index))   
						merged_hist_count.SetBinContent(smallbin[0]+1,smallbin[1]+1, testCase.counts_in_superbin(superbin_index))



				#for jjj,superbin in enumerate(testCase.superbin_indices):
				#	print("%s/%s/%s ------ unscaled counts in superbin %s: %s"%(year,region,hist_name, jjj,testCase.counts_in_superbin(jjj)) )

				if not dryRun:  
					out_txt_file.write("%s/%s/number of bins = %s/%s\n"%(year,region, len(testCase.superbin_indices), testCase.superbin_indices))
					out_txt_file.close()

				c = ROOT.TCanvas("c", "canvas", 1250, 1000)

				ROOT.gStyle.SetOptStat(0)
				bin_map_hist.GetZaxis().SetRangeUser(0,10000)
				#bin_map_hist.Write()
				bin_map_hist.Draw("colz")
				#bin_map_hist.Print()
				c.SaveAs( os.getenv('CMSSW_BASE')+  "/src/postprocess/plots/statUncertaintyPlots/postMergedPlots/bin_map_%s%s_%s.png"%(output_strs[iii],region,year)) 
				
				#stat_uncert_hist.Write()
				stat_uncert_hist.Draw("colz")
				#bin_map_hist.Print()
				c.SaveAs(os.getenv('CMSSW_BASE')+  "/src/postprocess/plots/statUncertaintyPlots/postMergedPlots/stat_uncert_%s%s_%s.png"%(output_strs[iii],region,year)) 
				
				#merged_hist_count.Write()
				merged_hist_count.Draw("colz")
				#bin_map_hist.Print()
				c.SaveAs(os.getenv('CMSSW_BASE')+  "/src/postprocess/plots/statUncertaintyPlots/postMergedPlots/bin_counts_%s%s_%s.png"%(output_strs[iii],region,year)) 
				


