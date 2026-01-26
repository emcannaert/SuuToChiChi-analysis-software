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


    legend_translator = {"ST_":"Single Top", "TTJets":r"t \bar{t}","WJets":"W+Jets","QCD":"QCD"}


    if not file_dir:
        file_dir    =  "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/"

    years = ["2015", "2016", "2017", "2018"]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    color_hexes = [
        "#D73027",  # Deep Red
        "#1A9850",  # Emerald Green
        "#FC8D59",  # Bright Orange
        "#FEE08B",  # Golden Yellow
        "#D9EF8B",  # Light Olive
        "#91CF60",  # Teal Green
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
     #"TTToLeptonicMC",
    #"TTToSemiLeptonicMC",
    #"TTToHadronicMC",
    "TTJetsMCHT800to1200",
    "TTJetsMCHT1200to2500",
    "TTJetsMCHT2500toInf",
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

    print("hist_names is %s"%(hist_names))


    output_pdf = os.path.join(output_dir, "%s_vs_%s_"%(hist_names[0],hist_names[1])+timestamp+ ".pdf")
    first_page = True


    for year in years:

        year_str = year
        if year == "2015": year_str = "2016preAPV"
        if year == "2016": year_str = "2016postAPV"



        c = ROOT.TCanvas("c", "c", 1600, 1200)
        legend = ROOT.TLegend(0.12, 0.40, 0.38, 0.64)

        stack_plots         = []
        BR_hists            = []
        combined_hists      = []


        for jjj,hist_name in enumerate(hist_names): 

            region = "preselected"

            cand_regions = ["AT1b","AT0b","CR","SR","ADT1b","ADT0b"]

            ## try to interpret the region from the hist name
            for cand_region in cand_regions:
                if cand_region in hist_name: 
                    region = cand_region
                    break

            print("For hist %s, interpreted region as %s."%(hist_name,region))


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

                "TTJetsMCHT800to1200": return_BR_SF(year, "TTJetsMCHT800to1200"),
                "TTJetsMCHT1200to2500": return_BR_SF(year, "TTJetsMCHT1200to2500"),
                "TTJetsMCHT2500toInf": return_BR_SF(year, "TTJetsMCHT2500toInf"),


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
                "QCDMC_Pt_3200toInf":   return_BR_SF(year, "QCDMC_Pt_3200toInf"),

                "QCD_Pt_170to300":   return_BR_SF(year, "QCDMC_Pt_170to300"),
                "QCD_Pt_300to470":    return_BR_SF(year, "QCDMC_Pt_300to470"),
                "QCD_Pt_470to600":     return_BR_SF(year, "QCDMC_Pt_470to600"),
                "QCD_Pt_600to800":    return_BR_SF(year, "QCDMC_Pt_600to800"),
                "QCD_Pt_800to1000":   return_BR_SF(year, "QCDMC_Pt_800to1000"),
                "QCD_Pt_1000to1400":   return_BR_SF(year, "QCDMC_Pt_1000to1400"),
                "QCD_Pt_1400to1800":  return_BR_SF(year, "QCDMC_Pt_1400to1800"),
                "QCD_Pt_1800to2400":  return_BR_SF(year, "QCDMC_Pt_1800to2400"),
                "QCD_Pt_2400to3200":  return_BR_SF(year, "QCDMC_Pt_2400to3200"),
                "QCD_Pt_3200toInf":   return_BR_SF(year, "QCDMC_Pt_3200toInf")
            
            }

            BR_types = ["ST_", "WJets", "TTJets", "QCD" ]

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
                hist.SetLineColor(colors[iii])
                #hist.SetLineColor(colors[iii])
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
                    print("ERROR: Histogram not found: %s, %s, %s"%(BR_types,hist_name, year))
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

            combined_hists.append(combined_hist_BR)

            if combined_hist_BR:

                #c.SetRightMargin(0.15)
                
                # Determine which histogram has a larger maximum

                combined_hist_BR.SetLineColor(colors[jjj])
                combined_hist_BR.GetYaxis().SetTitleOffset(1.2)
                combined_hist_BR.SetLineWidth(3)
                combined_hist_BR.SetMaximum(1.4*combined_hist_BR.GetMaximum())

                if jjj == 0: combined_hist_BR.Draw("HIST")
                else: combined_hist_BR.Draw("HIST, SAME")


                c.Update()

                x_min = 0
                x_max = 0
                
                print("hist_name is %s"%(hist_name))
                print("hist_name.split() is %s"%(hist_name.split("_")))
                print("hist_name.split()[1:] is %s"%(hist_name.split()[1:]))

                comparison_title =  " ".join(hist_name.split("_")[1:])

                print("The title is %s"%(comparison_title))

                obj_str = "Events"
                if "jet" in combined_hist_BR.GetTitle() or "Jet" in combined_hist_BR.GetTitle(): obj_str = "Jets"

                text = ROOT.TText()
                text.SetNDC(True)  
                text.SetTextSize(0.025)
                text.DrawText(0.125, 0.85 - jjj*0.06, "%s,   MC %s = %s"%( comparison_title, obj_str,np.round(combined_hist_BR.Integral(),2)))

                legend.AddEntry(combined_hist_BR, "%s"%( comparison_title), "f")
            else:
                print "No histograms combined for", hist_name

            legend.Draw()


            write_cms_text.write_cms_text(CMS_label_xpos=0.138, SIM_label_xpos=0.345,CMS_label_ypos = 0.925, SIM_label_ypos = 0.925, lumistuff_xpos=0.90, lumistuff_ypos=0.91, year = "", uses_data=True)
            png_path = os.path.join(output_dir, "%s_vs_%s"%(hist_names[0],hist_names[1]) + "_" + year + "_"+ region + ".png")
            #root_out_path = os.path.join(output_dir, "dataMC_" + hist_name + "_" + year + ".root")

            c.SaveAs(png_path)

            if first_page:
                c.SaveAs(output_pdf + "[")
                first_page = False

            c.SaveAs(output_pdf)


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




    args = parser.parse_args()
    hist_names = [name.strip() for name in args.hist_names.split(',')]

    if len(hist_names) != 2:
        raise ValueError("ERROR: only give two hist names (ex. python compare_var_distributions.py --hist_names h_one,h_two --output_dir plots/test)")
    make_plots(args.file_dir, hist_names,args.output_dir)




# EX:
# python compare_var_distributions.py --hist_names h_disuperjet_mass_unshifted_SR,h_disuperjet_mass_SR --output_dir plots/var_comparisons/shifted_disuperjet_mass_SR_vs_disuperjet_mass_unshifted_SR --file_dir "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles_shiftedMass/" 


