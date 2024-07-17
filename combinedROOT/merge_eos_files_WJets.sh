
	xrdfs root://cmseos.fnal.gov ls -R /store/user/ecannaer/SuuToChiChi_2024418_165246 > all_files.txt

	grep -v root all_files.txt | grep "_2015" | grep "WJetsMC" | grep /000  > WJets_eos_paths_2015.txt
	grep -v root all_files.txt | grep "_2016" | grep "WJetsMC" | grep /000  > WJets_eos_paths_2016.txt
	grep -v root all_files.txt | grep "_2017" | grep "WJetsMC" | grep /000  > WJets_eos_paths_2017.txt
	grep -v root all_files.txt | grep "_2018" | grep "WJetsMC" | grep /000  > WJets_eos_paths_2018.txt



	echo "Copying W+Jets Files"
	python create_eos_copy_commands.py WJets_eos_paths_2015.txt
	source eos_copy_commands.sh
	rm WJets*_combined_*.root
	xrdcp -f *2015*combined.root root://cmseos.fnal.gov//store/user/ecannaer/combinedROOT/
	rm *2015*combined.root

	python create_eos_copy_commands.py WJets_eos_paths_2016.txt
	source eos_copy_commands.sh
	rm WJets*_combined_*.root
	xrdcp -f *2016*combined.root root://cmseos.fnal.gov//store/user/ecannaer/combinedROOT/
	rm *2016*combined.root

	python create_eos_copy_commands.py WJets_eos_paths_2017.txt
	source eos_copy_commands.sh
	rm WJets*_combined_*.root
	xrdcp -f *2017*combined.root root://cmseos.fnal.gov//store/user/ecannaer/combinedROOT/
	rm *2017*combined.root

	python create_eos_copy_commands.py WJets_eos_paths_2018.txt
	source eos_copy_commands.sh
	rm WJets*_combined_*.root
	xrdcp -f *2018*combined.root root://cmseos.fnal.gov//store/user/ecannaer/combinedROOT/
	rm *2018*combined.root

	rm WJets_eos_paths*.txt
