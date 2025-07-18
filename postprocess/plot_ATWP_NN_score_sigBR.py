import ROOT
import os
from return_BR_SF.return_BR_SF import return_BR_SF
from return_signal_SF.return_signal_SF import return_signal_SF
from write_cms_text import write_cms_text
import numpy as np
ROOT.gROOT.SetBatch(True)


SIGBR_CUTOFF = 0.70







working_points = ["05","10","12","15","17","20"]

years = ["2015", "2016", "2017", "2018"]
regions = ["0b"] #"AT1b","AT0b", CR
_hist_name =  "h_BEST_score_TSJ"


#_hist_name =  "h_BEST_score_ATSJ"
#regions = ["AT1b","AT0b"] #


#regions = ["ADT0b","ADT1b"] #"AT1b","AT0b"
#_hist_name =  "h_BEST_score_ATSJ"



"""
h_BEST_score_ATSJ
h_BEST_score

"""

    

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
"QCDMC1000to1500",
 "QCDMC1500to2000",
"QCDMC2000toInf"] 



def validate_thstack(thstack):
    # Check all histograms in the stack - make sure none are null or zombie
    for i in range(thstack.GetNhists()):
        hist = thstack.GetHists()[i]
        if not hist:
            print("Histogram %d in THStack is None!" % i)
            return False
    return True



def create_sqrt_hist(original_hist, setErrors=False, setTitle=True):
    # Create a new histogram with the same binning as the original
    sqrt_hist = original_hist.Clone("sqrt_hist")
    if setTitle: sqrt_hist.SetTitle("Square Root of Original Histogram")
    sqrt_hist.SetDirectory(0)
    # Loop over bins and set each bin content to sqrt of the original bin content
    for bin_idx in range(1, original_hist.GetNbinsX() + 1):
        original_content = original_hist.GetBinContent(bin_idx)
        if abs(original_content) > 1e-9:
            orig_sign = original_content / abs(original_content) 
        else: 
            orig_sign = 0

        #print("sqrt hist: bin %s --- original yield is %s, sign is %s for hist %s."%(bin_idx,original_content,orig_sign,original_hist.GetName()))        

        sqrt_content = orig_sign*ROOT.TMath.Sqrt(abs(original_content))
        sqrt_hist.SetBinContent(bin_idx, sqrt_content)

        if setErrors: sqrt_hist.SetBinError(bin_idx, original_hist.GetBinError(bin_idx))  # Set errors to zero if needed
        else: sqrt_hist.SetBinError(bin_idx, 0)  # Set errors to zero if needed

    return sqrt_hist


def create_squared_hist(original_hist):
    squared_Hist = original_hist.Clone("squared_Hist")
    squared_Hist.SetDirectory(0)
    for bin_idx in range(1, original_hist.GetNbinsX() + 1):
        original_content = original_hist.GetBinContent(bin_idx)
        if abs(original_content) > 1e-9:
            orig_sign = original_content / abs(original_content) 
        else: 
            orig_sign = 0
        #print("squared hist: bin %s --- original yield is %s, sign is %s for hist %s."%(bin_idx,original_content,orig_sign,original_hist.GetName()))        
        sq_content = orig_sign*pow(original_content,2)
        squared_Hist.SetBinContent(bin_idx, sq_content)
        squared_Hist.SetBinError(  bin_idx, original_hist.GetBinError(bin_idx))  # Set errors to zero if needed

    return squared_Hist



def get_uncert_bands(year, region, WP, BR_samples, N_bins):
    # returns +- total uncertainty hists for combined BRs

    systematics = ["bTagSF_med",  "JER", "JEC", "PUSF", "pdf", "scale"]   
 
    total_vars_up = ROOT.TH1F("sys_vars_up","total up systematic variations",N_bins,0,1.0)
    total_vars_down = ROOT.TH1F("sys_vars_down","total down systematic variations",N_bins,0,1.0)

    total_vars_up.SetDirectory(0)
    total_vars_down.SetDirectory(0)

    tot_up_vars   = np.zeros((16,N_bins)) # first index is the number of BR samples, second is the number of bins
    tot_down_vars = np.zeros((16,N_bins)) 

    for systematic in systematics:

        tot_BR_up   = None
        tot_BR_down = None
        tot_BR_nom = None

        for iii,sample in enumerate(BR_samples):

            ## get histogram
            if region in ["ADT0b","ADT1b"]: 
                file_name = sample + "_" + year + "_WP0p" + wp + "_processed.root"
            else:
                file_name = sample + "_" + year + "_ATWP0p" + wp + "_processed.root"
            file_path = os.path.join(wp_dir, file_name)

            if not os.path.exists(file_path):
                print "  WARNING: File not found:", file_path
                continue

            f = ROOT.TFile.Open(file_path)
            if not f or f.IsZombie():
                print "  ERROR: Could not open:", file_path
                continue

            hist_nom = f.Get("nom/" + hist_name)
            hist_up = f.Get("%s_up/"%systematic + hist_name)
            hist_down = f.Get("%s_down/"%systematic + hist_name)


            if ("ST_" in sample or "TTTo" in sample ) and systematic in ["pdf", "scale"]: 
                hist_up = hist_nom
                hist_down = hist_nom


            if not hist_nom:
                print "  ERROR: Histogram not found:", "nom/" + hist_name, "in", file_path
                f.Close()
                continue
            if not hist_up:
                print "  ERROR: Histogram not found:", "%s_up/"%systematic + hist_name, "in", file_path
                f.Close()
                continue
            if not hist_down:
                print "  ERROR: Histogram not found:", "%s_down/"%systematic + hist_name, "in", file_path
                f.Close()
                continue


            if tot_BR_nom is None:
                tot_BR_up   = hist_up.Clone("hist_up")
                tot_BR_nom  = hist_nom.Clone("hist_nom")
                tot_BR_down = hist_down.Clone("hist_down")

                tot_BR_up.SetDirectory(0)
                tot_BR_down.SetDirectory(0)
                tot_BR_nom.SetDirectory(0)


            else:
                tot_BR_up.Add(hist_up)
                tot_BR_nom.Add(hist_nom)
                tot_BR_down.Add(hist_down)

        tot_BR_up.Add(tot_BR_nom,-1)
        tot_BR_up.Divide(tot_BR_nom)

        tot_BR_down.Add(tot_BR_nom,-1)
        tot_BR_down.Divide(tot_BR_nom)

        #tot_BR_up.Add(ones_hist)
        #tot_BR_down.Add(ones_hist)


        """for iii in range(1,total_vars_up.GetNbinsX()+1):
            print("PARTIAL (%s) up var bin %s = %s"%(systematic,iii,tot_BR_up.GetBinContent(iii)) )
        for iii in range(1,total_vars_down.GetNbinsX()+1):
            print("PARTIAL (%s) down var bin %s = %s"%(systematic,iii,tot_BR_down.GetBinContent(iii)) )"""


        ## determine which to add to
        avg_content_up   = tot_BR_up.GetSumOfWeights() / tot_BR_up.GetNbinsX();
        avg_content_down = tot_BR_down.GetSumOfWeights() / tot_BR_down.GetNbinsX();


        # want to add the vars in quadrature 
        
        tot_BR_up   = create_squared_hist(tot_BR_up)
        tot_BR_down = create_squared_hist(tot_BR_down)


        #print("Avg quared up BR contribution from %s is %s for %s/%s/%s."%(systematic, tot_BR_up.GetSumOfWeights() / tot_BR_up.GetNbinsX(), region,year,WP))
        #print("Avg quared down BR contribution from %s is %s for %s/%s/%s."%(systematic, tot_BR_down.GetSumOfWeights() / tot_BR_down.GetNbinsX(), region,year,WP))

        if avg_content_up > 0 and avg_content_down < 0:
            total_vars_up.Add(tot_BR_up)
            total_vars_down.Add(tot_BR_down)
        elif avg_content_up < 0 and avg_content_down > 0:
            total_vars_up.Add( tot_BR_down)
            total_vars_down.Add(tot_BR_up)
        elif avg_content_up < 0 and avg_content_down < 0:
            if avg_content_up > avg_content_down:
                total_vars_up.Add(tot_BR_down,-1 )
                total_vars_down.Add( tot_BR_down)
            else:
                total_vars_up.Add(tot_BR_up,-1 )
                total_vars_down.Add(tot_BR_up )

        elif avg_content_up > 0 and avg_content_down > 0:
            if avg_content_up > avg_content_down:
                total_vars_up.Add(tot_BR_up )
                total_vars_down.Add(tot_BR_up,-1 )
            else:
                total_vars_up.Add(tot_BR_down )
                total_vars_down.Add(tot_BR_down,-1 )

    ## get sqrt of hists 

    total_vars_up   = create_sqrt_hist(total_vars_up, setErrors=True, setTitle=False)
    total_vars_down = create_sqrt_hist(total_vars_down, setErrors=True, setTitle=False)


    #print("Avg sqrt up BR OTAL   is %s for %s/%s/%s."%(total_vars_up.GetSumOfWeights() / total_vars_up.GetNbinsX(), region,year,WP))
    #print("Avg sqrt down BR TOTAL is %s for %s/%s/%s."%(total_vars_down.GetSumOfWeights() / total_vars_down.GetNbinsX(), region,year,WP))


    #print("Avg sqrt up BR TOTAL integral is %s."%total_vars_up.Integral())
    #print("Avg sqrt down BR TOTAL integral is %s."%total_vars_down.Integral())

    for iii in range(1,total_vars_up.GetNbinsX()+1):
        total_vars_up.SetBinContent(iii, total_vars_up.GetBinContent(iii) +1)
        #print("------------- tot up var bin %s = %s"%(iii,total_vars_up.GetBinContent(iii)) )
    for iii in range(1,total_vars_down.GetNbinsX()+1):
        total_vars_down.SetBinContent(iii, total_vars_down.GetBinContent(iii) + 1)
        #print("------------- tot down var bin %s = %s"%(iii,total_vars_down.GetBinContent(iii)) )

    return total_vars_up,total_vars_down






for region in regions:

    base_dir = "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/ATWP_study"
    if region in ["ADT1b","ADT0b"]: 
        base_dir = "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/WP_study"


    ## cutoff = (max value to draw for data) values based on sig / sqrt(BR)
    """SCORE_CUTOFFS = { "WP0p05":{"2015": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0    }, 
                      "2016": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0     }, 
                      "2017": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0     }, 
                      "2018": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0} },
                      "WP0p10":{"2015": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0   }, 
                      "2016": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0     }, 
                      "2017": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0     }, 
                      "2018": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0} },
                      "WP0p12":{"2015": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0   }, 
                      "2016": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0     }, 
                      "2017": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0     }, 
                      "2018": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0} },
                      "WP0p15":{"2015": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0   }, 
                      "2016": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0     }, 
                      "2017": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0     }, 
                      "2018": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0} },
                      "WP0p17":{"2015": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0   }, 
                      "2016": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0     }, 
                      "2017": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0     }, 
                      "2018": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0} },
                      "WP0p20":{"2015": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0   }, 
                      "2016": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0     }, 
                      "2017": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0     }, 
                      "2018": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0} },
                      "WP0p25":{"2015": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0   }, 
                      "2016": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0     }, 
                      "2017": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0     }, 
                      "2018": {"Suu4_chi1":0.0, "Suu6_chi2":0.0 , "Suu8_chi3":0.0} }  } """


    wps = ["05", "10", "12", "15", "17", "20", "25", "30", "35", "40", "45", "50", "55", "60", "65", "70", "80"]
    signals = ["Suu4_chi1", "Suu6_chi2", "Suu8_chi3"]

    SCORE_CUTOFFS = {}

    for wp in wps:
        wp_key = "WP0p%s" % wp
        SCORE_CUTOFFS[wp_key] = {}
        for year in years:
            SCORE_CUTOFFS[wp_key][year] = {}
            for signal in signals:
                SCORE_CUTOFFS[wp_key][year][signal] = 0.0

    if region in ["ADT0b","ADT1b"]: 
        working_points = ["25", "30", "35", "40", "45", "50", "55", "60", "65", "70", "80"]
        
        
    for wp in working_points:

        wp_dir = os.path.join(base_dir, "WP0p" + wp)
        print "Processing WP:", wp

        wp_str = "WP0p" + wp

        hist_name = _hist_name + "_" + region
        output_pdf = os.path.join(base_dir, "combined_" + hist_name + ".pdf")
        first_page = True

        for year in years:

            year_str = year
            if year == "2015": year_str = "2016preAPV"
            if year == "2016": year_str = "2016postAPV"

            BR_hists            = []
            sig_hists_Suu4_chi1 = []
            sig_hists_Suu6_chi2 = []
            sig_hists_Suu8_chi3 = []

            hs = ROOT.THStack("h_BR", "NN Output Scores (%s) (%s) ; NN Output Score; superjets"%(region,year_str))

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
            }
            sig_Suu4_chi1_samples = {
                "Suu4_chi1_HTHT": return_signal_SF(year, "Suu4_chi1","HTHT"),
                "Suu4_chi1_ZTZT": return_signal_SF(year, "Suu4_chi1","ZTZT"),
                "Suu4_chi1_WBWB": return_signal_SF(year, "Suu4_chi1","WBWB"),
                "Suu4_chi1_WBHT": return_signal_SF(year, "Suu4_chi1","WBHT"),
                "Suu4_chi1_WBZT": return_signal_SF(year, "Suu4_chi1","WBZT"),
                "Suu4_chi1_HTZT": return_signal_SF(year, "Suu4_chi1", "HTZT"),
            }
            sig_Suu6_chi2_samples = {
                "Suu6_chi2_HTHT": return_signal_SF(year, "Suu6_chi2","HTHT"),
                "Suu6_chi2_ZTZT": return_signal_SF(year, "Suu6_chi2","ZTZT"),
                "Suu6_chi2_WBWB": return_signal_SF(year, "Suu6_chi2","WBWB"),
                "Suu6_chi2_WBHT": return_signal_SF(year, "Suu6_chi2","WBHT"),
                "Suu6_chi2_WBZT": return_signal_SF(year, "Suu6_chi2","WBZT"),
                "Suu6_chi2_HTZT": return_signal_SF(year, "Suu6_chi2", "HTZT"),
            }
            sig_Suu8_chi3_samples = {
                "Suu8_chi3_HTHT": return_signal_SF(year, "Suu8_chi3","HTHT"),
                "Suu8_chi3_ZTZT": return_signal_SF(year, "Suu8_chi3","ZTZT"),
                "Suu8_chi3_WBWB": return_signal_SF(year, "Suu8_chi3","WBWB"),
                "Suu8_chi3_WBHT": return_signal_SF(year, "Suu8_chi3","WBHT"),
                "Suu8_chi3_WBZT": return_signal_SF(year, "Suu8_chi3","WBZT"),
                "Suu8_chi3_HTZT": return_signal_SF(year, "Suu8_chi3", "HTZT"),
            }

            ### combined BRs
            combined_hist_BR = None
            for iii,sample in enumerate(BR_samples):
                scale = qcd_samples[sample]

                if region in ["ADT0b","ADT1b"]: 
                    file_name = sample + "_" + year + "_WP0p" + wp + "_processed.root"
                else:
                    file_name = sample + "_" + year + "_ATWP0p" + wp + "_processed.root"
                file_path = os.path.join(wp_dir, file_name)

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
                hist.SetMinimum(1e-3)
                hist.SetFillColor(colors[iii])
                hist.SetLineColor(colors[iii])

                hist.GetXaxis().SetTitle("NN Output Score")
                hist.SetStats(0)
                BR_hists.append(hist)
                hs.Add(hist)
                f.Close()

                if combined_hist_BR is None:
                    combined_hist_BR = hist.Clone("combined_hist_BR")
                else:
                    combined_hist_BR.Add(hist)

            ### Suu4_chi1
            combined_hist_Suu4_chi1 = None

            for sample in sig_Suu4_chi1_samples:
                scale = sig_Suu4_chi1_samples[sample]

                if region in ["ADT0b","ADT1b"]: 
                    file_name = sample + "_" + year + "_WP0p" + wp + "_processed.root"
                else:
                    file_name = sample + "_" + year + "_ATWP0p" + wp + "_processed.root"
                file_path = os.path.join(wp_dir, file_name)

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
                sig_hists_Suu4_chi1.append(hist)

                f.Close()

                if combined_hist_Suu4_chi1 is None:
                    combined_hist_Suu4_chi1 = hist.Clone("combined_hist_Suu4_chi1")
                else:
                    combined_hist_Suu4_chi1.Add(hist)


            ### Suu6_chi2
            combined_hist_Suu6_chi2 = None

            for sample in sig_Suu6_chi2_samples:
                scale = sig_Suu6_chi2_samples[sample]
                if region in ["ADT0b","ADT1b"]: 
                    file_name = sample + "_" + year + "_WP0p" + wp + "_processed.root"
                else:
                    file_name = sample + "_" + year + "_ATWP0p" + wp + "_processed.root"
                file_path = os.path.join(wp_dir, file_name)

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
                sig_hists_Suu6_chi2.append(hist)
                f.Close()

                if combined_hist_Suu6_chi2 is None:
                    combined_hist_Suu6_chi2 = hist.Clone("combined_hist_Suu6_chi2")
                else:
                    combined_hist_Suu6_chi2.Add(hist)

            ### Suu8_chi3
            combined_hist_Suu8_chi3 = None

            for sample in sig_Suu8_chi3_samples:
                scale = sig_Suu8_chi3_samples[sample]

                if region in ["ADT0b","ADT1b"]: 
                    file_name = sample + "_" + year + "_WP0p" + wp + "_processed.root"
                else:
                    file_name = sample + "_" + year + "_ATWP0p" + wp + "_processed.root"
                file_path = os.path.join(wp_dir, file_name)

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
                sig_hists_Suu8_chi3.append(hist)
                f.Close()

                if combined_hist_Suu8_chi3 is None:
                    combined_hist_Suu8_chi3 = hist.Clone("combined_hist_Suu8_chi3")
                else:
                    combined_hist_Suu8_chi3.Add(hist)

            sig_colors    = [ROOT.kBlack,ROOT.kCyan,ROOT.kGreen] 
            sig_line_styles = [2,8,10]
            sig_hists      = [combined_hist_Suu4_chi1,combined_hist_Suu6_chi2,combined_hist_Suu8_chi3 ]


            c = ROOT.TCanvas("c", "c", 1200, 1200)

            if combined_hist_BR and combined_hist_Suu4_chi1 and combined_hist_Suu6_chi2 and combined_hist_Suu8_chi3 and hs:
                c.SetRightMargin(0.15)
                combined_hist_BR.SetTitle(hist_name + " (Year " + year + ", AT WP = 0." + wp + ")")

                hs.SetMinimum(1e-3)

                combined_hist_Suu4_chi1.SetLineColor(ROOT.kBlack)
                combined_hist_Suu6_chi2.SetLineColor(ROOT.kCyan)
                combined_hist_Suu8_chi3.SetLineColor(ROOT.kGreen)

                # Create a canvas and pads for upper and lower plots
                pad1 = ROOT.TPad("pad1", "Top pad", 0, 0.30, 1, 1.0)
                pad2 = ROOT.TPad("pad2", "Bottom pad", 0, 0.0, 1, 0.290)
                
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
                max_value = max( sig_hists[0].GetMaximum(),sig_hists[1].GetMaximum(),sig_hists[2].GetMaximum(), combined_hist_BR.GetMaximum()   )


                #print("THStack contains the following histograms:")
                #for i, h in enumerate(hs.GetHists()):
                #    print("  [%d] %s (entries = %s)" % (i, h.GetName(), h.GetEntries()))

                hs.Draw("HIST")
                hs.SetMaximum(100*max_value)
                hs.SetMinimum(1e-2)
                
                c.SaveAs("some_test.png")

                # validate the THstack

                combined_hist_Suu4_chi1.SetLineWidth(2)
                combined_hist_Suu6_chi2.SetLineWidth(2)
                combined_hist_Suu8_chi3.SetLineWidth(2)

                combined_hist_Suu4_chi1.Draw("HIST,same")
                combined_hist_Suu6_chi2.Draw("HIST,same")
                combined_hist_Suu8_chi3.Draw("HIST,same")


                # Draw the ratio on the lower pad
                pad2.cd()
                pad2.SetLogy()
                x_min = 0
                x_max = 0

                hRatios = []
                mass_points = ["Suu4_chi1","Suu6_chi2","Suu8_chi3"]
                
                for iii,sig_hist in enumerate(sig_hists):

                    hRatio = sig_hist.Clone("hRatio%s"%iii)
                    hRatios.append(hRatio)
                    hRatio.Divide( create_sqrt_hist(combined_hist_BR))  # Compute the ratio h2 / hStackTotal
                    hRatio.SetLineStyle(sig_line_styles[iii])
                    hRatio.SetTitle("")
                    hRatio.GetYaxis().SetTitle(r"sig / #sqrt{BR}")
                    #hRatio.GetYaxis().SetNdivisions(505)
                    #hRatio.GetYaxis().SetRangeUser(0.0, 1.5)  # Adjust the y-axis range for clarity
                    hRatio.GetYaxis().SetTitleSize(0.1)
                    hRatio.GetYaxis().SetTitleOffset(0.4)
                    hRatio.GetYaxis().SetLabelSize(0.08)
                    hRatio.GetXaxis().SetTitleSize(0.12)
                    hRatio.GetXaxis().SetLabelSize(0.1)
                    hRatio.GetXaxis().SetTitle("NN Output Score")
                    hRatio.SetLineWidth(2)
                    #hRatio.SetFillColor(ROOT.kGray )
                    

                    for jjj in range(1,hRatio.GetNbinsX()+1):
                        if hRatio.GetBinContent(jjj) < SIGBR_CUTOFF:
                            SCORE_CUTOFFS[wp_str][year][mass_points[iii]] = hRatio.GetBinCenter(jjj)

                    print("-------- FOR YEAR %s and mass point %s, the sig/BR cutoff point is %s."%(year,mass_points[iii],SCORE_CUTOFFS[wp_str][year][mass_points[iii]] ))

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


                nom_line_down = ROOT.TLine(x_min, 0.7, x_max, 0.7)
                nom_line_down.SetLineStyle(2)  # Dotted line style
                nom_line_down.SetLineColor(ROOT.kRed)  # Dotted line style
                nom_line_down.Draw("same")


                cutoff_label = ROOT.TLatex()
                cutoff_label.SetNDC()
                cutoff_label.SetTextSize(0.045)
                cutoff_label.SetTextFont(62)
                cutoff_label.DrawLatex(0.80, 0.95, "Cutoff:\n %s"%(min( SCORE_CUTOFFS[wp_str][year]["Suu4_chi1"] ,SCORE_CUTOFFS[wp_str][year]["Suu6_chi2"] ,SCORE_CUTOFFS[wp_str][year]["Suu8_chi3"] )))


                # Add legend and TLatex text
                pad1.cd()


                if region not in ["CR","SR"]:
                    label = ROOT.TLatex()
                    label.SetNDC()
                    label.SetTextSize(0.045)
                    label.SetTextFont(62)
                    if region in ["AT1b","AT0b"]: label.DrawLatex(0.40, 0.91, "Year: " + year_str + "   AT WP: " + "0."+ wp)
                    elif region in ["0b"]: label.DrawLatex(0.40, 0.91, "Year: " + year_str + ", SJ1 WP: 0.50")


                
                legend = ROOT.TLegend(0.155, 0.70, 0.80, 0.88)
                legend.SetNColumns(4);  
                legend.SetTextSize(0.01) 

                legend.SetBorderSize(0)
                legend.SetFillStyle(0) 

                legend.AddEntry(BR_hists[0], "ST-s-channel-hadrons", "f")
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
                legend.AddEntry(BR_hists[13], "QCD1000to1500", "f")
                legend.AddEntry(BR_hists[14], "QCD1500to2000", "f")
                legend.AddEntry(BR_hists[15], "QCD2000toInf", "f")


                legend.AddEntry(sig_hists[0], r"\mbox{signal } (\mbox{M}_{S_{uu}} = \mbox{ 4 TeV, } \mbox{M}_{\chi} = \mbox{ 1 TeV)}", "l")
                legend.AddEntry(sig_hists[1], r"\mbox{signal } (\mbox{M}_{S_{uu}} = \mbox{ 6 TeV, } \mbox{M}_{\chi} = \mbox{ 2 TeV)}", "l")
                legend.AddEntry(sig_hists[2], r"\mbox{signal } (\mbox{M}_{S_{uu}} = \mbox{ 8 TeV, } \mbox{M}_{\chi} = \mbox{ 3 TeV)}", "l")
                legend.Draw() 

                if region in ["0b"]: write_cms_text.write_cms_text(CMS_label_xpos=0.140, SIM_label_xpos=0.275,CMS_label_ypos = 0.925, SIM_label_ypos = 0.925, lumistuff_xpos=0.94, lumistuff_ypos=0.91, year=year, uses_data=False)
                else:  write_cms_text.write_cms_text(CMS_label_xpos=0.140, SIM_label_xpos=0.275,CMS_label_ypos = 0.925, SIM_label_ypos = 0.925, lumistuff_xpos=0.90, lumistuff_ypos=0.91, year=year, uses_data=False)
                

                png_path = os.path.join(wp_dir, "combined_" + hist_name + "_" + year + "_"+ region + "_ATWP0p" + wp + ".png")
                #root_out_path = os.path.join(wp_dir, "combined_" + hist_name + "_" + year + "_ATWP0p" + wp + ".root")

                c.SaveAs(png_path)

                if first_page:
                    c.SaveAs(output_pdf + "[")
                    first_page = False

                c.SaveAs(output_pdf)

                #out_file = ROOT.TFile(root_out_path, "RECREATE")
                #combined_hist_BR.Write()
                #out_file.Close()


                print "Saved", hist_name, "for WP", wp 
            else:
                print "No histograms combined for", hist_name, "WP", wp, " --------- BR hist / Suu4_chi1 hist / Suu6_chi2 hist / Suu8_chi3 hist are %s/%s/%s/%s"%(combined_hist_BR,combined_hist_Suu4_chi1,combined_hist_Suu6_chi2,combined_hist_Suu8_chi3) 
 
            del c 

    #print("%s cutoffs are %s"%(region,SCORE_CUTOFFS))


    ### now draw data / MC:
    for wp in working_points:
        wp_dir = os.path.join(base_dir, "WP0p" + wp)
        print "Processing WP:", wp

        wp_str = "WP0p" + wp

        hist_name = _hist_name + "_" + region

        for year in years:

            year_str = year
            if year == "2015": year_str = "2016preAPV"
            if year == "2016": year_str = "2016postAPV"

            BR_hists            = []

            hs = ROOT.THStack("h_BR", "NN Output Scores (%s) (%s) ; NN Output Score; superjets"%(region,year_str))

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

            }

            data_samples = {"2015": ["dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM" ,"dataF-HIPM"], 
            "2016": ["dataF","dataG","dataH"], 
            "2017": ["dataB","dataC","dataD","dataE","dataF"], 
            "2018": ["dataA","dataB", "dataC", "dataD"] }


           

            ### combined BRs
            combined_hist_BR = None
            for iii,sample in enumerate(BR_samples):
                scale = qcd_samples[sample]

                if region in ["ADT0b","ADT1b"]: 
                    file_name = sample + "_" + year + "_WP0p" + wp + "_processed.root"
                else:
                    file_name = sample + "_" + year + "_ATWP0p" + wp + "_processed.root"
                file_path = os.path.join(wp_dir, file_name)

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

                hist.GetXaxis().SetTitle("NN Output Score")
                hist.SetStats(0)
                BR_hists.append(hist)
                hs.Add(hist)


                if combined_hist_BR is None:
                    combined_hist_BR = hist.Clone("combined_hist_BR")
                    combined_hist_BR.SetDirectory(0)
                else:
                    combined_hist_BR.Add(hist)

                hist.SetDirectory(0)
                f.Close()


            _combined_data = None
            ## get combined data hist
            for iii,sample in enumerate(data_samples[year]):

                if region in ["ADT0b","ADT1b"]: 
                    file_name = sample + "_" + year + "_WP0p" + wp + "_processed.root"
                else:
                    file_name = sample + "_" + year + "_ATWP0p" + wp + "_processed.root"
                file_path = os.path.join(wp_dir, file_name)

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
                hist.GetXaxis().SetTitle("NN Output Score")
                hist.SetStats(0)

                f.Close()

                if _combined_data is None:
                    _combined_data = hist.Clone("combined_data")
                else:
                    _combined_data.Add(hist)

            ## data histogram:
            combined_data = None
            if _combined_data:
                combined_data = _combined_data.Clone("combined_data_masked")
                combined_data.Reset()
                for iii in range(1, _combined_data.GetNbinsX()+1):
                    if _combined_data.GetBinCenter(iii) < min( SCORE_CUTOFFS[wp_str][year]["Suu4_chi1"] ,SCORE_CUTOFFS[wp_str][year]["Suu6_chi2"] ,SCORE_CUTOFFS[wp_str][year]["Suu8_chi3"] ):
                        combined_data.SetBinContent(iii,_combined_data.GetBinContent(iii))
                        combined_data.SetBinError(iii,_combined_data.GetBinError(iii))

            c = ROOT.TCanvas("c", "c", 1200, 1200)
            if combined_hist_BR and combined_data:

                c.SetRightMargin(0.15)
                
                # Create a canvas and pads for upper and lower plots
                pad1 = ROOT.TPad("pad1", "Top pad", 0, 0.30, 1, 1.0)
                pad2 = ROOT.TPad("pad2", "Bottom pad", 0, 0.0, 1, 0.290)
                
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
                max_value = max( combined_data.GetMaximum(), combined_hist_BR.GetMaximum()   )


                hs.Draw("HIST")
                hs.SetMaximum(100*max_value)

                combined_data.SetMarkerStyle(20)         # Solid circles
                combined_data.SetMarkerColor(ROOT.kBlack)
                combined_data.SetLineColor(ROOT.kBlack)  # Error bar color
                combined_data.SetLineWidth(1)
                combined_data.Draw("PE1,SAME")

                c.Update()

                # Draw the ratio on the lower pad
                pad2.cd()
                #pad2.SetLogy()
                x_min = 0
                x_max = 0

                mass_points = ["Suu4_chi1","Suu6_chi2","Suu8_chi3"]

                hRatio = combined_data.Clone("hRatio%s"%iii)
                hRatio.SetMinimum(0.05)
                hRatio.SetMaximum(2.0)
                hRatio.SetTitle("")
                hRatio.Divide( combined_hist_BR)  # Compute the ratio h2 / hStackTotal
                hRatio.GetYaxis().SetTitle(r"data / MC")
                #hRatio.GetYaxis().SetNdivisions(505)
                #hRatio.GetYaxis().SetRangeUser(0.0, 1.5)  # Adjust the y-axis range for clarity
                hRatio.GetYaxis().SetTitleSize(0.1)
                hRatio.GetYaxis().SetTitleOffset(0.4)
                hRatio.GetYaxis().SetLabelSize(0.08)
                hRatio.GetXaxis().SetTitleSize(0.12)
                hRatio.GetXaxis().SetLabelSize(0.1)
                hRatio.GetXaxis().SetTitle("NN Output Score")
    
                hRatio.Draw()


                BR_var_up, BR_var_down = get_uncert_bands(year, region, wp, BR_samples, hRatio.GetNbinsX())

                BR_var_up.SetLineColor(ROOT.kBlue)
                BR_var_down.SetLineColor(ROOT.kRed)
                BR_var_up.Draw("HIST, SAME")
                BR_var_down.Draw("HIST, SAME")


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

                
                cutoff_label = ROOT.TLatex()
                cutoff_label.SetNDC()
                cutoff_label.SetTextSize(0.045)
                cutoff_label.SetTextFont(62)
                cutoff_label.DrawLatex(0.80, 0.88, "Cutoff:\n %s"%(min( SCORE_CUTOFFS[wp_str][year]["Suu4_chi1"] ,SCORE_CUTOFFS[wp_str][year]["Suu6_chi2"] ,SCORE_CUTOFFS[wp_str][year]["Suu8_chi3"] )))


                # Add legend and TLatex text
                pad1.cd()


                if region not in ["CR","SR"]:
                    label = ROOT.TLatex()
                    label.SetNDC()
                    label.SetTextSize(0.045)
                    label.SetTextFont(62)
                    if region in ["AT1b","AT0b"]: label.DrawLatex(0.40, 0.91, "Year: " + year_str + "   AT WP: " + "0."+ wp)
                    elif region in ["0b"]: label.DrawLatex(0.40, 0.91, "Year: " + year_str + ", SJ1 WP: 0.50")

                legend = ROOT.TLegend(0.155, 0.70, 0.80, 0.88)
                legend.SetNColumns(4);  
                legend.SetTextSize(0.01) 

                legend.SetBorderSize(0)
                legend.SetFillStyle(0) 

                legend.AddEntry(BR_hists[0], "ST-s-channel-hadrons", "f")
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
                legend.AddEntry(BR_hists[13], "QCD1000to1500", "f")
                legend.AddEntry(BR_hists[14], "QCD1500to2000", "f")
                legend.AddEntry(BR_hists[15], "QCD2000toInf", "f")


                legend.AddEntry(combined_data, "Data", "p")
                legend.Draw()

                if region in ["0b"]: write_cms_text.write_cms_text(CMS_label_xpos=0.138, SIM_label_xpos=0.275,CMS_label_ypos = 0.925, SIM_label_ypos = 0.925, lumistuff_xpos=0.94, lumistuff_ypos=0.91, year = "", uses_data=True)
                else:  write_cms_text.write_cms_text(CMS_label_xpos=0.138, SIM_label_xpos=0.275,CMS_label_ypos = 0.925, SIM_label_ypos = 0.925, lumistuff_xpos=0.90, lumistuff_ypos=0.91, year = "", uses_data=True)
                png_path = os.path.join(wp_dir, "dataMC_" + hist_name + "_" + year + "_"+ region + "_ATWP0p" + wp + ".png")
                root_out_path = os.path.join(wp_dir, "dataMC_" + hist_name + "_" + year + "_ATWP0p" + wp + ".root")

                c.SaveAs(png_path)

                if first_page:
                    c.SaveAs(output_pdf + "[")
                    first_page = False

                c.SaveAs(output_pdf)

                out_file = ROOT.TFile(root_out_path, "RECREATE")
                combined_hist_BR.Write()
                out_file.Close()




                print "Saved", hist_name, "for WP", wp
            else:
                print "No histograms combined for", hist_name, "WP", wp

            del c 
    
    c2 = ROOT.TCanvas("", "", 1200, 1200)
    if not first_page:
        c2.SaveAs(output_pdf + "]")
        print "All plots written to", output_pdf
    else:
        print "No plots created for", hist_name, ". PDF not generated."
    del c2  






