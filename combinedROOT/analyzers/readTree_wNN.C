#include <iostream>
#include <string>
#include "TLorentzVector.h"
#include <cstdlib>

using namespace std;
bool doThings(std::string inFileName, std::string outFileName, double& nEvents, double& nHTcut, double& nAK8JetCut,double& nHeavyAK8Cut, double& nBtagCut, double& nDoubleTagged,double& nNoBjets, double& nDoubleTaggedCR, double& NNDoubleTag, double& nZeroBtagAntiTag, double & nOneBtagAntiTag, double & nNN_SR, double & nNN_CR, double & nNN_AT1b, double & nNN_AT0b,  std::string dataYear,std::string systematic, std::string dataBlock, std::string runType, bool verbose = false)
{


	double BEST_WP = 0.5;
	double BEST_AT_WP = 0.2;

   TH1::SetDefaultSumw2();
   TH2::SetDefaultSumw2();
   int eventnum = 0;int nhadevents = 0; int nfatjets = 0;int raw_nfatjets;int tot_nAK4_50,tot_nAK4_70;int SJ_nAK4_50[100],SJ_nAK4_70[100];
   double jet_pt[100], jet_eta[100], jet_phi[50],jet_mass[100], jet_dr[100], raw_jet_mass[100],raw_jet_pt[100],raw_jet_phi[100];
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
   double nomBtaggingWeight = 1.0;
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
   int eventNumber, ntrueInt, nTau_VLooseVsJet_VLooseVsMuon_VVLooseVse, nMuons_looseID_medIso, nElectrons_looseID_looseISO;

   double _eventWeightPU,_puWeightDown,_puWeightUp;
   int eventTTbarCRFlag =0;
   
   int nEventsTTbarCR = 0;   
   ////////////////////////////   btag SF variables //////////////////////
   int _eventNumBTag,_eventNumPU, _nAK4;
   double _eventWeightBTag, _AK4_pt[100];

   double diAK8Jet_mass [100];
   double fourAK8JetMass;
   double AK4_eta[100];
   double bTag_eventWeight_T ,bTag_eventWeight_M = 1.0, PU_eventWeight = 1.0;
   bool AK4_fails_veto_map[100], AK8_fails_veto_map[100];

   double bTag_eventWeight_bc_M_corr_up = 1,  bTag_eventWeight_bc_M_corr_down = 1;
   double bTag_eventWeight_light_M_corr_up = 1, bTag_eventWeight_light_M_corr_down =1;

   double bTag_eventWeight_bc_M_up = 1,  bTag_eventWeight_bc_M_down = 1;
   double bTag_eventWeight_light_M_up = 1, bTag_eventWeight_light_M_down = 1;

	double JEC_uncert_AK8[50], JEC_uncert_AK4[50], AK8_JER[50];

	double bTag_eventWeight_T_nom = 1, bTag_eventWeight_T_up= 1, bTag_eventWeight_T_down = 1, bTag_eventWeight_M_up = 1, bTag_eventWeight_M_down = 1,bTag_eventWeight_T_corr_up  = 1, bTag_eventWeight_T_corr_down = 1;
	double bTag_eventWeight_M_corr_up= 1, bTag_eventWeight_M_corr_down = 1,  bTag_eventWeight_bc_T_corr_up= 1,  bTag_eventWeight_bc_T_corr_down= 1, bTag_eventWeight_light_T_corr_up = 1, bTag_eventWeight_light_T_corr_down  = 1; 
	double bTag_eventWeight_bc_T_up= 1, bTag_eventWeight_bc_T_down = 1, bTag_eventWeight_light_T_up = 1,bTag_eventWeight_light_T_down = 1;
	double bTag_eventWeight_M_nom = 1;

   double prefiringWeight = 1;
   double pdf_weight = 1.0,factWeight=1.0, renormWeight = 1.0, scale_weight = 1.0,topPtWeight=1.0;
   std::vector<std::string> systematic_suffices;


   double largest_JEC_corr = -1e12;
   double avg_JEC_corr     = 0;
   int total_jets 			= 0;

   double largest_JEC_corr_AK4 = -1e12;
   double avg_JEC_corr_AK4     = 0;
   int total_jets_AK4 			= 0;


   double nfatjets_double, nfatjets_pre_double, nAK4_double;

   int total_1b = 0, total_0b = 0;

   int totEventsUncut;

   double SJ1_BEST_scores, SJ2_BEST_scores;
   int SJ1_decision, SJ2_decision;
   bool fatjet_isHEM[100],jet_isHEM[100] ;

   if(systematic == "nom")
   {
		// want to run only once with the 
		systematic_suffices = {""};
   }
   else if( systematic == "topPt")
   {
		 systematic_suffices = {"up"}; // top pt uncertainty has only "with top pt scaling" and "without top pt scaling"
   }
   else
   {
		systematic_suffices = {"up","down"};
   }

   bool passesPFHT = false, passesPFJet = false;

   const char *_inFilename = inFileName.c_str();
   const char *_outFilename = outFileName.c_str();

   //std::cout << "---------  Reading file: " << _inFilename << std::endl;

   TFile *f = TFile::Open(_inFilename,"READ");

   if ((f == nullptr)||(f->IsZombie()) )
   {
		std::cout << "ERROR: File " << _inFilename << " not found - skipping !!" << std::endl;
		delete f;
		return false;
   }
   TFile * outFile = TFile::Open(_outFilename,"UPDATE");


   
   for(auto systematic_suffix = systematic_suffices.begin(); systematic_suffix < systematic_suffices.end();systematic_suffix++)
   {

		outFile->cd();   // return to outer directory
		if(systematic == "nom" )
		{

         TDirectory* dir = outFile->GetDirectory(systematic.c_str()); // CHANGE
         if (!dir)   
         {
            dir = outFile->mkdir( "nom" ); // CHANGE
         }
         dir->cd();
			//outFile.cd( systematic.c_str() );   // go inside the systematic directory 
		}
		else
		{

         TDirectory* dir = outFile->GetDirectory((systematic+"_"+ *systematic_suffix).c_str() ); // CHANGE
         if (!dir)   
         {
            dir = outFile->mkdir( (systematic+"_"+ *systematic_suffix).c_str() ); // CHANGE
         }
         dir->cd();
			//gDirectory->mkdir( (systematic+"_"+ *systematic_suffix).c_str()  );   //create directory for this systematic
			//outFile.cd( (systematic+"_"+*systematic_suffix).c_str() );   // go inside the systematic directory 
		}
	
		std::string tree_name;
		std::string systematic_use = systematic;

		if((systematic == "nom" ) || (systematic == "bTagSF_tight" ) || (systematic == "bTagSF_tight_corr") || (systematic == "bTagSF_med_corr") || (systematic == "bTagSF_med") ||  (systematic =="bTag_eventWeight_bc_T") ||  (systematic =="bTag_eventWeight_light_T") ||  (systematic =="bTag_eventWeight_bc_M") || (systematic =="bTag_eventWeight_light_M") ||	 (systematic =="bTag_eventWeight_bc_T_corr") ||  (systematic =="bTag_eventWeight_light_T_corr") ||  (systematic =="bTag_eventWeight_bc_M_corr") || (systematic =="bTag_eventWeight_light_M_corr") || (systematic =="bTag_eventWeight_bc_T_year") ||  (systematic =="bTag_eventWeight_light_T_year") ||  (systematic =="bTag_eventWeight_bc_M_year") || (systematic =="bTag_eventWeight_light_M_year")   || (systematic == "bTagSF") || (systematic == "PUSF" ) || (systematic == "L1Prefiring") || (systematic == "pdf") || (systematic == "topPt")|| (systematic == "scale") || (systematic == "renorm") || (systematic == "fact"))
		{
			// these systematics are characterized by event weights that are stored in the "nom" tree
			tree_name = "nom";
			systematic_use = "";
		}
		else
		{
			tree_name = systematic+"_"+*systematic_suffix;
		}

		TTree *t1;
		Int_t nentries;

		try
		{  
			t1 = (TTree*)f->Get(   ( tree_name  + "/skimmedTree_"+ tree_name ).c_str()    );
			if(t1 == nullptr)
			{
				std::cout << "ERROR: tree not found - " << ( tree_name  + "/skimmedTree_"+ tree_name ).c_str()  <<std::endl;
				delete f;
				return false;
			}
			nentries = t1->GetEntries();
		}
		catch(...)
		{
			std::cout << "ERROR: tree not found - " << ( tree_name  + "/skimmedTree_"+ tree_name ).c_str()  <<std::endl;
			delete f;
			return false;
		}
		std::cout << "Successfully got tree " << tree_name  + "/skimmedTree_"+ tree_name << std::endl;
		

		//////////////////////////////////////////////////h_AK8_jet_mass
		/////////// kinematics and diagnostics ///////////
		//////////////////////////////////////////////////

		TH1F* h_totHT  = new TH1F("h_totHT","Total Event H_{T} (w/ L1Prefire, top p_{T} and PU weights); H_{T} [GeV]; Events / 200 GeV",50,0.,10000);
		TH1F* h_totHT_unscaled  = new TH1F("h_totHT_unscaled","Total Event HT (uncorrected by event weights); H_{T} [GeV]; Events / 200 GeV",50,0.,10000);


		TH1F* h_nfatjets_pre  = new TH1F("h_nfatjets_pre","Number of AK8 Jets (p_{T} > 500 GeV, M_{PUPPI} > 45 GeV) per Event ;nAK8 Jets; Events",10,-0.5,9.5);
		TH2F *h_MSJ_mass_vs_MdSJ_dijet = new TH2F("h_MSJ_mass_vs_MdSJ_dijet","Superjet mass vs diSuperjet mass (dijet technique); 4-jet mass [GeV];avg dijet mass", 22,1250., 9500, 20, 500, 3500);  /// 375 * 125
		TH1F* h_nfatjets = new TH1F("h_nfatjets","Number of AK8 Jets (E_{T} > 300 GeV per Event ;nAK8 Jets; Events",10,-0.5,9.5);
		TH1F* h_nAK4 = new TH1F("h_nAK4","Number of AK4 jets;# AK4 jets; Events",20,-0.5,19.5);

		TH1F* h_nAK4_pt50 = new TH1F("h_nAK4_pt50","Number of AK4 jets (p_{T} > 50 GeV);# AK4 jets; Events",20,-0.5,19.5);
		TH1F* h_nAK4_pt75 = new TH1F("h_nAK4_pt75","Number of AK4 jets (p_{T} > 75 GeV);# AK4 jets; Events",20,-0.5,19.5);
		TH1F* h_nAK4_pt100 = new TH1F("h_nAK4_pt100","Number of AK4 jets (p_{T} > 100 GeV);# AK4 jets; Events",20,-0.5,19.5);
		TH1F* h_nAK4_pt150 = new TH1F("h_nAK4_pt150","Number of AK4 jets (p_{T} > 150 GeV);# AK4 jets; Events",20,-0.5,19.5);

		TH1F* h_dijet_mass = new TH1F("h_dijet_mass","Dijet Mass (after nAK8 cut); Mass [GeV]; Events / 60 GeV",40,0,2400);
		TH1F* h_AK8_jet_mass = new TH1F("h_AK8_jet_mass","Mass of Selected AK8 jets (after pre-selection); Mass [GeV] ;Events / 50 GeV",40,0,2000);
		TH1F* h_AK8_jet_pt = new TH1F("h_AK8_jet_pt","p_{T} of Selected AK8 jets (after pre-selection); Mass [GeV]; Events / 75 GeV",40,0,3000);
		TH1F* h_AK8_eta = new TH1F("h_AK8_eta","Eta of AK8 Jets (pre-selected); Eta; Events",50,-3.0,3.0);
		TH1F* h_AK8_phi = new TH1F("h_AK8_phi","Phi of AK8 jets (pre-selected); Phi; Events",50,-3.5,3.5);


		TH1F* h_AK4_eta = new TH1F("h_AK4_eta","Eta of AK4 Jets (pre-selected); Eta; Events",50,-3.0,3.0);
		TH1F* h_AK4_phi = new TH1F("h_AK4_phi","Phi of AK4 jets (pre-selected); Phi; Events",50,-3.5,3.5);

		TH1F* h_nAK4_all  = new TH1F("h_nAK4_all","Number of Lab AK4 Jets (all events);nAK4 Jets; Events",20,-0.5,19.5);
		
		TH1F* h_nCA4_300_1b  = new TH1F("h_nCA4_300_1b","Number of Reclustered SJ CA4 jets (E > 300 GeV) in the 1b region;nJets; Events",10,-0.5,9.5);
		TH1F* h_nCA4_300_0b  = new TH1F("h_nCA4_300_0b","Number of Reclustered SJ CA4 jets (E > 300 GeV) in the 0b region;nJets; Events",10,-0.5,9.5);


		// failed events indices
		// bin 0 triggers
		// bin 1 lepton veto
		// bin 2 veto maps
		// bin 3 HEM
		// bin 4 bad event SF
		// bin 5 HT cut
		// bin 6 nfatjet cut
		// bin 7 heavy AK8 / dijet cut 

		std::string failedEventTitle = "Failed events (index gives cause of failure)  (" + dataBlock  +") "  +   + "("+  systematic+"_"+ *systematic_suffix + ")" +   + "("+ dataYear + ") ; index of failure; Events";
		TH1I* h_failed_events  = new TH1I("h_failed_events", failedEventTitle.c_str(),8,-0.5,7.5);


		// bad event weight indices
		// bin 0 PU
		// bin 1  fact
		// bin 2 renorm
		// bin 3 top pt
		// bin 4  pdf
		// bin 5 btagging med 
		// bin 6 prefiring 
		// bin 7 full event SF

		std::string badeventWeightTitle = "Bad event weights (index gives weight type)  (" + dataBlock  +") "  +   + "("+  systematic+"_"+ *systematic_suffix + ")" +   + "("+ dataYear + ") ; index of failure; Events";
		TH1I* h_bad_event_weights  = new TH1I("h_bad_event_weights", badeventWeightTitle.c_str(),8,-0.5,7.5);

		
		/////////////////////////////////////////////////////////////////////////////
		/////////////more for verifying the CR //////////////////////////////////////
		/////////////////////////////////////////////////////////////////////////////

		TH1F* h_AK8_jet_mass_SR  = new TH1F("h_AK8_jet_mass_SR","AK8 Jet Mass (SR region);Mass [GeV]; Events / 30 5GeV",50,0.,1500);
		TH1F* h_AK8_jet_mass_CR  = new TH1F("h_AK8_jet_mass_CR","AK8 Jet Mass (CR);Mass [GeV]; Events / 30 GeV",50,0.,1500);

		TH1F* h_AK4_jet_mass_SR  = new TH1F("h_AK4_jet_mass_SR","AK4 Jet Mass (SR region);Mass [GeV]; Events / 25 GeV",40,0.,1000);
		TH1F* h_AK4_jet_mass_CR  = new TH1F("h_AK4_jet_mass_CR","AK4 Jet Mass (CR);Mass [GeV]; Events / 25 GeV",40,0.,1000);

		TH1F* h_totHT_SR  = new TH1F("h_totHT_SR","Event H_{T} (SR);H_{T} [GeV]; Events / 200 5GeV",50,0.,10000);
		TH1F* h_totHT_CR  = new TH1F("h_totHT_CR","Event H_{T} (CR);H_{T} [GeV]; Events / 200 GeV",50,0.,10000);
		TH1F* h_totHT_AT1b  = new TH1F("h_totHT_AT1b","Event H_{T} (AT1b);H_{T} [GeV]; Events / 200 5GeV",50,0.,10000);
		TH1F* h_totHT_AT0b  = new TH1F("h_totHT_AT0b","Event H_{T} (AT0b);H_{T} [GeV]; Events / 200 GeV",50,0.,10000);

		TH1F* h_totHT_1b  = new TH1F("h_totHT_1b","Event H_{T} (1b region);H_{T} [GeV]; Events / 200 GeV",50,0.,10000);


		TH1F* h_SJ_mass  = new TH1F("h_SJ_mass","SuperJet Mass (preselected) (cut-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass  = new TH1F("h_disuperjet_mass","diSuperJet Mass (preselected) (cut-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);

		TH1F* h_SJ_mass_uncorrected  = new TH1F("h_SJ_mass_uncorrected","SuperJet Mass (preselected) (no event weights) (cut-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_uncorrected  = new TH1F("h_disuperjet_mass_uncorrected","diSuperJet Mass (preselected) (no event weights) (cut-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);


		// number of tagged superjets per SJ mass bin ----- cut-based
		TH1F* h_SJ_mass_tagged_SJs_1b  = new TH1F("h_SJ_mass_tagged_SJs_1b","Number of Tagged SJs by Superjet mass (1b region);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ_mass_tagged_SJs_0b  = new TH1F("h_SJ_mass_tagged_SJs_0b","Number of Tagged SJs by Superjet mass (0b region);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ_mass_tagged_SJs  = new TH1F("h_SJ_mass_tagged_SJs","Number of Tagged SJs by Superjet mass;SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		
		TH1F* h_SJ2_mass_tagged_SJs_ATSJ1_1b  = new TH1F("h_SJ2_mass_tagged_SJs_ATSJ1_1b","Number of Tagged SJ2 by Superjet mass (SJ1 antitagged) (1b region);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ2_mass_tagged_SJs_ATSJ1_0b  = new TH1F("h_SJ2_mass_tagged_SJs_ATSJ1_0b","Number of Tagged SJs by Superjet mass bin (SJ1 antitagged) (0b region);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ2_mass_tagged_SJs_ATSJ1  = new TH1F("h_SJ2_mass_tagged_SJs_ATSJ1","Number of Tagged SJs per Superjet mass bin (SJ1 antitagged) ;SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
				
		// total number of superjets per mass bin
		TH1F* h_SJ_mass_total_SJs_1b  = new TH1F("h_SJ_mass_total_SJs_1b","Total number of SJs by Superjet mass (1b region);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ_mass_total_SJs_0b  = new TH1F("h_SJ_mass_total_SJs_0b","Total number of SJs by Superjet mass (0b region);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ_mass_total_SJs  = new TH1F("h_SJ_mass_total_SJs","Total number of SJs by Superjet mass;SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		
		TH1F* h_SJ2_mass_total_SJs_ATSJ1_1b  = new TH1F("h_SJ2_mass_total_SJs_ATSJ1_1b","Total number of SJ2 by Superjet mass (SJ1 antitagged) (1b region);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ2_mass_total_SJs_ATSJ1_0b  = new TH1F("h_SJ2_mass_total_SJs_ATSJ1_0b","Total number of SJs by Superjet mass bin (SJ1 antitagged) (0b region);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ2_mass_total_SJs_ATSJ1  = new TH1F("h_SJ2_mass_total_SJs_ATSJ1","Total number of SJs per Superjet mass bin (SJ1 antitagged) ;SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		
		TH1F* h_SJ1_mass_total_SJs_ATSJ2_1b  = new TH1F("h_SJ1_mass_total_SJs_ATSJ2_1b","Total number of SJ1 by Superjet mass (SJ2 antitagged) (1b region);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ1_mass_total_SJs_ATSJ2_0b  = new TH1F("h_SJ1_mass_total_SJs_ATSJ2_0b","Total number of SJs by Superjet mass bin (SJ2 antitagged) (0b region);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ1_mass_total_SJs_ATSJ2  = new TH1F("h_SJ1_mass_total_SJs_ATSJ2","Total number of SJs per Superjet mass bin (SJ2 antitagged) ;SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		


		// number of tagged superjets per SJ mass bin ----- NN-based
		TH1F* h_SJ_mass_tagged_SJs_1b_NN  = new TH1F("h_SJ_mass_tagged_SJs_1b_NN","Number of Tagged SJs by Superjet mass (1b region) (NN-based);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ_mass_tagged_SJs_0b_NN  = new TH1F("h_SJ_mass_tagged_SJs_0b_NN","Number of Tagged SJs by Superjet mass (0b region) (NN-based);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ_mass_tagged_SJs_NN  = new TH1F("h_SJ_mass_tagged_SJs_NN","Number of Tagged SJs by Superjet mass;SJ mass [GeV] (NN-based); Events / 100 GeV",50,0.,5000);
		
		TH1F* h_SJ2_mass_tagged_SJs_ATSJ1_1b_NN  = new TH1F("h_SJ2_mass_tagged_SJs_ATSJ1_1b_NN","Number of Tagged SJ2 by Superjet mass (SJ1 antitagged) (1b region) (NN-based);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ2_mass_tagged_SJs_ATSJ1_0b_NN  = new TH1F("h_SJ2_mass_tagged_SJs_ATSJ1_0b_NN","Number of Tagged SJs by Superjet mass bin (SJ1 antitagged) (0b region) (NN-based);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ2_mass_tagged_SJs_ATSJ1_NN  = new TH1F("h_SJ2_mass_tagged_SJs_ATSJ1_NN","Number of Tagged SJs per Superjet mass bin (SJ1 antitagged) (NN-based);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
			
		TH1F* h_SJ2_mass_total_SJs_ATSJ1_1b_NN  = new TH1F("h_SJ2_mass_total_SJs_ATSJ1_1b_NN","Total number of SJ2 by Superjet mass (SJ1 antitagged) (1b region) (NN-based);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ2_mass_total_SJs_ATSJ1_0b_NN  = new TH1F("h_SJ2_mass_total_SJs_ATSJ1_0b_NN","Total number of SJs by Superjet mass bin (SJ1 antitagged) (0b region) (NN-based);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ2_mass_total_SJs_ATSJ1_NN  = new TH1F("h_SJ2_mass_total_SJs_ATSJ1_NN","Total number of SJs per Superjet mass bin (SJ1 antitagged) (NN-based);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
			
		TH1F* h_SJ1_mass_total_SJs_ATSJ2_1b_NN  = new TH1F("h_SJ1_mass_total_SJs_ATSJ2_1b_NN","Total number of SJ1 by Superjet mass (SJ2 antitagged) (1b region) (NN-based);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ1_mass_total_SJs_ATSJ2_0b_NN  = new TH1F("h_SJ1_mass_total_SJs_ATSJ2_0b_NN","Total number of SJs by Superjet mass bin (SJ2 antitagged) (0b region) (NN-based);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ1_mass_total_SJs_ATSJ2_NN  = new TH1F("h_SJ1_mass_total_SJs_ATSJ2_NN","Total number of SJs per Superjet mass bin (SJ2 antitagged) (NN-based);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);

		TH1F* h_SJ1_mass_tagged_SJs_ATSJ2_1b_NN  = new TH1F("h_SJ1_mass_tagged_SJs_ATSJ2_1b_NN","Number of Tagged SJ1 by Superjet mass (SJ2 antitagged) (1b region) (NN-based);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ1_mass_tagged_SJs_ATSJ2_0b_NN  = new TH1F("h_SJ1_mass_tagged_SJs_ATSJ2_0b_NN","Number of Tagged SJs by Superjet mass bin (SJ2 antitagged) (0b region) (NN-based);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ1_mass_tagged_SJs_ATSJ2_NN  = new TH1F("h_SJ1_mass_tagged_SJs_ATSJ2_NN","Number of Tagged SJs per Superjet mass bin (SJ2 antitagged) (NN-based);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);

		TH1F* h_SJ1_mass_tagged_SJs_ATSJ2_1b  = new TH1F("h_SJ1_mass_tagged_SJs_ATSJ2_1b","Number of Tagged SJ2 by Superjet mass (SJ2 antitagged) (1b region);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ1_mass_tagged_SJs_ATSJ2_0b  = new TH1F("h_SJ1_mass_tagged_SJs_ATSJ2_0b","Number of Tagged SJs by Superjet mass bin (SJ2 antitagged) (0b region);SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
		TH1F* h_SJ1_mass_tagged_SJs_ATSJ2  = new TH1F("h_SJ1_mass_tagged_SJs_ATSJ2","Number of Tagged SJs per Superjet mass bin (SJ2 antitagged) ;SJ mass [GeV]; Events / 100 GeV",50,0.,5000);
				

		TH1F* h_nfatjets_SR = new TH1F("h_nfatjets_SR","Number of AK8 Jets (E_{T} > 300 GeV per Event ;nAK8 Jets; Events",10,-0.5,9.5);
		TH1F* h_nfatjets_CR = new TH1F("h_nfatjets_CR","Number of AK8 Jets (E_{T} > 300 GeV per Event ;nAK8 Jets; Events",10,-0.5,9.5);

		TH1F* h_nAK4_SR = new TH1F("h_nAK4_SR","Number of AK4 Jets (E_{T} > 30 GeV per Event ;nAK8 Jets; Events",30,-0.5,29.5);
		TH1F* h_nAK4_CR = new TH1F("h_nAK4_CR","Number of AK4 Jets (E_{T} > 30 GeV per Event ;nAK8 Jets; Events",30,-0.5,29.5);

		/////////////////////////////////////////
		//////  Region-specific histograms /////
		////////////////////////////////////////

		// SR
		TH1F* h_SJ_nAK4_100_SR  = new TH1F("h_SJ_nAK4_100_SR","Number of Reclustered AK4 Jets (E_{COM} > 100 GeV) per SJ (Signal Region) (cut-based);nAK4 Jets (E_{COM} > 100 GeV); Events",10,-0.5,9.5);
		TH1F* h_SJ_nAK4_200_SR = new TH1F("h_SJ_nAK4_200_SR","Number of Reclustered AK4 Jets (E_{COM} > 200 GeV) per SJ (Signal Region) (cut-based);nAK4 Jets (E_{COM} > 200 GeV); Events",10,-0.5,9.5);
		TH1F* h_SJ_mass_SR  = new TH1F("h_SJ_mass_SR","SuperJet Mass (Signal Region) (cut-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_SR  = new TH1F("h_disuperjet_mass_SR","diSuperJet Mass (Signal Region) (cut-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH2F *h_MSJ_mass_vs_MdSJ_SR = new TH2F("h_MSJ_mass_vs_MdSJ_SR","Superjet mass vs diSuperjet mass (Signal Region) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F* h_MSJ1_vs_MSJ2_SR = new TH2F("h_MSJ1_vs_MSJ2_SR","M_{superjet 2} vs M_{superjet 1} in the Signal Region (cut-based); M_{superjet 1} Events / 70 GeV;M_{superjet 2} Events / 70 GeV",50,0, 3500, 50, 0, 3500);

		// CR
		TH1F* h_SJ_nAK4_100_CR  = new TH1F("h_SJ_nAK4_100_CR","Number of Reclustered AK4 Jets (E_{COM} > 100 GeV) per SJ (Control Region) (cut-based);nAK4 Jets (E_{COM} > 100 GeV); Events",10,-0.5,9.5);
		TH1F* h_SJ_nAK4_200_CR  = new TH1F("h_SJ_nAK4_200_CR","Number of Reclustered AK4 Jets (E_{COM} > 200 GeV) per SJ (Control Region) (cut-based);nAK4 Jets (E_{COM} > 200 GeV); Events",10,-0.5,9.5);
		TH1F* h_SJ_mass_CR  = new TH1F("h_SJ_mass_CR","SuperJet Mass (Control Region) (cut-based);Mass [GeV]; Events / 125 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_CR  = new TH1F("h_disuperjet_mass_CR","diSuperJet Mass (Control Region) (cut-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH2F *h_MSJ_mass_vs_MdSJ_CR = new TH2F("h_MSJ_mass_vs_MdSJ_CR","Superjet mass vs diSuperjet mass (Control Region) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F* h_MSJ1_vs_MSJ2_CR = new TH2F("h_MSJ1_vs_MSJ2_CR","M_{superjet 2} vs M_{superjet 1} in the Control Region (cut-based); M_{superjet 1} Events / 70 GeV;M_{superjet 2} Events / 70 GeV",50,0, 3500, 50, 0, 3500);

		/// AT0b
		TH2F *h_MSJ_mass_vs_MdSJ_AT0b = new TH2F("h_MSJ_mass_vs_MdSJ_AT0b","Tagged Superjet 2 mass vs diSuperjet mass (AT0b) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH1F* h_SJ_mass_AT0b  = new TH1F("h_SJ_mass_AT0b","SuperJet Mass (AT0b) (cut-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_AT0b  = new TH1F("h_disuperjet_mass_AT0b","diSuperJet Mass (AT0b) (cut-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH1F* h_nAK4_AT0b  = new TH1F("h_nAK4_AT0b","Number of Lab AK4 Jets (AT0b) (cut-based);nAK4 Jets; Events",25,-0.5,24.5);

		// AT1b
		TH2F *h_MSJ_mass_vs_MdSJ_AT1b = new TH2F("h_MSJ_mass_vs_MdSJ_AT1b","Tagged Superjet 2 mass vs diSuperjet mass (AT1b) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH1F* h_SJ_mass_AT1b  = new TH1F("h_SJ_mass_AT1b","SuperJet Mass (AT1b) (cut-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_AT1b  = new TH1F("h_disuperjet_mass_AT1b","diSuperJet Mass (AT1b) (cut-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH1F* h_nAK4_AT1b  = new TH1F("h_nAK4_AT1b","Number of Lab AK4 Jets (AT1b) (cut-based);nAK4 Jets; Events",25,-0.5,24.5);
		TH1F* h_nTightbTags_AT1b  = new TH1F("h_nTightbTags_AT1b","Number of tight b-tagged Lab AK4 Jets (AT1b) (cut-based);n b tags; Events",8,-0.5,7.5);

		/// AT0tb
		TH2F *h_MSJ_mass_vs_MdSJ_AT0tb = new TH2F("h_MSJ_mass_vs_MdSJ_AT0tb","Tagged Superjet 2 mass vs diSuperjet mass (AT0tb) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH1F* h_SJ_mass_AT0tb  = new TH1F("h_SJ_mass_AT0tb","SuperJet Mass (AT0tb) (cut-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_AT0tb  = new TH1F("h_disuperjet_mass_AT0tb","diSuperJet Mass (AT0tb) (cut-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);

		// AT1tb
		TH2F *h_MSJ_mass_vs_MdSJ_AT1tb = new TH2F("h_MSJ_mass_vs_MdSJ_AT1tb","Tagged Superjet 2 mass vs diSuperjet mass (AT1tb) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH1F* h_SJ_mass_AT1tb  = new TH1F("h_SJ_mass_AT1tb","SuperJet Mass (AT1tb) (cut-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_AT1tb  = new TH1F("h_disuperjet_mass_AT1tb","diSuperJet Mass (AT1tb) (cut-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);

		/// ADT0b
		TH2F *h_MSJ_mass_vs_MdSJ_ADT0b = new TH2F("h_MSJ_mass_vs_MdSJ_ADT0b","Tagged Superjet 2 mass vs diSuperjet mass (ADT0b) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH1F* h_SJ_mass_ADT0b  = new TH1F("h_SJ_mass_ADT0b","SuperJet Mass (ADT0b) (cut-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_ADT0b  = new TH1F("h_disuperjet_mass_ADT0b","diSuperJet Mass (ADT0b) (cut-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH1F* h_nAK4_ADT0b  = new TH1F("h_nAK4_ADT0b","Number of Lab AK4 Jets (ADT0b) (cut-based);nAK4 Jets; Events",25,-0.5,24.5);

		// ADT1b
		TH2F *h_MSJ_mass_vs_MdSJ_ADT1b = new TH2F("h_MSJ_mass_vs_MdSJ_ADT1b","Tagged Superjet 2 mass vs diSuperjet mass (ADT1b) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH1F* h_SJ_mass_ADT1b  = new TH1F("h_SJ_mass_ADT1b","SuperJet Mass (ADT1b) (cut-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_ADT1b  = new TH1F("h_disuperjet_mass_ADT1b","diSuperJet Mass (ADT1b) (cut-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH1F* h_nAK4_ADT1b  = new TH1F("h_nAK4_ADT1b","Number of Lab AK4 Jets (ADT1b) (cut-based);nAK4 Jets; Events",25,-0.5,24.5);
		TH1F* h_nTightbTags_ADT1b  = new TH1F("h_nTightbTags_ADT1b","Number of tight b-tagged Lab AK4 Jets (ADT1b) (cut-based);n b tags; Events",8,-0.5,7.5);
 
		// different b-regions --- cut-based
		TH2F *h_MSJ_mass_vs_MdSJ_SR_bpt75 = new TH2F("h_MSJ_mass_vs_MdSJ_SR_bpt75","Superjet mass vs diSuperjet mass (Signal Region) (cut-based) (b jet p_{T} > 75 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_SR_bpt100 = new TH2F("h_MSJ_mass_vs_MdSJ_SR_bpt100","Superjet mass vs diSuperjet mass (Signal Region) (cut-based) (b jet p_{T} > 100 GeV) ; diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_SR_bpt150 = new TH2F("h_MSJ_mass_vs_MdSJ_SR_bpt150","Superjet mass vs diSuperjet mass (Signal Region) (cut-based) (b jet p_{T} > 150 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		TH2F *h_MSJ_mass_vs_MdSJ_CR_bpt75 = new TH2F("h_MSJ_mass_vs_MdSJ_CR_bpt75","Superjet mass vs diSuperjet mass (Control Region) (cut-based) (b jet p_{T} > 75 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_CR_bpt100 = new TH2F("h_MSJ_mass_vs_MdSJ_CR_bpt100","Superjet mass vs diSuperjet mass (Control Region) (cut-based) (b jet p_{T} > 100 GeV) ; diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_CR_bpt150 = new TH2F("h_MSJ_mass_vs_MdSJ_CR_bpt150","Superjet mass vs diSuperjet mass (Control Region) (cut-based) (b jet p_{T} > 150 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		TH2F *h_MSJ_mass_vs_MdSJ_AT1b_bpt75 = new TH2F("h_MSJ_mass_vs_MdSJ_AT1b_bpt75","Superjet mass vs diSuperjet mass (AT1b Region) (cut-based) (b jet p_{T} > 75 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_AT1b_bpt100 = new TH2F("h_MSJ_mass_vs_MdSJ_AT1b_bpt100","Superjet mass vs diSuperjet mass (AT1b Region) (cut-based) (b jet p_{T} > 100 GeV) ; diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_AT1b_bpt150 = new TH2F("h_MSJ_mass_vs_MdSJ_AT1b_bpt150","Superjet mass vs diSuperjet mass (AT1b Region) (cut-based) (b jet p_{T} > 150 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		TH2F *h_MSJ_mass_vs_MdSJ_AT0b_bpt75 = new TH2F("h_MSJ_mass_vs_MdSJ_AT0b_bpt75","Superjet mass vs diSuperjet mass (AT0b Region) (cut-based) (b jet p_{T} > 75 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_AT0b_bpt100 = new TH2F("h_MSJ_mass_vs_MdSJ_AT0b_bpt100","Superjet mass vs diSuperjet mass (AT0b Region) (cut-based) (b jet p_{T} > 100 GeV) ; diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_AT0b_bpt150 = new TH2F("h_MSJ_mass_vs_MdSJ_AT0b_bpt150","Superjet mass vs diSuperjet mass (AT0b Region) (cut-based) (b jet p_{T} > 150 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		// different b-regions --- NN-based
		TH2F *h_MSJ_mass_vs_MdSJ_NN_SR_bpt75 = new TH2F("h_MSJ_mass_vs_MdSJ_NN_SR_bpt75","Superjet mass vs diSuperjet mass (Signal Region) (NN-based) (b jet p_{T} > 75 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_NN_SR_bpt100 = new TH2F("h_MSJ_mass_vs_MdSJ_NN_SR_bpt100","Superjet mass vs diSuperjet mass (Signal Region) (NN-based) (b jet p_{T} > 100 GeV) ; diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_NN_SR_bpt150 = new TH2F("h_MSJ_mass_vs_MdSJ_NN_SR_bpt150","Superjet mass vs diSuperjet mass (Signal Region) (NN-based) (b jet p_{T} > 150 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		TH2F *h_MSJ_mass_vs_MdSJ_NN_CR_bpt75 = new TH2F("h_MSJ_mass_vs_MdSJ_NN_CR_bpt75","Superjet mass vs diSuperjet mass (Control Region) (NN-based) (b jet p_{T} > 75 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_NN_CR_bpt100 = new TH2F("h_MSJ_mass_vs_MdSJ_NN_CR_bpt100","Superjet mass vs diSuperjet mass (Control Region) (NN-based) (b jet p_{T} > 100 GeV) ; diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_NN_CR_bpt150 = new TH2F("h_MSJ_mass_vs_MdSJ_NN_CR_bpt150","Superjet mass vs diSuperjet mass (Control Region) (NN-based) (b jet p_{T} > 150 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		TH2F *h_MSJ_mass_vs_MdSJ_NN_AT1b_bpt75 = new TH2F("h_MSJ_mass_vs_MdSJ_NN_AT1b_bpt75","Superjet mass vs diSuperjet mass (AT1b Region) (NN-based) (b jet p_{T} > 75 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_NN_AT1b_bpt100 = new TH2F("h_MSJ_mass_vs_MdSJ_NN_AT1b_bpt100","Superjet mass vs diSuperjet mass (AT1b Region) (NN-based) (b jet p_{T} > 100 GeV) ; diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_NN_AT1b_bpt150 = new TH2F("h_MSJ_mass_vs_MdSJ_NN_AT1b_bpt150","Superjet mass vs diSuperjet mass (AT1b Region) (NN-based) (b jet p_{T} > 150 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		TH2F *h_MSJ_mass_vs_MdSJ_NN_AT0b_bpt75 = new TH2F("h_MSJ_mass_vs_MdSJ_NN_AT0b_bpt75","Superjet mass vs diSuperjet mass (AT0b Region) (NN-based) (b jet p_{T} > 75 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_NN_AT0b_bpt100 = new TH2F("h_MSJ_mass_vs_MdSJ_NN_AT0b_bpt100","Superjet mass vs diSuperjet mass (AT0b Region) (NN-based) (b jet p_{T} > 100 GeV) ; diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_NN_AT0b_bpt150 = new TH2F("h_MSJ_mass_vs_MdSJ_NN_AT0b_bpt150","Superjet mass vs diSuperjet mass (AT0b Region) (NN-based) (b jet p_{T} > 150 GeV); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125


		/////////////////////////////
		//////// BEST stuff /////////
		/////////////////////////////

		TH1F* h_SJ1_BEST_score_1b  = new TH1F("h_SJ1_BEST_score_1b","SJ1 BEST Score (1b region); Score; superjets",50,0,1.0);
		TH1F* h_SJ1_BEST_score_0b  = new TH1F("h_SJ1_BEST_score_0b","SJ1 BEST Score (0b region); Score; superjets",50,0,1.0);


		TH1F* h_SJ2_BEST_score_1b  = new TH1F("h_SJ2_BEST_score_1b","SJ1 BEST Score (1b region); Score; superjets",50,0,1.0);
		TH1F* h_SJ2_BEST_score_0b  = new TH1F("h_SJ2_BEST_score_0b","SJ2 BEST Score (0b region); Score; superjets",50,0,1.0);

		TH1F* h_SJ1_decision_1b  = new TH1F("h_SJ1_decision_1b","Superjet decision category (1b region);Category; Superjets",3,-0.5,2.5);
		TH1F* h_SJ1_decision_0b  = new TH1F("h_SJ1_decision_0b","Superjet decision category (0b region);Category; Superjets",3,-0.5,2.5);

		TH1F* h_SJ2_decision_1b  = new TH1F("h_SJ2_decision_1b","superjet decision category (1b region);Category; Superjets",3,-0.5,2.5);
		TH1F* h_SJ2_decision_0b  = new TH1F("h_SJ2_decision_0b","superjet decision category (0b region);Category; Superjets",3,-0.5,2.5);
			   

		TH1F* h_SJ1_BEST_score  = new TH1F("h_SJ1_BEST_score","SJ2 BEST Score (All SJ1); Score; superjets",50,0,1.0);
		TH1F* h_SJ2_BEST_score  = new TH1F("h_SJ2_BEST_score","SJ1 BEST Score (All SJ2); Score; superjets",50,0,1.0);

		TH1F* h_SJ1_decision  = new TH1F("h_SJ1_decision","Superjet 1 decision category;Category; Superjets",3,-0.5,2.5);
		TH1F* h_SJ2_decision  = new TH1F("h_SJ2_decision","Superjet 2 decision category;Category; Superjets",3,-0.5,2.5);


		// antitagged SJ2 NN scores (for data/MC comparisons)
		TH1F* h_SJ2_BEST_score_1b_SJ1AT  = new TH1F("h_SJ2_BEST_score_1b_SJ1AT","SJ2 BEST Score (1b region) (AT region); Score; superjets",50,0,1.0);
		TH1F* h_SJ2_BEST_score_0b_SJ1AT  = new TH1F("h_SJ2_BEST_score_0b_SJ1AT","SJ2 BEST Score (0b region) (AT region); Score; superjets",50,0,1.0);
		TH1F* h_SJ2_BEST_score_SJ1AT  = new TH1F("h_SJ2_BEST_score_SJ1AT","SJ2 BEST Score (AT region); Score; superjets",50,0,1.0);

		TH1F* h_SJ2_decision_1b_SJ1AT  = new TH1F("h_SJ2_decision_1b_SJ1AT","Superjet decision category (1b region) (AT region);Category; Superjets",3,-0.5,2.5);
		TH1F* h_SJ2_decision_0b_SJ1AT  = new TH1F("h_SJ2_decision_0b_SJ1AT","Superjet decision category (0b region) (AT region);Category; Superjets",3,-0.5,2.5);
		TH1F* h_SJ2_decision_SJ1AT  = new TH1F("h_SJ2_decision_SJ1AT","Superjet decision category (AT region);Category; Superjets",3,-0.5,2.5);

		TH1F* h_SJ1_BEST_score_1b_SJ2AT  = new TH1F("h_SJ1_BEST_score_1b_SJ2AT","SJ1 BEST Score (1b region) (AT region); Score; superjets",50,0,1.0);
		TH1F* h_SJ1_BEST_score_0b_SJ2AT  = new TH1F("h_SJ1_BEST_score_0b_SJ2AT","SJ1 BEST Score (0b region) (AT region); Score; superjets",50,0,1.0);
		TH1F* h_SJ1_BEST_score_SJ2AT  = new TH1F("h_SJ1_BEST_score_SJ2AT","SJ1 BEST Score (AT region); Score; superjets",50,0,1.0);

		TH1F* h_SJ1_decision_1b_SJ2AT  = new TH1F("h_SJ1_decision_1b_SJ2AT","Superjet decision category (1b region) (AT region);Category; Superjets",3,-0.5,2.5);
		TH1F* h_SJ1_decision_0b_SJ2AT  = new TH1F("h_SJ1_decision_0b_SJ2AT","Superjet decision category (0b region) (AT region);Category; Superjets",3,-0.5,2.5);
		TH1F* h_SJ1_decision_SJ2AT  = new TH1F("h_SJ1_decision_SJ2AT","Superjet decision category (AT region);Category; Superjets",3,-0.5,2.5);



		/////////////////////////////////////////////
		/////////// systematic uncertainties ///////
		////////////////////////////////////////////

		// overall event weights

		TH1I * h_numTrueInteractions= new TH1I("h_numTrueInteractions", "Number of true pileup interactions per event; PU interactions; Events",100,-0.5,99.5);


		TH1F * h_pdf_EventWeight= new TH1F("h_pdf_EventWeight", "PDF event weight; event weight; Events",40,0.0,4.0);
		TH1F * h_renorm_EventWeight= new TH1F("h_renorm_EventWeight", "Renorm. event weight; event weight; Events",40,0.0,2.5);
		TH1F * h_factor_EventWeight= new TH1F("h_factor_EventWeight", "Fact. event weight; event weight; Events",40,0.0,2.5);
		TH1F * h_scale_EventWeight= new TH1F("h_scale_EventWeight", "Scale event weight (using envelope); event weight; Events",40,0.0,2.5);

		TH1F* h_PU_eventWeight  = new TH1F("h_PU_eventWeight","Pileup Event Weights;Event Weight; Events",40,0.0,3.0);
		TH1F* h_bTag_eventWeight_T  = new TH1F("h_bTag_eventWeight_T","b tagging Event Weights (tight WP);Event Weight; Events",100,0.0,4.0);
		TH1F* h_bTag_eventWeight_M  = new TH1F("h_bTag_eventWeight_M","b tagging Event Weights (medium WP);Event Weight; Events",100,0.0,4.0);
		TH1F* h_L1PrefiringWeight  = new TH1F("h_L1PrefiringWeight","L1 Prefiring Event Weights ;Event Weight; Events",40,0.0,1.5);
		//TH1F* h_topPtWeight  = new TH1F("h_topPtWeight","Top p_{T} Event Weights ;Event Weight  (SR); Events",50,0.0,3.0);
		


		TH1F* h_JEC_uncert_AK8  = new TH1F("h_JEC_uncert_AK8","AK8 JEC Uncertainty ;JEC Uncertainty; Jets",100,0.94,1.06);
		TH1F* h_JEC_uncert_AK4  = new TH1F("h_JEC_uncert_AK4","AK8 JEC Uncertainty ;JEC Uncertainty; Jets",100,0.94,1.06);
		TH1F* h_AK8_JER  = new TH1F("h_AK8_JER","AK8 JER Correction Factor ;Correction Factor; Jets",100,0.94,1.06);



		// event weights by region


		// SR
		TH1F * h_pdf_EventWeight_SR= new TH1F("h_pdf_EventWeight_SR", "PDF event weight (SR) ; event weight; Events",40,0.0,4.0);
		TH1F * h_renorm_EventWeight_SR= new TH1F("h_renorm_EventWeight_SR", "Renorm. event weight  (SR); event weight; Events",40,0.0,2.5);
		TH1F * h_factor_EventWeight_SR= new TH1F("h_factor_EventWeight_SR", "Fact. event weight  (SR); event weight; Events",40,0.0,2.5);
		TH1F * h_scale_EventWeight_SR= new TH1F("h_scale_EventWeight_SR", "Scale event weight (using envelope) (SR); event weight; Events",40,0.0,2.5);

		TH1F* h_PU_eventWeight_SR  = new TH1F("h_PU_eventWeight_SR","Pileup Event Weights  (SR);Event Weight; Events",40,0.0,3.0);
		TH1F* h_bTag_eventWeight_T_SR  = new TH1F("h_bTag_eventWeight_T_SR","b tagging Event Weights (tight WP)  (SR);Event Weight; Events",100,0.0,4.0);
		TH1F* h_bTag_eventWeight_M_SR  = new TH1F("h_bTag_eventWeight_M_SR","b tagging Event Weights (medium WP)  (SR);Event Weight; Events",100,0.0,4.0);
		TH1F* h_L1PrefiringWeight_SR  = new TH1F("h_L1PrefiringWeight_SR","L1 Prefiring Event Weights ;Event Weight  (SR); Events",40,0.0,1.5);
		TH1F* h_topPtWeight_SR  = new TH1F("h_topPtWeight_SR","Top p_{T} Event Weights ;Event Weight  (SR); Events",40,0.0,2.0);

		TH1F* h_JEC_uncert_AK8_SR  = new TH1F("h_JEC_uncert_AK8_SR","AK8 JEC Uncertainty (SR);JEC Uncertainty; Jets",100,0.94,1.06);
		TH1F* h_JEC_uncert_AK4_SR  = new TH1F("h_JEC_uncert_AK4_SR","AK8 JEC Uncertainty (SR);JEC Uncertainty; Jets",100,0.94,1.06);
		TH1F* h_AK8_JER_SR  = new TH1F("h_AK8_JER_SR","AK8 JER Correction Factor (SR);Correction Factor; Jets",100,0.94,1.06);

		// CR
		TH1F * h_pdf_EventWeight_CR= new TH1F("h_pdf_EventWeight_CR", "PDF event weight (CR) ; event weight; Events",40,0.0,4.0);
		TH1F * h_renorm_EventWeight_CR= new TH1F("h_renorm_EventWeight_CR", "Renorm. event weight  (CR); event weight; Events",40,0.0,2.5);
		TH1F * h_factor_EventWeight_CR= new TH1F("h_factor_EventWeight_CR", "Fact. event weight  (CR); event weight; Events",40,0.0,2.5);
		TH1F * h_scale_EventWeight_CR= new TH1F("h_scale_EventWeight_CR", "Scale event weight (using envelope) (CR); event weight; Events",40,0.0,2.5);

		TH1F* h_PU_eventWeight_CR  = new TH1F("h_PU_eventWeight_CR","Pileup Event Weights  (CR);Event Weight; Events",40,0.0,3.0);
		TH1F* h_bTag_eventWeight_T_CR  = new TH1F("h_bTag_eventWeight_T_CR","b tagging Event Weights (tight WP)  (CR);Event Weight; Events",100,0.0,4.0);
		TH1F* h_bTag_eventWeight_M_CR  = new TH1F("h_bTag_eventWeight_M_CR","b tagging Event Weights (medium WP)  (CR);Event Weight; Events",100,0.0,4.0);
		TH1F* h_L1PrefiringWeight_CR  = new TH1F("h_L1PrefiringWeight_CR","L1 Prefiring Event Weights ;Event Weight  (CR); Events",40,0.0,1.5);
		TH1F* h_topPtWeight_CR  = new TH1F("h_topPtWeight_CR","Top p_{T} Event Weights ;Event Weight  (CR); Events",40,0.0,2.0);

		TH1F* h_JEC_uncert_AK8_CR  = new TH1F("h_JEC_uncert_AK8_CR","AK8 JEC Uncertainty (CR);JEC Uncertainty; Jets",100,0.94,1.06);
		TH1F* h_JEC_uncert_AK4_CR  = new TH1F("h_JEC_uncert_AK4_CR","AK8 JEC Uncertainty (CR);JEC Uncertainty; Jets",100,0.94,1.06);
		TH1F* h_AK8_JER_CR  = new TH1F("h_AK8_JER_CR","AK8 JER Correction Factor (CR);Correction Factor; Jets",100,0.94,1.06);

		// AT1b
		TH1F * h_pdf_EventWeight_AT1b= new TH1F("h_pdf_EventWeight_AT1b", "PDF event weight (AT1b) ; event weight; Events",40,0.0,4.0);
		TH1F * h_renorm_EventWeight_AT1b= new TH1F("h_renorm_EventWeight_AT1b", "Renorm. event weight  (AT1b); event weight; Events",40,0.0,2.5);
		TH1F * h_factor_EventWeight_AT1b= new TH1F("h_factor_EventWeight_AT1b", "Fact. event weight  (AT1b); event weight; Events",40,0.0,2.5);
		TH1F * h_scale_EventWeight_AT1b= new TH1F("h_scale_EventWeight_AT1b", "Scale event weight (using envelope) (AT1b); event weight; Events",40,0.0,2.5);

		TH1F* h_PU_eventWeight_AT1b  = new TH1F("h_PU_eventWeight_AT1b","Pileup Event Weights  (AT1b);Event Weight; Events",40,0.0,3.0);
		TH1F* h_bTag_eventWeight_T_AT1b  = new TH1F("h_bTag_eventWeight_T_AT1b","b tagging Event Weights (tight WP)  (AT1b);Event Weight; Events",100,0.0,4.0);
		TH1F* h_bTag_eventWeight_M_AT1b  = new TH1F("h_bTag_eventWeight_M_AT1b","b tagging Event Weights (medium WP)  (AT1b);Event Weight; Events",100,0.0,4.0);
		TH1F* h_L1PrefiringWeight_AT1b  = new TH1F("h_L1PrefiringWeight_AT1b","L1 Prefiring Event Weights ;Event Weight  (AT1b); Events",40,0.0,1.5);
		TH1F* h_topPtWeight_AT1b  = new TH1F("h_topPtWeight_AT1b","Top p_{T} Event Weights ;Event Weight  (AT1b); Events",40,0.0,2.0);

		TH1F* h_JEC_uncert_AK8_AT1b  = new TH1F("h_JEC_uncert_AK8_AT1b","AK8 JEC Uncertainty (AT1b);JEC Uncertainty; Jets",100,0.94,1.06);
		TH1F* h_JEC_uncert_AK4_AT1b  = new TH1F("h_JEC_uncert_AK4_AT1b","AK8 JEC Uncertainty (AT1b);JEC Uncertainty; Jets",100,0.94,1.06);
		TH1F* h_AK8_JER_AT1b  = new TH1F("h_AK8_JER_AT1b","AK8 JER Correction Factor (AT1b);Correction Factor; Jets",100,0.94,1.06);

		// AT0b
		TH1F * h_pdf_EventWeight_AT0b= new TH1F("h_pdf_EventWeight_AT0b", "PDF event weight (AT0b) ; event weight; Events",40,0.0,4.0);
		TH1F * h_renorm_EventWeight_AT0b= new TH1F("h_renorm_EventWeight_AT0b", "Renorm. event weight  (AT0b); event weight; Events",40,0.0,2.5);
		TH1F * h_factor_EventWeight_AT0b= new TH1F("h_factor_EventWeight_AT0b", "Fact. event weight  (AT0b); event weight; Events",40,0.0,2.5);
		TH1F * h_scale_EventWeight_AT0b= new TH1F("h_scale_EventWeight_AT0b", "Scale event weight (using envelope) (AT0b); event weight; Events",40,0.0,2.5);

		TH1F* h_PU_eventWeight_AT0b  = new TH1F("h_PU_eventWeight_AT0b","Pileup Event Weights  (AT0b);Event Weight; Events",40,0.0,3.0);
		TH1F* h_bTag_eventWeight_T_AT0b  = new TH1F("h_bTag_eventWeight_T_AT0b","b tagging Event Weights (tight WP)  (AT0b);Event Weight; Events",100,0.0,4.0);
		TH1F* h_bTag_eventWeight_M_AT0b  = new TH1F("h_bTag_eventWeight_M_AT0b","b tagging Event Weights (medium WP)  (AT0b);Event Weight; Events",100,0.0,4.0);
		TH1F* h_L1PrefiringWeight_AT0b  = new TH1F("h_L1PrefiringWeight_AT0b","L1 Prefiring Event Weights ;Event Weight  (AT0b); Events",40,0.0,1.5);
		TH1F* h_topPtWeight_AT0b  = new TH1F("h_topPtWeight_AT0b","Top p_{T} Event Weights ;Event Weight  (AT0b); Events",40,0.0,2.0);

		TH1F* h_JEC_uncert_AK8_AT0b  = new TH1F("h_JEC_uncert_AK8_AT0b","AK8 JEC Uncertainty (AT0b);JEC Uncertainty; Jets",100,0.94,1.06);
		TH1F* h_JEC_uncert_AK4_AT0b  = new TH1F("h_JEC_uncert_AK4_AT0b","AK8 JEC Uncertainty (AT0b);JEC Uncertainty; Jets",100,0.94,1.06);
		TH1F* h_AK8_JER_AT0b  = new TH1F("h_AK8_JER_AT0b","AK8 JER Correction Factor (AT0b);Correction Factor; Jets",100,0.94,1.06);


		///////////////////////////////
		////////// b-tagging //////////
		///////////////////////////////

		TH1F* h_nLooseBTags = new TH1F("h_nLooseBTags","Number of Loosely b-tagged AK4 Jets; Events",10,-0.5,9.5);
		TH1F* h_nMedBTags = new TH1F("h_nMedBTags","Number of Mediumly b-tagged AK4 Jets; Events",10,-0.5,9.5);
		TH1F* h_nTightBTags = new TH1F("h_nTightBTags","Number of Tightly b-tagged AK4 Jets; Events",10,-0.5,9.5);

		TH1F* h_nMedBTags_pt50 = new TH1F("h_nMedBTags_pt50","Number of Mediumly b-tagged AK4 Jets (p_{T} > 50 GeV); Events",10,-0.5,9.5);
		TH1F* h_nTightBTags_pt50 = new TH1F("h_nTightBTags_pt50","Number of Tightly b-tagged AK4 Jets (p_{T} > 50 GeV); Events",10,-0.5,9.5);

		TH1F* h_nMedBTags_pt75 = new TH1F("h_nMedBTags_pt75","Number of Mediumly b-tagged AK4 Jets (p_{T} > 75 GeV); Events",10,-0.5,9.5);
		TH1F* h_nTightBTags_pt75 = new TH1F("h_nTightBTags_pt75","Number of Tightly b-tagged AK4 Jets (p_{T} > 75 GeV); Events",10,-0.5,9.5);

		TH1F* h_nMedBTags_pt100 = new TH1F("h_nMedBTags_pt100","Number of Mediumly b-tagged AK4 Jets (p_{T} > 100 GeV); Events",10,-0.5,9.5);
		TH1F* h_nTightBTags_pt100 = new TH1F("h_nTightBTags_pt100","Number of Tightly b-tagged AK4 Jets (p_{T} > 100 GeV); Events",10,-0.5,9.5);

		TH1F* h_nMedBTags_pt150 = new TH1F("h_nMedBTags_pt150","Number of Mediumly b-tagged AK4 Jets (p_{T} > 150 GeV); Events",10,-0.5,9.5);
		TH1F* h_nTightBTags_pt150 = new TH1F("h_nTightBTags_pt150","Number of Tightly b-tagged AK4 Jets (p_{T} > 150 GeV); Events",10,-0.5,9.5);


		TH1F* h_AK4_partonFlavour = new TH1F("h_AK4_partonFlavour","AK4 parton Flavour ;parton flavour ; Events",59,-29.5,29.5);

		TH1F* h_AK4_DeepJet_disc  = new TH1F("h_AK4_DeepJet_disc","AK4 DeepFlavour bdisc scores;bdisc",25,0.,1.25);
		TH1F* h_AK4_DeepJet_disc_all  = new TH1F("h_AK4_DeepJet_disc_all","AK4 DeepFlavour bdisc scores;bdisc",25,0.,1.25);

		TH1F* h_true_b_jets_SR  = new TH1F("h_true_b_jets_SR","True (gen-tagged) b AK4 jets per event in the SR; nJets; Events",10,-0.5,9.5);
		TH1F* h_true_b_jets_CR  = new TH1F("h_true_b_jets_CR","True (gen-tagged) b AK4 jets per event in the CR; nJets; Events",10,-0.5,9.5);
		TH1F* h_true_b_jets_AT1b  = new TH1F("h_true_b_jets_AT1b","True (gen-tagged) b AK4 jets per event in the AT1b; nJets; Events",10,-0.5,9.5);
		TH1F* h_true_b_jets_AT0b  = new TH1F("h_true_b_jets_AT0b","True (gen-tagged) b AK4 jets per event in the AT0b; nJets; Events",10,-0.5,9.5);
		TH1F* h_true_b_jets_DT  = new TH1F("h_true_b_jets_DT","True (gen-tagged) b AK4 jets per event in the double tagged regions; nJets; Events",10,-0.5,9.5);
		TH1F* h_true_b_jets_AT  = new TH1F("h_true_b_jets_AT","True (gen-tagged) b AK4 jets per event in the anti-tagged regions; nJets; Events",10,-0.5,9.5);

		TGraph* g_bTagSF_T_vs_HT  = new TGraph();
		g_bTagSF_T_vs_HT->SetTitle("b-tag Event weight (tight WP) as a function of event H_{T}; H_{T} [GeV]; b-tag Event Weight");
		g_bTagSF_T_vs_HT->SetName("g_bTagSF_T_vs_HT");

		TGraph* g_bTagSF_M_vs_HT  = new TGraph();
		g_bTagSF_M_vs_HT->SetTitle("b-tag Event weight (medium WP) as a function of event H_{T}; H_{T} [GeV]; b-tag Event Weight");
		g_bTagSF_M_vs_HT->SetName("g_bTagSF_M_vs_HT");

		TH1F* h_trueb_jets_tight_b_tagged_by_pt = new TH1F("h_trueb_jets_tight_b_tagged_by_pt","The number of true b jets that are tight b-tagged AK4 jets per p_{T} bin; Number of Tagged Jets; Events",50,0.,3000);
		TH1F* h_trueb_jets_med_b_tagged_by_pt   = new TH1F("h_trueb_jets_med_b_tagged_by_pt","The number of true b jets that are med b-tagged AK4 jets per p_{T} bin; Number of Tagged Jets; Events",50,0.,3000);

		TH1F* h_truec_jets_tight_b_tagged_by_pt = new TH1F("h_truec_jets_tight_b_tagged_by_pt","The number of true c jets that are tight b-tagged AK4 jets per p_{T} bin; Number of Tagged Jets; Events",50,0.,3000);
		TH1F* h_truec_jets_med_b_tagged_by_pt   = new TH1F("h_truec_jets_med_b_tagged_by_pt","The number of true c jets that are med b-tagged AK4 jets per p_{T} bin; Number of Tagged Jets; Events",50,0.,3000);

		TH1F* h_trueLight_jets_tight_b_tagged_by_pt = new TH1F("h_trueLight_jets_tight_b_tagged_by_pt","The number of true light jets that are tight b-tagged AK4 jets per p_{T} bin; Number of Tagged Jets; Events",50,0.,3000);
		TH1F* h_trueLight_jets_med_b_tagged_by_pt   = new TH1F("h_trueLight_jets_med_b_tagged_by_pt","The number of true light jets that are med b-tagged AK4 jets per p_{T} bin; Number of Tagged Jets; Events",50,0.,3000);


		TH1F* h_trueb_jets_by_pt = new TH1F("h_trueb_jets_by_pt","The number of AK4 jets per p_{T} bin with |parton flavour| == 5; Number of Tagged Jets; Events",50,0.,3000);
		TH1F* h_truec_jets_by_pt = new TH1F("h_truec_jets_by_pt","The number of AK4 jets per p_{T} bin with |parton flavour| == 4; Number of Tagged Jets; Events",50,0.,3000);
		TH1F* h_trueLight_jets_by_pt = new TH1F("h_trueLight_jets_by_pt","The number of AK4 jets per p_{T} bin with |parton flavour| < 4; Number of Tagged Jets; Events",50,0.,3000);

		///////////////////////////////////////////////////////////////////////
		///////////////////////// NN - based tagging //////////////////////////
		///////////////////////////////////////////////////////////////////////


		TH1F* h_SJ_mass_NN_SR  = new TH1F("h_SJ_mass_NN_SR","SuperJet Mass (Signal Region) (NN-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_NN_SR  = new TH1F("h_disuperjet_mass_NN_SR","diSuperJet Mass (Signal Region) (NN-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH2F *h_MSJ_mass_vs_MdSJ_NN_SR = new TH2F("h_MSJ_mass_vs_MdSJ_NN_SR","Superjet mass vs diSuperjet mass (Signal Region) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		TH1F* h_SJ_mass_NN_CR  = new TH1F("h_SJ_mass_NN_CR","SuperJet Mass (Control Region) (NN-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_NN_CR  = new TH1F("h_disuperjet_mass_NN_CR","diSuperJet Mass (Control Region) (NN-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH2F *h_MSJ_mass_vs_MdSJ_NN_CR = new TH2F("h_MSJ_mass_vs_MdSJ_NN_CR","Superjet mass vs diSuperjet mass (Control Region) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		TH1F* h_SJ_mass_NN_AT1b   = new TH1F("h_SJ_mass_NN_AT1b","SuperJet Mass (AT1b) (NN-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_NN_AT1b  = new TH1F("h_disuperjet_mass_NN_AT1b","diSuperJet Mass (AT1b) (NN-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH2F *h_MSJ_mass_vs_MdSJ_NN_AT1b = new TH2F("h_MSJ_mass_vs_MdSJ_NN_AT1b","Superjet mass vs diSuperjet mass (AT1b) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		TH1F* h_SJ_mass_NN_AT0b  = new TH1F("h_SJ_mass_NN_AT0b","SuperJet Mass (AT0b) (NN-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_NN_AT0b  = new TH1F("h_disuperjet_mass_NN_AT0b","diSuperJet Mass (AT0b) (NN-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH2F *h_MSJ_mass_vs_MdSJ_NN_AT0b = new TH2F("h_MSJ_mass_vs_MdSJ_NN_AT0b","Superjet mass vs diSuperjet mass (AT0b) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		TH1F* h_SJ_mass_NN_AT1tb   = new TH1F("h_SJ_mass_NN_AT1tb","SuperJet Mass (AT1tb) (NN-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_NN_AT1tb  = new TH1F("h_disuperjet_mass_NN_AT1tb","diSuperJet Mass (AT1tb) (NN-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH2F *h_MSJ_mass_vs_MdSJ_NN_AT1tb = new TH2F("h_MSJ_mass_vs_MdSJ_NN_AT1tb","Superjet mass vs diSuperjet mass (AT1tb) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		TH1F* h_SJ_mass_NN_AT0tb  = new TH1F("h_SJ_mass_NN_AT0tb","SuperJet Mass (AT0tb) (NN-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_NN_AT0tb  = new TH1F("h_disuperjet_mass_NN_AT0tb","diSuperJet Mass (AT0tb) (NN-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH2F *h_MSJ_mass_vs_MdSJ_NN_AT0tb = new TH2F("h_MSJ_mass_vs_MdSJ_NN_AT0tb","Superjet mass vs diSuperjet mass (AT0tb) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		TH1F* h_SJ_mass_NN_ADT1b   = new TH1F("h_SJ_mass_NN_ADT1b","SuperJet Mass (ADT1b) (NN-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_NN_ADT1b  = new TH1F("h_disuperjet_mass_NN_ADT1b","diSuperJet Mass (ADT1b) (NN-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH2F *h_MSJ_mass_vs_MdSJ_NN_ADT1b = new TH2F("h_MSJ_mass_vs_MdSJ_NN_ADT1b","Superjet mass vs diSuperjet mass (ADT1b) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		TH1F* h_SJ_mass_NN_ADT0b  = new TH1F("h_SJ_mass_NN_ADT0b","SuperJet Mass (ADT0b) (NN-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_NN_ADT0b  = new TH1F("h_disuperjet_mass_NN_ADT0b","diSuperJet Mass (ADT0b) (NN-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH2F *h_MSJ_mass_vs_MdSJ_NN_ADT0b = new TH2F("h_MSJ_mass_vs_MdSJ_NN_ADT0b","Superjet mass vs diSuperjet mass (ADT0b) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		TH1F* h_true_b_jets_NN_SR  = new TH1F("h_true_b_jets_NN_SR","True (gen-tagged) b AK4 jets per event in the SR; nJets; Events",10,-0.5,9.5);
		TH1F* h_true_b_jets_NN_CR  = new TH1F("h_true_b_jets_NN_CR","True (gen-tagged) b AK4 jets per event in the CR; nJets; Events",10,-0.5,9.5);

		TH1F* h_true_b_jets_NN_AT1b  = new TH1F("h_true_b_jets_NN_AT1b","True (gen-tagged) b AK4 jets per event in the AT1b; nJets; Events",10,-0.5,9.5);
		TH1F* h_true_b_jets_NN_AT0b  = new TH1F("h_true_b_jets_NN_AT0b","True (gen-tagged) b AK4 jets per event in the AT0b; nJets; Events",10,-0.5,9.5);

		TH1F* h_true_b_jets_NN_DT  = new TH1F("h_true_b_jets_NN_DT","True (gen-tagged) b AK4 jets per event in the double tagged regions; nJets; Events",10,-0.5,9.5);
		TH1F* h_true_b_jets_NN_AT  = new TH1F("h_true_b_jets_NN_AT","True (gen-tagged) b AK4 jets per event in the anti-tagged regions; nJets; Events",10,-0.5,9.5);


		///////////////////////////////////////////////////////////////////////
		///////////////////////// side-band plots // //////////////////////////
		///////////////////////////////////////////////////////////////////////

		TH1F* h_totHT_SB  = new TH1F("h_totHT_SB","Event H_{T} (sideband region);H_{T} [GeV]; Events / 200 5GeV",20,1200.,1600);

		TH1F* h_SJ_mass_SB1b		 = new TH1F("h_SJ_mass_SB1b","SuperJet Mass (SB1b) (cut-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_SB1b  = new TH1F("h_disuperjet_mass_SB1b","diSuperJet Mass (SB1b) (cut-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH2F *h_MSJ_mass_vs_MdSJ_SB1b = new TH2F("h_MSJ_mass_vs_MdSJ_SB1b","Superjet mass vs diSuperjet mass (SB1b) (cut-based); diSuperjet mass [GeV];superjet mass", 15,0.0, 8000, 12, 0.0, 3000);  

		TH1F* h_SJ_mass_SB0b		 = new TH1F("h_SJ_mass_SB0b","SuperJet Mass (SB0b) (cut-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
		TH1F* h_disuperjet_mass_SB0b  = new TH1F("h_disuperjet_mass_SB0b","diSuperJet Mass (SB0b) (cut-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
		TH2F *h_MSJ_mass_vs_MdSJ_SB0b = new TH2F("h_MSJ_mass_vs_MdSJ_SB0b","Superjet mass vs diSuperjet mass (SB0b) (cut-based); diSuperjet mass [GeV];superjet mass",  15 ,0.0, 8000, 12, 0.0, 3000);  

   ////////////////////////////////////////////////////////////////////////////////////////////////////////
      t1->SetBranchAddress("eventNumber", &eventNumber); 
		t1->SetBranchAddress("passesPFHT", &passesPFHT); 
		t1->SetBranchAddress("passesPFJet", &passesPFJet); 

		t1->SetBranchAddress("nfatjets", &nfatjets);   
		t1->SetBranchAddress("nSuperJets", &nSuperJets);   
		t1->SetBranchAddress("tot_nAK4_50", &tot_nAK4_50);				//total #AK4 jets (E>50 GeV) for BOTH superjets
		t1->SetBranchAddress("tot_nAK4_70", &tot_nAK4_70);   
		t1->SetBranchAddress("diSuperJet_mass", &diSuperJet_mass);   
		t1->SetBranchAddress("diSuperJet_mass_100", &diSuperJet_mass_100); 
		t1->SetBranchAddress("nfatjet_pre", &nfatjet_pre); 
		t1->SetBranchAddress("jet_pt", jet_pt);   
		t1->SetBranchAddress("jet_eta", jet_eta); 
		t1->SetBranchAddress("jet_phi", jet_phi);   
		t1->SetBranchAddress("jet_mass", jet_mass);   
		t1->SetBranchAddress("SJ_nAK4_50", SJ_nAK4_50);   
		t1->SetBranchAddress("SJ_nAK4_70", SJ_nAK4_70);   
		t1->SetBranchAddress("SJ_mass_50", SJ_mass_50);   
		t1->SetBranchAddress("SJ_mass_70", SJ_mass_70); 
		t1->SetBranchAddress("SJ_mass_150", SJ_mass_150);
		t1->SetBranchAddress("totHT", &totHT);
		t1->SetBranchAddress("SJ_nAK4_300", SJ_nAK4_300);
		t1->SetBranchAddress("SJ_mass_50", SJ_mass_50);
		t1->SetBranchAddress("superJet_mass", superJet_mass);   
		t1->SetBranchAddress("SJ_AK4_50_mass", SJ_AK4_50_mass);   //mass of individual reclustered AK4 jets
		t1->SetBranchAddress("SJ_AK4_70_mass", SJ_AK4_70_mass); 
		t1->SetBranchAddress("SJ_nAK4_150", SJ_nAK4_150);   
		t1->SetBranchAddress("SJ_nAK4_200", SJ_nAK4_200);  
		t1->SetBranchAddress("SJ_nAK4_300", SJ_nAK4_300);     
		t1->SetBranchAddress("SJ_nAK4_400", SJ_nAK4_400);    
		t1->SetBranchAddress("nAK4" , &nAK4); 
		t1->SetBranchAddress("SJ_mass_100", SJ_mass_100);   
		t1->SetBranchAddress("SJ_nAK4_100", SJ_nAK4_100);   
		t1->SetBranchAddress("AK4_eta", AK4_eta); 
		t1->SetBranchAddress("AK4_phi", AK4_phi); 
		t1->SetBranchAddress("AK4_mass", AK4_mass); 
		t1->SetBranchAddress("lab_AK4_pt", AK4_pt); 




		t1->SetBranchAddress("dijetMassOne", &dijetMassOne); 
		t1->SetBranchAddress("dijetMassTwo", &dijetMassTwo); 
		t1->SetBranchAddress("AK4_DeepJet_disc", AK4_DeepJet_disc); 
		t1->SetBranchAddress("fourAK8JetMass", &fourAK8JetMass); 
		t1->SetBranchAddress("diAK8Jet_mass", &diAK8Jet_mass); 

		t1->SetBranchAddress("AK4_fails_veto_map", AK4_fails_veto_map); 
		t1->SetBranchAddress("AK8_fails_veto_map", AK8_fails_veto_map); 

		t1->SetBranchAddress("SJ1_BEST_scores", &SJ1_BEST_scores); 
		t1->SetBranchAddress("SJ2_BEST_scores", &SJ2_BEST_scores); 
		t1->SetBranchAddress("SJ1_decision", &SJ1_decision); 
		t1->SetBranchAddress("SJ2_decision", &SJ2_decision); 

		t1->SetBranchAddress("JEC_uncert_AK8", JEC_uncert_AK8); 
		t1->SetBranchAddress("JEC_uncert_AK4", JEC_uncert_AK4); 

		t1->SetBranchAddress("AK8_JER", AK8_JER); 


		t1->SetBranchAddress("fatjet_isHEM", fatjet_isHEM); 
		t1->SetBranchAddress("jet_isHEM", jet_isHEM); 
		t1->SetBranchAddress("prefiringWeight_nom", &prefiringWeight);

      t1->SetBranchAddress("nTau_VLooseVsJet_VLooseVsMuon_VVLooseVse", &nTau_VLooseVsJet_VLooseVsMuon_VVLooseVse); 
      t1->SetBranchAddress("nMuons_looseID_medIso", &nMuons_looseID_medIso); 
      t1->SetBranchAddress("nElectrons_looseID_looseISO", &nElectrons_looseID_looseISO); 

		// MC-only vars 
		if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos))
		{ 
			// nominal systematics
			t1->SetBranchAddress("bTag_eventWeight_T_nom", &bTag_eventWeight_T_nom); 
			t1->SetBranchAddress("bTag_eventWeight_M_nom", &bTag_eventWeight_M_nom);
			t1->SetBranchAddress("PU_eventWeight_nom", &PU_eventWeight);

			t1->SetBranchAddress("AK4_partonFlavour", AK4_partonFlavour); 
			t1->SetBranchAddress("AK4_hadronFlavour", AK4_HadronFlavour);
			t1->SetBranchAddress("ntrueInt", &ntrueInt);

		}

		pdf_weight = 1.0; 
		scale_weight = 1.0; 
		renormWeight = 1.0;
		factWeight   = 1.0;
		topPtWeight = 1.0;


		if ( (inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos)) 
		{

		
			if (systematic.find("bTag") != std::string::npos)
			{ 
				/// partially split up ----- UNCORRELATED ----- b-tagging systematics (T & M split, bc and light jets considered together)
				if     ((systematic == "bTagSF_tight") && (*systematic_suffix == "up"))  t1->SetBranchAddress("bTag_eventWeight_T_up", &bTag_eventWeight_T_up);
				else if((systematic == "bTagSF_tight") && (*systematic_suffix == "down")) t1->SetBranchAddress("bTag_eventWeight_T_down", &bTag_eventWeight_T_down);
				
				else if     ((systematic == "bTagSF_med") && (*systematic_suffix == "up"))t1->SetBranchAddress("bTag_eventWeight_M_up", &bTag_eventWeight_M_up);
				else if((systematic == "bTagSF_med") && (*systematic_suffix == "down")) t1->SetBranchAddress("bTag_eventWeight_M_down", &bTag_eventWeight_M_down);
				
				/// partially split up ----- CORELLATED ---- b-tagging systematics (T & M split, bc and light jets considered together)
				else if     ((systematic == "bTagSF_tight_corr") && (*systematic_suffix == "up"))t1->SetBranchAddress("bTag_eventWeight_T_corr_up", &bTag_eventWeight_T_corr_up);
				else if((systematic == "bTagSF_tight_corr") && (*systematic_suffix == "down")) t1->SetBranchAddress("bTag_eventWeight_T_corr_down", &bTag_eventWeight_T_corr_down);
				
				else if     ((systematic == "bTagSF_med_corr") && (*systematic_suffix == "up")) t1->SetBranchAddress("bTag_eventWeight_M_corr_up", &bTag_eventWeight_M_corr_up);
				else if((systematic == "bTagSF_med_corr") && (*systematic_suffix == "down"))t1->SetBranchAddress("bTag_eventWeight_M_corr_down", &bTag_eventWeight_M_corr_down);

				/// split up CORRELATED b-tagging systematics
				else if     ((systematic == "bTag_eventWeight_bc_T_corr") && (*systematic_suffix == "up")) t1->SetBranchAddress("bTag_eventWeight_bc_T_corr_up", &bTag_eventWeight_bc_T_corr_up);
				else if((systematic == "bTag_eventWeight_bc_T_corr") && (*systematic_suffix == "down"))t1->SetBranchAddress("bTag_eventWeight_bc_T_corr_down", &bTag_eventWeight_bc_T_corr_down);

				else if     ((systematic == "bTag_eventWeight_bc_M_corr") && (*systematic_suffix == "up"))t1->SetBranchAddress("bTag_eventWeight_bc_M_corr_up", &bTag_eventWeight_bc_M_corr_up);
				else if((systematic == "bTag_eventWeight_bc_M_corr") && (*systematic_suffix == "down"))t1->SetBranchAddress("bTag_eventWeight_bc_M_corr_down", &bTag_eventWeight_bc_M_corr_down);

				else if     ((systematic == "bTag_eventWeight_light_T_corr") && (*systematic_suffix == "up"))t1->SetBranchAddress("bTag_eventWeight_light_T_corr_up", &bTag_eventWeight_light_T_corr_up);
				else if((systematic == "bTag_eventWeight_light_T_corr") && (*systematic_suffix == "down"))t1->SetBranchAddress("bTag_eventWeight_light_T_corr_down", &bTag_eventWeight_light_T_corr_down);

				else if     ((systematic == "bTag_eventWeight_light_M_corr") && (*systematic_suffix == "up"))t1->SetBranchAddress("bTag_eventWeight_light_M_corr_up", &bTag_eventWeight_light_M_corr_up);
				else if((systematic == "bTag_eventWeight_light_M_corr") && (*systematic_suffix == "down"))t1->SetBranchAddress("bTag_eventWeight_light_M_corr_down", &bTag_eventWeight_light_M_corr_down);

				/// split up UNCORRELATED b-tagging systematics
				else if     ((systematic == "bTag_eventWeight_bc_T_year") && (*systematic_suffix == "up"))t1->SetBranchAddress("bTag_eventWeight_bc_T_up", &bTag_eventWeight_bc_T_up);
				else if((systematic == "bTag_eventWeight_bc_T_year") && (*systematic_suffix == "down"))t1->SetBranchAddress("bTag_eventWeight_bc_T_down", &bTag_eventWeight_bc_T_down);

				else if     ((systematic == "bTag_eventWeight_bc_M_year") && (*systematic_suffix == "up")) t1->SetBranchAddress("bTag_eventWeight_bc_M_up", &bTag_eventWeight_bc_M_up);
				else if((systematic == "bTag_eventWeight_bc_M_year") && (*systematic_suffix == "down"))t1->SetBranchAddress("bTag_eventWeight_bc_M_down", &bTag_eventWeight_bc_M_down);

				else if     ((systematic == "bTag_eventWeight_light_T_year") && (*systematic_suffix == "up"))t1->SetBranchAddress("bTag_eventWeight_light_T_up", &bTag_eventWeight_light_T_up);
				else if((systematic == "bTag_eventWeight_light_T_year") && (*systematic_suffix == "down"))t1->SetBranchAddress("bTag_eventWeight_light_T_down", &bTag_eventWeight_light_T_down);

				else if     ((systematic == "bTag_eventWeight_light_M_year") && (*systematic_suffix == "up"))t1->SetBranchAddress("bTag_eventWeight_light_M_up", &bTag_eventWeight_light_M_up);
				else if((systematic == "bTag_eventWeight_light_M_year") && (*systematic_suffix == "down"))t1->SetBranchAddress("bTag_eventWeight_light_M_down", &bTag_eventWeight_light_M_down);
			}
			//////// pileup systematic 
			if     ((systematic == "PUSF") && (*systematic_suffix == "up"))        t1->SetBranchAddress("PU_eventWeight_up", &PU_eventWeight);
			else if((systematic == "PUSF") && (*systematic_suffix == "down")) t1->SetBranchAddress("PU_eventWeight_down", &PU_eventWeight);
			
			//////// pdf weight systematic 
			else if((systematic == "pdf") && (*systematic_suffix == "up"))        t1->SetBranchAddress("PDFWeightUp_BEST", &pdf_weight);
			else if((systematic == "pdf") && (*systematic_suffix == "down")) t1->SetBranchAddress("PDFWeightDown_BEST", &pdf_weight);

			/////// scale stuff 
			//////// renormalization scale systematic 
			else if((systematic == "renorm") && (*systematic_suffix == "up"))   t1->SetBranchAddress("QCDRenormalization_up_BEST", &renormWeight); // alternative:  PDFWeights_renormWeight_up
			else if((systematic == "renorm") && (*systematic_suffix == "down")) t1->SetBranchAddress("QCDRenormalization_down_BEST", &renormWeight); // alternative: PDFWeights_renormWeight_down

			//////// factorization scale systematic 
			else if((systematic == "fact") && (*systematic_suffix == "up"))   t1->SetBranchAddress("QCDFactorization_up_BEST", &factWeight);     // alternative:  PDFWeights_factWeightsRMS_up 
			else if((systematic == "fact") && (*systematic_suffix == "down")) t1->SetBranchAddress("QCDFactorization_down_BEST", &factWeight);     // alternative: PDFWeights_factWeightsRMS_down
			
			//////// renormalization and factorization scale systematics COMBImED
			else if((systematic == "scale") && (*systematic_suffix == "up"))   t1->SetBranchAddress("PDFWeights_envelope_scale_uncertainty_up", &scale_weight); // alternative:  PDFWeights_renormWeight_up
			else if((systematic == "scale") && (*systematic_suffix == "down")) t1->SetBranchAddress("PDFWeights_envelope_scale_uncertainty_down", &scale_weight); // alternative: PDFWeights_renormWeight_down
		   
			//////// prefiring systematic 
			else if((systematic == "L1Prefiring") && (*systematic_suffix == "up"))        t1->SetBranchAddress("prefiringWeight_up", &prefiringWeight);
			else if((systematic == "L1Prefiring") && (*systematic_suffix == "down")) t1->SetBranchAddress("prefiringWeight_down", &prefiringWeight);
			
			//////// top pt systematic 
			else if ( (inFileName.find("TTJets") != std::string::npos) || (inFileName.find("TTTo") != std::string::npos) ) if((systematic == "topPt") && (*systematic_suffix == "up")) t1->SetBranchAddress("top_pt_weight", &topPtWeight);
		}

		int nbTagSF_vs_HT_points = 0;
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
		double sum_eventSF_AT1b = 0, sum_eventSF_AT0b = 0;
		double sum_btagSF_1b_antiTag = 0.0, sum_btagSF_0b_antiTag = 0, sum_btagSF_SR = 0.0, sum_btagSF_CR = 0.0;
		double sum_PUSF_1b_antiTag = 0.0, sum_PUSF_0b_antiTag = 0, sum_PUSF_SR = 0.0, sum_PUSF_CR = 0.0;

		double nEvents_unscaled_1b_antiTag = 0.0,nEvents_unscaled_0b_antiTag = 0,nEvents_unscaled_SR =0, nEvents_unscaled_CR =0;
		int num_bad_btagSF = 0, num_bad_PUSF = 0, num_bad_topPt = 0, num_bad_scale = 0, num_bad_pdf = 0, num_bad_prefiring = 0;
		int badEventSF = 0;

		totEventsUncut = nentries;

	    std::cout << "=========================================" << std::endl;
	    std::cout << "=========================================" << std::endl;
	    std::cout << " WARNING: SR DEFINED BY nMedBTags > 0" << std::endl;
	    std::cout << "=========================================" << std::endl;
	    std::cout << "=========================================" << std::endl;


		for (Int_t i=0;i<nentries;i++) 
		{  
			nomBtaggingWeight=1.0;

			t1->GetEntry(i);

		  ///// APPLY TRIGGER 
		  if ( (!passesPFHT) && (!passesPFJet) ) 
		  {
		  		h_failed_events->Fill(0);  //
		  		continue; // skip events that don't pass at least one trigger
			}
		  	
		  	// apply additional, looser lepton vetoes 
			if ((nTau_VLooseVsJet_VLooseVsMuon_VVLooseVse > 0 ) || (nMuons_looseID_medIso >0) || (nElectrons_looseID_looseISO > 0))
			{
				h_failed_events->Fill(1);
				continue;
			}
			nfatjets_double = 1.0 *nfatjets;
			nfatjets_pre_double = 1.0*nfatjet_pre;
			nAK4_double = 1.0*nAK4;

			h_nAK4_all->Fill(nAK4_double);
			h_nfatjets->Fill(nfatjets_double);
			h_totHT_unscaled->Fill(totHT);

			h_SJ_mass_uncorrected->Fill(superJet_mass[0]);
			h_SJ_mass_uncorrected->Fill(superJet_mass[1]);
			h_disuperjet_mass_uncorrected->Fill(diSuperJet_mass);


			// JET VETO MAPS AND HEM VETOES	
			bool fails_veto_map = false;
			bool fails_HEM      = false;
			for(int iii=0;iii<nfatjets;iii++) // a non-zero value is a bad thing from AK8_fails_veto_map 
			{

				if ((dataYear == "2018")   && (dataBlock.find("dataD") != std::string::npos) )
				{
					if( fatjet_isHEM[iii]  )	  fails_HEM = true; // CHANGED FROM if (AK8_fails_veto_map[iii]) fails_veto_map = true; 
				}

				if( AK8_fails_veto_map[iii]) fails_veto_map = true;
			}

			if(fails_veto_map)
			{
				h_failed_events->Fill(2);
				continue;
			}
			if(fails_HEM) 
			{
				h_failed_events->Fill(3);
				continue; 
			}

			double nAK4_recount = 0;
			double eventScaleFactor = 1.0;
			double bTag_eventWeight_M = 1, bTag_eventWeight_T = 1;

			if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos)  )
			{

				if (!(systematic.find("scale") != std::string::npos)) scale_weight = renormWeight*factWeight;  
				
				h_numTrueInteractions->Fill(ntrueInt);

				////// check MC systematics and make sure they aren't bad
				if ((bTag_eventWeight_T != bTag_eventWeight_T) || (std::isinf(bTag_eventWeight_T)) || (std::isnan(bTag_eventWeight_T)) || (abs(bTag_eventWeight_T) > 100) || (bTag_eventWeight_T < 0.)  )
				{
					bTag_eventWeight_T = 1.0;
					num_bad_btagSF++;
				}
				if ((PU_eventWeight != PU_eventWeight) || (std::isinf(PU_eventWeight))|| (std::isnan(PU_eventWeight)) || (abs(PU_eventWeight) > 100) || (PU_eventWeight < 0.)   )
				{
					PU_eventWeight = 1.0;
					num_bad_PUSF++;
					h_bad_event_weights->Fill(0);
				}
				if ((factWeight != factWeight) || (std::isinf(factWeight))  || (std::isnan(factWeight)) || (abs(factWeight) > 100) || (factWeight < 0. ))
				{
					factWeight = 1.0;
					h_bad_event_weights->Fill(1);
				}

				if ((renormWeight != renormWeight) || (std::isinf(renormWeight))  || (std::isnan(renormWeight)) || (abs(renormWeight) > 100) || (renormWeight < 0.))
				{
					renormWeight = 1.0;
					h_bad_event_weights->Fill(2);
				}
				if ((topPtWeight != topPtWeight) || (std::isinf(topPtWeight)) || (std::isnan(topPtWeight)) || (abs(topPtWeight) > 100) || (topPtWeight < 0.))
				{
					topPtWeight = 1.0;
					num_bad_topPt++;
					h_bad_event_weights->Fill(3);
				}
				if ((pdf_weight != pdf_weight) || (std::isinf(pdf_weight)) || (std::isnan(pdf_weight)) || (abs(pdf_weight) > 100) || (pdf_weight < 0.)  )
				{
					pdf_weight = 1.0;
					num_bad_pdf++;
					h_bad_event_weights->Fill(4);
				}
	 
				eventScaleFactor = PU_eventWeight*topPtWeight;   /// these are all MC-only systematics, the b-tagging, fact, and renorm event weights will be applied after selection

				// set the b-tagging event weight based on the systematic
				// only valid for MC
				bTag_eventWeight_M = bTag_eventWeight_M_nom;
				bTag_eventWeight_T = bTag_eventWeight_T_nom;

				if((systematic.find("bTag") != std::string::npos)) // if this is a btagging uncert, change the weight to be the appropriate variation
				{ 
					/// partially split up ----- UNCORRELATED ----- b-tagging systematics (T & M split, bc and light jets considered together)
					if     ((systematic == "bTagSF_tight") && (*systematic_suffix == "up"))   bTag_eventWeight_T = bTag_eventWeight_T_up;
					else if((systematic == "bTagSF_tight") && (*systematic_suffix == "down")) bTag_eventWeight_T = bTag_eventWeight_T_down;
					
					else if     ((systematic == "bTagSF_med") && (*systematic_suffix == "up"))    bTag_eventWeight_M = bTag_eventWeight_M_up;
					else if((systematic == "bTagSF_med") && (*systematic_suffix == "down"))  bTag_eventWeight_M = bTag_eventWeight_M_down;
					
					/// partially split up ----- CORELLATED ---- b-tagging systematics (T & M split, bc and light jets considered together)
					else if     ((systematic == "bTagSF_tight_corr") && (*systematic_suffix == "up"))    bTag_eventWeight_T = bTag_eventWeight_T_corr_up;
					else if((systematic == "bTagSF_tight_corr") && (*systematic_suffix == "down"))  bTag_eventWeight_T = bTag_eventWeight_T_corr_down;
					
					else if     ((systematic == "bTagSF_med_corr") && (*systematic_suffix == "up"))    bTag_eventWeight_M = bTag_eventWeight_M_corr_up;
					else if((systematic == "bTagSF_med_corr") && (*systematic_suffix == "down"))  bTag_eventWeight_M = bTag_eventWeight_M_corr_down;
					

					/// split up CORRELATED b-tagging systematics
					else if     ((systematic == "bTag_eventWeight_bc_T_corr") && (*systematic_suffix == "up"))    bTag_eventWeight_T = bTag_eventWeight_bc_T_corr_up;
					else if((systematic == "bTag_eventWeight_bc_T_corr") && (*systematic_suffix == "down"))  bTag_eventWeight_T = bTag_eventWeight_bc_T_corr_down;

					else if     ((systematic == "bTag_eventWeight_bc_M_corr") && (*systematic_suffix == "up"))     bTag_eventWeight_M = bTag_eventWeight_bc_M_corr_up;
					else if((systematic == "bTag_eventWeight_bc_M_corr") && (*systematic_suffix == "down"))    bTag_eventWeight_M = bTag_eventWeight_bc_M_corr_down;

					else if     ((systematic == "bTag_eventWeight_light_T_corr") && (*systematic_suffix == "up"))    bTag_eventWeight_T = bTag_eventWeight_light_T_corr_up;
					else if((systematic == "bTag_eventWeight_light_T_corr") && (*systematic_suffix == "down"))  bTag_eventWeight_T = bTag_eventWeight_light_T_corr_down;
	 
					else if     ((systematic == "bTag_eventWeight_light_M_corr") && (*systematic_suffix == "up"))      bTag_eventWeight_M = bTag_eventWeight_light_M_corr_up;
					else if((systematic == "bTag_eventWeight_light_M_corr") && (*systematic_suffix == "down"))     bTag_eventWeight_M = bTag_eventWeight_light_M_corr_down;


					/// split up UNCORRELATED b-tagging systematics
					else if     ((systematic == "bTag_eventWeight_bc_T_year") && (*systematic_suffix == "up"))    bTag_eventWeight_T = bTag_eventWeight_bc_T_up;
					else if((systematic == "bTag_eventWeight_bc_T_year") && (*systematic_suffix == "down"))  bTag_eventWeight_T = bTag_eventWeight_bc_T_down;

					else if     ((systematic == "bTag_eventWeight_bc_M_year") && (*systematic_suffix == "up"))     bTag_eventWeight_M = bTag_eventWeight_bc_M_up;
					else if((systematic == "bTag_eventWeight_bc_M_year") && (*systematic_suffix == "down"))    bTag_eventWeight_M = bTag_eventWeight_bc_M_down;
	 
					else if     ((systematic == "bTag_eventWeight_light_T_year") && (*systematic_suffix == "up"))   bTag_eventWeight_T = bTag_eventWeight_light_T_up;
					else if((systematic == "bTag_eventWeight_light_T_year") && (*systematic_suffix == "down")) bTag_eventWeight_T = bTag_eventWeight_light_T_down;

					else if     ((systematic == "bTag_eventWeight_light_M_year") && (*systematic_suffix == "up"))    bTag_eventWeight_M = bTag_eventWeight_light_M_up;
					else if((systematic == "bTag_eventWeight_light_M_year") && (*systematic_suffix == "down"))   bTag_eventWeight_M = bTag_eventWeight_light_M_down;

					g_bTagSF_T_vs_HT->SetPoint(nbTagSF_vs_HT_points, totHT, bTag_eventWeight_T);
					g_bTagSF_M_vs_HT->SetPoint(nbTagSF_vs_HT_points, totHT, bTag_eventWeight_M);

					nbTagSF_vs_HT_points++;
				}
				////// check MC systematics
				if ((bTag_eventWeight_M != bTag_eventWeight_M) || (std::isinf(bTag_eventWeight_M)) || (std::isnan(bTag_eventWeight_M)) || (abs(bTag_eventWeight_M) > 100) || (bTag_eventWeight_M < 0.)  )
				{
					bTag_eventWeight_M = 1.0;
					//std::cout << "event weight was bad!!" << std::endl;
					num_bad_btagSF++;
					h_bad_event_weights->Fill(5);
				}	
			} 

			////// check data systematics
			if ((prefiringWeight != prefiringWeight) || (std::isinf(prefiringWeight)) || (abs(prefiringWeight) > 100) || (prefiringWeight < 0.001)   )
			{
				prefiringWeight = 1.0;
				num_bad_prefiring++;
				h_bad_event_weights->Fill(6);
			}

			eventScaleFactor *= prefiringWeight;   // these are the non-MC-only systematics

			if ((eventScaleFactor != eventScaleFactor) || (std::isinf(eventScaleFactor)) ||  (std::isnan(eventScaleFactor)) || (abs(eventScaleFactor) > 100) || (abs(eventScaleFactor) < 0.001)  )
			{
				//std::cout << "ERROR: failed event scale factor on " << systematic << "_" << *systematic_suffix << std::endl;
				badEventSF++;
				h_bad_event_weights->Fill(7);
				h_failed_events->Fill(4);
				continue;
			}


			h_SJ_mass->Fill(superJet_mass[0],eventScaleFactor);
			h_SJ_mass->Fill(superJet_mass[1],eventScaleFactor);
			h_disuperjet_mass->Fill(diSuperJet_mass, eventScaleFactor);

			for(int iii=0; iii<nAK4; iii++)
			{
				if(AK4_pt[iii] > 30.)nAK4_recount+=1;
				h_JEC_uncert_AK4->Fill(JEC_uncert_AK4[iii]);
				h_AK4_eta->Fill(AK4_eta[iii], eventScaleFactor);
				h_AK4_phi->Fill(AK4_phi[iii], eventScaleFactor);
			}

			h_pdf_EventWeight->Fill(pdf_weight);
			h_renorm_EventWeight->Fill(renormWeight);
			h_factor_EventWeight->Fill(factWeight);
			h_scale_EventWeight->Fill(scale_weight);

			h_PU_eventWeight->Fill(PU_eventWeight);
			h_bTag_eventWeight_T->Fill(bTag_eventWeight_T);
			h_bTag_eventWeight_M->Fill(bTag_eventWeight_M);
			h_L1PrefiringWeight->Fill(prefiringWeight);


			int nTightBTags = 0, nMedBTags = 0, nLooseBtags =0;
			int nAK4_pt50 = 0, nAK4_pt75 = 0, nAK4_pt100 = 0, nAK4_pt150 =0;
			int nMedBTags_pt50 = 0, nMedBTags_pt75 = 0, nMedBTags_pt100 = 0, nMedBTags_pt150 =0;
			int nTightBTags_pt30 = 0, nTightBTags_pt50 = 0, nTightBTags_pt75 = 0, nTightBTags_pt100 = 0, nTightBTags_pt150 =0;

			int nGenBJets;
			for(int iii = 0;iii< nAK4; iii++)
			{

				largest_JEC_corr_AK4 = max(abs(1.0-JEC_uncert_AK4[iii]),largest_JEC_corr_AK4);
				avg_JEC_corr_AK4 += abs(1.0-JEC_uncert_AK4[iii]);
				total_jets_AK4++;

				// try different AK4 pt cuts
				if (AK4_pt[iii] > 150) 
				{
					nAK4_pt150++;
					if ( AK4_DeepJet_disc[iii] > tightDeepCSV_DeepJet ) nTightBTags_pt150++;
					if  (AK4_DeepJet_disc[iii] > medDeepCSV_DeepJet )   nMedBTags_pt150++;
				}
				if (AK4_pt[iii] > 100)
				{
					nAK4_pt100++;
					if ( AK4_DeepJet_disc[iii] > tightDeepCSV_DeepJet ) nTightBTags_pt100++;
					if  (AK4_DeepJet_disc[iii] > medDeepCSV_DeepJet )   nMedBTags_pt100++;
				}
				if (AK4_pt[iii] > 75)
				{
					nAK4_pt75++;
					if ( AK4_DeepJet_disc[iii] > tightDeepCSV_DeepJet ) nTightBTags_pt75++;
					if  (AK4_DeepJet_disc[iii] > medDeepCSV_DeepJet )   nMedBTags_pt75++;
				}
				if (AK4_pt[iii] > 50)
				{
					nAK4_pt50++;
					if ( AK4_DeepJet_disc[iii] > tightDeepCSV_DeepJet ) nTightBTags_pt50++;
					if  (AK4_DeepJet_disc[iii] > medDeepCSV_DeepJet )   nMedBTags_pt50++;
				}

				h_AK4_DeepJet_disc->Fill(AK4_DeepJet_disc[iii]);
				if ( (AK4_DeepJet_disc[iii] > tightDeepCSV_DeepJet ) && (AK4_pt[iii] > 70.))
				{
					if(abs(AK4_HadronFlavour[iii]) == 5) h_trueb_jets_tight_b_tagged_by_pt->Fill(AK4_pt[iii]);
					else if(abs(AK4_HadronFlavour[iii]) == 4) h_truec_jets_tight_b_tagged_by_pt->Fill(AK4_pt[iii]);
					else if(abs(AK4_HadronFlavour[iii]) == 0) h_trueLight_jets_tight_b_tagged_by_pt->Fill(AK4_pt[iii]);				
					nTightBTags++;
				} 
				if ( (AK4_DeepJet_disc[iii] > medDeepCSV_DeepJet )   && (AK4_pt[iii] > 70.)) 
				{
					if(abs(AK4_HadronFlavour[iii]) == 5) h_trueb_jets_med_b_tagged_by_pt->Fill(AK4_pt[iii]);
					else if(abs(AK4_HadronFlavour[iii]) == 4) h_truec_jets_med_b_tagged_by_pt->Fill(AK4_pt[iii]);
					else if(abs(AK4_HadronFlavour[iii]) == 0) h_trueLight_jets_med_b_tagged_by_pt->Fill(AK4_pt[iii]);
					nMedBTags++; 
				}
				if ( (AK4_DeepJet_disc[iii] > looseDeepCSV_DeepJet ) && (AK4_pt[iii] > 70.)) nLooseBtags++;

				if(abs(AK4_HadronFlavour[iii]) == 5)
			  	{
			  		h_trueb_jets_by_pt->Fill(AK4_pt[iii]);
			  		nGenBJets++;
			  	} 
				else if(abs(AK4_HadronFlavour[iii]) == 4)
			  	{
			  		h_truec_jets_by_pt->Fill(AK4_pt[iii]);
			  	} 
				else if(abs(AK4_HadronFlavour[iii]) == 0)
			  	{
			  		h_trueLight_jets_by_pt->Fill(AK4_pt[iii]);
			  	} 
			}

			nfatjets_double = 1.0 *nfatjets;
			nfatjets_pre_double = 1.0*nfatjet_pre;
			nAK4_double = 1.0*nAK4;

			h_nAK4_all->Fill(nAK4_double,eventScaleFactor);
			h_totHT->Fill(totHT,eventScaleFactor);


			double allEventWeights = prefiringWeight;
			double L1prefiringAndTopPt = prefiringWeight;
			double L1prefiringAndTopPtAndPU = prefiringWeight;

			double allEventWeights_noBtag = prefiringWeight;

			if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos)) 
			{
				L1prefiringAndTopPt       *= topPtWeight;
				L1prefiringAndTopPtAndPU  *= (topPtWeight*PU_eventWeight);
				allEventWeights_noBtag    *= (PU_eventWeight*topPtWeight* scale_weight*pdf_weight);
				allEventWeights           *= (PU_eventWeight*topPtWeight* scale_weight*pdf_weight*bTag_eventWeight_M);
			}


			if (verbose)
			{
				std::cout << "eventScaleFactor (just L1 prefiring + PU + top pt) is " << eventScaleFactor<< std::endl;
				std::cout << "L1prefiringAndTopPt is " << L1prefiringAndTopPt << std::endl;
				std::cout << "L1prefiringAndTopPtAndPU is " << L1prefiringAndTopPtAndPU << std::endl;
				std::cout << "allEventWeights is " << allEventWeights << std::endl;
				std::cout << "allEventWeights_noBtag is " << allEventWeights_noBtag << std::endl;
			
			}


			//std::cout << "---- New event ----" << std::endl;
			for(int iii = 0 ; iii < nfatjets; iii++)
			{
				h_AK8_jet_mass->Fill(jet_mass[iii],eventScaleFactor);
				h_AK8_jet_pt->Fill(jet_pt[iii],eventScaleFactor);
				h_JEC_uncert_AK8->Fill(JEC_uncert_AK8[iii]);
				h_AK8_JER->Fill(AK8_JER[iii]);


				largest_JEC_corr = max(abs(1.0-JEC_uncert_AK8[iii]),largest_JEC_corr);
				avg_JEC_corr += abs(1.0-JEC_uncert_AK8[iii]);
				total_jets++;

				//std::cout << "AK8 jet #" << iii << ", JEC uncert value is " <<JEC_uncert_AK8[iii] << std::endl;

				h_AK8_eta->Fill(jet_eta[iii], eventScaleFactor);
				h_AK8_phi->Fill(jet_phi[iii], eventScaleFactor);

			}	


			if(nMedBTags > 0) total_1b++;
			else { total_0b++;}

			nEvents+=eventScaleFactor;


			if(runType == "main-band")
			{
				if ( (totHT < 1600.)    )
				{
					h_failed_events->Fill(5);
					continue;
				}
			}
			else if(runType == "side-band")
			{
				if ( (totHT > 1600.)  || (totHT < 1200)   )
				{
					h_failed_events->Fill(5);
					continue;
				}
			}

			h_nfatjets->Fill(nfatjets_double,eventScaleFactor);

			nHTcut+=eventScaleFactor;

			if( (nfatjets < 3) )
			{
				h_failed_events->Fill(6);
				continue;
			}

			nAK8JetCut+=eventScaleFactor;

			h_nfatjets_pre->Fill(nfatjets_pre_double,eventScaleFactor);
			h_dijet_mass->Fill(dijetMassOne, eventScaleFactor);
			h_dijet_mass->Fill(dijetMassTwo, eventScaleFactor);


			if ((nfatjet_pre < 2) && ( (dijetMassOne < 1000. ) || ( dijetMassTwo < 1000.)  ))
			{
				h_failed_events->Fill(7);
				continue;
			} 

			nHeavyAK8Cut+=eventScaleFactor;
			h_nAK4->Fill(nAK4);
			double eventWeightToUse = eventScaleFactor; 
		
			if (eventWeightToUse< 0.001)  std::cout << "ERROR: bad eventWeightToUse for " <<dataBlock << "/" << systematic << "/" << dataYear << ", value = " << eventWeightToUse <<std::endl;

			if(verbose)
			{
				std::cout << "-------------------------------------------------------------------------------------------------------------" << std::endl;
				std::cout << "Event number " << eventnum << ", systematic is " << systematic << "_" << *systematic_suffix << std::endl;

				std::cout << "bTag_eventWeight_M_up: " << bTag_eventWeight_M_up<< std::endl;
				std::cout << "bTag_eventWeight_M_down: " << bTag_eventWeight_M_down<< std::endl;
				std::cout << "bTag_eventWeight_M_corr_up: " << bTag_eventWeight_M_corr_up<< std::endl;
				std::cout << "bTag_eventWeight_M_corr_down: " << bTag_eventWeight_M_corr_down<< std::endl;
				std::cout << "bTag_eventWeight_bc_M_corr_up: " << bTag_eventWeight_bc_M_corr_up<< std::endl;
				std::cout << "bTag_eventWeight_bc_M_corr_down: " << bTag_eventWeight_bc_M_corr_down << std::endl;
				std::cout << "bTag_eventWeight_light_M_corr_up: " <<bTag_eventWeight_light_M_corr_up << std::endl;
				std::cout << "bTag_eventWeight_light_M_corr_down: " << bTag_eventWeight_light_M_corr_down << std::endl;
				std::cout << "bTag_eventWeight_bc_M_up: " << bTag_eventWeight_bc_M_up << std::endl;
				std::cout << "bTag_eventWeight_bc_M_down: " << bTag_eventWeight_bc_M_down << std::endl;
				std::cout << "bTag_eventWeight_light_M_up: " << bTag_eventWeight_light_M_up << std::endl;
				std::cout << "bTag_eventWeight_light_M_down: " << bTag_eventWeight_light_M_down << std::endl;
				std::cout << "bTag_eventWeight_M_nom: " << bTag_eventWeight_M_nom << std::endl;

				std::cout << "======= the used event scale factor is --- " << bTag_eventWeight_M << " ---" << std::endl; 
				//std::cout << "Event number " << eventnum << ", systematic is " << systematic << "_" << *systematic_suffix << ".   Is this bTag_eventWeight_light_M_corr_up/bTag_eventWeight_light_M_corr_down? " << ((systematic == "bTag_eventWeight_light_M_corr") && (*systematic_suffix == "up")) << "/" << ((systematic == "bTag_eventWeight_light_M_corr") && (*systematic_suffix == "down")) << ". Nom b tag weight is " <<  nomBtaggingWeight << ", used systematic weight is " << bTag_eventWeight_M << std::endl;
			}

			///////////////////////////////////////////////////////
			/////////////////// main-band /////////////////////////
			///////////////////////////////////////////////////////

		

			if(runType == "main-band")
			{
				///////////////////////////////////////////////////////
				////////////////////// b-tagging //////////////////////
				///////////////////////////////////////////////////////

				eventnum++;
				for(int iii = 0;iii< nAK4; iii++)
				{
					//if(AK4_pt[iii] > 80.) _nAK4++;
					h_AK4_DeepJet_disc_all->Fill(AK4_DeepJet_disc[iii],eventWeightToUse);
				}    
				
				h_nTightBTags->Fill(nTightBTags,eventWeightToUse);
				h_nMedBTags->Fill(nMedBTags,eventWeightToUse);
				h_nLooseBTags->Fill(nLooseBtags,eventWeightToUse);

				h_nTightBTags_pt50->Fill(1.0*nTightBTags_pt50,eventWeightToUse);
				h_nMedBTags_pt50->Fill(1.0*nMedBTags_pt50,eventWeightToUse);
				h_nAK4_pt50->Fill(1.0*nAK4_pt50,eventWeightToUse);

				h_nTightBTags_pt75->Fill(1.0*nTightBTags_pt75,eventWeightToUse);
				h_nMedBTags_pt75->Fill(1.0*nMedBTags_pt75,eventWeightToUse);
				h_nAK4_pt75->Fill(1.0*nAK4_pt75,eventWeightToUse);

				h_nTightBTags_pt100->Fill(1.0*nTightBTags_pt100,eventWeightToUse);
				h_nMedBTags_pt100->Fill(1.0*nMedBTags_pt100,eventWeightToUse);
				h_nAK4_pt100->Fill(1.0*nAK4_pt100,eventWeightToUse);

				h_nTightBTags_pt150->Fill(1.0*nTightBTags_pt150,eventWeightToUse);
				h_nMedBTags_pt150->Fill(1.0*nTightBTags_pt150,eventWeightToUse);
				h_nAK4_pt150->Fill(1.0*nAK4_pt150,eventWeightToUse);


				h_SJ1_BEST_score->Fill( SJ1_BEST_scores  ,eventWeightToUse);
				h_SJ2_BEST_score->Fill( SJ2_BEST_scores,eventWeightToUse);

				if (SJ2_BEST_scores > BEST_WP )  h_SJ2_decision->Fill( 1.0 ,eventWeightToUse);
				else { h_SJ2_decision->Fill( 0.0 ,eventWeightToUse);  }
				if (SJ1_BEST_scores > BEST_WP ) h_SJ1_decision->Fill( 1.0,eventWeightToUse);
				else {  h_SJ1_decision->Fill( 0.0,eventWeightToUse);   }

				///////////////////////////////
				////////// 0b region //////////
				///////////////////////////////

				double eventWeightToUse_preBtag = eventWeightToUse;

				if( nMedBTags < 1 ) 
				{

					h_nCA4_300_0b->Fill(SJ_nAK4_300[0],eventWeightToUse);
					h_nCA4_300_0b->Fill(SJ_nAK4_300[1],eventWeightToUse);

					if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos))
				  {
				  		// check b-tag event weight problem


				  		if(bTag_eventWeight_M < 0)
				  		{
				  		 std::cout << "ERROR: bad bTag_eventWeight_M for " <<dataBlock << "/" << systematic << "/" << dataYear << ", value = " << bTag_eventWeight_M <<std::endl;
				  		 bTag_eventWeight_M = 1.0;
				  		}

				  		eventWeightToUse*=bTag_eventWeight_M;
						
				  } 

				  ///////////////////////////////////
				  /////// tagging study stuff ///////
				  ///////////////////////////////////


				  double eventWeightToUse_taggingStudy = eventWeightToUse*pdf_weight*scale_weight;   
				  double eventWeightToUse_taggingStudy_noBTag = eventWeightToUse_preBtag*pdf_weight*scale_weight;   

					h_SJ_mass_total_SJs_0b->Fill(superJet_mass[0],eventWeightToUse_taggingStudy);
					h_SJ_mass_total_SJs_0b->Fill(superJet_mass[1],eventWeightToUse_taggingStudy);

					h_SJ_mass_total_SJs->Fill(superJet_mass[0],eventWeightToUse_taggingStudy_noBTag);
					h_SJ_mass_total_SJs->Fill(superJet_mass[1],eventWeightToUse_taggingStudy_noBTag);

					// SJ1 tag
					if(   (SJ_nAK4_300[0]>=2) && (SJ_mass_100[0]>400.)   )
					{
						h_SJ_mass_tagged_SJs_0b->Fill(superJet_mass[0],eventWeightToUse_taggingStudy);
						h_SJ_mass_tagged_SJs->Fill(superJet_mass[0],eventWeightToUse_taggingStudy_noBTag);
					}
					// SJ2 tag
					if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
					{
						h_SJ_mass_tagged_SJs_0b->Fill(superJet_mass[1],eventWeightToUse_taggingStudy);
						h_SJ_mass_tagged_SJs->Fill(superJet_mass[1],eventWeightToUse_taggingStudy_noBTag);
					}

					// SJ1 cut-based antitag, SJ2 tag
					if(   (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<150.)   )
					{
						h_SJ2_mass_total_SJs_ATSJ1_0b->Fill(superJet_mass[1],eventWeightToUse_taggingStudy);
						h_SJ2_mass_total_SJs_ATSJ1->Fill(superJet_mass[1],eventWeightToUse_taggingStudy_noBTag);
						if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
						{
							h_SJ2_mass_tagged_SJs_ATSJ1_0b->Fill(superJet_mass[1],eventWeightToUse_taggingStudy);
							h_SJ2_mass_tagged_SJs_ATSJ1->Fill(superJet_mass[1],eventWeightToUse_taggingStudy_noBTag);
						}
					}
					// SJ2 cut-based antitag, SJ2 tag
					if(   (SJ_nAK4_50[1]<1) && (SJ_mass_100[1]<150.)   )
					{
						h_SJ1_mass_total_SJs_ATSJ2_0b->Fill(superJet_mass[0],eventWeightToUse_taggingStudy);
						h_SJ1_mass_total_SJs_ATSJ2->Fill(superJet_mass[0],eventWeightToUse_taggingStudy_noBTag);
						if((SJ_nAK4_300[0]>=2) && (SJ_mass_100[0]>=400.)   )
						{
							h_SJ1_mass_tagged_SJs_ATSJ2_0b->Fill(superJet_mass[0],eventWeightToUse_taggingStudy);
							h_SJ1_mass_tagged_SJs_ATSJ2->Fill(superJet_mass[0],eventWeightToUse_taggingStudy_noBTag);
						}
					}

					/// NN-based tagging

					// SJ1 tag
					if(   SJ1_BEST_scores > BEST_WP ) // should kill some of the ST BR
					{
						h_SJ_mass_tagged_SJs_0b_NN->Fill(superJet_mass[0],eventWeightToUse_taggingStudy);
						h_SJ_mass_tagged_SJs_NN->Fill(superJet_mass[0],eventWeightToUse_taggingStudy_noBTag);
					}
					// SJ2 tag
					if(  SJ2_BEST_scores > BEST_WP   )
					{
						h_SJ_mass_tagged_SJs_0b_NN->Fill(superJet_mass[1],eventWeightToUse_taggingStudy);
						h_SJ_mass_tagged_SJs_NN->Fill(superJet_mass[1],eventWeightToUse_taggingStudy_noBTag);
					}

					// SJ1 antitag
					if(  SJ1_BEST_scores < BEST_AT_WP   )
					{
						h_SJ2_mass_total_SJs_ATSJ1_0b_NN->Fill(superJet_mass[1],eventWeightToUse_taggingStudy);
						h_SJ2_mass_total_SJs_ATSJ1_NN->Fill(superJet_mass[1],eventWeightToUse_taggingStudy_noBTag);

						h_SJ2_BEST_score_0b_SJ1AT->Fill( SJ2_BEST_scores,eventWeightToUse_taggingStudy);
						h_SJ2_BEST_score_SJ1AT->Fill( SJ2_BEST_scores,eventWeightToUse_taggingStudy_noBTag);

						if (SJ2_BEST_scores > BEST_WP)  
						{
							h_SJ2_decision_SJ1AT->Fill( 1, eventWeightToUse_taggingStudy_noBTag);
							h_SJ2_decision_0b_SJ1AT->Fill(1,eventWeightToUse_taggingStudy);
							h_SJ2_mass_tagged_SJs_ATSJ1_0b_NN->Fill(superJet_mass[1],eventWeightToUse_taggingStudy);
							h_SJ2_mass_tagged_SJs_ATSJ1_NN->Fill(superJet_mass[1],eventWeightToUse_taggingStudy_noBTag);
						}
						else
						{ 
							h_SJ2_decision_SJ1AT->Fill( 0.0, eventWeightToUse_taggingStudy_noBTag); 
							h_SJ2_decision_0b_SJ1AT->Fill(0.0,eventWeightToUse_taggingStudy); 
						} 
					}


					// SJ2 antitag
					if(   SJ2_BEST_scores < BEST_AT_WP   )
					{
						h_SJ1_mass_total_SJs_ATSJ2_0b_NN->Fill(superJet_mass[0],eventWeightToUse_taggingStudy);
						h_SJ1_mass_total_SJs_ATSJ2_NN->Fill(superJet_mass[0],eventWeightToUse_taggingStudy_noBTag);

						h_SJ1_BEST_score_0b_SJ2AT->Fill( SJ1_BEST_scores,eventWeightToUse_taggingStudy);
						h_SJ1_BEST_score_SJ2AT->Fill( SJ1_BEST_scores,eventWeightToUse_taggingStudy_noBTag);

						// SJ1 tag
						if (SJ1_BEST_scores > BEST_WP) 
						{
							h_SJ1_decision_SJ2AT->Fill( 1, eventWeightToUse_taggingStudy_noBTag);
							h_SJ1_decision_0b_SJ2AT->Fill(1,eventWeightToUse_taggingStudy);

							h_SJ1_mass_tagged_SJs_ATSJ2_0b_NN->Fill(superJet_mass[0],eventWeightToUse_taggingStudy);
							h_SJ1_mass_tagged_SJs_ATSJ2_NN->Fill(superJet_mass[0],eventWeightToUse_taggingStudy_noBTag);
						}
						else 
						{  
							h_SJ1_decision_SJ2AT->Fill( 0.0, eventWeightToUse_taggingStudy_noBTag); 
							h_SJ1_decision_0b_SJ2AT->Fill(0.0,eventWeightToUse_taggingStudy);
						}
					}




					//////////////////////////////////////////

				
					h_SJ2_BEST_score_0b->Fill(SJ2_BEST_scores,eventWeightToUse);
					if ( SJ2_BEST_scores > BEST_WP) h_SJ2_decision_0b->Fill(1,eventWeightToUse);
					else { h_SJ2_decision_0b->Fill(0.0,eventWeightToUse); }

					h_SJ1_BEST_score_0b->Fill(SJ1_BEST_scores,eventWeightToUse);
					if ( SJ1_BEST_scores > BEST_WP) h_SJ1_decision_0b->Fill(1,eventWeightToUse);
					else { h_SJ1_decision_0b->Fill(0.0,eventWeightToUse); }

					
					
					nNoBjets+=eventScaleFactor;
					h_SJ_nAK4_100_CR->Fill(SJ_nAK4_100[0],eventWeightToUse);
					h_SJ_nAK4_100_CR->Fill(SJ_nAK4_100[1],eventWeightToUse);

					h_SJ_nAK4_200_CR->Fill(SJ_nAK4_200[0],eventWeightToUse);
					h_SJ_nAK4_200_CR->Fill(SJ_nAK4_200[1],eventWeightToUse);

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


					////////////////////////////////////////////////////////////
					///////////////////// cut-based tagging ////////////////////
					////////////////////////////////////////////////////////////


					///////////////////
					/////// CR ////////
					///////////////////

					if(   (SJ_nAK4_300[0]>=2) && (SJ_mass_100[0]>400.)   )
					{
						if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
						{
							eventWeightToUse *= pdf_weight*scale_weight;   

							h_pdf_EventWeight_CR->Fill(pdf_weight);
							h_renorm_EventWeight_CR->Fill(renormWeight);
							h_factor_EventWeight_CR->Fill(factWeight);
							h_scale_EventWeight_CR->Fill(scale_weight);
							h_PU_eventWeight_CR->Fill(PU_eventWeight);
							h_bTag_eventWeight_T_CR->Fill(bTag_eventWeight_T);
							h_bTag_eventWeight_M_CR->Fill(bTag_eventWeight_M);
							h_L1PrefiringWeight_CR->Fill(prefiringWeight);
							h_topPtWeight_CR->Fill(topPtWeight);


							//std::cout << "------------ In the CR for " << systematic << "/" << *systematic_suffix<< " and event number " << eventnum << " : bTag_eventWeight_M is " << bTag_eventWeight_M  <<     std::endl;

							h_disuperjet_mass_CR->Fill(diSuperJet_mass,eventWeightToUse);
							h_SJ_mass_CR->Fill( (superJet_mass[0]+superJet_mass[1])/2. ,eventWeightToUse );
							h_totHT_CR->Fill(totHT,eventWeightToUse);
							nDoubleTaggedCR+=eventScaleFactor;
							h_MSJ_mass_vs_MdSJ_CR->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2   ,eventWeightToUse );
							h_MSJ1_vs_MSJ2_CR->Fill(superJet_mass[0],superJet_mass[1],eventWeightToUse);
							sum_eventSF_CR+=eventWeightToUse;
							nEvents_unscaled_CR+=1;
							h_true_b_jets_DT->Fill(nGenBJets);
							h_true_b_jets_CR->Fill(nGenBJets);
							for(int iii=0; iii<nfatjets; iii++)
							{
								h_JEC_uncert_AK8_CR->Fill(JEC_uncert_AK8[iii]);
								h_AK8_JER_CR->Fill(AK8_JER[iii]);
							}
							for(int iii=0; iii<nAK4; iii++)
							{
								h_JEC_uncert_AK4_CR->Fill(JEC_uncert_AK4[iii]);
							}
						}

					}

					///////////////////
					////// AT0b ///////
					///////////////////

					//// SJ1 antitag
					else if(   (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<150.)   )
					{
						if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
						{
							
							eventWeightToUse *= pdf_weight*scale_weight;  //

							h_pdf_EventWeight_AT0b->Fill(pdf_weight);
							h_renorm_EventWeight_AT0b->Fill(renormWeight);
							h_factor_EventWeight_AT0b->Fill(factWeight);
							h_scale_EventWeight_AT0b->Fill(scale_weight);
							h_PU_eventWeight_AT0b->Fill(PU_eventWeight);
							h_bTag_eventWeight_T_AT0b->Fill(bTag_eventWeight_T);
							h_bTag_eventWeight_M_AT0b->Fill(bTag_eventWeight_M);
							h_L1PrefiringWeight_AT0b->Fill(prefiringWeight);
							h_topPtWeight_AT0b->Fill(topPtWeight);


							//std::cout << "------------ In the AT0b for " << systematic << "/" << *systematic_suffix<< " and event number " << eventnum << " : bTag_eventWeight_M is " << bTag_eventWeight_M  <<     std::endl;

							h_totHT_AT0b->Fill(totHT,eventWeightToUse);

							nZeroBtagAntiTag+=eventScaleFactor;
							h_MSJ_mass_vs_MdSJ_AT0b->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse);
							h_disuperjet_mass_AT0b->Fill(diSuperJet_mass,eventWeightToUse);
							h_SJ_mass_AT0b->Fill(superJet_mass[1],eventWeightToUse);
							sum_eventSF_0b_antiTag+=eventWeightToUse;
							nEvents_unscaled_0b_antiTag+=1;
							h_nAK4_AT0b->Fill(nAK4_recount,eventWeightToUse);
							sum_eventSF_AT1b+=eventWeightToUse;
							h_true_b_jets_AT->Fill(nGenBJets);
							h_true_b_jets_AT0b->Fill(nGenBJets);
							sum_eventSF_AT0b+=eventWeightToUse;

							for(int iii=0; iii<nfatjets; iii++)
							{
								h_JEC_uncert_AK8_AT0b->Fill(JEC_uncert_AK8[iii]);
								h_AK8_JER_AT0b->Fill(AK8_JER[iii]);

							}
							for(int iii=0; iii<nAK4; iii++)
							{
								h_JEC_uncert_AK4_AT0b->Fill(JEC_uncert_AK4[iii]);
							}
						}  

					}
					// SJ2 antitag
					else if(   (SJ_nAK4_50[1]<1) && (SJ_mass_100[1]<150.)   )
					{
						if((SJ_nAK4_300[0]>=2) && (SJ_mass_100[0]>=400.)   )
						{
							
							eventWeightToUse *= pdf_weight*scale_weight;  //

							h_pdf_EventWeight_AT0b->Fill(pdf_weight);
							h_renorm_EventWeight_AT0b->Fill(renormWeight);
							h_factor_EventWeight_AT0b->Fill(factWeight);
							h_scale_EventWeight_AT0b->Fill(scale_weight);
							h_PU_eventWeight_AT0b->Fill(PU_eventWeight);
							h_bTag_eventWeight_T_AT0b->Fill(bTag_eventWeight_T);
							h_bTag_eventWeight_M_AT0b->Fill(bTag_eventWeight_M);
							h_L1PrefiringWeight_AT0b->Fill(prefiringWeight);
							h_topPtWeight_AT0b->Fill(topPtWeight);

							sum_eventSF_AT0b+=eventWeightToUse;

							//std::cout << "------------ In the AT0b for " << systematic << "/" << *systematic_suffix<< " and event number " << eventnum << " : bTag_eventWeight_M is " << bTag_eventWeight_M  <<     std::endl;

							h_totHT_AT0b->Fill(totHT,eventWeightToUse);

							nZeroBtagAntiTag+=eventScaleFactor;
							h_MSJ_mass_vs_MdSJ_AT0b->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse);
							h_disuperjet_mass_AT0b->Fill(diSuperJet_mass,eventWeightToUse);
							h_SJ_mass_AT0b->Fill(superJet_mass[1],eventWeightToUse);
							sum_eventSF_0b_antiTag+=eventWeightToUse;
							nEvents_unscaled_0b_antiTag+=1;
							h_nAK4_AT0b->Fill(nAK4_recount,eventWeightToUse);
							h_true_b_jets_AT->Fill(nGenBJets);
							h_true_b_jets_AT0b->Fill(nGenBJets);

							for(int iii=0; iii<nfatjets; iii++)
							{
								h_JEC_uncert_AK8_AT0b->Fill(JEC_uncert_AK8[iii]);
								h_AK8_JER_AT0b->Fill(AK8_JER[iii]);

							}
							for(int iii=0; iii<nAK4; iii++)
							{
								h_JEC_uncert_AK4_AT0b->Fill(JEC_uncert_AK4[iii]);
							}
						}  

					}
					///////////////////
					////// ADT0b ///////
					///////////////////


					else if(   (SJ_nAK4_200[0]<1) && (SJ_mass_100[0]<200.)   )
					{
						if(  (SJ_nAK4_200[1]<1) && (SJ_mass_100[1]<200.)    )
						{
							 eventWeightToUse *= pdf_weight*scale_weight;  //factWeight*renormWeight

							h_MSJ_mass_vs_MdSJ_ADT0b->Fill(diSuperJet_mass, ( superJet_mass[0] + superJet_mass[1])/2.0,eventWeightToUse);
							h_disuperjet_mass_ADT0b->Fill(diSuperJet_mass,eventWeightToUse);
							h_SJ_mass_ADT0b->Fill( ( superJet_mass[0] + superJet_mass[1])/2.0,eventWeightToUse);
							h_nAK4_ADT0b->Fill(nAK4_recount,eventWeightToUse);
							h_true_b_jets_AT->Fill(nGenBJets);
						}  
					}


					////////////////////////////////////////////////////////////
					///////////////////// NN-based tagging /////////////////////
					////////////////////////////////////////////////////////////

					///////////////////
					////// NN CR //////
					///////////////////
					if( (SJ1_BEST_scores > BEST_WP) && (SJ2_BEST_scores > BEST_WP) )  // should kill some of the ST BR
					{



						 double eventWeightToUse_NN = eventScaleFactor;
						 if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos)) eventWeightToUse_NN*=bTag_eventWeight_M;
						 eventWeightToUse_NN *= pdf_weight*scale_weight; //factWeight*renormWeight

						nNN_CR +=eventWeightToUse_NN;
						h_SJ_mass_NN_CR->Fill((superJet_mass[0]+superJet_mass[1])/2. ,eventWeightToUse_NN);
						h_disuperjet_mass_NN_CR->Fill(diSuperJet_mass,eventWeightToUse_NN);
						h_MSJ_mass_vs_MdSJ_NN_CR->Fill(diSuperJet_mass,(superJet_mass[1]+superJet_mass[0])/2,eventWeightToUse_NN);
						h_true_b_jets_NN_CR->Fill(nGenBJets,eventWeightToUse_NN);
						h_true_b_jets_NN_DT->Fill(nGenBJets,eventWeightToUse_NN);
					}

					///////////////////
					///// NN AT0b /////
					///////////////////
					// SJ2 antitag w/ SJ1 tagged
					else if( (SJ1_BEST_scores > BEST_WP) && (SJ2_BEST_scores < BEST_AT_WP) ) // want to be quite sure the second superjet is not tagged
					{
						 double eventWeightToUse_NN = eventScaleFactor*=bTag_eventWeight_M;
						 if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos)) eventWeightToUse_NN*=bTag_eventWeight_M;
						 eventWeightToUse_NN *= pdf_weight*scale_weight;   //factWeight*renormWeight

						nNN_AT0b +=eventScaleFactor;
						h_SJ_mass_NN_AT0b->Fill(superJet_mass[0],eventWeightToUse_NN);
						h_disuperjet_mass_NN_AT0b->Fill(diSuperJet_mass,eventWeightToUse_NN);
						h_MSJ_mass_vs_MdSJ_NN_AT0b->Fill(diSuperJet_mass,superJet_mass[0],eventWeightToUse_NN);
						h_true_b_jets_NN_AT0b->Fill(nGenBJets);
						h_true_b_jets_NN_AT->Fill(nGenBJets);
					} 
					// SJ1 antitag w/ SJ12tagged
					else if(  (SJ1_BEST_scores < BEST_AT_WP ) && (SJ2_BEST_scores > BEST_WP) ) // want to be quite sure the second superjet is not tagged
					{
						 double eventWeightToUse_NN = eventScaleFactor*=bTag_eventWeight_M;
						 if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos)) eventWeightToUse_NN*=bTag_eventWeight_M;
						 eventWeightToUse_NN *= pdf_weight*scale_weight;   //factWeight*renormWeight

						nNN_AT0b +=eventScaleFactor;
						h_SJ_mass_NN_AT0b->Fill(superJet_mass[1],eventWeightToUse_NN);
						h_disuperjet_mass_NN_AT0b->Fill(diSuperJet_mass,eventWeightToUse_NN);
						h_MSJ_mass_vs_MdSJ_NN_AT0b->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse_NN);
						h_true_b_jets_NN_AT0b->Fill(nGenBJets);
						h_true_b_jets_NN_AT->Fill(nGenBJets);
					} 
					///////////////////
					///// NN ADT0b /////
					///////////////////
					else if(  (SJ1_BEST_scores < BEST_AT_WP) && (SJ2_BEST_scores < BEST_AT_WP) ) // want to be quite sure the second superjet is not tagged
					{
						double eventWeightToUse_NN = eventScaleFactor*=bTag_eventWeight_M;
						 if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos)) eventWeightToUse_NN*=bTag_eventWeight_M;
						 eventWeightToUse_NN *= pdf_weight*scale_weight;  // factWeight*renormWeight

						h_SJ_mass_NN_ADT0b->Fill( ( superJet_mass[0] + superJet_mass[1])/2.0,eventWeightToUse_NN);
						h_disuperjet_mass_NN_ADT0b->Fill(diSuperJet_mass,eventWeightToUse_NN);
						h_MSJ_mass_vs_MdSJ_NN_ADT0b->Fill(diSuperJet_mass, (superJet_mass[0] + superJet_mass[1])/2.0,eventWeightToUse_NN);
						h_true_b_jets_NN_AT->Fill(nGenBJets);
					} 


				}
				
				/////////////////////////////
				///////// 1b region /////////
				/////////////////////////////



				else if ( (nMedBTags > 0)  )
				{



					h_nCA4_300_1b->Fill(SJ_nAK4_300[0], eventWeightToUse);
					h_nCA4_300_1b->Fill(SJ_nAK4_300[1], eventWeightToUse);

					if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventWeightToUse*=bTag_eventWeight_M;


					h_totHT_1b->Fill(totHT, eventWeightToUse);


					h_MSJ_mass_vs_MdSJ_dijet->Fill(fourAK8JetMass, (diAK8Jet_mass[0]+diAK8Jet_mass[1])/2.,eventWeightToUse);

					nBtagCut+=eventWeightToUse;
					h_SJ_nAK4_100_SR->Fill(SJ_nAK4_100[0],eventWeightToUse);
					h_SJ_nAK4_100_SR->Fill(SJ_nAK4_100[1],eventWeightToUse);

					h_SJ_nAK4_200_SR->Fill(SJ_nAK4_200[0],eventWeightToUse);
					h_SJ_nAK4_200_SR->Fill(SJ_nAK4_200[1],eventWeightToUse);


					h_SJ2_BEST_score_1b->Fill(SJ2_BEST_scores,eventWeightToUse);
					if (SJ2_BEST_scores > BEST_WP) h_SJ2_decision_1b->Fill(1,eventWeightToUse);
					else { h_SJ2_decision_1b->Fill(0.0,eventWeightToUse);  }

					h_SJ1_BEST_score_1b->Fill(SJ1_BEST_scores,eventWeightToUse);
					if (SJ1_BEST_scores > BEST_WP) h_SJ1_decision_1b->Fill(1,eventWeightToUse);
					else { h_SJ1_decision_1b->Fill(0.0,eventWeightToUse);  }


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




				  ///////////////////////////////////
				  /////// tagging study stuff ///////
				  ///////////////////////////////////




					/// cut-based tagging

				  double eventWeightToUse_taggingStudy = eventWeightToUse*pdf_weight*scale_weight;   
				  double eventWeightToUse_taggingStudy_noBTag = eventWeightToUse_preBtag*pdf_weight*scale_weight;   


					h_SJ_mass_total_SJs_1b->Fill(superJet_mass[0],eventWeightToUse_taggingStudy);
					h_SJ_mass_total_SJs_1b->Fill(superJet_mass[1],eventWeightToUse_taggingStudy);

					h_SJ_mass_total_SJs->Fill(superJet_mass[0],eventWeightToUse_taggingStudy_noBTag);
					h_SJ_mass_total_SJs->Fill(superJet_mass[1],eventWeightToUse_taggingStudy_noBTag);


					////////////// cut-based tagging

					// SJ1 tag
					if(   (SJ_nAK4_300[0]>=2) && (SJ_mass_100[0]>400.)   )
					{
						h_SJ_mass_tagged_SJs_1b->Fill(superJet_mass[0],eventWeightToUse_taggingStudy);
						h_SJ_mass_tagged_SJs->Fill(superJet_mass[0],eventWeightToUse_taggingStudy_noBTag);
					}
					// SJ2 tag
					if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
					{
						h_SJ_mass_tagged_SJs_1b->Fill(superJet_mass[1],eventWeightToUse_taggingStudy);
						h_SJ_mass_tagged_SJs->Fill(superJet_mass[1],eventWeightToUse_taggingStudy_noBTag);
					}




					// SJ1 cut-based antitag
					if(   (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<150.)   )
					{
						h_SJ2_mass_total_SJs_ATSJ1_1b->Fill(superJet_mass[1],eventWeightToUse_taggingStudy);
						h_SJ2_mass_total_SJs_ATSJ1->Fill(superJet_mass[1],eventWeightToUse_taggingStudy_noBTag);


						//SJ2 cut-based tag
						if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
						{
							h_SJ2_mass_tagged_SJs_ATSJ1_1b->Fill(superJet_mass[1],eventWeightToUse_taggingStudy);
							h_SJ2_mass_tagged_SJs_ATSJ1->Fill(superJet_mass[1],eventWeightToUse_taggingStudy_noBTag);
						}
					}
					// SJ2 cut-based antitag
					if(   (SJ_nAK4_50[1]<1) && (SJ_mass_100[1]<150.)   )
					{
						h_SJ1_mass_total_SJs_ATSJ2_1b->Fill(superJet_mass[0],eventWeightToUse_taggingStudy);
						h_SJ1_mass_total_SJs_ATSJ2->Fill(superJet_mass[0],eventWeightToUse_taggingStudy_noBTag);

						// SJ1 cut-based tag
						if((SJ_nAK4_300[0]>=2) && (SJ_mass_100[0]>=400.)   )
						{
							h_SJ1_mass_tagged_SJs_ATSJ2_1b->Fill(superJet_mass[0],eventWeightToUse_taggingStudy);
							h_SJ1_mass_tagged_SJs_ATSJ2->Fill(superJet_mass[0],eventWeightToUse_taggingStudy_noBTag);
						}
					}
					/////////////////////////////////////////////////////



					/// NN-based tagging

					// SJ1 tag
					if(  SJ1_BEST_scores > BEST_WP ) 
					{
						h_SJ_mass_tagged_SJs_1b_NN->Fill(superJet_mass[0],eventWeightToUse_taggingStudy);
						h_SJ_mass_tagged_SJs_NN->Fill(superJet_mass[0],eventWeightToUse_taggingStudy_noBTag);
					}
					// SJ2 tag
					if(  SJ2_BEST_scores > BEST_WP   )
					{
						h_SJ_mass_tagged_SJs_1b_NN->Fill(superJet_mass[1],eventWeightToUse_taggingStudy);
						h_SJ_mass_tagged_SJs_NN->Fill(superJet_mass[1],eventWeightToUse_taggingStudy_noBTag);
					}

					// SJ1 antitag
					if(  SJ1_BEST_scores < BEST_AT_WP    )
					{
						h_SJ2_mass_total_SJs_ATSJ1_1b_NN->Fill(superJet_mass[1],eventWeightToUse_taggingStudy);
						h_SJ2_mass_total_SJs_ATSJ1_NN->Fill(superJet_mass[1],eventWeightToUse_taggingStudy_noBTag);
						

						// SJ scores
						h_SJ2_BEST_score_1b_SJ1AT->Fill( SJ2_BEST_scores,eventWeightToUse_taggingStudy);
						h_SJ2_BEST_score_SJ1AT->Fill( SJ2_BEST_scores,eventWeightToUse_taggingStudy_noBTag);


						if(SJ2_BEST_scores > BEST_WP) 
						{
							h_SJ2_decision_1b_SJ1AT->Fill(1,eventWeightToUse_taggingStudy);
							h_SJ2_decision_SJ1AT->Fill( 1, eventWeightToUse_taggingStudy_noBTag);
							h_SJ2_mass_tagged_SJs_ATSJ1_1b_NN->Fill(superJet_mass[1],eventWeightToUse_taggingStudy);
							h_SJ2_mass_tagged_SJs_ATSJ1_NN->Fill(superJet_mass[1],eventWeightToUse_taggingStudy_noBTag);
						}
						else 
						{ 
							h_SJ2_decision_1b_SJ1AT->Fill(0.0,eventWeightToUse_taggingStudy);
							h_SJ2_decision_SJ1AT->Fill( 0.0, eventWeightToUse_taggingStudy_noBTag);     
						}

					}
					// SJ2 antitag
					if(  SJ2_BEST_scores < BEST_AT_WP  )
					{
						h_SJ1_mass_total_SJs_ATSJ2_1b_NN->Fill(superJet_mass[0],eventWeightToUse_taggingStudy);
						h_SJ1_mass_total_SJs_ATSJ2_NN->Fill(superJet_mass[0],eventWeightToUse_taggingStudy_noBTag);
						


						h_SJ1_BEST_score_1b_SJ2AT->Fill( SJ1_BEST_scores,eventWeightToUse_taggingStudy);
						h_SJ1_BEST_score_SJ2AT->Fill( SJ1_BEST_scores,eventWeightToUse_taggingStudy_noBTag);

						

						if (SJ1_BEST_scores > BEST_WP) 
						{
							h_SJ1_decision_1b_SJ2AT->Fill(1.0,eventWeightToUse_taggingStudy);
							h_SJ1_decision_SJ2AT->Fill( 1.0, eventWeightToUse_taggingStudy_noBTag);
							h_SJ1_mass_tagged_SJs_ATSJ2_1b_NN->Fill(superJet_mass[0],eventWeightToUse_taggingStudy);
							h_SJ1_mass_tagged_SJs_ATSJ2_NN->Fill(superJet_mass[0],eventWeightToUse_taggingStudy_noBTag);
						}
						else 
						{  
							h_SJ1_decision_SJ2AT->Fill( 0.0, eventWeightToUse_taggingStudy_noBTag);    
							h_SJ1_decision_1b_SJ2AT->Fill(0.0,eventWeightToUse_taggingStudy);
						}

					}







					////////////////////////////////////////////////////////////
					///////////////////// cut-based tagging ////////////////////
					////////////////////////////////////////////////////////////


					///////////////////
					/////// SR ////////
					///////////////////

					if(   (SJ_nAK4_300[0]>=2) && (SJ_mass_100[0]>400.)   )
					{
						if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
						{

							h_pdf_EventWeight_SR->Fill(pdf_weight);
							h_renorm_EventWeight_SR->Fill(renormWeight);
							h_factor_EventWeight_SR->Fill(factWeight);
							h_scale_EventWeight_SR->Fill(scale_weight);
							h_PU_eventWeight_SR->Fill(PU_eventWeight);
							h_bTag_eventWeight_T_SR->Fill(bTag_eventWeight_T);
							h_bTag_eventWeight_M_SR->Fill(bTag_eventWeight_M);
							h_L1PrefiringWeight_SR->Fill(prefiringWeight);
							h_topPtWeight_SR->Fill(topPtWeight);

							eventWeightToUse *= pdf_weight*scale_weight;  // factWeight*renormWeight

							//std::cout << "------------ In the SR for " << systematic << "/" << *systematic_suffix<< " and event number " << eventnum << " : bTag_eventWeight_M is " << bTag_eventWeight_M  <<     std::endl;

							h_totHT_SR->Fill(totHT,eventWeightToUse);

							h_true_b_jets_DT->Fill(nGenBJets);
							h_true_b_jets_SR->Fill(nGenBJets);

							h_disuperjet_mass_SR->Fill(diSuperJet_mass,eventWeightToUse);
							h_SJ_mass_SR->Fill( (superJet_mass[0]+superJet_mass[1])/2. ,eventWeightToUse );
							nDoubleTagged+= eventScaleFactor;
							h_MSJ_mass_vs_MdSJ_SR->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventWeightToUse   );
							h_MSJ1_vs_MSJ2_SR->Fill(superJet_mass[0],superJet_mass[1],eventWeightToUse);
							sum_eventSF_SR+=eventWeightToUse;
							nEvents_unscaled_SR+=1;

							for(int iii=0; iii<nfatjets; iii++)
							{
								h_JEC_uncert_AK8_SR->Fill(JEC_uncert_AK8[iii]);
								h_AK8_JER_SR->Fill(AK8_JER[iii]);

							}
							for(int iii=0; iii<nAK4; iii++)
							{
								h_JEC_uncert_AK4_SR->Fill(JEC_uncert_AK4[iii]);
							}

						}
					}


					///////////////////
					////// AT1b ///////
					///////////////////

					/// SJ1 antitag
					else if(   (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<150.)   )
					{
						if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
						{

							//std::cout << "------------ In the AT1b for " << systematic << "/" << *systematic_suffix<< " and event number " << eventnum << " : bTag_eventWeight_M is " << bTag_eventWeight_M  <<     std::endl;

							eventWeightToUse *= pdf_weight*scale_weight;    // factWeight*renormWeight

							h_pdf_EventWeight_AT1b->Fill(pdf_weight);
							h_renorm_EventWeight_AT1b->Fill(renormWeight);
							h_factor_EventWeight_AT1b->Fill(factWeight);
							h_scale_EventWeight_AT1b->Fill(scale_weight);
							h_PU_eventWeight_AT1b->Fill(PU_eventWeight);
							h_bTag_eventWeight_T_AT1b->Fill(bTag_eventWeight_T);
							h_bTag_eventWeight_M_AT1b->Fill(bTag_eventWeight_M);
							h_L1PrefiringWeight_AT1b->Fill(prefiringWeight);
							h_topPtWeight_AT1b->Fill(topPtWeight);

							h_totHT_AT1b->Fill(totHT,eventWeightToUse);

							h_true_b_jets_AT->Fill(nGenBJets);
							h_true_b_jets_AT0b->Fill(nGenBJets);

							nOneBtagAntiTag+=eventWeightToUse;
							h_MSJ_mass_vs_MdSJ_AT1b->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse);
							h_SJ_mass_AT1b->Fill(superJet_mass[1],eventWeightToUse);
							h_disuperjet_mass_AT1b->Fill(diSuperJet_mass,eventWeightToUse);
							sum_eventSF_1b_antiTag+= eventWeightToUse;
							nEvents_unscaled_1b_antiTag+=1;
							h_nAK4_AT1b->Fill(nAK4_recount);
							sum_eventSF_AT1b+=eventWeightToUse;
							h_nTightbTags_AT1b->Fill(nTightBTags);

							for(int iii=0; iii<nfatjets; iii++)
							{
								h_JEC_uncert_AK8_AT1b->Fill(JEC_uncert_AK8[iii]);
								h_AK8_JER_AT1b->Fill(AK8_JER[iii]);

							}
							for(int iii=0; iii<nAK4; iii++)
							{
								h_JEC_uncert_AK4_AT1b->Fill(JEC_uncert_AK4[iii]);
							}
						}
					}
					// SJ2 antitag
					else if(   (SJ_nAK4_50[1]<1) && (SJ_mass_100[1]<150.)   )
					{
						if((SJ_nAK4_300[0]>=2) && (SJ_mass_100[0]>=400.)   )
						{

							//std::cout << "------------ In the AT1b for " << systematic << "/" << *systematic_suffix<< " and event number " << eventnum << " : bTag_eventWeight_M is " << bTag_eventWeight_M  <<     std::endl;

							eventWeightToUse *= pdf_weight*scale_weight;    // factWeight*renormWeight

							h_pdf_EventWeight_AT1b->Fill(pdf_weight);
							h_renorm_EventWeight_AT1b->Fill(renormWeight);
							h_factor_EventWeight_AT1b->Fill(factWeight);
							h_scale_EventWeight_AT1b->Fill(scale_weight);
							h_PU_eventWeight_AT1b->Fill(PU_eventWeight);
							h_bTag_eventWeight_T_AT1b->Fill(bTag_eventWeight_T);
							h_bTag_eventWeight_M_AT1b->Fill(bTag_eventWeight_M);
							h_L1PrefiringWeight_AT1b->Fill(prefiringWeight);
							h_topPtWeight_AT1b->Fill(topPtWeight);

							h_totHT_AT1b->Fill(totHT,eventWeightToUse);

							h_true_b_jets_AT->Fill(nGenBJets);
							h_true_b_jets_AT0b->Fill(nGenBJets);

							nOneBtagAntiTag+=eventWeightToUse;
							h_MSJ_mass_vs_MdSJ_AT1b->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse);
							h_SJ_mass_AT1b->Fill(superJet_mass[1],eventWeightToUse);
							h_disuperjet_mass_AT1b->Fill(diSuperJet_mass,eventWeightToUse);
							sum_eventSF_1b_antiTag+= eventWeightToUse;
							nEvents_unscaled_1b_antiTag+=1;
							h_nAK4_AT1b->Fill(nAK4_recount);
							h_nTightbTags_AT1b->Fill(nTightBTags);
							sum_eventSF_AT1b+=eventWeightToUse;

							for(int iii=0; iii<nfatjets; iii++)
							{
								h_JEC_uncert_AK8_AT1b->Fill(JEC_uncert_AK8[iii]);
								h_AK8_JER_AT1b->Fill(AK8_JER[iii]);
							}
							for(int iii=0; iii<nAK4; iii++)
							{
								h_JEC_uncert_AK4_AT1b->Fill(JEC_uncert_AK4[iii]);
							}
						}
					}

					///////////////////
					////// ADT1b ///////
					///////////////////
					 else if( (SJ_nAK4_200[0]<1) && (SJ_mass_100[0]<200.)   )
					 {
						if(  (SJ_nAK4_200[1]<1) && (SJ_mass_100[1]<200.)    )
						{
							h_true_b_jets_AT->Fill(nGenBJets);
							h_true_b_jets_AT0b->Fill(nGenBJets);

							h_MSJ_mass_vs_MdSJ_ADT1b->Fill(diSuperJet_mass, (superJet_mass[0] + superJet_mass[1])/2.0,eventWeightToUse);
							h_SJ_mass_ADT1b->Fill( ( superJet_mass[0] + superJet_mass[1])/2.0,eventWeightToUse);
							h_disuperjet_mass_ADT1b->Fill(diSuperJet_mass,eventWeightToUse);
							h_nAK4_ADT1b->Fill(nAK4_recount);
							h_nTightbTags_ADT1b->Fill(nTightBTags);
						}

					}

					////////////////////////////////////////////////////////////
					///////////////////// NN-based tagging /////////////////////
					////////////////////////////////////////////////////////////

					///////////////////
					////// NN SR //////
					///////////////////
					if(   (SJ1_BEST_scores > BEST_WP ) && (SJ2_BEST_scores > BEST_WP ) )  // should kill some of the ST BR
					{
						{
							 double eventWeightToUse_NN = eventScaleFactor;
							 if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventWeightToUse_NN*=bTag_eventWeight_M;
							 eventWeightToUse_NN *= pdf_weight*scale_weight;   // factWeight*renormWeight

							nNN_SR +=eventScaleFactor;
							h_SJ_mass_NN_SR->Fill((superJet_mass[0]+superJet_mass[1])/2. ,eventWeightToUse_NN );
							h_disuperjet_mass_NN_SR->Fill(diSuperJet_mass,eventWeightToUse_NN);
							h_MSJ_mass_vs_MdSJ_NN_SR->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventWeightToUse_NN);
							h_true_b_jets_NN_SR->Fill(nGenBJets);
							h_true_b_jets_NN_DT->Fill(nGenBJets);
						}
					}

					///////////////////
					///// NN AT1b /////
					///////////////////

					// SJ2 antitag w/ SJ1 tagged
					else if(   (SJ1_BEST_scores > BEST_WP ) && (SJ2_BEST_scores < BEST_AT_WP )  ) // want to be quite sure the second superjet is not tagged
					{
						{
							 double eventWeightToUse_NN = eventScaleFactor;
							 if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventWeightToUse_NN*=bTag_eventWeight_M;
							 eventWeightToUse_NN *= pdf_weight*scale_weight;   // factWeight*renormWeight

							nNN_AT1b +=eventScaleFactor;
							h_SJ_mass_NN_AT1b->Fill(superJet_mass[0],eventWeightToUse_NN);
							h_disuperjet_mass_NN_AT1b->Fill(diSuperJet_mass,eventWeightToUse_NN );
							h_MSJ_mass_vs_MdSJ_NN_AT1b->Fill(diSuperJet_mass,superJet_mass[0],eventWeightToUse_NN );
							h_true_b_jets_NN_AT1b->Fill(nGenBJets);
							h_true_b_jets_NN_AT->Fill(nGenBJets);
						}
					} 
					// SJ1 antitag w/ SJ2 tagged
					else if(   (SJ1_BEST_scores < BEST_AT_WP ) && (SJ2_BEST_scores > BEST_WP )  ) // want to be quite sure the second superjet is not tagged
					{
						{
							 double eventWeightToUse_NN = eventScaleFactor;
							 if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventWeightToUse_NN*=bTag_eventWeight_M;
							 eventWeightToUse_NN *= pdf_weight*scale_weight;   // factWeight*renormWeight

							nNN_AT1b +=eventScaleFactor;
							h_SJ_mass_NN_AT1b->Fill(superJet_mass[1],eventWeightToUse_NN);
							h_disuperjet_mass_NN_AT1b->Fill(diSuperJet_mass,eventWeightToUse_NN );
							h_MSJ_mass_vs_MdSJ_NN_AT1b->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse_NN );
							h_true_b_jets_NN_AT1b->Fill(nGenBJets);
							h_true_b_jets_NN_AT->Fill(nGenBJets);
						}
					} 
					///////////////////
					///// NN ADT1b /////
					///////////////////
					else if(   (SJ1_BEST_scores < BEST_AT_WP ) && (SJ2_BEST_scores < BEST_AT_WP ) ) // want to be quite sure the second superjet is not tagged
					{
						 double eventWeightToUse_NN = eventScaleFactor;
						 if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventWeightToUse_NN*=bTag_eventWeight_M;
						 eventWeightToUse_NN *= pdf_weight*scale_weight;  // factWeight*renormWeight

						h_SJ_mass_NN_ADT1b->Fill( ( superJet_mass[0] + superJet_mass[1])/2.0,eventWeightToUse_NN);
						h_disuperjet_mass_NN_ADT1b->Fill(diSuperJet_mass,eventWeightToUse_NN );
						h_MSJ_mass_vs_MdSJ_NN_ADT1b->Fill(diSuperJet_mass,(superJet_mass[0] + superJet_mass[1])/2.0,eventWeightToUse_NN );
						h_true_b_jets_NN_AT->Fill(nGenBJets);
					} 
				}



				///////////////////////////////////////////
				// 1 tight and 0 tight b tagged regions ///
				///////////////////////////////////////////

				if (nTightBTags < 1) // 0 tight b region
				{
					if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos))eventWeightToUse*=bTag_eventWeight_T;

					///////////////////
					////// AT0tb ///////
					///////////////////

					if(   (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<150.)   )
					{
						if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
						{
							 eventWeightToUse *= pdf_weight*scale_weight;   // factWeight*renormWeight

							h_MSJ_mass_vs_MdSJ_AT0tb->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse);
							h_disuperjet_mass_AT0tb->Fill(diSuperJet_mass,eventWeightToUse);
							h_SJ_mass_AT0tb->Fill(superJet_mass[1],eventWeightToUse);
						}  

					}

					///////////////////
					///// NN AT0tb /////
					///////////////////

					// SJ2 anti-tagged, SJ1 tagged
					if(   (SJ1_BEST_scores > BEST_WP ) && (SJ2_BEST_scores < BEST_AT_WP )  ) // want to be quite sure the second superjet is not tagged
					{

						 double eventWeightToUse_NN = eventScaleFactor;
						 if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventWeightToUse_NN*=bTag_eventWeight_T;
						 eventWeightToUse_NN *= pdf_weight*scale_weight;   // factWeight*renormWeight

						h_SJ_mass_NN_AT0tb->Fill(superJet_mass[0],eventWeightToUse_NN);
						h_disuperjet_mass_NN_AT0tb->Fill(diSuperJet_mass,eventWeightToUse_NN);
						h_MSJ_mass_vs_MdSJ_NN_AT0tb->Fill(diSuperJet_mass,superJet_mass[0],eventWeightToUse_NN);
					} 

				}
				else if (nTightBTags > 0)
				{

					if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos))eventWeightToUse*=bTag_eventWeight_T;

					///////////////////
					////// AT1tb ///////
					///////////////////
					if(   (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<150.)   )
					{
						if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
						{

							eventWeightToUse *= pdf_weight*scale_weight;    // factWeight*renormWeight

							h_MSJ_mass_vs_MdSJ_AT1tb->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse);
							h_SJ_mass_AT1tb->Fill(superJet_mass[1],eventWeightToUse);
							h_disuperjet_mass_AT1tb->Fill(diSuperJet_mass,eventWeightToUse);

						}

					}
					///////////////////
					///// NN AT1tb /////
					///////////////////

					// SJ1 tagged, SJ2 anti-tagged
					if(   (SJ1_BEST_scores > BEST_WP ) && (SJ2_BEST_scores < BEST_AT_WP )  ) // want to be quite sure the second superjet is not tagged
					{
						 double eventWeightToUse_NN = eventScaleFactor;
						 if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventWeightToUse_NN*=bTag_eventWeight_T;
						 eventWeightToUse_NN *= pdf_weight*scale_weight;  // factWeight*renormWeight

						h_SJ_mass_NN_AT1tb->Fill(superJet_mass[0],eventWeightToUse_NN);
						h_disuperjet_mass_NN_AT1tb->Fill(diSuperJet_mass,eventWeightToUse_NN );
						h_MSJ_mass_vs_MdSJ_NN_AT1tb->Fill(diSuperJet_mass,superJet_mass[0],eventWeightToUse_NN );

					} 

				}
			}

			else if (runType == "side-band")
			{


				h_totHT_SB->Fill(totHT, eventWeightToUse  );

				h_nTightBTags->Fill(nTightBTags,eventWeightToUse);
				h_nMedBTags->Fill(nMedBTags,eventWeightToUse);
				h_nLooseBTags->Fill(nLooseBtags,eventWeightToUse);

				if ( (nMedBTags < 1)  )
				{
					if((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventWeightToUse*=bTag_eventWeight_M;
					h_SJ_mass_SB0b->Fill((superJet_mass[0]+superJet_mass[1])/2. ,eventWeightToUse);
					h_disuperjet_mass_SB0b->Fill(diSuperJet_mass,eventWeightToUse);
					h_MSJ_mass_vs_MdSJ_SB0b->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventWeightToUse );

				}
				else if ( (nMedBTags > 0)  )
				{
					if((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventWeightToUse*=bTag_eventWeight_M;
					h_SJ_mass_SB1b->Fill((superJet_mass[0]+superJet_mass[1])/2. ,eventWeightToUse);
					h_disuperjet_mass_SB1b->Fill(diSuperJet_mass,eventWeightToUse);
					h_MSJ_mass_vs_MdSJ_SB1b->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventWeightToUse );
				}

			}



			double eventScaleFactor_M_pt75 = 1.0*prefiringWeight;
			double eventScaleFactor_M_pt100 = 1.0*prefiringWeight;
			double eventScaleFactor_M_pt150 = 1.0*prefiringWeight;

			if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos) )
			{
				eventScaleFactor_M_pt75  = PU_eventWeight*topPtWeight*pdf_weight*scale_weight; // factWeight*renormWeight   
				eventScaleFactor_M_pt100 = PU_eventWeight*topPtWeight*pdf_weight*scale_weight; // factWeight*renormWeight   
				eventScaleFactor_M_pt150 = PU_eventWeight*topPtWeight*pdf_weight*scale_weight; // factWeight*renormWeight   
			}



			// alternative b jet selection regions --- cut-based tagging
			bool isDoubleTagged = false;
			bool isAntiTagged = false;

			if( (SJ_nAK4_300[0]>=2) && (SJ_mass_100[0]>400.) )
			{
				if( (SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.) ) isDoubleTagged = true;
			}
			else if( (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<150.) )
			{
				if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.) ) isAntiTagged = true;
			}
			if(nMedBTags_pt75 > 0)
			{

				if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventScaleFactor_M_pt75*=bTag_eventWeight_M;
				if(isDoubleTagged) 		h_MSJ_mass_vs_MdSJ_SR_bpt75->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventScaleFactor_M_pt75   );
				else if(isAntiTagged)   h_MSJ_mass_vs_MdSJ_AT1b_bpt75->Fill(diSuperJet_mass,   superJet_mass[1] ,eventScaleFactor_M_pt75   );
			}
			else
			{
				if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventScaleFactor_M_pt75*=bTag_eventWeight_M;
				if(isDoubleTagged) 		h_MSJ_mass_vs_MdSJ_CR_bpt75->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventScaleFactor_M_pt75   );
				else if(isAntiTagged)   h_MSJ_mass_vs_MdSJ_AT0b_bpt75->Fill(diSuperJet_mass,   superJet_mass[1] ,eventScaleFactor_M_pt75   );
			}

			if(nMedBTags_pt100 > 0)
			{
				if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventScaleFactor_M_pt100*=bTag_eventWeight_M;

				if(isDoubleTagged) 		h_MSJ_mass_vs_MdSJ_SR_bpt100->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventScaleFactor_M_pt100   );
				else if(isAntiTagged)   h_MSJ_mass_vs_MdSJ_AT1b_bpt100->Fill(diSuperJet_mass,superJet_mass[1] ,eventScaleFactor_M_pt100   );
			}
			else
			{
				if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventScaleFactor_M_pt100*=bTag_eventWeight_M;

				if(isDoubleTagged) 		h_MSJ_mass_vs_MdSJ_CR_bpt100->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventScaleFactor_M_pt100   );
				else if(isAntiTagged)   h_MSJ_mass_vs_MdSJ_AT0b_bpt100->Fill(diSuperJet_mass,superJet_mass[1] ,eventScaleFactor_M_pt100   );
			}
			if(nMedBTags_pt150 > 0)
			{
				if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventScaleFactor_M_pt150*=bTag_eventWeight_M;

				if(isDoubleTagged) 		h_MSJ_mass_vs_MdSJ_SR_bpt150->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventScaleFactor_M_pt150   );
				else if(isAntiTagged)   h_MSJ_mass_vs_MdSJ_AT1b_bpt150->Fill(diSuperJet_mass,superJet_mass[1] ,eventScaleFactor_M_pt150   );
			}
			else
			{
				if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventScaleFactor_M_pt150*=bTag_eventWeight_M;

				if(isDoubleTagged) 		h_MSJ_mass_vs_MdSJ_CR_bpt150->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventScaleFactor_M_pt150   );
				else if(isAntiTagged)   h_MSJ_mass_vs_MdSJ_AT0b_bpt150->Fill(diSuperJet_mass,superJet_mass[1] , eventScaleFactor_M_pt150   );
			}

		
			// alternative b jet selection regions --- NN-tagging
			bool isDoubleNNTagged = false;
			bool isNNAntiTagged = false;


			if(  (SJ1_BEST_scores > BEST_WP ) && (SJ2_BEST_scores > BEST_WP ) ) isDoubleNNTagged = true;
			else if(  ( (SJ1_BEST_scores > BEST_WP ) && (SJ2_BEST_scores < BEST_AT_WP ) ) || (  (SJ1_BEST_scores < BEST_AT_WP ) && (SJ2_BEST_scores > BEST_WP )     ) ) isNNAntiTagged = true;
			if(nMedBTags_pt150 > 0)
			{
				if(isDoubleNNTagged) h_MSJ_mass_vs_MdSJ_NN_SR_bpt75->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventScaleFactor_M_pt75   );
				else if(isNNAntiTagged)   h_MSJ_mass_vs_MdSJ_NN_AT1b_bpt75->Fill(diSuperJet_mass,   superJet_mass[1] ,eventScaleFactor_M_pt75   );
			}
			else
			{
				if(isDoubleNNTagged) h_MSJ_mass_vs_MdSJ_NN_CR_bpt75->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventScaleFactor_M_pt75   );
				else if(isNNAntiTagged)   h_MSJ_mass_vs_MdSJ_NN_AT0b_bpt75->Fill(diSuperJet_mass,   superJet_mass[1] ,eventScaleFactor_M_pt75   );
			}

			if(nMedBTags_pt100 > 0)
			{
				if(isDoubleNNTagged) h_MSJ_mass_vs_MdSJ_NN_SR_bpt100->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventScaleFactor_M_pt100   );
				else if(isNNAntiTagged)   h_MSJ_mass_vs_MdSJ_NN_AT1b_bpt100->Fill(diSuperJet_mass,superJet_mass[1] ,eventScaleFactor_M_pt100   );
			}
			else
			{
				if(isDoubleNNTagged) h_MSJ_mass_vs_MdSJ_NN_CR_bpt100->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventScaleFactor_M_pt100   );
				else if(isNNAntiTagged)   h_MSJ_mass_vs_MdSJ_NN_AT0b_bpt100->Fill(diSuperJet_mass,superJet_mass[1] ,eventScaleFactor_M_pt100   );
			}
			if(nMedBTags_pt150 > 0)
			{
				if(isDoubleNNTagged) h_MSJ_mass_vs_MdSJ_NN_SR_bpt150->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventScaleFactor_M_pt150   );
				else if(isNNAntiTagged)   h_MSJ_mass_vs_MdSJ_NN_AT1b_bpt150->Fill(diSuperJet_mass,superJet_mass[1] ,eventScaleFactor_M_pt150   );
			}
			else
			{
				if(isDoubleNNTagged) h_MSJ_mass_vs_MdSJ_NN_CR_bpt150->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventScaleFactor_M_pt150   );
				else if(isNNAntiTagged)   h_MSJ_mass_vs_MdSJ_NN_AT0b_bpt150->Fill(diSuperJet_mass,superJet_mass[1] ,eventScaleFactor_M_pt150   );
			}

		}



		outFile->Write();
		//std::cout << "The average event scale factors were " << sum_eventSF_SR/nEvents_unscaled_SR  << "/" <<sum_eventSF_CR/nEvents_unscaled_CR << "/" <<sum_eventSF_0b_antiTag/nEvents_unscaled_0b_antiTag << "/" << sum_eventSF_1b_antiTag/nEvents_unscaled_1b_antiTag<<  "in the signal/control/0b-antiTag/1b-antiTag regions" << std::endl;
		//std::cout << "This can be further broken down - average b-tag SF is " << sum_eventSF_SR/nEvents_unscaled_SR  << "/" <<sum_eventSF_CR/nEvents_unscaled_CR << "/" <<sum_eventSF_0b_antiTag/nEvents_unscaled_0b_antiTag << "/" << sum_eventSF_1b_antiTag/nEvents_unscaled_1b_antiTag<<  "in the signal/control/0b-antiTag/1b-antiTag regions" << std::endl;
		//std::cout << "The number of bad btag and PU SFs was " << num_bad_btagSF << " and " << num_bad_PUSF << std::endl;
		std::cout << "Finishing systematic " << systematic << " "<< *systematic_suffix << std::endl;
		std::cout << "Total Events: " << totEventsUncut << " in " << inFileName << " for " << systematic << " "<< *systematic_suffix << std::endl;
		std::cout << "In " << inFileName << " there were " << num_bad_btagSF<< "/" << num_bad_PUSF<< "/"<< num_bad_topPt<< "/"<< num_bad_scale<< "/"<<num_bad_pdf << "/" <<num_bad_prefiring << " bad btag/PU/topPt/scale/pdf/prefiring event weights" << std::endl; 
		std::cout << "There were " << badEventSF << " bad events." << std::endl;
		std::cout << "Signal  Region for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << ", "<<  dataYear  << " : total/HTcut/AK8jetCut/heavyAK8JetCut/nBtagCut/nSJEnergyCut: - " <<   sum_eventSF_SR   << std::endl;
		std::cout << "Control  Region for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << ", "<<  dataYear  << " : total/HTcut/AK8jetCut/heavyAK8JetCut/nBtagCut/nSJEnergyCut: - " <<   sum_eventSF_CR   << std::endl;
		std::cout << "AT1b  Region for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << ", "<<  dataYear  << " : total/HTcut/AK8jetCut/heavyAK8JetCut/nBtagCut/nSJEnergyCut: - " <<   sum_eventSF_AT1b   << std::endl;
		std::cout << "AT0b  Region for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << ", "<<  dataYear  << " : total/HTcut/AK8jetCut/heavyAK8JetCut/nBtagCut/nSJEnergyCut: - " <<   sum_eventSF_AT0b   << std::endl;


		std::cout << dataBlock << "/" << dataYear << "/" << systematic+ "_" + *systematic_suffix << " : there was a total of " << total_1b << "/" << total_0b << " events in the 1b/0b region (all pre-selected)." << std::endl;




		std::cout << "-------- The largest AK8 JEC Uncertainty corr for " << dataBlock << "/" << dataYear << "/" << systematic+ "_" + *systematic_suffix  << " was " <<largest_JEC_corr << " with average corr " << avg_JEC_corr / (1.0*total_jets) << std::endl;
		std::cout << "-------- The largest AK4 JEC Uncertainty corr for " << dataBlock << "/" << dataYear << "/" << systematic+ "_" + *systematic_suffix  << " was " <<largest_JEC_corr_AK4 << " with average corr " << avg_JEC_corr_AK4 / (1.0*total_jets_AK4) << std::endl;



		g_bTagSF_T_vs_HT->Write();
		g_bTagSF_M_vs_HT->Write();

	   delete g_bTagSF_T_vs_HT,  h_totHT, h_totHT_unscaled, h_nfatjets_pre,  h_SJ_nAK4_100_CR,  h_SJ_nAK4_200_CR,  h_SJ_mass_CR,  h_disuperjet_mass_CR,  h_MSJ_mass_vs_MdSJ_CR,  h_SJ_nAK4_100_SR,
	    h_SJ_nAK4_200_SR,  h_SJ_mass_SR,  h_disuperjet_mass_SR,  h_MSJ_mass_vs_MdSJ_SR,  h_MSJ_mass_vs_MdSJ_dijet,  h_nLooseBTags,  h_nMedBTags,  h_nTightBTags,
	    h_nfatjets,  h_MSJ_mass_vs_MdSJ_AT1b,  h_SJ_mass_AT1b,  h_disuperjet_mass_AT1b,  h_nAK4_AT1b,  h_nTightbTags_AT1b,
	    h_SJ1_BEST_score_1b,  h_SJ1_BEST_score_0b,  h_SJ2_BEST_score_1b,  h_SJ2_BEST_score_0b,  h_SJ1_decision_1b,  h_SJ1_decision_0b,
	    h_SJ2_decision_1b,  h_SJ2_decision_0b,  h_AK8_jet_mass_SR,  h_AK8_jet_mass_CR,  h_AK4_jet_mass_SR,  h_AK4_jet_mass_CR,  h_totHT_SR,  h_totHT_CR, h_totHT_AT0b, h_totHT_AT1b,
	    h_nfatjets_SR,  h_nfatjets_CR,  h_nAK4_SR,  h_nAK4_CR,  h_AK4_partonFlavour,  h_AK4_DeepJet_disc,  h_AK4_DeepJet_disc_all,  h_nAK4,  h_MSJ1_vs_MSJ2_SR,
	    h_MSJ1_vs_MSJ2_CR,  h_nAK4_all,  h_MSJ_mass_vs_MdSJ_AT0b, h_SJ_mass_AT0b,  h_disuperjet_mass_AT0b, h_SJ_mass_NN_SR,
	    h_disuperjet_mass_NN_SR, h_MSJ_mass_vs_MdSJ_NN_SR, h_SJ_mass_NN_CR, h_disuperjet_mass_NN_CR, h_MSJ_mass_vs_MdSJ_NN_CR, h_SJ_mass_NN_AT1b, h_disuperjet_mass_NN_AT1b,
	    h_MSJ_mass_vs_MdSJ_NN_AT1b, h_SJ_mass_NN_AT0b, h_disuperjet_mass_NN_AT0b, h_MSJ_mass_vs_MdSJ_NN_AT0b, h_scale_EventWeight, h_scale_EventWeight_SR, h_scale_EventWeight_CR, h_scale_EventWeight_AT1b, h_scale_EventWeight_AT0b,
	    h_SJ_mass_tagged_SJs_1b, h_SJ_mass_tagged_SJs_0b, h_SJ_mass_tagged_SJs, h_SJ2_mass_tagged_SJs_ATSJ1_1b,
		h_SJ2_mass_tagged_SJs_ATSJ1_0b, h_SJ2_mass_tagged_SJs_ATSJ1, h_SJ_mass_total_SJs_1b, h_SJ_mass_total_SJs_0b,
		h_SJ_mass_total_SJs, h_SJ2_mass_total_SJs_ATSJ1_1b, h_SJ2_mass_total_SJs_ATSJ1_0b, h_SJ2_mass_total_SJs_ATSJ1, h_SJ_mass_tagged_SJs_1b_NN,
		h_SJ_mass_tagged_SJs_0b_NN, h_SJ_mass_tagged_SJs_NN, h_SJ2_mass_tagged_SJs_ATSJ1_1b_NN, h_SJ2_mass_tagged_SJs_ATSJ1_0b_NN,
		h_SJ2_mass_tagged_SJs_ATSJ1_NN, h_SJ2_mass_total_SJs_ATSJ1_1b_NN, h_SJ2_mass_total_SJs_ATSJ1_0b_NN, h_SJ2_mass_total_SJs_ATSJ1_NN;
		delete h_AK8_eta, h_AK8_phi,h_AK4_eta,h_AK4_phi,h_JEC_uncert_AK8,h_JEC_uncert_AK4,h_AK8_JER, h_JEC_uncert_AK8_SR,h_JEC_uncert_AK4_SR,h_AK8_JER_SR;
		delete h_JEC_uncert_AK8_CR,h_JEC_uncert_AK4_CR,h_AK8_JER_CR, h_JEC_uncert_AK8_AT1b,h_JEC_uncert_AK4_AT1b,h_AK8_JER_AT1b, h_JEC_uncert_AK8_AT0b,h_JEC_uncert_AK4_AT0b,h_AK8_JER_AT0b;

		delete h_SJ_mass, h_disuperjet_mass, h_SJ_mass_uncorrected, h_disuperjet_mass_uncorrected;
	}

   outFile->Close();
   std::cout << "--------- Finished file " << inFileName << std::endl;
   delete f;
   delete outFile;
   return true;
}

void readTree()
{  

   bool debug 				= false;
   bool _verbose     	= false;
   bool runData			= false;
   bool runSignal    	= false;
   bool runBR	  			= false;
   bool runAll	 			= false;
   bool runDataBR    	= true;
   bool runSelection 	= false;
   bool runSingleFile 	= false;
   bool runSideband 		= false;
   int nFailedFiles = 0;
   std::string failedFiles = "";

   std::string runType = "main-band";
   std::string outputFolder = "processedFiles/";





   if(runSideband) outputFolder = "sideband_processedFiles/";
   std::string eos_path	 =  "root://cmseos.fnal.gov//store/user/ecannaer/skimmedFiles/";


   std::vector<std::string> dataYears = {"2015","2016","2017","2018"};

   if(runSelection) dataYears = {"2018"};




   std::vector<std::string> systematics = { "nom", "scale", "bTagSF_med", "bTagSF_tight",   "bTagSF_med_corr", "bTagSF_tight_corr",  "bTag_eventWeight_bc_T_corr", "bTag_eventWeight_light_T_corr", "bTag_eventWeight_bc_M_corr", "bTag_eventWeight_light_M_corr",  "bTag_eventWeight_bc_T_year", "bTag_eventWeight_light_T_year", "bTag_eventWeight_bc_M_year", "bTag_eventWeight_light_M_year",  "JER", "JER_eta193", "JER_193eta25", "JEC", "JEC_FlavorQCD", "JEC_RelativeBal",  "JEC_Absolute", "JEC_AbsoluteCal",  "JEC_AbsoluteScale", "JEC_Fragmentation", "JEC_AbsoluteMPFBias","JEC_RelativeFSR", "JEC_AbsoluteTheory", "JEC_AbsolutePU", "JEC_BBEC1_year",  "JEC_Absolute_year",  "JEC_RelativeSample_year", "PUSF", "topPt", "L1Prefiring", "pdf","renorm", "fact"};  // "scale"    "JEC_HF", "JEC_BBEC1", "JEC_EC2","JEC_HF_year", "JEC_EC2_year",   "bTag_eventWeight_bc_T", "bTag_eventWeight_light_T", "bTag_eventWeight_bc_M", "bTag_eventWeight_light_M", 


   //if(runSelection) systematics = {"JEC", "JEC_FlavorQCD", "JEC_RelativeBal",  "JEC_Absolute", "JEC_AbsoluteCal",  "JEC_AbsoluteScale", "JEC_Fragmentation", "JEC_AbsoluteMPFBias","JEC_RelativeFSR", "JEC_AbsoluteTheory", "JEC_AbsolutePU", "JEC_BBEC1_year",  "JEC_Absolute_year",  "JEC_RelativeSample_year"};


   // these were replaced by the below
   //std::vector<std::string> JEC1_ucerts = {"JEC_FlavorQCD", "JEC_RelativeBal", "JEC_HF", "JEC_BBEC1", "JEC_EC2", "JEC_BBEC1_year", "JEC_EC2_year"}; // the types of JEC uncertainties stored in the "JEC1" file for BR/data
   //std::vector<std::string> JEC2_ucerts = {"JEC_Absolute_year", "JEC_HF_year", "JEC_RelativeSample_year", "AbsoluteCal","AbsoluteTheory", "AbsolutePU", "Absolute", "JEC"}; // the types of JEC uncertainties stored in the "JEC1" file for bR/data

   //std::vector<std::string> sig_JEC1_ucerts = {"JEC_FlavorQCD", "JEC_RelativeBal", "JEC_HF", "JEC_BBEC1", "JEC_EC2", "JEC_BBEC1_year", "JEC_EC2_year", "JEC_Absolute_year", "JEC_HF_year", "JEC_RelativeSample_year", "JEC"}; // the types of uncertainties stored in the "JEC1" file for signal
   //std::vector<std::string> sig_nom_ucerts =  {"nom", "JER_eta193", "JER_193eta25", "JER", "AbsoluteCal","AbsoluteTheory", "AbsolutePU", "Absolute"}; // the types of JEC uncertainties stored in the "nom" file for signal


   std::vector<std::string> JEC1_ucerts = {"JEC_FlavorQCD", "JEC_RelativeBal","JEC_BBEC1_year",  "JEC_AbsoluteScale", "JEC_Fragmentation", "JEC_AbsoluteMPFBias","JEC_RelativeFSR", "JEC_AbsoluteTheory"}; // the types of JEC uncertainties stored in the "JEC1" file for BR/data
   std::vector<std::string> JEC2_ucerts = {"JEC_Absolute_year",  "JEC_RelativeSample_year", "JEC_AbsoluteCal", "JEC_AbsolutePU", "JEC_Absolute", "JEC"}; // the types of JEC uncertainties stored in the "JEC1" file for bR/data

   std::vector<std::string> sig_JEC1_ucerts = {"JEC_FlavorQCD", "JEC_RelativeBal",  "JEC_BBEC1_year",  "JEC_Absolute_year", "JEC_RelativeSample_year", "JEC", "JEC_AbsoluteScale", "JEC_Fragmentation", "JEC_AbsoluteTheory"}; // the types of uncertainties stored in the "JEC1" file for signal
   std::vector<std::string> sig_nom_ucerts =  {"nom", "JER_eta193", "JER_193eta25", "JER", "JEC_AbsoluteCal", "JEC_AbsolutePU", "JEC_Absolute", "JEC_AbsoluteMPFBias","JEC_RelativeFSR"}; // the types of JEC uncertainties stored in the "nom" file for signal


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
		std::cout << ("Deleting old " + *dataYear + " ROOT files in /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combimedROOT/"+outputFolder +  " .").c_str() << std::endl;
		int delete_result = 1;

		// delete existing processed files 
		if((runDataBR)||(runBR)||(runAll) ) 
		{
			delete_result *= system( ("rm /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/"+outputFolder +  "*QCD*" + *dataYear+ "*.root").c_str() ) ;
			delete_result *= system( ("rm /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/"+outputFolder +  "*ST_*" + *dataYear+ "*.root").c_str() ) ;
			delete_result *= system( ("rm /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/"+outputFolder +  "*TTTo*" + *dataYear+ "*.root").c_str() ) ;
			delete_result *= system( ("rm /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/"+outputFolder +  "*TTJets*" + *dataYear+ "*.root").c_str() ) ;
		}
		if((runSignal)||(runAll) ) 
		{
			delete_result *= system( ("rm /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combimedROOT/"+outputFolder +  "*Suu*" + *dataYear+ "*.root").c_str() ) ;
		}
		if((runDataBR)||(runData)||(runAll) ) 
		{
			delete_result *= system( ("rm /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combimedROOT/"+outputFolder +  "*data*" + *dataYear+ "*.root").c_str() ) ;
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

		if(!runSideband)  ///////// RUN MAIN-BAND, get list of samples to run over
		{
			if (runAll)
			{
				if(*dataYear == "2015")
				{
					dataBlocks = {"dataB-ver2_","dataC-HIPM_","dataD-HIPM_","dataE-HIPM_","dataF-HIPM_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_",  "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_","QCDMC_Pt_170to300_",
            "QCDMC_Pt_300to470_",
            "QCDMC_Pt_470to600_",
            "QCDMC_Pt_600to800_",
            "QCDMC_Pt_800to1000_",
            "QCDMC_Pt_1000to1400_",
            "QCDMC_Pt_1400to1800_",
            "QCDMC_Pt_1800to2400_",
            "QCDMC_Pt_2400to3200_",
            "QCDMC_Pt_3200toInf_"}; // dataB-ver1 not present
				}
				else if(*dataYear == "2016")
				{
					dataBlocks = {"dataF_", "dataG_", "dataH_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_", "TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_","QCDMC_Pt_170to300_",
            "QCDMC_Pt_300to470_",
            "QCDMC_Pt_470to600_",
            "QCDMC_Pt_600to800_",
            "QCDMC_Pt_800to1000_",
            "QCDMC_Pt_1000to1400_",
            "QCDMC_Pt_1400to1800_",
            "QCDMC_Pt_1800to2400_",
            "QCDMC_Pt_2400to3200_",
            "QCDMC_Pt_3200toInf_"};
				}
				else if(*dataYear == "2017")
				{
					dataBlocks = {"dataB_","dataC_","dataD_","dataE_", "dataF_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_","QCDMC_Pt_170to300_",
            "QCDMC_Pt_300to470_",
            "QCDMC_Pt_470to600_",
            "QCDMC_Pt_600to800_",
            "QCDMC_Pt_800to1000_",
            "QCDMC_Pt_1000to1400_",
            "QCDMC_Pt_1400to1800_",
            "QCDMC_Pt_1800to2400_",
            "QCDMC_Pt_2400to3200_",
            "QCDMC_Pt_3200toInf_"};
				}
				else if(*dataYear == "2018")
				{
					dataBlocks = {"dataA_","dataB_","dataC_","dataD_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_","QCDMC_Pt_170to300_",
            "QCDMC_Pt_300to470_",
            "QCDMC_Pt_470to600_",
            "QCDMC_Pt_600to800_",
            "QCDMC_Pt_800to1000_",
            "QCDMC_Pt_1000to1400_",
            "QCDMC_Pt_1400to1800_",
            "QCDMC_Pt_1800to2400_",
            "QCDMC_Pt_2400to3200_",
            "QCDMC_Pt_3200toInf_"};
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
			  dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_",
			"QCDMC_Pt_300to470_",
            "QCDMC_Pt_470to600_",
            "QCDMC_Pt_600to800_",
            "QCDMC_Pt_800to1000_",
            "QCDMC_Pt_1000to1400_",
            "QCDMC_Pt_1400to1800_",
            "QCDMC_Pt_1800to2400_",
            "QCDMC_Pt_2400to3200_",
            "QCDMC_Pt_3200toInf_"};
			}
			else if(runDataBR)
			{
				std::cout << "Running as data+BR" << std::endl;
				if(*dataYear == "2015")
				{
					dataBlocks = {"dataB-ver2_","dataC-HIPM_","dataD-HIPM_","dataE-HIPM_","dataF-HIPM_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_",
				"QCDMC_Pt_170to300_",
				"QCDMC_Pt_300to470_",
            "QCDMC_Pt_470to600_",
            "QCDMC_Pt_600to800_",
            "QCDMC_Pt_800to1000_",
            "QCDMC_Pt_1000to1400_",
            "QCDMC_Pt_1400to1800_",
            "QCDMC_Pt_1800to2400_",
            "QCDMC_Pt_2400to3200_",
            "QCDMC_Pt_3200toInf_"}; // dataB-ver1 not present
				}
				else if(*dataYear == "2016")
				{
					dataBlocks = {"dataF_", "dataG_", "dataH_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_",
				"QCDMC_Pt_170to300_",
				"QCDMC_Pt_300to470_",
            "QCDMC_Pt_470to600_",
            "QCDMC_Pt_600to800_",
            "QCDMC_Pt_800to1000_",
            "QCDMC_Pt_1000to1400_",
            "QCDMC_Pt_1400to1800_",
            "QCDMC_Pt_1800to2400_",
            "QCDMC_Pt_2400to3200_",
            "QCDMC_Pt_3200toInf_"};
				}
				else if(*dataYear == "2017")
				{
					dataBlocks = {"dataB_","dataC_","dataD_","dataE_", "dataF_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_",
				"QCDMC_Pt_170to300_",
				"QCDMC_Pt_300to470_",
            "QCDMC_Pt_470to600_",
            "QCDMC_Pt_600to800_",
            "QCDMC_Pt_800to1000_",
            "QCDMC_Pt_1000to1400_",
            "QCDMC_Pt_1400to1800_",
            "QCDMC_Pt_1800to2400_",
            "QCDMC_Pt_2400to3200_",
            "QCDMC_Pt_3200toInf_"};
				}
				else if(*dataYear == "2018")
				{
					dataBlocks = {"dataA_","dataB_","dataC_","dataD_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_",
				"QCDMC_Pt_170to300_",
				"QCDMC_Pt_300to470_",
            "QCDMC_Pt_470to600_",
            "QCDMC_Pt_600to800_",
            "QCDMC_Pt_800to1000_",
            "QCDMC_Pt_1000to1400_",
            "QCDMC_Pt_1400to1800_",
            "QCDMC_Pt_1800to2400_",
            "QCDMC_Pt_2400to3200_",
            "QCDMC_Pt_3200toInf_"};
				}   
			}
			else if(runSelection)
			{

				dataBlocks = {



				"QCDMC_Pt_800to1000_",
            "QCDMC_Pt_1000to1400_",
            "QCDMC_Pt_1400to1800_"

				/*"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_",
				//"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"

				"QCDMC_Pt_170to300_",
            "QCDMC_Pt_300to470_",
            "QCDMC_Pt_470to600_",
            "QCDMC_Pt_600to800_",
            "QCDMC_Pt_800to1000_",
            "QCDMC_Pt_1000to1400_",
            "QCDMC_Pt_1400to1800_",
            "QCDMC_Pt_1800to2400_",
            "QCDMC_Pt_2400to3200_",
            "QCDMC_Pt_3200toInf_"  */

            } ; 
				//dataBlocks = {"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"};
			}
			else if ( runSingleFile)
			{

				double nEvents = 0, nHTcut  = 0, nAK8JetCut = 0, nHeavyAK8Cut = 0, nBtagCut = 0, nDoubleTagged = 0, nNoBjets = 0;
				double nDoubleTaggedCR = 0, NNDoubleTag = 0, nZeroBtagAntiTag = 0, nOneBtagAntiTag = 0;
				double nNN_SR = 0, nNN_CR = 0 , nNN_AT1b = 0,nNN_AT0b = 0;	  

				std::string dataYear = "2018";
				std::string systematic = "nom";
				std::string dataBlock = "Suu4TeV_chi1TeV_";

				///   Suu6_chi1p5_ZTZT_2018_genPartFiltered_combimed.root
				std::string inFileName = ( dataBlock+  dataYear + "_genPartFiltered_combimed.root").c_str();
				std::string outFileName = ( dataBlock+  dataYear + "_genPartFiltered_processed.root").c_str();

				doThings(inFileName,outFileName,nEvents,nHTcut,nAK8JetCut,nHeavyAK8Cut,nBtagCut,nDoubleTagged,nNoBjets,nDoubleTaggedCR, NNDoubleTag,nZeroBtagAntiTag, nOneBtagAntiTag, nNN_SR, nNN_CR, nNN_AT1b,nNN_AT0b, dataYear,systematic, dataBlock, runType );

				std::cout << "Total 1b double tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/1+ b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nBtagCut << "/" << nDoubleTagged << std::endl;
				std::cout << "Total 0b double tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/0 b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nNoBjets << "/" << nDoubleTaggedCR << std::endl;
				std::cout << "Total 1b anti tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/0 b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nBtagCut << "/" << nOneBtagAntiTag << std::endl;
				std::cout << "Total 0b anti tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/0 b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nNoBjets << "/" << nZeroBtagAntiTag << std::endl;
				//std::cout << "number of events NN tagged: " << NNDoubleTag << std::endl;
				std::cout << "Total events in the NN_SR/NN_CR/NN_AT1b/NN_AT0b: " << nNN_SR << "/" << nNN_CR << "/" << nNN_AT1b << "/" << nNN_AT0b << std::endl;
				std::cout << "Finished with "<< inFileName << "." << std::endl;
				std::cout << std::endl;
				std::cout << std::endl;
				std::cout << std::endl;
				std::cout << std::endl;
				return;
			}
			else
			{
				std::cout << "No/incorrect sample options selected" << std::endl;
				return;
			}
		}
		else if(runSideband) // get lists of all the samples to run over for the sideband
		{
			runType = "side-band";
			eos_path	 =   "root://cmseos.fnal.gov//store/user/ecannaer/sideband_skimmedFiles/";     //"root://cmsxrootd.fnal.gov//store/user/ecannaer/sideband_skimmedFiles/";

			if((runDataBR) || (runAll))
			{
				if(*dataYear == "2015")
				{
					dataBlocks = {"dataB-ver2_","dataC-HIPM_","dataD-HIPM_","dataE-HIPM_","dataF-HIPM_","QCDMC1000to1500_","QCDMC1500to2000_","TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"}; // dataB-ver1 not present
				}
				else if(*dataYear == "2016")
				{
					dataBlocks = {"dataF_", "dataG_", "dataH_","QCDMC1000to1500_","QCDMC1500to2000_","TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"};
				}
				else if(*dataYear == "2017")
				{
					dataBlocks = {"dataB_","dataC_","dataD_","dataE_", "dataF_","QCDMC1000to1500_","QCDMC1500to2000_","TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_",  "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"};
				}
				else if(*dataYear == "2018")
				{
					dataBlocks = {"dataA_","dataB_","dataC_","dataD_","QCDMC1000to1500_","QCDMC1500to2000_","TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_",  "ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"};
				}   
			}
			else if(runSignal)
			{
				dataBlocks = signalFilePaths;
			}
			else
			{
				std::cout << "No options selected" << std::endl;
				return;
			}
			if(runAll)
			{
				dataBlocks.reserve( dataBlocks.size() + signalFilePaths.size() ); // preallocate memory
				dataBlocks.insert( dataBlocks.end(), signalFilePaths.begin(), signalFilePaths.end() );
			}
		}
		

		for(auto systematic = systematics.begin();systematic<systematics.end();systematic++)
		{

			std::cout << "------------ Looking at systematic: " << *systematic << " --------------" << std::endl;

			for(auto dataBlock = dataBlocks.begin();dataBlock < dataBlocks.end();dataBlock++)
			{
				//if(( (*dataBlock).find("Suu")!= std::string::npos ) &&( *systematic == "JER" )) continue; // why am I doing this?

				if ((*dataBlock).find("data")!= std::string::npos)
				{  
					// these are MC-only systematics 
					if(*systematic != "nom") continue; // don't do any variations for data_obs
					//if ((*systematic == "bTagSF_tight") || (*systematic == "bTagSF_med") || (*systematic == "bTagSF") || (*systematic == "PUSF") || (*systematic == "JER")  || (*systematic == "JER_eta193") || (*systematic == "JER_193eta25") ||  (*systematic == "topPt") || (*systematic == "pdf") || (*systematic == "scale") || (*systematic == "fact") || (*systematic == "renorm") || (*systematic=="bTag_eventWeight_bc_T") ||  (*systematic=="bTag_eventWeight_light_T") || (*systematic =="bTag_eventWeight_bc_M") || (*systematic ==  "bTag_eventWeight_light_M") || (*systematic=="bTag_eventWeight_bc_T_year") ||  (*systematic=="bTag_eventWeight_light_T_year") || (*systematic =="bTag_eventWeight_bc_M_year") || (*systematic ==  "bTag_eventWeight_light_M_year") ) continue;
				}
				
				double nEvents = 0, nHTcut  = 0, nAK8JetCut = 0, nHeavyAK8Cut = 0, nBtagCut = 0, nDoubleTagged = 0, nNoBjets = 0;
				double nDoubleTaggedCR = 0, NNDoubleTag = 0, nZeroBtagAntiTag = 0, nOneBtagAntiTag = 0;
				double nNN_SR = 0, nNN_CR = 0 , nNN_AT1b = 0,nNN_AT0b = 0;

				std::string year = *dataYear;
				std::string systematic_str;  

				if ((*systematic == "nom" ) || (*systematic == "bTagSF_tight" ) || (*systematic == "bTagSF_med") || (*systematic == "bTagSF_tight_corr" ) || (*systematic == "bTagSF_med_corr") || (*systematic == "bTagSF")|| (*systematic == "PUSF" ) || (*systematic == "pdf") || (*systematic == "L1Prefiring") || (*systematic == "pdf") || (*systematic == "topPt")|| (*systematic == "scale")|| (*systematic == "renorm") || (*systematic == "fact")  ||  (*systematic=="bTag_eventWeight_bc_T") ||  (*systematic=="bTag_eventWeight_light_T") || (*systematic =="bTag_eventWeight_bc_M") || (*systematic ==  "bTag_eventWeight_light_M") ||  (*systematic =="bTag_eventWeight_bc_T_corr") ||  (*systematic =="bTag_eventWeight_light_T_corr") ||  (*systematic =="bTag_eventWeight_bc_M_corr") || (*systematic =="bTag_eventWeight_light_M_corr") || (*systematic=="bTag_eventWeight_bc_T_year") ||  (*systematic=="bTag_eventWeight_light_T_year") || (*systematic =="bTag_eventWeight_bc_M_year") || (*systematic ==  "bTag_eventWeight_light_M_year") ) systematic_str = "nom";
				else if ( std::find(JEC1_ucerts.begin(), JEC1_ucerts.end(), *systematic) != JEC1_ucerts.end() ) systematic_str = "JEC1";
				else if ( std::find(JEC2_ucerts.begin(), JEC2_ucerts.end(), *systematic) != JEC2_ucerts.end() ) systematic_str = "JEC2";
				else if ( systematic->find("JER") != std::string::npos ) systematic_str = "JER";
				else {systematic_str = *systematic;}



				// find the correct systematic_str for signal
				if(  (*dataBlock).find("Suu")!= std::string::npos  )
				{
					if ( std::find(sig_JEC1_ucerts.begin(), sig_JEC1_ucerts.end(), *systematic) != sig_JEC1_ucerts.end() ) systematic_str = "JEC";
					else if ( std::find(sig_nom_ucerts.begin(), sig_nom_ucerts.end(), *systematic) != sig_nom_ucerts.end() ) systematic_str = "nom";
					else { systematic_str = "nom"; }
				}



				if(debug) std::cout << "@@@@@@@@@@@@@ WARNING: YOU ARE IN DEBUG MODE. NOT ALL FILES WILL BE RUN. @@@@@@@@@@@@@@" << std::endl;
				std::string inFileName = (eos_path + *dataBlock+  year +  "_"+ systematic_str+ "_SKIMMED.root").c_str();
				

				// if this is JEC and the uncertainty isn't in the JEC1 list, it must be in the nom list and should use the nom naming scheme
				if (( inFileName.find("Suu") != std::string::npos) &&  !( std::find(sig_JEC1_ucerts.begin(), sig_JEC1_ucerts.end(), *systematic) != sig_JEC1_ucerts.end()     )  ) inFileName = (eos_path+ *dataBlock+  year + "_SKIMMED.root").c_str();
				std::string outFileName = (outputFolder  + *dataBlock+ year + "_processed.root").c_str();

				if( failedFiles.find( (*dataBlock +"/" + year ).c_str()  ) != std::string::npos) continue; // skip files that failed for other uncertainties


				std::cout << "Reading File " << inFileName << " for year,sample,systematic " << year << "/" <<*dataBlock << "/" << *systematic<< std::endl;

				if (!doThings(inFileName,outFileName,nEvents,nHTcut,nAK8JetCut,nHeavyAK8Cut,nBtagCut,nDoubleTagged,nNoBjets,nDoubleTaggedCR, NNDoubleTag,nZeroBtagAntiTag, nOneBtagAntiTag, nNN_SR, nNN_CR, nNN_AT1b, nNN_AT0b, *dataYear,*systematic, *dataBlock,runType, _verbose ))
				{
					std::cout << "ERROR: Failed for year/sample/systematic: " << year<< "/" << *dataBlock << "/" << *systematic << std::endl;
					if( !(failedFiles.find( (*dataBlock +"/" + year ).c_str()  ) != std::string::npos)) // don't copy this multiple times
					{
						failedFiles+= (", "+ *dataBlock +"/" + year +"/"  + systematic_str ).c_str();
						nFailedFiles++;
					}
				}
				std::cout << " @@@@@@@@ There have been " << nFailedFiles << " failed jobs files @@@@@@@@" << std::endl;
				std::cout << "Failed files: " << failedFiles << std::endl;
				if(_verbose)
				{
					std::cout << "----------------------------------- Starting " << *dataBlock << "-----------------------------------"<< std::endl;
					std::cout << "Total 1b double tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/1+ b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nBtagCut << "/" << nDoubleTagged << std::endl;
					std::cout << "Total 0b double tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/0 b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nNoBjets << "/" << nDoubleTaggedCR << std::endl;
					std::cout << "Total 1b anti tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/0 b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nBtagCut << "/" << nOneBtagAntiTag << std::endl;
					std::cout << "Total 0b anti tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/0 b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nNoBjets << "/" << nZeroBtagAntiTag << std::endl;
					std::cout << "Total events in the NN_SR/NN_CR/NN_AT1b/NN_AT0b: " << nNN_SR << "/" << nNN_CR << "/" << nNN_AT1b << "/" << nNN_AT0b << std::endl;
					//std::cout << "number of events NN tagged: " << NNDoubleTag << std::endl;
					std::cout << "Finished with "<< inFileName << "." << std::endl;
					std::cout << std::endl;
					std::cout << std::endl;
					std::cout << std::endl;
					std::cout << std::endl;
				}
			} // end dataBlock loop
		} // end systematic loop
   } // end year loop
} // end function


