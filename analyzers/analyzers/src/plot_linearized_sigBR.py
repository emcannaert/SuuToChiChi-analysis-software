import ROOT
from write_cms_text import write_cms_text

def plot_histograms(year,region,mass_point, technique_type):

    CMS_label_pos = 0.152
    SIM_label_pos = 0.295

    file_name = "/Users/ethan/Documents/rootFiles/finalCombineFiles/combine_%s%s_%s.root"%(technique_type, year, mass_point)
    
    root_file = ROOT.TFile.Open(file_name)

    sig_hist_name   = "%s/sig"
    allBR_hist_name = "%s/allBR"

    # Get the histograms
    sig_hist   = root_file.Get(sig_hist_name)
    sig_hist.SetLineStyle(2)
    sig_hist.SetLineWidth(4)
    allBR_hist = root_file.Get(allBR_hist_name)
    allBR_hist.SetLineColor(kRed)
    allBR_hist.SetLineWidth(4)

    technique_str = "cut-based"
    if "NN" in technique_type:
        technique_str = "NN-based"
    allBR_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s)"%(mass_point,regin,year,technique_str))
    sig_hist.SetTitle("Linearized Background vs Signal (%s) (%s) (%s) (%s)"%(mass_point,regin,year,technique_str))

    # Check if histograms exist
    if not sig_hist or not allBR_hist:
        print("ERROR: One or both histograms not found in the file.")
        return

    # Create a canvas
    canvas = ROOT.TCanvas("canvas", "Histograms", 1200, 1000)

    # Determine which histogram has a larger maximum
    if sig_hist_name.GetMaximum() > allBR_hist.GetMaximum():
        sig_hist_name.Draw("HIST")
        allBR_hist.Draw("HIST,same")
    else:
        allBR_hist.Draw("SAME")
        sig_hist_name.Draw("HIST,same")

    # Add legend

    write_cms_text.write_cms_text(CMS_label_pos, SIM_label_pos)

    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(sig_hist_name, "signal", "l")
    legend.AddEntry(allBR_hist, "combined background", "l")
    legend.Draw()

    # Save the canvas as an image
    output_file = "/Users/ethan/Documents/plots/ANPlots/linearized_sigBR/sig_vs_BR_%s_%s%s_%s.png"%(mass_point,technique_type,region,year)
    canvas.SaveAs(output_file)

    # Close the ROOT file
    root_file.Close()

    del sig_hist
    del allBR_hist
    del canvas


if __name__=="__main__":
    years = ["2015","2016","2017","2018"]
    mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1","Suu5_chi1p5","Suu5_chi2","Suu6_chi1","Suu6_chi1p5","Suu6_chi2","Suu6_chi2p5","Suu7_chi1",
   "Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3","Suu8_chi1","Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"] 
   regions = ["SR","CR","AT0b", "AT1b"]
   technique_types = ["", "NN_"]
   for year in years:
    for region in regions:
        for mass_point in mass_points:
            for technique_type in technique_types:
                plot_histograms(year,region,mass_point, technique_type)