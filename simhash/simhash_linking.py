# -*- coding: utf-8 -*-  
from simhash_index import Simhash, SimhashIndex


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

if __name__ == '__main__':
    data = process_data(load_data("cora_org.txt"))
    data_dict = {}

    index = 1;
    for record in data:
        data_dict[index] = record[1]
        index = index + 1

    objs = [(str(k), Simhash(v)) for k, v in data_dict.items()]
    index = SimhashIndex(objs)

    s1 = Simhash(data_dict[34])
    result = index.get_near_dups(s1)

    print result

    for i in result:
        print data_dict[int(i)]