import json
import os

def add_str_to_lines(f_name, str_to_add): 
    with open(f_name, "r") as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            lines[index] = str_to_add + line.strip() + "\n"
    with open(f_name, "w") as f:
        for line in lines:
            f.write(line)

#year = 2015
#files = ['sigsamples_%d.json'%year]

name = "QCD_HT1000to1500"
inputDataset = "/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM"
year = 2016

#year = 2015
#files = ['mcsamples_%d.json'%year]

#for i, infile in enumerate(files):
   #with open(infile) as json_file:
     #data = json.load(json_file)
     #for p in data:
       #if p['name']=="TTGamma_Dilept":
        #if p['name']=="TTGJets":
if 1:
         print ("**********************")
         #fname = "%s_%d.txt" % (p['name'], year)
         #cmd = 'dasgoclient -query="parent dataset=%s" > %s' % (p['inputDataset'], fname)
         fname = "%s_%d.txt" % (name, year)
         cmd = 'dasgoclient -query="parent dataset=%s" > %s' % (inputDataset, fname)
         print(cmd)
         os.system(cmd)
         with open(fname) as file:
             line = file.readline()
         line = line.rstrip('\n')
         cmd = 'dasgoclient -query="file dataset=%s" > %s' % (line, fname)
         print(cmd)
         os.system(cmd)
         add_str_to_lines(fname, "root://cmsxrootd.fnal.gov//")
         cmd = 'cmsRun ana.py inputFiles="%s" maxEvents=-1' % (fname)
         print(cmd)
         os.system(cmd)
         print ("**********************")
         #break 
