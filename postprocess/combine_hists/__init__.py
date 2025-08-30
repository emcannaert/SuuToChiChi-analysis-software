import ROOT

def combine_hists(sample_types, file_paths, hist_name, hist_weights=None, new_title=None, hist_label = None):
    """
    Combines histograms from multiple ROOT files.

    Parameters:
    -----------
    sample_types : list of str
        Names of the sample types (keys to file_paths and hist_weights).
    file_paths : dict
        Dictionary mapping sample_type -> ROOT file path.
    hist_name : str
        Path to the histogram inside the ROOT file (e.g., "folder/histname").
    hist_weights : dict, optional
        Dictionary mapping sample_type -> weight factor (default 1 for all if None).
    new_title : str, optional
        Title for the combined histogram (defaults to original hist title of first sample).

    Returns:
    --------
    ROOT.TH1 : Combined histogram (directory set to 0 to avoid ownership issues)
    """

    combined_hist = None

    for sample in sample_types:
        file_path = file_paths[sample]
        weight = hist_weights.get(sample, 1.0) if hist_weights else 1.0

        # Open ROOT file
        f = ROOT.TFile.Open(file_path, "READ")
        if not f or f.IsZombie():
            raise RuntimeError("Could not open ROOT file: %s" % file_path)

        # Extract histogram
        hist = f.Get(hist_name)
        if not hist:
            raise RuntimeError("Histogram '%s' not found in %s" % (hist_name, file_path))

        # Clone to detach from file memory
        hist_clone = hist.Clone()
        hist_clone.SetDirectory(0)  # avoid ROOT memory ownership issues
        hist_clone.Scale(weight)

        if combined_hist is None:
            # First histogram initializes combined
            combined_hist = hist_clone
        else:
            combined_hist.Add(hist_clone)

        f.Close()

    if new_title:
        combined_hist.SetTitle(new_title)
    
    combined_hist.SetDirectory(0)
    if hist_label: combined_hist.SetName(hist_label)
    return combined_hist


"""
Example usage:

sample_types = ["WJets", "TTbar", "QCD"]
file_paths = {
    "WJets": "WJets.root",
    "TTbar": "TTbar.root",
    "QCD": "QCD.root"
}
hist_weights = {"WJets": 1.2, "TTbar": 0.8, "QCD": 1.0}

combined = combine_histograms(
    sample_types,
    file_paths,
    "myFolder/myHist",
    hist_weights=hist_weights,
    new_title="Combined Sample"
)"""
