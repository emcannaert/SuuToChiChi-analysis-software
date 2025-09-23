#!/bin/bash

# usage: find_eos_files.sh <main eos folder to search> <year>

EOSBASE="/store/user/ecannaer/" 

if [ -z "$1"  ];
then 
	echo "Invalid crab submission folder. Please provide the most recent crab submission folder on eos (Ex. SuuToChiChi_123421234)."
	echo "The second option should be the year to process."
else
	echo "Looking for EOS files for directory $EOSBASE$1 for year $2."

	xrdfs root://cmseos.fnal.gov ls -R $EOSBASE$1 > ../txt_files/all_files.txt
	

	#grep -v root all_files.txt | grep /0000 | grep HTHT > HTHT_eos_paths.txt
	#grep -v root all_files.txt | grep /0000 | grep WBWB > WBWB_eos_paths.txt
	#grep -v root all_files.txt | grep /0000 | grep ZTZT > ZTZT_eos_paths.txt
	#grep -v root all_files.txt | grep /0000 | grep WBHT > WBHT_eos_paths.txt
	#grep -v root all_files.txt | grep /0000 | grep WBZT > WBZT_eos_paths.txt
	#grep -v root all_files.txt | grep /0000 | grep HTZT > HTZT_eos_paths.txt

	grep -v root all_files.txt | grep -E "_${2}_"  | grep "WW_MC" | grep /000  > ../txt_files/WW_eos_paths.txt

	grep -v root all_files.txt | grep -E "_${2}_"  | grep "WW_MC" | grep /000  > ../txt_files/WW_eos_paths.txt
	grep -v root all_files.txt | grep -E "_${2}_"  | grep "ZZ_MC" | grep /000  > ../txt_files/ZZ_eos_paths.txt
	grep -v root all_files.txt | grep -E "_${2}_"  | grep "WJets" | grep /000  > ../txt_files/WJets_eos_paths.txt
	grep -v root all_files.txt | grep -E "_${2}_"  | grep "MSuu" | grep /000  > ../txt_files/signal_eos_paths.txt
	grep -v root all_files.txt | grep -E "_${2}_"  | grep "TTJets" | grep /000  > ../txt_files/TTbar_eos_paths.txt
	grep -v root all_files.txt | grep -E "_${2}_"  | grep "TTTo" | grep /000  >> ../txt_files/TTbar_eos_paths.txt # new, done to get the leptonic and semi-leptonic TTbar files
	grep -v root all_files.txt | grep -E "_${2}_"  | grep "QCD_HT" | grep /000  > ../txt_files/QCD_eos_paths.txt
	grep -v root all_files.txt | grep -E "_${2}_"  | grep "QCD_Pt" | grep /000  > ../txt_files/QCD_Pt_eos_paths.txt
	grep -v root all_files.txt | grep -E "_${2}_"  | grep "ST_" | grep /000  > ../txt_files/ST_eos_paths.txt	
	grep -v root all_files.txt | grep -E "_${2}_"  | grep "data" | grep /000  > ../txt_files/data_eos_paths.txt
	echo "Finished."
    #rm all_files.txt
fi


