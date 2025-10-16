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
bool doThings(std::string inFileName, std::string outFileName, std::string dataYear,std::string systematic, std::string dataBlock, std::string WP, bool verbose = false)
{

   TH1::SetDefaultSumw2();
   TH2::SetDefaultSumw2();
   int eventnum = 0;int nhadevents = 0; int nfatjets = 0, totEventsUncut=0,total_1b = 0, total_0b = 0;
   int SJ_nAK4_300[100];
   double AK4_DeepJet_disc[100], AK4_pt[100], AK4_mass[100], superJet_mass[100], jet_pt[100], jet_eta[100], jet_mass[100],AK4_eta[100];
   double diSuperJet_mass, dijetMassOne, dijetMassTwo, bTag_eventWeight_M_nom = 1, bTag_eventWeight_M_up = 1, bTag_eventWeight_M_down = 1, pdf_weight = 1.0,  scale_weight = 1.0, SJ1_BEST_scores, SJ2_BEST_scores, prefiringWeight;
   double  bTag_eventWeight_M = 1.0, PU_eventWeight = 1.0, totHT = 0;   
   int nfatjet_pre, nAK4, nSuperJets, nTau_VLooseVsJet_VLooseVsMuon_VVLooseVse, nMuons_looseID_medIso, nElectrons_looseID_looseISO;
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


   	////////////////////////////////////////////////////////////////////////////////////////////////////////
		t1->SetBranchAddress("passesPFHT", &passesPFHT); 
		t1->SetBranchAddress("passesPFJet", &passesPFJet); 

		t1->SetBranchAddress("nfatjets", &nfatjets);   
		t1->SetBranchAddress("nSuperJets", &nSuperJets);   
		t1->SetBranchAddress("diSuperJet_mass", &diSuperJet_mass);   
		t1->SetBranchAddress("nfatjet_pre", &nfatjet_pre);
		//t1->SetBranchAddress("jet_pt", jet_pt);   
		//t1->SetBranchAddress("jet_eta", jet_eta);   
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
			double bTag_eventWeight_M = 1, bTag_eventWeight_T = 1;

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

			int nMedBTags = 0;
			for(int iii = 0;iii< nAK4; iii++)
			{
				if ((AK4_pt[iii] > 70)  && (AK4_DeepJet_disc[iii] > medDeepCSV_DeepJet)) nMedBTags++;
			}

			nEvents+=eventScaleFactor;

			/////// APPLY CUSTOM HT CUT
			if ( (totHT < HT_cut)    ) continue;
			

			nHTcut+=eventScaleFactor;

			///////// APPLY CUSTOM nAK8 CUT
			if( (nfatjets < nAK8_cut) ) continue;


			nAK8JetCut+=eventScaleFactor;

			///////// APPLY CUSTOM nHeavyAK8 CUT
			if ((nfatjet_pre < nHeavyAK8_cut) && ( (dijetMassOne < 1000. ) || ( dijetMassTwo < 1000.)  )) continue;

			nHeavyAK8Cut+=eventScaleFactor;

			double eventWeightToUse = eventScaleFactor; 
		
			if (eventWeightToUse< 0.0001) continue;

			eventnum++;

			h_MSJ_mass_vs_MdSJ_prebTag->Fill(diSuperJet_mass, (superJet_mass[0]+superJet_mass[1])/2.0   ,eventWeightToUse);

			///////////////////////////////
			////////// 1b region //////////
			///////////////////////////////

			if( nMedBTags > 0 ) 
			{
				eventWeightToUse*= bTag_eventWeight_M;
				nBtagCut +=eventWeightToUse;

				h_MSJ_mass_vs_MdSJ_postbTag->Fill(diSuperJet_mass, (superJet_mass[0]+superJet_mass[1])/2.0   ,eventWeightToUse);

				if((SJ_nAK4_300[0]>=2) && (SJ_nAK4_300[1]>=2)) 
				{
					nDoubleTagged+=eventWeightToUse;
					h_MSJ_mass_vs_MdSJ_postSJTag->Fill(diSuperJet_mass, (superJet_mass[0]+superJet_mass[1])/2.0   ,eventWeightToUse);
				}
			}
		}

		outFile->Write();
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
   bool runBR	  			= true;
   bool runAll	 			= false;
   bool runSelection 	= false;
   bool runData  			= false;
   int nFailedFiles = 0;
   std::string failedFiles = "";

   std::string eos_path	 =  "root://cmseos.fnal.gov//store/user/tjian/skimmedFiles/";


   std::vector<std::string> dataYears = {"2015","2016","2017","2018"};

   dataYears = {"2018"};

   std::vector<std::string> systematics = { "nom", "bTagSF_med",   "JEC" }; //"PUSF",

   std::vector<std::string> JEC2_ucerts = {"JEC"};
   std::vector<std::string> sig_JEC1_ucerts = {"JEC"}; // the types of uncertainties stored in the "JEC1" file for signal
   std::vector<std::string> sig_nom_ucerts =  {"nom"}; // the types of JEC uncertainties stored in the "nom" file for signal , , "JER"


   std::vector<std::string> AK8_ET_cuts = {"200","300","400"};
   std::vector<std::string> jet_HT_cuts = {"1600","1800","2000","2200"};
   std::vector<std::string> nAK8_cuts   = {"2","3","4"};
   std::vector<std::string> nHeavyAK8_cuts   = {"2","3"};

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


   if(debug)
   {
   	dataYears = {"2017"};
   	systematics = { "nom", "JEC","bTagSF_med"};  // , "JER", "JEC", "PUSF", 
   	WPs = {"300_1600_2_1"};
   }



   // delete root files in the /Users/ethan/Documents/rootFiles/processedRootFiles folder
   std::vector<std::string> signalFilePaths;
   std::vector<std::string> decays = {"WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"};
   std::vector<std::string> mass_points = {"Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1",  "Suu5_chi2", "Suu6_chi1", "Suu6_chi2",
    "Suu7_chi1","Suu7_chi2","Suu8_chi1", "Suu8_chi2","Suu8_chi3"};

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
		if (mkdir(output_dir.c_str(), 0755) == 0 || errno == EEXIST) 
		{
			std::cout << "Directory exists or created.\n";
		} 


	   for(auto dataYear = dataYears.begin(); dataYear < dataYears.end();dataYear++ )
	   {
			std::cout << "----------- Looking at year " << *dataYear << " ------------" << std::endl;


			std::vector<std::string> dataBlocks; 

			if (runAll)
			{
				if(*dataYear == "2015")
				{
					//dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_"}; // dataB-ver1 not present
					dataBlocks = {"QCD_Pt_470to600_","QCD_Pt_600to800_","QCD_Pt_800to1000_", "QCD_Pt_1000to1400_","QCD_Pt_1400to1800_","QCD_Pt_1800to2400_"}; // dataB-ver1 not present
				}
				else if(*dataYear == "2016")
				{
					//dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_"}; 
					dataBlocks = {"QCD_Pt_470to600_","QCD_Pt_600to800_","QCD_Pt_800to1000_", "QCD_Pt_1000to1400_","QCD_Pt_1400to1800_","QCD_Pt_1800to2400_"}; // dataB-ver1 not present
				}
				else if(*dataYear == "2017")
				{
					//dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_"}; 
					dataBlocks = {"QCD_Pt_470to600_","QCD_Pt_600to800_","QCD_Pt_800to1000_", "QCD_Pt_1000to1400_","QCD_Pt_1400to1800_","QCD_Pt_1800to2400_"}; // dataB-ver1 not present
				}
				else if(*dataYear == "2018")
				{
					//dataBlocks = {"QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_"}; 
					dataBlocks = {"QCD_Pt_470to600_","QCD_Pt_600to800_","QCD_Pt_800to1000_", "QCD_Pt_1000to1400_","QCD_Pt_1400to1800_","QCD_Pt_1800to2400_"}; // dataB-ver1 not present
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
				dataBlocks = {"QCD_Pt_470to600_","QCD_Pt_600to800_","QCD_Pt_800to1000_", "QCD_Pt_1000to1400_","QCD_Pt_1400to1800_","QCD_Pt_1800to2400_"}; // dataB-ver1 not present

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
			if(debug)dataBlocks = {"QCDMC2000toInf_"};
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

					systematic_str = "JEC";  // all uncerts are here


					// find the correct systematic_str for signal
					if(  (*dataBlock).find("Suu")!= std::string::npos  )
					{
						if ( std::find(sig_JEC1_ucerts.begin(), sig_JEC1_ucerts.end(), *systematic) != sig_JEC1_ucerts.end() ) systematic_str = "JEC1";
						else if ( std::find(sig_nom_ucerts.begin(), sig_nom_ucerts.end(), *systematic) != sig_nom_ucerts.end() ) systematic_str = "nom";
						else { systematic_str = "nom"; }
					}


					if(debug) std::cout << "@@@@@@@@@@@@@ WARNING: YOU ARE IN DEBUG MODE. NOT ALL FILES WILL BE RUN. @@@@@@@@@@@@@@" << std::endl;
					std::string inFileName = (eos_path + *dataBlock+  year +  "_JEC_SKIMMED.root").c_str();
					
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

					if (!doThings(inFileName,outFileName, *dataYear,*systematic, *dataBlock, *WP, _verbose ))
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


