#include <iostream>
#include <string>
#include "TLorentzVector.h"
#include "TRatioPlot.h"
#include "THStack.h"

using namespace std;

double SuuToChiChi_MSuu8TeV_Mchi3TeV_SF = 1.93E-02;
double SuuToChiChi_MSuu5TeV_Mchi2TeV_SF = 8.67E-01;

double QCD1000to1500_SF[4] = {1.578683216,1.482632755,3.126481451,4.407417122};
double QCD1500to2000_SF[4] = {0.2119142341,0.195224041,0.3197450474,0.5425809983}; 
double QCD2000toInf_SF[4] = {0.08568186031,0.07572795371,0.14306915,0.2277769275}; 
double h_TTToHadronic_SF[4] = {0.075592,0.05808655696,0.06651018525,0.06588049107}; 
double h_TTToSemiLeptonic_SF[4] = {0.05395328118,0.05808655696,0.04264829286,0.04563489275}; 
double h_TTTo2l2nu_SF[4] = {0.0459517611,0.03401684391,0.03431532926,0.03617828025}; 

double h_TTJetsMCHT800to1200_SF[4]   = {0.002884466085,0.002526405224,0.003001100916,0.004897196802};
double h_TTJetsMCHT1200to2500_SF[4]  = {0.002722324842,0.002255554525,0.002675947994,0.003918532089};
double h_TTJetsMCHT2500toInf_SF[4]   = {0.00005679863673,0.00005025384367,0.00005947217017,0.00008408965681};
double ST_t_channel_top_5f_SF[4]     = {0.0409963154,0.03607115071,0.03494669125,0.03859114659}; 
double ST_t_channel_antitop_5f_SF[4] = {0.05673857623,0.04102705994,0.04238814865,0.03606630944}; 
double ST_s_channel_4f_hadrons_SF[4] = {0.04668187234,0.03564988679,0.03985938616,0.04102795437}; 
double ST_s_channel_4f_leptons_SF[4] = {0.01323030083,0.01149139097,0.01117527734,0.01155448784}; 
double ST_tW_antitop_5f_SF[4] = {0.2967888696,0.2301666797,0.2556495594,0.2700032391}; 
double ST_tW_top_5f_SF[4] = {0.2962796522,0.2355829386,0.2563403788,0.2625270613}; 

double WJetsMC_LNu_HT800to1200_SF[4] = {0.04172270958,0.04230432205,0.04374224695,0.04394190568}; 
double WJetsMC_LNu_HT1200to2500_SF[4] = {0.01068088067,0.00932744847,0.009709510545,0.01070780024}; 
double WJetsMC_LNu_HT2500toInf_SF[4] = {0.0001931363546,0.0001895618832,0.0002799036518,0.0007547032677}; 
double WJetsMC_QQ_HT800toInf_SF[4] = {0.072501767,0.07139611301,0.08100232455,0.128194465}; 

double QCDMC_Pt_170to300_SF[4] = {72.27560548, 58.13790684, 144.0132837, 208.6671047}; 
double QCDMC_Pt_300to470_SF[4] = {2.464537119, 2.077524247, 5.087240079, 7.056447936}; 
double QCDMC_Pt_470to600_SF[4] = {0.2122207081, 0.1770874866, 0.4500561659, 0.6298074855}; 
double QCDMC_Pt_600to800_SF[4] = {0.04929452011, 0.04041858714, 0.09634485522, 0.1387005244}; 
double QCDMC_Pt_800to1000_SF[4] = {0.01443931658, 0.01169252025, 0.02954986175, 0.04231249731}; 
double QCDMC_Pt_1000to1400_SF[4] = {0.007643465954, 0.006312623165, 0.01566430413, 0.0226523112}; 
double QCDMC_Pt_1400to1800_SF[4] = {0.001150615273, 0.001016564447, 0.00244639185, 0.003532486979}; 
double QCDMC_Pt_1800to2400_SF[4] = {0.000324331737, 0.0002806910428, 0.0006608229592, 0.000952638299}; 
double QCDMC_Pt_2400to3200_SF[4] = {0.00003408026676, 0.00003090490169, 0.00007246889556, 0.0001045278212}; 
double QCDMC_Pt_3200toInf_SF[4] = {0.000002648864, 0.000002290278112, 0.000005628836, 0.000008118931}; 


void write_cms_text(double CMS_label_pos, double SIM_label_pos, double CMS_label_posy, double SIM_label_posy,  TCanvas * canvas, bool noStats) {
    // do all the fancy formatting 
    //gStyle->SetOptStat(0);
    
    TText *CMSLabel = new TText();
    CMSLabel->SetNDC();
    CMSLabel->SetTextFont(1);
    CMSLabel->SetTextColor(1);
    CMSLabel->SetTextSize(0.0385);
    CMSLabel->SetTextAlign(22);
    CMSLabel->SetTextAngle(0);
    CMSLabel->DrawText(CMS_label_pos, CMS_label_posy, "CMS");
    CMSLabel->Draw();
    
    TText *simLabel = new TText();
    simLabel->SetNDC();
    simLabel->SetTextFont(52);
    simLabel->SetTextColor(1);
    simLabel->SetTextSize(0.024);
    simLabel->SetTextAlign(22);
    simLabel->SetTextAngle(0);
    simLabel->DrawText(SIM_label_pos, SIM_label_posy, "Private Work (CMS Simulation)");
    simLabel->Draw();
    
    TLatex *latex = new TLatex();
    TString lumistuff = "(13 TeV)";
    latex->SetNDC();
    latex->SetTextAngle(0);
    latex->SetTextColor(kBlack);  
    latex->SetTextFont(42);
    latex->SetTextAlign(31);
    latex->SetTextSize(0.030); 
    if (!noStats)  latex->DrawLatex(0.75, 0.91, lumistuff.Data());
    else { latex->DrawLatex(0.89, 0.91, lumistuff.Data()) ;}
    canvas->Update();
    delete CMSLabel;
    delete simLabel;
    delete latex;
}

void SetLogScaleYAxis(THStack* stack, TCanvas * canvas) 
{
    // Iterate over histograms in the THStack
    TList* list = stack->GetHists();
    if (!list) return;

    Double_t ymin = DBL_MAX;
    Double_t ymax = -DBL_MAX;

    Int_t numHistograms = list->GetSize();
    for (Int_t iii = 0; iii < numHistograms; ++iii) 
    {
        TH1* hist = dynamic_cast<TH1*>(list->At(iii));

        if (!hist)
        {
          std::cout << "Bad histogram inside stack. Returning." << std::endl;
          return;
        }

        Double_t histMax = hist->GetMaximum();

        for (Int_t i = 1; i <= hist->GetNbinsX(); ++i) 
        {
          Double_t binContent = hist->GetBinContent(i);
          if ( (binContent > 0) && (binContent < ymin) )
          {
              ymin = binContent;
          }
        }

        if (histMax > ymax)
        {
          //std::cout << "New xmax: from" << xmax << " to " << binCenter << ". In this bin there is content " << content << std::endl;
          ymax = histMax;
        } 
    }

    // need the minimum value that is non-zero
    stack->SetMinimum(ymin);
    stack->SetMaximum(ymax);

    gPad->SetLogy();
    //canvas->SetLeftMargin(0.15);
    //canvas->SetBottomMargin(0.15);
    canvas->Update();

}
void SetLogScaleZAxis(TH2F * hist, TCanvas * canvas) 
{
    // Iterate over histograms in the THStack

    Double_t zmin = DBL_MAX;
    Double_t zmax = -DBL_MAX;


    Double_t histMax = hist->GetMaximum();

    for (Int_t i = 1; i <= hist->GetNbinsX(); ++i) 
    {
      for (Int_t j = 1; j <= hist->GetNbinsY(); ++j) 
      {
        Double_t binContent = hist->GetBinContent(i,j);
        if ( (binContent > 0) && (binContent < zmin) )
        {
            zmin = binContent;
        }
      }

    }

    if (histMax > zmax)
    {
      //std::cout << "New xmax: from" << xmax << " to " << binCenter << ". In this bin there is content " << content << std::endl;
      zmax = histMax;
    } 

    // need the minimum value that is non-zero
    hist->SetMinimum(zmin);
    hist->SetMaximum(zmax);

    gPad->SetLogz();
    //canvas->SetLeftMargin(0.15);
    //canvas->SetBottomMargin(0.15);
    canvas->Update();

}
void setDynamicXScale(TH1* hist) {
    if (!hist) {
        std::cerr << "Error: Histogram is null." << std::endl;
        return;
    }

    Double_t xmin = DBL_MAX;
    Double_t xmax = -DBL_MAX;

    Int_t nBins = hist->GetNbinsX();
    for (Int_t i = 1; i <= nBins; ++i) {
        Double_t content = hist->GetBinContent(i);
        if (content > 0) {
            Double_t binCenter = hist->GetBinCenter(i);
            if (binCenter < xmin) xmin = binCenter;
            if (binCenter > xmax) xmax = binCenter;
        }
    }

    // Set x-axis scale dynamically
    Double_t xRange = xmax - xmin;

    hist->GetXaxis()->SetRangeUser(xmin *0.75, xmax*1.25);
}


void setDynamicXScale(THStack* stack) {
    if (!stack) 
    {
        std::cerr << "Error: THStack is null." << std::endl;
        return;
    }

    Double_t xmin = DBL_MAX;
    Double_t xmax = -DBL_MAX;

    TList* list = stack->GetHists();

    Int_t numHistograms = list->GetSize();
    for (Int_t iii = 0; iii < numHistograms; ++iii) 
    {
        TH1* hist = dynamic_cast<TH1*>(list->At(iii));

        if (!hist)
        {
          std::cout << "Bad histogram inside stack. Returning." << std::endl;
          return;
        }

        Int_t nBins = hist->GetNbinsX();
        for (Int_t jjj = 1; jjj <= nBins; ++jjj) 
        {
            Double_t content = hist->GetBinContent(jjj);
            if (content > 0) 
            {
                Double_t binCenter = hist->GetBinCenter(jjj);
                if (binCenter < xmin)
                {
                  //std::cout << "New xmin: from" << xmin << " to " << binCenter << ". In this bin there is content " << content << std::endl;
                  xmin = binCenter;
                } 
                if (binCenter > xmax)
                {
                  //std::cout << "New xmax: from" << xmax << " to " << binCenter << ". In this bin there is content " << content << std::endl;
                  xmax = binCenter;
                } 
            }
        }
    }

    stack->GetXaxis()->SetLimits(xmin*0.9, xmax*1.1);



    /*
    // set the range of each sub-histogram 
    Int_t numHistograms = list->GetSize();
    for (Int_t i = 0; i < numHistograms; ++i) 
    {
        TH1* hist = dynamic_cast<TH1*>(list->At(i));
        if (hist) 
        {
           hist->GetXaxis()->SetRangeUser(xmin*0.75, xmax*1.25);
        }
    } 
    */
}

template <typename T> std::vector<T> get_histograms(std::vector<std::string> fnames, std::string hist_name, std::string folderName)
{

    std::cout << "Looking for histname " << hist_name << " and folder name " << folderName << std::endl;

    TH1::AddDirectory(false);

    std::string folder_str = "";
    if(folderName != "")
    {
      folder_str = folderName;
    }

    std::vector<T> return_files;
    std::cout <<fnames.size() << " files found. " << std::endl;

    for(auto iii = fnames.begin();iii<fnames.end();iii++)
    {
      std::cout << "looking for histogram " << (folderName+hist_name).c_str() << " in " << *iii <<std::endl;

      TFile * f1 = TFile::Open((*iii).c_str(), "READ" ); // open TFile for each fname
      return_files.push_back( (T) f1->Get(  (folderName+hist_name).c_str() )  );
      f1->Close();
      delete f1;
      //std::cout << "File: " << typeid((T)(*iii)->Get( ("nom_/" + hist_name).c_str() )).name() << " " << std::endl;
    }
    std::cout << std::endl;
    return return_files;
}

template <typename T> T combine_histograms(std::vector<T> _hists, double weights[])
{
  

  TH1::AddDirectory(false);

  T first_hist_scaled = T(_hists[0]);
  double original_events = first_hist_scaled->Integral();

  first_hist_scaled->Scale(weights[0]);

  T comb_hist = T(first_hist_scaled);
  int counter = 0;
  for(auto iii = _hists.begin() + 1;iii<_hists.end();iii++)
  {

    original_events = (*iii)->Integral();
    T dummy_hist = T(*iii);
    dummy_hist->Scale(weights[counter+1]);
    //(*iii)->Scale(weights[counter+1]);
    comb_hist->Add(dummy_hist);
    counter++;
  }
  return comb_hist;
}


template <typename T> void create_plots(std::vector<std::string> dataFiles, std::vector<std::string> QCDFiles, std::vector<std::string> TTbarFiles, std::vector<std::string> WJetsFiles,  std::vector<std::string> STFiles, double QCD_weights[], double TTbar_weights[], double WJets_weights[], double ST_weights[], std::string histName, std::string year,bool makeStack = false, bool makeLog = false, bool noStats = false, std::string plotName = "", std::string plot_description = "", std::string folderName = ""  )
{


  TH1::AddDirectory(false);

  std::cout << "Running year " << year << " and hist name " << histName<< std::endl;

  std::string year_str = "2016preAPV";
  if (year == "2016") year_str = "2016postAPV";
  else if (year == "2017") year_str = "2017";
  else if (year == "2018") year_str = "2018";

  //double h_TTJets2500toInf_SF  = 0.00008408965681;
  TCanvas *c1 = new TCanvas("c1","",400,20, 1250,1000);

  if(!makeStack)     // This means this is a TH2F, create more room on the right side of plot
  {
    c1->SetRightMargin(0.16);
  }

  std::string plot_home = "plots/combinedSamplePlots/";
  if(plotName == "") plotName = histName;

  std::string getName = histName;

  double weights_data[20];
  std::fill_n(weights_data, 20, 1.0); //dummy weights for data

  double CMS_label_pos = 0.152;
  double SIM_label_pos = 0.31;

  double CMS_label_posy = 0.925;
  double SIM_label_posy = 0.921; 

  if(makeLog) gPad->SetLogy();
  if(noStats) gStyle->SetOptStat(0);
  else{ gStyle->SetOptStat(1111);}

  
  std::vector<T>  h_TTbar_hists    = get_histograms<T>(TTbarFiles, getName.c_str(), folderName);
  T  h_all_TTbar_MC    = combine_histograms<T>(h_TTbar_hists,TTbar_weights);
  h_all_TTbar_MC->SetTitle((plot_description + " (" +year_str+  " combined TTbar MC)").c_str());
  
  std::cout << "Got TTbar histograms" << std::endl;

  std::vector<T>  h_WJets_hists    = get_histograms<T>(WJetsFiles, getName.c_str(), folderName);
  T  h_all_WJets_MC    = combine_histograms<T>(h_WJets_hists,WJets_weights);
  h_all_WJets_MC->SetTitle((plot_description + " (" +year_str+  " combined WJets MC)").c_str());

  std::cout << "Got WJets histograms" << std::endl;


  //std::cout << "Loading data files." << std::endl;
  //std::vector<T>  h_data_hists  = get_histograms<T>(dataFiles, getName.c_str());
  //std::cout << "Loading MC files." << std::endl;
  std::vector<T>  h_QCD_hists    = get_histograms<T>(QCDFiles, getName.c_str(), folderName);
  std::vector<T>  h_ST_hists    = get_histograms<T>(STFiles, getName.c_str(), folderName);


  //T  h_all_data    = combine_histograms<T>(h_data_hists,weights_data);
  //std::cout << "Data integral is " << h_all_data->Integral() << std::endl;
  T  h_all_QCD_MC      = combine_histograms<T>(h_QCD_hists,QCD_weights);
  T  h_all_ST_MC       = combine_histograms<T>(h_ST_hists,ST_weights);

  //std::cout << "MC integral is " << h_all_MC->Integral() << std::endl;

  //h_all_data->SetTitle((plotName + " (" +*year+  "data)").c_str());
  h_all_QCD_MC->SetTitle((plot_description + " (" +year_str+  " combined QCD MC)").c_str());
  std::cout << "Gtt QCD histograms" << std::endl;

  h_all_ST_MC->SetTitle((plot_description + " (" +year_str+  " combined ST MC)").c_str());
  std::cout << "Got ST histograms" << std::endl;




  if(!makeStack)
  {

        double CMS_label_pos = 0.152;
        double SIM_label_pos = 0.235;

        double CMS_label_posy = 0.875;
        double SIM_label_posy = 0.84; 
 

        gStyle->SetPalette(kViridis);
        TColor::InvertPalette(); // reverse the order of the color palette

        h_all_TTbar_MC->GetZaxis()->SetTitle("Events");
        h_all_TTbar_MC->GetZaxis()->SetTitleOffset(1.35);
        h_all_TTbar_MC->GetZaxis()->SetTitleSize(0.035);
        h_all_TTbar_MC->GetZaxis()->SetLabelSize(0.035);
        h_all_TTbar_MC->GetZaxis()->SetLabelOffset(0.005);

        std::string updated_y_title = std::string(h_all_TTbar_MC->GetYaxis()->GetTitle())  + " [GeV]";

        h_all_TTbar_MC->GetYaxis()->SetTitle( updated_y_title.c_str() );
        h_all_QCD_MC->GetYaxis()->SetTitle( updated_y_title.c_str() );
        h_all_WJets_MC->GetYaxis()->SetTitle( updated_y_title.c_str() );
        h_all_ST_MC->GetYaxis()->SetTitle( updated_y_title.c_str() );

        h_all_QCD_MC->GetZaxis()->SetTitle("Events");
        h_all_QCD_MC->GetZaxis()->SetTitleOffset(1.35);
        h_all_QCD_MC->GetZaxis()->SetTitleSize(0.035);
        h_all_QCD_MC->GetZaxis()->SetLabelSize(0.035);
        h_all_QCD_MC->GetZaxis()->SetLabelOffset(0.005);

        h_all_WJets_MC->GetZaxis()->SetTitle("Events");
        h_all_WJets_MC->GetZaxis()->SetTitleOffset(1.35);
        h_all_WJets_MC->GetZaxis()->SetTitleSize(0.035);
        h_all_WJets_MC->GetZaxis()->SetLabelSize(0.035);
        h_all_WJets_MC->GetZaxis()->SetLabelOffset(0.005);


        h_all_ST_MC->GetZaxis()->SetTitle("Events");
        h_all_ST_MC->GetZaxis()->SetTitleOffset(1.35);
        h_all_ST_MC->GetZaxis()->SetTitleSize(0.035);
        h_all_ST_MC->GetZaxis()->SetLabelSize(0.035);
        h_all_ST_MC->GetZaxis()->SetLabelOffset(0.005);

      if( (histName.find("h_MSJ_mass_vs_MdSJ") != std::string::npos)   ) 
      {
        TH2F * dummy_h2 = (TH2F*)h_all_QCD_MC;
        SetLogScaleZAxis(h_all_TTbar_MC, c1);
        SetLogScaleZAxis(h_all_QCD_MC, c1);
        SetLogScaleZAxis(h_all_WJets_MC, c1);
        SetLogScaleZAxis(h_all_ST_MC, c1);

        SetLogScaleZAxis(dummy_h2, c1);
      }

      h_all_TTbar_MC->GetYaxis()->SetTitleOffset(1.5);
      h_all_TTbar_MC->Draw("colz");
      write_cms_text(CMS_label_pos,SIM_label_pos,CMS_label_posy, SIM_label_posy, c1, noStats);
      c1->SaveAs( (plot_home + plotName +"_TTbar_combined_"+ year+".png").c_str());
      if(plotName == "top_pt_weight")return; // these are only saved for top datasets
      h_all_QCD_MC->GetYaxis()->SetTitleOffset(1.5);
      h_all_QCD_MC->Draw("colz");
      write_cms_text(CMS_label_pos,SIM_label_pos,CMS_label_posy, SIM_label_posy, c1, noStats);
      c1->SaveAs( (plot_home + plotName +"_QCDMC_combined_"+ year+".png").c_str()); 

      h_all_WJets_MC->GetYaxis()->SetTitleOffset(1.5);
      h_all_WJets_MC->Draw("colz");
      write_cms_text(CMS_label_pos,SIM_label_pos,CMS_label_posy, SIM_label_posy, c1, noStats);
      c1->SaveAs( (plot_home + plotName +"_WJetsMC_combined_"+ year+".png").c_str()); 


      h_all_ST_MC->GetYaxis()->SetTitleOffset(1.5);
      h_all_ST_MC->Draw("colz");
      write_cms_text(CMS_label_pos,SIM_label_pos,CMS_label_posy, SIM_label_posy, c1, noStats);
      c1->SaveAs( (plot_home + plotName +"_STMC_combined_"+ year+".png").c_str()); 


      //backup: non-stack, combined plot
      T h_allBR = (T)h_all_QCD_MC->Clone();
      h_allBR->Add(h_all_TTbar_MC);
      h_allBR->Add(h_all_WJets_MC);
      h_allBR->Add(h_all_ST_MC);
      h_allBR->SetTitle((plot_description + " (" +year_str+  ") (Combined BR)").c_str());

      h_allBR->GetZaxis()->SetTitle("Events");
      h_allBR->GetZaxis()->SetTitleOffset(1.35);
      h_allBR->GetZaxis()->SetTitleSize(0.035);
      h_allBR->GetZaxis()->SetLabelSize(0.035);
      h_allBR->GetZaxis()->SetLabelOffset(0.005);




      if( (histName.find("h_MSJ_mass_vs_MdSJ") != std::string::npos)   ) 
      {
        TH2F * dummy_h2 = (TH2F*)h_allBR;
        SetLogScaleZAxis(h_allBR, c1);
	      SetLogScaleZAxis(dummy_h2, c1);
      }

      h_allBR->GetYaxis()->SetTitleOffset(1.5);
      h_allBR->Draw("colz");
      write_cms_text(CMS_label_pos,SIM_label_pos,CMS_label_posy, SIM_label_posy, c1, noStats);

      c1->SaveAs( (plot_home + plotName +"_allBR_"+ year+".png").c_str()); 
      return;  /// ?
  }
  else
  {    


      setDynamicXScale( h_all_TTbar_MC );
      h_all_TTbar_MC->Draw("HIST");
      write_cms_text(CMS_label_pos,SIM_label_pos,CMS_label_posy, SIM_label_posy, c1, noStats);
      c1->SaveAs( (plot_home + plotName +"_TTbar_combined_"+ year+".png").c_str());
      if(plotName == "top_pt_weight")return; // these are only saved for top datasets


      setDynamicXScale( h_all_WJets_MC );
      h_all_WJets_MC->Draw("HIST");
      write_cms_text(CMS_label_pos,SIM_label_pos,CMS_label_posy, SIM_label_posy, c1, noStats);

      setDynamicXScale( h_all_QCD_MC );

      h_all_QCD_MC->Draw("HIST");
      write_cms_text(CMS_label_pos,SIM_label_pos,CMS_label_posy, SIM_label_posy, c1, noStats);

      c1->SaveAs( (plot_home + plotName +"_QCDMC_combined_"+ year+".png").c_str()); 
      h_all_ST_MC->Draw("HIST");
      h_all_ST_MC->Draw("HIST");
      write_cms_text(CMS_label_pos,SIM_label_pos,CMS_label_posy, SIM_label_posy, c1, noStats);

      c1->SaveAs( (plot_home + plotName +"_STMC_combined_"+ year+".png").c_str()); 

      //write_cms_text(CMS_label_pos,SIM_label_pos,CMS_label_posy, SIM_label_posy, c1, noStats);
      //h_allBR->Draw("HIST");
      //c1->SaveAs( (plot_home + plotName +"_allBR_"+ year+".png").c_str()); 
  }

  gPad->SetLogy(false);
  // create combined BR STACK plot
  THStack *h_allBR_stack = new THStack( (plotName+"_stack").c_str(), (plot_description + " ("+  year_str+ ") (combined BR)").c_str() );

  //h_all_QCD_MC->SetFillColor(kRed);
  //h_all_TTbar_MC->SetFillColor(kYellow);
  //h_all_WJets_MC->SetFillColor(kViolet);
  //h_all_ST_MC->SetFillColor(kGreen);

  int color1 = TColor::GetColor(228, 37, 54);
  int color2 = TColor::GetColor(87, 144, 252);
  int color3 = TColor::GetColor(248, 156, 32);
  int color4 = TColor::GetColor(150, 74, 139);

  h_all_ST_MC->SetFillColor(color4);
  h_all_TTbar_MC->SetFillColor(color2);
  h_all_WJets_MC->SetFillColor(color3);
  h_all_QCD_MC->SetFillColor(color1);

  h_allBR_stack->Add(h_all_ST_MC);
  h_allBR_stack->Add(h_all_TTbar_MC);
  h_allBR_stack->Add(h_all_WJets_MC);
  h_allBR_stack->Add(h_all_QCD_MC);

  //h_allBR_stack->GetYaxis()->SetRangeUser(h_allBR_stack->GetMinimum(), h_allBR_stack->GetMaximum());
  //h_allBR_stack->SetMinimum(h_allBR_stack->GetMinimum());

  h_allBR_stack->Draw("HIST");

  h_allBR_stack->GetXaxis()->SetTitle( h_all_QCD_MC->GetXaxis()->GetTitle());
  h_allBR_stack->GetYaxis()->SetTitle(h_all_QCD_MC->GetYaxis()->GetTitle());
  SetLogScaleYAxis(h_allBR_stack, c1);
  
  /*
  if(makeLog)
  {  
    //h_allBR_stack->GetYaxis()->SetRangeUser(0.1*h_allBR_stack->GetMinimum(), 10*h_allBR_stack->GetMaximum());
    //h_allBR_stack->Draw("HIST");
  }*/
  
  //setDynamicXScale( h_allBR_stack );

  TLegend *legend = new TLegend(0.7, 0.7, 0.9, 0.9);
  legend->AddEntry(h_all_QCD_MC, "QCD MC", "f");
  legend->AddEntry(h_all_TTbar_MC, "TTbar MC", "f");
  legend->AddEntry(h_all_ST_MC, "ST MC", "f");
  legend->AddEntry(h_all_WJets_MC, "WJets MC", "f");
  legend->Draw();

  //backup: non-stack, combined plot
  //T h_allBR = (T)h_all_QCD_MC->Clone();
  //h_allBR->Add(h_all_TTbar_MC);
  //h_allBR->Add(h_all_ST_MC);
  //h_allBR->SetTitle((plotName + " (" +xyear+  "combined BRs)").c_str());
  write_cms_text(CMS_label_pos,SIM_label_pos,CMS_label_posy, SIM_label_posy, c1, noStats);
  //h_allBR->Draw("HIST");
  c1->SaveAs( (plot_home + plotName +"_allBR_"+ year+".png").c_str()); 
  
  delete h_allBR_stack;
  delete c1;
  delete legend;
  return;
}


void make_combined_sample_plots()
{



  bool debug = false;
  bool runEOS = true;
  std::vector<std::string> years = {"2015","2016","2017","2018"};

  if(debug) years = {"2015"};
  


  //double weights[20];
  //std::fill_n(weights, 20, 1.0);


  // histograms to make from skimmed files
  std::vector<std::string> histNames = 
  {
    "h_btag_eventWeight_nom",           /// 0
    "h_PU_eventWeight_nom",             /// 1
    "h_L1Prefiring_eventWeight_nom",    /// 2
    "h_JER_ScaleFactor_nom",            /// 3
    "h_tot_HT_semiRAW",                 /// 4
    "h_btag_EventWeight_up",            /// 5
    "h_PU_eventWeight_up",              /// 6
    "h_L1Prefiring_eventWeight_up",     /// 7
    "h_pdf_EventWeight_up",             /// 8
    "h_renorm_EventWeight_up",          /// 9
    "h_factor_EventWeight_up",          /// 10
    //"h_JER_ScaleFactor_up",
    "h_TopPT_EventWeight_up",           /// 11
    "h_btag_EventWeight_down",          /// 12
    "h_PU_eventWeight_down",            /// 13
    "h_L1Prefiring_eventWeight_down",   /// 14
    "h_pdf_EventWeight_down",           /// 15
    "h_renorm_EventWeight_down",        /// 16
    "h_factor_EventWeight_down",        /// 17
    //"h_JER_ScaleFactor_down"
  };
  if(debug)histNames = {"h_btag_eventWeight_nom"};
  std::vector<bool> makeLog = {true,true,true,true,true, true,true,true,true,true,true, true, true,true,true,true,true, true, true,true};
  std::vector<bool> noStats = {false,false,false,false,false, false,false,false,false,false,false, false,false,false,false,false,false, false,false,false};

  std::vector<std::string> plot_descriptions = 
  {
    "b-tagging event weight (nom)",       /// 0
    "Pileup event weight (nom)",          /// 1
    "L1 Prefiring event weight (nom)",    /// 2
    "JER scale factors (nom)",            /// 3
    "total event H_{T}",                  /// 4
    "b-tagging event weight (up)",        /// 5
    "Pileup event weight (up)",           /// 6
    "L1 prefiring event weight (up)",     /// 7
    "PDF event weight (up)",              /// 8
    "Renormalization weight (up)",        /// 9
    "Factorization weight (up)",          /// 10
    //"JER Scale Factor (up)",
    "Top p_{T} event weight (up)",        /// 11
    "b-tagging event weight (down)",      /// 12
    "Pileup event weight (down)",         /// 13
    "L1 prefiring event weight (down)",   /// 14  
    "PDF event weight (down)",            /// 15
    "Renormalization event weight weight (down)",   /// 16
    "Factorization event weight (down)",            /// 17
    //"JER scale factor (down)"
  };
  if(debug ) plot_descriptions = {"b-tagging event weight (nom)"};
  ///// histograms to make from processed files
  std::vector<std::string> histNames_2D = 
  {
    "h_MSJ_mass_vs_MdSJ_SR",
    "h_MSJ_mass_vs_MdSJ_CR",
    "h_MSJ_mass_vs_MdSJ_AT1b",
    "h_MSJ_mass_vs_MdSJ_AT0b",

    "h_MSJ_mass_vs_MdSJ_NN_SR",
    "h_MSJ_mass_vs_MdSJ_NN_CR",
    "h_MSJ_mass_vs_MdSJ_NN_AT1b",
    "h_MSJ_mass_vs_MdSJ_NN_AT0b"


  };

  if(debug) histNames_2D = {"h_MSJ_mass_vs_MdSJ_SR"};
  std::vector<bool> makeLog2 = {false,false,false,false,false,false,false,false};
  std::vector<bool> noStats2 = {true,true,true,true,true,true,true,true};

  std::vector<std::string> plot_descriptions_2D = 
  {
    "M_{SJ} vs M_{diSJ} in the SR (cut-based)",
    "M_{SJ} vs M_{diSJ} in the CR (cut-based)",
    "M_{SJ} vs M_{diSJ} in the AT1b (cut-based)",
    "M_{SJ} vs M_{diSJ} in the AT0b (cut-based)",

    "M_{SJ} vs M_{diSJ} in the SR (NN-tagging)",
    "M_{SJ} vs M_{diSJ} in the CR (NN-tagging)",
    "M_{SJ} vs M_{diSJ} in the AT1b (NN-tagging)",
    "M_{SJ} vs M_{diSJ} in the AT0b (NN-tagging)",
  } ;
  std::vector<std::string> histNames_proc = 
  {
    "h_SJ_mass_SR",
    "h_disuperjet_mass_SR",
     "h_SJ_mass_CR",
    "h_disuperjet_mass_CR",
     "h_SJ_mass_AT1b",
    "h_disuperjet_mass_AT1b",
     "h_SJ_mass_AT0b",
    "h_disuperjet_mass_AT0b",

    "h_SJ_mass_NN_SR",
    "h_disuperjet_mass_NN_SR",
     "h_SJ_mass_NN_CR",
    "h_disuperjet_mass_NN_CR",
     "h_SJ_mass_NN_AT1b",
    "h_disuperjet_mass_NN_AT1b",
     "h_SJ_mass_NN_AT0b",
    "h_disuperjet_mass_NN_AT0b"

  };
  if(debug) histNames_proc =  {"h_SJ_mass_SR"};

  std::vector<bool> makeLog3 = {true,true,true,true,true,true,true,true};
  std::vector<bool> noStats3= {true,true,true,true,true,true};

  std::vector<std::string> plot_descriptions_proc = 
  {
    "Superjet mass in the SR (cut-based)",
    "disuperjet mass in the SR (cut-based)",
     "Superjet mass in the CR (cut-based)",
    "disuperjet mass in the CR (cut-based)",
     "Superjet in the AT1b (cut-based)",
    "disuperjet mass in the AT1b (cut-based)",
     "Superjet mass in the AT0b (cut-based)",
    "disuperjet mass in the AT0b (cut-based)",

    "Superjet mass in the SR (NN-tagging)",
    "disuperjet mass in the SR (NN-tagging)",
     "Superjet mass in the CR (NN-tagging)",
    "disuperjet mass in the CR (NN-tagging)",
     "Superjet in the AT1b (NN-tagging)",
    "disuperjet mass in the AT1b (NN-tagging)",
     "Superjet mass in the AT0b (NN-tagging)",
    "disuperjet mass in the AT0b (NN-tagging)"

  };

  //std::string plotName = "";  // get from histName
  int iii = 0;
  for(auto year = years.begin();year!= years.end();year++)
  {
    std::vector<std::string> dataFiles;

/*
         if(*dataYear == "2015")
         {
            dataBlocks = {"dataB-ver2_","dataC-HIPM_","dataD-HIPM_","dataE-HIPM_","dataF-HIPM_"}; // dataB-ver1 not present
         }
         else if(*dataYear == "2016")
         {
            dataBlocks = {"dataF_", "dataG_", "dataH_"};
         }
         else if(*dataYear == "2017")
         {
            dataBlocks = {"dataB_","dataC_","dataD_","dataE_", "dataF_"};
         }
         else if(*dataYear == "2018")
         {
            dataBlocks = {"dataA_","dataB_","dataC_","dataD_"};
         }


*/
    //double QCD_weights[] = {QCD1000to1500_SF[iii],QCD1500to2000_SF[iii],QCD2000toInf_SF[iii]};


    double QCD_weights[] = {QCDMC_Pt_170to300_SF[iii],QCDMC_Pt_300to470_SF[iii],QCDMC_Pt_470to600_SF[iii], QCDMC_Pt_600to800_SF[iii], QCDMC_Pt_800to1000_SF[iii], 
                            QCDMC_Pt_1000to1400_SF[iii], QCDMC_Pt_1400to1800_SF[iii], QCDMC_Pt_1800to2400_SF[iii], QCDMC_Pt_2400to3200_SF[iii], QCDMC_Pt_3200toInf_SF[iii]    };
    double TTbar_weights[] = {h_TTJetsMCHT800to1200_SF[iii], h_TTJetsMCHT1200to2500_SF[iii],h_TTJetsMCHT2500toInf_SF[iii]};
    double WJets_weights[] = {WJetsMC_LNu_HT800to1200_SF[iii], WJetsMC_LNu_HT1200to2500_SF[iii], WJetsMC_LNu_HT2500toInf_SF[iii],WJetsMC_QQ_HT800toInf_SF[iii]}; 
    double ST_weights[] = {ST_s_channel_4f_hadrons_SF[iii], ST_s_channel_4f_leptons_SF[iii], ST_t_channel_antitop_5f_SF[iii], ST_t_channel_top_5f_SF[iii], ST_tW_antitop_5f_SF[iii],ST_tW_top_5f_SF[iii]};

    /*
    if (*year == "2015")
    {
      dataFiles  = {"/Users/ethan/Documents/rootFiles/cutflowFiles/dataB-ver2_2015_nom_CUTFLOW.root",
                    "/Users/ethan/Documents/rootFiles/cutflowFiles/dataC-HIPM_2015_nom_CUTFLOW.root",
                    "/Users/ethan/Documents/rootFiles/cutflowFiles/dataD-HIPM_2015_nom_CUTFLOW.root",
                    "/Users/ethan/Documents/rootFiles/cutflowFiles/dataE-HIPM_2015_nom_CUTFLOW.root",
                    "/Users/ethan/Documents/rootFiles/cutflowFiles/dataF-HIPM_2015_nom_CUTFLOW.root"};
    }
    else if (*year == "2016")
    {
        dataFiles = {"/Users/ethan/Documents/rootFiles/cutflowFiles/dataF_2016_nom_CUTFLOW.root",
    "/Users/ethan/Documents/rootFiles/cutflowFiles/dataG_2016_nom_CUTFLOW.root",
    "/Users/ethan/Documents/rootFiles/cutflowFiles/dataH_2016_nom_CUTFLOW.root"};
    }
    else if (*year == "2017")
    {
        dataFiles = {"/Users/ethan/Documents/rootFiles/cutflowFiles/dataB_2017_nom_CUTFLOW.root",
    "/Users/ethan/Documents/rootFiles/cutflowFiles/dataC_2017_nom_CUTFLOW.root",
    "/Users/ethan/Documents/rootFiles/cutflowFiles/dataD_2017_nom_CUTFLOW.root",
    "/Users/ethan/Documents/rootFiles/cutflowFiles/dataE_2017_nom_CUTFLOW.root",
    "/Users/ethan/Documents/rootFiles/cutflowFiles/dataF_2017_nom_CUTFLOW.root"};
    }
    else if (*year == "2018")
    {
        dataFiles = {"/Users/ethan/Documents/rootFiles/cutflowFiles/dataA_2018_nom_CUTFLOW.root",
    "/Users/ethan/Documents/rootFiles/cutflowFiles/dataB_2018_nom_CUTFLOW.root",
    "/Users/ethan/Documents/rootFiles/cutflowFiles/dataC_2018_nom_CUTFLOW.root",
    "/Users/ethan/Documents/rootFiles/cutflowFiles/dataD_2018_nom_CUTFLOW.root"};
    }
    else
    {
      std::cout << "ERROR: incorrect year" << std::endl;
      return;
    }

  std::vector<std::string> QCDFiles   = { ("/Users/ethan/Documents/rootFiles/cutflowFiles/QCDMC1000to1500_"+*year+"_nom_CUTFLOW.root").c_str(),
("/Users/ethan/Documents/rootFiles/cutflowFiles/QCDMC1500to2000_"+*year+"_nom_CUTFLOW.root").c_str(),
("/Users/ethan/Documents/rootFiles/cutflowFiles/QCDMC2000toInf_"+*year+"_nom_CUTFLOW.root").c_str()};

  std::vector<std::string> TTbarFiles = {   //("/Users/ethan/Documents/rootFiles/cutflowFiles/TTToHadronicMC_"+*year+"_nom_CUTFLOW.root").c_str(),
//("/Users/ethan/Documents/rootFiles/cutflowFiles/TTToLeptonicMC_"+*year+"_nom_CUTFLOW.root").c_str(),
//("/Users/ethan/Documents/rootFiles/cutflowFiles/TTToSemiLeptonicMC_"+*year+"_nom_CUTFLOW.root").c_str()
("/Users/ethan/Documents/rootFiles/cutflowFiles/TTJetsMCHT1200to2500_"+ *year+ "_nom_CUTFLOW.root").c_str(),
      ("/Users/ethan/Documents/rootFiles/cutflowFiles/TTJetsMCHT2500toInf_"+ *year+ "_nom_CUTFLOW.root").c_str()



  };

  std::vector<std::string> STFiles = {("/Users/ethan/Documents/rootFiles/cutflowFiles/ST_s-channel-hadronsMC_"+*year+"_nom_CUTFLOW.root").c_str(),
("/Users/ethan/Documents/rootFiles/cutflowFiles/ST_s-channel-leptonsMC_"+*year+"_nom_CUTFLOW.root").c_str(),
("/Users/ethan/Documents/rootFiles/cutflowFiles/ST_t-channel-antitop_inclMC_"+*year+"_nom_CUTFLOW.root").c_str(),
("/Users/ethan/Documents/rootFiles/cutflowFiles/ST_t-channel-top_inclMC_"+*year+"_nom_CUTFLOW.root").c_str(),
("/Users/ethan/Documents/rootFiles/cutflowFiles/ST_tW-antiTop_inclMC_"+*year+"_nom_CUTFLOW.root").c_str(),
("/Users/ethan/Documents/rootFiles/cutflowFiles/ST_tW-top_inclMC_"+*year+"_nom_CUTFLOW.root").c_str()};


*/


  std::string fileDirectory = "../combinedROOT/processedFiles/";

  if(runEOS) fileDirectory=  "root://cmseos.fnal.gov//store/user/ecannaer/processedFiles/";
  /*
    std::vector<std::string> QCDFiles_processed   = { (fileDirectory+ "/QCDMC1000to1500_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/QCDMC1500to2000_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/QCDMC2000toInf_"+*year+"_processed.root").c_str()};*/


    std::vector<std::string> QCDFiles_processed   = { (fileDirectory+ "/QCDMC_Pt_170to300_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/QCDMC_Pt_300to470_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/QCDMC_Pt_470to600_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/QCDMC_Pt_600to800_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/QCDMC_Pt_800to1000_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/QCDMC_Pt_1000to1400_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/QCDMC_Pt_1400to1800_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/QCDMC_Pt_1800to2400_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/QCDMC_Pt_2400to3200_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/QCDMC_Pt_3200toInf_"+*year+"_processed.root").c_str()     };  

    



    std::vector<std::string> TTbarFiles_processed = {(fileDirectory+ "/TTJetsMCHT800to1200_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/TTJetsMCHT1200to2500_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/TTJetsMCHT2500toInf_"+*year+"_processed.root").c_str()};


    std::vector<std::string> WJetsFiles_processed = {(fileDirectory+ "/WJetsMC_LNu-HT800to1200_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/WJetsMC_LNu-HT1200to2500_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/WJetsMC_LNu-HT2500toInf_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/WJetsMC_QQ-HT800toInf_"+*year+"_processed.root").c_str()};


      std::vector<std::string> STFiles_processed = {(fileDirectory+ "/ST_s-channel-hadronsMC_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/ST_s-channel-leptonsMC_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/ST_t-channel-antitop_inclMC_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/ST_t-channel-top_inclMC_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/ST_tW-antiTop_inclMC_"+*year+"_processed.root").c_str(),
    (fileDirectory+ "/ST_tW-top_inclMC_"+*year+"_processed.root").c_str()};

  
    /*
    int counter = 0;
    // make combined/partially combined plots from cutflow files
    for(auto histName = histNames.begin(); histName < histNames.end(); histName++)
    {

      std::cout << *histName << " " << plot_descriptions[counter] << std::endl;
      create_plots<TH1F*>(dataFiles, QCDFiles, TTbarFiles, STFiles, QCD_weights, TTbar_weights, ST_weights, *histName, *year,true, makeLog[counter], noStats[counter], *histName, plot_descriptions[counter], ""); // the bool is to tell it to make a stack plot, this won't work for 2D plots below
      counter++;
    } 
    */

  

    // make combined/partially combined plots from processed files 
    std::string nomFolderName = "nom/";
    // I think the processed files will be within systematic folders, so plot names will have to have folder strings attached

    int counter = 0;
    for(auto histName = histNames_proc .begin(); histName < histNames_proc.end(); histName++)
    {
        std::cout << "Running 1D plots for year" << *year << " and hist name " << *histName << std::endl;
        create_plots<TH2F*>(dataFiles, QCDFiles_processed, TTbarFiles_processed, WJetsFiles_processed, STFiles_processed, QCD_weights, TTbar_weights, WJets_weights, ST_weights, *histName, *year,  true, makeLog3[counter],noStats3[counter], *histName, plot_descriptions_proc[counter], nomFolderName);
        counter++;  
    }

    counter =0;
    for(auto histName = histNames_2D .begin(); histName < histNames_2D.end(); histName++)
    {
        std::cout << "Running 2D plots for year" << *year << " and hist name " << *histName << std::endl;
      create_plots<TH2F*>(dataFiles, QCDFiles_processed, TTbarFiles_processed, WJetsFiles_processed, STFiles_processed, QCD_weights, TTbar_weights, WJets_weights, ST_weights, *histName, *year, false, makeLog2[counter], noStats2[counter],*histName, plot_descriptions_2D[counter], nomFolderName);
      counter++;
    }

    iii++;

  }



}
