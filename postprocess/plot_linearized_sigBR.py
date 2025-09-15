import ROOT
from write_cms_text import write_cms_text


ROOT.TH1.SetDefaultSumw2(True)
ROOT.TH2.SetDefaultSumw2(True) 

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


# plots linearized signal and BR (stacked) with signal sensitity as a function of linerized bin number
def plot_linearized_signal_vs_BR_histogram(year,region,mass_point, technique_type,QCD_type):

    CMS_label_pos = 0.132
    SIM_label_pos = 0.270

    technique_str = "cut-based"
    if "NN" in technique_type:
        #print("Technique type is %s."%technique_type)
        technique_str = "NN-based"

    file_name = "finalCombineFilesNewStats/%s/combine_%s%s_%s.root"%(QCD_type,technique_type, year, mass_point)
    
    root_file = ROOT.TFile.Open(file_name)
    if not root_file:
        print("ERROR: couldn't find file %s"%file_name)
        return
    sig_hist_name   = "%s/sig"%region
    allBR_hist_name = "%s/allBR"%region

    QCD_hist_name = "%s/QCD"%region
    TTbar_hist_name = "%s/TTbar"%region
    WJets_hist_name = "%s/WJets"%region
    ST_hist_name = "%s/ST"%region


    # Get the histograms
    sig_hist   = root_file.Get(sig_hist_name)
    sig_hist.SetLineStyle(2)
    sig_hist.SetLineWidth(5)
    sig_hist.SetLineColor(ROOT.kBlack)

    allBR_hist = root_file.Get(allBR_hist_name)

    QCD_hist = root_file.Get(QCD_hist_name)
    WJets_hist = root_file.Get(WJets_hist_name)
    TTbar_hist = root_file.Get(TTbar_hist_name)
    ST_hist = root_file.Get(ST_hist_name)


    QCD_hist.SetLineColor(ROOT.kRed)
    TTbar_hist.SetLineColor(ROOT.kYellow)
    WJets_hist.SetLineColor(ROOT.kViolet)
    ST_hist.SetLineColor(ROOT.kGreen)

    # Set colors for each sub-histogram in the stack
    QCD_hist.SetFillColor(ROOT.kRed)
    TTbar_hist.SetFillColor(ROOT.kYellow)
    WJets_hist.SetFillColor(ROOT.kViolet)
    ST_hist.SetFillColor(ROOT.kGreen)

    QCD_hist.SetMinimum(1e-1) 
    TTbar_hist.SetMinimum(1e-1)
    WJets_hist.SetMinimum(1e-1)
    ST_hist.SetMinimum(1e-1)


    # Create a THStack and add the sub-histograms
    hs = ROOT.THStack("h_stack", "Linearized Background vs Signal (%s) (%s) (%s) (%s)"%(mass_point, region,year, technique_str))
    hs.Add(TTbar_hist)
    hs.Add(ST_hist)
    hs.Add(WJets_hist)
    hs.Add(QCD_hist)

    hs.SetMinimum(1e-1)

    allBR_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year,technique_str))
    sig_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year,technique_str))

    QCD_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year,technique_str))
    TTbar_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year,technique_str))
    ST_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year,technique_str))
    WJets_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year,technique_str))

    """# Check if histograms exist
    if not sig_hist or not allBR_hist or not QCD_hist or not TTbar_hist or not ST_hist:
        print("ERROR: One or both histograms not found in the file.")
        return"""

    # Create a canvas and pads for upper and lower plots
    c = ROOT.TCanvas("c", "", 1200, 1000)
    pad1 = ROOT.TPad("pad1", "Top pad", 0, 0.30, 1, 1.0)
    pad2 = ROOT.TPad("pad2", "Bottom pad", 0, 0.0, 1, 0.295)
    

    # Adjust margins
    pad1.SetTopMargin(0.1)  # Default is 0.05; increase if needed
    pad1.SetBottomMargin(0.01)  # Space between the top and bottom pad
    pad2.SetTopMargin(0.00)
    pad2.SetBottomMargin(0.4)  # Increase for better spacing in bottom pad

    pad1.Draw()
    pad2.Draw()

    # Draw the stack and h2 on the upper pad
    pad1.cd()
    pad1.SetLogy()

    hRatio = sig_hist.Clone("hRatio")

    # Determine which histogram has a larger maximum
    if sig_hist.GetMaximum() > allBR_hist.GetMaximum():
        
        hs.SetMaximum(1.1*sig_hist.GetMaximum())
        hs.Draw("HIST")
        sig_hist.Draw("HIST,SAME")

    else:
        hs.Draw("HIST")
        sig_hist.Draw("HIST,same")
        
    # Draw the ratio on the lower pad
    pad2.cd()

    hRatio.Divide( create_sqrt_histogram(allBR_hist))  # Compute the ratio h2 / hStackTotal
    hRatio.SetMarkerStyle(20)
    hRatio.SetTitle("")
    hRatio.GetYaxis().SetTitle(r"sig / #sqrt{BR}")
    #hRatio.GetYaxis().SetNdivisions(505)
    #hRatio.GetYaxis().SetRangeUser(0.0, 1.5)  # Adjust the y-axis range for clarity
    hRatio.GetYaxis().SetTitleSize(0.1)
    hRatio.GetYaxis().SetTitleOffset(0.4)
    hRatio.GetYaxis().SetLabelSize(0.08)
    hRatio.GetXaxis().SetTitleSize(0.12)
    hRatio.GetXaxis().SetLabelSize(0.1)
    hRatio.SetFillColor(ROOT.kGray )
    hRatio.Draw("E2")


    x_min = hRatio.GetXaxis().GetXmin()
    x_max = hRatio.GetXaxis().GetXmax()
    """# Draw a reference line at y = 1 on the ratio plot

    line = ROOT.TLine(x_min, 1.0, x_max, 1.0)
    #line.SetLineColor(ROOT.kGray+2)
    line.SetLineStyle(2)
    line.Draw()"""

    ### create ratio lines at 0.8, 1.0, 1.2
    nom_line = ROOT.TLine(x_min, 1.0, x_max, 1.0)
    nom_line.SetLineStyle(2)  # Dotted line style
    nom_line.Draw("same")

    nom_line_up = ROOT.TLine(x_min, 1.2, x_max, 1.2)
    nom_line_up.SetLineStyle(2)  # Dotted line style
    nom_line_up.Draw("same")


    nom_line_down = ROOT.TLine(x_min, 0.8, x_max, 0.8)
    nom_line_down.SetLineStyle(2)  # Dotted line style
    nom_line_down.Draw("same")

    # Add legend
    pad1.cd()

    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(QCD_hist, "QCD", "f")
    legend.AddEntry(TTbar_hist, "TTbar", "f")
    legend.AddEntry(ST_hist, "ST", "f")
    legend.AddEntry(WJets_hist, "WJets", "f")
    legend.AddEntry(sig_hist, "signal", "l")
    legend.Draw()

    write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)

    # Save the canvas as an image
    output_file = "plots/linearized_sigBR/%s/sig_vs_BR_%s_%s%s_%s.png"%(QCD_type,mass_point,technique_type,region,year)
    c.SaveAs(output_file)

    sig_hist.Draw("HIST")
    output_file = "plots/linearized_sig/%s/linearized_sig_%s_%s%s_%s.png"%(QCD_type,mass_point,technique_type,region,year)
    c.SaveAs(output_file)

    # Close the ROOT file
    root_file.Close()

    del sig_hist
    del allBR_hist
    del c
    del QCD_hist
    del TTbar_hist
    del ST_hist

# plots linearized signal (a few mass points) and BR (stacked) with signal sensitity as a function of linerized bin number
def plot_linearized_signal_vs_BR_multi_mass(year,region, technique_type,QCD_type):


    year_str = "2016preAPV"
    if year == "2016": year_str = "2016postAPV"
    elif year == "2017": year_str = "2017"
    elif year == "2018": year_str = "2018"

    technique_str = "cut-based"
    if "NN" in technique_type:
        print("Technique type is %s."%technique_type)
        technique_str = "NN-based"

    mass_points = ["Suu4_chi1", "Suu6_chi2","Suu8_chi3"]
    file_names = [ "finalCombineFilesNewStats/%s/combine_%s%s_%s.root"%(QCD_type,technique_type, year, mass_point) for mass_point in mass_points ] 
    
    root_files = [ ROOT.TFile.Open(file_name) for file_name in file_names    ]
    for iii,root_file in enumerate(root_files):
        if not root_file:
            print("ERROR: couldn't find file %s"%file_names[iii])
            return


    sig_hist_name   = "%s/sig"%region
    allBR_hist_name = "%s/allBR"%region

    QCD_hist_name = "%s/QCD"%region
    TTbar_hist_name = "%s/TTbar"%region
    WJets_hist_name = "%s/WJets"%region
    ST_hist_name = "%s/ST"%region

    line_colors = [ROOT.kBlack, ROOT.kCyan,ROOT.kGreen]

    # Get the histograms
    hist_line_styles = [2,8,10]
    sig_hists   = [ root_file.Get(sig_hist_name) for root_file in root_files  ]
    for iii,sig_hist in enumerate(sig_hists):
        sig_hist.SetLineStyle(hist_line_styles[iii])
        sig_hist.SetLineWidth(5)
        sig_hist.SetLineColor(line_colors[iii])


    
    allBR_hist = root_files[0].Get(allBR_hist_name)  ## will be the same for all mass points

    colors = [ ROOT.TColor.GetColor(87, 144, 252), ROOT.TColor.GetColor(248, 156, 32), ROOT.TColor.GetColor(228, 37, 54), ROOT.TColor.GetColor(150, 74, 139), ROOT.TColor.GetColor(156, 156, 161), ROOT.TColor.GetColor(122, 33, 221)] 

    QCD_hist = root_files[0].Get(QCD_hist_name)
    WJets_hist = root_files[0].Get(TTbar_hist_name)
    TTbar_hist = root_files[0].Get(WJets_hist_name)
    ST_hist = root_files[0].Get(ST_hist_name)


    QCD_hist.SetLineColor(colors[2])
    TTbar_hist.SetLineColor(colors[3])
    WJets_hist.SetLineColor(colors[0])
    ST_hist.SetLineColor(colors[1])

    # Set colors for each sub-histogram in the stack
    QCD_hist.SetFillColor(colors[2])
    TTbar_hist.SetFillColor(colors[3])
    WJets_hist.SetFillColor(colors[0])
    ST_hist.SetFillColor(colors[1])

    QCD_hist.SetMinimum(1e-1) 
    TTbar_hist.SetMinimum(1e-1)
    WJets_hist.SetMinimum(1e-1)
    ST_hist.SetMinimum(1e-1)


    # Create a THStack and add the sub-histograms
    hs = ROOT.THStack("h_stack", "Linearized Background vs Signal (%s) (%s) (%s); Linearized Bin Number; Events"%(region,year_str, technique_str))
    hs.Add(TTbar_hist)
    hs.Add(ST_hist)
    hs.Add(WJets_hist)
    hs.Add(QCD_hist)

    hs.SetMinimum(1e-1)

    allBR_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year_str,technique_str))
    sig_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year_str,technique_str))

    QCD_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year_str,technique_str))
    TTbar_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year_str,technique_str))
    ST_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year_str,technique_str))
    WJets_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year_str,technique_str))

    """# Check if histograms exist
    if not sig_hist or not allBR_hist or not QCD_hist or not TTbar_hist or not ST_hist:
        print("ERROR: One or both histograms not found in the file.")
        return"""

    # Create a canvas and pads for upper and lower plots
    c = ROOT.TCanvas("c", "", 1200, 1000)
    pad1 = ROOT.TPad("pad1", "Top pad", 0, 0.30, 1, 1.0)
    pad2 = ROOT.TPad("pad2", "Bottom pad", 0, 0.0, 1, 0.295)
    

    # Adjust margins
    pad1.SetTopMargin(0.1)  # Default is 0.05; increase if needed
    pad1.SetBottomMargin(0.01)  # Space between the top and bottom pad
    pad2.SetTopMargin(0.00)
    pad2.SetBottomMargin(0.4)  # Increase for better spacing in bottom pad

    pad1.Draw()
    pad2.Draw()

    # Draw the stack and h2 on the upper pad
    pad1.cd()
    pad1.SetLogy()


    # Determine which histogram has a larger maximum
    max_value = max( sig_hists[0].GetMaximum(),sig_hists[1].GetMaximum(),sig_hists[2].GetMaximum(), allBR_hist.GetMaximum()   )

    hs.Draw("HIST")
    hs.SetMaximum(1.1*max_value)
    sig_hists[0].Draw("HIST,same")
    sig_hists[1].Draw("HIST,same")
    sig_hists[2].Draw("HIST,same")


    ## not draw ratio plots
    # Draw the ratio on the lower pad
    pad2.cd()
    pad2.SetLogy()
    x_min = 0
    x_max = 0

    hRatios = []
    for iii,sig_hist in enumerate(sig_hists):

        hRatio = sig_hist.Clone("hRatio%s"%iii)
        hRatios.append(hRatio)
        hRatio.Divide( create_sqrt_histogram(allBR_hist))  # Compute the ratio h2 / hStackTotal
        hRatio.SetLineStyle(hist_line_styles[iii])
        hRatio.SetTitle("")
        hRatio.GetYaxis().SetTitle(r"sig / #sqrt{BR}")
        #hRatio.GetYaxis().SetNdivisions(505)
        #hRatio.GetYaxis().SetRangeUser(0.0, 1.5)  # Adjust the y-axis range for clarity
        hRatio.GetYaxis().SetTitleSize(0.1)
        hRatio.GetYaxis().SetTitleOffset(0.4)
        hRatio.GetYaxis().SetLabelSize(0.08)
        hRatio.GetXaxis().SetTitleSize(0.12)
        hRatio.GetXaxis().SetLabelSize(0.1)
        #hRatio.SetFillColor(ROOT.kGray )
        
        if iii < 1: hRatio.Draw("HIST")
        else: hRatio.Draw("HIST, SAME")
        x_min = hRatio.GetXaxis().GetXmin()
        x_max = hRatio.GetXaxis().GetXmax()

    ### create ratio lines at 0.8, 1.0, 1.2
    nom_line = ROOT.TLine(x_min, 1.0, x_max, 1.0)
    nom_line.SetLineStyle(2)  # Dotted line style
    nom_line.Draw("same")

    nom_line_up = ROOT.TLine(x_min, 1.2, x_max, 1.2)
    nom_line_up.SetLineStyle(2)  # Dotted line style
    #nom_line_up.Draw("same")


    nom_line_down = ROOT.TLine(x_min, 0.8, x_max, 0.8)
    nom_line_down.SetLineStyle(2)  # Dotted line style
    #nom_line_down.Draw("same")

    # Add legend
    pad1.cd()

    legend = ROOT.TLegend(0.62, 0.7, 0.9, 0.9)
    legend.SetTextSize(0.02) 
    legend.AddEntry(QCD_hist, "QCD", "f")
    legend.AddEntry(TTbar_hist, "TTbar", "f")
    legend.AddEntry(ST_hist, "ST", "f")
    legend.AddEntry(WJets_hist, "WJets", "f")
    legend.AddEntry(sig_hists[0], r"\mbox{signal } (\mbox{M}_{S_{uu}} = \mbox{ 4 TeV, } \mbox{M}_{\chi} = \mbox{ 1 TeV)}", "l")
    legend.AddEntry(sig_hists[1], r"\mbox{signal } (\mbox{M}_{S_{uu}} = \mbox{ 6 TeV, } \mbox{M}_{\chi} = \mbox{ 2 TeV)}", "l")
    legend.AddEntry(sig_hists[2], r"\mbox{signal } (\mbox{M}_{S_{uu}} = \mbox{ 8 TeV, } \mbox{M}_{\chi} = \mbox{ 3 TeV)}", "l")

    legend.Draw()

    write_cms_text.write_cms_text(CMS_label_xpos=0.132, SIM_label_xpos=0.248,CMS_label_ypos = 0.92, SIM_label_ypos = 0.90, lumistuff_xpos=0.90, lumistuff_ypos=0.91, year = "", uses_data=False)

    # Save the canvas as an image
    output_file = "plots/linearized_sigBR/%s/sig_vs_BR_multi_mass_%s%s_%s.png"%(QCD_type,technique_type,region,year)
    c.SaveAs(output_file)


    # Close the ROOT file
    
    for root_file in root_files:
        root_file.Close()

    del sig_hist
    del allBR_hist
    del c
    del QCD_hist
    del TTbar_hist
    del ST_hist



# plots signal and BR (stacked) with signal sensitity as a function of linerized bin number
def plot_linearized_BR_histogram(year,region,mass_point, technique_type, run_count,QCD_type):

    if run_count > 0: return   #only need to plot this once

    CMS_label_pos = 0.152
    SIM_label_pos = 0.295

    technique_str = "cut-based"
    if "NN" in technique_type:
        technique_str = "NN-based"

    file_name = "finalCombineFilesNewStats/%s/combine_%s%s_%s.root"%(QCD_type,technique_type, year, mass_point)
    
    root_file = ROOT.TFile.Open(file_name)

    if not root_file:
        print("ERROR: file %s not found."%file_name )
        return
    QCD_hist_name = "%s/QCD"%region
    TTbar_hist_name = "%s/TTbar"%region
    ST_hist_name = "%s/ST"%region
    WJets_hist_name = "%s/WJets"%region

    QCD_hist = root_file.Get(QCD_hist_name)
    QCD_hist.SetLineWidth(2)
    QCD_hist.SetMinimum(1e-1)
    TTbar_hist = root_file.Get(TTbar_hist_name)
    TTbar_hist.SetLineWidth(2)
    TTbar_hist.SetMinimum(1e-1)
    WJets_hist = root_file.Get(WJets_hist_name)
    WJets_hist.SetLineWidth(2)
    WJets_hist.SetMinimum(1e-1)
    ST_hist = root_file.Get(ST_hist_name)
    ST_hist.SetLineWidth(2)
    ST_hist.SetMinimum(1e-1)

    # Set colors for each sub-histogram in the stack
    QCD_hist.SetFillColor(ROOT.kRed)
    TTbar_hist.SetFillColor(ROOT.kYellow)
    WJets_hist.SetFillColor(ROOT.kViolet)
    ST_hist.SetFillColor(ROOT.kGreen)

    # Create a THStack and add the sub-histograms
    hs = ROOT.THStack("h_stack", "Linearized Backgrounds (%s) (%s) (%s);linearized bin number; events"%(region,year, technique_str))
    hs.Add(TTbar_hist)
    hs.Add(ST_hist)
    hs.Add(WJets_hist)
    hs.Add(QCD_hist)

    hs.SetMinimum(1e-1)


    QCD_hist.SetTitle("Linearized Backgrounds (%s) (%s) (%s);linearized bin number; events"%(region,year,technique_str))
    TTbar_hist.SetTitle("Linearized Backgrounds (%s) (%s) (%s);linearized bin number; events"%(region,year,technique_str))
    ST_hist.SetTitle("Linearized Backgrounds (%s) (%s) (%s);linearized bin number; events"%(region,year,technique_str))
    WJets_hist.SetTitle("Linearized Backgrounds (%s) (%s) (%s);linearized bin number; events"%(region,year,technique_str))

    # Create a canvas and pads for upper and lower plots
    c = ROOT.TCanvas("c", "", 1200, 1000)

    c.SetLogy()
    hs.Draw("HIST")


    # Add legend
    write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)

    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(QCD_hist, "QCD", "f")
    legend.AddEntry(TTbar_hist, "TTbar", "f")
    legend.AddEntry(WJets_hist, "WJets", "f")
    legend.AddEntry(ST_hist, "ST", "f")

    legend.Draw()

    # Save the canvas as an image
    output_file = "plots/linearized_background/%s/linearized_BR_%s%s_%s.png"%(QCD_type,technique_type,region,year)
    c.SaveAs(output_file)

    output_file = "plots/linearized_background/%s/linearized_QCD_%s%s_%s.png"%(QCD_type,technique_type,region,year)
    QCD_hist.SetLineWidth(4)
    QCD_hist.Draw("HIST")
    c.SaveAs(output_file)

    output_file = "plots/linearized_background/%s/linearized_TTbar_%s%s_%s.png"%(QCD_type,technique_type,region,year)
    TTbar_hist.SetLineWidth(4)
    TTbar_hist.Draw("HIST")
    c.SaveAs(output_file)

    output_file = "plots/linearized_background/%s/linearized_WJets_%s%s_%s.png"%(QCD_type,technique_type,region,year)
    WJets_hist.SetLineWidth(4)
    WJets_hist.Draw("HIST")
    c.SaveAs(output_file)

    output_file = "plots/linearized_background/%s/linearized_ST_%s%s_%s.png"%(QCD_type,technique_type,region,year)
    ST_hist.SetLineWidth(4)
    ST_hist.Draw("HIST")
    c.SaveAs(output_file)

    # Close the ROOT file
    root_file.Close()

    del c
    del QCD_hist
    del TTbar_hist
    del ST_hist

if __name__=="__main__":

    debug = False

    years = ["2015","2016","2017","2018"]
    mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1","Suu5_chi1p5","Suu5_chi2","Suu6_chi1","Suu6_chi1p5","Suu6_chi2","Suu6_chi2p5","Suu7_chi1",
    "Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3","Suu8_chi1","Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"] 
    regions = ["SR","CR","AT0b", "AT1b"]   # "AT1tb", "AT0tb"
    technique_types = ["", "NN_"]

    technique_types = [""]


    QCD_types = ["QCDPT","QCDHT"]

    if debug:
        years = ["2015"]
        mass_points = ["Suu4_chi1",] 
        regions = ["SR"]   # "AT1tb", "AT0tb"
        technique_types = [""]

    for QCD_type in QCD_types:

        for year in years:
            for region in regions:
                for technique_type in technique_types:
                    run_count = 0 

                    plot_linearized_signal_vs_BR_multi_mass(year,region, technique_type,QCD_type) ## only need to run once per year/region/technique

                    for mass_point in mass_points:
                        
                        #try:
                        if "Suu4_chi1" in mass_point:
                            plot_linearized_BR_histogram(year,region,mass_point, technique_type,run_count,QCD_type)  # only need to do this once
                        plot_linearized_signal_vs_BR_histogram(year,region,mass_point, technique_type,QCD_type)
                        run_count+=1
                        #except:
                        #    print("ERROR: failed for %s/%s/%s/%s"%(year,region,mass_point,technique_type))
