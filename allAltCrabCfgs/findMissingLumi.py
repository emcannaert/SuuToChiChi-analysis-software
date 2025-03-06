#from FWCore.DataStructs.LumiList import LumiList
#from LumiList.Lumilist import LumiList
from FWCore.PythonUtilities.LumiList import LumiList
originalLumiList1 = LumiList(filename='/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/allAltCrabCfgs/crab_projects_old/crab_clustAlg_QCDMC2000toInf_2018_JEC2_AltDatasets_000/results/input_dataset_lumis.json')
originalLumiList2 = LumiList(filename='/uscms_data/d3/cannaert/analysis/CMSSW_10_6_30/src/allAltCrabCfgs/crab_projects_old/crab_clustAlg_QCDMC2000toInf_2018_JEC2_AltDatasets_000/results/processedLumis.json')
print("originalLumiList1 is ", originalLumiList1)
print("originalLumiList2 is ", originalLumiList2)
print(originalLumiList1.getCompactList())
print(originalLumiList2.getCompactList())


print("originalLumiList1.filterLumiList() is ", originalLumiList1.filterLumiList())
print("originalLumiList2.filterLumiList() is ", originalLumiList2.filterLumiList())




newLumiList = originalLumiList1 - originalLumiList2
newLumiList.writeJSON('skippedLumis.json')
