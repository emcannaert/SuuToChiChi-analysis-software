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
def plot_linearized_signal_vs_BR_histogram(year,region,mass_point, technique_type):

    CMS_label_pos = 0.152
    SIM_label_pos = 0.255

    technique_str = "cut-based"
    if "NN" in technique_type:
        technique_str = "NN-based"

    file_name = "finalCombineFiles/combine_%s%s_%s.root"%(technique_type, year, mass_point)
    
    root_file = ROOT.TFile.Open(file_name)
    if not root_file:
        print("ERROR: couldn't find file %s"%file_name)
        return
    sig_hist_name   = "%s/sig"%region
    allBR_hist_name = "%s/allBR"%region

    QCD_hist_name = "%s/QCD"%region
    TTbar_hist_name = "%s/TTbar"%region
    ST_hist_name = "%s/ST"%region


    # Get the histograms
    sig_hist   = root_file.Get(sig_hist_name)
    sig_hist.SetLineStyle(2)
    sig_hist.SetLineWidth(4)
    sig_hist.SetLineColor(ROOT.kBlack)
    allBR_hist = root_file.Get(allBR_hist_name)
    #allBR_hist.SetLineColor(ROOT.kRed)
    allBR_hist.SetLineWidth(2)

    QCD_hist = root_file.Get(QCD_hist_name)
    QCD_hist.SetLineWidth(2)
    TTbar_hist = root_file.Get(TTbar_hist_name)
    TTbar_hist.SetLineWidth(2)
    ST_hist = root_file.Get(ST_hist_name)
    ST_hist.SetLineWidth(2)

    QCD_hist.SetLineColor(ROOT.kBlack)
    TTbar_hist.SetLineColor(ROOT.kBlack)
    ST_hist.SetLineColor(ROOT.kBlack)

    # Set colors for each sub-histogram in the stack
    QCD_hist.SetFillColor(ROOT.kRed)
    TTbar_hist.SetFillColor(ROOT.kYellow)
    ST_hist.SetFillColor(ROOT.kGreen)

    # Create a THStack and add the sub-histograms
    hs = ROOT.THStack("h_stack", "Linearized Background vs Signal (%s) (%s) (%s) (%s)"%(mass_point, region,year, technique_str))
    hs.Add(TTbar_hist)
    hs.Add(ST_hist)
    hs.Add(QCD_hist)

    allBR_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year,technique_str))
    sig_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year,technique_str))

    QCD_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year,technique_str))
    TTbar_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year,technique_str))
    ST_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s);linearized bin number; events"%(mass_point,region,year,technique_str))

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

    #sig_hist.GetXaxis().SetLabelSize(0)
    #QCD_hist.GetXaxis().SetLabelSize(0)
    #TTbar_hist.GetXaxis().SetLabelSize(0)
    #ST_hist.GetXaxis().SetLabelSize(0)

    # Determine which histogram has a larger maximum
    if sig_hist.GetMaximum() > allBR_hist.GetMaximum():
        sig_hist.Draw("HIST")
        hs.Draw("HIST,same")
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
    legend.AddEntry(sig_hist, "signal", "l")
    legend.Draw()

    write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)



    # Save the canvas as an image
    output_file = "plots/linearized_sigBR/sig_vs_BR_%s_%s%s_%s.png"%(mass_point,technique_type,region,year)
    c.SaveAs(output_file)

    # Close the ROOT file
    root_file.Close()

    del sig_hist
    del allBR_hist
    del c
    del QCD_hist
    del TTbar_hist
    del ST_hist


# plots signal and BR (stacked) with signal sensitity as a function of linerized bin number
def plot_linearized_BR_histogram(year,region,mass_point, technique_type, run_count):

    if run_count > 0: return   #only need to plot this once

    CMS_label_pos = 0.152
    SIM_label_pos = 0.295

    technique_str = "cut-based"
    if "NN" in technique_type:
        technique_str = "NN-based"

    file_name = "finalCombineFiles/combine_%s%s_%s.root"%(technique_type, year, mass_point)
    
    root_file = ROOT.TFile.Open(file_name)

    if not root_file:
        print("ERROR: file %s not found."%file_name )
        return
    QCD_hist_name = "%s/QCD"%region
    TTbar_hist_name = "%s/TTbar"%region
    ST_hist_name = "%s/ST"%region


    QCD_hist = root_file.Get(QCD_hist_name)
    QCD_hist.SetLineWidth(2)
    TTbar_hist = root_file.Get(TTbar_hist_name)
    TTbar_hist.SetLineWidth(2)
    ST_hist = root_file.Get(ST_hist_name)
    ST_hist.SetLineWidth(2)

    # Set colors for each sub-histogram in the stack
    QCD_hist.SetFillColor(ROOT.kRed)
    TTbar_hist.SetFillColor(ROOT.kYellow)
    ST_hist.SetFillColor(ROOT.kGreen)

    # Create a THStack and add the sub-histograms
    hs = ROOT.THStack("h_stack", "Linearized Backgrounds (%s) (%s) (%s);linearized bin number; events"%(region,year, technique_str))
    hs.Add(TTbar_hist)
    hs.Add(ST_hist)
    hs.Add(QCD_hist)

    QCD_hist.SetTitle("Linearized Backgrounds (%s) (%s) (%s);linearized bin number; events"%(region,year,technique_str))
    TTbar_hist.SetTitle("Linearized Backgrounds (%s) (%s) (%s);linearized bin number; events"%(region,year,technique_str))
    ST_hist.SetTitle("Linearized Backgrounds (%s) (%s) (%s);linearized bin number; events"%(region,year,technique_str))

    # Create a canvas and pads for upper and lower plots
    c = ROOT.TCanvas("c", "", 1200, 1000)

    c.SetLogy()
    hs.Draw("HIST")


    # Add legend
    write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)

    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(QCD_hist, "QCD", "f")
    legend.AddEntry(TTbar_hist, "TTbar", "f")
    legend.AddEntry(ST_hist, "ST", "f")

    legend.Draw()

    # Save the canvas as an image
    output_file = "plots/linearized_background/linearized_BR_%s%s_%s.png"%(technique_type,region,year)
    c.SaveAs(output_file)

    # Close the ROOT file
    root_file.Close()

    del c
    del QCD_hist
    del TTbar_hist
    del ST_hist

if __name__=="__main__":
    years = ["2015","2016","2017","2018"]
    mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1","Suu5_chi1p5","Suu5_chi2","Suu6_chi1","Suu6_chi1p5","Suu6_chi2","Suu6_chi2p5","Suu7_chi1",
    "Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3","Suu8_chi1","Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"] 
    regions = ["SR","CR","AT0b", "AT1b"]
    technique_types = ["", "NN_"]

    for year in years:
        for region in regions:
            for technique_type in technique_types:
                run_count = 0 
                for mass_point in mass_points:
                    
                    #try:
                    plot_linearized_BR_histogram(year,region,mass_point, technique_type,run_count)
                    plot_linearized_signal_vs_BR_histogram(year,region,mass_point, technique_type)
                    run_count+=1
                    #except:
                    #    print("ERROR: failed for %s/%s/%s/%s"%(year,region,mass_point,technique_type))
