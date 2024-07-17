#include <iostream>
#include <string>
#include "TLorentzVector.h"

bool doThings(std::string inFileName, std::string outFileName, double &eventScaleFactors, std::string year, std::vector<std::string> systematics, std::string dataBlock, std::string runType)
{
   double totHT, dijetMassOne, dijetMassTwo;
   int nfatjets, nfatjet_pre,nAK4;
   double SJ_mass_100[100], AK4_pt[100],AK4_DeepJet_disc[100];
   int SJ_nAK4_300[100], SJ_nAK4_50[100], SJ_nAK4_100[100], SJ_nAK4_150[100];
   double PU_eventWeight_nom, bTag_eventWeight_T_nom = 1.0,bTag_eventWeight_M_nom = 1.0;
   double superJet_mass[100];
   double diSuperJet_mass;
   double average_bTagSF = 0;
   double average_PUSF   = 0;
   double total_events_unscaled = 0;
   double SJ_mass_200[10], SJ_mass_300[10];
   double AK8_partonFlavour[100];
   int AK4_hadronFlavour[100];
   int eventNumber;
   int AK8_SJ_assignment[100],AK4_SJ_assignment[100];
   bool AK8_is_near_highE_CA4[100],AK4_is_near_highE_CA4[100];
   int SJ1_decision, SJ2_decision;
   int totEventsUncut = 0;
   bool verbose = true;

   const char *_inFilename = inFileName.c_str();
   int total_btags =0;
   
   if(verbose)std::cout << "Opening file: " << _inFilename << std::endl;

   TFile *f = TFile::Open(_inFilename);   //import filename and open file

   if( (f == nullptr) || (f->IsZombie()) )
   {
      std::cout << "ERROR: Can't find file " << _inFilename << std::endl;
      return false;
   }
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

         double nEvents =0,nHTcut =0 ,nAK8JetCut =0,nHeavyAK8Cut=0,nBtagCut=0,nSJEnergyCut=0, nSJMass100Cut=0, nNN_tagged_SR =0 ;
         double nZeroBtag = 0, nZeroBtagnSJEnergyCut = 0, nZeroBtagnSJMass100Cut = 0, nNN_tagged_CR = 0;
         double nNoBTags = 0, nAT0b = 0, nAT1b = 0, nSR = 0, nCR = 0, nAT1b_noScale = 0, nAT0b_noScale = 0, nNN_tagged_AT1b = 0, nNN_tagged_AT0b = 0 ;
         std::cout << "Looking at the " << *systematic_suffix << " tree" << std::endl;
         int nBadEvents = 0;
         std::string tree_string;
         std::string new_tree_string;
         if( systematic == "nom")
         {
            tree_string = "nom";
            new_tree_string = "nom";
         } 
         else if( systematic == "") 
         {
            tree_string = "nom";
            new_tree_string = "nom";
         }
         else
         { 
            tree_string = ( systematic+ "_" + *systematic_suffix   ).c_str();
            new_tree_string = (systematic + "_" + *systematic_suffix).c_str();
         }


         std::string oldTreeName = ("clusteringAnalyzerAll_" + tree_string + "/tree_"+ tree_string).c_str();
         std::string newTreeName = ("skimmedTree_"+ new_tree_string ).c_str();
         std::string newTreeDirectory;

         if(( systematic == "nom") || (systematic == ""))
         {
           newTreeDirectory = "nom";
         }
         else
         {
            newTreeDirectory = systematic + "_" + *systematic_suffix; // Ex. JER + _ + up
         }
         
         if(verbose)std::cout << "looking for tree name: " << oldTreeName<< std::endl;
         if(verbose)std::cout << "naming new tree " << newTreeName << std::endl;

         outFile.cd();   // return to outer directory
         //gDirectory->mkdir( (systematic+"_"+ *systematic_suffix).c_str()  );   //create directory for this systematic
         gDirectory->mkdir( newTreeDirectory.c_str()  );   //create directory for this systematic
         outFile.cd( newTreeDirectory.c_str() );   // go inside the systematic directory 

         TTree *t1;
         TTree *t2;
         //try 
         //{
         t1 = (TTree*)f->Get( oldTreeName.c_str()   ); 
         if(t1 == nullptr)
         {
            std::cout << "ERROR: Tree " <<oldTreeName << " not found - skipping!!!. " << std::endl;
            return false;
         } 
         t2 = t1->CloneTree(0);
         std::cout << "Successfully found tree "<< oldTreeName << std::endl;

        // }
         /*
         catch(...)
         {
            std::cout << "Failed finding tree " << oldTreeName<< " for file " << inFileName << std::endl;
            return;
         } */

         t2->SetName(   newTreeName.c_str() );
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
         t1->SetBranchAddress("SJ_mass_200", SJ_mass_200);
         t1->SetBranchAddress("SJ_mass_300", SJ_mass_300);


         t1->SetBranchAddress("SJ_nAK4_300", SJ_nAK4_300);
         t1->SetBranchAddress("SJ_nAK4_100", SJ_nAK4_100);
         t1->SetBranchAddress("SJ_nAK4_150", SJ_nAK4_150);

         t1->SetBranchAddress("SJ1_decision", &SJ1_decision);
         t1->SetBranchAddress("SJ2_decision", &SJ2_decision);



         t1->SetBranchAddress("SJ_nAK4_50", SJ_nAK4_50);

         t1->SetBranchAddress("AK4_DeepJet_disc", AK4_DeepJet_disc); 


         if( !(inFileName.find("data") != std::string::npos))
         {
            t1->SetBranchAddress("bTag_eventWeight_T_nom", &bTag_eventWeight_T_nom); 
            t1->SetBranchAddress("bTag_eventWeight_M_nom", &bTag_eventWeight_M_nom); 
            t1->SetBranchAddress("PU_eventWeight_nom", &PU_eventWeight_nom); 
            t1->SetBranchAddress("AK4_hadronFlavour", AK4_hadronFlavour); 
            t1->SetBranchAddress("AK8_partonFlavour", AK8_partonFlavour); 
         }


         t1->SetBranchAddress("superJet_mass", superJet_mass); 
         t1->SetBranchAddress("diSuperJet_mass", &diSuperJet_mass); 
         t1->SetBranchAddress("lab_AK4_pt", AK4_pt); 

         t1->SetBranchAddress("AK8_SJ_assignment", AK8_SJ_assignment); 
         t1->SetBranchAddress("AK4_SJ_assignment", AK4_SJ_assignment); 
         t1->SetBranchAddress("AK8_is_near_highE_CA4", AK8_is_near_highE_CA4); 
         t1->SetBranchAddress("AK4_is_near_highE_CA4", AK4_is_near_highE_CA4); 


         t1->SetBranchAddress("eventNumber", &eventNumber); 

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

         int nAK4FoundNearHighECA4_light = 0, nAK4FoundNearHighECA4_c = 0, nAK4FoundNearHighECA4_b = 0;
         int nAK8FoundNearHighECA4_light = 0, nAK8FoundNearHighECA4_c = 0, nAK8FoundNearHighECA4_b = 0;

         int nAK4FoundInTaggedSJ_light = 0, nAK4FoundInTaggedSJ_c = 0, nAK4FoundInTaggedSJ_b = 0;
         int nAK8FoundInTaggedSJ_light = 0, nAK8FoundInTaggedSJ_c = 0, nAK8FoundInTaggedSJ_b = 0;

         int tot_nAK4_light = 0,  tot_nAK4_c = 0, tot_nAK4_b = 0;

         totEventsUncut = 0;
         for (Int_t i=0;i<nentries;i++) 
         {  



            t1->GetEntry(i);
            totEventsUncut++;
            if ((dataBlock.find("Suu") != std::string::npos))
            {
               if( eventNumber%10 > 2) continue; // should only be for signal
            }
            eventWeight = 1.0;
            total_events_unscaled+=1;
            if ((dataBlock.find("MC") != std::string::npos) || (dataBlock.find("Suu") != std::string::npos))
            {
               if ((bTag_eventWeight_T_nom != bTag_eventWeight_T_nom) || (std::isinf(bTag_eventWeight_T_nom)))
               {
                  bTag_eventWeight_T_nom = 1.0;
                  //std::cout << "ERROR: bad event weight due to bTag event weight." << std::endl;
                  nBadEvents++;
               }
               if ((PU_eventWeight_nom != PU_eventWeight_nom) || (std::isinf(PU_eventWeight_nom)))
               {
                  PU_eventWeight_nom = 1.0;
                  nBadEvents++;
                  //std::cout << "ERROR: bad event weight due to PU weight." << std::endl;
               }

               if ((bTag_eventWeight_M_nom != bTag_eventWeight_M_nom) || (std::isinf(bTag_eventWeight_M_nom)))
               {
                  bTag_eventWeight_M_nom = 1.0;
                  //std::cout << "ERROR: bad event weight due to bTag event weight." << std::endl;
                  nBadEvents++;
               }

               eventWeight = PU_eventWeight_nom;
               average_bTagSF+= bTag_eventWeight_T_nom;
               average_PUSF  += PU_eventWeight_nom;
               //if(eventWeight < 1e-5)std::cout << "ERROR: bad event weight." << std::endl;
            }

            nEvents+=eventWeight;
            if (runType == "main-band")
            {
               if (totHT < 1600.) continue; 
            }
            else if( runType == "side-band")
            {
               if ((totHT > 1600) || (totHT < 1200))continue;
            }
            nHTcut+=eventWeight;
            if( (nfatjets < 3)   ) continue;
            nAK8JetCut+=eventWeight;
            if ((nfatjet_pre < 2) && ( (dijetMassOne < 1000. ) || ( dijetMassTwo < 1000.)  ))continue;
            nHeavyAK8Cut+=eventWeight;

            int nTightBTags = 0, nMedBTags = 0;
            for(int iii = 0;iii< nAK4; iii++)
            {
               if ( (AK4_DeepJet_disc[iii] > tightDeepCSV_DeepJet ) && (AK4_pt[iii] > 30.) )
               {
                  total_btags++;
                  nTightBTags++;
               } 


               if ( (AK4_DeepJet_disc[iii] > medDeepCSV_DeepJet ) && (AK4_pt[iii] > 30.) )
               {
                  nMedBTags++;
               } 
               if( AK4_hadronFlavour[iii] == 0  )
               {
                  tot_nAK4_light++;
                  if(AK4_is_near_highE_CA4[iii])nAK4FoundNearHighECA4_light++;
               }
               else if( AK4_hadronFlavour[iii] == 4  )
               {
                  tot_nAK4_c++;
                  if(AK4_is_near_highE_CA4[iii])nAK4FoundNearHighECA4_c++;
               }
               else if(  AK4_hadronFlavour[iii] == 5)
               {
                  tot_nAK4_b++;
                  if(AK4_is_near_highE_CA4[iii])nAK4FoundNearHighECA4_b++;
               }

               if((SJ_nAK4_300[0] > 1) &&(AK4_SJ_assignment[iii] == 0))
               {
                  if(AK4_hadronFlavour[iii] == 0)nAK4FoundInTaggedSJ_light++;
                  else if(AK4_hadronFlavour[iii] == 4)nAK4FoundInTaggedSJ_c++;
                  else if(AK4_hadronFlavour[iii] == 5)nAK4FoundInTaggedSJ_b++;
                  
                     
               }
               if((SJ_nAK4_300[1] > 1) && (AK4_SJ_assignment[iii] == 1))
               {
                  if(AK4_hadronFlavour[iii] == 0)nAK4FoundInTaggedSJ_light++;
                  else if(AK4_hadronFlavour[iii] == 4)nAK4FoundInTaggedSJ_c++;
                  else if(AK4_hadronFlavour[iii] == 5)nAK4FoundInTaggedSJ_b++;
               }

            }
            if ( (nTightBTags > 0)  )
            {


               eventWeight*= bTag_eventWeight_T_nom;

               nBtagCut+=eventWeight;

               ////////////////////// CUTBASED ///////////////////////
               // Signal region
               if( ( (SJ_nAK4_300[0]>=2) && (SJ_nAK4_300[1]>=2) ) )     //|| (  ( (SJ_nAK4_150[0] + SJ_nAK4_150[1]) > 4) && (SJ_mass_200[0]> 500) && (SJ_mass_200[1]> 500) )  )  // alternative cut to improve 1 TeV efficiency ->   // || ( (SJ_mass_200[0]> 400) && (SJ_mass_200[1]> 400)  ) 
               {
                  nSR++;
                  nSJEnergyCut+=eventWeight;
                  if(((SJ_mass_100[0]>=400.) && (SJ_mass_100[1]>400.))   )
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
                     nAT1b_noScale++;
                  }
               }
               ///////////////////////// NN-based //////////////////////// 
               // NN signal region
               if ((SJ1_decision == 0) &&(SJ2_decision == 0))
               {
                  nNN_tagged_SR+= eventWeight;
               }
               // NN AT1b region
               if (  (SJ1_decision != 0)&&( SJ2_decision == 0)    )
               {
                  nNN_tagged_AT1b+=eventWeight;
               }
            }
            else if((nMedBTags < 1))
            {

               eventWeight*= bTag_eventWeight_M_nom;

               nZeroBtag+=eventWeight;
               //CR
               if( (SJ_nAK4_300[0]>=2) && (SJ_nAK4_300[1]>=2)   )
               {
                  nCR++;
                  nZeroBtagnSJEnergyCut+=eventWeight;
               }
               //AT0b
               if(   (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<150.)   )
               {
                  if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
                  {
                     nAT0b+=eventWeight;
                     nAT0b_noScale++;

                  }
               }
               ///////////////////////// NN-based //////////////////////// 

               // NN control region
               if ((SJ1_decision == 0) && (SJ2_decision == 0))
               {
                  nNN_tagged_CR+=eventWeight;
               }
               // NN AT0b region
               if (  (SJ1_decision != 0)&&( SJ2_decision == 0)    )
               {
                  nNN_tagged_AT0b+=eventWeight;
               }


               
            }
            t2->Fill();
         }
         outFile.Write();

         std::cout << "--------------------------------------   new systematic --------------------------------------" << std::endl;

         std::cout << "Signal  Region for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << ", "<<  year << " and " << tree_string << ": total/HTcut/AK8jetCut/heavyAK8JetCut/nBtagCut/nSJEnergyCut: - " <<nEvents << "-" << nHTcut << "-" << nAK8JetCut<< "-" << nHeavyAK8Cut<< "-" << nBtagCut << "-" << nSJEnergyCut << std::endl;
         std::cout << "Control Region for " << systematic+ "_" + *systematic_suffix << " " <<dataBlock << ", "<<  year << " and " << tree_string << ": total/HTcut/AK8jetCut/heavyAK8JetCut/nZeroBtag/nAT0b: - " <<nEvents << "-" << nHTcut << "-" << nAK8JetCut<< "-" << nHeavyAK8Cut<< "-" << nZeroBtag << "-" << nZeroBtagnSJEnergyCut << std::endl;
         std::cout << "AT1b    Region for " << systematic+ "_" + *systematic_suffix << " " <<dataBlock << ", "<<  year << " and " << tree_string << ": total/HTcut/AK8jetCut/heavyAK8JetCut/nBtagCut/nBtagCut: - "  <<nEvents << "-" << nHTcut << "-" << nAK8JetCut<< "-" << nHeavyAK8Cut<< "-" << nBtagCut << "-" << nAT1b << std::endl;
         std::cout << "AT0b    Region for " << systematic+ "_" + *systematic_suffix << " " <<dataBlock << ", "<<  year << " and " << tree_string << ": total/HTcut/AK8jetCut/heavyAK8JetCut/nZeroBtag/nAT1b: - " <<nEvents << "-" << nHTcut << "-" << nAK8JetCut<< "-" << nHeavyAK8Cut<< "-" << nZeroBtag << "-" << nAT0b << std::endl;

         std::cout << "NN_SR for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << ", "<<  year << " and " << tree_string << " " <<  nNN_tagged_SR << std::endl;
         std::cout << "NN_CR for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << ", "<<  year << " and " << tree_string << " " << nNN_tagged_CR << std::endl;
         std::cout << "NN_AT1b for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << ", "<<  year << " and " << tree_string << " " <<  nNN_tagged_AT1b << std::endl;
         std::cout << "NN_AT0b for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << ", "<<  year << " and " << tree_string <<  " " << nNN_tagged_AT0b << std::endl;

         //std::cout << "There were a total of " << total_btags << " tight b-tagged jets in this sample." << std::endl; 
         //std::cout << "The average bTagSF was " << average_bTagSF/total_events_unscaled << ", the average PUSF was " << average_PUSF/total_events_unscaled << std::endl; 
         //std::cout << "WARNING: The btag SF is set to 1. Change this when not testing "  << std::endl;

         std::cout << "TotalEvents/TotalPassed: Signal  Region for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << " "<<  year << " " << totEventsUncut << "/" << nSR << std::endl;
         std::cout << "TotalEvents/TotalPassed: Control Region for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << " "<<  year << " " << totEventsUncut << "/"<< nCR  <<std::endl;
         std::cout << "TotalEvents/TotalPassed: AT1b    Region for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << " "<<  year << " " << totEventsUncut << "/"<< nAT1b_noScale <<std::endl;
         std::cout << "TotalEvents/TotalPassed: AT0b    Region for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << " "<<  year << " " << totEventsUncut << "/"<< nAT0b_noScale <<std::endl;

         std::cout << "Number of bad events (due to b-tagging and PU): " << nBadEvents << std::endl;
         std::cout << "------------- b tagging flavour stuff ------------" << std::endl;
         std::cout << "rate at which light/c/b AK4 jets are found near high-energy reclustered CA4 jets: " << (1.0*nAK4FoundNearHighECA4_light)/tot_nAK4_light<< "/" << (1.0*nAK4FoundNearHighECA4_c)/tot_nAK4_c<< "/" << (1.0*nAK4FoundNearHighECA4_b)/tot_nAK4_b<< std::endl;
         std::cout << "rate at which light/c/b AK4 jets are inside tagged superjets: " << ( 1.0*nAK4FoundInTaggedSJ_light)/tot_nAK4_light << "/" << ( 1.0*nAK4FoundInTaggedSJ_c)/tot_nAK4_c << "/" << (1.0*nAK4FoundInTaggedSJ_b)/tot_nAK4_b<< std::endl;

      }

   }
   f->Close();
   outFile.Close();
   delete f;
   return true;

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
   std::string eos_path       = "root://cmsxrootd.fnal.gov//store/user/ecannaer/combinedROOT/";
   std:string runType = "main-band";
   // you must change these ........
   bool runAll = false;
   bool runData = false;
   bool runSignal = false;
   bool runDataBR = true;
   bool runTTbar  = false;
   bool runSelection = false;
   bool runSingleFile = false;
   bool runExtras    = false;
   bool runSideband = false;
   std::vector<std::string> years = {"2015","2016","2017","2018"};  
   std::vector<std::string> systematics = {"nom", "JEC", "JER",  };//{"nom", "JEC","JER"};   // will eventually use this to skim the systematic files too
   int yearNum = 0;
   int nFailedFiles = 0;
   std::string failedFiles = "";

   //need to have the event scale factors calculated for each year and dataset
   double eventScaleFactor = 1; 

   if (runSelection) years = {"2015"};  // single year to run over 

   if(runSingleFile)
   {

      std::string pathToFile = eos_path;

      std::string year_ = "2017";
      std::vector<std::string> use_systematic_ = {"nom"};
      std::string dataBlock_ = "QCDMC1000to1500_";

      std::string systematic_str_  = "_nom";
      std::string inFileName_ = (pathToFile + dataBlock_ + year_ +  systematic_str_ + "_combined.root").c_str();
      std::string outFileName_ = (dataBlock_ + year_ +  systematic_str_ + "_SKIMMED.root").c_str();

      doThings(inFileName_, outFileName_, eventScaleFactor, year_, use_systematic_, dataBlock_, runType);
      return;
   }




   for(auto datayear = years.begin();datayear<years.end();datayear++)
   {
      std::vector<std::string> dataBlocks_non_sig; 
      std::vector<std::string> dataBlocks; 
      std::string skimmedFilePaths;
      if (runAll)
      {
         if(*datayear == "2015")
         {
            dataBlocks_non_sig = {"dataB-ver2_","dataC-HIPM_","dataD-HIPM_","dataE-HIPM_","dataF-HIPM_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_", "TTToHadronicMC_","TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_", "ZZ_MC_", "WW_MC_"}; // dataB-ver1 not present
         }
         else if(*datayear == "2016")
         {
            dataBlocks_non_sig = {"dataF_", "dataG_", "dataH_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_", "TTToHadronicMC_","TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_","ZZ_MC_", "WW_MC_"};
         }
         else if(*datayear == "2017")
         {
            dataBlocks_non_sig = {"dataB_","dataC_","dataD_","dataE_", "dataF_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_","ZZ_MC_", "WW_MC_"};
         }
         else if(*datayear == "2018")
         {
            dataBlocks_non_sig = {"dataA_","dataB_","dataC_","dataD_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_","ZZ_MC_", "WW_MC_"};
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
      else if (runDataBR)
      {
         std::cout << "Running data & BR MC." << std::endl;
         if(*datayear == "2015")
         {
            dataBlocks = {"dataB-ver2_","dataC-HIPM_","dataD-HIPM_","dataE-HIPM_","dataF-HIPM_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_", "TTToHadronicMC_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_","ZZ_MC_", "WW_MC_"}; // dataB-ver1 not present
         }
         else if(*datayear == "2016")
         {
            dataBlocks = {"dataF_", "dataG_", "dataH_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_", "TTToHadronicMC_","TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_","ZZ_MC_", "WW_MC_"};
         }
         else if(*datayear == "2017")
         {
            dataBlocks = {"dataB_","dataC_","dataD_","dataE_", "dataF_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_","ZZ_MC_", "WW_MC_"};
         }
         else if(*datayear == "2018")
         {
            dataBlocks = {"dataA_","dataB_","dataC_","dataD_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_","ZZ_MC_", "WW_MC_"};
         }   
         else{std::cout << "ERROR: incorrect year. "; return;} 
      }
      else if(runTTbar)
      {
         dataBlocks = {"TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_", "TTToLeptonicMC_", "TTToHadronicMC_",};
      }
      else if(runSelection)
      {
         std::cout << "Running a selection of samples" << std::endl;
         dataBlocks = {"ZZ_MC_", "WW_MC_"};  
      }
      else if(runExtras)
      {
         std::cout << "Running WJets and extra TTJets datasets. " << std::endl;
         dataBlocks = {   "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_",  "TTJetsMCHT800to1200_"};
      }
      else if(runSideband)
      {

         std::cout << "Running side-band region." << std::endl;

          std::vector<std::string> dataBlocks_non_sig = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_" };
      


         if(*datayear == "2015")
         {
            dataBlocks_non_sig = {"dataB-ver2_","dataC-HIPM_","dataD-HIPM_","dataE-HIPM_","dataF-HIPM_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_", "WW_MC_","ZZ_MC_" }; // dataB-ver1 not present
         }
         else if(*datayear == "2016")
         {
            dataBlocks_non_sig = {"dataF_", "dataG_", "dataH_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_", "WW_MC_","ZZ_MC_" };
         }
         else if(*datayear == "2017")
         {
            dataBlocks_non_sig = {"dataB_","dataC_","dataD_","dataE_", "dataF_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_", "WW_MC_","ZZ_MC_" };
         }
         else if(*datayear == "2018")
         {
            dataBlocks_non_sig = {"dataA_","dataB_","dataC_","dataD_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_", "WW_MC_","ZZ_MC_" };
         }    

         dataBlocks.reserve( dataBlocks_non_sig.size() + signal_samples.size() ); // preallocate memory
         dataBlocks.insert( dataBlocks.end(), dataBlocks_non_sig.begin(), dataBlocks_non_sig.end() );
         dataBlocks.insert( dataBlocks.end(), signal_samples.begin(), signal_samples.end() );


         runType = "side-band";

         eos_path       = "root://cmsxrootd.fnal.gov//store/user/ecannaer/sideband_combinedROOT/";

      } 
      else
      {  
        dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToSemiLeptonicMC_", "TTToLeptonicMC_", "TTToHadronicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_","ZZ_MC_", "WW_MC_"};
      }
      for(auto dataBlock = dataBlocks.begin();dataBlock < dataBlocks.end();dataBlock++)
      {

         bool JEC_has_been_opened = false;
         std::vector<std::string> use_systematics;
         for( auto systematic = systematics.begin(); systematic < systematics.end();systematic++)
         {

            if(( dataBlock->find("data") != std::string::npos  ) && (systematic->find("JER") != std::string::npos)) continue; // there are no JER files for data
            std::string year           = *datayear;
            std::string systematic_str = *systematic;

            std::string inFileName;
            std::string outFileName;

            std::cout << year << " " << systematic_str << " " << *dataBlock << std::endl; 

            if (dataBlock->find("Suu") != std::string::npos)  // all signal systematics are in a single file
            {
               if(*systematic != "nom") continue; // only need to run once for signal
               std::cout << "Running as signal." << std::endl;
               std::cout << "looking at sample/year/systematic:" << year<< "/" << *dataBlock<< "/" <<systematic_str << std::endl;
               use_systematics = {"nom","JER_eta193", "JER_193eta25", "JER","JEC_FlavorQCD", "JEC_RelativeBal", "JEC_HF", "JEC_BBEC1", "JEC_EC2", "JEC_Absolute", "JEC_BBEC1_year", "JEC_EC2_year", "JEC_Absolute_year", "JEC_HF_year", "JEC_RelativeSample_year","JEC"};
               inFileName  = (eos_path + *dataBlock + year +"_"+ systematic_str + "_combined.root").c_str();
               outFileName= (*dataBlock + year + "_SKIMMED.root").c_str();
            }
            else if (*systematic == "JEC")  // JEC systematics comprise a large amount of sub-systematics 
            {
               std::cout << "Running JEC uncertainties." << std::endl;
               std::cout << "looking at sample/year/systematic:" << year<< "/" << *dataBlock<< "/" <<systematic_str << std::endl;
               use_systematics = { "JEC_FlavorQCD", "JEC_RelativeBal", "JEC_HF", "JEC_BBEC1", "JEC_EC2", "JEC_Absolute", "JEC_BBEC1_year", "JEC_EC2_year", "JEC_Absolute_year", "JEC_HF_year", "JEC_RelativeSample_year","JEC"};    // should be list of all JEC uncertainties 
               inFileName  = (eos_path + *dataBlock + year +"_JEC_combined.root").c_str();   // all JEC systematics will be in the JEC_combined.root file
               // if the JEC file has not yet been opened, delete the file so that it is being started from fresh 
               outFileName= (*dataBlock + year + "_JEC_SKIMMED.root").c_str();

            }  
            else if ( (*systematic == "JER") && !(dataBlock->find("data") != std::string::npos))  // JEC systematics comprise a large amount of sub-systematics 
            {
               std::cout << "Running JER uncertainties." << std::endl;
               std::cout << "looking at sample/year/systematic:" << year<< "/" << *dataBlock<< "/" <<systematic_str << std::endl;
               use_systematics = {"JER_eta193", "JER_193eta25", "JER"};    // should be list of all JEC uncertainties 
               inFileName  = (eos_path + *dataBlock + year +"_JER_combined.root").c_str();   // all JEC systematics will be in the JEC_combined.root file
               // if the JEC file has not yet been opened, delete the file so that it is being started from fresh 
               outFileName= (*dataBlock + year + "_JER_SKIMMED.root").c_str();

            } 
            else  // should trigger for all other uncertainties (which are under the nom uncertainty and are skimmed the same as the nom uncertainty)
            {  
               std::cout << "looking at sample/year/systematic:" << year<< "/" << *dataBlock<< "/" <<systematic_str << std::endl;
               std::string output_dir = "";
               use_systematics = {*systematic};
               inFileName  = (eos_path + *dataBlock + year +  "_" + systematic_str + "_combined.root").c_str();
               outFileName= (output_dir+ *dataBlock + year + "_"+ systematic_str + "_SKIMMED.root").c_str();
            }
            //if (runSignal) inFileName  = (eos_path+*dataBlock+  year +  "_" + systematic_str+ "_combined.root").c_str();

            std::cout << "======================================================================================================================= " << std::endl;
            std::cout << "======================================================================================================================= " << std::endl;
            std::cout << "             Reading file " << inFileName << "." << std::endl;
            std::cout << "======================================================================================================================= " << std::endl;
            std::cout << "======================================================================================================================= " << std::endl;

            if (!doThings(inFileName, outFileName, eventScaleFactor, year, use_systematics, *dataBlock, runType))
            {
               failedFiles+= (", "+ *dataBlock +"/" + year +"/"  + systematic_str ).c_str();
               nFailedFiles++;
            }
            else
            {
               std::cout << "Moving file " << outFileName << " to " << "root://cmseos.fnal.gov//store/user/ecannaer/skimmedFiles/" << std::endl;
               int delete_result = 1;
               std::cout << "The directory looks like this: " << std::endl;
               delete_result *= system( "ls -ltrh") ;

               delete_result *= system( ("source  /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/scp_file.sh " + outFileName + " root://cmseos.fnal.gov//store/user/ecannaer/skimmedFiles/").c_str() ) ;
               delete_result *= system( ("rm  /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/" + outFileName ).c_str() ) ;


            }
            
            std::cout << "Finished with "<< inFileName << std::endl;
            std:: cout << std::endl;
            std:: cout << std::endl;
            std:: cout << std::endl;
            std:: cout << std::endl;

            std::cout << " @@@@@@@@ There have been " << nFailedFiles << " failed jobs files @@@@@@@@" << std::endl;
            std::cout << "Failed files: " << failedFiles << std::endl;


            yearNum++;
         }
      }
   }
}

