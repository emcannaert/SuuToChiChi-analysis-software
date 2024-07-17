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
   edm::FileInPath JECUncert_AK8_path;
   edm::FileInPath JECUncert_AK4_path;

   JetCorrectionUncertainty *jecUnc_AK4;
   JetCorrectionUncertainty *jecUnc_AK8;
   
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


};

//_constructor_
calculateBtagEfficiencyMaps::calculateBtagEfficiencyMaps(const edm::ParameterSet& iConfig)

{

   runType        = iConfig.getParameter<std::string>("runType");
   year           = iConfig.getParameter<std::string>("year");

   JECUncert_AK8_path = iConfig.getParameter<edm::FileInPath>("JECUncert_AK8_path");
   JECUncert_AK4_path = iConfig.getParameter<edm::FileInPath>("JECUncert_AK4_path");

   jecUnc_AK4 = new JetCorrectionUncertainty(JECUncert_AK4_path.fullPath().c_str());
   jecUnc_AK8 = new JetCorrectionUncertainty(JECUncert_AK8_path.fullPath().c_str());

   JetCorrectionUncertainty *jecUnc_AK4;
   JetCorrectionUncertainty *jecUnc_AK8;

   int NBINSX;
   double PTMAX;
   if(runType.find("Suu") != std::string::npos)
   {
      NBINSX = 40;
      PTMAX  = 6000.;  // best to keep bin sizes the same between these
   }
   else
   {
      NBINSX = 40;
      PTMAX  = 6000.;  // best to keep bin sizes the same between these
   }

   // tight WP
   h_nLightJets_tight = new TH2F("h_nLightJets_tight" ,"total number of true light jets; jet p_{T} [GeV];jet eta", NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruebJets_tight = new TH2F("h_nTruebJets_tight" ,"total number of true b jets; jet p_{T} [GeV];jet eta",  NBINSX,0, 6000, 18, -2.4, 2.4);
   h_nTruecJets_tight = new TH2F("h_nTruecJets_tight" ,"total number of true c jets; jet p_{T} [GeV];jet eta", NBINSX ,0, PTMAX, 18, -2.4, 2.4);

   h_nLightJets_tight_btagged = new TH2F("h_nLightJets_tight_btagged" ,"total number of true light jets that are b-tagged; jet p_{T} [GeV];jet eta", NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruebJets_tight_btagged = new TH2F("h_nTruebJets_tight_btagged" ,"total number of true b jets that are b-tagged; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruecJets_tight_btagged = new TH2F("h_nTruecJets_tight_btagged" ,"total number of true c jets that are b-tagged; jet p_{T} [GeV];jet eta",   NBINSX ,0, PTMAX, 18, -2.4, 2.4);

   // med WP
   h_nLightJets_med = new TH2F("h_nLightJets_med" ,"total number of true light jets; jet p_{T} [GeV];jet eta", NBINSX ,0, PTMAX, 18, -2.4, 2.4);
   h_nTruebJets_med = new TH2F("h_nTruebJets_med" ,"total number of true b jets; jet p_{T} [GeV];jet eta",  NBINSX,0, 6000, 18, -2.4, 2.4);
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
void calculateBtagEfficiencyMaps::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   //need to correct AK4 jet 4-vectors with JECs and JERs, I'm not doing anything with AK8 jet b-tagging, so no need to have these for anything

   edm::Handle<std::vector<pat::Jet> > smallJets;
   iEvent.getByToken(jetToken_, smallJets);

   JME::JetResolution resolution_AK4               = JME::JetResolution::get(iSetup, "AK4PFchs_pt");                          //load JER stuff from global tag
   JME::JetResolutionScaleFactor resolution_sf_AK4 = JME::JetResolutionScaleFactor::get(iSetup, "AK4PFchs");

   edm::Handle<double> rho;
   iEvent.getByToken(m_rho_token, rho);

   // set working points 
   double deepJet_wp_loose, deepjet_wp_med, deepjet_wp_tight;
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


   for(auto iJet = smallJets->begin(); iJet != smallJets->end(); iJet++) 
   {

      double AK4_sf_total = 1.0;

      ///////////// JEC shifts (shift all jets up and down ) ///////////////
      double JEC_sf_up = 1.0, JEC_sf_down = 1.0;

      jecUnc_AK4->setJetEta( iJet->eta() );
      jecUnc_AK4->setJetPt( iJet->pt() );

      double AK4_JEC_uncertainty = fabs(jecUnc_AK4->getUncertainty(true));
      JEC_sf_up   = 1 + AK4_JEC_uncertainty;
      JEC_sf_down = 1 - AK4_JEC_uncertainty;

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


      double AK4_JER_corr_factor = 1.0; // this won't be touched for data

      if ((runType.find("MC") != std::string::npos) || (runType.find("Suu") ) )
      {
         double AK4_JER_corr_factor = 1.0; // this won't be touched for data

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
         AK4_sf_total*= AK4_JER_corr_factor;

      }


      AK4_sf_total*= AK4_JER_corr_factor;

      // create scaled jet object that will be used for cuts 
      pat::Jet  corrJet(*iJet); 
      LorentzVector corrJetP4(AK4_sf_total*iJet->px(),AK4_sf_total*iJet->py(),AK4_sf_total*iJet->pz(),AK4_sf_total*iJet->energy());
      corrJet.setP4(corrJetP4);

      pat::Jet  corrJet_up(*iJet); 
      LorentzVector corrJetP4_up(JEC_sf_up*AK4_sf_total*iJet->px(),JEC_sf_up*AK4_sf_total*iJet->py(),JEC_sf_up*AK4_sf_total*iJet->pz(),JEC_sf_up*AK4_sf_total*iJet->energy());
      corrJet_up.setP4(corrJetP4_up);

      pat::Jet  corrJet_down(*iJet); 
      LorentzVector corrJetP4_down(JEC_sf_down*AK4_sf_total*iJet->px(),JEC_sf_down*AK4_sf_total*iJet->py(),JEC_sf_down*AK4_sf_total*iJet->pz(),JEC_sf_down*AK4_sf_total*iJet->energy());
      corrJet_down.setP4(corrJetP4_down);

      bool PUID = true;
      if(doPUID)
      {
         PUID = bool(corrJet.userInt("pileupJetIdUpdated:fullId") & (1 << 1));
      }
      //if( (corrJet.pt()  < 50.) && (!PUID)) continue; //if particle doesn't pass the PUID
      if( (corrJet.pt()  <30.) || (!(corrJet.isPFJet())) || (!isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(), PUID, corrJet.pt()))  ) continue;


      if (isHEM(corrJet.eta(),corrJet.phi())) return;


      //    double deepJet_wp_loose, deepjet_wp_med, deepjet_wp_tight;
      double deepJetScore = corrJet.bDiscriminator("pfDeepFlavourJetTags:probb") + corrJet.bDiscriminator("pfDeepFlavourJetTags:probbb")+ corrJet.bDiscriminator("pfDeepFlavourJetTags:problepb");
      if(corrJet.hadronFlavour() == 0)   //light jets
      {  
         // nom JEC uncertainty 
         h_nLightJets_tight->Fill(corrJet.pt(),corrJet.eta());
         h_nLightJets_med->Fill(corrJet.pt(),corrJet.eta());

          // up JEC uncertainty 
         h_nLightJets_tight->Fill(corrJet_up.pt(),corrJet_up.eta());
         h_nLightJets_med->Fill(corrJet_up.pt(),corrJet_up.eta());

          // down JEC uncertainty 
         h_nLightJets_tight->Fill(corrJet_down.pt(),corrJet_down.eta());
         h_nLightJets_med->Fill(corrJet_down.pt(),corrJet_down.eta());

         if(deepJetScore > deepjet_wp_tight)
         {
            h_nLightJets_tight_btagged->Fill(corrJet.pt(),corrJet.eta());
            h_nLightJets_tight_btagged->Fill(corrJet_up.pt(),corrJet_up.eta());
            h_nLightJets_tight_btagged->Fill(corrJet_down.pt(),corrJet_down.eta());

         }
         if(deepJetScore > deepjet_wp_med)
         {
            h_nLightJets_med_btagged->Fill(corrJet.pt(),corrJet.eta());
            h_nLightJets_med_btagged->Fill(corrJet_up.pt(),corrJet_up.eta());
            h_nLightJets_med_btagged->Fill(corrJet_down.pt(),corrJet_down.eta());

         }
      }
      else if(corrJet.hadronFlavour() == 4) //charm jets
      {
         // nom JEC uncertainty 
         h_nTruecJets_tight->Fill(corrJet.pt(),corrJet.eta());
         h_nTruecJets_med->Fill(corrJet.pt(),corrJet.eta());

         // up JEC uncertainty 
         h_nTruecJets_tight->Fill(corrJet_up.pt(),corrJet_up.eta());
         h_nTruecJets_med->Fill(corrJet_up.pt(),corrJet_up.eta());

         // down JEC uncertainty 
         h_nTruecJets_tight->Fill(corrJet_down.pt(),corrJet_down.eta());
         h_nTruecJets_med->Fill(corrJet_down.pt(),corrJet_down.eta());

         if(deepJetScore > deepjet_wp_tight)
         {
            h_nTruecJets_tight_btagged->Fill(corrJet.pt(),corrJet.eta());
            h_nTruecJets_tight_btagged->Fill(corrJet_up.pt(),corrJet_up.eta());
            h_nTruecJets_tight_btagged->Fill(corrJet_down.pt(),corrJet_down.eta());

         }
         if(deepJetScore > deepjet_wp_med)
         {
            h_nTruecJets_med_btagged->Fill(corrJet.pt(),corrJet.eta());
            h_nTruecJets_med_btagged->Fill(corrJet_up.pt(),corrJet_up.eta());
            h_nTruecJets_med_btagged->Fill(corrJet_down.pt(),corrJet_down.eta());

         }
      }
      else if(corrJet.hadronFlavour() == 5) // b jets
      {
         // nom JEC uncertainty 
         h_nTruebJets_tight->Fill(corrJet.pt(),corrJet.eta());
         h_nTruebJets_med->Fill(corrJet.pt(),corrJet.eta());

         // up JEC uncertainty 
         h_nTruebJets_tight->Fill(corrJet_up.pt(),corrJet_up.eta());
         h_nTruebJets_med->Fill(corrJet_up.pt(),corrJet_up.eta());

         // down JEC uncertainty 
         h_nTruebJets_tight->Fill(corrJet_down.pt(),corrJet_down.eta());
         h_nTruebJets_med->Fill(corrJet_down.pt(),corrJet_down.eta());

         if(deepJetScore > deepjet_wp_tight)
         {
            h_nTruebJets_tight_btagged->Fill(corrJet.pt(),corrJet.eta());
            h_nTruebJets_tight_btagged->Fill(corrJet_up.pt(),corrJet_up.eta());
            h_nTruebJets_tight_btagged->Fill(corrJet_down.pt(),corrJet_down.eta());

         }
         if(deepJetScore > deepjet_wp_med)
         {
            h_nTruebJets_med_btagged->Fill(corrJet.pt(),corrJet.eta());
            h_nTruebJets_med_btagged->Fill(corrJet_up.pt(),corrJet_up.eta());
            h_nTruebJets_med_btagged->Fill(corrJet_down.pt(),corrJet_down.eta());

         }
      }
   }

   //fill the histograms as necessary and save these 
}   
DEFINE_FWK_MODULE(calculateBtagEfficiencyMaps);
//_bottom_
