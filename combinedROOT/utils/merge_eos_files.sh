#!/bin/bash

# usage: find_eos_files.sh <main eos folder to search> <year>

EOSBASE="/store/user/ecannaer/" 
runOptWP=""    
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

# restore positional parameters
set -- "${POSITIONAL[@]}"

if [ -z "$1" ];
then 
	echo "Invalid crab submission folder. Please provide the most recent crab submission folder on eos (Ex. SuuToChiChi_123421234)."
	echo "The second option should be the year to process."
else
	echo "Getting all eos file paths"
	source find_eos_files.sh $1 $2
	
	## try to make these two folders that will be needed
	eosmkdir $EOSBASE/combinedROOT
	eosmkdir $EOSBASE/combinedROOT_temp

	rm eos_copy_commands.sh

	if ! $signalOnly; then
		echo "Copying WW Files"
		python create_eos_copy_commands.py ../txt_files/WW_eos_paths.txt ${runOptWP}
		source eos_copy_commands.sh
		eosrm $EOSBASE/combinedROOT_temp/WW_MC*_combined_*.root

		echo "Copying ZZ Files"
		python create_eos_copy_commands.py ../txt_files/ZZ_eos_paths.txt ${runOptWP}
		source eos_copy_commands.sh
		eosrm $EOSBASE/combinedROOT_temp/ZZ_MC*_combined_*.root


		echo "Copying QCD Pt Files"
		python create_eos_copy_commands.py ../txt_files/QCD_Pt_eos_paths.txt ${runOptWP}
		source eos_copy_commands.sh
		eosrm $EOSBASE/combinedROOT_temp/QCDMC_Pt_*_combined_*.root



		echo "Copying W+Jets Files"
		python create_eos_copy_commands.py ../txt_files/WJets_eos_paths.txt ${runOptWP}
		source eos_copy_commands.sh
		if source eos_copy_commands.sh; then
			echo "WJets files successfully merged. Now removing any residual files in combinedROOT_temp."
			eosrm $EOSBASE/combinedROOT_temp/WJets*_combined_*.root
		else
		    echo "---------------> ERROR: WJets file merging failed."
		fi

		echo "Copying TTbar Files"
		python create_eos_copy_commands.py ../txt_files/TTbar_eos_paths.txt ${runOptWP}
		source eos_copy_commands.sh
		if source eos_copy_commands.sh; then
			echo "TTbar files successfully merged. Now removing any residual files in combinedROOT_temp."
			eosrm $EOSBASE/combinedROOT_temp/TTTo*_combined_*.root
			eosrm $EOSBASE/combinedROOT_temp/TTJets*_combined_*.root

		else
		    echo "---------------> ERROR: TTbar file merging failed."
		fi

		echo "Copying QCD Files"
		python create_eos_copy_commands.py ../txt_files/QCD_eos_paths.txt ${runOptWP}
		source eos_copy_commands.sh
		if source eos_copy_commands.sh; then
			echo "QCD files successfully merged. Now removing any residual files in combinedROOT_temp."
			eosrm $EOSBASE/combinedROOT_temp/QCDMC*_combined_*.root
		else
		    echo "---------------> ERROR: QCD file merging failed."
		fi

		echo "Copying Single Top Files"
		python create_eos_copy_commands.py ../txt_files/ST_eos_paths.txt ${runOptWP}
		source eos_copy_commands.sh
		if source eos_copy_commands.sh; then
			echo "ST files successfully merged. Now removing any residual files in combinedROOT_temp."
			eosrm $EOSBASE/combinedROOT_temp/ST_*_combined_*.root
		else
		    echo "---------------> ERROR: ST file merging failed."
		fi

		echo "Copying data files"
		python create_eos_copy_commands.py ../txt_files/data_eos_paths.txt ${runOptWP}
		if source eos_copy_commands.sh; then
			echo "Data files successfully merged. Now removing any residual files in combinedROOT_temp."
			eosrm $EOSBASE/combinedROOT_temp/data*_combined_*.root
		else
		    echo "---------------> ERROR: data file merging failed."
		fi

	else
		echo "Copying signal files"
		python create_eos_copy_commands.py ../txt_files/signal_eos_paths.txt ${runOptWP}

		if source eos_copy_commands.sh; then
			echo "Signal files successfully merged. Now removing any residual files in combinedROOT_temp."
		    eosrm $EOSBASE/combinedROOT_temp/*Suu*_combined_*.root
		else
		    echo "---------------> ERROR: signal file merging failed."
		fi
	fi
	## to merge
		# get the file paths
		# run create_eos_copy_commands.py to create commands
		# run the .sh from this
		# rm old eos paths
		# copy new files to eos
		# remove files from combinedROOT

	#echo "Moving eos files to root://cmseos.fnal.gov/$EOSBASE/combinedROOT"
	#eosmv -f root://cmseos.fnal.gov/$EOSBASE/combinedROOT_temp/*$2*combined.root root://cmseos.fnal.gov/$EOSHOME/combinedROOT/
	#echo "Deleting eos files here to save space."
	#rm *$2*combined.root

	rm ../txt_files/WJets_eos_paths.txt
	rm ../txt_files/TTbar_eos_paths.txt
	rm ../txt_files/QCD_eos_paths.txt
	rm ../txt_files/ST_eos_paths.txt
	rm ../txt_files/data_eos_paths.txt
	#rm ../txt_files/signal_eos_paths.txt
	rm ../txt_files/WW_eos_paths.txt
	rm ../txt_files/ZZ_eos_paths.txt
	echo "The eos folder $1 was merged on $(date)" >> ../txt_files/last_merge.txt

	echo "Finished."
	#$echo "WARNING: data files are set to not be copied. Change this in the script if you want these."

fi


