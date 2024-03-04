import sys,os

	
def year_converter(year):
	year_dict = {"2015":"2016preAPV", "2016":"2016postAPV","2017":"2017","2018":"2018"}
	return year_dict[year]
if __name__=="__main__":
	years = ["2015","2016","2017","2018"]
	output_file = open("event_weight_latex_text.txt",'w')
	samples = ["QCDMC","TTbarMC","STMC","SuuToChiChi"]
	plot_types = ["h_btag_eventWeight_nom", "h_PU_eventWeight_nom", "h_L1Prefiring_eventWeight_nom","h_TopPT_eventWeight_nom", "h_JER_scaleFactor_nom"]
	#syst_names = []
	syst_type = ["event weight","event weight","event weight","event weight","scale factor applied to each AK8 jet"]
	for year in years:
		for iii,plot_type in enumerate(plot_types):
				print(plot_type)
				output_file.write(r"\begin{figure" + "}\n")
				output_file.write(r"\subfloat[]{\includegraphics[width = 3in]" + "{plots/cutflow_plots/%s_QCDMC_combined_%s.png}} \n"%(plot_type,year))
				output_file.write(r"\subfloat[]{\includegraphics[width = 3in]" + "{plots/cutflow_plots/%s_TTbarMC_combined_%s.png}}\\\n"%(plot_type,year))
				output_file.write(r"\subfloat[]{\includegraphics[width = 3in]" + "{plots/cutflow_plots/%s_STMC_combined_%s.png}}\n"%(plot_type,year))
				output_file.write(r"\subfloat[]{\includegraphics[width = 3in]" + "{plots/cutflow_plots/%s_SuuToChiChi_%s.png}} \n"%(plot_type,year))
				output_file.write(r"\caption{ " + "The nominal %s systematic %s for the combined QCD (a), TTbar (b), single top (c), and SuuToChiChi signal (d) samples for %s }"%(plot_type.split("_")[1], syst_type[iii],year_dict[year] )+ "\n")
				output_file.write(r"\label{fig:" + "%s_%s}\n"%(plot_type.split("_")[1],year) ) 
				output_file.write(r"\end{figure}" + "\n")
				output_file.write("\n")
				output_file.write("\n")
	output_file.close()
	print("Finished - output saved to event_weight_latex_text.txt")

