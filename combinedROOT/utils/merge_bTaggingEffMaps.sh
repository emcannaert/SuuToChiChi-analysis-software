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

	echo "Copying TTbar Files"
	python create_eos_copy_commands_btaggingEffMaps.py ../txt_files/TTbar_eos_paths.txt
	source eos_copy_commands_btagging.sh

	echo "Copying QCD Files"
	python create_eos_copy_commands_btaggingEffMaps.py ../txt_files/QCD_eos_paths.txt
	source eos_copy_commands_btagging.sh

	echo "Copying Single Top Files"
	python create_eos_copy_commands_btaggingEffMaps.py ../txt_files/ST_eos_paths.txt
	source eos_copy_commands_btagging.sh

	echo "Copying signal files"
	python create_eos_copy_commands_btaggingEffMaps.py ../txt_files/signal_eos_paths.txt
	source eos_copy_commands_btagging.sh

	rm btagging_efficiencyMap*_combined_*_*.root

	rm ../txt_files/TTbar_eos_paths.txt
	rm ../txt_files/QCD_eos_paths.txt
	rm ../txt_files/ST_eos_paths.txt
	rm ../txt_files/data_eos_paths.txt
	rm ../txt_files/signal_eos_paths.txt

	echo "Finished."

fi


