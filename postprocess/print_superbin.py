import ast
import argparse

def load_superbin_indices(year, region, superbin_number, technique_str=""):
    # load in the superbin indices (located in a text file)
    _superbin_indices = []
    open_file = open("binMaps/superbin_indices%s_%s.txt" % (technique_str, year), "r")
    for line in open_file:
        columns = line.split('/')
        if columns[0] == year and columns[1] == region:
            _superbin_indices = columns[3]
    open_file.close()
    return ast.literal_eval(_superbin_indices)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load superbin indices.")
    parser.add_argument("--year", type=str, required=True, help="Year of the data (e.g., 2017)")
    parser.add_argument("--region", type=str, required=True, help="Region to load (e.g., 'SR')")
    parser.add_argument("--technique_str", type=str, default="", help="Technique string ('' or 'NN_'")
    parser.add_argument("--superbin_number", type=str, required=True, help="Superbin index")

    args = parser.parse_args()

    superbin_indices = load_superbin_indices(args.year, args.region, args.superbin_number, args.technique_str)
    print("Superbin %s for year %s, region %s, technique_str %s: %s"%(args.superbin_number, args.year,args.region, args.technique_str,superbin_indices[int(args.superbin_number)] ))