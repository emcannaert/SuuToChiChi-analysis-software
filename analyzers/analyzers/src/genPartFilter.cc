// -*- C++ -*-
//
// Package:    genPartFilter/genPartFilter
// Class:      genPartFilter
// 
/**\class genPartFilter genPartFilter.cc genPartFilter/genPartFilter/plugins/genPartFilter.cc

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
// class declaration
//

class genPartFilter : public edm::stream::EDFilter<> {
   public:
      explicit genPartFilter(const edm::ParameterSet&);
      ~genPartFilter();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:
      virtual void beginStream(edm::StreamID) override;
      virtual bool filter(edm::Event&, const edm::EventSetup&) override;
      virtual void endStream() override;
      const reco::Candidate* parse_chain(const reco::Candidate*);
      edm::EDGetTokenT<std::vector<reco::GenParticle>> genPartToken_; 
      
      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      int nWbHt = 0;
        int nWbZt = 0;
        int nWbWb = 0;
        int nHtZt = 0;
        int nHtHt = 0;
        int nZtZt = 0;
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
genPartFilter::genPartFilter(const edm::ParameterSet& iConfig)
{
   //now do what ever initialization is needed
   //genPartToken_ = consumes<std::vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("genPartCollection"));
// Gen Particles
    edm::InputTag genPartTag_;
    genPartTag_ = edm::InputTag("prunedGenParticles", "", "PAT");
    genPartToken_ = consumes<std::vector<reco::GenParticle> >(genPartTag_);

}


genPartFilter::~genPartFilter()
{
 
   // do anything here that needs to be done at destruction time
   // (e.g. close files, deallocate resources etc.)

}

const reco::Candidate* genPartFilter::parse_chain(const reco::Candidate* cand)
{  
   for (unsigned int iii=0; iii<cand->numberOfDaughters(); iii++)
   {
      if(cand->daughter(iii)->pdgId() == cand->pdgId()) return parse_chain(cand->daughter(iii));
   }
   return cand;
}
//
// member functions
//

// ------------ method called on each new Event  ------------
bool
genPartFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   //using namespace edm;
   /*#ifdef THIS_IS_AN_EVENT_EXAMPLE
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);
   #endif */
////////////Gen Particles//////////////////////////////////
//////////////////////////////////////////////////////////
    //------------------------------------------------------------------------------
    // Gen Particles Loop ----------------------------------------------------------
    //------------------------------------------------------------------------------
   int suu_pdgid = 9936661;
   int chi_pdgid = 9936662;
   //int chi_pdgid = 8000001;
   int nSuu = 0;
   int nChi = 0;
   int nW   = 0;
   int ntop = 0;
   int nH   = 0;
   int nhq  = 0;
   int nSuub = 0;
   int nZ    = 0;
   int nZq   = 0;
   int nTopb = 0;
   int nWq   = 0;
   int nhGlu = 0;
   int nhWq = 0;
   int nhZq = 0;
   int nSuu_W = 0;
   std::vector<TLorentzVector> genChiZt;
   std::vector<TLorentzVector> genChiHt;
   std::vector<TLorentzVector> genChiWb;


   std::vector<TLorentzVector> Zquarks;
   std::vector<TLorentzVector> Wquarks;
   std::vector<TLorentzVector> Hquarks;
   std::vector<TLorentzVector> TopWquarks;
   std::vector<TLorentzVector> Topb;
   std::vector<TLorentzVector> Suub;

   edm::Handle< std::vector<reco::GenParticle> > genPartCollection;
   iEvent.getByToken(genPartToken_, genPartCollection);
   std::vector<reco::GenParticle> genPart = *genPartCollection.product(); 
//want only fully hadronic events_
   for (auto iG = genPartCollection->begin(); iG != genPartCollection->end(); iG++) 
   {
      if ((abs(iG->pdgId()) == 24) && ((abs(iG->mother()->pdgId()) == chi_pdgid)) ) 
      {
         genChiWb.push_back( TLorentzVector(iG->mother()->px(),iG->mother()->py(),iG->mother()->pz(),iG->mother()->energy())  );
         const reco::Candidate* W_final = parse_chain(iG->clone());
         for (unsigned int iii=0; iii<W_final->numberOfDaughters(); iii++)
         {
            const reco::Candidate* W_daughter = W_final->daughter(iii);
            if(abs(W_daughter->pdgId()) < 6)
            { 
               Wquarks.push_back(TLorentzVector(W_daughter->px(),W_daughter->py(),W_daughter->pz(),W_daughter->energy()));
               nWq++;
            }
         }

         nSuu_W++;
      }
      else if ( (abs(iG->pdgId()) == 5) && (abs(iG->mother()->pdgId()) == chi_pdgid)  )
      {
         Suub.push_back(TLorentzVector(iG->px(),iG->py(),iG->pz(),iG->energy()));
         nSuub++;
      } 

      else if ( (abs(iG->pdgId()) == 6) && ((abs(iG->mother()->pdgId()) == chi_pdgid)) ) 
      {
         const reco::Candidate* t_final = parse_chain(iG->clone());

         for (unsigned int iii=0; iii<t_final->numberOfDaughters(); iii++)
         {
            const reco::Candidate* t_daughter = t_final->daughter(iii);
            if (abs(t_daughter->pdgId())==24) 
            {
               const reco::Candidate* W_final = parse_chain(t_daughter->clone());
               for (unsigned int jjj=0; jjj<W_final->numberOfDaughters(); jjj++)
               {
                  const reco::Candidate* W_daughter = W_final->daughter(jjj);
                  if(abs(W_daughter->pdgId()) < 6)
                  {
                     TopWquarks.push_back(TLorentzVector(W_daughter->px(),W_daughter->py(),W_daughter->pz(),W_daughter->energy()));
                     nWq++;
                  }
               }
               nW++;
            }
            else if(abs(t_daughter->pdgId())==5) 
            {
               Topb.push_back(TLorentzVector(t_daughter->px(),t_daughter->py(),t_daughter->pz(),t_daughter->energy()));
               nTopb++;
            }
         }
         ntop++;
      }
      else if ( (abs(iG->pdgId()) == 25) && ((abs(iG->mother()->pdgId()) == chi_pdgid)) ) 
      {
         genChiHt.push_back( TLorentzVector(iG->mother()->px(),iG->mother()->py(),iG->mother()->pz(),iG->mother()->energy())  );
         const reco::Candidate* h_final = parse_chain(iG->clone());
         for (unsigned int iii=0; iii<h_final->numberOfDaughters(); iii++)
         {
            const reco::Candidate* h_daughter = h_final->daughter(iii);
            if (abs(h_daughter->pdgId())<6)
            {
               Hquarks.push_back(TLorentzVector(h_daughter->px(),h_daughter->py(),h_daughter->pz(),h_daughter->energy()));
               nhq++;
            }
            else if (abs(h_daughter->pdgId()) ==24)
            {
               const reco::Candidate* higgsW_final = parse_chain(h_daughter->clone());
               for (unsigned int jjj=0; jjj<higgsW_final->numberOfDaughters(); jjj++)
               {
                  const reco::Candidate* higgsW_daughter = higgsW_final->daughter(jjj);
                  if( (abs(higgsW_daughter->pdgId()) < 6))
                  {
                     Hquarks.push_back(TLorentzVector(h_daughter->px(),h_daughter->py(),h_daughter->pz(),h_daughter->energy()));
                     nhWq++;
                  } 
               }
            }
            else if (abs(h_daughter->pdgId()) ==23)
            {
               const reco::Candidate* higgsZ_final = parse_chain(h_daughter->clone());
               for (unsigned int jjj=0; jjj<higgsZ_final->numberOfDaughters(); jjj++)
               {
                  const reco::Candidate* higgsZ_daughter = higgsZ_final->daughter(jjj);
                  if( (abs(higgsZ_daughter->pdgId()) < 6))
                  {
                     Hquarks.push_back(TLorentzVector(h_daughter->px(),h_daughter->py(),h_daughter->pz(),h_daughter->energy()));
                     nhZq++;
                  } 
               }
            }
            else if (abs(h_daughter->pdgId()) ==21)
            {
                Hquarks.push_back(TLorentzVector(h_daughter->px(),h_daughter->py(),h_daughter->pz(),h_daughter->energy()));
                nhGlu++;
            }
         }
         nH++;
      }
      else if ( (abs(iG->pdgId()) == 23) && ((abs(iG->mother()->pdgId()) == chi_pdgid)) ) 
      {
         genChiZt.push_back( TLorentzVector(iG->mother()->px(),iG->mother()->py(),iG->mother()->pz(),iG->mother()->energy())  );

         const reco::Candidate* Z_final = parse_chain(iG->clone());
         for (unsigned int jjj=0; jjj<Z_final->numberOfDaughters(); jjj++)
         {
            const reco::Candidate* Z_daughter = Z_final->daughter(jjj);
            if(abs(Z_daughter->pdgId()) < 6)
            {

               Zquarks.push_back(TLorentzVector(Z_daughter->px(),Z_daughter->py(),Z_daughter->pz(),Z_daughter->energy()));
               nZq++;
            }         
         }
         nZ++;

      }
      else if ((abs(iG->pdgId()) == chi_pdgid) && (iG->isLastCopy()))
      {
         //std::cout << "chi mass is " << iG->mass() << std::endl;
         nChi++;
      }  
      /*
      else if ((abs(iG->pdgId()) == suu_pdgid) && (iG->isLastCopy()))  
      {
         std::cout << "Suu mass is " << iG->mass() << std::endl;
      }
      */
      //else if  ((abs(iG->pdgId()) == chi_pdgid) && (iG->isLastCopy())) nChi++;
   }

   //std::cout << "----------------------end event --------------------------------" << std::endl;
   bool _htWb = false;
   bool _htZt = false;
   bool _ZtWb = false;
   bool _WbWb = false;
   bool _htht = false;
   bool _ZtZt = false;
   //nEvents++;

   //if      ( (nChi<2) || (nSuu < 1) ) return; //don't want anything to do with these bad events anyways 
   if      ((nH == 2) && (nSuub == 0) && (nTopb >= 2) && ( (nhq+nhGlu+nhWq+nhZq) == 4) && (nWq == 4) && (nZq == 0) && (ntop == 2) && (nW == 2)  && (nZ == 0))
   {
      _htht = true; 
      nHtHt++;
   } 
   else if ((nH == 0) && (nSuub == 0) && (nTopb >= 2) && ( (nhq+nhGlu+nhWq+nhZq) == 0) && (nWq == 4) && (nZq == 4) && (ntop == 2) && (nW == 2)  && (nZ == 2))
   {
      _ZtZt = true;
      nZtZt++;
   } 
   else if ((nH == 0) && (nSuub == 2) && (nTopb >= 0) && ( (nhq+nhGlu+nhWq+nhZq) == 0) && (nWq == 4) && (nZq == 0) && (ntop == 0) && (nSuu_W == 2)  && (nZ == 0))
   {
      _WbWb = true;
      nWbWb++;
   } 
   else if ((nH == 1) && (nSuub == 1) && (nTopb >= 1) && ( (nhq+nhGlu+nhWq+nhZq) == 2) && (nWq == 4) && (nZq == 0) && (ntop == 1) && (nW == 1) && (nSuu_W == 1)  && (nZ == 0))
   {
      _htWb = true;
      nWbHt++;
   }
   else if ((nH == 0) && (nSuub == 1) && (nTopb >= 1) && ( (nhq+nhGlu+nhWq+nhZq) == 0) && (nWq == 4) && (nZq == 2) && (ntop == 1) && (nW == 1) && (nSuu_W == 1)  && (nZ == 1))
   {
      _ZtWb = true;
      nWbZt++;
   }
   else if ((nH == 1) && (nSuub == 0) && (nTopb >= 2) && ( (nhq+nhGlu+nhWq+nhZq) == 2) && (nWq == 4) && (nZq == 2) && (ntop == 2) && (nW == 2)  && (nZ == 1))
   { 
      _htZt = true;
      nHtZt++;
   } 
     
  /* 
   //if ( (nH==0)&&(ntop>0)    )
   //{
      for(int iii=0; iii<nH; iii++)
      {
	  std::cout << "ht decay" << std::endl;
      }
   //} 
   //if ( (nW>0)&&(nSuub > 0)   )
   //{
      for(int iii=0;iii<nSuub;iii++)
      {
         std::cout << "Wb decay" << std::endl;
      }
   //} 
   //if ( (nZ>0)&&(ntop>0)  )
   //{
      for(int iii=0;iii<nZ;iii++)
      {
  	std::cout << "Zt decay" << std::endl;
      }
    */
  // }
   //std::cout << " nChi " << nChi<< " ntop "<< ntop<< " nH  " <<nH << " nZ " << nZ << " nSuub " << nSuub <<" nhWq  " <<nhWq << " nhZq " << nhZq << " nhq " << nhq <<  std::endl;

/*  
   if      ((nH == 2) && (nSuub >= 0) && (ntop == 2) && (nW == 2)  && (nZ == 0))
   {
      _htht = true; 
   } 
   else if ((nH == 0) && (nSuub >= 0) && (ntop == 2) && (nW == 2)  && (nZ == 2))
   {
      _ZtZt = true;
   } 
   else if ((nH == 0) && (nSuub >= 2) && (ntop == 0) && (nW == 2)  && (nZ == 0))
   {
      _WbWb = true;
   } 
   else if ((nH == 1) && (nSuub >= 1) && (ntop == 1) && (nW == 2)  && (nZ == 0))
   {
      _htWb = true;
   }
   else if ((nH == 0) && (nSuub >= 1) && (ntop == 1) && (nW == 2)  && (nZ == 1))
   {
      _ZtWb = true;
   }
   else if ((nH == 1) && (nSuub >= 0) && (ntop == 2) && (nW == 2)  && (nZ == 1))
   {
      _htZt = true;
   }  
*/
   //if(!_ZtZt)return false;
   if (! ( _htWb || _htZt || _ZtWb || _WbWb || _htht || _ZtZt)  ) return false;
   else
   { 

      //std::cout << "nHtHt " << nHtHt<< " nWbWb "<< nWbWb<< " nZtZt " << nZtZt<< " nWbHt " << nWbHt<< " nWbZt " << nWbZt<< " nHtZ t" << nHtZt << std::endl;

      return true;
   }
   
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void
genPartFilter::beginStream(edm::StreamID)
{
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void
genPartFilter::endStream() {
}

// ------------ method called when starting to processes a run  ------------
/*
void
genPartFilter::beginRun(edm::Run const&, edm::EventSetup const&)
{ 
}
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
void
g
enPartFilter::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
void
genPartFilter::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
genPartFilter::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
genPartFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(genPartFilter);

