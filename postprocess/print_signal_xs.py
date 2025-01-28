from return_signal_SF.return_signal_SF import return_Suu_to_chi_chi_xs


if __name__=="__main__":
	mass_points = ["Suu4_chi1", "Suu4_chi1p5", "Suu5_chi1","Suu5_chi1p5","Suu5_chi2","Suu6_chi1","Suu6_chi1p5","Suu6_chi2","Suu6_chi2p5","Suu7_chi1",
   "Suu7_chi1p5","Suu7_chi2","Suu7_chi2p5","Suu7_chi3","Suu8_chi1","Suu8_chi1p5","Suu8_chi2","Suu8_chi2p5","Suu8_chi3"]	
	decays = ["WBWB","ZTZT","HTHT","WBHT","WBZT","HTZT"]


	for mass_point in mass_points:
		for decay in decays:
   			return_Suu_to_chi_chi_xs(mass_point,decay)