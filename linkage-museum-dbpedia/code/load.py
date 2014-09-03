import csv
import codecs
# -*- encoding: utf-8 -*-
import unicodedata
import json
import re
import time

# load dbpedia dataset content
def load_dbpedia(filename):
	res = []
	with open(filename, 'rb') as fp:
		content = csv.reader(fp)
		flag = 0
		for line in content:
			if (flag == 0):
				flag = 1
				continue
			tmp = list(line)
			for t in tmp:
				try:
					tt = t.decode('utf-8')
				except:
					continue
			flag = True
			i = len(tmp) - 1
			while ((i > 5) and (tmp[i] == '')):
				del tmp[i]
				i -= 1
			# bug fix
			if (len(tmp) > 6):
				for i in xrange(1, len(tmp)-5):
					tmp[0] += tmp[i]
				for i in xrange(1, len(tmp)-5):
					tmp.remove(tmp[i])
			try:
				assert (len(tmp) == 6), 'error: [load_dbpedia] incompatible'
			except:
				print tmp
			res.append(tmp)
	return res


# def load_dbpedia(filename):
# 	res = []
# 	place_data = load_place_data('place.txt')
# 	newfp = open('dbpedia-place.csv', 'wb')
# 	writer = csv.writer(newfp)
# 	writer.writerow(['person', 'birthDate', 'deathDate', 'name', 'birthPlace', 'deathPlace'])
# 	sss = [0, 0]
# 	timemark = time.time()
# 	with open(filename, 'rb') as fp:
# 		content = csv.reader(fp)
# 		flag = 0
# 		for line in content:
# 			if (flag == 0):
# 				flag = 1
# 				continue
# 			tmp = list(line)
# 			for t in tmp:
# 				try:
# 					tt = t.decode('utf-8')
# 				except:
# 					continue
# 			flag = True
# 			i = len(tmp) - 1
# 			while (tmp[i] == ''):
# 				del tmp[i]
# 				i -= 1
# 			# bug fix
# 			if (len(tmp) > 4):
# 				for i in xrange(1, len(tmp)-3):
# 					tmp[0] += tmp[i]
# 				for i in xrange(1, len(tmp)-3):
# 					tmp.remove(tmp[i])
# 			if not tmp[0].strip().lower() in place_data.keys():
# 				tmp += ['', '']
# 			else:
# 				tmp += place_data[tmp[0].strip().lower()]
# 				# print tmp
# 			try:
# 				assert (len(tmp) == 6), 'error: [load_dbpedia] incompatible'
# 				# assert (len(tmp) == 4), 'error: [load_dbpedia] incompatible'
# 				writer.writerow(tmp)
# 			except:
# 				print tmp
# 			res.append(tmp)
# 			sss[0] += 1
# 			sss[1] += 1
# 			if (sss[0] == 1000):
# 				# newfp.close()
# 				# return res
# 				sss[0] = 0
# 				print str(sss[1]) + '---' + str(time.time()-timemark)
# 				timemark = time.time()
# 	newfp.close()
# 	return res


# load museum dataset content
def load_museum(filename):
	res = []
	with open(filename, 'rb') as fp:
		content = csv.reader(fp)
		flag = 0
		for line in content:
			if (flag == 0):
				flag = 1
				continue
			tmp = list(line)
			res.append(tmp)


# load ground truth file starting with a
def load_groundtruth_a(filename):
	res = {}
	with open(filename, 'rb') as fp:
		content = csv.reader(fp)
		flag = 0
		for line in content:
			if (flag == 0):
				flag = 1
				continue
			tmp = list(line)
			if (tmp[5].strip() == 'same') or (tmp[5].strip() == 'not same'):
				pattern = re.compile('\d+')
				pid = pattern.findall(tmp[0].strip())[0]
				url = tmp[2].strip()
				if (url.strip() != ''):
					res[pid] = url
	return res

# reconstruct a dbpedia file
# backup function, not in use
def write_dbpedia(data):
	fp = open('dbpedia_new.csv', 'wb')
	writer = csv.writer(fp)
	writer.writerow(['person', 'birthDate', 'deathDate', 'name'])
	res = []
	for rec in data:
		flag = True
		for dim in rec:
			try:
				tmp = dim.decode('utf-8')
			except:
				flag = False
				break
		if not flag:
			continue
		res.append(tuple(rec))
	writer.writerows(res)
	fp.close()

# load place data
# (we don't need this anymore)
def load_place_data(filename):
	fp = open(filename)
	data = {}
	lines = [line.strip().split('-+-') for line in fp]
	count = 0
	for line in lines:
		try:
			assert (len(line) == 3), 'error: [load_place_data]'
		except:
			count += 1
			print line
			continue
			# assert (len(line) == 3), 'error: [load_place_data]'
		data[line[0]] = [line[1].strip(), line[2].strip()]
	print count
	print len(data)
	print type(data)
	return data



if __name__ == '__main__':
	print 'load files'
