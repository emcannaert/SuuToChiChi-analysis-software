#!/bin/bash

EOSBASE="/store/user/ecannaer/" 

if [ $1 -q ""]
then 
	echo "Invalid crab submission folder. Please provide the most recent crab submission folder on eos (Ex. SuuToChiChi_123421234)"
	exit 1
fi

echo "Looking for EOS files for directory $EOSBASE$1."

xrdfs root://cmseos.fnal.gov ls -R /store/user/ecannaer/SuuToChiChi_202426_233436/ > all_files.txt

grep HTHT all_files.txt | grep .root > HTHT_eos_paths.txt
grep WBWB all_files.txt | grep .root > WBWB_eos_paths.txt
grep ZTZT all_files.txt | grep .root > ZTZT_eos_paths.txt
grep WBHT all_files.txt | grep .root > WBHT_eos_paths.txt
grep WBZT all_files.txt | grep .root > WBZT_eos_paths.txt
grep HTZT all_files.txt | grep .root > HTZT_eos_paths.txt

echo "Finished."

rm all_files.txt
