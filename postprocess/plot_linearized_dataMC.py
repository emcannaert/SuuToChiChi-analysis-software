import ROOT

def plot_region( year, region, technique_str):
    # Open the ROOT file

    linearized_root_dir = "finalCombineFilesNewStats/correctedFinalCombineFiles/"
    output_dir          = "plots/dataMC/linearized/"
    technique_title = "cut-based"
    if "NN" in technique_str:     
        linearized_root_dir = "finalCombineFilesNewStats/"
        technique_title = "NN-based"
                ## only need to draw for a single mass point
    file_name = linearized_root_dir + "combine%s_%s_Suu4_chi1.root"%(technique_str,year)
    print("Looking for file %s."%(file_name))
    file = ROOT.TFile.Open(file_name, "READ")

    if not file or file.IsZombie():
        print "Error: Cannot open file {}".format(file_name)
        return

    # Get histograms for QCD, TTbar, ST, and data_obs
    hist_qcd = file.Get("{}/QCD".format(region))
    hist_ttbar = file.Get("{}/TTbar".format(region))
    hist_st = file.Get("{}/ST".format(region))
    hist_data = file.Get("{}/data_obs".format(region))
    
    # Check that all histograms were retrieved
    if not all([hist_qcd, hist_ttbar, hist_st, hist_data]):
        print "Error: One or more histograms are missing in the region '{}'.".format(region)
        print("hist_qcd/hist_ttbar/hist_st/hist_data: %s/%s/%s/%s"%(type(hist_qcd),type(hist_ttbar),type(hist_st),type(hist_data)) )
        return

    # Set fill colors for the histograms
    hist_qcd.SetFillColor(ROOT.kRed)
    hist_ttbar.SetFillColor(ROOT.kYellow)
    hist_st.SetFillColor(ROOT.kGreen)
    
    # Stack the MC histograms
    stack = ROOT.THStack("stack", "data vs combined backgrounds (%s) (%s) (%s)"%(technique_title,region,year))
    stack.Add(hist_qcd)
    stack.Add(hist_ttbar)
    stack.Add(hist_st)

    # Create a canvas with upper and lower pads
    canvas = ROOT.TCanvas("canvas", "Data/MC Comparison", 800, 800)
    canvas.Divide(1, 2)
    pad1 = canvas.cd(1)
    pad1.SetPad(0, 0.35, 1, 1)
    pad1.SetLogy()
    pad1.SetBottomMargin(0.02)  # Reduce bottom margin

    # Draw the stack plot
    stack.Draw("HIST")
    stack.GetXaxis().SetLabelSize(0)  # Hide x-axis labels
    stack.GetYaxis().SetTitle("Events")
    stack.GetYaxis().SetTitleSize(0.05)
    stack.GetYaxis().SetTitleOffset(1.2)

    # Overlay data on top
    hist_data.SetMarkerStyle(20)
    hist_data.SetMarkerSize(0.8)
    hist_data.Draw("SAME PE")

    # Add a legend
    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(hist_qcd, "QCD", "f")
    legend.AddEntry(hist_ttbar, "TTbar", "f")
    legend.AddEntry(hist_st, "ST", "f")
    legend.AddEntry(hist_data, "Data", "pe")
    legend.Draw()

    # Lower pad for data/MC ratio
    pad2 = canvas.cd(2)
    pad2.SetPad(0, 0, 1, 0.35)
    pad2.SetTopMargin(0.02)
    pad2.SetBottomMargin(0.35)
    
    # Calculate data/MC ratio
    hist_mc_total = hist_qcd.Clone("MC_Total")
    hist_mc_total.Add(hist_ttbar)
    hist_mc_total.Add(hist_st)

    hist_ratio = hist_data.Clone("Data_MC_Ratio")
    hist_ratio.Divide(hist_mc_total)

    # Add uncertainty band to ratio plot
    hist_uncertainty = hist_mc_total.Clone("MC_Uncertainty")
    hist_uncertainty.Divide(hist_mc_total)  # Normalize uncertainty to 1
    hist_uncertainty.SetFillColor(ROOT.kGray)
    hist_uncertainty.SetFillStyle(3004)  # Dotted fill style
    hist_uncertainty.SetMarkerStyle(0)  # No markers

    # Draw the ratio plot
    hist_uncertainty.Draw("E2")  # Draw uncertainty band first
    hist_uncertainty.SetMaximum(2.0)
    hist_uncertainty.SetMinimum(0.2)
    hist_ratio.SetMarkerStyle(20)
    hist_ratio.SetMarkerSize(0.8)
    hist_ratio.GetYaxis().SetTitle("Data / MC")
    hist_ratio.GetYaxis().SetNdivisions(505)
    hist_ratio.GetYaxis().SetTitleSize(0.1)
    hist_ratio.GetYaxis().SetTitleOffset(0.5)
    hist_ratio.GetYaxis().SetLabelSize(0.08)
    hist_ratio.GetXaxis().SetTitle(hist_data.GetXaxis().GetTitle())
    hist_ratio.GetXaxis().SetTitleSize(0.1)
    hist_ratio.GetXaxis().SetTitleOffset(1.0)
    hist_ratio.GetXaxis().SetLabelSize(0.08)

    hist_ratio.SetMaximum(2.0)
    hist_ratio.SetMinimum(0.2)
    hist_ratio.Draw("SAME PE")

    # Draw horizontal lines at y=1, 0.8, and 1.2
    line1 = ROOT.TLine(hist_ratio.GetXaxis().GetXmin(), 1, hist_ratio.GetXaxis().GetXmax(), 1)
    line1.SetLineColor(ROOT.kBlack)
    line1.SetLineStyle(2)
    line1.Draw()

    line2 = ROOT.TLine(hist_ratio.GetXaxis().GetXmin(), 0.8, hist_ratio.GetXaxis().GetXmax(), 0.8)
    line2.SetLineColor(ROOT.kRed)
    line2.SetLineStyle(2)
    line2.Draw()

    line3 = ROOT.TLine(hist_ratio.GetXaxis().GetXmin(), 1.2, hist_ratio.GetXaxis().GetXmax(), 1.2)
    line3.SetLineColor(ROOT.kRed)
    line3.SetLineStyle(2)
    line3.Draw()

    # Save the canvas
    canvas.SaveAs(output_dir+ "linearized_dataMC%s_%s_%s.png"%(technique_str,year,region))

    # Clean up
    file.Close()

def plot_region_SRCR( year, regions, hist_type, technique_str):  ## plot SR/CR, AT1b/AT0b, SB1b/SB0b shapes for both data and MC
    ## hist_type will be allBR or data_obs
    _1b_region_name = regions[0]  ## this will be SR/AT1b/SB1b
    _0b_region_name = regions[1]  ## this will be CR/AT0b/SB0b


    ROOT.gStyle.SetOptStat(0)

    #print("_1b_region_name/_0b_region_name: %s/%s"%(_1b_region_name,_0b_region_name))

    # Open the ROOT file
    linearized_root_dir = "finalCombineFilesNewStats/correctedFinalCombineFiles/"
    output_dir          = "plots/SRCR/"
    technique_title = "cut-based"
    if "NN" in technique_str:     
        linearized_root_dir = "finalCombineFilesNewStats/"
        technique_title = "NN-based"
                ## only need to draw for a single mass point
    file_name = linearized_root_dir + "combine%s_%s_Suu4_chi1.root"%(technique_str,year)
    print("Looking for file %s."%(file_name))
    file = ROOT.TFile.Open(file_name, "READ")

    if not file or file.IsZombie():
        print "Error: Cannot open file {}".format(file_name)
        return

    # Get histograms for QCD, TTbar, ST, and data_obs

    hist_1b = file.Get("%s/%s"%(_1b_region_name,hist_type))
    hist_0b = file.Get("%s/%s"%(_0b_region_name,hist_type))
    
    # Check that all histograms were retrieved
    if not all([hist_1b, hist_0b]):
        print "Error: One or more histograms are missing in the region '{}'.".format(region)
        print("hist_1b/hist_0b: %s/%s"%(type(hist_1b),type(hist_0b)) )
        return

    # normalize histograms
    hist_1b.Scale(1.0/hist_1b.Integral())
    hist_0b.Scale(1.0/hist_0b.Integral())
    
    # Set fill colors for the histograms
    hist_1b.SetLineColor(ROOT.kBlue)
    hist_0b.SetLineColor(ROOT.kRed)

    hist_type_str = "combined MC backgrounds"
    if hist_type == "data_obs": hist_type_str = "data"
    hist_1b.SetTitle("%s vs %s (normalized) shape comparison for %s (%s) (%s) "%(_1b_region_name, _0b_region_name, hist_type_str, year, technique_title ))

    # Create a canvas with upper and lower pads
    canvas = ROOT.TCanvas("canvas", "shape comparisons", 800, 800)
    canvas.Divide(1, 2)
    pad1 = canvas.cd(1)
    pad1.SetPad(0, 0.35, 1, 1)
    pad1.SetLogy()
    pad1.SetBottomMargin(0.02)  # Reduce bottom margin

    hist_1b.SetStats(0)
    # Draw the stack plot
    hist_1b.Draw("HIST")
    hist_1b.GetXaxis().SetLabelSize(0)  # Hide x-axis labels
    hist_1b.GetYaxis().SetTitle("Events")
    hist_1b.GetYaxis().SetTitleSize(0.05)
    hist_1b.GetYaxis().SetTitleOffset(1.2)

    # Overlay data on top
    hist_0b.SetMarkerStyle(20)
    hist_0b.SetMarkerSize(0.8)
    hist_0b.Draw("SAME,HIST")

    # Add a legend
    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(hist_1b, _1b_region_name, "l")
    legend.AddEntry(hist_0b, _0b_region_name, "l")
    legend.Draw()

    # Lower pad for data/MC ratio
    pad2 = canvas.cd(2)
    pad2.SetPad(0, 0, 1, 0.35)
    pad2.SetTopMargin(0.02)
    pad2.SetBottomMargin(0.35)
    
    # Calculate data/MC ratio

    hist_ratio = hist_1b.Clone("Data_MC_Ratio")
    hist_ratio.SetTitle("")
    hist_ratio.SetStats(0)
    hist_ratio.SetTitle("")
    hist_ratio.Divide(hist_0b)

    hist_ratio.SetMarkerStyle(20)
    hist_ratio.SetMarkerSize(0.8)
    hist_ratio.GetYaxis().SetTitle("%s / %s"%(_1b_region_name,_0b_region_name))
    hist_ratio.GetYaxis().SetNdivisions(505)
    hist_ratio.GetYaxis().SetTitleSize(0.1)
    hist_ratio.GetYaxis().SetTitleOffset(0.5)
    hist_ratio.GetYaxis().SetLabelSize(0.08)
    hist_ratio.GetXaxis().SetTitle(hist_1b.GetXaxis().GetTitle())
    hist_ratio.GetXaxis().SetTitleSize(0.1)
    hist_ratio.GetXaxis().SetTitleOffset(1.0)
    hist_ratio.GetXaxis().SetLabelSize(0.08)

    hist_ratio.SetMaximum(2.0)
    hist_ratio.SetMinimum(0.2)
    hist_ratio.SetFillColor(ROOT.kGray)
    hist_ratio.Draw("E2")

    # Draw horizontal lines at y=1, 0.8, and 1.2
    line1 = ROOT.TLine(hist_ratio.GetXaxis().GetXmin(), 1, hist_ratio.GetXaxis().GetXmax(), 1)
    line1.SetLineColor(ROOT.kBlack)
    line1.SetLineStyle(2)
    line1.Draw()

    line2 = ROOT.TLine(hist_ratio.GetXaxis().GetXmin(), 0.8, hist_ratio.GetXaxis().GetXmax(), 0.8)
    line2.SetLineColor(ROOT.kRed)
    line2.SetLineStyle(2)
    line2.Draw()

    line3 = ROOT.TLine(hist_ratio.GetXaxis().GetXmin(), 1.2, hist_ratio.GetXaxis().GetXmax(), 1.2)
    line3.SetLineColor(ROOT.kRed)
    line3.SetLineStyle(2)
    line3.Draw()

    # Save the canvas
    regions_str = "SRCR"
    if "AT" in _1b_region_name: regions_str = "AT"
    elif "SB" in _1b_region_name: regions_str = "SB"

    canvas.SaveAs(output_dir+ "linearized_%s_%s_shape%s_%s.png"%(regions_str,hist_type,technique_str,year))

    # Clean up
    file.Close()

if __name__=="__main__":
    years = ["2015","2016","2017","2018"]
    regions = ["SR","CR","AT1b","AT0b","SB1b","SB0b"]
    technique_strs = ["","_NN"]

    print("------ Creating linearized data/MC plots ")
    for year in years:
        for region in regions:
            for technique_str in technique_strs:
                # Example usage
                if technique_str == "_NN" and "SB" in region: continue
                print("Running for year/region/technique: %s/%s/%s"%(year,region,technique_str))
                plot_region(year,region, technique_str)

    regions_tuples = [ ("SR","CR"), ("AT1b","AT0b"), ("SB1b","SB0b") ]
    print("------ Creating linearized SRCR plots ")
    hist_types = ["allBR","data_obs"]
    for year in years:
        for regions_tuple in regions_tuples:
            for technique_str in technique_strs:
                if technique_str == "_NN" and "SB" in regions_tuple[0]: continue
                for hist_type in hist_types:
                    print("Running for year/regions/technique: %s/%s/%s"%(year,regions_tuple,technique_str))
                    plot_region_SRCR( year, regions_tuple, hist_type, technique_str)





