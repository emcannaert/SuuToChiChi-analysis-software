## compare QCDPT up/nom/down FOR INDIVIDUAL SAMPLE

TFile * QCDMC_Pt_300to470_2017_processed   = TFile::Open("QCDMC_Pt_300to470_2017_processed.root"); 
TFile * QCDMC_Pt_470to600_2017_processed   = TFile::Open("QCDMC_Pt_470to600_2017_processed.root"); 
TFile * QCDMC_Pt_600to800_2017_processed   = TFile::Open("QCDMC_Pt_600to800_2017_processed.root"); 
TFile * QCDMC_Pt_800to1000_2017_processed  = TFile::Open("QCDMC_Pt_800to1000_2017_processed.root"); 
TFile * QCDMC_Pt_1000to1400_2017_processed = TFile::Open("QCDMC_Pt_1000to1400_2017_processed.root"); 
TFile * QCDMC_Pt_1400to1800_2017_processed = TFile::Open("QCDMC_Pt_1400to1800_2017_processed.root"); 
TFile * QCDMC_Pt_1800to2400_2017_processed = TFile::Open("QCDMC_Pt_1800to2400_2017_processed.root"); 
TFile * QCDMC_Pt_2400to3200_2017_processed = TFile::Open("QCDMC_Pt_2400to3200_2017_processed.root"); 
TFile * QCDMC_Pt_3200toInf_2017_processed  = TFile::Open("QCDMC_Pt_3200toInf_2017_processed.root"); 

TH1F * h_QCDMC_Pt_300to470_nom = (TH1F*)QCDMC_Pt_300to470_2017_processed->Get("nom/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_470to600_nom = (TH1F*)QCDMC_Pt_470to600_2017_processed->Get("nom/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_600to800_nom = (TH1F*)QCDMC_Pt_600to800_2017_processed->Get("nom/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_800to1000_nom = (TH1F*)QCDMC_Pt_800to1000_2017_processed->Get("nom/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_1000to1400_nom = (TH1F*)QCDMC_Pt_1000to1400_2017_processed->Get("nom/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_1400to1800_nom = (TH1F*)QCDMC_Pt_1400to1800_2017_processed->Get("nom/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_1800to2400_nom = (TH1F*)QCDMC_Pt_1800to2400_2017_processed->Get("nom/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_2400to3200_nom = (TH1F*)QCDMC_Pt_2400to3200_2017_processed->Get("nom/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_3200toInf_nom = (TH1F*)QCDMC_Pt_3200toInf_2017_processed->Get("nom/h_SJ_mass_SR");

h_QCDMC_Pt_300to470_nom->Scale(2.464537119);
h_QCDMC_Pt_470to600_nom->Scale(0.2122207081);
h_QCDMC_Pt_600to800_nom->Scale(0.04929452011);
h_QCDMC_Pt_800to1000_nom->Scale(0.01443931658);
h_QCDMC_Pt_1000to1400_nom->Scale(0.007643465954);
h_QCDMC_Pt_1400to1800_nom->Scale(0.001150615273);
h_QCDMC_Pt_1800to2400_nom->Scale(0.000324331737);
h_QCDMC_Pt_2400to3200_nom->Scale(0.00003408026676);
h_QCDMC_Pt_3200toInf_nom->Scale(0.000002648864);



TH1F * h_QCDMC_Pt_300to470_up = (TH1F*)QCDMC_Pt_300to470_2017_processed->Get("JEC_Absolute_up/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_470to600_up = (TH1F*)QCDMC_Pt_470to600_2017_processed->Get("JEC_Absolute_up/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_600to800_up = (TH1F*)QCDMC_Pt_600to800_2017_processed->Get("JEC_Absolute_up/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_800to1000_up = (TH1F*)QCDMC_Pt_800to1000_2017_processed->Get("JEC_Absolute_up/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_1000to1400_up = (TH1F*)QCDMC_Pt_1000to1400_2017_processed->Get("JEC_Absolute_up/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_1400to1800_up = (TH1F*)QCDMC_Pt_1400to1800_2017_processed->Get("JEC_Absolute_up/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_1800to2400_up = (TH1F*)QCDMC_Pt_1800to2400_2017_processed->Get("JEC_Absolute_up/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_2400to3200_up = (TH1F*)QCDMC_Pt_2400to3200_2017_processed->Get("JEC_Absolute_up/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_3200toInf_up = (TH1F*)QCDMC_Pt_3200toInf_2017_processed->Get("JEC_Absolute_up/h_SJ_mass_SR");

h_QCDMC_Pt_300to470_up->Scale(2.464537119);
h_QCDMC_Pt_470to600_up->Scale(0.2122207081);
h_QCDMC_Pt_600to800_up->Scale(0.04929452011);
h_QCDMC_Pt_800to1000_up->Scale(0.01443931658);
h_QCDMC_Pt_1000to1400_up->Scale(0.007643465954);
h_QCDMC_Pt_1400to1800_up->Scale(0.001150615273);
h_QCDMC_Pt_1800to2400_up->Scale(0.000324331737);
h_QCDMC_Pt_2400to3200_up->Scale(0.00003408026676);
h_QCDMC_Pt_3200toInf_up->Scale(0.000002648864);



TH1F * h_QCDMC_Pt_300to470_down = (TH1F*)QCDMC_Pt_300to470_2017_processed->Get("JEC_Absolute_down/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_470to600_down = (TH1F*)QCDMC_Pt_470to600_2017_processed->Get("JEC_Absolute_down/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_600to800_down = (TH1F*)QCDMC_Pt_600to800_2017_processed->Get("JEC_Absolute_down/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_800to1000_down = (TH1F*)QCDMC_Pt_800to1000_2017_processed->Get("JEC_Absolute_down/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_1000to1400_down = (TH1F*)QCDMC_Pt_1000to1400_2017_processed->Get("JEC_Absolute_down/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_1400to1800_down = (TH1F*)QCDMC_Pt_1400to1800_2017_processed->Get("JEC_Absolute_down/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_1800to2400_down = (TH1F*)QCDMC_Pt_1800to2400_2017_processed->Get("JEC_Absolute_down/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_2400to3200_down = (TH1F*)QCDMC_Pt_2400to3200_2017_processed->Get("JEC_Absolute_down/h_SJ_mass_SR");
TH1F * h_QCDMC_Pt_3200toInf_down = (TH1F*)QCDMC_Pt_3200toInf_2017_processed->Get("JEC_Absolute_down/h_SJ_mass_SR");

h_QCDMC_Pt_300to470_down->Scale(2.464537119);
h_QCDMC_Pt_470to600_down->Scale(0.2122207081);
h_QCDMC_Pt_600to800_down->Scale(0.04929452011);
h_QCDMC_Pt_800to1000_down->Scale(0.01443931658);
h_QCDMC_Pt_1000to1400_down->Scale(0.007643465954);
h_QCDMC_Pt_1400to1800_down->Scale(0.001150615273);
h_QCDMC_Pt_1800to2400_down->Scale(0.000324331737);
h_QCDMC_Pt_2400to3200_down->Scale(0.00003408026676);
h_QCDMC_Pt_3200toInf_down->Scale(0.000002648864);








h_QCDMC_Pt_300to470_down->SetLineColor(kBlue);
h_QCDMC_Pt_470to600_down->SetLineColor(kBlue);
h_QCDMC_Pt_600to800_down->SetLineColor(kBlue);
h_QCDMC_Pt_800to1000_down->SetLineColor(kBlue);
h_QCDMC_Pt_1000to1400_down->SetLineColor(kBlue);
h_QCDMC_Pt_1400to1800_down->SetLineColor(kBlue);
h_QCDMC_Pt_1800to2400_down->SetLineColor(kBlue);
h_QCDMC_Pt_2400to3200_down->SetLineColor(kBlue);
h_QCDMC_Pt_3200toInf_down->SetLineColor(kBlue);

h_QCDMC_Pt_300to470_down->SetLineWidth(2);
h_QCDMC_Pt_470to600_down->SetLineWidth(2);
h_QCDMC_Pt_600to800_down->SetLineWidth(2);
h_QCDMC_Pt_800to1000_down->SetLineWidth(2);
h_QCDMC_Pt_1000to1400_down->SetLineWidth(2);
h_QCDMC_Pt_1400to1800_down->SetLineWidth(2);
h_QCDMC_Pt_1800to2400_down->SetLineWidth(2);
h_QCDMC_Pt_2400to3200_down->SetLineWidth(2);
h_QCDMC_Pt_3200toInf_down->SetLineWidth(2);

h_QCDMC_Pt_300to470_up->SetLineColor(kRed);
h_QCDMC_Pt_470to600_up->SetLineColor(kRed);
h_QCDMC_Pt_600to800_up->SetLineColor(kRed);
h_QCDMC_Pt_800to1000_up->SetLineColor(kRed);
h_QCDMC_Pt_1000to1400_up->SetLineColor(kRed);
h_QCDMC_Pt_1400to1800_up->SetLineColor(kRed);
h_QCDMC_Pt_1800to2400_up->SetLineColor(kRed);
h_QCDMC_Pt_2400to3200_up->SetLineColor(kRed);
h_QCDMC_Pt_3200toInf_up->SetLineColor(kRed);

h_QCDMC_Pt_300to470_up->SetLineWidth(2);
h_QCDMC_Pt_470to600_up->SetLineWidth(2);
h_QCDMC_Pt_600to800_up->SetLineWidth(2);
h_QCDMC_Pt_800to1000_up->SetLineWidth(2);
h_QCDMC_Pt_1000to1400_up->SetLineWidth(2);
h_QCDMC_Pt_1400to1800_up->SetLineWidth(2);
h_QCDMC_Pt_1800to2400_up->SetLineWidth(2);
h_QCDMC_Pt_2400to3200_up->SetLineWidth(2);
h_QCDMC_Pt_3200toInf_up->SetLineWidth(2);


h_QCDMC_Pt_300to470_up->Draw("HIST")
h_QCDMC_Pt_300to470_nom->Draw("HIST,SAME")
h_QCDMC_Pt_300to470_down->Draw("HIST,SAME")

c1->SaveAs("h_QCDMC_Pt_300to470_JEC_Absolute_upnomdown_2017.png")




h_QCDMC_Pt_470to600_up->Draw("HIST")
h_QCDMC_Pt_470to600_nom->Draw("HIST,SAME")
h_QCDMC_Pt_470to600_down->Draw("HIST,SAME")

c1->SaveAs("h_QCDMC_Pt_470to600_JEC_Absolute_upnomdown_2017.png")



h_QCDMC_Pt_600to800_up->Draw("HIST")
h_QCDMC_Pt_600to800_nom->Draw("HIST,SAME")
h_QCDMC_Pt_600to800_down->Draw("HIST,SAME")

c1->SaveAs("h_QCDMC_Pt_600to800_JEC_Absolute_upnomdown_2017.png")





h_QCDMC_Pt_800to1000_up->Draw("HIST")
h_QCDMC_Pt_800to1000_nom->Draw("HIST,SAME")
h_QCDMC_Pt_800to1000_down->Draw("HIST,SAME")

c1->SaveAs("h_QCDMC_Pt_800to1000_JEC_Absolute_upnomdown_2017.png")






h_QCDMC_Pt_1000to1400_up->Draw("HIST")
h_QCDMC_Pt_1000to1400_nom->Draw("HIST,SAME")
h_QCDMC_Pt_1000to1400_down->Draw("HIST,SAME")

c1->SaveAs("h_QCDMC_Pt_1000to1400_JEC_Absolute_upnomdown_2017.png")






h_QCDMC_Pt_1400to1800_up->Draw("HIST")
h_QCDMC_Pt_1400to1800_nom->Draw("HIST,SAME")
h_QCDMC_Pt_1400to1800_down->Draw("HIST,SAME")

c1->SaveAs("h_QCDMC_Pt_1400to1800_JEC_Absolute_upnomdown_2017.png")





h_QCDMC_Pt_1800to2400_up->Draw("HIST")
h_QCDMC_Pt_1800to2400_nom->Draw("HIST,SAME")
h_QCDMC_Pt_1800to2400_down->Draw("HIST,SAME")

c1->SaveAs("h_QCDMC_Pt_1800to2400_JEC_Absolute_upnomdown_2017.png")



h_QCDMC_Pt_2400to3200_up->Draw("HIST")
h_QCDMC_Pt_2400to3200_nom->Draw("HIST,SAME")
h_QCDMC_Pt_2400to3200_down->Draw("HIST,SAME")

c1->SaveAs("h_QCDMC_Pt_2400to3200_JEC_Absolute_upnomdown_2017.png")



h_QCDMC_Pt_3200toInf_up->Draw("HIST")
h_QCDMC_Pt_3200toInf_nom->Draw("HIST,SAME")
h_QCDMC_Pt_3200toInf_down->Draw("HIST,SAME")

c1->SaveAs("h_QCDMC_Pt_3200toInf_JEC_Absolute_upnomdown_2017.png")



