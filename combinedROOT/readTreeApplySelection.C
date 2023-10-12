#include <iostream>
#include <string>
#include "TLorentzVector.h"

using namespace std;

void doThings(std::string inFileName, std::string outFileName, double& nEvents,double &nHTcut,  double &nAK8JetCut, double &nHeavyAK8Cut,double &nBtagCut,double &nDoubleTagged, double &eventScaleFactors, std::string year, std::string systematic)
{


   double totHT, dijetMassOne, dijetMassTwo;
   int nfatjets, nfatjet_pre;

   const char *_inFilename = inFileName.c_str();

   std::cout << "Reading file: " << _inFilename << std::endl;

   TFile *f = new TFile(_inFilename);   //import filename and open file
   const char *_outFilename = outFileName.c_str();    //create the output file where the skimmed tree will be 

   std::cout << "The output file name is : " << _outFilename << std::endl;

   TFile outFile(_outFilename,"RECREATE");
   
   std::vector<std::string> systematic_suffices;

   if(systematic == "nom") systematic_suffices = {""};

   else { systematic_suffices = {"up", "down"};}


   for(auto systematic_suffix = systematic_suffices.begin(); systematic_suffix < systematic_suffices.end();systematic_suffix++)
   {
      std::cout << "Looking at the " << *systematic_suffix << " tree" << std::endl;


      //std::string treeName = ("clusteringAnalyzerAll_" + systematic+ "_" + *systematic_suffix+ "/tree_"+ systematic + "_" + *systematic_suffix).c_str();

      //std::cout << "Interpolated the tree name to be " << treeName  << std::endl;

      std::string tree_string;
      std::string new_tree_string;
      if(*systematic_suffix == "")
      {
         tree_string = "";
         new_tree_string = "nom";
      } 
      else
      { 
         tree_string = ( systematic+ "_" + *systematic_suffix   ).c_str();
         new_tree_string = (systematic + "_").c_str();
      }


      std::string oldTreeName = ("clusteringAnalyzerAll_" + tree_string + "/tree_"+ tree_string).c_str();
      std::string newTreeName = ("skimmedTree_"+ new_tree_string + *systematic_suffix).c_str();

      std::cout << "looking for tree name: " << oldTreeName<< std::endl;
      std::cout << "naming new tree " << newTreeName << std::endl;

      TTree *t1 = (TTree*)f->Get( ("clusteringAnalyzerAll_" + tree_string + "/tree_"+ tree_string).c_str()   ); 



      outFile.cd();   // return to outer directory
      gDirectory->mkdir( (systematic+"_"+ *systematic_suffix).c_str()  );   //create directory for this systematic
      outFile.cd( (systematic+"_"+*systematic_suffix).c_str() );   // go inside the systematic directory 

      auto *t2 = t1->CloneTree(0);

      t2->SetName(   ("skimmedTree_"+ new_tree_string + *systematic_suffix).c_str()  );

      const Int_t nentries = t1->GetEntries();


      t1->SetBranchAddress("totHT", &totHT);   
      t1->SetBranchAddress("nfatjets", &nfatjets);     
      t1->SetBranchAddress("nfatjet_pre", &nfatjet_pre); 
      t1->SetBranchAddress("dijetMassOne", &dijetMassOne);   
      t1->SetBranchAddress("dijetMassTwo", &dijetMassTwo);   

      for (Int_t i=0;i<nentries;i++) 
      {  
         nEvents+=eventScaleFactors;
         t1->GetEntry(i);
         if (totHT < 1500.) continue; 
         nHTcut+=eventScaleFactors;
         if( (nfatjets < 3)   ) continue;
         nAK8JetCut+=eventScaleFactors;
         if ((nfatjet_pre < 2) && ( (dijetMassOne < 1000. ) || ( dijetMassTwo < 1000.)  ))continue;

         nHeavyAK8Cut+=eventScaleFactors;
         t2->Fill();
      }
      outFile.Write();


   }
   outFile.Close();

}


void readTreeApplySelection()
{

   // you must change these ........
   bool runData = false;
   bool includeTTBar = true;
   bool allHTBins    = true;
   double nEvents = 0.;
   double nHTcut  = 0.;
   double nAK8JetCut = 0.;
   double nHeavyAK8Cut = 0.;
   double nBtagCut = 0.;
   double nDoubleTagged = 0.;
   //std::vector<std::string> dataYear = {"2015","2016","2017","2018"};
   std::vector<std::string> dataYear = {"2018"};    // for testing 

   std::vector<std::string> systematics = {"JEC","JER","nom"};   // will eventually use this to skim the systematic files too
   if(!runData)
   {
      int yearNum = 0;
      if(includeTTBar && allHTBins)
      {


         //need to have the event scale factors calculated for each year and dataset
         double eventScaleFactors[4][4] = {  {1.0,1.0,1.0}, {1.0,1.0,1.0}, {1.0,1.0,1.0},{1.0,1.0,1.0}   }; //TODO
         for(auto year = dataYear.begin();year<dataYear.end();year++)
         {
            for( auto systematic = systematics.begin(); systematic < systematics.end();systematic++)
            {


               std::string dataYear = *year;
               std::string systematic_str = *systematic;
               std::vector<std::string> inFileNames = { "TTToHadronic_"+dataYear +  "_"+ systematic_str+ "_combined.root"
 
                                                /*   TESTING
                                                 ("/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/QCDMC_HT1000to1500_" +dataYear+ "_"+systematic_str +"_combined.root").c_str(),
                                                 ("/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/QCDMC_HT1500to2000_" +dataYear+ "_"+systematic_str +"_combined.root").c_str(),
                                                  ("/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/QCDMC_HT2000toInf_" +dataYear+ "_" +systematic_str +"_combined.root").c_str(),
                                                  ("/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/TTToHadronic_" +dataYear+ "_" +systematic_str +"_combined.root").c_str()*/
                                               };
               std::vector<std::string> outFileNames = {"TTToHadronic_"+dataYear +  "_"+ systematic_str+ "_SKIMMED.root"

                                                /*           TESTING
                                                 ("/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/QCDMC_HT1000to1500_" +dataYear+ "_" +systematic_str+"_SKIMMED.root").c_str(),
                                                 ("/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/QCDMC_HT1500to2000_" +dataYear+ "_" +systematic_str+"_SKIMMED.root").c_str(),
                                                  ("/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/QCDMC_HT2000toInf_" +dataYear+ "_" +systematic_str+"_SKIMMED.root").c_str(),
                                                  ("/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/TTToHadronic_" +dataYear+ "_" +systematic_str+"_SKIMMED.root").c_str()*/
                                               };
           
               for(unsigned int iii = 0; iii<inFileNames.size(); iii++)
               {
                  doThings(inFileNames[iii],outFileNames[iii],nEvents,nHTcut,nAK8JetCut,nHeavyAK8Cut,nBtagCut,nDoubleTagged,eventScaleFactors[yearNum][iii],*year, *systematic);
               }

               std::cout << "Finished with "<< inFileNames.size() << " files for "<< *year<< "." << std::endl;
               std::cout << "For " << *year<< ": total/HTcut/AK8jetCut/heavyAK8JetCut:" <<nEvents << "/" << nHTcut << "/" << nAK8JetCut<< "/" << nHeavyAK8Cut<< std::endl;

               yearNum++;
            }
         }


      }
   }
}

