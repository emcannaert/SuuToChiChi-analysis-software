////////////////////////////HELP////////////////////////////////
//////////////Uses new clustering algorithm to capture heavy resonance jet substructure//////////////
////////////////Last updated 17 Jul 2024 ////////////////////////////////////////////////////////////

//_top_
// system include files
#include <fastjet/JetDefinition.hh>
#include <fastjet/GhostedAreaSpec.hh>
#include <fastjet/PseudoJet.hh>
#include <fastjet/tools/Filter.hh>
#include <fastjet/ClusterSequence.hh>
//#include <fastjet/ActiveAreaSpec.hh>
#include <fastjet/ClusterSequenceArea.hh>
#include "FWCore/Framework/interface/EventSetup.h"
#include <memory>
#include <iostream>
#include <fstream>
#include <vector>
#include <thread>
#include <math.h>
#include "TH2.h"
#include<TRandom3.h>

#include "correction.h"
#include "ROOT/RDataFrame.hxx"
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CondFormats/DataRecord/interface/JetResolutionRcd.h"
#include "CondFormats/DataRecord/interface/JetResolutionScaleFactorRcd.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "FWCore/Common/interface/TriggerNames.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "PhysicsTools/CandUtils/interface/EventShapeVariables.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "SimDataFormats/GeneratorProducts/interface/GenRunInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
// new includes
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Math/interface/PtEtaPhiMass.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "PhysicsTools/CandUtils/interface/Thrust.h"
//#include "Thrust.h"
#include <TTree.h>
#include <cmath>
#include "TLorentzVector.h"
#include "TVector3.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include <algorithm>   
#include "DataFormats/PatCandidates/interface/MET.h"

#include "TTree.h"
#include "TFile.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "JetMETCorrections/JetCorrector/interface/JetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetResolutionObject.h"
#include "JetMETCorrections/Modules/interface/JetResolution.h"
#include "PhysicsTools/PatUtils/interface/SmearedJetProducerT.h"

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include <string>
#include "sortJets.h"
#include "BESTtoolbox.h"
#include "CacheHandler.h"
#include "BESTEvaluation.h"

#include "LHAPDF/LHAPDF.h"
#include "LHAPDF/Reweighting.h"

//#include "AnalysisDataFormats/TopObjects/interface/TtGenEvent.h"
//#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
using namespace reco;
using namespace correction;
typedef math::XYZTLorentzVector LorentzVector;
typedef math::XYZVector Vector;
using correction::CorrectionSet;
using namespace LHAPDF;
class selectionStudier : public edm::EDAnalyzer 
{
public:
   explicit selectionStudier(const edm::ParameterSet&);
private:
   virtual void analyze(const edm::Event&, const edm::EventSetup&);
   bool isgoodjet(double eta, double NHF,double NEMF, const size_t NumConst,double CHF,const int CHM, double MUF, double CEMF, double iJet_pt);
   bool isgoodjet(double eta, double NHF,double NEMF, const size_t NumConst,double CHF,const int CHM, double MUF, double CEMF, int nfatjets);

   bool isgoodjet(double eta, double NHF,double NEMF, const size_t NumConst,double CHF,const int CHM, double MUF, double CEMF);   // overloaded AK8 jet version of isGoodJet for cross-checks 

   bool isHEM(double jet_eta, double jet_phi);
   double top_pt_SF(double top_pt);
   std::map<std::string, std::map<std::string, std::string>> file_map;

   //init all inpaths, tokens, instrings
   edm::EDGetTokenT<std::vector<pat::Jet>> fatJetToken_;
   edm::EDGetTokenT<std::vector<pat::Jet>> jetToken_;
   edm::EDGetTokenT<std::vector<PileupSummaryInfo> > puSummaryToken_;
   edm::EDGetTokenT<edm::TriggerResults> triggerBits_;

   edm::EDGetTokenT< double > prefweight_token;


   TTree * tree;
   edm::FileInPath bTagSF_path;
   edm::FileInPath bTagEff_path;
   edm::EDGetTokenT<double> m_rho_token;

   edm::FileInPath PUfile_path;
   std::string runType;
   std::string systematicType;
   std::string year;
   std::string lumiTag;

   std::string jetVetoMapName;
   edm::FileInPath jetVetoMapFile;

   std::vector<std::string> triggers;

   bool doPUID = false;
   bool doPDF = false;
   int eventnum = 0;
   int nAK4 = 0;
   int nfatjets = 0;
   int raw_nfatjets;
   int tot_nAK4_50 =0,tot_nAK4_70 = 0;
   int tot_mpp_AK4 = 0;
   std::map<std::string, float> BESTmap;


   //init event variables
   bool doJEC              = true;
   bool doJER              = false;
   bool doBtagSF           = false;
   bool doPUSF             = false;
   bool doTopPtReweight    = false;
   bool doPDFWeights       = false;
   bool doPrefiringWeight  = true;
   bool _verbose           = false; // do printouts of each section for debugging
   bool debug              = false; // print out some other debug stuff
   bool runSideband        = false;
   double jet_pt[100], jet_eta[100], jet_mass[100], jet_dr[100], raw_jet_mass[100],raw_jet_pt[100],raw_jet_phi[100];
   double AK4_mass[100], AK4_E[500], leadAK8_mass[10];
   double top_pt_weight;
   double totHT = 0;
   double dijetMassOne, dijetMassTwo;
   int nfatjet_pre = 0;
   double AK4_bdisc[100], AK4_DeepJet_disc[100];
   int jet_ndaughters[100], jet_nAK4[100];
   int lab_nAK4 = 0;
   double lab_AK4_pt[100];
   double diAK8Jet_mass[100];

   bool passesJetPUID[100];
   double fourAK8JetMass;
   //double btag_score_uncut[100];
   double AK4_eta[100], AK4_phi[100];
   double bTag_eventWeight_T_nom, bTag_eventWeight_T_up, bTag_eventWeight_T_down, bTag_eventWeight_bc_T_up, bTag_eventWeight_bc_T_down, bTag_eventWeight_light_T_up, bTag_eventWeight_light_T_down;
   double bTag_eventWeight_M_nom, bTag_eventWeight_M_up, bTag_eventWeight_M_down, bTag_eventWeight_bc_M_up, bTag_eventWeight_bc_M_down, bTag_eventWeight_light_M_up, bTag_eventWeight_light_M_down;
   //BES variables

   double jet_phi[100];
   int ntrueInt;
   double PU_eventWeight_nom;
   double deepJet_wp_loose, deepJet_wp_med, deepjet_wp_tight;

   bool AK8_fails_veto_map[100], AK4_fails_veto_map[100];
   bool jet_isHEM[100], jet_pre_isHEM[100];
   TH2F *truebjet_eff,*truecjet_eff, *lightjet_eff;
   TH2F *truebjet_eff_med,*truecjet_eff_med, *lightjet_eff_med;

   TH2F * jetVetoMap;
   double prefiringWeight_nom;

   double bTagEffMap_PtRange, bTagEffMap_Eta_high, bTagEffMap_Eta_low;
   int bTagEffMap_nPtBins, bTagEffMap_nEtaBins;

   TRandom3 *randomNum = new TRandom3(); // for JERs

   bool passesPFJet = false, passesPFHT = false;

   // variables to create a control region

   int nHeavyAK8_pt400_M10 = 0, nHeavyAK8_pt400_M20 = 0, nHeavyAK8_pt400_M30 = 0;
   int nHeavyAK8_pt300_M10 = 0, nHeavyAK8_pt300_M20 = 0, nHeavyAK8_pt300_M30 = 0; 
   int nHeavyAK8_pt200_M10 = 0, nHeavyAK8_pt200_M20 = 0, nHeavyAK8_pt200_M30 = 0; 




   int nAK8_pt200 = 0, nAK8_pt300 = 0, nAK8_pt150 = 0, nHeavyAK8_pt500_M45 = 0, nAK8_pt500 = 0;   // |eta| < 2.4, tight jet ID, NO other cuts
   int nAK8_pt200_noCorr = 0, nAK8_pt300_noCorr = 0, nAK8_pt150_noCorr = 0, nHeavyAK8_pt500_M45_noCorr = 0, nAK8_pt500_noCorr = 0;   // these variables don't have weird eta cuts applied to them,

   ///////////////////////////////////////////////

   // btag scale factor stuff
   std::unique_ptr<CorrectionSet> cset;
   Correction::Ref cset_corrector_bc;
   Correction::Ref cset_corrector_light; 

   // Jet correction uncertainty classes
   JetCorrectionUncertainty *jecUnc_AK4;
   JetCorrectionUncertainty *jecUnc_AK8;
   std::unique_ptr<CorrectionSet> PUjson;
   Correction::Ref PUjson_year;

   // jet veto map stuff
   double jetVetoMap_XRange, jetVetoMap_YRange, jetVetoMap_Xmin, jetVetoMap_Ymin;
   int jetVetoMap_nBinsX, jetVetoMap_nBinsY;

};

//_constructor_
selectionStudier::selectionStudier(const edm::ParameterSet& iConfig)
{
   // import parameters from cfg, set variables needed to analyze the event
   runType        = iConfig.getParameter<std::string>("runType");
   systematicType = iConfig.getParameter<std::string>("systematicType");
   year           = iConfig.getParameter<std::string>("year");

   _verbose           = iConfig.getParameter<bool>("verbose");
   runSideband        = iConfig.getParameter<bool>("runSideband");

   jetVetoMapName = iConfig.getParameter<std::string>("jetVetoMapName");
   jetVetoMapFile = iConfig.getParameter<edm::FileInPath>("jetVetoMapFile");


   prefweight_token     = consumes< double >(edm::InputTag("prefiringweight:nonPrefiringProb"));

   doPDF = iConfig.getParameter<bool>("doPDF");

   triggerBits_ = consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"));

   if( (runType.find("MC") != std::string::npos) || (runType.find("Suu") != std::string::npos))    //don't want these variables for data
   {
      // these will only be done for MC
      doBtagSF = true;
      doJER    = true;
      doPUSF   = true;
      if(doPDF)doPDFWeights = true; 
      else {doPDFWeights = false;}

      if ((runType.find("TTTo") != std::string::npos) || (runType.find("TTJets") != std::string::npos)) doTopPtReweight = true;  

      bTagSF_path    = iConfig.getParameter<edm::FileInPath>("bTagSF_path");
      bTagEff_path   = iConfig.getParameter<edm::FileInPath>("bTagEff_path");

   }
   PUfile_path        = iConfig.getParameter<edm::FileInPath>("PUfile_path");

   // prefiring weights
   prefweight_token     = consumes< double >(edm::InputTag("prefiringweight:nonPrefiringProb"));

   doPUID = iConfig.getParameter<bool>("doPUID");

   m_rho_token  = consumes<double>(edm::InputTag("fixedGridRhoAll", "", "RECO"));

   fatJetToken_ = consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("fatJetCollection"));
   jetToken_    = consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("jetCollection"));

   edm::Service<TFileService> fs;      
   tree = fs->make<TTree>(  ("tree_"+systematicType).c_str(), ("tree_"+systematicType).c_str());
   TFile *bTagEff_file;
   TFile *jetVetoMap_file;

   if(year == "2018")
   {
      //deepJet_wp_loose = 0.0490;
      deepJet_wp_med   = 0.2783;
      deepjet_wp_tight = 0.7100;
      lumiTag = "Collisions18_UltraLegacy_goldenJSON";
      triggers = {"HLT_PFJet500_v", "HLT_PFHT1050_v"};
   }
   else if(year == "2017")
   {
      //deepJet_wp_loose = 0.0532;
      deepJet_wp_med   = 0.3040;
      deepjet_wp_tight = 0.7476;
      lumiTag = "Collisions17_UltraLegacy_goldenJSON";
      triggers = {"HLT_PFJet500_v", "HLT_PFHT1050_v"};
   }
   else if(year == "2016")
   {
      //deepJet_wp_loose = 0.0480;
      deepJet_wp_med   = 0.2489;
      deepjet_wp_tight = 0.6377;
      lumiTag = "Collisions16_UltraLegacy_goldenJSON";
      triggers  = {"HLT_PFHT900_v", "HLT_PFJet450_v"};
   }
   else if(year == "2015")
   {
      //deepJet_wp_loose = 0.0508;
      deepJet_wp_med   = 0.2598;
      deepjet_wp_tight = 0.6502;
      lumiTag = "Collisions16_UltraLegacy_goldenJSON";
      triggers = {"HLT_PFHT900_v", "HLT_PFJet450_v"};
   }
   else
   {
      std::cout << "Incorrect year: " << year << std::endl;
      return; // return cut
   }


   ///////////////////////////////////////////////////////////////
   //////////////////////// B-tagging stuff //////////////////////
   ///////////////////////////////////////////////////////////////

   if( (runType.find("MC") != std::string::npos) || (runType.find("Suu") != std::string::npos))    //don't want these variables for data
   {

      if(_verbose)std::cout << "Setting up b-tag efficiency maps" << std::endl;
      bTagEff_file = new TFile( bTagEff_path.fullPath().c_str() );   //this path might need to be updated

      truebjet_eff = (TH2F*)bTagEff_file->Get("h_effbJets_tight");   
      truecjet_eff = (TH2F*)bTagEff_file->Get("h_effcJets_tight");  
      lightjet_eff = (TH2F*)bTagEff_file->Get("h_effLightJets_tight"); 

      truebjet_eff_med = (TH2F*)bTagEff_file->Get("h_effbJets_med"); 
      truecjet_eff_med = (TH2F*)bTagEff_file->Get("h_effcJets_med"); 
      lightjet_eff_med = (TH2F*)bTagEff_file->Get("h_effLightJets_med"); 


      bTagEffMap_PtRange = lightjet_eff->GetXaxis()->GetXmax();
      bTagEffMap_Eta_high = lightjet_eff->GetYaxis()->GetXmax();
      bTagEffMap_Eta_low  = lightjet_eff->GetYaxis()->GetXmin();

      bTagEffMap_nPtBins = lightjet_eff->GetNbinsX();
      bTagEffMap_nEtaBins = lightjet_eff->GetNbinsY();

      if(_verbose)std::cout << "Setting up b-tag correctionlib corrector" << std::endl;

      cset = CorrectionSet::from_file(bTagSF_path.fullPath());
      cset_corrector_bc    = cset->at("deepJet_mujets");   //deepJet_comb,    // deepJet_mujets -> what we were using originally, deepJet_ttbar -> what BTV suggested we could use, UPDATE: deepJet_ttbar is not recognized!!!
      if(_verbose)std::cout << "Got bc b-tag correctionlib corrector" << std::endl;
      cset_corrector_light = cset->at("deepJet_incl");   //deepJet_incl
      

      //get corrections from PU file
      PUjson = CorrectionSet::from_file(PUfile_path.fullPath());
      PUjson_year = PUjson->at(lumiTag);
      if(_verbose)std::cout << "Set up pileup correctionlib corrector" << std::endl;
   }

   if(_verbose)std::cout << "Setting up jet veto map files and ranges" << std::endl;


   //////////////////////////////////////
   //////// Jet veto map stuff //////////
   ////////////////////////////////////// 

   jetVetoMap_file = new TFile( jetVetoMapFile.fullPath().c_str() ); 
   jetVetoMap = (TH2F*)jetVetoMap_file->Get(jetVetoMapName.c_str());
   jetVetoMap_XRange = jetVetoMap->GetXaxis()->GetXmax() - jetVetoMap->GetXaxis()->GetXmin();
   jetVetoMap_YRange = jetVetoMap->GetYaxis()->GetXmax() - jetVetoMap->GetYaxis()->GetXmin();

   jetVetoMap_Xmin = jetVetoMap->GetXaxis()->GetXmin();
   jetVetoMap_Ymin = jetVetoMap->GetYaxis()->GetXmin();
   jetVetoMap_nBinsX = jetVetoMap->GetNbinsX();
   jetVetoMap_nBinsY = jetVetoMap->GetNbinsY();


   if(_verbose)std::cout << "Initializing TTree variables." << std::endl;

   ///////////////////////////////////////
   ////////// init tree branches /////////
   ///////////////////////////////////////

   tree->Branch("nfatjets", &nfatjets, "nfatjets/I");

   

   tree->Branch("passesPFJet", &passesPFJet, "passesPFJet/O");
   tree->Branch("passesPFHT", &passesPFHT, "passesPFHT/O");

   tree->Branch("nAK4", &nAK4, "nAK4/I");
   tree->Branch("passesJetPUID", passesJetPUID, "passesJetPUID[nAK4]/O");

   tree->Branch("AK4_DeepJet_disc", AK4_DeepJet_disc, "AK4_DeepJet_disc[nAK4]/D");

   tree->Branch("nfatjet_pre",&nfatjet_pre, "nfatjet_pre/I");
   tree->Branch("totHT",&totHT, "totHT/D");
   
   tree->Branch("jet_pt", jet_pt, "jet_pt[nfatjets]/D");
   tree->Branch("jet_eta", jet_eta, "jet_eta[nfatjets]/D");
   tree->Branch("jet_phi", jet_phi, "jet_phi[nfatjets]/D");
   tree->Branch("AK8_fails_veto_map", AK8_fails_veto_map, "AK8_fails_veto_map[nfatjets]/O");

   tree->Branch("jet_isHEM", jet_isHEM, "jet_isHEM[nfatjets]/O");
   tree->Branch("jet_pre_isHEM", jet_pre_isHEM, "jet_pre_isHEM[nfatjet_pre]/O");

   tree->Branch("lab_nAK4", &lab_nAK4, "lab_nAK4/I");
   tree->Branch("lab_AK4_pt", lab_AK4_pt, "lab_AK4_pt[lab_nAK4]/D");
   tree->Branch("AK4_eta", AK4_eta  , "AK4_eta[lab_nAK4]/D");
   tree->Branch("AK4_phi", AK4_phi  , "AK4_phi[lab_nAK4]/D");
   tree->Branch("AK4_fails_veto_map", AK4_fails_veto_map  , "AK4_fails_veto_map[lab_nAK4]/O");

   tree->Branch("jet_mass", jet_mass, "jet_mass[nfatjets]/D");
   tree->Branch("AK4_mass", AK4_mass, "AK4_mass[nAK4]/D");

   tree->Branch("dijetMassOne", &dijetMassOne, "dijetMassOne/D");
   tree->Branch("dijetMassTwo", &dijetMassTwo, "dijetMassTwo/D");

   tree->Branch("prefiringWeight_nom",  &prefiringWeight_nom, "prefiringWeight_nom/D");

   /////////// (2) Add grid variables here ///////////

   tree->Branch("nHeavyAK8_pt400_M10",  &nHeavyAK8_pt400_M10, "nHeavyAK8_pt400_M10/I");
   tree->Branch("nHeavyAK8_pt400_M20",  &nHeavyAK8_pt400_M20, "nHeavyAK8_pt400_M20/I");
   tree->Branch("nHeavyAK8_pt400_M30",  &nHeavyAK8_pt400_M30, "nHeavyAK8_pt400_M30/I");
   tree->Branch("nHeavyAK8_pt300_M10",  &nHeavyAK8_pt300_M10, "nHeavyAK8_pt300_M10/I");
   tree->Branch("nHeavyAK8_pt300_M20",  &nHeavyAK8_pt300_M20, "nHeavyAK8_pt300_M20/I");
   tree->Branch("nHeavyAK8_pt300_M30",  &nHeavyAK8_pt300_M30, "nHeavyAK8_pt300_M30/I");
   tree->Branch("nHeavyAK8_pt200_M10",  &nHeavyAK8_pt200_M10, "nHeavyAK8_pt200_M10/I");
   tree->Branch("nHeavyAK8_pt200_M20",  &nHeavyAK8_pt200_M20, "nHeavyAK8_pt200_M20/I");
   tree->Branch("nHeavyAK8_pt200_M30",  &nHeavyAK8_pt200_M30, "nHeavyAK8_pt200_M30/I");

   tree->Branch("nAK8_pt200",  &nAK8_pt200, "nAK8_pt200/I");
   tree->Branch("nAK8_pt300",  &nAK8_pt300, "nAK8_pt300/I");
   tree->Branch("nAK8_pt150",  &nAK8_pt150, "nAK8_pt150/I");
   tree->Branch("nAK8_pt150",  &nAK8_pt150, "nAK8_pt150/I");
   tree->Branch("nAK8_pt500",  &nAK8_pt500, "nAK8_pt500/I");

   tree->Branch("nHeavyAK8_pt500_M45",  &nHeavyAK8_pt500_M45, "nHeavyAK8_pt500_M45/I");

   tree->Branch("nAK8_pt200_noCorr",  &nAK8_pt200_noCorr, "nAK8_pt200_noCorr/I");
   tree->Branch("nAK8_pt300_noCorr",  &nAK8_pt300_noCorr, "nAK8_pt300_noCorr/I");
   tree->Branch("nAK8_pt150_noCorr",  &nAK8_pt150_noCorr, "nAK8_pt150_noCorr/I");
   tree->Branch("nAK8_pt500_noCorr",  &nAK8_pt500_noCorr, "nAK8_pt500_noCorr/I");

   tree->Branch("nHeavyAK8_pt500_M45_noCorr",  &nHeavyAK8_pt500_M45_noCorr, "nHeavyAK8_pt500_M45_noCorr/I");



   ///////////////////////////////////////////////

   if( (runType.find("MC") != std::string::npos) || (runType.find("Suu") != std::string::npos))    //don't want these variables for data
   {
      if(_verbose)std::cout << "Setting up MC-specific stuff (genParts tokens, MC-specific TTree vars)" << std::endl;

      puSummaryToken_         = consumes<std::vector<PileupSummaryInfo>>(iConfig.getParameter<edm::InputTag>("pileupCollection"));

      if(doTopPtReweight) tree->Branch("top_pt_weight", &top_pt_weight, "top_pt_weight/D");

      tree->Branch("bTag_eventWeight_T_nom", &bTag_eventWeight_T_nom  , "bTag_eventWeight_T_nom/D");  /// tight WP event weight
      tree->Branch("bTag_eventWeight_M_nom", &bTag_eventWeight_M_nom  , "bTag_eventWeight_M_nom/D");  /// med WP event weight

      if(doPUSF)  tree->Branch("PU_eventWeight_nom", &PU_eventWeight_nom, "PU_eventWeight_nom/D");


   }
   else if(runType == "Data")
   {
         std::cout <<"Running as data ..." << std::endl;
   }

}





// returns bool if jet (or more generally, object) is within the HEM region
bool selectionStudier::isHEM(double jet_eta, double jet_phi)
{
   if(year != "2018") return false; // HEM is only relevant for 2018

   if( (jet_phi >  -1.57)&&( jet_phi < -0.87) )
   {
      if( (jet_eta > -3.0)&&(jet_eta < -1.3))return true;

   }
   return false;
}

// bool corresponding to if AK4 jet passes tight ID
bool selectionStudier::isgoodjet(double eta, double NHF,double NEMF, const size_t NumConst,double CHF,const int CHM, double MUF, double CEMF, double iJet_pt)
{
   if( (abs(eta) > 2.4)) return false; 

   // apply the MEDIUM PU jet id https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJetIDUL
   //if( (!jetPUid) && (iJet_pt < 50.0)) return false; // jet PU ID is only relevant for AK4 jets with pt < 50 GeV

   // apply the tight jet ID
   if ((NHF>0.9) || (NEMF>0.9) || (NumConst<1) || (CHF<0.) || (CHM<0) || (MUF > 0.8) || (CEMF > 0.8)) return false;
   

   return true;

}
// checks AK8 jet (tight) ID and applies some eta conditions
bool selectionStudier::isgoodjet(double eta, double NHF,double NEMF, const size_t NumConst,double CHF,const int CHM, double MUF, double CEMF, int nfatjets)
{
   if ( (nfatjets < 2) && (abs(eta) > 2.4) ) return false;
   else if ( (nfatjets >= 2) && (abs(eta) > 1.4) ) return false;

   if ((NHF>0.9) || (NEMF>0.9) || (NumConst<1) || (CHF<0.) || (CHM<0) || (MUF > 0.8) || (CEMF > 0.8)) return false;
   return true;
}


// checks AK8 jet (tight) ID
bool selectionStudier::isgoodjet(double eta, double NHF,double NEMF, const size_t NumConst,double CHF,const int CHM, double MUF, double CEMF)
{
   if ( abs(eta) > 2.4 ) return false;

   if ((NHF>0.9) || (NEMF>0.9) || (NumConst<1) || (CHF<0.) || (CHM<0) || (MUF > 0.8) || (CEMF > 0.8)) 
   {
      return false;
   }
   else{ return true;}

}


// returns the top pt scale factor as detailed here - https://twiki.cern.ch/twiki/bin/view/CMS/TopPtReweighting#Run_1_strategy_Obsolete
double selectionStudier::top_pt_SF(double top_pt)
{
   if (top_pt > 500.) top_pt = 500.;
   //$SF(p_T)=e^{0.0615-0.0005\cdot p_T}$ for data/POWHEG+Pythia8
   //return 0.103*exp(-0.0118*top_pt) -0.000134*top_pt+ 0.973;
   return exp(0.0615-0.0005*top_pt);  // this is the scale factor based on data aka data-NLO and data-NNLO weights
}



// main analyzer function: pre-select events, recluster superjets, calculate all variables from superjets
void selectionStudier::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   if(_verbose)std::cout << " -----------------Starting Event ----------------- " << std::endl;

   edm::Handle< std::vector<reco::GenParticle> > genPartCollection; // this will be used several times throughout the code

   ////////////////////////////////// 
   ///////// Apply Triggers /////////
   //////////////////////////////////


   edm::Handle<edm::TriggerResults> triggerBits;
   iEvent.getByToken(triggerBits_, triggerBits);

   const edm::TriggerNames &names = iEvent.triggerNames(*triggerBits);
   
   passesPFJet = false;
   passesPFHT  = false;

   for(auto iT = triggers.begin(); iT != triggers.end(); iT++)
   {
      std::string trigname = *iT;
      if(debug)std::cout << "Looking for the " << trigname << " trigger." << std::endl; 

      //bool pass = false;
      for (unsigned int i = 0; i < triggerBits->size(); ++i) 
      {
         const std::string name = names.triggerName(i);
         const bool accept = triggerBits->accept(i);
         if ((name.find(trigname) != std::string::npos) &&(accept))
         {

            //std::cout << "trigname is " << trigname << std::endl;
            if( ( trigname == "HLT_PFJet500_v") || (trigname == "HLT_PFJet450_v") ) passesPFJet = true;
            else if( ( trigname == "HLT_PFHT900_v") || (trigname == "HLT_PFHT1050_v") ) passesPFHT = true;

            if(debug)std::cout << "Found the " << *iT << " trigger." << std::endl;
            //pass =true;
         }
      } 
   }
   

   if(_verbose)std::cout << "In analyze" << std::endl;


   /////////////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   ///////////////////////////////////   _Background MC area_ //////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////


   if ((runType.find("MC") != std::string::npos) || (runType.find("Suu")!=std::string::npos ) )
   {

      if(_verbose)std::cout << "before pileup" << std::endl;


      ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      /////////////////////////////////////////////////////////////////////_pileup_//////////////////////////////////////////////////////////////
      ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      //                                              get the pileup weight for this event
      if(doPUSF)
      {
         edm::Handle<std::vector<PileupSummaryInfo> > PupInfo;
         iEvent.getByToken(puSummaryToken_, PupInfo);

         for (auto const& v : *PupInfo)
         {
            ntrueInt = v.getTrueNumInteractions();
            PU_eventWeight_nom  = PUjson_year->evaluate( {std::real(ntrueInt),"nominal"});

            if ((PU_eventWeight_nom != PU_eventWeight_nom) || (std::isinf(PU_eventWeight_nom)))
            {
               std::cout << "Found bad PUSF: val/ntrueInt = " << PU_eventWeight_nom << "/" << ntrueInt <<std::endl;
            }
         }  
      }

   }  

   edm::Handle<double> rho;
   iEvent.getByToken(m_rho_token, rho);




   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////_prefiring_/////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

   edm::Handle< double > theprefweight;
   iEvent.getByToken(prefweight_token, theprefweight ) ;
   prefiringWeight_nom =(*theprefweight);




   if(_verbose)std::cout << "before AK4 jets" << std::endl;
   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
   ////////////////////////////////////////////////////////////////////_AK4 jets_/////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
   totHT = 0;
   lab_nAK4 = 0;
   nAK4 = 0;
   std::vector<TLorentzVector> leadAK4Jets;

   JME::JetResolution resolution_AK4               = JME::JetResolution::get(iSetup, "AK4PFchs_pt");                          //load JER stuff from global tag
   JME::JetResolutionScaleFactor resolution_sf_AK4 = JME::JetResolutionScaleFactor::get(iSetup, "AK4PFchs");

   edm::Handle<std::vector<pat::Jet>> smallJets;
   iEvent.getByToken(jetToken_, smallJets);


   //// tight b-tag WP variables
   double MC_tagged = 1.0,  MC_notTagged = 1.0, data_tagged = 1.0, data_notTagged = 1.0; //these are for the bTagging SFs

   //// med b-tag WP variables
   double MC_tagged_med = 1.0,  MC_notTagged_med = 1.0, data_tagged_med = 1.0, data_notTagged_med = 1.0; //these are for the bTagging SFs

   // loop over AK4 jets: correct with JECs and JERs, get information for selection, save kinematic information, and calculate b-tagging event weights
   for(auto iJet = smallJets->begin(); iJet != smallJets->end(); iJet++) 
   {

      double AK4_sf_total = 1.0;



      // this code was removed with most recent test!!!x
      //if( (iJet->pt() < 10. ) || (!(iJet->isPFJet())) || ( abs(iJet->eta()) > 2.5 )) continue;   //don't even bother with these jets, lost causes

      ////////////////////////////////////////////////////////////////////////////////////////////////////////////
      //////////   _JET ENERGY RESOLUTION STUFF //////////////////////////////////////////////////////////////////
      ////////////////////////////////////////////////////////////////////////////////////////////////////////////

      if(doJER)
      {
         if ((runType.find("MC") != std::string::npos) || (runType.find("Suu") != std::string::npos) )
         {
            double AK4_JER_corr_factor = 1.0; // this won't be touched for data

            if(_verbose)std::cout << "doing JER" << std::endl;

            double sJER     = -9999.;    //JER scale factor
            double sigmaJER = -9999.;    //this is the "resolution" you get from the scale factors 
            
            JME::JetParameters parameters_1;
            parameters_1.setJetPt(iJet->pt());
            parameters_1.setJetEta(iJet->eta());
            parameters_1.setRho(*rho);
            sigmaJER = resolution_AK4.getResolution(parameters_1);   //pT resolution

            //JME::JetParameters
            JME::JetParameters parameters;
            parameters.setJetPt(iJet->pt());
            parameters.setJetEta(iJet->eta());
            sJER =  resolution_sf_AK4.getScaleFactor(parameters  );  //{{JME::Binning::JetEta, iJet->eta()}});
            

            const reco::GenJet *genJet = iJet->genJet();
            if( genJet)   // try the first technique
            {
               AK4_JER_corr_factor = 1 + (sJER - 1)*(iJet->pt()-genJet->pt())/iJet->pt();
            }
            else   // if no gen jet is matched, try the second technique
            {
               randomNum->SetSeed( abs(static_cast<int>(iJet->phi()*1e4)) );
               double JERrand = randomNum->Gaus(0.0, sigmaJER);
               //double JERrand = 1.0 + sigmaJER;
               AK4_JER_corr_factor = std::max(0., 1 + JERrand*sqrt(std::max(pow(sJER,2)-1,0.)));   //want to make sure this is truncated at 0
            }
            if(_verbose)std::cout << "finished with JER" << std::endl;
            AK4_sf_total*= AK4_JER_corr_factor;

         }
      }


      // create corrected (scaled) jet object that will be used for cuts 
      pat::Jet corrJet(*iJet);

      LorentzVector corrJetP4(AK4_sf_total*iJet->px(),AK4_sf_total*iJet->py(),AK4_sf_total*iJet->pz(),AK4_sf_total*iJet->energy());
      corrJet.setP4(corrJetP4);
      if (_verbose)std::cout << "The PU id bool is " << bool(corrJet.userInt("pileupJetIdUpdated:fullId") & (1 << 1) )<< std::endl;

      //measure event HT
      if((corrJet.pt() > 30.)&&(abs(corrJet.eta()) < 2.5)  )totHT+= abs(corrJet.pt() );

      // apply AK4 jet selection (post JEC and JER)
      bool PUID = true;  // assumed true if not applying this
      if(doPUID)
      {
         PUID = false;
         PUID = bool( (corrJet.userInt("pileupJetIdUpdated:fullId") & (1 << 1)) || (corrJet.pt() > 50.) );
      }

      if (  ( corrJet.pt()  < 30. ) ||  (!(corrJet.isPFJet()))  ||  (!isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(), corrJet.pt() ))   ) continue;

      //if( isHEM(corrJet.eta(), corrJet.phi()))return;  //RETURN CUT - if a jet is in the HEM (=bad) region, don't use this event

      double deepJetScore = corrJet.bDiscriminator("pfDeepFlavourJetTags:probb") + corrJet.bDiscriminator("pfDeepFlavourJetTags:probbb")+ corrJet.bDiscriminator("pfDeepFlavourJetTags:problepb");

      if(_verbose)std::cout << "the year is " << year << " with working point value of " << deepjet_wp_tight << ". The hadronFlavour is " << corrJet.hadronFlavour() <<  " and deepjet score " << deepJetScore<< std::endl;
      


      //////////////////////////////////////////////////////////////////////////////////////////////////////////////
      ////////////////////////////////////// b tagging event weight stuff //////////////////////////////////////////
      //////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if(doBtagSF)
      {
         // calculate the b-tag scale factor for the event using the efficiency maps that were loaded in the constructor and correctionlib
         if ( ( runType.find("MC") != std::string::npos  ) || (runType.find("Suu")!= std::string::npos ) )    //only run this on MC (we won't have the hadron flavor stuff for data )
         {

            //these are the bins of the eff histogram you need to draw from
            // histogram size:  63, 0, 6000, 18, -2.4, 2.4   

            // should import the histogram size here so this dosn't have to be manually changed
            int xbin = (int)(corrJet.pt()*bTagEffMap_nPtBins/bTagEffMap_PtRange) + 1;
            int ybin = (int)((corrJet.eta()-bTagEffMap_Eta_low)*bTagEffMap_nEtaBins/(bTagEffMap_Eta_high-bTagEffMap_Eta_low)) +1;

            if(debug) std::cout << "bTagEffMap_nPtBins/bTagEffMap_PtRange/bTagEffMap_Eta_low/bTagEffMap_nEtaBins/bTagEffMap_Eta_high:" <<bTagEffMap_nPtBins << "/"  <<bTagEffMap_PtRange << "/" <<bTagEffMap_Eta_low << "/" <<bTagEffMap_nEtaBins << "/" <<bTagEffMap_Eta_high << std::endl;
            double SF;
            double SF_med;
            double bTag_eff_value, bTag_eff_value_med;

            if(corrJet.hadronFlavour() == 0)   //light jets
            {

               bTag_eff_value = lightjet_eff->GetBinContent(xbin,ybin);
               bTag_eff_value_med = lightjet_eff_med->GetBinContent(xbin,ybin);

               SF = cset_corrector_light->evaluate({"central", "T", 0, std::abs(corrJet.eta()), corrJet.pt()}); /// tight WP SF
               SF_med = cset_corrector_light->evaluate({"central", "M", 0, std::abs(corrJet.eta()), corrJet.pt()});

               //////// MED WP SCALE FACTOR ////////
               if( deepJetScore > deepJet_wp_med)
               {
                  // med WP
                  MC_tagged_med *= bTag_eff_value_med;
                  data_tagged_med *= SF_med*bTag_eff_value_med;

                  if(_verbose)std::cout << "tagged light jet: MC_tagged/data_tagged: " << bTag_eff_value << ":" << SF*bTag_eff_value << std::endl;
               }
               else
               {
                  // med WP
                  MC_notTagged_med *= (1 - bTag_eff_value_med);
                  data_notTagged_med *= (1 - SF_med*bTag_eff_value_med);
               }

               //////// TIGHT WP SCALE FACTOR ///////
               if(_verbose)std::cout << "Scale factor is " << SF << std::endl;
               if(deepJetScore > deepjet_wp_tight)
               {

                  // tight WP
                  MC_tagged *= bTag_eff_value;
                  data_tagged *= SF*bTag_eff_value;
               }

               else
               {
                  // tight WP
                  MC_notTagged *= (1 - bTag_eff_value);
                  data_notTagged *= (1 - SF*bTag_eff_value);

                  if(_verbose)std::cout << "untagged light jet: MC_notTagged/data_notTagged: " << (1- bTag_eff_value) << ":" << (1- SF*bTag_eff_value) << std::endl;
               }
            }
            else if(corrJet.hadronFlavour() == 4) //charm jets
            {
               bTag_eff_value = truecjet_eff->GetBinContent(xbin,ybin);
               bTag_eff_value_med = truecjet_eff_med->GetBinContent(xbin,ybin);

               SF = cset_corrector_bc->evaluate(   {"central", "T", 4, std::abs(corrJet.eta()), corrJet.pt()});
               SF_med = cset_corrector_bc->evaluate(   {"central", "M", 4, std::abs(corrJet.eta()), corrJet.pt()});

               if(_verbose)std::cout << "Scale factor is " << SF << std::endl;

               //////// MED WP SCALE FACTOR ////////
               if(deepJetScore > deepJet_wp_med)
               {
                  // med WP
                  MC_tagged_med  *= bTag_eff_value_med;
                  data_tagged_med *= SF_med*bTag_eff_value_med;
               }
               else
               {
                  // med WP
                  MC_notTagged_med *= (1 - bTag_eff_value_med);
                  data_notTagged_med *= (1 - SF_med*bTag_eff_value_med);

               }

               //////// TIGHT WP SCALE FACTOR ////////
               if(deepJetScore > deepjet_wp_tight)
               {
                  // tight WP
                  MC_tagged  *= bTag_eff_value;
                  data_tagged *= SF*bTag_eff_value;

                  if(_verbose)std::cout << "tagged c jet: MC_tagged/data_tagged: " << bTag_eff_value << ":" << SF*bTag_eff_value << std::endl;
               }
               else
               {
                  // tight WP
                  MC_notTagged *= (1 - bTag_eff_value);
                  data_notTagged *= (1 - SF*bTag_eff_value);

                  if(_verbose)std::cout << "untagged c jet: MC_notTagged/data_notTagged: " << (1- bTag_eff_value) << ":" << (1- SF*bTag_eff_value) << std::endl;
               }
            }
            else if(corrJet.hadronFlavour() == 5) // b jets
            {
               bTag_eff_value = truebjet_eff->GetBinContent(xbin,ybin);
               bTag_eff_value_med = truebjet_eff_med->GetBinContent(xbin,ybin);

               SF             = cset_corrector_bc->evaluate(   {"central", "T", 5, std::abs(corrJet.eta()), corrJet.pt()}); // tight WP
               SF_med         = cset_corrector_bc->evaluate(   {"central", "M", 5, std::abs(corrJet.eta()), corrJet.pt()}); // med WP

               if(_verbose)std::cout << "Scale factor is " << SF << std::endl;

               //////// MED WP SCALE FACTOR ////////
               if(deepJetScore > deepJet_wp_med)
               {
                  // med WP
                  MC_tagged_med  *= bTag_eff_value_med;
                  data_tagged_med *= SF_med*bTag_eff_value_med;
               }
               else
               {
                  // med WP
                  MC_notTagged_med *= (1 - bTag_eff_value_med);
                  data_notTagged_med *= (1 - SF_med*bTag_eff_value_med);
               }

               //////// TIGHT WP SCALE FACTOR ////////
               if(deepJetScore > deepjet_wp_tight)
               {
                  // tight WP
                  MC_tagged  *= bTag_eff_value;
                  data_tagged *= SF*bTag_eff_value;

                  if(_verbose)std::cout << "tagged b jet: MC_tagged/data_tagged: " << bTag_eff_value << ":" << SF*bTag_eff_value << std::endl;
               }
               else
               {  
                  // tight WP
                  MC_notTagged *= (1 - bTag_eff_value);
                  data_notTagged *= (1 - SF*bTag_eff_value);

                  if(_verbose)std::cout << "untagged b jet: MC_notTagged/data_notTagged: " << (1- bTag_eff_value) << ":" << (1- SF*bTag_eff_value) << std::endl;
               }
            }
            else
            {
               std::cout << "ERROR: invalid AK4 hadron flavour. " << std::endl;
            }
            double epsilon = 1e-12;
            if ( (abs(MC_tagged)<epsilon )||(abs(MC_tagged)<epsilon )||(abs(MC_tagged)<epsilon )||(abs(MC_tagged)<epsilon ))
            {
                  if(_verbose)std::cout << "bTag_eff_value/SF/MC_tagged/MC_notTagged/data_tagged/data_notTagged: " << bTag_eff_value<< " / " << SF<< " / " << MC_tagged<< " / " << MC_notTagged << " / " <<data_tagged << " / " << data_notTagged << std::endl;
            }
         }
      }

      int vetoMap_xbin = (int)((corrJet.eta() - jetVetoMap_Xmin)*jetVetoMap_nBinsX/jetVetoMap_XRange ) +1;
      int vetoMap_ybin = (int)((corrJet.phi() - jetVetoMap_Ymin)*jetVetoMap_nBinsY/jetVetoMap_YRange ) +1;       // pt(b) = b*(range / # bins) + b0 -> (pt(b) - b0)*(# bins / range)
      AK4_fails_veto_map[nAK4] = false;
      if(jetVetoMap->GetBinContent(vetoMap_xbin,vetoMap_ybin) > 0)
      {
         AK4_fails_veto_map[nAK4] = true;
      }

      lab_AK4_pt[nAK4] = corrJet.pt();
      AK4_mass[nAK4] = corrJet.mass();
      AK4_eta[nAK4] = corrJet.eta();
      AK4_phi[nAK4] = corrJet.phi();
      if(doPUID) passesJetPUID[nAK4] = PUID;
      AK4_DeepJet_disc[nAK4] = deepJetScore;


      if(nAK4 < 4)
      {
         leadAK4Jets.push_back(TLorentzVector(corrJet.px(),corrJet.py(),corrJet.pz(),corrJet.energy()));
      }


      nAK4++;

   }


   //if(nAK4 <4)return;   // RETURN cut




   ///////////////////// calculate b tag event weights //////////////////////
   if(doBtagSF)
   {
      // tight WP
      bTag_eventWeight_T_nom =  (data_tagged*data_notTagged) / (MC_tagged*MC_notTagged);
      // med WP
      bTag_eventWeight_M_nom =  (data_tagged_med*data_notTagged_med) / (MC_tagged_med*MC_notTagged_med);

      if ((bTag_eventWeight_T_nom != bTag_eventWeight_T_nom) || (std::isinf(bTag_eventWeight_T_nom)) || (bTag_eventWeight_T_nom < 1e-9))
      {
         //std::cout << "BAD BTAG SF: " << bTag_eventWeight_T_nom << std::endl;
         if(_verbose)std::cout << "data_tagged_up/data_notTagged_up/MC_tagged/MC_notTagged: " <<data_tagged << "/" <<data_notTagged << "/" << MC_notTagged<< "/" << MC_notTagged<<  std::endl;
      } 
   }

   lab_nAK4 = nAK4;


   /////////////////////////////////
   // (3) Apply loose HT selection criteria  (= looser than grid points)
   /////////////////////////////////


    if( totHT < 1400) return; // normal HT cut



   ///////////////////////////////////
   ////// Calculate dijet masses /////
   ///////////////////////////////////



   /*
   // calculate the candidate dijet delta R values
   double minDeltaRDisc12 = sqrt( pow(leadAK4Jets[0].DeltaR(leadAK4Jets[1]),2) + pow(leadAK4Jets[2].DeltaR(leadAK4Jets[3]),2));    // dijet one always has j1 in it
   double minDeltaRDisc13 = sqrt( pow(leadAK4Jets[0].DeltaR(leadAK4Jets[2]),2) + pow(leadAK4Jets[1].DeltaR(leadAK4Jets[3]),2));
   double minDeltaRDisc14 = sqrt( pow(leadAK4Jets[0].DeltaR(leadAK4Jets[3]),2) + pow(leadAK4Jets[1].DeltaR(leadAK4Jets[2]),2));

   if (  abs(min(minDeltaRDisc12, min(minDeltaRDisc13,minDeltaRDisc14)) -minDeltaRDisc12)<1e-8 ) 
   {
      //set dijet masses
      dijetMassOne = (leadAK4Jets[0] +leadAK4Jets[1]).M();
      dijetMassTwo = (leadAK4Jets[2] +leadAK4Jets[3]).M();
   }
   else if (  abs(min(minDeltaRDisc12, min(minDeltaRDisc13,minDeltaRDisc14)) -minDeltaRDisc13)<1e-8 ) 
   {
      // set dijet masses
      dijetMassOne = (leadAK4Jets[0] +leadAK4Jets[2]).M();
      dijetMassTwo = (leadAK4Jets[1] +leadAK4Jets[3]).M();
   }
   else if (  abs(min(minDeltaRDisc12, min(minDeltaRDisc13,minDeltaRDisc14)) -minDeltaRDisc14)<1e-8 ) 
   {
      //set dijet masses
      dijetMassOne = (leadAK4Jets[0] +leadAK4Jets[3]).M();
      dijetMassTwo = (leadAK4Jets[1] +leadAK4Jets[2]).M();
   }

   */

   if(_verbose)std::cout << "before AK8 jets" << std::endl;

   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
   ////////////////////////////////////////////////////////////_AK8 Jets_/////////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

   edm::Handle<std::vector<pat::Jet> > fatJets;
   iEvent.getByToken(fatJetToken_, fatJets);

   JME::JetResolution resolution = JME::JetResolution::get(iSetup, "AK8PF_pt");                          //load JER stuff from global tag
   JME::JetResolutionScaleFactor resolution_sf = JME::JetResolutionScaleFactor::get(iSetup, "AK8PF");

   nfatjets = 0;
   nfatjet_pre = 0;


   /////////// (4) set grid variable variable counters to zero (ex. nAK8_Et250 = 0;) ///////////

   nHeavyAK8_pt400_M10 = 0; nHeavyAK8_pt400_M20 = 0; nHeavyAK8_pt400_M30 = 0;
   nHeavyAK8_pt300_M10 = 0; nHeavyAK8_pt300_M20 = 0; nHeavyAK8_pt300_M30 = 0; 
   nHeavyAK8_pt200_M10 = 0; nHeavyAK8_pt200_M20 = 0; nHeavyAK8_pt200_M30 = 0; 


   nAK8_pt200 = 0 ; nAK8_pt300 = 0; nAK8_pt150 = 0; nHeavyAK8_pt500_M45 = 0, nAK8_pt500 = 0;
   nAK8_pt200_noCorr = 0; nAK8_pt300_noCorr = 0; nAK8_pt150_noCorr = 0; nHeavyAK8_pt500_M45_noCorr = 0, nAK8_pt500_noCorr = 0;

   /////////////////////////////////////////////////////////////////////////////////////////////


   std::vector<TLorentzVector> leadAK8Jets;


   // loop over AK8 jets, save information for event selection, grab particles to create superjets
   for(auto iJet = fatJets->begin(); iJet != fatJets->end(); iJet++)    
   {

      // this was removed for the most recent update!!
      //if( (sqrt(pow(iJet->mass(),2)+pow(iJet->pt(),2)) < 25.) || (!(iJet->isPFJet())) || ( abs(iJet->eta()) > 2.4 )) continue;   //don't even bother with these jets

      int vetoMap_xbin = (int)((iJet->eta() - jetVetoMap_Xmin)*jetVetoMap_nBinsX/jetVetoMap_XRange ) +1;
      int vetoMap_ybin = (int)((iJet->phi() - jetVetoMap_Ymin)*jetVetoMap_nBinsY/jetVetoMap_YRange ) +1;       // pt(b) = b*(range / # bins) + b0 -> (pt(b) - b0)*(# bins / range)
      bool AK8_fails_veto_map_unCorr = false;
      if(jetVetoMap->GetBinContent(vetoMap_xbin,vetoMap_ybin) > 0.) AK8_fails_veto_map_unCorr = true;


      // cross-check stuff 
      if ( (iJet->isPFJet() ) && ( abs(iJet->eta()) < 2.4 ) && (    isgoodjet(iJet->eta(),iJet->neutralHadronEnergyFraction(), iJet->neutralEmEnergyFraction(),iJet->numberOfDaughters(),iJet->chargedHadronEnergyFraction(),iJet->chargedMultiplicity(),iJet->muonEnergyFraction(),iJet->chargedEmEnergyFraction() ) ) )
      {
         if(!isHEM(iJet->eta(),iJet->phi()) && ( !AK8_fails_veto_map_unCorr ))
         {
            if( iJet->pt() > 150.) nAK8_pt150_noCorr++;
            if( (iJet->pt() > 200.) ) nAK8_pt200_noCorr++;
            if( (iJet->pt() > 300.) ) nAK8_pt300_noCorr++;
            if( (iJet->pt() > 500.) ) nAK8_pt500_noCorr++;
            if( (iJet->pt() > 500.)  && (iJet->userFloat("ak8PFJetsPuppiSoftDropMass") > 45.)  ) nHeavyAK8_pt500_M45_noCorr++;
         }

      }

      double AK8_sf_total = 1.0;     // this scales jet/particle 4-vectors, compounds all scale factors

      ////////////////////////////////////////////////////////////////////////////////////////////////////////////
      //////////   _JET ENERGY RESOLUTION STUFF //////////////////////////////////////////////////////////////////
      ////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if(doJER)
      {
         double AK8_JER_corr_factor = 1.0; // this won't be touched for data
         
         if( (runType.find("MC") != std::string::npos)|| (runType.find("Suu")!= std::string::npos ) ) //if((runType == "SigMC") || (runType == "QCDMC") || (runType == "TTbarMC") ) 
         {
            if(_verbose)std::cout << "doing JER" << std::endl;

            double sJER     = -9999.;    //JER scale factor
            double sigmaJER = -9999.;    //this is the "resolution" you get from the scale factors 
            
            //these are for getting the JER scale factors
            JME::JetParameters parameters_1;
            parameters_1.setJetPt(iJet->pt());
            parameters_1.setJetEta(iJet->eta());
            parameters_1.setRho(*rho);
            sigmaJER = resolution.getResolution(parameters_1);   //pT resolution

            //JME::JetParameters
            JME::JetParameters parameters;
            parameters.setJetPt(iJet->pt());
            parameters.setJetEta(iJet->eta());
            sJER =  resolution_sf.getScaleFactor(parameters  );  //{{JME::Binning::JetEta, iJet->eta()}});

            const reco::GenJet *genJet = iJet->genJet();
            if( genJet)   // try the first technique
            {
               AK8_JER_corr_factor = 1 + (sJER - 1)*(iJet->pt()-genJet->pt())/iJet->pt();
            }
            else   // if no gen jet is matched, try the second technique
            {
               randomNum->SetSeed( abs(static_cast<int>(iJet->phi()*1e4)) );
               double JERrand = randomNum->Gaus(0.0, sigmaJER);
               //double JERrand = 1.0 + sigmaJER;
               AK8_JER_corr_factor = max(0., 1 + JERrand*sqrt(max(pow(sJER,2)-1,0.)));   //want to make sure this is truncated at 0
            }

            if(_verbose)std::cout << "finished with JER" << std::endl;
         }
         AK8_sf_total*= AK8_JER_corr_factor;
      }

      /////////////////////////////////////////////////////////////////////////////////////////////////////////////
      /////////////////////////////////////////////////////////////////////////////////////////////////////////////

      // create corrected (scaled) jet object that will be used for cuts 
      pat::Jet corrJet(*iJet);
      LorentzVector corrJetP4(AK8_sf_total*iJet->px(),AK8_sf_total*iJet->py(),AK8_sf_total*iJet->pz(),AK8_sf_total*iJet->energy());
      corrJet.setP4(corrJetP4);



      vetoMap_xbin = (int)((corrJet.eta() - jetVetoMap_Xmin)*jetVetoMap_nBinsX/jetVetoMap_XRange ) +1;
      vetoMap_ybin = (int)((corrJet.phi() - jetVetoMap_Ymin)*jetVetoMap_nBinsY/jetVetoMap_YRange ) +1;       // pt(b) = b*(range / # bins) + b0 -> (pt(b) - b0)*(# bins / range)
      bool AK8_fails_veto_map_ = false;
      if(jetVetoMap->GetBinContent(vetoMap_xbin,vetoMap_ybin) > 0.) AK8_fails_veto_map_ = true;


      if ( (corrJet.isPFJet() ) && ( abs(corrJet.eta()) < 2.4 ) && (    isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction() ) ) )
      {

         if(!isHEM(corrJet.eta(),corrJet.phi()) && ( !AK8_fails_veto_map_ ))
         {
            if( corrJet.pt() > 150.) nAK8_pt150++;
            if( (corrJet.pt() > 200.) ) nAK8_pt200++;
            if( (corrJet.pt() > 300.) ) nAK8_pt300++;
            if( (corrJet.pt() > 500.) ) nAK8_pt500++;
            if( (corrJet.pt() > 500.)  && (corrJet.userFloat("ak8PFJetsPuppiSoftDropMass") > 45.)  ) nHeavyAK8_pt500_M45++;
         }
      }


      if(_verbose)  std::cout << "nominal p4: " << iJet->px()<< "," <<iJet->py() << "," << iJet->pz()<< "," << iJet->energy()<< std::endl;
      if(_verbose)  std::cout << "corrected p4: " << corrJet.px()<< "," <<corrJet.py() << "," << corrJet.pz()<< "," << corrJet.energy()<< std::endl;

      if((corrJet.pt() > 500.) && ((corrJet.isPFJet())) && (isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(),nfatjets) ) && (corrJet.userFloat("ak8PFJetsPuppiSoftDropMass") > 45.)) 
      {
         if(isHEM(corrJet.eta(),corrJet.phi())) jet_pre_isHEM[nfatjet_pre] = true;
         else{ jet_pre_isHEM[nfatjet_pre] = false;}

         nfatjet_pre++;
      }

      /////////// (5) calculate grid variables here ///////////

 
      if((corrJet.pt() > 400.) && ((corrJet.isPFJet())) && (isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(),nfatjets) ) && (corrJet.userFloat("ak8PFJetsPuppiSoftDropMass") > 10.) && (!isHEM(corrJet.eta(),corrJet.phi()))) nHeavyAK8_pt400_M10++;
      if((corrJet.pt() > 400.) && ((corrJet.isPFJet())) && (isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(),nfatjets) ) && (corrJet.userFloat("ak8PFJetsPuppiSoftDropMass") > 20.) && (!isHEM(corrJet.eta(),corrJet.phi()))) nHeavyAK8_pt400_M20++;
      if((corrJet.pt() > 400.) && ((corrJet.isPFJet())) && (isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(),nfatjets) ) && (corrJet.userFloat("ak8PFJetsPuppiSoftDropMass") > 30.) && (!isHEM(corrJet.eta(),corrJet.phi()))) nHeavyAK8_pt400_M30++;

      if((corrJet.pt() > 300.) && ((corrJet.isPFJet())) && (isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(),nfatjets) ) && (corrJet.userFloat("ak8PFJetsPuppiSoftDropMass") > 10.) && (!isHEM(corrJet.eta(),corrJet.phi()))) nHeavyAK8_pt300_M10++;
      if((corrJet.pt() > 300.) && ((corrJet.isPFJet())) && (isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(),nfatjets) ) && (corrJet.userFloat("ak8PFJetsPuppiSoftDropMass") > 20.) && (!isHEM(corrJet.eta(),corrJet.phi()))) nHeavyAK8_pt300_M20++;
      if((corrJet.pt() > 300.) && ((corrJet.isPFJet())) && (isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(),nfatjets) ) && (corrJet.userFloat("ak8PFJetsPuppiSoftDropMass") > 30.) && (!isHEM(corrJet.eta(),corrJet.phi()))) nHeavyAK8_pt300_M30++;

      if((corrJet.pt() > 200.) && ((corrJet.isPFJet())) && (isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(),nfatjets) ) && (corrJet.userFloat("ak8PFJetsPuppiSoftDropMass") > 10.) && (!isHEM(corrJet.eta(),corrJet.phi()))) nHeavyAK8_pt200_M10++;
      if((corrJet.pt() > 200.) && ((corrJet.isPFJet())) && (isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(),nfatjets) ) && (corrJet.userFloat("ak8PFJetsPuppiSoftDropMass") > 20.) && (!isHEM(corrJet.eta(),corrJet.phi()))) nHeavyAK8_pt200_M20++;
      if((corrJet.pt() > 200.) && ((corrJet.isPFJet())) && (isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(),nfatjets) ) && (corrJet.userFloat("ak8PFJetsPuppiSoftDropMass") > 30.) && (!isHEM(corrJet.eta(),corrJet.phi()))) nHeavyAK8_pt200_M30++;


      ///////////////////////////////////////////////////////

      if((sqrt(pow(corrJet.mass(),2)+pow(corrJet.pt(),2)) < 200.) || (!(corrJet.isPFJet())) || (!isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(),nfatjets )) || (corrJet.mass()< 0.)) continue; //userFloat("ak8PFJetsPuppiSoftDropMass")
      

      ////// HEM and jet veto map stuff //////

      AK8_fails_veto_map[nfatjets] = AK8_fails_veto_map_;

      if(isHEM(corrJet.eta(),corrJet.phi())) jet_isHEM[nfatjets] = true;
      else{jet_isHEM[nfatjets] = false;}

      ////////////////////////////////////////

      if(nfatjets < 4)leadAK8Jets.push_back(TLorentzVector(corrJet.px(),corrJet.py(),corrJet.pz(),corrJet.energy()));

      AK8_fails_veto_map[nfatjets] = AK8_fails_veto_map_;

      if(jetVetoMap->GetBinContent(vetoMap_xbin,vetoMap_ybin) > 0.) AK8_fails_veto_map[nfatjets] = true;

      jet_pt[nfatjets] = corrJet.pt();
      jet_phi[nfatjets] = iJet->phi();  
      jet_eta[nfatjets] = corrJet.eta();
      jet_mass[nfatjets] = corrJet.mass();

      nfatjets++;
   }

   diAK8Jet_mass[0] = 0; diAK8Jet_mass[1] = 0;
   fourAK8JetMass = 0;
   if(nfatjets >3)
   {

      fourAK8JetMass = (leadAK8Jets[0] + leadAK8Jets[1] +  leadAK8Jets[2] + leadAK8Jets[3]).M();
      double minDeltaRDisc12_AK8 = sqrt( pow(leadAK8Jets[0].DeltaR(leadAK8Jets[1]),2) + pow(leadAK8Jets[2].DeltaR(leadAK8Jets[3]),2));    // dijet one always has j1 in it
      double minDeltaRDisc13_AK8 = sqrt( pow(leadAK8Jets[0].DeltaR(leadAK8Jets[2]),2) + pow(leadAK8Jets[1].DeltaR(leadAK8Jets[3]),2));
      double minDeltaRDisc14_AK8 = sqrt( pow(leadAK8Jets[0].DeltaR(leadAK8Jets[3]),2) + pow(leadAK8Jets[1].DeltaR(leadAK8Jets[2]),2));

      if (  abs(min(minDeltaRDisc12_AK8, min(minDeltaRDisc13_AK8,minDeltaRDisc14_AK8)) - minDeltaRDisc12_AK8)<1e-8 ) 
      {
         //set dijet masses
         diAK8Jet_mass[0] = (leadAK8Jets[0] +leadAK8Jets[1]).M();
         diAK8Jet_mass[1] = (leadAK8Jets[2] +leadAK8Jets[3]).M();
      }
      else if (  abs(min(minDeltaRDisc12_AK8, min(minDeltaRDisc13_AK8,minDeltaRDisc14_AK8)) -minDeltaRDisc13_AK8)<1e-8 ) 
      {
         // set dijet masses
         diAK8Jet_mass[0] = (leadAK8Jets[0] +leadAK8Jets[2]).M();
         diAK8Jet_mass[1] = (leadAK8Jets[1] +leadAK8Jets[3]).M();
      }
      else if (  abs(min(minDeltaRDisc12_AK8, min(minDeltaRDisc13_AK8,minDeltaRDisc14_AK8)) -minDeltaRDisc14_AK8)<1e-8 ) 
      {
         //set dijet masses
         diAK8Jet_mass[0] = (leadAK8Jets[0] +leadAK8Jets[3]).M();
         diAK8Jet_mass[1] = (leadAK8Jets[1] +leadAK8Jets[2]).M();
      }
   }


   // could use uncorrected variables for this selection? 
   if ((nAK8_pt150_noCorr < 2) || ((nHeavyAK8_pt400_M30 < 1  )  ) )return; // RETURN cut     ///   ((dijetMassOne < 800.) || (dijetMassTwo < 800.) // normal selection







   tree->Fill();

}   
DEFINE_FWK_MODULE(selectionStudier);
//_bottom_
