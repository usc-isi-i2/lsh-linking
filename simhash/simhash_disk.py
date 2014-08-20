# -*- coding: utf-8 -*-  
from simhash_index import Simhash, SimhashIndex


def write_to_disk(index):
	for (k, v) in index.bucket.items():
		filename = 'data/' + str(k).replace(":", "_")
		file_object = open(filename, 'a+')
		for item in v:
			file_object.write(item)
		file_object.close()


def index_to_disk(data, field):
    objs = [(str(k), Simhash(v[field])) for k, v in data.items()]
    index = SimhashIndex(objs)

    write_to_disk(index)


