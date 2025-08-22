import matplotlib
matplotlib.use('Agg')  # batch mode for non-GUI environments
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def parse_file(filepath):
    with open(filepath) as f:
        lines = f.readlines()

    headers = lines[0].strip().split()
    wps = []
    data = {}
    for colname in headers[1:]:
        data[colname] = []

    for line in lines[1:]:
        if line.strip().startswith("#") or not line.strip():
            continue
        fields = line.strip().split()
        if len(fields) != len(headers):
            print("Warning: Skipping malformed line: {}".format(line.strip()))
            continue

        try:
            wp = float(fields[0])
        except ValueError:
            continue

        wps.append(wp)

        for i, colname in enumerate(headers[1:]):
            try:
                value = float(fields[i + 1])
            except (ValueError, IndexError):
                value = np.nan
            data[colname].append(value)

    return wps, data

# Years to process
years = ["2015", "2016", "2017", "2018"]

# Color and line style setup
colors = sns.color_palette("tab20", 20)
line_styles = ['-', '--', '-.', ':']

for year in years:
    path = "txt_files/WP_study_yields/SR_event_summary_{}.txt".format(year)
    print("Processing: {}".format(path))

    wps, data = parse_file(path)

    plt.figure(figsize=(14, 8))

    keys = sorted(data.keys())
    num_colors = len(colors)
    num_linestyles = len(line_styles)

    for i, key in enumerate(keys):
        color = colors[i % num_colors]
        linestyle = line_styles[(i // num_colors) % num_linestyles]
        lwidth = 1.8

        if key == "N_BR_SR":
            color = 'k'
            linestyle = '--'
            lwidth = 3.0  # Make BR line thicker and black

        plt.plot(wps, data[key], label=key, color=color, linestyle=linestyle, linewidth=lwidth)

    plt.xlabel("Tagging Working Point")
    plt.ylabel("Events in SR")
    plt.yscale("log")
    plt.title("Signal and Background Yields vs WP ({})".format(year))
    plt.legend(loc="upper right", fontsize="x-small", ncol=2)
    plt.grid(True, which="both", linestyle=":", linewidth=1.0)

    plt.tight_layout()
    plt.savefig("yields_vs_WP_{}.png".format(year), dpi=300)
    plt.close()