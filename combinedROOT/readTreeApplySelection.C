#include <iostream>
#include <string>
#include "TLorentzVector.h"

using namespace std;

void doThings(std::string inFileName, std::string outFileName, double &eventScaleFactors, std::string year, std::string systematic, std::string dataBlock)
{

   double totHT, dijetMassOne, dijetMassTwo;
   int nfatjets, nfatjet_pre,nAK4;
   double SJ_mass_100[100], AK4_pt[100],AK4_DeepJet_disc[100];
   int SJ_nAK4_300[100];
   double PU_eventWeight_nom, bTag_eventWeight_nom;

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

      double nEvents =0,nHTcut =0 ,nAK8JetCut =0,nHeavyAK8Cut=0,nBtagCut=0,nSJEnergyCut=0, nSJMass100Cut=0;
      double nZeroBtag = 0, nZeroBtagnSJEnergyCut = 0, nZeroBtagnSJMass100Cut = 0;
      double nCR_antitag = 0, nSR_antitag = 0;
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

      t1->SetBranchAddress("dijetMassTwo", &dijetMassTwo);   
      t1->SetBranchAddress("dijetMassTwo", &dijetMassTwo);   
      t1->SetBranchAddress("dijetMassTwo", &dijetMassTwo);   
      t1->SetBranchAddress("nAK4" , &nAK4); 

      t1->SetBranchAddress("SJ_mass_100", SJ_mass_100);   
      t1->SetBranchAddress("lab_AK4_pt", AK4_pt); 
      t1->SetBranchAddress("SJ_nAK4_300", SJ_nAK4_300);
      t1->SetBranchAddress("AK4_DeepJet_disc", AK4_DeepJet_disc); 

      t1->SetBranchAddress("bTag_eventWeight_nom", &bTag_eventWeight_nom); 
      t1->SetBranchAddress("PU_eventWeight_nom", &PU_eventWeight_nom); 

      double looseDeepCSV_DeepJet;
      double medDeepCSV_DeepJet;
      double tightDeepCSV_DeepJet;

      if(year == "2015")
      {
         looseDeepCSV_DeepJet = 0.0490;
         medDeepCSV_DeepJet   = 0.2783;
         tightDeepCSV_DeepJet = 0.7100;
      }
      else if(year == "2016")
      {
         looseDeepCSV_DeepJet = 0.0490;
         medDeepCSV_DeepJet   = 0.2783;
         tightDeepCSV_DeepJet = 0.7100;
      }
      else if(year == "2017")
      {
         looseDeepCSV_DeepJet = 0.0490;
         medDeepCSV_DeepJet   = 0.2783;
         tightDeepCSV_DeepJet = 0.7100;
      }
      else if(year == "2018")
      {
         looseDeepCSV_DeepJet = 0.0490;
         medDeepCSV_DeepJet   = 0.2783;
         tightDeepCSV_DeepJet = 0.7100;
      }
      double eventWeight = 1.0;
      for (Int_t i=0;i<nentries;i++) 
      {  


         if ((bTag_eventWeight_nom != bTag_eventWeight_nom) || (std::isinf(bTag_eventWeight_nom)))
         {
            bTag_eventWeight_nom = 0;
         }
         if ((PU_eventWeight_nom != PU_eventWeight_nom) || (std::isinf(PU_eventWeight_nom)))
         {
            PU_eventWeight_nom = 0;
         }
         eventWeight = bTag_eventWeight_nom*PU_eventWeight_nom;

         //std::cout <<"Count is "<<nEvents  << ", " << bTag_eventWeight_nom << " " << PU_eventWeight_nom<< std::endl;
         nEvents+=eventWeight;
         t1->GetEntry(i);
         if (totHT < 1500.) continue; 
         nHTcut+=eventWeight;
         if( (nfatjets < 3)   ) continue;
         nAK8JetCut+=eventWeight;
         if ((nfatjet_pre < 2) && ( (dijetMassOne < 1000. ) || ( dijetMassTwo < 1000.)  ))continue;
         nHeavyAK8Cut+=eventWeight;

         int nTightBTags = 0;
         for(int iii = 0;iii< nAK4; iii++)
         {

            if ( (AK4_DeepJet_disc[iii] > tightDeepCSV_DeepJet ) && (AK4_pt[iii] > 30.)) nTightBTags++;
         }
         if ( (nTightBTags > 0)  )
         {
            nBtagCut+=eventWeight;
            if((SJ_nAK4_300[0]>=2) && (SJ_nAK4_300[1]>=2)   )
            {
               nSJEnergyCut+=eventWeight;
               if((SJ_mass_100[0]>=400.) && (SJ_mass_100[1]>400.)   )
               {
                  nSJMass100Cut+=eventWeight;
               }
            }
         }
         else
         {
            nZeroBtag+=eventWeight;
            if((SJ_nAK4_300[0]>=2) && (SJ_nAK4_300[1]>=2)   )
            {
               nZeroBtagnSJEnergyCut+=eventWeight;
               if((SJ_mass_100[0]>=400.) && (SJ_mass_100[1]>400.)   )
               {
                  nZeroBtagnSJMass100Cut+=eventWeight;
               }
            }
            
         }
         t2->Fill();
      }
      outFile.Write();
      std::cout << "Signal Region for " << dataBlock << ", "<<  year << " and " << tree_string << ": total/HTcut/AK8jetCut/heavyAK8JetCut/nBtagCut/nSJEnergyCut/nSJMass100Cut:" <<nEvents << " " << nHTcut << " " << nAK8JetCut<< " " << nHeavyAK8Cut<< " " << nBtagCut << " " << nSJEnergyCut << " " << nSJMass100Cut << std::endl;
      std::cout << "Control Region for " << dataBlock << ", "<<  year << " and " << tree_string << ": total/HTcut/AK8jetCut/heavyAK8JetCut/nZeroBtag/nZeroBtagnSJEnergyCut/nZeroBtagnSJMass100Cut:" <<nEvents << " " << nHTcut << " " << nAK8JetCut<< " " << nHeavyAK8Cut<< " " << nZeroBtag << " " << nZeroBtagnSJEnergyCut << " " << nZeroBtagnSJMass100Cut << std::endl;


   }
   outFile.Close();

}


void readTreeApplySelection()
{

   // you must change these ........
   bool runData = false;
   bool includeTTBar = true;
   bool allHTBins    = true;

   std::vector<std::string> years = {"2015"};//{"2015","2016","2017","2018"};    // for testing  "2015","2016","2017"
   std::vector<std::string> systematics = {"nom"};//{"nom", "JEC","JER"};   // will eventually use this to skim the systematic files too
   int yearNum = 0;
   //need to have the event scale factors calculated for each year and dataset
   double eventScaleFactor = 1; 
   for(auto datayear = years.begin();datayear<years.end();datayear++)
   {

      std::vector<std::string> dataBlocks; 
      std::string skimmedFilePaths;

      if(runData)
      {

         if(*datayear == "2015")
         {
            dataBlocks = {"JetHT_dataB-ver2_","JetHT_dataC-HIPM_","JetHT_dataD-HIPM_","JetHT_dataE-HIPM_","JetHT_dataF-HIPM_"}; // JetHT_dataB-ver1 not present
         }
         else if(*datayear == "2016")
         {
            dataBlocks = {"JetHT_dataF_", "JetHT_dataG_", "JetHT_dataH_"};
         }
         else if(*datayear == "2017")
         {
            dataBlocks = {"JetHT_dataB_","JetHT_dataC_","JetHT_dataD_","JetHT_dataE_", "JetHT_dataF_"};
         }
         else if(*datayear == "2018")
         {
            dataBlocks = {"JetHT_dataA_","JetHT_dataB_","JetHT_dataC_","JetHT_dataD_"};
         }
      }
      else
      {  
        //dataBlocks = {"QCDMC2000toInf_"}; 
        // dataBlocks = {"ST_t-channel-top_inclMC","ST_t-channel-antitop_inclMC","ST_s-channel-hadronsMC","ST_s-channel-leptonsMC","ST_tW-antiTop_inclMC","ST_tW-top_inclMC"};
	     dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"};
         //dataBlocks = {"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"};
      }
      for(auto dataBlock = dataBlocks.begin();dataBlock < dataBlocks.end();dataBlock++)
      {
         for( auto systematic = systematics.begin(); systematic < systematics.end();systematic++)
         {


            std::string year = *datayear;
            std::string systematic_str = *systematic;

            std::string inFileName = (*dataBlock+year +  "_"+ systematic_str+ "_combined.root").c_str();
            std::string outFileName = (*dataBlock+year +  "_"+ systematic_str+ "_SKIMMED.root").c_str();

            doThings(inFileName,outFileName,eventScaleFactor,year, *systematic,*dataBlock);

            std::cout << "Finished with "<< inFileName << std::endl;

            yearNum++;
         }
      }
   }
}

