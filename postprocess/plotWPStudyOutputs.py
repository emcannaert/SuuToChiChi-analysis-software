import ROOT
import os
from return_BR_SF.return_BR_SF import return_BR_SF


# Disable GUI (batch mode)
ROOT.gROOT.SetBatch(True)

# Working points to loop over
working_points = ["25","30","35","40","45", "50","55", "60", "65", "70", "80",  "90"]
years = ["2015","2016","2017","2018"]

first_page = True

base_dir = "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/WP_study"
output_pdf = os.path.join(base_dir, "combined_background_hists.pdf")


for year in years:

    qcd_samples = {
        #"QCDMC1000to1500": return_BR_SF(year,"QCD1000to1500".replace("-","_")) ,  # TODO: Replace with actual scale factor
        #"QCDMC1500to2000": return_BR_SF(year,"QCD1500to2000".replace("-","_")) ,  # TODO: Replace with actual scale factor
        "QCDMC2000toInf":  return_BR_SF(year,"QCD2000toInf".replace("-","_")) ,   # TODO: Replace with actual scale factor

        #"WJetsMC_LNu-HT1200to2500": return_BR_SF(year,"WJetsMC_LNu-HT1200to2500".replace("-","_"))  ,
        #"WJetsMC_LNu-HT2500toInf": return_BR_SF(year,"WJetsMC_LNu-HT2500toInf".replace("-","_")) ,
        #"WJetsMC_LNu-HT800to1200": return_BR_SF(year,"WJetsMC_LNu-HT800to1200".replace("-","_")) ,
        #"WJetsMC_QQ-HT800toInf":   return_BR_SF(year,"WJetsMC_QQ-HT800toInf".replace("-","_")) ,

        #"TTToHadronicMC": return_BR_SF(year,"TTToHadronicMC".replace("-","_")) ,
        #"TTToLeptonicMC": return_BR_SF(year,"TTToLeptonicMC".replace("-","_")) ,
        #"TTToSemiLeptonicMC": return_BR_SF(year,"TTToSemiLeptonicMC".replace("-","_")) ,
        
        #"TTJetsMCHT800to1200":   return_BR_SF(year,"TTJetsMCHT800to1200".replace("-","_")) ,
        #"TTJetsMCHT1200to2500": return_BR_SF(year,"TTJetsMCHT1200to2500".replace("-","_")) ,
        #"TTJetsMCHT2500toInf": return_BR_SF(year,"TTJetsMCHT2500toInf".replace("-","_")) ,


        #"ST_s-channel-hadronsMC": return_BR_SF(year,"ST_s-channel-hadronsMC".replace("-","_")) ,
        #"ST_s-channel-leptonsMC": return_BR_SF(year,"ST_s-channel-leptonsMC".replace("-","_")) ,
        #"ST_t-channel-antitop_inclMC": return_BR_SF(year,"ST_t-channel-antitop_inclMC".replace("-","_")) ,
        #"ST_t-channel-top_inclMC":return_BR_SF(year,"ST_t-channel-top_inclMC".replace("-","_"))  ,
        #"ST_tW-antiTop_inclMC": return_BR_SF(year,"ST_tW-antiTop_inclMC".replace("-","_")) ,
        #"ST_tW-top_inclMC":  return_BR_SF(year,"ST_tW-top_inclMC".replace("-","_")) 
    }


    for wp in working_points:
        wp_dir = os.path.join(base_dir, "WP0p" + wp)
        print "Processing WP:", wp

        combined_hist = None

        for sample in qcd_samples:
            scale = qcd_samples[sample]
            file_name = "%s_%s_WP0p%s_processed.root" % (sample, year, wp)
            file_path = os.path.join(wp_dir, file_name)

            if not os.path.exists(file_path):
                print "  WARNING: File not found:", file_path
                continue

            f = ROOT.TFile.Open(file_path)
            if not f or f.IsZombie():
                print "  ERROR: Could not open:", file_path
                continue

            hist = f.Get("nom/h_MSJ_mass_vs_MdSJ_NN_SR")
            if not hist:
                print "  ERROR: Histogram not found in:", file_path
                f.Close()
                continue

            hist.SetDirectory(0)
            f.Close()

            hist.Scale(scale)

            if combined_hist is None:
                combined_hist = hist.Clone("combined_hist")
            else:
                combined_hist.Add(hist)

        if combined_hist:
            # Draw and save
            c = ROOT.TCanvas("c", "c", 800, 700)
            c.SetRightMargin(0.15)
            c.SetLogz()

            combined_hist.SetTitle("Combined Background (WP %s)" % wp)
            combined_hist.GetZaxis().SetTitleOffset(1.2)
            combined_hist.SetStats(0)
            combined_hist.Draw("COLZ")

            img_path = os.path.join(wp_dir, "combined_hist_WP0p%s.png" % wp)
            root_out_path = os.path.join(wp_dir, "combined_hist_WP0p%s.root" % wp)


            # Add bold label with TLatex
            label = ROOT.TLatex()
            label.SetNDC()
            label.SetTextSize(0.045)
            label.SetTextFont(62)  # 62 = bold
            label.DrawLatex(0.18, 0.92, "Year: %s   WP: %s" % (year, wp))

            c.SaveAs(img_path)

            # Append to multi-page PDF
            if first_page:
                c.SaveAs(output_pdf + "[")  # Open PDF
                first_page = False

            c.SaveAs(output_pdf)

            out_file = ROOT.TFile(root_out_path, "RECREATE")
            combined_hist.Write()
            out_file.Close()

            print "Saved histogram for WP %s" % wp
        else:
            print "No histograms combined for WP %s" % wp

# Close multi-page PDF
if not first_page:
    c.SaveAs(output_pdf + "]")  # Close PDF
    print "All plots written to", output_pdf
else:
    print "No plots were created, PDF not generated."