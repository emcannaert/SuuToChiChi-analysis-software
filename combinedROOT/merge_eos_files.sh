#!/bin/bash

# usage: find_eos_files.sh <main eos folder to search> <year>

EOSBASE="/store/user/ecannaer/" 

if [ $1 -q ""];
then 
	echo "Invalid crab submission folder. Please provide the most recent crab submission folder on eos (Ex. SuuToChiChi_123421234)."
	echo "The second option should be the year to process."
else

	echo "Getting all eos file paths"
	source find_eos_files.sh $1 $2
	echo "Copying TTbar Files"

	python create_eos_copy_commands.py TTbar_eos_paths.txt
	source eos_copy_commands.sh

	echo "Copying QCD Files"
	python create_eos_copy_commands.py QCD_eos_paths.txt
	source eos_copy_commands.sh

	echo "Copying Single Top Files"
	python create_eos_copy_commands.py ST_eos_paths.txt
	source eos_copy_commands.sh

	python create_eos_copy_commands.py data_eos_paths.txt
	#source eos_copy_commands.sh

	python create_eos_copy_commands.py signal_eos_paths.txt
	#source eos_copy_commands.sh

	## to merge
		# get the file paths
		# run create_eos_copy_commands.py to create commands
		# run the .sh from this
		# rm old eos paths
		# copy new files to eos
		# remove files from combinedROOT

	echo "Removing old eos file paths."
	eosrm /store/user/ecannaer/combinedROOT/*$2*combined.root

	echo "Copying new eos files to root://cmseos.fnal.gov//store/user/ecannaer/combinedROOT"
	xrdcp *$2*combined.root root://cmseos.fnal.gov//store/user/ecannaer/combinedROOT/
	echo "Deleting eos files here to save space."
	rm *$2*combined.root
	rm TTbar_eos_paths.txt
	rm QCD_eos_paths.txt
	rm ST_eos_paths.txt
	rm data_eos_paths.txt
	rm signal_eos_paths.txt
	echo "Finished."

	echo "WARNING: data and signal files are set to not be copied. Change this in the script if you want these."

fi


