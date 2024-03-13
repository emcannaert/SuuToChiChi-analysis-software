for year in "2015" "2016" "2017" "2018";
do
        for syst in "_JEC" "_JER";
        do

                echo crab resubmit --maxmemory 3500 -d crab_projects/crab_clustAlg_TTToSemiLeptonicMC_${year}${syst}_AltDatasets_000 >> resubmitCrab_MC${syst}_${year}.sh
                echo crab resubmit --maxmemory 3500 -d crab_projects/crab_clustAlg_TTToLeptonicMC_${year}${syst}_AltDatasets_000 >> resubmitCrab_MC${syst}_${year}.sh
        done
done


for year in "2015" "2016" "2017" "2018";
do

        echo crab resubmit --maxmemory 3500 -d crab_projects/crab_clustAlg_TTToSemiLeptonicMC_${year}_nom_AltDatasets_000 >> resubmitCrab_MC_${year}.sh
        echo crab resubmit --maxmemory 3500 -d crab_projects/crab_clustAlg_TTToLeptonicMC_${year}_nom_AltDatasets_000 >> resubmitCrab_MC_${year}.sh
done

