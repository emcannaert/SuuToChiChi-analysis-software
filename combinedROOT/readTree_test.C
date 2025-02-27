#include <iostream>
#include <string>
#include "TLorentzVector.h"
#include <cstdlib>
#include <fstream>  // For file handling

// helper function 
double return_BR_SF(const std::string& year, const std::string& sample) 
{
    double scale_factor = 1.0;


    // Define the scale factors map
    std::map<std::string, std::map<std::string, double>> scale_factors = {
        {"QCDMC1000to1500_", {{"2015", 1.578683216}, {"2016", 1.482632755}, {"2017", 3.126481451}, {"2018", 4.407417122}}},
        {"QCDMC1500to2000_", {{"2015", 0.2119142341}, {"2016", 0.195224041}, {"2017", 0.3197450474}, {"2018", 0.5425809983}}},
        {"QCDMC2000toInf_", {{"2015", 0.08568186031}, {"2016", 0.07572795371}, {"2017", 0.14306915}, {"2018", 0.2277769275}}},
        {"TTToHadronicMC_", {{"2015", 0.075592}, {"2016", 0.05808655696}, {"2017", 0.06651018525}, {"2018", 0.06588049107}}},
        {"TTToSemiLeptonicMC_", {{"2015", 0.05395328118}, {"2016", 0.05808655696}, {"2017", 0.04264829286}, {"2018", 0.04563489275}}},
        {"TTToLeptonicMC_", {{"2015", 0.0459517611}, {"2016", 0.03401684391}, {"2017", 0.03431532926}, {"2018", 0.03617828025}}},
        {"TTJetsMCHT800to1200_", {{"2015", 0.002884466085}, {"2016", 0.002526405224}, {"2017", 0.003001100916}, {"2018", 0.004897196802}}},
        {"TTJetsMCHT1200to2500_", {{"2015", 0.002722324842}, {"2016", 0.002255554525}, {"2017", 0.00267594799}, {"2018", 0.003918532089}}},
        {"TTJetsMCHT2500toInf_", {{"2015", 0.000056798633}, {"2016", 0.000050253843}, {"2017", 0.00005947217}, {"2018", 0.000084089656}}},
        {"ST_t-channel-top_inclMC_", {{"2015", 0.0409963154}, {"2016", 0.03607115071}, {"2017", 0.03494669125}, {"2018", 0.03859114659}}},
        {"ST_t-channel-antitop_inclMC_", {{"2015", 0.05673857623}, {"2016", 0.04102705994}, {"2017", 0.04238814865}, {"2018", 0.03606630944}}},
        {"ST_s-channel-hadronsMC_", {{"2015", 0.04668187234}, {"2016", 0.03564988679}, {"2017", 0.03985938616}, {"2018", 0.04102795437}}},
        {"ST_s-channel-leptonsMC_", {{"2015", 0.01323030083}, {"2016", 0.01149139097}, {"2017", 0.01117527734}, {"2018", 0.01155448784}}},
        {"ST_tW-antiTop_inclMC_", {{"2015", 0.2967888696}, {"2016", 0.2301666797}, {"2017", 0.2556495594}, {"2018", 0.2700032391}}},
        {"ST_tW-top_inclMC_", {{"2015", 0.2962796522}, {"2016", 0.2355829386}, {"2017", 0.2563403788}, {"2018", 0.2625270613}}},
        {"WJetsMC_LNu-HT800to1200_", {{"2015", 0.04172270958}, {"2016", 0.04230432205}, {"2017", 0.04374224695}, {"2018", 0.04394190568}}},
        {"WJetsMC_LNu-HT1200to2500_", {{"2015", 0.01068088067}, {"2016", 0.00932744847}, {"2017", 0.009709510545}, {"2018", 0.01070780024}}},
        {"WJetsMC_LNu-HT2500toInf_", {{"2015", 0.0001931363546}, {"2016", 0.0001895618832}, {"2017", 0.0002799036518}, {"2018", 0.0007547032677}}},
        {"WJetsMC_QQ-HT800toInf_", {{"2015", 0.072501767}, {"2016", 0.07139611301}, {"2017", 0.08100232455}, {"2018", 0.128194465}}},
        {"WW_MC", {{"2015", 0.09385207138}, {"2016", 0.08101652866}, {"2017", 0.2023058718}, {"2018", 0.2909648256}}},
        {"ZZ_MC", {{"2015", 0.1848461778}, {"2016", 0.1773009557}, {"2017", 0.1860928307}, {"2018", 0.2059943846}}}
    };

    // Find the sample in the map
    if (scale_factors.find(sample) != scale_factors.end()) 
    {
        const auto& year_map = scale_factors[sample];
        if (year_map.find(year) != year_map.end()) 
        {
            scale_factor = year_map.at(year);
        } 
        else 
        {
            throw std::invalid_argument("ERROR: Year not found: " + year);
        }
    } 
    else 
    {
        throw std::invalid_argument("ERROR: Sample name not found: " + sample);
    }

    return scale_factor;
}


double calculate_Suu_to_chi_chi_BR(double Suu_mass, double chi_mass, double y_uu = 2.0, double y_x = 2.0) {
    // Suu to up quark pair partial width
    double tau_SuuToUU = pow(y_uu, 2) * Suu_mass / (32 * M_PI);

    // Suu to VLQ pair partial width
    double chi_mass_ratio = chi_mass / Suu_mass;
    double tau_SuuToChiChi = (pow(y_x, 2) * Suu_mass * (1 - 2 * pow(chi_mass_ratio, 2)) *
                              sqrt(1 - 4 * pow(chi_mass_ratio, 2))) /
                             (32 * M_PI);

    return tau_SuuToChiChi / (tau_SuuToChiChi + tau_SuuToUU);
}


// helper function to get signal scale factor 
double return_signal_SF(const std::string &year, const std::string &mass_point, const std::string &decay, 
                        double y_uu = 2.0, double y_x = 2.0) {
    // Determine Suu_mass
    double Suu_mass = 4000;
    if (mass_point.find("Suu5") != std::string::npos) Suu_mass = 5000;
    else if (mass_point.find("Suu6") != std::string::npos) Suu_mass = 6000;
    else if (mass_point.find("Suu7") != std::string::npos) Suu_mass = 7000;
    else if (mass_point.find("Suu8") != std::string::npos) Suu_mass = 8000;

    // Determine chi_mass
    double chi_mass = 1000;
    if (mass_point.find("chi1p5") != std::string::npos) chi_mass = 1500;
    else if (mass_point.find("chi2") != std::string::npos) chi_mass = 2000;
    else if (mass_point.find("chi2p5") != std::string::npos) chi_mass = 2500;
    else if (mass_point.find("chi3") != std::string::npos) chi_mass = 3000;

    // Define Suu production cross-sections
    std::map<std::string, double> Suu_prod_xs = 
    {
        {"4000", 1000.0 * pow(1.0 * y_uu, 2) / pow(2.0, 2)},
        {"5000", 500.0 * pow(1.0 * y_uu, 2) / pow(2.0, 2)},
        {"6000", 200.0 * pow(1.0 * y_uu, 2) / pow(2.0, 2)},
        {"7000", 28.0 * pow(1.0 * y_uu, 2) / pow(2.0, 2)},
        {"8000", 3.5 * pow(1.0 * y_uu, 2) / pow(2.0, 2)}
    };

    // Collected data
    std::map<std::string, double> collected_data = 
    {
        {"2015", 19.52}, {"2016", 16.81}, {"2017", 41.48}, {"2018", 59.83}
    };

    // Branching ratios
    double WB_BR = 0.50, ZT_BR = 0.25, HT_BR = 0.25;
    double Z_had_BR = 0.6991, W_had_BR = 0.6741, H_had_BR = 0.58, t_had_BR = 0.6741;

    double frac_of_events_used = 0.3;
    int nEvents = 0;

    if (decay == "WBWB" || decay == "ZTZT" || decay == "HTHT") 
    {
        nEvents = (mass_point.find("Suu8") != std::string::npos || mass_point.find("Suu7") != std::string::npos || 
                   mass_point.find("Suu6") != std::string::npos) ? 30000 : 60000;
    } 
    else if (decay == "WBHT" || decay == "WBZT" || decay == "HTZT") 
    {
        nEvents = (mass_point.find("Suu8") != std::string::npos || mass_point.find("Suu7") != std::string::npos || 
                   mass_point.find("Suu6") != std::string::npos) ? 50000 : 100000;
    }

    if (year == "2015" || year == "2016") 
    {
        nEvents /= 2;  // Halve for 2016preAPV and 2016postAPV
    }

    double lumi_eff = nEvents * frac_of_events_used / 
                      (Suu_prod_xs[std::to_string((int)Suu_mass)] * 
                       calculate_Suu_to_chi_chi_BR(Suu_mass, chi_mass, y_uu, y_x));
    double lumi_year = collected_data[year];
    double SF_fullBR = lumi_year / lumi_eff;

    // Decay-specific hadronic branching ratios
    double WBWB_had_BR = (WB_BR * WB_BR) * (W_had_BR * W_had_BR);
    double HTHT_had_BR = (HT_BR * HT_BR) * (H_had_BR * t_had_BR) * (H_had_BR * t_had_BR);
    double ZTZT_had_BR = (ZT_BR * ZT_BR) * (Z_had_BR * t_had_BR) * (Z_had_BR * t_had_BR);
    double WBHT_had_BR = 2 * (WB_BR * HT_BR) * (W_had_BR) * (H_had_BR * t_had_BR);
    double WBZT_had_BR = 2 * (WB_BR * ZT_BR) * (W_had_BR) * (Z_had_BR * t_had_BR);
    double HTZT_had_BR = 2 * (HT_BR * ZT_BR) * (H_had_BR * t_had_BR) * (Z_had_BR * t_had_BR);

    if (decay == "WBWB") return SF_fullBR * WBWB_had_BR;
    else if (decay == "HTHT") return SF_fullBR * HTHT_had_BR;
    else if (decay == "ZTZT") return SF_fullBR * ZTZT_had_BR;
    else if (decay == "WBHT") return SF_fullBR * WBHT_had_BR;
    else if (decay == "WBZT") return SF_fullBR * WBZT_had_BR;
    else if (decay == "HTZT") return SF_fullBR * HTZT_had_BR;
    else {
        std::cerr << "ERROR: decay " << decay << " did not match any accepted decays (WBWB, HTHT, ZTZT, WBHT, WBZT, HTZT).\n";
        return -1;  // Indicate error
    }
}








// test script to loop over samples for just the nominal uncertainty without any extras

using namespace std;
bool doThings(std::string inFileName, std::string outFileName,double & total_QCD_SR,  double & total_TTbar_SR, double & total_WJets_SR, double & total_ST_SR,  double & total_data_SR,std::map<std::string, std::map<std::string, double>> & signal_mass_SR, double & total_QCD_CR, double & total_TTbar_CR, double & total_WJets_CR, double & total_ST_CR, double & total_data_CR, std::map<std::string, std::map<std::string, double>> & signal_mass_CR, double & total_QCD_AT1b, double & total_TTbar_AT1b, double & total_WJets_AT1b, double & total_ST_AT1b, double & total_data_AT1b, double & total_AK4_jets_QCD, double & btagged_AK4_jets_QCD, double & total_AK4_jets_TTbar, double & btagged_AK4_jets_TTbar, double & btagged_trueb_jets_QCD,double & total_trueb_jets_QCD,double & btagged_trueb_jets_TTbar,double & total_trueb_jets_TTbar,std::map<std::string, std::map<std::string, double>> &signal_mass_AT1b, double & total_QCD_AT0b, double & total_TTbar_AT0b, double & total_WJets_AT0b, double total_ST_AT0b, double & total_data_AT0b,  std::map<std::string, std::map<std::string, double>> & signal_mass_AT0b,   std::string dataYear,std::string systematic, std::string dataBlock, std::string runType, bool verbose = false)
{



    std::ofstream outFile_txt( ("../postprocess/txt_files/NN_scores/NN_scores_" + dataYear  + "_"+ dataBlock   + ".txt").c_str()   );

    if (outFile_txt.is_open()) 
    { 
        std::cout << "Output text succesffully opened." << std::endl;
        outFile_txt << "SJ1_signal_score" << "     " << "SJ1_TTbar_score" << "     " << "SJ1_QCD_score" << "     " << "SJ2_signal_score" << "     " << "SJ2_TTbar_score" << "     " << "SJ2_QCD_score" <<  "\n";
    } 
    else 
    {
        std::cerr << "Error: Could not create the output text file!\n";
    }



   TH1::SetDefaultSumw2();
   TH2::SetDefaultSumw2();
   int eventnum = 0;int nhadevents = 0; int nfatjets = 0;int raw_nfatjets;int tot_nAK4_50,tot_nAK4_70;int SJ_nAK4_50[100],SJ_nAK4_70[100];
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
   int eventNumber;

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

   double AK4_m1[2], AK4_m2[2];

	double bTag_eventWeight_T_nom = 1, bTag_eventWeight_T_up= 1, bTag_eventWeight_T_down = 1, bTag_eventWeight_M_up = 1, bTag_eventWeight_M_down = 1,bTag_eventWeight_T_corr_up  = 1, bTag_eventWeight_T_corr_down = 1;
	double bTag_eventWeight_M_corr_up= 1, bTag_eventWeight_M_corr_down = 1,  bTag_eventWeight_bc_T_corr_up= 1,  bTag_eventWeight_bc_T_corr_down= 1, bTag_eventWeight_light_T_corr_up = 1, bTag_eventWeight_light_T_corr_down  = 1; 
	double bTag_eventWeight_bc_T_up= 1, bTag_eventWeight_bc_T_down = 1, bTag_eventWeight_light_T_up = 1,bTag_eventWeight_light_T_down = 1;
	double bTag_eventWeight_M_nom = 1;

   double prefiringWeight = 1;
   double pdf_weight = 1.0,factWeight=1.0, renormWeight = 1.0, scale_weight = 1.0,topPtWeight=1.0;
   std::vector<std::string> systematic_suffices;


   double nfatjets_double, nfatjets_pre_double, nAK4_double;

   int total_1b = 0, total_0b = 0;

   int totEventsUncut;

   double SJ1_BEST_scores[50], SJ2_BEST_scores[50];
   int SJ1_decision, SJ2_decision;
   bool fatjet_isHEM[100],jet_isHEM[100] ;


	systematic_suffices = {""};


   bool passesPFHT = false, passesPFJet = false;

   const char *_inFilename = inFileName.c_str();
   const char *_outFilename = outFileName.c_str();

   //std::cout << "---------  Reading file: " << _inFilename << std::endl;

   TFile *f = TFile::Open(_inFilename,"READ");

   if ((f == nullptr)||(f->IsZombie()) )
   {
		std::cout << "ERROR: File " << _inFilename << " not found - skipping !!" << std::endl;
		delete f;
        outFile_txt.close();
		return false;
   }
   TFile * outFile = TFile::Open(_outFilename,"UPDATE");
   
   for(auto systematic_suffix = systematic_suffices.begin(); systematic_suffix < systematic_suffices.end();systematic_suffix++)
   {

		outFile->cd();   // return to outer directory


      TDirectory* dir = outFile->GetDirectory(systematic.c_str()); // CHANGE
      if (!dir)   
      {
         dir = outFile->mkdir( "nom" ); // CHANGE
      }
      dir->cd();


	
		std::string tree_name;
		std::string systematic_use = systematic;

		// these systematics are characterized by event weights that are stored in the "nom" tree
		tree_name = "nom";
		systematic_use = "";


		TTree *t1;
		Int_t nentries;

		try
		{  
			t1 = (TTree*)f->Get(   ( tree_name  + "/skimmedTree_"+ tree_name ).c_str()    );
			if(t1 == nullptr)
			{
				std::cout << "ERROR: tree not found - " << ( tree_name  + "/skimmedTree_"+ tree_name ).c_str()  <<std::endl;
				delete f;
                outFile_txt.close();
				return false;
			}
			nentries = t1->GetEntries();
		}
		catch(...)
		{
			std::cout << "ERROR: tree not found - " << ( tree_name  + "/skimmedTree_"+ tree_name ).c_str()  <<std::endl;
			delete f;
            outFile_txt.close();
			return false;
		}
		std::cout << "Successfully got tree " << tree_name  + "/skimmedTree_"+ tree_name << std::endl;
		

		/////////////////////////////////////////
		//////  Region-specific histograms /////
		////////////////////////////////////////

		// SR
		TH2F *h_MSJ_mass_vs_MdSJ_SR = new TH2F("h_MSJ_mass_vs_MdSJ_SR","Superjet mass vs diSuperjet mass (Signal Region) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		// CR
		TH2F *h_MSJ_mass_vs_MdSJ_CR = new TH2F("h_MSJ_mass_vs_MdSJ_CR","Superjet mass vs diSuperjet mass (Control Region) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		/// AT0b
		TH2F *h_MSJ_mass_vs_MdSJ_AT0b = new TH2F("h_MSJ_mass_vs_MdSJ_AT0b","Tagged Superjet 2 mass vs diSuperjet mass (AT0b) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		// AT1b
		TH2F *h_MSJ_mass_vs_MdSJ_AT1b = new TH2F("h_MSJ_mass_vs_MdSJ_AT1b","Tagged Superjet 2 mass vs diSuperjet mass (AT1b) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		/// AT0tb
		TH2F *h_MSJ_mass_vs_MdSJ_AT0tb = new TH2F("h_MSJ_mass_vs_MdSJ_AT0tb","Tagged Superjet 2 mass vs diSuperjet mass (AT0tb) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		// AT1tb
		TH2F *h_MSJ_mass_vs_MdSJ_AT1tb = new TH2F("h_MSJ_mass_vs_MdSJ_AT1tb","Tagged Superjet 2 mass vs diSuperjet mass (AT1tb) (cut-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125

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




        TH1F* h_totHT_1b  = new TH1F("h_totHT_1b","Event H_{T} (1b region);H_{T} [GeV]; Events / 200 GeV",50,0.,10000);

		///////////////////////////////////////////////////////////////////////
		///////////////////////// NN - based tagging //////////////////////////
		///////////////////////////////////////////////////////////////////////

		TH2F *h_MSJ_mass_vs_MdSJ_NN_SR = new TH2F("h_MSJ_mass_vs_MdSJ_NN_SR","Superjet mass vs diSuperjet mass (Signal Region) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_NN_CR = new TH2F("h_MSJ_mass_vs_MdSJ_NN_CR","Superjet mass vs diSuperjet mass (Control Region) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_NN_AT1b = new TH2F("h_MSJ_mass_vs_MdSJ_NN_AT1b","Superjet mass vs diSuperjet mass (AT1b) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125
		TH2F *h_MSJ_mass_vs_MdSJ_NN_AT0b = new TH2F("h_MSJ_mass_vs_MdSJ_NN_AT0b","Superjet mass vs diSuperjet mass (AT0b) (NN-based); diSuperjet mass [GeV];superjet mass", 22,1250., 10000, 20, 500, 5000);  /// 375 * 125


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

		t1->SetBranchAddress("SJ1_BEST_scores", SJ1_BEST_scores); 
		t1->SetBranchAddress("SJ2_BEST_scores", SJ2_BEST_scores); 
		t1->SetBranchAddress("SJ1_decision", &SJ1_decision); 
		t1->SetBranchAddress("SJ2_decision", &SJ2_decision); 

		t1->SetBranchAddress("AK4_m1", AK4_m1); 
		t1->SetBranchAddress("AK4_m2", AK4_m2); 

		t1->SetBranchAddress("SJ2_decision", &SJ2_decision); 

		t1->SetBranchAddress("fatjet_isHEM", fatjet_isHEM); 
		t1->SetBranchAddress("jet_isHEM", jet_isHEM); 
		t1->SetBranchAddress("prefiringWeight_nom", &prefiringWeight);


		// MC-only vars 
		if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos))
		{ 
			// nominal systematics
			t1->SetBranchAddress("bTag_eventWeight_T_nom", &bTag_eventWeight_T_nom); 
			t1->SetBranchAddress("bTag_eventWeight_M_nom", &bTag_eventWeight_M_nom);
			t1->SetBranchAddress("PU_eventWeight_nom", &PU_eventWeight);

			t1->SetBranchAddress("AK4_partonFlavour", AK4_partonFlavour); 
			t1->SetBranchAddress("AK4_hadronFlavour", AK4_HadronFlavour);
		}

		pdf_weight = 1.0; 
		scale_weight = 1.0; 
		renormWeight = 1.0;
		factWeight   = 1.0;
		topPtWeight = 1.0;

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

		double nEvents = 0,nHTcut  = 0,nAK8JetCut = 0,nHeavyAK8Cut = 0,nBtagCut = 0,nDoubleTagged = 0, nZeroBtagAntiTag = 0,nNN_CR = 0,nNN_AT0b = 0,
			nOneBtagAntiTag = 0,nNN_SR = 0,nNN_AT1b = 0, nDoubleTaggedCR = 0, nNoBjets = 0;

		for (Int_t i=0;i<nentries;i++) 
		{  
			nomBtaggingWeight=1.0;

			t1->GetEntry(i);

			if ((dataBlock.find("Suu") != std::string::npos))
			{
				if( eventNumber%10 > 2) continue; // should only be for signal
			}

		  ///// APPLY TRIGGER 
		  if ( (!passesPFHT) && (!passesPFJet) ) continue; // skip events that don't pass at least one trigger
	
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

			if(fails_veto_map) continue;
			if(fails_HEM) continue; 

			double eventScaleFactor = 1.0;
			double bTag_eventWeight_M = 1, bTag_eventWeight_T = 1;





			if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos)  )
			{

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
				}

				if ((factWeight != factWeight) || (std::isinf(factWeight))  || (std::isnan(factWeight)) || (abs(factWeight) > 100) || (factWeight < 0. ))
				{
					factWeight = 1.0;
				  // num_bad_scale++;
					//std::cout << "BAD factorization weight during " << systematic << "_" << *systematic_suffix << ": " << factWeight << std::endl;
				}

				if ((renormWeight != renormWeight) || (std::isinf(renormWeight))  || (std::isnan(renormWeight)) || (abs(renormWeight) > 100) || (renormWeight < 0.))
				{
					renormWeight = 1.0;

				  //std::cout << "BAD renormalization weight during " << systematic << "_" << *systematic_suffix << ": " << renormWeight << std::endl;
				}

				scale_weight = renormWeight*factWeight;  

				if ((topPtWeight != topPtWeight) || (std::isinf(topPtWeight)) || (std::isnan(topPtWeight)) || (abs(topPtWeight) > 100) || (topPtWeight < 0.))
				{
					topPtWeight = 1.0;
					num_bad_topPt++;

				}
				

				if ((pdf_weight != pdf_weight) || (std::isinf(pdf_weight)) || (std::isnan(pdf_weight)) || (abs(pdf_weight) > 100) || (pdf_weight < 0.)  )
				{
					pdf_weight = 1.0;
					num_bad_pdf++;

				}
	 
				eventScaleFactor = PU_eventWeight*topPtWeight;   /// these are all MC-only systematics, the b-tagging, fact, and renorm event weights will be applied after selection

				// set the b-tagging event weight based on the systematic
				// only valid for MC
				bTag_eventWeight_M = bTag_eventWeight_M_nom;
				bTag_eventWeight_T = bTag_eventWeight_T_nom;

				////// check MC systematics
				if ((bTag_eventWeight_M != bTag_eventWeight_M) || (std::isinf(bTag_eventWeight_M)) || (std::isnan(bTag_eventWeight_M)) || (abs(bTag_eventWeight_M) > 100) || (bTag_eventWeight_M < 0.)  )
				{
					bTag_eventWeight_M = 1.0;
					//std::cout << "event weight was bad!!" << std::endl;
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

			int nTightBTags = 0, nMedBTags = 0, nLooseBtags =0;
			int nAK4_pt50 = 0, nAK4_pt75 = 0, nAK4_pt100 = 0, nAK4_pt150 =0;
			int nMedBTags_pt50 = 0, nMedBTags_pt75 = 0, nMedBTags_pt100 = 0, nMedBTags_pt150 =0;
			int nTightBTags_pt30 = 0, nTightBTags_pt50 = 0, nTightBTags_pt75 = 0, nTightBTags_pt100 = 0, nTightBTags_pt150 =0;

			int nGenBJets;
			for(int iii = 0;iii< nAK4; iii++)
			{

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
				if ( (AK4_DeepJet_disc[iii] > tightDeepCSV_DeepJet ) && (AK4_pt[iii] > 150.))nTightBTags++;
				if ( (AK4_DeepJet_disc[iii] > medDeepCSV_DeepJet )   && (AK4_pt[iii] > 150.)) nMedBTags++; 
				if ( (AK4_DeepJet_disc[iii] > looseDeepCSV_DeepJet ) && (AK4_pt[iii] > 150.)) nLooseBtags++;
				if(abs(AK4_HadronFlavour[iii]) == 5) nGenBJets++;


                // some b-tagging rate stuff
                if ((dataBlock.find("QCD") != std::string::npos)    && ( AK4_pt[iii] > 75.    ))
                {
                    if(abs(AK4_HadronFlavour[iii]) == 5)
                    {
                        total_trueb_jets_QCD+=1.0;
                        if ( AK4_DeepJet_disc[iii] > medDeepCSV_DeepJet )  btagged_trueb_jets_QCD+=1.0;                        
                    }
                    total_AK4_jets_QCD+=1.0;
                    if ( AK4_DeepJet_disc[iii] > medDeepCSV_DeepJet ) btagged_AK4_jets_QCD+=1.0;
                }
                else if (    ((dataBlock.find("TTbar") != std::string::npos)   || (dataBlock.find("TTJets") != std::string::npos   )  ) && ( AK4_pt[iii] > 75.   )   )
                {
                    if(abs(AK4_HadronFlavour[iii]) == 5)
                    {
                        total_trueb_jets_TTbar+=1.0;
                        if ( AK4_DeepJet_disc[iii] > medDeepCSV_DeepJet )btagged_trueb_jets_TTbar+=1.0;
                    }

                    total_AK4_jets_TTbar+=1.0;
                    if ( AK4_DeepJet_disc[iii] > medDeepCSV_DeepJet )btagged_AK4_jets_TTbar+=1.0;
                }

			}

			nEvents+=eventScaleFactor;


			if(runType == "main-band")
			{
				if ( (totHT < 1600.)    ) continue;
			}
			else if(runType == "side-band")
			{
				 if ( (totHT > 1600.)  || (totHT < 1200)   ) continue;
			}
			nHTcut+=eventScaleFactor;
			if( (nfatjets < 3) ) continue;
			nAK8JetCut+=eventScaleFactor;
			if ((nfatjet_pre < 2) && ( (dijetMassOne < 1000. ) || ( dijetMassTwo < 1000.)  ))continue;
 

            outFile_txt << SJ1_BEST_scores[0] << "     " << SJ1_BEST_scores[1] << "     " << SJ1_BEST_scores[2] << "     " << SJ2_BEST_scores[0] << "     " << SJ2_BEST_scores[1] << "     " << SJ2_BEST_scores[2] <<  "\n";




			nHeavyAK8Cut+=eventScaleFactor;
			double eventWeightToUse = eventScaleFactor; 

			if (eventWeightToUse< 0.001)  std::cout << "ERROR: bad eventWeightToUse for " <<dataBlock << "/" << systematic << "/" << dataYear << ", value = " << eventWeightToUse <<std::endl;

			///////////////////////////////////////////////////////
			/////////////////// main-band /////////////////////////
			///////////////////////////////////////////////////////

			if(runType == "main-band")
			{
				///////////////////////////////////////////////////////
				////////////////////// b-tagging //////////////////////
				///////////////////////////////////////////////////////
				eventnum++;

				///////////////////////////////
				////////// 0b region //////////
				///////////////////////////////

				if( nMedBTags < 1 ) 
				{



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
                    nNoBjets+=eventScaleFactor;

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
							eventWeightToUse *= pdf_weight*factWeight*renormWeight;


							/// CHANGE THIS
							//eventWeightToUse = 1.0;

							nDoubleTaggedCR+=eventWeightToUse;
							h_MSJ_mass_vs_MdSJ_CR->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2   ,eventWeightToUse );
 
						}

					}

					///////////////////
					////// AT0b ///////
					///////////////////

					else if(   (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<25.)  && (AK4_m1[0] < 25.) && (AK4_m2[0] < 25.)  )  
					{
						if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
						{
							eventWeightToUse *= pdf_weight*factWeight*renormWeight;

							/// CHANGE THIS
							//eventWeightToUse = 1.0;

							nZeroBtagAntiTag+=eventWeightToUse;
							h_MSJ_mass_vs_MdSJ_AT0b->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse);
						}  

					}

					////////////////////////////////////////////////////////////
					///////////////////// NN-based tagging /////////////////////
					////////////////////////////////////////////////////////////

					///////////////////
					////// NN CR //////
					///////////////////
					if(  (SJ1_decision == 0) && (SJ2_decision == 0) && (SJ2_BEST_scores[0] > 0.4) && (SJ2_BEST_scores[0])> 0.4) // should kill some of the ST BR
					{



						 double eventWeightToUse_NN = eventScaleFactor;
						 if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos)) eventWeightToUse_NN*=bTag_eventWeight_M;
						 eventWeightToUse_NN *= pdf_weight*factWeight*renormWeight;

						nNN_CR +=eventWeightToUse_NN;
						h_MSJ_mass_vs_MdSJ_NN_CR->Fill(diSuperJet_mass,(superJet_mass[1]+superJet_mass[0])/2,eventWeightToUse_NN);

					}

					///////////////////
					///// NN AT0b /////
					///////////////////
					else if(  (SJ1_decision == 0) && (SJ2_decision != 0) && (SJ2_BEST_scores[0] < 0.2) ) // want to be quite sure the second superjet is not tagged
					{
						 double eventWeightToUse_NN = eventScaleFactor*=bTag_eventWeight_M;
						 if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos)) eventWeightToUse_NN*=bTag_eventWeight_M;
						 eventWeightToUse_NN *= pdf_weight*factWeight*renormWeight;

						nNN_AT0b +=eventScaleFactor;
						h_MSJ_mass_vs_MdSJ_NN_AT0b->Fill(diSuperJet_mass,superJet_mass[0],eventWeightToUse_NN);

					} 
				}
				
				/////////////////////////////
				///////// 1b region /////////
				/////////////////////////////



				else if ( (nMedBTags > 0)  )
				{

					if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventWeightToUse*=bTag_eventWeight_M;


                    h_totHT_1b->Fill(totHT, eventWeightToUse);   // this is for getting the fraction of events per sample HT bin in the 1b region 

					nBtagCut+=eventWeightToUse;

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

							eventWeightToUse *= pdf_weight*factWeight*renormWeight;


							/// CHANGE THIS
							//eventWeightToUse = 1.0;
							nDoubleTagged+= eventWeightToUse; 

							h_MSJ_mass_vs_MdSJ_SR->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventWeightToUse   );
						}
					}


					///////////////////
					////// AT1b ///////
					///////////////////
					else if(   (SJ_nAK4_50[0]<1) && (SJ_mass_100[0]<25.)  && (AK4_m1[0] < 25.) && (AK4_m2[0] < 25.)  )  
					{
						if((SJ_nAK4_300[1]>=2) && (SJ_mass_100[1]>=400.)   )
						{
							eventWeightToUse *= pdf_weight*factWeight*renormWeight;

							/// CHANGE THIS
							//eventWeightToUse = 1.0;

							nOneBtagAntiTag+=eventWeightToUse;
							h_MSJ_mass_vs_MdSJ_AT1b->Fill(diSuperJet_mass,superJet_mass[1],eventWeightToUse);
						}
					}


					////////////////////////////////////////////////////////////
					///////////////////// NN-based tagging /////////////////////
					////////////////////////////////////////////////////////////

					///////////////////
					////// NN SR //////
					///////////////////
					if(  (SJ1_decision == 0) && (SJ2_decision == 0) && (SJ2_BEST_scores[0] > 0.4) && (SJ2_BEST_scores[0])> 0.4) // should kill some of the ST BR
					{
						{
							 double eventWeightToUse_NN = eventScaleFactor;
							 if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventWeightToUse_NN*=bTag_eventWeight_M;
							 eventWeightToUse_NN *= pdf_weight*factWeight*renormWeight;
							nNN_SR +=eventScaleFactor;
							h_MSJ_mass_vs_MdSJ_NN_SR->Fill(diSuperJet_mass,(    superJet_mass[1]+superJet_mass[0])/2 ,eventWeightToUse_NN);
						}
					}

					///////////////////
					///// NN AT1b /////
					///////////////////
					else if(  (SJ1_decision == 0) && (SJ2_decision != 0) && (SJ2_BEST_scores[0] < 0.2) ) // want to be quite sure the second superjet is not tagged
					{
						{
							 double eventWeightToUse_NN = eventScaleFactor;
							 if ((inFileName.find("MC") != std::string::npos) ||(inFileName.find("Suu") != std::string::npos))eventWeightToUse_NN*=bTag_eventWeight_M;
							 eventWeightToUse_NN *= pdf_weight*factWeight*renormWeight;

							nNN_AT1b +=eventScaleFactor;
							h_MSJ_mass_vs_MdSJ_NN_AT1b->Fill(diSuperJet_mass,superJet_mass[0],eventWeightToUse_NN );
						}
					} 

				}

			}

			double eventScaleFactor_M_pt75 = 1.0*prefiringWeight;
			double eventScaleFactor_M_pt100 = 1.0*prefiringWeight;
			double eventScaleFactor_M_pt150 = 1.0*prefiringWeight;

			if ((inFileName.find("MC") != std::string::npos) || (inFileName.find("Suu") != std::string::npos) )
			{
				eventScaleFactor_M_pt75  = PU_eventWeight*topPtWeight*pdf_weight*factWeight*renormWeight;  
				eventScaleFactor_M_pt100 = PU_eventWeight*topPtWeight*pdf_weight*factWeight*renormWeight;  
				eventScaleFactor_M_pt150 = PU_eventWeight*topPtWeight*pdf_weight*factWeight*renormWeight;  
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


			if(  (SJ1_decision == 0) && (SJ2_decision == 0) && (SJ2_BEST_scores[0] > 0.4) && (SJ2_BEST_scores[0])> 0.4 ) isDoubleNNTagged = true;
			else if(  (SJ1_decision == 0) && (SJ2_decision != 0) && (SJ2_BEST_scores[0] < 0.2) ) isNNAntiTagged = true;
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
 
		/// update counters
		double MC_SF = 1.0;

		if (( dataBlock.find("Suu") != std::string::npos) )
		{
		   std::vector<std::string> decays = {"WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"};
		   std::vector<std::string> mass_points = {"Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1", "Suu5_chi1p5", "Suu5_chi2", "Suu6_chi1","Suu6_chi1p5", "Suu6_chi2",
		   "Suu6_chi2p5", "Suu7_chi1","Suu7_chi1p5","Suu7_chi2", "Suu7_chi2p5", "Suu7_chi3","Suu8_chi1", "Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"};

		   std::string decay = "";
		   std:;string mass_point = "";

		   for(auto mass_point_i = mass_points.begin(); mass_point_i != mass_points.end(); mass_point_i++)
		   {
		   	if ( dataBlock.find(*mass_point_i) != std::string::npos) mass_point = *mass_point_i;
			}
			for(auto decay_i = decays.begin(); decay_i != decays.end(); decay_i++)
		   {
		   	if ( dataBlock.find(*decay_i) != std::string::npos) decay = *decay_i;
		   }

		   MC_SF = return_signal_SF( dataYear, mass_point,decay);

		   // now get the event scale factor 
		   signal_mass_SR[mass_point][decay]+= MC_SF*nDoubleTagged;
			signal_mass_CR[mass_point][decay]+= MC_SF*nDoubleTaggedCR;
			signal_mass_AT1b[mass_point][decay]+= MC_SF*nOneBtagAntiTag;
			signal_mass_AT0b[mass_point][decay]+= MC_SF*nZeroBtagAntiTag;

		}
		else if(  dataBlock.find("QCD") != std::string::npos )
		{
			MC_SF = return_BR_SF(dataYear, dataBlock) ;

			total_QCD_SR+= MC_SF*nDoubleTagged;
			total_QCD_CR+= MC_SF*nDoubleTaggedCR;
			total_QCD_AT1b+= MC_SF*nOneBtagAntiTag;
			total_QCD_AT0b+= MC_SF*nZeroBtagAntiTag;
		}

		else if(  (dataBlock.find("TTTo") != std::string::npos )  )  // || (dataBlock.find("TTJets") != std::string::npos)
		{
			MC_SF = return_BR_SF(dataYear, dataBlock) ;

			total_TTbar_SR+= MC_SF*nDoubleTagged;
			total_TTbar_CR+= MC_SF*nDoubleTaggedCR;
			total_TTbar_AT1b+= MC_SF*nOneBtagAntiTag;
			total_TTbar_AT0b+= MC_SF*nZeroBtagAntiTag;
		}

		else if(  dataBlock.find("ST_") != std::string::npos )
		{
			MC_SF = return_BR_SF(dataYear, dataBlock) ;

			total_ST_SR+= MC_SF*nDoubleTagged;
			total_ST_CR+= MC_SF*nDoubleTaggedCR;
			total_ST_AT1b+= MC_SF*nOneBtagAntiTag;
			total_ST_AT0b+= MC_SF*nZeroBtagAntiTag;
		}
		else if(  dataBlock.find("WJets") != std::string::npos )
		{
			MC_SF = return_BR_SF(dataYear, dataBlock) ;

			total_WJets_SR+= MC_SF*nDoubleTagged;
			total_WJets_CR+= MC_SF*nDoubleTaggedCR;
			total_WJets_AT1b+= MC_SF*nOneBtagAntiTag;
			total_WJets_AT0b+= MC_SF*nZeroBtagAntiTag;
		}
		else if (  dataBlock.find("data") != std::string::npos )
		{
			total_data_SR+= nDoubleTagged;
			total_data_CR+= nDoubleTaggedCR;
			total_data_AT1b+= nOneBtagAntiTag;
			total_data_AT0b+= nZeroBtagAntiTag;

		}

		// kill histograms
		delete h_MSJ_mass_vs_MdSJ_SR, h_MSJ_mass_vs_MdSJ_CR, h_MSJ_mass_vs_MdSJ_AT0b, h_MSJ_mass_vs_MdSJ_AT1b, h_MSJ_mass_vs_MdSJ_AT0tb, h_MSJ_mass_vs_MdSJ_AT1tb, 
	    h_MSJ_mass_vs_MdSJ_SR_bpt75, h_MSJ_mass_vs_MdSJ_SR_bpt100, h_MSJ_mass_vs_MdSJ_SR_bpt150, h_MSJ_mass_vs_MdSJ_CR_bpt75, h_MSJ_mass_vs_MdSJ_CR_bpt100, 
		h_MSJ_mass_vs_MdSJ_CR_bpt150, h_MSJ_mass_vs_MdSJ_AT1b_bpt75, h_MSJ_mass_vs_MdSJ_AT1b_bpt100, h_MSJ_mass_vs_MdSJ_AT1b_bpt150, h_MSJ_mass_vs_MdSJ_AT0b_bpt75, h_MSJ_mass_vs_MdSJ_AT0b_bpt100, 
		h_MSJ_mass_vs_MdSJ_AT0b_bpt150, h_MSJ_mass_vs_MdSJ_NN_SR_bpt75, h_MSJ_mass_vs_MdSJ_NN_SR_bpt100, h_MSJ_mass_vs_MdSJ_NN_SR_bpt150, h_MSJ_mass_vs_MdSJ_NN_CR_bpt75, 
		h_MSJ_mass_vs_MdSJ_NN_CR_bpt100, h_MSJ_mass_vs_MdSJ_NN_CR_bpt150, h_MSJ_mass_vs_MdSJ_NN_AT1b_bpt75, h_MSJ_mass_vs_MdSJ_NN_AT1b_bpt100, h_MSJ_mass_vs_MdSJ_NN_AT1b_bpt150, 
		h_MSJ_mass_vs_MdSJ_NN_AT0b_bpt75, h_MSJ_mass_vs_MdSJ_NN_AT0b_bpt100, h_MSJ_mass_vs_MdSJ_NN_AT0b_bpt150, h_MSJ_mass_vs_MdSJ_NN_SR, h_MSJ_mass_vs_MdSJ_NN_CR, h_MSJ_mass_vs_MdSJ_NN_AT1b, 
		h_MSJ_mass_vs_MdSJ_NN_AT0b;




        std::cout << std::endl;
        std::cout << std::endl;
        std::cout << std::endl;

        std::cout << "#########################################################################################" << std::endl;
        std::cout << "#########################################################################################" << std::endl;
        std::cout << "###################################### UNSCALED #########################################" << std::endl;
        std::cout << "#########################################################################################" << std::endl;
        std::cout << "#########################################################################################" << std::endl;

        std::cout << std::endl;
        std::cout << std::endl;
        std::cout << std::endl;
        std::cout << "Total 1b double tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/1+ b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nBtagCut << "/" << nDoubleTagged << std::endl;
        std::cout << "Total 0b double tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/0 b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nNoBjets << "/" << nDoubleTaggedCR << std::endl;
        std::cout << "Total 1b anti tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/0 b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nBtagCut << "/" << nOneBtagAntiTag << std::endl;
        std::cout << "Total 0b anti tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/0 b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nNoBjets << "/" << nZeroBtagAntiTag << std::endl;
        std::cout << "Total events in the NN_SR/NN_CR/NN_AT1b/NN_AT0b: " << nNN_SR << "/" << nNN_CR << "/" << nNN_AT1b << "/" << nNN_AT0b << std::endl;
        std::cout << std::endl;
        std::cout << std::endl;
        std::cout << std::endl;





		// scale these with the appropriate event SF
		nEvents*= MC_SF; nHTcut*= MC_SF;nAK8JetCut*= MC_SF;nHeavyAK8Cut*= MC_SF;nBtagCut*= MC_SF;nDoubleTagged*= MC_SF;
		nNoBjets*= MC_SF;nDoubleTaggedCR*= MC_SF;nOneBtagAntiTag*= MC_SF;nZeroBtagAntiTag*= MC_SF;



        std::cout << std::endl;
        std::cout << std::endl;
        std::cout << std::endl;

        std::cout << "#########################################################################################" << std::endl;
        std::cout << "#########################################################################################" << std::endl;
        std::cout << "###################################### SCALED #########################################" << std::endl;
        std::cout << "#########################################################################################" << std::endl;
        std::cout << "#########################################################################################" << std::endl;


		std::cout << "Finishing systematic " << systematic << " "<< *systematic_suffix << std::endl;
		//std::cout << "Total Events: " << totEventsUncut << " in " << inFileName << " for " << systematic << " "<< *systematic_suffix << std::endl;
		std::cout << "In " << inFileName << " there were " << num_bad_btagSF<< "/" << num_bad_PUSF<< "/"<< num_bad_topPt<< "/"<< num_bad_scale<< "/"<<num_bad_pdf << "/" <<num_bad_prefiring << " bad btag/PU/topPt/scale/pdf/prefiring event weights" << std::endl; 
		std::cout << "There were " << badEventSF << " bad events." << std::endl;
		std::cout << "Signal  Region for " << systematic+ "_" + *systematic_suffix << " " << dataBlock << ", "<<  dataYear  << " :" << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << "Total 1b double tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/1+ b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nBtagCut << "/" << nDoubleTagged << std::endl;
		std::cout << "Total 0b double tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/0 b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nNoBjets << "/" << nDoubleTaggedCR << std::endl;
		std::cout << "Total 1b anti tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/0 b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nBtagCut << "/" << nOneBtagAntiTag << std::endl;
		std::cout << "Total 0b anti tag breadown: " << " events total/HT/nAK8 jet/heavy AK8 +dijet/0 b jet/double tagged " << nEvents << "/"<<nHTcut << "/" <<nAK8JetCut << "/" <<nHeavyAK8Cut << "/" << nNoBjets << "/" << nZeroBtagAntiTag << std::endl;
		std::cout << "Total events in the NN_SR/NN_CR/NN_AT1b/NN_AT0b: " << nNN_SR << "/" << nNN_CR << "/" << nNN_AT1b << "/" << nNN_AT0b << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;




	}

   outFile_txt.close();
   outFile->Close();
   std::cout << "--------- Finished file " << inFileName << std::endl;
   delete f;
   delete outFile;
   return true;
}

void readTree_test()
{  

   bool debug 			= false;
   bool _verbose     	= false;
   bool runData			= false;
   bool runSignal    	= false;
   bool runBR	  		= false;
   bool runAll	 		= true;
   bool runDataBR    	= false;
   bool runSelection 	= false;
   bool runSingleFile 	= false;
   bool runSideband 		= false;
   int nFailedFiles = 0;
   std::string failedFiles = "";

   std::string runType = "main-band";
   std::string outputFolder = "processedFiles/test/";
   std::string eos_path	 =  "root://cmseos.fnal.gov//store/user/ecannaer/skimmedFiles/";


   std::vector<std::string> dataYears = {"2015","2016","2017","2018"};
   if(runSelection) dataYears = {"2015","2016","2017","2018"};
   std::vector<std::string> systematics = {"nom"};  // "scale"    "JEC_HF", "JEC_BBEC1", "JEC_EC2","JEC_HF_year", "JEC_EC2_year",   "bTag_eventWeight_bc_T", "bTag_eventWeight_light_T", "bTag_eventWeight_bc_M", "bTag_eventWeight_light_M", 


   // delete root files in the /Users/ethan/Documents/rootFiles/processedRootFiles folder
   std::vector<std::string> signalFilePaths;
   std::vector<std::string> decays = {"WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"};
   std::vector<std::string> mass_points = {"Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1", "Suu5_chi1p5", "Suu5_chi2", "Suu6_chi1","Suu6_chi1p5", "Suu6_chi2",
   "Suu6_chi2p5", "Suu7_chi1","Suu7_chi1p5","Suu7_chi2", "Suu7_chi2p5", "Suu7_chi3","Suu8_chi1", "Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"};


    // Create the nested map
    std::map<std::string, std::map<std::string, double>> signal_mass_SR;
    std::map<std::string, std::map<std::string, double>> signal_mass_CR;
    std::map<std::string, std::map<std::string, double>> signal_mass_AT1b;
    std::map<std::string, std::map<std::string, double>> signal_mass_AT0b;

    // Populate the map with default values
    for (const auto& mass_point : mass_points) 
    {
        for (const auto& decay : decays) 
        {
            signal_mass_SR[mass_point][decay] = 0.0; 
            signal_mass_CR[mass_point][decay] = 0.0;
            signal_mass_AT1b[mass_point][decay] = 0.0; 
            signal_mass_AT0b[mass_point][decay] = 0.0; 
        }
    }



   for(auto decay = decays.begin(); decay!= decays.end();decay++)
   {
		for(auto mass_point = mass_points.begin();mass_point!= mass_points.end();mass_point++)
		{
			signalFilePaths.push_back((*mass_point+ "_"+ *decay + "_").c_str());
		}
   }
 
   for(auto dataYear = dataYears.begin(); dataYear < dataYears.end();dataYear++ )
   {


        // want to know the total number of events in each region for each year. 
       double total_QCD_SR = 0;
       double total_TTbar_SR = 0;
       double total_WJets_SR = 0;
       double total_ST_SR    = 0;
       double total_data_SR    = 0;

       double total_QCD_CR = 0;
       double total_TTbar_CR = 0;
       double total_WJets_CR = 0;
       double total_ST_CR    = 0;
       double total_data_CR    = 0;

       double total_QCD_AT1b = 0;
       double total_TTbar_AT1b = 0;
       double total_WJets_AT1b = 0;
       double total_ST_AT1b = 0 ;
       double total_data_AT1b    = 0;

       double total_QCD_AT0b = 0;
       double total_TTbar_AT0b = 0;
       double total_WJets_AT0b = 0;
       double total_ST_AT0b = 0 ;
       double total_data_AT0b    = 0;

       double total_AK4_jets_QCD      = 0;
       double btagged_AK4_jets_QCD    = 0; 
       double total_AK4_jets_TTbar    = 0;
       double btagged_AK4_jets_TTbar  = 0;


        double btagged_trueb_jets_QCD      = 0;
        double total_trueb_jets_QCD      = 0;
        double btagged_trueb_jets_TTbar      = 0;
        double total_trueb_jets_TTbar      = 0;


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
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_",  "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"}; // dataB-ver1 not present
				}
				else if(*dataYear == "2016")
				{
					dataBlocks = {"dataF_", "dataG_", "dataH_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_", "TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"};
				}
				else if(*dataYear == "2017")
				{
					dataBlocks = {"dataB_","dataC_","dataD_","dataE_", "dataF_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"};
				}
				else if(*dataYear == "2018")
				{
					dataBlocks = {"dataA_","dataB_","dataC_","dataD_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"};
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
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"};
			}
			else if(runDataBR)
			{
				std::cout << "Running as data+BR" << std::endl;
				if(*dataYear == "2015")
				{
					dataBlocks = {"dataB-ver2_","dataC-HIPM_","dataD-HIPM_","dataE-HIPM_","dataF-HIPM_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_","TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"}; // dataB-ver1 not present
				}
				else if(*dataYear == "2016")
				{
					dataBlocks = {"dataF_", "dataG_", "dataH_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"};
				}
				else if(*dataYear == "2017")
				{
					dataBlocks = {"dataB_","dataC_","dataD_","dataE_", "dataF_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"};
				}
				else if(*dataYear == "2018")
				{
					dataBlocks = {"dataA_","dataB_","dataC_","dataD_","QCDMC1000to1500_","QCDMC1500to2000_","QCDMC2000toInf_", "TTJetsMCHT800to1200_", "TTJetsMCHT1200to2500_", "TTJetsMCHT2500toInf_","TTToHadronicMC_","TTToSemiLeptonicMC_" , "TTToLeptonicMC_",
				"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_", "WJetsMC_LNu-HT800to1200_", "WJetsMC_LNu-HT1200to2500_",  "WJetsMC_LNu-HT2500toInf_", "WJetsMC_QQ-HT800toInf_"};
				}   
			}
			else if(runSelection)
			{

				dataBlocks = { "Suu7_chi2p5_HTHT_", "Suu5_chi2_HTZT_", "Suu5_chi1p5_ZTZT_", "Suu6_chi2_ZTZT_", "Suu8_chi3_ZTZT_"} ; 
				//dataBlocks = {"ST_t-channel-top_inclMC_","ST_t-channel-antitop_inclMC_","ST_s-channel-hadronsMC_","ST_s-channel-leptonsMC_","ST_tW-antiTop_inclMC_","ST_tW-top_inclMC_"};
			}
			else if ( runSingleFile)
			{

				double nEvents = 0, nHTcut  = 0, nAK8JetCut = 0, nHeavyAK8Cut = 0, nBtagCut = 0, nDoubleTagged = 0, nNoBjets = 0;
				double nDoubleTaggedCR = 0, NNDoubleTag = 0, nZeroBtagAntiTag = 0, nOneBtagAntiTag = 0;
				double nNN_SR = 0, nNN_CR = 0 , nNN_AT1b = 0,nNN_AT0b = 0;	  


				double eventScaleFactor = 1.0;
				std::string dataYear = "2018";
				std::string systematic = "nom";
				std::string dataBlock = "Suu4TeV_chi1TeV_";

				///   Suu6_chi1p5_ZTZT_2018_genPartFiltered_combimed.root
				std::string inFileName = ( dataBlock+  dataYear + "_genPartFiltered_combimed.root").c_str();
				std::string outFileName = ( dataBlock+  dataYear + "_genPartFiltered_processed.root").c_str();

				doThings(inFileName,outFileName,total_QCD_SR, total_TTbar_SR, total_WJets_SR, total_ST_SR, total_data_SR, signal_mass_SR, total_QCD_CR, total_TTbar_CR, total_WJets_CR, total_ST_CR, total_data_CR, signal_mass_CR, total_QCD_AT1b, total_TTbar_AT1b, total_WJets_AT1b, total_ST_AT1b, total_data_AT1b, total_AK4_jets_QCD, btagged_AK4_jets_QCD, total_AK4_jets_TTbar, btagged_AK4_jets_TTbar, btagged_trueb_jets_QCD,total_trueb_jets_QCD,btagged_trueb_jets_TTbar,total_trueb_jets_TTbar,     signal_mass_AT1b, total_QCD_AT0b, total_TTbar_AT0b, total_WJets_AT0b, total_ST_AT0b, total_data_AT0b, signal_mass_AT0b,  dataYear,systematic, dataBlock, runType );

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
				double nEvents = 0, nHTcut  = 0, nAK8JetCut = 0, nHeavyAK8Cut = 0, nBtagCut = 0, nDoubleTagged = 0, nNoBjets = 0;
				double nDoubleTaggedCR = 0, NNDoubleTag = 0, nZeroBtagAntiTag = 0, nOneBtagAntiTag = 0;
				double nNN_SR = 0, nNN_CR = 0 , nNN_AT1b = 0,nNN_AT0b = 0;

				std::string year = *dataYear;
				std::string systematic_str = "nom";

				if(debug) std::cout << "@@@@@@@@@@@@@ WARNING: YOU ARE IN DEBUG MODE. NOT ALL FILES WILL BE RUN. @@@@@@@@@@@@@@" << std::endl;
				std::string inFileName = (eos_path + *dataBlock+  year +  "_"+ systematic_str+ "_SKIMMED.root").c_str();
			
				if (( inFileName.find("Suu") != std::string::npos) ) inFileName = (eos_path+ *dataBlock+  year + "_SKIMMED.root").c_str();


				// if this is JEC and the uncertainty isn't in the JEC1 list, it must be in the nom list and should use the nom naming scheme
				std::string outFileName = (outputFolder  + *dataBlock+ year + "_processed.root").c_str();

				if( failedFiles.find( (*dataBlock +"/" + year ).c_str()  ) != std::string::npos) continue; // skip files that failed for other uncertainties


				std::cout << "Reading File " << inFileName << " for year,sample,systematic " << year << "/" <<*dataBlock << "/" << *systematic<< std::endl;

				if (!doThings(inFileName,outFileName,total_QCD_SR, total_TTbar_SR, total_WJets_SR, total_ST_SR, total_data_SR, signal_mass_SR, total_QCD_CR, total_TTbar_CR, total_WJets_CR, total_ST_CR, total_data_CR, signal_mass_CR, total_QCD_AT1b, total_TTbar_AT1b, total_WJets_AT1b, total_ST_AT1b, total_data_AT1b, total_AK4_jets_QCD, btagged_AK4_jets_QCD, total_AK4_jets_TTbar, btagged_AK4_jets_TTbar, btagged_trueb_jets_QCD,total_trueb_jets_QCD,btagged_trueb_jets_TTbar,total_trueb_jets_TTbar, signal_mass_AT1b, total_QCD_AT0b, total_TTbar_AT0b, total_WJets_AT0b, total_ST_AT0b, total_data_AT0b, signal_mass_AT0b,  *dataYear, *systematic, *dataBlock, runType ))
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

		// print out the event information in a coherent way

		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout <<  "--------------------------- SUMMARY OF " << *dataYear <<" ------------------------- " << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << " ######### SIGNAL REGION ######### " << std::endl;
		std::cout << " ----   QCD: " << total_QCD_SR << std::endl;
		std::cout << " ---- TTbar: " << total_TTbar_SR << std::endl;
		std::cout << " ---- WJets: " << total_WJets_SR << std::endl;
		std::cout << " ----    ST: " << total_ST_SR << std::endl;
		std::cout << " -------------- TOTAL: " << (total_QCD_SR+total_TTbar_SR+total_WJets_SR+total_ST_SR) << std::endl;
		std::cout << std::endl;
		std::cout << " --------------- data: " << total_data_SR << std::endl;
		std::cout << std::endl;

		std::cout << "------- signal yields: " << std::endl;
	   // Populate the map with default values
	   for (const auto& mass_point : mass_points) 
	   {
			double total_signal_yield_SR = 0;
			for (const auto& decay : decays) 
			{
				total_signal_yield_SR += signal_mass_SR[mass_point][decay]; 
			}
			std::cout << "--- " << mass_point << ": " << total_signal_yield_SR << std::endl;
		}
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;

		std::cout << " ######### CONTROL REGION ######### " << std::endl;
		std::cout << " ----   QCD: " << total_QCD_CR << std::endl;
		std::cout << " ---- TTbar: " << total_TTbar_CR << std::endl;
		std::cout << " ---- WJets: " << total_WJets_CR << std::endl;
		std::cout << " ----    ST: " << total_ST_CR << std::endl;
		std::cout << " -------------- TOTAL: " << (total_QCD_CR+total_TTbar_CR+total_WJets_CR+total_ST_CR) << std::endl;
		std::cout << std::endl;
		std::cout << " --------------- data: " << total_data_CR << std::endl;
		std::cout << std::endl;

		std::cout << "------- signal yields: " << std::endl;
	   // Populate the map with default values
	   for (const auto& mass_point : mass_points) 
	   {
			double total_signal_yield_CR = 0;
			for (const auto& decay : decays) 
			{
				total_signal_yield_CR += signal_mass_CR[mass_point][decay]; 
			}
			std::cout << "--- " << mass_point << ": " << total_signal_yield_CR << std::endl;
		}
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;

		std::cout << " ######### AT1b REGION ######### " << std::endl;
		std::cout << " ----   QCD: " << total_QCD_AT1b << std::endl;
		std::cout << " ---- TTbar: " << total_TTbar_AT1b << std::endl;
		std::cout << " ---- WJets: " << total_WJets_AT1b << std::endl;
		std::cout << " ----    ST: " << total_ST_AT1b << std::endl;
		std::cout << " -------------- TOTAL: " << (total_QCD_AT1b+total_TTbar_AT1b+total_WJets_AT1b+total_ST_AT1b) << std::endl;
		std::cout << std::endl;
		std::cout << " --------------- data: " << total_data_AT1b << std::endl;
		std::cout << std::endl;

		std::cout << "------- signal yields: " << std::endl;
	   // Populate the map with default values
	   for (const auto& mass_point : mass_points) 
	   {
			double total_signal_yield_AT1b = 0;
			for (const auto& decay : decays) 
			{
				total_signal_yield_AT1b += signal_mass_AT1b[mass_point][decay]; 
			}
			std::cout << "--- " << mass_point << ": " << total_signal_yield_AT1b << std::endl;
		}
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;

		std::cout << " ######### AT0b REGION ######### " << std::endl;
		std::cout << " ----   QCD: " << total_QCD_AT0b << std::endl;
		std::cout << " ---- TTbar: " << total_TTbar_AT0b << std::endl;
		std::cout << " ---- WJets: " << total_WJets_AT0b << std::endl;
		std::cout << " ----    ST: " << total_ST_AT0b << std::endl;
		std::cout << " -------------- TOTAL: " << (total_QCD_AT0b+total_TTbar_AT0b+total_WJets_AT0b+total_ST_AT0b) << std::endl;
		std::cout << std::endl;
		std::cout << " --------------- data: " << total_data_AT0b << std::endl;
		std::cout << std::endl;

		std::cout << "------- signal yields: " << std::endl;
	   // Populate the map with default values
	   for (const auto& mass_point : mass_points) 
	   {
			double total_signal_yield_AT0b = 0;
			for (const auto& decay : decays) 
			{
				total_signal_yield_AT0b += signal_mass_AT0b[mass_point][decay]; 
			}
			std::cout << "--- " << mass_point << ": " << total_signal_yield_AT0b << std::endl;
		}
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;
		std::cout << std::endl;



        std::cout << std::endl;
        std::cout << std::endl;
        std::cout << std::endl;
        std::cout << std::endl;


        std::cout << "b-tagging rates: " << std::endl; 
        std::cout << std::endl;
        std::cout << std::endl;
        std::cout << "The QCD b-tagging rate (of all AK4 jets with pt > 75 GeV ) for " << *dataYear<<  "(all HT bins) was " << 1.0*btagged_AK4_jets_QCD/(1.0*total_AK4_jets_QCD ) <<"." << std::endl;
        std::cout << "The TTbar b-tagging rate (of all AK4 jets with pt > 75 GeV ) for " << *dataYear<<  "(all HT bins) was " << 1.0*btagged_AK4_jets_TTbar/(1.0*total_AK4_jets_TTbar ) <<"." << std::endl;
        std::cout << std::endl;
        std::cout << std::endl;
        std::cout << "The QCD b-tagging rate of true b jets for " << *dataYear<<  "(all HT bins) was " << 1.0*btagged_trueb_jets_QCD/(1.0*total_trueb_jets_QCD ) <<"." << std::endl;
        std::cout << "The TTbar b-tagging rate of true b jets for " << *dataYear<<  "(all HT bins) was " << 1.0*btagged_trueb_jets_TTbar/(1.0*total_trueb_jets_TTbar ) <<"." << std::endl;
        std::cout << std::endl;
        std::cout << std::endl;
        std::cout << std::endl;
        std::cout << std::endl;






   } // end year loop
} // end function


