


// utility that takes in a list of file paths and then returns a 
TH1F* combineHistograms(const std::vector<std::string>& filePaths, std::string histName,std::string year, std::string hist_limit) 
{
    TH1F* combinedHist = nullptr;

    int i = 0;
    for (const auto& filePath : filePaths) 
    {
        std::cout << "Looking for TFile " << filePath << " for year/histName: " << year<< "/" << histName <<std::endl;
        // Open the ROOT file
        TFile* file = TFile::Open(filePath.c_str());
        if (!file || file->IsZombie()) 
        {
            std::cerr << "Error opening file: " << filePath << std::endl;
            continue; 
        }
        TTree* tree_data_temp = (TTree*)file->Get("clusteringAnalyzerAll_nom/tree_nom");
        tree_data_temp->Draw(Form("%s>>h_%s_data%d(%s)", histName.c_str(), histName.c_str(), i, hist_limit.c_str()));
        TH1F* hist = (TH1F*)gDirectory->Get(Form("h_%s_data%d", histName.c_str(), i));

        if (!hist) 
        {   
            std::cout << "ERROR: histogram " << Form("h_%s_data%d", histName.c_str(), i) << " (grabbed using "<< histName <<" from the TTree) " << " from file " << filePath << " failed." << std::endl;
            file->Close();
            continue; 
        }
        else
        {
            std::cout << "Histogram " << hist->GetName() << " was found." << std::endl;
        }
        if (!combinedHist) 
        {
            combinedHist = (TH1F*)(hist->Clone("combinedHist"));
            combinedHist->SetTitle( (histName + " (Combined QCD) (" + year + ")").c_str()  );
            combinedHist->SetDirectory(nullptr);
        } 
        else 
        {   
            combinedHist->Add(hist);
        }
        i++;

        // Close the current file
        file->Close();
    }
    if (combinedHist) return combinedHist;
    else 
    {
        std::cerr << "No histograms were combined." << std::endl;
        return nullptr;
    }
}




// creates dataMC DIRECTLY from combined root files 
void make_dataMC_plot(std::string year, std::string histName, std::string hist_limit, std::vector<std::string> dataFileNames ,double QCD1000to1500_SF, double QCD1500to2000_SF, double QCD2000toInf_SF, double TTToHadronic_SF, double TTToSemiLeptonic_SF, double TTToLeptonic_SF) 
{ 


    // Open the ROOT files
    TFile* QCD1000to1500_file = TFile::Open(Form("root://cmseos.fnal.gov//store/user/ecannaer/combinedROOT/QCDMC1000to1500_%s_nom_combined.root", year.c_str()));
    TFile* QCD1500to2000_file = TFile::Open(Form("root://cmseos.fnal.gov//store/user/ecannaer/combinedROOT/QCDMC1500to2000_%s_nom_combined.root", year.c_str()));
    TFile* QCD2000toInf_file = TFile::Open(Form("root://cmseos.fnal.gov//store/user/ecannaer/combinedROOT/QCDMC2000toInf_%s_nom_combined.root", year.c_str()));
    
    TFile* TTToHadronic_file = TFile::Open(Form("root://cmseos.fnal.gov//store/user/ecannaer/combinedROOT/TTToHadronicMC_%s_nom_combined.root", year.c_str()));
    TFile* TTToSemiLeptonic_file = TFile::Open(Form("root://cmseos.fnal.gov//store/user/ecannaer/combinedROOT/TTToSemiLeptonicMC_%s_nom_combined.root", year.c_str()));
    TFile* TTToLeptonic_file = TFile::Open(Form("root://cmseos.fnal.gov//store/user/ecannaer/combinedROOT/TTToLeptonicMC_%s_nom_combined.root", year.c_str()));

    // Get the TTrees from the files
    TTree* tree_QCD1000to1500 = (TTree*)QCD1000to1500_file->Get("clusteringAnalyzerAll_nom/tree_nom");
    TTree* tree_QCD1500to2000 = (TTree*)QCD1500to2000_file->Get("clusteringAnalyzerAll_nom/tree_nom");
    TTree* tree_QCD2000toInf = (TTree*)QCD2000toInf_file->Get("clusteringAnalyzerAll_nom/tree_nom");


    // Get the TTrees from the files
    TTree* tree_TTToHadronic = (TTree*)TTToHadronic_file->Get("clusteringAnalyzerAll_nom/tree_nom");
    TTree* tree_TTToSemiLeptonic = (TTree*)TTToSemiLeptonic_file->Get("clusteringAnalyzerAll_nom/tree_nom");
    TTree* tree_TTToLeptonic = (TTree*)TTToLeptonic_file->Get("clusteringAnalyzerAll_nom/tree_nom");

    // Draw the histograms
    tree_QCD1000to1500->Draw(Form("%s>>h_%s_QCD1000to1500(%s)", histName.c_str(), histName.c_str(), hist_limit.c_str()));
    TH1F* h_QCD1000to1500 = (TH1F*)gDirectory->Get(Form("h_%s_QCD1000to1500", histName.c_str()));
    tree_QCD1500to2000->Draw(Form("%s>>h_%s_QCD1500to2000(%s)", histName.c_str(), histName.c_str(), hist_limit.c_str()));
    TH1F* h_QCD1500to2000 = (TH1F*)gDirectory->Get(Form("h_%s_QCD1500to2000", histName.c_str()));
    tree_QCD2000toInf->Draw(Form("%s>>h_%s_QCD2000toInf(%s)", histName.c_str(), histName.c_str(), hist_limit.c_str()));
    TH1F* h_QCD2000toInf = (TH1F*)gDirectory->Get(Form("h_%s_QCD2000toInf", histName.c_str()));



    tree_TTToHadronic->Draw(Form("%s>>h_%s_TTToHadronic(%s)", histName.c_str(), histName.c_str(), hist_limit.c_str()));
    TH1F* h_TTToHadronic = (TH1F*)gDirectory->Get(Form("h_%s_TTToHadronic", histName.c_str()));
    tree_TTToSemiLeptonic->Draw(Form("%s>>h_%s_TTToSemiLeptonic(%s)", histName.c_str(), histName.c_str(), hist_limit.c_str()));
    TH1F* h_TTToSemiLeptonic = (TH1F*)gDirectory->Get(Form("h_%s_TTToSemiLeptonic", histName.c_str()));
    tree_TTToLeptonic->Draw(Form("%s>>h_%s_TTToLeptonic(%s)", histName.c_str(), histName.c_str(), hist_limit.c_str()));
    TH1F* h_TTToLeptonic = (TH1F*)gDirectory->Get(Form("h_%s_TTToLeptonic", histName.c_str()));




    // Scale the histograms
    h_QCD1000to1500->Scale(QCD1000to1500_SF);
    h_QCD1500to2000->Scale(QCD1500to2000_SF);
    h_QCD2000toInf->Scale(QCD2000toInf_SF);

    // Scale the histograms
    h_TTToHadronic->Scale(TTToHadronic_SF);
    h_TTToSemiLeptonic->Scale(TTToSemiLeptonic_SF);
    h_TTToLeptonic->Scale(TTToLeptonic_SF);


    // Combine the histograms
    TH1F* h_allQCD = (TH1F*)h_QCD1000to1500->Clone();
    h_allQCD->Add(h_QCD1500to2000);
    h_allQCD->Add(h_QCD2000toInf);



    TH1F* h_allTTbar = (TH1F*)h_TTToHadronic->Clone();
    h_allTTbar->Add(h_TTToSemiLeptonic);
    h_allTTbar->Add(h_TTToLeptonic);

    h_allQCD->Add(h_allTTbar);

    TH1F* h_allData =  combineHistograms(dataFileNames,histName,year, hist_limit) ;



    TCanvas* c = new TCanvas("c", "", 1200, 1000);


    // create ratio plot

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


    pad1->cd();

    h_allData->Draw();

    h_allQCD->Draw("SAME,HIST");
    h_allData->SetMarkerStyle(20);

    // Draw ratio plot on the lower pad
    pad2->cd();
    TH1* hRatio = (TH1*)h_allData->Clone("hRatio");
    hRatio->SetTitle("");
    hRatio->GetYaxis()->SetTitle("data/MC");
    hRatio->Divide(h_allQCD);   
    hRatio->SetMinimum(0.25); // Set y-axis range for ratio plot
    hRatio->SetMaximum(3.0);
    hRatio->SetMarkerStyle(20);
    hRatio->Draw("E1");


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


    c->SaveAs(Form("plots/dataMC/initialSelection_combinedROOT/%s_dataMC_%s.png", histName.c_str(), year.c_str()));
 
}
void make_combinedROOT_comparisons()
{
    std::vector<std::string> years = {"2015", "2016", "2017", "2018"};
    std::vector<double> QCD1000to1500_SFs = {1.578683216,1.482632755,3.126481451,4.407417122};
    std::vector<double> QCD1500to2000_SFs = {0.2119142341,0.195224041, 0.3197450474,0.5425809983};
    std::vector<double> QCD2000toInf_SFs = {0.08568186031, 0.07572795371, 0.14306915, 0.2277769275};

    std::vector<double> TTToHadronic_SFs = {0.08568186031, 0.07572795371, 0.14306915, 0.2277769275};
    std::vector<double> TTToSemiLeptonic_SFs = {0.08568186031, 0.07572795371, 0.14306915, 0.2277769275};
    std::vector<double> TTToLeptonic_SFs = {0.08568186031, 0.07572795371, 0.14306915, 0.2277769275};

    std::vector<std::string> histNames = {    "totHT",           "nfatjets",      "nfatjet_pre",  "AK4_DeepJet_disc" }; // ,   "superJet_mass",  "diSuperJet_mass"  
    std::vector<std::string> hist_limits = { "30, 1200, 3500",  "8,-0.5,7.5",      "6,-0.5,5.5",   "25, 0, 1.0"    }; // ,        "30,0,3000",      "40,0,9000"  


    for (size_t  iii = 0; iii < years.size(); iii++) 
    {
        std::string year = years[iii];
        double QCD1000to1500_SF = QCD1000to1500_SFs[iii];
        double QCD1500to2000_SF = QCD1500to2000_SFs[iii];
        double QCD2000toInf_SF = QCD2000toInf_SFs[iii];
        double TTToHadronic_SF =  TTToHadronic_SFs[iii];
        double TTToSemiLeptonic_SF = TTToSemiLeptonic_SFs[iii];
        double TTToLeptonic_SF = TTToLeptonic_SFs[iii];

        std::string eosPath = "root://cmseos.fnal.gov//store/user/ecannaer/combinedROOT/";



        std::vector<std::string> dataFileNames;
        dataFileNames = {Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataB-ver2", year.c_str()),Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataC-HIPM", year.c_str()),Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataD-HIPM", year.c_str()),Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataE-HIPM", year.c_str()),Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataF-HIPM", year.c_str())};

        if(year == "2016") dataFileNames = {Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataF", year.c_str()),Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataG", year.c_str()),Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataH", year.c_str()) };
        else if(year == "2017")dataFileNames = {Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataB", year.c_str()),Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataC", year.c_str()),Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataD", year.c_str()),Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataE", year.c_str()), Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataF", year.c_str())  };  // 
        else if(year == "2018")dataFileNames = {Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataA", year.c_str()),Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataB", year.c_str()),Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataC", year.c_str()),Form("%s%s_%s_nom_combined.root", eosPath.c_str(), "dataD", year.c_str()) };
        for (size_t jjj = 0; jjj < histNames.size(); jjj++)
        {
            std::string hist_limit = hist_limits[jjj];
            std::string histName = histNames[jjj];

            make_dataMC_plot(year, histName, hist_limit,dataFileNames, QCD1000to1500_SF, QCD1500to2000_SF, QCD2000toInf_SF, TTToHadronic_SF, TTToSemiLeptonic_SF, TTToLeptonic_SF);

        }
    }


}






