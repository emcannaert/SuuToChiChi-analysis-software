#include <iomanip>
#include <TH1D.h>
#include <TCanvas.h>
#include <iostream>
#include <TFile.h>
#include <TTree.h>
#include <fstream>

void plotGenHT()
{   

   const int nbins = 6;
   const double xbins[nbins+1] = {0, 600, 800, 1200, 2500, 3800, 10000};



   TCanvas * c = new TCanvas("c", "", 400, 400);
   TLegend *legend = new TLegend(0.7, 0.7, 0.9, 0.9);

   const double TTToHadronic_xs = 377.96, TTToSemiLeptonic_xs = 365.34, TTToLeptonic_xs = 88.29;
   const double TTJets_xs_inc =  496.1;  //830.;

   double lumi_2018 = 59.83;  // fb-1



   /////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////
   //////////////////////////////////////// TTJets /////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////


   TFile *file_TTJets = new TFile("TTToHadronic_xs.root", "RECREATE");

   //TH1D * h = new TH1D("h", ";LHE_HT;", 6, 0, 2000.);
   TH1D * h = new TH1D("h", ";LHE_HT;", nbins, xbins);

   std::cout << "Running over TTJets" << std::endl;
   std::ifstream infile("TTToHadronic.txt");
   std::string line;
   double ntotinc = 0;
   int nfiles = 0;
   int failedFiles_TTJets = 0;
   while (std::getline(infile, line)) 
   {

      std::cout << "opening file : " << line.c_str() << " ("<< nfiles << ") (" << failedFiles_TTJets << " failed)"<< std::endl;
      // download the file
      //char cmd_download[1000];
      //sprintf(cmd_download, "xrdcp -f root://cmsxrootd.fnal.gov//%s /uscmst1b_scratch/lpc1/3DayLifetime/cannaert/CMSSW_10_6_30/src", line.c_str());
      //std::cout << cmd_download << std::endl;
      //system(cmd_download);
      // fill the histogram
      try
      {  
         //std::string fname_; // = basename(line.c_str());
         //sprintf(fname_, "root://cmsxrootd.fnal.gov//%s", line.c_str());

         std::string fname = "root://cmsxrootd.fnal.gov//" + line; // buffer to store the copy of the filename
         //strcpy(fname, fname_);
         //char infile_[100];
         //sprintf(infile_, "/uscmst1b_scratch/lpc1/3DayLifetime/cannaert/CMSSW_10_6_30/src/%s", fname);
         TFile * f = TFile::Open(fname.c_str());
         if((f == nullptr) ||(f->IsZombie()))
         {
            std::cout << "ERROR: file can't be opened for " << line.c_str() << std::endl;
            continue;
         }
         TTree * t = (TTree*)f->Get("Events");
         if(t == nullptr)
         {
            std::cout << "ERROR: tree can't be found for " << line.c_str() << std::endl;
            continue;
         }
         h->SetDirectory(f);
         ntotinc += t->Project("+h", "LHE_HT"); // project onto existing histogram
         // delete the file
         //char cmd_delete[1000];
         //sprintf(cmd_delete, "rm /uscmst1b_scratch/lpc1/3DayLifetime/cannaert/CMSSW_10_6_30/src/%s", fname);
         //std::cout << cmd_delete << std::endl;
         //system(cmd_delete);
         delete t;
         f->Close();
         ++nfiles;
         //if (nfiles>10) break; // remove this to run on entire dataset
      }
      catch(...)
      {
         std::cout << "ERROR: Failed with file "<< line.c_str() << std::endl;
         ++nfiles;
         failedFiles_TTJets++;
      }

   }
   std::cout << "TTJets: number of files processed: " << nfiles << std::endl;
   std::cout << "TTJets: number of entries processed: " << ntotinc << std::endl;


   double TTJets_SF = lumi_2018 / (ntotinc / (TTJets_xs_inc*1000));

   std::cout << "cd to TTJets out file" << std::endl;


   file_TTJets->cd();

   std::cout << "set up TTJets output root file" << std::endl;

   h->Scale(TTJets_SF);
   std::cout << "scaled TTJets output root file" << std::endl;
   //h->SetLineWidth(4);
   std::cout << "setting log" << std::endl;
   c->SetLogy();  // are there bins with 0??
   std::cout << "setting minimum TTJets output root file" << std::endl;
   h->SetMinimum(1e-1);
   std::cout << "setting maximum TTJets output root file" << std::endl;
   h->SetMaximum(1e8);
   std::cout << "draw TTJets output root file" << std::endl;

   h->Draw("HIST");

   std::cout << "write TTJets output root file" << std::endl;

   h->Write();
   c->SaveAs("TTToHadronic_xs_2018.png");
   std::cout << "close TTJets output root file" << std::endl;

   file_TTJets->Close();

   /*
   /////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////
   //////////////////////////////////// TTToHadronic ///////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////

   std::cout << "Running over TTToHadronic" << std::endl;

   TFile *file_had = new TFile("TTToHadronic_xs.root", "RECREATE");


   TH1D * h_had     = new TH1D("h_had", ";LHE_HT;", nbins, xbins);

   std::ifstream infile_had("TTToHadronic.txt");
   std::string line_had;
   double ntotinc_had = 0;
   int nfiles_had = 0;
   int failedFiles_had = 0;
   while (std::getline(infile_had, line_had)) {
      std::cout << "opening file : " << line_had.c_str() << " ("<< nfiles_had << ") (" << failedFiles_had << " failed)"<< std::endl;
      // download the file
      
      //char cmd_download[1000];
      //sprintf(cmd_download, "xrdcp -f root://cmsxrootd.fnal.gov//%s /uscmst1b_scratch/lpc1/3DayLifetime/cannaert/CMSSW_10_6_30/src", line_had.c_str());
      //std::cout << cmd_download << std::endl;
      //system(cmd_download);
      // fill the histogram
      try
      {  
         //std::string fname_; // basename(line_had.c_str());
         //sprintf(fname_, "root://cmsxrootd.fnal.gov//%s", line_had.c_str());
         //std::cout << "fname_ is " << fname_ << std::endl;

         std::string fname =  "root://cmsxrootd.fnal.gov//" + line_had; // buffer to store the copy of the filename
         //strcpy(fname, fname_);
         std::cout << "fname is " << fname << std::endl;
         //std::string infile_had_;
         //sprintf(infile_had_, "/uscmst1b_scratch/lpc1/3DayLifetime/cannaert/CMSSW_10_6_30/src/%s", fname);
         TFile * f = TFile::Open(fname.c_str());  // want to open the filename 
         if((f == nullptr) ||(f->IsZombie()))
         {
            std::cout << "ERROR: file can't be opened for " << line_had.c_str() << std::endl;
            continue;
         }
         TTree * t = (TTree*)f->Get("Events");
         if(t == nullptr)
         {
            std::cout << "ERROR: tree can't be found for " << line_had.c_str() << std::endl;
            continue;
         }
         h_had->SetDirectory(f);
         ntotinc_had += t->Project("+h_had", "LHE_HT"); // project onto existing histogram
         // delete the file
         //char cmd_delete[1000];
         //sprintf(cmd_delete, "rm /uscmst1b_scratch/lpc1/3DayLifetime/cannaert/CMSSW_10_6_30/src/%s", fname);
         //system(cmd_delete);
         delete t;

         f->Close();
         ++nfiles_had;
      }
      catch(...)
      {
         std::cout << "ERROR: Failed with file "<< line_had.c_str() << std::endl;
         ++nfiles_had;
         failedFiles_had++;
      }


   }
   std::cout << "TTToHadronic: number of files processed: " << nfiles_had << std::endl;
   std::cout << "TTToHadronic: number of entries processed: " << ntotinc_had << std::endl;


   double TTToHadronic_SF = lumi_2018 / (ntotinc_had / (TTToHadronic_xs*1000));

   // add overflow to last bin
   //h_had->AddBinContent(nbins, h_had->GetBinContent(nbins+1));
   // clear overflow bin
   //h_had->SetBinContent(nbins+1, 0);

   file_had->cd();

   h_had->Scale(TTToHadronic_SF);
   h_had->Draw("HIST");
   h_had->SetLineWidth(4);
   h_had->SetMinimum(1e-1);
   h_had->SetMaximum(1e8);
   h_had->Write();
   c->SaveAs("TTToHadronic_xs_2018.png");

   file_had->Close();

   /////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////
   ///////////////////////////////// TTToSemiLeptonic //////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////

   std::cout << "Running over TTToLeptonic" << std::endl;

   ///store/mc/RunIISummer20UL18NanoAODv9/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/270000/5592BA84-283F-CB46-AC52-DF81B1FE09DA.root

   TFile *file_semilep = new TFile("TTToSemiLeptonic_xs.root", "RECREATE");

   TH1D * h_semilep = new TH1D("h_semilep", ";LHE_HT;", nbins, xbins);

   std::ifstream infile_semilep("TTToSemiLeptonic.txt");
   std::string line_semilep;
   double ntotinc_semilep = 0;
   int nfiles_semilep = 0;
   int failedFiles_semilep = 0;
   while (std::getline(infile_semilep, line_semilep)) {
      std::cout << "opening file : " << line_semilep.c_str() << " ("<< nfiles_semilep << ") (" << failedFiles_semilep << " failed)"<< std::endl;
      // download the file

      std::cout << "------------- Looking at file " << line_semilep.c_str() << std::endl;

      //char cmd_download[1000];
      //sprintf(cmd_download, "xrdcp -f root://cmsxrootd.fnal.gov//%s /uscmst1b_scratch/lpc1/3DayLifetime/cannaert/CMSSW_10_6_30/src", line_semilep.c_str());
      //std::cout << cmd_download << std::endl;
      //system(cmd_download);

      // fill the histogram
      try
      {
         //std::string fname_;
         //sprintf(fname_, "root://cmsxrootd.fnal.gov//%s", line_semilep.c_str()); ;//basename(line_semilep.c_str());
         std::string fname = "root://cmsxrootd.fnal.gov//" + line_semilep; // buffer to store the copy of the filename
         //strcpy(fname, fname_);

         //char infile_semilep_[100];
         //sprintf(infile_semilep_, "/uscmst1b_scratch/lpc1/3DayLifetime/cannaert/CMSSW_10_6_30/src/%s", fname);
         TFile * f = TFile::Open(fname.c_str());
         if((f == nullptr) ||(f->IsZombie()) )
         {
            std::cout << "ERROR: file can't be opened for " << line_semilep.c_str() << std::endl;
            continue;
         }
         TTree * t = (TTree*)f->Get("Events");
         if(t == nullptr)
         {
            std::cout << "ERROR: tree can't be found for " << line_semilep.c_str() << std::endl;
            continue;
         }
         h_semilep->SetDirectory(f);
         ntotinc_semilep += t->Project("+h_semilep", "LHE_HT"); // project onto existing histogram
         // delete the file
         //char cmd_delete[1000];
         //sprintf(cmd_delete, "rm /uscmst1b_scratch/lpc1/3DayLifetime/cannaert/CMSSW_10_6_30/src/%s", fname);
         //std::cout << cmd_delete << std::endl;
         //system(cmd_delete);
         delete t;

         f->Close();
         ++nfiles_semilep;
         //if (nfiles_semilep>10) break; // remove this to run on entire dataset

      }
      catch(...)
      {
         std::cout << "ERROR: Failed with file "<< line_semilep.c_str() << std::endl;
         ++nfiles_semilep;
         failedFiles_semilep++;
      }

   }
   std::cout << "TTToSemiLeptonic: number of files processed: " << nfiles_semilep << std::endl;
   std::cout << "TTToSemiLeptonic: number of entries processed: " << ntotinc_semilep << std::endl;

   // add overflow to last bin
   //h_semilep->AddBinContent(nbins, h_semilep->GetBinContent(nbins+1));
   // clear overflow bin
   //h_semilep->SetBinContent(nbins+1, 0);

   double TTToSemiLeptonic_SF = lumi_2018 / (ntotinc_semilep / (TTToSemiLeptonic_xs*1000));


   file_semilep->cd();

   h_semilep->Scale(TTToSemiLeptonic_SF);
   h_semilep->Draw("HIST");
   h_semilep->SetLineWidth(4);
   h_semilep->SetMinimum(1e-1);
   h_semilep->SetMaximum(1e8);
   h_semilep->Write();
   c->SaveAs("TTToSemiLeptonic_xs_2018.png");

   file_semilep->Close();


   /////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////
   //////////////////////////////////// TTToLeptonic ///////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////

   std::cout << "Running over TTToLeptonic" << std::endl;

   TFile *file_lep = new TFile("TTLeptonic_xs.root", "RECREATE");
   TH1D * h_lep     = new TH1D("h_lep", ";LHE_HT;", nbins, xbins);

   std::ifstream infile_lep("TTToLeptonic.txt");
   std::string line_lep;
   double ntotinc_lep = 0;
   int nfiles_lep = 0;
   int failedFiles_lep = 0;
   while (std::getline(infile_lep, line_lep)) {
      std::cout << "opening file : " << line_lep.c_str() << " ("<< nfiles_lep << ") (" << failedFiles_lep << " failed)"<< std::endl;
      // download the file
      //char cmd_download[1000];
      //sprintf(cmd_download, "xrdcp -f root://cmsxrootd.fnal.gov//%s /uscmst1b_scratch/lpc1/3DayLifetime/cannaert/CMSSW_10_6_30/src", line_lep.c_str());
      //std::cout << cmd_download << std::endl;
      //system(cmd_download);
      // fill the histogram
      try
      {
         //std::string fname_;  //basename(line_lep.c_str());
         //sprintf(fname_, "root://cmsxrootd.fnal.gov//%s", line_lep.c_str());
         std::string fname = "root://cmsxrootd.fnal.gov//" + line_lep; // buffer to store the copy of the filename
         //strcpy(fname, fname_);

         //char infile_lep_[100];
         //std::cout << "fname is " << fname << std::endl;
         //sprintf(infile_lep_, "/uscmst1b_scratch/lpc1/3DayLifetime/cannaert/CMSSW_10_6_30/src/%s", fname);
         TFile * f = TFile::Open(fname.c_str());
         std::cout << "1" << std::endl;
         if((f == nullptr) ||(f->IsZombie()))
         {
            std::cout << "ERROR: file can't be opened for " << line_lep.c_str() << std::endl;
            continue;
         }
         std::cout << "2" << std::endl;
         TTree * t = (TTree*)f->Get("Events");
         std::cout << "3" << std::endl;

         if(t == nullptr)
         {
            std::cout << "ERROR: tree can't be found for " << line_lep.c_str() << std::endl;
            continue;
         }
         std::cout << "4" << std::endl;

         h_lep->SetDirectory(f);
         std::cout << "5" << std::endl;

         ntotinc_lep += t->Project("+h_lep", "LHE_HT"); // project onto existing histogram
         std::cout << "6" << std::endl;

         // delete the file
         //char cmd_delete[1000];
         //sprintf(cmd_delete, "rm /uscmst1b_scratch/lpc1/3DayLifetime/cannaert/CMSSW_10_6_30/src/%s", fname);
         //std::cout << cmd_delete << std::endl;
         //system(cmd_delete);
         delete t;

         f->Close();
         std::cout << "7" << std::endl;

         ++nfiles_lep;
         //if (nfiles_lep>10) break; // remove this to run on entire dataset
      }
      catch(...)
      {
         std::cout << "ERROR: Failed with file "<< line_lep.c_str() << std::endl;
         ++nfiles_lep;
         failedFiles_lep++;
      }
   }
   std::cout << "TTToLeptonic: number of files processed: " << nfiles_lep << std::endl;
   std::cout << "TTToLeptonic: number of entries processed: " << ntotinc_lep << std::endl;

   // add overflow to last bin
   //h_lep->AddBinContent(nbins, h_lep->GetBinContent(nbins+1));
   // clear overflow bin
   //h_lep->SetBinContent(nbins+1, 0);

   double TTToLeptonic_SF = lumi_2018 / (ntotinc_lep / (TTToLeptonic_xs*1000));



   file_lep->cd();

   h_lep->Scale(TTToLeptonic_SF);
   h_lep->Draw("HIST");
   h_lep->SetLineWidth(4);
   h_lep->SetMinimum(1e-1);
   h_lep->SetMaximum(1e8);
   h_lep->Write();
   c->SaveAs("TTToLeptonic_xs_2018.png");

   file_lep->Close();




   std::cout << "################################################################################################################" << std::endl;
   std::cout << "################################################################################################################" << std::endl;
   std::cout << "################################################################################################################" << std::endl;
   std::cout << "################################################################################################################" << std::endl;
   std::cout << "################################################################################################################" << std::endl;
   std::cout << "################################################################################################################" << std::endl;
   std::cout << "################################################################################################################" << std::endl;
   std::cout << "Failed files: TTjets/TTToHadronic/TTToSemiLeptonic/TTToLeptonic: " << failedFiles_TTJets<< "/" <<failedFiles_had << "/" <<failedFiles_semilep << "/" << failedFiles_lep << std::endl;
   std::cout << "################################################################################################################" << std::endl;
   std::cout << "################################################################################################################" << std::endl;
   std::cout << "################################################################################################################" << std::endl;
   std::cout << "################################################################################################################" << std::endl;
   std::cout << "################################################################################################################" << std::endl;
   std::cout << "################################################################################################################" << std::endl;
   std::cout << "################################################################################################################" << std::endl;

   


   /////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////
   //////////////////////////////////// Sum datasets ///////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////
   /////////////////////////////////////////////////////////////////////////////////////////


   TH1D * h_TTTo_all = (TH1D*)h_had->Clone("cloneHist");
   h_TTTo_all->SetTitle("Inclusive TTbar (from TTTo* datasets)");
   h_TTTo_all->Reset();

   double f[nbins], ferr[nbins];
   double ninc[nbins];
   double xs[nbins], xserr[nbins];

   double f_had[nbins], ferr_had[nbins];
   double ninc_had[nbins];
   double xs_had[nbins], xserr_had[nbins];

   double f_semilep[nbins], ferr_semilep[nbins];
   double ninc_semilep[nbins];
   double xs_semilep[nbins], xserr_semilep[nbins];

   double f_lep[nbins], ferr_lep[nbins];
   double ninc_lep[nbins];
   double xs_lep[nbins], xserr_lep[nbins];

   double xs_TTTo[nbins], xserr_TTTo[nbins];


   for (int i = 0; i < nbins; ++i) 
   {
      ninc[i] = h->GetBinContent(i+1);
      f[i] = ninc[i]/ntotinc;
      ferr[i] = f[i] * sqrt((1./ninc[i])+(1./ntotinc));
      xs[i] = TTJets_xs_inc * f[i];
      xserr[i] = TTJets_xs_inc * ferr[i];

      ninc_had[i] = h_had->GetBinContent(i+1);
      f_had[i] = ninc_had[i]/ntotinc_had;
      ferr_had[i] = f_had[i] * sqrt((1./ninc_had[i])+(1./ntotinc_had));
      xs_had[i] = TTToHadronic_xs * f_had[i];
      xserr_had[i] = TTToHadronic_xs * ferr_had[i];

      ninc_semilep[i] = h_semilep->GetBinContent(i+1);
      f_semilep[i] = ninc_semilep[i]/ntotinc_semilep;
      ferr_semilep[i] = f_semilep[i] * sqrt((1./ninc_semilep[i])+(1./ntotinc_semilep));
      xs_semilep[i] = TTToSemiLeptonic_xs * f_semilep[i];
      xserr_semilep[i] = TTToSemiLeptonic_xs * ferr_semilep[i];

      ninc_lep[i] = h_lep->GetBinContent(i+1);
      f_lep[i] = ninc_lep[i]/ntotinc_lep;
      ferr_lep[i] = f_lep[i] * sqrt((1./ninc_lep[i])+(1./ntotinc_lep));
      xs_lep[i] = TTToLeptonic_xs * f_lep[i];
      xserr_lep[i] = TTToLeptonic_xs * ferr_lep[i];


      xs_TTTo[i] = xs_had[i] + xs_semilep[i]  + xs_lep[i];
      xserr_TTTo[i] = sqrt(pow(xserr_lep[i],2)+pow(xserr_semilep[i],2)+pow(xserr_had[i],2));

   }


   std::cout << "----------------- TTJets ---------------- " << std::endl;
   for (int i = 0; i < nbins; ++i) {
      std::cout << "LHE_HT: " << i << std::endl;
      std::cout << "   number of events: " << ninc[i] << std::endl;
      std::cout << "   fraction of inclusive: " << f[i] << "+-" << ferr[i] << std::endl;
      std::cout << "   xs: " << xs[i] << "+-" << xserr[i] << std::endl;
   }

   std::cout << "----------------- TTToHadronic ---------------- " << std::endl;
   for (int i = 0; i < nbins; ++i) {
      std::cout << "LHE_HT: " << i << std::endl;
      std::cout << "   number of events: " << ninc_had[i] << std::endl;
      std::cout << "   fraction of inclusive: " << f_had[i] << "+-" << ferr_had[i] << std::endl;
      std::cout << "   xs: " << xs_had[i] << "+-" << xserr_had[i] << std::endl;
   }

   std::cout << "----------------- TTToSemiLeptonic ---------------- " << std::endl;
   for (int i = 0; i < nbins; ++i) {
      std::cout << "LHE_HT: " << i << std::endl;
      std::cout << "   number of events: " << ninc_semilep[i] << std::endl;
      std::cout << "   fraction of inclusive: " << f_semilep[i] << "+-" << ferr_semilep[i] << std::endl;
      std::cout << "   xs: " << xs_semilep[i] << "+-" << xserr_semilep[i] << std::endl;
   }

   std::cout << "----------------- TTToLeptonic ---------------- " << std::endl;
   for (int i = 0; i < nbins; ++i) {
      std::cout << "LHE_HT: " << i << std::endl;
      std::cout << "   number of events: " << ninc_lep[i] << std::endl;
      std::cout << "   fraction of inclusive: " << f_lep[i] << "+-" << ferr_lep[i] << std::endl;
      std::cout << "   xs: " << xs_lep[i] << "+-" << xserr_lep[i] << std::endl;
   }
   TFile *file = new TFile("TTbar_xs.root", "RECREATE");

   h->Write();
   h_had->Write();
   h_semilep->Write();
   h_lep->Write();


   h_TTTo_all->Add(h_had);
   h_TTTo_all->Add(h_semilep);
   h_TTTo_all->Add(h_lep);
   h_TTTo_all->SetLineColor(kRed);
   h_TTTo_all->Write();
   h_TTTo_all->Draw("HIST");
   
   h->SetLineColor(kGreen);
   h->Draw("HIST,SAME");

   legend->AddEntry(h_TTTo_all, "TTTo* MC", "l");
   legend->AddEntry(h, "TTJets MC", "l");

   legend->Draw();
   c->Update();

   c->SaveAs("TTJets_and_TTTo_xs_2018.png");
   */

}
