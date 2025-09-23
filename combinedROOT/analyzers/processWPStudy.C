#include <iostream>
#include <string>
#include "TLorentzVector.h"
#include <cstdlib>
// check out the SJ mass ratio, this might be really weird for TTbar and could be used to kill some of this


using namespace std;
bool doThings(std::string inFileName, std::string outFileName, double& nEvents, double& nHTcut, double& nAK8JetCut,double& nHeavyAK8Cut, double& nBtagCut, double& nDoubleTagged,double& nNoBjets, double& nDoubleTaggedCR, double& NNDoubleTag, double& nZeroBtagAntiTag, double & nOneBtagAntiTag, double & nNN_SR, double & nNN_CR, double & nNN_AT1b, double & nNN_AT0b,  std::string dataYear,std::string systematic, std::string dataBlock, double BEST_WP, double BEST_AT_WP, bool verbose = false)
{

   TH1::SetDefaultSumw2();
   TH2::SetDefaultSumw2();
   int eventnum = 0;int nhadevents = 0; int nfatjets = 0, totEventsUncut=0,total_1b = 0, total_0b = 0;
   int SJ_nAK4_300[100];
   double AK4_DeepJet_disc[100], AK4_pt[100], AK4_mass[100], superJet_mass[100], jet_pt[100], jet_eta[100], jet_mass[100],AK4_eta[100];
   double diSuperJet_mass, dijetMassOne, dijetMassTwo, bTag_eventWeight_M_nom = 1, bTag_eventWeight_M_up = 1, bTag_eventWeight_M_down = 1, pdf_weight = 1.0,  scale_weight = 1.0, SJ1_BEST_scores, SJ2_BEST_scores, prefiringWeight;
   double  bTag_eventWeight_M = 1.0, PU_eventWeight = 1.0, totHT = 0;   
   int eventNumber, ntrueInt, nfatjet_pre, nAK4, nSuperJets, nTau_VLooseVsJet_VLooseVsMuon_VVLooseVse, nMuons_looseID_medIso, nElectrons_looseID_looseISO;
   bool AK4_fails_veto_map[100], AK8_fails_veto_map[100],fatjet_isHEM[100],jet_isHEM[100] ;

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
			tree_name = "nom/skimmedTree_nom";
			systematic_use = "";
		}
		else{tree_name =  systematic+"_"+*systematic_suffix  + "/skimmedTree_" + systematic+"_"+*systematic_suffix  ; }

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
		TH2F *h_MSJ_mass_vs_MdSJ_NN_SR = new TH2F("h_MSJ_mass_vs_MdSJ_NN_SR","Superjet mass vs diSuperjet mass (Signal Region) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_NN_CR = new TH2F("h_MSJ_mass_vs_MdSJ_NN_CR","Superjet mass vs diSuperjet mass (Control Region) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_NN_AT1b = new TH2F("h_MSJ_mass_vs_MdSJ_NN_AT1b","Superjet mass vs diSuperjet mass (AT1b) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_NN_AT0b = new TH2F("h_MSJ_mass_vs_MdSJ_NN_AT0b","Superjet mass vs diSuperjet mass (AT0b) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		
		TH2F *h_MSJ_mass_vs_MdSJ_NN_ADT0b = new TH2F("h_MSJ_mass_vs_MdSJ_NN_ADT0b","Superjet mass vs diSuperjet mass (ADT0b) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_NN_ADT1b = new TH2F("h_MSJ_mass_vs_MdSJ_NN_ADT1b","Superjet mass vs diSuperjet mass (ADT1b) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		// full AT SJ2 2D hists
		TH2F *h_ATSJ_mass_vs_MdSJ_NN_AT1b = new TH2F("h_ATSJ_mass_vs_MdSJ_NN_AT1b","(Antitagged) Superjet mass vs diSuperjet mass (AT1b) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_ATSJ_mass_vs_MdSJ_NN_AT0b = new TH2F("h_ATSJ_mass_vs_MdSJ_NN_AT0b","(Antitagged) Superjet mass vs diSuperjet mass (AT0b) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

		// full AT SJ2 BEST scores
		TH1F* h_BEST_score_ATSJ_AT1b  = new TH1F("h_BEST_score_ATSJ_AT1b","Antitagged SJ BEST Score (1b region); NN Score; superjets",50,0,1.0);
		TH1F* h_BEST_score_ATSJ_AT0b  = new TH1F("h_BEST_score_ATSJ_AT0b","Antitagged SJ BEST Score (0b region); NN Score; superjets",50,0,1.0);

		// ADT BEST scores
		TH1F* h_BEST_score_ATSJ_ADT1b  = new TH1F("h_BEST_score_ATSJ_ADT1b","SJ BEST Score (ADT1b region); NN Score; superjets",50,0,1.0);
		TH1F* h_BEST_score_ATSJ_ADT0b  = new TH1F("h_BEST_score_ATSJ_ADT0b","SJ BEST Score (ADT0b region); NN Score; superjets",50,0,1.0);





   	////////////////////////////////////////////////////////////////////////////////////////////////////////
      t1->SetBranchAddress("eventNumber", &eventNumber); 
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
		t1->SetBranchAddress("AK4_fails_veto_map", AK4_fails_veto_map); 
		t1->SetBranchAddress("AK8_fails_veto_map", AK8_fails_veto_map); 
		t1->SetBranchAddress("SJ1_BEST_scores", &SJ1_BEST_scores); 
		t1->SetBranchAddress("SJ2_BEST_scores", &SJ2_BEST_scores); 
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
			t1->SetBranchAddress("bTag_eventWeight_M_nom", &bTag_eventWeight_M_nom);
			t1->SetBranchAddress("PU_eventWeight_nom", &PU_eventWeight);
			t1->SetBranchAddress("ntrueInt", &ntrueInt);

		}

		pdf_weight = 1.0; 
		scale_weight = 1.0; 


		if ( (inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos)) 
		{
			if (systematic.find("bTag") != std::string::npos)
			{ 
				if     ((systematic == "bTagSF_med") && (*systematic_suffix == "up"))   t1->SetBranchAddress("bTag_eventWeight_M_up", &bTag_eventWeight_M_up);
				else if((systematic == "bTagSF_med") && (*systematic_suffix == "down")) t1->SetBranchAddress("bTag_eventWeight_M_down", &bTag_eventWeight_M_down);
			}
			//////// pileup systematic 
			if     ((systematic == "PUSF") && (*systematic_suffix == "up"))   t1->SetBranchAddress("PU_eventWeight_up", &PU_eventWeight);
			else if((systematic == "PUSF") && (*systematic_suffix == "down")) t1->SetBranchAddress("PU_eventWeight_down", &PU_eventWeight);
			
			//////// pdf weight systematic 
			else if((systematic == "pdf") && (*systematic_suffix == "up"))   t1->SetBranchAddress("PDFWeightUp_BEST", &pdf_weight);
			else if((systematic == "pdf") && (*systematic_suffix == "down")) t1->SetBranchAddress("PDFWeightDown_BEST", &pdf_weight);

			/////// scale stuff 
			//////// renormalization and factorization scale systematics COMBINED
			else if((systematic == "scale") && (*systematic_suffix == "up"))   t1->SetBranchAddress("PDFWeights_envelope_scale_uncertainty_up", &scale_weight); // alternative:  PDFWeights_renormWeight_up
			else if((systematic == "scale") && (*systematic_suffix == "down")) t1->SetBranchAddress("PDFWeights_envelope_scale_uncertainty_down", &scale_weight); // alternative: PDFWeights_renormWeight_down
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

			t1->GetEntry(i);

			if ((dataBlock.find("Suu") != std::string::npos))
			{
				if( eventNumber%10 > 2) continue; // should only be for signal
			}

			if ((nTau_VLooseVsJet_VLooseVsMuon_VVLooseVse > 0 ) || (nMuons_looseID_medIso >0) || (nElectrons_looseID_looseISO > 0)) continue;

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
					if( fatjet_isHEM[iii]  )	  fails_HEM = true; // CHANGED FROM if (AK8_fails_veto_map[iii]) fails_veto_map = true; 
				}
				if( AK8_fails_veto_map[iii]) fails_veto_map = true;
			}

			if(fails_veto_map)
			{
				continue;
			}
			if(fails_HEM) 
			{
				continue; 
			}


			double eventScaleFactor = 1.0;
			double bTag_eventWeight_M = 1, bTag_eventWeight_T = 1;

			if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos)  )
			{				

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

			int nMedBTags = 0;
			for(int iii = 0;iii< nAK4; iii++)
			{
				if ((AK4_pt[iii] > 70)  && (AK4_DeepJet_disc[iii] > medDeepCSV_DeepJet)) nMedBTags++;
			}


			if(nMedBTags > 0) 
			{
				total_1b++;
			}
			else { total_0b++;}

			nEvents+=eventScaleFactor;

			if ( (totHT < 1600.)    ) continue;
			
			nHTcut+=eventScaleFactor;

			if( (nfatjets < 3) ) continue;

			nAK8JetCut+=eventScaleFactor;

			if ((nfatjet_pre < 2) && ( (dijetMassOne < 1000. ) || ( dijetMassTwo < 1000.)  )) continue;

			nHeavyAK8Cut+=eventScaleFactor;

			double eventWeightToUse = eventScaleFactor; 
		
			if (eventWeightToUse< 0.0001)  std::cout << "ERROR: bad eventWeightToUse for " <<dataBlock << "/" << systematic << "/" << dataYear << ", value = " << eventWeightToUse <<std::endl;

			eventnum++;


			///////////////////////////////
			////////// 0b region //////////
			///////////////////////////////

			double eventWeightToUse_preBtag = eventWeightToUse;

			if( nMedBTags < 1 ) 
			{

				


				////////////////////////////////////////////////////////////
				///////////////////// NN-based tagging /////////////////////
				////////////////////////////////////////////////////////////

				///////////////////
				////// NN CR //////
				///////////////////
				if( (SJ1_BEST_scores > BEST_WP) && (SJ2_BEST_scores > BEST_WP) ) 
				{
					 double eventWeightToUse_NN = eventScaleFactor;
					 if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos)) eventWeightToUse_NN*=bTag_eventWeight_M;
					 eventWeightToUse_NN *= pdf_weight*scale_weight; 
					nNN_CR +=eventWeightToUse_NN;
					h_MSJ_mass_vs_MdSJ_NN_CR->Fill(diSuperJet_mass,(superJet_mass[1]+superJet_mass[0])/2,eventWeightToUse_NN);
				}


				// SJ2 antitag w/ SJ1 tagged
				else if( (SJ2_BEST_scores < BEST_AT_WP) ) 
				{
					 double eventWeightToUse_NN = eventScaleFactor*=bTag_eventWeight_M;
					 if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos)) eventWeightToUse_NN*=bTag_eventWeight_M;
					 eventWeightToUse_NN *= pdf_weight*scale_weight;   
					nNN_AT0b +=eventScaleFactor;


					h_ATSJ_mass_vs_MdSJ_NN_AT0b->Fill(diSuperJet_mass,superJet_mass[0],eventWeightToUse_NN);
					h_BEST_score_ATSJ_AT0b->Fill(SJ1_BEST_scores, eventWeightToUse_NN);
					///////////////////
					///// NN AT0b /////
					///////////////////
					if (SJ1_BEST_scores > BEST_WP)
					{
						h_MSJ_mass_vs_MdSJ_NN_AT0b->Fill(diSuperJet_mass,superJet_mass[0],eventWeightToUse_NN);

					}
				} 
				// SJ1 antitag w/ SJ12tagged
				else if(  (SJ1_BEST_scores < BEST_AT_WP ) ) // want to be quite sure the second superjet is not tagged
				{
					double eventWeightToUse_NN = eventScaleFactor*=bTag_eventWeight_M;
					if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos)) eventWeightToUse_NN*=bTag_eventWeight_M;
					eventWeightToUse_NN *= pdf_weight*scale_weight;   //factWeight*renormWeight
					nNN_AT0b +=eventScaleFactor;
					
					h_ATSJ_mass_vs_MdSJ_NN_AT0b->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse_NN);
					h_BEST_score_ATSJ_AT0b->Fill(SJ2_BEST_scores, eventWeightToUse_NN);
					if (SJ2_BEST_scores > BEST_WP)
					{
						h_MSJ_mass_vs_MdSJ_NN_AT0b->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse_NN);
					}

				} 
				///////////////////
				///// NN ADT0b /////
				///////////////////
				else if(  (SJ1_BEST_scores < BEST_WP) && (SJ2_BEST_scores < BEST_WP) ) // want to be quite sure the second superjet is not tagged
				{
					double eventWeightToUse_NN = eventScaleFactor*=bTag_eventWeight_M;
					if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos)) eventWeightToUse_NN*=bTag_eventWeight_M;
					eventWeightToUse_NN *= pdf_weight*scale_weight;  // factWeight*renormWeight
					h_MSJ_mass_vs_MdSJ_NN_ADT0b->Fill(diSuperJet_mass, (superJet_mass[0] + superJet_mass[1])/2.0,eventWeightToUse_NN);
					h_BEST_score_ATSJ_ADT0b->Fill(SJ1_BEST_scores,eventWeightToUse_NN);
					h_BEST_score_ATSJ_ADT0b->Fill(SJ2_BEST_scores,eventWeightToUse_NN);

				} 


			}
			
			/////////////////////////////
			///////// 1b region /////////
			/////////////////////////////



			else if ( (nMedBTags > 0)  )
			{


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
						h_MSJ_mass_vs_MdSJ_NN_SR->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventWeightToUse_NN);
					}
				}

				///////////////////
				///// NN AT1b /////
				///////////////////

				// SJ2 antitag w/ SJ1 tagged
				else if(   (SJ2_BEST_scores < BEST_AT_WP )  ) // want to be quite sure the second superjet is not tagged
				{
					{
						double eventWeightToUse_NN = eventScaleFactor;
						if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventWeightToUse_NN*=bTag_eventWeight_M;
						eventWeightToUse_NN *= pdf_weight*scale_weight;   // factWeight*renormWeight
						nNN_AT1b +=eventScaleFactor;

						h_ATSJ_mass_vs_MdSJ_NN_AT1b->Fill(diSuperJet_mass,superJet_mass[0],eventWeightToUse_NN );
						h_BEST_score_ATSJ_AT1b->Fill(SJ1_BEST_scores, eventWeightToUse_NN);

						if (SJ1_BEST_scores > BEST_WP )
						{
							h_MSJ_mass_vs_MdSJ_NN_AT1b->Fill(diSuperJet_mass,superJet_mass[0],eventWeightToUse_NN );
						}
					}
				} 


				

				// SJ1 antitag w/ SJ2 tagged
				else if(   (SJ1_BEST_scores < BEST_AT_WP )   ) // want to be quite sure the second superjet is not tagged
				{
					{
						double eventWeightToUse_NN = eventScaleFactor;
						if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventWeightToUse_NN*=bTag_eventWeight_M;
						eventWeightToUse_NN *= pdf_weight*scale_weight;   // factWeight*renormWeight
						nNN_AT1b +=eventScaleFactor;

						h_ATSJ_mass_vs_MdSJ_NN_AT1b->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse_NN );
						h_BEST_score_ATSJ_AT1b->Fill(SJ2_BEST_scores, eventWeightToUse_NN);

						if (SJ2_BEST_scores > BEST_WP )
						{
							h_MSJ_mass_vs_MdSJ_NN_AT1b->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse_NN );
						}
						
					}
				}
				///////////////////
				///// NN ADT1b /////
				///////////////////
				else if(  (SJ1_BEST_scores < BEST_WP) && (SJ2_BEST_scores < BEST_WP) ) // want to be quite sure the second superjet is not tagged
				{
					double eventWeightToUse_NN = eventScaleFactor*=bTag_eventWeight_M;
					 if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos)) eventWeightToUse_NN*=bTag_eventWeight_M;
					 eventWeightToUse_NN *= pdf_weight*scale_weight;  // factWeight*renormWeight
					h_MSJ_mass_vs_MdSJ_NN_ADT1b->Fill(diSuperJet_mass, (superJet_mass[0] + superJet_mass[1])/2.0,eventWeightToUse_NN);
					h_BEST_score_ATSJ_ADT1b->Fill(SJ1_BEST_scores,eventWeightToUse_NN);
					h_BEST_score_ATSJ_ADT1b->Fill(SJ2_BEST_scores,eventWeightToUse_NN);
				}  

			}

		}

		outFile->Write();
		std::cout << "Finishing systematic " << systematic << " "<< *systematic_suffix << std::endl;
		std::cout << "Total Events: " << totEventsUncut << " in " << inFileName << " for " << systematic << " "<< *systematic_suffix << std::endl;
		std::cout << "In " << inFileName << " there were " << num_bad_btagSF<< "/" << num_bad_PUSF<< "/"<< num_bad_topPt<< "/"<< num_bad_scale<< "/"<<num_bad_pdf << "/" <<num_bad_prefiring << " bad btag/PU/topPt/scale/pdf/prefiring event weights" << std::endl; 
		std::cout << "There were " << badEventSF << " bad events." << std::endl;
		std::cout << "NN Signal  Region for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << ", "<<  dataYear  << " : total/HTcut/AK8jetCut/heavyAK8JetCut/nBtagCut/nSJEnergyCut: - " <<   nNN_SR   << std::endl;
		std::cout << dataBlock << "/" << dataYear << "/" << systematic+ "_" + *systematic_suffix << " : there was a total of " << total_1b << "/" << total_0b << " events in the 1b/0b region (all pre-selected)." << std::endl;

		delete h_MSJ_mass_vs_MdSJ_NN_SR, h_MSJ_mass_vs_MdSJ_NN_CR, h_MSJ_mass_vs_MdSJ_NN_AT1b,h_MSJ_mass_vs_MdSJ_NN_AT0b, h_MSJ_mass_vs_MdSJ_NN_ADT1b, h_MSJ_mass_vs_MdSJ_NN_ADT0b;
		delete h_ATSJ_mass_vs_MdSJ_NN_AT1b, h_ATSJ_mass_vs_MdSJ_NN_AT0b, h_BEST_score_ATSJ_AT1b, h_BEST_score_ATSJ_AT0b;

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


void processWPStudy()
{  

   bool debug 				= false;
   bool _verbose     	= false;
   bool runSignal    	= true;
   bool runBR	  			= false;
   bool runAll	 			= false;
   bool runSelection 	= false;
   bool runData  			= false;
   int nFailedFiles = 0;
   std::string failedFiles = "";

   std::string eos_path	 =  "root://cmseos.fnal.gov//store/user/ecannaer/skimmedFiles/";


   std::vector<std::string> dataYears = {"2015","2016","2017","2018"};

   if(runSelection) dataYears = {"2018"};
   std::vector<std::string> systematics = { "nom", "scale", "bTagSF_med",  "JER", "JEC", "PUSF", "pdf"}; 

   std::vector<std::string> JEC2_ucerts = {"JEC"};
   std::vector<std::string> sig_JEC1_ucerts = {"JEC"}; // the types of uncertainties stored in the "JEC1" file for signal
   std::vector<std::string> sig_nom_ucerts =  {"nom", "JER"}; // the types of JEC uncertainties stored in the "nom" file for signal


   std::vector<double> WPs = {0.25,0.30,0.35,0.40,0.45,0.5,0.55,0.60,0.65,0.70,0.80,0.90}; // ,0.92,0.95,0.97,0.98,0.99


 	WPs = {0.90};

   double BEST_AT_WP = 0.12;

   if(debug)
   {
   	dataYears = {"2017"};
   	systematics = { "nom"};  // , "JER", "JEC", "PUSF"
   	WPs = {0.40,0.50,0.60};
   }



   // delete root files in the /Users/ethan/Documents/rootFiles/processedRootFiles folder
   std::vector<std::string> signalFilePaths;
   std::vector<std::string> decays = {"WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"};
   std::vector<std::string> mass_points = {"Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1", "Suu5_chi1p5", "Suu5_chi2", "Suu6_chi1","Suu6_chi1p5", "Suu6_chi2",
   "Suu6_chi2p5", "Suu7_chi1","Suu7_chi1p5","Suu7_chi2", "Suu7_chi2p5", "Suu7_chi3","Suu8_chi1", "Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"};


 	mass_points = {"Suu7_chi2", "Suu7_chi2p5", "Suu7_chi3","Suu8_chi1", "Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"};

   for(auto decay = decays.begin(); decay!= decays.end();decay++)
   {
		for(auto mass_point = mass_points.begin();mass_point!= mass_points.end();mass_point++)
		{
			signalFilePaths.push_back((*mass_point+ "_"+ *decay + "_").c_str());
		}
   }


   for(auto WP = WPs.begin(); WP < WPs.end(); WP++)
   {
	   std::string WPDoubleStr = convertDouble(*WP); 
   	std::string outputFolder = "WP_study/WP" + WPDoubleStr + "/";

   	std::cout << "------------- Running WP " << WPDoubleStr << " -----------------" << std::endl;
	   for(auto dataYear = dataYears.begin(); dataYear < dataYears.end();dataYear++ )
	   {
			std::cout << "----------- Looking at year " << *dataYear << " ------------" << std::endl;

			std::cout << ("Deleting old " + *dataYear + " ROOT files in /uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combimedROOT/"+outputFolder +  " .").c_str() << std::endl;
			int delete_result = 1;

			// delete existing processed files 
			if((runBR)||(runAll) ) 
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
			if(runAll ) 
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

			if (runAll)
			{
				if(*dataYear == "2015")
				{
					dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_",  "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"}; // dataB-ver1 not present
				}
				else if(*dataYear == "2016")
				{
					dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_", "TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"};
				}
				else if(*dataYear == "2017")
				{
					dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"};
				}
				else if(*dataYear == "2018")
				{
					dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"};
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
			  dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_", "TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"};
			}
			else if(runSelection)
			{
				dataBlocks = {"Suu6_chi2p5", "Suu7_chi1","Suu7_chi1p5","Suu7_chi2", "Suu7_chi2p5", "Suu7_chi3","Suu8_chi1", "Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"} ; 
			}
			else
			{
				std::cout << "No/incorrect sample options selected" << std::endl;
				return;
			}
			
			for(auto systematic = systematics.begin();systematic<systematics.end();systematic++)
			{

				std::cout << "------------ Looking at systematic: " << *systematic << " --------------" << std::endl;

				for(auto dataBlock = dataBlocks.begin();dataBlock < dataBlocks.end();dataBlock++)
				{

					if (  (dataBlock->find("data") != std::string::npos)  && (*systematic != "nom") ) continue;


					double nEvents = 0, nHTcut  = 0, nAK8JetCut = 0, nHeavyAK8Cut = 0, nBtagCut = 0, nDoubleTagged = 0, nNoBjets = 0;
					double nDoubleTaggedCR = 0, NNDoubleTag = 0, nZeroBtagAntiTag = 0, nOneBtagAntiTag = 0;
					double nNN_SR = 0, nNN_CR = 0 , nNN_AT1b = 0,nNN_AT0b = 0;

					std::string year = *dataYear;
					std::string systematic_str;  

					if ((*systematic == "nom" )|| (*systematic == "bTagSF_med") || (*systematic == "bTagSF")|| (*systematic == "PUSF" ) || (*systematic == "pdf") || (*systematic == "scale") ) systematic_str = "nom";
					else if ( std::find(JEC2_ucerts.begin(), JEC2_ucerts.end(), *systematic) != JEC2_ucerts.end() ) systematic_str = "JEC2";
					else if ( systematic->find("JER") != std::string::npos ) systematic_str = "JER";




					// find the correct systematic_str for signal
					if(  (*dataBlock).find("Suu")!= std::string::npos  )
					{
						if ( std::find(sig_JEC1_ucerts.begin(), sig_JEC1_ucerts.end(), *systematic) != sig_JEC1_ucerts.end() ) systematic_str = "JEC1";
						else if ( std::find(sig_nom_ucerts.begin(), sig_nom_ucerts.end(), *systematic) != sig_nom_ucerts.end() ) systematic_str = "nom";
						else { systematic_str = "nom"; }
					}


					if(debug) std::cout << "@@@@@@@@@@@@@ WARNING: YOU ARE IN DEBUG MODE. NOT ALL FILES WILL BE RUN. @@@@@@@@@@@@@@" << std::endl;
					std::string inFileName = (eos_path + *dataBlock+  year +  "_"+ systematic_str+ "_SKIMMED.root").c_str();
					
					// if this is JEC and the uncertainty isn't in the JEC1 list, it must be in the nom list and should use the nom naming scheme
					if ( inFileName.find("Suu") != std::string::npos)
					{
						if (!( std::find(sig_JEC1_ucerts.begin(), sig_JEC1_ucerts.end(), *systematic) != sig_JEC1_ucerts.end()     )  ) inFileName = (eos_path+ *dataBlock+  year + "_SKIMMED.root").c_str();
						else { inFileName = (eos_path+ *dataBlock+  year + "_JEC_SKIMMED.root").c_str(); }

					}
					std::string outFileName = (outputFolder  + *dataBlock+ year + "_WP" + WPDoubleStr + "_processed.root").c_str();

					if( failedFiles.find( (*dataBlock +"/" + year ).c_str()  ) != std::string::npos) continue; // skip files that failed for other uncertainties

					std::cout << "Reading File " << inFileName << " for year,sample,systematic " << year << "/" <<*dataBlock << "/" << *systematic<< std::endl;

					if (!doThings(inFileName,outFileName,nEvents,nHTcut,nAK8JetCut,nHeavyAK8Cut,nBtagCut,nDoubleTagged,nNoBjets,nDoubleTaggedCR, NNDoubleTag,nZeroBtagAntiTag, nOneBtagAntiTag, nNN_SR, nNN_CR, nNN_AT1b, nNN_AT0b, *dataYear,*systematic, *dataBlock, *WP, BEST_AT_WP, _verbose ))
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
						std::cout << "Wrote out to " << outFileName << "." << std::endl;
					}
				} // end dataBlock loop
			} // end systematic loop
	   } // end year loop
	} // end WP loop
} // end function


