import os,sys
import numpy as numpy


def scale_samples(year,systematic):

if __name__=="__main__":
	years = ["2015","2016","2017","2018"]
	systematics = ["nom", "JEC", "JER"]
	for year in years:
		for systematic in systematics:
			hadd_samples(year,systematic)