import sys,os

	
def year_converter(year):
	year_dict = {"2015":"2016preAPV", "2016":"2016postAPV","2017":"2017","2018":"2018"}
	return year_dict[year]
if __name__=="__main__":
	years = ["2015","2016","2017","2018"]
	output_file = open("btag_eff_latex_text.txt",'w')
	samples = ["QCDMC","TTbarMC","STMC","SuuToChiChi"]
	plot_types = ["b", "c", "Light"]
	for year in years:
		for plot_type in plot_types:
				output_file.write(r"\begin{figure}\n")
				output_file.write(r"\subfloat[]{\includegraphics[width = 3in]" + "{plots/btagEffPlots/h_eff%sJets_QCDMC_combined_%s.png}} \n")%(plot_type,year_dict[year])
				output_file.write(r"\subfloat[]{\includegraphics[width = 3in]" + "{plots/btagEffPlots/h_eff%sJets_TTbarMC_combined_%s.png}}\\\n")%(plot_type,year_dict[year])
				output_file.write(r"\subfloat[]{\includegraphics[width = 3in]" + "{plots/btagEffPlots/h_eff%sJets_STMC_combined_%s.png}}\n")%(plot_type,year_dict[year])
				output_file.write(r"\subfloat[]{\includegraphics[width = 3in]" + "{plots/btagEffPlots/h_eff%sJets_SuuToChiChi_%s.png}} \n")%(plot_type,year_dict[year])
				output_file.write(r"\caption{The true " + " %s jet b-tagging Efficiency maps used in the calculation of the %s b-tagging event weight corrections for each input dataset. Datasets of like-background are combined for larger statistics, and the signal datasets are also combined. The b jets used are selected as described" + r" in \ref{section:jetID} and tagged using the DeepFlavour/DeepJet algorithm with the tight working point.}\n")%(plot_type,year_dict[year])
				output_file.write(r"\label{fig:" + "btagEff%s}\n")
				output_file.write(r"\end{figure}'\n")
				output_file.write("\n")
				output_file.write("\n")
	output_file.close()
	print("Finished - output saved to btag_eff_latex_text.txt")

