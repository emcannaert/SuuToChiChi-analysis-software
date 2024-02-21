
## now loop through the above array
for year in '2015' '2016' '2017' '2018';
do
	for systematic in 'nom' 'JEC' 'JER';
	do
		hadd -f QCDMC_combined_${year}_${systematic}_CUTFLOW.root QCDMC1000to1500_${year}_${systematic}_CUTFLOW.root QCDMC1500to2000_${year}_${systematic}_CUTFLOW.root QCDMC2000toInf_${year}_${systematic}_CUTFLOW.root
		hadd -f TTbarMC_combined_${year}_${systematic}_CUTFLOW.root TTToHadronicMC_${year}_${systematic}_CUTFLOW.root TTToSemiLeptonicMC_${year}_${systematic}_CUTFLOW.root TTToLeptonicMC_${year}_${systematic}_CUTFLOW.root
		hadd -f STMC_combined_${year}_${systematic}_CUTFLOW.root ST_t-channel-top_inclMC_${year}_${systematic}_CUTFLOW.root ST_t-channel-antitop_inclMC_${year}_${systematic}_CUTFLOW.root ST_s-channel-hadronsMC_${year}_${systematic}_CUTFLOW.root ST_s-channel-leptonsMC_${year}_${systematic}_CUTFLOW.root ST_tW-antiTop_inclMC_${year}_${systematic}_CUTFLOW.root ST_tW-top_inclMC_${year}_${systematic}_CUTFLOW.root
	done
done