# -*- coding: utf-8 -*-  
from simhash_disk import *
import time, csv


def index_dbpedia_data(filename, slice = 10000, field = 'info'):
	time1 = time.time()
	count = 0
	tot = 0
	data_dict = {}

	raw_data = csv.reader(file(filename, 'rb'))	

	for line in raw_data:
		data_dict[tot] = {}
		data_dict[tot]['info'] = ''
		try:
			if line[-2] == '':
				data_dict[tot]['info'] += line[-3].lstrip().rstrip().decode('UTF-8')
			else:
				data_dict[tot]['info'] += line[-2].lstrip().rstrip().decode('UTF-8')
		except:
			print tot
		count += 1
		tot += 1

		if count < slice:
			pass
		else:
			index_to_disk(data_dict, field)
			count = 0
			data_dict = {}
			time2 = time.time()
			print time2 - time1, tot

	index_to_disk(data_dict, field)
	time2 = time.time()
	print time2 - time1, tot