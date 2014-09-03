# -*- coding: utf-8 -*-  
from simhash_disk import *
import time, csv


def index_saam_data(filename, slice = -1, field = 'info'):
	time1 = time.time()
	count = 0
	data_dict = {}

	raw_data = csv.reader(file(filename, 'rb'))

	for line in raw_data:
		data_dict[count] = {}
		data_dict[count]['info'] = ''

		for data in line[1:2]:
			data_dict[count]['info'] += data.lstrip().rstrip().decode('UTF-8')

		count += 1
	index_to_disk(data_dict, field)
	time2 = time.time()
	print time2 - time1