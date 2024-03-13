for year in "2015" "2016" "2017" "2018";
do
        for syst in "_JEC" "_JER" "";
        do
                sed -i "/TTToSemiLeptonicMC/d" resubmitCrab_MC${syst}_${year}.sh
                sed -i "/TTToLeptonicMC/d" resubmitCrab_MC${syst}_${year}.sh

        done
done
