#!/usr/bin/env python
import ROOT
import os

ROOT.gROOT.SetBatch(True)

# Define sample types and years
sample_types = ["QCDMC", "TTbarMC", "WJetsMC", "STMC", "SuuToChiChi"]
years = ["2015", "2016", "2017", "2018"]

# Histograms to extract
hist_names = ["h_effLightJets_med", "h_effbJets_med", "h_effcJets_med"]

hist_name_translator = {"h_effLightJets_med":"Rate at which True Light Jets are Tagged as b (Med WP)","h_effbJets_med":"Rate at which True b Jets are Tagged as b (Med WP)","h_effcJets_med":"Rate at which True c Jets are Tagged as b (Med WP)"}
# Output directory
outdir = "plots/bTagEfficiencyMaps/"

for sample in sample_types:
    for year in years:
        filename = "../data/btaggingEffMaps/btag_efficiency_map_%s_combined_%s.root"%(sample,year)
        if not os.path.exists(filename):
            print("File not found:", filename)
            continue

        f = ROOT.TFile.Open(filename)
        if not f or f.IsZombie():
            print("Could not open:", filename)
            continue

        for hist_name in hist_names:
            hist = f.Get(hist_name)
            if not hist:
                print(" Histogram %s not found in %s"%(hist_name,filename))
                continue

            c = ROOT.TCanvas("c", "c", 1600, 1200)


            hist.SetStats(0)
            hist.SetTitle("%s (%s, %s)"%(hist_name_translator[hist_name],sample,year))

            hist.GetXaxis().SetTitle("AK4 Jet p_{T} [GeV]")
            hist.GetYaxis().SetTitle("AK4 Jet #eta")
            #hist.GetYaxis().SetTitleOffset(0.8)
            hist.Draw("COLZ")

            outpath = os.path.join(outdir, "%s_%s_%s.png"%(hist_name,sample,year))
            c.SaveAs(outpath)
            c.Close()

        f.Close()

print("All plots created and saved in:", outdir)