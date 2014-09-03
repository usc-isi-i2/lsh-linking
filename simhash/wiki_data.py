# -*- coding: utf-8 -*-  
from simhash_disk import *
import time


def index_wiki_data(filename, slice = 10000, field = 'TOKEN'):
    time1 = time.time()
    file_object = open(filename)
    tot = 0
    data_list = []
    data_dict = {}

    for line in file_object:
		data_list = line.rsplit('\t')
		if data_list[0] == 'URL':
			if tot%slice == 0 and tot>0:
				index_to_disk(data_dict, field)
				data_dict = {}
				time2 = time.time()
				print time2 - time1, tot
			else:
				pass
			tot += 1
			data_dict[tot] = {}
			data_dict[tot]['URL'] = data_list[1].decode('UTF-8')
			data_dict[tot]['MENTION'] = ''.decode('UTF-8')
			data_dict[tot]['TOKEN'] = ''.decode('UTF-8')

		elif data_list[0] == 'MENTION':
			data_dict[tot]['MENTION'] += data_list[1].decode('UTF-8')
			data_dict[tot]['MENTION'] += ' '.decode('UTF-8')
		elif data_list[0] == 'TOKEN':
			data_dict[tot]['TOKEN'] += data_list[1].decode('UTF-8')
			data_dict[tot]['TOKEN'] += ' '.decode('UTF-8')
		else:
			pass
			
	index_to_disk(data_dict, field)
	time2 = time.time()
	print time2 - time1, tot