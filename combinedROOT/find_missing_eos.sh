echo "Enter the most recent eos crab output directory"
eosls -l /store/user/ecannaer/combinedROOT/ | grep root > all_eos_files.txt
xrdfs root://cmseos.fnal.gov ls -R /store/user/ecannaer/$1 > all_eos_crab_files.txt
python check_missing_eos.py
echo "Missing eos files written to check_missing_eos.py "
