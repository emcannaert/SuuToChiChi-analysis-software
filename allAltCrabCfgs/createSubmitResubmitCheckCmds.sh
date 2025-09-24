ls crab_projects/*2015* | grep 000 > checkCrab_2015.sh
sed -i 's/000:/000/g' checkCrab_2015.sh 
sed -i 's/crab_projects/crab status -d crab_projects/g' checkCrab_2015.sh


ls crab_projects/*2015* | grep 000 > resubmitCrab_2015.sh
sed -i 's/000:/000/g' resubmitCrab_2015.sh 
sed -i 's/crab_projects/crab resubmit  --maxmemory 4000 -d crab_projects/g' resubmitCrab_2015.sh


ls *2015*.py > submitCrab_2015.sh
sed -i 's/crab_clustering/crab submit -c crab_clustering/g' submitCrab_2015.sh

ls crab_projects/*2016* | grep 000 > checkCrab_2016.sh
sed -i 's/000:/000/g' checkCrab_2016.sh 
sed -i 's/crab_projects/crab status -d crab_projects/g' checkCrab_2016.sh


ls crab_projects/*2016* | grep 000 > resubmitCrab_2016.sh
sed -i 's/000:/000/g' resubmitCrab_2016.sh 
sed -i 's/crab_projects/crab resubmit  --maxmemory 4000 -d crab_projects/g' resubmitCrab_2016.sh


ls *2016*.py > submitCrab_2016.sh
sed -i 's/crab_clustering/crab submit -c crab_clustering/g' submitCrab_2016.sh

ls crab_projects/*2017* | grep 000 > checkCrab_2017.sh
sed -i 's/000:/000/g' checkCrab_2017.sh 
sed -i 's/crab_projects/crab status -d crab_projects/g' checkCrab_2017.sh


ls crab_projects/*2017* | grep 000 > resubmitCrab_2017.sh
sed -i 's/000:/000/g' resubmitCrab_2017.sh 
sed -i 's/crab_projects/crab resubmit  --maxmemory 4000 -d crab_projects/g' resubmitCrab_2017.sh


ls *2017*.py > submitCrab_2017.sh
sed -i 's/crab_clustering/crab submit -c crab_clustering/g' submitCrab_2017.sh


ls crab_projects/*2018* | grep 000 > checkCrab_2018.sh
sed -i 's/000:/000/g' checkCrab_2018.sh 
sed -i 's/crab_projects/crab status -d crab_projects/g' checkCrab_2018.sh


ls crab_projects/*2018* | grep 000 > resubmitCrab_2018.sh
sed -i 's/000:/000/g' resubmitCrab_2018.sh 
sed -i 's/crab_projects/crab resubmit  --maxmemory 4000 -d crab_projects/g' resubmitCrab_2018.sh


ls *2018*.py > submitCrab_2018.sh
sed -i 's/crab_clustering/crab submit -c crab_clustering/g' submitCrab_2018.sh
