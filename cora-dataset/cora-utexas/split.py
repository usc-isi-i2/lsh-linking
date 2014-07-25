# -*- coding: utf-8 -*- 
import re
import json
def load_json(filename):	
	file_object = open(filename)
	try:
	     raw_data = file_object.read()
	finally:
	     file_object.close()

	return json.loads(raw_data)


def split_person(data):
	count = 0;
	file_object = open("split_name.txt", 'w')

	for record in data:
		persons_str = record[u'persons'].encode('UTF-8')[:-1]
		split_name = {}

		if persons_str.find(";") != -1:
			split_name = persons_str.replace("and", "").replace("&", "").rsplit(";")
		elif persons_str.find(".,") != -1:
			split_name = persons_str.replace(", and", ", ").replace("and", ".,").replace(", &", ", ").replace("&", ".,").rsplit(".,")
		elif persons_str.find("and") != -1:
			if persons_str.find(". and") !=-1:
				split_name = persons_str.replace(". and", ". ").rsplit(".")
			elif persons_str.find(", and") !=-1:
				split_name = persons_str.replace(", and", ", ").rsplit(",")
			else:
				split_name = persons_str.rsplit("and")
		elif persons_str.find("&") != -1:
			if persons_str.find(". &") !=-1:
				split_name = persons_str.replace(". &", ". ").rsplit(".")
			elif persons_str.find(", &") !=-1:
				split_name = persons_str.replace(", &", ", ").rsplit(",")
			else:
				split_name = persons_str.rsplit("&")
		elif persons_str.find(".:") != -1:
			split_name = persons_str.rsplit(",")
		else:
			split_name = persons_str.rsplit(",")

		if split_name == {}:
			count=count+1
			print persons_str
		else:
			for name in split_name:
				file_object.write("<")
				file_object.write(name.lstrip().rstrip())
				file_object.write("> ")
			file_object.write("\n")

	file_object.close()
	print count

if __name__ =='__main__':
	split_person(load_json("cora.txt-people.json"))