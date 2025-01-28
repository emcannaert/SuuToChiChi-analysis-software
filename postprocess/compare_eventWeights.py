import ROOT

## this script creates comparisons of the systematic event weights between years as well as comparisons between regions for individual years


canvas = ROOT.TCanvas("canvas", "Histograms", 1200, 1000)
canvas.SetLogy() 

def plot_nom_weight_comparisons_by_sample(hist_name, sample_type):
    years = [2015, 2016, 2017, 2018]
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen + 2, ROOT.kOrange]
    
    canvas.Clear()  # Clear the canvas
    legend = ROOT.TLegend(0.6, 0.6, 0.8, 0.8)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    ROOT.gStyle.SetOptStat(0)  # Disable stats box

    max_y_value = -99999

    for i, year in enumerate(years):
        file_name = "../combinedROOT/processedFiles/{}_{}_processed.root".format(sample_type, year)
        file = ROOT.TFile.Open(file_name, "READ")
        if not file or file.IsZombie():
            print("Error: Could not open {}".format(file_name))
            continue

        hist = file.Get("nom/" + hist_name)
        if not hist or hist.IsZombie():
            print("Error: Histogram {} not found in {}".format(hist_name, file_name))
            continue

        hist.SetDirectory(0)  # Detach from file
        file.Close()  # Close file after detaching histograms
        hist.SetLineWidth(2)  # Detach from file

        if hist.Integral() > 0:
            hist.Scale(1.0 / hist.Integral())
        hist.SetLineColor(colors[i])

        #if hist.GetMaximum() > max_y_value :  max_y_value = hist.GetMaximum()

        max_y_value = hist.SetMaximum(1.5)

        legend.AddEntry(hist, str(year), "l")
        draw_option = "HIST" if i == 0 else "HIST SAME"
        hist.Draw(draw_option)

    legend.Draw()
    canvas.Update()

    # Save the canvas
    output_name = "plots/nom_systematic_comparisons/years_by_sample/{}_{}_comparison.png".format(sample_type, hist_name)
    canvas.SaveAs(output_name)







def plot_nom_weight_comparisons_by_sample_and_region(hist_name, sample_type,year):
    regions = ["SR","CR","AT1b","AT0b"]
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen + 2, ROOT.kOrange]
    
    canvas.Clear()  # Clear the canvas
    legend = ROOT.TLegend(0.6, 0.6, 0.8, 0.8)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    ROOT.gStyle.SetOptStat(0)  # Disable stats box

    max_y_value = -99999

    for i, region in enumerate(regions):
        file_name = "../combinedROOT/processedFiles/{}_{}_processed.root".format(sample_type, year)
        file = ROOT.TFile.Open(file_name, "READ")
        if not file or file.IsZombie():
            print("Error: Could not open {}".format(file_name))
            continue

        hist = file.Get("nom/" + hist_name+ "_%s"%(region))
        if not hist or hist.IsZombie():
            print("Error: Histogram {} not found in {}".format(hist_name, file_name))
            continue

        hist.SetDirectory(0)  # Detach from file
        file.Close()  # Close file after detaching histograms
        hist.SetLineWidth(2)  # Detach from file

        if hist.Integral() > 0:
            hist.Scale(1.0 / hist.Integral())
        hist.SetLineColor(colors[i])

        #if hist.GetMaximum() > max_y_value :  max_y_value = hist.GetMaximum()

        max_y_value = hist.SetMaximum(1.5)

        legend.AddEntry(hist, region, "l")
        draw_option = "HIST" if i == 0 else "HIST SAME"
        hist.Draw(draw_option)

    legend.Draw()
    canvas.Update()

    # Save the canvas
    output_name = "plots/nom_systematic_comparisons/regions_by_sample_and_year/{}_{}_{}_comparison.png".format(sample_type, hist_name,year)
    canvas.SaveAs(output_name)



if __name__=="__main__":

    systematics = [ 
        #"h_pdf_EventWeight",
        #"h_renorm_EventWeight",
        #"h_factor_EventWeight",
        #"h_scale_EventWeight",
        "h_PU_eventWeight",
        #"h_bTag_eventWeight_T",
        "h_bTag_eventWeight_M",
        "h_L1PrefiringWeight"    ]


    #systematic_folders = [  "PUSF", "nom" ]   # "pdf", "renorm", "fact", "scale",

    #systematic_sufices = ["up", "down"]

    samples     = [ "QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTJetsMCHT800to1200", "TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf",
    "TTToHadronicMC","TTToSemiLeptonicMC" , "TTToLeptonicMC", "WJetsMC_LNu-HT1200to2500",  "WJetsMC_LNu-HT2500toInf", "WJetsMC_QQ-HT800toInf"   ]  
    ### LESS IMPORTANT BACKGROUNDS
    ###  "ST_t-channel-top_inclMC","ST_t-channel-antitop_inclMC","ST_s-channel-hadronsMC","ST_s-channel-leptonsMC", "ST_tW-antiTop_inclMC","ST_tW-top_inclMC",  "WJetsMC_LNu-HT800to1200",

    for sample in samples:
        for systematic in systematics:
            print("Running for systematic %s and sample type %s"%(systematic, sample ))
            plot_nom_weight_comparisons_by_sample(systematic, sample)

    years = ["2015","2016","2017","2018"]

    for year in years:
        for sample in samples:
            for systematic in systematics:
                plot_nom_weight_comparisons_by_sample_and_region(systematic, sample,year)


