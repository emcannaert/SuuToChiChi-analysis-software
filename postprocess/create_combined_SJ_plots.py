import ROOT
import os
from return_BR_SF.return_BR_SF import return_BR_SF
from return_signal_SF.return_signal_SF import return_signal_SF
from write_cms_text import write_cms_text
import numpy as np
import argparse
import datetime
ROOT.gROOT.SetBatch(True)


ROOT.gStyle.SetPalette(ROOT.kViridis);
ROOT.TColor.InvertPalette();
ROOT.gStyle.SetNumberContours(255);

useTTTo  = True
useQCDHT = True
### create_combined_SJ_plots.py
#
# creates plots of SJ mass, diSJ mass, and avg. SJ mass vs diSJ mass for ALL years combined.
# ratio plots showing signal / sqrt(BR) for different signal mass points are shown 
# In control regions, data / MC is also shown (data points)


file_dir =  "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/"
output_dir =  "plots/combined_SJ_plots/"

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

pdf_type_str = ""
if useTTTo: pdf_type_str += "_wTTTo"
if useQCDHT: pdf_type_str += "_wQCDHT"

output_pdf = os.path.join(output_dir, "combined_SJ_plots"+ pdf_type_str +"_" +timestamp+ ".pdf")
first_page = True

def create_sqrt_histogram(original_hist):
    # Create a new histogram with the same binning as the original
    sqrt_hist = original_hist.Clone("sqrt_hist")
    sqrt_hist.SetTitle("Square Root of Original Histogram")
    sqrt_hist.SetDirectory(0)
    # Loop over bins and set each bin content to sqrt of the original bin content
    for bin_idx in range(1, original_hist.GetNbinsX() + 1):
        original_content = original_hist.GetBinContent(bin_idx)
        sqrt_content = ROOT.TMath.Sqrt(original_content)
        sqrt_hist.SetBinContent(bin_idx, sqrt_content)
        sqrt_hist.SetBinError(bin_idx, 0)  # Set errors to zero if needed

    return sqrt_hist


def SetLogScaleZAxis(hist, canvas):

    zmin = 1e10
    zmax = -1e10

    histMax = hist.GetMaximum();

    for i in range(1,hist.GetNbinsX()):
        for j in range(1,hist.GetNbinsY()):
            binContent = hist.GetBinContent(i,j)
            if ( (binContent > 0) and (binContent < zmin) ):
                zmin = binContent

    if (histMax > zmax): zmax = histMax

    hist.SetMinimum(zmin)
    hist.SetMaximum(zmax)
    ROOT.gPad.SetLogz()
    canvas.Update()





def make_2D_plot(region, isMasked, hist_name):

    global first_page
    global useTTTo
    global useQCDHT

    # will loop over all of these
    years = ["2015", "2016", "2017", "2018"]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

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




    ] 

    if useTTTo: BR_samples.extend( [ "TTToLeptonicMC", "TTToSemiLeptonicMC", "TTToHadronicMC"  ]  )
    else:       BR_samples.extend( [     "TTJetsMCHT800to1200", "TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf", ]  )

    if useQCDHT: BR_samples.extend([      "QCDMC1000to1500","QCDMC1500to2000", "QCDMC2000toInf"   ])
    else: BR_samples.extend( [
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
        ])

    combined_2D_plot = None
    all_hists = []
    for iii,sample in enumerate(BR_samples):
        for year in years:

            scale = return_BR_SF(year, sample.replace("-","_"))

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

            hist = f.Get("nom/" + hist_name + "_" + region )

            if not hist:
                print "  ERROR: Histogram not found:", hist_name  + "_" + region , "in", file_path
                f.Close()
                continue

            hist.SetDirectory(0)
            hist.Scale(scale)
            hist.SetStats(0)
            all_hists.append(hist)
            #print("Getting histogram %s"%("nom/" + hist_name + "_" + region))
            #print("hist integral is %s"%(hist.Integral()))
            if not combined_2D_plot: 
                combined_2D_plot = hist.Clone("combined_2D_plot")
                combined_2D_plot.SetDirectory(0)
            else: combined_2D_plot.Add(hist)
            #print("Full hist integral is %s"%(combined_2D_plot.Integral()))

            f.Close()


    c = ROOT.TCanvas("c", "c", 1300, 1200)
    if combined_2D_plot:

        combined_2D_plot.SetTitle("Average Superjet Mass vs Disuperjet Mass (%s) (Full Run 2)"%(region))
        combined_2D_plot.GetYaxis().SetTitle("Avg. SJ Mass [GeV]")

        SetLogScaleZAxis(combined_2D_plot, c)

        c.SetRightMargin(0.15)
        c.SetLeftMargin(0.12)
        combined_2D_plot.Draw("colz")

        text = ROOT.TText()
        text.SetNDC(True)  
        text.SetTextSize(0.025)
        text.DrawText(0.4, 0.85, "MC Events = %s"%(np.round(combined_2D_plot.Integral(),2)))

        write_cms_text.write_cms_text(CMS_label_xpos=0.17, SIM_label_xpos=0.39,CMS_label_ypos = 0.925, SIM_label_ypos = 0.925, lumistuff_xpos=0.90, lumistuff_ypos=0.91, year = "", uses_data=True)
        

        type_str = ""
        if useTTTo: type_str += "_wTTTo"
        if useQCDHT: type_str += "_wQCDHT"
        png_path = os.path.join(output_dir, "combined_h_MSJ_mass_vs_MdSJ_"+ type_str + region + "_" + "FullRun2" + "_"+ region + ".png")
        #root_out_path = os.path.join(output_dir, "dataMC_" + hist_name + "_" + year + ".root")

        c.SaveAs(png_path)

        if first_page:
            c.SaveAs(output_pdf + "[")
            first_page = False

        c.SaveAs(output_pdf)

    else:
        print "No histograms combined for", hist_name + "_" + region
        print "combined_2D_plot: :", combined_2D_plot
    del c 





def make_plots(region, isMasked, hist_name):

    global first_page
    global useTTTo
    global useQCDHT

    legend_translator = {"ST_":"Single Top", "TTJets":r"t \bar{t}","TTTo":r"t \bar{t}"  ,"WJets":"W+Jets","QCD":"QCD"}

    split_BRs = False # to split each BR into its sub-datasets

    # will loop over all of these
    years = ["2015", "2016", "2017", "2018"]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    color_hexes = [
        "#D73027",  # Deep Red
        #"#FC8D59",  # Bright Orange
        "#FEE08B",  # Golden Yellow
        "#D9EF8B",  # Light Olive
        "#91CF60",  # Teal Green
        "#1A9850",  # Emerald Green
        "#66BD63",  # Sky Blue
        #"#A6D96A",  # Light Cyan
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
        #"#33A02C",  # Lime Green
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




    ] 

    if useTTTo: BR_samples.extend( [ "TTToLeptonicMC", "TTToSemiLeptonicMC", "TTToHadronicMC"  ]  )
    else:       BR_samples.extend( [     "TTJetsMCHT800to1200", "TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf", ]  )

    if useQCDHT: BR_samples.extend([      "QCDMC1000to1500","QCDMC1500to2000", "QCDMC2000toInf"   ])
    else: BR_samples.extend( [
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
        ])


    BR_hists            = []

    x_axis = "disuperjet mass" if "disuperjet" in hist_name else "SJ Mass"
    bin_width = 200 if "disuper" in hist_name else 100
    hs = ROOT.THStack("h_BR", "(Full Run 2); %s [GeV];Events / %s GeV"%(x_axis,bin_width)) # region (%s)


    data_samples = {"2015": ["dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM" ,"dataF-HIPM"], 
    "2016": ["dataF","dataG","dataH"], 
    "2017": ["dataB","dataC","dataD","dataE","dataF"], 
    "2018": ["dataA","dataB", "dataC", "dataD"] }


    if split_BRs:
        BR_types = BR_samples
    else: 
        BR_types = ["ST_", "WJets", "TTJets", "QCD" ]

    BR_groups = {BR_type: None for BR_type in BR_types}


    for iii,sample in enumerate(BR_samples):
        for year in years:

            scale = return_BR_SF(year, sample.replace("-","_"))

            # find out which type of BR this is
            BR_type = ""
            for _BR_type in BR_types:
                if _BR_type in sample: 
                    BR_type = _BR_type
                    break
                elif _BR_type == "TTJets" and "TTTo" in sample:
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

            hist = f.Get("nom/" + hist_name + "_" + region )

            if not hist:
                print "  ERROR: Histogram not found:", hist_name  + "_" + region , "in", file_path
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
            print("ERROR: Histogram not found: %s, %s, %s"%(BR_types,hist_name, year))
            continue

        if iii == 0: 
            #print("hist is %s, title is %s"%(hist.GetName(),hist.GetTitle()))
            hs.SetTitle("%s (Full Run 2);%s [GeV]; Events / %s"%(hist.GetTitle(), hist.GetXaxis().GetTitle(), hist.GetYaxis().GetTitle() ))

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
    for year in years:
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

            hist = f.Get("nom/" + hist_name + "_"+ region)
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



    if isMasked:
        data_masked = combined_data.Clone(combined_data.GetName() + "_masked")
        data_masked.SetDirectory(0)  # detach from any TFile

        for iii in range(1, data_masked.GetNbinsX()+1):
            data_masked.SetBinContent(iii, 0.0)
            data_masked.SetBinError(iii, 0.0)
        combined_data = data_masked


    ### get signal mass points

    mass_points = ["Suu4_chi1","Suu6_chi2","Suu8_chi3"]
    decays = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]

    signal_hists = [None,None,None]

    for iii,mass_point in enumerate(mass_points):
        for decay in decays:

            file_name = mass_point + "_" + decay + "_" + year + "_processed.root"
            file_path = os.path.join(file_dir, file_name)

            if not "cmseos" in file_dir:
                if not os.path.exists(file_path):
                    print "  WARNING: File not found:", file_path
                    continue

            f = ROOT.TFile.Open(file_path)
            if not f or f.IsZombie():
                print "  ERROR: Could not open:", file_path
                continue

            hist = f.Get("nom/" + hist_name + "_" + region)
            if not hist:
                print "  ERROR: Histogram not found:", hist_name, "in", file_path
                f.Close()
                continue

            hist.SetDirectory(0)
            hist.SetMinimum(1e-2)
            hist.SetStats(0)

            scale = return_signal_SF(year,mass_point,decay)

            hist.Scale(scale)

            if signal_hists[iii]:
                signal_hists[iii].Add(hist)
                #print("added hist to %s"%signal_hists[iii].GetName())
            else:
                signal_hists[iii] = hist.Clone("combined_%s"%(mass_point))
                #print("created hist %s"%signal_hists[iii].GetName())
            signal_hists[iii].SetDirectory(0)
            f.Close()

    valid_sig_hists = sum([  not sig_hist.IsZombie() for sig_hist in signal_hists])

    c = ROOT.TCanvas("c", "c", 1200, 1200)
    if combined_hist_BR and combined_data and valid_sig_hists == 3:

        c.SetRightMargin(0.15)
        
        sig_colors = [ROOT.kOrange, ROOT.kCyan, ROOT.kGreen]

        # Create a canvas and pads for upper and lower plots
        pad1 = ROOT.TPad("pad1", "Top pad", 0, 0.33, 1, 1.0)
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

        sig_max_max = max([hist.GetMaximum() for hist in signal_hists])

        max_value = max( combined_data.GetMaximum(), combined_hist_BR.GetMaximum(), sig_max_max )

        hs.Draw("HIST")
        hs.SetMaximum(100*max_value)
        hs.SetMinimum(1e-2)

        combined_data.SetMarkerStyle(20)         # Solid circles
        combined_data.SetMarkerColor(ROOT.kBlack)
        combined_data.SetLineColor(ROOT.kBlack)  # Error bar color
        combined_data.SetLineWidth(1)
        combined_data.Draw("PE1,SAME")


        # draw signal mass points
        for iii,sig_hist in enumerate(signal_hists):
            sig_hist.SetLineColor(sig_colors[iii])
            sig_hist.SetLineWidth(3)
            sig_hist.Draw("SAME,HIST")


        c.Update()

        # Draw the ratio on the lower pad
        pad2.cd()

        if region != "SR":
            hRatio = combined_data.Clone("hRatio_data")

            hRatio.SetTitle("")
            hRatio.Divide( combined_hist_BR)  # Compute the ratio h2 / hStackTotal
            hRatio.GetYaxis().SetTitle(r"obs. / MC")

            hRatio.GetYaxis().SetTitleSize(0.1)
            hRatio.GetYaxis().SetTitleOffset(0.4)
            hRatio.GetYaxis().SetLabelSize(0.08)
            hRatio.GetXaxis().SetTitleSize(0.12)
            hRatio.GetXaxis().SetLabelSize(0.1)

            hRatio.SetMinimum(0.05)
            hRatio.SetMaximum(2.0)

            hRatio.Draw()

            x_min = hRatio.GetXaxis().GetXmin()
            x_max = hRatio.GetXaxis().GetXmax()

        if region == "SR":


            ratio_hists = []

            max_value = -999
            
            pad2.SetLogy()
            for iii,sig_hist in enumerate(signal_hists):

                hRatio_sig = sig_hist.Clone("hRatio_sig%s"%iii)
                hRatio_sig.SetMinimum(0.05)
                #hRatio_sig.SetMaximum(2.0)
                hRatio_sig.Divide( create_sqrt_histogram(combined_hist_BR) ) # Compute the ratio h2 / hStackTotal

                if hRatio_sig.GetMaximum() > max_value: max_value = hRatio_sig.GetMaximum()

            for iii,sig_hist in enumerate(signal_hists):

                hRatio_sig = sig_hist.Clone("hRatio_sig%s"%iii)
                hRatio_sig.SetMinimum(0.05)
                hRatio_sig.SetMaximum(4*max_value)
                hRatio_sig.SetTitle("")
                hRatio_sig.GetYaxis().SetTitle(r"sig / #sqrt{BR}")
                hRatio_sig.Divide( create_sqrt_histogram(combined_hist_BR) ) # Compute the ratio h2 / hStackTotal
                hRatio_sig.SetLineColor(sig_colors[iii])
                hRatio_sig.SetLineWidth(3)
                hRatio_sig.GetYaxis().SetTitleSize(0.1)
                hRatio_sig.GetYaxis().SetTitleOffset(0.4)
                hRatio_sig.GetYaxis().SetLabelSize(0.08)
                hRatio_sig.GetXaxis().SetTitleSize(0.12)
                hRatio_sig.GetXaxis().SetLabelSize(0.1)
                ratio_hists.append(hRatio_sig)
                #for jjj in range(1,hRatio_sig.GetNbinsX()):
                #    print("%s ---- bin %s, yield = %s"%(hRatio_sig.GetName(), jjj, hRatio_sig.GetBinContent(jjj)))

                #print("Drawing hist %s with max value %s"%(hRatio_sig.GetName(), hRatio_sig.GetMaximum()))

                if iii == 0: hRatio_sig.Draw("HIST")
                else: hRatio_sig.Draw("SAME HIST")

                x_min = hRatio_sig.GetXaxis().GetXmin()
                x_max = hRatio_sig.GetXaxis().GetXmax()
            pad2.Update()
            c.Update()

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
            legend = ROOT.TLegend(0.6, 0.50, 0.9, 0.88)

        print("Made %s total combined BR hists. "%(len(BR_hists)))


        legend.SetLineColor(0)
        legend.SetBorderSize(0)

        for iii,found_sample in enumerate(found_samples):
            legend.AddEntry(BR_hists[iii], legend_translator[found_sample], "f")


        sig_names = ["M_{S_{uu}} = "  +  r"\mbox{4 TeV, }" + "M_{#chi} = "  +  r"\mbox{1 TeV}", 
                        "M_{S_{uu}} = "  +  r"\mbox{6 TeV, }" + "M_{#chi} = "  +  r"\mbox{2 TeV}", 
                        "M_{S_{uu}} = "  +  r"\mbox{8 TeV, }" + "M_{#chi} = "  +  r"\mbox{3 TeV}", ]


        for iii,sig_hist in enumerate(signal_hists):
            legend.AddEntry(sig_hist, sig_names[iii], "l")

        if region != "SR": legend.AddEntry(combined_data, "Data", "p")
        legend.Draw()

        obj_str = "Events" if "disuper" in hist_name else "Superjets"

        text = ROOT.TText()
        text.SetNDC(True)  
        text.SetTextSize(0.025)
        text.DrawText(0.4, 0.85, "MC %s = %s"%(obj_str,np.round(combined_hist_BR.Integral(),2)))
        text.DrawText(0.4, 0.80, "Data %s = %s"%(obj_str,np.round(combined_data.Integral(),2)))

        pad2.Update()
        c.Update()

        type_str = ""
        if useTTTo: type_str += "_wTTTo"
        if useQCDHT: type_str += "_wQCDHT"

        write_cms_text.write_cms_text(CMS_label_xpos=0.138, SIM_label_xpos=0.305,CMS_label_ypos = 0.925, SIM_label_ypos = 0.925, lumistuff_xpos=0.90, lumistuff_ypos=0.91, year = "", uses_data=True)
        png_path = os.path.join(output_dir, "combined_" + hist_name + "_"+ type_str + region + "_" + "FullRun2" + "_"+ region + ".png")
        #root_out_path = os.path.join(output_dir, "dataMC_" + hist_name + "_" + year + ".root")

        c.SaveAs(png_path)

        if first_page:
            c.SaveAs(output_pdf + "[")
            first_page = False

        c.SaveAs(output_pdf)

        #out_file = ROOT.TFile(root_out_path, "RECREATE")
        #combined_hist_BR.Write()
        #out_file.Close()

        #print "Saved", hist_name,
    else:
        print "No histograms combined for", hist_name + "_" + region
        print "combined_hist_BR: :", combined_hist_BR
        print "combined_data     :", combined_data
        print "valid_sig_hists   :", valid_sig_hists
        print "combined_hist_BR is %s"%combined_hist_BR
        print "combined_data is %s"%combined_data
        print "valid_sig_hists is %s"%valid_sig_hists
    del c 





if __name__=="__main__":


    regions = ["SR","CR","AT1b","AT0b"]
    isMasked = [True,False,False,False]

    hist_names = ["h_SJ_mass","h_disuperjet_mass",]

    for iii,region in enumerate(regions):
        for hist_name in hist_names:


            make_plots(region,isMasked[iii],hist_name)
        make_2D_plot(region,isMasked[iii],"h_MSJ_mass_vs_MdSJ")

c2 = ROOT.TCanvas("", "", 1200, 1200)
if not first_page:
    c2.SaveAs(output_pdf + "]")
    print "All plots written to", output_pdf
else:
    print "No plots created for", hist_name, ". PDF not generated."
del c2  


