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
    Int_t   smallestNJets;
    Double_t jet_eta[MAXJETS];
    Double_t jet_jec_full[MAXJETS];
    Double_t jet_pt[MAXJETS];
    Double_t jet_pt_perc_diff[MAXJETS];

    tree->SetBranchAddress("nAK8", &nfatjets);
    tree->SetBranchAddress("jet_eta", jet_eta);
    tree->SetBranchAddress("jet_pt", jet_pt);
    tree->SetBranchAddress("jet_jec_full", jet_jec_full);

    tree->SetBranchAddress("smallestNJets", &smallestNJets);
    tree->SetBranchAddress("jet_pt_perc_diff", jet_pt_perc_diff);

    // Graph
    TGraph* gr_eta0p5 = new TGraph();
    gr_eta0p5->SetName(Form("gr_eta0p5_jec_vs_eta_%s", tag.c_str()));
    gr_eta0p5->SetTitle(Form("AK8 JEC Scale Factor vs AK8 p_{T} (%s) (|#eta| < 0.5);jet p_{T} [GeV];JEC Factor", tag.c_str()));

    TGraph* gr_eta0p5to1p5 = new TGraph();
    gr_eta0p5to1p5->SetName(Form("gr_eta0p5to1p5_jec_vs_eta_%s", tag.c_str()));
    gr_eta0p5to1p5->SetTitle(Form("AK8 JEC Scale Factor vs AK8 p_{T} (%s) (0.5 < #eta < 1.5 or -0.5 > #eta > -1.5);jet p_{T} [GeV];JEC Factor", tag.c_str()));

    TGraph* gr_eta1p5to2p5 = new TGraph();
    gr_eta1p5to2p5->SetName(Form("gr_eta1p5to2p5_jec_vs_eta_%s", tag.c_str()));
    gr_eta1p5to2p5->SetTitle(Form("AK8 JEC Scale Factor vs AK8 p_{T} (%s) (1.5 < #eta < 2.5 or -1.5 > #eta > -2.5);jet p_{T} [GeV];JEC Factor", tag.c_str()));

    TH1F* h_jet_pt_perc_diff  = new TH1F("h_jet_pt_perc_diff","Percent p_{T} Difference Between Corresponding Lab-Frame AK8 and COM-frame CA8 Jets; p_{T, AK8, lab} - p_{T, CA8, COM}) / p_{T, AK8, lab} ; Jets",75,-1.1,1.1);

    gr_eta0p5->SetMarkerStyle(20);
    gr_eta0p5to1p5->SetMarkerStyle(20);
    gr_eta1p5to2p5->SetMarkerStyle(20);

    gr_eta0p5->SetMarkerSize(0.5);
    gr_eta0p5to1p5->SetMarkerSize(0.5);
    gr_eta1p5to2p5->SetMarkerSize(0.5);

    Long64_t nEntries = tree->GetEntries();
    int point_eta0p5 = 0,point_eta0p5to1p5 = 0, point_eta1p5to2p5 = 0;

    for (Long64_t i = 0; i < nEntries; ++i) 
    {
        tree->GetEntry(i);

        for (int j = 0; j < nfatjets; ++j) 
        {

            if( jet_eta[j] < 0.5 && jet_eta[j] > -0.5)
            {
                gr_eta0p5->SetPoint(point_eta0p5, jet_pt[j], jet_jec_full[j]);
                //std::cout << "Setting point_eta0p5 " << jet_pt[j] << ", " << jet_jec_full[j] << std::endl;
                ++point_eta0p5;
            }
            else if( (jet_eta[j] < 1.5 && jet_eta[j] > 0.5) || (jet_eta[j] > -1.5 && jet_eta[j] < -0.5)) 
            {
                gr_eta0p5to1p5->SetPoint(point_eta0p5to1p5, jet_pt[j], jet_jec_full[j]);
                //std::cout << "Setting point_eta0p5 " << jet_pt[j] << ", " << jet_jec_full[j] << std::endl;
                ++point_eta0p5to1p5;
            }
            else if( (jet_eta[j] < 2.5 && jet_eta[j] > 1.5) || (jet_eta[j] > -2.5 && jet_eta[j] < -1.5)) 
            {
                gr_eta1p5to2p5->SetPoint(point_eta1p5to2p5, jet_pt[j], jet_jec_full[j]);
                //std::cout << "Setting point_eta0p5 " << jet_pt[j] << ", " << jet_jec_full[j] << std::endl;
                ++point_eta1p5to2p5;
            }
        }
        for (int j = 0; j < smallestNJets; ++j) 
        {
            h_jet_pt_perc_diff->Fill(jet_pt_perc_diff[j]);
        }
                    


    }

    std::cout << "Filled graph with " << point_eta0p5 << " point_eta0p5s\n";

    // Fit |eta| < 0.5
    TF1* fit = new TF1(
        Form("fit_%s", tag.c_str()),
        "pol2",
        0, 6000.0
    );
    gr_eta0p5->Fit(fit, "Q");

    // Draw
    TCanvas* c = new TCanvas(
        Form("c_%s", tag.c_str()),
        "JEC vs eta",
        1600, 1200
    );

    gr_eta0p5->Draw("AP");
    fit->Draw("same");

    c->SetLeftMargin(0.1);

    // Save output
    c->SaveAs(Form("%s_JEC_vs_pt_eta0p5.png", tag.c_str()));
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

    ratio->SetTitle("JEC response to +10% shift (|#eta| < 0.5);AK8 Jet p_{T};f(1.10x)/f(x)");
    ratio->Draw();

    c2->SaveAs(Form("%s_JEC_diff_eta0p5.png", tag.c_str()));




    // Fit 0.5 < eta < 1.5, -0.5 > eta > -1.5
    fit = new TF1(
        Form("fit_%s", tag.c_str()),
        "pol2",
        300, 1600.0
    );
    gr_eta0p5to1p5->Fit(fit, "Q");

    c = new TCanvas(
        Form("c_%s", tag.c_str()),
        "JEC vs eta",
        1600, 1200
    );

    gr_eta0p5to1p5->Draw("AP");
    fit->Draw("same");

    c->SetLeftMargin(0.1);

    // Save output
    c->SaveAs(Form("%s_JEC_vs_pt_eta0p5to1p5.png", tag.c_str()));

    ratio = new TF1(
    "ratio",
    [fit](double* x, double*) {
        double v = x[0];
        return fit->Eval(1.10 * v) / fit->Eval(v);
    },
    fit->GetXmin(),
    fit->GetXmax(),
    0 );


    c2 = new TCanvas("c_ratio", "JEC ratio", 1600, 1200);
    c2->SetLeftMargin(0.1);

    ratio->SetTitle("JEC response to +10% shift (0.5 < #eta < 1.5 or -0.5 > #eta > -1.5);AK8 Jet p_{T};f(1.10x)/f(x)");
    ratio->Draw();

    c2->SaveAs(Form("%s_JEC_diff_eta0p5to1p5.png", tag.c_str()));



    // Fit 1.5 < eta < 2.5, -1.5 > eta > -2.5
    fit = new TF1(
        Form("fit_%s", tag.c_str()),
        "pol2",
        400, 1400.0
    );
    gr_eta1p5to2p5->Fit(fit, "Q");

    c = new TCanvas(
        Form("c_%s", tag.c_str()),
        "JEC vs eta",
        1600, 1200
    );

    gr_eta1p5to2p5->Draw("AP");
    fit->Draw("same");

    c->SetLeftMargin(0.1);

    // Save output
    c->SaveAs(Form("%s_JEC_vs_pt_eta1p5to2p5.png", tag.c_str()));

    ratio = new TF1(
    "ratio",
    [fit](double* x, double*) {
        double v = x[0];
        return fit->Eval(1.10 * v) / fit->Eval(v);
    },
    fit->GetXmin(),
    fit->GetXmax(),
    0 );


    c2 = new TCanvas("c_ratio", "JEC ratio", 1600, 1200);
    c2->SetLeftMargin(0.1);

    ratio->SetTitle("JEC response to +10% shift (1.5 < #eta < 2.5 or -1.5 > #eta > -2.5);AK8 Jet p_{T};f(1.10x)/f(x)");
    ratio->Draw();

    c2->SaveAs(Form("%s_JEC_diff_eta1p5to2p5.png", tag.c_str()));



    h_jet_pt_perc_diff->Draw("HIST");
    c2->SaveAs(Form("%s_pt_diff.png", tag.c_str()));







}