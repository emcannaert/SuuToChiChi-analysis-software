
### returns the data samples for a given year (no trailing underscore)

def return_data_samples(year):
	if year == "2015": return ["dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM","dataF-HIPM"]
	elif year == "2016": return ["dataF", "dataG", "dataH"]
	elif year == "2017": return ["dataB","dataC","dataD","dataE", "dataF"]
	elif year == "2018": return ["dataA","dataB","dataC","dataD"]
	else: 
		print("ERROR: incorrect year provided: %s (2015,2016,2017,2018 are valid)."%year)
		return None