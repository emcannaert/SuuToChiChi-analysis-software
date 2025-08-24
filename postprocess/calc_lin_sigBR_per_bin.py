#!/usr/bin/env python2
import ROOT
import os, math

def makeSensitivities():
    regions     = ["SR", "CR", "AT1b", "AT0b"]
    QCD_types   = ["QCDHT", "QCDPT"]
    years       = ["2015", "2016", "2017", "2018"]
    mass_points = [
        "Suu4_chi1","Suu4_chi1p5","Suu5_chi1","Suu5_chi1p5","Suu5_chi2",
        "Suu6_chi1","Suu6_chi1p5","Suu6_chi2","Suu6_chi2p5",
        "Suu7_chi1","Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3",
        "Suu8_chi1","Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"
    ]

    for qcd in QCD_types:
        # Output location
        out_folder = "finalCombineFilesNewStats/sigBR_by_bin/{}".format(qcd)
        outname = out_folder + "/sigBR_by_bin_%s.root"%qcd
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        fout = ROOT.TFile(outname, "RECREATE")

        for year in years:
            for mass_point in mass_points:
                infile_name = "finalCombineFilesNewStats/{}/correctedFinalCombineFiles/combine_{}_{}.root".format(qcd, year, mass_point)
                fin = ROOT.TFile.Open(infile_name, "READ")
                if not fin or fin.IsZombie():
                    print("Could not open {}".format(infile_name))
                    continue

                print("Opened {}".format(infile_name))

                for region in regions:
                    h_allBR = fin.Get("{}/allBR".format(region))
                    h_sig   = fin.Get("{}/sig".format(region))
                    if not h_allBR or not h_sig:
                        print("Missing allBR or sig in {} region {}".format(infile_name, region))
                        continue

                    h_sens = h_sig.Clone(mass_point + "_sig_sensitivity")
                    h_sens.Reset()

                    for b in range(1, h_sens.GetNbinsX()+1):
                        s = h_sig.GetBinContent(b)
                        bkg = h_allBR.GetBinContent(b)
                        sens = s / math.sqrt(bkg) if bkg > 0 else 0.0
                        h_sens.SetBinContent(b, sens)

                    # Write to output under <year>/<region>
                    outdir_name = "{}/{}".format(year, region)
                    fout.cd()
                    if not fout.GetDirectory(outdir_name):
                        fout.mkdir(outdir_name)
                    fout.cd(outdir_name)
                    h_sens.Write(mass_point + "_sig_sensitivity")

                fin.Close()

        fout.Close()
        print("Signal sensitivity (per bin) output written to {}".format(outname))


if __name__ == "__main__":
    makeSensitivities()