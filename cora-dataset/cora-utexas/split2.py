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
		persons_str = record[u'persons'].encode('UTF-8')
		split_name = {}

		persons_str = persons_str.replace(":", "")
		persons_str = persons_str + '#'
		#name_test = 'cesa-bianchi, n., freund, y., haussler, d., helmbold, d. p., schapire, r. e., & warmuth, m. k.#'
		pattern = re.compile(r'(([a-z]|\-){2,})\,((\s?[a-z]\.)+)(\,|\#|(\s(\&|and)))')
		persons_str = pattern.sub(r'\3\1,', persons_str)
		persons_str = persons_str.replace("#", "")

		if persons_str.find(";") != -1:
			split_name = persons_str.replace("and", "").replace("&", "").rsplit(";")
		elif persons_str.find(".,") != -1:
			split_name = persons_str.replace(", and", ", ").replace("and", ".,").replace(", &", ", ").replace("&", ".,").rsplit(".,")
		elif persons_str.find(" and ") != -1:
			if persons_str.find(". and") !=-1:
				split_name = persons_str.replace(". and", ". ").rsplit(".")
			elif persons_str.find(", and") !=-1:
				split_name = persons_str.replace(", and", ", ").rsplit(",")
			else:
				split_name = persons_str.replace(" and ", " ,").rsplit(",")
		elif persons_str.find(" & ") != -1:
			if persons_str.find(". &") !=-1:
				split_name = persons_str.replace(". &", ". ").rsplit(".")
			elif persons_str.find(", &") !=-1:
				split_name = persons_str.replace(", &", ", ").rsplit(",")
			else:
				split_name = persons_str.replace(" & ", " ,").rsplit(",")
		else:
			split_name = persons_str.rsplit(",")

		#pattern = re.compile(r'([a-z]\-)+\s([a-z]\-)+|[a-z].\s([a-z]\-)+|[a-z].\s[a-z].\s([a-z]\-)+|')
		#persons_str = pattern
				


		'''elif persons_str.find(".,") != -1:
			pattern = re.compile(r'(\,\s[a-z].)(\,)')
			persons_str = pattern.sub(r'\1;', persons_str)
			split_name = persons_str.replace(",", ";").replace("and", "").replace("&", "").rsplit(";")'''

		for name in split_name:
			save_str = name.lstrip().rstrip()
			if save_str != "":
				file_object.write("<")
				file_object.write(save_str)
				file_object.write("> ")
		file_object.write("\n")

	file_object.close()

if __name__ =='__main__':
	split_person(load_json("cora.txt-people.json"))
	'''name_test = 'a. ehrenfeucht, d. haussler, m. kearns, and l. valiant.#'
	pattern = re.compile(r'(([a-z]|\-){2,})\,((\s?[a-z]{1}.)+(\,|\#))')
	persons_str = pattern.sub(r'\1.\3', name_test)
	print persons_str'''