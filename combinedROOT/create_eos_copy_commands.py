import os, sys
import pickle
import numpy as np



if __name__=="__main__":
	#try:


					 

	# keeping track of how many copy commands have already been made for each of the samples and systematics

	nCommands	= {  "2015": { "QCDMC2000toInf": { 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },     #nCommands[year][sample][systematic]
					 "QCDMC1500to2000":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_s-channel-hadronsMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "TTToHadronicMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "TTToSemiLeptonicMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "TTToLeptonicMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  }, 
					 "TTJetsMCHT800to1200":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 },
					 "TTJetsMCHT1200to2500":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 },
					 "TTJetsMCHT2500toInf":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 },
					 "ST_t-channel-antitop_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_t-channel-top_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_s-channel-leptonsMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_tW-antiTop_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_tW-top_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_LNu-HT800to1200":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_LNu-HT1200to2500":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_LNu-HT2500toInf":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_QQ-HT800toInf":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WW_MC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ZZ_MC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "dataB-ver2":{'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 } ,
					 "dataC-HIPM":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 } ,
					 "dataD-HIPM":{'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 } ,
					 "dataF-HIPM":{'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 } , 
					 "dataE-HIPM":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  }} , 
					 "2016": { "QCDMC2000toInf": { 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "QCDMC1500to2000":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "TTToHadronicMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "TTToSemiLeptonicMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "TTToLeptonicMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "TTJetsMCHT800to1200":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 },
					 "TTJetsMCHT1200to2500":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 },
					 "TTJetsMCHT2500toInf":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 },
					 "ST_t-channel-antitop_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_t-channel-top_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_s-channel-hadronsMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_s-channel-leptonsMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_tW-antiTop_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_tW-top_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_LNu-HT800to1200":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_LNu-HT1200to2500":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_LNu-HT2500toInf":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_QQ-HT800toInf":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WW_MC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ZZ_MC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					  "dataF":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  } ,
					 "dataG":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  } ,
					 "dataH":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  }  } ,
					 "2017": { "QCDMC2000toInf": { 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "QCDMC1500to2000":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "TTToHadronicMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "TTToSemiLeptonicMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "TTToLeptonicMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0    },
					 "TTJetsMCHT800to1200":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 },
					 "TTJetsMCHT1200to2500":{'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 },
					 "TTJetsMCHT2500toInf":{'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 },
					  "ST_t-channel-antitop_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_t-channel-top_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_s-channel-hadronsMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_s-channel-leptonsMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_tW-antiTop_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_tW-top_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_LNu-HT800to1200":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_LNu-HT1200to2500":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_LNu-HT2500toInf":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_QQ-HT800toInf":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WW_MC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ZZ_MC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "dataB":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  } ,
					 "dataC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0   } ,
					 "dataD":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  } ,
					 "dataE":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  } , 
					 "dataF":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  }  } ,
					 "2018": { "QCDMC2000toInf": { 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "QCDMC1500to2000":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "QCDMC1000to1500":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "TTToHadronicMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "TTToSemiLeptonicMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "TTToLeptonicMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "TTJetsMCHT800to1200":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 },
					 "TTJetsMCHT1200to2500":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 },
					 "TTJetsMCHT2500toInf":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0 },
					 "ST_t-channel-antitop_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_t-channel-top_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_s-channel-hadronsMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_s-channel-leptonsMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_tW-antiTop_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ST_tW-top_inclMC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_LNu-HT800to1200":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_LNu-HT1200to2500":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_LNu-HT2500toInf":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WJetsMC_QQ-HT800toInf":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "WW_MC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					 "ZZ_MC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  },
					  "dataA":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  }   ,
					 "dataB":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  } ,
					 "dataC":{ 'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  } ,
					 "dataD":{'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  }  } }
	all_files_made	= {  "2015": { "QCDMC2000toInf": { 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },     #nCommands[year][sample][systematic]
					 "QCDMC1500to2000":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "TTToHadronicMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "TTToSemiLeptonicMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "TTToLeptonicMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "TTJetsMCHT1200to2500":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "TTJetsMCHT2500toInf":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "ST_t-channel-antitop_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_t-channel-top_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_s-channel-hadronsMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_s-channel-leptonsMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_tW-antiTop_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_tW-top_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					"TTJetsMCHT800to1200":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "WJetsMC_LNu-HT800to1200":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "WJetsMC_LNu-HT1200to2500":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]   },
					 "WJetsMC_LNu-HT2500toInf":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "WJetsMC_QQ-HT800toInf":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "WW_MC":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ZZ_MC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "dataB-ver2":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } ,
					 "dataC-HIPM":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } ,
					 "dataD-HIPM":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } ,
					 "dataE-HIPM":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } , 
					 "dataF-HIPM":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  }  }, 
					 "2016": { "QCDMC2000toInf": { 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "QCDMC1500to2000":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "TTToHadronicMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "TTToSemiLeptonicMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "TTToLeptonicMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "TTJetsMCHT1200to2500":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "TTJetsMCHT2500toInf":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "ST_t-channel-antitop_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_t-channel-top_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_s-channel-hadronsMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_s-channel-leptonsMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_tW-antiTop_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_tW-top_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } ,
					"TTJetsMCHT800to1200":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "WJetsMC_LNu-HT800to1200":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "WJetsMC_LNu-HT1200to2500":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]   },
					 "WJetsMC_LNu-HT2500toInf":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "WJetsMC_QQ-HT800toInf":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
 					 "WW_MC":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ZZ_MC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "dataF":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } ,
					 "dataG":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } ,
					 "dataH":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } } ,
					 "2017": { "QCDMC2000toInf": { 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "QCDMC1500to2000":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "TTToHadronicMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "TTToSemiLeptonicMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "TTToLeptonicMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "TTJetsMCHT1200to2500":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "TTJetsMCHT2500toInf":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "ST_t-channel-antitop_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_t-channel-top_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_s-channel-hadronsMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_s-channel-leptonsMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_tW-antiTop_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_tW-top_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					"TTJetsMCHT800to1200":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "WJetsMC_LNu-HT800to1200":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "WJetsMC_LNu-HT1200to2500":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]   },
					 "WJetsMC_LNu-HT2500toInf":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "WJetsMC_QQ-HT800toInf":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
 					 "WW_MC":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ZZ_MC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "dataB":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } ,
					 "dataC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } ,
					 "dataD":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } ,
					 "dataE":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } , 
					 "dataF":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } } ,

					 "2018": { "QCDMC2000toInf": { 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "QCDMC1500to2000":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "QCDMC1000to1500":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "TTToHadronicMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "TTToSemiLeptonicMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "TTToLeptonicMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } ,
					 "TTJetsMCHT1200to2500":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "TTJetsMCHT2500toInf":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "ST_t-channel-antitop_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_t-channel-top_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_tW-antiTop_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_s-channel-hadronsMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_s-channel-leptonsMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ST_tW-top_inclMC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  }  , 
					 "TTJetsMCHT800to1200":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "WJetsMC_LNu-HT800to1200":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[] },
					 "WJetsMC_LNu-HT1200to2500":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]   },
					 "WJetsMC_LNu-HT2500toInf":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "WJetsMC_QQ-HT800toInf":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "WW_MC":{'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "ZZ_MC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  },
					 "dataA":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  }   ,
					 "dataB":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } ,
					 "dataC":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } ,
					 "dataD":{ 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  } }}


	samples = ["QCDMC2000toInf","QCDMC1500to2000","QCDMC1000to1500","TTToHadronicMC", "TTToLeptonicMC", "TTToSemiLeptonicMC","TTJetsMCHT1200to2500", "TTJetsMCHT2500toInf","ST_t-channel-antitop_inclMC", "ST_t-channel-top_inclMC", "ST_tW-antiTop_inclMC","ST_tW-top_inclMC",
	"ST_s-channel-hadronsMC",
	"ST_s-channel-leptonsMC", "dataB-ver2","dataC-HIPM","dataD-HIPM","dataE-HIPM","dataF-HIPM", "dataF", "dataG", "dataH","dataB","dataC","dataD","dataE", "dataF", "dataA",
"TTJetsMCHT800to1200",
"WJetsMC_LNu-HT800to1200",
"WJetsMC_LNu-HT1200to2500",
"WJetsMC_LNu-HT2500toInf",
"WJetsMC_QQ-HT800toInf",
	"WW_MC",
	"ZZ_MC"

	]

	signal_samples_pkl = open('../data/pkl/signal_samples.pkl', 'r')
  	signal_samples     = pickle.load(signal_samples_pkl)
	signal_samples = np.array(signal_samples)

  	signal_nCommands_pkl = open('../data/pkl/signal_nCommands.pkl', 'r')
  	signal_nCommands     = pickle.load(signal_nCommands_pkl)
	signal_nCommands["2015"]["SuuToChiChi"] = {'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  }
	signal_nCommands["2016"]["SuuToChiChi"] = {'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  }
	signal_nCommands["2017"]["SuuToChiChi"] = {'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  }
	signal_nCommands["2018"]["SuuToChiChi"] = {'JEC1':0, 'JEC2':0, 'JER':0,'nom':0  }

	signal_files_made_pkl = open('../data/pkl/signal_files_made.pkl', 'r')
  	signal_files_made     = pickle.load(signal_files_made_pkl)

  	signal_files_made["2015"]["SuuToChiChi"] = { 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  }
  	signal_files_made["2016"]["SuuToChiChi"] = { 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  }
  	signal_files_made["2017"]["SuuToChiChi"] = { 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  }
  	signal_files_made["2018"]["SuuToChiChi"] = { 'JEC1':[], 'JEC2': [], 'JER':[],'nom':[]  }



	years = ["2015","2016","2017","2018"]
	eos_path = open(sys.argv[1], "r")
	command_path = open("eos_copy_commands.sh", "w")
	for line in eos_path:
		if line.split() == "[]" or line == "\n" or line == "":
			continue
		num_str = ""
		year_str = ""
		sys_str = ""
		sample_str = ""
		for sample in samples:
			if sample in line and sample_str == "":
				sample_str = sample
		for sample in signal_samples:
			if sample in line  and sample_str == "":
				sample_str = sample
		
		if "JEC1" in line:
			sys_str = "JEC1"
		elif "JEC2" in line:
			sys_str = "JEC2"
		elif "JER" in line:
			sys_str = "JER"
		elif "data" in line and "__" in line:
			sys_str = "nom"
		else:   #nominal systematic calculations
			sys_str = "nom"
		for year in years:
			if "_%s_"%year in line:
				year_str = year		
		if sample_str == "" or year_str == "":
			print("Can't figure out what type of file this is (QCD,TTbar,etc.) or what the year is: ")
			print("Line is: ", line.strip())
			continue
		#print("num/year/sys/sample = %s/%s/%s/%s"%(num_str,year_str,sys_str,sample_str))
		if "Suu" in sample_str:
			num_str = "%s"%(signal_nCommands[year_str][sample_str][sys_str])
			#print("num/year/sys/sample = %s/%s/%s/%s"%(num_str,year_str,sys_str,sample_str))
			signal_files_made[year_str][sample_str][sys_str].append("%s_%s_%s_combined_%s.root"%(sample_str, year_str, sys_str, num_str))
			signal_nCommands[year_str][sample_str][sys_str]+=1
		else:

			num_str = "%s"%(nCommands[year_str][sample_str][sys_str])
			all_files_made[year_str][sample_str][sys_str].append("%s_%s_%s_combined_%s.root"%(sample_str, year_str, sys_str, num_str))
			nCommands[year_str][sample_str][sys_str]+=1
		pipe = '|'
		command_path.write(r'hadd -f %s_%s_%s_combined_%s.root `xrdfsls -u %s %s grep "\.root"`'%(sample_str, year_str, sys_str, num_str,line.strip(),pipe) + "\n")

	#print(all_files_made)
	### now add to this .sh script a section that combines all files together into a single "_combined.root", renames files to this if they don't need to be added together
	for year,year_dict in all_files_made.items():
		for sample, sample_dict in year_dict.items():
			for syst,syst_dict in sample_dict.items():
				combined_file_name = "%s_%s_%s_combined.root"%(sample, year, syst)
				if len(syst_dict) > 1:    # if there are actually files in this 
					command_path.write('hadd -f %s '%combined_file_name)
					for iii,one_file in enumerate(syst_dict):
						command_path.write(" %s"%one_file.strip()) 
						if iii == (len(syst_dict)-1):
							command_path.write("\n")
				elif len(syst_dict) == 1:
					## rename the one file 
					command_path.write("mv %s %s\n"%(syst_dict[0], combined_file_name) )

	## merge together the signal files
	for year,year_dict in signal_files_made.items():
		for sample, sample_dict in year_dict.items():
			for syst,syst_dict in sample_dict.items():
				combined_file_name = "%s_%s_%s_combined.root"%(sample, year, syst)
				if len(syst_dict) > 1:    # if there are actually files in this 
					command_path.write('hadd -f %s '%combined_file_name)
					for iii,one_file in enumerate(syst_dict):
						command_path.write(" %s"%one_file.strip()) 
						if iii == (len(syst_dict)-1):
							command_path.write("\n")
				elif len(syst_dict) == 1:
					## rename the one file 
					command_path.write("mv %s %s\n"%(syst_dict[0], combined_file_name) )

	#except:
	#	print("Enter in a valid text file with a list of the files you want to copy from EOS (no spaces in between)")
	#	pass
