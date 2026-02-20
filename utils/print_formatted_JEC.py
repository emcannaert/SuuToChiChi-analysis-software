import argparse

def parse_jec_file(filename):
    jec = {}
    current_source = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("{") or line.startswith(r'#'):
                continue

            if line.startswith("[") and line.endswith("]"):
                current_source = line[1:-1]
                jec[current_source] = []
                continue

            parts = line.split()
            nums = [float(x) for x in parts]

            eta_min = nums[0]
            eta_max = nums[1]

            # ignore the mysterious CMS field
            data = nums[3:]

            if len(data) % 3 != 0:
                raise ValueError("Malformed JEC line:\n" + line)

            n_pt = len(data) // 3

            row = []
            for i in range(n_pt):
                pt = data[3*i]
                unc = data[3*i + 2]  # symmetric
                row.append((pt, unc))

            jec[current_source].append((eta_min, eta_max, row))

    return jec


def print_jec_matrices(jec):
    for source in jec:
        print("===================================")
        print(source)
        print("===================================")

        # Assume pT bins are identical for all eta bins
        first_eta = jec[source][0]
        pt_bins = [pt for pt, _ in first_eta[2]]

        # Header
        header = "eta_min eta_max"
        for pt in pt_bins:
            header += "  %7.1f" % pt
        print(header)

        # Rows
        for eta_min, eta_max, pt_vals in jec[source]:
            row = "%6.2f %6.2f" % (eta_min, eta_max)
            for _, unc in pt_vals:
                row += "  %7.4f" % unc
            print(row)

        print("")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Linearize 2D histograms in order to reach a minimum stat uncertainty and scaled/unscaled bin yield. ")
    parser.add_argument("-file", "--file", type=str, required=True, help="Path to the JEC file to print.")

    args = parser.parse_args()

    jec = parse_jec_file(args.file)
    print_jec_matrices(jec)
