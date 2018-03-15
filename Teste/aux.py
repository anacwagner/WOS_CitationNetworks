import json
import csv

import numpy as np
import pandas as pd


def allJournals(year_list):
	'''
		Extract journals information from json files (WoS). 

		INPUT:
			year_list: list of years

		OUTPUT:
			journals: dictionary
	'''

	journals = {}

	for year in year_list:
		with open('journals/' + str(year) + '.json') as json_data:
			file = json.load(json_data)

		for i in file['data']:
			if i['journalTitle'] not in list(journals.keys()):

				journals[i['journalTitle']] = {
				'year': [i['year']],
				'impact_factor': [i['journalImpactFactor']],
				'eigen_factor': [i['normEigenFactor']]
				}

			else:
				journals[i['journalTitle']]['year'].append(i['year'])
				journals[i['journalTitle']]['impact_factor'].append(i['journalImpactFactor'])
				journals[i['journalTitle']]['eigen_factor'].append(i['normEigenFactor'])

	return journals


def journalsMetrics(journals_dic, metric, year_list):
	'''
		Extract metrics from journals.

		INPUT: 
			journals_dic: dictionary with all journals informations
			metric: 'impact_factor' or 'eigen_factor'
			year_list: list of years

		OUTPUT:
			df: data frame with metric informations
	'''

	df = pd.DataFrame(columns = ['TITLE'] + [str(year) for year in year_list])

	k = 0
	for i in journals_dic:
		df.loc[k+1] = [i] + [0 for year in year_list]
		k = k + 1

	for i in range(len(df)):
		values = list(journals_dic.values())[i]

		j = 0
		for year in values['year']:
			df[str(year)][i+1] = values[metric][j]
			j = j + 1

	return df