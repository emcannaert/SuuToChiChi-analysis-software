#include <iostream>

using namespace std;



void calc_signal_eff()
{



	std::vector<std::string> YEARS = {"2015","2016","2017","2018"};


	//##### TO CHANGE ////
	//std::string YEAR="2015";
	std::string MASS_POINT="Suu8_chi3";
	//


	for(auto YEAR: YEARS)
	{

		TString WBWB_scale_str_inp = ("python print_single_signal_xs.py --year " + YEAR +  " --mass_point "+ MASS_POINT +" --decay WBWB" ).c_str();
		TString HTHT_scale_str_inp = ("python print_single_signal_xs.py --year " + YEAR +  " --mass_point "+ MASS_POINT +" --decay HTHT" ).c_str();
		TString ZTZT_scale_str_inp = ("python print_single_signal_xs.py --year " + YEAR +  " --mass_point "+ MASS_POINT +" --decay ZTZT" ).c_str();
		TString WBHT_scale_str_inp = ("python print_single_signal_xs.py --year " + YEAR +  " --mass_point "+ MASS_POINT +" --decay WBHT" ).c_str();
		TString WBZT_scale_str_inp = ("python print_single_signal_xs.py --year " + YEAR +  " --mass_point "+ MASS_POINT +" --decay WBZT" ).c_str();
		TString HTZT_scale_str_inp = ("python print_single_signal_xs.py --year " + YEAR +  " --mass_point "+ MASS_POINT +" --decay HTZT" ).c_str();

		TString WBWB_scale_str = gSystem->GetFromPipe(WBWB_scale_str_inp );
		TString HTHT_scale_str = gSystem->GetFromPipe(HTHT_scale_str_inp );
		TString ZTZT_scale_str = gSystem->GetFromPipe(ZTZT_scale_str_inp );
		TString WBHT_scale_str = gSystem->GetFromPipe(WBHT_scale_str_inp );
		TString WBZT_scale_str = gSystem->GetFromPipe(WBZT_scale_str_inp );
		TString HTZT_scale_str = gSystem->GetFromPipe(HTZT_scale_str_inp );

		double WBWB_scale = WBWB_scale_str.Atof();
		double HTHT_scale = HTHT_scale_str.Atof();
		double ZTZT_scale = ZTZT_scale_str.Atof();
		double WBHT_scale = WBHT_scale_str.Atof();
		double WBZT_scale = WBZT_scale_str.Atof();
		double HTZT_scale = HTZT_scale_str.Atof();


		//std::cout << WBWB_scale <<std::endl;
		//std::cout << HTHT_scale <<std::endl;
		//std::cout << ZTZT_scale <<std::endl;
		//std::cout << WBHT_scale <<std::endl;
		//std::cout << WBZT_scale <<std::endl;
		//std::cout << HTZT_scale <<std::endl;



		TFile * WBWB_file = TFile::Open( ("root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/" + MASS_POINT +  "_WBWB_" + YEAR +"_processed.root").c_str(),"READ");
		TH1F * WBWB_hist = (TH1F*)WBWB_file->Get("nom/h_SJ_mass_SR");

		TFile * HTHT_file = TFile::Open( ("root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/" + MASS_POINT +  "_HTHT_" + YEAR +"_processed.root").c_str(),"READ");
		TH1F * HTHT_hist = (TH1F*)HTHT_file->Get("nom/h_SJ_mass_SR");

		TFile * ZTZT_file = TFile::Open( ("root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/" + MASS_POINT +  "_ZTZT_" + YEAR +"_processed.root").c_str(),"READ");
		TH1F * ZTZT_hist = (TH1F*)ZTZT_file->Get("nom/h_SJ_mass_SR");

		TFile * WBHT_file = TFile::Open( ("root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/" + MASS_POINT +  "_WBHT_" + YEAR +"_processed.root").c_str(),"READ");
		TH1F * WBHT_hist = (TH1F*)WBHT_file->Get("nom/h_SJ_mass_SR");

		TFile * WBZT_file = TFile::Open( ("root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/" + MASS_POINT +  "_WBZT_" + YEAR +"_processed.root").c_str(),"READ");
		TH1F * WBZT_hist = (TH1F*)WBZT_file->Get("nom/h_SJ_mass_SR");

		TFile * HTZT_file = TFile::Open( ("root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/" + MASS_POINT +  "_HTZT_" + YEAR +"_processed.root").c_str(),"READ");
		TH1F * HTZT_hist = (TH1F*)HTZT_file->Get("nom/h_SJ_mass_SR");

		//////////////////////////////

		WBWB_hist->Scale(WBWB_scale);
		HTHT_hist->Scale(HTHT_scale);
		ZTZT_hist->Scale(ZTZT_scale);
		WBHT_hist->Scale(WBHT_scale);
		WBZT_hist->Scale(WBZT_scale);
		HTZT_hist->Scale(HTZT_scale);

		TH1F * combined_sig = (TH1F*)WBWB_hist->Clone("combined_sig");
		combined_sig->Add(HTHT_hist);
		combined_sig->Add(ZTZT_hist);
		combined_sig->Add(WBHT_hist);
		combined_sig->Add(WBZT_hist);
		combined_sig->Add(HTZT_hist);

		TCanvas * c1 = new TCanvas("","",1200,1000);

		combined_sig->Draw("HIST");

		c1->SaveAs("test_hist.png");




		////////// CHANGE ///////

		double x1 = 2300;
		double x2 = 3300;

		////




		int bin1 = combined_sig->FindBin(x1);
		int bin2 = combined_sig->FindBin(x2);

		double good_integral = combined_sig->Integral(bin1, bin2);
		double bad_integral = combined_sig->Integral() - good_integral;

		std::cout <<  "For year " <<  YEAR << ", approximately " << good_integral / combined_sig->Integral() << " of superjets are correctly sorted." << std::endl;
	}


	
	return;
}




