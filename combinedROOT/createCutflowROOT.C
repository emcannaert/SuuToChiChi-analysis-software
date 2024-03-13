#include <iostream>
#include <string>
#include "TLorentzVector.h"

using namespace std;

void doThings(std::string inFileName, std::string outFileName, double &eventScaleFactors, std::string year, std::vector<std::string> systematics, std::string dataBlock)
{

   double totHT, dijetMassOne, dijetMassTwo;
   int nfatjets, nfatjet_pre,nAK4;
   double SJ_mass_100[100],AK4_DeepJet_disc[100];
   int SJ_nAK4_300[100], SJ_nAK4_50[100];
   double bTag_eventWeight_nom;
   double superJet_mass[100];
   double diSuperJet_mass;
   double average_bTagSF = 0;
   double average_PUSF   = 0;
   double total_events_unscaled = 0;
   // event weights
   double TopPT_EventWeight_nom = 1, PU_eventWeight_nom = 1, L1Prefiring_eventWeight_nom = 1;
   double AK8_phi[100], AK8_eta[100], AK8_pt[100], AK8_mass[100];
   double AK4_phi[100], AK4_eta[100], AK4_pt[100], AK4_mass[100];
   double AK8_JER[100];
   std::map<std::string, std::map<std::string, double> > scale_factors = 
   {
      {"QCDMC1000to1500_",     { {"2015", 1.578683216}, {"2016",1.482632755},  {"2017",3.126481451},  {"2018",4.407417122}  }},
      {"QCDMC1500to2000_",     { {"2015", 0.2119142341},{"2016",0.195224041} , {"2017", 0.3197450474},{"2018",0.5425809983} }},
      {"QCDMC2000toInf_",      { {"2015",0.08568186031},{"2016",0.07572795371},{"2017",0.14306915},   {"2018",0.2277769275} }},
      {"TTToHadronicMC_",      { {"2015",0.075592},     {"2016",0.05808655696},{"2017",0.06651018525},{"2018",0.06588049107}}},
      {"TTToSemiLeptonicMC_",  { {"2015",0.05395328118},{"2016",0.05808655696},{"2017",0.04264829286},{"2018",0.04563489275}}},
      {"TTToLeptonicMC_",      { {"2015",0.0459517611}, {"2016",0.03401684391},{"2017",0.03431532926},{"2018",0.03617828025}}},

      {"TTJetsMCHT1200to2500_",      { {"2015",0.002722324842},{"2016",0.002255554525},{"2017",0.002675947994},{"2018",0.003918532089}  } },
      {"TTJetsMCHT2500toInf_",       { {"2015",0.00005679863673},{"2016",0.00005025384367},{"2017",0.00005947217017},{"2018",0.00008408965681}  } },

      {"ST_t-channel-top_inclMC_",    { {"2015",0.0409963154}, {"2016",0.03607115071},{"2017",0.03494669125},{"2018",0.03859114659}  } } ,
      {"ST_t-channel-antitop_inclMC_", { {"2015",0.05673857623},{"2016",0.04102705994},{"2017",0.04238814865},{"2018",0.03606630944}  } },
      {"ST_s-channel-hadronsMC_",     { {"2015",0.04668187234},{"2016",0.03564988679},{"2017",0.03985938616},{"2018",0.04102795437}  } },
      {"ST_s-channel-leptonsMC_",     { {"2015",0.01323030083},{"2016",0.01149139097},{"2017",0.01117527734},{"2018",0.01155448784}  } },
      {"ST_tW-antiTop_inclMC_",       { {"2015",0.2967888696}, {"2016",0.2301666797},{"2017",0.2556495594},{"2018",0.2700032391}  } },
      {"ST_tW-top_inclMC_",           { {"2015",0.2962796522}, {"2016",0.2355829386},{"2017",0.2563403788},{"2018",0.2625270613} } }

   };

   // get the MC scale factor for each sample. Don't have these for signal yet, so don't scale signal 
   double event_SF;
   if ( ( (dataBlock.find("Suu") != std::string::npos) ) || (dataBlock.find("data") != std::string::npos)) event_SF = 1.0;
   else { event_SF = scale_factors[dataBlock][year];}



   std::cout << "The event SF is " << event_SF <<  " for sample "<< dataBlock <<std::endl;



   const char *_inFilename = inFileName.c_str();
   int total_btags =0;
   std::cout << "Reading file: " << _inFilename << std::endl;

   TFile *f = TFile::Open( _inFilename) ;   //import filename and open file

   if (f->IsZombie())
   {
      std::cout << "ERROR in " << _inFilename << std::endl;
      return;
   }
   const char *_outFilename = outFileName.c_str();    //create the output file where the skimmed tree will be 

   std::cout << "The output file name is : " << _outFilename << std::endl;

   TFile outFile(_outFilename,"RECREATE");
   


   for(auto systematic_ = systematics.begin(); systematic_ < systematics.end();systematic_++)
   {

      std::cout << "--------- new systematic: "<< *systematic_ << " --------" << std::endl;
      std::string systematic = *systematic_;
      std::vector<std::string> systematic_suffices;

      if(systematic == "nom") systematic_suffices = {""};
      else if(systematic == "") systematic_suffices = {""};
      else { systematic_suffices = {"up", "down"};}


      for(auto systematic_suffix = systematic_suffices.begin(); systematic_suffix < systematic_suffices.end();systematic_suffix++)
      {

         double nEvents =0,nHTcut =0 ,nAK8JetCut =0,nHeavyAK8Cut=0,nBtagCut=0,nSJEnergyCut=0, nSJMass100Cut=0;
         double nZeroBtag = 0, nZeroBtagnSJEnergyCut = 0, nZeroBtagnSJMass100Cut = 0;
         double nNoBTags = 0, nAT0b = 0, nAT1b = 0;
         std::cout << "Looking at the " << *systematic_suffix << " tree" << std::endl;

         //create histograms

         TH1F * h_tot_HT_semiRAW= new TH1F("h_tot_HT_semiRAW","Total Event H_{T} (Saved Events); H_{T} [GeV]; Events / 100 GeV",100,0.,10000);
         TH1F * h_nfatjets_semiRAW= new TH1F("h_nfatjets_semiRAW","AK8 Jets / Event (H_{T} cut); nAK8 Jets; Events",9,-0.5,8.5);
         TH1F *h_nfatjets_pre_semiRAW = new TH1F("h_nfatjets_pre_semiRAW","Heavy AK8 Jets / Event (H_{T}, nAK8 cuts); nAK8 Jets (M_{softdrop} > 45 GeV); Events",7,-0.5,6.5);
         TH1F *h_dijet_mass_semiRAW= new TH1F("h_dijet_mass_semiRAW","Dijet Pair Mass (H_{T}, nAK8 cuts); Mass [GeV]; Events / 100 GeV",60,0.,6000);
         TH1F *h_nDijet_pairs_semiRAW= new TH1F("h_nDijet_pairs_semiRAW","Number of Heavy Dijet Pairs / Event (H_{T}, nAK8 cuts); Number of Dijet Pairs (M_{dijet} > 1 TeV); Events",6,-0.5,5.5);

         TH1F *h_nTight_b_jets_semiRAW= new TH1F("h_nTight_b_jets_semiRAW","b-tagged AK4 jets / Event (Tight WP) (H_{T}, nAK8, nHeavyAK8 cuts); Number of tight b-tagged AK4 jets; Events",8,-0.5,7.5) ;
         TH1F * h_SJ_nAK4_300_semiRAW= new TH1F("h_SJ_nAK4_300_semiRAW","Number of Reclustered SJ CA4 Jets (E_{SJ,COM} > 300 GeV); Number of Jets (E_{COM} > 300 GeV); Events",6,-0.5,5.5);
         //TH1F *h_nLoose_b_jets_semiRAW= new TH1F("h_nLoose_b_jets_semiRAW","b-tagged AK4 jets / Event (Loose WP) (H_{T}, nAK8, nHeavyAK8 cuts); Number of Loose b-tagged AK4 jets; Events",10,-0.5,9.5);
        // TH1F *h_nMed_b_jets_semiRAW= new TH1F("h_nMed_b_jets_semiRAW","b-tagged AK4 jets / Event (Med WP) (H_{T}, nAK8, nHeavyAK8 cuts); Number of Med b-tagged AK4 jets; Events",8,-0.5,7.5);

         TH1F *h_AK8_pt= new TH1F("h_AK8_pt", "Selected AK8 jet p_{T} (Event H_{T} > 1.5 TeV); AK8 jet p_{T}; Events / 50 GeV",100,0.,5000);
         TH1F *h_AK8_eta= new TH1F("h_AK8_eta", "Selected AK8 jet eta (Event H_{T} > 1.5 TeV); AK8 jet eta; Events / 0.1",50,-2.5,2.5);
         TH1F *h_AK8_phi= new TH1F("h_AK8_phi", "Selected AK8 jet phi (Event H_{T} > 1.5 TeV); AK8 jet phi; Events / 0.1 rads",80,-4.,4.);
         TH1F *h_AK8_mass= new TH1F("h_AK8_mass", "Selected AK8 jet mass (Event H_{T} > 1.5 TeV); AK8 jet mass; Events / 25 GeV",100,0.,2500.);

         TH1F *h_AK4_pt= new TH1F("h_AK4_pt", "Selected AK4 jet p_{T} (Event H_{T} > 1.5 TeV); AK4 jet p_{T}; Events / 50 GeV",100,0.,5000);
         TH1F *h_AK4_eta= new TH1F("h_AK4_eta", "Selected AK4 jet eta (Event H_{T} > 1.5 TeV); AK4 jet eta; Events / 0.1",50,-2.5,2.5);
         TH1F *h_AK4_phi= new TH1F("h_AK4_phi", "Selected AK4 jet phi (Event H_{T} > 1.5 TeV); AK4 jet phi; Events / 0.2 rads",80,-4.0,4.0);
         TH1F *h_AK4_mass= new TH1F("h_AK4_mass", "Selected AK4 jet mass (Event Event H_{T} > 1.5 TeV); AK4 jet mass; Events / 20 GeV",50,0.,1000.);

         //TH1F * h_AK4_eta_goodphi= new TH1F("h_AK4_eta_goodphi", "AK4 jet eta ( 0.0 > $phi$ or $phi$ > 1.0); AK4 jet eta; Normalized Events",50,-2.5,2.5);
         //TH1F *h_AK4_eta_badphi = new TH1F("h_AK4_eta_badphi", "AK4 jet eta ( 0.0 < $phi$ < 1.0); AK4 jet eta; Normalized Events",50,-2.5,2.5);


         
         TH1F * h_btag_eventWeight_nom= new TH1F("h_btag_eventWeight_nom", "b-tagging event weight (nom); event weight; Events",200,0.0,2.0);
         TH1F * h_PU_eventWeight_nom= new TH1F("h_PU_eventWeight_nom", "Pileup event weight (nom); event weight; Events",200,0.0,4.0);
         TH1F * h_L1Prefiring_eventWeight_nom= new TH1F("h_L1Prefiring_eventWeight_nom", "L1 Prefiring event weigh (nom); event weight; Events",200,0.5,2.0);
         //TH1F * h_PDFEventWeight_nom= new TH1F("h_PDFEventWeight_nom", "PDF event weight (nom); event weight; Events",200,0.0,10.0);
         //TH1F * h_ScaleEventWeight_nom= new TH1F("h_ScaleEventWeight_nom", "Fact. & Renorm. event weight (nom); event weight; Events",200,0.0,10.0);
         TH1F * h_TopPT_eventWeight_nom= new TH1F("h_TopPT_eventWeight_nom", "Top p_{T} event weight (nom); event weight; Events",200,0.0,2.0);
         TH1F * h_JER_ScaleFactor_nom= new TH1F("h_JER_ScaleFactor_nom", "JER Scale Factors applied to AK8 jets (nom); SF; nJets",200,0.5,1.5);

         /*
         TH1F * h_btagEventWeight_up= new TH1F("h_btagEventWeight_up", "b-tagging event weight (up); event weight; Events",200,0.0,2.0);
         TH1F * h_PUEventWeight_up= new TH1F("h_PUEventWeight_up", "Pileup event weight; event weight (up); Events",200,0.0,4.0);
         TH1F * h_PrefiringEventWeight_up= new TH1F("h_PrefiringEventWeight_up", "L1 Prefiring event weight (up); event weight; Events",200,0.0,2.0);
         TH1F * h_PDFEventWeight_up= new TH1F("h_PDFEventWeight_up", "PDF event weight (up); event weight; Events",200,0.0,10.0);
         TH1F * h_ScaleEventWeight_up= new TH1F("h_ScaleEventWeight_up", "Fact. & Renorm. Scale event weight (up); event weight; Events",200,0.0,10.0);
         TH1F * h_TopPTEventWeight_up= new TH1F("h_TopPTEventWeight_up", "Top p_{T} event weight (up); event weight; Events",200,0.0,2.0);
         TH1F * h_JERScaleFactor_up= new TH1F("h_JERScaleFactor_up", "JER Scale Factors applied to AK8 jets (up); SF; nJets",200,0.5,1.5);

         TH1F * h_btagEventWeight_down= new TH1F("h_btagEventWeight_down", "b-tagging event weight (down); event weight; Events",200,0.0,2.0);
         TH1F * h_PUEventWeight_down= new TH1F("h_PUEventWeight_down", "Pileup event weight (down); event weight; Events",200,0.0,4.0);
         TH1F * h_PrefiringEventWeight_down= new TH1F("h_PrefiringEventWeight_down", "L1 Prefiring event weight (down); event weight; Events",200,0.0,2.0);
         TH1F * h_PDFEventWeight_down= new TH1F("h_PDFEventWeight_down", ""PDF event weight (down); event weight; Events",200,0.0,10.0);
         TH1F * h_ScaleEventWeight_down= new TH1F("h_ScaleEventWeight_down", "Fact. & Renorm. Scale event weight (down); event weight; Events",200,0.0,10.0);
         TH1F * h_TopPTEventWeight_down= new TH1F("h_TopPTEventWeight_down", "Top p_{T} event weight (down); event weight; Events",200,0.0,2.0);
         TH1F * h_JERScaleFactor_down= new TH1F("h_JERScaleFactor_down", "JER Scale Factors applied to AK8 jets (down); SF; nJets",200,0.5,1.5);
         */

         TH1F *h_superjet_mass_SR = new TH1F("h_superjet_mass_SR", "AT1b SJ mass; SJ mass [GeV]; Events / 70 GeV",50,0.0,3500);
         TH1F *h_superjet_mass_CR = new TH1F("h_superjet_mass_CR", "AT1b SJ mass; SJ mass [GeV]; Events / 70 GeV",50,0.0,3500);



         TH1F *h_m_SJ1_AT1b = new TH1F("h_m_SJ1_AT1b", "AT1b SJ mass; SJ mass [GeV]; Events / 70 GeV",50,0.0,3500);
         TH1F *h_m_SJ1_AT0b = new TH1F("h_m_SJ1_AT0b", "AT0b SJ mass; SJ mass [GeV]; Events / 70 GeV",50,0.0,3500);
         TH1F *  h_m_SJ1_SR = new TH1F("h_m_SJ1_SR", "SR SJ mass; SJ mass [GeV]; Events / 70 GeV",50,0.0,3500);
         TH1F *  h_m_SJ1_CR = new TH1F("h_m_SJ1_CR", "CR SJ mass; SJ mass [GeV]; Events / 70 GeV",50,0.0,3500);

         TH1F *  h_m_diSJ_SR = new TH1F("h_m_diSJ_SR", "SR diSuperjet mass; SJ mass [GeV]; Events / 70 GeV",100,0.0,8000);
         TH1F *  h_m_diSJ_CR = new TH1F("h_m_diSJ_CR", "CR diSuperjet mass; SJ mass [GeV]; Events / 70 GeV",100,0.0,8000);




         std::string tree_string;
         std::string new_tree_string;
         if( systematic == "nom")
         {
            tree_string = "nom";
            new_tree_string = "nom";
         } 
         else if (systematic == "")
         {
            tree_string = "";
            new_tree_string = "";
         }
         else
         { 
            tree_string = ( systematic+ "_" + *systematic_suffix   ).c_str();
            new_tree_string = (systematic + "_").c_str();
         }

         std::string oldTreeName = "clusteringAnalyzerAll_" + tree_string + "/tree_"+ tree_string;
         std::string newTreeName = "skimmedTree_"+ new_tree_string + *systematic_suffix;

         std::cout << "looking for tree name: " << oldTreeName<< std::endl;
         std::cout << "naming new tree " << newTreeName << std::endl;
         std::cout << "getting tree " << (oldTreeName).c_str() << std::endl;

         TTree *t1 = (TTree*)f->Get( oldTreeName.c_str()   ); 


         outFile.cd();   // return to outer directory
         //gDirectory->mkdir( (systematic+"_"+ *systematic_suffix).c_str()  );   //create directory for this systematic
         gDirectory->mkdir( newTreeName.c_str()  );   //create directory for this systematic
         outFile.cd( newTreeName.c_str() );   // go inside the systematic directory 

         auto *t2 = t1->CloneTree(0);

         t2->SetName(   (newTreeName).c_str()  );

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


         t1->SetBranchAddress("lab_AK4_pt", AK4_pt); 
         t1->SetBranchAddress("AK4_eta", AK4_eta);
         t1->SetBranchAddress("AK4_phi", AK4_phi);
         t1->SetBranchAddress("AK4_mass", AK4_mass);

         t1->SetBranchAddress("jet_pt", AK8_pt);
         t1->SetBranchAddress("jet_eta", AK8_eta);
         t1->SetBranchAddress("jet_phi", AK8_phi);
         t1->SetBranchAddress("jet_mass", AK8_mass);

         t1->SetBranchAddress("AK4_DeepJet_disc", AK4_DeepJet_disc); 

         // SF stuff
         t1->SetBranchAddress("bTag_eventWeight_nom", &bTag_eventWeight_nom); 
         t1->SetBranchAddress("PU_eventWeight_nom", &PU_eventWeight_nom); 
         t1->SetBranchAddress("prefiringWeight_nom", &L1Prefiring_eventWeight_nom); 
         if( (dataBlock.find("TTJets") != std::string::npos) ) t1->SetBranchAddress("top_pt_weight", &TopPT_EventWeight_nom); 
         t1->SetBranchAddress("AK8_JER", AK8_JER); 


         
         t1->SetBranchAddress("superJet_mass", superJet_mass); 
         t1->SetBranchAddress("diSuperJet_mass", &diSuperJet_mass); 

         std::cout << "got tree, set branch addresses. " << std::endl;

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

            eventWeight = 1.0;
            TopPT_EventWeight_nom=1.0;
            L1Prefiring_eventWeight_nom=1.0;
            total_events_unscaled+=1;

            if ((dataBlock.find("MC") != std::string::npos))
            {
               if ((bTag_eventWeight_nom != bTag_eventWeight_nom) || (std::isinf(bTag_eventWeight_nom)))
               {
                  bTag_eventWeight_nom = 1.0;
                  std::cout << "ERROR: bad event weight due to bTag event weight." << std::endl;
               }
               if ((PU_eventWeight_nom != PU_eventWeight_nom) || (std::isinf(PU_eventWeight_nom)))
               {
                  PU_eventWeight_nom = 0.0;
                  std::cout << "ERROR: bad event weight due to PU weight." << std::endl;
               }

               eventWeight = PU_eventWeight_nom*bTag_eventWeight_nom ;
               average_bTagSF+= bTag_eventWeight_nom;
               average_PUSF  += PU_eventWeight_nom;

               if((dataBlock.find("TTJets") != std::string::npos)) eventWeight*= TopPT_EventWeight_nom;

            }
            eventWeight *= L1Prefiring_eventWeight_nom;
            eventWeight *= event_SF; 
            //std::cout <<"Count is "<<nEvents  << ", " << bTag_eventWeight_nom << "-" << PU_eventWeight_nom<< std::endl;

            h_btag_eventWeight_nom->Fill(bTag_eventWeight_nom ,event_SF);
            h_PU_eventWeight_nom->Fill(PU_eventWeight_nom,event_SF);
            h_TopPT_eventWeight_nom->Fill(TopPT_EventWeight_nom,event_SF);
            h_L1Prefiring_eventWeight_nom->Fill(L1Prefiring_eventWeight_nom,event_SF);


            //h_PDFEventWeight_nom->Fill();   // nom versions of these are just 1
            //h_ScaleEventWeight_nom->Fill(); // nom versions of these are just 1

            nEvents+=eventWeight;


            h_tot_HT_semiRAW->Fill(totHT,eventWeight);

            if (totHT < 1500.) continue; 

            for(int iii = 0; iii< nAK4; iii++)
            {
               h_AK4_pt->Fill(AK4_pt[iii],eventWeight);
               h_AK4_eta->Fill(AK4_eta[iii],eventWeight);
               h_AK4_phi->Fill(AK4_phi[iii],eventWeight);
               h_AK4_mass->Fill(AK4_mass[iii],eventWeight);
            }

            for(int iii = 0; iii < nfatjets; iii++)
            {
               h_AK8_pt->Fill(AK8_pt[iii],eventWeight);
               h_AK8_eta->Fill(AK8_eta[iii],eventWeight);
               h_AK8_phi->Fill(AK8_phi[iii],eventWeight);
               h_AK8_mass->Fill(AK8_mass[iii],eventWeight);
               h_JER_ScaleFactor_nom->Fill(AK8_JER[iii],event_SF);
            }


            nHTcut+=eventWeight;
            h_nfatjets_semiRAW->Fill(double(nfatjets),eventWeight);
            if( (nfatjets < 3)   ) continue;
            nAK8JetCut+=eventWeight;
            h_nfatjets_pre_semiRAW->Fill( double(nfatjet_pre),eventWeight);
            h_dijet_mass_semiRAW->Fill(dijetMassOne,eventWeight);
            h_dijet_mass_semiRAW->Fill(dijetMassTwo,eventWeight);

            int nDijetPairs = int(dijetMassOne > 1000.) + int(dijetMassTwo > 1000.);
            h_nDijet_pairs_semiRAW->Fill(nDijetPairs);
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

            h_nTight_b_jets_semiRAW->Fill(nTightBTags,eventWeight);
            if ( (nTightBTags > 0)  )
            {
               nBtagCut+=eventWeight;
               h_SJ_nAK4_300_semiRAW->Fill(SJ_nAK4_300[1],eventWeight); 

               if((SJ_nAK4_300[0]>=2) && (SJ_nAK4_300[1]>=2)   )
               {
                  //signal region
                  nSJEnergyCut+=eventWeight;
                  if((SJ_mass_100[0]>=400.) && (SJ_mass_100[1]>400.)   )
                  {
                     nSJMass100Cut+=eventWeight;
                     h_m_SJ1_SR->Fill(superJet_mass[1],eventWeight);
                     h_m_diSJ_SR->Fill(diSuperJet_mass, eventWeight);
                  }
               }

               // AT1b region
               if(   (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<150.)   )
               {
                  if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
                  {
                     h_m_SJ1_AT1b->Fill(superJet_mass[1],eventWeight);
                     h_m_diSJ_AT1b->Fill(diSuperJet_mass, eventWeight);

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
                  h_m_SJ1_CR->Fill(superJet_mass[1],eventWeight);                     
                  h_m_diSJ_CR->Fill(diSuperJet_mass, eventWeight);

               }

               //AT0b
               if(   (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<150.)   )
               {
                  if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
                  {
                     nAT0b+=eventWeight;
                     h_m_SJ1_AT0b->Fill(superJet_mass[1],eventWeight);
                     h_m_diSJ_AT0b->Fill(diSuperJet_mass, eventWeight);

                  }
               }
               
            }
            t2->Fill();
         }
         outFile.Write();

         // now that histograms are written, kill the old histograms so the ram isn't overused
         delete h_tot_HT_semiRAW;
         delete h_nfatjets_semiRAW;
         delete h_nfatjets_pre_semiRAW;
         delete h_dijet_mass_semiRAW;
         delete h_nDijet_pairs_semiRAW;
         delete h_nTight_b_jets_semiRAW;
         delete h_SJ_nAK4_300_semiRAW;
         delete h_AK8_pt;
         delete h_AK8_eta;
         delete h_AK8_phi;
         delete h_AK8_mass;
         delete h_AK4_pt;
         delete h_AK4_eta;
         delete h_AK4_phi;
         delete h_AK4_mass;
         delete h_btag_eventWeight_nom;
         delete h_PU_eventWeight_nom;
         delete h_L1Prefiring_eventWeight_nom;
         delete h_TopPT_eventWeight_nom;
         delete h_JER_ScaleFactor_nom;
         delete h_superjet_mass_SR;
         delete h_superjet_mass_CR;
         delete h_m_SJ1_AT1b;
         delete h_m_SJ1_AT0b;
         delete h_m_SJ1_SR;
         delete h_m_SJ1_CR;
         delete h_m_diSJ_SR;
         delete h_m_diSJ_CR;
      }
   }
   outFile.Close();




}


void createCutflowROOT()
{


   std::string eos_path       = "root://cmsxrootd.fnal.gov//store/user/ecannaer/combinedROOT/";

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

   std::vector<std::string> background_samples = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"};




   // you must change these ........
   bool runData   = false;
   bool runSignal = false;
   bool runBR     = false;
   bool runAll = false;
   bool runSelection = true;
   bool runDataBR = false;
   std::vector<std::string> years = {"2018","2017","2016","2015"};//{"2015","2016","2017","2018"};    // for testing  "2015","2016","2017"
   std::vector<std::string> systematics = {"nom", "JEC","JER"};   // will eventually use this to skim the systematic files too
   int yearNum = 0;
   //need to have the event scale factors calculated for each year and dataset
   double eventScaleFactor = 1; 
   for(auto datayear = years.begin();datayear<years.end();datayear++)
   {



      std::vector<std::string> data_samples;
      if(*datayear == "2015")
      {
         data_samples = {"dataB-ver2_","dataC-HIPM_","dataD-HIPM_","dataE-HIPM_","dataF-HIPM_"}; // dataB-ver1 not present
      }
      else if(*datayear == "2016")
      {
         data_samples = {"dataF_", "dataG_", "dataH_"};
      }
      else if(*datayear == "2017")
      {
         data_samples = {"dataB_","dataC_","dataD_","dataE_", "dataF_"};
      }
      else if(*datayear == "2018")
      {
         data_samples = {"dataA_","dataB_","dataC_","dataD_"};
      }

      std::vector<std::string> dataBlocks; 
      std::string skimmedFilePaths;
      if (runAll)
      {

         //dataBlocks = signal_samples;

         dataBlocks.reserve( signal_samples.size() + background_samples.size() +data_samples.size() ); // preallocate memory

         dataBlocks.insert( dataBlocks.end(), signal_samples.begin(), signal_samples.end() );
         dataBlocks.insert( dataBlocks.end(), background_samples.begin(), background_samples.end() );
         dataBlocks.insert( dataBlocks.end(), data_samples.begin(), data_samples.end() );

      }
      else if (runDataBR)
      {
         dataBlocks.reserve( background_samples.size() +data_samples.size() ); // preallocate memory
         dataBlocks.insert( dataBlocks.end(), background_samples.begin(), background_samples.end() );
         dataBlocks.insert( dataBlocks.end(), data_samples.begin(), data_samples.end() );
      }
      else if(runData)
      {
         dataBlocks = data_samples;
      }
      else if (runSignal)
      {
         dataBlocks = signal_samples;
      }
      else if (runBR)
      {  
	     dataBlocks = background_samples;
      }
      else if(runSelection)
         dataBlocks = { "TTJetsMCHT1200to2500_"};
      else
      {
         std::cout << "ERROR: Incorrect sample options." << std::endl;
         return;
      }
      for(auto dataBlock = dataBlocks.begin();dataBlock < dataBlocks.end();dataBlock++)
      {
         std::vector<std::string> use_systematics;
         for( auto systematic = systematics.begin(); systematic < systematics.end();systematic++)
         {


            std::string year = *datayear;
            std::string systematic_str = *systematic;

            std::string inFileName;
            std::string outFileName;
            if ((dataBlock->find("Suu") != std::string::npos))
            {
               if(*systematic != "nom") continue; // only need to run once for signal
               inFileName  = (eos_path + *dataBlock + year + "_combined.root").c_str();
               outFileName = ("cutflowFiles/"+*dataBlock+year + "_CUTFLOW.root").c_str();
               use_systematics = systematics;
            } 
            if ((dataBlock->find("data") != std::string::npos) && (*systematic == "JER"))
            {
               continue; // JER is for MC only
            }
            else
            { 
               inFileName= (eos_path + *dataBlock + year + "_"+ systematic_str +"_combined.root").c_str();
               use_systematics = {*systematic};
               outFileName= ("cutflowFiles/"+*dataBlock+year +  "_"+ systematic_str+ "_CUTFLOW.root").c_str();
            }
             
            try
            {
               doThings(inFileName,outFileName,eventScaleFactor,year, use_systematics,*dataBlock);
            }
            catch(...)
            {
               try
               {
                  use_systematics = {""};
                  doThings(inFileName,outFileName,eventScaleFactor,year, use_systematics,*dataBlock);
               }
               catch(...)
               {
                  std::cout << "ERROR: Failed with sample: "<< *dataBlock<< "/" << year << "/" << systematic_str<< std::endl; 
                  continue;
               }
               

            }

            std::cout << "Finished with "<< inFileName << std::endl;

            yearNum++;
         }
      }
   }
}

