////////////////////////////HELP////////////////////////////////
//////////////Uses new clustering algorithm to capture heavy resonance jet substructure//////////////
////////////////Last updated Feb 23 2021 ////////////////////////////////////////////////////////////

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
#include<TRandom3.h>
#include "TH2.h"

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
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
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
#include "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_29/src/sortJets.h"
#include "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_29/src/BESTtoolbox.h"
#include "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_29/src/CacheHandler.h"
//#include "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_29/src/analyzers/analyzers/src/CacheHandler.cc"
#include "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_29/src/BESTEvaluation.h"
using namespace reco;
typedef math::XYZTLorentzVector LorentzVector;
typedef math::XYZVector Vector;

class calculateBtagEfficiencyMaps : public edm::EDAnalyzer 
{
public:
   explicit calculateBtagEfficiencyMaps(const edm::ParameterSet&);
private:
   virtual void analyze(const edm::Event&, const edm::EventSetup&);

   bool isHEM(const float jet_eta, const float jet_phi);
   std::string returnJECFile(std::string year, std::string systematicType, std::string runType);
   double getJECUncertaintyFromSources(double pt, double eta);
   bool isgoodjet(const float eta, const float NHF,const float NEMF, const size_t NumConst,const float CHF,const int CHM, const float MUF, const float CEMF,bool jetPUid, const float iJet_pt);
   bool isgoodjet(const float eta, const float NHF,const float NEMF, const size_t NumConst,const float CHF,const int CHM, const float MUF, const float CEMF, int nfatjets);
   const reco::Candidate* parse_chain(const reco::Candidate* cand);
   
   std::string runType;
   std::string year;

   edm::EDGetTokenT<std::vector<pat::Jet>> fatJetToken_;
   edm::EDGetTokenT<std::vector<reco::GenParticle>> genPartToken_; 
   edm::EDGetTokenT<std::vector<pat::Jet>> jetToken_;
   edm::EDGetTokenT<std::vector<pat::MET>> metToken_;
   edm::EDGetTokenT<std::vector<PileupSummaryInfo> > puSummaryToken_;
   edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
   edm::EDGetTokenT<std::vector<pat::Muon>> muonToken_;
   edm::EDGetTokenT<std::vector<pat::Electron>> electronToken_;
   edm::EDGetTokenT<std::vector<pat::Tau>> tauToken_;
   edm::EDGetTokenT<double> m_rho_token;
   //edm::FileInPath JECUncert_AK4_path;

   std::map<std::string, std::map<std::string, std::string>> file_map;

   //JetCorrectionUncertainty *jecUnc_AK4;
   
   bool doPUID;

   TTree * tree;


   TH2F *h_nLightJets_tight;
   TH2F *h_nTruebJets_tight;
   TH2F *h_nTruecJets_tight; 

   TH2F *h_nLightJets_tight_btagged; 
   TH2F *h_nTruebJets_tight_btagged; 
   TH2F *h_nTruecJets_tight_btagged; 

   TH2F *h_nLightJets_med;
   TH2F *h_nTruebJets_med;
   TH2F *h_nTruecJets_med; 

   TH2F *h_nLightJets_med_btagged; 
   TH2F *h_nTruebJets_med_btagged; 
   TH2F *h_nTruecJets_med_btagged; 


   TRandom3 *randomNum = new TRandom3(); // for JERs

   std::map<std::string, std::unique_ptr<JetCorrectionUncertainty>> JEC_map_AK4;   // contains the correctors for each uncertainty source
   
   //JetCorrectionUncertainty *jecUnc_AK4;


   std::vector<std::string> systematics;
   std::vector<std::string> uncertainty_sources; // will be reused


   //int numberOfJetsRunOver = 0;

};

//// return back the JEC file for a given systematic, year, and jet type
std::string calculateBtagEfficiencyMaps::returnJECFile(std::string year, std::string systematicType, std::string runType)
{
   std::string data_type = "MC";
   std::string jet_str = "AK4PFchs";

   return  ("SuuToChiChi_analysis_software/data/JEC_uncertainty_sources/" + file_map[year][data_type] + "/" + file_map[year][data_type] + "_UncertaintySources_" +jet_str  + ".txt" ).c_str();
}


//_constructor_
calculateBtagEfficiencyMaps::calculateBtagEfficiencyMaps(const edm::ParameterSet& iConfig)

{

   runType        = iConfig.getParameter<std::string>("runType");
   year           = iConfig.getParameter<std::string>("year");

   //JECUncert_AK4_path = iConfig.getParameter<edm::FileInPath>("JECUncert_AK4_path");

   //jecUnc_AK4 = new JetCorrectionUncertainty(JECUncert_AK4_path.fullPath().c_str());

   int NBINSX;
   double PTMAX;
   if(runType.find("Suu") != std::string::npos)
   {
      NBINSX = 40;
      PTMAX  = 6000.;  // best to keep bin sizes the same between these
         // change this to an even wider range?
   }
   else
   {
      NBINSX = 40;
      PTMAX  = 6000.;  // best to keep bin sizes the same between these
   }

   // tight WP
   h_nLightJets_tight = new TH2F("h_nLightJets_tight" ,"total number of true light jets; jet p_{T} [GeV];jet eta", NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruebJets_tight = new TH2F("h_nTruebJets_tight" ,"total number of true b jets; jet p_{T} [GeV];jet eta",  NBINSX,0, PTMAX, 18, -2.4, 2.4);
   h_nTruecJets_tight = new TH2F("h_nTruecJets_tight" ,"total number of true c jets; jet p_{T} [GeV];jet eta", NBINSX ,0, PTMAX, 18, -2.4, 2.4);

   h_nLightJets_tight_btagged = new TH2F("h_nLightJets_tight_btagged" ,"total number of true light jets that are b-tagged; jet p_{T} [GeV];jet eta", NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruebJets_tight_btagged = new TH2F("h_nTruebJets_tight_btagged" ,"total number of true b jets that are b-tagged; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruecJets_tight_btagged = new TH2F("h_nTruecJets_tight_btagged" ,"total number of true c jets that are b-tagged; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);

   // med WP
   h_nLightJets_med = new TH2F("h_nLightJets_med" ,"total number of true light jets; jet p_{T} [GeV];jet eta", NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruebJets_med = new TH2F("h_nTruebJets_med" ,"total number of true b jets; jet p_{T} [GeV];jet eta",  NBINSX,0, PTMAX, 18, -2.4, 2.4);
   h_nTruecJets_med = new TH2F("h_nTruecJets_med" ,"total number of true c jets; jet p_{T} [GeV];jet eta", NBINSX ,0, PTMAX, 18, -2.4, 2.4);

   h_nLightJets_med_btagged = new TH2F("h_nLightJets_med_btagged" ,"total number of true light jets that are b-tagged; jet p_{T} [GeV];jet eta", NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruebJets_med_btagged = new TH2F("h_nTruebJets_med_btagged" ,"total number of true b jets that are b-tagged; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruecJets_med_btagged = new TH2F("h_nTruecJets_med_btagged" ,"total number of true c jets that are b-tagged; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);


   doPUID = iConfig.getParameter<bool>("doPUID");
   edm::InputTag fixedGridRhoAllTag_ = edm::InputTag("fixedGridRhoAll", "", "RECO");   
   fatJetToken_ = consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("fatJetCollection"));
   jetToken_    = consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("jetCollection"));
   m_rho_token  = consumes<double>(fixedGridRhoAllTag_);
   edm::Service<TFileService> fs;      

   h_nLightJets_tight = fs->make<TH2F>("h_nLightJets_tight" ,"total number of true light jets; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruebJets_tight = fs->make<TH2F>("h_nTruebJets_tight" ,"total number of true b jets; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruecJets_tight = fs->make<TH2F>("h_nTruecJets_tight" ,"total number of true c jets; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);

   h_nLightJets_tight_btagged = fs->make<TH2F>("h_nLightJets_tight_btagged" ,"total number of true light jets that are b-tagged; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruebJets_tight_btagged = fs->make<TH2F>("h_nTruebJets_tight_btagged" ,"total number of true b jets that are b-tagged; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruecJets_tight_btagged = fs->make<TH2F>("h_nTruecJets_tight_btagged" ,"total number of true c jets that are b-tagged; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);

   h_nLightJets_med = fs->make<TH2F>("h_nLightJets_med" ,"total number of true light jets; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruebJets_med = fs->make<TH2F>("h_nTruebJets_med" ,"total number of true b jets; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruecJets_med = fs->make<TH2F>("h_nTruecJets_med" ,"total number of true c jets; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);

   h_nLightJets_med_btagged = fs->make<TH2F>("h_nLightJets_med_btagged" ,"total number of true light jets that are b-tagged; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruebJets_med_btagged = fs->make<TH2F>("h_nTruebJets_med_btagged" ,"total number of true b jets that are b-tagged; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruecJets_med_btagged = fs->make<TH2F>("h_nTruecJets_med_btagged" ,"total number of true c jets that are b-tagged; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);


 /////////////////////////////////////////////////////////////////////////
   //////////////// create file maps for the JEC sources ///////////////////

   file_map["2015"]["MC"] = "Summer19UL16APV_V9_MC";
   file_map["2016"]["MC"] = "Summer19UL16_V9_MC";
   file_map["2017"]["MC"] = "Summer19UL17_V6_MC";
   file_map["2018"]["MC"] = "Summer19UL18_V5_MC";

   file_map["2015"]["dataBCD"] = "Summer19UL16APV_RunBCD_V7_DATA";
   file_map["2015"]["dataEF"]  = "Summer19UL16APV_RunEF_V7_DATA";
   file_map["2016"]["dataFGH"] = "Summer19UL16_RunFGH_V7_DATA";

   file_map["2017"]["dataB"] = "Summer19UL17_RunB_V6_DATA";
   file_map["2017"]["dataC"] = "Summer19UL17_RunC_V6_DATA";
   file_map["2017"]["dataD"] = "Summer19UL17_RunD_V6_DATA";
   file_map["2017"]["dataE"] = "Summer19UL17_RunE_V6_DATA";
   file_map["2017"]["dataF"] = "Summer19UL17_RunF_V6_DATA";

   file_map["2018"]["dataA"] = "Summer19UL18_RunA_V6_DATA";
   file_map["2018"]["dataB"] = "Summer19UL18_RunB_V6_DATA";
   file_map["2018"]["dataC"] = "Summer19UL18_RunC_V6_DATA";
   file_map["2018"]["dataD"] = "Summer19UL18_RunD_V6_DATA";



   systematics = 
   {
      "JEC",
      "BBEC1_year",
      "Absolute_year",
      "RelativeSample_year",
      "FlavorQCD",
      "RelativeBal",
      "AbsoluteCal",
      "AbsolutePU",
      "Absolute",
      "AbsoluteTheory",
      "AbsoluteScale",
      "Fragmentation",
      "AbsoluteMPFBias",
      "RelativeFSR"
   };



   for( auto systematic: systematics)
   {
       edm::FileInPath  JEC_source_text_AK4 = (edm::FileInPath )returnJECFile(year, systematic, runType );

      // load in the JetCorrectors for each uncertainty source for the given reduced uncertainty source
      if ((systematic.find("JEC") != std::string::npos) )               uncertainty_sources = {"Total"};
      else if ((systematic.find("BBEC1_year") != std::string::npos) )          uncertainty_sources = {"RelativeJEREC1","RelativePtEC1","RelativeStatEC"};
      else if ((systematic.find("Absolute_year") != std::string::npos) )       uncertainty_sources = {"AbsoluteStat","RelativeStatFSR","TimePtEta"};
      else if ((systematic.find("RelativeSample_year") != std::string::npos))  uncertainty_sources = {"RelativeSample"};
      else if ((systematic.find("FlavorQCD") != std::string::npos) )           uncertainty_sources = {"FlavorQCD"};
      else if ((systematic.find("RelativeBal") != std::string::npos))          uncertainty_sources = {"RelativeBal"};
      else if ((systematic.find("Absolute") != std::string::npos) )            uncertainty_sources = {"AbsoluteMPFBias", "AbsoluteScale", "Fragmentation","PileUpDataMC","PileUpPtRef","RelativeFSR","SinglePionECAL","SinglePionHCAL"};

      for(const auto &uncertainty_source: uncertainty_sources)
      {

         //std::cout << "Initializing source_parameters_reduced_AK4 for systematic / uncertainty source " << systematic << "/" << uncertainty_source << std::endl;
         JetCorrectorParameters source_parameters_reduced_AK4(JEC_source_text_AK4.fullPath().c_str(), uncertainty_source);
         //std::cout << "source_uncertainty_reduced_AK4 for systematic / uncertainty source " << systematic << "/" << uncertainty_source << std::endl;
         std::unique_ptr<JetCorrectionUncertainty> source_uncertainty_reduced_AK4(new JetCorrectionUncertainty(source_parameters_reduced_AK4));
         //std::cout << "moving uncertainty_source:source_uncertainty_reduced_AK4 to JEC_map_AK4 for systematic / uncertainty source " << systematic << "/" << uncertainty_source << std::endl;
         JEC_map_AK4.emplace(uncertainty_source, std::move(source_uncertainty_reduced_AK4));
      }
   }

   


}


bool calculateBtagEfficiencyMaps::isgoodjet(const float eta, const float NHF,const float NEMF, const size_t NumConst,const float CHF,const int CHM, const float MUF, const float CEMF, bool jetPUid, const float iJet_pt)
{
   if( (abs(eta) > 2.4)) return false;

   if( (!jetPUid) && (iJet_pt < 50.0)) return false;

   if ((NHF>0.9) || (NEMF>0.9) || (NumConst<1) || (CHF<0.) || (CHM<0) || (MUF > 0.8) || (CEMF > 0.8)) 
      {
         return false;
      }
   else{ return true;}

}
bool calculateBtagEfficiencyMaps::isgoodjet(const float eta, const float NHF,const float NEMF, const size_t NumConst,const float CHF,const int CHM, const float MUF, const float CEMF, int nfatjets)
{
   if ( (nfatjets < 2) && (abs(eta) > 2.4) ) return false;
   else if ( (nfatjets >= 2) && (abs(eta) > 1.4) ) return false;

   if ((NHF>0.9) || (NEMF>0.9) || (NumConst<1) || (CHF<0.) || (CHM<0) || (MUF > 0.8) || (CEMF > 0.8)) 
      {
         return false;
      }
   else{ return true;}

}

bool calculateBtagEfficiencyMaps::isHEM(const float jet_eta, const float jet_phi)
{

   if(year != "2018") return false; // HEM is only relevant for 2018

   if( (jet_phi >  -1.57)&&( jet_phi < -0.87) )
   {
      if( (jet_eta > -3.0)&&(jet_eta < -1.3))return true;

   }
   return false;
}


/// returns the JEC uncertainty scale factor (from a specific, reduced source) for a given jet with pt, eta
double calculateBtagEfficiencyMaps::getJECUncertaintyFromSources(double pt, double eta)
{  

   double uncert = 0.0;
   //std::cout << "Getting JEC Uncertainty from sources: " << std::endl;
   for(auto uncert_source = uncertainty_sources.begin(); uncert_source!=uncertainty_sources.end();uncert_source++)
   {
      /// get the uncertainty from the JetCorrector object
      double AK4_JEC_uncertainty = -999;
      //std::cout << "uncert_source is " << *uncert_source << std::endl;
      JEC_map_AK4[*uncert_source]->setJetEta(eta );
      JEC_map_AK4[*uncert_source]->setJetPt( pt );
      AK4_JEC_uncertainty = fabs(JEC_map_AK4[*uncert_source]->getUncertainty(true));
      uncert+= pow(AK4_JEC_uncertainty,2);
   }

   return sqrt(uncert);  // sqrt because these are added in quadrature
}  



void calculateBtagEfficiencyMaps::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

   /*
   for (const auto& pair : JEC_map_AK4) 
   {
      const std::string& key = pair.first;
      const auto& ptr = pair.second;

      if (ptr) 
      {
         std::cout << "Key " << key << " has a valid JetCorrectionUncertainty object.\n";
      } 
      else 
      {
         std::cerr << "Warning: Key " << key << " has a nullptr!\n";
      }
   }

   */

   //need to correct AK4 jet 4-vectors with JECs and JERs, I'm not doing anything with AK8 jet b-tagging, so no need to have these for anything

   edm::Handle<std::vector<pat::Jet> > smallJets;
   iEvent.getByToken(jetToken_, smallJets);

   JME::JetResolution resolution_AK4               = JME::JetResolution::get(iSetup, "AK4PFchs_pt");                          //load JER stuff from global tag
   JME::JetResolutionScaleFactor resolution_sf_AK4 = JME::JetResolutionScaleFactor::get(iSetup, "AK4PFchs");

   edm::Handle<double> rho;
   iEvent.getByToken(m_rho_token, rho);

   // set working points 
   double deepjet_wp_med, deepjet_wp_tight; // deepJet_wp_loose
   if(year == "2018")
   {
      //deepJet_wp_loose = 0.0490;
      deepjet_wp_med   = 0.2783;    
      deepjet_wp_tight = 0.7100;
   }
   else if(year == "2017")
   {
      //deepJet_wp_loose = 0.0532;
      deepjet_wp_med   = 0.3040;
      deepjet_wp_tight = 0.7476;
   }
   else if(year == "2016")
   {
      //deepJet_wp_loose = 0.0480;
      deepjet_wp_med   = 0.2489;
      deepjet_wp_tight = 0.6377;
   }
   else if(year == "2015")
   {
      //deepJet_wp_loose = 0.0508;
      deepjet_wp_med   = 0.2598;
      deepjet_wp_tight = 0.6502;
   }
   else {std::cout << "ERROR: enter valid run year into cfg"; return;}

   int nAK4_passed = 0;
   for(auto iJet = smallJets->begin(); iJet != smallJets->end(); iJet++) 
   {


      if( (iJet->pt() < 10. ) || (!(iJet->isPFJet())) || ( abs(iJet->eta()) > 2.5 )) continue;   //don't even bother with these jets, lost causes



      /* old JEC way

      ///////////// JEC shifts (shift all jets up and down ) ///////////////
      double JEC_sf_up = 1.0, JEC_sf_down = 1.0;

      jecUnc_AK4->setJetEta( iJet->eta() );
      jecUnc_AK4->setJetPt( iJet->pt() );

      double AK4_JEC_uncertainty = fabs(jecUnc_AK4->getUncertainty(true));
      JEC_sf_up   = 1 + AK4_JEC_uncertainty;
      JEC_sf_down = 1 - AK4_JEC_uncertainty;
      */ 
      ////////////////////////////////////////////////////////////////////////////////////////////////////////////
      //////////   _JET ENERGY RESOLUTION STUFF //////////////////////////////////////////////////////////////////
      ////////////////////////////////////////////////////////////////////////////////////////////////////////////
      /*
      double AK4_JER_corr_factor = 1.0; // this won't be touched for data
      if ((runType.find("MC") != std::string::npos) || (runType.find("Suu") ) ) 
      {

         double sJER     = -9999.;    //JER scale factor
         double sigmaJER = -9999.;    //this is the "resolution" you get from the scale factors 
         
         //these are for getting the JER scale factors
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
            TRandom3 randomNum( abs(static_cast<int>(iJet->phi()*1e4)) );
            double JERrand = randomNum.Gaus(0.0, sigmaJER);
     
            AK4_JER_corr_factor = max(0., 1 + JERrand*sqrt(max(pow(sJER,2)-1,0.)));   //want to make sure this is truncated at 0
         }
      }
      */


      double AK4_JER_corr_factor = 1.0, AK4_JER_corr_factor_up = 1.0, AK4_JER_corr_factor_down = 1.0 ; // this won't be touched for data

      if ((runType.find("MC") != std::string::npos) || (runType.find("Suu") ) )
      {
         double sJER     = -9999., sJER_up  = -9999., sJER_down = -9999.;    //JER scale factor
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
         sJER      =  resolution_sf_AK4.getScaleFactor(parameters);  //{{JME::Binning::JetEta, iJet->eta()}});
         sJER_up   = resolution_sf_AK4.getScaleFactor(parameters, Variation::UP  ); 
         sJER_down = resolution_sf_AK4.getScaleFactor(parameters, Variation::DOWN); 

         const reco::GenJet *genJet = iJet->genJet();
         if( genJet)   // try the first technique
         {
            AK4_JER_corr_factor      = 1 + (sJER - 1     )*(iJet->pt()-genJet->pt())/iJet->pt();
            AK4_JER_corr_factor_up   = 1 + (sJER_up - 1  )*(iJet->pt()-genJet->pt())/iJet->pt();
            AK4_JER_corr_factor_down = 1 + (sJER_down - 1)*(iJet->pt()-genJet->pt())/iJet->pt();
         }
         else   // if no gen jet is matched, try the second technique
         {
            randomNum->SetSeed( abs(static_cast<int>(iJet->phi()*1e4)) );
            double JERrand = randomNum->Gaus(0.0, sigmaJER);
            //double JERrand = 1.0 + sigmaJER;
            AK4_JER_corr_factor      = max(0., 1 + JERrand*sqrt(max(pow(sJER,2)-1,0.)));   //want to make sure this is truncated at 0
            AK4_JER_corr_factor_up   = max(0., 1 + JERrand*sqrt(max(pow(sJER_up,2)-1,0.)));   //want to make sure this is truncated at 0
            AK4_JER_corr_factor_down = max(0., 1 + JERrand*sqrt(max(pow(sJER_down,2)-1,0.)));   //want to make sure this is truncated at 0

         }
      }

      // get JEC correction factors

      std::vector<double> correction_shifts;

      for(auto systematic: systematics)
      {
         if ((systematic.find("JEC") != std::string::npos) )                          uncertainty_sources = {"Total"};
         else if ((systematic.find("BBEC1_year") != std::string::npos) )          uncertainty_sources = {"RelativeJEREC1","RelativePtEC1","RelativeStatEC"};
         else if ((systematic.find("Absolute_year") != std::string::npos) )       uncertainty_sources = {"AbsoluteStat","RelativeStatFSR","TimePtEta"};
         else if ((systematic.find("RelativeSample_year") != std::string::npos))  uncertainty_sources = {"RelativeSample"};
         else if ((systematic.find("FlavorQCD") != std::string::npos) )           uncertainty_sources = {"FlavorQCD"};
         else if ((systematic.find("RelativeBal") != std::string::npos))          uncertainty_sources = {"RelativeBal"};
         else if ((systematic.find("AbsoluteCal") != std::string::npos) )         uncertainty_sources = {"SinglePionECAL","SinglePionHCAL"};
         else if ((systematic.find("AbsolutePU") != std::string::npos) )          uncertainty_sources = { "PileUpDataMC","PileUpPtRef"};
         else if ((systematic.find("Absolute") != std::string::npos) )            uncertainty_sources = {"AbsoluteMPFBias", "AbsoluteScale", "Fragmentation","PileUpDataMC","PileUpPtRef","RelativeFSR","SinglePionECAL","SinglePionHCAL"};
         else if ((systematic.find("AbsoluteTheory") != std::string::npos) )      uncertainty_sources = {"AbsoluteScale", "Fragmentation","AbsoluteMPFBias","RelativeFSR"};
         else if ((systematic.find("AbsoluteScale") != std::string::npos) )       uncertainty_sources = {"AbsoluteScale"};
         else if ((systematic.find("Fragmentation") != std::string::npos) )       uncertainty_sources = {"Fragmentation"};
         else if ((systematic.find("AbsoluteMPFBias") != std::string::npos) )     uncertainty_sources = {"AbsoluteMPFBias"};
         else if ((systematic.find("RelativeFSR") != std::string::npos) )         uncertainty_sources = {"RelativeFSR"};

         //std::cout << "Running systematic " << systematic << std::endl;

         double AK4_JEC_shift = getJECUncertaintyFromSources(iJet->pt(), iJet->eta());
         correction_shifts.push_back(1.00+AK4_JEC_shift);
      }


      correction_shifts.push_back(AK4_JER_corr_factor_up/AK4_JER_corr_factor);     // nominal JEC and up JER
      correction_shifts.push_back(AK4_JER_corr_factor_down/AK4_JER_corr_factor);   // nominal JEC and down JER
      correction_shifts.push_back(1.0);                                            // nominal JEC and nominal JER

      bool PUID = true;
      if(doPUID)PUID = bool(iJet->userInt("pileupJetIdUpdated:fullId") & (1 << 1));
      
      bool jetIsGood = isgoodjet(iJet->eta(),iJet->neutralHadronEnergyFraction(), iJet->neutralEmEnergyFraction(),iJet->numberOfDaughters(),iJet->chargedHadronEnergyFraction(),iJet->chargedMultiplicity(),iJet->muonEnergyFraction(),iJet->chargedEmEnergyFraction(), PUID, iJet->pt());
      
      double jetHadronFlavor = iJet->hadronFlavour();

      if ((!(iJet->isPFJet())) || (!jetIsGood)) continue;
      if (isHEM(iJet->eta(),iJet->phi())) continue;

      double deepJetScore = iJet->bDiscriminator("pfDeepFlavourJetTags:probb") + iJet->bDiscriminator("pfDeepFlavourJetTags:probbb")+ iJet->bDiscriminator("pfDeepFlavourJetTags:problepb");
      
      for(auto correction_shift: correction_shifts)
      {
         if( (AK4_JER_corr_factor*correction_shift*iJet->pt()) < 30) 
         {
            //std::cout << "jet FAILED, pt = " << AK4_JER_corr_factor*correction_shift*iJet->pt()<< ", correction factor is "<< AK4_JER_corr_factor*correction_shift<< ", original pt = "<< iJet->pt()  << std::endl;
            continue;
         }
         else
         {


            //nAK4_passed++;
            //numberOfJetsRunOver++;
            //std::cout << "jet PASSED, pt = " << AK4_JER_corr_factor*correction_shift*iJet->pt()<< ", correction factor is "<< AK4_JER_corr_factor*correction_shift<< ", original pt = "<< iJet->pt()  << std::endl;
         }

         double corr_pt = correction_shift*iJet->pt();
         if(jetHadronFlavor == 0)   //light jets
         {  
            // nom JEC uncertainty 
            h_nLightJets_tight->Fill(corr_pt,iJet->eta());
            h_nLightJets_med->Fill(corr_pt,iJet->eta());

            if(deepJetScore > deepjet_wp_tight)
            {
               h_nLightJets_tight_btagged->Fill(corr_pt,iJet->eta());
            }
            if(deepJetScore > deepjet_wp_med)
            {
               h_nLightJets_med_btagged->Fill(corr_pt,iJet->eta());
            }
         }
         else if(jetHadronFlavor == 4) //charm jets
         {
            // nom JEC uncertainty 
            h_nTruecJets_tight->Fill(corr_pt,iJet->eta());
            h_nTruecJets_med->Fill(corr_pt,iJet->eta());

            if(deepJetScore > deepjet_wp_tight)
            {
               h_nTruecJets_tight_btagged->Fill(corr_pt,iJet->eta());
            }
            if(deepJetScore > deepjet_wp_med)
            {
               h_nTruecJets_med_btagged->Fill(corr_pt,iJet->eta());
            }
         }
         else if(jetHadronFlavor == 5) // b jets
         {
            // nom JEC uncertainty 
            h_nTruebJets_tight->Fill(corr_pt,iJet->eta());
            h_nTruebJets_med->Fill(corr_pt,iJet->eta());

            if(deepJetScore > deepjet_wp_tight)
            {
               h_nTruebJets_tight_btagged->Fill(corr_pt,iJet->eta());
            }
            if(deepJetScore > deepjet_wp_med)
            {
               h_nTruebJets_med_btagged->Fill(corr_pt,iJet->eta());
            }
         }
      }
   }




   //std::cout << "number of jets in this event: " << nAK4_passed << ", total number of jets passed: " << numberOfJetsRunOver << std::endl;


   //fill the histograms as necessary and save these 
}   
DEFINE_FWK_MODULE(calculateBtagEfficiencyMaps);
//_bottom_
