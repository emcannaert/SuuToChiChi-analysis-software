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

python create_eos_copy_commands.py TTbar_eos_paths.txt
source eos_copy_commands.sh
rm TTTo*_combined_*.root

echo "Removing old eos file paths."
eosrm /store/user/ecannaer/combinedROOT/TTJets*$2*combined.root
fi