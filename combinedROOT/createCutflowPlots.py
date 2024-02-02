import ROOT
import sys, os
import numpy as np
import glob
import math
#from pathlib import Path  

def create_plots(inFile_name, sample, year,systematic):

	##### b-tagging scale factors
	if year == "2015":
		looseDeepCSV_DeepJet = 0.0508
		medDeepCSV_DeepJet   = 0.2598
		tightDeepCSV_DeepJet = 0.6502
	elif year == "2016":
		looseDeepCSV_DeepJet = 0.0480
		medDeepCSV_DeepJet   = 0.2489
		tightDeepCSV_DeepJet = 0.6377
	elif year == "2017":
		looseDeepCSV_DeepJet = 0.0532
		medDeepCSV_DeepJet   = 0.3040
		tightDeepCSV_DeepJet = 0.7476
	elif year == "2018":
		looseDeepCSV_DeepJet = 0.0490
		medDeepCSV_DeepJet   = 0.2783
		tightDeepCSV_DeepJet = 0.7100

	else:
		print("invalid year")
		return

	inFile = ROOT.TFile.Open(inFile_name, "READ")

	outFile_name = "cutflow_plot_histograms_%s_%s_%s.root"%(sample,systematic,year)
	outFile = ROOT.TFile.Open(outFile_name, "RECREATE")
	print("Reading File %s."%inFile_name)

	### tot_HT, nfatjets, nHeavy AK8 jets && dijet masses, & number of dijet pairs with M > 1 TeV, nbtags, SJ_nAK4300
	hist_list = []

	#### problem due to ints??? 
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

	hist_list.append(ROOT.TH1F("h_btagEventWeight", "b-tagging event weight (%s) (%s); event weight; Events"%(sample, year),200,0.5,1.5)) 

	h_m_SJ1_AT1b = ROOT.TH1F("h_m_SJ1_AT1b", "AT1b SJ mass (%s) (%s); SJ mass [GeV]; Events / 70 GeV"%(sample, year),50,0.0,3500)
	h_m_SJ1_AT0b = ROOT.TH1F("h_m_SJ1_AT0b", "AT0b SJ mass (%s) (%s); SJ mass [GeV]; Events / 70 GeV"%(sample, year),50,0.0,3500)
	h_m_SJ1_SR = ROOT.TH1F("h_m_SJ1_SR", "SR SJ mass (%s) (%s); SJ mass [GeV]; Events / 70 GeV"%(sample, year),50,0.0,3500)
	h_m_SJ1_CR = ROOT.TH1F("h_m_SJ1_CR", "CR SJ mass (%s) (%s); SJ mass [GeV]; Events / 70 GeV"%(sample, year),50,0.0,3500)

	totEvents = 0
	passed_HT = 0
	passed_AK8 = 0
	passed_heavyAK8 = 0
	passed_btag = 0 
	passed_nAK4_300 = 0 
	not_passed_btag = 0
	nAT1b = 0
	nAT0b = 0
	nCR = 0
	total_btags = 0
	nFailedEvents = 0
	tree_name = "clusteringAnalyzerAll_/tree_"  # example clusteringAnalyzerAll_JEC_up, clusteringAnalyzerAll_JEC_down, clusteringAnalyzerAll_1
	tree = inFile.Get(tree_name)
	useEventWeights = True
	tot_events_unscaled = 0.0

	average_btagSF = 0
	average_PUSF   = 0
	nLargeBtagSF = 0
	nLargePUSF = 0
	nSmallBtagSF = 0
	nSmallPUSF = 0
	for iii,event in enumerate(tree):
		

	for hist in hist_list:
		hist.Write()
	h_m_SJ1_AT1b.Write()
	h_m_SJ1_AT0b.Write()
	h_m_SJ1_SR.Write()
	h_m_SJ1_CR.Write()
	print("Finished - wrote output hists to %s."%outFile_name)
	print("SR   breakdown: %s : total/HT/nAK8/nHeavyAK8/nBtagged/nSR:   - %s-%s-%s-%s-%s-%s"%(sample, totEvents, passed_HT,passed_AK8,passed_heavyAK8,passed_btag,passed_nAK4_300) )
	print("CR   breakdown: %s : total/HT/nAK8/nHeavyAK8/nBtagged/nCR:   - %s-%s-%s-%s-%s-%s"%(sample,totEvents, passed_HT,passed_AK8,passed_heavyAK8,not_passed_btag,nCR) )
	print("AT1b breakdown: %s : total/HT/nAK8/nHeavyAK8/nBtagged/nAT1b: - %s-%s-%s-%s-%s-%s"%(sample,totEvents, passed_HT,passed_AK8,passed_heavyAK8,passed_btag,nAT1b) )
	print("AT0b breakdown: %s : total/HT/nAK8/nHeavyAK8/nBtagged/nAT0b: - %s-%s-%s-%s-%s-%s"%(sample,totEvents, passed_HT,passed_AK8,passed_heavyAK8,not_passed_btag,nAT0b) )

	print("There were %i failed events due to btag SF out of %i total events"%(nFailedEvents, tot_events_unscaled))
	print("There were %i total b jets tagged in this sample"%(total_btags))
	print("The average btagSF for the event was %s, the average PUSF was %s"%(average_btagSF/tot_events_unscaled, average_PUSF/tot_events_unscaled))
	print("Out of %i events, there were %i/%i large/small btag SFs, and %i/%s large/small PU SFs"%(tot_events_unscaled,nLargeBtagSF,nSmallBtagSF,nLargePUSF,nSmallPUSF))
	outFile.Close()
	
### returns the scale factor for a specific sample and year


if __name__=="__main__":
	years = ["2018"]
	systematics = ["nom"]
	samples = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTToHadronic", "TTToSemiLeptonic", "TTToLeptonic","ST_t-channel-top_incl","ST_t-channel-antitop_incl","ST_s-channel-hadrons","ST_s-channel-leptons","ST_tW-antiTop_incl","ST_tW-top_incl",
	"dataA",
	"dataB",
	"dataC",
	"dataD",
	"dataE",
	"dataF",
	"dataG",
	"dataH"]
	if year == "2018":
		samples = ["QCDMC1000to1500","QCDMC1500to2000","QCDMC2000toInf","TTToHadronicMC", "TTToSemiLeptonicMC", "TTToLeptonicMC","ST_t-channel-top_inclMC","ST_t-channel-antitop_inclMC","ST_s-channel-hadronsMC","ST_s-channel-leptonsMC","ST_tW-antiTop_inclMC","ST_tW-top_inclMC",
	"dataA",
	"dataB",
	"dataC",
	"dataD"]
	
	for sample in samples:
		for year in years:
			for systematic in systematics:
				fname = "/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/combinedROOT/%s_%s_%s_combined.root"%(sample, year, systematic)
				create_plots(fname,sample,year,systematic)

				

"""

		# apply b-tag SFs
		eventSF = 1.0
		
		if ("MC" in inFile_name) and useEventWeights:
        	
			PU_eventWeight_nom = tree.PU_eventWeight_nom
			bTag_eventWeight_nom = tree.bTag_eventWeight_nom

			if ((math.isnan(bTag_eventWeight_nom)) or (math.isinf(bTag_eventWeight_nom))):
				
				print("Failed b-tagging event weight: %f"%bTag_eventWeight_nom)
				bTag_eventWeight_nom = 1
				nFailedEvents+=1
			if ((math.isnan(PU_eventWeight_nom)) or (math.isinf(PU_eventWeight_nom))):
				PU_eventWeight_nom = 1
				print("Failed b-tagging event weight: %f"%bTag_eventWeight_nom)
            
			eventSF = bTag_eventWeight_nom*PU_eventWeight_nom
			

			if (bTag_eventWeight_nom > 1.4):
				nLargeBtagSF+=1
			#print("ERROR: large event scale factor %s"%eventSF)
			elif (bTag_eventWeight_nom < 0.60):
				nSmallBtagSF+=1
			if PU_eventWeight_nom > 1.4:
				nLargePUSF+=1
			elif PU_eventWeight_nom < 0.6:
				nSmallPUSF+=1


		if "data" not in inFile_name:
			hist_list[17].Fill(eventSF)
		if iii%1000000 == 0:
			print("Starting event %i. SF is %f"%(iii,eventSF))


		#if(eventSF < 1e-5):
			#print("ERROR: bad event SF found while starting event selection")
			#print("ERROR: small event scale factor: %s"%eventSF)
		tot_HT = float(tree.totHT)
		totEvents+=eventSF
		hist_list[0].Fill(tot_HT,eventSF)

		if (tot_HT < 1500):
			continue




		passed_HT+=eventSF
		jet_pt  = tree.jet_pt
		jet_eta = tree.jet_eta
		#jet_phi = tree.jet_phi

		AK4_pt  = tree.lab_AK4_pt
		AK4_eta = tree.AK4_eta
		AK4_phi = tree.AK4_phi

		#ones_ = np.ones(100)
		hist_list[9].FillN(len(jet_pt), np.array(jet_pt), np.full(len(jet_pt), eventSF) )
		hist_list[10].FillN(len(jet_eta),np.array(jet_eta),np.full(len(jet_eta), eventSF))
		#hist_list[11].FillN(len(jet_phi), np.array(jet_phi),ones_[:len(jet_phi)])

		hist_list[12].FillN(len(AK4_pt),np.array(AK4_pt),np.full(len(AK4_pt), eventSF))
		hist_list[13].FillN(len(AK4_eta), np.array(AK4_eta),np.full(len(AK4_eta), eventSF))
		hist_list[14].FillN(len(AK4_phi),np.array(AK4_phi),np.full(len(AK4_phi), eventSF))

		nfatjets = int(tree.nfatjets)
		hist_list[1].Fill(nfatjets,eventSF)


		if (nfatjets < 3):
			continue
		tot_events_unscaled+=1
		if ("MC" in inFile_name) and useEventWeights:
			average_btagSF+=bTag_eventWeight_nom
			average_PUSF+=PU_eventWeight_nom
		passed_AK8+=eventSF
		nfatjets_pre = int(tree.nfatjet_pre)
		dijetMassOne = int(tree.dijetMassOne)
		dijetMassTwo = int(tree.dijetMassTwo)

		hist_list[2].Fill(nfatjets_pre,eventSF)
		hist_list[3].Fill(dijetMassOne,eventSF) 
		hist_list[3].Fill(dijetMassTwo,eventSF)

		hist_list[4].Fill( sum([dijetMassOne > 1000., dijetMassTwo > 1000.]),eventSF )

		if ((nfatjets_pre < 2) and ( (dijetMassOne < 1000. ) or ( dijetMassTwo < 1000.)  )):
			continue
		passed_heavyAK8+=eventSF
		AK4_DeepJet_disc = np.array(tree.AK4_DeepJet_disc)
		nAK4 = tree.nAK4


		n_tight_b_jets = 0
		n_med_b_jets = 0
		n_loose_b_jets = 0
		for jjj in range(0,nAK4):
			if tree.lab_AK4_pt[jjj] > 30.0:
				if AK4_DeepJet_disc[jjj] > tightDeepCSV_DeepJet:
					n_tight_b_jets+=1
					n_med_b_jets+=1
					n_loose_b_jets+=1
					total_btags+=1
				elif AK4_DeepJet_disc[jjj] > medDeepCSV_DeepJet:
					n_med_b_jets+=1
					n_loose_b_jets+=1
				elif AK4_DeepJet_disc[jjj] > looseDeepCSV_DeepJet:
					n_loose_b_jets+=1

		#n_tight_b_jets = len( AK4_DeepJet_disc[AK4_DeepJet_disc > tightDeepCSV_DeepJet] )
		#n_med_b_jets  = len( AK4_DeepJet_disc[AK4_DeepJet_disc > medDeepCSV_DeepJet] )
		#n_loose_b_jets= len( AK4_DeepJet_disc[AK4_DeepJet_disc > looseDeepCSV_DeepJet] )

		hist_list[5].Fill(n_tight_b_jets,eventSF)
		hist_list[7].Fill(n_loose_b_jets,eventSF)
		hist_list[8].Fill(n_med_b_jets,eventSF)



		superJet_mass = np.array(tree.superJet_mass)
		diSuperJet_mass = float(tree.diSuperJet_mass)
		SJ_nAK4_300 = np.array(tree.SJ_nAK4_300)

		if(n_tight_b_jets > 0):

			SJ_nAK4_50 = np.array(tree.SJ_nAK4_50)
			SJ_mass_100 = tree.SJ_mass_100

			passed_btag+=eventSF
			
			hist_list[6].Fill(SJ_nAK4_300[0],eventSF) # show only one superjet
			
			#SR
			if ( (SJ_nAK4_300[0] >= 2 ) and (SJ_nAK4_300[1]>=2) ):
				if((SJ_mass_100[0]>=400.) and (SJ_mass_100[1]>400.)   ):
					h_m_SJ1_AT1b.Fill( (superJet_mass[0]+superJet_mass[1])/2.0,eventSF)
					passed_nAK4_300+=eventSF
			#AT1b
			if(   (SJ_nAK4_50[0]<1) and (SJ_mass_100[0]<150.)   ):
				if((SJ_nAK4_300[1]>=2) and (SJ_mass_100[1]>=400.)   ):
					h_m_SJ1_SR.Fill(superJet_mass[1],eventSF)
					superJet_mass = np.array(tree.superJet_mass)
					diSuperJet_mass = float(tree.diSuperJet_mass)
					#print("In the AT1b region: SJ mass/diSJ mass/nAK8/AK4/nBtags/eventWeight are %s/%s/%s/%s/%s/%s"%(superJet_mass[1],diSuperJet_mass,nfatjets ,tree.nAK4,n_tight_b_jets,eventSF))

					nAT1b+=eventSF;
		if(n_tight_b_jets < 1e-8):
			SJ_nAK4_300 = np.array(tree.SJ_nAK4_300)
			SJ_nAK4_50 = tree.SJ_nAK4_50
			SJ_mass_100 = tree.SJ_mass_100
			not_passed_btag+=eventSF
			#CR
			if ( (SJ_nAK4_300[0] > 1 ) and (SJ_nAK4_300[1]>1) ):
				if((SJ_mass_100[0]>=400.) and (SJ_mass_100[1]>400.)   ):
					h_m_SJ1_CR.Fill((superJet_mass[0]+superJet_mass[1])/2.0,eventSF)
					nCR+=eventSF
			#nAT0b
			if(   (SJ_nAK4_50[0]<1) and (SJ_mass_100[0]<150.)   ):
				if((SJ_nAK4_300[1]>=2) and (SJ_mass_100[1]>=400.)   ):
					h_m_SJ1_AT0b.Fill(superJet_mass[1],eventSF)
					nAT0b+=eventSF;




"""



