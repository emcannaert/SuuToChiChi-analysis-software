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
#ROOT.TColor.InvertPalette();
ROOT.gStyle.SetNumberContours(255);

### create_combined_SJ_plots.py
#
# creates plots of SJ mass, diSJ mass, and avg. SJ mass vs diSJ mass for ALL years combined.
# ratio plots showing signal / sqrt(BR) for different signal mass points are shown 
# In control regions, data / MC is also shown (data points)


file_dir =  "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/"
output_dir =  "plots/combined_sig_SJ_plots/"

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")

pdf_type_str = ""


output_pdf = os.path.join(output_dir, "combined_sig_SJ_plots"+ pdf_type_str +"_" +timestamp+ ".pdf")
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





def make_2D_plot(region, mass_point, hist_name):

    global first_page


    # will loop over all of these
    years = ["2015", "2016", "2017", "2018"]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #sig_samples = [] 

    decays      = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]

    #for decay in decays:
    #    sig_samples.append("%s_%s"%(mass_point,decay))

    combined_2D_plot = None
    all_hists = []
    for decay in decays:
        for year in years:  

            scale = return_signal_SF(year,mass_point,decay)

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

        combined_2D_plot.SetTitle("Average Superjet Mass vs Disuperjet Mass (%s) (%s) (Full Run 2)"%(mass_point,region))
        combined_2D_plot.GetYaxis().SetTitle("Avg. SJ Mass [GeV]")

        SetLogScaleZAxis(combined_2D_plot, c)

        c.SetRightMargin(0.15)
        c.SetLeftMargin(0.12)
        combined_2D_plot.Draw("colz")

        text = ROOT.TText()
        text.SetNDC(True)  
        text.SetTextSize(0.025)
        text.DrawText(0.25, 0.85, "Total MC Events = %s"%(np.round(combined_2D_plot.Integral(),2)))

        write_cms_text.write_cms_text(CMS_label_xpos=0.17, SIM_label_xpos=0.39,CMS_label_ypos = 0.925, SIM_label_ypos = 0.925, lumistuff_xpos=0.90, lumistuff_ypos=0.91, year = "", uses_data=True)
        

        type_str = ""
        png_path = os.path.join(output_dir, "combined_MSJ_mass_vs_MdSJ_"+ mass_point + "_" +type_str + region + "_" + "FullRun2" + "_"+ region + ".png")
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





def make_plots(region, hist_name):

    global first_page


    mass_points = ["Suu4_chi1","Suu5_chi1p5","Suu6_chi2","Suu7_chi2p5","Suu8_chi3"]


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


    ### get signal mass points

    mass_points = ["Suu4_chi1","Suu5_chi1p5","Suu6_chi2","Suu7_chi2p5","Suu8_chi3"]
    decays      = ["WBWB","HTHT","ZTZT","WBHT","WBZT","HTZT"]

    signal_hists = [None,None,None,None,None]

    for iii,mass_point in enumerate(mass_points):
        for year in years: 
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

    c = ROOT.TCanvas("c", "c", 1400, 1200)
    c.SetLeftMargin(1.0)
    c.SetLogy()

    if valid_sig_hists == 5:

        #c.SetRightMargin(0.1)
        
        sig_colors = [ROOT.kOrange, ROOT.kCyan, ROOT.kGreen, ROOT.kRed, ROOT.kBlack]


        # Determine which histogram has a larger maximum

        sig_max_max = 10*max([hist.GetMaximum() for hist in signal_hists])

        max_value =sig_max_max 


        # draw signal mass points
        for iii,sig_hist in enumerate(signal_hists):
            sig_hist.SetLineColor(sig_colors[iii])
            sig_hist.SetLineWidth(3)
            
            sig_hist.SetMaximum(sig_max_max)

            if iii == 0: sig_hist.Draw("HIST")
            else: sig_hist.Draw("SAME,HIST")


        c.Update()



        legend = ROOT.TLegend(0.62, 0.6, 0.875, 0.88)


        legend.SetLineColor(0)
        legend.SetBorderSize(0)

        sig_names = ["M_{S_{uu}} = "  +  r"\mbox{4 TeV, }" + "M_{#chi} = "  +  r"\mbox{1 TeV}", 
                        "M_{S_{uu}} = "  +  r"\mbox{5 TeV, }" + "M_{#chi} = "  +  r"\mbox{1.5 TeV}", 
                        "M_{S_{uu}} = "  +  r"\mbox{6 TeV, }" + "M_{#chi} = "  +  r"\mbox{2 TeV}",
                        "M_{S_{uu}} = "  +  r"\mbox{7 TeV, }" + "M_{#chi} = "  +  r"\mbox{2.5 TeV}",  
                        "M_{S_{uu}} = "  +  r"\mbox{8 TeV, }" + "M_{#chi} = "  +  r"\mbox{3 TeV}", ]
        sig_names_tex = [
            "M_{S_{uu}} = 4 TeV, M_{#chi} = 1 TeV",
            "M_{S_{uu}} = 5 TeV, M_{#chi} = 1.5 TeV",
            "M_{S_{uu}} = 6 TeV, M_{#chi} = 2 TeV",
            "M_{S_{uu}} = 7 TeV, M_{#chi} = 2.5 TeV",
            "M_{S_{uu}} = 8 TeV, M_{#chi} = 3 TeV",
        ]

        for iii,sig_hist in enumerate(signal_hists):
            legend.AddEntry(sig_hist, sig_names[iii], "l")

        legend.Draw()

        obj_str = "Events"

        
        label = ROOT.TLatex()
        label.SetNDC(True)  
        label.SetTextSize(0.015)
        label.SetTextAlign(13) 

        for iii,signal_hist in enumerate(signal_hists):
            label.DrawLatex(0.15, 0.88 - 0.02*iii, "Total %s Events = %s"%(sig_names_tex[iii],np.round(signal_hist.Integral(),2)))






        c.Update()

        type_str = ""

        write_cms_text.write_cms_text(CMS_label_xpos=0.138, SIM_label_xpos=0.345,CMS_label_ypos = 0.925, SIM_label_ypos = 0.925, lumistuff_xpos=0.90, lumistuff_ypos=0.91, year = "", uses_data=True)
        png_path = os.path.join(output_dir, "combined_sig_" + hist_name + "_"+ type_str + region + "_" + "FullRun2" + "_"+ region + ".png")
        #root_out_path = os.path.join(output_dir, "dataMC_" + hist_name + "_" + year + ".root")

        c.SaveAs(png_path)

        if first_page:
            c.SaveAs(output_pdf + "[")
            first_page = False

        c.SaveAs(output_pdf)

    else:
        print("Failed for region %s"%region)
    del c 





if __name__=="__main__":


    regions = ["SR","CR","AT1b","AT0b"]
    hist_names = ["h_SJ_mass","h_disuperjet_mass",]
    mass_points = ["Suu4_chi1","Suu5_chi1p5","Suu6_chi2","Suu7_chi2p5","Suu8_chi3"]



    for iii,region in enumerate(regions):
        for hist_name in hist_names:
            make_plots(region,hist_name)
        for mass_point in mass_points:
            make_2D_plot(region, mass_point, "h_MSJ_mass_vs_MdSJ")

c2 = ROOT.TCanvas("", "", 1200, 1200)
if not first_page:
    c2.SaveAs(output_pdf + "]")
    print "All plots written to", output_pdf
else:
    print "No plots created for", hist_name, ". PDF not generated."
del c2  


