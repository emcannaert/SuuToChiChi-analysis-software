python calculateStatisticalUncertaintyBins.py   ## create the bin masks + SB groups
python master_linearizer.py --year 2015         ## linearize
python master_linearizer.py --year 2016
python master_linearizer.py --year 2017
python master_linearizer.py --year 2018
python make_region_masks.py  					## create region masks
python master_linearizer.py --year 2015			## created masked linear files
python master_linearizer.py --year 2016
python master_linearizer.py --year 2017
python master_linearizer.py --year 2018
python fix_asymmetric_uncerts.py                ## make uncert vars symmetric
python create_masked_superbin_groups.py  		## created masked superbin groups
