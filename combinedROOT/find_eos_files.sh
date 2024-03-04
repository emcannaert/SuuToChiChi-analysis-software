#!/bin/bash

# usage: find_eos_files.sh <main eos folder to search> <year>

EOSBASE="/store/user/ecannaer/" 

if [ $1 -q ""];
then 
	echo "Invalid crab submission folder. Please provide the most recent crab submission folder on eos (Ex. SuuToChiChi_123421234)."
	echo "The second option should be the year to process."
else
	echo "Looking for EOS files for directory $EOSBASE$1 for year $2."

	xrdfs root://cmseos.fnal.gov ls -R /store/user/ecannaer/$1 > all_files.txt
	

	#grep -v root all_files.txt | grep /0000 | grep HTHT > HTHT_eos_paths.txt
	#grep -v root all_files.txt | grep /0000 | grep WBWB > WBWB_eos_paths.txt
	#grep -v root all_files.txt | grep /0000 | grep ZTZT > ZTZT_eos_paths.txt
	#grep -v root all_files.txt | grep /0000 | grep WBHT > WBHT_eos_paths.txt
	#grep -v root all_files.txt | grep /0000 | grep WBZT > WBZT_eos_paths.txt
	#grep -v root all_files.txt | grep /0000 | grep HTZT > HTZT_eos_paths.txt
	grep -v root all_files.txt | grep $2 | grep "MSuu" | grep /000  > signal_eos_paths.txt
	grep -v root all_files.txt | grep $2 | grep "TTJets" | grep /000  > TTbar_eos_paths.txt
	grep -v root all_files.txt | grep $2 | grep "QCD" | grep /000  > QCD_eos_paths.txt
	grep -v root all_files.txt | grep $2 | grep "ST_" | grep /000  > ST_eos_paths.txt	
	grep -v root all_files.txt | grep $2 | grep "data" | grep /000  > data_eos_paths.txt
	echo "Finished."
    #rm all_files.txt
fi


