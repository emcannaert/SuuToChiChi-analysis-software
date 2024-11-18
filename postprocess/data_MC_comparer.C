void write_cms_text(double CMS_label_pos, double SIM_label_pos, TCanvas * canvas) {
    // do all the fancy formatting 
    //gStyle->SetOptStat(0);
    
    TText *CMSLabel = new TText();
    CMSLabel->SetNDC();
    CMSLabel->SetTextFont(1);
    CMSLabel->SetTextColor(1);
    CMSLabel->SetTextSize(0.0385);
    CMSLabel->SetTextAlign(22);
    CMSLabel->SetTextAngle(0);
    CMSLabel->DrawText(CMS_label_pos, 0.92, "CMS");
    CMSLabel->Draw();
    
    TText *simLabel = new TText();
    simLabel->SetNDC();
    simLabel->SetTextFont(52);
    simLabel->SetTextColor(1);
    simLabel->SetTextSize(0.024);
    simLabel->SetTextAlign(22);
    simLabel->SetTextAngle(0);
    simLabel->DrawText(SIM_label_pos, 0.92, "Simulation Preliminary");
    simLabel->Draw();
    
    TLatex *latex = new TLatex();
    TString lumistuff = "(13 TeV)";
    latex->SetNDC();
    latex->SetTextAngle(0);
    latex->SetTextColor(kBlack);  
    latex->SetTextFont(42);
    latex->SetTextAlign(31);
    latex->SetTextSize(0.030); 
    latex->DrawLatex(0.88, 0.91, lumistuff.Data());
    //latex->DrawLatex(0.89, 0.91, lumistuff.Data()) ;
    canvas->Update();
    delete CMSLabel;
    delete simLabel;
    delete latex;
}

double return_BR_SF(std::string year, std::string sample)
{

    std::map<std::string, std::map<std::string, double>> scale_factors = {

        {"QCDMC1000to1500", {{"2015", 1.578683216}, {"2016", 1.482632755}, {"2017", 3.126481451}, {"2018", 4.407417122}}},
        {"QCDMC1500to2000", {{"2015", 0.2119142341}, {"2016", 0.195224041}, {"2017", 0.3197450474}, {"2018", 0.5425809983}}},
        {"QCDMC2000toInf", {{"2015", 0.08568186031}, {"2016", 0.07572795371}, {"2017", 0.14306915}, {"2018", 0.2277769275}}},
        {"TTToHadronicMC", {{"2015", 0.075592}, {"2016", 0.05808655696}, {"2017", 0.06651018525}, {"2018", 0.06588049107}}},
        {"TTToSemiLeptonicMC", {{"2015", 0.05395328118}, {"2016", 0.05808655696}, {"2017", 0.04264829286}, {"2018", 0.04563489275}}},
        {"TTToLeptonicMC", {{"2015", 0.0459517611}, {"2016", 0.03401684391}, {"2017", 0.03431532926}, {"2018", 0.03617828025}}},

        {"TTJetsMCHT800to1200", {{"2015", 0.002884466085}, {"2016", 0.002526405224}, {"2017", 0.003001100916}, {"2018", 0.004897196802}}},
        {"TTJetsMCHT1200to2500", {{"2015", 0.002722324842}, {"2016", 0.002255554525}, {"2017", 0.00267594799}, {"2018", 0.003918532089}}},
        {"TTJetsMCHT2500toInf", {{"2015", 0.000056798633}, {"2016", 0.000050253843}, {"2017", 0.00005947217}, {"2018", 0.000084089656}}},

        {"ST_t_channel_top_inclMC", {{"2015", 0.0409963154}, {"2016", 0.03607115071}, {"2017", 0.03494669125}, {"2018", 0.03859114659}}},
        {"ST_t_channel_antitop_incMC", {{"2015", 0.05673857623}, {"2016", 0.04102705994}, {"2017", 0.04238814865}, {"2018", 0.03606630944}}},
        {"ST_s_channel_hadronsMC", {{"2015", 0.04668187234}, {"2016", 0.03564988679}, {"2017", 0.03985938616}, {"2018", 0.04102795437}}},
        {"ST_s_channel_leptonsMC", {{"2015", 0.01323030083}, {"2016", 0.01149139097}, {"2017", 0.01117527734}, {"2018", 0.01155448784}}},
        {"ST_tW_antiTop_inclMC", {{"2015", 0.2967888696}, {"2016", 0.2301666797}, {"2017", 0.2556495594}, {"2018", 0.2700032391}}},
        {"ST_tW_top_inclMC", {{"2015", 0.2962796522}, {"2016", 0.2355829386}, {"2017", 0.2563403788}, {"2018", 0.2625270613}}},

        {"WJetsMC_LNu-HT800to1200", {{"2015", 0.04172270958}, {"2016", 0.04230432205}, {"2017", 0.04374224695}, {"2018", 0.04394190568}}},
        {"WJetsMC_LNu-HT1200to2500", {{"2015", 0.01068088067}, {"2016", 0.00932744847}, {"2017", 0.009709510545}, {"2018", 0.01070780024}}},
        {"WJetsMC_LNu-HT2500toInf", {{"2015", 0.0001931363546}, {"2016", 0.0001895618832}, {"2017", 0.0002799036518}, {"2018", 0.0007547032677}}},
        {"WJetsMC_QQ-HT800toInf", {{"2015", 0.072501767}, {"2016", 0.07139611301}, {"2017", 0.08100232455}, {"2018", 0.128194465}}},

        {"WW_MC", {{"2015", 0.09385207138}, {"2016", 0.08101652866}, {"2017", 0.2023058718}, {"2018", 0.2909648256}}},
        {"ZZ_MC", {{"2015", 0.1848461778}, {"2016", 0.1773009557}, {"2017", 0.1860928307}, {"2018", 0.2059943846}}}

    };
    return scale_factors[sample][year];

}


//// give list of filenames and histogram names (with folder names) and this will return a vector of that histogram from the given files
////   looks for histograms named according to this format :    (hist_name).c_str()
template <typename T> std::vector<T> get_histograms(std::vector<std::string> fnames, std::string hist_name)
{

    TH1::SetDefaultSumw2();
    TH1::AddDirectory(false);


    std::vector<T> return_files;
    std::cout <<fnames.size() << " files found. " << std::endl;

    for(auto iii = fnames.begin();iii<fnames.end();iii++)
    {
      std::cout << "looking for histogram " << (hist_name).c_str() << " in " << *iii <<std::endl;

      TFile * f1 = new TFile((*iii).c_str(), "READ" ); // open TFile for each fname
      return_files.push_back( (T) f1->Get(  (hist_name).c_str() )  );
      std::cout << "Found histogram " << hist_name << " in " << (*iii).c_str() << ", Total number of events in histogram: " << ((T) f1->Get(  (hist_name).c_str() ))->Integral() << std::endl;
      f1->Close();
      delete f1;
      //std::cout << "File: " << typeid((T)(*iii)->Get( ("nom_/" + hist_name).c_str() )).name() << " " << std::endl;
    }
    std::cout << std::endl;
    return return_files;
}


//// give list of histograms and weights and this will return a combined histogram
template <typename T> T combine_histograms(std::vector<T> _hists, double weights[])
{


  TH1::SetDefaultSumw2();
  TH1::AddDirectory(false);

  T first_hist_scaled = T(_hists[0]);
  double original_events = first_hist_scaled->Integral();


  std::cout << "Events in histogram 0: " << original_events << std::endl;

  first_hist_scaled->Scale(weights[0]);

  T comb_hist = T(first_hist_scaled);
  int counter = 1;
  for(auto iii = _hists.begin() + 1;iii<_hists.end();iii++)
  {

    original_events = (*iii)->Integral();
    std::cout << "Events in histogram " << counter << ": " << (*iii)->Integral() << std::endl;
    T dummy_hist = T(*iii);
    dummy_hist->Scale(weights[counter+1]);
    //(*iii)->Scale(weights[counter+1]);
    comb_hist->Add(dummy_hist);
    counter++;
  }
  return comb_hist;
}

// given a histogram and some x_threshold, this masks histograms by replacing all values above the threshold by 0
void mask_histogram(TH1* hist, double x_threshold=1e10) {
    // Get the number of bins in the histogram
    int n_bins = hist->GetNbinsX();
    TH1::SetDefaultSumw2();
    // Loop over all bins
    for (int i = 1; i <= n_bins; ++i) {  // Bin index starts at 1 in ROOT
        // Get the x-axis bin center
        double x_value = hist->GetBinCenter(i);
        
        // If the x-value exceeds the threshold, set the bin content and error to 0
        if (x_value > x_threshold) {
            hist->SetBinContent(i, 0);
            hist->SetBinError(i, 0);  // Optionally, also reset the bin error to 0
        }
    }
}

void make_plot(std::string year, std::string histName, bool runControlRegions = false , bool runSideband = false, std::string region = "", bool doMasking=false) 
{

    double CMS_label_pos = 0.125;
    double SIM_label_pos = 0.225;

    TH1::SetDefaultSumw2();

    bool necessaryToMask = doMasking;
    if( (region == "AT1b") || (region== "AT0b") || (region == "SB1b") || (region == "SB0b"))necessaryToMask = false; // these don't need to be masked
    else if (( histName == "h_nAK4_all")   ||  (histName == "h_nfatjets") || (histName == "h_nfatjets_pre") || (histName == "h_nCA4_300_1b") || (histName == "h_nCA4_300_0b")   )necessaryToMask = false; // these don't need to be masked
    else if ( (histName == "h_nfatjets")  || (histName == "h_nfatjets_pre") || (histName== "h_AK4_pt") || (histName == "h_nAK4") || (histName == "h_AK4_pt") || (histName == "h_AK8_mass") || (histName== "h_AK4_mass"))necessaryToMask = false;
    
    std::vector<std::string> nonMaskedHists = {"h_nHeavyAK8_pt400_M10", "h_nHeavyAK8_pt400_M20", "h_nHeavyAK8_pt400_M30", "h_nHeavyAK8_pt300_M10", "h_nHeavyAK8_pt300_M20", "h_nHeavyAK8_pt300_M30",
     "h_nHeavyAK8_pt200_M10", "h_nHeavyAK8_pt200_M20", "h_nHeavyAK8_pt200_M30",
    "h_nAK8_pt200", "h_nAK8_pt300", "h_nAK8_pt150", "h_nAK8_pt500",
    "h_nAK8_pt200_noCorr", "h_nAK8_pt300_noCorr", "h_nAK8_pt150_noCorr", "h_nAK8_pt500_noCorr", "h_nHeavyAK8_pt500_M45", "h_nHeavyAK8_pt500_M45_noCorr","h_AK4_eta", "h_AK4_phi", "h_AK8_eta", "h_AK8_phi"};

    if (std::find(nonMaskedHists.begin(), nonMaskedHists.end(), histName) != nonMaskedHists.end()) necessaryToMask = false;


    std::string year_str = year;

    if (year == "2015") year_str = "2016preAPV";
    else if (year == "2016") year_str = "2016postAPV";

    std::map<std::string, double> maskValues = {  {"h_disuperjet_mass", 4000   } ,  {"h_SJ_mass", 3500  }, {"h_totHT", 3500} , {"h_dijet_mass", 1000} , {"h_AK8_jet_mass", 1000} , {"h_AK8_jet_pt",2000} } ; // mask threshold for various histogram types

    std::string histTitleDataMC = histName + " - data vs combined BR (" + year_str  + ") ";
    if (region != "") histTitleDataMC += Form(" (%s)", region.c_str());



    TCanvas* c = new TCanvas("c", "", 1250, 1000);

    std::string processedFilePaths = "../combinedROOT/processedFiles_selectionStudy/";
    std::string output_path        = "plots/dataMC/selectionStudy/";
    std::string folderName = histName;

    std::string saveStr    = ""; 

    //saveStr = region + "_";

    if (runControlRegions)
    {

        folderName = "nom/" + histName + "_" + region;

        if (saveStr == "") saveStr    = "";
        if ( !(histName == "h_disuperjet_mass") && !(histName == "h_SJ_mass")  )
        {
            folderName = "nom/" + histName;
            saveStr    = ""; 
        }

        std::cout << "----------------- Creating control region plots ------------------ " << std::endl;
        if(runSideband) processedFilePaths = "../combinedROOT/sideband_processedFiles/";
        else{ processedFilePaths = "../combinedROOT/processedFiles/"; }

        std::cout << "Using files in " << processedFilePaths << std::endl;

        output_path        = "plots/dataMC/controlRegions/";

        std::cout << "folderName is "  << folderName << " processedFilePaths is " << processedFilePaths << std::endl;
    }




    std::vector<std::string> dataFileNames;
    dataFileNames = {(processedFilePaths+"dataB-ver2_" + year+ "_processed.root").c_str(),(processedFilePaths+"dataC-HIPM_" + year+ "_processed.root").c_str(),(processedFilePaths+"dataD-HIPM_" + year+ "_processed.root").c_str(),(processedFilePaths+"dataE-HIPM_" + year+ "_processed.root").c_str(),(processedFilePaths+"dataF-HIPM_" + year+ "_processed.root").c_str()};
    if(year == "2016")dataFileNames = {(processedFilePaths+"dataF_" + year+ "_processed.root").c_str(), (processedFilePaths+"dataG_" + year+ "_processed.root").c_str(), (processedFilePaths+"dataH_" + year+ "_processed.root").c_str()};
    else if(year == "2017")dataFileNames = { (processedFilePaths+"dataB_" + year+ "_processed.root").c_str(),(processedFilePaths+"dataC_" + year+ "_processed.root").c_str(),(processedFilePaths+"dataD_" + year+ "_processed.root").c_str(),(processedFilePaths+"dataE_" + year+ "_processed.root").c_str(), (processedFilePaths+"dataF_" + year+ "_processed.root").c_str()};
    else if(year == "2018")dataFileNames = {(processedFilePaths+"dataA_" + year+ "_processed.root").c_str(),(processedFilePaths+"dataB_" + year+ "_processed.root").c_str(),(processedFilePaths+"dataC_" + year+ "_processed.root").c_str(),(processedFilePaths+"dataD_" + year+ "_processed.root").c_str()};


    // this is annoying here because the SB regions use different files ...

    std::string QCD1000to1500_filename      = processedFilePaths + "QCDMC1000to1500_" + year+ "_processed.root";
    std::string QCD1500to2000_filename      = processedFilePaths + "QCDMC1500to2000_" + year+ "_processed.root";
    std::string QCD2000toInf_filename       = processedFilePaths +"QCDMC2000toInf_" + year+ "_processed.root";

    std::string TTToHadronic_filename       = processedFilePaths +"TTToHadronicMC_" + year+ "_processed.root";
    std::string TTToSemiLeptonic_filename   = processedFilePaths +"TTToSemiLeptonicMC_" + year+ "_processed.root";
    std::string TTToLeptonic_filename       = processedFilePaths +"TTToLeptonicMC_" + year+ "_processed.root";
                 
    std::string TTJetMCHT800to1200_filename = processedFilePaths +"TTJetsMCHT800to1200_" + year+ "_processed.root";
    std::string TTJetMCHT1200to2500_filename = processedFilePaths +"TTJetsMCHT1200to2500_" + year+ "_processed.root";

    std::string ST_t_channel_top_inclMC_filename        = processedFilePaths + "ST_t-channel-top_inclMC_" + year+ "_processed.root";
    std::string ST_t_channel_antitop_inclMC_filename    = processedFilePaths + "ST_t-channel-antitop_inclMC_" + year+ "_processed.root";
    std::string ST_s_channel_hadronsMC_filename         = processedFilePaths + "ST_s-channel-hadronsMC_" + year+ "_processed.root";
    std::string ST_s_channel_leptonsMC_filename         = processedFilePaths + "ST_s-channel-leptonsMC_" + year+ "_processed.root";
    std::string ST_tW_antiTop_inclMC_filename           = processedFilePaths + "ST_tW-antiTop_inclMC_" + year+ "_processed.root";
    std::string ST_tW_top_inclMC_filename               = processedFilePaths + "ST_tW-top_inclMC_" + year+ "_processed.root";




    double QCD1000to1500_SF        = return_BR_SF(year, "QCDMC1000to1500" );
    double QCD1500to2000_SF        = return_BR_SF(year, "QCDMC1500to2000" );
    double QCD2000toInf_SF         = return_BR_SF(year, "QCDMC2000toInf" );
    double TTToHadronic_SF         = return_BR_SF(year, "TTToHadronicMC" );
    double TTToSemiLeptonic_SF     = return_BR_SF(year, "TTToSemiLeptonic" );
    double TTToLeptonic_SF         = return_BR_SF(year, "TTToLeptonic" );
    double TTJetsMCHT800to1200_SF  = return_BR_SF(year, "TTJetsMCHT800to1200" );
    double TTJetsMCHT1200to2500_SF = return_BR_SF(year, "TTJetsMCHT1200to2500" );

    double ST_t_channel_top_inclMC_SF       = return_BR_SF(year, "ST_t_channel_top_inclMC" );
    double ST_t_channel_antitop_inclMC_SF   = return_BR_SF(year, "ST_t_channel_antitop_inclMC" );
    double ST_s_channel_hadronsMC_SF        = return_BR_SF(year, "ST_s_channel_hadronsMC" );
    double ST_s_channel_leptonsMC_SF        = return_BR_SF(year, "ST_s_channel_leptonsMC" );
    double ST_tW_antiTop_inclMC_SF          = return_BR_SF(year, "ST_tW_antiTop_inclMC" );
    double ST_tW_top_inclMC_SF              = return_BR_SF(year, "ST_tW_top_inclMC" );


    double data_weights[10] = {1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0};

    std::vector<TH1F*>  h_data_hists    = get_histograms<TH1F*>(dataFileNames, folderName);


    std::cout << "Got data histograms for " << year << "/" <<  histName << "/"<< region << std::endl;
    TH1F*  h_data_combined    = combine_histograms<TH1F*>(h_data_hists,data_weights);
    h_data_combined->Sumw2();
    std::cout << "For " << year << ", the total number of DATA events is " << h_data_combined->Integral() << std::endl;

    // Open background files and get histograms

    TFile* bgFiles[10];
    TH1* hBackgrounds[10];
    TH1F * QCD_combined;
    TH1F * TTbar_combined;
    TH1F * ST_combined;
    std::string hStack_yaxis_title = "";
    if (!runSideband) 
    {
        bgFiles[0] = TFile::Open(QCD1000to1500_filename.c_str()); 
        bgFiles[1] = TFile::Open(QCD1500to2000_filename.c_str());
        bgFiles[2] = TFile::Open(QCD2000toInf_filename.c_str());
        bgFiles[3] = TFile::Open(TTToHadronic_filename.c_str());
        bgFiles[4] = TFile::Open(TTToSemiLeptonic_filename.c_str());
        bgFiles[5] = TFile::Open(TTToLeptonic_filename.c_str());

        hBackgrounds[0] = (TH1*)bgFiles[0]->Get( (folderName).c_str());  
        hBackgrounds[1] = (TH1*)bgFiles[1]->Get( (folderName).c_str());
        hBackgrounds[2] = (TH1*)bgFiles[2]->Get( (folderName).c_str());
        hBackgrounds[3] = (TH1*)bgFiles[3]->Get( (folderName).c_str());
        hBackgrounds[4] = (TH1*)bgFiles[4]->Get( (folderName).c_str());
        hBackgrounds[5] = (TH1*)bgFiles[5]->Get( (folderName).c_str());

        // Scale histograms
        hBackgrounds[0]->Scale(QCD1000to1500_SF);
        hBackgrounds[1]->Scale(QCD1500to2000_SF);
        hBackgrounds[2]->Scale(QCD2000toInf_SF);
        hBackgrounds[3]->Scale(TTToHadronic_SF);
        hBackgrounds[4]->Scale(TTToSemiLeptonic_SF);
        hBackgrounds[5]->Scale(TTToLeptonic_SF);


        hBackgrounds[0]->SetTitle( (histName + " - QCDMCHT1000to1500 (" + year  + ") ").c_str()    );
        hBackgrounds[1]->SetTitle( (histName + " - QCDMCHT1500to2000 (" + year  + ") ").c_str() );
        hBackgrounds[2]->SetTitle( (histName + " - QCDMCHT2000toInf (" + year  + ") ").c_str() );
        hBackgrounds[3]->SetTitle( (histName + " - TTToHadronicMC (" + year  + ") ").c_str() );
        hBackgrounds[4]->SetTitle( (histName + " - TTToSemiLeptonicMC (" + year  + ") ").c_str() );
        hBackgrounds[5]->SetTitle( (histName + " - TTToLeptonicMC (" + year  + ") ").c_str() );


        hStack_yaxis_title = hBackgrounds[0]->GetYaxis()->GetTitle();

        hBackgrounds[0]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path+ "backgrounds/"+ histName+  "_QCDMC1000to1500_" + year +".png").c_str()   );

        hBackgrounds[1]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path+  "backgrounds/"+histName + "_QCDMC1500to2000_" + year +".png").c_str()   );
        
        hBackgrounds[2]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path+ "backgrounds/"+histName + "_QCDMC2000toInf_" + year +".png").c_str()   );

        hBackgrounds[3]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path+ "backgrounds/"+histName + "_TTToHadronic_" + year +".png").c_str()   );

        hBackgrounds[4]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path+ "backgrounds/"+histName + "_TTToSemiLeptonic_" + year +".png").c_str()   );

        hBackgrounds[5]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path+ "backgrounds/"+histName + "_TTToLeptonic_" + year +".png").c_str()   );


        QCD_combined = (TH1F*)hBackgrounds[0]->Clone("QCD_combined");
        QCD_combined->Add(hBackgrounds[1]);
        QCD_combined->Add(hBackgrounds[2]);

        std::cout << "For " << year << ", the total number of QCD events is " << QCD_combined->Integral() << std::endl;
        QCD_combined->SetFillColor(kRed);

        TTbar_combined = (TH1F*)hBackgrounds[3]->Clone("TTbar_combined");
        TTbar_combined->Add(hBackgrounds[4]);
        TTbar_combined->Add(hBackgrounds[5]);
        std::cout << "For " << year << ", the total number of TTbar events is " << TTbar_combined->Integral() << std::endl;
    }
    else  // running the sideband
    {
        bgFiles[0] = TFile::Open(QCD1000to1500_filename.c_str()); 
        bgFiles[1] = TFile::Open(QCD1500to2000_filename.c_str());
        bgFiles[2] = TFile::Open(TTJetMCHT800to1200_filename.c_str());
        bgFiles[3] = TFile::Open(TTJetMCHT1200to2500_filename.c_str());
        bgFiles[4] = TFile::Open(ST_t_channel_top_inclMC_filename.c_str());
        bgFiles[5] = TFile::Open(ST_t_channel_antitop_inclMC_filename.c_str());
        bgFiles[6] = TFile::Open(ST_s_channel_hadronsMC_filename.c_str());
        bgFiles[7] = TFile::Open(ST_s_channel_leptonsMC_filename.c_str());
        bgFiles[8] = TFile::Open(ST_tW_antiTop_inclMC_filename.c_str());
        bgFiles[9] = TFile::Open(ST_tW_top_inclMC_filename.c_str());


        hBackgrounds[0] = (TH1*)bgFiles[0]->Get( (folderName).c_str());   // QCD1000to1500
        hBackgrounds[1] = (TH1*)bgFiles[1]->Get( (folderName).c_str());   // QCD1500to2000
        hBackgrounds[2] = (TH1*)bgFiles[2]->Get( (folderName).c_str());   //TTJets800to1200
        hBackgrounds[3] = (TH1*)bgFiles[3]->Get( (folderName).c_str());   //TTJets1200to2500

        hBackgrounds[4] = (TH1*)bgFiles[4]->Get( (folderName).c_str());   //TTJets1200to2500
        hBackgrounds[5] = (TH1*)bgFiles[5]->Get( (folderName).c_str());   //TTJets1200to2500
        hBackgrounds[6] = (TH1*)bgFiles[6]->Get( (folderName).c_str());   //TTJets1200to2500
        hBackgrounds[7] = (TH1*)bgFiles[7]->Get( (folderName).c_str());   //TTJets1200to2500
        hBackgrounds[8] = (TH1*)bgFiles[8]->Get( (folderName).c_str());   //TTJets1200to2500
        hBackgrounds[9] = (TH1*)bgFiles[9]->Get( (folderName).c_str());   //TTJets1200to2500

        // Scale histograms
        hBackgrounds[0]->Scale(QCD1000to1500_SF);
        hBackgrounds[1]->Scale(QCD1500to2000_SF);
        hBackgrounds[2]->Scale(TTJetsMCHT800to1200_SF);
        hBackgrounds[3]->Scale(TTJetsMCHT1200to2500_SF);

        hBackgrounds[4]->Scale(ST_t_channel_top_inclMC_SF);
        hBackgrounds[5]->Scale(ST_t_channel_antitop_inclMC_SF);
        hBackgrounds[6]->Scale(ST_s_channel_hadronsMC_SF);
        hBackgrounds[7]->Scale(ST_s_channel_leptonsMC_SF);
        hBackgrounds[8]->Scale(ST_tW_antiTop_inclMC_SF);
        hBackgrounds[9]->Scale(ST_tW_top_inclMC_SF);


        hBackgrounds[0]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path+ "backgrounds/" + histName+  "_QCDMC1000to1500_" + saveStr + year +".png").c_str()   );

        hBackgrounds[1]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path+ "backgrounds/" + histName + "_QCDMC1500to2000_" + saveStr + year +".png").c_str()   );
        
        hBackgrounds[2]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path+ "backgrounds/" +histName + "_TTJetsMCHT800to1200_" + saveStr + year +".png").c_str()   );

        hBackgrounds[3]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path+ "backgrounds/" +histName + "_TTJetsMCHT1200to2500_" + saveStr + year +".png").c_str()   );


        hBackgrounds[4]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path+ "backgrounds/" +histName + "_ST_t_channel_top_inclMC_" + saveStr + year +".png").c_str()   );


        hBackgrounds[5]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path+ "backgrounds/" +histName + "_ST_t_channel_antitop_inclMC_" + saveStr + year +".png").c_str()   );


        hBackgrounds[6]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path + "backgrounds/" +histName + "_ST_s_channel_hadronsMC_" + saveStr + year +".png").c_str()   );


        hBackgrounds[7]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path+ "backgrounds/" +histName + "_ST_s_channel_leptonsMC_" + saveStr + year +".png").c_str()   );


        hBackgrounds[8]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path+ "backgrounds/" +histName + "_ST_tW_antiTop_inclMC_" + saveStr + year +".png").c_str()   );


        hBackgrounds[9]->Draw("HIST");
        write_cms_text(CMS_label_pos,SIM_label_pos, c);
        c->SaveAs( (output_path+ "backgrounds/" +histName + "_ST_tW_top_inclMC_" + saveStr + year +".png").c_str()   );


        QCD_combined = (TH1F*)hBackgrounds[0]->Clone("QCD_combined");
        QCD_combined->Add(hBackgrounds[1]);

        std::cout << "For " << year << ", the total number of QCD events is " << QCD_combined->Integral() << std::endl;
        QCD_combined->SetFillColor(kRed);

        TTbar_combined = (TH1F*)hBackgrounds[2]->Clone("TTbar_combined");
        TTbar_combined->Add(hBackgrounds[3]);

        ST_combined = (TH1F*)hBackgrounds[4]->Clone("ST_combined");
        ST_combined->Add(hBackgrounds[5]);
        ST_combined->Add(hBackgrounds[6]);
        ST_combined->Add(hBackgrounds[7]);
        ST_combined->Add(hBackgrounds[8]);
        ST_combined->Add(hBackgrounds[9]);

        std::cout << "For " << year << ", the total number of ST (HT-binned) events is " << ST_combined->Integral() << std::endl;

    }




    ///  do data / MC comparison

    TTbar_combined->SetFillColor(kYellow);


    TH1F * MC_BR_combined = (TH1F*)QCD_combined->Clone("MC_BR_combined");
    MC_BR_combined->Sumw2();
    MC_BR_combined->Add(TTbar_combined);
    if(runSideband)MC_BR_combined->Add(ST_combined);
    // Create a THStack and add all histograms
    THStack* hs = new THStack("hs", ("Combined BR (QCD+TTbar) (" + year_str + ")").c_str()  );
    hs->Add(QCD_combined);
    hs->Add(TTbar_combined);

    if(runSideband)hs->Add(ST_combined);


    hs->SetMinimum(1e-2);

    // Create canvas and pads
    gStyle->SetOptStat(0);
    TPad* pad1 = new TPad("pad1", "Top pad", 0, 0.3, 1, 1);
    TPad* pad2 = new TPad("pad2", "Bottom pad", 0, 0, 1, 0.3);
    pad1->SetBottomMargin(0.01);
    pad2->SetTopMargin(0.01);
    pad2->SetBottomMargin(0.3);
    pad1->SetLogy();
    pad1->Draw();
    pad2->Draw();


    // Draw the stack and data on the upper pad
    pad1->cd();

        
    hs->SetTitle(histTitleDataMC.c_str());
    h_data_combined->SetTitle(histTitleDataMC.c_str());

    //if (h_data_combined->GetMaximum() < MC_BR_combined->GetMaximum())
    //{
    h_data_combined->SetMaximum(1.25*MC_BR_combined->GetMaximum());
    //}

    hs->Draw("HIST");
    hs->GetYaxis()->SetTitle( hStack_yaxis_title.c_str() );
    hs->GetYaxis()->SetLabelOffset(0.02);

    h_data_combined->Draw("SAME");
    write_cms_text(CMS_label_pos,SIM_label_pos, c);

    h_data_combined->SetMarkerStyle(20);

    if(necessaryToMask ) mask_histogram(h_data_combined, maskValues[histName]); // mask this histogram if necessary (= region is SR/CR, hist is a sensitive one)


    // Draw ratio plot on the lower pad
    pad2->cd();
    TH1* hRatio = (TH1*)h_data_combined->Clone("hRatio");
    hRatio->Sumw2();
    hRatio->SetTitle("");
    hRatio->GetYaxis()->SetTitle("data/MC");
    hRatio->Divide(MC_BR_combined);   // this might be incorrect ...
    hRatio->SetMinimum(0.25); // Set y-axis range for ratio plot
    hRatio->SetMaximum(3.0);
    hRatio->GetYaxis()->SetLabelOffset(0.05);
    hRatio->SetMarkerStyle(20);
    hRatio->SetFillColor(kGray);
    hRatio->Draw("E2");


    // Get the x-axis range for the lines
    double x_min = hRatio->GetXaxis()->GetXmin();
    double x_max = hRatio->GetXaxis()->GetXmax();

    // Draw TLines at 0.8, 1.0, and 1.2
    TLine *line_08 = new TLine(x_min, 0.8, x_max, 0.8);
    TLine *line_10 = new TLine(x_min, 1.0, x_max, 1.0);
    TLine *line_12 = new TLine(x_min, 1.2, x_max, 1.2);

    // Set line styles (optional)
    line_08->SetLineStyle(2); // dashed line
    line_10->SetLineStyle(1); // solid line
    line_12->SetLineStyle(2); // dashed line


    // Draw the lines on the current pad
    line_08->Draw();
    line_10->Draw();
    line_12->Draw();


    hRatio->GetXaxis()->SetLabelSize(0.08); // Increase label font size
    hRatio->GetXaxis()->SetTitleSize(0.08); // Increase title font size
    hRatio->GetYaxis()->SetLabelSize(0.08); // Increase label font size
    hRatio->GetYaxis()->SetTitleSize(0.08); // Increase title font size


    if(necessaryToMask)
    {

        // Get x and y range for the box, covering the full histogram range
        double x_min = maskValues[histName];
        double x_max = h_data_combined->GetXaxis()->GetXmax();
        double y_min = 0.0;  // Starting from zero on the y-axis, adjust if needed
        double y_max = h_data_combined->GetMaximum() * 1.05; // Extend slightly above max for visibility

        // Create the box to mask the data
        TBox* maskedBox = new TBox(x_min, y_min, x_max, y_max);
        maskedBox->SetFillColor(kGray + 2);  // Gray color for mask
        maskedBox->SetFillStyle(3004);       // Semi-transparent fill with crosshatch pattern

        // Draw the histogram first
        pad1->cd();

        // Draw the mask box on top of the histogram
        maskedBox->Draw("same");

        // Calculate the center position for the text
        double x_center = (x_min + x_max) / 2.0;
        double y_center = (y_min + y_max) / 2.0;

        // Create and draw the text in the middle of the box
        TLatex* maskedText = new TLatex(x_center, y_center, "data masked");
        maskedText->SetTextAlign(22);  // Center alignment
        maskedText->SetTextSize(0.05); // Adjust text size as needed
        maskedText->SetTextColor(kBlack); // Text color
        maskedText->Draw("SAME");

    }


    if(!runControlRegions)  c->SaveAs( (output_path+ "dataMC/" + histName + "_dataMC_" + year +".png").c_str()  );
    else {    c->SaveAs( (output_path+ "dataMC/" + histName + "_dataMC_" + region + "_" + year +".png").c_str()  ) ; }


    int nFiles = 6;
    if (runSideband) nFiles = 4;
    std::cout << "Finished with " << year << "/" << region << "/" << histName  << std::endl;  ;
    for (int i = 0; i < nFiles; ++i) 
    {
        delete bgFiles[i];
    }
    delete hs; delete pad1; delete pad2;
    delete c;
}



void data_MC_comparer()
{   


    bool runControlRegions = true;  // flag to run the normal processed root files as opposed to the selectionStudy ones
    bool runSideband  = false;       // flag to run over the sideband region (if these files are processed)

    bool doMasking = true; // mask sensitive regions of SR/CR

    ///// SELECTION STUDY PORTION (creates data/MC plots for loose region, NOT SR/CR/AT/SB regions)
    std::vector<std::string> hist_names = {"h_totHT", "h_nfatjets","h_nfatjets_pre", "h_AK8_pt", "h_nAK4", "h_AK4_pt", "h_AK8_mass", "h_AK4_mass",  
    "h_nHeavyAK8_pt400_M10", "h_nHeavyAK8_pt400_M20", "h_nHeavyAK8_pt400_M30", "h_nHeavyAK8_pt300_M10", "h_nHeavyAK8_pt300_M20", "h_nHeavyAK8_pt300_M30",
     "h_nHeavyAK8_pt200_M10", "h_nHeavyAK8_pt200_M20", "h_nHeavyAK8_pt200_M30",
    "h_nAK8_pt200", "h_nAK8_pt300", "h_nAK8_pt150", "h_nAK8_pt500", "h_AK4_eta", "h_AK4_phi", "h_AK8_eta", "h_AK8_phi"};

    std::vector<std::string> years = {"2015","2016","2017","2018"};
    /*for(auto year = years.begin(); year != years.end(); year++)
    {
        for(auto hist_name = hist_names.begin();hist_name!=hist_names.end();hist_name++)
        {

            std::cout << "Running selection study for " << *year << "/" << *hist_name << std::endl;
            make_plot(*year, *hist_name, false, false,"", doMasking);
        }
    }

*/
    ///// CONTROL REGION STUDY PORTION (creates data/MC plot comparing data/MC for SB1b, SB0b, and AT0b regions)
    hist_names = {"h_totHT", "h_nfatjets","h_nfatjets_pre", "h_nAK4_all", "h_AK8_jet_mass", "h_AK8_jet_pt", "h_nCA4_300_1b", "h_nCA4_300_0b" };

    if(runControlRegions)
    {



        std::vector<std::string> regions;
        hist_names = { "h_disuperjet_mass",  "h_SJ_mass"};  // removed theese "h_nAK4_all", "h_nfatjets","h_totHT","h_nfatjets_pre", "h_dijet_mass", "h_AK8_jet_mass", "h_AK8_jet_pt", "h_nCA4_300_1b", "h_nCA4_300_0b" 

        if(runSideband) 
        {
            regions    = {"SB1b", "SB0b"};
        

            for(auto year = years.begin(); year != years.end(); year++)
            {   
                for(auto region=regions.begin(); region!= regions.end();region++)
                {
                    for(auto hist_name = hist_names.begin();hist_name!=hist_names.end();hist_name++)
                    {
                        std::cout << "Running control region for " << *year << "/" << *region << "/" << *hist_name << std::endl;
                        make_plot(*year, *hist_name, runControlRegions, runSideband, *region, doMasking);
                    }
                }
            }
        }
        // run over AT regions
        runSideband = false;
        regions    = {"SR","CR","AT1b","AT0b"};        

        for(auto year = years.begin(); year != years.end(); year++)
        {   
            for(auto region=regions.begin(); region!= regions.end();region++)
            {
                for(auto hist_name = hist_names.begin();hist_name!=hist_names.end();hist_name++)
                {
                    std::cout << "Running control region for " << *year << "/" << *region << "/" << *hist_name << std::endl;
                    make_plot(*year, *hist_name, runControlRegions, runSideband, *region, doMasking);
                }
            }
        }

    }




}







