import sys
import ROOT

######### usage information ##########

# first submit jobs for calculateBtagEFficiencyMaps for each sample and year 
# hadd these files together and put the combined root file in the data folder
# with the name scheme btagging_efficiencyMap_<sample>_<year>_output.root 
# Important: The output files are combined by background: ["QCDMC_combined","TTBarMC_combined","STMC_combined"]
# you can run all years and samples by giving the single option ALL
# this will only need to be done once unless some huge change is made
# from this information, the actual efficiency maps are made with this script
# this takes in the name of your sample and the year and write the output 
# efficiency map root file to the data/ folder
# 

######################################



def makeBtagEffMap(year,sample):

   #systematic = "nom"
   inFileName  = "../data/btaggingEffMapsRAW/btagging_efficiencyMap_RAW_combined_%s_%s.root"%(sample,year)
   print("Attempting to open file %s"%(inFileName))

   outFileName = "../data/btaggingEffMaps/btag_efficiency_map_%s_combined_%s.root"%(sample,year)
   print("Reading btagging efficiency map info from ",inFileName, "and writing the actual maps to " ,outFileName)
   inFile = ROOT.TFile.Open(inFileName, "READ")
   outHistFile = ROOT.TFile.Open(outFileName,"RECREATE")
   print("Successfully opened file.")

   h_nLightJets = inFile.Get( "calculateBtagEfficiencyMaps/h_nLightJets")
   h_nTruebJets = inFile.Get( "calculateBtagEfficiencyMaps/h_nTruebJets")
   h_nTruecJets = inFile.Get( "calculateBtagEfficiencyMaps/h_nTruecJets")

   h_nLightJets_btagged = inFile.Get( "calculateBtagEfficiencyMaps/h_nLightJets_btagged")
   h_nTruebJets_btagged = inFile.Get( "calculateBtagEfficiencyMaps/h_nTruebJets_btagged")
   h_nTruecJets_btagged = inFile.Get( "calculateBtagEfficiencyMaps/h_nTruecJets_btagged")

   print("Imported histograms from file.")

   h_effLightJets = h_nLightJets_btagged.Clone();
   h_effbJets     = h_nTruebJets_btagged.Clone();
   h_effcJets     = h_nTruecJets_btagged.Clone();

   h_effLightJets.SetTitle("Light jet efficiency maps")
   h_effbJets.SetTitle("true b jet efficiency maps")
   h_effcJets.SetTitle("true c jet efficiency maps")

   h_effLightJets.SetName("h_effLightJets")
   h_effbJets.SetName("h_effbJets")
   h_effcJets.SetName("h_effcJets")


   h_effLightJets.Divide(h_nLightJets)
   h_effbJets.Divide(h_nTruebJets)
   h_effcJets.Divide(h_nTruecJets)
   print("Did TH2 division.")

   h_effLightJets.Write()
   h_effbJets.Write()
   h_effcJets.Write()
   print("Wrote efficiency maps to %s"%outFileName)

   outHistFile.Close()
   return
   
if __name__ == "__main__":
   if len(sys.argv) != 3 and len(sys.argv) != 2 :
      print("USAGE: <sample type (ex: sigMC_Suu8TeV_chi3TeV ... ,QCDMC1000to1500,TTbarMC, data )>  <year> or ALL")
      sys.exit(1)
   if len(sys.argv) == 2 and sys.argv[1] == "ALL":
      years =["2015","2016","2017","2018"]
      years = ["2018","2017","2016","2015"]
      #samples = ["QCDMC2000toInf","QCDMC1500to2000","QCDMC1000to1500","TTToHadronicMC", "TTToLeptonicMC", "TTToSemiLeptonicMC","ST_t-channel-antitop_inclMC", "ST_t-channel-top_inclMC", "ST_tW-antiTop_inclMC","ST_tW-top_inclMC","ST_s-channel-hadronsMC","ST_s-channel-leptonsMC"]
      #samples = ["TTToHadronic", "TTToLeptonic", "TTToSemiLeptonic","ST_t-channel-antitop_incl", "ST_t-channel-top_incl", "ST_tW-antiTop_incl","ST_tW-top_incl","ST_s-channel-hadrons","ST_s-channel-leptons"]
      samples = ["QCDMC", "TTbarMC", "STMC", "SuuToChiChi"]
      for year in years:
         for sample in samples:
            makeBtagEffMap(year, sample)

