#use the shape of the CR + WJets + TTbar + ST to estimate the SR



TH1F* QCD_SR = (TH1F*)_file0->Get("SR/QCD");
TH1F* TTbar_SR = (TH1F*)_file0->Get("CR/TTTo");
TH1F* WJets_SR = (TH1F*)_file0->Get("SR/WJets");
TH1F* ST_SR = (TH1F*)_file0->Get("SR/ST");
TH1F* data_obs_SR = (TH1F*)_file0->Get("SR/data_obs");



TH1F* QCD_CR = (TH1F*)_file0->Get("CR/QCD");
TH1F* TTbar_CR = (TH1F*)_file0->Get("SR/TTTo");
TH1F* WJets_CR = (TH1F*)_file0->Get("CR/WJets");
TH1F* ST_CR = (TH1F*)_file0->Get("CR/ST");
TH1F* data_obs_CR = (TH1F*)_file0->Get("CR/data_obs");

TTbar_CR->Scale(-1)
WJets_CR->Scale(-1)
ST_CR->Scale(-1)

data_obs_CR->Add(TTbar_CR);
data_obs_CR->Add(WJets_CR);
data_obs_CR->Add(ST_CR);
data_obs_CR->Scale(QCD_SR->Integral() / data_obs_CR->Integral());

data_obs_CR->Add(TTbar_SR )
data_obs_CR->Add(WJets_SR )
data_obs_CR->Add(ST_SR )

data_obs_CR->SetLineColor(kRed);
data_obs_CR->Draw("HIST");
data_obs_SR->Draw("SAME");



TH1F* QCD_AT1b = (TH1F*)_file0->Get("AT1b/QCD");
TH1F* TTbar_AT1b = (TH1F*)_file0->Get("AT0b/TTTo");
TH1F* WJets_AT1b = (TH1F*)_file0->Get("AT1b/WJets");
TH1F* ST_AT1b = (TH1F*)_file0->Get("AT1b/ST");
TH1F* data_obs_AT1b = (TH1F*)_file0->Get("AT1b/data_obs");



TH1F* QCD_AT0b = (TH1F*)_file0->Get("AT0b/QCD");
TH1F* TTbar_AT0b = (TH1F*)_file0->Get("AT1b/TTTo");
TH1F* WJets_AT0b = (TH1F*)_file0->Get("AT0b/WJets");
TH1F* ST_AT0b = (TH1F*)_file0->Get("AT0b/ST");
TH1F* data_obs_AT0b = (TH1F*)_file0->Get("AT0b/data_obs");

TTbar_AT0b->Scale(-1)
WJets_AT0b->Scale(-1)
ST_AT0b->Scale(-1)

data_obs_AT0b->Add(TTbar_AT0b);
data_obs_AT0b->Add(WJets_AT0b);
data_obs_AT0b->Add(ST_AT0b);
data_obs_AT0b->Scale(QCD_AT1b->Integral() / data_obs_AT0b->Integral());


TTbar_AT1b->Scale(3.0)

data_obs_AT0b->Add(TTbar_AT1b )
data_obs_AT0b->Add(WJets_AT1b )
data_obs_AT0b->Add(ST_AT1b )

data_obs_AT0b->SetLineColor(kRed);
data_obs_AT0b->Draw("HIST");
data_obs_AT1b->Draw("SAME");