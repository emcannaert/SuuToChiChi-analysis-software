import ROOT
from combine_hists import combine_hists
from return_BR_SF.return_BR_SF import return_BR_SF
import sys, os

## this script creates comparisons of the systematic event weights between years 
## as well as comparisons between regions for individual years

BR_SFs = return_BR_SF()

canvas = ROOT.TCanvas("canvas", "Histograms", 1200, 1000)
canvas.SetLogy() 
useEOS  = True
file_path = "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/" if useEOS else "../combinedROOT/processedFiles/"

pdf_folder = "pdf"

# PDF canvas setup
c1 = ROOT.TCanvas("pdf_canvas", "pdf", 2400, 2000)
nx, ny = 4, 4  # 4x4 grid = 16 plots per page
c1.Divide(nx, ny)

if not os.path.exists(pdf_folder):
    os.makedirs(pdf_folder)

pdf_file = os.path.join(pdf_folder, "all_eventWeights.pdf")
c1.Print(pdf_file + "[")  # start multi-page PDF

pad_num = 1  # global pad counter for PDF


## do plot with multiple years for pre-selected region
def plot_var_weight_comparisons_by_sample(hist_name, sample_list, systematic):
    global pad_num
    years = ["2015", "2016", "2017", "2018"]
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen + 2, ROOT.kOrange]

    hist_name_str = hist_name[2:]

    if "QCD" in sample_list[0]:   BR_type = "QCD" 
    elif "TTTo" in sample_list[0]: BR_type = "TTbar"
    elif "TTJets" in sample_list[0]: BR_type = "TTJets"
    elif "WJets" in sample_list[0]: BR_type = "WJets"
    elif "ST_" in sample_list[0]: BR_type = "ST"
    else:
        print("ERROR: cannot tell BR type.")
        return
    variations = [""] if systematic == "nom" else ["_up", "_down"] 

    for var in variations:

        canvas.Clear()  # Clear the PNG canvas
        legend = ROOT.TLegend(0.6, 0.6, 0.8, 0.8)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        ROOT.gStyle.SetOptStat(0)  # Disable stats box

        var_str = "nom" if var == "" else var.split("_")[1]
        saved_hists = []
        for i, year in enumerate(years):
            hist_name_use = "%s%s/%s"%( systematic,var,hist_name)

            file_paths = { sample_type: "{}{}_{}_processed.root".format(file_path,sample_type, year) for sample_type in sample_list   }
            hist_weights = { sample_type: BR_SFs[sample_type.replace("-","_")][year] for sample_type in sample_list }

            hist = combine_hists(
                sample_list,
                file_paths,
                hist_name_use,
                hist_weights=hist_weights,
                hist_label = hist_name + "_" + year
            )

            hist.SetDirectory(0)  
            #hist.SetLineWidth(1)  
            hist.SetTitle("%s (%s) (%s) (%s var) (%s)"%(hist.GetTitle(), BR_type, systematic, var_str, year))

            if hist.Integral() > 0:
                hist.Scale(1.0 / hist.Integral())
            hist.SetLineColor(colors[i])
            hist.SetMaximum(1.5)

            draw_option = "HIST" if i == 0 else "HIST SAME"
            hist.Draw(draw_option)
            saved_hists.append(hist)
            legend.AddEntry(hist, year, "l")

        legend.Draw()

        # ---- PDF handling ----
        c1.cd(pad_num)
        canvas.DrawClonePad()  # copy PNG canvas into PDF pad
        pad_num += 1
        if pad_num > nx * ny:
            c1.Update()
            c1.Print(pdf_file)
            c1.Clear()
            c1.Divide(nx, ny)
            pad_num = 1

        # ---- PNG handling ----
        output_name = "plots/nom_systematic_comparisons/years_by_sample/{}_{}_{}{}_comparison.png".format(
            BR_type, hist_name_str, systematic, var
        )
        canvas.SaveAs(output_name)



## do plot with multiple regions for individual years
def plot_var_weight_comparisons_by_sample_and_region(hist_name, sample_list,year,systematic):
    global pad_num
    regions = ["SR","CR","AT1b","AT0b"]
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen + 2, ROOT.kOrange]
    
    variations = [""] if systematic == "nom" else ["_up", "_down"] 
    hist_name_str = hist_name[2:]

    if "QCD" in sample_list[0]:  BR_type = "QCD" 
    elif "TTTo" in sample_list[0]: BR_type = "TTbar"
    elif "TTJets" in sample_list[0]: BR_type = "TTJets"
    elif "WJets" in sample_list[0]: BR_type = "WJets"
    elif "ST_" in sample_list[0]: BR_type = "ST"
    else:
        print("ERROR: cannot tell BR type.")
        return

    for var in variations:

        var_str = "nom" if var == "" else var.split("_")[1]

        canvas.Clear()  
        legend = ROOT.TLegend(0.6, 0.6, 0.8, 0.8)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        ROOT.gStyle.SetOptStat(0)  

        saved_hists = []
        for i, region in enumerate(regions):
            hist_name_use = "%s%s/%s_%s"%( systematic,var,hist_name,  region)

            file_paths = { sample_type: "{}{}_{}_processed.root".format(file_path,sample_type, year) for sample_type in sample_list   }
            hist_weights = { sample_type: BR_SFs[sample_type.replace("-","_")][year] for sample_type in sample_list }

            hist = combine_hists(
                sample_list,
                file_paths,
                hist_name_use,
                hist_weights=hist_weights,
                hist_label = hist_name + "_region"
            )

            hist.SetDirectory(0)  
            hist.SetLineWidth(1)  
            hist.SetTitle("%s  (%s) (%s) (%s var) (%s)"%(hist.GetTitle(), BR_type, systematic, var_str, year))

            if hist.Integral() > 0:
                hist.Scale(1.0 / hist.Integral())
            hist.SetLineColor(colors[i])
            hist.SetMaximum(1.5)

            saved_hists.append(hist)
            legend.AddEntry(hist, region, "l")
            draw_option = "HIST" if i == 0 else "HIST SAME"
            hist.Draw(draw_option)

        legend.Draw()

        # ---- PDF handling ----
        c1.cd(pad_num)
        canvas.DrawClonePad()
        pad_num += 1
        if pad_num > nx * ny:
            c1.Update()
            c1.Print(pdf_file)
            c1.Clear()
            c1.Divide(nx, ny)
            pad_num = 1

        # ---- PNG handling ----
        output_name = "plots/nom_systematic_comparisons/regions_by_sample_and_year/{}_{}_{}{}_{}_comparison.png".format(
            BR_type, hist_name_str, systematic,var,year
        )
        canvas.SaveAs(output_name)


if __name__=="__main__":
    combined_BRs = True
    use_QCD_Pt = True

    if use_QCD_Pt: 
        QCD_samples = [
            "QCDMC_Pt_170to300","QCDMC_Pt_300to470","QCDMC_Pt_470to600",
            "QCDMC_Pt_600to800","QCDMC_Pt_800to1000","QCDMC_Pt_1000to1400",
            "QCDMC_Pt_1400to1800","QCDMC_Pt_1800to2400","QCDMC_Pt_2400to3200",
            "QCDMC_Pt_3200toInf"
        ]
    else: 
        QCD_samples = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf"]

    if combined_BRs: 
        samples = [
            QCD_samples,
            ["TTJetsMCHT800to1200", "TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf"],
            ["TTToHadronicMC","TTToSemiLeptonicMC" , "TTToLeptonicMC"],
            ["WJetsMC_LNu-HT800to1200","WJetsMC_LNu-HT1200to2500","WJetsMC_LNu-HT2500toInf","WJetsMC_QQ-HT800toInf"],
            ["ST_t-channel-top_inclMC","ST_t-channel-antitop_inclMC","ST_s-channel-hadronsMC","ST_s-channel-leptonsMC","ST_tW-antiTop_inclMC","ST_tW-top_inclMC"]
        ]  
    else:
        QCD_separate = [[QCD_separate] for QCD_separate in QCD_samples]
        samples = [
            ["TTJetsMCHT800to1200"], ["TTJetsMCHT1200to2500"], ["TTJetsMCHT2500toInf"],
            ["TTToHadronicMC"],["TTToSemiLeptonicMC"],["TTToLeptonicMC"],
            ["WJetsMC_LNu-HT800to1200"],["WJetsMC_LNu-HT1200to2500"],["WJetsMC_LNu-HT2500toInf"],["WJetsMC_QQ-HT800toInf"],
            ["ST_t-channel-top_inclMC"],["ST_t-channel-antitop_inclMC"],["ST_s-channel-hadronsMC"],["ST_s-channel-leptonsMC"],
            ["ST_tW-antiTop_inclMC"],["ST_tW-top_inclMC"]
        ]  
        samples.extend(QCD_separate)

    systematics = ["nom","scale","pdf","renorm","fact","JER","JER_eta193","JER_193eta25",
        "JEC","JEC_FlavorQCD","JEC_RelativeBal","JEC_Absolute","JEC_AbsoluteCal","JEC_AbsoluteScale",
        "JEC_Fragmentation","JEC_AbsoluteMPFBias","JEC_RelativeFSR","JEC_AbsoluteTheory","JEC_AbsolutePU",
        "JEC_BBEC1_year","JEC_Absolute_year","JEC_RelativeSample_year"]

    years = ["2015","2016","2017","2018"]

    for systematic in systematics:
        if "JEC" in systematic:
            hist_names = ["h_JEC_uncert_AK8", "h_JEC_uncert_AK4"]
        elif "JER" in systematic:
            hist_names = ["h_AK8_JER"]
        elif systematic == "pdf":
            hist_names = ["h_pdf_EventWeight"]
        elif systematic == "renorm":
            hist_names = ["h_renorm_EventWeight"]
        elif systematic == "factor":
            hist_names = ["h_factor_EventWeight"]
        elif systematic == "scale":
            hist_names = ["h_scale_EventWeight"]
        elif systematic == "nom":
            hist_names = ["h_pdf_EventWeight","h_scale_EventWeight","h_PU_eventWeight",
                "h_bTag_eventWeight_M","h_L1PrefiringWeight","h_AK8_JER"]
        for year in years:
            for sample_list in samples:
                for hist_name in hist_names:
                    try:
                        plot_var_weight_comparisons_by_sample_and_region(hist_name, sample_list,year,systematic)
                    except:
                        print("ERROR: failed on %s/%s/%s"%(year,hist_name, sample_list))

    for systematic in systematics:
        if "JEC" in systematic:
            hist_names = ["h_JEC_uncert_AK8", "h_JEC_uncert_AK4"]
        elif "JER" in systematic:
            hist_names = ["h_AK8_JER"]
        elif systematic == "pdf":
            hist_names = ["h_pdf_EventWeight"]
        elif systematic == "renorm":
            hist_names = ["h_renorm_EventWeight"]
        elif systematic == "factor":
            hist_names = ["h_factor_EventWeight"]
        elif systematic == "scale":
            hist_names = ["h_scale_EventWeight"]
        elif systematic == "nom":
            hist_names = ["h_pdf_EventWeight","h_scale_EventWeight","h_PU_eventWeight",
                "h_bTag_eventWeight_M","h_L1PrefiringWeight","h_AK8_JER"]
        for sample_list in samples:
            for hist_name in hist_names:
                print("Running for systematic %s, and sample type %s"%(systematic, sample_list ))
                try:
                    plot_var_weight_comparisons_by_sample(hist_name, sample_list, systematic)
                except:
                    print("ERROR: failed on %s/%s"%(hist_name, sample_list))


# flush remaining plots if last page not full
if pad_num > 1:
    c1.Update()
    c1.Print(pdf_file)

c1.Print(pdf_file + "]")