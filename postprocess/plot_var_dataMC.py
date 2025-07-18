import ROOT
import os
from return_BR_SF.return_BR_SF import return_BR_SF
from return_signal_SF.return_signal_SF import return_signal_SF
from write_cms_text import write_cms_text
import numpy as np
import argparse
import datetime
ROOT.gROOT.SetBatch(True)


def make_plots(file_dir, hist_names,output_dir):

    years = ["2015", "2016", "2017", "2018"]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    color_hexes = [
        "#D73027",  # Deep Red
        "#FC8D59",  # Bright Orange
        "#FEE08B",  # Golden Yellow
        "#D9EF8B",  # Light Olive
        "#91CF60",  # Teal Green
        "#1A9850",  # Emerald Green
        "#66BD63",  # Sky Blue
        "#A6D96A",  # Light Cyan
        "#3288BD",  # Ocean Blue
        "#9E0142",  # Soft Purple
        "#C51B7D",  # Mauve Pink
        "#762A83",  # Deep Violet
        "#666666",  # Slate Gray
        "#F46D43",  # Coral Pink
        "#5E4FA2",  # Cool Blue
        "#006837",  # Forest Green
    ]

    colors = [ROOT.TColor.GetColor(hex_code) for hex_code in color_hexes]

    BR_samples = ["ST_s-channel-hadronsMC",
    "ST_s-channel-leptonsMC",
    "ST_t-channel-antitop_inclMC",
    "ST_t-channel-top_inclMC",
    "ST_tW-antiTop_inclMC",
    "ST_tW-top_inclMC",
    "WJetsMC_LNu-HT1200to2500",
    "WJetsMC_LNu-HT2500toInf",
     "WJetsMC_LNu-HT800to1200",
    "WJetsMC_QQ-HT800toInf",
     "TTToLeptonicMC",
    "TTToSemiLeptonicMC",
    "TTToHadronicMC",
    "QCDMC1000to1500",
     "QCDMC1500to2000",
    "QCDMC2000toInf"] 

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

    output_pdf = os.path.join(output_dir, "var_dataMC_"+timestamp+ ".pdf")
    first_page = True

    for hist_name in hist_names: 

        region = "preselected"

        cand_regions = ["AT1b","AT0b","CR","SR","ADT1b","ADT0b"]

        ## try to interpret the region from the hist name
        for cand_region in cand_regions:
            if cand_region in hist_name: 
                region = cand_region
                break

        print("For hist %s, interpreted region as %s."%(hist_name,region))


        for year in years:

            year_str = year
            if year == "2015": year_str = "2016preAPV"
            if year == "2016": year_str = "2016postAPV"

            BR_hists            = []

            hs = ROOT.THStack("h_BR", "(%s) (%s);"%(region,year_str))

            qcd_samples = {

                "ST_s-channel-hadronsMC": return_BR_SF(year, "ST_s-channel-hadronsMC".replace("-","_")),
                "ST_s-channel-leptonsMC": return_BR_SF(year, "ST_s-channel-leptonsMC".replace("-","_")),
                "ST_t-channel-antitop_inclMC": return_BR_SF(year, "ST_t-channel-antitop_inclMC".replace("-","_")),
                "ST_t-channel-top_inclMC": return_BR_SF(year, "ST_t-channel-top_inclMC".replace("-","_")),
                "ST_tW-antiTop_inclMC": return_BR_SF(year, "ST_tW-antiTop_inclMC".replace("-","_")),
                "ST_tW-top_inclMC": return_BR_SF(year, "ST_tW-top_inclMC".replace("-","_")),

                "WJetsMC_LNu-HT1200to2500": return_BR_SF(year, "WJetsMC_LNu-HT1200to2500".replace("-","_")),
                "WJetsMC_LNu-HT2500toInf": return_BR_SF(year, "WJetsMC_LNu-HT2500toInf".replace("-","_")),
                "WJetsMC_LNu-HT800to1200": return_BR_SF(year, "WJetsMC_LNu-HT800to1200".replace("-","_")),
                "WJetsMC_QQ-HT800toInf": return_BR_SF(year, "WJetsMC_QQ-HT800toInf".replace("-","_")) ,

                "TTToLeptonicMC": return_BR_SF(year, "TTToLeptonicMC"),
                "TTToSemiLeptonicMC": return_BR_SF(year, "TTToSemiLeptonicMC"),
                "TTToHadronicMC": return_BR_SF(year, "TTToHadronicMC"),

                "QCDMC1000to1500": return_BR_SF(year, "QCD1000to1500"),
                "QCDMC1500to2000": return_BR_SF(year, "QCD1500to2000"),
                "QCDMC2000toInf": return_BR_SF(year, "QCD2000toInf"),

            }

            data_samples = {"2015": ["dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM" ,"dataF-HIPM"], 
            "2016": ["dataF","dataG","dataH"], 
            "2017": ["dataB","dataC","dataD","dataE","dataF"], 
            "2018": ["dataA","dataB", "dataC", "dataD"] }


            ### combined BRs
            combined_hist_BR = None
            for iii,sample in enumerate(BR_samples):
                scale = qcd_samples[sample]

                file_name = sample + "_" + year + "_processed.root"
                file_path = os.path.join(file_dir, file_name)

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

                if iii == 0: 
                    hs.SetTitle("%s %s"%(hist.GetTitle(), hs.GetTitle()))
                #hs.SetXaxis().SetTitle(hist.GetXaxis().GetTitle())
                #hs.SetYaxis().SetTitle(hist.GetYaxis().GetTitle()) # this might not work

                hist.SetDirectory(0)
                hist.Scale(scale)
                hist.SetMinimum(1e-2)
                hist.SetFillColor(colors[iii])
                hist.SetLineColor(colors[iii])

                hist.SetStats(0)
                BR_hists.append(hist)
                hs.Add(hist)


                if combined_hist_BR is None:
                    combined_hist_BR = hist.Clone("combined_hist_BR")
                    combined_hist_BR.SetDirectory(0)
                else:
                    combined_hist_BR.Add(hist)

                hist.SetDirectory(0)
                f.Close()

            combined_data = None
            ## get combined data hist
            for iii,sample in enumerate(data_samples[year]):

                file_name = sample + "_" + year + "_processed.root"
                file_path = os.path.join(file_dir, file_name)

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
                hist.SetMinimum(1e-2)
                hist.SetStats(0)

                f.Close()

                if combined_data is None:
                    combined_data = hist.Clone("combined_data")
                else:
                    combined_data.Add(hist)


            c = ROOT.TCanvas("c", "c", 1200, 1200)
            if combined_hist_BR and combined_data:

                c.SetRightMargin(0.15)
                
                # Create a canvas and pads for upper and lower plots
                pad1 = ROOT.TPad("pad1", "Top pad", 0, 0.30, 1, 1.0)
                pad2 = ROOT.TPad("pad2", "Bottom pad", 0, 0.0, 1, 0.290)
                
                # Adjust margins
                pad1.SetTopMargin(0.1)  
                pad1.SetBottomMargin(0.01)  # Space between the top and bottom pad
                pad2.SetTopMargin(0.00)
                pad2.SetBottomMargin(0.4)  # Increase for better spacing in bottom pad

                pad1.Draw()
                pad2.Draw()

                # Draw the stack and h2 on the upper pad
                pad1.cd()
                pad1.SetLogy()

                # Determine which histogram has a larger maximum
                max_value = max( combined_data.GetMaximum(), combined_hist_BR.GetMaximum()   )

                hs.Draw("HIST")
                hs.SetMaximum(100*max_value)
                hs.SetMinimum(1e-2)

                combined_data.SetMarkerStyle(20)         # Solid circles
                combined_data.SetMarkerColor(ROOT.kBlack)
                combined_data.SetLineColor(ROOT.kBlack)  # Error bar color
                combined_data.SetLineWidth(1)
                combined_data.Draw("PE1,SAME")

                c.Update()

                # Draw the ratio on the lower pad
                pad2.cd()
                x_min = 0
                x_max = 0

                hRatio = combined_data.Clone("hRatio%s"%iii)
                hRatio.SetMinimum(0.05)
                hRatio.SetMaximum(2.0)
                hRatio.SetTitle("")
                hRatio.Divide( combined_hist_BR)  # Compute the ratio h2 / hStackTotal
                hRatio.GetYaxis().SetTitle(r"data / MC")
                hRatio.GetYaxis().SetTitleSize(0.1)
                hRatio.GetYaxis().SetTitleOffset(0.4)
                hRatio.GetYaxis().SetLabelSize(0.08)
                hRatio.GetXaxis().SetTitleSize(0.12)
                hRatio.GetXaxis().SetLabelSize(0.1)

                hRatio.Draw()


                x_min = hRatio.GetXaxis().GetXmin()
                x_max = hRatio.GetXaxis().GetXmax()

                ### create ratio lines at 0.8, 1.0, 1.2
                nom_line = ROOT.TLine(x_min, 1.0, x_max, 1.0)
                nom_line.SetLineStyle(1)  
                nom_line.Draw("same")

                nom_line_up = ROOT.TLine(x_min, 1.2, x_max, 1.2)
                nom_line_up.SetLineStyle(2)  # Dotted line style
                nom_line_up.Draw("same")


                nom_line_down = ROOT.TLine(x_min, 0.8, x_max, 0.8)
                nom_line_down.SetLineStyle(2)  # Dotted line style
                nom_line_down.Draw("same")


                # Add legend and TLatex text
                pad1.cd()

                legend = ROOT.TLegend(0.155, 0.70, 0.80, 0.88)
                legend.SetNColumns(4);  
                legend.SetTextSize(0.01) 

                legend.SetBorderSize(0)
                legend.SetFillStyle(0) 

                legend.AddEntry(BR_hists[0], "ST-s-channel-hadrons", "f")
                legend.AddEntry(BR_hists[1], "ST_s-channel-leptons", "f")
                legend.AddEntry(BR_hists[2], "ST_t-channel-antitop", "f")
                legend.AddEntry(BR_hists[3], "ST_t-channel-top", "f")
                legend.AddEntry(BR_hists[4], "ST_tW-antiTop", "f")
                legend.AddEntry(BR_hists[5], "ST_tW-top_incl", "f")
                legend.AddEntry(BR_hists[6], "WJets-LNu-1200to2500", "f")
                legend.AddEntry(BR_hists[7], "WJets-LNu-2500toInf", "f")
                legend.AddEntry(BR_hists[8], "WJets-LNu-800to1200", "f")
                legend.AddEntry(BR_hists[9], "WJets-QQ-800toInf", "f")
                legend.AddEntry(BR_hists[10], "TTToLeptonic", "f")
                legend.AddEntry(BR_hists[11], "TTToSemiLeptonic", "f")
                legend.AddEntry(BR_hists[12], "TTToHadronic", "f")
                legend.AddEntry(BR_hists[13], "QCD1000to1500", "f")
                legend.AddEntry(BR_hists[14], "QCD1500to2000", "f")
                legend.AddEntry(BR_hists[15], "QCD2000toInf", "f")


                legend.AddEntry(combined_data, "Data", "p")
                legend.Draw()

                write_cms_text.write_cms_text(CMS_label_xpos=0.138, SIM_label_xpos=0.305,CMS_label_ypos = 0.925, SIM_label_ypos = 0.925, lumistuff_xpos=0.90, lumistuff_ypos=0.91, year = "", uses_data=True)
                png_path = os.path.join(output_dir, "dataMC_" + hist_name + "_" + year + "_"+ region + ".png")
                #root_out_path = os.path.join(output_dir, "dataMC_" + hist_name + "_" + year + ".root")

                c.SaveAs(png_path)

                if first_page:
                    c.SaveAs(output_pdf + "[")
                    first_page = False

                c.SaveAs(output_pdf)

                #out_file = ROOT.TFile(root_out_path, "RECREATE")
                #combined_hist_BR.Write()
                #out_file.Close()

                print "Saved", hist_name,
            else:
                print "No histograms combined for", hist_name

            del c 

    c2 = ROOT.TCanvas("", "", 1200, 1200)
    if not first_page:
        c2.SaveAs(output_pdf + "]")
        print "All plots written to", output_pdf
    else:
        print "No plots created for", hist_name, ". PDF not generated."
    del c2  



if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Parse input ROOT file and histogram names.")
    parser.add_argument("--file_dir", required=True, help="Path to where input ROOT files are stored")
    parser.add_argument("--hist_names", required=True, help="Comma-separated list of histogram names")
    parser.add_argument("--output_dir", required=True, help="Path to desired output directory")
    
    args = parser.parse_args()
    hist_names = [name.strip() for name in args.hist_names.split(',')]

    make_plots(args.file_dir, hist_names,args.output_dir)


