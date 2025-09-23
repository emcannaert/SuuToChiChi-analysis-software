#!/bin/bash

print_file_info() {
	if [ $# -eq 0 ]; then
	    echo "Usage: $0 <eos path1> [<eos path 2> ...]"
	    echo "Enter the most recent eos crab output directory"
	    return 1  # running as a function so this doesn't exit out from remote connections
	fi

	rm ../txt_files/all_eos_crab_files.txt
	touch ../txt_files/all_eos_crab_files.txt

	eosls -l /store/user/ecannaer/combinedROOT/ | grep root > ../txt_files/all_combined_eos_files.txt
	eosls -l /store/user/ecannaer/skimmedFiles/ | grep root > ../txt_files/all_skimmed_eos_files.txt
	eosls -l /store/user/ecannaer/cutflowFiles/ | grep root > ../txt_files/all_cutflow_eos_files.txt

	ls -ltrh processedFiles | grep root > ../txt_files/all_processed_eos_files.txt

	for path in "$@"; do
	    echo "Adding eos information from: $path"
	    xrdfs root://cmseos.fnal.gov ls -l -R /store/user/ecannaer/$path | grep -v root > ../txt_files/all_eos_crab_files.txt
	done

	python check_missing_eos.py
	
	rm ../txt_files/all_combined_eos_files.txt
	rm ../txt_files/all_skimmed_eos_files.txt
	rm ../txt_files/all_cutflow_eos_files.txt
	rm ../txt_files/all_processed_eos_files.txt
	rm ../txt_files/all_eos_crab_files.txt	

	echo "Missing eos files written to missing_files.txt "
}
print_file_info "$@"
