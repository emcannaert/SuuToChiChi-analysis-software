#!/bin/bash

# usage: find_eos_files.sh <main eos folder to search> <year>

EOSBASE="/store/user/ecannaer/" 

runOptWP=""  
forceNonOptWP=""  
signalOnly=false

POSITIONAL=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --runOptWP)
            runOptWP="runOptWP"
            echo "Merging as optimized WP data."
            shift
            ;;
        --signalOnly)
            signalOnly=true
            echo "Running SIGNAL ONLY workflow."
            shift
            ;;
        --forceNonOptWP)
            forceNonOptWP="-f"
            echo "Forcing to NOT be optWP."
            shift
            ;;
        --) # end of options
            shift
            break
            ;;
        -*|--*)
            echo "Warning: unknown option: $1" >&2
            shift
            ;;
        *)
            POSITIONAL+=("$1") # save positional
            shift
            ;;
    esac
done

if [ -z "$1" ];
then 
	echo "Invalid crab submission folder. Please provide the most recent crab submission folder on eos (Ex. SuuToChiChi_123421234)."
	echo "The second option should be the year to process."
else

	echo "Getting all eos file paths"
	source find_eos_files.sh $1 $2
	
	echo "Copying signal files"
	python create_eos_copy_commands.py ../txt_files/signal_eos_paths.txt ${runOptWP:-""} ${forceNonOptWP:-""} 
	source eos_copy_commands.sh
	
	rm *Suu*_combined_*.root

	## to merge
		# get the file paths
		# run create_eos_copy_commands.py to create commands
		# run the .sh from this
		# rm old eos paths
		# copy new files to eos
		# remove files from combinedROOT


	echo "Copying new eos files to root://cmseos.fnal.gov/$EOSBASE/combinedROOT"
	xrdcp -f *$2*combined.root root://cmseos.fnal.gov/$EOSBASE/combinedROOT/
	echo "Deleting eos files here to save space."
	rm *$2*combined.root
	rm *_eos_paths.txt
	rm ../txt_files/signal_eos_paths.txt
	echo "The eos folder $1 was merged on $(date)" >> last_merge.txt

	echo "Finished."
	#$echo "WARNING: data files are set to not be copied. Change this in the script if you want these."

fi
