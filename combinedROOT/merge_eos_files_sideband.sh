#!/bin/bash

# usage: find_eos_files.sh <main eos folder to search> <year>

EOSBASE="/store/user/ecannaer/" 

if [ -z "$1" ];
then 
	echo "Invalid crab submission folder. Please provide the most recent crab submission folder on eos (Ex. SuuToChiChi_123421234)."
	echo "The second option should be the year to process."
else

	echo "Getting all eos file paths"
	source find_eos_files.sh $1 $2
	
	echo "Copying W+Jets Files"
	python create_eos_copy_commands.py WJets_eos_paths.txt
	source eos_copy_commands.sh
	rm WJets*_combined_*.root

	echo "Copying TTbar Files"
	python create_eos_copy_commands.py TTbar_eos_paths.txt
	source eos_copy_commands.sh
	rm TTTo*_combined_*.root

	echo "Copying QCD Files"
	python create_eos_copy_commands.py QCD_eos_paths.txt
	source eos_copy_commands.sh
	rm QCD*_combined_*.root

	echo "Copying Single Top Files"
	python create_eos_copy_commands.py ST_eos_paths.txt
	source eos_copy_commands.sh
	rm ST_*_combined_*.root

	echo "Copying data files"
	python create_eos_copy_commands.py data_eos_paths.txt
	source eos_copy_commands.sh
	rm data*_combined_*.root
	echo "Copying signal files"
	python create_eos_copy_commands.py signal_eos_paths.txt
	source eos_copy_commands.sh
	
	rm *Suu*_combined_*.root

	## to merge
		# get the file paths
		# run create_eos_copy_commands.py to create commands
		# run the .sh from this
		# rm old eos paths
		# copy new files to eos
		# remove files from combinedROOT


	echo "Removing old eos file paths."
	#eosrm /store/user/ecannaer/combinedROOT/*$2*combined.root

	echo "Copying new eos files to root://cmseos.fnal.gov//store/user/ecannaer/combinedROOT"
	xrdcp -f *$2*combined.root root://cmseos.fnal.gov//store/user/ecannaer/sideband_combinedROOT/
	echo "Deleting eos files here to save space."
	rm *$2*combined.root

	rm WJets_eos_paths.txt
	rm TTbar_eos_paths.txt
	rm QCD_eos_paths.txt
	rm ST_eos_paths.txt
	rm data_eos_paths.txt
	rm signal_eos_paths.txt

	echo "The eos folder $1 was merged on $(date)" >> last_merge.txt

	echo "Finished."
	echo "WARNING: data files are set to not be copied. Change this in the script if you want these."

fi


