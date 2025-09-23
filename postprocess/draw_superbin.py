import ROOT
import ast
import random

### this script will show what a specific superbin looks like. Now added functionality to test what superbin groups look like.

def generate_random_numbers(n, lower=1, upper=10000):
    return [random.randint(lower, upper) for _ in range(n)]

def load_superbin_indices(year,technique_str, region="SR"):    # load in the superbin indices (located in a text file )
	_superbin_indices = []

	index_file_home = "binMaps/"

	open_file = open(index_file_home+"QCDPT_superbin_indices%s_%s.txt"%(technique_str,year),"r")
	for line in open_file:
		columns = line.split('/')
		if columns[0] == year and columns[1] == region:
			_superbin_indices = columns[3]
	open_file.close()
	return ast.literal_eval(_superbin_indices)


def load_superbin_groups(year,technique_str, region="SR"):    # load in the superbin indices (located in a text file )
	_superbin_indices = []

	index_file_home = "superbinGroups/"

	open_file = open(index_file_home+"QCDPT_superbin_groups%s_%s.txt"%(technique_str,year),"r")
	for line in open_file:
		columns = line.split('/')
		if columns[0] == year and columns[1] == region:
			_superbin_groups = columns[3]
	open_file.close()
	return ast.literal_eval(_superbin_groups)




def draw_superbin(year, technique_str, superbin_number, region, superbin_indices,canvas,output_pdf_name):


	output_dir = "plots/superbins/"
	#output_pdf_name  = output_dir+"superbins_%s_%s%s.pdf"%(region, technique_str,year)

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



def draw_superbin_group(year, technique_str, superbin_group_number, region, superbin_groups,canvas,output_pdf_name, superbin_indices):


	output_dir = "plots/superbinGroups/"
	#output_pdf_name  = output_dir+"superbin_groups_%s_%s%s.pdf"%(region, technique_str,year)




	#print("superbin_groups: %s"%superbin_groups)
	print("superbin_group_number: %s"%superbin_group_number)

	# List of bins to be filled, each as a tuple (x_bin_number, y_bin_number)
	superbin_group = superbin_groups[superbin_group_number]

	print("superbin_group: %s."%superbin_group)
	# Create a 2D histogram with the specified dimensions and limits
	hist = ROOT.TH2F("selected_superbin_group%s"%superbin_group_number, "%s superbin group %s (containing superbins %s) for %s"%(region,superbin_group_number, superbin_group, year), 22, 1250, 10000, 20, 500, 5000) # x-axis: 22 bins, range [1250, 10000]   # y-axis: 20 bins, range [500, 5000]

	random_numbers = generate_random_numbers(len(superbin_group))

	print("Length of random_numbers is %s."%len(random_numbers))
	for iii,superbin_index in enumerate(superbin_group):

		print("For superbin group #%s, drawing superbin #%s"%(superbin_group_number + 1, superbin_index))
		superbin_indices_to_draw = superbin_indices[superbin_index]

		for x_bin, y_bin in superbin_indices_to_draw:
			hist.SetBinContent(x_bin+1, y_bin+1, random_numbers[iii])

		#fill_value += 10.0

	# Value to fill in each bin

	# Fill the specified bins with the given value


	# Optional: Draw the histogram for visualization

	hist.Draw("COLZ")  
	canvas.SaveAs(output_pdf_name)

	#canvas.SaveAs(output_dir+"superbin%s_%s_%s.png"%(superbin_number,region,year))  # Save the histogram as an image







if __name__=="__main__":
	years = ["2015","2016","2017","2018"]
	regions = ["SR","AT1b"  ]
	technique_strs = ["", "NN_"]

	technique_strs = [""]
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




	output_dir = "plots/superbinGroups/"


	for year in years:
		for region in regions:
			for technique_str in technique_strs:
				superbin_groups  = load_superbin_groups(year,technique_str,region)
				superbin_indices = load_superbin_indices(year,technique_str,region)

				output_pdf_name  = output_dir+"superbin_groups_%s_%s%s.pdf"%(region, technique_str,year)
				canvas.SaveAs(output_pdf_name + "(")

				for iii in range(0,len(superbin_groups)):	
					bin_number = iii	
					print("For year/region/technique, superbin iii: %s/%s/%s, %s"%(year,region,technique_str,iii))
					draw_superbin_group(year, technique_str, bin_number, region, superbin_groups,canvas,output_pdf_name, superbin_indices)

				canvas.SaveAs(output_pdf_name + ")")








