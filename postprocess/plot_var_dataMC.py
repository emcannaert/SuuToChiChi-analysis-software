import ROOT
import os
from return_BR_SF.return_BR_SF import return_BR_SF
from return_signal_SF.return_signal_SF import return_signal_SF
from write_cms_text import write_cms_text
import numpy as np
import argparse
import datetime
ROOT.gROOT.SetBatch(True)


def make_plots(file_dir, hist_names,output_dir, masks, split_BRs):


    legend_translator = {"ST_":"Single Top", "TTTo":r"t \bar{t}","WJets":"W+Jets","QCD":"QCD"}


    if not file_dir:
        file_dir    =  "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/"

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

        # Additional 10 hex colors
        "#E31A1C",  # Crimson Red
        "#FF7F00",  # Vivid Orange
        "#FDBF6F",  # Pale Orange
        "#CAB2D6",  # Lavender
        "#6A3D9A",  # Grape Purple
        "#B15928",  # Brown
        "#A6CEE3",  # Light Blue
        "#1F78B4",  # Medium Blue
        "#33A02C",  # Lime Green
        "#B2DF8A",  # Mint Green
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
    #"QCDMC1000to1500",
    #"QCDMC1500to2000",
    #"QCDMC2000toInf"

    "QCDMC_Pt_170to300",
    "QCDMC_Pt_300to470",
    "QCDMC_Pt_470to600",
    "QCDMC_Pt_600to800",
    "QCDMC_Pt_800to1000",
    "QCDMC_Pt_1000to1400",
    "QCDMC_Pt_1400to1800",
    "QCDMC_Pt_1800to2400",
    "QCDMC_Pt_2400to3200",
    "QCDMC_Pt_3200toInf"

    ] 

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

            hs = ROOT.THStack("h_BR", "(%s);"%(year_str)) # region (%s)

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


                "QCDMC_Pt_170to300":   return_BR_SF(year, "QCDMC_Pt_170to300"),
                "QCDMC_Pt_300to470":    return_BR_SF(year, "QCDMC_Pt_300to470"),
                "QCDMC_Pt_470to600":     return_BR_SF(year, "QCDMC_Pt_470to600"),
                "QCDMC_Pt_600to800":    return_BR_SF(year, "QCDMC_Pt_600to800"),
                "QCDMC_Pt_800to1000":   return_BR_SF(year, "QCDMC_Pt_800to1000"),
                "QCDMC_Pt_1000to1400":   return_BR_SF(year, "QCDMC_Pt_1000to1400"),
                "QCDMC_Pt_1400to1800":  return_BR_SF(year, "QCDMC_Pt_1400to1800"),
                "QCDMC_Pt_1800to2400":  return_BR_SF(year, "QCDMC_Pt_1800to2400"),
                "QCDMC_Pt_2400to3200":  return_BR_SF(year, "QCDMC_Pt_2400to3200"),
                "QCDMC_Pt_3200toInf":   return_BR_SF(year, "QCDMC_Pt_3200toInf")
            



            }

            data_samples = {"2015": ["dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM" ,"dataF-HIPM"], 
            "2016": ["dataF","dataG","dataH"], 
            "2017": ["dataB","dataC","dataD","dataE","dataF"], 
            "2018": ["dataA","dataB", "dataC", "dataD"] }




            ### combined BRs

            # loop over backgrounds and add each group to a list [    ]


            # problems: order of BRs or the color association are wrong
                        # order of sample names in legend must match the order of histograms
            # titles



            # ROUND 2: 
                #colors are still wrong


            if split_BRs:
                BR_types = BR_samples
            else: 
                BR_types = ["ST_", "WJets", "TTTo", "QCD" ]
            BR_groups = {BR_type: None for BR_type in BR_types}

            for iii,sample in enumerate(BR_samples):
                scale = qcd_samples[sample]

                # find out which type of BR this is
                BR_type = ""
                for _BR_type in BR_types:
                    if _BR_type in sample: 
                        BR_type = _BR_type
                        break


                file_name = sample + "_" + year + "_processed.root"
                file_path = os.path.join(file_dir, file_name)


                if not "cmseos" in file_dir:
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
                hist.SetMinimum(1e-2)
                hist.SetFillColor(colors[iii])
                hist.SetLineColor(colors[iii])
                hist.SetStats(0)

                if BR_groups[BR_type] is None:
                    BR_groups[BR_type] = hist.Clone("combined_hist_%s"%BR_type)
                    BR_groups[BR_type].SetDirectory(0)
                else:
                    BR_groups[BR_type].Add(hist)

                hist.SetDirectory(0)
                f.Close()


            found_samples = []
            # Now add these to a combined BR hist and the stack plot
            combined_hist_BR = None
            iii = 0
            
            for BR_type in BR_types:

                hist = BR_groups[BR_type]

                if not hist:
                    print "  ERROR: Histogram not found:", BR_group
                    continue

                if iii == 0: 
                    print("hist is %s, title is %s"%(hist.GetName(),hist.GetTitle()))
                    hs.SetTitle("%s %s"%(hist.GetTitle(), year))

                BR_hists.append(hist)
                found_samples.append(BR_type)

                hs.Add(hist)

                if combined_hist_BR is None:
                    combined_hist_BR = hist.Clone("combined_hist_BR")
                    combined_hist_BR.SetDirectory(0)
                else:
                    combined_hist_BR.Add(hist)
                iii+=1



            combined_data = None
            ## get combined data hist
            for iii,sample in enumerate(data_samples[year]):

                file_name = sample + "_" + year + "_processed.root"
                file_path = os.path.join(file_dir, file_name)


                if not "cmseos" in file_dir:
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



            if masks:
                if hist_name in masks:
                    # mask the histogram at the designated value
                    data_masked = combined_data.Clone(combined_data.GetName() + "_masked")
                    data_masked.SetDirectory(0)  # detach from any TFile

                    xmax = masks[hist_name]

                    for iii in range(1, data_masked.GetNbinsX()+1):
                        if data_masked.GetBinCenter(iii) > xmax:
                            data_masked.SetBinContent(iii, 0.0)
                            data_masked.SetBinError(iii, 0.0)
                    combined_data = data_masked


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

                if masks:
                    if hist_name in masks:
                        x_mask_min = masks[hist_name]

                        ymin = hRatio.GetMinimum()
                        ymax = hRatio.GetMaximum()
                        xmin = hRatio.GetXaxis().GetXmin()
                        xmax = hRatio.GetXaxis().GetXmax()

                        box = ROOT.TBox(x_mask_min, ymin, xmax, ymax)
                        box.SetFillColor(ROOT.kGray+1)
                        box.SetFillStyle(3001)   
                        box.SetLineColor(0)
                        box.Draw("same")

                        latex = ROOT.TLatex()
                        latex.SetTextSize(0.15)
                        latex.SetTextColor(ROOT.kRed+2)
                        latex.SetTextAlign(22)
                        latex.DrawLatex((x_mask_min+xmax)/2.0, (ymin+ymax)/2.0, "MASKED")

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

                if split_BRs:
                    legend = ROOT.TLegend(0.155, 0.70, 0.80, 0.88)
                    legend.SetNColumns(4);  
                    legend.SetTextSize(0.01) 
                    legend.SetBorderSize(0)
                    legend.SetFillStyle(0) 
                else:
                    legend = ROOT.TLegend(0.7, 0.50, 0.86, 0.74)
                
                



                print("Made %s total combined BR hists. "%(len(BR_hists)))



                for iii,found_sample in enumerate(found_samples):
                    legend.AddEntry(BR_hists[iii], legend_translator[found_sample], "f")


                """legend.AddEntry(BR_hists[0], "ST-s-channel-hadrons", "f")
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
                #legend.AddEntry(BR_hists[13], "QCD1000to1500", "f")
                #legend.AddEntry(BR_hists[14], "QCD1500to2000", "f")
                #legend.AddEntry(BR_hists[15], "QCD2000toInf", "f")


                legend.AddEntry(BR_hists[13], "QCDMC_Pt_170to300", "f")
                legend.AddEntry(BR_hists[14], "QCDMC_Pt_300to470", "f")
                legend.AddEntry(BR_hists[15], "QCDMC_Pt_470to600", "f")
                legend.AddEntry(BR_hists[16], "QCDMC_Pt_600to800", "f")
                legend.AddEntry(BR_hists[17], "QCDMC_Pt_800to1000", "f")
                legend.AddEntry(BR_hists[18], "QCDMC_Pt_1000to1400", "f")
                legend.AddEntry(BR_hists[19], "QCDMC_Pt_1400to1800", "f")
                legend.AddEntry(BR_hists[20], "QCDMC_Pt_1800to2400", "f")
                legend.AddEntry(BR_hists[21], "QCDMC_Pt_2400to3200", "f")
                legend.AddEntry(BR_hists[22], "QCDMC_Pt_3200toInf", "f")"""


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
    parser.add_argument("--file_dir", required=False, help="Path to where input ROOT files are stored, default is on EOS.")
    parser.add_argument("--hist_names", required=True, help="Comma-separated list of histogram names")
    parser.add_argument("--output_dir", required=True, help="Path to desired output directory")
    parser.add_argument("--mask",     default=None ,required=False, help="Lower bound to mask certain input hists. Ex: --mask h_totHT:1500,h_jet_mass:1000, ...")
    parser.add_argument("--split_BRs",     action="store_true" , help="Option to combine like backgrounds into processes.")

    args = parser.parse_args()
    hist_names = [name.strip() for name in args.hist_names.split(',')]

    if args.mask:
        for mask_pair in args.mask.split(','):
            if len(mask_pair.split(":"))< 2:
                raise ValueError("ERROR with %s: unpaired mask/value"%(mask_pair))
        masks = {mask_pair.split(":")[0]: float(mask_pair.split(":")[1]) for mask_pair in args.mask.split(',')}
    else:
        masks = None

    make_plots(args.file_dir, hist_names,args.output_dir,masks, args.split_BRs)




# EX:
#python plot_var_dataMC.py --hist_names h_nAK4_all,h_totHT,h_AK8_jet_mass,h_AK8_jet_pt,h_nfatjets,h_nfatjets_pre,h_dijet_mass,h_AK8_jet_mass_CR,h_AK4_jet_mass_CR,h_totHT_CR,h_totHT_AT1b,h_totHT_AT0b,h_nfatjets_CR,h_nAK4_CR,h_SJ_nAK4_100_CR,h_SJ_nAK4_200_CR,h_SJ_mass_CR,h_disuperjet_mass_CR,h_SJ_mass_AT0b,h_disuperjet_mass_AT0b,h_nAK4_AT0b,h_nMedBTags --output_dir plots/B2G_update --mask h_totHT:3000,h_AK8_jet_mass:500,h_AK8_jet_pt:1200,h_dijet_mass:1200,h_AK8_jet_mass_CR:500,h_AK4_jet_mass_CR:250,h_totHT_CR:3000,h_totHT_AT1b:4000,h_SJ_mass_CR:2000,h_disuperjet_mass_CR:4000
