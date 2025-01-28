import math
# overloaded version to work for the individual decays 
def return_signal_SF(year,mass_point,decay, y_uu = 2.0, y_x = 2.0):    ## parameters are theory couplings
	## input signal mass point in the format Suu$Mass_chi$Mass
	## can be imported into other modules when needed


	Suu_mass = 4000
	if "Suu5" in mass_point: Suu_mass = 5000
	elif "Suu6" in mass_point: Suu_mass = 6000
	elif "Suu7" in mass_point: Suu_mass = 7000
	elif "Suu8" in mass_point: Suu_mass = 8000

	chi_mass = 1000
	if "chi1p5" in mass_point: chi_mass = 1500
	if "chi2" in mass_point: chi_mass = 2000
	if "chi2p5" in mass_point: chi_mass = 2500
	if "chi3" in mass_point: chi_mass = 3000

	# the production xs of Suu depends on y_uu^2, all values below are reference values for y_uu = 2
	Suu_prod_xs = { "4000": 1000.  * (pow(1.0*y_uu,2) / pow(2.0,2) ),   #fb
					"5000": 500.   * (pow(1.0*y_uu,2) / pow(2.0,2) ),   #fb
					"6000": 200.   * (pow(1.0*y_uu,2) / pow(2.0,2) ),   #fb  
					"7000": 28     * (pow(1.0*y_uu,2) / pow(2.0,2) ),   #fb
					"8000": 3.5    * (pow(1.0*y_uu,2) / pow(2.0,2) )    #fb
	    }

	collected_data = {"2015":19.52,"2016":16.81, "2017":41.48, "2018":59.83}  # collected luminosity per year 

	WB_BR = 0.50
	ZT_BR = 0.25
	HT_BR = 0.25

	Z_had_BR = 0.6991
	W_had_BR = 0.6741
	H_had_BR = 0.58
	t_had_BR = 0.6741

	frac_of_events_used = 0.3

	nEvents = 0

	if decay in ["WBWB","ZTZT","HTHT"]:
		if "Suu8" in mass_point or "Suu7" in mass_point or "Suu6" in mass_point:
			nEvents = 30000
		else: nEvents = 60000
	elif decay in ["WBHT","WBZT","HTZT"]:
		if "Suu8" in mass_point or "Suu7" in mass_point or "Suu6" in mass_point:
			nEvents = 50000
		else: nEvents = 100000

	if year in ["2015","2016"]:
		nEvents /= 2   ### 2016preAPV and 2016postAPV have half as many stats
	lumi_eff = nEvents*frac_of_events_used/ (  Suu_prod_xs[ "%s"%Suu_mass ] * calculate_Suu_to_chi_chi_BR( Suu_mass, chi_mass, y_uu, y_x)    )
	lumi_year = collected_data[year]

	#print("decay is %s"%decay)
	#print("Suu_prod_xs is %f"%Suu_prod_xs[mass_point][year])
	#print("nevents is %i"%nEvents)

	#print("Effective luminosity is %f"%lumi_eff)
	SF_fullBR = lumi_year/lumi_eff

	#if not decay:
	#	return SF_fullBR

	WBWB_had_BR = (WB_BR*WB_BR)*(W_had_BR)*(W_had_BR)   # the Suu -> chi chi -> WBWB -> all had branching fraction
	HTHT_had_BR = (HT_BR*HT_BR)*(H_had_BR*t_had_BR)*(H_had_BR*t_had_BR)
	ZTZT_had_BR = (ZT_BR*ZT_BR)*(Z_had_BR*t_had_BR)*(Z_had_BR*t_had_BR)
	WBHT_had_BR = 2*(WB_BR*HT_BR)*(W_had_BR)*(H_had_BR*t_had_BR)
	WBZT_had_BR = 2*(WB_BR*ZT_BR)*(W_had_BR)*(Z_had_BR*t_had_BR)
	HTZT_had_BR = 2*(HT_BR*ZT_BR)*(H_had_BR*t_had_BR)*(Z_had_BR*t_had_BR)


	if decay == "WBWB":
		return SF_fullBR*WBWB_had_BR
	elif decay == "HTHT":
		return SF_fullBR*HTHT_had_BR
	elif decay == "ZTZT":
		return SF_fullBR*ZTZT_had_BR
	elif decay == "WBHT":
		return SF_fullBR*WBHT_had_BR
	elif decay == "WBZT":
		return SF_fullBR*WBZT_had_BR
	elif decay == "HTZT":
		return SF_fullBR*HTZT_had_BR
	else:
		print("ERROR: decay %s did not match any of the accepted SuuToChiChi decays (WBWB,HTHT,ZTZT,WBHT,WBZT,HTZT)."%decay)
		return None


def return_Suu_to_chi_chi_xs(mass_point,decay, y_uu = 2.0, y_x = 2.0):
	## input signal mass point in the format Suu$Mass_chi$Mass
	## can be imported into other modules when needed


	Suu_mass = 4000
	if "Suu5" in mass_point: Suu_mass = 5000
	elif "Suu6" in mass_point: Suu_mass = 6000
	elif "Suu7" in mass_point: Suu_mass = 7000
	elif "Suu8" in mass_point: Suu_mass = 8000

	chi_mass = 1000
	if "chi1p5" in mass_point: chi_mass = 1500
	if "chi2" in mass_point: chi_mass = 2000
	if "chi2p5" in mass_point: chi_mass = 2500
	if "chi3" in mass_point: chi_mass = 3000

	# the production xs of Suu depends on y_uu^2, all values below are reference values for y_uu = 2
	Suu_prod_xs = { "4000": 1000.  * (pow(1.0*y_uu,2) / pow(2.0,2) ),   #fb
					"5000": 500.   * (pow(1.0*y_uu,2) / pow(2.0,2) ),   #fb
					"6000": 200.   * (pow(1.0*y_uu,2) / pow(2.0,2) ),   #fb  
					"7000": 28     * (pow(1.0*y_uu,2) / pow(2.0,2) ),   #fb
					"8000": 3.5    * (pow(1.0*y_uu,2) / pow(2.0,2) )    #fb 
	}

	collected_data = {"2015":19.52,"2016":16.81, "2017":41.48, "2018":59.83}  # collected luminosity per year 

	WB_BR = 0.50
	ZT_BR = 0.25
	HT_BR = 0.25

	Z_had_BR = 0.6991
	W_had_BR = 0.6741
	H_had_BR = 0.58
	t_had_BR = 0.6741

	WBWB_had_BR = (WB_BR*WB_BR)*(W_had_BR)*(W_had_BR)   # the Suu -> chi chi -> WBWB -> all had branching fraction
	HTHT_had_BR = (HT_BR*HT_BR)*(H_had_BR*t_had_BR)*(H_had_BR*t_had_BR)
	ZTZT_had_BR = (ZT_BR*ZT_BR)*(Z_had_BR*t_had_BR)*(Z_had_BR*t_had_BR)
	WBHT_had_BR = 2*(WB_BR*HT_BR)*(W_had_BR)*(H_had_BR*t_had_BR)
	WBZT_had_BR = 2*(WB_BR*ZT_BR)*(W_had_BR)*(Z_had_BR*t_had_BR)
	HTZT_had_BR = 2*(HT_BR*ZT_BR)*(H_had_BR*t_had_BR)*(Z_had_BR*t_had_BR)

	Suu_to_chi_chi_to_VLQs_xs = Suu_prod_xs[ "%s"%Suu_mass ] * calculate_Suu_to_chi_chi_BR( Suu_mass, chi_mass, y_uu, y_x) 




	if decay == "WBWB":
		print( "mass point is %s, decay is %s, Suu production xs is %s, Suu -> chi chi BR is %s, hadronic BR is %s, total xs is %s."%(mass_point,decay,Suu_prod_xs[ "%s"%Suu_mass ], calculate_Suu_to_chi_chi_BR( Suu_mass, chi_mass, y_uu, y_x),WBWB_had_BR , Suu_to_chi_chi_to_VLQs_xs*WBWB_had_BR ) )

		return Suu_to_chi_chi_to_VLQs_xs*WBWB_had_BR
	elif decay == "HTHT":
		print( "mass point is %s, decay is %s, Suu production xs is %s, Suu -> chi chi BR is %s, hadronic BR is %s, total xs is %s."%(mass_point,decay,Suu_prod_xs[ "%s"%Suu_mass ], calculate_Suu_to_chi_chi_BR( Suu_mass, chi_mass, y_uu, y_x), HTHT_had_BR, Suu_to_chi_chi_to_VLQs_xs*HTHT_had_BR ) )

		return Suu_to_chi_chi_to_VLQs_xs*HTHT_had_BR
	elif decay == "ZTZT":
		print( "mass point is %s, decay is %s, Suu production xs is %s, Suu -> chi chi BR is %s, hadronic BR is %s, total xs is %s."%(mass_point,decay,Suu_prod_xs[ "%s"%Suu_mass ], calculate_Suu_to_chi_chi_BR( Suu_mass, chi_mass, y_uu, y_x), ZTZT_had_BR,Suu_to_chi_chi_to_VLQs_xs*ZTZT_had_BR ) )

		return Suu_to_chi_chi_to_VLQs_xs*ZTZT_had_BR
	elif decay == "WBHT":
		print( "mass point is %s, decay is %s, Suu production xs is %s, Suu -> chi chi BR is %s, hadronic BR is %s, total xs is %s."%(mass_point,decay,Suu_prod_xs[ "%s"%Suu_mass ], calculate_Suu_to_chi_chi_BR( Suu_mass, chi_mass, y_uu, y_x), WBHT_had_BR, Suu_to_chi_chi_to_VLQs_xs*WBHT_had_BR ) )

		return Suu_to_chi_chi_to_VLQs_xs*WBHT_had_BR
	elif decay == "WBZT":
		print( "mass point is %s, decay is %s, Suu production xs is %s, Suu -> chi chi BR is %s, hadronic BR is %s, total xs is %s."%(mass_point,decay,Suu_prod_xs[ "%s"%Suu_mass ], calculate_Suu_to_chi_chi_BR( Suu_mass, chi_mass, y_uu, y_x), WBZT_had_BR, Suu_to_chi_chi_to_VLQs_xs*WBZT_had_BR ) )

		return Suu_to_chi_chi_to_VLQs_xs*WBZT_had_BR
	elif decay == "HTZT":
		print( "mass point is %s, decay is %s, Suu production xs is %s, Suu -> chi chi BR is %s, hadronic BR is %s, total xs is %s."%(mass_point,decay,Suu_prod_xs[ "%s"%Suu_mass ], calculate_Suu_to_chi_chi_BR( Suu_mass, chi_mass, y_uu, y_x),HTZT_had_BR,Suu_to_chi_chi_to_VLQs_xs*HTZT_had_BR  ) )

		return Suu_to_chi_chi_to_VLQs_xs*HTZT_had_BR
	else:
		print("ERROR: decay %s did not match any of the accepted SuuToChiChi decays (WBWB,HTHT,ZTZT,WBHT,WBZT,HTZT)."%decay)
		return None



def calculate_Suu_to_chi_chi_BR(Suu_mass, chi_mass, y_uu = 2.0, y_x = 2.0):
	# y_x = sqrt(pow(y_x_R,2) = pow(y_x_L,2)), eq 2.3 from bogdan's paper http://www.arxiv.org/pdf/1810.09429
	
	 # Suu to up quark pair partial width
	tau_SuuToUU = pow(y_uu , 2)* Suu_mass / (32*math.pi)   

	# Suu to VLQ pair partial width  (eq 2.8 of Bogdan's paper)

	tau_SuuToChiChi = ( pow(y_x,2) * Suu_mass * ( 1 - 2*pow( (1.0*chi_mass)/(1.0*Suu_mass),2) ) * pow(  1 - 4*pow( (1.0*chi_mass)/(1.0*Suu_mass),2)  ,0.5) )  / ( 32*math.pi )

	#print("The branching fraction for M_Suu = %s / M_chi = %s is "%(Suu_mass,chi_mass), ( tau_SuuToChiChi / (tau_SuuToChiChi + tau_SuuToUU) ) ) 
	return (tau_SuuToChiChi / (tau_SuuToChiChi + tau_SuuToUU))








