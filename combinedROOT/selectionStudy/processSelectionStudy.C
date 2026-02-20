#include <iostream>
#include <string>
#include "TLorentzVector.h"
#include <cstdlib>
#include <sstream>

#include <sys/stat.h>
#include <sys/types.h>
#include <cerrno>
#include <cstring>

// processSelectionStudy.C
// create histograms for all grid points:
	//HT AK4 jet ET:  200, 300, 400    # 150, 250, 350, 100,
	//jet HT: 1600, 1800, 2000, 2200
	//nAK4: 2, 3, 4
	//nHeavyAK8, 1,2,3

using namespace std;
bool doThings(std::string inFileName, std::string outFileName, std::string dataYear,std::string systematic, std::string dataBlock, std::string WP, bool runOptimal = false, bool verbose = false)
{

   TH1::SetDefaultSumw2();
   TH2::SetDefaultSumw2();
   int eventnum = 0;int nhadevents = 0; int nfatjets = 0, totEventsUncut=0,total_1b = 0, total_0b = 0;
   int SJ_nAK4_300[100];
   double AK4_DeepJet_disc[100], AK4_pt[100], AK4_mass[100], superJet_mass[100], jet_pt[100], jet_eta[100], jet_phi[100], jet_mass[100],AK4_eta[100],AK4_phi[100];
   double JEC_uncert_AK8[100], JEC_uncert_AK4[100], AK8_JER[100];
   double diSuperJet_mass, dijetMassOne, dijetMassTwo, bTag_eventWeight_M_nom = 1, bTag_eventWeight_M_up = 1, bTag_eventWeight_M_down = 1, pdf_weight = 1.0,  scale_weight = 1.0, SJ1_BEST_scores, SJ2_BEST_scores, prefiringWeight;
   double  PU_eventWeight = 1.0, totHT = 0;   
   int nfatjet_pre, nAK4, nSuperJets, nTau_VLooseVsJet_VLooseVsMuon_VVLooseVse, nMuons_looseID_medIso, nElectrons_looseID_looseISO;
   bool AK4_fails_veto_map[100], AK8_fails_veto_map[100],fatjet_isHEM[100],jet_isHEM[100];

   std::vector<std::string> systematic_suffices;

   if(systematic == "nom") systematic_suffices = {""};
   else{ systematic_suffices = {"up","down"}; }

   bool passesPFHT = false, passesPFJet = false;

   const char *_inFilename = inFileName.c_str();
   const char *_outFilename = outFileName.c_str();

   TFile *f = TFile::Open(_inFilename,"READ");

   if ((f == nullptr)||(f->IsZombie()) )
   {
		std::cout << "ERROR: File " << _inFilename << " not found - skipping !!" << std::endl;
		delete f;
		return false;
   }
   TFile * outFile = TFile::Open(_outFilename,"UPDATE");






   /////////////////////////////////////////////////////////////////
   // split up the input "WP" to the different cuts it represents
   /////////////////////////////////////////////////////////////////

   std::string ET_cut;   // ----> goes to the input tree name and output folder name
   double HT_cut;
   double nAK8_cut;
   double nHeavyAK8_cut;

	std::stringstream ss(WP);
	std::getline(ss, ET_cut, '_');
	std::string tmp;
	std::getline(ss, tmp, '_');       HT_cut        = std::stod(tmp);
	std::getline(ss, tmp, '_');       nAK8_cut      = std::stod(tmp);
	std::getline(ss, tmp, '_');       nHeavyAK8_cut = std::stod(tmp);


	std::cout << "WP is " << WP << ", HT cut is " << HT_cut<< ", nAK8 cut is " <<nAK8_cut << ", nHeavyAK8 cut is " << nHeavyAK8_cut << std::endl;



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

		}
	
		std::string tree_name;
		std::string systematic_use = systematic;

		if((systematic == "nom" )|| (systematic == "bTagSF_med")  || (systematic == "bTagSF") || (systematic == "PUSF" )  || (systematic == "pdf") || (systematic == "scale"))
		{
			tree_name = "clusteringAnalyzerAll_" + ET_cut +  "_nom/tree_nom";
			systematic_use = "";
		}
		else{tree_name =  "clusteringAnalyzerAll_" + ET_cut + "_" + systematic+"_"+*systematic_suffix  + "/tree_" + systematic+"_"+*systematic_suffix  ; }

		TTree *t1;
		Int_t nentries;

		try
		{  

			t1 = (TTree*)f->Get(   ( tree_name ).c_str()    );
			if(t1 == nullptr)
			{
				std::cout << "ERROR: tree not found - " << ( tree_name ).c_str()  <<std::endl;
				delete f;
				return false;
			}
			nentries = t1->GetEntries();
		}
		catch(...)
		{
			std::cout << "ERROR: tree not found - " << ( tree_name  ).c_str()  <<std::endl;
			delete f;
			return false;
		}
		std::cout << "Successfully got tree " << tree_name << std::endl;
		

		// main 2D hists

		TH2F *h_MSJ_mass_vs_MdSJ_prebTag   = new TH2F("h_MSJ_mass_vs_MdSJ_prebTag","Superjet mass vs diSuperjet mass (before b-tag cut) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_postbTag  = new TH2F("h_MSJ_mass_vs_MdSJ_postbTag","Superjet mass vs diSuperjet mass (after b-tag cut) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_postSJTag = new TH2F("h_MSJ_mass_vs_MdSJ_postSJTag","Superjet mass vs diSuperjet mass (post SJ double-tag) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		// HISTS FOR OPTIMAL WP STUDY 
		TH1F* h_totHT;TH1F* h_nfatjets_pre;TH1F* h_nfatjets;TH1F* h_nAK4;TH1F* h_dijet_mass;TH1F* h_AK8_jet_mass;TH1F* h_AK8_jet_pt;TH1F* h_AK8_eta;TH1F* h_AK8_phi;TH1F* h_AK4_eta;TH1F* h_AK4_phi;TH1F* h_nCA4_300_1b;TH1F* h_nCA4_300_0b;TH1F* h_SJ_mass;TH1F* h_disuperjet_mass;TH1F* h_AK8_jet_mass_SR;TH1F* h_AK8_jet_mass_CR;TH1F* h_totHT_SR;TH1F* h_totHT_CR;TH1F* h_SJ_mass_SR;TH1F* h_disuperjet_mass_SR;
		TH2F *h_MSJ_mass_vs_MdSJ_SR ;  TH1F* h_SJ_mass_CR;TH1F* h_disuperjet_mass_CR;TH2F *h_MSJ_mass_vs_MdSJ_CR; TH1F * h_pdf_EventWeight_SR;
		TH1F * h_scale_EventWeight_SR;TH1F* h_PU_eventWeight_SR;TH1F* h_bTag_eventWeight_M_SR;TH1F* h_L1PrefiringWeight_SR;TH1F* h_Full_Event_Weight_SR;TH1F* h_JEC_uncert_AK8_SR;TH1F* h_JEC_uncert_AK4_SR;TH1F* h_AK8_JER_SR;
		TH1F * h_pdf_EventWeight_CR;
		TH1F * h_scale_EventWeight_CR;TH1F* h_PU_eventWeight_CR;TH1F* h_bTag_eventWeight_M_CR;TH1F* h_L1PrefiringWeight_CR;TH1F* h_JEC_uncert_AK8_CR;TH1F* h_JEC_uncert_AK4_CR;TH1F* h_AK8_JER_CR;TH1F* h_nMedBTags;
		TH1F* h_AK4_jet_mass;TH1F* h_AK4_jet_mass_SR;TH1F* h_AK4_jet_mass_CR;TH1F* h_nAK4_pt75;TH1F* h_nAK4_pt75_SR;TH1F* h_nAK4_pt75_CR;
		TH1F* h_AK8_eta_SR;TH1F* h_AK8_phi_SR;TH1F* h_AK4_eta_SR;TH1F* h_AK4_phi_SR;TH1F* h_AK8_eta_CR;TH1F* h_AK8_phi_CR;TH1F* h_AK4_eta_CR;TH1F* h_AK4_phi_CR;
		TH1F* h_AK8_jet_pt_SR; TH1F* h_AK8_jet_pt_CR; TH1F*  h_Full_Event_Weight_CR;

		if(runOptimal)
		{

			h_totHT  = new TH1F("h_totHT","Total Event H_{T} (w/ L1Prefire, top p_{T} and PU weights); H_{T} [GeV]; Events / 200 GeV",50,0.,10000);
			h_nfatjets_pre  = new TH1F("h_nfatjets_pre","Number of AK8 Jets (p_{T} > 500 GeV, M_{PUPPI} > 45 GeV) per Event ;nAK8 Jets; Events",10,-0.5,9.5);
			h_nfatjets = new TH1F("h_nfatjets","Number of AK8 Jets (E_{T} > 300 GeV per Event ;nAK8 Jets; Events",10,-0.5,9.5);
			h_nAK4 = new TH1F("h_nAK4","Number of AK4 jets;# AK4 jets; Events",20,-0.5,19.5);
			h_dijet_mass = new TH1F("h_dijet_mass","Dijet Mass (after nAK8 cut); Mass [GeV]; Events / 80 GeV",50,0,4000);
			h_AK8_jet_mass = new TH1F("h_AK8_jet_mass","Mass of Selected AK8 jets (after pre-selection); Mass [GeV] ;Events / 50 GeV",40,0,2000);
			h_AK8_jet_pt = new TH1F("h_AK8_jet_pt","p_{T} of Selected AK8 jets (after pre-selection); p_{T} [GeV]; Events / 100 GeV",50,0,5000);
			h_AK8_eta = new TH1F("h_AK8_eta","Eta of AK8 Jets (pre-selected); Eta; Events",50,-3.0,3.0);
			h_AK8_phi = new TH1F("h_AK8_phi","Phi of AK8 jets (pre-selected); Phi; Events",50,-3.5,3.5);
			h_AK4_eta = new TH1F("h_AK4_eta","Eta of AK4 Jets (pre-selected); Eta; Events",50,-3.0,3.0);
			h_AK4_phi = new TH1F("h_AK4_phi","Phi of AK4 jets (pre-selected); Phi; Events",50,-3.5,3.5);
			h_nCA4_300_1b  = new TH1F("h_nCA4_300_1b","Number of Reclustered SJ CA4 jets (E > 300 GeV) in the 1b region;nJets; Events",10,-0.5,9.5);
			h_nCA4_300_0b  = new TH1F("h_nCA4_300_0b","Number of Reclustered SJ CA4 jets (E > 300 GeV) in the 0b region;nJets; Events",10,-0.5,9.5);
			h_SJ_mass  = new TH1F("h_SJ_mass","SuperJet Mass (preselected) (cut-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
			h_disuperjet_mass  = new TH1F("h_disuperjet_mass","diSuperJet Mass (preselected) (cut-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
			h_AK8_jet_mass_SR  = new TH1F("h_AK8_jet_mass_SR","AK8 Jet Mass (SR region);Mass [GeV]; Events / 30 GeV",50,0.,1500);
			h_AK8_jet_mass_CR  = new TH1F("h_AK8_jet_mass_CR","AK8 Jet Mass (CR);Mass [GeV]; Events / 30 GeV",50,0.,1500);
			h_totHT_SR  = new TH1F("h_totHT_SR","Event H_{T} (SR);H_{T} [GeV]; Events / 200 5GeV",50,0.,10000);
			h_totHT_CR  = new TH1F("h_totHT_CR","Event H_{T} (CR);H_{T} [GeV]; Events / 200 GeV",50,0.,10000);
			h_SJ_mass_SR  = new TH1F("h_SJ_mass_SR","SuperJet Mass (Signal Region) (cut-based);Mass [GeV]; Events / 100 GeV",40,0.,5000);
			h_disuperjet_mass_SR  = new TH1F("h_disuperjet_mass_SR","diSuperJet Mass (Signal Region) (cut-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
			h_MSJ_mass_vs_MdSJ_SR = new TH2F("h_MSJ_mass_vs_MdSJ_SR","Superjet mass vs diSuperjet mass (Signal Region) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
			h_SJ_mass_CR  = new TH1F("h_SJ_mass_CR","SuperJet Mass (Control Region) (cut-based);Mass [GeV]; Events / 125 GeV",40,0.,5000);
			h_disuperjet_mass_CR  = new TH1F("h_disuperjet_mass_CR","diSuperJet Mass (Control Region) (cut-based);Mass [GeV]; Events / 200 GeV",50,0.,10000);
			h_MSJ_mass_vs_MdSJ_CR = new TH2F("h_MSJ_mass_vs_MdSJ_CR","Superjet mass vs diSuperjet mass (Control Region) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
			h_pdf_EventWeight_SR= new TH1F("h_pdf_EventWeight_SR", "PDF Event Weights (SR) ; Event Weight; Events",40,0.0,4.0);
			h_scale_EventWeight_SR= new TH1F("h_scale_EventWeight_SR", "Scale Event Weight (using envelope) (SR); Event Weight; Events",40,0.0,2.5);
			h_PU_eventWeight_SR  = new TH1F("h_PU_eventWeight_SR","Pileup Event Weights  (SR);Event Weight; Events",40,0.0,3.0);
			h_bTag_eventWeight_M_SR  = new TH1F("h_bTag_eventWeight_M_SR","b tagging Event Weights (medium WP)  (SR);Event Weight; Events",100,0.0,4.0);
			h_L1PrefiringWeight_SR  = new TH1F("h_L1PrefiringWeight_SR","L1 Prefiring Event Weights (SR);Event Weight  (SR); Events",40,0.0,1.5);
			h_Full_Event_Weight_SR  = new TH1F("h_Full_Event_Weight_SR","Full Event Weight (= product of all used event weights) (SR) ;Event Weight  (SR); Events",40,0.0,2.0);
			h_JEC_uncert_AK8_SR  = new TH1F("h_JEC_uncert_AK8_SR","AK8 JEC Uncertainty (SR);JEC Uncertainty; Jets",100,0.94,1.06);
			h_JEC_uncert_AK4_SR  = new TH1F("h_JEC_uncert_AK4_SR","AK4 JEC Uncertainty (SR);JEC Uncertainty; Jets",100,0.94,1.06);
			h_AK8_JER_SR  = new TH1F("h_AK8_JER_SR","AK8 JER Correction Factor (SR);Correction Factor; Jets",100,0.94,1.06);
			h_pdf_EventWeight_CR= new TH1F("h_pdf_EventWeight_CR", "PDF Event Weight (CR) ; Event Weight; Events",40,0.0,4.0);
			h_scale_EventWeight_CR= new TH1F("h_scale_EventWeight_CR", "Scale Event Weight (using envelope) (CR); Event Weight; Events",40,0.0,2.5);
			h_PU_eventWeight_CR  = new TH1F("h_PU_eventWeight_CR","Pileup Event Weights  (CR);Event Weight; Events",40,0.0,3.0);
			h_bTag_eventWeight_M_CR  = new TH1F("h_bTag_eventWeight_M_CR","b tagging Event Weights (medium WP)  (CR);Event Weight; Events",100,0.0,4.0);
			h_L1PrefiringWeight_CR  = new TH1F("h_L1PrefiringWeight_CR","L1 Prefiring Event Weights ;Event Weight  (CR); Events",40,0.0,1.5);
			h_JEC_uncert_AK8_CR  = new TH1F("h_JEC_uncert_AK8_CR","AK8 JEC Uncertainty (CR);JEC Uncertainty; Jets",100,0.94,1.06);
			h_JEC_uncert_AK4_CR  = new TH1F("h_JEC_uncert_AK4_CR","AK4 JEC Uncertainty (CR);JEC Uncertainty; Jets",100,0.94,1.06);
			h_AK8_JER_CR  = new TH1F("h_AK8_JER_CR","AK8 JER Correction Factor (CR);Correction Factor; Jets",100,0.94,1.06);
			h_nMedBTags = new TH1F("h_nMedBTags","Number of Mediumly b-tagged AK4 Jets; Events",10,-0.5,9.5);
			h_AK4_jet_mass  = new TH1F("h_AK4_jet_mass","AK4 Jet Mass;Mass [GeV]; Events / 25 GeV",40,0.,1000);
			h_AK4_jet_mass_SR  = new TH1F("h_AK4_jet_mass_SR","AK4 Jet Mass (SR region);Mass [GeV]; Events / 25 GeV",40,0.,1000);
			h_AK4_jet_mass_CR  = new TH1F("h_AK4_jet_mass_CR","AK4 Jet Mass (CR);Mass [GeV]; Events / 25 GeV",40,0.,1000);
			h_nAK4_pt75 = new TH1F("h_nAK4_pt75","Number of AK4 jets (p_{T} > 75 GeV);# AK4 jets; Events",20,-0.5,19.5);
			h_nAK4_pt75_SR = new TH1F("h_nAK4_pt75_SR","Number of AK4 jets (p_{T} > 75 GeV) (SR);# AK4 jets; Events",20,-0.5,19.5);
			h_nAK4_pt75_CR = new TH1F("h_nAK4_pt75_CR","Number of AK4 jets (p_{T} > 75 GeV) (CR);# AK4 jets; Events",20,-0.5,19.5);
			h_AK8_jet_pt_SR = new TH1F("h_AK8_jet_pt_SR","p_{T} of Selected AK8 jets (after pre-selection) (SR); p_{T} [GeV]; Events / 100 GeV",50,0,5000);
			h_AK8_jet_pt_CR = new TH1F("h_AK8_jet_pt_CR","p_{T} of Selected AK8 jets (after pre-selection) (CR); p_{T} [GeV]; Events / 100 GeV",50,0,5000);
			h_Full_Event_Weight_CR  = new TH1F("h_Full_Event_Weight_CR","Full Event Weight (= product of all used event weights) (CR) ;Event Weight  (SR); Events",40,0.0,2.0);

			h_AK8_eta_SR = new TH1F("h_AK8_eta_SR","Eta of AK8 Jets (SR); Eta; Events",50,-3.0,3.0);
			h_AK8_phi_SR = new TH1F("h_AK8_phi_SR","Phi of AK8 jets (SR); Phi; Events",50,-3.5,3.5);
			h_AK4_eta_SR = new TH1F("h_AK4_eta_SR","Eta of AK4 Jets (SR); Eta; Events",50,-3.0,3.0);
			h_AK4_phi_SR = new TH1F("h_AK4_phi_SR","Phi of AK4 jets (SR); Phi; Events",50,-3.5,3.5);

			h_AK8_eta_CR = new TH1F("h_AK8_eta_CR","Eta of AK8 Jets (CR); Eta; Events",50,-3.0,3.0);
			h_AK8_phi_CR = new TH1F("h_AK8_phi_CR","Phi of AK8 jets (CR); Phi; Events",50,-3.5,3.5);
			h_AK4_eta_CR = new TH1F("h_AK4_eta_CR","Eta of AK4 Jets (CR); Eta; Events",50,-3.0,3.0);
			h_AK4_phi_CR = new TH1F("h_AK4_phi_CR","Phi of AK4 jets (CR); Phi; Events",50,-3.5,3.5);

		}


   	////////////////////////////////////////////////////////////////////////////////////////////////////////
		t1->SetBranchAddress("passesPFHT", &passesPFHT); 
		t1->SetBranchAddress("passesPFJet", &passesPFJet); 

		t1->SetBranchAddress("nfatjets", &nfatjets);   
		t1->SetBranchAddress("nSuperJets", &nSuperJets);   
		t1->SetBranchAddress("diSuperJet_mass", &diSuperJet_mass);   
		t1->SetBranchAddress("nfatjet_pre", &nfatjet_pre);
		t1->SetBranchAddress("jet_pt", jet_pt);   
		t1->SetBranchAddress("jet_eta", jet_eta);   

		t1->SetBranchAddress("totHT", &totHT);
		t1->SetBranchAddress("superJet_mass", superJet_mass);   
		t1->SetBranchAddress("nAK4" , &nAK4); 
		t1->SetBranchAddress("AK4_eta", AK4_eta); 
		t1->SetBranchAddress("AK4_mass", AK4_mass); 
		t1->SetBranchAddress("lab_AK4_pt", AK4_pt); 
		t1->SetBranchAddress("dijetMassOne", &dijetMassOne); 
		t1->SetBranchAddress("dijetMassTwo", &dijetMassTwo); 
		t1->SetBranchAddress("AK4_DeepJet_disc", AK4_DeepJet_disc); 
		t1->SetBranchAddress("AK8_fails_veto_map", AK8_fails_veto_map); 
		t1->SetBranchAddress("fatjet_isHEM", fatjet_isHEM); 
		t1->SetBranchAddress("prefiringWeight_nom", &prefiringWeight); 
		t1->SetBranchAddress("SJ_nAK4_300", SJ_nAK4_300);     


		if(runOptimal)
		{
			t1->SetBranchAddress("AK4_phi", AK4_phi);     
			t1->SetBranchAddress("jet_mass", jet_mass);  
			t1->SetBranchAddress("jet_phi", jet_phi);   
			t1->SetBranchAddress("SJ_nAK4_300", SJ_nAK4_300);     
			t1->SetBranchAddress("SJ_nAK4_300", SJ_nAK4_300);  
			t1->SetBranchAddress("JEC_uncert_AK8", JEC_uncert_AK8); 
			t1->SetBranchAddress("JEC_uncert_AK4", JEC_uncert_AK4);   
			t1->SetBranchAddress("AK8_JER", AK8_JER);
		}


		// these weren't in the input SKIMMED files
      //t1->SetBranchAddress("nTau_VLooseVsJet_VLooseVsMuon_VVLooseVse", &nTau_VLooseVsJet_VLooseVsMuon_VVLooseVse); 
      //t1->SetBranchAddress("nMuons_looseID_medIso", &nMuons_looseID_medIso); 
      //t1->SetBranchAddress("nElectrons_looseID_looseISO", &nElectrons_looseID_looseISO); 

		// MC-only vars 
		if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos))
		{ 
			// nominal systematics
			t1->SetBranchAddress("bTag_eventWeight_M_nom", &bTag_eventWeight_M_nom);
			t1->SetBranchAddress("PU_eventWeight_nom", &PU_eventWeight);
		}

		pdf_weight = 1.0; 
		scale_weight = 1.0; 


		if ( (inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos)) 
		{
			if (systematic.find("bTag") != std::string::npos)
			{ 
				if     ((systematic == "bTagSF_med") && (*systematic_suffix == "up"))   t1->SetBranchAddress("bTag_eventWeight_M_up", &bTag_eventWeight_M_up);
				else if((systematic == "bTagSF_med") && (*systematic_suffix == "down")) t1->SetBranchAddress("bTag_eventWeight_M_down", &bTag_eventWeight_M_down);
				//t1->SetBranchAddress("bTag_eventWeight_M_up", &bTag_eventWeight_M_up);
				//t1->SetBranchAddress("bTag_eventWeight_M_down", &bTag_eventWeight_M_down);
			}
			//////// pileup systematic 
			else if((systematic == "PUSF") && (*systematic_suffix == "up"))   t1->SetBranchAddress("PU_eventWeight_up", &PU_eventWeight);
			else if((systematic == "PUSF") && (*systematic_suffix == "down")) t1->SetBranchAddress("PU_eventWeight_down", &PU_eventWeight);
			
			//////// pdf weight systematic 
			else if((systematic == "pdf") && (*systematic_suffix == "up"))   t1->SetBranchAddress("PDFWeightUp_BEST", &pdf_weight);
			else if((systematic == "pdf") && (*systematic_suffix == "down")) t1->SetBranchAddress("PDFWeightDown_BEST", &pdf_weight);

			/////// scale stuff 
			//////// renormalization and factorization scale systematics COMBINED
			else if((systematic == "scale") && (*systematic_suffix == "up"))   t1->SetBranchAddress("PDFWeights_envelope_scale_uncertainty_up", &scale_weight); // alternative:  PDFWeights_renormWeight_up
			else if((systematic == "scale") && (*systematic_suffix == "down")) t1->SetBranchAddress("PDFWeights_envelope_scale_uncertainty_down", &scale_weight); // alternative: PDFWeights_renormWeight_down
		}

		double medDeepCSV_DeepJet;

		if(dataYear == "2015")
		{
			medDeepCSV_DeepJet   = 0.2598;
		}
		else if(dataYear == "2016")
		{
			medDeepCSV_DeepJet   = 0.2489;
		}
		else if(dataYear == "2017")
		{
			medDeepCSV_DeepJet   = 0.3040;
		}
		else if(dataYear == "2018")
		{
			medDeepCSV_DeepJet   = 0.2783;
		}

		int num_bad_btagSF = 0, num_bad_PUSF = 0, num_bad_topPt = 0, num_bad_scale = 0, num_bad_pdf = 0, num_bad_prefiring = 0;
		int badEventSF = 0;

		double nEvents = 0, nHTcut  = 0, nAK8JetCut = 0, nHeavyAK8Cut = 0, nBtagCut = 0, nDoubleTagged = 0;

		totEventsUncut = nentries;

		for (Int_t i=0;i<nentries;i++) 
		{  

			t1->GetEntry(i);


			//if ((nTau_VLooseVsJet_VLooseVsMuon_VVLooseVse > 0 ) || (nMuons_looseID_medIso >0) || (nElectrons_looseID_looseISO > 0)) continue;

		  ///// APPLY TRIGGER 
		  if ( (!passesPFHT) && (!passesPFJet) ) 
		  {
		  		continue; // skip events that don't pass at least one trigger
		  }
			// JET VETO MAPS AND HEM VETOES	
			bool fails_veto_map = false;
			bool fails_HEM      = false;
			for(int iii=0;iii<nfatjets;iii++) // a non-zero value is a bad thing from AK8_fails_veto_map 
			{

				if ((dataYear == "2018")  )   //  && (dataBlock.find("dataD") != std::string::npos) 
				{
					if( fatjet_isHEM[iii]  )	  
					{
						fails_HEM = true; // CHANGED FROM if (AK8_fails_veto_map[iii]) fails_veto_map = true; 
					}
				}
				if( AK8_fails_veto_map[iii])
				{
					fails_veto_map = true;
				}
			}

			if((fails_veto_map) || (fails_HEM)) continue;

			double eventScaleFactor = 1.0;
			double bTag_eventWeight_M = 1.0;

			if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos)  )
			{		

				//std::cout << "ET cut is "  << ET_cut <<  ", HT cut is " << HT_cut<< ", nAK8 cut is " <<nAK8_cut << ", nHeavyAK8 cut is " <<nHeavyAK8_cut << std::endl;	

				////// check MC systematics and make sure they aren't bad
				if ((PU_eventWeight != PU_eventWeight) || (std::isinf(PU_eventWeight))|| (std::isnan(PU_eventWeight)) || (abs(PU_eventWeight) > 100) || (PU_eventWeight < 0.)   )
				{
					PU_eventWeight = 1.0;
					num_bad_PUSF++;
				}
				
				if ((pdf_weight != pdf_weight) || (std::isinf(pdf_weight)) || (std::isnan(pdf_weight)) || (abs(pdf_weight) > 100) || (pdf_weight < 0.)  )
				{
					pdf_weight = 1.0;
					num_bad_pdf++;
				}
	 
				eventScaleFactor = PU_eventWeight;   /// these are all MC-only systematics, the b-tagging, fact, and renorm event weights will be applied after selection

				// set the b-tagging event weight based on the systematic
				// only valid for MC
				bTag_eventWeight_M = bTag_eventWeight_M_nom;

				if((systematic.find("bTag") != std::string::npos)) // if this is a btagging uncert, change the weight to be the appropriate variation
				{ 
					if     ((systematic == "bTagSF_med") && (*systematic_suffix == "up"))    bTag_eventWeight_M = bTag_eventWeight_M_up;
					else if((systematic == "bTagSF_med") && (*systematic_suffix == "down"))  bTag_eventWeight_M = bTag_eventWeight_M_down;
				}
				////// check MC systematics
				if ((bTag_eventWeight_M != bTag_eventWeight_M) || (std::isinf(bTag_eventWeight_M)) || (std::isnan(bTag_eventWeight_M)) || (abs(bTag_eventWeight_M) > 100) || (bTag_eventWeight_M < 0.)  )
				{
					bTag_eventWeight_M = 1.0;
					num_bad_btagSF++;
				}	
			} 

			////// check data systematics
			if ((prefiringWeight != prefiringWeight) || (std::isinf(prefiringWeight)) || (abs(prefiringWeight) > 100) || (prefiringWeight < 0.001)   )
			{
				prefiringWeight = 1.0;
				num_bad_prefiring++;
			}

			eventScaleFactor *= prefiringWeight;   // these are the non-MC-only systematics

			if ((eventScaleFactor != eventScaleFactor) || (std::isinf(eventScaleFactor)) ||  (std::isnan(eventScaleFactor)) || (abs(eventScaleFactor) > 100) || (abs(eventScaleFactor) < 0.001)  )
			{
				//std::cout << "ERROR: failed event scale factor on " << systematic << "_" << *systematic_suffix << std::endl;
				badEventSF++;
				continue;
			}

			nEvents+=eventScaleFactor;

			if(runOptimal)h_totHT->Fill(totHT,eventScaleFactor);


			/////// APPLY CUSTOM HT CUT
			if ( (totHT < HT_cut)    ) continue;
			

			nHTcut+=eventScaleFactor;


			if(runOptimal)h_nfatjets->Fill(nfatjets,eventScaleFactor);

			///////// APPLY CUSTOM nAK8 CUT
			if( (nfatjets < nAK8_cut) ) continue;


			nAK8JetCut+=eventScaleFactor;

			///////// APPLY CUSTOM nHeavyAK8 CUT

			if(runOptimal)
			{
				h_nfatjets_pre->Fill(nfatjet_pre,eventScaleFactor);
				h_dijet_mass->Fill(dijetMassOne,eventScaleFactor);
				h_dijet_mass->Fill(dijetMassTwo,eventScaleFactor);
			}

			if ((nfatjet_pre < nHeavyAK8_cut) && ( (dijetMassOne < 1000. ) || ( dijetMassTwo < 1000.)  )) continue;

			nHeavyAK8Cut+=eventScaleFactor;

			double eventWeightToUse = eventScaleFactor; 
		
			if (eventWeightToUse< 0.001) continue;

			eventnum++;

			h_MSJ_mass_vs_MdSJ_prebTag->Fill(diSuperJet_mass, (superJet_mass[0]+superJet_mass[1])/2.0   ,eventWeightToUse);

			int nMedBTags = 0;
			for(int iii = 0;iii< nAK4; iii++)
			{
				if ((AK4_pt[iii] > 70)  && (AK4_DeepJet_disc[iii] > medDeepCSV_DeepJet)) nMedBTags++;

				if(runOptimal)
				{
					h_AK4_eta->Fill(AK4_eta[iii]  ,eventWeightToUse);
					h_AK4_phi->Fill(AK4_phi[iii]  ,eventWeightToUse);
					if(AK4_pt[iii] > 75.) h_nAK4_pt75->Fill(AK4_pt[iii]  ,eventWeightToUse);
					h_AK4_jet_mass->Fill(AK4_mass[iii]  ,eventWeightToUse);
				}
			}

			// fill pre-selection "optimal" study hists

			if(runOptimal)
			{
				h_nAK4->Fill(nAK4, eventWeightToUse);

				for(int iii=0;iii < nfatjets; iii++)
				{
					h_AK8_jet_mass->Fill(jet_mass[iii]  ,eventWeightToUse);
					h_AK8_jet_pt->Fill(jet_pt[iii]  ,eventWeightToUse);
					h_AK8_eta->Fill(jet_eta[iii]  ,eventWeightToUse);
					h_AK8_phi->Fill(jet_phi[iii]  ,eventWeightToUse);
				}

				h_SJ_mass->Fill(superJet_mass[0]  ,eventWeightToUse);
				h_SJ_mass->Fill(superJet_mass[1]  ,eventWeightToUse);
				h_disuperjet_mass->Fill(diSuperJet_mass  ,eventWeightToUse);
				h_nMedBTags->Fill(nMedBTags  ,eventWeightToUse);
			}

			if(verbose)std::cout << "Systematic is " << systematic<<  " + " << *systematic_suffix << ", the used  b-tagging event weight is " << bTag_eventWeight_M << std::endl;
			if(verbose)std::cout << "Where up / nom / down b-tagging weights are: " << bTag_eventWeight_M_up << " / " << bTag_eventWeight_M_nom  << " / " << bTag_eventWeight_M_down << std::endl;


			///////////////////////////////
			////////// 1b region //////////
			///////////////////////////////

			if( nMedBTags > 0 ) 
			{
				eventWeightToUse*= bTag_eventWeight_M;
				nBtagCut +=eventWeightToUse;

				if(verbose)std::cout << "In b-tag clause ----- Systematic is " << systematic<<  " + " << *systematic_suffix << ", full event weight is " << eventWeightToUse << std::endl;


				if(runOptimal)
				{
					h_nCA4_300_1b->Fill(SJ_nAK4_300[0], eventWeightToUse);
					h_nCA4_300_1b->Fill(SJ_nAK4_300[1], eventWeightToUse);
				}

				h_MSJ_mass_vs_MdSJ_postbTag->Fill(diSuperJet_mass, (superJet_mass[0]+superJet_mass[1])/2.0   ,eventWeightToUse);

				if((SJ_nAK4_300[0]>=2) && (SJ_nAK4_300[1]>=2)) 
				{
					nDoubleTagged+=eventWeightToUse;
					h_MSJ_mass_vs_MdSJ_postSJTag->Fill(diSuperJet_mass, (superJet_mass[0]+superJet_mass[1])/2.0   ,eventWeightToUse);

 
					if(runOptimal) // if studying the optimal WP, fill a bunch of hists
					{

						for(int iii=0;iii < nfatjets; iii++)
						{
							h_AK8_jet_mass_SR->Fill(jet_mass[iii] ,eventWeightToUse);
							h_AK8_jet_pt_SR->Fill(jet_pt[iii], eventWeightToUse);
							h_JEC_uncert_AK8_SR->Fill(JEC_uncert_AK8[iii]);
							h_AK8_JER_SR->Fill(AK8_JER[iii]);
							h_AK8_eta_SR->Fill(jet_eta[iii]  ,eventWeightToUse);
							h_AK8_phi_SR->Fill(jet_phi[iii]  ,eventWeightToUse);
						}

						for(int iii = 0;iii< nAK4; iii++)
						{
							h_JEC_uncert_AK4_SR->Fill(JEC_uncert_AK4[iii]);
							h_AK4_jet_mass_SR->Fill(AK4_mass[iii], eventWeightToUse);
							if(AK4_pt[iii] > 75.) h_nAK4_pt75_SR->Fill(AK4_pt[iii], eventWeightToUse);

							h_AK4_eta_SR->Fill(AK4_eta[iii]  ,eventWeightToUse);
							h_AK4_phi_SR->Fill(AK4_phi[iii]  ,eventWeightToUse);
						}
						
						h_totHT_SR->Fill(totHT, eventWeightToUse);
						h_SJ_mass_SR->Fill(superJet_mass[0], eventWeightToUse);
						h_SJ_mass_SR->Fill(superJet_mass[1], eventWeightToUse);
						h_disuperjet_mass_SR->Fill(diSuperJet_mass, eventWeightToUse);
						h_MSJ_mass_vs_MdSJ_SR->Fill(diSuperJet_mass, (superJet_mass[0]+superJet_mass[1])/2.0, eventWeightToUse );

						h_pdf_EventWeight_SR->Fill(pdf_weight);
						h_scale_EventWeight_SR->Fill(scale_weight);
						h_PU_eventWeight_SR->Fill(PU_eventWeight);
						h_bTag_eventWeight_M_SR->Fill(bTag_eventWeight_M);
						h_L1PrefiringWeight_SR->Fill(prefiringWeight);
						h_Full_Event_Weight_SR->Fill(eventWeightToUse);

					}

				}
			}

			///////////////////////////////
			////////// 0b region //////////
			///////////////////////////////

			else 
			{

				if(runOptimal)
				{
					h_nCA4_300_0b->Fill(SJ_nAK4_300[0], eventWeightToUse);
					h_nCA4_300_0b->Fill(SJ_nAK4_300[1], eventWeightToUse);
				}

				if(runOptimal) // if studying the optimal WP, fill a bunch of hists
				{
					if((SJ_nAK4_300[0]>=2) && (SJ_nAK4_300[1]>=2)) 
					{

						for(int iii=0;iii < nfatjets; iii++)
						{
							h_AK8_jet_mass_CR->Fill(jet_mass[iii], eventWeightToUse);
							h_AK8_jet_pt_CR->Fill(jet_pt[iii], eventWeightToUse);
							h_JEC_uncert_AK8_CR->Fill(JEC_uncert_AK8[iii]);
							h_AK8_JER_CR->Fill(AK8_JER[iii]);
							h_AK8_eta_CR->Fill(jet_eta[iii]  ,eventWeightToUse);
							h_AK8_phi_CR->Fill(jet_phi[iii]  ,eventWeightToUse);
						}

						for(int iii = 0;iii< nAK4; iii++)
						{
							h_JEC_uncert_AK4_CR->Fill(JEC_uncert_AK4[iii]);
							h_AK4_jet_mass_CR->Fill(AK4_mass[iii], eventWeightToUse);
							if(AK4_pt[iii] > 75.) h_nAK4_pt75_CR->Fill(AK4_pt[iii], eventWeightToUse);
							h_AK4_eta_CR->Fill(AK4_eta[iii]  ,eventWeightToUse);
							h_AK4_phi_CR->Fill(AK4_phi[iii]  ,eventWeightToUse);
						}
						
						h_totHT_CR->Fill(totHT, eventWeightToUse);
						h_SJ_mass_CR->Fill(superJet_mass[0], eventWeightToUse);
						h_SJ_mass_CR->Fill(superJet_mass[1], eventWeightToUse);
						h_disuperjet_mass_CR->Fill(diSuperJet_mass, eventWeightToUse);
						h_MSJ_mass_vs_MdSJ_CR->Fill(diSuperJet_mass, (superJet_mass[0]+superJet_mass[1])/2.0, eventWeightToUse );

						h_pdf_EventWeight_CR->Fill(pdf_weight);
						h_scale_EventWeight_CR->Fill(scale_weight);
						h_PU_eventWeight_CR->Fill(PU_eventWeight);
						h_bTag_eventWeight_M_CR->Fill(bTag_eventWeight_M);
						h_L1PrefiringWeight_CR->Fill(prefiringWeight);
						h_Full_Event_Weight_CR->Fill(eventWeightToUse);

					}
				}
			}
		}

		if(verbose)std::cout << "For systematic " << systematic<<  " + " << *systematic_suffix << ", the integrated total number of events in h_MSJ_mass_vs_MdSJ_postbTag is  " << h_MSJ_mass_vs_MdSJ_postbTag->Integral() << std::endl;


		outFile->Write();
		if(verbose)
		{
			std::cout << std::endl;
			std::cout << std::endl;
			std::cout << std::endl;
			std::cout << std::endl;
			std::cout << "Finishing systematic " << systematic << " "<< *systematic_suffix << std::endl;
			std::cout << "Total Events: " << totEventsUncut << " in " << inFileName << " for " << systematic << " "<< *systematic_suffix << std::endl;
			std::cout << "In " << inFileName << " there were " << num_bad_btagSF<< "/" << num_bad_PUSF<< "/"<< num_bad_topPt<< "/"<< num_bad_scale<< "/"<<num_bad_pdf << "/" <<num_bad_prefiring << " bad btag/PU/topPt/scale/pdf/prefiring event weights" << std::endl; 
			std::cout << "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------" << std::endl;
			std::cout << "For  Sample = " << dataBlock  <<  ", year = " << dataYear << ", systematic = " << systematic << ", and WP = " << WP  << std::endl;
			std::cout << "SR Event Breakdown " << " total/HT/nAK8 jet/heavy AK8 +dijet/1+ b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nBtagCut << "/" << nDoubleTagged << std::endl;
			std::cout << "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------" << std::endl;
			std::cout << std::endl;
			std::cout << std::endl;
			std::cout << std::endl;
			std::cout << std::endl;
		}

		delete h_MSJ_mass_vs_MdSJ_prebTag, h_MSJ_mass_vs_MdSJ_postbTag, h_MSJ_mass_vs_MdSJ_postSJTag;
	}

   outFile->Close();
   std::cout << "--------- Finished file " << inFileName << std::endl;
   delete f;
   delete outFile;
   return true;
	
}
std::string convertDouble(double value) 
{
    std::ostringstream oss;
    oss << std::fixed << std::setprecision(2) << value; 
    std::string str = oss.str();
    std::replace(str.begin(), str.end(), '.', 'p');
    return str;
}


void processSelectionStudy()
{  

   bool debug 				= false;
   bool _verbose     	= false;
   bool runSignal    	= false;
   bool runBR	  			= false;
   bool runAll	 			= false;
   bool runSelection 	= false;
   bool runData  			= false;
   bool runOptimal      = true;
   int nFailedFiles = 0;
   std::string failedFiles = "";

   std::string eos_path	 =  "root://cmseos.fnal.gov//store/user/tjian/skimmedFiles/";


   std::vector<std::string> dataYears = {"2015","2016","2017","2018"};

   std::vector<std::string> systematics = { "nom", "bTagSF_med",   "JEC" }; //"PUSF",

   std::vector<std::string> JEC2_ucerts 		= {"JEC"};
   std::vector<std::string> sig_JEC1_ucerts  = {"JEC"}; // the types of uncertainties stored in the "JEC1" file for signal
   std::vector<std::string> sig_nom_ucerts 	=  {"nom"}; // the types of JEC uncertainties stored in the "nom" file for signal , , "JER"


   std::vector<std::string> AK8_ET_cuts 		= {"200","300","400"};
   std::vector<std::string> jet_HT_cuts 		= {"1600","1800","2000","2200"};
   std::vector<std::string> nAK8_cuts   		= {"2","3","4"};
   std::vector<std::string> nHeavyAK8_cuts   = {"1","2","3"};

	//HT AK4 jet ET:  200, 300, 400    # 150, 250, 350, 100,
	//jet HT: 1600, 1800, 2000, 2200
	//nAK4: 2, 3, 4
	//nHeavyAK8, 1,2,3

   std::vector<std::string> WPs = {}; // ,0.92,0.95,0.97,0.98,0.99

   for(auto AK8_ET_cut: AK8_ET_cuts )
   {
   	for(auto jet_HT_cut: jet_HT_cuts)
   	{
   		for(auto nAK8_cut: nAK8_cuts)
   		{
   			for(auto nHeavyAK8_cut: nHeavyAK8_cuts)
   			{
   				WPs.push_back(AK8_ET_cut + "_" + jet_HT_cut + "_"+ nAK8_cut + "_" + nHeavyAK8_cut);
   			}
   		}
   	}

   }



   if(runOptimal)
   {
   	WPs = {"400_2200_3_3"};
   }

   if(debug)
   {
   	dataYears = {"2015","2017"};
   	systematics = { "bTagSF_med"};  // , "JER", "JEC", "PUSF", 
   	WPs = {"200_1600_2_1","300_1800_3_2","400_2200_4_2"};

   }



   // delete root files in the /Users/ethan/Documents/rootFiles/processedRootFiles folder
   std::vector<std::string> signalFilePaths;
   std::vector<std::string> decays = {"WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"};
   std::vector<std::string> mass_points = {"Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1", "Suu5_chi1p5", "Suu5_chi2", "Suu6_chi1", "Suu6_chi2", "Suu6_chi2p5",
    "Suu7_chi1","Suu7_chi2","Suu7_chi3","Suu8_chi1", "Suu8_chi2","Suu8_chi3"};

   for(auto decay = decays.begin(); decay!= decays.end();decay++)
   {
		for(auto mass_point = mass_points.begin();mass_point!= mass_points.end();mass_point++)
		{
			signalFilePaths.push_back((*mass_point+ "_"+ *decay + "_").c_str());
		}
   }


   for(auto WP = WPs.begin(); WP < WPs.end(); WP++)
   {

   	std::cout << "------------- Running WP " << *WP << " -----------------" << std::endl;



	   std::string ET_cut;   // ----> goes to the input tree name and output folder name
	   std::string HT_cut;
	   std::string nAK8_cut;
	   std::string nHeavyAK8_cut;

		std::stringstream ss(*WP);
		std::getline(ss, ET_cut, '_');
		std::getline(ss, HT_cut, '_');              
		std::getline(ss, nAK8_cut, '_');            
		std::getline(ss, nHeavyAK8_cut, '_');  


   	// create output folder 
   	std::string output_dir = "ET" + ET_cut + "_HT" + HT_cut + "_nAK8" + nAK8_cut + "_nHAK8"+ nHeavyAK8_cut + "/";

   	if(runOptimal)output_dir = "optimal/";

   	if(debug) output_dir = "test/";

		if (mkdir(output_dir.c_str(), 0755) == 0 || errno == EEXIST) 
		{
			std::cout << "Directory exists or created.\n";
		} 


	   for(auto dataYear = dataYears.begin(); dataYear < dataYears.end();dataYear++ )
	   {
			std::cout << "----------- Looking at year " << *dataYear << " ------------" << std::endl;


			std::vector<std::string> dataBlocks; 

			if ((runAll) || (runOptimal))
			{
				if(*dataYear == "2015")
				{
					//dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_"}; // dataB-ver1 not present
					dataBlocks = {"JetHT_","QCD_Pt_300to470_","QCD_Pt_470to600_","QCD_Pt_600to800_","QCD_Pt_800to1000_", "QCD_Pt_1000to1400_","QCD_Pt_1400to1800_","QCD_Pt_1800to2400_","QCD_Pt_2400to3200_","QCD_Pt_3200toInf_"}; // dataB-ver1 not present
				}
				else if(*dataYear == "2016")
				{
					//dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_"}; 
					dataBlocks = {"JetHT_","QCD_Pt_300to470_","QCD_Pt_470to600_","QCD_Pt_600to800_","QCD_Pt_800to1000_", "QCD_Pt_1000to1400_","QCD_Pt_1400to1800_","QCD_Pt_1800to2400_","QCD_Pt_2400to3200_","QCD_Pt_3200toInf_"}; // dataB-ver1 not present
				}
				else if(*dataYear == "2017")
				{
					//dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_"}; 
					dataBlocks = {"JetHT_","QCD_Pt_300to470_","QCD_Pt_470to600_","QCD_Pt_600to800_","QCD_Pt_800to1000_", "QCD_Pt_1000to1400_","QCD_Pt_1400to1800_","QCD_Pt_1800to2400_","QCD_Pt_2400to3200_","QCD_Pt_3200toInf_"}; // dataB-ver1 not present
				}
				else if(*dataYear == "2018")
				{
					//dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_"}; 
					dataBlocks = {"JetHT_","QCD_Pt_300to470_","QCD_Pt_470to600_","QCD_Pt_600to800_","QCD_Pt_800to1000_", "QCD_Pt_1000to1400_","QCD_Pt_1400to1800_","QCD_Pt_1800to2400_","QCD_Pt_2400to3200_","QCD_Pt_3200toInf_"}; // dataB-ver1 not present
				}   
				dataBlocks.insert(dataBlocks.end(), signalFilePaths.begin(), signalFilePaths.end());
			}
			else if (runSignal)
			{
				dataBlocks = signalFilePaths;
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
			else if(runBR)
			{  
			 // dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				//"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"};
				dataBlocks = { "QCD_Pt_300to470_","QCD_Pt_470to600_","QCD_Pt_600to800_","QCD_Pt_800to1000_", "QCD_Pt_1000to1400_","QCD_Pt_1400to1800_","QCD_Pt_1800to2400_","QCD_Pt_2400to3200_","QCD_Pt_3200toInf_"}; // dataB-ver1 not present

			}
			else if(runSelection)
			{
				dataBlocks = {  
									"Suu6_chi1p5_WBWB_", 
									"Suu6_chi1p5_HTHT_", 
									"Suu6_chi1p5_ZTZT_", 
									"Suu6_chi1p5_WBZT_", 
									"Suu6_chi1p5_WBHT_", 
									"Suu6_chi1p5_HTZT_",

									"Suu7_chi1p5_WBWB_", 
									"Suu7_chi1p5_HTHT_", 
									"Suu7_chi1p5_ZTZT_", 
									"Suu7_chi1p5_WBZT_", 
									"Suu7_chi1p5_WBHT_", 
									"Suu7_chi1p5_HTZT_",

									"Suu8_chi1p5_WBWB_", 
									"Suu8_chi1p5_HTHT_", 
									"Suu8_chi1p5_ZTZT_", 
									"Suu8_chi1p5_WBZT_", 
									"Suu8_chi1p5_WBHT_", 
									"Suu8_chi1p5_HTZT_",

									"Suu7_chi2p5_WBWB_", 
									"Suu7_chi2p5_HTHT_", 
									"Suu7_chi2p5_ZTZT_", 
									"Suu7_chi2p5_WBZT_", 
									"Suu7_chi2p5_WBHT_", 
									"Suu7_chi2p5_HTZT_",

									"Suu8_chi2p5_WBWB_", 
									"Suu8_chi2p5_HTHT_", 
									"Suu8_chi2p5_ZTZT_", 
									"Suu8_chi2p5_WBZT_", 
									"Suu8_chi2p5_WBHT_", 
									"Suu8_chi2p5_HTZT_",
								} ; 

				//dataBlocks = {"Suu6_chi2p5", "Suu7_chi1","Suu7_chi1p5","Suu7_chi2", "Suu7_chi2p5", "Suu7_chi3","Suu8_chi1", "Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"} ; 
			}
			else
			{
				std::cout << "No/incorrect sample options selected" << std::endl;
				return;
			}
			





			if(debug) dataBlocks = {"QCD_Pt_300to470_","QCD_Pt_470to600_","QCD_Pt_600to800_","QCD_Pt_800to1000_", "QCD_Pt_1000to1400_","QCD_Pt_1400to1800_","QCD_Pt_1800to2400_","QCD_Pt_2400to3200_","QCD_Pt_3200toInf_"};
			for(auto dataBlock = dataBlocks.begin();dataBlock < dataBlocks.end();dataBlock++)
			{
				

				for(auto systematic = systematics.begin();systematic<systematics.end();systematic++)
				{

					std::cout << "------------ Looking at systematic: " << *systematic << " --------------" << std::endl;

					if (  (dataBlock->find("data") != std::string::npos)  && (*systematic != "nom") ) continue;



					std::string year = *dataYear;
					std::string systematic_str;  

					//if ((*systematic == "nom" )|| (*systematic == "bTagSF_med") || (*systematic == "bTagSF")|| (*systematic == "PUSF" ) || (*systematic == "pdf") || (*systematic == "scale") ) systematic_str = "nom";
					//if ( std::find(JEC2_ucerts.begin(), JEC2_ucerts.end(), *systematic) != JEC2_ucerts.end() ) systematic_str = "JEC2";
					//else if ( systematic->find("JER") != std::string::npos ) systematic_str = "JER";

					if( (*dataBlock).find("JetHT")!= std::string::npos )systematic_str = "nom";  // all uncerts are here
					else { systematic_str = "JEC";}




					// find the correct systematic_str for signal
					if(  (*dataBlock).find("Suu")!= std::string::npos  )
					{
						if ( std::find(sig_JEC1_ucerts.begin(), sig_JEC1_ucerts.end(), *systematic) != sig_JEC1_ucerts.end() ) systematic_str = "JEC1";
						else if ( std::find(sig_nom_ucerts.begin(), sig_nom_ucerts.end(), *systematic) != sig_nom_ucerts.end() ) systematic_str = "nom";
						else { systematic_str = "nom"; }
					}


					if(debug) std::cout << "@@@@@@@@@@@@@ WARNING: YOU ARE IN DEBUG MODE. NOT ALL FILES WILL BE RUN. @@@@@@@@@@@@@@" << std::endl;
					std::string inFileName = (eos_path + *dataBlock+  year +  "_JEC_SKIMMED.root").c_str();
					
					if( (*dataBlock).find("JetHT")!= std::string::npos ) inFileName = (eos_path + *dataBlock+  year +  "_nom_SKIMMED.root").c_str();

					// if this is JEC and the uncertainty isn't in the JEC1 list, it must be in the nom list and should use the nom naming scheme
					if ( inFileName.find("Suu") != std::string::npos)
					{
						if (!( std::find(sig_JEC1_ucerts.begin(), sig_JEC1_ucerts.end(), *systematic) != sig_JEC1_ucerts.end()     )  ) inFileName = (eos_path+ *dataBlock+  year + "_JEC_SKIMMED.root").c_str();
						else { inFileName = (eos_path+ *dataBlock+  year + "_JEC_SKIMMED.root").c_str(); }

					}
					std::string outFileName = (output_dir  + *dataBlock+ year + "_processed.root").c_str();

					if( failedFiles.find( (*dataBlock +"/" + year ).c_str()  ) != std::string::npos) continue; // skip files that failed for other uncertainties

					std::cout << "Reading File " << inFileName << " for year,sample,systematic " << year << "/" <<*dataBlock << "/" << *systematic<< std::endl;


					std::cout << "----------------------------------- Starting " << *dataBlock << "-----------------------------------"<< std::endl;

					if (!doThings(inFileName,outFileName, *dataYear,*systematic, *dataBlock, *WP, runOptimal, _verbose ))
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

						std::cout << "Finished with "<< inFileName << "." << std::endl;
						std::cout << std::endl;
						std::cout << std::endl;
						std::cout << std::endl;
						std::cout << std::endl;
						std::cout << "Wrote out to " << outFileName << "." << std::endl;
					}
				} // end dataBlock loop
			} // end systematic loop
	   } // end year loop
	} // end WP loop
} // end function


