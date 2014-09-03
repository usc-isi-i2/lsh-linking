# -*- coding: utf-8 -*-  
from wiki_data import *
from saam_data import *
from dbpedia_data import *
from cora_data import *

if __name__ == '__main__':
    #data = process_data_json(load_data_json("cora.json"))
    #simhash_split(data, 'title')
    #index = disk_to_index(read_from_disk('./data'))

    #for (k, v) in index.bucket.items():
        #print k, v
   	#index_saam_data('saam-people.csv')
    #index_dbpedia_data('dbpedia.csv')
    #si = SimhashIndex()
    #res = si.query_from_disk('data', Simhash('Unknown photographer'))
    #print res
    index_wiki_data('data-00000-of-00010')