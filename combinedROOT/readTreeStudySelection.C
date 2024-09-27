#include <iostream>
#include <string>
#include "TLorentzVector.h"
#include <cstdlib>
// check out the SJ mass ratio, this might be really weird for TTbar and could be used to kill some of this


using namespace std;
bool doThings(std::string inFileName, std::string outFileName, double eventScaleFactor, std::string dataYear,std::string systematic, std::string dataBlock, std::string runType)
{


   TH1::SetDefaultSumw2();
   TH2::SetDefaultSumw2();
   double jet_pt[100], jet_eta[100], jet_mass[100], jet_dr[100], raw_jet_mass[100],raw_jet_pt[100],raw_jet_phi[100];
   double AK4_mass_20[100],AK4_mass_30[100],AK4_mass_50[100],AK4_mass_70[100],AK4_mass_100[100],SJ_mass_150[100],SJ_mass_600[100],SJ_mass_800[100],SJ_mass_1000[100];
   double SJ_mass_50[100], SJ_mass_70[100],superJet_mass[100],SJ_AK4_50_mass[100],SJ_AK4_70_mass[100];
   int nSuperJets;
   int jet_ndaughters[100], jet_nAK4[100],jet_nAK4_20[100],jet_nAK4_30[100],jet_nAK4_50[100],jet_nAK4_70[100],SJ_nAK4_150[100],jet_nAK4_150[100],SJ_nAK4_200[100],SJ_nAK4_400[100],SJ_nAK4_600[100],SJ_nAK4_800[100],SJ_nAK4_1000[100];
   int ntotalevents = 0;
   int nAK4;
   double AK4_mass[100];
   double SJ_mass_100[100],AK4_E[500];
   int SJ_nAK4_100[100];
   double totHT = 0;
   int SJ_nAK4_300[100];
   int nfatjet_pre, nfatjets;
   double SJ_mass_300[100],AK4_phi[100];
   double AK4_DeepJet_disc[100];
   double AK4_pt[100];

   double dijetMassOne, dijetMassTwo;
   double AK4_eta[100];
   double bTag_eventWeight_T, bTag_eventWeight_M = 1.0,PU_eventWeight = 1.0;
   bool AK4_fails_veto_map[100], AK8_fails_veto_map[100];

   double prefiringWeight = 1;
   double pdf_weight = 1.0,factWeight=1.0, renormWeight = 1.0, scale_weight = 1.0,topPtWeight=1.0;
   std::vector<std::string> systematic_suffices;



   int total_1b = 0, total_0b = 0;

   int totEventsUncut;

   double SJ1_BEST_scores[50], SJ2_BEST_scores[50];
   int SJ1_decision, SJ2_decision;


   if(systematic == "nom")
   {
      // want to run only once with the 
      systematic_suffices = {""};

   }
   else if( systematic == "topPt")
   {
       systematic_suffices = {"up"};
   }
   else
   {
      systematic_suffices = {"up","down"};
   }


   const char *_inFilename = inFileName.c_str();
   const char *_outFilename = outFileName.c_str();

   std::cout << "---------  Reading file: " << _inFilename << std::endl;

   TFile *f = TFile::Open(_inFilename);

   if ((f == nullptr)||(f->IsZombie()) )
   {
      std::cout << "ERROR: File " << _inFilename << " not found - skipping !!" << std::endl;
      delete f;
      return false;
   }
   TFile outFile(_outFilename,"UPDATE");


   std::cout << "----------------------------------------------------- " << std::endl;
   std::cout << "----------------------------------------------------- " << std::endl;
   std::cout << "----------------------------------------------------- " << std::endl;
   std::cout << "----------------------------------------------------- " << std::endl;
   std::cout << " ---- WARNING: All corrections set to 1 ------" << std::endl; 
   std::cout << "----------------------------------------------------- " << std::endl;
   std::cout << "----------------------------------------------------- " << std::endl;
   std::cout << "----------------------------------------------------- " << std::endl;
   std::cout << "----------------------------------------------------- " << std::endl;

   for(auto systematic_suffix = systematic_suffices.begin(); systematic_suffix < systematic_suffices.end();systematic_suffix++)
   {

   
      std::string tree_string;
      if( systematic == "nom")
      {
         tree_string = "nom";
      } 
      else if( systematic == "") 
      {
         tree_string = "nom";
      }
      else
      { 
         tree_string = ( systematic+ "_" + *systematic_suffix   ).c_str();
      }


      std::string oldTreeName = ("selectionStudier_" + tree_string + "/tree_"+ tree_string).c_str();

      TTree *t1;
      Int_t nentries;

      try
      {  
         t1 = (TTree*)f->Get(  oldTreeName.c_str()    );
         if(t1 == nullptr)
         {
            std::cout << "ERROR: tree not found - " << oldTreeName  <<std::endl;
            delete f;
            return false;
         }
         nentries = t1->GetEntries();
      
      }
      
      catch(...)
      {
         std::cout << "ERROR: tree not found - " << oldTreeName  <<std::endl;
         delete f;
         return false;
      }
      std::cout << "Successfully got tree." << std::endl;
      

      //////////////////////////////////////////////////
      /////////// kinematics and diagnostics ///////////
      //////////////////////////////////////////////////

      TH1F* h_totHT  = new TH1F("h_totHT","Total Event HT;H_{T} [GeV]; Events / 200 GeV",50,0.,10000);
      TH1I* h_nfatjets_pre  = new TH1I("h_nfatjets_pre","Number of AK8 Jets (p_{T} > 500 GeV, M_{PUPPI} > 45 GeV) per Event ;nAK8 Jets; Events",10,-0.5,9.5);
      TH1I* h_nfatjets = new TH1I("h_nfatjets","Number of AK8 Jets (E_{T} > 300 GeV per Event ;nAK8 Jets; Events",10,-0.5,9.5);




   ////////////////////////////////////////////////////////////////////////////////////////////////////////

      t1->SetBranchAddress("nfatjets", &nfatjets);   

      t1->SetBranchAddress("nfatjet_pre", &nfatjet_pre); 
      t1->SetBranchAddress("jet_pt", jet_pt);   
      t1->SetBranchAddress("jet_eta", jet_eta);   
      t1->SetBranchAddress("jet_mass", jet_mass);   

      t1->SetBranchAddress("totHT", &totHT);
      t1->SetBranchAddress("nAK4" , &nAK4); 
      t1->SetBranchAddress("AK4_eta", AK4_eta); 
      t1->SetBranchAddress("AK4_phi", AK4_phi); 

      t1->SetBranchAddress("AK4_mass", AK4_mass); 

      t1->SetBranchAddress("lab_AK4_pt", AK4_pt); 

      t1->SetBranchAddress("dijetMassOne", &dijetMassOne); 
      t1->SetBranchAddress("dijetMassTwo", &dijetMassTwo); 
      
      t1->SetBranchAddress("AK4_fails_veto_map", AK4_fails_veto_map); 
      t1->SetBranchAddress("AK8_fails_veto_map", AK8_fails_veto_map); 

      // nominal systematics
      t1->SetBranchAddress("bTag_eventWeight_T_nom", &bTag_eventWeight_T);
      t1->SetBranchAddress("bTag_eventWeight_M_nom", &bTag_eventWeight_M);

      t1->SetBranchAddress("PU_eventWeight_nom", &PU_eventWeight);
      t1->SetBranchAddress("prefiringWeight_nom", &prefiringWeight);

      pdf_weight = 1.0; 
      scale_weight = 1.0; 
      renormWeight = 1.0;
      factWeight   = 1.0;
      topPtWeight = 1.0;

      
      double looseDeepCSV_DeepJet;
      double medDeepCSV_DeepJet;
      double tightDeepCSV_DeepJet;

      if(dataYear == "2015")
      {
         looseDeepCSV_DeepJet = 0.0508;
         medDeepCSV_DeepJet   = 0.2598;
         tightDeepCSV_DeepJet = 0.6502;  
      }
      else if(dataYear == "2016")
      {
         looseDeepCSV_DeepJet =  0.0480;
         medDeepCSV_DeepJet   = 0.2489;
         tightDeepCSV_DeepJet = 0.6377; 
      }
      else if(dataYear == "2017")
      {
         looseDeepCSV_DeepJet = 0.0532;
         medDeepCSV_DeepJet   = 0.3040;
         tightDeepCSV_DeepJet = 0.7476;
      }
      else if(dataYear == "2018")
      {
         looseDeepCSV_DeepJet = 0.0490;
         medDeepCSV_DeepJet   = 0.2783;
         tightDeepCSV_DeepJet = 0.7100;
      }


      int num_bad_btagSF = 0, num_bad_PUSF = 0, num_bad_topPt = 0, num_bad_scale = 0, num_bad_pdf = 0, num_bad_prefiring = 0;
      int badEventSF = 0;

      totEventsUncut = nentries;


      for (Int_t i=0;i<nentries;i++) 
      {  

         t1->GetEntry(i);
         
         prefiringWeight = 1.0;

         // check to make sure none of the AK4 or AK8 jets are in the veto region
         bool fails_veto_map = false;
         for(int iii=0;iii<nfatjets;iii++)
         {
            if (AK8_fails_veto_map[iii]) fails_veto_map = true;
         }
         for(int iii = 0;iii<nAK4;iii++)
         {
            if (AK4_fails_veto_map[iii]) fails_veto_map = true;
         }

         //if(fails_veto_map)continue;


         eventScaleFactor = 1.0;


         if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos)  )
         {

            ////// check MC systematics
            if ((bTag_eventWeight_T != bTag_eventWeight_T) || (std::isinf(bTag_eventWeight_T)) || (std::isnan(bTag_eventWeight_T)) || (abs(bTag_eventWeight_T) > 100) || (abs(bTag_eventWeight_T) < 0.001)  )
            {
               bTag_eventWeight_T = 1.0;
               num_bad_btagSF++;
            }

            ////// check MC systematics
            if ((bTag_eventWeight_M != bTag_eventWeight_M) || (std::isinf(bTag_eventWeight_M)) || (std::isnan(bTag_eventWeight_M)) || (abs(bTag_eventWeight_M) > 100) || (abs(bTag_eventWeight_M) < 0.001)  )
            {
               bTag_eventWeight_M = 1.0;
               num_bad_btagSF++;
            }

            if ((PU_eventWeight != PU_eventWeight) || (std::isinf(PU_eventWeight))|| (std::isnan(PU_eventWeight)) || (abs(PU_eventWeight) > 100) || (abs(PU_eventWeight) < 0.001)   )
            {
               PU_eventWeight = 1.0;
               num_bad_PUSF++;
            }

            if ((factWeight != factWeight) || (std::isinf(factWeight))  || (std::isnan(factWeight)) || (abs(factWeight) > 100) || (abs(factWeight) < 0.001) )
            {
               factWeight = 1.0;
              // num_bad_scale++;
               //std::cout << "BAD factorization weight during " << systematic << "_" << *systematic_suffix << ": " << factWeight << std::endl;
            }

            if ((renormWeight != renormWeight) || (std::isinf(renormWeight))  || (std::isnan(renormWeight)) || (abs(renormWeight) > 100) || (abs(renormWeight) < 0.001))
            {
               renormWeight = 1.0;
              //std::cout << "BAD renormalization weight during " << systematic << "_" << *systematic_suffix << ": " << renormWeight << std::endl;
            }

            scale_weight = renormWeight*factWeight;  

            if ((topPtWeight != topPtWeight) || (std::isinf(topPtWeight)) || (std::isnan(topPtWeight)) || (abs(topPtWeight) > 100) || (abs(topPtWeight) < 0.001))
            {
               topPtWeight = 1.0;
               num_bad_topPt++;
            }
            

            if ((pdf_weight != pdf_weight) || (std::isinf(pdf_weight)) || (std::isnan(pdf_weight)) || (abs(pdf_weight) > 100) || (abs(pdf_weight) < 0.001)  )
            {
               pdf_weight = 1.0;
               num_bad_pdf++;
            }
 
            eventScaleFactor = PU_eventWeight*pdf_weight*topPtWeight*factWeight*renormWeight*bTag_eventWeight_T;   /// these are all MC-only systematics
            
         }  


         ////// check data systematics
         if ((prefiringWeight != prefiringWeight) || (std::isinf(prefiringWeight)))
         {
            prefiringWeight = 1.0;
            num_bad_prefiring++;
         }

         eventScaleFactor *= prefiringWeight;   // these are the non-MC-only systematics


         eventScaleFactor = 1.0;

         if ((eventScaleFactor != eventScaleFactor) || (std::isinf(eventScaleFactor)) ||  (std::isnan(eventScaleFactor)) || (abs(eventScaleFactor) > 100) || (abs(eventScaleFactor) < 0.001)  )
         {
            std::cout << "ERROR: failed event scale factor on " << systematic << "_" << *systematic_suffix << ": value is " << eventScaleFactor << std::endl;
            if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos)) std::cout << "PU/pdf/topPt/fact/renorm/btagging med/btagging tight";

            std::cout << "prefiring event weights: ";
            if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos)) std::cout << PU_eventWeight<< "/" << pdf_weight << "/" <<topPtWeight<< "/" <<factWeight<< "/" <<renormWeight<< "/" <<bTag_eventWeight_T << "/" << bTag_eventWeight_T << "/";
            std::cout << " " << prefiringWeight << std::endl;

            badEventSF++;
            continue;
         }




         h_totHT->Fill(totHT,eventScaleFactor);

         if( totHT > 1600)
         {

            h_nfatjets->Fill(nfatjets,eventScaleFactor);
            if(nfatjets > 2)
            {  
               h_nfatjets_pre->Fill(nfatjet_pre,eventScaleFactor);
            }
         }
         // fill a few histograms 

      }

      
      outFile.Write();


      delete h_totHT; delete h_nfatjets; delete h_nfatjets_pre;


   }

   std::cout << "--------- Finished file " << inFileName << std::endl;
   delete f;
   return true;
}

void readTreeStudySelection()
{  

   bool debug = false;
   bool _verbose     = false;
   bool includeTTBar = true;
   bool allHTBins    = true;
   bool runData      = false;
   bool runBR        = false;
   bool runDataBR    = false;
   bool runSelection = true;
   bool runSideband = false;
   int nFailedFiles = 0;
   std::string failedFiles = "";

   std::string runType = "main-band";
   std::string outputFolder = "processedFiles_selectionStudy/";
   if(runSideband) outputFolder = "sideband_processedFile_selectionStudys/";
   std::string eos_path       =  "root://cmseos.fnal.gov//store/user/ecannaer/selectionStudy_combinedROOT/"; 


   std::vector<std::string> dataYears = {"2015","2016","2017","2018"};

   std::vector<std::string> systematics = {"nom"}; 


   for(auto dataYear = dataYears.begin(); dataYear < dataYears.end();dataYear++ )
   {
      std::cout << "----------- Looking at year " << *dataYear << " ------------" << std::endl;
      std::cout << ("Deleting old " + *dataYear + " ROOT files in /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/"+outputFolder +  " .").c_str() << std::endl;
      int delete_result = 1;

      // delete existing processed files 
      if((runDataBR)||(runBR) ) 
      {
         delete_result *= system( ("rm /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/"+outputFolder +  "*QCD*" + *dataYear+ "*.root").c_str() ) ;
         delete_result *= system( ("rm /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/"+outputFolder +  "*ST_*" + *dataYear+ "*.root").c_str() ) ;
         delete_result *= system( ("rm /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/"+outputFolder +  "*TTTo*" + *dataYear+ "*.root").c_str() ) ;
         delete_result *= system( ("rm /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/"+outputFolder +  "*TTJets*" + *dataYear+ "*.root").c_str() ) ;
      }

      if((runDataBR)||(runData)) 
      {
         delete_result *= system( ("rm /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/"+outputFolder +  "*data*" + *dataYear+ "*.root").c_str() ) ;
      }
      if (delete_result == 0) 
      {
         std::cout << "Deleted old ROOT files." << std::endl;
      }
      else 
      {
         std::cout << "Error deleting old ROOT files ...." << std::endl;
         std::cout << "There might have been no root files present there." << std::endl;
      }


      std::vector<std::string> dataBlocks; 
      std::string skimmedFilePaths;

      if(!runSideband)  ///////// RUN MAIN-BAND
      {
         if(runData)
         {

            if(*dataYear == "2015")
            {
               dataBlocks = {"dataB-ver2_","dataC-HIPM_","dataD-HIPM_","dataE-HIPM_","dataF-HIPM_"}; // dataB-ver1 not present
            }
            else if(*dataYear == "2016")
            {
               dataBlocks = {"dataF_", "dataG_", "dataH_"};
            }
            else if(*dataYear == "2017")
            {
               dataBlocks = {"dataB_","dataC_","dataD_","dataE_", "dataF_"};
            }
            else if(*dataYear == "2018")
            {
               dataBlocks = {"dataA_","dataB_","dataC_","dataD_"};
            }
         }
         else if(runBR)
         {  
           dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_" , "TTToLeptonicMC_"};
         }
         else if(runDataBR)
         {
            std::cout << "Running as data+BR" << std::endl;
            if(*dataYear == "2015")
            {
               dataBlocks = {"dataB-ver2_","dataC-HIPM_","dataD-HIPM_","dataE-HIPM_","dataF-HIPM_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_"}; 
            }
            else if(*dataYear == "2016")
            {
               dataBlocks = {"dataF_", "dataG_", "dataH_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_"};
            }
            else if(*dataYear == "2017")
            {
               dataBlocks = {"dataB_","dataC_","dataD_","dataE_", "dataF_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_"};
            }
            else if(*dataYear == "2018")
            {
               dataBlocks = {"dataA_","dataB_","dataC_","dataD_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_"};
            }   
         }
         else if(runSelection)
         {
            dataBlocks = {"QCDMC2000toInf_"};
         }

         else
         {
            std::cout << "No options selected" << std::endl;
            return;
         }
      }
      else if(runSideband)
      {
         runType = "side-band";
         eos_path       =   "root://cmseos.fnal.gov//store/user/ecannaer/selectionStudy_sideband_combinedROOT/";    

         if((runDataBR))
         {
            if(*dataYear == "2015")
            {
               dataBlocks = {"dataB-ver2_","dataC-HIPM_","dataD-HIPM_","dataE-HIPM_","dataF-HIPM_","QCDMC1000to1500_","QCDMC1500to2000_"}; // dataB-ver1 not present
            }
            else if(*dataYear == "2016")
            {
               dataBlocks = {"dataF_", "dataG_", "dataH_","QCDMC1000to1500_","QCDMC1500to2000_"};
            }
            else if(*dataYear == "2017")
            {
               dataBlocks = {"dataB_","dataC_","dataD_","dataE_", "dataF_","QCDMC1000to1500_","QCDMC1500to2000_"};
            }
            else if(*dataYear == "2018")
            {
               dataBlocks = {"dataA_","dataB_","dataC_","dataD_","QCDMC1000to1500_","QCDMC1500to2000_"};
            }   
         }

         else
         {
            std::cout << "No options selected" << std::endl;
            return;
         }

      }
      

      for(auto systematic = systematics.begin();systematic<systematics.end();systematic++)
      {

         double eventScaleFactor = 1; 
         std::cout << "------------ Looking at systematic: " << *systematic << " --------------" << std::endl;

         for(auto dataBlock = dataBlocks.begin();dataBlock < dataBlocks.end();dataBlock++)
         {
            
            std::string year = *dataYear;
            std::string systematic_str;  
            // event weight systematics (below)
            if ((*systematic == "nom" )  ) systematic_str = "nom";
            else
            {
               systematic_str = *systematic;
            }
            if(debug) std::cout << "@@@@@@@@@@@@@ WARNING: YOU ARE IN DEBUG MODE. NOT ALL FILES WILL BE RUN. @@@@@@@@@@@@@@" << std::endl;
            std::string inFileName = (eos_path + *dataBlock+  year +  "_"+ systematic_str+ "_combined.root").c_str();
            
            std::string outFileName = (outputFolder  + *dataBlock+ year + "_processed.root").c_str();

            if( failedFiles.find( (*dataBlock +"/" + year ).c_str()  ) != std::string::npos)
            {
               continue;
            }

            std::cout << "Reading File " << inFileName << " for year,sample,systematic " << year << "/" <<*dataBlock << "/" << *systematic<< std::endl;
            //try
            //{
               if (!doThings(inFileName,outFileName, eventScaleFactor, *dataYear,*systematic, *dataBlock,runType ))
               {

                  std::cout << "ERROR: Failed for year/sample/systematic" << year<< "/" << *dataBlock << "/" << *systematic << std::endl;
                  if( !(failedFiles.find( (*dataBlock +"/" + year ).c_str()  ) != std::string::npos)) // don't copy this multiple times
                  {
                     failedFiles+= (", "+ *dataBlock +"/" + year +"/"  + systematic_str ).c_str();
                     nFailedFiles++;
                  }
               }
            //}
            /*
            catch(...)
            {
               std::cout << "ERROR: Failed for year/sample/systematic" << year<< "/" << *dataBlock << "/" << *systematic << std::endl;
               continue;
            } 
            */
            std::cout << " @@@@@@@@ There have been " << nFailedFiles << " failed jobs files @@@@@@@@" << std::endl;
            std::cout << "Failed files: " << failedFiles << std::endl;


         }
      }
   }
}






//look at nBtag plots ... 
