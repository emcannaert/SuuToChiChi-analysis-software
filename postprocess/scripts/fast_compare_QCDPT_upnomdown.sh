## compare QCDPT up/nom/down

//TFile * QCDMC_Pt_170to300_2015_processed   = TFile::Open("QCDMC_Pt_170to300_2015_processed.root"); 
TFile * QCDMC_Pt_300to470_2015_processed   = TFile::Open("QCDMC_Pt_300to470_2015_processed.root"); 
TFile * QCDMC_Pt_470to600_2015_processed   = TFile::Open("QCDMC_Pt_470to600_2015_processed.root"); 
TFile * QCDMC_Pt_600to800_2015_processed   = TFile::Open("QCDMC_Pt_600to800_2015_processed.root"); 
TFile * QCDMC_Pt_800to1000_2015_processed  = TFile::Open("QCDMC_Pt_800to1000_2015_processed.root"); 
TFile * QCDMC_Pt_1000to1400_2015_processed = TFile::Open("QCDMC_Pt_1000to1400_2015_processed.root"); 
TFile * QCDMC_Pt_1400to1800_2015_processed = TFile::Open("QCDMC_Pt_1400to1800_2015_processed.root"); 
TFile * QCDMC_Pt_1800to2400_2015_processed = TFile::Open("QCDMC_Pt_1800to2400_2015_processed.root"); 
TFile * QCDMC_Pt_2400to3200_2015_processed = TFile::Open("QCDMC_Pt_2400to3200_2015_processed.root"); 
TFile * QCDMC_Pt_3200toInf_2015_processed  = TFile::Open("QCDMC_Pt_3200toInf_2015_processed.root"); 

//TH1F * h_1_nom = (TH1F*)QCDMC_Pt_170to300_2015_processed->Get("nom/h_SJ_mass_uncorrected");
TH1F * h_2_nom = (TH1F*)QCDMC_Pt_300to470_2015_processed->Get("nom/h_SJ_mass_uncorrected");
TH1F * h_3_nom = (TH1F*)QCDMC_Pt_470to600_2015_processed->Get("nom/h_SJ_mass_uncorrected");
TH1F * h_4_nom = (TH1F*)QCDMC_Pt_600to800_2015_processed->Get("nom/h_SJ_mass_uncorrected");
TH1F * h_5_nom = (TH1F*)QCDMC_Pt_800to1000_2015_processed->Get("nom/h_SJ_mass_uncorrected");
TH1F * h_6_nom = (TH1F*)QCDMC_Pt_1000to1400_2015_processed->Get("nom/h_SJ_mass_uncorrected");
TH1F * h_7_nom = (TH1F*)QCDMC_Pt_1400to1800_2015_processed->Get("nom/h_SJ_mass_uncorrected");
TH1F * h_8_nom = (TH1F*)QCDMC_Pt_1800to2400_2015_processed->Get("nom/h_SJ_mass_uncorrected");
TH1F * h_9_nom = (TH1F*)QCDMC_Pt_2400to3200_2015_processed->Get("nom/h_SJ_mass_uncorrected");
TH1F * h_10_nom = (TH1F*)QCDMC_Pt_3200toInf_2015_processed->Get("nom/h_SJ_mass_uncorrected");

//h_1_nom->Scale(72.27560548);
h_2_nom->Scale(2.464537119);
h_3_nom->Scale(0.2122207081);
h_4_nom->Scale(0.04929452011);
h_5_nom->Scale(0.01443931658);
h_6_nom->Scale(0.007643465954);
h_7_nom->Scale(0.001150615273);
h_8_nom->Scale(0.000324331737);
h_9_nom->Scale(0.00003408026676);
h_10_nom->Scale(0.000002648864);

//h_1_nom->Add(h_2_nom);
h_2_nom->Add(h_3_nom);
h_2_nom->Add(h_4_nom);
h_2_nom->Add(h_5_nom);
h_2_nom->Add(h_6_nom);
h_2_nom->Add(h_7_nom);
h_2_nom->Add(h_8_nom);
h_2_nom->Add(h_9_nom);
h_2_nom->Add(h_10_nom);


//TH1F * h_1_up = (TH1F*)QCDMC_Pt_170to300_2015_processed->Get("JEC_up/h_SJ_mass_uncorrected");
TH1F * h_2_up = (TH1F*)QCDMC_Pt_300to470_2015_processed->Get("JEC_up/h_SJ_mass_uncorrected");
TH1F * h_3_up = (TH1F*)QCDMC_Pt_470to600_2015_processed->Get("JEC_up/h_SJ_mass_uncorrected");
TH1F * h_4_up = (TH1F*)QCDMC_Pt_600to800_2015_processed->Get("JEC_up/h_SJ_mass_uncorrected");
TH1F * h_5_up = (TH1F*)QCDMC_Pt_800to1000_2015_processed->Get("JEC_up/h_SJ_mass_uncorrected");
TH1F * h_6_up = (TH1F*)QCDMC_Pt_1000to1400_2015_processed->Get("JEC_up/h_SJ_mass_uncorrected");
TH1F * h_7_up = (TH1F*)QCDMC_Pt_1400to1800_2015_processed->Get("JEC_up/h_SJ_mass_uncorrected");
TH1F * h_8_up = (TH1F*)QCDMC_Pt_1800to2400_2015_processed->Get("JEC_up/h_SJ_mass_uncorrected");
TH1F * h_9_up = (TH1F*)QCDMC_Pt_2400to3200_2015_processed->Get("JEC_up/h_SJ_mass_uncorrected");
TH1F * h_10_up = (TH1F*)QCDMC_Pt_3200toInf_2015_processed->Get("JEC_up/h_SJ_mass_uncorrected");

//h_1_up->Scale(72.27560548);
h_2_up->Scale(2.464537119);
h_3_up->Scale(0.2122207081);
h_4_up->Scale(0.04929452011);
h_5_up->Scale(0.01443931658);
h_6_up->Scale(0.007643465954);
h_7_up->Scale(0.001150615273);
h_8_up->Scale(0.000324331737);
h_9_up->Scale(0.00003408026676);
h_10_up->Scale(0.000002648864);

//h_1_up->Add(h_2_up);
h_2_up->Add(h_3_up);
h_2_up->Add(h_4_up);
h_2_up->Add(h_5_up);
h_2_up->Add(h_6_up);
h_2_up->Add(h_7_up);
h_2_up->Add(h_8_up);
h_2_up->Add(h_9_up);
h_2_up->Add(h_10_up);

//TH1F * h_1_down = (TH1F*)QCDMC_Pt_170to300_2015_processed->Get("JEC_down/h_SJ_mass_uncorrected");
TH1F * h_2_down = (TH1F*)QCDMC_Pt_300to470_2015_processed->Get("JEC_down/h_SJ_mass_uncorrected");
TH1F * h_3_down = (TH1F*)QCDMC_Pt_470to600_2015_processed->Get("JEC_down/h_SJ_mass_uncorrected");
TH1F * h_4_down = (TH1F*)QCDMC_Pt_600to800_2015_processed->Get("JEC_down/h_SJ_mass_uncorrected");
TH1F * h_5_down = (TH1F*)QCDMC_Pt_800to1000_2015_processed->Get("JEC_down/h_SJ_mass_uncorrected");
TH1F * h_6_down = (TH1F*)QCDMC_Pt_1000to1400_2015_processed->Get("JEC_down/h_SJ_mass_uncorrected");
TH1F * h_7_down = (TH1F*)QCDMC_Pt_1400to1800_2015_processed->Get("JEC_down/h_SJ_mass_uncorrected");
TH1F * h_8_down = (TH1F*)QCDMC_Pt_1800to2400_2015_processed->Get("JEC_down/h_SJ_mass_uncorrected");
TH1F * h_9_down = (TH1F*)QCDMC_Pt_2400to3200_2015_processed->Get("JEC_down/h_SJ_mass_uncorrected");
TH1F * h_10_down = (TH1F*)QCDMC_Pt_3200toInf_2015_processed->Get("JEC_down/h_SJ_mass_uncorrected");

//h_1_down->Scale(72.27560548);
h_2_down->Scale(2.464537119);
h_3_down->Scale(0.2122207081);
h_4_down->Scale(0.04929452011);
h_5_down->Scale(0.01443931658);
h_6_down->Scale(0.007643465954);
h_7_down->Scale(0.001150615273);
h_8_down->Scale(0.000324331737);
h_9_down->Scale(0.00003408026676);
h_10_down->Scale(0.000002648864);


//h_1_down->Add(h_2_down);
h_2_down->Add(h_3_down);
h_2_down->Add(h_4_down);
h_2_down->Add(h_5_down);
h_2_down->Add(h_6_down);
h_2_down->Add(h_7_down);
h_2_down->Add(h_8_down);
h_2_down->Add(h_9_down);
h_2_down->Add(h_10_down);


h_2_down->SetLineColor(kBlue);
h_2_up->SetLineColor(kRed);


h_2_up->Draw("HIST")
h_2_nom->Draw("HIST,SAME")
h_2_down->Draw("HIST,SAME")

# compare h_AK8_JER, 

# h_SJ_mass_uncorrected
# h_SJ_mass_uncorrected
# h_disuperjet_mass_uncorrected


