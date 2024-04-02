// -*- C++ -*-
//
// Package:    hadronFilter/hadronFilter
// Class:      hadronFilter
// 
/**\class hadronFilter hadronFilter.cc hadronFilter/hadronFilter/plugins/hadronFilter.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Ethan Cannaert
//         Created:  Mon, 29 Mar 2021 15:55:02 GMT
//
//


// system include files
// user include files
#include "FWCore/Framework/interface/stream/EDFilter.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

#include <fastjet/JetDefinition.hh>
#include <fastjet/GhostedAreaSpec.hh>
#include <fastjet/PseudoJet.hh>
#include <fastjet/tools/Filter.hh>
#include <fastjet/ClusterSequence.hh>
//#include <fastjet/ActiveAreaSpec.hh>
#include <fastjet/ClusterSequenceArea.hh>

#include <memory>
#include <iostream>
#include <fstream>
#include <vector>
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
// new includes
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/Math/interface/PtEtaPhiMass.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include <math.h>

#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
//#include "PhysicsTools/CandUtils/interface/Thrust.h"
#include <TTree.h>
#include <TCanvas.h>
#include <TF1.h>
#include <TGraph.h>
#include <cmath>
#include "TLorentzVector.h"
#include "TVector3.h"
#include<TRandom3.h>
 
#include "DataFormats/Candidate/interface/Candidate.h"
#include  "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include <algorithm>   

#include "FWCore/Framework/interface/EDProducer.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include <DataFormats/Math/interface/deltaR.h>
#include "FWCore/Utilities/interface/EDGetToken.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include <string>


///// JEC and JER stuff 

#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "JetMETCorrections/JetCorrector/interface/JetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetResolutionObject.h"
#include "JetMETCorrections/Modules/interface/JetResolution.h"
#include "PhysicsTools/PatUtils/interface/SmearedJetProducerT.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CondFormats/DataRecord/interface/JetResolutionRcd.h"
#include "CondFormats/DataRecord/interface/JetResolutionScaleFactorRcd.h"

typedef math::XYZTLorentzVector LorentzVector;

// class declaration
//

class hadronFilter_bTagSF : public edm::stream::EDFilter<> {
   public:
      explicit hadronFilter_bTagSF(const edm::ParameterSet&);
      ~hadronFilter_bTagSF();
      bool isgoodjet(const float eta, const float NHF,const float NEMF, const size_t NumConst,const float CHF,const int CHM, const float MUF, const float CEMF);
      bool isgoodjet(const float eta, const float NHF,const float NEMF, const size_t NumConst,const float CHF,const int CHM, const float MUF, const float CEMF, int nfatjets);

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginStream(edm::StreamID) override;
      virtual bool filter(edm::Event&, const edm::EventSetup&) override;
      virtual void endStream() override;
      edm::EDGetTokenT<std::vector<pat::Jet>> fatJetToken_;
      edm::EDGetTokenT<std::vector<pat::Jet>> jetToken_;
      edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
      std::string systematicType;
      std::string runType;
      std::vector<std::string> triggers;

      std::string year;

      bool doJER = true;
      bool _verbose = false;
      bool debug = false;
      edm::EDGetTokenT<double> m_rho_token;
      TRandom3 *randomNum = new TRandom3();
      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
hadronFilter_bTagSF::hadronFilter_bTagSF(const edm::ParameterSet& iConfig)
{

   //now do what ever initialization is needed
   fatJetToken_ =    consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("fatJetCollection"));
   triggerBits_ = consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"));
   jetToken_    = consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("jetCollection"));
   systematicType = iConfig.getParameter<std::string>("systematicType");
   //triggers     = iConfig.getParameter<std::string>("triggers");
   runType = iConfig.getParameter<std::string>("runType");


   //JECUncert_AK4_path = iConfig.getParameter<edm::FileInPath>("JECUncert_AK4_path");
   edm::InputTag fixedGridRhoAllTag_ = edm::InputTag("fixedGridRhoAll", "", "RECO");   
   m_rho_token  = consumes<double>(fixedGridRhoAllTag_);
   year = iConfig.getParameter<std::string>("year");

   if(year == "2018")
   {
      triggers = {"HLT_PFJet500_v", "HLT_PFHT1050_v"};
   }
   else if(year == "2017")
   {
      triggers = {"HLT_PFJet500_v", "HLT_PFHT1050_v"};
   }
   else if(year == "2016")
   {
      triggers  = {"HLT_PFHT900_v", "HLT_PFJet450_v"};
   }
   else if(year == "2015")
   {
      triggers  = {"HLT_PFHT900_v", "HLT_PFJet450_v"};
   }

   //jecUnc_AK4 = new JetCorrectionUncertainty(JECUncert_AK4_path.fullPath().c_str());

}


hadronFilter_bTagSF::~hadronFilter_bTagSF()
{
 
   // do anything here that needs to be done at destruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//
bool hadronFilter_bTagSF::isgoodjet(const float eta, const float NHF,const float NEMF, const size_t NumConst,const float CHF,const int CHM, const float MUF, const float CEMF)
{
   if( (abs(eta) > 2.5)) return false;

   if ((NHF>0.9) || (NEMF>0.9) || (NumConst<1) || (CHF<0.) || (CHM<0) || (MUF > 0.8) || (CEMF > 0.8)) 
      {
         return false;
      }
   else{ return true;}

}
bool hadronFilter_bTagSF::isgoodjet(const float eta, const float NHF,const float NEMF, const size_t NumConst,const float CHF,const int CHM, const float MUF, const float CEMF, int nfatjets)
{
   if ( (nfatjets < 2) && (abs(eta) > 2.4) ) return false;
   else if ( (nfatjets >= 2) && (abs(eta) > 1.5) ) return false;

   if ((NHF>0.9) || (NEMF>0.9) || (NumConst<1) || (CHF<0.) || (CHM<0) || (MUF > 0.8) || (CEMF > 0.8)) 
      {
         return false;
      }
   else{ return true;}

}
// ------------ method called on each new Event  ------------
bool hadronFilter_bTagSF::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{

/////////////////Trigger///////////////

   edm::Handle<edm::TriggerResults> triggerBits;
   iEvent.getByToken(triggerBits_, triggerBits);

   const edm::TriggerNames &names = iEvent.triggerNames(*triggerBits);
   
   for(auto iT = triggers.begin(); iT != triggers.end(); iT++)
   {
      std::string trigname = *iT;
      if(debug)std::cout << "Looking for the " << trigname << " trigger." << std::endl;

      bool pass = false;
      for (unsigned int i = 0; i < triggerBits->size(); ++i) 
      {

         const std::string name = names.triggerName(i);
         const bool accept = triggerBits->accept(i);
         if ((name.find(trigname) != std::string::npos) &&(accept))
         {
            if(debug)std::cout << "Found the " << *iT << " trigger." << std::endl;
            pass =true;
         }
      } 
      if(!pass)
      {  
          return false; // if any of the triggers aren't found, skip event
      }
   }

   //std::cout << "Pases trigger" << std::endl;
   //calculate HT -> make HT > 1250. GeV


   ///////////////////////////////////
   //////////// rho //////////////////
   ///////////////////////////////////

   edm::Handle<double> rho;
   iEvent.getByToken(m_rho_token, rho);


///////////////////////////AK4 jets  && HT
   double totHT = 0;
   int nAK4 = 0;
   int nAK8 = 0;
   int nHeavyAK8 = 0;


   JME::JetResolution resolution_AK4               = JME::JetResolution::get(iSetup, "AK4PFchs_pt");                          //load JER stuff from global tag
   JME::JetResolutionScaleFactor resolution_sf_AK4 = JME::JetResolutionScaleFactor::get(iSetup, "AK4PFchs");

   edm::Handle<std::vector<pat::Jet> > smallJets;
   iEvent.getByToken(jetToken_, smallJets);

   for(auto iJet = smallJets->begin(); iJet != smallJets->end(); iJet++) 
   {  
      if( (iJet->pt() < 15. ) || (!(iJet->isPFJet())) || ( abs(iJet->eta()) > 2.5 )) continue;   //don't even bother with these jets

      double AK4_sf_total = 1.0;


      ////////////////////////////////////////////////////////////////////////////////////////////////////////////
      //////////   _JET ENERGY RESOLUTION STUFF //////////////////////////////////////////////////////////////////
      ////////////////////////////////////////////////////////////////////////////////////////////////////////////

      if(doJER)
      {
         if ((runType.find("MC") != std::string::npos) || (runType.find("Suu") ) )
         {
            double AK4_JER_corr_factor = 1.0; // this won't be touched for data

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
               double JERrand = randomNum->Gaus(0, sigmaJER);
               //double JERrand = 1.0 + sigmaJER;     
               AK4_JER_corr_factor = std::max(0., 1 + JERrand*sqrt(  std::max(pow(sJER,2)-1.0,0.) )  );   //want to make sure this is truncated at 0
            }
            AK4_sf_total*= AK4_JER_corr_factor;

         }
      }

      // create scaled jet object that will be used for cuts 
      pat::Jet corrJet(*iJet);
      LorentzVector corrJetP4(AK4_sf_total*iJet->px(),AK4_sf_total*iJet->py(),AK4_sf_total*iJet->pz(),AK4_sf_total*iJet->energy());
      corrJet.setP4(corrJetP4);


      if(corrJet.pt() > 30.)totHT+= abs(corrJet.pt() );

      //loose WP 0.1522
      if( (corrJet.pt()  <30.) || (!(corrJet.isPFJet())) || (!isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction())) ) continue;
      nAK4++;
   }



   if (totHT < 1600.) 
   {
      //std::cout << "failed HT" << std::endl;
      return false;  //btagged jet cuts
   }
   if (nAK4 < 4)
   {
      //std::cout << "failed nAK4" << std::endl;
      return false;
   }



   /////////////////////////// AK8 jets 


   edm::Handle<std::vector<pat::Jet> > fatJets;
   iEvent.getByToken(fatJetToken_, fatJets);


   JME::JetResolution resolution = JME::JetResolution::get(iSetup, "AK8PF_pt");                          //load JER stuff from global tag
   JME::JetResolutionScaleFactor resolution_sf = JME::JetResolutionScaleFactor::get(iSetup, "AK8PF");


   for(auto iJet = fatJets->begin(); iJet != fatJets->end(); iJet++)    //Over AK8 Jets
   {
      if( (sqrt(pow(iJet->mass(),2)+pow(iJet->pt(),2)) < 100.) || (!(iJet->isPFJet())) || ( abs(iJet->eta()) > 2.4 )) continue;   //don't even bother with these jets

      double AK8_sf_total = 1.0;     // this scales jet/particle 4-vectors, compounds all scale factors


      ////////////////////////////////////////////////////////////////////////////////////////////////////////////
      //////////   _JET ENERGY RESOLUTION STUFF //////////////////////////////////////////////////////////////////
      ////////////////////////////////////////////////////////////////////////////////////////////////////////////
      if(doJER)
      {
         double AK8_JER_corr_factor = 1.0; // this won't be touched for data
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
            AK8_JER_corr_factor = std::max(0., 1 + JERrand*sqrt(std::max(pow(sJER,2)-1,0.)));   //want to make sure this is truncated at 0
         }

         AK8_sf_total*= AK8_JER_corr_factor;
      }
      /////////////////////////////////////////////////////////////////////////////////////////////////////////////
      /////////////////////////////////////////////////////////////////////////////////////////////////////////////

      pat::Jet corrJet(*iJet);
      LorentzVector corrJetP4(AK8_sf_total*iJet->px(),AK8_sf_total*iJet->py(),AK8_sf_total*iJet->pz(),AK8_sf_total*iJet->energy());
      corrJet.setP4(corrJetP4);

      if((corrJet.pt() > 500.) && ((corrJet.isPFJet())) && (isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(),nAK8) ) && (corrJet.userFloat("ak8PFJetsPuppiSoftDropMass") > 45.))nHeavyAK8++;
      if((sqrt(pow(corrJet.mass(),2)+pow(corrJet.pt(),2)) < 200.) || (!(corrJet.isPFJet())) || (!isgoodjet(corrJet.eta(),corrJet.neutralHadronEnergyFraction(), corrJet.neutralEmEnergyFraction(),corrJet.numberOfDaughters(),corrJet.chargedHadronEnergyFraction(),corrJet.chargedMultiplicity(),corrJet.muonEnergyFraction(),corrJet.chargedEmEnergyFraction(),nAK8 )) || (corrJet.mass()< 0.))continue;
      nAK8++;
   }

   if(nAK8 < 3 )
   {
      //std::cout << "failed nAK8" << std::endl;
      return false;
   } 
   if (nHeavyAK8<2)
   {
      //std::cout << "failed nHeavyAK8" << std::endl;
      return false;
   }
   else{return true;}

   
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void
hadronFilter_bTagSF::beginStream(edm::StreamID)
{
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void
hadronFilter_bTagSF::endStream() {
}

// ------------ method called when starting to processes a run  ------------
/*
void
hadronFilter_bTagSF::beginRun(edm::Run const&, edm::EventSetup const&)
{ 
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
void
hadronFilter_bTagSF::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
hadronFilter_bTagSF::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
hadronFilter_bTagSF::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
hadronFilter_bTagSF::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(hadronFilter_bTagSF);
