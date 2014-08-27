# -*- coding: utf-8 -*-  
from simhash_disk import *
import time


def index_saam_data(filename, slice = -1, field = 'info'):
	time1 = time.time()
	count = -1
	data_list = []
	data_dict = {}

	file_object = open(filename)

	raw_data = file_object.readlines()

	for line in raw_data:
		data_list = line.replace('\n', '').rsplit('","')
		if count > -1:
			data_dict[count] = {}
			data_dict[count]['info'] = ''
			for data in data_list[1:]:
				data_dict[count]['info'] += data.replace('"', '').decode('UTF-8')
				data_dict[count]['info'] += ' '.decode('UTF-8')
		else:
			pass

		count += 1

	index_to_disk(data_dict, field)
	time2 = time.time()
	print time2 - time1