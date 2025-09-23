import ROOT

def process_and_plot_histograms(year, working_point, sample):

    inFile_dir = '../combinedROOT/processedFiles/'
    output_dir = 'plots/btag_studies/tagging_vs_pt/'
    hist_folder = "nom/"

    ST_t_channel_top_5f_SF      = {'2015':0.0409963154,  '2016':0.03607115071, '2017':0.03494669125, '2018': 0.03859114659 }
    ST_t_channel_antitop_5f_SF  = {'2015':0.05673857623, '2016':0.04102705994, '2017':0.04238814865, '2018': 0.03606630944 }
    ST_s_channel_4f_hadrons_SF  = {'2015':0.04668187234, '2016':0.03564988679, '2017':0.03985938616, '2018': 0.04102795437 }
    ST_s_channel_4f_leptons_SF  = {'2015':0.01323030083, '2016':0.01149139097, '2017':0.01117527734, '2018': 0.01155448784 }
    ST_tW_antitop_5f_SF         = {'2015':0.2967888696,  '2016':0.2301666797,  '2017':0.2556495594,  '2018': 0.2700032391  }
    ST_tW_top_5f_SF             = {'2015':0.2962796522,  '2016':0.2355829386,  '2017':0.2563403788,  '2018': 0.2625270613  }

    SF_TTJetsMCHT1200to2500 = {"2015":0.002722324842,"2016":0.002255554525,"2017":0.00267594799,"2018":0.003918532089}
    SF_TTJetsMCHT2500toInf = {"2015":0.000056798633,"2016":0.000050253843,"2017":0.00005947217,"2018":0.000084089656}   

    SF_1000to1500 = {'2015': 1.578683216 ,   '2016':1.482632755 ,  '2017': 3.126481451,  '2018': 4.289571744   }
    SF_1500to2000 = {'2015': 0.2119142341,   '2016':0.195224041 ,  '2017': 0.3197450474, '2018': 0.4947703875  }
    SF_2000toInf  = {'2015': 0.08568186031 , '2016':0.07572795371, '2017': 0.14306915,   '2018': 0.2132134533  }


    if sample == "QCD":
        filenames = [ inFile_dir+ "QCDMC1000to1500"+ "_" + year + "_processed.root",  inFile_dir+"QCDMC1500to2000"+ "_" + year + "_processed.root", inFile_dir+"QCDMC2000toInf"+ "_" + year + "_processed.root"]
        #scale_factors = [ SF_1000to1500[year], SF_1500to2000[year],SF_2000toInf[year]] 
        scale_factors = [ 1.0,1.0,1.0] 
    elif sample == "TTbar":
        filenames = [ inFile_dir+"TTJetsMCHT1200to2500"+ "_" + year + "_processed.root", inFile_dir+"TTJetsMCHT2500toInf"+ "_" + year + "_processed.root"]
        #scale_factors = [  SF_TTJetsMCHT1200to2500[year] ,SF_TTJetsMCHT2500toInf[year]] 
        scale_factors = [  1.0,1.0] 
    elif sample == "ST":
        filenames = [ inFile_dir+"ST_t-channel-top_inclMC"+ "_" + year + "_processed.root", inFile_dir+"ST_t-channel-antitop_inclMC"+ "_" + year + "_processed.root", inFile_dir+"ST_s-channel-hadronsMC"+ "_" + year + "_processed.root", inFile_dir+"ST_s-channel-leptonsMC"+ "_" + year + "_processed.root", inFile_dir+"ST_tW-antiTop_inclMC"+ "_" + year + "_processed.root",inFile_dir+"ST_tW-top_inclMC"+ "_" + year + "_processed.root"]
        #scale_factors = [ ST_t_channel_top_5f_SF[year], ST_t_channel_antitop_5f_SF[year], ST_s_channel_4f_hadrons_SF[year],  ST_s_channel_4f_leptons_SF[year], ST_tW_antitop_5f_SF[year] ,  ST_tW_top_5f_SF[year] ] 
        scale_factors = [1.0,1.0,1.0,1.0,1.0,1.0] 

    else:
        print("ERROR: incorrect sample.")
        return



    nBtagged_true_b_hist_name     = "h_trueb_jets_%s_b_tagged_by_pt"%working_point
    nBtagged_true_c_hist_name     = "h_truec_jets_%s_b_tagged_by_pt"%working_point
    nBtagged_true_light_hist_name = "h_trueLight_jets_%s_b_tagged_by_pt"%working_point

    nTrue_b_hist_name     = "h_trueb_jets_by_pt"
    nTrue_c_hist_name     = "h_truec_jets_by_pt"
    nTrue_light_hist_name = "h_trueLight_jets_by_pt"

    # Initialize pointers to summed histograms
    sum_nBtagged_true_b_hist     = None
    sum_nBtagged_true_c_hist     = None
    sum_nBtagged_true_light_hist = None
    sum_nTrue_b_hist             = None
    sum_nTrue_c_hist             = None
    sum_nTrue_light_hist         = None


    # Loop over the 11 ROOT files
    for i, fname in enumerate(filenames):
        # Open the ROOT file
        f = ROOT.TFile.Open(fname, "READ")
        
        # Retrieve the two histograms
        nBtagged_true_b_hist = f.Get(hist_folder+nBtagged_true_b_hist_name)
        nBtagged_true_c_hist = f.Get(hist_folder+nBtagged_true_c_hist_name)
        nBtagged_true_light_hist = f.Get(hist_folder+nBtagged_true_light_hist_name)

        nTrue_b_hist = f.Get(hist_folder+nTrue_b_hist_name)
        nTrue_c_hist = f.Get(hist_folder+nTrue_c_hist_name)
        nTrue_light_hist = f.Get(hist_folder+nTrue_light_hist_name)

        try:

            # Add histograms together 
            #(1)
            if sum_nBtagged_true_b_hist is None:
                sum_nBtagged_true_b_hist = nBtagged_true_b_hist.Clone("sum_nBtagged_true_b_hist")
                sum_nBtagged_true_b_hist.SetDirectory(0)  # Keep the histogram even after file is closed
            else:
                sum_nBtagged_true_b_hist.Add(nBtagged_true_b_hist)
        except:
            print("ERROR: failed to find hist %s (%s/%s/%s) in %s"%(hist_folder+nBtagged_true_b_hist_name,year, working_point, sample, fname))
        try:
            #(2)
            if sum_nBtagged_true_c_hist is None:
                sum_nBtagged_true_c_hist = nBtagged_true_c_hist.Clone("sum_nBtagged_true_c_hist")
                sum_nBtagged_true_c_hist.SetDirectory(0)  # Keep the histogram even after file is closed
            else:
                sum_nBtagged_true_c_hist.Add(nBtagged_true_c_hist)
        except:
            print("ERROR: failed to find hist %s (%s/%s/%s) in %s"%(hist_folder+nBtagged_true_c_hist_name,year, working_point, sample, fname))
        try:
            #(3)
            if sum_nBtagged_true_light_hist is None:
                sum_nBtagged_true_light_hist = nBtagged_true_light_hist.Clone("sum_nBtagged_true_light_hist")
                sum_nBtagged_true_light_hist.SetDirectory(0)  # Keep the histogram even after file is closed
            else:
                sum_nBtagged_true_light_hist.Add(nBtagged_true_light_hist)
        except:
            print("ERROR: failed to find hist %s (%s/%s/%s) in %s"%(hist_folder+nBtagged_true_light_hist_name,year, working_point, sample, fname))
        try:
            #(4)
            if sum_nTrue_b_hist is None:
                sum_nTrue_b_hist = nTrue_b_hist.Clone("sum_nTrue_b_hist")
                sum_nTrue_b_hist.SetDirectory(0)  # Keep the histogram even after file is closed
            else:
                sum_nTrue_b_hist.Add(nTrue_b_hist)
        except:
            print("ERROR: failed to find hist %s (%s/%s/%s) in %s"%(hist_folder+nTrue_b_hist_name,year, working_point, sample, fname))
        try:
            #(5)
            if sum_nTrue_c_hist is None:
                sum_nTrue_c_hist = nTrue_c_hist.Clone("sum_nTrue_c_hist")
                sum_nTrue_c_hist.SetDirectory(0)  # Keep the histogram even after file is closed
            else:
                sum_nTrue_c_hist.Add(nTrue_c_hist)
        except:
            print("ERROR: failed to find hist %s (%s/%s/%s) in %s"%(hist_folder+nTrue_c_hist_name,year, working_point, sample, fname))
        try:
            #(6)
            if sum_nTrue_light_hist is None:
                sum_nTrue_light_hist = nTrue_light_hist.Clone("sum_nTrue_light_hist")
                sum_nTrue_light_hist.SetDirectory(0)  # Keep the histogram even after file is closed
            else:
                sum_nTrue_light_hist.Add(nTrue_light_hist)
        except:
            print("ERROR: failed to find hist %s (%s/%s/%s) in %s"%(hist_folder+nTrue_light_hist_name,year, working_point, sample, fname))
        # Close the ROOT file
        f.Close()

    # Now, divide the two summed histograms
    true_b_rate_vs_pt = sum_nBtagged_true_b_hist.Clone("true_b_rate_vs_pt")
    true_b_rate_vs_pt.Divide(sum_nTrue_b_hist)

    true_c_rate_vs_pt = sum_nBtagged_true_c_hist.Clone("true_c_rate_vs_pt")
    true_c_rate_vs_pt.Divide(sum_nTrue_c_hist)

    true_light_rate_vs_pt = sum_nBtagged_true_light_hist.Clone("true_light_rate_vs_pt")
    true_light_rate_vs_pt.Divide(sum_nTrue_light_hist)


    # Create a canvas to plot the histogram
    c = ROOT.TCanvas("c", "c", 1200, 1000)
    true_b_rate_vs_pt.SetTitle("Number of true b jets (|partonFlavour| == 5) b-tagged / total true b jets (%s WP) (%s) (%s)"%(working_point,sample, year))
    true_b_rate_vs_pt.GetXaxis().SetTitle("jet p_{T} [GeV]")
    true_b_rate_vs_pt.GetYaxis().SetTitle("Number of tagged jets / total jets")
    
    true_c_rate_vs_pt.SetTitle("Number of true c jets (|partonFlavour| == 4) b-tagged / total true c jets (%s WP) (%s) (%s)"%(working_point,sample, year))
    true_c_rate_vs_pt.GetXaxis().SetTitle("jet p_{T} [GeV]")
    true_c_rate_vs_pt.GetYaxis().SetTitle("Number of tagged jets / total jets")
    
    true_light_rate_vs_pt.SetTitle("Number of true light jets (|partonFlavour| < 4) b-tagged / total true light jets (%s WP) (%s) (%s)"%(working_point,sample, year))
    true_light_rate_vs_pt.GetXaxis().SetTitle("jet p_{T} [GeV]")
    true_light_rate_vs_pt.GetYaxis().SetTitle("Number of tagged jets / total jets")
    
    # Draw the result
    true_b_rate_vs_pt.Draw("HIST")
    c.SaveAs( output_dir + "%s_trueb_btag_rate_vs_pt_%s_%s.png"%(sample, working_point, year) )
    true_c_rate_vs_pt.Draw("HIST")
    c.SaveAs( output_dir + "%s_truec_btag_rate_vs_pt_%s_%s.png"%(sample, working_point, year) )
    true_light_rate_vs_pt.Draw("HIST")
    c.SaveAs( output_dir + "%s_trueLight_btag_rate_vs_pt_%s_%s.png"%(sample, working_point, year) )



if __name__=="__main__":

    years = ["2015","2016","2017","2018"]
    working_points = ["med", "tight"]
    samples =  ["QCD","TTbar","ST"]
    for year in years:
        # Call the function
        for working_point in working_points:
            for sample in samples:
                process_and_plot_histograms(year,working_point,sample)