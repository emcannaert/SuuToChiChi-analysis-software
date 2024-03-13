for year in "2015" "2016" "2017" "2018";
do
	for syst in "_JEC" "_JER" "";
	do
		echo crab submit -c crab_clusteringAnalyzer_TTToLeptonicMC_${year}${syst}.py  >> submitCrab_MC_${year}${syst}.sh
		echo crab submit -c crab_clusteringAnalyzer_TTToSemiLeptonicMC_${year}${syst}_cfg.py >>  submitCrab_MC_${year}${syst}.sh
	done
done
