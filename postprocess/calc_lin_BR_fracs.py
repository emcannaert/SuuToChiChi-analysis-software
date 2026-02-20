#!/usr/bin/env python2
import ROOT
import os

def makeBRFracs(useOptWP):
    regions   = ["SR", "CR", "AT1b", "AT0b"]
    QCD_types = ["QCDHT", "QCDPT"]
    years     = ["2015", "2016", "2017", "2018"]
    BR_types  = ["QCD", "TTbar", "WJets", "ST"]


    dir_str = ""

    if useOptWP: 
        dir_str = "OptWP"
        QCD_types = ["QCDPT"]


    for qcd in QCD_types:
	if not os.path.exists("finalCombineFilesNewStats%s/BR_fracs/%s"%(dir_str,qcd)):
        	os.makedirs("finalCombineFilesNewStats%s/BR_fracs/%s"%(dir_str,qcd))
	outname = "finalCombineFilesNewStats%s/BR_fracs/%s/BR_fracs.root"%(dir_str,qcd)
	fout = ROOT.TFile(outname, "RECREATE")
        for year in years:
            infile_name = "finalCombineFilesNewStats{}/{}/correctedFinalCombineFiles/combine_{}_Suu4_chi1.root".format(dir_str,qcd, year)
            fin = ROOT.TFile.Open(infile_name, "READ")
            if not fin or fin.IsZombie():
                print("Could not open {}".format(infile_name))
                continue

            print("Opened {}".format(infile_name))

            for region in regions:
                hists = []
                for br in BR_types:
                    histname = "{}/{}".format(region, br)
                    h = fin.Get(histname)
                    if not h:
                        print("Missing histogram: {} in {}".format(histname, infile_name))
                        continue
                    clone = h.Clone()
                    clone.SetDirectory(0) # detach from input file
                    hists.append((br, clone))

                if len(hists) == 0:
                    continue

                # build total histogram
                h_total = hists[0][1].Clone("h_total")
                h_total.Reset()
                for _, h in hists:
                    h_total.Add(h)

                # make output dir
                outdir_name = "{}/{}/{}".format(qcd, year, region)
                fout.cd()
                if not fout.GetDirectory(outdir_name):
                    fout.mkdir(outdir_name)
                fout.cd(outdir_name)

                # fractions
                for br, h in hists:
                    h_frac = h.Clone(br + "_frac")
                    h_frac.Divide(h_total)
                    h_frac.Write()

                h_total.Delete()
                for _, h in hists:
                    h.Delete()

            fin.Close()

    fout.Close()
    print("Output written to {}".format(outname))

if __name__ == "__main__":

    useOptWP = True

    makeBRFracs(useOptWP)
