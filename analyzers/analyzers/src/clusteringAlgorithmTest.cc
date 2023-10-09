////////////////////////////HELP////////////////////////////////
//////////////Uses new clustering algorithm to capture heavy resonance jet substructure//////////////
////////////////Last updated Feb 23 2021 ////////////////////////////////////////////////////////////

//_top_

// system include files
#include <fastjet/JetDefinition.hh>
//#include <fastjet/GhostedAreaSpec.hh>
#include <fastjet/PseudoJet.hh>
#include <fastjet/tools/Filter.hh>
#include <fastjet/ClusterSequence.hh>
#include <fastjet/ActiveAreaSpec.hh>
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

#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "PhysicsTools/CandUtils/interface/EventShapeVariables.h"
//#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
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
#include "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/sortJets.h"
#include "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/BESTtoolbox.h"
#include "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/CacheHandler.h"
//#include "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_29/src/analyzers/analyzers/src/CacheHandler.cc"
#include "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/BESTEvaluation.h"
using namespace reco;
using namespace correction;

typedef math::XYZTLorentzVector LorentzVector;
typedef math::XYZVector Vector;

using correction::CorrectionSet;

class clusteringAnalyzerTest : public edm::EDAnalyzer 
{
public:
   explicit clusteringAnalyzerTest(const edm::ParameterSet&);
private:
   virtual void analyze(const edm::Event&, const edm::EventSetup&);
   double calc_mass(std::vector<TLorentzVector> candSuperJet);
   double calc_mag(double px,double py, double pz);
   double calcMPP(TLorentzVector superJetTLV ); 
   bool isMatchedtoSJ(std::vector<TLorentzVector> superJetTLVs, TLorentzVector candJet); 
   bool fillSJVars(std::map<std::string, float> &treeVars, std::vector<fastjet::PseudoJet> iSJ, int nSuperJets);
   bool isgoodjet(const float eta, const float NHF,const float NEMF, const size_t NumConst,const float CHF,const int CHM, const float MUF, const float CEMF);
   bool isgoodjet(const float eta, const float NHF,const float NEMF, const size_t NumConst,const float CHF,const int CHM, const float MUF, const float CEMF, int nfatjets);

   const reco::Candidate* parse_chain(const reco::Candidate* cand);
   
   edm::EDGetTokenT<std::vector<pat::Jet>> fatJetToken_;
   edm::EDGetTokenT<std::vector<reco::GenParticle>> genPartToken_; 
   edm::EDGetTokenT<std::vector<pat::Jet>> jetToken_;
   edm::EDGetTokenT<std::vector<PileupSummaryInfo> > puSummaryToken_;


   edm::EDGetTokenT<double> m_rho_token;

   TTree * tree;
   BESTEvaluation* BEST_;
   const CacheHandler* cache_;
   edm::FileInPath path_;
   edm::FileInPath bTagSF_path;
   edm::FileInPath bTagEff_path;
   edm::FileInPath PUfile_path;
   std::string runType;
   std::string systematicType;
   std::string year;
   std::string lumiTag;
   int eventnum = 0;
   int nAK4 = 0;
   int nfatjets = 0;
   int raw_nfatjets;
   int tot_nAK4_50 =0,tot_nAK4_70 = 0;
   int tot_mpp_AK4 = 0;
   std::map<std::string, float> BESTmap;

   int SJ_nAK4_50[100],SJ_nAK4_70[100],SJ_nAK4_100[100],SJ_nAK4_125[100],SJ_nAK4_150[100],SJ_nAK4_200[100],SJ_nAK4_300[100],SJ_nAK4_400[100],SJ_nAK4_600[100],SJ_nAK4_800[100],SJ_nAK4_1000[100];
   double jet_pt[100], jet_eta[100], jet_mass[100], jet_dr[100], raw_jet_mass[100],raw_jet_pt[100],raw_jet_phi[100];
   double jet_beta[100], beta_T[100], AK4_mass_20[100],AK4_mass_30[100],AK4_mass_50[100],AK4_mass_70[100],AK4_mass_100[100],AK4_mass_150[100];
   double SJ_mass_50[100], SJ_mass_70[100],SJ_mass_100[100],superJet_mass[100],SJ_AK4_50_mass[100],SJ_AK4_70_mass[100];
   double SJ_mass_125[100], SJ_mass_150[100], SJ_mass_200[100],SJ_mass_300[100],SJ_mass_400[100],SJ_mass_600[100],SJ_mass_800[100],SJ_mass_1000[100];   
   double tot_jet_mass,decay_inv_mass, chi_inv_mass;
   double AK4_mass[100], AK4_E[500], leadAK8_mass[100];
   double event_reco_pt;
   double diSuperJet_mass,diSuperJet_mass_100;
   double chi_dr,topPart_dr,higgs_dr,SuuW_dr,HiggsTop_dr,SuuWb_dr;
   double topAK8_dr, WSuuAK8_dr,bSuuAK8_dr,higgsAK8_dr,topWAK8_dr,topbAK8_dr;
   double topAK4_dr, WSuuAK4_dr,bSuuAK4_dr,higgsAK4_dr,topWAK4_dr,topbAK4_dr;
   double recoCOM_eta,recoCOM_phi;
   double eventBetaCOM   = -999.;
   int nGoodEvents = 0;
   double totHT = 0;
   double dijetMassOne, dijetMassTwo;
   int nfatjet_pre = 0;
   int nSuperJets = 0;
   int nhadevents = 0;
   double AK4_bdisc[100], AK4_DeepJet_disc[100];
   int nBadClusters =0;
   int correctlySortedChi1, correctlySortedChi2;
   int jet_ndaughters[100], jet_nAK4[100],jet_nAK4_20[100],jet_nAK4_30[100],jet_nAK4_50[100],jet_nAK4_70[100],jet_nAK4_100[100],jet_nAK4_150[100];
   double totMET;
   int lab_nAK4 = 0;
   double lab_AK4_pt[100];
   double daughter_mass_comb[100];
   double btag_score_uncut[100];
   int nAK4_uncut = 0;
   int nGenBJets_AK4[100],AK4_hadronFlavour[100], AK4_partonFlavour[100];
   double genSuperJetMass[100];
   int nCategories = 4;
   double AK4_ptot[100], AK4_eta[100], AK4_phi[100];
   int SJ1_decision,SJ2_decision;
   double SJ1_BEST_scores[4],SJ2_BEST_scores[4];
   double bTag_eventWeight_nom, bTag_eventWeight_up, bTag_eventWeight_down;
   bool _htWb,_htZt,_ZtWb,_WbWb,_htht,_ZtZt;
   //BES variables
   double AK4_m1[2], AK4_m2[2],AK4_m3[2],AK4_m4[2], AK41_E_tree[2],AK42_E_tree[2],AK43_E_tree[2],AK44_E_tree[2], AK4_m12[2],AK4_m13[2],AK4_m14[2],AK4_m23[2],AK4_m24[2],AK4_m34[2];
   double AK4_m123[2],AK4_m124[2],AK4_m134[2],AK4_m234[2], AK4_m1234[2],AK4_theta12[2],AK4_theta13[2],AK4_theta14[2],AK4_theta23[2],AK4_theta24[2],AK4_theta34[2];
   int AK41_ndaughters[2], AK41_nsubjets[2];
   double AK41_thrust[2],AK41_sphericity[2],AK41_asymmetry[2],AK41_isotropy[2],AK41_aplanarity[2],AK41_FW1[2],AK41_FW2[2],AK41_FW3[2],AK41_FW4[2];
   int AK42_ndaughters[2], AK42_nsubjets[2]; 
   double AK42_thrust[2],AK42_sphericity[2],AK42_asymmetry[2],AK42_isotropy[2],AK42_aplanarity[2],AK42_FW1[2],AK42_FW2[2],AK42_FW3[2],AK42_FW4[2];
   int AK43_ndaughters[2], AK43_nsubjets[2]; 
   double AK43_thrust[2],AK43_sphericity[2],AK43_asymmetry[2],AK43_isotropy[2],AK43_aplanarity[2],AK43_FW1[2],AK43_FW2[2],AK43_FW3[2],AK43_FW4[2];
   double SJ_thrust[2],SJ_sphericity[2],SJ_asymmetry[2],SJ_isotropy[2],SJ_aplanarity[2],SJ_FW1[2],SJ_FW2[2],SJ_FW3[2],SJ_FW4[2];
   int eventTTbarCRFlag = 0;

   //MP superjet AK4 jet momenta and energies, tedious,but means we can do some SJ calculations locally, these will also become BEST variables
   double SJ1_AK4_px[100], SJ1_AK4_py[100], SJ1_AK4_pz[100], SJ1_AK4_E[100];

   double SJ2_AK4_px[100], SJ2_AK4_py[100], SJ2_AK4_pz, SJ2_AK4_E[100];

   double SJ1_SortCombinations_alt[100],SJ2_SortCombinations_alt[100];
   double SJ1_mass_genParts,SJ2_mass_genParts;
   int nCombinations;
   int ntrueInt;
   double diAK8Jet_mass[100];
   double fourAK8JetMass;
   int nAK8diJets = 2;
   bool isQCD = false,isTTbar =false;
   double PU_eventWeight_up, PU_eventWeight_nom, PU_eventWeight_down;
   double deepJet_wp_loose, deepJet_wp_med, deepjet_wp_tight;

   //TH2F *truebjet_eff,*truecjet_eff, *lightjet_eff;

   // btag scale factor stuff
   /*
   std::unique_ptr<CorrectionSet> cset;
   Correction::Ref cset_corrector_bc;
   Correction::Ref cset_corrector_light; 
   */
/*
   std::unique_ptr<CorrectionSet> PUjson;
   Correction::Ref PUjson_year;
*/

   bool doJEC = true;   
   bool doJER = true;
   bool doBtagSF = true; 
   bool doPUSF   = true;

   //TRandom3 *randomNum = new TRandom3(); // for JERs

};




//_constructor_
clusteringAnalyzerTest::clusteringAnalyzerTest(const edm::ParameterSet& iConfig):
path_ (iConfig.getParameter<edm::FileInPath>("path"))
{

   cache_ = new CacheHandler(path_);
   BEST_ = new BESTEvaluation(cache_);
   BEST_->configure(iConfig);

   runType        = iConfig.getParameter<std::string>("runType");
   systematicType = iConfig.getParameter<std::string>("systematicType");

   year = iConfig.getParameter<std::string>("year");



   bTagSF_path = iConfig.getParameter<edm::FileInPath>("bTagSF_path");
   bTagEff_path = iConfig.getParameter<edm::FileInPath>("bTagEff_path");
   PUfile_path = iConfig.getParameter<edm::FileInPath>("PUfile_path");

   edm::InputTag fixedGridRhoAllTag_ = edm::InputTag("fixedGridRhoAll", "", "RECO");   
   fatJetToken_ =    consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("fatJetCollection"));
   //triggerBits_ = consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"));
   jetToken_    = consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("jetCollection"));
   //metToken_    = consumes<std::vector<pat::MET>>(iConfig.getParameter<edm::InputTag>("metCollection"));
   //muonToken_ =    consumes<std::vector<pat::Muon>>(iConfig.getParameter<edm::InputTag>("muonCollection"));
   //electronToken_ =    consumes<std::vector<pat::Electron>>(iConfig.getParameter<edm::InputTag>("electronCollection"));
   //tauToken_ =    consumes<std::vector<pat::Tau>>(iConfig.getParameter<edm::InputTag>("tauCollection"));
   m_rho_token  = consumes<double>(fixedGridRhoAllTag_);
   edm::Service<TFileService> fs;      

   tree = fs->make<TTree>(  ("tree_"+systematicType).c_str(), ("tree_"+systematicType).c_str());


/*
   TFile *bTagEff_file = new TFile( bTagEff_path.fullPath().c_str() );   //this path might need to be updated



   truebjet_eff = (TH2F*)bTagEff_file->Get("h_effbJets");
   truecjet_eff = (TH2F*)bTagEff_file->Get("h_effcJets");
   lightjet_eff = (TH2F*)bTagEff_file->Get("h_effLightJets");

   cset = CorrectionSet::from_file(bTagSF_path.fullPath());
   cset_corrector_bc = cset->at("deepJet_mujets");   //deepJet_comb, 
   cset_corrector_light = cset->at("deepJet_incl");   //deepJet_incl
*/
   if(year == "2018")
   {
      //deepJet_wp_loose = 0.0490;
      //deepJet_wp_med   = 0.2783;
      deepjet_wp_tight = 0.7100;
      lumiTag = "Collisions18_UltraLegacy_goldenJSON";
   }
   else if(year == "2017")
   {
      //deepJet_wp_loose = 0.0532;
      //deepJet_wp_med   = 0.3040;
      deepjet_wp_tight = 0.7476;
      lumiTag = "Collisions17_UltraLegacy_goldenJSON";
   }
   else if(year == "2016")
   {
      //deepJet_wp_loose = 0.0480;
      //deepJet_wp_med   = 0.2489;
      deepjet_wp_tight = 0.8767;
      lumiTag = "Collisions16_UltraLegacy_goldenJSON";
   }
   else if(year == "2015")
   {
      //deepJet_wp_loose = 0.0508;
      //deepJet_wp_med   = 0.2598;
      deepjet_wp_tight = 0.6502;
      lumiTag = "Collisions16_UltraLegacy_goldenJSON";
   }
   else
   {
      std::cout << "Incorrect year: " << year << std::endl;
      return;
   }

/*
   PUjson = CorrectionSet::from_file(PUfile_path.fullPath());
   PUjson_year = PUjson->at(lumiTag);
*/

   tree->Branch("nfatjets", &nfatjets, "nfatjets/I");

   tree->Branch("nAK4", &nAK4, "nAK4/I");
   tree->Branch("AK4_bdisc", AK4_bdisc, "AK4_bdisc[nAK4]/D");
   tree->Branch("AK4_DeepJet_disc", AK4_DeepJet_disc, "AK4_DeepJet_disc[nAK4]/D");

   tree->Branch("tot_mpp_AK4", &tot_mpp_AK4, "tot_mpp_AK4/I");
   tree->Branch("nSuperJets", &nSuperJets, "nSuperJets/I");
   tree->Branch("tot_nAK4_50", &tot_nAK4_50, "tot_nAK4_50/I");             //total #AK4 jets (E>50 GeV) for BOTH superjets
   tree->Branch("tot_nAK4_70", &tot_nAK4_70, "tot_nAK4_70/I");
   tree->Branch("eventBetaCOM",&eventBetaCOM, "eventBetaCOM/D");
   tree->Branch("diSuperJet_mass",&diSuperJet_mass, "diSuperJet_mass/D");
   tree->Branch("diSuperJet_mass_100",&diSuperJet_mass_100, "diSuperJet_mass_100/D");
   tree->Branch("nfatjet_pre",&nfatjet_pre, "nfatjet_pre/I");
   tree->Branch("totHT",&totHT, "totHT/D");

   tree->Branch("totMET",&totMET, "totMET/D");
   
   tree->Branch("jet_pt", jet_pt, "jet_pt[nfatjets]/D");
   tree->Branch("jet_eta", jet_eta, "jet_eta[nfatjets]/D");
   tree->Branch("jet_mass", jet_mass, "jet_mass[nfatjets]/D");
   tree->Branch("AK4_mass", AK4_mass, "AK4_mass[nAK4]/D");

   tree->Branch("dijetMassOne", &dijetMassOne, "dijetMassOne/D");
   tree->Branch("dijetMassTwo", &dijetMassTwo, "dijetMassTwo/D");

   tree->Branch("SJ_nAK4_50", SJ_nAK4_50, "SJ_nAK4_50[nSuperJets]/I");
   tree->Branch("SJ_nAK4_70", SJ_nAK4_70, "SJ_nAK4_70[nSuperJets]/I");
   tree->Branch("SJ_nAK4_100", SJ_nAK4_100, "SJ_nAK4_100[nSuperJets]/I");
   tree->Branch("SJ_nAK4_125", SJ_nAK4_125, "SJ_nAK4_125[nSuperJets]/I");
   tree->Branch("SJ_nAK4_150", SJ_nAK4_150, "SJ_nAK4_150[nSuperJets]/I");
   tree->Branch("SJ_nAK4_200", SJ_nAK4_200, "SJ_nAK4_200[nSuperJets]/I");
   tree->Branch("SJ_nAK4_300", SJ_nAK4_300, "SJ_nAK4_300[nSuperJets]/I");
   tree->Branch("SJ_nAK4_400", SJ_nAK4_400, "SJ_nAK4_400[nSuperJets]/I");
   tree->Branch("SJ_nAK4_600", SJ_nAK4_600, "SJ_nAK4_600[nSuperJets]/I");
   tree->Branch("SJ_nAK4_800", SJ_nAK4_800, "SJ_nAK4_800[nSuperJets]/I");
   tree->Branch("SJ_nAK4_1000", SJ_nAK4_1000, "SJ_nAK4_1000[nSuperJets]/I");
////////////////////////// works 

   tree->Branch("SJ_mass_50", SJ_mass_50, "SJ_mass_50[nSuperJets]/D");
   tree->Branch("SJ_mass_70", SJ_mass_70, "SJ_mass_70[nSuperJets]/D");
   tree->Branch("SJ_mass_100", SJ_mass_100, "SJ_mass_100[nSuperJets]/D");
   tree->Branch("SJ_mass_125", SJ_mass_125, "SJ_mass_125[nSuperJets]/D");
   tree->Branch("SJ_mass_150", SJ_mass_150, "SJ_mass_150[nSuperJets]/D");
   tree->Branch("SJ_mass_200", SJ_mass_200, "SJ_mass_200[nSuperJets]/D");
   tree->Branch("SJ_mass_300", SJ_mass_300, "SJ_mass_300[nSuperJets]/D");
   tree->Branch("SJ_mass_400", SJ_mass_400, "SJ_mass_400[nSuperJets]/D");
   tree->Branch("SJ_mass_600", SJ_mass_600, "SJ_mass_600[nSuperJets]/D");
   tree->Branch("SJ_mass_800", SJ_mass_800, "SJ_mass_800[nSuperJets]/D");
   tree->Branch("SJ_mass_1000", SJ_mass_1000, "SJ_mass_1000[nSuperJets]/D");
   // doesn't work ....

   
   tree->Branch("superJet_mass", superJet_mass, "superJet_mass[nSuperJets]/D");
   tree->Branch("SJ_AK4_50_mass", SJ_AK4_50_mass, "SJ_AK4_50_mass[tot_nAK4_50]/D");    //mass of individual reclustered AK4 jets
   tree->Branch("SJ_AK4_70_mass", SJ_AK4_70_mass, "SJ_AK4_70_mass[tot_nAK4_70]/D");
   tree->Branch("AK4_E", AK4_E, "AK4_E[tot_mpp_AK4]/D");

   tree->Branch("leadAK8_mass",leadAK8_mass, "leadAK8_mass[nfatjets]/D");
   tree->Branch("event_reco_pt", &event_reco_pt, "event_reco_pt/D");

   tree->Branch("recoCOM_phi", &recoCOM_phi, "recoCOM_phi/D");
   tree->Branch("recoCOM_eta", &recoCOM_eta, "recoCOM_eta/D");

   tree->Branch("daughter_mass_comb", daughter_mass_comb, "daughter_mass_comb[nSuperJets]/D");
   
   tree->Branch("lab_nAK4", &lab_nAK4, "lab_nAK4/I");
   tree->Branch("lab_AK4_pt", lab_AK4_pt, "lab_AK4_pt[lab_nAK4]/D");


////////////////////////////////////////////////////////////////////////////////
   tree->Branch("AK4_m1",AK4_m1 , "AK4_m1[nSuperJets]/D");
   tree->Branch("AK4_m2",AK4_m2 , "AK4_m2[nSuperJets]/D");
   tree->Branch("AK4_m3",AK4_m3 , "AK4_m3[nSuperJets]/D");
   tree->Branch("AK4_m4",AK4_m4 , "AK4_m4[nSuperJets]/D");

   tree->Branch("AK41_E_tree",AK41_E_tree , "AK41_E_tree[nSuperJets]/D");
   tree->Branch("AK42_E_tree",AK42_E_tree , "AK42_E_tree[nSuperJets]/D");
   tree->Branch("AK43_E_tree",AK43_E_tree , "AK43_E_tree[nSuperJets]/D");
   tree->Branch("AK44_E_tree",AK44_E_tree , "AK44_E_tree[nSuperJets]/D");
   tree->Branch("AK4_m12",AK4_m12 , "AK4_m12[nSuperJets]/D");
   tree->Branch("AK4_m13",AK4_m13 , "AK4_m13[nSuperJets]/D");
   tree->Branch("AK4_m14",AK4_m14 , "AK4_m14[nSuperJets]/D");
   tree->Branch("AK4_m23",AK4_m23 , "AK4_m23[nSuperJets]/D");
   tree->Branch("AK4_m24",AK4_m24 , "AK4_m24[nSuperJets]/D");
   tree->Branch("AK4_m34",AK4_m34 , "AK4_m34[nSuperJets]/D");
   tree->Branch("AK4_m123", AK4_m123, "AK4_m123[nSuperJets]/D");
   tree->Branch("AK4_m124", AK4_m124, "AK4_m124[nSuperJets]/D");
   tree->Branch("AK4_m134",AK4_m134 , "AK4_m134[nSuperJets]/D");
   tree->Branch("AK4_m234",AK4_m234 , "AK4_m234[nSuperJets]/D");
   tree->Branch("AK4_m1234",AK4_m1234 , "AK4_m1234[nSuperJets]/D");
   tree->Branch("AK4_theta12",AK4_theta12 , "AK4_theta12[nSuperJets]/D");
   tree->Branch("AK4_theta13",AK4_theta13,  "AK4_theta13[nSuperJets]/D");
   tree->Branch("AK4_theta14", AK4_theta14, "AK4_theta14[nSuperJets]/D");
   tree->Branch("AK4_theta23",AK4_theta23 , "AK4_theta23[nSuperJets]/D");
   tree->Branch("AK4_theta24",AK4_theta24 , "AK4_theta24[nSuperJets]/D");
   tree->Branch("AK4_theta34", AK4_theta34, "AK4_theta34[nSuperJets]/D");


   tree->Branch("AK41_ndaughters",AK41_ndaughters , "AK41_ndaughters[nSuperJets]/I");
   tree->Branch("AK41_nsubjets", AK41_nsubjets, "AK41_nsubjets[nSuperJets]/I");
   tree->Branch("AK41_thrust", AK41_thrust, "AK41_thrust[nSuperJets]/D");
   tree->Branch("AK41_sphericity", AK41_sphericity, "AK41_sphericity[nSuperJets]/D");
   tree->Branch("AK41_asymmetry",AK41_asymmetry , "AK41_asymmetry[nSuperJets]/D");
   tree->Branch("AK41_isotropy",AK41_isotropy , "AK41_isotropy[nSuperJets]/D");
   tree->Branch("AK41_aplanarity", AK41_aplanarity, "AK41_aplanarity[nSuperJets]/D");
   tree->Branch("AK41_FW1", AK41_FW1, "AK41_FW1[nSuperJets]/D");
   tree->Branch("AK41_FW2", AK41_FW2, "AK41_FW2[nSuperJets]/D");
   tree->Branch("AK41_FW3", AK41_FW3, "AK41_FW3[nSuperJets]/D");
   tree->Branch("AK41_FW4", AK41_FW4, "AK41_FW4[nSuperJets]/D");

   tree->Branch("SJ_thrust", SJ_thrust, "SJ_thrust[nSuperJets]/D");
   tree->Branch("SJ_sphericity", SJ_sphericity, "SJ_sphericity[nSuperJets]/D");
   tree->Branch("SJ_asymmetry", SJ_asymmetry, "SJ_asymmetry[nSuperJets]/D");
   tree->Branch("SJ_isotropy", SJ_isotropy, "SJ_isotropy[nSuperJets]/D");
   tree->Branch("SJ_aplanarity", SJ_aplanarity, "SJ_aplanarity[nSuperJets]/D");
   tree->Branch("SJ_FW1", SJ_FW1, "SJ_FW1[nSuperJets]/D");
   tree->Branch("SJ_FW2", SJ_FW2, "SJ_FW2[nSuperJets]/D");
   tree->Branch("SJ_FW3", SJ_FW3, "SJ_FW3[nSuperJets]/D");
   tree->Branch("SJ_FW4", SJ_FW4, "SJ_FW4[nSuperJets]/D");

   tree->Branch("AK42_ndaughters",AK42_ndaughters , "AK42_ndaughters[nSuperJets]/I");
   tree->Branch("AK42_nsubjets", AK42_nsubjets, "AK42_nsubjets[nSuperJets]/I");

   tree->Branch("nCategories", &nCategories, "nCategories/I");
   tree->Branch("SJ1_BEST_scores", SJ1_BEST_scores, "SJ1_BEST_scores[nCategories]/D");
   tree->Branch("SJ2_BEST_scores", SJ2_BEST_scores, "SJ2_BEST_scores[nCategories]/D");
   tree->Branch("SJ1_decision", &SJ1_decision, "SJ1_decision/I");
   tree->Branch("SJ2_decision", &SJ2_decision, "SJ2_decision/I");

   tree->Branch("nAK4_uncut", &nAK4_uncut, "nAK4_uncut/I");
   tree->Branch("btag_score_uncut", btag_score_uncut, "btag_score_uncut[nAK4_uncut]/D");

   tree->Branch("AK4_ptot", AK4_ptot  , "AK4_ptot[lab_nAK4]/D");
   tree->Branch("AK4_eta", AK4_eta  , "AK4_eta[lab_nAK4]/D");
   tree->Branch("AK4_phi", AK4_phi  , "AK4_phi[lab_nAK4]/D");

   tree->Branch("ntrueInt", &ntrueInt  , "ntrueInt/I");
   tree->Branch("eventTTbarCRFlag", &eventTTbarCRFlag  , "eventTTbarCRFlag/I");

   tree->Branch("AK4_phi", AK4_phi  , "AK4_phi[lab_nAK4]/D");

   tree->Branch("nCombinations", &nCombinations  , "nCombinations/I");
   tree->Branch("SJ1_SortCombinations_alt", SJ1_SortCombinations_alt  , "SJ1_SortCombinations_alt[nCombinations]/D");
   tree->Branch("SJ2_SortCombinations_alt", SJ2_SortCombinations_alt  , "SJ2_SortCombinations_alt[nCombinations]/D");

   tree->Branch("nAK8diJets", &nAK8diJets  , "nAK8diJets/I");

   tree->Branch("diAK8Jet_mass", diAK8Jet_mass  , "diAK8Jet_mass[nAK8diJets]/D");
   tree->Branch("fourAK8JetMass", &fourAK8JetMass  , "fourAK8JetMass/D");

   tree->Branch("bTag_eventWeight_up", &bTag_eventWeight_up  , "bTag_eventWeight_up/D");
   tree->Branch("bTag_eventWeight_nom", &bTag_eventWeight_nom  , "bTag_eventWeight_nom/D");
   tree->Branch("bTag_eventWeight_down", &bTag_eventWeight_down  , "bTag_eventWeight_down/D");

   tree->Branch("PU_eventWeight_up", &PU_eventWeight_up, "PU_eventWeight_up/D");
   tree->Branch("PU_eventWeight_nom", &PU_eventWeight_nom, "PU_eventWeight_nom/D");
   tree->Branch("PU_eventWeight_down", &PU_eventWeight_down, "PU_eventWeight_down/D");

   //_tree_

   if( (runType.find("MC") != std::string::npos) || (runType.find("Suu") != std::string::npos))    //don't want these variables for data
   {

      genPartToken_ = consumes<std::vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("genPartCollection"));
      puSummaryToken_    = consumes<std::vector<PileupSummaryInfo>>(iConfig.getParameter<edm::InputTag>("pileupCollection"));

      if(runType.find("Suu") != std::string::npos)   //sig MC 
      {
         tree->Branch("_htWb", &_htWb, "_htWb/O");
         tree->Branch("_htZt", &_htZt, "_htZt/O");
         tree->Branch("_ZtWb", &_ZtWb, "_ZtWb/O");
         tree->Branch("_WbWb", &_WbWb, "_WbWb/O");
         tree->Branch("_htht", &_htht, "_htht/O");
         tree->Branch("_ZtZt", &_ZtZt, "_ZtZt/O");

         tree->Branch("SJ1_mass_genParts",&SJ1_mass_genParts,"SJ1_mass_genParts/D");
         tree->Branch("SJ2_mass_genParts",&SJ2_mass_genParts,"SJ2_mass_genParts/D");

      }
      else if ((runType.find("QCD") != std::string::npos) || (runType.find("TTbar") != std::string::npos) )  // BRMC
      {
         tree->Branch("nGenBJets_AK4", nGenBJets_AK4, "nGenBJets_AK4[lab_nAK4]/I");
         tree->Branch("AK4_partonFlavour", AK4_partonFlavour  , "AK4_partonFlavour[lab_nAK4]/I");
         tree->Branch("AK4_hadronFlavour", AK4_hadronFlavour  , "AK4_hadronFlavour[lab_nAK4]/I");
      }
      else
      {
         std::cout <<"Running as data ..." << std::endl;
      }

   }
   else if(runType == "Data")
   {
         std::cout <<"Running as data ..." << std::endl;
   }

}


double clusteringAnalyzerTest::calc_mag(double px,double py, double pz)
{
   return sqrt(pow(px,2)+pow(py,2)+pow(pz,2));
}
const reco::Candidate* clusteringAnalyzerTest::parse_chain(const reco::Candidate* cand)
{  
   for (unsigned int iii=0; iii<cand->numberOfDaughters(); iii++)
   {
      if(cand->daughter(iii)->pdgId() == cand->pdgId()) return parse_chain(cand->daughter(iii));
   }
   return cand;
}

bool clusteringAnalyzerTest::isgoodjet(const float eta, const float NHF,const float NEMF, const size_t NumConst,const float CHF,const int CHM, const float MUF, const float CEMF)
{
   if( (abs(eta) > 2.4)) return false;

   if ((NHF>0.9) || (NEMF>0.9) || (NumConst<1) || (CHF<0.) || (CHM<0) || (MUF > 0.8) || (CEMF > 0.8)) 
      {
         return false;
      }
   else{ return true;}

}
bool clusteringAnalyzerTest::isgoodjet(const float eta, const float NHF,const float NEMF, const size_t NumConst,const float CHF,const int CHM, const float MUF, const float CEMF, int nfatjets)
{
   if ( (nfatjets < 2) && (abs(eta) > 2.4) ) return false;
   else if ( (nfatjets >= 2) && (abs(eta) > 1.5) ) return false;

   if ((NHF>0.9) || (NEMF>0.9) || (NumConst<1) || (CHF<0.) || (CHM<0) || (MUF > 0.8) || (CEMF > 0.8)) 
      {
         return false;
      }
   else{ return true;}

}

double clusteringAnalyzerTest::calcMPP(TLorentzVector superJetTLV ) 
{
   Vector jet_axis(superJetTLV.Px()/superJetTLV.P(),superJetTLV.Py()/superJetTLV.P(),superJetTLV.Pz()/superJetTLV.P());
   double min_pp = 99999999999999.;
   double min_boost = 0.;

   for(int iii=0;iii<10000;iii++)
   {
      TLorentzVector superJetTLV_ = superJetTLV;
      double beta_cand = iii/10000.;
      superJetTLV_.Boost(-beta_cand*jet_axis.X(),-beta_cand*jet_axis.Y(),-beta_cand*jet_axis.Z());
      if(abs( ( superJetTLV_.Px()*superJetTLV.Px()+superJetTLV_.Py()*superJetTLV.Py() +superJetTLV_.Pz()*superJetTLV.Pz() )/superJetTLV.P() ) < min_pp) 
         {
            min_boost = beta_cand; 
            min_pp = abs( ( superJetTLV_.Px()*superJetTLV.Px()+superJetTLV_.Py()*superJetTLV.Py() +superJetTLV_.Pz()*superJetTLV.Pz() )/superJetTLV.P() ) ;
         }
      }
      return min_boost;
}
double clusteringAnalyzerTest::calc_mass(std::vector<TLorentzVector> candSuperJet)
{
   double px_tot = 0., py_tot = 0., pz_tot= 0.,E_tot = 0.;
   for(auto _iJet = candSuperJet.begin(); _iJet!=candSuperJet.end();_iJet++)
   {
      px_tot+=_iJet->Px();py_tot+=_iJet->Py();pz_tot+=_iJet->Pz();E_tot+=_iJet->E();
   }
   return sqrt(pow(E_tot,2) - pow(px_tot,2) - pow(py_tot,2) - pow(pz_tot,2));
}
bool clusteringAnalyzerTest::isMatchedtoSJ(std::vector<TLorentzVector> superJetTLVs, TLorentzVector candJet)
{
   for(auto iJet = superJetTLVs.begin(); iJet!=superJetTLVs.end(); iJet++)
   {
      if( abs(candJet.Angle(iJet->Vect())) < 0.001) return true;
      
   }
   
   return false;
}

bool clusteringAnalyzerTest::fillSJVars(std::map<std::string, float> &treeVars, std::vector<fastjet::PseudoJet> iSJ, int nSuperJets )
{
   double superJetpx=0,superJetpy=0,superJetpz=0,superJetE=0;
   for(auto iP = iSJ.begin();iP != iSJ.end();iP++)
   {
      superJetpx+=iP->px();superJetpy+=iP->py();superJetpz+=iP->pz();superJetE +=iP->E();
   }

   TLorentzVector superJetTLV(superJetpx,superJetpy,superJetpz,superJetE);    //Lorentz vector representing jet axis -> now minimize the parallel momentum
      
   //boost COM
   std::vector<fastjet::PseudoJet> boostedSuperJetPart;

   //boost particles in SuperJet to COM frame
   for(auto iP = iSJ.begin();iP != iSJ.end();iP++)
   {
      TLorentzVector iP_(iP->px(),iP->py(),iP->pz(),iP->E());
      iP_.Boost(-superJetTLV.Px()/superJetTLV.E(),-superJetTLV.Py()/superJetTLV.E(),-superJetTLV.Pz()/superJetTLV.E());
      boostedSuperJetPart.push_back(fastjet::PseudoJet(iP_.Px(),iP_.Py(),iP_.Pz(),iP_.E()));
   }

   ///////////get a bunch of versions of SJ particle collection to calclate BES variables
   std::vector<TLorentzVector> boostedSuperJetPart_TLV;
   std::vector<reco::LeafCandidate> boostedSuperJetPart_LC;
   std::vector<math::XYZVector> boostedSuperJetPart_XYZ;
   double sumPz = 0, sumP = 0;
   for(auto iP_= boostedSuperJetPart.begin(); iP_ !=boostedSuperJetPart.end(); iP_++)
   {   
      boostedSuperJetPart_TLV.push_back(TLorentzVector(iP_->px(),iP_->py(),iP_->pz(),iP_->E()));
      boostedSuperJetPart_LC.push_back(reco::LeafCandidate(+1, reco::Candidate::LorentzVector(iP_->px(),iP_->py(),iP_->pz(),iP_->E())));
      boostedSuperJetPart_XYZ.push_back(math::XYZVector( iP_->px(),iP_->py(),iP_->pz() ));
      sumPz += iP_->pz();
      sumP += abs(sqrt(pow(iP_->pz(),2) + pow(iP_->px(),2)+ pow(iP_->py(),2)));
   }


   ///reclustering SuperJet that is now boosted into the SJ COM frame
   double R = 0.4;

   //fastjet::JetDefinition jet_def(fastjet::antikt_algorithm, R);
   fastjet::JetDefinition jet_def(fastjet::cambridge_algorithm, R);
   fastjet::ClusterSequence cs_jet(boostedSuperJetPart, jet_def); 
   std::vector<fastjet::PseudoJet> jetsFJ_jet = fastjet::sorted_by_E(cs_jet.inclusive_jets(0.0));


   double SJ_25_px = 0, SJ_25_py=0,SJ_25_pz=0,SJ_25_E=0;
   double SJ_50_px = 0, SJ_50_py=0,SJ_50_pz=0,SJ_50_E=0;
   double SJ_100_px = 0, SJ_100_py=0,SJ_100_pz=0,SJ_100_E=0;
   double SJ_150_px = 0, SJ_150_py=0,SJ_150_pz=0,SJ_150_E=0;
   double SJ_200_px = 0, SJ_200_py=0,SJ_200_pz=0,SJ_200_E=0;
   double SJ_300_px = 0, SJ_300_py=0,SJ_300_pz=0,SJ_300_E=0;

   int SJ_nAK4_25_ = 0;
   int SJ_nAK4_50_ = 0,SJ_nAK4_100_ = 0,SJ_nAK4_150_ = 0,SJ_nAK4_200_ = 0,SJ_nAK4_300_ = 0;

   std::vector<TLorentzVector> AK41_parts;
   std::vector<TLorentzVector> AK42_parts;
   std::vector<TLorentzVector> AK43_parts;
   std::vector<TLorentzVector> AK44_parts;

   double AK41_px = 0, AK41_py=0,AK41_pz = 0, AK41_E = 0;
   double AK42_px = 0, AK42_py=0,AK42_pz = 0, AK42_E = 0;
   double AK43_px = 0, AK43_py=0,AK43_pz = 0, AK43_E = 0;
   double AK44_px = 0, AK44_py=0,AK44_pz = 0, AK44_E = 0;

   if (jetsFJ_jet.size() < 4)
   {
      std::cout << "A pseudojet vector has a size smaller than 4 - not reclustering many jets from whole pool of particles - " << jetsFJ_jet.size() << std::endl;
      return false;
   }
   int pseudoJetNum = 0;
   for (auto iPJ=jetsFJ_jet.begin(); iPJ<jetsFJ_jet.end(); iPJ++)                             
   {

      // do calculations of AK4 btagged particle ratios for leading 4 AK4 jets
      std::vector<fastjet::PseudoJet> iPJ_daughters = iPJ->constituents();
            
      if(pseudoJetNum == 0)
      {   
         treeVars["SJ_AK41_px"] = iPJ->px();
         treeVars["SJ_AK41_py"] = iPJ->py();
         treeVars["SJ_AK41_pz"] = iPJ->pz();
         treeVars["SJ_AK41_E"] = iPJ->E();
         for(auto iPart = iPJ_daughters.begin(); iPart != iPJ_daughters.end(); iPart++)
         {
            AK41_parts.push_back(TLorentzVector(iPart->px(),iPart->py(),iPart->pz(),iPart->E()));
            AK41_px+=iPart->px();AK41_py+=iPart->py();AK41_pz+=iPart->pz();AK41_E+=iPart->E();
         }

      }
      else if(pseudoJetNum == 1)
      {
         treeVars["SJ_AK42_px"] = iPJ->px();
         treeVars["SJ_AK42_py"] = iPJ->py();
         treeVars["SJ_AK42_pz"] = iPJ->pz();
         treeVars["SJ_AK42_E"] = iPJ->E();
         for(auto iPart = iPJ_daughters.begin(); iPart != iPJ_daughters.end(); iPart++)
         {
            AK42_parts.push_back(TLorentzVector(iPart->px(),iPart->py(),iPart->pz(),iPart->E()));
            AK42_px+=iPart->px();AK42_py+=iPart->py();AK42_pz+=iPart->pz();AK42_E+=iPart->E();
         }
      }
      else if(pseudoJetNum == 2)
      {
         treeVars["SJ_AK43_px"] = iPJ->px();
         treeVars["SJ_AK43_py"] = iPJ->py();
         treeVars["SJ_AK43_pz"] = iPJ->pz();
         treeVars["SJ_AK43_E"] = iPJ->E();
         for(auto iPart = iPJ_daughters.begin(); iPart != iPJ_daughters.end(); iPart++)
         {
            AK43_parts.push_back(TLorentzVector(iPart->px(),iPart->py(),iPart->pz(),iPart->E()));
            AK43_px+=iPart->px();AK43_py+=iPart->py();AK43_pz+=iPart->pz();AK43_E+=iPart->E();
         }
      }
      else if(pseudoJetNum == 3)
      {
         treeVars["SJ_AK44_px"] = iPJ->px();
         treeVars["SJ_AK44_py"] = iPJ->py();
         treeVars["SJ_AK44_pz"] = iPJ->pz();
         treeVars["SJ_AK44_E"] = iPJ->E();      
         for(auto iPart = iPJ_daughters.begin(); iPart != iPJ_daughters.end(); iPart++)
         {
            AK44_parts.push_back(TLorentzVector(iPart->px(),iPart->py(),iPart->pz(),iPart->E()));
            AK44_px+=iPart->px();AK44_py+=iPart->py();AK44_pz+=iPart->pz();AK44_E+=iPart->E();

         }

      }
      if(iPJ->E()>25.)
      {
         SJ_25_px+=iPJ->px();SJ_25_py+=iPJ->py();SJ_25_pz+=iPJ->pz();SJ_25_E+=iPJ->E();
         SJ_nAK4_25_++;
      }

      if(iPJ->E()>50.)
      {
         SJ_50_px+=iPJ->px();SJ_50_py+=iPJ->py();SJ_50_pz+=iPJ->pz();SJ_50_E+=iPJ->E();
         SJ_nAK4_50_++;
      }

      if(iPJ->E()>100)
      {
         SJ_100_px+=iPJ->px();SJ_100_py+=iPJ->py();SJ_100_pz+=iPJ->pz();SJ_100_E+=iPJ->E();
         SJ_nAK4_100_++; 
      }

      if(iPJ->E()>150)
      {
         SJ_150_px+=iPJ->px();SJ_150_py+=iPJ->py();SJ_150_pz+=iPJ->pz();SJ_150_E+=iPJ->E();
         SJ_nAK4_150_++; 
      }

      if(iPJ->E()>200)
      {
         SJ_200_px+=iPJ->px();SJ_200_py+=iPJ->py();SJ_200_pz+=iPJ->pz();SJ_200_E+=iPJ->E();
         SJ_nAK4_200_++; 
      }

      if(iPJ->E()>300)
      {
         SJ_300_px+=iPJ->px();SJ_300_py+=iPJ->py();SJ_300_pz+=iPJ->pz();SJ_300_E+=iPJ->E();
         SJ_nAK4_300_++; 
      }
      pseudoJetNum++;
   }

   boostedSuperJetPart.clear();   //shouldn't be needed, just in case

   /////annoying process of getting the BES information for the reclustered AK4 jets

   TVector3 AK41_boost(AK41_px/AK41_E,AK41_py/AK41_E,AK41_pz/AK41_E);
   TVector3 AK42_boost(AK42_px/AK42_E,AK42_py/AK42_E,AK42_pz/AK42_E);
   TVector3 AK43_boost(AK43_px/AK43_E,AK43_py/AK43_E,AK43_pz/AK43_E);
   TVector3 AK44_boost(AK44_px/AK44_E,AK44_py/AK44_E,AK44_pz/AK44_E);

   std::vector<TLorentzVector> boostedAK41_Part_TLV;
   std::vector<reco::LeafCandidate>  boostedAK41_Part_LC;
   std::vector<math::XYZVector>  boostedAK41_Part_XYZ;

   std::vector<TLorentzVector> boostedAK42_Part_TLV;
   std::vector<reco::LeafCandidate>  boostedAK42_Part_LC;
   std::vector<math::XYZVector>  boostedAK42_Part_XYZ;

   std::vector<TLorentzVector> boostedAK43_Part_TLV;
   std::vector<reco::LeafCandidate>  boostedAK43_Part_LC;
   std::vector<math::XYZVector>  boostedAK43_Part_XYZ;

   std::vector<TLorentzVector> boostedAK44_Part_TLV;
   std::vector<reco::LeafCandidate>  boostedAK44_Part_LC;
   std::vector<math::XYZVector>  boostedAK44_Part_XYZ;

   double sumPz_AK41 =0,sumPz_AK42 = 0,sumPz_AK43 = 0,sumPz_AK44 = 0;
   double sumP_AK41 = 0,sumP_AK42 = 0,sumP_AK43 = 0, sumP_AK44 = 0;
   for(auto iP = AK41_parts.begin(); iP != AK41_parts.end(); iP++)
   {
      iP->Boost(-AK41_boost.X(),-AK41_boost.Y(), -AK41_boost.Z());
      boostedAK41_Part_TLV.push_back(TLorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E()));
      boostedAK41_Part_LC.push_back(reco::LeafCandidate(+1, reco::Candidate::LorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E())));
      boostedAK41_Part_XYZ.push_back(math::XYZVector( iP->Px(),iP->Py(),iP->Pz() ));
      sumPz_AK41+=iP->Pz(); sumP_AK41+= abs(iP->P());
   }
   for(auto iP = AK42_parts.begin(); iP != AK42_parts.end(); iP++)
   {
      iP->Boost(-AK42_boost.X(),-AK42_boost.Y(), -AK42_boost.Z());
      boostedAK42_Part_TLV.push_back(TLorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E()));
      boostedAK42_Part_LC.push_back(reco::LeafCandidate(+1, reco::Candidate::LorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E())));
      boostedAK42_Part_XYZ.push_back(math::XYZVector( iP->Px(),iP->Py(),iP->Pz() ));  
      sumPz_AK42+=iP->Pz(); sumP_AK42+= abs(iP->P());
   }
   for(auto iP = AK43_parts.begin(); iP != AK43_parts.end(); iP++)
   {
      iP->Boost(-AK43_boost.X(),-AK43_boost.Y(), -AK43_boost.Z());
      boostedAK43_Part_TLV.push_back(TLorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E()));
      boostedAK43_Part_LC.push_back(reco::LeafCandidate(+1, reco::Candidate::LorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E())));
      boostedAK43_Part_XYZ.push_back(math::XYZVector( iP->Px(),iP->Py(),iP->Pz() )); 
      sumPz_AK43 += iP->Pz(); sumP_AK43 += abs(iP->P());   
   }
   for(auto iP = AK44_parts.begin(); iP != AK44_parts.end(); iP++)
   {
      iP->Boost(-AK44_boost.X(),-AK44_boost.Y(), -AK44_boost.Z());
      boostedAK44_Part_TLV.push_back(TLorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E()));
      boostedAK44_Part_LC.push_back(reco::LeafCandidate(+1, reco::Candidate::LorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E())));
      boostedAK44_Part_XYZ.push_back(math::XYZVector( iP->Px(),iP->Py(),iP->Pz() )); 
      sumPz_AK44 += iP->Pz(); sumP_AK44 += abs(iP->P());   
   }

   ////vectors to get angles
        
   TVector3 AK4_jet1(jetsFJ_jet[0].px(),jetsFJ_jet[0].py(),jetsFJ_jet[0].pz());
   TVector3 AK4_jet2(jetsFJ_jet[1].px(),jetsFJ_jet[1].py(),jetsFJ_jet[1].pz());
   TVector3 AK4_jet3(jetsFJ_jet[2].px(),jetsFJ_jet[2].py(),jetsFJ_jet[2].pz());
   TVector3 AK4_jet4(jetsFJ_jet[3].px(),jetsFJ_jet[3].py(),jetsFJ_jet[3].pz());

   //fill superjet variables here ...
   //SJ mass variables
   treeVars["SJ_mass"]    = sqrt(pow(superJetE,2)-pow(superJetpx,2)-pow(superJetpy,2)-pow(superJetpz,2)); 
   treeVars["SJ_mass_25"] = sqrt(pow(SJ_25_E,2)-pow(SJ_25_px,2)-pow(SJ_25_py,2)-pow(SJ_25_pz,2)); 
   treeVars["SJ_mass_50"] = sqrt(pow(SJ_50_E,2)-pow(SJ_50_px,2)-pow(SJ_50_py,2)-pow(SJ_50_pz,2)); 
   treeVars["SJ_mass_100"] = sqrt(pow(SJ_100_E,2)-pow(SJ_100_px,2)-pow(SJ_100_py,2)-pow(SJ_100_pz,2)); 
   treeVars["SJ_mass_150"] = sqrt(pow(SJ_150_E,2)-pow(SJ_150_px,2)-pow(SJ_150_py,2)-pow(SJ_150_pz,2)); 
   treeVars["SJ_mass_200"] = sqrt(pow(SJ_200_E,2)-pow(SJ_200_px,2)-pow(SJ_200_py,2)-pow(SJ_200_pz,2)); 
   treeVars["SJ_mass_300"] = sqrt(pow(SJ_300_E,2)-pow(SJ_300_px,2)-pow(SJ_300_py,2)-pow(SJ_300_pz,2)); 


   //SJ nAK4 variables
   treeVars["SJ_nAK4_25"] = SJ_nAK4_25_; 
   treeVars["SJ_nAK4_50"] = SJ_nAK4_50_; 
   treeVars["SJ_nAK4_100"] = SJ_nAK4_100_; 
   treeVars["SJ_nAK4_150"] = SJ_nAK4_150_; 
   treeVars["SJ_nAK4_200"] = SJ_nAK4_200_; 
   treeVars["SJ_nAK4_300"] = SJ_nAK4_300_; 

   //softdrop mass???
   //bjet particle percentages

   //AK4 jet mass combinations
   treeVars["AK4_m1"] = jetsFJ_jet[0].m();   
   treeVars["AK4_m2"] = jetsFJ_jet[1].m(); 
   treeVars["AK4_m3"] = jetsFJ_jet[2].m(); 
   treeVars["AK4_m4"] = jetsFJ_jet[3].m(); 

   treeVars["AK41_E"] = jetsFJ_jet[0].E(); 
   treeVars["AK42_E"] = jetsFJ_jet[1].E(); 
   treeVars["AK43_E"] = jetsFJ_jet[2].E(); 
   treeVars["AK44_E"] = jetsFJ_jet[3].E(); 


   treeVars["AK4_m12"] = sqrt( pow(jetsFJ_jet[0].E() + jetsFJ_jet[1].E() ,2) - pow(jetsFJ_jet[0].px() + jetsFJ_jet[1].px(),2) - pow(jetsFJ_jet[0].py() + jetsFJ_jet[1].py(),2)- pow(jetsFJ_jet[0].pz() + jetsFJ_jet[1].pz(),2));   
   treeVars["AK4_m13"] = sqrt( pow(jetsFJ_jet[0].E() + jetsFJ_jet[2].E() ,2) - pow(jetsFJ_jet[0].px() + jetsFJ_jet[2].px(),2) - pow(jetsFJ_jet[0].py() + jetsFJ_jet[2].py(),2)- pow(jetsFJ_jet[0].pz() + jetsFJ_jet[2].pz(),2));   
   treeVars["AK4_m14"] = sqrt( pow(jetsFJ_jet[0].E() + jetsFJ_jet[3].E() ,2) - pow(jetsFJ_jet[0].px() + jetsFJ_jet[3].px(),2) - pow(jetsFJ_jet[0].py() + jetsFJ_jet[3].py(),2)- pow(jetsFJ_jet[0].pz() + jetsFJ_jet[3].pz(),2));   
   treeVars["AK4_m23"] = sqrt( pow(jetsFJ_jet[2].E() + jetsFJ_jet[1].E() ,2) - pow(jetsFJ_jet[2].px() + jetsFJ_jet[1].px(),2) - pow(jetsFJ_jet[2].py() + jetsFJ_jet[1].py(),2)- pow(jetsFJ_jet[2].pz() + jetsFJ_jet[1].pz(),2));   
   treeVars["AK4_m24"] = sqrt( pow(jetsFJ_jet[3].E() + jetsFJ_jet[1].E() ,2) - pow(jetsFJ_jet[3].px() + jetsFJ_jet[1].px(),2) - pow(jetsFJ_jet[3].py() + jetsFJ_jet[1].py(),2)- pow(jetsFJ_jet[3].pz() + jetsFJ_jet[1].pz(),2));   
   treeVars["AK4_m34"] = sqrt( pow(jetsFJ_jet[2].E() + jetsFJ_jet[3].E() ,2) - pow(jetsFJ_jet[2].px() + jetsFJ_jet[3].px(),2) - pow(jetsFJ_jet[2].py() + jetsFJ_jet[3].py(),2)- pow(jetsFJ_jet[2].pz() + jetsFJ_jet[3].pz(),2));   

   treeVars["AK4_m123"] =sqrt( pow(jetsFJ_jet[0].E() + jetsFJ_jet[1].E() + jetsFJ_jet[2].E() ,2) - pow(jetsFJ_jet[0].px() + jetsFJ_jet[1].px() + jetsFJ_jet[2].px(),2) - pow(jetsFJ_jet[0].py() + jetsFJ_jet[1].py() + jetsFJ_jet[2].py(),2)- pow(jetsFJ_jet[0].pz() + jetsFJ_jet[1].pz() + jetsFJ_jet[2].pz(),2));   
   treeVars["AK4_m124"] =sqrt( pow(jetsFJ_jet[0].E() + jetsFJ_jet[1].E() + jetsFJ_jet[3].E() ,2) - pow(jetsFJ_jet[0].px() + jetsFJ_jet[1].px() + jetsFJ_jet[3].px(),2) - pow(jetsFJ_jet[0].py() + jetsFJ_jet[1].py() + jetsFJ_jet[3].py(),2)- pow(jetsFJ_jet[0].pz() + jetsFJ_jet[1].pz() + jetsFJ_jet[3].pz(),2));   
   treeVars["AK4_m134"] =sqrt( pow(jetsFJ_jet[0].E() + jetsFJ_jet[2].E() + jetsFJ_jet[3].E() ,2) - pow(jetsFJ_jet[0].px() + jetsFJ_jet[2].px() + jetsFJ_jet[3].px(),2) - pow(jetsFJ_jet[0].py() + jetsFJ_jet[2].py() + jetsFJ_jet[3].py(),2)- pow(jetsFJ_jet[0].pz() + jetsFJ_jet[2].pz() + jetsFJ_jet[3].pz(),2));   
   treeVars["AK4_m234"] =sqrt( pow(jetsFJ_jet[1].E() + jetsFJ_jet[2].E() + jetsFJ_jet[3].E() ,2) - pow(jetsFJ_jet[1].px() + jetsFJ_jet[2].px() + jetsFJ_jet[3].px(),2) - pow(jetsFJ_jet[1].py() + jetsFJ_jet[2].py() + jetsFJ_jet[3].py(),2)- pow(jetsFJ_jet[1].pz() + jetsFJ_jet[2].pz() + jetsFJ_jet[3].pz(),2));   

   treeVars["AK4_m1234"] =sqrt( pow(jetsFJ_jet[0].E() + jetsFJ_jet[1].E() + jetsFJ_jet[2].E()+jetsFJ_jet[3].E() ,2) - pow(jetsFJ_jet[0].px() + jetsFJ_jet[1].px() + jetsFJ_jet[2].px()+jetsFJ_jet[3].px(),2) - pow(jetsFJ_jet[0].py() + jetsFJ_jet[1].py() + jetsFJ_jet[2].py()+jetsFJ_jet[3].py(),2)- pow(jetsFJ_jet[0].pz() + jetsFJ_jet[1].pz() + jetsFJ_jet[2].pz()+jetsFJ_jet[3].pz(),2));   
   

   //AK4 jet angles 
   treeVars["AK4_theta12"] = abs(AK4_jet1.Angle(AK4_jet2));   
   treeVars["AK4_theta13"] = abs(AK4_jet1.Angle(AK4_jet3));
   treeVars["AK4_theta14"] = abs(AK4_jet1.Angle(AK4_jet4));
   treeVars["AK4_theta23"] = abs(AK4_jet2.Angle(AK4_jet3));
   treeVars["AK4_theta24"] = abs(AK4_jet2.Angle(AK4_jet4));
   treeVars["AK4_theta34"] = abs(AK4_jet3.Angle(AK4_jet4));

   EventShapeVariables eventShapesAK41( boostedAK41_Part_XYZ );
   Thrust thrustCalculatorAK41( boostedAK41_Part_LC.begin(), boostedAK41_Part_LC.end() );
   double fwmAK41[5] = { 0.0, 0.0 ,0.0 ,0.0,0.0};
   FWMoments( boostedAK41_Part_TLV, fwmAK41); 

   EventShapeVariables eventShapesAK42( boostedAK42_Part_XYZ );
   Thrust thrustCalculatorAK42( boostedAK42_Part_LC.begin(), boostedAK42_Part_LC.end() );
   double fwmAK42[5] = { 0.0, 0.0 ,0.0 ,0.0,0.0};
   FWMoments( boostedAK42_Part_TLV, fwmAK42); 

   EventShapeVariables eventShapesAK43( boostedAK43_Part_XYZ );
   Thrust thrustCalculatorAK43( boostedAK43_Part_LC.begin(), boostedAK43_Part_LC.end() );
   double fwmAK43[5] = { 0.0, 0.0 ,0.0 ,0.0,0.0};
   FWMoments( boostedAK43_Part_TLV, fwmAK43); 

   EventShapeVariables eventShapesAK44( boostedAK44_Part_XYZ );
   Thrust thrustCalculatorAK44( boostedAK44_Part_LC.begin(), boostedAK44_Part_LC.end() );
   double fwmAK44[5] = { 0.0, 0.0 ,0.0 ,0.0,0.0};
   FWMoments( boostedAK44_Part_TLV, fwmAK44); 


   //AK4 jet boosted information - boost reclustered AK4 jets into their COM and look at BES variables, ndaughters, nsubjettiness
   treeVars["AK41_ndaughters"] = jetsFJ_jet[0].constituents().size();  
   treeVars["AK41_nsubjets"] = jetsFJ_jet[0].n_exclusive_subjets(0.2); 
   treeVars["AK41_thrust"] = thrustCalculatorAK41.thrust();
   treeVars["AK41_sphericity"] = eventShapesAK41.sphericity();
   treeVars["AK41_asymmetry"] = sumPz_AK41/sumP_AK41; 
   treeVars["AK41_isotropy"] = eventShapesAK41.isotropy();
   treeVars["AK41_aplanarity"] = eventShapesAK41.aplanarity();
   treeVars["AK41_FW1"] = fwmAK41[1]; 
   treeVars["AK41_FW2"] = fwmAK41[2]; 
   treeVars["AK41_FW3"] = fwmAK41[3]; 
   treeVars["AK41_FW4"] = fwmAK41[4]; 

   treeVars["AK42_ndaughters"] = jetsFJ_jet[1].constituents().size(); 
   treeVars["AK42_nsubjets"] = jetsFJ_jet[1].exclusive_subjets(0.2).size();
   treeVars["AK42_thrust"] = thrustCalculatorAK42.thrust(); 
   treeVars["AK42_sphericity"] = eventShapesAK42.sphericity();
   treeVars["AK42_asymmetry"] = sumPz_AK42/sumP_AK42; 
   treeVars["AK42_isotropy"] = eventShapesAK42.isotropy();
   treeVars["AK42_aplanarity"] = eventShapesAK42.aplanarity();
   treeVars["AK42_FW1"] = fwmAK42[1]; 
   treeVars["AK42_FW2"] = fwmAK42[2]; 
   treeVars["AK42_FW3"] = fwmAK42[3]; 
   treeVars["AK42_FW4"] = fwmAK42[4]; 

   treeVars["AK43_ndaughters"] = jetsFJ_jet[2].constituents().size(); 
   treeVars["AK43_nsubjets"] = jetsFJ_jet[2].exclusive_subjets(0.2).size();
   treeVars["AK43_thrust"] = thrustCalculatorAK43.thrust();
   treeVars["AK43_sphericity"] = eventShapesAK43.sphericity();
   treeVars["AK43_asymmetry"] = sumPz_AK43/sumP_AK43; 
   treeVars["AK43_isotropy"] = eventShapesAK43.isotropy();
   treeVars["AK43_aplanarity"] = eventShapesAK43.aplanarity();
   treeVars["AK43_FW1"] = fwmAK43[1]; 
   treeVars["AK43_FW2"] = fwmAK43[2]; 
   treeVars["AK43_FW3"] = fwmAK43[3]; 
   treeVars["AK43_FW4"] = fwmAK43[4]; 

   //Full SJ BES variablesf
   EventShapeVariables eventShapes( boostedSuperJetPart_XYZ );
   Thrust thrustCalculator( boostedSuperJetPart_LC.begin(), boostedSuperJetPart_LC.end() );
   double fwm[5] = { 0.0, 0.0 ,0.0 ,0.0,0.0};
   FWMoments( boostedSuperJetPart_TLV, fwm); 
   treeVars["SJ_thrust"] = thrustCalculator.thrust();
   treeVars["SJ_sphericity"] = eventShapes.sphericity();
   treeVars["SJ_asymmetry"] = sumPz/sumP; 
   treeVars["SJ_isotropy"] = eventShapes.isotropy();
   treeVars["SJ_aplanarity"] = eventShapes.aplanarity();
   treeVars["SJ_FW1"] = fwm[1]; 
   treeVars["SJ_FW2"] = fwm[2]; 
   treeVars["SJ_FW3"] = fwm[3]; 
   treeVars["SJ_FW4"] = fwm[4]; 

///////////////////// BESvars for tree//////////////////////////////////////////

   //AK4 jet mass combinations
   AK4_m1[nSuperJets] = jetsFJ_jet[0].m();   
   AK4_m2[nSuperJets] = jetsFJ_jet[1].m(); 
   AK4_m3[nSuperJets] = jetsFJ_jet[2].m(); 
   AK4_m4[nSuperJets] = jetsFJ_jet[3].m(); 

   AK41_E_tree[nSuperJets] = jetsFJ_jet[0].E(); 
   AK42_E_tree[nSuperJets] = jetsFJ_jet[1].E(); 
   AK43_E_tree[nSuperJets] = jetsFJ_jet[2].E(); 
   AK44_E_tree[nSuperJets] = jetsFJ_jet[3].E(); 


   AK4_m12[nSuperJets] = sqrt( pow(jetsFJ_jet[0].E() + jetsFJ_jet[1].E() ,2) - pow(jetsFJ_jet[0].px() + jetsFJ_jet[1].px(),2) - pow(jetsFJ_jet[0].py() + jetsFJ_jet[1].py(),2)- pow(jetsFJ_jet[0].pz() + jetsFJ_jet[1].pz(),2));   
   AK4_m13[nSuperJets] = sqrt( pow(jetsFJ_jet[0].E() + jetsFJ_jet[2].E() ,2) - pow(jetsFJ_jet[0].px() + jetsFJ_jet[2].px(),2) - pow(jetsFJ_jet[0].py() + jetsFJ_jet[2].py(),2)- pow(jetsFJ_jet[0].pz() + jetsFJ_jet[2].pz(),2));   
   AK4_m14[nSuperJets] = sqrt( pow(jetsFJ_jet[0].E() + jetsFJ_jet[3].E() ,2) - pow(jetsFJ_jet[0].px() + jetsFJ_jet[3].px(),2) - pow(jetsFJ_jet[0].py() + jetsFJ_jet[3].py(),2)- pow(jetsFJ_jet[0].pz() + jetsFJ_jet[3].pz(),2));   
   AK4_m23[nSuperJets] = sqrt( pow(jetsFJ_jet[2].E() + jetsFJ_jet[1].E() ,2) - pow(jetsFJ_jet[2].px() + jetsFJ_jet[1].px(),2) - pow(jetsFJ_jet[2].py() + jetsFJ_jet[1].py(),2)- pow(jetsFJ_jet[2].pz() + jetsFJ_jet[1].pz(),2));   
   AK4_m24[nSuperJets] = sqrt( pow(jetsFJ_jet[3].E() + jetsFJ_jet[1].E() ,2) - pow(jetsFJ_jet[3].px() + jetsFJ_jet[1].px(),2) - pow(jetsFJ_jet[3].py() + jetsFJ_jet[1].py(),2)- pow(jetsFJ_jet[3].pz() + jetsFJ_jet[1].pz(),2));   
   AK4_m34[nSuperJets] = sqrt( pow(jetsFJ_jet[2].E() + jetsFJ_jet[3].E() ,2) - pow(jetsFJ_jet[2].px() + jetsFJ_jet[3].px(),2) - pow(jetsFJ_jet[2].py() + jetsFJ_jet[3].py(),2)- pow(jetsFJ_jet[2].pz() + jetsFJ_jet[3].pz(),2));   

   AK4_m123[nSuperJets] =sqrt( pow(jetsFJ_jet[0].E() + jetsFJ_jet[1].E() + jetsFJ_jet[2].E() ,2) - pow(jetsFJ_jet[0].px() + jetsFJ_jet[1].px() + jetsFJ_jet[2].px(),2) - pow(jetsFJ_jet[0].py() + jetsFJ_jet[1].py() + jetsFJ_jet[2].py(),2)- pow(jetsFJ_jet[0].pz() + jetsFJ_jet[1].pz() + jetsFJ_jet[2].pz(),2));   
   AK4_m124[nSuperJets] =sqrt( pow(jetsFJ_jet[0].E() + jetsFJ_jet[1].E() + jetsFJ_jet[3].E() ,2) - pow(jetsFJ_jet[0].px() + jetsFJ_jet[1].px() + jetsFJ_jet[3].px(),2) - pow(jetsFJ_jet[0].py() + jetsFJ_jet[1].py() + jetsFJ_jet[3].py(),2)- pow(jetsFJ_jet[0].pz() + jetsFJ_jet[1].pz() + jetsFJ_jet[3].pz(),2));   
   AK4_m134[nSuperJets] =sqrt( pow(jetsFJ_jet[0].E() + jetsFJ_jet[2].E() + jetsFJ_jet[3].E() ,2) - pow(jetsFJ_jet[0].px() + jetsFJ_jet[2].px() + jetsFJ_jet[3].px(),2) - pow(jetsFJ_jet[0].py() + jetsFJ_jet[2].py() + jetsFJ_jet[3].py(),2)- pow(jetsFJ_jet[0].pz() + jetsFJ_jet[2].pz() + jetsFJ_jet[3].pz(),2));   
   AK4_m234[nSuperJets] =sqrt( pow(jetsFJ_jet[1].E() + jetsFJ_jet[2].E() + jetsFJ_jet[3].E() ,2) - pow(jetsFJ_jet[1].px() + jetsFJ_jet[2].px() + jetsFJ_jet[3].px(),2) - pow(jetsFJ_jet[1].py() + jetsFJ_jet[2].py() + jetsFJ_jet[3].py(),2)- pow(jetsFJ_jet[1].pz() + jetsFJ_jet[2].pz() + jetsFJ_jet[3].pz(),2));   

   AK4_m1234[nSuperJets] =sqrt( pow(jetsFJ_jet[0].E() + jetsFJ_jet[1].E() + jetsFJ_jet[2].E()+jetsFJ_jet[3].E() ,2) - pow(jetsFJ_jet[0].px() + jetsFJ_jet[1].px() + jetsFJ_jet[2].px()+jetsFJ_jet[3].px(),2) - pow(jetsFJ_jet[0].py() + jetsFJ_jet[1].py() + jetsFJ_jet[2].py()+jetsFJ_jet[3].py(),2)- pow(jetsFJ_jet[0].pz() + jetsFJ_jet[1].pz() + jetsFJ_jet[2].pz()+jetsFJ_jet[3].pz(),2));   

   AK4_theta12[nSuperJets] = abs(AK4_jet1.Angle(AK4_jet2));   
   AK4_theta13[nSuperJets] = abs(AK4_jet1.Angle(AK4_jet3));
   AK4_theta14[nSuperJets] = abs(AK4_jet1.Angle(AK4_jet4));
   AK4_theta23[nSuperJets] = abs(AK4_jet2.Angle(AK4_jet3));
   AK4_theta24[nSuperJets] = abs(AK4_jet2.Angle(AK4_jet4));
   AK4_theta34[nSuperJets] = abs(AK4_jet3.Angle(AK4_jet4));
   //AK4 jet boosted information - boost reclustered AK4 jets into their COM and look at BES variables, ndaughters, nsubjettiness
   AK41_ndaughters[nSuperJets] = jetsFJ_jet[0].constituents().size();  
   AK41_nsubjets[nSuperJets] = jetsFJ_jet[0].n_exclusive_subjets(0.2); 
   AK41_thrust[nSuperJets] = thrustCalculatorAK41.thrust();
   AK41_sphericity[nSuperJets] = eventShapesAK41.sphericity();
   AK41_asymmetry[nSuperJets] = sumPz_AK41/sumP_AK41; 
   AK41_isotropy[nSuperJets] = eventShapesAK41.isotropy();
   AK41_aplanarity[nSuperJets] = eventShapesAK41.aplanarity();
   AK41_FW1[nSuperJets] = fwmAK41[1]; 
   AK41_FW2[nSuperJets] = fwmAK41[2]; 
   AK41_FW3[nSuperJets] = fwmAK41[3]; 
   AK41_FW4[nSuperJets] = fwmAK41[4]; 

   AK42_ndaughters[nSuperJets] = jetsFJ_jet[1].constituents().size(); 
   AK42_nsubjets[nSuperJets] = jetsFJ_jet[1].exclusive_subjets(0.2).size();
   AK42_thrust[nSuperJets] = thrustCalculatorAK42.thrust(); 
   AK42_sphericity[nSuperJets] = eventShapesAK42.sphericity();
   AK42_asymmetry[nSuperJets] = sumPz_AK42/sumP_AK42; 
   AK42_isotropy[nSuperJets] = eventShapesAK42.isotropy();
   AK42_aplanarity[nSuperJets] = eventShapesAK42.aplanarity();
   AK42_FW1[nSuperJets] = fwmAK42[1]; 
   AK42_FW2[nSuperJets] = fwmAK42[2]; 
   AK42_FW3[nSuperJets] = fwmAK42[3]; 
   AK42_FW4[nSuperJets] = fwmAK42[4]; 

   AK43_ndaughters[nSuperJets] = jetsFJ_jet[2].constituents().size(); 
   AK43_nsubjets[nSuperJets] = jetsFJ_jet[2].exclusive_subjets(0.2).size();
   AK43_thrust[nSuperJets] = thrustCalculatorAK43.thrust();
   AK43_sphericity[nSuperJets] = eventShapesAK43.sphericity();
   AK43_asymmetry[nSuperJets] = sumPz_AK43/sumP_AK43; 
   AK43_isotropy[nSuperJets] = eventShapesAK43.isotropy();
   AK43_aplanarity[nSuperJets] = eventShapesAK43.aplanarity();
   AK43_FW1[nSuperJets] = fwmAK43[1]; 
   AK43_FW2[nSuperJets] = fwmAK43[2]; 
   AK43_FW3[nSuperJets] = fwmAK43[3]; 
   AK43_FW4[nSuperJets] = fwmAK43[4]; 

   SJ_thrust[nSuperJets] = thrustCalculator.thrust();
   SJ_sphericity[nSuperJets] = eventShapes.sphericity();
   SJ_asymmetry[nSuperJets] = sumPz/sumP; 
   SJ_isotropy[nSuperJets] = eventShapes.isotropy();
   SJ_aplanarity[nSuperJets] = eventShapes.aplanarity();
   SJ_FW1[nSuperJets] = fwm[1]; 
   SJ_FW2[nSuperJets] = fwm[2]; 
   SJ_FW3[nSuperJets] = fwm[3]; 
   SJ_FW4[nSuperJets] = fwm[4];

   for (auto i = treeVars.begin(); i!=treeVars.end(); i++)
   {
      if (  (i->second  != i->second ) || ( isinf(i->second   )  ) )
      {
            return false;
      }
      else if ( abs( i->second+999.99 ) < 1.0e-10 ) return false;
   }
   //std::cout << "--------------- new SJ ----------------" << std::endl;
   return true;


}

void clusteringAnalyzerTest::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   bool _verbose = false;                    // do printouts of each section for debugging
   if(_verbose)std::cout << " -----------------Starting Event -----------------" << std::endl;
   eventnum++;

   edm::Handle<std::vector<pat::Jet> > smallJets;
   iEvent.getByToken(jetToken_, smallJets);

   edm::Handle<std::vector<pat::Jet> > fatJets;
   iEvent.getByToken(fatJetToken_, fatJets);

   //if(( (fatJets->end() - fatJets->begin()) < 2) || ( (smallJets->end() - smallJets->end()) <4) ) return;
   if(( fatJets->size() < 2) || ( smallJets->size() <4) ) return;

/*
   edm::ESHandle<JetCorrectorParametersCollection> JetCorParColl_AK4;//c-r
   iSetup.get<JetCorrectionsRecord>().get("AK4PFchs",JetCorParColl_AK4);//c-r
   JetCorrectorParameters const & JetCorPar_AK4 =( (*JetCorParColl_AK4)["Uncertainty"]);//c-r
   JetCorrectionUncertainty *jecUnc_AK4 = new JetCorrectionUncertainty(JetCorPar_AK4);//c-r

*/

   /////////////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   //////////////////////////////////    _sigMC area_ //////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   
 



   /////////////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   ///////////////////////////////    _shared area_   //////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////////////

/*
   if ( (runType.find("QCD") != std::string::npos) || (runType.find("TTbar") != std::string::npos) )
   {

      if(_verbose)std::cout << "before pileup" << std::endl;

      // I am presuming the PU scale factors are only for MC because they involve the number of "true" interactions

      ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
      /////////////////////////////////////////////////////////////////////_pileup_//////////////////////////////////////////////////////////////
      ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

      if(doPUSF)
      {
         edm::Handle<std::vector<PileupSummaryInfo> > PupInfo;
         iEvent.getByToken(puSummaryToken_, PupInfo);

         for (auto const& v : *PupInfo)
         {
            ntrueInt = v.getTrueNumInteractions();
            PU_eventWeight_nom  = PUjson_year->evaluate( {std::real(ntrueInt),"nominal"});
            PU_eventWeight_up  = PUjson_year->evaluate({std::real(ntrueInt),"up"});
            PU_eventWeight_down = PUjson_year->evaluate({std::real(ntrueInt),"down"}); 
         }  
      }
   }
*/
   if(_verbose)std::cout << "before AK4 jets" << std::endl;
   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
   ////////////////////////////////////////////////////////////////////_AK4 jets_/////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
   totHT = 0;
   lab_nAK4 = 0;
   nAK4 = 0;
   nAK4_uncut = 0;   
   std::vector<TLorentzVector> leadAK4Jets;

/*
   edm::Handle<double> rho;
   iEvent.getByToken(m_rho_token, rho);
*/
/*
   JME::JetResolution resolution_AK4               = JME::JetResolution::get(iSetup, "AK4PFchs_pt");                          //load JER stuff from global tag
   JME::JetResolutionScaleFactor resolution_sf_AK4 = JME::JetResolutionScaleFactor::get(iSetup, "AK4PFchs");
*/
   double MC_tagged = 1.0,  MC_notTagged = 1.0, data_tagged = 1.0, data_notTagged = 1.0; //these are for the bTagging SFs
   double data_tagged_up = 1.0, data_notTagged_up = 1.0; //these are for the bTagging SFs
   double data_tagged_down = 1.0, data_notTagged_down = 1.0; //these are for the bTagging SFs


   for(auto iJet = smallJets->begin(); iJet != smallJets->end(); iJet++) 
   {

      double AK4_sf_total = 1.0;

      if( (iJet->pt() < 15. ) || (!(iJet->isPFJet())) || ( abs(iJet->eta()) > 2.5 )) continue;   //don't even bother with these jets, corrections aren't going to bring these back into the range we are interest in




/*
      if(doJEC)
      {

         double AK4_JEC_corr_factor = 1.0;

         jecUnc_AK4->setJetEta( iJet->eta() );
         jecUnc_AK4->setJetPt( iJet->pt() );
         double AK4_JEC_uncertainty = fabs(jecUnc_AK4->getUncertainty(true));
         if(systematicType=="JEC_up")
         {
            AK4_JEC_corr_factor = 1 + AK4_JEC_uncertainty;
         }
         else if (systematicType=="JEC_down")
         {
            AK4_JEC_corr_factor = 1 - AK4_JEC_uncertainty;
         }   
         AK4_sf_total*= AK4_JEC_corr_factor;
      }*/

      ////////////////////////////////////////////////////////////////////////////////////////////////////////////
      //////////   _JET ENERGY RESOLUTION STUFF //////////////////////////////////////////////////////////////////
      ////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*
      if(doJER)
      {
         if ((runType.find("MC") != std::string::npos) || (runType.find("Suu") ) )
         {
            double AK4_JER_corr_factor = 1.0; // this won't be touched for data

            if(_verbose)std::cout << "doing JER" << std::endl;

            double sJER     = -9999.;    //JER scale factor
            double sigmaJER = -9999.;    //this is the "resolution" you get from the scale factors 
            
            //these are for getting the JER scale factors
            //JME::JetParameters parameters = {{JME::Binning::JetEta, AK8_JEC_corr_factor*iJet->eta()}, {JME::Binning::Rho, rho}};

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
            if(systematicType=="JER_up")
            {
               sJER = resolution_sf_AK4.getScaleFactor(parameters, Variation::UP);    // SF + 1 sigma uncertainty
            }
            else if (systematicType=="JER_down")
            {
               sJER = resolution_sf_AK4.getScaleFactor(parameters, Variation::DOWN);  // SF - 1 sigma uncertainty
            }
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
               AK4_JER_corr_factor = max(0., 1 + JERrand*sqrt(max(pow(sJER,2)-1,0.)));   //want to make sure this is truncated at 0
            }
            if(_verbose)std::cout << "finished with JER" << std::endl;
            AK4_sf_total*= AK4_JER_corr_factor;

         }

      }*/

      // create scaled jet object that will be used for cuts 
      pat::Jet corrJet(*iJet);
      LorentzVector corrJetP4(AK4_sf_total*iJet->px(),AK4_sf_total*iJet->py(),AK4_sf_total*iJet->pz(),AK4_sf_total*iJet->energy());
      corrJet.setP4(corrJetP4);


      btag_score_uncut[nAK4_uncut] = corrJet.bDiscriminator("pfDeepCSVJetTags:probb") + corrJet.bDiscriminator("pfDeepCSVJetTags:probbb");
      nAK4_uncut++;

      if((corrJet.pt() > 30.)&&(abs(corrJet.eta()) < 2.5)  )totHT+= abs(corrJet.pt() );
      
      if( (corrJet.pt()  <30.) || (!(corrJet.isPFJet())) || (!isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction())) ) continue;
      

      double deepJetScore = corrJet.bDiscriminator("pfDeepFlavourJetTags:probb") + corrJet.bDiscriminator("pfDeepFlavourJetTags:probbb")+ corrJet.bDiscriminator("pfDeepFlavourJetTags:problepb");

      if(_verbose)std::cout << "the year is " << year << " with working point value of " << deepjet_wp_tight << ". The hadronFlavour is " << corrJet.hadronFlavour() <<  " and deepjet score " << deepJetScore<< std::endl;
      

      //////////////////////////////////////////////////////////////////////////////////////////////////////////////
      ////////////////////////////////////// b tagging event weight stuff //////////////////////////////////////////
      //////////////////////////////////////////////////////////////////////////////////////////////////////////////
      /*
      if(doBtagSF)
      {
         if ( ( runType.find("MC") != std::string::npos  )  || (runType.find("Suu")) )    //only run this on MC (we won't have the hadron flavor stuff for data )
         {

            //these are the bins of the eff histogram you need to draw from
            // histogram size:  60, 0, 3000, 24, -2.4, 2.4)   

            int xbin = (int)(corrJet.pt()*60./3000.);
            int ybin = (int)((corrJet.eta()+2.4)*24/4.8);

            double SF, SF_up, SF_down;

            double bTag_eff_value;

            if(corrJet.hadronFlavour() == 0)   //light jets
            {
               bTag_eff_value = lightjet_eff->GetBinContent(xbin,ybin);
               SF = cset_corrector_light->evaluate({"central", "T", corrJet.hadronFlavour(), std::abs(corrJet.eta()), corrJet.pt()});
               SF_up   = cset_corrector_light->evaluate({"up_correlated", "T", corrJet.hadronFlavour(), std::abs(corrJet.eta()), corrJet.pt()});
               SF_down = cset_corrector_light->evaluate({"down_correlated", "T", corrJet.hadronFlavour(), std::abs(corrJet.eta()), corrJet.pt()});
               if(_verbose)std::cout << "Scale factor is " << SF << std::endl;
               if(deepJetScore > deepjet_wp_tight)
               {
                  MC_tagged *= bTag_eff_value;
                  data_tagged *= SF*bTag_eff_value;
                  data_tagged_up *= SF_up*bTag_eff_value;
                  data_tagged_down *= SF_down*bTag_eff_value;
                  if(_verbose)std::cout << "tagged light jet: MC_tagged/data_tagged: " << bTag_eff_value << ":" << SF*bTag_eff_value << std::endl;
               }
               else
               {
                  MC_notTagged *= (1- bTag_eff_value);
                  data_notTagged *= (1- SF*bTag_eff_value);
                  data_notTagged_up *= (1- SF_up*bTag_eff_value);
                  data_notTagged_down *= (1- SF_down*bTag_eff_value);
                  if(_verbose)std::cout << "untagged light jet: MC_notTagged/data_notTagged: " << (1- bTag_eff_value) << ":" << (1- SF*bTag_eff_value) << std::endl;
               }
            }
            else if(corrJet.hadronFlavour() == 4) //charm jets
            {
               bTag_eff_value = truecjet_eff->GetBinContent(xbin,ybin);
               SF = cset_corrector_bc->evaluate(   {"central", "T", corrJet.hadronFlavour(), std::abs(corrJet.eta()), corrJet.pt()});
               SF_up = cset_corrector_bc->evaluate({"up_correlated", "T", corrJet.hadronFlavour(), std::abs(corrJet.eta()), corrJet.pt()});
               SF_down = cset_corrector_bc->evaluate(   {"down_correlated", "T", corrJet.hadronFlavour(), std::abs(corrJet.eta()), corrJet.pt()});
               if(_verbose)std::cout << "Scale factor is " << SF << std::endl;

               if(deepJetScore > deepjet_wp_tight)
               {
                  MC_tagged  *= bTag_eff_value;
                  data_tagged *= SF*bTag_eff_value;
                  data_tagged_up *= bTag_eff_value;
                  data_tagged_down *= bTag_eff_value;
                  if(_verbose)std::cout << "tagged c jet: MC_tagged/data_tagged: " << bTag_eff_value << ":" << SF*bTag_eff_value << std::endl;


               }
               else
               {
                  MC_notTagged *= (1- bTag_eff_value);
                  data_notTagged *= (1- SF*bTag_eff_value);
                  data_notTagged_up *= (1- SF_up*bTag_eff_value);
                  data_notTagged_down *= (1- SF_down*bTag_eff_value);
                  if(_verbose)std::cout << "untagged c jet: MC_notTagged/data_notTagged: " << (1- bTag_eff_value) << ":" << (1- SF*bTag_eff_value) << std::endl;

               }
            }
            else if(corrJet.hadronFlavour() == 5) // b jets
            {
               bTag_eff_value = truebjet_eff->GetBinContent(xbin,ybin);
               SF = cset_corrector_bc->evaluate(   {"central", "T", corrJet.hadronFlavour(), std::abs(corrJet.eta()), corrJet.pt()});
               SF_up = cset_corrector_bc->evaluate({"up_correlated", "T", corrJet.hadronFlavour(), std::abs(corrJet.eta()), corrJet.pt()});
               SF_down = cset_corrector_bc->evaluate(   {"down_correlated", "T", corrJet.hadronFlavour(), std::abs(corrJet.eta()), corrJet.pt()});
               if(_verbose)std::cout << "Scale factor is " << SF << std::endl;

               if(deepJetScore > deepjet_wp_tight)
               {
                  MC_tagged  *= bTag_eff_value;
                  data_tagged *= SF*bTag_eff_value;
                  data_tagged_up *= SF_up*bTag_eff_value;
                  data_tagged_down *= SF_down*bTag_eff_value;
                  if(_verbose)std::cout << "tagged c jet: MC_tagged/data_tagged: " << bTag_eff_value << ":" << SF*bTag_eff_value << std::endl;

               }
               else
               {
                  MC_notTagged *= (1-bTag_eff_value);
                  data_notTagged *= (1-SF*bTag_eff_value);
                  data_notTagged_up *= (1-SF_up*bTag_eff_value);
                  data_notTagged_down  *= (1-SF_down*bTag_eff_value);
                  if(_verbose)std::cout << "untagged b jet: MC_notTagged/data_notTagged: " << (1- bTag_eff_value) << ":" << (1- SF*bTag_eff_value) << std::endl;

               }
            }
         }
      }*/
   
      lab_AK4_pt[nAK4] = corrJet.pt();
      AK4_mass[nAK4] = corrJet.mass();
      AK4_ptot[nAK4] = corrJet.p();
      AK4_eta[nAK4] = corrJet.eta();
      AK4_phi[nAK4] = corrJet.phi();
      AK4_bdisc[nAK4] = corrJet.bDiscriminator("pfDeepCSVJetTags:probb") + corrJet.bDiscriminator("pfDeepCSVJetTags:probbb");
      AK4_DeepJet_disc[nAK4] = deepJetScore;
      if(nAK4 < 4)
      {
         leadAK4Jets.push_back(TLorentzVector(corrJet.px(),corrJet.py(),corrJet.pz(),corrJet.energy()));
      }
      nAK4++;

   }

   ///////////////////// b tag event weights //////////////////////

   lab_nAK4 = nAK4;

   if(nAK4 <4)return;


   ///////////////////// b tag event weights //////////////////////
   if(doBtagSF)
   {
      bTag_eventWeight_nom =  (data_tagged*data_notTagged) / (MC_tagged*MC_notTagged);
      bTag_eventWeight_up  =  (data_tagged_up*data_notTagged_up) / (MC_tagged*MC_notTagged);    // MC portion doesn't contain any scale factor portion, so there is no "up" or "down"
      bTag_eventWeight_down = (data_tagged_down*data_notTagged_down) / (MC_tagged*MC_notTagged);    
   }


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

   if(_verbose)std::cout << "before MET loop" << std::endl;


   /*
   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////_MET_///////////////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

   edm::Handle<std::vector<pat::MET> > _totMET;
   iEvent.getByToken(metToken_, _totMET);
   for(auto iMET = _totMET->begin(); iMET != _totMET->end(); iMET++)
   {
      if(iMET->isPFMET())
      {
         totMET = iMET->pt();
      }
   }
   */

   if(_verbose)std::cout << "before AK8 jets" << std::endl;


   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
   ////////////////////////////////////////////////////////////_AK8 Jets_/////////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
   std::vector<reco::LeafCandidate> candsBoosted;   
   std::vector<reco::LeafCandidate> candsUnboosted;
   std::vector<fastjet::PseudoJet> superJetOne;        //jets for dot prduct #cos(theta) > 0
   std::vector<fastjet::PseudoJet> superJetTwo;       //jets for dot product #cos(theta) < 0
   std::vector<TLorentzVector> superJetOneLV;        //workaround for weird fastjet bug
   std::vector<TLorentzVector> superJetTwoLV;        //workaround for weird fastjet bug



/*
   edm::ESHandle<JetCorrectorParametersCollection> JetCorParColl;//c-r
   iSetup.get<JetCorrectionsRecord>().get("AK8PFPuppi",JetCorParColl);//c-r
   JetCorrectorParameters const & JetCorPar =( (*JetCorParColl)["Uncertainty"]);//c-r                    //load JEC stuff from global tag
   JetCorrectionUncertainty *jecUnc_ = new JetCorrectionUncertainty(JetCorPar);//c-r
*/

/*
   JME::JetResolution resolution = JME::JetResolution::get(iSetup, "AK8PF_pt");                          //load JER stuff from global tag
   JME::JetResolutionScaleFactor resolution_sf = JME::JetResolutionScaleFactor::get(iSetup, "AK8PF");
*/
   //Get AK8 jet info in order to get to COM frame and get a vector of all the (good) AK8 jet particles
   nfatjets = 0;
   eventTTbarCRFlag = 0;
   nfatjet_pre = 0;
   TLorentzVector allAK8(0,0,0,0);
   std::vector<TLorentzVector> leadAK8Jets;
   //diAK8Jet_mass
   double tot_jet_px=0,tot_jet_py=0,tot_jet_pz=0, tot_jet_E=0;
   for(auto iJet = fatJets->begin(); iJet != fatJets->end(); iJet++)    //Over AK8 Jets
   {


      if( (sqrt(pow(iJet->mass(),2)+pow(iJet->pt(),2)) < 100.) || (!(iJet->isPFJet())) || ( abs(iJet->eta()) > 2.4 )) continue;   //don't even bother with these jets
      
      double AK8_sf_total = 1.0;     // this scales jet/particle 4-vectors, compounds all scale factors

      
/*
      if(doJEC)
      {
         double AK8_JEC_corr_factor = 1.0;

         jecUnc_->setJetEta( iJet->eta() );
         jecUnc_->setJetPt( iJet->pt() );

         // JECs are already applied in cfg with updateJetCollection, this is for getting the uncertainties 
         double AK8_JEC_uncertainty = jecUnc_->getUncertainty(true);
         if(systematicType=="JEC_up")
         {
            AK8_JEC_corr_factor = 1 + AK8_JEC_uncertainty;
         }
         else if (systematicType=="JEC_down")
         {
            AK8_JEC_corr_factor = 1 - AK8_JEC_uncertainty;
         }
         AK8_sf_total*=AK8_JEC_corr_factor;

      }
*/

      ////////////////////////////////////////////////////////////////////////////////////////////////////////////
      //////////   _JET ENERGY RESOLUTION STUFF //////////////////////////////////////////////////////////////////
      ////////////////////////////////////////////////////////////////////////////////////////////////////////////
      /*
      if(doJER)
      {
         double AK8_JER_corr_factor = 1.0; // this won't be touched for data
         
         if( (runType.find("MC") != std::string::npos)|| (runType.find("Suu") ) ) //if((runType == "SigMC") || (runType == "QCDMC") || (runType == "TTbarMC") ) 
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
            if(systematicType=="JER_up")
            {
               sJER = resolution_sf.getScaleFactor(parameters, Variation::UP);    // SF + 1 sigma uncertainty
            }
            else if (systematicType=="JER_down")
            {
               sJER = resolution_sf.getScaleFactor(parameters, Variation::DOWN);  // SF - 1 sigma uncertainty
            }
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
      }*/

      // create scaled jet object that will be used for cuts 
      pat::Jet corrJet(*iJet);
      LorentzVector corrJetP4(AK8_sf_total*iJet->px(),AK8_sf_total*iJet->py(),AK8_sf_total*iJet->pz(),AK8_sf_total*iJet->energy());
      corrJet.setP4(corrJetP4);


      if(_verbose)  std::cout << "nominal p4: " << iJet->px()<< "," <<iJet->py() << "," << iJet->pz()<< "," << iJet->energy()<< std::endl;
      if(_verbose)  std::cout << "corrected p4: " << corrJet.px()<< "," <<corrJet.py() << "," << corrJet.pz()<< "," << corrJet.energy()<< std::endl;

      if((corrJet.pt() > 500.) && ((corrJet.isPFJet())) && (isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction())) && (corrJet.userFloat("ak8PFJetsPuppiSoftDropMass") > 45.)) nfatjet_pre++;

      if((sqrt(pow(corrJet.mass(),2)+pow(corrJet.pt(),2)) < 300.) || (!(corrJet.isPFJet())) || (!isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(),nfatjets)) || (corrJet.mass()< 0.)) continue; //userFloat("ak8PFJetsPuppiSoftDropMass")
      if(nfatjets < 2) leadAK8_mass[nfatjets] = corrJet.userFloat("ak8PFJetsPuppiSoftDropMass");
      jet_pt[nfatjets] = corrJet.pt();
      jet_eta[nfatjets] = corrJet.eta();
      jet_mass[nfatjets] = corrJet.mass();
      for (unsigned int iii=0; iii<iJet->numberOfDaughters();iii++)   // get all jet particles
      {
         const reco::Candidate* iJ = iJet->daughter(iii);
         const pat::PackedCandidate* candJetbegin = (pat::PackedCandidate*) iJ;
         double puppiweight = candJetbegin->puppiWeight();
         candsUnboosted.push_back(LeafCandidate(iJet->daughter(iii)->charge(), Particle::LorentzVector(AK8_sf_total*puppiweight*iJ->px(), AK8_sf_total*puppiweight*iJ->py(), AK8_sf_total*puppiweight*iJ->pz(), AK8_sf_total*puppiweight*iJ->energy())));
         tot_jet_px+=AK8_sf_total*puppiweight*candJetbegin->px();tot_jet_py+=AK8_sf_total*puppiweight*candJetbegin->py();tot_jet_pz+=AK8_sf_total*puppiweight*candJetbegin->pz();tot_jet_E+=AK8_sf_total*puppiweight*candJetbegin->energy();
      }
      if(nfatjets < 4)
      {
         leadAK8Jets.push_back(TLorentzVector(corrJet.px(),corrJet.py(),corrJet.pz(),corrJet.energy()));
      }
      nfatjets++;
   }
   event_reco_pt = sqrt(pow(tot_jet_px,2) + pow(tot_jet_py,2));

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
      //std::cout << diAK8Jet_mass[0] << "/" << diAK8Jet_mass[1] << " with diSJ mass " << fourAK8JetMass  << std::endl;
   }




   if (nfatjets < 2)return;

   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
   ////////////////////////////////////////////////////////////_Clustering_///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

   if(_verbose)std::cout << "before cluster" << std::endl;
   /////calculate COM frame boost////////////////////////////////////////////////////////////////////?????///////////////
   TVector3 totJetBeta = TVector3(tot_jet_px/tot_jet_E,tot_jet_py/tot_jet_E ,tot_jet_pz/tot_jet_E);


   //////////boost all jet particles into MPP frame//////////////////////////////////////////////////////////////////////
   std::vector<TLorentzVector> candsBoostedTLV_;
   double pxCOM = 0,pyCOM=0,pzCOM=0;
   for(auto iC = candsUnboosted.begin();iC != candsUnboosted.end(); iC++)
   {
      TLorentzVector iC_(iC->px(),iC->py(),iC->pz(),iC->energy());
      iC_.Boost(-totJetBeta.X(),-totJetBeta.Y(),-totJetBeta.Z());
      pxCOM+=iC_.Px();pyCOM+=iC_.Py();pzCOM+=iC_.Pz();
      candsBoostedTLV_.push_back( iC_ );

   }
   std::vector<fastjet::PseudoJet> candsBoostedPJ;
   for(auto iP=candsBoostedTLV_.begin();iP!=candsBoostedTLV_.end();iP++ )
   {
      candsBoostedPJ.push_back( fastjet::PseudoJet(iP->Px(),iP->Py(),iP->Pz(),iP->E()   ) );
   }

   ///////take all boosted particles in MPP frame and recluster, then sort these AK8 jets
   double R0 = 0.8;
    //fastjet::JetDefinition jet_def0(fastjet::antikt_algorithm, R0);
   fastjet::JetDefinition jet_def0(fastjet::cambridge_algorithm, R0);

   fastjet::ClusterSequence cs_jet0(candsBoostedPJ, jet_def0); 
   // shedding particles here -> can change this energy threshold, just changed it from 50. 
   std::vector<fastjet::PseudoJet> jetsFJ_jet0 = fastjet::sorted_by_E(cs_jet0.inclusive_jets(10.));
   double MPP_COM2_px = 0,MPP_COM2_py=0,MPP_COM2_pz =0,MPP_COM2_E = 0;
   int counter = 0;

   std::vector<TLorentzVector> candsBoostedTLV;   
   for (auto iJet=jetsFJ_jet0.begin(); iJet<jetsFJ_jet0.end(); iJet++)                             
   {   
      if (iJet->constituents().size() > 0)
      {
         for(auto iDaughter = iJet->constituents().begin(); iDaughter != iJet->constituents().end(); iDaughter++)
         {
            //std::cout << counter << " ";
            counter++;
            candsBoosted.push_back(reco::LeafCandidate(+1, reco::Candidate::LorentzVector(iDaughter->px(), iDaughter->py(), iDaughter->pz(), iDaughter->E())));
            candsBoostedTLV.push_back(TLorentzVector( iDaughter->px(), iDaughter->py(), iDaughter->pz(), iDaughter->E()    ));
            if(counter > 300)return;
         }
      }
      MPP_COM2_px+= iJet->px(); MPP_COM2_py+= iJet->py(); MPP_COM2_pz+=iJet->pz() ; MPP_COM2_E+=iJet->E() ;
   }
    TVector3 MPP_COM2 = TVector3(MPP_COM2_px/MPP_COM2_E,MPP_COM2_py/MPP_COM2_E ,MPP_COM2_pz/MPP_COM2_E);
    std::vector<reco::LeafCandidate> candsBoosted_MPPCOM2;   

    for(auto iPart = candsBoostedTLV.begin(); iPart != candsBoostedTLV.end(); iPart++)
    {
        iPart->Boost(-MPP_COM2.X(), -MPP_COM2.Y(), -MPP_COM2.Z());
        candsBoosted_MPPCOM2.push_back( reco::LeafCandidate(+1, reco::Candidate::LorentzVector( iPart->Px(),iPart->Py(),iPart->Pz(),iPart->E()   ) )       );
    }

    Thrust thrust_(candsBoosted.begin(), candsBoosted.end());                             //thrust axis in COM frame
    math::XYZVector thrustAxis = thrust_.axis();
    TVector3 thrust_vector(thrustAxis.X(),thrustAxis.Y(),thrustAxis.Z());
   


///////////////////////////get vector of sorted superjets//////////////////////////////////////////////////////   
    if(_verbose)std::cout << "sorted jets" << std::endl;

    std::vector<TLorentzVector> negSuperJet_preSort;
    std::vector<TLorentzVector> posSuperJet_preSort;
    std::vector<TLorentzVector> miscJets;

    //std::vector<TLorentzVector> negSuperJet_alt;
    //std::vector<TLorentzVector> posSuperJet_alt;
    //std::vector<TLorentzVector> miscJets_alt;
    for (auto iJet=jetsFJ_jet0.begin(); iJet<jetsFJ_jet0.end(); iJet++)                             
    {
        TLorentzVector candJet(iJet->px(),iJet->py(),iJet->pz(),iJet->E());
        TVector3 candJet_vec = candJet.Vect();
        double cosAngle = cos(candJet_vec.Angle(thrust_vector));
        if    (cosAngle < -0.85) negSuperJet_preSort.push_back(candJet);  
        else if(cosAngle > 0.85) posSuperJet_preSort.push_back(candJet);
        else{ miscJets.push_back(candJet); }
    }
   nCombinations = 0;
   if(_verbose)std::cout << "enter sort jets" << std::endl;



    std::vector<TLorentzVector> negSuperJet;
    std::vector<TLorentzVector> posSuperJet;



    /// the problem is with more than 6 misc jets ... why is this happening? need to check sortJets








   if(( miscJets.size() > 0) )
   {   
      sortJets testing(negSuperJet_preSort,posSuperJet_preSort,miscJets);
      negSuperJet = testing.finalSuperJet1;
      posSuperJet = testing.finalSuperJet2;

   }
   /*
   std::cout << "left sort jets" << std::endl;

   std::cout << "There are " << nfatjets << "/" << nfatjet_pre << " AK8 jets in this event ..." << std::endl;
   
   std::cout << "There are " << jetsFJ_jet0.size() << " reclustered AK8 jets in the MPP frame" << std::endl;

   std::cout << "there are " << miscJets.size() << "/" <<posSuperJet.size() << "/" << negSuperJet.size() << " miscJets/posSJ/negSJ" << std::endl;

   std::cout<< "There are " << negSuperJet_preSort.size() << "/" << posSuperJet_preSort.size() << " negative/positive perSort jets" << std::endl;
   */




   if( (negSuperJet.size() < 1 ) || (posSuperJet.size()<1)   ) 
   {
      return;
   }
   TLorentzVector SJ1(0,0,0,0);
   TLorentzVector SJ2(0,0,0,0);

   for(unsigned int iii = 0; iii < negSuperJet.size();iii++)
   {
      SJ2+=negSuperJet[iii];
   }

   for(unsigned int iii = 0; iii < posSuperJet.size();iii++)
   {
      SJ1+=posSuperJet[iii];
   }
///////////////////////////////////////////////////////////////////////////////////////////

 /// don't need this any more with new technique
    //get vector of pseudo jet particles for all particles in each superjet, one per superjet
    for (auto iJet=jetsFJ_jet0.begin(); iJet<jetsFJ_jet0.end(); iJet++)                             
    {   
        TLorentzVector candJet(iJet->px(),iJet->py(),iJet->pz(),iJet->E());

        int SJMatch = 0;
        if      (isMatchedtoSJ(posSuperJet,candJet)) SJMatch = 1;
        else if (isMatchedtoSJ(negSuperJet,candJet)) SJMatch = 2;
        else if(SJMatch == 0) std::cout << "Something didn't work... " << std::endl;

        //sort jet particles into either SuperJet 1 or SuperJet 2
        if (iJet->constituents().size() > 0)
        {
            for(auto iJ = iJet->constituents().begin(); iJ != iJet->constituents().end(); iJ++)
            {  
                if     (SJMatch==1)superJetOneLV.push_back(TLorentzVector(iJ->px(),iJ->py(),iJ->pz(),iJ->E()));
                else if(SJMatch==2)superJetTwoLV.push_back(TLorentzVector(iJ->px(),iJ->py(),iJ->pz(),iJ->E()));
            }
         }        
   }

   for(auto iPart = superJetOneLV.begin(); iPart != superJetOneLV.end(); iPart++)
   {
         superJetOne.push_back(fastjet::PseudoJet(iPart->Px(),iPart->Py(),iPart->Pz(),iPart->E()));
   }
   for(auto iPart = superJetTwoLV.begin(); iPart != superJetTwoLV.end(); iPart++)
   {
        superJetTwo.push_back(fastjet::PseudoJet(iPart->Px(),iPart->Py(),iPart->Pz(),iPart->E()));
   }



   ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
   ////////////////////////////////////////// superjet analysis /////////////////////////////////////////////////
   //////////////////////////////////////////////////////////////////////////////////////////////////////////////


   if(_verbose)std::cout << "Starting superjet loop." << std::endl;
   double superJetpx,superJetpy,superJetpz,superJetE;
   std::vector<std::vector<fastjet::PseudoJet>> superJets;
   superJets.push_back(superJetOne);
   superJets.push_back(superJetTwo);
   nSuperJets = 0;   
   tot_nAK4_70 = 0; 
   tot_nAK4_50 = 0;
   tot_mpp_AK4 = 0;
   double diSuperJet_E = 0, diSuperJet_px = 0,diSuperJet_py = 0,diSuperJet_pz =0;
   double diSuperJet_E_100 = 0, diSuperJet_px_100 = 0,diSuperJet_py_100 = 0,diSuperJet_pz_100 =0;
   if(_verbose)std::cout << "about to loop over superjets" << std::endl;

   for(auto iSJ = superJets.begin();iSJ!= superJets.end();iSJ++)
   {
     if(_verbose)std::cout << "starting superjet" << nSuperJets <<std::endl;

      ////////////////////////inside superjet loop //////////////////
      ///////         fill BESTmap for superjet ////////////////////

      /////////////////////////////////////////////////////////////
      //////get BEST scores for superjet /////////
      BESTmap.clear();
      BESTmap["tot_pt"] = allAK8.Pt();
      BESTmap["tot_HT"] = totHT;


      std::vector<float> BESTScores;

      if (!fillSJVars(BESTmap, *iSJ,nSuperJets))    //if this fails somehow, event is skipped
      {
         return;
      }

      BESTScores = BEST_->getPrediction(BESTmap);
      ///store BEST scores in tree
      int decision = std::distance(BESTScores.begin(), std::max_element(BESTScores.begin(), BESTScores.end() ) );

      if (nSuperJets == 0)
      {
         SJ1_BEST_scores[0] = (double) BESTScores[0];
         SJ1_BEST_scores[1] = (double) BESTScores[1];
         SJ1_BEST_scores[2] = (double) BESTScores[2];
         SJ1_BEST_scores[3] = (double) BESTScores[3];
         //SJ1_BEST_scores[4] = (double) BESTScores[4];
         SJ1_decision = decision;
      }
      else if (nSuperJets == 1)
      {
         SJ2_BEST_scores[0] = (double) BESTScores[0];
         SJ2_BEST_scores[1] = (double) BESTScores[1];
         SJ2_BEST_scores[2] = (double) BESTScores[2];
         SJ2_BEST_scores[3] = (double) BESTScores[3];
         //SJ2_BEST_scores[4] = (double) BESTScores[4];
         SJ2_decision = decision;
      }


      superJetpx=0;superJetpy=0;superJetpz=0;superJetE=0;
      for(auto iP = iSJ->begin();iP != iSJ->end();iP++)
      {
         superJetpx+=iP->px();superJetpy+=iP->py();superJetpz+=iP->pz();superJetE +=iP->E();
         diSuperJet_E +=iP->E();diSuperJet_px+=iP->px();diSuperJet_py+=iP->py();diSuperJet_pz+=iP->pz();
      }
      superJet_mass[nSuperJets] = sqrt(pow(superJetE,2)-pow(superJetpx,2)-pow(superJetpy,2)-pow(superJetpz,2));
      TLorentzVector superJetTLV(superJetpx,superJetpy,superJetpz,superJetE);    //Lorentz vector representing jet axis -> now minimize the parallel momentum
      
      //double betaMag = calcMPP(superJetTLV);
      double betaMag = sqrt(pow(superJetpx,2)+pow(superJetpy,2)+pow(superJetpz,2))/superJetE;

      std::vector<fastjet::PseudoJet> boostedSuperJetPart;
      //boost particles in SuperJet to MPP frame
      for(auto iP = iSJ->begin();iP != iSJ->end();iP++)
      {
         TLorentzVector iP_(iP->px(),iP->py(),iP->pz(),iP->E());
         iP_.Boost(-betaMag*superJetTLV.Px()/superJetTLV.P(),-betaMag*superJetTLV.Py()/superJetTLV.P(),-betaMag*superJetTLV.Pz()/superJetTLV.P());
         boostedSuperJetPart.push_back(fastjet::PseudoJet(iP_.Px(),iP_.Py(),iP_.Pz(),iP_.E()));
      }

      ///reclustering SuperJet that is now boosted into the MPP frame
      double R = 0.4;
      //fastjet::JetDefinition jet_def(fastjet::antikt_algorithm, R);
      fastjet::JetDefinition jet_def(fastjet::cambridge_algorithm, R);
      fastjet::ClusterSequence cs_jet(boostedSuperJetPart, jet_def); 
      std::vector<fastjet::PseudoJet> jetsFJ_jet = fastjet::sorted_by_E(cs_jet.inclusive_jets(0.0));

      double SJ_50_px = 0, SJ_50_py=0,SJ_50_pz=0,SJ_50_E=0;
      double SJ_70_px = 0, SJ_70_py=0,SJ_70_pz=0,SJ_70_E=0;
      double SJ_100_px = 0, SJ_100_py=0,SJ_100_pz=0,SJ_100_E=0;
      double SJ_125_px = 0, SJ_125_py=0,SJ_125_pz=0,SJ_125_E=0;
      double SJ_150_px = 0, SJ_150_py=0,SJ_150_pz=0,SJ_150_E=0;
      double SJ_200_px = 0, SJ_200_py=0,SJ_200_pz=0,SJ_200_E=0;
      double SJ_300_px = 0, SJ_300_py=0,SJ_300_pz=0,SJ_300_E=0;
      double SJ_400_px = 0, SJ_400_py=0,SJ_400_pz=0,SJ_400_E=0;
      double SJ_600_px = 0, SJ_600_py=0,SJ_600_pz=0,SJ_600_E=0;
      double SJ_800_px = 0, SJ_800_py=0,SJ_800_pz=0,SJ_800_E=0;
      double SJ_1000_px = 0, SJ_1000_py=0,SJ_1000_pz=0,SJ_1000_E=0;

      /*
         double SJ1_AK41_px, SJ1_AK41_py, SJ1_AK41_pz, SJ1_AK41_E;
         double SJ1_AK42_px, SJ1_AK42_py, SJ1_AK42_pz, SJ1_AK42_E;
         double SJ1_AK43_px, SJ1_AK43_py, SJ1_AK43_pz, SJ1_AK43_E;
         double SJ1_AK44_px, SJ1_AK44_py, SJ1_AK44_pz, SJ1_AK44_E;

         double SJ2_AK41_px, SJ2_AK41_py, SJ2_AK41_pz, SJ2_AK41_E;
         double SJ2_AK42_px, SJ2_AK42_py, SJ2_AK42_pz, SJ2_AK42_E;
         double SJ2_AK43_px, SJ2_AK43_py, SJ2_AK43_pz, SJ2_AK43_E;
         double SJ2_AK44_px, SJ2_AK44_py, SJ2_AK44_pz, SJ2_AK44_E;
      */


      SJ_nAK4_50[nSuperJets] = 0,  SJ_nAK4_70[nSuperJets] =0,SJ_nAK4_100[nSuperJets] = 0,SJ_nAK4_125[nSuperJets] = 0,SJ_nAK4_150[nSuperJets] = 0,SJ_nAK4_200[nSuperJets] = 0,SJ_nAK4_300[nSuperJets] = 0,SJ_nAK4_400[nSuperJets] = 0,SJ_nAK4_1000[nSuperJets] = 0;
      SJ_nAK4_600[nSuperJets] = 0, SJ_nAK4_800[nSuperJets] = 0;
      for (auto iPJ=jetsFJ_jet.begin(); iPJ<jetsFJ_jet.end(); iPJ++)                             
      {

         if(nSuperJets == 0)  //SJ1
         {
            SJ1_AK4_px[tot_mpp_AK4] = iPJ->px();
            SJ1_AK4_py[tot_mpp_AK4] = iPJ->py();
            SJ1_AK4_pz[tot_mpp_AK4] = iPJ->pz();
            SJ1_AK4_E[tot_mpp_AK4]  = iPJ->E();           
         }
         else if(nSuperJets == 1) //SJ2
         {
            SJ2_AK4_px[tot_mpp_AK4] = iPJ->px();
            SJ2_AK4_py[tot_mpp_AK4] = iPJ->py(); 
            SJ1_AK4_pz[tot_mpp_AK4] = iPJ->pz();
            SJ2_AK4_E[tot_mpp_AK4]  = iPJ->E();          
         }

         AK4_E[tot_mpp_AK4]= iPJ->E();
         if(iPJ->E()>50.)
         {
            SJ_AK4_50_mass[tot_nAK4_50] = iPJ->m();
            SJ_50_px+=iPJ->px();SJ_50_py+=iPJ->py();SJ_50_pz+=iPJ->pz();SJ_50_E+=iPJ->E();
            SJ_nAK4_50[nSuperJets]++;
            tot_nAK4_50++;
         }
         if(iPJ->E()> 70.)
         {
            SJ_AK4_70_mass[tot_nAK4_70] = iPJ->m();
            SJ_70_px+=iPJ->px();SJ_70_py+=iPJ->py();SJ_70_pz+=iPJ->pz();SJ_70_E+=iPJ->E();
            SJ_nAK4_70[nSuperJets]++;
            tot_nAK4_70++;
         }
         if(iPJ->E()>100)
         {
            SJ_100_px+=iPJ->px();SJ_100_py+=iPJ->py();SJ_100_pz+=iPJ->pz();SJ_100_E+=iPJ->E();
            diSuperJet_E_100 +=iPJ->E();diSuperJet_px_100+=iPJ->px();diSuperJet_py_100+=iPJ->py();diSuperJet_pz_100+=iPJ->pz();

            SJ_nAK4_100[nSuperJets]++; 
         }
         if(iPJ->E()>125)
         {
            SJ_125_px+=iPJ->px();SJ_125_py+=iPJ->py();SJ_125_pz+=iPJ->pz();SJ_125_E+=iPJ->E();

            SJ_nAK4_125[nSuperJets]++; 
         }
         if(iPJ->E()>150)
         {
            SJ_150_px+=iPJ->px();SJ_150_py+=iPJ->py();SJ_150_pz+=iPJ->pz();SJ_150_E+=iPJ->E();

            SJ_nAK4_150[nSuperJets]++; 
         }
         if(iPJ->E()>200)
         {
            SJ_200_px+=iPJ->px();SJ_200_py+=iPJ->py();SJ_200_pz+=iPJ->pz();SJ_200_E+=iPJ->E();

            SJ_nAK4_200[nSuperJets]++; 
         }
         if(iPJ->E()>300)
         {
            SJ_300_px+=iPJ->px();SJ_300_py+=iPJ->py();SJ_300_pz+=iPJ->pz();SJ_300_E+=iPJ->E();

            SJ_nAK4_300[nSuperJets]++; 
         }
         if(iPJ->E()>400)
         {
            SJ_400_px+=iPJ->px();SJ_400_py+=iPJ->py();SJ_400_pz+=iPJ->pz();SJ_400_E+=iPJ->E();

            SJ_nAK4_400[nSuperJets]++; 
         }
         if(iPJ->E()>600)
         {
            SJ_600_px+=iPJ->px();SJ_600_py+=iPJ->py();SJ_600_pz+=iPJ->pz();SJ_600_E+=iPJ->E();

            SJ_nAK4_600[nSuperJets]++; 
         }
         if(iPJ->E()>800)
         {
            SJ_800_px+=iPJ->px();SJ_800_py+=iPJ->py();SJ_800_pz+=iPJ->pz();SJ_800_E+=iPJ->E();

            SJ_nAK4_800[nSuperJets]++; 
         }
         if(iPJ->E()>1000)
         {
            SJ_1000_px+=iPJ->px();SJ_1000_py+=iPJ->py();SJ_1000_pz+=iPJ->pz();SJ_1000_E+=iPJ->E();

            SJ_nAK4_1000[nSuperJets]++; 
         }
         tot_mpp_AK4++;
      }

      SJ_mass_50[nSuperJets]= sqrt(pow(SJ_50_E,2)-pow(SJ_50_px,2)-pow(SJ_50_py,2)-pow(SJ_50_pz,2));
      SJ_mass_70[nSuperJets]= sqrt(pow(SJ_70_E,2)-pow(SJ_70_px,2)-pow(SJ_70_py,2)-pow(SJ_70_pz,2));
      SJ_mass_100[nSuperJets]= sqrt(pow(SJ_100_E,2)-pow(SJ_100_px,2)-pow(SJ_100_py,2)-pow(SJ_100_pz,2));
      SJ_mass_125[nSuperJets]= sqrt(pow(SJ_125_E,2)-pow(SJ_125_px,2)-pow(SJ_125_py,2)-pow(SJ_125_pz,2));
      SJ_mass_150[nSuperJets]= sqrt(pow(SJ_150_E,2)-pow(SJ_150_px,2)-pow(SJ_150_py,2)-pow(SJ_150_pz,2));
      SJ_mass_200[nSuperJets]= sqrt(pow(SJ_200_E,2)-pow(SJ_200_px,2)-pow(SJ_200_py,2)-pow(SJ_200_pz,2));
      SJ_mass_300[nSuperJets]= sqrt(pow(SJ_300_E,2)-pow(SJ_300_px,2)-pow(SJ_300_py,2)-pow(SJ_300_pz,2));
      SJ_mass_400[nSuperJets]= sqrt(pow(SJ_400_E,2)-pow(SJ_400_px,2)-pow(SJ_400_py,2)-pow(SJ_400_pz,2));
      SJ_mass_600[nSuperJets]= sqrt(pow(SJ_600_E,2)-pow(SJ_600_px,2)-pow(SJ_600_py,2)-pow(SJ_600_pz,2));
      SJ_mass_800[nSuperJets]= sqrt(pow(SJ_800_E,2)-pow(SJ_800_px,2)-pow(SJ_800_py,2)-pow(SJ_800_pz,2));
      SJ_mass_1000[nSuperJets]= sqrt(pow(SJ_1000_E,2)-pow(SJ_1000_px,2)-pow(SJ_1000_py,2)-pow(SJ_1000_pz,2));

      boostedSuperJetPart.clear();   //shouldn't be needed, just in case
      if(_verbose)std::cout << "ending superjet" << nSuperJets <<std::endl;
      nSuperJets++; 
   }
   if(_verbose)std::cout << "calculating disuperjet masses" <<std::endl;
   diSuperJet_mass = sqrt(pow(diSuperJet_E,2)-pow(diSuperJet_px,2)-pow(diSuperJet_py,2)-pow(diSuperJet_pz,2));
   diSuperJet_mass_100 = sqrt(pow(diSuperJet_E_100,2)-pow(diSuperJet_px_100,2)-pow(diSuperJet_py_100,2)-pow(diSuperJet_pz_100,2));
   if(_verbose)std::cout << "clear superjets"  <<std::endl;

   superJetOne.clear();
   superJetTwo.clear();
   if(_verbose)std::cout << "Filling the tree" <<std::endl;
   tree->Fill();
   if(_verbose)std::cout << " -----------------event end -----------------" << std::endl;
}   
DEFINE_FWK_MODULE(clusteringAnalyzerTest);
//_bottom_
