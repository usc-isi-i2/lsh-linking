# -*- coding: utf-8 -*-  
from simhash_disk import *
import time


def index_dbpedia_data(filename, slice = 10000, field = 'info'):
	time1 = time.time()
	file_object = open(filename)
	count = -1
	tot = 0
	data_list = []
	data_dict = {}

	raw_data = file_object.readlines()

	for line in raw_data:
		data_list = line.replace('\n', '').rsplit(',')
		if count < slice:
			if count > -1:
				data_dict[count] = {}
				data_dict[count]['info'] = ''
				for data in data_list[1:]:
					data_dict[count]['info'] += data.decode('UTF-8')
					data_dict[count]['info'] += ' '.decode('UTF-8')
			else:
				pass
			count += 1
			tot += 1
		else:
			#index_to_disk(data_dict, field)
			count = 0
			data_dict = {}
			time2 = time.time()
			print time2 - time1, tot


	index_to_disk(data_dict, field)
	time2 = time.time()
	print time2 - time1, tot