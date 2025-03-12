import ROOT

def write_cms_text(CMS_label_xpos=0.152, SIM_label_xpos=0.255,CMS_label_ypos = 0.92, SIM_label_ypos = 0.92, lumistuff_xpos=0.89, lumistuff_ypos=0.91, year = "", uses_data=False):

    ## options for years are 2015 (=2016preAPV), 2016 (=2016postAPV), 2017, 2018, and Run2
    ## Will have to find what the best positions are for each of the bits of text (CMS label, SIM labe, and lumistuff)
    ## when there is data involved, be sure that uses_data is passed as True and that you include the correct year

    data_type_str = "Private Work (CMS simulation)" 
    lumistuff =  "(13 TeV)"

    if uses_data:
        if year =="2015": lumistuff   =  "19.5 fb^{-1} "+ lumistuff
        elif year =="2016": lumistuff =  "16.8 fb^{-1} "+ lumistuff
        elif year =="2017": lumistuff =  "41.8 fb^{-1} "+ lumistuff
        elif year =="2018": lumistuff =  "59.8 fb^{-1} "+ lumistuff

        data_type_str = "Private Work (CMS data/simulation)" 
   

    # do all the fancy formatting 
    ROOT.gStyle.SetOptStat(0);
    CMSLabel = ROOT.TText()
    CMSLabel.SetNDC()
    CMSLabel.SetTextFont(1)
    CMSLabel.SetTextColor(1)
    CMSLabel.SetTextSize(0.0385)
    CMSLabel.SetTextAlign(22)
    CMSLabel.SetTextAngle(0)
    CMSLabel.DrawText(CMS_label_xpos, CMS_label_ypos, "CMS")
    CMSLabel.Draw()

    simLabel = ROOT.TText()
    simLabel.SetNDC()
    simLabel.SetTextFont(52)
    simLabel.SetTextColor(1)
    simLabel.SetTextSize(0.024)
    simLabel.SetTextAlign(22)
    simLabel.SetTextAngle(0)
    simLabel.DrawText(SIM_label_xpos, SIM_label_ypos, data_type_str)
    simLabel.Draw()

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack);  
    latex.SetTextFont(42)
    latex.SetTextAlign(31);
    latex.SetTextSize(0.030);   
    latex.DrawLatex(lumistuff_xpos,lumistuff_ypos,lumistuff)
    return


"""

def write_cms_text(CMS_label_pos, SIM_label_pos):
	# do all the fancy formatting 
	ROOT.gStyle.SetOptStat(0);
	CMSLabel = ROOT.TText()
	CMSLabel.SetNDC()
	CMSLabel.SetTextFont(1)
	CMSLabel.SetTextColor(1)
	CMSLabel.SetTextSize(0.0385)
	CMSLabel.SetTextAlign(22)
	CMSLabel.SetTextAngle(0)
	CMSLabel.DrawText(CMS_label_pos, 0.92, "CMS")
	CMSLabel.Draw()

	simLabel = ROOT.TText()
	simLabel.SetNDC()
	simLabel.SetTextFont(52)
	simLabel.SetTextColor(1)
	simLabel.SetTextSize(0.024)
	simLabel.SetTextAlign(22)
	simLabel.SetTextAngle(0)
	simLabel.DrawText(SIM_label_pos, 0.92, "Simulation Preliminary")
	simLabel.Draw()

	latex = ROOT.TLatex()
	lumistuff =  "(13 TeV)"
	latex.SetNDC()
	latex.SetTextAngle(0)
	latex.SetTextColor(ROOT.kBlack);  
	latex.SetTextFont(42)
	latex.SetTextAlign(31);
	latex.SetTextSize(0.030);   
	latex.DrawLatex(0.89,0.91,lumistuff)

	return




"""