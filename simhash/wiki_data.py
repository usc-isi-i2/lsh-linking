# -*- coding: utf-8 -*-  
from simhash_disk import *
import time


def index_wiki_data(filename, slice = 10000, field = 'MENTION'):
    time1 = time.time()
    file_object = open(filename)
    count = -1
    tot = 0
    data_list = []
    data_dict = {}

    for line in file_object:
		data_list = line.rsplit('\t')
		if data_list[0] == 'URL':
			count += 1
			tot += 1
			if count < slice:
				data_dict[count] = {}
				data_dict[count]['URL'] = data_list[1].decode('UTF-8')
				data_dict[count]['MENTION'] = ''.decode('UTF-8')
				data_dict[count]['TOKEN'] = ''.decode('UTF-8')
			else:
				print tot
				count = 0
				data_dict = {}
				index_to_disk(data_dict, field)
		elif data_list[0] == 'MENTION':
			data_dict[count]['MENTION'] += data_list[1].decode('UTF-8')
			data_dict[count]['MENTION'] += ' '.decode('UTF-8')
		elif data_list[0] == 'TOKEN':
			data_dict[count]['TOKEN'] += data_list[1].decode('UTF-8')
			data_dict[count]['TOKEN'] += ' '.decode('UTF-8')
		else:
			pass
    time2 = time.time()
    print time2 - time1, tot