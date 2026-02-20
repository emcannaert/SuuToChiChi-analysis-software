#include <TFile.h>
#include <TTree.h>
#include <TGraph.h>
#include <TF1.h>
#include <TCanvas.h>
#include <iostream>


// creates a JEC value (for fixed eta range) as a fuction of jet_pt and fits it to a function
// this then allows one to see how much / little the JEC value varies when jet_pt is shifted by some amount 
// usage: root -l -q 'plotJetJECvsEta.C("path/to/myFile.root")'


#include <TFile.h>
#include <TTree.h>
#include <TGraph.h>
#include <TF1.h>
#include <TCanvas.h>
#include <TSystem.h>
#include <iostream>
#include <string>

// Helper: strip path + .root
std::string baseName(const std::string& path)
{
    std::string file = gSystem->BaseName(path.c_str());
    size_t pos = file.rfind(".root");
    if (pos != std::string::npos)
        file.erase(pos);
    return file;
}

void plotJetJECvsEta(const char* inputFile)
{
    std::string tag = baseName(inputFile);

    // Open file
    TFile* file = TFile::Open(inputFile);
    if (!file || file->IsZombie()) {
        std::cerr << "Error opening file: " << inputFile << std::endl;
        return;
    }

    // Get tree
    TTree* tree = (TTree*)file->Get("clusteringAnalyzerAll_nom/tree_nom");
    if (!tree) {
        std::cerr << "Tree not found\n";
        return;
    }

    // Branch variables
    const int MAXJETS = 200;
    Int_t   nfatjets;
    Double_t jet_eta[MAXJETS];
    Double_t jet_jec_full[MAXJETS];
    Double_t jet_pt[MAXJETS];

    tree->SetBranchAddress("nfatjets", &nfatjets);
    tree->SetBranchAddress("jet_eta", jet_eta);
    tree->SetBranchAddress("jet_pt", jet_pt);
    tree->SetBranchAddress("jet_jec_full", jet_jec_full);

    // Graph
    TGraph* gr = new TGraph();
    gr->SetName(Form("gr_jec_vs_eta_%s", tag.c_str()));
    gr->SetTitle(Form("AK8 JEC Scale Factor vs AK8 p_{T} (%s);jet p_{T} [GeV];JEC Factor", tag.c_str()));

    Long64_t nEntries = tree->GetEntries();
    int point = 0;

    for (Long64_t i = 0; i < nEntries; ++i) 
    {
        tree->GetEntry(i);

        for (int j = 0; j < nfatjets; ++j) 
        {

            if( jet_eta[j] < 0.25 && jet_eta[j] > -0.25)
            {
                gr->SetPoint(point, jet_pt[j], jet_jec_full[j]);
                //std::cout << "Setting point " << jet_pt[j] << ", " << jet_jec_full[j] << std::endl;
                ++point;
            }

        }
    }

    std::cout << "Filled graph with " << point << " points\n";

    // Fit
    TF1* fit = new TF1(
        Form("fit_%s", tag.c_str()),
        "pol2",
        0, 6000.0
    );
    gr->Fit(fit, "Q");

    // Draw
    TCanvas* c = new TCanvas(
        Form("c_%s", tag.c_str()),
        "JEC vs eta",
        1600, 1200
    );

    gr->Draw("AP");
    fit->Draw("same");

    c->SetLeftMargin(0.1);

    // Save output
    c->SaveAs(Form("%s_JEC_vs_pt.png", tag.c_str()));
    // c->SaveAs(Form("%s_JEC_vs_eta.pdf", tag.c_str()));


    TF1* ratio = new TF1(
    "ratio",
    [fit](double* x, double*) {
        double v = x[0];
        return fit->Eval(1.10 * v) / fit->Eval(v);
    },
    fit->GetXmin(),
    fit->GetXmax(),
    0 );


    TCanvas* c2 = new TCanvas("c_ratio", "JEC ratio", 1600, 1200);
    c2->SetLeftMargin(0.1);

    ratio->SetTitle("JEC response to +10% shift;AK8 Jet p_{T};f(1.10x)/f(x)");
    ratio->Draw();

    c2->SaveAs(Form("%s_JEC_diff.png", tag.c_str()));


}