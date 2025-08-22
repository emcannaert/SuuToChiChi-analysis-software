#include <TPrincipal.h>
#include <TTree.h>
#include <TFile.h>
#include <TMatrixD.h>


void create_corr_matrix()
{

    TFile *file = TFile::Open("your_file.root");
    TTree *tree = (TTree*)file->Get("your_tree");

    TPrincipal *principal = new TPrincipal(4, "ND"); // 4 = number of variables

    Float_t x, y, z, w;
    tree->SetBranchAddress("x", &x);
    tree->SetBranchAddress("y", &y);
    tree->SetBranchAddress("z", &z);
    tree->SetBranchAddress("w", &w);

    Long64_t nentries = tree->GetEntries();
    for (Long64_t i = 0; i < nentries; ++i) {
        tree->GetEntry(i);
        Double_t vars[4] = {x, y, z, w};
        principal->AddRow(vars);
    }

    principal->MakePrincipals(); // Computes covariance and correlation matrices

    // Now get the correlation matrix:
    TMatrixD *corr = const_cast<TMatrixD*>(principal->GetCorrelationMatrix());

    corr->Print();   
}




