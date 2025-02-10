

TFile * f_QCD1000to1500 = TFile::Open("../combinedROOT/processedFiles/QCDMC1000to1500_2016_processed.root")
TFile * f_QCD1500to2000 = TFile::Open("../combinedROOT/processedFiles/QCDMC1500to2000_2016_processed.root")
TFile * f_QCD2000toInf = TFile::Open("../combinedROOT/processedFiles/QCDMC2000toInf_2016_processed.root")

TH1F * h_QCD1000to1500 = (TH1F*)f_QCD1000to1500->Get("nom/h_totHT_SR")
TH1F * h_QCD1500to2000 = (TH1F*)f_QCD1500to2000->Get("nom/h_totHT_SR")
TH1F * h_QCD2000toInf  = (TH1F*)f_QCD2000toInf->Get("nom/h_totHT_SR")

TFile * f_TTToHadronic = TFile::Open("../combinedROOT/processedFiles/TTToHadronicMC_2016_processed.root")
TFile * f_TTToSemiLeptonic = TFile::Open("../combinedROOT/processedFiles/TTToSemiLeptonicMC_2016_processed.root")
TFile * f_TTToLeptonic  = TFile::Open("../combinedROOT/processedFiles/TTToLeptonicMC_2016_processed.root")

TH1F * h_TTToHadronic 	  = (TH1F*)f_TTToHadronic->Get("nom/h_totHT_SR")
TH1F * h_TTToSemiLeptonic = (TH1F*)f_TTToSemiLeptonic->Get("nom/h_totHT_SR")
TH1F * h_TTToLeptonic     = (TH1F*)f_TTToLeptonic->Get("nom/h_totHT_SR")

h_QCD1000to1500->Scale(1.482632755)
h_QCD1500to2000->Scale(0.195224041)
h_QCD2000toInf->Scale(0.07572795371)

h_TTToHadronic->Scale(0.05808655696)
h_TTToSemiLeptonic->Scale(0.04236184005)
h_TTToLeptonic->Scale(0.03401684391)



#h_QCD1000to1500->Scale(4.289571744)
#h_QCD1500to2000->Scale(0.4947703875)
#h_QCD2000toInf->Scale(0.2132134533)

#h_TTToHadronic->Scale(0.06588049107)
#h_TTToSemiLeptonic->Scale(0.04563489275)
#h_TTToLeptonic->Scale(0.03617828025)



TH1F * h_QCD_combined = (TH1F*)h_QCD1000to1500->Clone()
h_QCD_combined->Add(h_QCD1500to2000)
h_QCD_combined->Add(h_QCD2000toInf)


TH1F * h_TTbar_combined = (TH1F*)h_TTToHadronic->Clone()
h_TTbar_combined->Add(h_TTToSemiLeptonic)
h_TTbar_combined->Add(h_TTToLeptonic)





TFile * f_WJets1 = TFile::Open("../combinedROOT/processedFiles/WJetsMC_LNu-HT800to1200_2016_processed.root")
TFile * f_WJets2 = TFile::Open("../combinedROOT/processedFiles/WJetsMC_LNu-HT1200to2500_2016_processed.root")
TFile * f_WJets3 = TFile::Open("../combinedROOT/processedFiles/WJetsMC_LNu-HT2500toInf_2016_processed.root")
TFile * f_WJets4 = TFile::Open("../combinedROOT/processedFiles/WJetsMC_QQ-HT800toInf_2016_processed.root")

TH1F * h_WJets1 = (TH1F*)f_WJets1->Get("nom/h_totHT_SR")
TH1F * h_WJets2 = (TH1F*)f_WJets2->Get("nom/h_totHT_SR")
TH1F * h_WJets3  = (TH1F*)f_WJets3->Get("nom/h_totHT_SR")
TH1F * h_WJets4  = (TH1F*)f_WJets4->Get("nom/h_totHT_SR")


h_WJets1->Scale(0.04230432205)
h_WJets2->Scale(0.00932744847)
h_WJets3->Scale(0.0001895618832)
h_WJets4->Scale(0.07139611301)


#h_WJets1->Scale(0.04394190568)
#h_WJets2->Scale(0.01070780024)
#h_WJets3->Scale(0.0002282078928)
#h_WJets4->Scale(0.1266526072)




TH1F * WJets_combined = (TH1F*)h_WJets1->Clone()
WJets_combined->Add(h_WJets2)
WJets_combined->Add(h_WJets3)
WJets_combined->Add(h_WJets4)






TFile * f_dataF = TFile::Open("../combinedROOT/processedFiles/dataF_2016_processed.root")
TFile * f_dataG = TFile::Open("../combinedROOT/processedFiles/dataG_2016_processed.root")
TFile * f_dataH = TFile::Open("../combinedROOT/processedFiles/dataH_2016_processed.root")

TH1F * h_dataF = (TH1F*)f_dataF->Get("nom/h_totHT_SR")
TH1F * h_dataG = (TH1F*)f_dataG->Get("nom/h_totHT_SR")
TH1F * h_dataH  = (TH1F*)f_dataH->Get("nom/h_totHT_SR")

TH1F * h_data_combined = (TH1F*)h_dataF->Clone()
h_data_combined->Add(h_dataG)
h_data_combined->Add(h_dataH)



#TFile * f_dataA = TFile::Open("../combinedROOT/processedFiles/dataA_2016_processed.root")
#TFile * f_dataB = TFile::Open("../combinedROOT/processedFiles/dataB_2016_processed.root")
#TFile * f_dataC = TFile::Open("../combinedROOT/processedFiles/dataC_2016_processed.root")
#TFile * f_dataD = TFile::Open("../combinedROOT/processedFiles/dataD_2016_processed.root")

#TH1F * h_dataA = (TH1F*)f_dataA->Get("nom/h_totHT_SR")
#TH1F * h_dataB = (TH1F*)f_dataB->Get("nom/h_totHT_SR")
#TH1F * h_dataC  = (TH1F*)f_dataC->Get("nom/h_totHT_SR")
#TH1F * h_dataD  = (TH1F*)f_dataD->Get("nom/h_totHT_SR")

#TH1F * h_data_combined = (TH1F*)h_dataA->Clone()
#h_data_combined->Add(h_dataB)
#h_data_combined->Add(h_dataC)
#h_data_combined->Add(h_dataD)


TH1F* h_BR_combined = (TH1F*) h_QCD_combined->Clone()
h_QCD_combined->Add(h_TTbar_combined)
h_QCD_combined->Add(WJets_combined)



h_data_combined->Draw()
h_BR_combined->Draw("HIST,SAME")


c1->SaveAs("h_totHT_SR_dataMC_comparison_2016.png")




