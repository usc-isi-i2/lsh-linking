# -*- coding: utf-8 -*-  
from simhash_index import Simhash, SimhashIndex
import os, time
import os.path


def write_to_disk(index):
	for (k, v) in index.bucket.items():
		filename = 'data/'+str(k)[0:2]
		filename = filename.replace(':', '')
		file_object = open(filename, 'a+')
		file_object.write('<index>'+str(k)+'</index>\n')
		for item in v:
			file_object.write(item)
			file_object.write('\n')
		file_object.close()


def index_to_disk(data, field):
    objs = [(str(k), Simhash(v[field])) for k, v in data.items()]
    index = SimhashIndex(objs)
    write_to_disk(index)


def read_from_disk(path):
	data_dict = {}
	key = ''

	time1 = time.time()
 	for parent, dirnames, filenames in os.walk(path):
 		count = 0
 		record = 0
 		for filename in filenames:
 			file_object = open(path+'/'+filename)
 			try:
 				raw_data = file_object.readlines()
 				for item in raw_data:
 					item  = item.replace('\n', '')
 					if item.find('<index>') != -1:
 						key = item.replace('<index>', '').replace('</index>', '')
 						data_dict.setdefault(key, set())
 					else:
 						data_dict[key].add(item)
 						record += 1
 			finally:
 				file_object.close()

 			count += 1
 			print count, filename, record

 	time2 = time.time()
 	print time2 - time1
 	return data_dict


def disk_to_index(data):
	index = SimhashIndex()
	index.read(data)
	return index