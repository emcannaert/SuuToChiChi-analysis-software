import ROOT
import sys, os
import numpy as np
import glob
#from pathlib import Path  

def get_file_info(name):
	sample_str = ""
	year_str = ""
	systematic_str = ""
	samples = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTToHadronicMC", "TTToSemiLeptonicMC", "TTToLeptonicMC","ST_t-channel-top_inclMC","ST_t-channel-antitop_inclMC","ST_s-channel-hadronsMC","ST_s-channel-leptonsMC","ST_tW-antiTop_inclMC","ST_tW-top_inclMC"]
	years = ["2015","2016","2017","2018"]
	systematics = ["JEC","JER","nom"]
	for sample in samples:
		if sample in name:
			sample_str = sample
	for year in years:
		if year in name:
			year_str = year
	for systematic in systematics:
		if systematic in name:
			systematic_str = systematic
	return sample_str,year_str, systematic_str
def create_plots(sample, year,systematic):

	##### b-tagging scale factors
	if year == "2015":
		looseDeepCSV_DeepJet = 0.0490
		medDeepCSV_DeepJet   = 0.2783
		tightDeepCSV_DeepJet = 0.7100  
	elif year == "2016":
		looseDeepCSV_DeepJet = 0.0490
		medDeepCSV_DeepJet   = 0.2783
		tightDeepCSV_DeepJet = 0.7100
	elif year == "2017":
		looseDeepCSV_DeepJet = 0.0490
		medDeepCSV_DeepJet   = 0.2783
		tightDeepCSV_DeepJet = 0.7100
	elif year == "2018":
		looseDeepCSV_DeepJet = 0.0490
		medDeepCSV_DeepJet   = 0.2783
		tightDeepCSV_DeepJet = 0.7100

	else:
		print("invalid year")
		return

	inFile_name = "%s_%s_%s_combined.root"%(sample,year,systematic)
	inFile = ROOT.TFile.Open(inFile_name, "READ")

	outFile_name = "cutflow_plot_histograms_%s_%s.root"%(sample,year)
	outFile = ROOT.TFile.Open(outFile_name, "RECREATE")
	print("Reading File %s."%inFile_name)

	### tot_HT, nfatjets, nHeavy AK8 jets && dijet masses, & number of dijet pairs with M > 1 TeV, nbtags, SJ_nAK4300
	hist_list = []
	hist_list.append(ROOT.TH1F("h_tot_HT_semiRAW","Total Event H_{T} (Saved Events) (%s) (%s); H_{T} [GeV]; Events / 100 GeV"%(sample, year),100,0.,10000)) # tot_HT
	hist_list.append(ROOT.TH1I("h_nfatjets_semiRAW","AK8 Jets / Event (H_{T} cut) (%s) (%s); nAK8 Jets; Events"%(sample, year),9,-0.5,8.5)) # nfatjets
	hist_list.append(ROOT.TH1I("h_nfatjets_pre_semiRAW","Heavy AK8 Jets / Event (H_{T}, nAK8 cuts) (%s) (%s); nAK8 Jets (M_{softdrop} > 45 GeV); Events"%(sample, year),7,-0.5,6.5)) # nfatjets_pre
	hist_list.append(ROOT.TH1F("h_dijet_mass_semiRAW","Dijet Pair Mass (H_{T}, nAK8 cuts) (%s) (%s); Mass [GeV]; Events / 100 GeV"%(sample, year),60,0.,6000)) # dijet mass
	hist_list.append(ROOT.TH1I("h_nDijet_pairs_semiRAW","Heavy Dijet Pairs / Event (H_{T}, nAK8 cuts) (%s) (%s); Number of Dijet Pairs (M_{dijet} > 1 TeV); Events"%(sample, year),6,-0.5,5.5)) # ndijet pairs

	hist_list.append(ROOT.TH1I("h_nTight_b_jets_semiRAW","b-tagged AK4 jets / Event (Tight WP) (H_{T}, nAK8, nHeavyAK8 cuts) (%s) (%s); Number of tight b-tagged AK4 jets; Events"%(sample, year),8,-0.5,7.5)) # nTight b-tags 
	hist_list.append(ROOT.TH1I("h_SJ_nAK4_300_semiRAW","Number of Reclustered SJ CA4 Jets (E_{SJ,COM} > 300 GeV) (%s) (%s); Number of Jets (E_{COM} > 300 GeV); Events"%(sample, year),6,-0.5,5.5)) # SJ_nAK4_300 
	hist_list.append(ROOT.TH1I("h_nLoose_b_jets_semiRAW","b-tagged AK4 jets / Event (Loose WP) (H_{T}, nAK8, nHeavyAK8 cuts) (%s) (%s); Number of Loose b-tagged AK4 jets; Events"%(sample, year),10,-0.5,9.5)) # nloose b-tags 
	hist_list.append(ROOT.TH1I("h_nMed_b_jets_semiRAW","b-tagged AK4 jets / Event (Med WP) (H_{T}, nAK8, nHeavyAK8 cuts) (%s) (%s); Number of Med b-tagged AK4 jets; Events"%(sample, year),8,-0.5,7.5)) # nmed b-tags 

	hist_list.append(ROOT.TH1F("h_AK8_pt", "AK8 jet p_{T} (H_{T} > 1.5 TeV) (%s) (%s); AK8 jet p_{T}; Events / 50 GeV"%(sample, year),100,0.,5000)) 
	hist_list.append(ROOT.TH1F("h_AK8_eta", "AK8 jet eta (H_{T} > 1.5 TeV) (%s) (%s); AK8 jet eta; Events / 0.1"%(sample, year),50,-2.5,2.5)) 
	hist_list.append(ROOT.TH1F("h_AK8_phi", "AK8 jet phi (H_{T} > 1.5 TeV) (%s) (%s); AK8 jet phi; Events / 0.1 rads"%(sample, year),80,-4.,4.)) 

	hist_list.append(ROOT.TH1F("h_AK4_pt", "AK4 jet p_{T} (H_{T} > 1.5 TeV) (%s) (%s); AK4 jet p_{T}; Events / 50 GeV"%(sample, year),100,0.,5000)) 
	hist_list.append(ROOT.TH1F("h_AK4_eta", "AK4 jet eta (H_{T} > 1.5 TeV) (%s) (%s); AK4 jet eta; Events / 0.1"%(sample, year),50,-2.5,2.5)) 
	hist_list.append(ROOT.TH1F("h_AK4_phi", "AK4 jet phi (H_{T} > 1.5 TeV) (%s) (%s); AK4 jet phi; Events / 0.2 rads"%(sample, year),80,-4.0,4.0)) 

	hist_list.append(ROOT.TH1F("h_AK4_eta_goodphi", "AK4 jet eta ( 0.0 > $phi$ or $phi$ > 1.0) (%s) (%s); AK4 jet eta; Normalized Events"%(sample, year),50,-2.5,2.5)) 
	hist_list.append(ROOT.TH1F("h_AK4_eta_badphi", "AK4 jet eta ( 0.0 < $phi$ < 1.0) (%s) (%s); AK4 jet eta; Normalized Events"%(sample, year),50,-2.5,2.5)) 



	tree_name = "clusteringAnalyzerAll_/tree_"  # example clusteringAnalyzerAll_JEC_up, clusteringAnalyzerAll_JEC_down, clusteringAnalyzerAll_1
	tree = inFile.Get(tree_name)
	for iii,event in enumerate(tree):
		if iii%1000000 == 0:
			print("Starting event %i."%iii)
		n_dijets = 0
		n_tight_b_jets = 0
		n_med_b_jets = 0
		n_loose_b_jets = 0

		tot_HT = np.array(tree.totHT)



		AK4_eta = tree.AK4_eta
		AK4_phi = tree.AK4_phi

		for iii,AK4_eta_ in enumerate(AK4_eta):
			if ((tree.AK4_phi[iii] > 0) and (tree.AK4_phi[iii] < 1)):
				hist_list[15].Fill(AK4_eta_)
			else:
				hist_list[16].Fill(AK4_eta_)

		if (hist_list[15].Integral() > 0):
			hist_list[15].Scale( 1./hist_list[15].Integral())
		if (hist_list[16].Integral() > 0):
			hist_list[16].Scale( 1./hist_list[16].Integral())

		hist_list[0].Fill(tot_HT)
		if (tot_HT < 1500):
			continue


		jet_pt  = tree.jet_pt
		jet_eta = tree.jet_eta
		#jet_phi = tree.jet_phi

		AK4_pt  = tree.lab_AK4_pt
		AK4_eta = tree.AK4_eta
		AK4_phi = tree.AK4_phi

		ones_ = np.ones(100)
		hist_list[9].FillN(len(jet_pt), np.array(jet_pt),ones_[:len(jet_pt)])
		hist_list[10].FillN(len(jet_eta),np.array(jet_eta),ones_[:len(jet_eta)] )
		#hist_list[11].FillN(len(jet_phi), np.array(jet_phi),ones_[:len(jet_phi)])

		hist_list[12].FillN(len(AK4_pt),np.array(AK4_pt),ones_[:len(AK4_pt)])
		hist_list[13].FillN(len(AK4_eta), np.array(AK4_eta),ones_[:len(AK4_eta)])
		hist_list[14].FillN(len(AK4_phi),np.array(AK4_phi),ones_[:len(AK4_phi)])

		nfatjets = np.array(tree.nfatjets)
		hist_list[1].Fill(nfatjets)

		if (nfatjets < 3):
			continue

		nfatjets_pre = np.array(tree.nfatjet_pre)
		dijetMassOne = np.array(tree.dijetMassOne)
		dijetMassTwo = np.array(tree.dijetMassTwo)

		hist_list[2].Fill(nfatjets_pre)
		hist_list[3].Fill(dijetMassOne) 
		hist_list[3].Fill(dijetMassTwo)

		hist_list[4].Fill( sum([dijetMassOne > 1000., dijetMassTwo > 1000.]) )

		if ((nfatjets_pre < 2) and ( (dijetMassOne < 1000. ) or ( dijetMassOne < 1000.)  )):
			continue

		AK4_DeepJet_disc = np.array(tree.AK4_DeepJet_disc)

		n_tight_b_jets = len( AK4_DeepJet_disc[AK4_DeepJet_disc > tightDeepCSV_DeepJet] )
		n_med_b_jets   = len( AK4_DeepJet_disc[AK4_DeepJet_disc > medDeepCSV_DeepJet] )
		n_loose_b_jets = len( AK4_DeepJet_disc[AK4_DeepJet_disc > looseDeepCSV_DeepJet] )

		hist_list[5].Fill(n_tight_b_jets)
		hist_list[7].Fill(n_loose_b_jets)
		hist_list[8].Fill(n_med_b_jets)

		if(n_tight_b_jets > 0):

			superJet_mass = np.array(tree.superJet_mass)
			diSuperJet_mass = np.array(tree.diSuperJet_mass)
			SJ_nAK4_300 = np.array(tree.SJ_nAK4_300)
			hist_list[6].Fill(SJ_nAK4_300[0]) # show only one superjet



	for hist in hist_list:
		hist.Write()
	print("Finished - wrote output hists to %s."%outFile_name)
	outFile.Close()
	return
	
if __name__=="__main__":
	#years = ["2015","2016","2017","2018"]
	years = ["2015"]
	systematics = ["nom"]
	samples = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTToHadronic", "TTToSemiLeptonic", "TTToLeptonic","ST_t-channel-top_incl","ST_t-channel-antitop_incl","ST_s-channel-hadrons","ST_s-channel-leptons","ST_tW-antiTop_incl","ST_tW-top_incl"]
	#samples = ["QCDMC1500to2000"]
	for file in glob.glob('*_nom_combined.root'):
		sample, year, systematic = get_file_info(file)
		if year == "" or sample == "" or systematic == "":
			sys.exit("Info not found.")
		#if year != "2015":
		#	continue
		create_plots(sample,year,systematic)

	#for year in years:
		#for sample in samples:
			#for systematic in systematics:
				#create_plots(sample,year,systematic)






