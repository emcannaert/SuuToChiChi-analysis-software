from __future__ import division, print_function
import ROOT
import os
import numpy as np

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

import matplotlib.pyplot as plt

ROOT.gROOT.SetBatch(True)

years = ["2015", "2016", "2017", "2018"]

scale_factors = {
    "QCDMC1000to1500": [1.578683216, 1.482632755, 3.212373799, 4.407417122],
    "QCDMC1500to2000": [0.2119142341, 0.195224041, 0.3506426242, 0.5425809983],
    "QCDMC2000toInf":  [0.08568186031, 0.07572795371, 0.1528414409, 0.2277769275],
    "QCDMC_Pt_170to300":     [72.27560548, 58.13790684, 144.0132837, 208.6671047],
    "QCDMC_Pt_300to470":     [2.464537119, 2.077524247, 5.087240079, 7.056447936],
    "QCDMC_Pt_470to600":     [0.2122207081, 0.1770874866, 0.4500561659, 0.6298074855],
    "QCDMC_Pt_600to800":     [0.04929452011, 0.04041858714, 0.09634485522, 0.1387005244],
    "QCDMC_Pt_800to1000":    [0.01443931658, 0.01169252025, 0.02954986175, 0.04231249731],
    "QCDMC_Pt_1000to1400":   [0.007643465954, 0.006312623165, 0.01566430413, 0.0226523112],
    "QCDMC_Pt_1400to1800":   [0.001150615273, 0.001016564447, 0.00244639185, 0.003532486979],
    "QCDMC_Pt_1800to2400":   [0.000324331737, 0.0002806910428, 0.0006608229592, 0.000952638299],
    "QCDMC_Pt_2400to3200":   [0.00003408026676, 0.00003090490169, 0.00007246889556, 0.0001045278212],
    "QCDMC_Pt_3200toInf":    [0.000002648864, 0.000002290278112, 0.000005628836, 0.000008118931],
}

hist_name = "h_totHT"

def load_scaled_hist(dataset, year, iyear):
    
    hist_dir = "../combinedROOT/processedFiles/"
    fname = "%s_%s_processed.root" % (dataset, year)
    fname = hist_dir + fname
    
    if not os.path.exists(fname):
        print("Missing: %s" % fname)
        return None
    f = ROOT.TFile.Open(fname)
    h = f.Get("nom/"+hist_name)
    if not h:
        print("Missing hist %s in %s" % (hist_name, fname))
        return None
    h_clone = h.Clone("%s_%s_clone" % (dataset, year))
    h_clone.SetDirectory(0)
    h_clone.Scale(scale_factors[dataset][iyear])
    return h_clone

def hist_to_np(h):
    n = h.GetNbinsX()
    x = np.array([h.GetBinCenter(i+1) for i in range(n)])
    y = np.array([h.GetBinContent(i+1) for i in range(n)])
    e = np.array([h.GetBinError(i+1) for i in range(n)])
    return x, y, e

def add_hists(hlist):
    total = hlist[0].Clone("sum")
    for h in hlist[1:]:
        total.Add(h)
    return total

for iyear, year in enumerate(years):
    ht_hists = []
    pt_hists = []

    for ds in scale_factors:
        h = load_scaled_hist(ds, year, iyear)
        if h:
            if ds.startswith("QCDMC_Pt"):
                pt_hists.append(h)
            else:
                ht_hists.append(h)

    print("number of HT hists: %s, number of pt hists: %s."%(len(ht_hists),len(pt_hists)))


    if not ht_hists or not pt_hists:
        print("Skipping year %s due to missing histograms." % year)
        continue

    h_ht = add_hists(ht_hists)
    h_pt = add_hists(pt_hists)

    x_ht, y_ht, e_ht = hist_to_np(h_ht)
    x_pt, y_pt, e_pt = hist_to_np(h_pt)


    print("Ratios of HT/Pt-binned dataset content vs HT")
    for iii in range(len(x_ht)):
        print("--- HT = %s (bin %s), HT/Pt = %s (%s/%s)"%(x_ht[iii],iii, y_ht[iii]/y_pt[iii], y_ht[iii], y_pt[iii]  ))


    # Yield comparison
    plt.figure(figsize=(9, 6))
    plt.errorbar(x_ht, y_ht, yerr=e_ht, fmt="o", label="HT-binned QCD", color="blue")
    plt.errorbar(x_pt, y_pt, yerr=e_pt, fmt="s", label="pT-binned QCD", color="red")
    plt.xlabel("HT [GeV]")
    plt.ylabel("Scaled Events")
    plt.title("QCD HT vs Pt-binned comparison (%s)" % year)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("qcd_comparison_%s.png" % year)
    plt.close()

    # Relative uncertainty
    rel_ht = np.divide(e_ht, y_ht, out=np.zeros_like(e_ht), where=(y_ht > 0))
    rel_pt = np.divide(e_pt, y_pt, out=np.zeros_like(e_pt), where=(y_pt > 0))

    plt.figure(figsize=(9, 6))
    plt.plot(x_ht, rel_ht, "o-", label="HT rel. unc", color="blue")
    plt.plot(x_pt, rel_pt, "s--", label="pT rel. unc", color="red")
    plt.xlabel("HT [GeV]")
    plt.ylabel("Relative Statistical Uncertainty")
    plt.title("Stat. Uncertainty Comparison (%s)" % year)
    plt.yscale("log")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("qcd_stat_uncertainty_%s.png" % year)
    plt.close()