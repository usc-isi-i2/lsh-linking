import json
import re


def extract_place(filename):
	fp = open(filename)
	outfp = open('data.txt', 'w+')
	lines = [line.strip() for line in fp]
	pattern = re.compile('<([^<>]+)>')
	sss = [0, 0]
	for i in xrange(1, len(lines)-1):
		elements = pattern.findall(lines[i])
		# print elements
		if (len(elements) == 3):
			label = elements[1].strip().split('/')
			label = label[len(label)-1]
			if (label == 'birthPlace'):
				url = elements[0].strip()
				placeUrlElem = elements[2].strip().split('/')
				place = placeUrlElem[len(placeUrlElem)-1].replace('_', ' ')
				outfp.write(url + ' --- 0 --- ' + place + '\n')
			if (label == 'deathPlace'):
				url = elements[0].strip()
				placeUrlElem = elements[2].strip().split('/')
				place = placeUrlElem[len(placeUrlElem)-1].replace('_', ' ')
				outfp.write(url + ' --- 1 --- ' + place + '\n')
		sss[0] += 1
		sss[1] += 1
		if (sss[0] == 1000):
			sss[0] = 0
			print sss[1]
	fp.close()


def place_data_2json(filename):
	res = {}
	fp = open(filename)
	sss = [0, 0]
	lines = [line.strip().split(' --- ') for line in fp]
	for line in lines:
		assert(len(line) == 3)
		mark = int(line[1])
		url = line[0].strip().lower()
		place = line[2].strip().lower()
		if not url in res.keys():
			res[url] = ['', '']
		if (res[url][mark] == ''):
			res[url][mark] += place
		else:
			res[url][mark] += ', ' + place
		sss[0] += 1
		sss[1] += 1
		if (sss[0] == 1000):
			sss[0] = 0
			print sss[1]
	outfp = open('place.json', 'w+')
	json.dump(res, outfp)
	outfp.close()
	fp.close()


if __name__ == '__main__':
	# extract_place('persondata_en.nt')
	# place_data_2json('data.txt')
	print 'extract place data'
