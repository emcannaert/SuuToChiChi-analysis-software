#include <iostream>
#include <string>
#include "TLorentzVector.h"

using namespace std;

void doThings(std::string inFileName, std::string outFileName, double &eventScaleFactors, std::string year, std::vector<std::string> systematics, std::string dataBlock)
{

   double totHT, dijetMassOne, dijetMassTwo;
   int nfatjets, nfatjet_pre,nAK4;
   double SJ_mass_100[100], AK4_pt[100],AK4_DeepJet_disc[100];
   int SJ_nAK4_300[100], SJ_nAK4_50[100];
   double PU_eventWeight_nom, bTag_eventWeight_nom;
   double superJet_mass[100];
   double diSuperJet_mass;
   double average_bTagSF = 0;
   double average_PUSF   = 0;
   double total_events_unscaled = 0;
   const char *_inFilename = inFileName.c_str();
   int total_btags =0;
   std::cout << "Reading file: " << _inFilename << std::endl;

   TFile *f = TFile::Open(_inFilename);   //import filename and open file
   const char *_outFilename = outFileName.c_str();    //create the output file where the skimmed tree will be 

   std::cout << "The output file name is : " << _outFilename << std::endl;

   TFile outFile(_outFilename,"RECREATE");
   
   std::vector<std::string> systematic_suffices = {""};


   for(auto systematic_ = systematics.begin();systematic_ < systematics.end();systematic_++)
   {
      std::string systematic = *systematic_; 
      if(systematic == "nom") systematic_suffices = {""};
      else if(systematic == "") systematic_suffices = {""};
      else { systematic_suffices = {"up", "down"};}


      for(auto systematic_suffix = systematic_suffices.begin(); systematic_suffix < systematic_suffices.end();systematic_suffix++)
      {

         double nEvents =0,nHTcut =0 ,nAK8JetCut =0,nHeavyAK8Cut=0,nBtagCut=0,nSJEnergyCut=0, nSJMass100Cut=0;
         double nZeroBtag = 0, nZeroBtagnSJEnergyCut = 0, nZeroBtagnSJMass100Cut = 0;
         double nNoBTags = 0, nAT0b = 0, nAT1b = 0;
         std::cout << "Looking at the " << *systematic_suffix << " tree" << std::endl;


         //std::string treeName = ("clusteringAnalyzerAll_" + systematic+ "_" + *systematic_suffix+ "/tree_"+ systematic + "_" + *systematic_suffix).c_str();

         //std::cout << "Interpolated the tree name to be " << treeName  << std::endl;

         std::string tree_string;
         std::string new_tree_string;
         if( systematic == "nom")
         {
            tree_string = "nom";
            new_tree_string = "nom";
         } 
         else if( systematic == "") 
         {
            tree_string = "";
            new_tree_string = "";
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
         std::cout << "getting tree " << ("clusteringAnalyzerAll_" + tree_string + "/tree_"+ tree_string).c_str() << std::endl;
         TTree *t1 = (TTree*)f->Get( ("clusteringAnalyzerAll_" + tree_string + "/tree_"+ tree_string).c_str()   ); 

         outFile.cd();   // return to outer directory
         //gDirectory->mkdir( (systematic+"_"+ *systematic_suffix).c_str()  );   //create directory for this systematic
         gDirectory->mkdir( newTreeName.c_str()  );   //create directory for this systematic
         outFile.cd( newTreeName.c_str() );   // go inside the systematic directory 

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
         t1->SetBranchAddress("SJ_nAK4_300", SJ_nAK4_300);
         t1->SetBranchAddress("SJ_nAK4_50", SJ_nAK4_50);

         t1->SetBranchAddress("AK4_DeepJet_disc", AK4_DeepJet_disc); 

         t1->SetBranchAddress("bTag_eventWeight_nom", &bTag_eventWeight_nom); 
         t1->SetBranchAddress("PU_eventWeight_nom", &PU_eventWeight_nom); 


         t1->SetBranchAddress("superJet_mass", superJet_mass); 
         t1->SetBranchAddress("diSuperJet_mass", &diSuperJet_mass); 
         t1->SetBranchAddress("lab_AK4_pt", AK4_pt); 

         

         double looseDeepCSV_DeepJet;
         double medDeepCSV_DeepJet;
         double tightDeepCSV_DeepJet;

         if(year == "2015")
         {
            looseDeepCSV_DeepJet = 0.0508;
            medDeepCSV_DeepJet   = 0.2598;
            tightDeepCSV_DeepJet = 0.6502;  
         }
         else if(year == "2016")
         {
            looseDeepCSV_DeepJet =  0.0480;
            medDeepCSV_DeepJet   = 0.2489;
            tightDeepCSV_DeepJet = 0.6377; 
         }
         else if(year == "2017")
         {
            looseDeepCSV_DeepJet = 0.0532;
            medDeepCSV_DeepJet   = 0.3040;
            tightDeepCSV_DeepJet = 0.7476;
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

            t1->GetEntry(i);

            //// Keep only 10% of signal MC 
            int keep_var = (int)(1e8*AK4_DeepJet_disc[0]);         
            if ((dataBlock.find("Suu") != std::string::npos))
            {
               if( (keep_var % 10 !=1))continue;
            }
            eventWeight = 1.0;
            total_events_unscaled+=1;
            if ((dataBlock.find("MC") != std::string::npos) || (dataBlock.find("Suu") != std::string::npos))
            {
               if ((bTag_eventWeight_nom != bTag_eventWeight_nom) || (std::isinf(bTag_eventWeight_nom)))
               {
                  bTag_eventWeight_nom = 0.0;
                  std::cout << "ERROR: bad event weight due to bTag event weight." << std::endl;
               }
               if ((PU_eventWeight_nom != PU_eventWeight_nom) || (std::isinf(PU_eventWeight_nom)))
               {
                  PU_eventWeight_nom = 0.0;
                  std::cout << "ERROR: bad event weight due to PU weight." << std::endl;
               }
               eventWeight = PU_eventWeight_nom*bTag_eventWeight_nom;
               average_bTagSF+= bTag_eventWeight_nom;
               average_PUSF  += PU_eventWeight_nom;
               if(eventWeight < 1e-5)std::cout << "ERROR: bad event weight." << std::endl;
            }
            //std::cout <<"Count is "<<nEvents  << ", " << bTag_eventWeight_nom << "-" << PU_eventWeight_nom<< std::endl;
            eventWeight = 1;
            nEvents+=eventWeight;
            if (totHT < 1500.) continue; 
            nHTcut+=eventWeight;
            if( (nfatjets < 3)   ) continue;
            nAK8JetCut+=eventWeight;
            if ((nfatjet_pre < 2) && ( (dijetMassOne < 1000. ) || ( dijetMassTwo < 1000.)  ))continue;
            nHeavyAK8Cut+=eventWeight;

            int nTightBTags = 0;
            for(int iii = 0;iii< nAK4; iii++)
            {
               if ( (AK4_DeepJet_disc[iii] > tightDeepCSV_DeepJet ) && (AK4_pt[iii] > 30.) )
               {
                  total_btags++;
                  nTightBTags++;
               } 
            }
            if ( (nTightBTags > 0)  )
            {
               nBtagCut+=eventWeight;
               

               if((SJ_nAK4_300[0]>=2) && (SJ_nAK4_300[1]>=2)   )
               {
                  //signal region
                  nSJEnergyCut+=eventWeight;
                  if((SJ_mass_100[0]>=400.) && (SJ_mass_100[1]>400.)   )
                  {
                     nSJMass100Cut+=eventWeight;
                  }
               }

               // AT1b region
               if(   (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<150.)   )
               {
                  if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
                  {
                     //std::cout << "In the AT1b region: SJ mass/diSJ mass/nAK8/AK4/nBtags/eventweight are " << superJet_mass[1]<< "/" << diSuperJet_mass<< "/" << nfatjets << "/" << nAK4 << "/"<< nTightBTags << "/" << eventWeight <<  std::endl;
                     nAT1b+=eventWeight;
                  }
               }


            }
            if((nTightBTags < 1))
            {


               nZeroBtag+=eventWeight;

               //CR
               if((SJ_nAK4_300[0]>=2) && (SJ_nAK4_300[1]>=2)   )
               {
                  nZeroBtagnSJEnergyCut+=eventWeight;
               }

               //AT0b
               if(   (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<150.)   )
               {
                  if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
                  {
                     nAT0b+=eventWeight;
                  }
               }
               
            }
            t2->Fill();
         }
         outFile.Write();
         std::cout << "-------------   new systematic -------------" << std::endl;

         std::cout << "Signal  Region for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << ", "<<  year << " and " << tree_string << ": total/HTcut/AK8jetCut/heavyAK8JetCut/nBtagCut/nSJEnergyCut: - " <<nEvents << "-" << nHTcut << "-" << nAK8JetCut<< "-" << nHeavyAK8Cut<< "-" << nBtagCut << "-" << nSJEnergyCut << std::endl;
         std::cout << "Control Region for " << systematic+ "_" + *systematic_suffix << " " <<dataBlock << ", "<<  year << " and " << tree_string << ": total/HTcut/AK8jetCut/heavyAK8JetCut/nZeroBtag/nAT0b: - " <<nEvents << "-" << nHTcut << "-" << nAK8JetCut<< "-" << nHeavyAK8Cut<< "-" << nZeroBtag << "-" << nZeroBtagnSJEnergyCut << std::endl;
         std::cout << "AT1b    Region for " << systematic+ "_" + *systematic_suffix << " " <<dataBlock << ", "<<  year << " and " << tree_string << ": total/HTcut/AK8jetCut/heavyAK8JetCut/nBtagCut/nBtagCut: - "  <<nEvents << "-" << nHTcut << "-" << nAK8JetCut<< "-" << nHeavyAK8Cut<< "-" << nBtagCut << "-" << nAT1b << std::endl;
         std::cout << "AT0b    Region for " << systematic+ "_" + *systematic_suffix << " " <<dataBlock << ", "<<  year << " and " << tree_string << ": total/HTcut/AK8jetCut/heavyAK8JetCut/nZeroBtag/nAT1b: - " <<nEvents << "-" << nHTcut << "-" << nAK8JetCut<< "-" << nHeavyAK8Cut<< "-" << nZeroBtag << "-" << nAT0b << std::endl;

         std::cout << "There were a total of " << total_btags << " tight b-tagged jets in this sample." << std::endl; 
         std::cout << "The average bTagSF was " << average_bTagSF/total_events_unscaled << ", the average PUSF was " << average_PUSF/total_events_unscaled << std::endl; 
         std::cout << "WARNING: The btag SF is set to 1. Change this when not testing "  << std::endl;
      }

   }
   std::cout << "-------------   new sample -------------" << std::endl;

   outFile.Close();

}


void readTreeApplySelection()
{


   std::vector<std::string> signal_samples = {
"Suu4_chi1_HTHT_","Suu4_chi1p5_HTHT_","Suu5_chi1_HTHT_","Suu5_chi1p5_HTHT_","Suu5_chi2_HTHT_","Suu6_chi1_HTHT_","Suu6_chi1p5_HTHT_","Suu6_chi2_HTHT_","Suu6_chi2p5_HTHT_","Suu7_chi1_HTHT_","Suu7_chi1p5_HTHT_",
"Suu7_chi2_HTHT_","Suu7_chi2p5_HTHT_","Suu7_chi3_HTHT_","Suu8_chi1_HTHT_","Suu8_chi1p5_HTHT_","Suu8_chi2_HTHT_","Suu8_chi2p5_HTHT_","Suu8_chi3_HTHT_",
"Suu4_chi1_HTZT_","Suu4_chi1p5_HTZT_","Suu5_chi1_HTZT_","Suu5_chi1p5_HTZT_","Suu5_chi2_HTZT_","Suu6_chi1_HTZT_","Suu6_chi1p5_HTZT_","Suu6_chi2p5_HTZT_","Suu7_chi1_HTZT_",
"Suu7_chi1p5_HTZT_","Suu7_chi2_HTZT_","Suu7_chi2p5_HTZT_","Suu7_chi3_HTZT_","Suu8_chi1_HTZT_","Suu8_chi1p5_HTZT_","Suu8_chi2_HTZT_","Suu8_chi2p5_HTZT_","Suu8_chi3_HTZT_",
"Suu4_chi1_WBHT_","Suu4_chi1p5_WBHT_","Suu5_chi1_WBHT_","Suu5_chi1p5_WBHT_","Suu5_chi2_WBHT_","Suu6_chi1_WBHT_","Suu6_chi1p5_WBHT_","Suu6_chi2_WBHT_","Suu6_chi2p5_WBHT_",
"Suu7_chi1_WBHT_","Suu7_chi1p5_WBHT_","Suu7_chi2_WBHT_","Suu7_chi2p5_WBHT_","Suu7_chi3_WBHT_","Suu8_chi1_WBHT_","Suu8_chi1p5_WBHT_","Suu8_chi2_WBHT_","Suu8_chi2p5_WBHT_",
"Suu8_chi3_WBHT_","Suu4_chi1_WBWB_","Suu4_chi1p5_WBWB_","Suu5_chi1_WBWB_","Suu5_chi1p5_WBWB_","Suu5_chi2_WBWB_","Suu6_chi1_WBWB_","Suu6_chi1p5_WBWB_","Suu6_chi2_WBWB_",
"Suu6_chi2p5_WBWB_","Suu7_chi1_WBWB_","Suu7_chi1p5_WBWB_","Suu7_chi2_WBWB_","Suu7_chi2p5_WBWB_","Suu7_chi3_WBWB_","Suu8_chi1_WBWB_","Suu8_chi1p5_WBWB_","Suu8_chi2_WBWB_",
"Suu8_chi2p5_WBWB_","Suu8_chi3_WBWB_","Suu4_chi1_WBZT_","Suu4_chi1p5_WBZT_","Suu5_chi1_WBZT_","Suu5_chi1p5_WBZT_","Suu5_chi2_WBZT_","Suu6_chi1_WBZT_","Suu6_chi1p5_WBZT_",
"Suu6_chi2_WBZT_","Suu6_chi2p5_WBZT_","Suu7_chi1_WBZT_","Suu7_chi1p5_WBZT_","Suu7_chi2_WBZT_","Suu7_chi2p5_WBZT_","Suu7_chi3_WBZT_","Suu8_chi1_WBZT_","Suu8_chi1p5_WBZT_",
"Suu8_chi2_WBZT_","Suu8_chi2p5_WBZT_","Suu8_chi3_WBZT_","Suu4_chi1_ZTZT_","Suu4_chi1p5_ZTZT_","Suu5_chi1_ZTZT_","Suu5_chi1p5_ZTZT_","Suu5_chi2_ZTZT_","Suu6_chi1_ZTZT_",
"Suu6_chi1p5_ZTZT_","Suu6_chi2p5_ZTZT_","Suu7_chi1_ZTZT_","Suu7_chi1p5_ZTZT_","Suu7_chi2_ZTZT_","Suu7_chi2p5_ZTZT_","Suu7_chi3_ZTZT_","Suu8_chi1_ZTZT_","Suu8_chi1p5_ZTZT_",
"Suu8_chi2_ZTZT_","Suu8_chi2p5_ZTZT_"};  
   //std::vector<std::string> signal_samples = {"Suu8_chi2_WBZT_"};

   // you must change these ........
   bool runAll = false;
   bool runData = false;
   bool runSignal = false;
   std::vector<std::string> years = {"2017","2018"};//{"2015","2016","2017","2018"};    // for testing  "2015","2016","2017"
   std::vector<std::string> systematics = {"nom", "JEC", "JER"};//{"nom", "JEC","JER"};   // will eventually use this to skim the systematic files too
   int yearNum = 0;
   //need to have the event scale factors calculated for each year and dataset
   double eventScaleFactor = 1; 
   for(auto datayear = years.begin();datayear<years.end();datayear++)
   {
      std::vector<std::string> dataBlocks_non_sig; 
      std::vector<std::string> dataBlocks; 
      std::string skimmedFilePaths;

      if (runAll)
      {
         if(*datayear == "2015")
         {
            dataBlocks_non_sig = {"dataB-ver2_","dataC-HIPM_","dataD-HIPM_","dataE-HIPM_","dataF-HIPM_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"}; // dataB-ver1 not present
         }
         else if(*datayear == "2016")
         {
            dataBlocks_non_sig = {"dataF_", "dataG_", "dataH_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"};
         }
         else if(*datayear == "2017")
         {
            dataBlocks_non_sig = {"dataB_","dataC_","dataD_","dataE_", "dataF_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"};
         }
         else if(*datayear == "2018")
         {
            dataBlocks_non_sig = {"dataA_","dataB_","dataC_","dataD_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"};
         }    

         dataBlocks.reserve( dataBlocks_non_sig.size() + signal_samples.size() ); // preallocate memory
         dataBlocks.insert( dataBlocks.end(), dataBlocks_non_sig.begin(), dataBlocks_non_sig.end() );
         dataBlocks.insert( dataBlocks.end(), signal_samples.begin(), signal_samples.end() );

      }
      else if(runData)
      {
         //systematics = { "JEC"};  //TESTING

         if(*datayear == "2015")
         {
            dataBlocks = {"dataB-ver2_","dataC-HIPM_","dataD-HIPM_","dataE-HIPM_","dataF-HIPM_"}; // dataB-ver1 not present
         }
         else if(*datayear == "2016")
         {
            dataBlocks = {"dataF_", "dataG_", "dataH_"};
         }
         else if(*datayear == "2017")
         {
            dataBlocks = {"dataB_","dataC_","dataD_","dataE_", "dataF_"};
         }
         else if(*datayear == "2018")
         {
            dataBlocks = {"dataA_","dataB_","dataC_","dataD_"};
         }

      }
      else if (runSignal)
      {
         dataBlocks = signal_samples;
      }
      else
      {  
        //dataBlocks = {"TTToSemiLeptonic_"}; 
        dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"};
      }

      for(auto dataBlock = dataBlocks.begin();dataBlock < dataBlocks.end();dataBlock++)
      {

         std::vector<std::string> use_systematics;
         for( auto systematic = systematics.begin(); systematic < systematics.end();systematic++)
         {

            std::string year           = *datayear;
            std::string systematic_str = *systematic;
            std::string eos_path       = "root://cmsxrootd.fnal.gov//store/user/ecannaer/combinedROOT/";
            
            std::cout << "looking at sample/year/systematic:" << year<< "/" << *dataBlock<< "/" <<systematic_str << std::endl;

            std::string inFileName;
            std::string outFileName;
            if (dataBlock->find("Suu") != std::string::npos)  // all signal systematics are in a single file
            {
               if(*systematic != "nom") continue; // only need to run once for signal
               use_systematics = systematics;
               inFileName  = (eos_path + *dataBlock + year + "_combined.root").c_str();
               outFileName= (*dataBlock + year + "_SKIMMED.root").c_str();

            }
            else
            {  
               use_systematics = {*systematic};
               inFileName  = (eos_path + *dataBlock + year +  "_" + systematic_str + "_combined.root").c_str();
               outFileName= (*dataBlock + year + "_"+ systematic_str + "_SKIMMED.root").c_str();
            }

            if ((dataBlock->find("data") != std::string::npos) && (systematic_str == "JER")) continue;
            //if (runSignal) inFileName  = (eos_path+*dataBlock+  year +  "_" + systematic_str+ "_combined.root").c_str();

            std::cout << "Looking at file " << inFileName << "." << std::endl;
            try
            {
               doThings(inFileName,outFileName,eventScaleFactor,year, use_systematics,*dataBlock);
            }
            catch(...)
            {
               std::cout << "sample/year/systematic: " << year <<"/" << *dataBlock << "/" << systematic_str << " failed. Trying again with nom == ''" << std::endl;
               try
               {
                  use_systematics = {""};
                  doThings(inFileName,outFileName,eventScaleFactor,year, use_systematics,*dataBlock);
               }

               catch(...)
               {
                  std::cout << "-------- ERROR: Failed sample/year/systematic: " << year <<"/" << *dataBlock << "/" << systematic_str <<" --------" << std::endl;

                  continue;
               }
               
            }

            std::cout << "Finished with "<< inFileName << std::endl;

            yearNum++;
         }
      }
   }
}

