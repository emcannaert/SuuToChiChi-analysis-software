    bool fillSJVars(std::map<std::string, float> &treeVars, std::vector<fastjet::PseudoJet> iSJ, int nSuperJets);


// does filling of the superjet variables to give the NN
bool clusteringAnalyzerAll::fillSJVars(std::map<std::string, float> &treeVars, std::vector<fastjet::PseudoJet> iSJ, int nSuperJets )
{
    bool testNewVars = true; // include new SJ vars to give to NN

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
        sumPz += abs(iP_->pz());
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
    double SJ_75_px = 0, SJ_75_py=0,SJ_75_pz=0,SJ_75_E=0;
    double SJ_100_px = 0, SJ_100_py=0,SJ_100_pz=0,SJ_100_E=0;
    double SJ_150_px = 0, SJ_150_py=0,SJ_150_pz=0,SJ_150_E=0;
    double SJ_200_px = 0, SJ_200_py=0,SJ_200_pz=0,SJ_200_E=0;
    double SJ_300_px = 0, SJ_300_py=0,SJ_300_pz=0,SJ_300_E=0;
    double SJ_400_px = 0, SJ_400_py=0,SJ_400_pz=0,SJ_400_E=0;
    double SJ_500_px = 0, SJ_500_py=0,SJ_500_pz=0,SJ_500_E=0;
    double SJ_800_px = 0, SJ_800_py=0,SJ_800_pz=0,SJ_800_E=0;
    double SJ_1000_px = 0, SJ_1000_py=0,SJ_1000_pz=0,SJ_1000_E=0;

    int SJ_nAK4_1 = 0, SJ_nAK4_5 = 0, SJ_nAK4_10_ = 0;
    int SJ_nAK4_25_ = 0;
    int SJ_nAK4_50_ = 0, SJ_nAK4_75_ = 0, SJ_nAK4_100_ = 0,SJ_nAK4_150_ = 0,SJ_nAK4_200_ = 0,SJ_nAK4_300_ = 0;
    int SJ_nAK4_400_ = 0,SJ_nAK4_500_ = 0,SJ_nAK4_800_ = 0,SJ_nAK4_1000_ = 0;


    std::vector<TLorentzVector> AK41_parts;
    std::vector<TLorentzVector> AK42_parts;
    std::vector<TLorentzVector> AK43_parts;
    std::vector<TLorentzVector> AK44_parts;

    double AK41_px = 0, AK41_py=0,AK41_pz = 0, AK41_E = 0;
    double AK42_px = 0, AK42_py=0,AK42_pz = 0, AK42_E = 0;
    double AK43_px = 0, AK43_py=0,AK43_pz = 0, AK43_E = 0;
    double AK44_px = 0, AK44_py=0,AK44_pz = 0, AK44_E = 0;


    
    if (jetsFJ_jet.size() < 4) // fewer than 4 reclustered CA4 jets in superjet, this shouldn't reasonably happen ...
    {
        return false; // RETURN CUT
        std::cout << "A pseudojet vector has a size smaller than 2 - not reclustering enough jets from pool of particles - " << jetsFJ_jet.size() << std::endl;
    }

    int pseudoJetNum = 0;
    for (auto iPJ=jetsFJ_jet.begin(); iPJ<jetsFJ_jet.end(); iPJ++)                            
    {

        // do calculations of AK4 btagged particle ratios for leading 4 AK4 jets
        std::vector<fastjet::PseudoJet> iPJ_daughters = iPJ->constituents();

        if(pseudoJetNum == 0)
        {  
            treeVars["AK41_px"] = iPJ->px();
            treeVars["AK41_py"] = iPJ->py();
            treeVars["AK41_pz"] = iPJ->pz();
            treeVars["AK41_E"] = iPJ->E();
            for(auto iPart = iPJ_daughters.begin(); iPart != iPJ_daughters.end(); iPart++)
            {
                AK41_parts.push_back(TLorentzVector(iPart->px(),iPart->py(),iPart->pz(),iPart->E()));
                AK41_px+=iPart->px();AK41_py+=iPart->py();AK41_pz+=iPart->pz();AK41_E+=iPart->E();
            }
        }
        else if(pseudoJetNum == 1)
        {
            treeVars["AK42_px"] = iPJ->px();
            treeVars["AK42_py"] = iPJ->py();
            treeVars["AK42_pz"] = iPJ->pz();
            treeVars["AK42_E"] = iPJ->E();
            for(auto iPart = iPJ_daughters.begin(); iPart != iPJ_daughters.end(); iPart++)
            {
                AK42_parts.push_back(TLorentzVector(iPart->px(),iPart->py(),iPart->pz(),iPart->E()));
                AK42_px+=iPart->px();AK42_py+=iPart->py();AK42_pz+=iPart->pz();AK42_E+=iPart->E();
            }
        }
        else if(pseudoJetNum == 2)
        {
            treeVars["AK43_px"] = iPJ->px();
            treeVars["AK43_py"] = iPJ->py();
            treeVars["AK43_pz"] = iPJ->pz();
            treeVars["AK43_E"] = iPJ->E();
            for(auto iPart = iPJ_daughters.begin(); iPart != iPJ_daughters.end(); iPart++)
            {
                AK43_parts.push_back(TLorentzVector(iPart->px(),iPart->py(),iPart->pz(),iPart->E()));
                AK43_px+=iPart->px();AK43_py+=iPart->py();AK43_pz+=iPart->pz();AK43_E+=iPart->E();
            }
        }
        else if(pseudoJetNum == 3)
        {
            treeVars["AK44_px"] = iPJ->px();
            treeVars["AK44_py"] = iPJ->py();
            treeVars["AK44_pz"] = iPJ->pz();
            treeVars["AK44_E"] = iPJ->E();    
            for(auto iPart = iPJ_daughters.begin(); iPart != iPJ_daughters.end(); iPart++)
            {
                AK44_parts.push_back(TLorentzVector(iPart->px(),iPart->py(),iPart->pz(),iPart->E()));
                AK44_px+=iPart->px();AK44_py+=iPart->py();AK44_pz+=iPart->pz();AK44_E+=iPart->E();
            }
        }

        if(iPJ->E()>1.)    SJ_nAK4_1++;  // this is just used for a fraction calculation
        if(iPJ->E()>5.)    SJ_nAK4_5++;  // this is just used for a fraction calculation
        if(iPJ->E()>10.) SJ_nAK4_10_++;

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
        if(iPJ->E()>75.)
        {
            SJ_75_px+=iPJ->px();SJ_75_py+=iPJ->py();SJ_75_pz+=iPJ->pz();SJ_75_E+=iPJ->E();
            SJ_nAK4_75_++;
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
        if(iPJ->E()>400)
        {
            SJ_400_px+=iPJ->px();SJ_400_py+=iPJ->py();SJ_400_pz+=iPJ->pz();SJ_400_E+=iPJ->E();
            SJ_nAK4_400_++; 
        }
        if(iPJ->E()>500)
        {
            SJ_500_px+=iPJ->px();SJ_500_py+=iPJ->py();SJ_500_pz+=iPJ->pz();SJ_500_E+=iPJ->E();
            SJ_nAK4_500_++; 
        }
        if(iPJ->E()>800)
        {
            SJ_800_px+=iPJ->px();SJ_800_py+=iPJ->py();SJ_800_pz+=iPJ->pz();SJ_800_E+=iPJ->E();
            SJ_nAK4_800_++; 
        }
        if(iPJ->E()>1000)
        {
            SJ_1000_px+=iPJ->px();SJ_1000_py+=iPJ->py();SJ_1000_pz+=iPJ->pz();SJ_1000_E+=iPJ->E();
            SJ_nAK4_1000_++; 
        }
        pseudoJetNum++;
    }

    boostedSuperJetPart.clear();  //shouldn't be needed, just in case

    /////annoying process of getting the BES information for the reclustered AK4 jets

    TVector3 AK41_boost(AK41_px/AK41_E,AK41_py/AK41_E,AK41_pz/AK41_E);
    TVector3 AK42_boost(AK42_px/AK42_E,AK42_py/AK42_E,AK42_pz/AK42_E);
    TVector3 AK43_boost(AK43_px/AK43_E,AK43_py/AK43_E,AK43_pz/AK43_E);
    TVector3 AK44_boost(AK44_px/AK44_E,AK44_py/AK44_E,AK44_pz/AK44_E);

    std::vector<TLorentzVector> boostedAK41_Part_TLV;
    std::vector<reco::LeafCandidate> boostedAK41_Part_LC;
    std::vector<math::XYZVector> boostedAK41_Part_XYZ;

    std::vector<TLorentzVector> boostedAK42_Part_TLV;
    std::vector<reco::LeafCandidate> boostedAK42_Part_LC;
    std::vector<math::XYZVector> boostedAK42_Part_XYZ;

    std::vector<TLorentzVector> boostedAK43_Part_TLV;
    std::vector<reco::LeafCandidate> boostedAK43_Part_LC;
    std::vector<math::XYZVector> boostedAK43_Part_XYZ;

    std::vector<TLorentzVector> boostedAK44_Part_TLV;
    std::vector<reco::LeafCandidate> boostedAK44_Part_LC;
    std::vector<math::XYZVector> boostedAK44_Part_XYZ;

    double sumPz_AK41 =0,sumPz_AK42 = 0,sumPz_AK43 = 0,sumPz_AK44 = 0;
    double sumP_AK41 = 0,sumP_AK42 = 0,sumP_AK43 = 0, sumP_AK44 = 0;

    int n_AK41_parts_1 = 0, n_AK41_parts_5 = 0, n_AK41_parts_10 =0; // n_AK41_parts_20=0, n_AK41_parts_40=0, n_AK41_parts_50=0, n_AK41_parts_75=0, n_AK41_parts_100=0;
    int n_AK41_parts_0p1 = 0, n_AK41_parts_0p5 = 0, n_AK41_parts_2 =0, n_AK41_parts_7p5=0, n_AK41_parts_15=0;
    int n_AK42_parts_1 = 0, n_AK42_parts_5 = 0, n_AK42_parts_10 =0; 
    int n_AK42_parts_0p1 = 0, n_AK42_parts_0p5 = 0, n_AK42_parts_2 =0, n_AK42_parts_7p5=0, n_AK42_parts_15=0;
    int n_AK43_parts_1 = 0, n_AK43_parts_5 = 0, n_AK43_parts_10 =0; 
    int n_AK43_parts_0p1 = 0, n_AK43_parts_0p5 = 0, n_AK43_parts_2 =0, n_AK43_parts_7p5=0, n_AK43_parts_15=0;
    int n_AK44_parts_1 = 0, n_AK44_parts_5 = 0, n_AK44_parts_10 =0; 
    int n_AK44_parts_0p1 = 0, n_AK44_parts_0p5 = 0, n_AK44_parts_2 =0, n_AK44_parts_7p5=0, n_AK44_parts_15=0;



    // reclustered AK4 jets where only particles with energy greater than X are considered 
    TLorentzVector AK41_0p1(0,0,0,0); TLorentzVector AK41_0p5(0,0,0,0); TLorentzVector AK41_1(0,0,0,0); 
    TLorentzVector AK41_2(0,0,0,0); TLorentzVector AK41_5(0,0,0,0); TLorentzVector AK41_7p5(0,0,0,0);
    TLorentzVector AK41_10(0,0,0,0); TLorentzVector AK41_15(0,0,0,0);
    TLorentzVector AK41_20(0,0,0,0); //TLorentzVector AK41_40(0,0,0,0);
    //TLorentzVector AK41_50(0,0,0,0); TLorentzVector AK41_75(0,0,0,0); TLorentzVector AK41_100(0,0,0,0);
    TLorentzVector AK42_0p1(0,0,0,0); TLorentzVector AK42_0p5(0,0,0,0); TLorentzVector AK42_1(0,0,0,0); 
    TLorentzVector AK42_2(0,0,0,0); TLorentzVector AK42_5(0,0,0,0); TLorentzVector AK42_7p5(0,0,0,0);
    TLorentzVector AK42_10(0,0,0,0); TLorentzVector AK42_15(0,0,0,0);
    TLorentzVector AK42_20(0,0,0,0); 
    TLorentzVector AK43_0p1(0,0,0,0); TLorentzVector AK43_0p5(0,0,0,0); TLorentzVector AK43_1(0,0,0,0); 
    TLorentzVector AK43_2(0,0,0,0); TLorentzVector AK43_5(0,0,0,0); TLorentzVector AK43_7p5(0,0,0,0);
    TLorentzVector AK43_10(0,0,0,0); TLorentzVector AK43_15(0,0,0,0);
    TLorentzVector AK43_20(0,0,0,0); 
    TLorentzVector AK44_0p1(0,0,0,0); TLorentzVector AK44_0p5(0,0,0,0); TLorentzVector AK44_1(0,0,0,0); 
    TLorentzVector AK44_2(0,0,0,0); TLorentzVector AK44_5(0,0,0,0); TLorentzVector AK44_7p5(0,0,0,0);
    TLorentzVector AK44_10(0,0,0,0); TLorentzVector AK44_15(0,0,0,0);
    TLorentzVector AK44_20(0,0,0,0); 

    for(auto iP = AK41_parts.begin(); iP != AK41_parts.end(); iP++)
    {
        iP->Boost(-AK41_boost.X(),-AK41_boost.Y(), -AK41_boost.Z());
        boostedAK41_Part_TLV.push_back(TLorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E()));
        boostedAK41_Part_LC.push_back(reco::LeafCandidate(+1, reco::Candidate::LorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E())));
        boostedAK41_Part_XYZ.push_back(math::XYZVector( iP->Px(),iP->Py(),iP->Pz() ));
        if(iP->E() > 0.1)
        {
            AK41_0p1+= *iP;
            n_AK41_parts_0p1++;
        }
        if(iP->E() > 0.5)
        {
            AK41_0p5+= *iP;
            n_AK41_parts_0p5++;
        }
        if(iP->E() > 1)
        {
            AK41_1+= *iP;
            n_AK41_parts_1++;
        }
        if(iP->E() > 2)
        {
            AK41_2+= *iP;
            n_AK41_parts_2++;
        }
        if(iP->E() > 5)
        {
            AK41_5+= *iP;
            n_AK41_parts_5++;
        }
        if(iP->E() > 7.5)
        {
            AK41_7p5+= *iP;
            n_AK41_parts_7p5++;
        }
        if(iP->E() > 10)
        {
            AK41_10+= *iP;
            n_AK41_parts_10++;
        }
        if(iP->E() > 15)
        {
            AK41_15+= *iP;
            n_AK41_parts_15++;
        }
        sumPz_AK41+= abs(iP->Pz()); sumP_AK41+= abs(iP->P());
    }
    for(auto iP = AK42_parts.begin(); iP != AK42_parts.end(); iP++)
    {
        iP->Boost(-AK42_boost.X(),-AK42_boost.Y(), -AK42_boost.Z());
        boostedAK42_Part_TLV.push_back(TLorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E()));
        boostedAK42_Part_LC.push_back(reco::LeafCandidate(+1, reco::Candidate::LorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E())));
        boostedAK42_Part_XYZ.push_back(math::XYZVector( iP->Px(),iP->Py(),iP->Pz() ));    
        if(iP->E() > 0.1)
        {
            AK42_0p1+= *iP;
            n_AK42_parts_0p1++;
        }
        if(iP->E() > 0.5)
        {
            AK42_0p5+= *iP;
            n_AK42_parts_0p5++;
        }
        if(iP->E() > 1)
        {
            AK42_1+= *iP;
            n_AK42_parts_1++;
        }
        if(iP->E() > 2)
        {
            AK42_2+= *iP;
            n_AK42_parts_2++;
        }
        if(iP->E() > 5)
        {
            AK42_5+= *iP;
            n_AK42_parts_5++;
        }
        if(iP->E() > 7.5)
        {
            AK42_7p5+= *iP;
            n_AK42_parts_7p5++;
        }
        if(iP->E() > 10)
        {
            AK42_10+= *iP;
            n_AK42_parts_10++;
        }
        if(iP->E() > 15)
        {
            AK42_15+= *iP;
            n_AK42_parts_15++;
        }
        sumPz_AK42+= abs(iP->Pz()); sumP_AK42+= abs(iP->P());
    }
    for(auto iP = AK43_parts.begin(); iP != AK43_parts.end(); iP++)
    {
        iP->Boost(-AK43_boost.X(),-AK43_boost.Y(), -AK43_boost.Z());
        boostedAK43_Part_TLV.push_back(TLorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E()));
        boostedAK43_Part_LC.push_back(reco::LeafCandidate(+1, reco::Candidate::LorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E())));
        boostedAK43_Part_XYZ.push_back(math::XYZVector( iP->Px(),iP->Py(),iP->Pz() )); 
        if(iP->E() > 0.1)
        {
            AK43_0p1+= *iP;
            n_AK43_parts_0p1++;
        }
        if(iP->E() > 0.5)
        {
            AK43_0p5+= *iP;
            n_AK43_parts_0p5++;
        }
        if(iP->E() > 1)
        {
            AK43_1+= *iP;
            n_AK43_parts_1++;
        }
        if(iP->E() > 2)
        {
            AK43_2+= *iP;
            n_AK43_parts_2++;
        }
        if(iP->E() > 5)
        {
            AK43_5+= *iP;
            n_AK43_parts_5++;
        }
        if(iP->E() > 7.5)
        {
            AK43_7p5+= *iP;
            n_AK43_parts_7p5++;
        }
        if(iP->E() > 10)
        {
            AK43_10+= *iP;
            n_AK43_parts_10++;
        }
        if(iP->E() > 15)
        {
            AK43_15+= *iP;
            n_AK43_parts_15++;
        }
        sumPz_AK43 += abs(iP->Pz()); sumP_AK43 += abs(iP->P());  
    }
    for(auto iP = AK44_parts.begin(); iP != AK44_parts.end(); iP++)
    {
        iP->Boost(-AK44_boost.X(),-AK44_boost.Y(), -AK44_boost.Z());
        boostedAK44_Part_TLV.push_back(TLorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E()));
        boostedAK44_Part_LC.push_back(reco::LeafCandidate(+1, reco::Candidate::LorentzVector(iP->Px(),iP->Py(),iP->Pz(),iP->E())));
        boostedAK44_Part_XYZ.push_back(math::XYZVector( iP->Px(),iP->Py(),iP->Pz() )); 
        if(iP->E() > 0.1)
        {
            AK44_0p1+= *iP;
            n_AK44_parts_0p1++;
        }
        if(iP->E() > 0.5)
        {
            AK44_0p5+= *iP;
            n_AK44_parts_0p5++;
        }
        if(iP->E() > 1)
        {
            AK44_1+= *iP;
            n_AK44_parts_1++;
        }
        if(iP->E() > 2)
        {
            AK44_2+= *iP;
            n_AK44_parts_2++;
        }
        if(iP->E() > 5)
        {
            AK44_5+= *iP;
            n_AK44_parts_5++;
        }
        if(iP->E() > 7.5)
        {
            AK44_7p5+= *iP;
            n_AK44_parts_7p5++;
        }
        if(iP->E() > 10)
        {
            AK44_10+= *iP;
            n_AK44_parts_10++;
        }
        if(iP->E() > 15)
        {
            AK44_15+= *iP;
            n_AK44_parts_15++;
        }
        sumPz_AK44 += abs(iP->Pz()); sumP_AK44 += abs(iP->P());  
    }

    ////vectors to get angles
          
    TVector3 AK4_jet1(jetsFJ_jet[0].px(),jetsFJ_jet[0].py(),jetsFJ_jet[0].pz());
    TVector3 AK4_jet2(jetsFJ_jet[1].px(),jetsFJ_jet[1].py(),jetsFJ_jet[1].pz());
    TVector3 AK4_jet3(jetsFJ_jet[2].px(),jetsFJ_jet[2].py(),jetsFJ_jet[2].pz());
    TVector3 AK4_jet4(jetsFJ_jet[3].px(),jetsFJ_jet[3].py(),jetsFJ_jet[3].pz());

    //fill superjet variables here ...
    //SJ mass variables

    //treeVars["SJ_mass"]    = sqrt(pow(superJetE,2)-pow(superJetpx,2)-pow(superJetpy,2)-pow(superJetpz,2)); 
    treeVars["SJ_mass_25"] = sqrt(pow(SJ_25_E,2)-pow(SJ_25_px,2)-pow(SJ_25_py,2)-pow(SJ_25_pz,2)); 
    treeVars["SJ_mass_50"] = sqrt(pow(SJ_50_E,2)-pow(SJ_50_px,2)-pow(SJ_50_py,2)-pow(SJ_50_pz,2)); 
    treeVars["SJ_mass_100"] = sqrt(pow(SJ_100_E,2)-pow(SJ_100_px,2)-pow(SJ_100_py,2)-pow(SJ_100_pz,2)); 
    treeVars["SJ_mass_150"] = sqrt(pow(SJ_150_E,2)-pow(SJ_150_px,2)-pow(SJ_150_py,2)-pow(SJ_150_pz,2)); 
    treeVars["SJ_mass_200"] = sqrt(pow(SJ_200_E,2)-pow(SJ_200_px,2)-pow(SJ_200_py,2)-pow(SJ_200_pz,2)); 
    treeVars["SJ_mass_300"] = sqrt(pow(SJ_300_E,2)-pow(SJ_300_px,2)-pow(SJ_300_py,2)-pow(SJ_300_pz,2)); 

    treeVars["SJ_mass_400"] = sqrt(pow(SJ_400_E,2)-pow(SJ_400_px,2)-pow(SJ_400_py,2)-pow(SJ_400_pz,2)); 
    treeVars["SJ_mass_500"] = sqrt(pow(SJ_500_E,2)-pow(SJ_500_px,2)-pow(SJ_500_py,2)-pow(SJ_500_pz,2)); 
    treeVars["SJ_mass_800"] = sqrt(pow(SJ_800_E,2)-pow(SJ_800_px,2)-pow(SJ_800_py,2)-pow(SJ_800_pz,2)); 
    treeVars["SJ_mass_1000"] = sqrt(pow(SJ_1000_E,2)-pow(SJ_1000_px,2)-pow(SJ_1000_py,2)-pow(SJ_1000_pz,2)); 

    double offsetInts = 0.5;

    //SJ nAK4 variables
    treeVars["SJ_nAK4_25"] = SJ_nAK4_25_ + offsetInts; 
    treeVars["SJ_nAK4_50"] = SJ_nAK4_50_ + offsetInts; 
    treeVars["SJ_nAK4_100"] = SJ_nAK4_100_ + offsetInts; 
    treeVars["SJ_nAK4_150"] = SJ_nAK4_150_ + offsetInts; 
    treeVars["SJ_nAK4_200"] = SJ_nAK4_200_ + offsetInts; 
    treeVars["SJ_nAK4_300"] = SJ_nAK4_300_ + offsetInts; 
    treeVars["SJ_nAK4_400"] = SJ_nAK4_400_ + offsetInts; 
    treeVars["SJ_nAK4_500"] = SJ_nAK4_500_ + offsetInts; 
    treeVars["SJ_nAK4_800"] = SJ_nAK4_800_ + offsetInts; 
    treeVars["SJ_nAK4_1000"] = SJ_nAK4_1000_ + offsetInts; 


    treeVars["AK41_nDaughters"] = jetsFJ_jet[0].constituents().size() + offsetInts; 
    treeVars["AK42_nDaughters"] = jetsFJ_jet[1].constituents().size() + offsetInts; 
    treeVars["AK43_nDaughters"] = jetsFJ_jet[2].constituents().size() + offsetInts; 
    treeVars["AK44_nDaughters"] = jetsFJ_jet[3].constituents().size() + offsetInts; 


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

    AK4_theta12[nSuperJets] = cos(abs(AK4_jet1.Angle(AK4_jet2)));  
    AK4_theta13[nSuperJets] = cos(abs(AK4_jet1.Angle(AK4_jet3)));
    AK4_theta14[nSuperJets] = cos(abs(AK4_jet1.Angle(AK4_jet4)));
    AK4_theta23[nSuperJets] = cos(abs(AK4_jet2.Angle(AK4_jet3)));
    AK4_theta24[nSuperJets] = cos(abs(AK4_jet2.Angle(AK4_jet4)));
    AK4_theta34[nSuperJets] = cos(abs(AK4_jet3.Angle(AK4_jet4)));

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

    EventShapeVariables eventShapes( boostedSuperJetPart_XYZ );
    Thrust thrustCalculator( boostedSuperJetPart_LC.begin(), boostedSuperJetPart_LC.end() );
    double fwm[5] = { 0.0, 0.0 ,0.0 ,0.0,0.0};
    FWMoments( boostedSuperJetPart_TLV, fwm); 


    SJ_thrust[nSuperJets] = thrustCalculator.thrust();
    SJ_sphericity[nSuperJets] = eventShapes.sphericity();
    SJ_asymmetry[nSuperJets] = sumPz/sumP; 
    SJ_isotropy[nSuperJets] = eventShapes.isotropy();
    SJ_aplanarity[nSuperJets] = eventShapes.aplanarity();
    SJ_FW1[nSuperJets] = fwm[1]; 
    SJ_FW2[nSuperJets] = fwm[2]; 
    SJ_FW3[nSuperJets] = fwm[3]; 
    SJ_FW4[nSuperJets] = fwm[4];


    //AK4 jet mass combinations
    treeVars["AK4_m1"] = AK4_m1[nSuperJets]; 
    treeVars["AK4_m2"] = AK4_m2[nSuperJets]; 
    treeVars["AK4_m3"] = AK4_m3[nSuperJets]; 
    treeVars["AK4_m4"] = AK4_m4[nSuperJets]; 

    treeVars["AK41_E"] = AK41_E_tree[nSuperJets]; 
    treeVars["AK42_E"] = AK42_E_tree[nSuperJets]; 
    treeVars["AK43_E"] = AK43_E_tree[nSuperJets]; 
    treeVars["AK44_E"] = AK44_E_tree[nSuperJets]; 


    treeVars["AK4_m12"] = AK4_m12[nSuperJets];    
    treeVars["AK4_m13"] = AK4_m13[nSuperJets];    
    treeVars["AK4_m14"] = AK4_m14[nSuperJets];    
    treeVars["AK4_m23"] = AK4_m23[nSuperJets];    
    treeVars["AK4_m24"] = AK4_m24[nSuperJets];    
    treeVars["AK4_m34"] = AK4_m34[nSuperJets];    

    treeVars["AK4_m123"] = AK4_m123[nSuperJets];   
    treeVars["AK4_m124"] =AK4_m124[nSuperJets];  
    treeVars["AK4_m134"] =AK4_m134[nSuperJets];  
    treeVars["AK4_m234"] = AK4_m234[nSuperJets];   

    treeVars["AK4_m1234"] = AK4_m1234[nSuperJets];  
    

    //AK4 jet angles 
    treeVars["AK4_theta12"] = AK4_theta12[nSuperJets];   
    treeVars["AK4_theta13"] = AK4_theta13[nSuperJets];
    treeVars["AK4_theta14"] = AK4_theta14[nSuperJets];
    treeVars["AK4_theta23"] = AK4_theta23[nSuperJets];
    treeVars["AK4_theta24"] = AK4_theta24[nSuperJets];
    treeVars["AK4_theta34"] = AK4_theta34[nSuperJets];

    //AK4 jet boosted information - boost reclustered AK4 jets into their COM and look at BES variables, ndaughters, nsubjettiness
    treeVars["AK41_nsubjets"] = jetsFJ_jet[0].n_exclusive_subjets(0.2) + offsetInts; 
    treeVars["AK41_thrust"] = thrustCalculatorAK41.thrust();
    treeVars["AK41_sphericity"] = eventShapesAK41.sphericity();
    treeVars["AK41_asymmetry"] = sumPz_AK41/sumP_AK41; 
    treeVars["AK41_isotropy"] = eventShapesAK41.isotropy();
    treeVars["AK41_aplanarity"] = eventShapesAK41.aplanarity();
    treeVars["AK41_FW1"] = fwmAK41[1]; 
    treeVars["AK41_FW2"] = fwmAK41[2]; 
    treeVars["AK41_FW3"] = fwmAK41[3]; 
    treeVars["AK41_FW4"] = fwmAK41[4]; 

    treeVars["AK42_nsubjets"] = jetsFJ_jet[1].exclusive_subjets(0.2).size() + offsetInts;
    treeVars["AK42_thrust"] = thrustCalculatorAK42.thrust(); 
    treeVars["AK42_sphericity"] = eventShapesAK42.sphericity();
    treeVars["AK42_asymmetry"] = sumPz_AK42/sumP_AK42; 
    treeVars["AK42_isotropy"] = eventShapesAK42.isotropy();
    treeVars["AK42_aplanarity"] = eventShapesAK42.aplanarity();
    treeVars["AK42_FW1"] = fwmAK42[1]; 
    treeVars["AK42_FW2"] = fwmAK42[2]; 
    treeVars["AK42_FW3"] = fwmAK42[3]; 
    treeVars["AK42_FW4"] = fwmAK42[4]; 

    treeVars["AK43_nsubjets"] = jetsFJ_jet[2].exclusive_subjets(0.2).size() + offsetInts;
    treeVars["AK43_thrust"] = thrustCalculatorAK43.thrust();
    treeVars["AK43_sphericity"] = eventShapesAK43.sphericity();
    treeVars["AK43_asymmetry"] = sumPz_AK43/sumP_AK43; 
    treeVars["AK43_isotropy"] = eventShapesAK43.isotropy();
    treeVars["AK43_aplanarity"] = eventShapesAK43.aplanarity();
    treeVars["AK43_FW1"] = fwmAK43[1]; 
    treeVars["AK43_FW2"] = fwmAK43[2]; 
    treeVars["AK43_FW3"] = fwmAK43[3]; 
    treeVars["AK43_FW4"] = fwmAK43[4]; 

    treeVars["AK44_nsubjets"] = jetsFJ_jet[3].exclusive_subjets(0.2).size() + offsetInts;
    treeVars["AK44_thrust"] = thrustCalculatorAK44.thrust();
    treeVars["AK44_sphericity"] = eventShapesAK44.sphericity();
    treeVars["AK44_asymmetry"] = sumPz_AK44/sumP_AK44; 
    treeVars["AK44_isotropy"] = eventShapesAK44.isotropy();
    treeVars["AK44_aplanarity"] = eventShapesAK44.aplanarity();
    treeVars["AK44_FW1"] = fwmAK44[1]; 
    treeVars["AK44_FW2"] = fwmAK44[2]; 
    treeVars["AK44_FW3"] = fwmAK44[3]; 
    treeVars["AK44_FW4"] = fwmAK44[4]; 

    //Full SJ BES variablesf

    treeVars["SJ_thrust"] = thrustCalculator.thrust();
    treeVars["SJ_sphericity"] = eventShapes.sphericity();
    treeVars["SJ_asymmetry"] = sumPz/sumP; 
    treeVars["SJ_isotropy"] = eventShapes.isotropy();
    treeVars["SJ_aplanarity"] = eventShapes.aplanarity();
    treeVars["SJ_FW1"] = fwm[1]; 
    treeVars["SJ_FW2"] = fwm[2]; 
    treeVars["SJ_FW3"] = fwm[3]; 
    treeVars["SJ_FW4"] = fwm[4]; 

    if(testNewVars)
    {
        treeVars["SJ_AK4_frac_10"] = 1.0*SJ_nAK4_10_ / SJ_nAK4_1;
        treeVars["SJ_AK4_frac_25"] = 1.0*SJ_nAK4_25_ / SJ_nAK4_1;
        treeVars["SJ_AK4_frac_50"] = 1.0*SJ_nAK4_50_ / SJ_nAK4_1;
        treeVars["SJ_AK4_frac_75"] = 1.0*SJ_nAK4_75_ / SJ_nAK4_1;
        treeVars["SJ_AK4_frac_100"] = 1.0*SJ_nAK4_100_/ SJ_nAK4_1;
        treeVars["SJ_AK4_frac_200"] = 1.0*SJ_nAK4_200_/ SJ_nAK4_1;
        treeVars["SJ_AK4_frac_300"] = 1.0*SJ_nAK4_300_/ SJ_nAK4_1;
        treeVars["SJ_AK4_frac_500"] = 1.0*SJ_nAK4_500_ / SJ_nAK4_1;
        treeVars["SJ_AK4_frac_800"] = 1.0*SJ_nAK4_800_/ SJ_nAK4_1;

        treeVars["AK41_daughters_frac_0p1"] = 1.0*n_AK41_parts_0p1    /AK41_parts.size();   
        treeVars["AK41_daughters_frac_0p5"] = 1.0*n_AK41_parts_0p5    /AK41_parts.size();   
        treeVars["AK41_daughters_frac_1"] = 1.0*n_AK41_parts_1 /AK41_parts.size();  
        treeVars["AK41_daughters_frac_2"] = 1.0*n_AK41_parts_2 /AK41_parts.size();  
        treeVars["AK41_daughters_frac_5"] = 1.0*n_AK41_parts_5 /AK41_parts.size(); 
        treeVars["AK41_daughters_frac_7p5"] = 1.0*n_AK41_parts_7p5 /AK41_parts.size(); 
        treeVars["AK41_daughters_frac_10"] = 1.0*n_AK41_parts_10  /AK41_parts.size();  
        treeVars["AK41_daughters_frac_15"] = 1.0*n_AK41_parts_15 /AK41_parts.size();    

        treeVars["AK41_mass_0p1"] = AK41_0p1.M();
        treeVars["AK41_mass_0p5"] = AK41_0p5.M();
        treeVars["AK41_mass_1"] = AK41_1.M();
        treeVars["AK41_mass_2"] = AK41_2.M();
        //treeVars["AK41_mass_5"] = AK41_5.M();
        treeVars["AK41_mass_7p5"] = AK41_7p5.M();
        treeVars["AK41_mass_10"] = AK41_10.M();
        treeVars["AK41_mass_15"] = AK41_15.M();

        treeVars["AK42_daughters_frac_0p1"] = 1.0*n_AK42_parts_0p1    /AK42_parts.size();   
        treeVars["AK42_daughters_frac_0p5"] = 1.0*n_AK42_parts_0p5    /AK42_parts.size();   
        treeVars["AK42_daughters_frac_1"] = 1.0*n_AK42_parts_1 /AK42_parts.size();  
        treeVars["AK42_daughters_frac_2"] = 1.0*n_AK42_parts_2 /AK42_parts.size();  
        treeVars["AK42_daughters_frac_5"] = 1.0*n_AK42_parts_5 /AK42_parts.size(); 
        treeVars["AK42_daughters_frac_7p5"] = 1.0*n_AK42_parts_7p5 /AK42_parts.size(); 
        treeVars["AK42_daughters_frac_10"] = 1.0*n_AK42_parts_10  /AK42_parts.size();  
        treeVars["AK42_daughters_frac_15"] = 1.0*n_AK42_parts_15 /AK42_parts.size();    

        treeVars["AK42_mass_0p1"] = AK42_0p1.M();
        treeVars["AK42_mass_0p5"] = AK42_0p5.M();
        treeVars["AK42_mass_1"] = AK42_1.M();
        treeVars["AK42_mass_2"] = AK42_2.M();
        //treeVars["AK42_mass_5"] = AK42_5.M();
        treeVars["AK42_mass_7p5"] = AK42_7p5.M();
        treeVars["AK42_mass_10"] = AK42_10.M();
        treeVars["AK42_mass_15"] = AK42_15.M();

        treeVars["AK43_daughters_frac_0p1"] = 1.0*n_AK43_parts_0p1    /AK43_parts.size();   
        treeVars["AK43_daughters_frac_0p5"] = 1.0*n_AK43_parts_0p5    /AK43_parts.size();   
        treeVars["AK43_daughters_frac_1"] = 1.0*n_AK43_parts_1 /AK43_parts.size();  
        treeVars["AK43_daughters_frac_2"] = 1.0*n_AK43_parts_2 /AK43_parts.size();  
        treeVars["AK43_daughters_frac_5"] = 1.0*n_AK43_parts_5 /AK43_parts.size(); 
        treeVars["AK43_daughters_frac_7p5"] = 1.0*n_AK43_parts_7p5 /AK43_parts.size(); 
        treeVars["AK43_daughters_frac_10"] = 1.0*n_AK43_parts_10  /AK43_parts.size();  
        treeVars["AK43_daughters_frac_15"] = 1.0*n_AK43_parts_15 /AK43_parts.size();    

        treeVars["AK43_mass_0p1"] = AK43_0p1.M();
        treeVars["AK43_mass_0p5"] = AK43_0p5.M();
        treeVars["AK43_mass_1"] = AK43_1.M();
        treeVars["AK43_mass_2"] = AK43_2.M();
        //treeVars["AK43_mass_5"] = AK43_5.M();
        treeVars["AK43_mass_7p5"] = AK43_7p5.M();
        treeVars["AK43_mass_10"] = AK43_10.M();
        treeVars["AK43_mass_15"] = AK43_15.M();

        treeVars["AK44_daughters_frac_0p1"] = 1.0*n_AK44_parts_0p1    /AK44_parts.size();   
        treeVars["AK44_daughters_frac_0p5"] = 1.0*n_AK44_parts_0p5    /AK44_parts.size();   
        treeVars["AK44_daughters_frac_1"] = 1.0*n_AK44_parts_1 /AK44_parts.size();  
        treeVars["AK44_daughters_frac_2"] = 1.0*n_AK44_parts_2 /AK44_parts.size();  
        treeVars["AK44_daughters_frac_5"] = 1.0*n_AK44_parts_5 /AK44_parts.size(); 
        treeVars["AK44_daughters_frac_7p5"] = 1.0*n_AK44_parts_7p5 /AK44_parts.size(); 
        treeVars["AK44_daughters_frac_10"] = 1.0*n_AK44_parts_10  /AK44_parts.size();  
        treeVars["AK44_daughters_frac_15"] = 1.0*n_AK44_parts_15 /AK44_parts.size();    

        treeVars["AK44_mass_0p1"] = AK44_0p1.M();
        treeVars["AK44_mass_0p5"] = AK44_0p5.M();
        treeVars["AK44_mass_1"] = AK44_1.M();
        treeVars["AK44_mass_2"] = AK44_2.M();
        //treeVars["AK44_mass_5"] = AK44_5.M();
        treeVars["AK44_mass_7p5"] = AK44_7p5.M();
        treeVars["AK44_mass_10"] = AK44_10.M();
        treeVars["AK44_mass_15"] = AK44_15.M();

    }



    ///////////////////// BESvars for tree /////////////
    /////////// fill input variables to NN /////////////
    for (auto i = treeVars.begin(); i!=treeVars.end(); i++)
    {
        //std::cout<< i->first << " " << i->second << std::endl;
        if (  (i->second  != i->second ) || ( isinf(i->second )  ) )
        {
            i->second = 0;    //return false; // RETURN cut - event variables are NaN or inf
        }
        else if ( abs( i->second+999.99 ) < 1.0e-10 ) return false;
    }
    return true;

}


/*

    bool runBEST = false;


    runBEST   = iConfig.getParameter<bool>("runBEST");

    if(runBEST)
    {
        cache_ = new CacheHandler(path_);
        BEST_ = new BESTEvaluation(cache_);
        BEST_->configure(iConfig);
    }



    if(runBEST)
    {
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

        tree->Branch("AK4_m1",AK4_m1 , "AK4_m1[nSuperJets]/D");
        tree->Branch("AK4_m2",AK4_m2 , "AK4_m2[nSuperJets]/D");
        tree->Branch("AK4_m3",AK4_m3 , "AK4_m3[nSuperJets]/D");
        tree->Branch("AK4_m4",AK4_m4 , "AK4_m4[nSuperJets]/D");

        tree->Branch("nCategories", &nCategories, "nCategories/I");
        tree->Branch("SJ1_BEST_scores", &SJ1_BEST_scores, "SJ1_BEST_scores/D");
        tree->Branch("SJ2_BEST_scores", &SJ2_BEST_scores, "SJ2_BEST_scores/D");
        tree->Branch("SJ1_decision", &SJ1_decision, "SJ1_decision/I");
        tree->Branch("SJ2_decision", &SJ2_decision, "SJ2_decision/I");

    }


        if( runBEST )
        {

            ///////////////// /inside superjet loop //////////////////////
            ///////    fill BESTmap for superjet ////////////////////
            //////////////////////////////////////////////////////////////

            //////get BEST scores for superjet /////////
            BESTmap.clear();
            BESTmap["tot_pt"] = allAK8.Pt();
            BESTmap["tot_HT"] = totHT;

            BESTmap["eventNumber"] = eventNumber;

            if(_verbose)std::cout << "Filling BEST map in SJ " << nSuperJets <<std::endl;
            std::vector<float> BESTScores;
            if (!fillSJVars(BESTmap, *iSJ,nSuperJets))    //if this fails somehow, event is skipped
            {
                return;  // RETURN cut - tree was filled incorrectly
            }
            if(_verbose)std::cout << "Filled BEST map. Now getting prediction in SJ " << nSuperJets <<std::endl;


            BESTScores = BEST_->getPrediction(BESTmap);


            ///store BEST scores in tree
            int decision = (BESTScores[0] > 0.5) ? 0 : 1;

            if(_verbose)std::cout << "Got BEST prediction and decision in SJ " << nSuperJets <<std::endl;
            if (nSuperJets == 0)
            {
                SJ1_BEST_scores = static_cast<double> (BESTScores[0]);
                SJ1_decision = decision;
            }
            else if (nSuperJets == 1)
            {
                SJ2_BEST_scores = static_cast<double> (BESTScores[0]);
                SJ2_decision = decision;
            } 

        }*/



