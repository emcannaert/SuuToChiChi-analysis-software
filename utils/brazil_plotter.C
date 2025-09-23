
// Function to extract limits from a text file
bool extract_limits_from_text_file(const std::string& fileName, double& obs_limit, double& exp_limit, double& exp_limit_1sigma_up, double& exp_limit_1sigma_down, double& exp_limit_2sigma_up, double& exp_limit_2sigma_down, bool showObservedLimits) 
{
    std::ifstream infile(fileName);
    if (!infile.is_open()) 
    {
        std::cerr << "Error opening file: " << fileName << std::endl;
        return false;
    }

    std::string line;
    while (std::getline(infile, line)) 
    {
        if (line.find("Observed Limit") != std::string::npos && showObservedLimits) 
        {
            std::stringstream ss(line);
            std::string temp;
            ss >> temp >> temp >> temp >> temp >> obs_limit;  // Extract the observed limit
        } 
        else if (line.find("Expected 50.0%") != std::string::npos) 
        {
            std::stringstream ss(line);
            std::string temp;
            ss >> temp >> temp >> temp >> temp >> exp_limit;  // Extract the median expected limit
        } 
        else if (line.find("Expected 16.0%") != std::string::npos) 
        {
            std::stringstream ss(line);
            std::string temp;
            ss >> temp >> temp >> temp >> temp >> exp_limit_1sigma_down;  // Extract 1 sigma down
        } 
        else if (line.find("Expected 84.0%") != std::string::npos) 
        {
            std::stringstream ss(line);
            std::string temp;
            ss >> temp >> temp >> temp >> temp >> exp_limit_1sigma_up;  // Extract 1 sigma up
        } 
        else if (line.find("Expected 2.5%") != std::string::npos) 
        {
            std::stringstream ss(line);
            std::string temp;
            ss >> temp >> temp >> temp >> temp >> exp_limit_2sigma_down;  // Extract 2 sigma down
        } 
        else if (line.find("Expected 97.5%") != std::string::npos) 
        {
            std::stringstream ss(line);
            std::string temp;
            ss >> temp >> temp >> temp >> temp >> exp_limit_2sigma_up;  // Extract 2 sigma up
        }
    }
    infile.close();
    return true;
}


void write_cms_text(double CMS_label_pos, double SIM_label_pos, TCanvas * canvas, bool noStats, bool showObservedLimits) 
{
    // do all the fancy formatting 
    //gStyle->SetOptStat(0);
    
    TText *CMSLabel = new TText();
    CMSLabel->SetNDC();
    CMSLabel->SetTextFont(61);
    CMSLabel->SetTextColor(1);
    CMSLabel->SetTextSize(0.0385);
    CMSLabel->SetTextAlign(22);
    CMSLabel->SetTextAngle(0);
    CMSLabel->DrawText(CMS_label_pos, 0.92, "CMS");
    CMSLabel->Draw();
    
    TText *simLabel = new TText();
    simLabel->SetNDC();
    simLabel->SetTextFont(52);
    simLabel->SetTextColor(1);
    simLabel->SetTextSize(0.024);
    simLabel->SetTextAlign(22);
    simLabel->SetTextAngle(0);
    if(showObservedLimits)  std::cout << "can't remember what to add here ..." << std::endl;                //simLabel->DrawText(SIM_label_pos, 0.92, "Simulation Preliminary");
    else {simLabel->DrawText(SIM_label_pos, 0.92, "Simulation Preliminary"); }
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

void brazil_plot(std::vector<std::string> fileNames, int Suu_mass, std::vector<int> chi_masses, bool showObservedLimits) 
{

    // Number of files
    int N = fileNames.size();

    // Create vectors to hold graphs from each file
    TGraph *expectedLimit = new TGraph();
    TGraph *observedLimit = new TGraph();
    TGraphAsymmErrors *expectedLimit_1sigma = new TGraphAsymmErrors();  // For 1 sigma asymmetric errors
    TGraphAsymmErrors *expectedLimit_2sigma = new TGraphAsymmErrors();  // For 2 sigma asymmetric errors

    expectedLimit->SetName("expectedLimit");
    observedLimit->SetName("observedLimit");
    expectedLimit_1sigma->SetName("expectedLimit_1sigma");
    expectedLimit_2sigma->SetName("expectedLimit_2sigma");

    // Open each file and retrieve the limits
    for (int i = 0; i < N; ++i) 
    {
        double obs_limit = 0;
        double exp_limit = 0;
        double exp_limit_1sigma_up = 0;
        double exp_limit_1sigma_down = 0;
        double exp_limit_2sigma_up = 0;
        double exp_limit_2sigma_down = 0;

        if (!extract_limits_from_text_file(fileNames[i], obs_limit, exp_limit, exp_limit_1sigma_up, exp_limit_1sigma_down, exp_limit_2sigma_up, exp_limit_2sigma_down, showObservedLimits)) 
        {
            std::cerr << "Failed to extract limits from " << fileNames[i] << std::endl;
            continue;
        }

        // Fill expected limits
        expectedLimit->SetPoint(i, chi_masses[i], exp_limit);

        // For asymmetric 1 sigma band
        expectedLimit_1sigma->SetPoint(i, chi_masses[i], exp_limit);
        expectedLimit_1sigma->SetPointError(i, 0.0, 0.0, exp_limit - exp_limit_1sigma_down, exp_limit_1sigma_up - exp_limit);

        // For asymmetric 2 sigma band
        expectedLimit_2sigma->SetPoint(i, chi_masses[i], exp_limit);
        expectedLimit_2sigma->SetPointError(i, 0.0, 0.0, exp_limit - exp_limit_2sigma_down, exp_limit_2sigma_up - exp_limit);

        // Fill observed limits if applicable
        if (showObservedLimits) 
        {
            observedLimit->SetPoint(i, chi_masses[i], obs_limit);
        }
    }

    // The rest of your plot generation code remains the same

    // Draw the +-2sigma band first (yellow)
    expectedLimit_2sigma->SetFillColor(kYellow);
    expectedLimit_2sigma->Draw("A3");

    // Draw the +-1sigma band (green)
    expectedLimit_1sigma->SetFillColor(kGreen);
    expectedLimit_1sigma->Draw("3 same");

    // Draw the median expected limit line
    expectedLimit->SetLineColor(kBlack);
    expectedLimit->SetLineWidth(2);
    expectedLimit->SetLineStyle(9);  // set dotted line
    expectedLimit->Draw("L same");

    // Draw observed limits if applicable
    if (showObservedLimits) 
    {
        observedLimit->SetLineColor(kBlack);
        observedLimit->SetLineWidth(2);
        observedLimit->Draw("L same");
    }


    expectedLimit_2sigma->GetXaxis()->SetTitle("#chi Mass [GeV]");
    expectedLimit_2sigma->GetYaxis()->SetTitle("95% CL limit on #sigma/#sigma_{SM}");
    expectedLimit_2sigma->GetYaxis()->SetRangeUser(0.001, 100); // Adjust as necessary for your data
    c1->SetLogy(); // Set log scale

    // Create a legend
    TLegend* leg = new TLegend(0.6, 0.7, 0.9, 0.9);
    leg->AddEntry(expectedLimit, "Expected limit", "l");
    leg->AddEntry(expectedLimit_1sigma, "#pm 1#sigma", "f");
    leg->AddEntry(expectedLimit_2sigma, "#pm 2#sigma", "f");
    if (showObservedLimits) leg->AddEntry(observedLimit, "Observed limit", "l");
    leg->Draw();

    double CMS_label_pos = 0.13;
    double SIM_label_pos = 0.24;
    write_cms_text(CMS_label_pos, SIM_label_pos, c1, true);

    // Write Suu mass
    TText* text = new TText();
    double xPosition = 0.80; // X position (80% from the left)
    double yPosition = 0.15; // Y position (15% from the bottom)
    text->SetText(xPosition, yPosition, ("M_{S_{uu}} = " + std::to_string(Suu_mass) + " TeV").c_str());
    text->SetTextSize(0.04); // Text size
    text->SetTextFont(42);   // Font type (42 is a commonly used font)
    text->SetTextAlign(22);  // Align center (horizontally and vertically)
    text->Draw();

    // Update and save the canvas
    c1->Update();
    std::string plot_name = "exp_limits_MSuu" + std::to_string(Suu_mass) + "TeV.png";
    if (showObservedLimits) plot_name = "obs_limits_MSuu" + std::to_string(Suu_mass) + "TeV.png";
    c1->SaveAs(plot_name.c_str());

}

void brazil_plotter()
{

    showObservedLimits = false;

    std::vector<int> Suu_masses = {4000,5000,6000,7000,8000};

    std::string input_root_prefix = "mass_point_Suu";

    for(int iii = 0; iii< Suu_masses.size(); iii++)
    {
        std::vector<int> chi_masses = {1000,1500};
        std::vector<std::string> fileNames = { (input_root_prefix + Suu_masses[iii] +   "_chi1000.root").c_str(),(input_root_prefix + Suu_masses[iii] +   "_chi1500.root").c_str()};
        if(Suu_masses[iii] > 4999) 
            {  fileNames.push_back( (input_root_prefix + Suu_masses[iii] +   "_chi2000.root").c_str()  ); chi_masses.push_back(2000)  }
        if(Suu_masses[iii] > 5999) 
            {  fileNames.push_back( (input_root_prefix + Suu_masses[iii] +   "_chi2500.root").c_str()  ); chi_masses.push_back(2500) }
        if(Suu_masses[iii] > 6999) 
            {  fileNames.push_back( (input_root_prefix + Suu_masses[iii] +   "_chi3000.root").c_str()  ); chi_masses.push_back(3000)  }

        brazil_plot(fileNames, Suu_masses[iii], chi_masses, showObservedLimits);

    }
 
}