import ROOT
import ast

### this script will show what a specific superbin looks like 

def load_superbin_indices(year,technique_str, region="SR"):    # load in the superbin indices (located in a text file )
	_superbin_indices = []

	index_file_home = "binMaps/"

	open_file = open(index_file_home+"superbin_indices%s_%s.txt"%(technique_str,year),"r")
	for line in open_file:
		columns = line.split('/')
		if columns[0] == year and columns[1] == region:
			_superbin_indices = columns[3]
	open_file.close()
	return ast.literal_eval(_superbin_indices)



def draw_superbin(year, technique_str, superbin_number, region, superbin_indices,canvas,output_pdf_name):


	output_dir = "plots/superbins/"
	output_pdf_name  = output_dir+"superbins_%s_%s%s.pdf"%(region, technique_str,year)

	# Create a 2D histogram with the specified dimensions and limits
	hist = ROOT.TH2F("selected_superbin", "%s superbin #%s for %s"%(region,superbin_number,year), 
	                 22, 1250, 10000,  # x-axis: 22 bins, range [1250, 10000]
	                 20, 500, 5000)    # y-axis: 20 bins, range [500, 5000]


	# List of bins to be filled, each as a tuple (x_bin_number, y_bin_number)
	bins_to_fill = superbin_indices[superbin_number]

	# Value to fill in each bin
	fill_value = 1.0

	# Fill the specified bins with the given value
	for x_bin, y_bin in bins_to_fill:
	    hist.SetBinContent(x_bin+1, y_bin+1, fill_value)

	# Optional: Draw the histogram for visualization

	hist.Draw("COLZ")  
	canvas.SaveAs(output_pdf_name)

	#canvas.SaveAs(output_dir+"superbin%s_%s_%s.png"%(superbin_number,region,year))  # Save the histogram as an image



if __name__=="__main__":
	years = ["2015","2016","2017","2018"]
	regions = ["SR","AT1b"  ]
	technique_strs = ["", "NN_"]


	canvas = ROOT.TCanvas("canvas", "Canvas", 1200, 1000)
	ROOT.gStyle.SetOptStat(0)
	
	output_dir = "plots/superbins/"

	for year in years:
		for region in regions:
			for technique_str in technique_strs:

				superbin_indices = load_superbin_indices(year,technique_str,region)

				output_pdf_name  = output_dir+"superbins_%s_%s%s.pdf"%(region, technique_str,year)
				canvas.SaveAs(output_pdf_name + "(")

				for iii in range(0,len(superbin_indices)):	
					bin_number = iii	
					print("For year/region/technique, superbin iii: %s/%s/%s, %s"%(year,region,technique_str,iii))
					draw_superbin(year, technique_str, bin_number, region, superbin_indices,canvas,output_pdf_name)

				canvas.SaveAs(output_pdf_name + ")")






