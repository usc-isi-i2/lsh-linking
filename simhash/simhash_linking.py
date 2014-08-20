# -*- coding: utf-8 -*-  
from wiki_data import *
import json


def load_data(filename):
    file_object = open(filename)
    try:
        raw_data = file_object.readlines()
    finally:
        file_object.close()

    return raw_data


def process_data(data):
    data_list = []
    for record in data:
        data_list.append(record.rsplit('\t'))
    return data_list


def load_data_json(filename):
    file_object = open(filename)
    try:
         raw_data = file_object.read()
    finally:
         file_object.close()

    return json.loads(raw_data)


def process_data_json(data):
    data_dict = {}
    for (k0, v0) in data.items():
        data_dict[int(k0)] = {}
        for (k1, v1) in v0.items():
            data_dict[int(k0)][k1.encode('UTF-8')] = v1.encode('UTF-8')

    return data_dict
    

def simhash_split(data, field):
    time1 = time.time()
    objs = [(str(k), Simhash(v[field])) for k, v in data.items()]
    index = SimhashIndex(objs)
    time2 = time.time()
    print time2 - time1
    for i in xrange(1294):
        result = index.get_near_dups(Simhash(data[i]['title']))
    time3 = time.time()
    print time3-time2

    write_to_disk(index)


if __name__ == '__main__':
    #data = process_data_json(load_data_json("cora.json"))
    #simhash_split(data, 'title')

    index_wiki_data('data-00000-of-00010')