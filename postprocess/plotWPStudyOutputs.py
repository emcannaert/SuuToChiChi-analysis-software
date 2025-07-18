import ROOT
import os
from return_BR_SF.return_BR_SF import return_BR_SF

ROOT.gROOT.SetBatch(True)

working_points = ["25", "30", "35", "40", "45", "50", "55", "60", "65", "70", "80"]

working_points = ["05","10","12","15","17","20","25"]


years = ["2015", "2016", "2017", "2018"]
hist_names = [
    "h_MSJ_mass_vs_MdSJ_NN_SR",
    "h_ATSJ_mass_vs_MdSJ_NN_AT1b",
    "h_BEST_score_ATSJ_AT1b",
    "h_ATSJ_mass_vs_MdSJ_NN_AT0b",
    "h_BEST_score_ATSJ_AT0b"
]

base_dir = "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/ATWP_study"

for hist_name in hist_names:

    output_pdf = os.path.join(base_dir, "combined_" + hist_name + ".pdf")
    first_page = True

    for year in years:

        qcd_samples = {
            "QCDMC1000to1500": return_BR_SF(year, "QCD1000to1500"),
            "QCDMC1500to2000": return_BR_SF(year, "QCD1500to2000"),
            "QCDMC2000toInf": return_BR_SF(year, "QCD2000toInf"),
            "WJetsMC_LNu-HT1200to2500": return_BR_SF(year, "WJetsMC_LNu-HT1200to2500".replace("-","_")),
            "WJetsMC_LNu-HT2500toInf": return_BR_SF(year, "WJetsMC_LNu-HT2500toInf".replace("-","_")),
            "WJetsMC_LNu-HT800to1200": return_BR_SF(year, "WJetsMC_LNu-HT800to1200".replace("-","_")),
            "WJetsMC_QQ-HT800toInf": return_BR_SF(year, "WJetsMC_QQ-HT800toInf".replace("-","_")),
            "TTToHadronicMC": return_BR_SF(year, "TTToHadronicMC"),
            "TTToLeptonicMC": return_BR_SF(year, "TTToLeptonicMC"),
            "TTToSemiLeptonicMC": return_BR_SF(year, "TTToSemiLeptonicMC"),
            "ST_s-channel-hadronsMC": return_BR_SF(year, "ST_s-channel-hadronsMC".replace("-","_")),
            "ST_s-channel-leptonsMC": return_BR_SF(year, "ST_s-channel-leptonsMC".replace("-","_")),
            "ST_t-channel-antitop_inclMC": return_BR_SF(year, "ST_t-channel-antitop_inclMC".replace("-","_")),
            "ST_t-channel-top_inclMC": return_BR_SF(year, "ST_t-channel-top_inclMC".replace("-","_")),
            "ST_tW-antiTop_inclMC": return_BR_SF(year, "ST_tW-antiTop_inclMC".replace("-","_")),
            "ST_tW-top_inclMC": return_BR_SF(year, "ST_tW-top_inclMC".replace("-","_"))
        }

        for wp in working_points:

            c = ROOT.TCanvas("c", "c", 1200, 1200)
            wp_dir = os.path.join(base_dir, "WP0p" + wp)
            print "Processing WP:", wp, "Hist:", hist_name

            combined_hist = None

            for sample in qcd_samples:
                scale = qcd_samples[sample]
                file_name = sample + "_" + year + "_ATWP0p" + wp + "_processed.root"
                file_path = os.path.join(wp_dir, file_name)

                if not os.path.exists(file_path):
                    print "  WARNING: File not found:", file_path
                    continue

                f = ROOT.TFile.Open(file_path)
                if not f or f.IsZombie():
                    print "  ERROR: Could not open:", file_path
                    continue

                hist = f.Get("nom/" + hist_name)
                if not hist:
                    print "  ERROR: Histogram not found:", hist_name, "in", file_path
                    f.Close()
                    continue

                hist.SetDirectory(0)
                hist.Scale(scale)
                f.Close()

                if combined_hist is None:
                    combined_hist = hist.Clone("combined_hist")
                else:
                    combined_hist.Add(hist)

            if combined_hist:
                c.SetRightMargin(0.15)
                c.SetLogz()
                combined_hist.SetTitle(hist_name + " (Year " + year + ", AT WP = 0." + wp + ")")
                combined_hist.GetZaxis().SetTitleOffset(1.2)
                combined_hist.SetStats(0)
                combined_hist.Draw("COLZ")

                label = ROOT.TLatex()
                label.SetNDC()
                label.SetTextSize(0.045)
                label.SetTextFont(62)
                label.DrawLatex(0.18, 0.92, "Year: " + year + "   AT WP: " + "0."+ wp)

                png_path = os.path.join(wp_dir, "combined_" + hist_name + "_" + year + "_ATWP0p" + wp + ".png")
                root_out_path = os.path.join(wp_dir, "combined_" + hist_name + "_" + year + "_ATWP0p" + wp + ".root")

                c.SaveAs(png_path)

                if first_page:
                    c.SaveAs(output_pdf + "[")
                    first_page = False

                c.SaveAs(output_pdf)

                out_file = ROOT.TFile(root_out_path, "RECREATE")
                combined_hist.Write()
                out_file.Close()

                print "Saved", hist_name, "for WP", wp
            else:
                print "No histograms combined for", hist_name, "WP", wp

            del c

    c2 = ROOT.TCanvas("", "", 1200, 1200)
    if not first_page:
        c2.SaveAs(output_pdf + "]")
        print "All plots written to", output_pdf
    else:
        print "No plots created for", hist_name, "PDF not generated."
    del c2