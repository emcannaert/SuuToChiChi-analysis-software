for year in "2015" "2016" "2017" "2018";
do
	for syst in "_JEC" "_JER" "";
	do

		echo crab status -d crab_projects/crab_clustAlg_TTToSemiLeptonicMC_${year}${syst}_AltDatasets_000 >> checkCrab_All_MC_All_years.sh
		echo crab status -d crab_projects/crab_clustAlg_TTToLeptonicMC_${year}${syst}_AltDatasets_000 >> checkCrab_All_MC_All_years.sh

	done
done
