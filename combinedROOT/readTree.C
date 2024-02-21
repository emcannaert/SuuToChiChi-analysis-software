#include <iostream>
#include <string>
#include "TLorentzVector.h"
#include <cstdlib>
// check out the SJ mass ratio, this might be really weird for TTbar and could be used to kill some of this


using namespace std;
void doThings(std::string inFileName, std::string outFileName, double& nEvents, double& nHTcut, double& nAK8JetCut,double& nHeavyAK8Cut, double& nBtagCut, double& nDoubleTagged,double& nNoBjets, double& nDoubleTaggedCR, double& NNDoubleTag, double& nDoubleTaggedCRNN,double eventScaleFactor, double& nZeroBtagAntiTag, double & nOneBtagAntiTag, std::string dataYear,std::string systematic)
{


   TH1::SetDefaultSumw2();
   TH2::SetDefaultSumw2();
   int eventnum = 0;int nhadevents = 0;int nfatjets = 0;int raw_nfatjets;int tot_nAK4_50,tot_nAK4_70;int SJ_nAK4_50[100],SJ_nAK4_70[100];
   double jet_pt[100], jet_eta[100], jet_mass[100], jet_dr[100], raw_jet_mass[100],raw_jet_pt[100],raw_jet_phi[100];
   double jet_beta[100], beta_T[100], AK4_mass_20[100],AK4_mass_30[100],AK4_mass_50[100],AK4_mass_70[100],AK4_mass_100[100],SJ_mass_150[100],SJ_mass_600[100],SJ_mass_800[100],SJ_mass_1000[100];
   double SJ_mass_50[100], SJ_mass_70[100],superJet_mass[100],SJ_AK4_50_mass[100],SJ_AK4_70_mass[100],genSuperJetMass[100];double tot_jet_mass,decay_inv_mass, chi_inv_mass;
   int nSuperJets,correctlySortedChi1,correctlySortedChi2;
   int jet_ndaughters[100], jet_nAK4[100],jet_nAK4_20[100],jet_nAK4_30[100],jet_nAK4_50[100],jet_nAK4_70[100],SJ_nAK4_150[100],jet_nAK4_150[100],SJ_nAK4_200[100],SJ_nAK4_400[100],SJ_nAK4_600[100],SJ_nAK4_800[100],SJ_nAK4_1000[100];
   int ntotalevents = 0;
   int nAK4;
   double AK4_mass[100];
   double SJ_mass_100[100],AK4_E[500];
   int SJ_nAK4_100[100];
   double totHT = 0;
   int SJ_nAK4_300[100];
   int nfatjet_pre;
   double SJ_mass_300[100],AK4_phi[100];
   double AK4_bdisc[100],AK4_DeepJet_disc[100];
   double AK4_pt[100];
   double totMET;
   double diSuperJet_mass, diSuperJet_mass_100;
   double dijetMassOne, dijetMassTwo;
   //have to multiply these by scale factors  
   double daughter_mass_comb[100];
   int nGenBJets_AK4[100], AK4_partonFlavour[100],AK4_HadronFlavour[100];
   int SJ1_decision, SJ2_decision;

   double _eventWeightPU,_puWeightDown,_puWeightUp;
   int eventTTbarCRFlag =0;
   
   int nEventsTTbarCR = 0;   
   ////////////////////////////   btag SF variables //////////////////////
   int _eventNumBTag,_eventNumPU, _nAK4;
   double _eventWeightBTag, _AK4_pt[100];

   double diAK8Jet_mass [100];
   double fourAK8JetMass;
   double AK4_eta[100];
   double bTag_eventWeight,PU_eventWeight;
   std::vector<std::string> systematic_suffices;

   if(systematic == "nom")
   {
      // want to run only once with the 
      systematic_suffices = {""};

   }
   else
   {
      systematic_suffices = {"up","down"};
   }



   const char *_inFilename = inFileName.c_str();
   const char *_outFilename = outFileName.c_str();

   std::cout << "Reading file: " << _inFilename << std::endl;



   TFile *f = TFile::Open(_inFilename);

   TFile outFile(_outFilename,"UPDATE");

   for(auto systematic_suffix = systematic_suffices.begin(); systematic_suffix < systematic_suffices.end();systematic_suffix++)
   {

      outFile.cd();   // return to outer directory
      gDirectory->mkdir( (systematic+"_"+ *systematic_suffix).c_str()  );   //create directory for this systematic
      outFile.cd( (systematic+"_"+*systematic_suffix).c_str() );   // go inside the systematic directory 
      std::cout << "Writing out to tree " <<  (systematic+"_"+*systematic_suffix).c_str() << " in file " << outFileName.c_str() << std::endl;

       // need to tunnel into the directory of the infile   JEC_up, nom_ /   skimmedTree_nom / skimmedTree_JER_up

      std::string tree_name;
      std::string folder_name;
      std::string systematic_use = systematic;
      if(( systematic == "nom") || (systematic == "bTagSF")|| (systematic == "PUSF"))
      {
         tree_name = "nom";
         folder_name = "nom_";
         systematic_use = "";
      }
      else
      {
         tree_name = systematic+"_"+*systematic_suffix;
         folder_name = tree_name;
      }

      std::cout << "Looking for tree " << ( tree_name  + "/skimmedTree_"+ tree_name ).c_str() << std::endl;
      TTree *t1;
      Int_t nentries;
      try
      {
         t1 = (TTree*)f->Get(   ( tree_name  + "/skimmedTree_"+ tree_name ).c_str()    );
         nentries = t1->GetEntries();
      }
      
      catch(...)
      {
         std::string alternate_tree_name = ("skimmedTree_" + systematic_use +  "/skimmedTree_" + systematic_use).c_str();
         std::cout << "Normal tree naming scheme not found. Trying alternate scheme: " << alternate_tree_name <<std::endl;
         try
         {
             t1 = (TTree*)f->Get(  ( alternate_tree_name).c_str()    );
             nentries = t1->GetEntries();
         }
         catch(...)
         {

            std::cout << "Still failed. Skipping sample. "<<inFileName <<std::endl;
            return;
         }
      }
      std::cout << "Successfully got tree." << std::endl;
      
      TH1F* h_totHT  = new TH1F("h_totHT","Total Event HT;H_{T} [GeV]; Events / 200 GeV",50,0.,10000);
      TH1F* h_disuperjet_mass  = new TH1F("h_disuperjet_mass","diSuperJet Mass;Mass [GeV]; Events / 200 GeV",50,0.,10000);
      TH1F* h_disuperjet_mass_100  = new TH1F("h_disuperjet_mass_100","diSuperJet Mass (E_{AK4} > 100 GeV);Mass [GeV]; Events / 200 GeV",50,0.,10000);
      TH1I* h_nfatjets_pre  = new TH1I("h_nfatjets_pre","Number of AK8 Jets (p_{T} > 500 GeV, M_{PUPPI} > 45 GeV) per Event ;nAK8 Jets; Events",10,-0.5,9.5);

      // QCD control region stuff 
      TH1I* h_SJ_nAK4_100_CR  = new TH1I("h_SJ_nAK4_100_CR","Number of Reclustered AK4 Jets (E_{COM} > 100 GeV) per SJ (Control Region);nAK4 Jets (E_{COM} > 100 GeV); Events",10,-0.5,9.5);
      TH1I* h_SJ_nAK4_200_CR  = new TH1I("h_SJ_nAK4_200_CR","Number of Reclustered AK4 Jets (E_{COM} > 200 GeV) per SJ (Control Region);nAK4 Jets (E_{COM} > 200 GeV); Events",10,-0.5,9.5);
      TH1F* h_SJ_mass_CR  = new TH1F("h_SJ_mass_CR","SuperJet Mass (Control Region) ;Mass [GeV]; Events / 125 GeV",40,0.,5000);
      TH1F* h_disuperjet_mass_CR  = new TH1F("h_disuperjet_mass_CR","diSuperJet Mass (Control Region);Mass [GeV]; Events / 400 GeV",25,0.,10000);
      TH2F *h_MSJ_mass_vs_MdSJ_CR = new TH2F("h_MSJ_mass_vs_MdSJ_CR","Double Tagged Superjet mass vs diSuperjet mass (Control Region); diSuperjet mass [GeV];superjet mass", 22,1250., 9500, 20, 500, 3500);  /// 375 * 125

      // TTbar control region
      TH2F *h_MSJ_mass_vs_MdSJ_CRTTbar = new TH2F("h_MSJ_mass_vs_MdSJ_CRTTbar","Double Tagged Superjet mass vs diSuperjet mass (TTbar Control Region); diSuperjet mass [GeV];superjet mass", 22,1250., 9500, 20, 500, 3500);  /// 375 * 125


      // Signal regions stuff
      TH1I* h_SJ_nAK4_100_SR  = new TH1I("h_SJ_nAK4_100_SR","Number of Reclustered AK4 Jets (E_{COM} > 100 GeV) per SJ (Signal Region);nAK4 Jets (E_{COM} > 100 GeV); Events",10,-0.5,9.5);
      TH1I* h_SJ_nAK4_200_SR = new TH1I("h_SJ_nAK4_200_SR","Number of Reclustered AK4 Jets (E_{COM} > 200 GeV) per SJ (Signal Region);nAK4 Jets (E_{COM} > 200 GeV); Events",10,-0.5,9.5);
      TH1F* h_SJ_mass_SR  = new TH1F("h_SJ_mass_SR","SuperJet Mass (Signal Region) ;Mass [GeV]; Events / 100 GeV",40,0.,5000);
      TH1F* h_disuperjet_mass_SR  = new TH1F("h_disuperjet_mass_SR","diSuperJet Mass (Signal Region);Mass [GeV]; Events / / 400 GeV",25,0.,10000);
      TH2F *h_MSJ_mass_vs_MdSJ_SR = new TH2F("h_MSJ_mass_vs_MdSJ_SR","Double Tagged Superjet mass vs diSuperjet mass (Signal Region); diSuperjet mass [GeV];superjet mass", 22,1250., 9500, 20, 500, 3500);  /// 375 * 125

      TH2F *h_MSJ_mass_vs_MdSJ_dijet = new TH2F("h_MSJ_mass_vs_MdSJ_dijet","Double Tagged Superjet mass vs diSuperjet mass (dijet technique); 4-jet mass [GeV];avg dijet mass", 22,1250., 9500, 20, 500, 3500);  /// 375 * 125


      TH1I* h_nLooseBTags = new TH1I("h_nLooseBTags","Number of Loosely b-tagged AK4 Jets; Events",10,-0.5,9.5);
      TH1I* h_nMidBTags = new TH1I("h_nMidBTags","Number of Mediumly b-tagged AK4 Jets; Events",10,-0.5,9.5);
      TH1I* h_nTightBTags = new TH1I("h_nTightBTags","Number of Tightly b-tagged AK4 Jets; Events",10,-0.5,9.5);

      TH1I* h_nfatjets = new TH1I("h_nfatjets","Number of AK8 Jets (E_{T} > 300 GeV per Event ;nAK8 Jets; Events",10,-0.5,9.5);


      /////////////more for verifying the CR //////////////////////////////////////
      TH1F* h_AK8_jet_mass_SR  = new TH1F("h_AK8_jet_mass_SR","AK8 Jet Mass (SR region);Mass [GeV]; Events / 30 5GeV",50,0.,1500);
      TH1F* h_AK8_jet_mass_CR  = new TH1F("h_AK8_jet_mass_CR","AK8 Jet Mass (CR);Mass [GeV]; Events / 30 GeV",50,0.,1500);

      TH1F* h_AK4_jet_mass_SR  = new TH1F("h_AK4_jet_mass_SR","AK4 Jet Mass (SR region);Mass [GeV]; Events / 25 GeV",40,0.,1000);
      TH1F* h_AK4_jet_mass_CR  = new TH1F("h_AK4_jet_mass_CR","AK4 Jet Mass (CR);Mass [GeV]; Events / 25 GeV",40,0.,1000);

      TH1F* h_totHT_SR  = new TH1F("h_totHT_SR","Event H_{T} (DT region);H_{T} [GeV]; Events / 200 5GeV",50,0.,10000);
      TH1F* h_totHT_CR  = new TH1F("h_totHT_CR","Event H_{T} (CR);H_{T} [GeV]; Events / 200 GeV",50,0.,10000);

      TH1I* h_nfatjets_SR = new TH1I("h_nfatjets_SR","Number of AK8 Jets (E_{T} > 300 GeV per Event ;nAK8 Jets; Events",10,-0.5,9.5);
      TH1I* h_nfatjets_CR = new TH1I("h_nfatjets_CR","Number of AK8 Jets (E_{T} > 300 GeV per Event ;nAK8 Jets; Events",10,-0.5,9.5);

      TH1I* h_nAK4_SR = new TH1I("h_nAK4_SR","Number of AK4 Jets (E_{T} > 30 GeV per Event ;nAK8 Jets; Events",30,-0.5,29.5);
      TH1I* h_nAK4_CR = new TH1I("h_nAK4_CR","Number of AK4 Jets (E_{T} > 30 GeV per Event ;nAK8 Jets; Events",30,-0.5,29.5);


      TH1I* h_AK4_partonFlavour = new TH1I("h_AK4_partonFlavour","AK4 parton Flavour ;parton flavour ; Events",59,-29.5,29.5);

      TH1F* h_GenBtagged_HT = new TH1F("h_GenBtagged_HT","Event HT of AK4 jets tagged by genParts;H_{T}; Events/300 GeV",25,0.0,7500.0);
      TH1F* h_RECOBtagged_HT = new TH1F("h_RECOBtagged_HT","Event HT of AK4 jets tagged post RECO;H_{T}; Events/300 GeV",25,0.0,7500.0);

      TH1F* h_GenBtagged_pT = new TH1F("h_GenBtagged_pT","p_{T} of AK4 jets tagged by genParts;p_{T}; Events/100 GeV",25,0.0,2500.0);
      TH1F* h_RECOBtagged_pT = new TH1F("h_RECOBtagged_pT","p_{T} of AK4 jets tagged post RECO;p_{T}; Events/100 GeV",25,0.0,2500.0);

      TH1F* h_totHT_All  = new TH1F("h_totHT_All","Event H_{T} (All Events from EDAnalyzer);H_{T} [GeV]; Events / 200 GeV",50,0.,10000);
      TH1F* h_totHT_All1  = new TH1F("h_totHT_All1","Event H_{T} (All Events from EDAnalyzer 1);H_{T} [GeV]; Events / 200 GeV",50,0.,10000);
      TH1F* h_totHT_All2  = new TH1F("h_totHT_All2","Event H_{T} (All Events from EDAnalyzer 2 );H_{T} [GeV]; Events / 200 GeV",50,0.,10000);
      TH1F* h_totHT_All3  = new TH1F("h_totHT_All3","Event H_{T} (All Events from EDAnalyzer 3);H_{T} [GeV]; Events / 200 GeV",50,0.,10000);

      TH1F* h_AK4_DeepJet_disc  = new TH1F("h_AK4_DeepJet_disc","AK4 DeepFlavour bdisc scores;bdisc",25,0.,1.25);
      TH1F* h_AK4_DeepJet_disc_all  = new TH1F("h_AK4_DeepJet_disc_all","AK4 DeepFlavour bdisc scores;bdisc",25,0.,1.25);

      TH1I* h_nAK4 = new TH1I("h_nAK4","Number of AK4 jets;# AK4 jets; Events",20,-0.5,19.5);

      TH2F *h_MSJ_mass_vs_MdSJ_SR_NN = new TH2F("h_MSJ_mass_vs_MdSJ_SR_NN","Double Tagged Superjet mass vs diSuperjet mass (Signal Region, NN tagging); diSuperjet mass [GeV];superjet mass", 25,0, 10000, 20, 0, 6000);

     TH2F* h_MSJ1_vs_MSJ2_SR = new TH2F("h_MSJ1_vs_MSJ2_SR","M_{superjet 2} vs M_{superjet 1} in the Signal Region; M_{superjet 1} Events / 70 GeV;M_{superjet 2} Events / 70 GeV",50,0, 3500, 50, 0, 3500);

     TH2F* h_MSJ1_vs_MSJ2_CR = new TH2F("h_MSJ1_vs_MSJ2_CR","M_{superjet 2} vs M_{superjet 1} in the Control Region; M_{superjet 1} Events / 70 GeV;M_{superjet 2} Events / 70 GeV",50,0, 3500, 50, 0, 3500);

      TH1I* h_nAK4_all  = new TH1I("h_nAK4_all","Number of Lab AK4 Jets (all events);nAK4 Jets; Events",20,-0.5,19.5);
      TH1I* h_nAK4_all_barrel  = new TH1I("h_nAK4_all_barrel","Number of Lab AK4 Jets (all events in barrel);nAK4 Jets; Events",20,-0.5,19.5);
      TH1I* h_nAK4_all_endcap  = new TH1I("h_nAK4_all_endcap","Number of Lab AK4 Jets (all events in endcaps);nAK4 Jets; Events",20,-0.5,19.5);

     /// CR anti-tag region stuff
      TH2F *h_MSJ_mass_vs_MdSJ_antiTagCR = new TH2F("h_MSJ_mass_vs_MdSJ_antiTagCR","Tagged Superjet 2 mass vs diSuperjet mass (Anti-tagged Control Region); diSuperjet mass [GeV];superjet mass", 22,1250., 9500, 20, 500, 3500);  /// 375 * 125
      TH1F* h_SJ_mass_antiTagCR  = new TH1F("h_SJ_mass_antiTagCR","SuperJet Mass (Anti-tagged Control Region) ;Mass [GeV]; Events / 100 GeV",40,0.,5000);
      TH1F* h_disuperjet_mass_antiTagCR  = new TH1F("h_disuperjet_mass_antiTagCR","diSuperJet Mass (Anti-tagged Control Region);Mass [GeV]; Events / / 400 GeV",25,0.,10000);
      TH1I* h_nAK4_0b_antiTag  = new TH1I("h_nAK4_0b_antiTag","Number of Lab AK4 Jets (0b anti-tag region);nAK4 Jets; Events",25,-0.5,24.5);

      // 1-btag anti-tag region stuff
      TH2F *h_MSJ_mass_vs_MdSJ_antiTag_1b = new TH2F("h_MSJ_mass_vs_MdSJ_antiTag_1b","Tagged Superjet 2 mass vs diSuperjet mass (1+ b jet Anti-tagged); diSuperjet mass [GeV];superjet mass", 22,1250., 9500, 20, 500, 3500);  /// 375 * 125
      TH1F* h_SJ_mass_antiTag_1b  = new TH1F("h_SJ_mass_antiTag_1b","SuperJet Mass (1+ b jet Anti-tagged) ;Mass [GeV]; Events / 100 GeV",40,0.,5000);
      TH1F* h_disuperjet_mass_antiTag_1b  = new TH1F("h_disuperjet_mass_antiTag_1b","diSuperJet Mass (1+ b jet Anti-tagged);Mass [GeV]; Events / / 400 GeV",25,0.,10000);
      TH1I* h_nAK4_1b_antiTag  = new TH1I("h_nAK4_1b_antiTag","Number of Lab AK4 Jets (1b anti-tag region);nAK4 Jets; Events",25,-0.5,24.5);
      TH1I* h_nTightbTags_antiTag_1b  = new TH1I("h_nTightbTags_antiTag_1b","Number of tight b-tagged Lab AK4 Jets (1b anti-tag region);n b tags; Events",8,-0.5,7.5);


      TH2I* h_nAK4_wHEM  = new TH2I("h_nAK4_wHEM","Number of AK4 jets (HEM region included); eta; phi",60, -3, 3, 64,-3.2,3.2 );
      TH2I* h_nAK4_noHEM  = new TH2I("h_nAK4_noHEM","Number of AK4 jets (HEM region NOT included); eta; phi",60, -3, 3, 64,-3.2,3.2 );
      TH1F* h_AK4_phi_noHEM  = new TH1F("h_AK4_phi_noHEM","AK4 phi (HEM NOT included);eta; Events",64,-3.2,3.2);

   ////////////////////////////////////////////////////////////////////////////////////////////////////////
      t1->SetBranchAddress("nfatjets", &nfatjets);   
      t1->SetBranchAddress("nSuperJets", &nSuperJets);   
      t1->SetBranchAddress("tot_nAK4_50", &tot_nAK4_50);               //total #AK4 jets (E>50 GeV) for BOTH superjets
      t1->SetBranchAddress("tot_nAK4_70", &tot_nAK4_70);   
      t1->SetBranchAddress("diSuperJet_mass", &diSuperJet_mass);   
      t1->SetBranchAddress("diSuperJet_mass_100", &diSuperJet_mass_100); 
      t1->SetBranchAddress("nfatjet_pre", &nfatjet_pre); 
      t1->SetBranchAddress("jet_pt", jet_pt);   
      t1->SetBranchAddress("jet_eta", jet_eta);   
      t1->SetBranchAddress("jet_mass", jet_mass);   
      t1->SetBranchAddress("SJ_nAK4_50", SJ_nAK4_50);   
      t1->SetBranchAddress("SJ_nAK4_70", SJ_nAK4_70);   
      t1->SetBranchAddress("SJ_mass_50", SJ_mass_50);   
      t1->SetBranchAddress("SJ_mass_70", SJ_mass_70); 
      t1->SetBranchAddress("SJ_mass_150", SJ_mass_150);
      t1->SetBranchAddress("totHT", &totHT);
      t1->SetBranchAddress("SJ_nAK4_300", SJ_nAK4_300);
      t1->SetBranchAddress("SJ_mass_300", SJ_mass_300);
      t1->SetBranchAddress("SJ_mass_50", SJ_mass_50);
      t1->SetBranchAddress("SJ_mass_600", SJ_mass_600);
      t1->SetBranchAddress("SJ_mass_800", SJ_mass_800);
      t1->SetBranchAddress("SJ_mass_1000", SJ_mass_1000);
      t1->SetBranchAddress("superJet_mass", superJet_mass);   
      t1->SetBranchAddress("SJ_AK4_50_mass", SJ_AK4_50_mass);   //mass of individual reclustered AK4 jets
      t1->SetBranchAddress("SJ_AK4_70_mass", SJ_AK4_70_mass); 
      t1->SetBranchAddress("SJ_nAK4_150", SJ_nAK4_150);   
      t1->SetBranchAddress("SJ_nAK4_200", SJ_nAK4_200);  
      t1->SetBranchAddress("SJ_nAK4_300", SJ_nAK4_300);     
      t1->SetBranchAddress("SJ_nAK4_400", SJ_nAK4_400);   
      t1->SetBranchAddress("SJ_nAK4_600", SJ_nAK4_600);   
      t1->SetBranchAddress("SJ_nAK4_800", SJ_nAK4_800);   
      t1->SetBranchAddress("SJ_nAK4_1000", SJ_nAK4_1000);   
      t1->SetBranchAddress("nAK4" , &nAK4); 
      t1->SetBranchAddress("SJ_mass_100", SJ_mass_100);   
      t1->SetBranchAddress("SJ_nAK4_100", SJ_nAK4_100);   
      t1->SetBranchAddress("AK4_E", AK4_E);  
      t1->SetBranchAddress("totMET", &totMET); 
      t1->SetBranchAddress("AK4_bdisc", AK4_bdisc); 
      t1->SetBranchAddress("AK4_eta", AK4_eta); 
      t1->SetBranchAddress("AK4_phi", AK4_phi); 

      
      t1->SetBranchAddress("AK4_mass", AK4_mass); 

      t1->SetBranchAddress("SJ1_decision", &SJ1_decision); 
      t1->SetBranchAddress("SJ2_decision", &SJ2_decision); 

      t1->SetBranchAddress("lab_AK4_pt", AK4_pt); 

      t1->SetBranchAddress("dijetMassOne", &dijetMassOne); 
      t1->SetBranchAddress("dijetMassTwo", &dijetMassTwo); 

      t1->SetBranchAddress("nGenBJets_AK4", nGenBJets_AK4); 

      t1->SetBranchAddress("AK4_partonFlavour", AK4_partonFlavour); 
      t1->SetBranchAddress("AK4_hadronFlavour", AK4_HadronFlavour); 
      t1->SetBranchAddress("AK4_DeepJet_disc", AK4_DeepJet_disc); 

      t1->SetBranchAddress("eventTTbarCRFlag", &eventTTbarCRFlag); 

      t1->SetBranchAddress("fourAK8JetMass", &fourAK8JetMass); 
      t1->SetBranchAddress("diAK8Jet_mass", &diAK8Jet_mass); 

      if( (systematic == "bTagSF") && (*systematic_suffix == "up")) t1->SetBranchAddress("bTag_eventWeight_up", &bTag_eventWeight);
      else if((systematic == "bTagSF") && (*systematic_suffix == "down")) t1->SetBranchAddress("bTag_eventWeight_down", &bTag_eventWeight);
      else{t1->SetBranchAddress("bTag_eventWeight_nom", &bTag_eventWeight); }
      

      if((systematic == "PUSF") && (*systematic_suffix == "up")) t1->SetBranchAddress("PU_eventWeight_up", &PU_eventWeight);
      else if((systematic == "PUSF") && (*systematic_suffix == "down")) t1->SetBranchAddress("PU_eventWeight_down", &PU_eventWeight);
      else{t1->SetBranchAddress("PU_eventWeight_nom", &PU_eventWeight); }
      

      int totalEvents = 0;
      int nPreselected = 0;
      int totWithNoHeavyAK8 = 0;
      int totWithNoLessHeavyAK8 = 0;
      int nPassPreSelection = 0;
      int nControlRegion = 0;
      double looseDeepCSV = 0.1241;
      double medDeepCSV   = 0.4184;
      double tightDeepCSV = 0.7527;
      int passHTandAK8 = 0;

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

      double sum_eventSF_1b_antiTag = 0.0, sum_eventSF_0b_antiTag = 0, sum_eventSF_SR = 0, sum_eventSF_CR = 0;
      double sum_btagSF_1b_antiTag = 0.0, sum_btagSF_0b_antiTag = 0, sum_btagSF_SR = 0.0, sum_btagSF_CR = 0.0;
      double sum_PUSF_1b_antiTag = 0.0, sum_PUSF_0b_antiTag = 0, sum_PUSF_SR = 0.0, sum_PUSF_CR = 0.0;

      double nEvents_unscaled_1b_antiTag = 0.0,nEvents_unscaled_0b_antiTag = 0,nEvents_unscaled_SR =0, nEvents_unscaled_CR =0;
      int num_bad_btagSF = 0, num_bad_PUSF = 0;
      for (Int_t i=0;i<nentries;i++) 
      {  

         t1->GetEntry(i);

         // check if event is HEM
         for(int iii = 0; iii < nAK4; iii++)
         {
            h_nAK4_wHEM->Fill(AK4_eta[iii],AK4_phi[iii]);
         }
         bool  isHEM = false;
         for(int iii = 0; iii < nAK4; iii++)
         {
            if((AK4_phi[iii]>-1.57)&& (AK4_phi[iii]< -0.87) &&(AK4_eta[iii] > -3.0)&& (AK4_eta[iii] < -1.30)) isHEM= true;
         }
         if(isHEM)continue;



         for(int iii = 0; iii < nAK4; iii++)
         {
            h_AK4_phi_noHEM->Fill(AK4_phi[iii]);
            h_nAK4_noHEM->Fill(AK4_eta[iii],AK4_phi[iii]);
         }
         int nAK4_recount = 0;
         int nBarrelAK4 = 0, nEndcapAK4 = 0;

         for(int iii=0; iii<nAK4; iii++)
         {
            if(AK4_pt[iii] > 30.)nAK4_recount++;
            if( abs(AK4_eta[iii]) < 1.6 )nBarrelAK4++;
            else { nEndcapAK4++;}
         }

         h_nAK4_all->Fill(nAK4_recount);
         h_nAK4_all_barrel->Fill(nBarrelAK4);
         h_nAK4_all_endcap->Fill(nEndcapAK4);
         h_nfatjets->Fill(nfatjets);
         eventScaleFactor = 1.0;
         if ((inFileName.find("MC") != std::string::npos))
         {
            if ((bTag_eventWeight != bTag_eventWeight) || (std::isinf(bTag_eventWeight)))
            {
               bTag_eventWeight = 1.0;
               num_bad_btagSF++;
            }
            if ((PU_eventWeight != PU_eventWeight) || (std::isinf(PU_eventWeight)))
            {
               PU_eventWeight = 1.0;
               num_bad_PUSF++;
            }
            eventScaleFactor = bTag_eventWeight*PU_eventWeight;
         }  
         //if (eventScaleFactor>0) eventScaleFactor = 1.0/eventScaleFactor;
         nEvents+=eventScaleFactor;
         if ( (totHT < 1500.)    ) continue;
         nHTcut+=eventScaleFactor;
         if( (nfatjets < 3) ) continue;
         nAK8JetCut+=eventScaleFactor;
         if ((nfatjet_pre < 2) && ( (dijetMassOne < 1000. ) || ( dijetMassOne < 1000.)  ))
         {
            continue;
         } 
         nHeavyAK8Cut+=eventScaleFactor;
         h_nAK4->Fill(nAK4);

         double eventWeightToUse = eventScaleFactor;  // eventScaleFactor comes from the b-tagging and PU event weights
         
         /////////////////////////////////////////////////////////////////////////////////
         /////////////////////////////////////////////////////////////////////////////////

         eventnum++;
         //int _nAK4 = 0;
         for(int iii = 0;iii< nAK4; iii++)
         {
            //if(AK4_pt[iii] > 80.) _nAK4++;
            h_AK4_DeepJet_disc_all->Fill(AK4_DeepJet_disc[iii],eventWeightToUse);
         }    
         
         int nTightBTags = 0, nMedBTags = 0, nLooseBtags =0;

         for(int iii = 0;iii< nAK4; iii++)
         {

            h_AK4_DeepJet_disc->Fill(AK4_DeepJet_disc[iii]);
            if ( (AK4_DeepJet_disc[iii] > tightDeepCSV_DeepJet ) && (AK4_pt[iii] > 30.)) nTightBTags++;
            if ( (AK4_DeepJet_disc[iii] > medDeepCSV_DeepJet )   && (AK4_pt[iii] > 30.)) nMedBTags++;
            if ( (AK4_DeepJet_disc[iii] > looseDeepCSV_DeepJet ) && (AK4_pt[iii] > 30.)) nLooseBtags++;
            //if(abs(AK4_partonFlavour[iii])==5) nLooseBtags++;

         }
         h_nTightBTags->Fill(nTightBTags,eventWeightToUse);
         h_nMidBTags->Fill(nMedBTags,eventWeightToUse);
         h_nLooseBTags->Fill(nLooseBtags,eventWeightToUse);


         for(int iii = 0;iii<nAK4;iii++)
         {
            //if(nGenBJets_AK4[iii]>0)nLooseBtags++;
            //h_AK4_partonFlavour->Fill(AK4_partonFlavour[iii]);
            //if(abs(AK4_partonFlavour[iii])==5) nLooseBtags++;
            if(abs(AK4_partonFlavour[iii])==5)
            {
               h_GenBtagged_HT->Fill(totHT,eventWeightToUse);
               h_GenBtagged_pT->Fill(AK4_pt[iii],eventWeightToUse);
            }
            //std::cout << AK4_partonFlavour[iii] << std::endl;

            if(AK4_DeepJet_disc[nAK4]>looseDeepCSV_DeepJet)
            {
               h_RECOBtagged_HT->Fill(totHT,eventWeightToUse);
               h_RECOBtagged_pT->Fill(AK4_pt[iii],eventWeightToUse);
            }
         }



         /// QCD control region 
         if( nTightBTags < 1 ) 
         {
               nNoBjets+=eventScaleFactor;
               h_SJ_nAK4_100_CR->Fill(SJ_nAK4_100[0],eventWeightToUse);
               h_SJ_nAK4_100_CR->Fill(SJ_nAK4_100[1],eventWeightToUse);

               h_SJ_nAK4_200_CR->Fill(SJ_nAK4_200[0],eventWeightToUse);
               h_SJ_nAK4_200_CR->Fill(SJ_nAK4_200[1],eventWeightToUse);

               //h_SJ_mass_CR->Fill( (superJet_mass[0]+superJet_mass[1])/2. ,eventWeightToUse   );
               //h_SJ_mass_CR->Fill(superJet_mass[0]);
               //h_SJ_mass_CR->Fill(superJet_mass[1]);

               //h_SJ_mass_CR->Fill( superJet_mass[0]    );
               //h_SJ_mass_CR->Fill( superJet_mass[1]    );

               

               h_nfatjets_CR->Fill(nfatjets,eventWeightToUse);
               for(int iii = 0; iii< nfatjets; iii++)
               {
                  h_AK8_jet_mass_CR->Fill(jet_mass[iii],eventWeightToUse);
               }
               h_nAK4_CR->Fill(nAK4,eventWeightToUse);
               for(int iii = 0; iii< nAK4; iii++)
               {
                  h_AK4_jet_mass_CR->Fill(AK4_mass[iii],eventWeightToUse);
               }
               
               //CR
               if(   (SJ_nAK4_300[0]>=2) && (SJ_mass_100[0]>400.)   )
               {
                  if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
                  {


                     if( 0.25 < ( superJet_mass[0]- superJet_mass[1])/ min(superJet_mass[0],superJet_mass[1]))continue;
                     h_disuperjet_mass_CR->Fill(diSuperJet_mass,eventWeightToUse);
                     h_SJ_mass_CR->Fill( (superJet_mass[0]+superJet_mass[1])/2. ,eventWeightToUse );
                     h_totHT_CR->Fill(totHT,eventWeightToUse);
                     nDoubleTaggedCR+=eventScaleFactor;
                     h_MSJ_mass_vs_MdSJ_CR->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2   ,eventWeightToUse );
                     h_MSJ1_vs_MSJ2_CR->Fill(superJet_mass[0],superJet_mass[1],eventWeightToUse);
                     sum_eventSF_CR+=eventScaleFactor;
                     nEvents_unscaled_CR+=1;
                  }

               }
                           // double tagging NN based
               if(  (SJ1_decision<3) && (SJ2_decision<3)  )
               {
                  {
                     nDoubleTaggedCRNN+=eventScaleFactor;
                  }
               }

               //  AT0b
               if(   (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<150.)   )
               {
                  if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
                  {

                     nZeroBtagAntiTag+=eventScaleFactor;
                     h_MSJ_mass_vs_MdSJ_antiTagCR->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse);
                     h_disuperjet_mass_antiTagCR->Fill(diSuperJet_mass,eventWeightToUse);
                     h_SJ_mass_antiTagCR->Fill(superJet_mass[1],eventWeightToUse);
                     sum_eventSF_0b_antiTag+=eventScaleFactor;
                     nEvents_unscaled_0b_antiTag+=1;
                     h_nAK4_0b_antiTag->Fill(nAK4_recount,eventWeightToUse);

                  }  

               }


         }
         nPassPreSelection++;

         
         if ( (nTightBTags > 0)  )
         {
            h_MSJ_mass_vs_MdSJ_dijet->Fill(fourAK8JetMass, (diAK8Jet_mass[0]+diAK8Jet_mass[1])/2.,eventWeightToUse);

            nBtagCut+=eventScaleFactor;
            h_SJ_nAK4_100_SR->Fill(SJ_nAK4_100[0],eventWeightToUse);
            h_SJ_nAK4_100_SR->Fill(SJ_nAK4_100[1],eventWeightToUse);

            h_SJ_nAK4_200_SR->Fill(SJ_nAK4_200[0],eventWeightToUse);
            h_SJ_nAK4_200_SR->Fill(SJ_nAK4_200[1],eventWeightToUse);

            //h_SJ_mass_SR->Fill(superJet_mass[0]);
            //h_SJ_mass_SR->Fill(superJet_mass[1]);


            h_nfatjets_SR->Fill(nfatjets,eventWeightToUse);
            for(int iii = 0; iii< nfatjets; iii++)
            {
               h_AK8_jet_mass_SR->Fill(jet_mass[iii],eventWeightToUse);
            }
            h_nAK4_SR->Fill(nAK4,eventWeightToUse);
            for(int iii = 0; iii< nAK4; iii++)
            {
               h_AK4_jet_mass_SR->Fill(AK4_mass[iii],eventWeightToUse);
            }
            h_totHT_SR->Fill(totHT,eventWeightToUse);

               //SR
               if(   (SJ_nAK4_300[0]>=2) && (SJ_mass_100[0]>400.)   )
               {
                  if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
                  {


                     if( 0.25 < ( superJet_mass[0]- superJet_mass[1])/ min(superJet_mass[0],superJet_mass[1]))continue;


                     h_disuperjet_mass_SR->Fill(diSuperJet_mass,eventWeightToUse);
                     h_SJ_mass_SR->Fill( (superJet_mass[0]+superJet_mass[1])/2. ,eventWeightToUse );
                     nDoubleTagged+= eventScaleFactor;
                     h_MSJ_mass_vs_MdSJ_SR->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventWeightToUse   );
                     h_MSJ1_vs_MSJ2_SR->Fill(superJet_mass[0],superJet_mass[1],eventWeightToUse);
                     sum_eventSF_SR+=eventScaleFactor;
                     nEvents_unscaled_SR+=1;

                  }
               }
                  // double tagging NN based
               if(  (SJ1_decision<3) && (SJ2_decision<3)  )
               {
                  {
                     
                     h_MSJ_mass_vs_MdSJ_SR_NN->Fill(diSuperJet_mass, (superJet_mass[1]+superJet_mass[0]   )/2.,eventWeightToUse );
                     NNDoubleTag+=eventScaleFactor;
                  }
               }



            //AT0b
            if(   (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<150.)   )
            {
               if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
               {
                  nOneBtagAntiTag+=eventWeightToUse;
                  h_MSJ_mass_vs_MdSJ_antiTag_1b->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse);
                  h_SJ_mass_antiTag_1b->Fill(superJet_mass[1],eventWeightToUse);
                  h_disuperjet_mass_antiTag_1b->Fill(diSuperJet_mass,eventWeightToUse);
                  sum_eventSF_1b_antiTag+= eventWeightToUse;
                  nEvents_unscaled_1b_antiTag+=1;
                  h_nAK4_1b_antiTag->Fill(nAK4_recount);
                  h_nTightbTags_antiTag_1b->Fill(nTightBTags);
               }

            }
         }

         

         nPreselected++;
      }
      outFile.Write();
      //std::cout << "The average event scale factors were " << sum_eventSF_SR/nEvents_unscaled_SR  << "/" <<sum_eventSF_CR/nEvents_unscaled_CR << "/" <<sum_eventSF_0b_antiTag/nEvents_unscaled_0b_antiTag << "/" << sum_eventSF_1b_antiTag/nEvents_unscaled_1b_antiTag<<  "in the signal/control/0b-antiTag/1b-antiTag regions" << std::endl;
      //std::cout << "This can be further broken down - average b-tag SF is " << sum_eventSF_SR/nEvents_unscaled_SR  << "/" <<sum_eventSF_CR/nEvents_unscaled_CR << "/" <<sum_eventSF_0b_antiTag/nEvents_unscaled_0b_antiTag << "/" << sum_eventSF_1b_antiTag/nEvents_unscaled_1b_antiTag<<  "in the signal/control/0b-antiTag/1b-antiTag regions" << std::endl;
      //std::cout << "The number of bad btag and PU SFs was " << num_bad_btagSF << " and " << num_bad_PUSF << std::endl;
   }

   outFile.Close();
}


void readTree()
{  

   bool _verbose = false;
   bool includeTTBar = true;
   bool allHTBins    = true;
   bool runData      = false;
   bool runSignal = false;
   bool runAll = true;
   bool runBR = false;

   //std::string eos_path       = "root://cmsxrootd.fnal.gov//store/user/ecannaer/skimmedFiles/";

   //std::vector<std::string> dataYears = {"2015","2016","2017","2018"};
   //std::vector<std::string> systematics = {"nom","JEC","JER", "bTagSF", "PUSF"};  
   std::vector<std::string> dataYears = {"2018","2017","2016","2015"};
   std::vector<std::string> systematics = {"bTagSF","nom", "PUSF", "JEC", "JER"};  //TESTING
   // delete root files in the /Users/ethan/Documents/rootFiles/processedRootFiles folder


   std::vector<std::string> signalFilePaths;
   std::vector<std::string> decays = {"WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"};
   std::vector<std::string> mass_points = {"Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1", "Suu5_chi1p5", "Suu5_chi2", "Suu6_chi1","Suu6_chi1p5", "Suu6_chi2",
   "Suu6_chi2p5", "Suu7_chi1","Suu7_chi1p5","Suu7_chi2", "Suu7_chi2p5", "Suu7_chi3","Suu8_chi1", "Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"};

   for(auto decay = decays.begin(); decay!= decays.end();decay++)
   {
      for(auto mass_point = mass_points.begin();mass_point!= mass_points.end();mass_point++)
      {
         signalFilePaths.push_back((*mass_point+ "_"+ *decay + "_").c_str());
      }
   }
 
   for(auto dataYear = dataYears.begin(); dataYear < dataYears.end();dataYear++ )
   {

      std::cout << "----------- Looking at year " << *dataYear << " ------------" << std::endl;

      std::cout << ("Deleting old " + *dataYear + " ROOT files in /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/processedFiles/ .").c_str() << std::endl;
      int delete_result = system( ("rm /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/processedFiles/*" + *dataYear+ "*.root").c_str() ) ;

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
      if (runAll)
      {
         if(*dataYear == "2015")
         {
            dataBlocks = {"dataB-ver2_","dataC-HIPM_","dataD-HIPM_","dataE-HIPM_","dataF-HIPM_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"}; // dataB-ver1 not present
         }
         else if(*dataYear == "2016")
         {
            dataBlocks = {"dataF_", "dataG_", "dataH_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"};
         }
         else if(*dataYear == "2017")
         {
            dataBlocks = {"dataB_","dataC_","dataD_","dataE_", "dataF_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_",};
         }
         else if(*dataYear == "2018")
         {
            dataBlocks = {"dataA_","dataB_","dataC_","dataD_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"};
         }   
         dataBlocks.insert(dataBlocks.end(), signalFilePaths.begin(), signalFilePaths.end());
      }
      else if(runData)
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
      else if (runSignal)
      {
         dataBlocks = signalFilePaths;
      }
      else if(runBR)
      {  
        //dataBlocks = {"TTToSemiLeptonic_"}; 
        dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_", "TTToLeptonicMC_",
         "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"};
      }
      else
      {
         std::cout << "No options selected" << std::endl;
         return;
      }

      for(auto systematic = systematics.begin();systematic<systematics.end();systematic++)
      {
         double eventScaleFactor = 1; 
         std::cout << "------------ Looking at systematic: " << *systematic << " --------------" << std::endl;

         
         for(auto dataBlock = dataBlocks.begin();dataBlock < dataBlocks.end();dataBlock++)
         {


            if ((*dataBlock).find("data")!= std::string::npos)
            {
               if ((*systematic == "bTagSF") || (*systematic == "PUSF") || (*systematic == "JER")) continue;
            }
            
            double nEvents = 0;
            double nHTcut  = 0;
            double nAK8JetCut = 0;
            double nHeavyAK8Cut = 0;
            double nBtagCut = 0;
            double nDoubleTagged = 0;
            double nNoBjets = 0;
            double nDoubleTaggedCR = 0;
            double NNDoubleTag = 0;
            double nDoubleTaggedCRNN = 0;
            double nZeroBtagAntiTag = 0;
            double nOneBtagAntiTag = 0;

            std::string year = *dataYear;
            std::string systematic_str;
            if ((*systematic == "nom" ) || (*systematic == "bTagSF" ) || (*systematic == "PUSF" )  ) systematic_str = "nom";
            else
            {
               systematic_str = *systematic;
            }
            
            std::string inFileName = ("skimmedFiles/"+ *dataBlock+  year +  "_"+ systematic_str+ "_SKIMMED.root").c_str();
            if (inFileName.find("Suu") != std::string::npos) inFileName = ("skimmedFiles/"+*dataBlock+  year + "_SKIMMED.root").c_str();
            //std::string outFileName = ("/Users/ethan/Documents/rootFiles/processedRootFiles/"+ *dataBlock+year +  "_"+ *systematic+ "_processed.root").c_str();
            std::string outFileName = ("processedFiles/"+ *dataBlock+year + "_processed.root").c_str();
            std::cout << "Reading File " << inFileName << " for year,sample,systematic" << year << "/" <<*dataBlock << "/" << *systematic<< std::endl;
            //try
            //{
               doThings(inFileName,outFileName,nEvents,nHTcut,nAK8JetCut,nHeavyAK8Cut,nBtagCut,nDoubleTagged,nNoBjets,nDoubleTaggedCR, NNDoubleTag,nDoubleTaggedCRNN, eventScaleFactor,nZeroBtagAntiTag, nOneBtagAntiTag, *dataYear,*systematic );
            //}
            /*
            catch(...)
            {
               std::cout << "ERROR: Failed for year/sample/systematic" << year<< "/" << *dataBlock << "/" << *systematic << std::endl;
               continue;
            }*/
            if(_verbose)
            {
               std::cout << "----------------------------------- Starting " << *dataBlock << "-----------------------------------"<< std::endl;
               std::cout << "Total 1b double tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/1+ b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nBtagCut << "/" << nDoubleTagged << std::endl;
               std::cout << "Total 0b double tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/0 b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nNoBjets << "/" << nDoubleTaggedCR << std::endl;
               std::cout << "Total 1b anti tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/0 b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nBtagCut << "/" << nOneBtagAntiTag << std::endl;
               std::cout << "Total 0b anti tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/0 b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nNoBjets << "/" << nZeroBtagAntiTag << std::endl;
               //std::cout << "number of events NN tagged: " << NNDoubleTag << std::endl;
               std::cout << "Finished with "<< inFileName << "." << std::endl;
               std::cout << std::endl;
               std::cout << std::endl;
               std::cout << std::endl;
               std::cout << std::endl;
            }


         }

         
      }
   }
}






//look at nBtag plots ... 
