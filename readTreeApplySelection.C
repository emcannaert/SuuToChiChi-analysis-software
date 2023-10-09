#include <iostream>
#include <string>
#include "TLorentzVector.h"

using namespace std;

void doThings(std::string inFileName, std::string outFileName, double& nEvents)
{

   double totHT, dijetMassOne, dijetMassTwo;
   int nfatjets, nfatjet_pre;
   const char *_inFilename = inFileName.c_str();

   std::cout << "Reading file: " << _inFilename << std::endl;
   TFile *f = new TFile(_inFilename);
   
   const char *_outFilename = outFileName.c_str();

   TFile outFile(_outFilename,"RECREATE");

   TTree *t1 = (TTree*)f->Get("clusteringAnalyzerBR/tree");   //need to change this to something relevenet
   auto *t2 = t1->CloneTree(0);
   t2->SetName("skimmedTree");
   const Int_t nentries = t1->GetEntries();


   t1->SetBranchAddress("totHT", &totHT);   
   t1->SetBranchAddress("nfatjets", &nfatjets);     
   t1->SetBranchAddress("nfatjet_pre", &nfatjet_pre); 
   t1->SetBranchAddress("dijetMassOne", &dijetMassOne);   
   t1->SetBranchAddress("dijetMassTwo", &dijetMassTwo);   

   for (Int_t i=0;i<nentries;i++) 
   {  
      t1->GetEntry(i);
      if( (nfatjets < 3) || (totHT < 1500.)     ) continue;
      if ((nfatjet_pre < 2) && ( (dijetMassOne < 1000. ) || ( dijetMassTwo < 1000.)  ))continue;
      t2->Fill();
   }
   outFile.Write();
}


void readTreeApplySelection()
{
   bool includeTTBar = false;
   bool allHTBins    = false;
   double nEvents = 0;

   std::string dataYear = "2018";
   if(includeTTBar && allHTBins)
   {
      std::vector<std::string> inFileNames = {"/home/ethan/QCD_HT1000to1500.root",
                                        "/home/ethan/QCD_HT1500to2000.root",
                                        "/home/ethan/QCD_HT2000toInf.root",
                                         "/home/ethan/TTToHadronic.root",
                                         "/home/ethan/TTToLeptonic.root",
                                         "/home/ethan/TTToSemiLeptonic.root" };
      std::vector<std::string> outFileNames = {"/home/ethan/Documents/QCD_HT1000to1500_SKIMMED_TEST.root",
                                            "/home/ethan/Documents/QCD_HT1500to2000_SKIMMED_TEST.root",
                                            "/home/ethan/Documents/QCD_HT2000toInf_SKIMMED_TEST.root",
                                            "/home/ethan/Documents/TTToHadronic_SKIMMED_TEST.root",
                                            "/home/ethan/Documents/TTTo2l2nu_combine_cutbased_SKIMMED.root",
                                            "/home/ethan/Documents/TTtoSemiLeptonic_SKIMMED_TEST.root" };
  
      for(unsigned int iii = 0; iii<inFileNames.size(); iii++)
      {
         doThings(inFileNames[iii],outFileNames[iii],nEvents);
      }

      std::cout << "Finished with "<< inFileNames.size() << " files." << std::endl;
   }
   else if( !includeTTBar && allHTBins)
   {
      std::vector<std::string> inFileNames = {("/home/ethan/QCD_HT1000to1500_" + dataYear + ".root").c_str(),("/home/ethan/QCD_HT1500to2000_" + dataYear + ".root").c_str(), ("/home/ethan/QCD_HT2000toInf_" + dataYear + ".root").c_str()};

      std::vector<std::string> outFileNames = {("/home/ethan/Documents/QCD_HT1000to1500_SKIMMED_TEST_"+ dataYear + ".root").c_str(),("/home/ethan/Documents/QCD_HT1500to2000_SKIMMED_TEST_"+ dataYear + ".root").c_str(),("/home/ethan/Documents/QCD_HT2000toInf_SKIMMED_TEST_"+ dataYear + ".root").c_str()};
      for(unsigned int iii = 0; iii<inFileNames.size(); iii++)
      {
         doThings(inFileNames[iii],outFileNames[iii],nEvents);
      }
      std::cout << "Finished with "<< inFileNames.size() << " files." << std::endl;
   }
   else
   {
      std::vector<std::string> inFileNames = {("QCD_HT2000toInf_" + dataYear + ".root").c_str()};

      std::vector<std::string> outFileNames = {("QCD_HT2000toInf_SKIMMED_TEST_"+ dataYear + ".root").c_str()};
      for(unsigned int iii = 0; iii<inFileNames.size(); iii++)
      {
         doThings(inFileNames[iii],outFileNames[iii],nEvents);
      }

      std::cout << "Finished with "<< inFileNames.size() << " files." << std::endl;
   }



}


//look at nBtag plots ... 
